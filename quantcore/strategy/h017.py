from __future__ import annotations

"""Phase 2.4: H017 strategy integration.

Glues Phase 2.1-2.3 components into a single strategy producing per-bar
position sizes (as fraction of equity at risk) for USDJPY + XAUUSD.

Pipeline per symbol:
    OHLCV -> ATR -> chandelier stops + vol-target size -> signal
Then portfolio-level:
    signals + close-to-close returns -> heat governor -> multipliers
Final:
    position = signal * per_trade_risk * vol_mult * heat_mult

Q1-Q5 design decisions (locked):
    Q1: Inner-join on timestamps; heat governor needs aligned panels.
    Q2: Close-to-close pct_change for both vol_target input and
        heat-governor correlation input. Single source of truth for
        each symbol's returns.
    Q3: Position = fraction of equity at risk; Phase 3 backtest converts
        to lots using stop distance + symbol contract spec.
    Q4: Output desired position; backtest engine handles fill mechanics.
    Q5: H017Config.default() bakes in H017 reference settings.

Indicator-binding notes (read before changing kwargs here):
    - chandelier_exit signature: (df, atr, multiplier, lookback, side).
      Called TWICE per symbol (side='long' then side='short') because
      it returns a Series per side, not a DataFrame.
    - vol_target_size signature: (returns, target_vol_annual, lookback,
      periods_per_year, max_leverage). Takes a Series of returns, NOT
      a DataFrame.
    - average_true_range signature: (df, window).
    - periods_per_year defaults to 1512 here (H4 bars: 6 per day * 252
      trading days). vol_target's library default is 252 which would
      under-annualize H4 vol; we override it explicitly.
"""

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from quantcore.indicators import (
    average_true_range,
    chandelier_exit,
    vol_target_size,
)
from quantcore.strategy.heat_governor import HeatConfig, heat_governor
from quantcore.strategy.signals import (
    SignalConfig,
    usdjpy_trend_signal,
    xauusd_trend_signal,
)


def _default_usdjpy_signal() -> SignalConfig:
    """USDJPY default: 20-bar Donchian, no ATR floor."""
    return SignalConfig(lookback=20, min_atr_pct=None, atr_col="atr14")


def _default_xauusd_signal() -> SignalConfig:
    """XAUUSD default: 20-bar Donchian + 0.3% ATR-percent floor."""
    return SignalConfig(lookback=20, min_atr_pct=0.003, atr_col="atr14")


@dataclass(frozen=True)
class H017Config:
    """H017 strategy configuration.

    The default factory bakes in the H017 reference settings derived from
    the H011-H016 graveyard learnings. Override individual fields via
    dataclasses.replace or by passing a fully custom instance.

    Note on atr_window vs signal atr_col coupling:
        The XAUUSD signal references an ATR column by name. The default
        config uses 'atr14' on both the indicator side and the signal
        side. If you change atr_window, also update xauusd_signal.atr_col
        to match (e.g. 'atr20' for atr_window=20).

    Note on periods_per_year:
        Default 1512 = 6 H4 bars per day * 252 trading days. This is the
        annualization factor used by vol_target_size to convert per-bar
        realized vol to annualized vol before comparing to target_vol.
        For daily bars, override to 252; for hourly, 6*24*252 = 6048.
    """

    atr_window: int = 14
    chandelier_mult: float = 3.0
    chandelier_lookback: int = 22
    vol_target: float = 0.10
    vol_lookback: int = 20
    vol_max_leverage: float = 3.0
    periods_per_year: int = 1512
    usdjpy_signal: SignalConfig = field(default_factory=_default_usdjpy_signal)
    xauusd_signal: SignalConfig = field(default_factory=_default_xauusd_signal)
    heat: HeatConfig = field(default_factory=HeatConfig)

    @classmethod
    def default(cls) -> H017Config:
        """Reference H017 configuration (the H016 + heat-governor fix)."""
        return cls()


@dataclass(frozen=True)
class H017Result:
    """Output of run_h017.

    Attributes:
        positions: DataFrame [bars x symbols] of final position size as
            signed fraction of equity at risk.
            E.g. +0.0075 = long 0.75% of equity at risk in this symbol.
        signals: Raw direction panel {-1, 0, +1, NaN}.
        stops_long: Chandelier long-side stop levels per symbol.
        stops_short: Chandelier short-side stop levels per symbol.
        vol_multipliers: Inverse-vol size multipliers per symbol.
        heat_multipliers: Correlation-aware risk-cap multipliers in [0,1].
        heat_pre: Pre-governor combined heat per bar.
        heat_post: Post-governor combined heat per bar.
        heat_binding: True where the heat cap was binding.
    """

    positions: pd.DataFrame
    signals: pd.DataFrame
    stops_long: pd.DataFrame
    stops_short: pd.DataFrame
    vol_multipliers: pd.DataFrame
    heat_multipliers: pd.DataFrame
    heat_pre: pd.Series
    heat_post: pd.Series
    heat_binding: pd.Series


def _validate_ohlcv(df: pd.DataFrame, name: str) -> None:
    """Defensive depth at integration boundary."""
    required = {"open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"{name} missing canonical columns: {sorted(missing)}. "
            "Expected lowercase open/high/low/close/volume."
        )
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{name}.index must be DatetimeIndex.")
    if df.index.has_duplicates:
        raise ValueError(f"{name}.index has duplicates.")
    if not df.index.is_monotonic_increasing:
        raise ValueError(f"{name}.index must be sorted ascending.")


def run_h017(
    usdjpy_ohlcv: pd.DataFrame,
    xauusd_ohlcv: pd.DataFrame,
    config: H017Config | None = None,
) -> H017Result:
    """Run the full H017 pipeline.

    Args:
        usdjpy_ohlcv: Canonical OHLCV frame for USDJPY.
        xauusd_ohlcv: Canonical OHLCV frame for XAUUSD.
        config: Optional H017Config; default is H017Config.default().

    Returns:
        H017Result with the final positions panel and all intermediate
        artefacts. All output frames/series are aligned to the
        inner-joined timestamp index.

    Raises:
        ValueError: if either OHLCV frame is malformed, or if the two
            frames have no overlapping timestamps.
    """
    if config is None:
        config = H017Config.default()

    _validate_ohlcv(usdjpy_ohlcv, "usdjpy_ohlcv")
    _validate_ohlcv(xauusd_ohlcv, "xauusd_ohlcv")

    # Q1: inner-join on timestamps.
    common_idx = usdjpy_ohlcv.index.intersection(xauusd_ohlcv.index)
    if len(common_idx) == 0:
        raise ValueError(
            "USDJPY and XAUUSD OHLCV frames have no overlapping timestamps. "
            "Cannot run portfolio-level strategy."
        )

    jpy = usdjpy_ohlcv.loc[common_idx].copy()
    xau = xauusd_ohlcv.loc[common_idx].copy()

    atr_col = f"atr{config.atr_window}"

    # Per-symbol ATR. Attach to the frame for signal modules that
    # reference an ATR column by name (XAUUSD's volatility floor).
    jpy[atr_col] = average_true_range(jpy, window=config.atr_window)
    xau[atr_col] = average_true_range(xau, window=config.atr_window)

    # Chandelier stops: one Series per (symbol, side). Four calls total.
    chand_jpy_long = chandelier_exit(
        jpy,
        atr=jpy[atr_col],
        multiplier=config.chandelier_mult,
        lookback=config.chandelier_lookback,
        side="long",
    )
    chand_jpy_short = chandelier_exit(
        jpy,
        atr=jpy[atr_col],
        multiplier=config.chandelier_mult,
        lookback=config.chandelier_lookback,
        side="short",
    )
    chand_xau_long = chandelier_exit(
        xau,
        atr=xau[atr_col],
        multiplier=config.chandelier_mult,
        lookback=config.chandelier_lookback,
        side="long",
    )
    chand_xau_short = chandelier_exit(
        xau,
        atr=xau[atr_col],
        multiplier=config.chandelier_mult,
        lookback=config.chandelier_lookback,
        side="short",
    )

    # Q2: close-to-close pct_change feeds BOTH vol_target_size and
    # the heat governor. Compute once per symbol.
    rets_jpy = jpy["close"].pct_change()
    rets_xau = xau["close"].pct_change()

    # Vol-target inverse-vol multipliers (takes Series of returns).
    vol_jpy = vol_target_size(
        rets_jpy,
        target_vol_annual=config.vol_target,
        lookback=config.vol_lookback,
        periods_per_year=config.periods_per_year,
        max_leverage=config.vol_max_leverage,
    )
    vol_xau = vol_target_size(
        rets_xau,
        target_vol_annual=config.vol_target,
        lookback=config.vol_lookback,
        periods_per_year=config.periods_per_year,
        max_leverage=config.vol_max_leverage,
    )

    # Per-symbol Donchian signals.
    sig_jpy = usdjpy_trend_signal(jpy, config.usdjpy_signal)
    sig_xau = xauusd_trend_signal(xau, config.xauusd_signal)

    signals_panel = pd.DataFrame(
        {"USDJPY": sig_jpy, "XAUUSD": sig_xau},
        index=common_idx,
    )
    returns_panel = pd.DataFrame(
        {"USDJPY": rets_jpy, "XAUUSD": rets_xau},
        index=common_idx,
    ).fillna(0.0)

    heat = heat_governor(signals_panel, returns_panel, config.heat)

    # Q3: position = signal * per_trade_risk * vol_mult * heat_mult.
    # NaN signals (warm-up) treated as 0 for position math; raw signals
    # panel preserves the NaN for diagnostic visibility.
    sig_clean = signals_panel.fillna(0.0).astype(float)
    vol_panel = pd.DataFrame(
        {"USDJPY": vol_jpy, "XAUUSD": vol_xau},
        index=common_idx,
    ).fillna(0.0)

    r = config.heat.per_trade_risk
    positions = sig_clean * r * vol_panel * heat.multipliers
    positions.columns = ["USDJPY", "XAUUSD"]

    stops_long = pd.DataFrame(
        {"USDJPY": chand_jpy_long, "XAUUSD": chand_xau_long},
        index=common_idx,
    )
    stops_short = pd.DataFrame(
        {"USDJPY": chand_jpy_short, "XAUUSD": chand_xau_short},
        index=common_idx,
    )

    return H017Result(
        positions=positions,
        signals=signals_panel,
        stops_long=stops_long,
        stops_short=stops_short,
        vol_multipliers=vol_panel,
        heat_multipliers=heat.multipliers,
        heat_pre=heat.portfolio_heat_pre,
        heat_post=heat.portfolio_heat_post,
        heat_binding=heat.binding,
    )