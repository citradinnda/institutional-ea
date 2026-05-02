"""Tests for quantcore.data.loaders."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.data.loaders import (
    CANONICAL_COLS,
    _ensure_canonical,
    load_parquet,
    resample,
)


def _make_sample_ohlcv(n: int = 100, freq: str = "1h") -> pd.DataFrame:
    """Build a fake OHLCV DataFrame for testing."""
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    rng = np.random.default_rng(42)
    close = 100 + rng.standard_normal(n).cumsum()
    df = pd.DataFrame(
        {
            "open": close + rng.standard_normal(n) * 0.1,
            "high": close + np.abs(rng.standard_normal(n)) * 0.5,
            "low": close - np.abs(rng.standard_normal(n)) * 0.5,
            "close": close,
            "volume": rng.integers(100, 1000, n),
        },
        index=idx,
    )
    return df


# ---------- _ensure_canonical ----------

def test_ensure_canonical_lowercases_columns():
    df = _make_sample_ohlcv()
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    out = _ensure_canonical(df)
    assert list(out.columns) == CANONICAL_COLS


def test_ensure_canonical_raises_on_missing_columns():
    df = _make_sample_ohlcv().drop(columns=["volume"])
    with pytest.raises(ValueError, match="Missing required columns"):
        _ensure_canonical(df)


def test_ensure_canonical_localizes_naive_index_to_utc():
    df = _make_sample_ohlcv()
    df.index = df.index.tz_localize(None)  # strip timezone
    out = _ensure_canonical(df)
    assert str(out.index.tz) == "UTC"


def test_ensure_canonical_converts_non_utc_to_utc():
    df = _make_sample_ohlcv()
    df.index = df.index.tz_convert("America/New_York")
    out = _ensure_canonical(df)
    assert str(out.index.tz) == "UTC"


def test_ensure_canonical_drops_duplicates():
    df = _make_sample_ohlcv(n=10)
    df = pd.concat([df, df.iloc[[0]]])  # duplicate the first row
    out = _ensure_canonical(df)
    assert not out.index.has_duplicates
    assert len(out) == 10


def test_ensure_canonical_sorts_ascending():
    df = _make_sample_ohlcv(n=10)
    df = df.iloc[::-1]  # reverse it
    out = _ensure_canonical(df)
    assert out.index.is_monotonic_increasing


# ---------- resample ----------

def test_resample_h1_to_h4():
    df = _make_sample_ohlcv(n=24, freq="1h")  # 24 hours of data
    out = resample(df, "H4")
    # 24 hours / 4 = 6 four-hour bars
    assert len(out) == 6
    # H4 high must be >= every H1 high it contains
    assert out["high"].iloc[0] >= df["high"].iloc[:4].max() - 1e-9


def test_resample_aggregates_volume():
    df = _make_sample_ohlcv(n=24, freq="1h")
    out = resample(df, "H4")
    assert out["volume"].iloc[0] == df["volume"].iloc[:4].sum()


# ---------- load_parquet round trip ----------

def test_load_parquet_roundtrip(tmp_path):
    """Save a DataFrame to parquet, load it back, verify it survives intact."""
    df = _make_sample_ohlcv(n=50)
    path = tmp_path / "test.parquet"
    df.to_parquet(path)
    out = load_parquet(path)
    assert list(out.columns) == CANONICAL_COLS
    assert str(out.index.tz) == "UTC"
    assert len(out) == 50