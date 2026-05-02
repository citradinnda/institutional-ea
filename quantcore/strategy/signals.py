from __future__ import annotations

"""Deterministic per-symbol trend-following signal generators.

Why Donchian breakout (not EMA crossover, not ML):
    - H006/H007 graveyard: ML chooses entries unreliably; deterministic
      rules manage risk. Signals here are the entry trigger only — the
      stop (chandelier, Phase 2.1b) and the size (vol-target, Phase 2.1b)
      are what produce edge.
    - Donchian (price breaking the prior N-bar extreme) is in the same
      mathematical family as the chandelier exit (highest-high - mult*ATR),
      so entries and exits are coherent.
    - Crisp on/off events (no parameter drift, no smoothing artefacts)
      make the signal bit-for-bit reproducible — a test invariant.

Convention (matches indicators/ modules):
    - Input: canonical OHLCV DataFrame (lowercase columns, UTC index).
    - Output: pd.Series[int8] in {-1, 0, +1}, aligned to df.index, named
      'signal'. Warm-up bars (first `lookback`) are NaN before dropna,
      and the series dtype is float64 if NaN is present, int8 after dropna.
    - The signal at bar t is computable from data available AT bar t's
      close — no look-ahead. The Donchian channel uses the PRIOR N bars
      (shifted by 1), so the breakout is judged against the channel that
      existed before bar t.

Hold-vs-flip semantics (Q5):
    - Signal is desired direction, not a trade list.
    - Between breakouts, the most recent direction is held.
    - When opposite breakout fires, direction flips on that bar.
    - Initial state before the first breakout is 0 (flat).
    - Whether the integration layer (Phase 2.4) acts on every flip or
      filters it through the heat governor is NOT this module's concern.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SignalConfig:
    """Configuration for a Donchian-breakout signal generator.

    Attributes:
        lookback: Number of PRIOR bars defining the Donchian channel.
            E.g. lookback=20 means break of the prior 20-bar high/low.
            Must be >= 2.
        min_atr_pct: Optional volatility floor as ATR / close. If set,
            breakouts where atr[t] / close[t] < min_atr_pct are suppressed
            (signal holds previous direction rather than triggering).
            None disables the filter. Used on XAUUSD to suppress dead-flat
            chop; not used on USDJPY by default.
        atr_col: Column name in the input DataFrame containing ATR values
            (only consulted when min_atr_pct is not None). The caller is
            responsible for computing ATR via quantcore.indicators and
            attaching it to the OHLCV frame before calling.
    """

    lookback: int = 20
    min_atr_pct: float | None = None
    atr_col: str = "atr14"

    def __post_init__(self) -> None:
        if self.lookback < 2:
            raise ValueError(
                f"lookback must be >= 2, got {self.lookback}. "
                "A 1-bar lookback is degenerate (channel = previous bar)."
            )
        if self.min_atr_pct is not None and self.min_atr_pct < 0:
            raise ValueError(
                f"min_atr_pct must be >= 0 or None, got {self.min_atr_pct}."
            )


def _validate_ohlcv(df: pd.DataFrame) -> None:
    """Re-validate canonical OHLCV convention at signal-module boundary.

    Why re-validate: defensive depth. The caller is supposed to pass
    canonical frames (per quantcore/data/loaders.ensure_canonical), but
    indicators/ also re-validates and we match that pattern.
    """
    required = {"open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"DataFrame missing required canonical columns: {sorted(missing)}. "
            "Expected lowercase open/high/low/close/volume."
        )
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(
            f"DataFrame index must be pd.DatetimeIndex, got {type(df.index).__name__}."
        )
    if df.index.has_duplicates:
        raise ValueError("DataFrame index has duplicates; deduplicate before signaling.")
    if not df.index.is_monotonic_increasing:
        raise ValueError("DataFrame index must be sorted ascending.")


def donchian_signal(df: pd.DataFrame, config: SignalConfig) -> pd.Series:
    """Generic Donchian-breakout signal engine.

    Long when close[t] > max(high[t-N..t-1]); short when
    close[t] < min(low[t-N..t-1]); else hold previous direction.

    The shared engine is exposed so per-symbol wrappers stay one-liners
    AND so tests can hit the engine directly without going through a
    symbol-specific wrapper.

    Args:
        df: Canonical OHLCV frame. If config.min_atr_pct is set, must
            also contain an ATR column (default name 'atr14').
        config: SignalConfig defining lookback and optional ATR floor.

    Returns:
        pd.Series named 'signal', dtype float64 (because warm-up bars
        are NaN), values in {-1.0, 0.0, +1.0, NaN}, aligned to df.index.
        Cast to int8 after dropna() if you want a compact integer series.
    """
    _validate_ohlcv(df)
    n = config.lookback

    if len(df) <= n:
        # Not enough bars to form even one channel. Return all-NaN.
        return pd.Series(np.nan, index=df.index, name="signal", dtype="float64")

    # Donchian channel uses the PRIOR n bars: shift by 1 so bar t's
    # channel is built from bars t-n .. t-1, never including bar t itself.
    prior_high = df["high"].shift(1).rolling(window=n, min_periods=n).max()
    prior_low = df["low"].shift(1).rolling(window=n, min_periods=n).min()

    close = df["close"]
    long_break = close > prior_high
    short_break = close < prior_low

    # Optional ATR-percent floor: suppress breakouts in dead-flat regimes.
    if config.min_atr_pct is not None:
        if config.atr_col not in df.columns:
            raise ValueError(
                f"min_atr_pct is set but column '{config.atr_col}' not in DataFrame. "
                "Compute ATR via quantcore.indicators.average_true_range and attach first."
            )
        atr = df[config.atr_col]
        atr_pct = atr / close
        # Bars where ATR is NaN (warm-up) or below floor: suppress trigger.
        suppress = atr_pct.isna() | (atr_pct < config.min_atr_pct)
        long_break = long_break & ~suppress
        short_break = short_break & ~suppress

    # Build raw event series: +1 on long break, -1 on short break, 0 else,
    # NaN during the lookback warm-up where the channel itself is NaN.
    raw = pd.Series(0.0, index=df.index, name="signal", dtype="float64")
    raw[long_break.fillna(False)] = 1.0
    raw[short_break.fillna(False)] = -1.0

    # Warm-up: bars where prior_high or prior_low is NaN have no channel,
    # so the signal is undefined. The first n bars (indices 0..n-1) are NaN.
    warmup_mask = prior_high.isna() | prior_low.isna()
    raw[warmup_mask] = np.nan

    # Hold-vs-flip semantics: between breakouts, hold the most recent
    # non-zero direction. Implemented by replacing 0s with NaN, forward-
    # filling, then putting back 0 only where forward-fill found nothing
    # (i.e. before the first ever breakout).
    held = raw.replace(0.0, np.nan).ffill()

    # Restore the warm-up NaNs (ffill would have propagated past them only
    # if there were any non-NaN values before them, which there aren't —
    # but be explicit for safety).
    held[warmup_mask] = np.nan

    # Pre-first-breakout bars (post warm-up, before any signal fired):
    # ffill leaves them NaN, but they should be 0 (flat, not undefined).
    post_warmup = ~warmup_mask
    pre_first_signal = post_warmup & held.isna()
    held[pre_first_signal] = 0.0

    held.name = "signal"
    return held


def usdjpy_trend_signal(
    df: pd.DataFrame,
    config: SignalConfig | None = None,
) -> pd.Series:
    """Donchian-breakout signal for USDJPY.

    Default: 20-bar lookback, no ATR floor. USDJPY trends are smoother
    than gold's, so the volatility-floor filter is unnecessary and would
    only delay valid entries.

    Args:
        df: Canonical OHLCV frame for USDJPY.
        config: Optional override. If None, uses SignalConfig(lookback=20).

    Returns:
        pd.Series named 'signal' in {-1, 0, +1, NaN}, aligned to df.index.
    """
    if config is None:
        config = SignalConfig(lookback=20, min_atr_pct=None)
    return donchian_signal(df, config)


def xauusd_trend_signal(
    df: pd.DataFrame,
    config: SignalConfig | None = None,
) -> pd.Series:
    """Donchian-breakout signal for XAUUSD with volatility floor.

    Default: 20-bar lookback + ATR-percent floor of 0.003 (0.3% of price).
    Gold has more chop and false-breakout cost than JPY, so we suppress
    breakouts when realized volatility is degenerate. Caller must attach
    an 'atr14' column (or override via config.atr_col) before calling.

    Args:
        df: Canonical OHLCV frame for XAUUSD with an ATR column attached.
        config: Optional override. If None, uses
            SignalConfig(lookback=20, min_atr_pct=0.003, atr_col='atr14').

    Returns:
        pd.Series named 'signal' in {-1, 0, +1, NaN}, aligned to df.index.
    """
    if config is None:
        config = SignalConfig(lookback=20, min_atr_pct=0.003, atr_col="atr14")
    return donchian_signal(df, config)