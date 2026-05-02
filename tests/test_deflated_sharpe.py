"""Tests for Probabilistic Sharpe and Deflated Sharpe ratios."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import (
    DSRResult,
    PSRResult,
    deflated_sharpe_ratio,
    probabilistic_sharpe_ratio,
)
from quantcore.validation.deflated_sharpe import expected_max_sharpe


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _gaussian_returns(n: int, mu: float, sigma: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(loc=mu, scale=sigma, size=n)


# ---------------------------------------------------------------------------
# PSR: structural / API tests
# ---------------------------------------------------------------------------


def test_psr_returns_frozen_dataclass() -> None:
    r = _gaussian_returns(500, mu=0.001, sigma=0.01, seed=1)
    res = probabilistic_sharpe_ratio(r)
    assert isinstance(res, PSRResult)
    with pytest.raises(Exception):
        res.psr = 0.0  # type: ignore[misc]


def test_psr_probability_in_unit_interval() -> None:
    r = _gaussian_returns(500, mu=0.001, sigma=0.01, seed=2)
    res = probabilistic_sharpe_ratio(r)
    assert 0.0 <= res.psr <= 1.0


def test_psr_accepts_pandas_series() -> None:
    r = pd.Series(_gaussian_returns(300, 0.0005, 0.01, seed=3))
    res = probabilistic_sharpe_ratio(r)
    assert 0.0 <= res.psr <= 1.0
    assert res.n == 300


def test_psr_drops_nans() -> None:
    arr = _gaussian_returns(200, 0.001, 0.01, seed=4).copy()
    arr[::20] = np.nan
    res = probabilistic_sharpe_ratio(arr)
    assert res.n == 200 - len(arr[::20])


def test_psr_observed_sr_is_annualized() -> None:
    """observed_sr field should match metrics.sharpe_ratio (annualized)."""
    from quantcore.validation.metrics import sharpe_ratio

    r = _gaussian_returns(500, mu=0.001, sigma=0.01, seed=5)
    res = probabilistic_sharpe_ratio(r, periods_per_year=252)
    assert res.observed_sr == pytest.approx(
        float(sharpe_ratio(r, periods_per_year=252)), rel=1e-9
    )


# ---------------------------------------------------------------------------
# PSR: monotonicity / sanity tests
# ---------------------------------------------------------------------------


def test_psr_high_sr_gives_high_probability() -> None:
    """Strong positive edge => PSR close to 1 vs zero benchmark."""
    r = _gaussian_returns(2000, mu=0.002, sigma=0.005, seed=10)
    res = probabilistic_sharpe_ratio(r, sr_benchmark=0.0)
    assert res.psr > 0.99


def test_psr_negative_sr_gives_low_probability() -> None:
    r = _gaussian_returns(2000, mu=-0.002, sigma=0.005, seed=11)
    res = probabilistic_sharpe_ratio(r, sr_benchmark=0.0)
    assert res.psr < 0.01


def test_psr_zero_mean_returns_about_half() -> None:
    """Exactly zero sample mean => PSR == 0.5 vs zero benchmark.

    WHY centering: with seed-driven samples, the realized mean drifts off
    zero and pushes PSR away from 0.5 in a way that depends on the seed.
    The mathematical invariant we want to test is that SR_hat == 0 maps
    to PSR == 0.5 exactly, so we center the sample to enforce SR_hat = 0.
    """
    r = _gaussian_returns(5000, mu=0.0, sigma=0.01, seed=12)
    r = r - r.mean()  # force exact zero sample mean => exact zero per-period SR
    res = probabilistic_sharpe_ratio(r, sr_benchmark=0.0)
    assert res.psr == pytest.approx(0.5, abs=1e-9)


def test_psr_more_samples_increase_confidence() -> None:
    """Same per-period SR but more samples => PSR moves away from 0.5."""
    rng = np.random.default_rng(13)
    short = rng.normal(0.001, 0.01, size=100)
    rng = np.random.default_rng(13)
    long_ = rng.normal(0.001, 0.01, size=2000)
    p_short = probabilistic_sharpe_ratio(short).psr
    p_long = probabilistic_sharpe_ratio(long_).psr
    assert abs(p_long - 0.5) > abs(p_short - 0.5)


def test_psr_higher_benchmark_lowers_probability() -> None:
    r = _gaussian_returns(1000, mu=0.001, sigma=0.01, seed=14)
    p_low = probabilistic_sharpe_ratio(r, sr_benchmark=0.0).psr
    p_high = probabilistic_sharpe_ratio(r, sr_benchmark=2.0).psr
    assert p_low > p_high


def test_psr_negative_skew_penalizes_probability() -> None:
    """Holding SR roughly equal, negative skew should reduce PSR."""
    rng = np.random.default_rng(15)
    base = rng.normal(0.001, 0.01, size=1000)
    # Inject left-tail shocks to create negative skew without flipping sign
    skewed = base.copy()
    idx = rng.choice(1000, size=20, replace=False)
    skewed[idx] -= 0.05
    # Renormalize to keep mean / std roughly comparable
    skewed = skewed * (np.std(base) / np.std(skewed))
    skewed = skewed - (np.mean(skewed) - np.mean(base))
    p_base = probabilistic_sharpe_ratio(base).psr
    p_skew = probabilistic_sharpe_ratio(skewed).psr
    assert p_skew < p_base


# ---------------------------------------------------------------------------
# PSR: input validation
# ---------------------------------------------------------------------------


def test_psr_rejects_too_few_observations() -> None:
    with pytest.raises(ValueError):
        probabilistic_sharpe_ratio(np.array([0.01]))


def test_psr_rejects_zero_variance() -> None:
    with pytest.raises(ValueError):
        probabilistic_sharpe_ratio(np.full(100, 0.001))


def test_psr_rejects_bad_periods_per_year() -> None:
    r = _gaussian_returns(100, 0.0, 0.01, seed=20)
    with pytest.raises(ValueError):
        probabilistic_sharpe_ratio(r, periods_per_year=0)


def test_psr_rejects_2d_input() -> None:
    with pytest.raises(ValueError):
        probabilistic_sharpe_ratio(np.zeros((10, 2)))


# ---------------------------------------------------------------------------
# expected_max_sharpe helper
# ---------------------------------------------------------------------------


def test_expected_max_zero_when_one_trial() -> None:
    assert expected_max_sharpe(n_trials=1, sr_variance=0.5) == 0.0


def test_expected_max_zero_when_zero_variance() -> None:
    assert expected_max_sharpe(n_trials=100, sr_variance=0.0) == 0.0


def test_expected_max_increases_with_trials() -> None:
    a = expected_max_sharpe(n_trials=10, sr_variance=0.04)
    b = expected_max_sharpe(n_trials=1000, sr_variance=0.04)
    assert b > a > 0.0


def test_expected_max_increases_with_variance() -> None:
    a = expected_max_sharpe(n_trials=100, sr_variance=0.01)
    b = expected_max_sharpe(n_trials=100, sr_variance=0.04)
    assert b > a > 0.0


def test_expected_max_rejects_bad_inputs() -> None:
    with pytest.raises(ValueError):
        expected_max_sharpe(n_trials=0, sr_variance=0.01)
    with pytest.raises(ValueError):
        expected_max_sharpe(n_trials=10, sr_variance=-0.01)


# ---------------------------------------------------------------------------
# DSR: structural / sanity tests
# ---------------------------------------------------------------------------


def test_dsr_returns_frozen_dataclass() -> None:
    r = _gaussian_returns(500, 0.001, 0.01, seed=30)
    sr_est = np.linspace(-0.05, 0.10, 50)  # per-period SRs
    res = deflated_sharpe_ratio(r, sr_est)
    assert isinstance(res, DSRResult)
    with pytest.raises(Exception):
        res.dsr = 0.0  # type: ignore[misc]


def test_dsr_probability_in_unit_interval() -> None:
    r = _gaussian_returns(500, 0.001, 0.01, seed=31)
    sr_est = np.linspace(-0.05, 0.10, 50)
    res = deflated_sharpe_ratio(r, sr_est)
    assert 0.0 <= res.dsr <= 1.0


def test_dsr_equals_psr_when_single_trial() -> None:
    """With n_trials=1 the deflation is zero, so DSR == PSR (same benchmark)."""
    r = _gaussian_returns(800, 0.001, 0.01, seed=32)
    psr = probabilistic_sharpe_ratio(r, sr_benchmark=0.0).psr
    dsr_res = deflated_sharpe_ratio(r, sr_estimates=np.array([0.05]))
    assert dsr_res.dsr == pytest.approx(psr, rel=1e-9, abs=1e-12)
    assert dsr_res.expected_max_sr == 0.0
    assert dsr_res.n_trials == 1


def test_dsr_lower_than_psr_with_many_noisy_trials() -> None:
    """More trials with dispersion => higher deflation => DSR < PSR."""
    r = _gaussian_returns(1000, 0.0015, 0.01, seed=33)
    psr = probabilistic_sharpe_ratio(r, sr_benchmark=0.0).psr
    rng = np.random.default_rng(33)
    sr_est = rng.normal(0.0, 0.1, size=500)
    dsr = deflated_sharpe_ratio(r, sr_estimates=sr_est).dsr
    assert dsr < psr


def test_dsr_decreases_as_trials_grow() -> None:
    r = _gaussian_returns(1000, 0.0015, 0.01, seed=34)
    rng = np.random.default_rng(34)
    sr_small = rng.normal(0.0, 0.1, size=20)
    sr_big = rng.normal(0.0, 0.1, size=2000)
    d_small = deflated_sharpe_ratio(r, sr_small).dsr
    d_big = deflated_sharpe_ratio(r, sr_big).dsr
    assert d_big < d_small


def test_dsr_accepts_pandas_inputs() -> None:
    r = pd.Series(_gaussian_returns(400, 0.001, 0.01, seed=35))
    sr_est = pd.Series(np.linspace(-0.02, 0.05, 30))
    res = deflated_sharpe_ratio(r, sr_est)
    assert 0.0 <= res.dsr <= 1.0
    assert res.n_trials == 30


def test_dsr_drops_nans_in_sr_estimates() -> None:
    r = _gaussian_returns(400, 0.001, 0.01, seed=36)
    sr_est = np.array([0.01, np.nan, 0.02, np.nan, 0.03])
    res = deflated_sharpe_ratio(r, sr_est)
    assert res.n_trials == 3


def test_dsr_benchmark_field_includes_deflation() -> None:
    r = _gaussian_returns(400, 0.001, 0.01, seed=37)
    rng = np.random.default_rng(37)
    sr_est = rng.normal(0.0, 0.1, size=200)
    res = deflated_sharpe_ratio(r, sr_est, sr_benchmark=0.0)
    # Per-period benchmark = 0; deflated benchmark should be > 0.
    assert res.sr_benchmark_deflated > 0.0
    assert res.sr_benchmark_deflated == pytest.approx(res.expected_max_sr)


# ---------------------------------------------------------------------------
# DSR: input validation
# ---------------------------------------------------------------------------


def test_dsr_rejects_empty_sr_estimates() -> None:
    r = _gaussian_returns(200, 0.001, 0.01, seed=40)
    with pytest.raises(ValueError):
        deflated_sharpe_ratio(r, np.array([]))


def test_dsr_rejects_2d_sr_estimates() -> None:
    r = _gaussian_returns(200, 0.001, 0.01, seed=41)
    with pytest.raises(ValueError):
        deflated_sharpe_ratio(r, np.zeros((5, 2)))


def test_dsr_rejects_too_few_returns() -> None:
    with pytest.raises(ValueError):
        deflated_sharpe_ratio(np.array([0.01]), np.array([0.05]))