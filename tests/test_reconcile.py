"""Tests for quantcore.data.reconcile."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.data.reconcile import reconcile, ReconciliationReport


def _make_ohlcv(n: int = 100, seed: int = 0) -> pd.DataFrame:
    """Build a synthetic OHLCV DataFrame with realistic bar shapes."""
    idx = pd.date_range("2024-01-01", periods=n, freq="1h", tz="UTC")
    rng = np.random.default_rng(seed)
    close = 100 + rng.standard_normal(n).cumsum()
    df = pd.DataFrame(
        {
            "open": close + rng.standard_normal(n) * 0.05,
            "high": close + np.abs(rng.standard_normal(n)) * 0.5 + 0.1,
            "low": close - np.abs(rng.standard_normal(n)) * 0.5 - 0.1,
            "close": close,
            "volume": rng.integers(100, 1000, n),
        },
        index=idx,
    )
    return df


# ---------- happy path ----------

def test_reconcile_identical_data_passes():
    df = _make_ohlcv(n=100)
    report = reconcile(df, df.copy())
    assert report.passed
    assert report.n_mismatches == 0


def test_reconcile_returns_correct_n_bars():
    df = _make_ohlcv(n=100)
    report = reconcile(df, df.copy())
    assert report.n_bars == 100


# ---------- mismatch detection ----------

def test_reconcile_detects_large_mismatch():
    primary = _make_ohlcv(n=100)
    secondary = primary.copy()
    # Inject a 10-unit price spike at bar 50; clearly > 0.5 ATR
    secondary.loc[secondary.index[50], "close"] = primary["close"].iloc[50] + 10.0
    report = reconcile(primary, secondary)
    assert not report.passed
    assert report.n_mismatches >= 1


def test_reconcile_ignores_tiny_differences():
    primary = _make_ohlcv(n=100)
    secondary = primary.copy()
    # Tiny bid-ask-like difference, well under 0.5 ATR
    secondary["open"] = secondary["open"] + 0.001
    secondary["close"] = secondary["close"] + 0.001
    report = reconcile(primary, secondary)
    assert report.passed


# ---------- partial overlap ----------

def test_reconcile_uses_only_overlapping_timestamps():
    primary = _make_ohlcv(n=100)
    secondary = primary.iloc[20:80].copy()  # only 60 bars overlap
    report = reconcile(primary, secondary)
    assert report.n_bars == 60


def test_reconcile_raises_when_no_overlap():
    primary = _make_ohlcv(n=50)
    secondary = _make_ohlcv(n=50).copy()
    # Push secondary far in the future
    secondary.index = secondary.index + pd.Timedelta(days=365)
    with pytest.raises(ValueError, match="No overlapping timestamps"):
        reconcile(primary, secondary)


# ---------- tolerance parameter ----------

def test_reconcile_strict_tolerance_catches_more():
    primary = _make_ohlcv(n=100)
    secondary = primary.copy()
    # Add a moderate offset that passes lenient tolerance but fails strict
    secondary["close"] = secondary["close"] + 0.3
    lenient = reconcile(primary, secondary, tolerance_atr=1.0)
    strict = reconcile(primary, secondary, tolerance_atr=0.1)
    assert strict.n_mismatches >= lenient.n_mismatches


# ---------- report structure ----------

def test_report_is_dataclass_with_expected_fields():
    df = _make_ohlcv(n=100)
    report = reconcile(df, df.copy())
    assert isinstance(report, ReconciliationReport)
    assert hasattr(report, "n_bars")
    assert hasattr(report, "passed")
    assert hasattr(report, "max_open_diff_atr")


def test_report_str_is_human_readable():
    df = _make_ohlcv(n=100)
    report = reconcile(df, df.copy())
    text = str(report)
    assert "Reconciliation" in text
    assert "passed" in text