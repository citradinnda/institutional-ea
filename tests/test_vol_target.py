"""Tests for Phase 2.1b vol-target sizing."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.indicators import vol_target_size


def _returns(n: int = 500, sigma: float = 0.01, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-01-01", periods=n, freq="B")
    return pd.Series(rng.normal(0.0, sigma, size=n), index=idx, name="ret")


def test_vol_target_returns_aligned_named_series() -> None:
    r = _returns()
    out = vol_target_size(r, target_vol_annual=0.10, lookback=20)
    assert isinstance(out, pd.Series)
    assert out.index.equals(r.index)
    assert out.name == "vol_target_size"


def test_vol_target_warmup_nan() -> None:
    r = _returns(n=100)
    out = vol_target_size(r, lookback=20)
    # Window at index t spans [t-lookback .. t-1]. With shift(1) + window=20,
    # the first non-NaN index is lookback (index 20).
    assert out.iloc[:20].isna().all()
    assert not np.isnan(out.iloc[20])


def test_vol_target_inverse_to_realized_vol() -> None:
    """Doubling the underlying vol should approximately halve the multiplier."""
    r_low = _returns(n=500, sigma=0.005, seed=1)
    r_high = _returns(n=500, sigma=0.010, seed=1)
    m_low = vol_target_size(r_low, target_vol_annual=0.10, lookback=20).dropna()
    m_high = vol_target_size(r_high, target_vol_annual=0.10, lookback=20).dropna()
    # Median ratio should be ~2 (allow 20% tolerance for finite sample noise).
    ratio = m_low.median() / m_high.median()
    assert 1.6 < ratio < 2.4


def test_vol_target_clips_at_max_leverage() -> None:
    """With a target much higher than realized, multiplier saturates."""
    r = _returns(n=200, sigma=0.001, seed=2)  # near-zero realized vol
    out = vol_target_size(r, target_vol_annual=1.0, lookback=20, max_leverage=3.0)
    assert (out.dropna() <= 3.0 + 1e-12).all()
    assert (out.dropna() >= 3.0 - 1e-12).any()  # at least some saturated


def test_vol_target_no_lookahead() -> None:
    """vol_target_size[t] uses returns[t-lookback..t-1], NOT including t."""
    r = _returns(n=200, seed=3)
    full = vol_target_size(r, lookback=20)
    for cutoff in (50, 100, 150):
        truncated = vol_target_size(r.iloc[:cutoff], lookback=20)
        pd.testing.assert_series_equal(
            full.iloc[:cutoff], truncated, check_names=False
        )


def test_vol_target_value_at_t_independent_of_return_at_t() -> None:
    """Mutating returns[t] must not change multiplier[t] (only multiplier[t+1]+)."""
    r = _returns(n=100, seed=4)
    out_before = vol_target_size(r, lookback=20)
    r2 = r.copy()
    r2.iloc[50] = 100.0  # huge shock
    out_after = vol_target_size(r2, lookback=20)
    # multiplier[50] depends on returns[30..49] — must be unchanged.
    assert out_before.iloc[50] == pytest.approx(out_after.iloc[50])
    # multiplier[51] should differ (now sees the shock).
    assert out_before.iloc[51] != pytest.approx(out_after.iloc[51])


def test_vol_target_known_value() -> None:
    """Hand-check: constant-vol returns => predictable multiplier."""
    n = 60
    sigma = 0.01
    target = 0.20
    rng = np.random.default_rng(7)
    r = pd.Series(
        rng.normal(0.0, sigma, size=n),
        index=pd.date_range("2024-01-01", periods=n, freq="B"),
    )
    out = vol_target_size(
        r, target_vol_annual=target, lookback=20, periods_per_year=252,
        max_leverage=100.0,
    )
    # Expected near target / (sigma * sqrt(252)) = 0.20 / (0.01 * 15.87) ~ 1.26
    expected = target / (sigma * np.sqrt(252))
    assert 0.7 * expected < out.dropna().median() < 1.4 * expected


def test_vol_target_zero_vol_window_clips_to_max() -> None:
    """A constant-return window has realized vol = 0; multiplier clips to max."""
    n = 50
    r = pd.Series(
        np.zeros(n),
        index=pd.date_range("2024-01-01", periods=n, freq="B"),
    )
    out = vol_target_size(r, target_vol_annual=0.10, lookback=20, max_leverage=3.0)
    valid = out.dropna()
    assert np.allclose(valid.to_numpy(), 3.0)


def test_vol_target_rejects_bad_inputs() -> None:
    r = _returns(n=50)
    with pytest.raises(TypeError, match="Series"):
        vol_target_size(r.to_numpy())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="target_vol_annual"):
        vol_target_size(r, target_vol_annual=0.0)
    with pytest.raises(ValueError, match="lookback"):
        vol_target_size(r, lookback=1)
    with pytest.raises(ValueError, match="periods_per_year"):
        vol_target_size(r, periods_per_year=0)
    with pytest.raises(ValueError, match="max_leverage"):
        vol_target_size(r, max_leverage=0.0)


def test_vol_target_rejects_too_few_obs() -> None:
    short = _returns(n=15)
    with pytest.raises(ValueError, match="at least"):
        vol_target_size(short, lookback=20)