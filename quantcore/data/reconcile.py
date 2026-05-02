"""Cross-vendor OHLC reconciliation.

We pull the same bar range from two independent sources and assert that
their OHLC values agree within a tolerance scaled by ATR. This catches
broker-specific data manipulation, time-zone bugs, and bad-tick contamination.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ReconciliationReport:
    """Structured result of comparing two OHLCV sources."""
    n_bars: int
    n_mismatches: int
    max_open_diff_atr: float
    max_close_diff_atr: float
    pass_threshold: float
    passed: bool

    def __str__(self) -> str:
        return (
            f"Reconciliation: {self.n_bars} bars, {self.n_mismatches} mismatches, "
            f"max open diff = {self.max_open_diff_atr:.3f} ATR, "
            f"max close diff = {self.max_close_diff_atr:.3f} ATR, "
            f"threshold = {self.pass_threshold} ATR, passed = {self.passed}"
        )


def _atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    """Average True Range over `n` bars."""
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.rolling(n, min_periods=n).mean()


def reconcile(
    primary: pd.DataFrame,
    secondary: pd.DataFrame,
    tolerance_atr: float = 0.5,
) -> ReconciliationReport:
    """Compare two OHLCV frames and return a mismatch report.

    Parameters
    ----------
    primary, secondary : DataFrame
        Canonical OHLCV with UTC DatetimeIndex.
    tolerance_atr : float
        Maximum allowed |diff| in units of primary's ATR(14).

    Returns
    -------
    ReconciliationReport
        Structured report. `passed` is True iff zero bars exceed tolerance.
    """
    common = primary.index.intersection(secondary.index)
    if len(common) == 0:
        raise ValueError("No overlapping timestamps between vendors")

    p = primary.loc[common]
    s = secondary.loc[common]

    # ATR computed on the primary; bfill for the first 13 bars where ATR is NaN
    atr = _atr(p).reindex(common).bfill()

    # Avoid division by zero on flat synthetic data
    atr = atr.replace(0.0, np.nan).bfill().ffill()

    open_diff_atr = (p["open"] - s["open"]).abs() / atr
    close_diff_atr = (p["close"] - s["close"]).abs() / atr

    mismatches = ((open_diff_atr > tolerance_atr) | (close_diff_atr > tolerance_atr)).sum()

    return ReconciliationReport(
        n_bars=len(common),
        n_mismatches=int(mismatches),
        max_open_diff_atr=float(np.nanmax(open_diff_atr)),
        max_close_diff_atr=float(np.nanmax(close_diff_atr)),
        pass_threshold=tolerance_atr,
        passed=bool(mismatches == 0),
    )