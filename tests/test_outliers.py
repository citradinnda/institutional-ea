"""Tests for quantcore.data.outliers."""

from __future__ import annotations

import numpy as np
import pandas as pd

from quantcore.data.outliers import (
    flag_outliers,
    mad_zscore,
    outlier_summary,
)


def _make_clean_ohlcv(n: int = 500, seed: int = 0) -> pd.DataFrame:
    """Synthetic OHLCV with normally-distributed returns, no outliers."""
    idx = pd.date_range("2024-01-01", periods=n, freq="1h", tz="UTC")
    rng = np.random.default_rng(seed)
    returns = rng.normal(0, 0.001, n)  # ~0.1% per bar, gaussian
    close = 100 * np.exp(np.cumsum(returns))
    df = pd.DataFrame(
        {
            "open": close,
            "high": close * 1.001,
            "low": close * 0.999,
            "close": close,
            "volume": rng.integers(100, 1000, n),
        },
        index=idx,
    )
    return df


# ---------- mad_zscore ----------

def test_mad_zscore_returns_zero_for_constant_series():
    s = pd.Series([1.0] * 10)
    out = mad_zscore(s)
    assert (out == 0).all()


def test_mad_zscore_centers_at_median():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    out = mad_zscore(s)
    # Median is 3, so the middle value should be exactly zero
    assert out.iloc[2] == 0.0


def test_mad_zscore_robust_to_outliers():
    # Adding a single extreme value should not destroy the scale
    clean = pd.Series(np.random.default_rng(0).normal(0, 1, 100))
    contaminated = clean.copy()
    contaminated.iloc[50] = 1000.0
    z_clean = mad_zscore(clean).abs().median()
    z_contam = mad_zscore(contaminated).abs().median()
    # Median z-score should remain similar (robust to the spike)
    assert abs(z_clean - z_contam) < 0.5


# ---------- flag_outliers ----------

def test_flag_outliers_returns_no_flags_on_clean_data():
    df = _make_clean_ohlcv(n=500)
    flags = flag_outliers(df, z_threshold=8.0)
    assert flags.sum() == 0


def test_flag_outliers_catches_injected_spike():
    df = _make_clean_ohlcv(n=500)
    # Inject a 50% price jump at bar 250 — clearly a bad tick
    df.loc[df.index[250], "close"] = df["close"].iloc[249] * 1.5
    flags = flag_outliers(df, z_threshold=8.0)
    assert flags.sum() >= 1
    assert flags.iloc[250] or flags.iloc[251]  # spike or its reversal


def test_flag_outliers_first_bar_is_always_false():
    df = _make_clean_ohlcv(n=100)
    flags = flag_outliers(df)
    assert flags.iloc[0] == False  # noqa: E712


def test_flag_outliers_strict_threshold_flags_more():
    df = _make_clean_ohlcv(n=1000)
    df.loc[df.index[500], "close"] = df["close"].iloc[499] * 1.05  # mild spike
    strict = flag_outliers(df, z_threshold=3.0).sum()
    lenient = flag_outliers(df, z_threshold=8.0).sum()
    assert strict >= lenient


def test_flag_outliers_returns_series_aligned_with_input():
    df = _make_clean_ohlcv(n=100)
    flags = flag_outliers(df)
    assert len(flags) == len(df)
    assert flags.index.equals(df.index)
    assert flags.dtype == bool


# ---------- outlier_summary ----------

def test_outlier_summary_structure():
    df = _make_clean_ohlcv(n=100)
    summary = outlier_summary(df)
    assert summary["n_bars"] == 100
    assert summary["n_flagged"] == 0
    assert summary["pct_flagged"] == 0.0
    assert summary["z_threshold"] == 8.0
    assert summary["first_flagged_timestamps"] == []


def test_outlier_summary_reports_flagged_timestamps():
    df = _make_clean_ohlcv(n=500)
    df.loc[df.index[250], "close"] = df["close"].iloc[249] * 1.5
    summary = outlier_summary(df)
    assert summary["n_flagged"] >= 1
    assert len(summary["first_flagged_timestamps"]) >= 1