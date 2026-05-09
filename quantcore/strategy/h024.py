from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_OHLC_COLUMNS = ("open", "high", "low", "close")


@dataclass(frozen=True)
class H024SignalConfig:
    """Configuration for H024 regime-conditioned pullback continuation signals."""

    slow_window: int = 5
    slope_lag: int = 2
    atr_window: int = 3
    pullback_window: int = 3
    min_pullback_atr: float = 0.25
    max_pullback_atr: float = 3.00
    min_slope_atr: float = 0.05


def _validate_config(config: H024SignalConfig) -> None:
    if config.slow_window < 2:
        raise ValueError("slow_window must be >= 2")
    if config.slope_lag < 1:
        raise ValueError("slope_lag must be >= 1")
    if config.atr_window < 2:
        raise ValueError("atr_window must be >= 2")
    if config.pullback_window < 1:
        raise ValueError("pullback_window must be >= 1")
    if config.min_pullback_atr < 0:
        raise ValueError("min_pullback_atr must be >= 0")
    if config.max_pullback_atr < config.min_pullback_atr:
        raise ValueError("max_pullback_atr must be >= min_pullback_atr")
    if config.min_slope_atr < 0:
        raise ValueError("min_slope_atr must be >= 0")


def _require_ohlc(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_OHLC_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required OHLC columns: {missing}")


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


def generate_h024_signals(
    frame: pd.DataFrame,
    config: H024SignalConfig | None = None,
) -> pd.Series:
    """Generate H024 directional intents.

    Output values:
    - 1 for long pullback-continuation intent
    - -1 for short pullback-continuation intent
    - 0 for flat/no intent

    The signal is evaluated at the close of each H4 bar and is intended to be
    consumed by later bridge logic that opens on the next H4 bar. This function
    does not size trades, set stops, approve execution, or touch real data.
    """

    resolved_config = config or H024SignalConfig()
    _validate_config(resolved_config)
    _require_ohlc(frame)

    if frame.empty:
        return pd.Series(index=frame.index, dtype="int64", name="h024_signal")

    open_ = frame["open"].astype(float)
    high = frame["high"].astype(float)
    low = frame["low"].astype(float)
    close = frame["close"].astype(float)

    slow_ma = close.rolling(
        resolved_config.slow_window,
        min_periods=resolved_config.slow_window,
    ).mean()
    atr = _wilder_atr(frame, resolved_config.atr_window)

    slope = slow_ma - slow_ma.shift(resolved_config.slope_lag)
    slope_threshold = atr * resolved_config.min_slope_atr

    trend_up = (close > slow_ma) & (slope > slope_threshold)
    trend_down = (close < slow_ma) & (slope < -slope_threshold)

    previous_bearish = close.shift(1) < open_.shift(1)
    previous_bullish = close.shift(1) > open_.shift(1)

    recent_high_before_signal = high.shift(1).rolling(
        resolved_config.pullback_window,
        min_periods=resolved_config.pullback_window,
    ).max()
    recent_low_before_signal = low.shift(1).rolling(
        resolved_config.pullback_window,
        min_periods=resolved_config.pullback_window,
    ).min()

    long_pullback_depth_atr = (recent_high_before_signal - low.shift(1)) / atr.shift(1)
    short_pullback_depth_atr = (high.shift(1) - recent_low_before_signal) / atr.shift(1)

    long_pullback_ok = long_pullback_depth_atr.between(
        resolved_config.min_pullback_atr,
        resolved_config.max_pullback_atr,
        inclusive="both",
    )
    short_pullback_ok = short_pullback_depth_atr.between(
        resolved_config.min_pullback_atr,
        resolved_config.max_pullback_atr,
        inclusive="both",
    )

    long_resumption = close > high.shift(1)
    short_resumption = close < low.shift(1)

    long_signal = trend_up & previous_bearish & long_pullback_ok & long_resumption
    short_signal = trend_down & previous_bullish & short_pullback_ok & short_resumption

    signals = pd.Series(0, index=frame.index, dtype="int64", name="h024_signal")
    signals.loc[long_signal.fillna(False)] = 1
    signals.loc[short_signal.fillna(False)] = -1

    return signals
