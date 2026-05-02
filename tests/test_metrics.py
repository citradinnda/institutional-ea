from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.validation.metrics import (
    BootstrapCI,
    bootstrap_metric,
    calmar_ratio,
    max_drawdown,
    profit_factor,
    sharpe_ratio,
    sortino_ratio,
    stationary_bootstrap_indices,
    tail_ratio,
)


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

def _gaussian_returns(n: int = 1000, mu: float = 0.0005, sigma: float = 0.01,
                      seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(mu, sigma, n)


# --------------------------------------------------------------------------- #
# Sharpe
# --------------------------------------------------------------------------- #

def test_sharpe_zero_for_zero_mean():
    r = np.array([0.01, -0.01, 0.01, -0.01, 0.01, -0.01])
    assert abs(sharpe_ratio(r)) < 1e-12


def test_sharpe_known_value():
    """Sharpe of a constant-mean, constant-vol Gaussian series should
    converge to mu/sigma * sqrt(periods_per_year)."""
    n = 50_000
    r = _gaussian_returns(n=n, mu=0.001, sigma=0.01, seed=42)
    expected = 0.001 / 0.01 * np.sqrt(252)  # ≈ 1.587
    assert abs(sharpe_ratio(r) - expected) < 0.05  # generous, sample noise


def test_sharpe_handles_zero_variance():
    r = np.full(100, 0.001)
    assert np.isnan(sharpe_ratio(r))


def test_sharpe_accepts_pandas_series():
    s = pd.Series(_gaussian_returns(500))
    assert np.isfinite(sharpe_ratio(s))


# --------------------------------------------------------------------------- #
# Sortino
# --------------------------------------------------------------------------- #

def test_sortino_greater_than_sharpe_for_right_skewed():
    """Right-skewed returns: positive outliers don't hurt Sortino but
    they do inflate Sharpe's denominator. Sortino > Sharpe."""
    r = _gaussian_returns(n=5000, mu=0.001, sigma=0.01, seed=0)
    r[::100] += 0.10  # inject right-tail spikes
    assert sortino_ratio(r) > sharpe_ratio(r)


def test_sortino_zero_downside_returns_nan():
    r = np.array([0.01, 0.02, 0.03, 0.04])  # all positive
    assert np.isnan(sortino_ratio(r))


# --------------------------------------------------------------------------- #
# Max drawdown
# --------------------------------------------------------------------------- #

def test_max_drawdown_known_path():
    """Equity goes 1 -> 1.2 -> 0.9 -> 1.1. Peak=1.2, trough=0.9.
    Drawdown = 0.9/1.2 - 1 = -0.25 exactly."""
    eq = np.array([1.0, 1.2, 0.9, 1.1])
    r = np.diff(eq) / eq[:-1]
    assert abs(max_drawdown(r) - (-0.25)) < 1e-12


def test_max_drawdown_is_non_positive():
    r = _gaussian_returns(2000, seed=7)
    assert max_drawdown(r) <= 0.0


def test_max_drawdown_zero_for_monotone_up():
    r = np.full(100, 0.001)
    assert max_drawdown(r) == 0.0


# --------------------------------------------------------------------------- #
# Calmar
# --------------------------------------------------------------------------- #

def test_calmar_positive_for_winning_strategy():
    r = _gaussian_returns(n=10_000, mu=0.0005, sigma=0.005, seed=11)
    assert calmar_ratio(r) > 0


# --------------------------------------------------------------------------- #
# Profit factor
# --------------------------------------------------------------------------- #

def test_profit_factor_known_value():
    r = np.array([0.02, -0.01, 0.03, -0.02])
    # gains=0.05, losses=0.03 -> 5/3
    assert abs(profit_factor(r) - (5.0 / 3.0)) < 1e-12


def test_profit_factor_inf_when_no_losses():
    assert np.isinf(profit_factor(np.array([0.01, 0.02, 0.03])))


def test_profit_factor_nan_when_all_zero():
    assert np.isnan(profit_factor(np.zeros(10)))


# --------------------------------------------------------------------------- #
# Tail ratio
# --------------------------------------------------------------------------- #

def test_tail_ratio_one_for_symmetric():
    r = _gaussian_returns(n=20_000, mu=0.0, sigma=0.01, seed=3)
    assert abs(tail_ratio(r) - 1.0) < 0.1


def test_tail_ratio_above_one_for_right_skew():
    """We inject right-tail spikes into ~10% of bars so they actually
    influence the 95th percentile (with only 1% of bars spiked, the
    upper quantile sits BELOW the injected mass and the test is blind
    to the asymmetry — that was the original bug)."""
    rng = np.random.default_rng(0)
    r = rng.normal(0, 0.01, 5000)
    spike_idx = rng.choice(5000, size=500, replace=False)
    r[spike_idx] += 0.05
    assert tail_ratio(r) > 1.2


# --------------------------------------------------------------------------- #
# Stationary bootstrap indices
# --------------------------------------------------------------------------- #

def test_bootstrap_indices_shape_and_range():
    rng = np.random.default_rng(0)
    idx = stationary_bootstrap_indices(n=100, expected_block_length=10, rng=rng)
    assert idx.shape == (100,)
    assert idx.min() >= 0
    assert idx.max() < 100


def test_bootstrap_indices_reproducible_with_seed():
    a = stationary_bootstrap_indices(100, 10, np.random.default_rng(42))
    b = stationary_bootstrap_indices(100, 10, np.random.default_rng(42))
    assert np.array_equal(a, b)


def test_bootstrap_indices_block_structure():
    """With expected_block_length=20, consecutive-index runs should
    average around 20. Loose bound to avoid flaky tests."""
    rng = np.random.default_rng(123)
    idx = stationary_bootstrap_indices(n=10_000, expected_block_length=20, rng=rng)
    # A "run" is a maximal stretch where idx[t+1] == idx[t]+1 (mod n).
    diffs = (idx[1:] - idx[:-1]) % 10_000
    restarts = int((diffs != 1).sum()) + 1  # +1 for the first block
    avg_run_len = 10_000 / restarts
    # Expected ~20; allow a wide band because of geometric variance.
    assert 10 < avg_run_len < 35


# --------------------------------------------------------------------------- #
# bootstrap_metric end-to-end
# --------------------------------------------------------------------------- #

def test_bootstrap_metric_returns_dataclass():
    r = _gaussian_returns(500, seed=1)
    ci = bootstrap_metric(
        r, sharpe_ratio, n_resamples=500, seed=1, metric_name="sharpe"
    )
    assert isinstance(ci, BootstrapCI)
    assert ci.metric_name == "sharpe"
    assert ci.confidence == 0.95
    assert ci.n_resamples == 500


def test_bootstrap_ci_brackets_point_estimate_usually():
    """The CI should contain the point estimate the vast majority of
    the time (it's not a hard guarantee for percentile bootstraps,
    but for well-behaved metrics it's overwhelmingly the case)."""
    r = _gaussian_returns(2000, mu=0.001, sigma=0.01, seed=5)
    ci = bootstrap_metric(r, sharpe_ratio, n_resamples=1000, seed=5)
    assert ci.lower <= ci.point <= ci.upper


def test_bootstrap_ci_narrows_with_more_data():
    """Larger n -> tighter CI. This is the central reason CIs matter:
    they reveal whether your sample size is paying for your conclusion."""
    small = bootstrap_metric(
        _gaussian_returns(200, seed=0), sharpe_ratio, n_resamples=500, seed=0
    )
    large = bootstrap_metric(
        _gaussian_returns(5000, seed=0), sharpe_ratio, n_resamples=500, seed=0
    )
    assert (large.upper - large.lower) < (small.upper - small.lower)


def test_bootstrap_ci_reproducible_with_seed():
    r = _gaussian_returns(500, seed=2)
    a = bootstrap_metric(r, sharpe_ratio, n_resamples=500, seed=99)
    b = bootstrap_metric(r, sharpe_ratio, n_resamples=500, seed=99)
    assert a.lower == b.lower and a.upper == b.upper and a.point == b.point


def test_bootstrap_rejects_too_few_resamples():
    r = _gaussian_returns(200, seed=0)
    with pytest.raises(ValueError):
        bootstrap_metric(r, sharpe_ratio, n_resamples=50, seed=0)


def test_bootstrap_rejects_invalid_confidence():
    r = _gaussian_returns(200, seed=0)
    with pytest.raises(ValueError):
        bootstrap_metric(r, sharpe_ratio, n_resamples=500,
                         confidence=1.5, seed=0)


def test_bootstrap_works_with_any_metric():
    """Contract test: any callable r -> float should plug in."""
    r = _gaussian_returns(1000, seed=4)
    ci_dd = bootstrap_metric(
        r, max_drawdown, n_resamples=500, seed=4, metric_name="max_dd"
    )
    assert ci_dd.metric_name == "max_dd"
    assert ci_dd.upper <= 0.0  # max_drawdown is non-positive
    assert ci_dd.lower <= ci_dd.upper


def test_bootstrap_str_format():
    r = _gaussian_returns(500, seed=0)
    ci = bootstrap_metric(r, sharpe_ratio, n_resamples=500, seed=0,
                          metric_name="sharpe")
    s = str(ci)
    assert "sharpe" in s and "95%" in s and "[" in s and "]" in s