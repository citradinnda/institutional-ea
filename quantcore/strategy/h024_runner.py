from __future__ import annotations

"""H024 bridge adapter.

This module converts H024 pullback-continuation signals into an H017-compatible
risk-intent object through the existing H020 sizing contract.

It does not run real-data validation, execute fills, approve demo trading, or
approve live trading.
"""

from dataclasses import dataclass

import pandas as pd

from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h020 import H020SizingConfig, generate_h020_intent_panel
from quantcore.strategy.h024 import H024SignalConfig, generate_h024_signals


_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class H024BridgeConfig:
    signal_config: H024SignalConfig = H024SignalConfig()
    sizing_config: H020SizingConfig = H020SizingConfig()
    signed_risk_fraction: float = 0.01
    stop_atr_multiple: float = 2.0
    atr_window: int = 14
    starting_equity_usd: float = 10_000.0


def run_h024_bridge_shim(
    *,
    usdjpy_ohlcv: pd.DataFrame,
    xauusd_ohlcv: pd.DataFrame,
    config: H024BridgeConfig | None = None,
) -> H017Result:
    """Run H024 signals and return an H017-compatible bridge shim.

    Signal timing follows the existing bridge convention:
    - H024 decides at H4 timestamp t.
    - The later event bridge opens at t+1.
    - Stops are generated at decision time from ATR geometry.
    - H020 sizing suppresses invalid/tiny/over-levered intents.
    """

    cfg = config or H024BridgeConfig()
    _validate_h024_bridge_config(cfg)

    h4_by_symbol = {
        "USDJPY": _require_h4_frame(usdjpy_ohlcv, "USDJPY"),
        "XAUUSD": _require_h4_frame(xauusd_ohlcv, "XAUUSD"),
    }
    _require_matching_index(h4_by_symbol)

    index = h4_by_symbol["USDJPY"].index
    positions = pd.DataFrame(0.0, index=index, columns=_SYMBOLS)
    signals = pd.DataFrame(0.0, index=index, columns=_SYMBOLS)
    stops_long = pd.DataFrame(float("nan"), index=index, columns=_SYMBOLS)
    stops_short = pd.DataFrame(float("nan"), index=index, columns=_SYMBOLS)

    for symbol, frame in h4_by_symbol.items():
        raw_signals = generate_h024_signals(frame, config=cfg.signal_config)
        signed_signals = raw_signals.astype(float) * float(cfg.signed_risk_fraction)
        signals[symbol] = signed_signals
        positions[symbol] = signed_signals

        atr = _wilder_atr(frame, cfg.atr_window)
        stop_distance = atr * float(cfg.stop_atr_multiple)
        stops_long[symbol] = frame["close"].astype(float) - stop_distance
        stops_short[symbol] = frame["close"].astype(float) + stop_distance

    panels = generate_h020_intent_panel(
        positions=positions,
        stops_long=stops_long,
        stops_short=stops_short,
        h4_by_symbol=h4_by_symbol,
        equity_usd=cfg.starting_equity_usd,
        config=cfg.sizing_config,
    )

    sized_positions = pd.DataFrame(0.0, index=index, columns=_SYMBOLS)
    for panel in panels:
        for symbol, intent in panel.intents.items():
            if not intent.suppressed:
                sized_positions.at[panel.decision_time, symbol] = (
                    intent.final_signed_risk_fraction
                )

    multipliers = pd.DataFrame(1.0, index=index, columns=_SYMBOLS)
    heat = pd.Series(0.0, index=index)

    return H017Result(
        positions=sized_positions,
        stops_long=stops_long,
        stops_short=stops_short,
        signals=signals,
        vol_multipliers=multipliers,
        heat_multipliers=multipliers,
        heat_pre=heat,
        heat_post=heat,
        heat_binding=pd.Series(False, index=index),
    )


def _validate_h024_bridge_config(config: H024BridgeConfig) -> None:
    if config.signed_risk_fraction <= 0.0:
        raise ValueError("signed_risk_fraction must be positive")
    if config.stop_atr_multiple <= 0.0:
        raise ValueError("stop_atr_multiple must be positive")
    if config.atr_window < 2:
        raise ValueError("atr_window must be >= 2")
    if config.starting_equity_usd <= 0.0:
        raise ValueError("starting_equity_usd must be positive")


def _require_h4_frame(frame: pd.DataFrame, symbol: str) -> pd.DataFrame:
    required = ("open", "high", "low", "close")
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"{symbol} missing required OHLC columns: {missing}")
    if not isinstance(frame.index, pd.DatetimeIndex):
        raise ValueError(f"{symbol} must use a DatetimeIndex")
    if frame.index.has_duplicates:
        raise ValueError(f"{symbol} index must be unique")
    if not frame.index.is_monotonic_increasing:
        raise ValueError(f"{symbol} index must be monotonic increasing")
    return frame.copy()


def _require_matching_index(h4_by_symbol: dict[str, pd.DataFrame]) -> None:
    reference = h4_by_symbol["USDJPY"].index
    for symbol, frame in h4_by_symbol.items():
        if not frame.index.equals(reference):
            raise ValueError(f"{symbol} index must match USDJPY index")


def _wilder_atr(frame: pd.DataFrame, window: int) -> pd.Series:
    high = frame["high"].astype(float)
    low = frame["low"].astype(float)
    close = frame["close"].astype(float)

    previous_close = close.shift(1)
    true_range = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = pd.Series(index=frame.index, dtype="float64")
    if len(true_range) < window:
        return atr

    atr.iloc[window - 1] = true_range.iloc[:window].mean()
    for index in range(window, len(true_range)):
        atr.iloc[index] = ((atr.iloc[index - 1] * (window - 1)) + true_range.iloc[index]) / window

    return atr
