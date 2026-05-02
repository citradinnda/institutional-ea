"""
Tests for Phase 2.1 ATR indicator.

The hand-computed reference in `_hand_computed_df` uses a 6-bar synthetic
series with window=3 so correctness is verifiable by inspection:

    bar | open high low close | TR
     0  | 100  110  95  105   | 15  (high - low; no prev close)
     1  | 105  112  100 108   | max(12, |112-105|, |100-105|) = 12
     2  | 108  115  104 110   | max(11,  |115-108|, |104-108|) = 11
     3  | 110  113  105 107   | max( 8,  |113-110|, |105-110|) =  8
     4  | 107  109  100 102   | max( 9,  |109-107|, |100-107|) =  9
     5  | 102  106   98 104   | max( 8,  |106-102|, | 98-102|) =  8

ATR(3): seed at index 2 = (15+12+11)/3 = 38/3. Then Wilder recurrence.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.indicators import average_true_range


def _make_ohlcv(n: int = 50, seed: int = 0) -> pd.DataFrame:
    """Random but bounded OHLCV with low <= open/close <= high by construction."""
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0.0, 1.0, size=n))
    high = close + rng.uniform(0.5, 2.0, size=n)
    low = close - rng.uniform(0.5, 2.0, size=n)
    open_ = close + rng.normal(0.0, 0.4, size=n)
    # Clip open into [low, high] to keep OHLC well-formed.
    open_ = np.clip(open_, low, high)
    vol = rng.integers(100, 1000, size=n)
    idx = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": vol},
        index=idx,
    )


def _hand_computed_df() -> pd.DataFrame:
    data = {
        "open":   [100, 105, 108, 110, 107, 102],
        "high":   [110, 112, 115, 113, 109, 106],
        "low":    [ 95, 100, 104, 105, 100,  98],
        "close":  [105, 108, 110, 107, 102, 104],
        "volume": [  1,   1,   1,   1,   1,   1],
    }
    idx = pd.date_range("2024-01-01", periods=6, freq="D", tz="UTC")
    return pd.DataFrame(data, index=idx)


# ---------- structural tests ----------

def test_atr_returns_pd_series_aligned_to_input() -> None:
    df = _make_ohlcv()
    out = average_true_range(df, window=14)
    assert isinstance(out, pd.Series)
    assert len(out) == len(df)
    assert out.index.equals(df.index)


def test_atr_name_reflects_window() -> None:
    df = _make_ohlcv()
    assert average_true_range(df, window=14).name == "atr_14"
    assert average_true_range(df, window=21).name == "atr_21"


# ---------- numerical tests (hand-computed reference) ----------

def test_atr_seed_is_simple_mean_of_first_window_trs() -> None:
    df = _hand_computed_df()
    # TR[0]=15, TR[1]=12, TR[2]=11. Seed = 38/3.
    out = average_true_range(df, window=3)
    assert out.iloc[2] == pytest.approx(38 / 3)


def test_atr_known_values_window_3() -> None:
    df = _hand_computed_df()
    out = average_true_range(df, window=3)
    assert np.isnan(out.iloc[0])
    assert np.isnan(out.iloc[1])
    seed = 38 / 3
    a3 = (seed * 2 + 8) / 3
    a4 = (a3 * 2 + 9) / 3
    a5 = (a4 * 2 + 8) / 3
    assert out.iloc[2] == pytest.approx(seed)
    assert out.iloc[3] == pytest.approx(a3)
    assert out.iloc[4] == pytest.approx(a4)
    assert out.iloc[5] == pytest.approx(a5)


def test_atr_warmup_returns_nan() -> None:
    df = _make_ohlcv(n=30)
    window = 14
    out = average_true_range(df, window=window)
    assert out.iloc[: window - 1].isna().all()
    assert not np.isnan(out.iloc[window - 1])


def test_atr_wilder_recurrence_holds_throughout() -> None:
    df = _make_ohlcv(n=80, seed=42)
    window = 14
    out = average_true_range(df, window=window)
    # Recompute TR independently and check the recurrence at every bar.
    high = df["high"].to_numpy()
    low = df["low"].to_numpy()
    close = df["close"].to_numpy()
    prev_close = np.concatenate(([np.nan], close[:-1]))
    hl = high - low
    hc = np.abs(high - prev_close)
    lc = np.abs(low - prev_close)
    tr = np.where(np.isnan(prev_close), hl, np.maximum(hl, np.maximum(hc, lc)))
    atr = out.to_numpy()
    for t in range(window, len(df)):
        expected = (atr[t - 1] * (window - 1) + tr[t]) / window
        assert atr[t] == pytest.approx(expected, rel=1e-12)


def test_atr_is_strictly_positive_after_warmup() -> None:
    df = _make_ohlcv(n=200, seed=1)
    out = average_true_range(df, window=14)
    valid = out.dropna()
    assert (valid > 0).all()


def test_atr_responds_to_volatility_shock() -> None:
    """Insert a high-range bar; ATR should rise on the next bar."""
    df = _hand_computed_df().copy()
    out_before = average_true_range(df, window=3)
    # Replace bar 5 with a much wider range.
    df.loc[df.index[5], ["high", "low"]] = [130.0, 80.0]
    out_after = average_true_range(df, window=3)
    assert out_after.iloc[5] > out_before.iloc[5]


# ---------- lookahead-safety test ----------

def test_atr_no_lookahead() -> None:
    """ATR[t] must depend only on bars [0..t]. Truncating future bars
    cannot change earlier ATR values — same invariant verified by Phase 1.5
    `assert_no_lookahead` for validation primitives."""
    df = _make_ohlcv(n=100, seed=3)
    full = average_true_range(df, window=14)
    for cutoff in (20, 50, 80):
        truncated = average_true_range(df.iloc[:cutoff], window=14)
        pd.testing.assert_series_equal(
            full.iloc[:cutoff],
            truncated,
            check_names=False,
        )


# ---------- input-validation tests ----------

def test_atr_rejects_non_dataframe() -> None:
    with pytest.raises(TypeError, match="DataFrame"):
        average_true_range(np.zeros((10, 4)), window=14)  # type: ignore[arg-type]


def test_atr_rejects_missing_columns() -> None:
    df = _make_ohlcv(n=20).drop(columns=["high"])
    with pytest.raises(ValueError, match="missing required columns"):
        average_true_range(df, window=14)


def test_atr_rejects_uppercase_columns() -> None:
    df = _make_ohlcv(n=20).rename(
        columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"}
    )
    with pytest.raises(ValueError, match="missing required columns"):
        average_true_range(df, window=14)


def test_atr_rejects_non_datetime_index() -> None:
    df = _make_ohlcv(n=20).reset_index(drop=True)
    with pytest.raises(TypeError, match="DatetimeIndex"):
        average_true_range(df, window=14)


def test_atr_rejects_invalid_window() -> None:
    df = _make_ohlcv(n=30)
    with pytest.raises(ValueError, match="window must be >= 2"):
        average_true_range(df, window=1)
    with pytest.raises(ValueError, match="window must be >= 2"):
        average_true_range(df, window=0)


def test_atr_rejects_too_few_bars() -> None:
    df = _make_ohlcv(n=10)
    with pytest.raises(ValueError, match="requires at least"):
        average_true_range(df, window=14)