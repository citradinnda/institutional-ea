"""
Chandelier exit (LeBeau, 1990s).

WHY this stop, not a fixed-pip stop: chandelier widens with realized
volatility (via ATR) and trails the highest high (long) / lowest low
(short) over a lookback. This adapts to regime: tight stops in quiet
markets, wide stops when volatility expands. Matches H011-H013 graveyard
finding that ATR-based stops + chandelier exits produced real edge on
USDJPY.

Long stop  = highest_high(lookback) - multiplier * ATR
Short stop = lowest_low(lookback)   + multiplier * ATR

WHY warm-up returns NaN: stop is undefined until both ATR and the rolling
high/low window are filled. Caller must skip warm-up bars.

Reference:
    LeBeau, C., & Lucas, D. W. (1991). Computer Analysis of the Futures
    Markets. McGraw-Hill.
"""
from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

_REQUIRED_COLS: tuple[str, ...] = ("open", "high", "low", "close")
Side = Literal["long", "short"]


def chandelier_exit(
    df: pd.DataFrame,
    atr: pd.Series,
    multiplier: float = 3.0,
    lookback: int = 22,
    side: Side = "long",
) -> pd.Series:
    """
    Compute the chandelier trailing-stop level at each bar.

    Parameters
    ----------
    df : pd.DataFrame
        Canonical OHLCV per Phase 1.1.
    atr : pd.Series
        ATR series aligned to df.index. Typically from
        `quantcore.indicators.average_true_range`.
    multiplier : float, default 3.0
        ATR multiplier. Must be > 0.
    lookback : int, default 22
        Rolling window for highest-high / lowest-low. Must be >= 2.
    side : {"long", "short"}, default "long"

    Returns
    -------
    pd.Series
        Stop level aligned to df.index, name =
        f"chandelier_{side}_{multiplier}_{lookback}". NaN where either ATR
        or the rolling window has not yet warmed up.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"df must be a pandas DataFrame; got {type(df).__name__}"
        )
    missing = [c for c in _REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"df missing required columns {missing}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("df must have a DatetimeIndex")
    if not isinstance(atr, pd.Series):
        raise TypeError("atr must be a pandas Series")
    if not atr.index.equals(df.index):
        raise ValueError("atr.index must equal df.index")
    if multiplier <= 0:
        raise ValueError(f"multiplier must be > 0; got {multiplier}")
    if lookback < 2:
        raise ValueError(f"lookback must be >= 2; got {lookback}")
    if side not in ("long", "short"):
        raise ValueError(f"side must be 'long' or 'short'; got {side!r}")

    if side == "long":
        extreme = df["high"].rolling(lookback, min_periods=lookback).max()
        stop = extreme - multiplier * atr
    else:
        extreme = df["low"].rolling(lookback, min_periods=lookback).min()
        stop = extreme + multiplier * atr

    stop.name = f"chandelier_{side}_{multiplier}_{lookback}"
    return stop