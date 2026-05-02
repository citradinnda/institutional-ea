"""Tests for Phase 2.1b chandelier exit."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.indicators import average_true_range, chandelier_exit


def _make_ohlcv(n: int = 100, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0.0, 1.0, size=n))
    high = close + rng.uniform(0.5, 2.0, size=n)
    low = close - rng.uniform(0.5, 2.0, size=n)
    open_ = np.clip(close + rng.normal(0.0, 0.4, size=n), low, high)
    idx = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close,
         "volume": np.ones(n)},
        index=idx,
    )


def test_chandelier_long_aligned_and_named() -> None:
    df = _make_ohlcv()
    atr = average_true_range(df, window=14)
    out = chandelier_exit(df, atr, multiplier=3.0, lookback=22, side="long")
    assert isinstance(out, pd.Series)
    assert out.index.equals(df.index)
    assert out.name == "chandelier_long_3.0_22"


def test_chandelier_short_name_reflects_side() -> None:
    df = _make_ohlcv()
    atr = average_true_range(df, window=14)
    out = chandelier_exit(df, atr, multiplier=2.5, lookback=20, side="short")
    assert out.name == "chandelier_short_2.5_20"


def test_chandelier_long_below_high() -> None:
    df = _make_ohlcv(n=200, seed=1)
    atr = average_true_range(df, window=14)
    stop = chandelier_exit(df, atr, multiplier=3.0, lookback=22, side="long")
    valid = stop.dropna()
    rolling_high = df["high"].rolling(22).max().loc[valid.index]
    assert (valid <= rolling_high).all()


def test_chandelier_short_above_low() -> None:
    df = _make_ohlcv(n=200, seed=2)
    atr = average_true_range(df, window=14)
    stop = chandelier_exit(df, atr, multiplier=3.0, lookback=22, side="short")
    valid = stop.dropna()
    rolling_low = df["low"].rolling(22).min().loc[valid.index]
    assert (valid >= rolling_low).all()


def test_chandelier_widens_with_multiplier_long() -> None:
    """Larger multiplier => stop further below the rolling high."""
    df = _make_ohlcv(n=200, seed=3)
    atr = average_true_range(df, window=14)
    s2 = chandelier_exit(df, atr, multiplier=2.0, lookback=22, side="long")
    s5 = chandelier_exit(df, atr, multiplier=5.0, lookback=22, side="long")
    valid = s2.dropna().index.intersection(s5.dropna().index)
    assert (s5.loc[valid] < s2.loc[valid]).all()


def test_chandelier_widens_with_multiplier_short() -> None:
    df = _make_ohlcv(n=200, seed=4)
    atr = average_true_range(df, window=14)
    s2 = chandelier_exit(df, atr, multiplier=2.0, lookback=22, side="short")
    s5 = chandelier_exit(df, atr, multiplier=5.0, lookback=22, side="short")
    valid = s2.dropna().index.intersection(s5.dropna().index)
    assert (s5.loc[valid] > s2.loc[valid]).all()


def test_chandelier_warmup_nan() -> None:
    df = _make_ohlcv(n=100)
    atr = average_true_range(df, window=14)
    out = chandelier_exit(df, atr, multiplier=3.0, lookback=22, side="long")
    # Warm-up = max(atr_warmup=13, lookback-1=21) = 21
    assert out.iloc[:21].isna().all()
    assert not np.isnan(out.iloc[21])


def test_chandelier_no_lookahead() -> None:
    df = _make_ohlcv(n=120, seed=5)
    atr_full = average_true_range(df, window=14)
    full = chandelier_exit(df, atr_full, multiplier=3.0, lookback=22, side="long")
    for cutoff in (40, 80, 100):
        sub = df.iloc[:cutoff]
        atr_sub = average_true_range(sub, window=14)
        truncated = chandelier_exit(
            sub, atr_sub, multiplier=3.0, lookback=22, side="long"
        )
        pd.testing.assert_series_equal(
            full.iloc[:cutoff], truncated, check_names=False
        )


def test_chandelier_rejects_bad_inputs() -> None:
    df = _make_ohlcv(n=50)
    atr = average_true_range(df, window=14)
    with pytest.raises(TypeError, match="DataFrame"):
        chandelier_exit(np.zeros((50, 4)), atr)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="missing required columns"):
        chandelier_exit(df.drop(columns=["high"]), atr)
    with pytest.raises(TypeError, match="Series"):
        chandelier_exit(df, atr.to_numpy())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="multiplier"):
        chandelier_exit(df, atr, multiplier=0.0)
    with pytest.raises(ValueError, match="lookback"):
        chandelier_exit(df, atr, lookback=1)
    with pytest.raises(ValueError, match="side"):
        chandelier_exit(df, atr, side="bogus")  # type: ignore[arg-type]


def test_chandelier_rejects_misaligned_atr() -> None:
    df = _make_ohlcv(n=50)
    atr = average_true_range(df, window=14)
    bad_atr = atr.iloc[:-5]
    with pytest.raises(ValueError, match="atr.index must equal"):
        chandelier_exit(df, bad_atr)