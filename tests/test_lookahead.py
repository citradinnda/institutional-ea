from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.validation.lookahead import (
    LookaheadReport,
    LookaheadViolation,
    assert_no_lookahead,
)


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

def _ohlcv(n: int = 60, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC", name="time")
    close = 100.0 + np.cumsum(rng.standard_normal(n) * 0.1)
    return pd.DataFrame(
        {
            "open": close + rng.standard_normal(n) * 0.05,
            "high": close + np.abs(rng.standard_normal(n)) * 0.1,
            "low":  close - np.abs(rng.standard_normal(n)) * 0.1,
            "close": close,
            "volume": rng.integers(100, 1000, n).astype("int64"),
        },
        index=idx,
    )


# --------------------------------------------------------------------------- #
# CLEAN feature functions: must pass
# --------------------------------------------------------------------------- #

def test_clean_rolling_mean_passes():
    """A trailing rolling mean is the textbook lookahead-clean feature."""
    def f(df):
        return df["close"].rolling(5).mean().rename("sma5")

    report = assert_no_lookahead(f, _ohlcv())
    assert isinstance(report, LookaheadReport)
    assert report.clean is True
    assert report.violations == ()
    assert report.n_checks > 0


def test_clean_returns_passes():
    """pct_change uses only past+current bar; safe."""
    def f(df):
        return df["close"].pct_change().rename("ret")

    assert assert_no_lookahead(f, _ohlcv()).clean is True


def test_clean_dataframe_output_passes():
    """Multi-column feature output is supported."""
    def f(df):
        return pd.DataFrame(
            {
                "sma5":  df["close"].rolling(5).mean(),
                "sma10": df["close"].rolling(10).mean(),
            },
            index=df.index,
        )

    report = assert_no_lookahead(f, _ohlcv())
    assert report.clean is True


def test_clean_ewm_passes():
    """Exponentially weighted mean is causal by construction."""
    def f(df):
        return df["close"].ewm(span=10, adjust=False).mean().rename("ewm10")

    assert assert_no_lookahead(f, _ohlcv()).clean is True


# --------------------------------------------------------------------------- #
# DIRTY feature functions: must be flagged
# --------------------------------------------------------------------------- #

def test_dirty_negative_shift_is_caught():
    """shift(-1) literally pulls tomorrow's close into today. Classic lookahead."""
    def f(df):
        return df["close"].shift(-1).rename("tomorrow_close")

    with pytest.raises(AssertionError, match="LOOKAHEAD VIOLATION"):
        assert_no_lookahead(f, _ohlcv())


def test_dirty_global_zscore_is_caught():
    """Z-scoring with the FULL-series mean/std is a lookahead.

    This is the single most common 'silent' lookahead in ML pipelines:
    fitting a scaler on the whole series before the train/test split.
    """
    def f(df):
        x = df["close"]
        return ((x - x.mean()) / x.std()).rename("z")

    with pytest.raises(AssertionError, match="LOOKAHEAD VIOLATION"):
        assert_no_lookahead(f, _ohlcv())


def test_dirty_backfill_is_caught():
    """Backfill copies future values into past NaN slots.

    Detection requires a truncation length that excludes the bfill
    source. We place the NaN at position 20 and truncate at 21:
    in the full run, position 20 is filled from position 21;
    in the truncated run, position 21 doesn't exist so position 20
    stays NaN. The mismatch (NaN vs. real number) is the violation.

    This test also documents an important lesson: the lookahead
    guard's power is bounded by the truncation lengths chosen.
    Production usage should pin truncations around feature warmup
    boundaries, not just rely on defaults.
    """
    def f(df):
        x = df["close"].copy()
        x.iloc[20] = np.nan
        return x.bfill().rename("bfilled")

    with pytest.raises(AssertionError, match="LOOKAHEAD VIOLATION"):
        assert_no_lookahead(f, _ohlcv(), truncation_lengths=[21, 30, 45])


def test_dirty_centered_rolling_is_caught():
    """center=True averages bars on BOTH sides; uses future data."""
    def f(df):
        return df["close"].rolling(5, center=True).mean().rename("centered")

    with pytest.raises(AssertionError, match="LOOKAHEAD VIOLATION"):
        assert_no_lookahead(f, _ohlcv())


def test_no_raise_mode_returns_dirty_report():
    """raise_on_violation=False enables CI-style enumeration of all issues."""
    def f(df):
        return df["close"].shift(-1).rename("peek")

    report = assert_no_lookahead(f, _ohlcv(), raise_on_violation=False)
    assert report.clean is False
    assert len(report.violations) > 0
    v: LookaheadViolation = report.violations[0]
    assert v.column == "peek"
    assert v.truncation_length in report.truncation_lengths
    assert "LOOKAHEAD VIOLATION" in report.summary()


# --------------------------------------------------------------------------- #
# API contract
# --------------------------------------------------------------------------- #

def test_custom_truncation_lengths_are_used():
    def f(df):
        return df["close"].rolling(3).mean().rename("sma3")

    report = assert_no_lookahead(f, _ohlcv(), truncation_lengths=[10, 20, 30])
    assert report.truncation_lengths == (10, 20, 30)
    assert report.clean is True


def test_invalid_truncation_length_raises():
    df = _ohlcv(n=20)
    def f(df):
        return df["close"].rename("c")

    with pytest.raises(ValueError):
        assert_no_lookahead(f, df, truncation_lengths=[1])   # too small
    with pytest.raises(ValueError):
        assert_no_lookahead(f, df, truncation_lengths=[20])  # equals n
    with pytest.raises(ValueError):
        assert_no_lookahead(f, df, truncation_lengths=[100]) # exceeds n


def test_empty_dataframe_raises():
    df = pd.DataFrame({"close": []})
    def f(df):
        return df["close"]
    with pytest.raises(ValueError):
        assert_no_lookahead(f, df)


def test_feature_must_preserve_length():
    """A feature that returns the wrong length is a bug, not a lookahead."""
    def f(df):
        return df["close"].iloc[:-1].rename("dropped_last")

    with pytest.raises(ValueError, match="length"):
        assert_no_lookahead(f, _ohlcv())


def test_feature_must_return_series_or_dataframe():
    def f(df):
        return df["close"].to_numpy()  # bare ndarray — not allowed

    with pytest.raises(TypeError):
        assert_no_lookahead(f, _ohlcv())


def test_nan_in_warmup_region_is_not_a_violation():
    """The first (window-1) bars of a rolling mean are NaN. That is correct,
    not a lookahead — the test must not flag it."""
    def f(df):
        return df["close"].rolling(10).mean().rename("sma10")

    report = assert_no_lookahead(f, _ohlcv(), truncation_lengths=[15, 30, 50])
    assert report.clean is True