"""Tick / bar outlier detection using Median Absolute Deviation (MAD).

We flag bars whose log-return is statistically extreme relative to the
distribution of all returns in the series. We never auto-delete: the
researcher must consciously decide what to do with flagged bars.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# 1.4826 makes MAD a consistent estimator of standard deviation under normality.
_MAD_SCALE = 1.4826


def mad_zscore(returns: pd.Series) -> pd.Series:
    """Return the MAD-based z-score of each value in `returns`.

    Robust to outliers because median and MAD are both unaffected by extremes.
    Returns zeros (not NaN) when MAD is exactly zero (constant series).
    """
    med = returns.median()
    mad = (returns - med).abs().median()
    if mad == 0 or np.isnan(mad):
        return pd.Series(0.0, index=returns.index)
    return (returns - med) / (_MAD_SCALE * mad)


def flag_outliers(df: pd.DataFrame, z_threshold: float = 8.0) -> pd.Series:
    """Boolean Series, True where a bar's log-return is > z_threshold MAD units.

    Parameters
    ----------
    df : DataFrame
        Canonical OHLCV.
    z_threshold : float
        MAD z-score above which a bar is flagged. Default 8.0 is very strict;
        production values are typically 6–10.

    Returns
    -------
    Series of bool, same index as df. The first bar is always False (no return).
    """
    log_ret = np.log(df["close"]).diff()
    z = mad_zscore(log_ret)
    flagged = z.abs() > z_threshold
    flagged.iloc[0] = False  # first bar has NaN return, always False
    return flagged


def outlier_summary(df: pd.DataFrame, z_threshold: float = 8.0) -> dict:
    """Compact summary of outlier statistics for reporting."""
    flags = flag_outliers(df, z_threshold=z_threshold)
    n_flagged = int(flags.sum())
    return {
        "n_bars": len(df),
        "n_flagged": n_flagged,
        "pct_flagged": float(n_flagged / len(df) * 100) if len(df) > 0 else 0.0,
        "z_threshold": z_threshold,
        "first_flagged_timestamps": list(flags[flags].index[:5].astype(str)),
    }