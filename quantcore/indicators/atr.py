"""
Average True Range (Wilder 1978).

WHY Wilder's smoothing (RMA) instead of a simple moving average: Wilder's
recursive moving average gives more weight to recent volatility while still
smoothing noise. This is the original ATR formulation and remains the
standard for live trading systems. Using SMA would produce a different
(smoother, more lagged) series that would not match MT5's iATR or
TradingView's ATR — making backtest-vs-live discrepancies very hard to
diagnose.

WHY first-bar TR = high - low: with no prior close, the |high - prev_close|
and |low - prev_close| components of true range are undefined. Using
high - low for bar 0 is the standard convention and matches MT5.

WHY warm-up returns NaN, not zero: a zero ATR is a valid reading (a doji-
like bar) and would silently corrupt downstream sizing logic if confused
with "indicator not yet ready". NaN forces callers to handle the warm-up
explicitly — same convention as pandas .rolling().

References:
    Wilder, J. W. (1978). New Concepts in Technical Trading Systems.
    Trend Research, Greensboro, NC.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

_REQUIRED_COLS: tuple[str, ...] = ("open", "high", "low", "close")


def average_true_range(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """
    Compute Wilder's Average True Range.

    Parameters
    ----------
    df : pd.DataFrame
        Canonical OHLCV bars: lowercase columns 'open', 'high', 'low',
        'close' (volume column optional and ignored here) on a
        DatetimeIndex.
    window : int, default 14
        Smoothing period. Must be >= 2.

    Returns
    -------
    pd.Series
        ATR aligned to df.index, name = f"atr_{window}".
        - Indices [0 .. window-2] are NaN (warm-up).
        - ATR[window-1] is seeded as the simple mean of the first `window`
          true-range values.
        - For t >= window, ATR[t] = (ATR[t-1] * (n-1) + TR[t]) / n.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"df must be a pandas DataFrame; got {type(df).__name__}"
        )
    missing = [c for c in _REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            f"df missing required columns {missing}; OHLCV columns must be "
            f"lowercase per Phase 1.1 convention"
        )
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("df must have a DatetimeIndex")
    if window < 2:
        raise ValueError(f"window must be >= 2; got {window}")
    if len(df) < window:
        raise ValueError(
            f"df has {len(df)} bars but window={window} requires at least that many"
        )

    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    close = df["close"].to_numpy(dtype=float)

    # True range. Bar 0 has no prev close, so we fall back to high - low.
    prev_close = np.concatenate(([np.nan], close[:-1]))
    hl = high - low
    hc = np.abs(high - prev_close)
    lc = np.abs(low - prev_close)
    tr = np.where(
        np.isnan(prev_close),
        hl,
        np.maximum(hl, np.maximum(hc, lc)),
    )

    # Wilder's RMA: SMA seed at index window-1, then recurrence.
    atr = np.full(len(df), np.nan, dtype=float)
    atr[window - 1] = tr[:window].mean()
    for t in range(window, len(df)):
        atr[t] = (atr[t - 1] * (window - 1) + tr[t]) / window

    return pd.Series(atr, index=df.index, name=f"atr_{window}")