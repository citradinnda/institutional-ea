"""Tests for White's Reality Check."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import RealityCheckResult, whites_reality_check


def _gaussian_matrix(
    n_obs: int, n_strat: int, mu: float, sigma: float, seed: int
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(loc=mu, scale=sigma, size=(n_obs, n_strat))


# ---------------------------------------------------------------------------
# Structural / API tests
# ---------------------------------------------------------------------------


def test_rc_returns_frozen_dataclass() -> None:
    rmat = _gaussian_matrix(200, 5, mu=0.0, sigma=0.01, seed=1)
    res = whites_reality_check(rmat, n_bootstrap=200, random_state=1)
    assert isinstance(res, RealityCheckResult)
    with pytest.raises(Exception):
        res.p_value = 0.0  # type: ignore[misc]


def test_rc_p_value_in_unit_interval() -> None:
    rmat = _gaussian_matrix(200, 10, mu=0.0, sigma=0.01, seed=2)
    res = whites_reality_check(rmat, n_bootstrap=500, random_state=2)
    assert 0.0 <= res.p_value <= 1.0


def test_rc_reports_correct_best_index() -> None:
    """The strategy with the largest mean must be flagged as best."""
    rmat = _gaussian_matrix(300, 5, mu=0.0, sigma=0.01, seed=3)
    # Inject a strong winner at column 2.
    rmat[:, 2] += 0.005
    res = whites_reality_check(rmat, n_bootstrap=200, random_state=3)
    assert res.best_strategy_idx == 2


def test_rc_metadata_fields() -> None:
    rmat = _gaussian_matrix(150, 7, mu=0.0, sigma=0.01, seed=4)
    res = whites_reality_check(rmat, n_bootstrap=300, random_state=4)
    assert res.n_bootstrap == 300
    assert res.n_strategies == 7
    assert res.n_observations == 150
    assert res.block_length >= 1


def test_rc_default_block_length_is_cube_root() -> None:
    """T^(1/3) convention, matches Phase 1.6 metrics."""
    n_obs = 1000  # cube root ~= 10
    rmat = _gaussian_matrix(n_obs, 3, mu=0.0, sigma=0.01, seed=5)
    res = whites_reality_check(rmat, n_bootstrap=100, random_state=5)
    assert res.block_length == round(n_obs ** (1.0 / 3.0))


# ---------------------------------------------------------------------------
# Statistical sanity tests
# ---------------------------------------------------------------------------


def test_rc_high_p_value_under_null() -> None:
    """Pure noise => no strategy beats zero benchmark => p-value should
    NOT be small. We allow a generous band (>0.05) to keep the test
    deterministic across random seeds."""
    rmat = _gaussian_matrix(500, 20, mu=0.0, sigma=0.01, seed=10)
    res = whites_reality_check(rmat, n_bootstrap=500, random_state=10)
    assert res.p_value > 0.05


def test_rc_low_p_value_with_strong_real_edge() -> None:
    """A strategy with a clear positive mean should drive p-value low."""
    rmat = _gaussian_matrix(500, 5, mu=0.0, sigma=0.01, seed=11)
    rmat[:, 0] += 0.003  # strong real edge in column 0
    res = whites_reality_check(rmat, n_bootstrap=500, random_state=11)
    assert res.p_value < 0.05


def test_rc_more_strategies_inflate_p_value() -> None:
    """Adding noise strategies should NOT make the p-value smaller --
    this is the whole point of correcting for data snooping. The best
    strategy is the same; only the candidate pool grows."""
    rng = np.random.default_rng(12)
    base = rng.normal(0.0005, 0.01, size=(500, 1))  # weak real edge
    noise = rng.normal(0.0, 0.01, size=(500, 50))
    small_pool = base
    big_pool = np.hstack([base, noise])
    p_small = whites_reality_check(
        small_pool, n_bootstrap=500, random_state=12
    ).p_value
    p_big = whites_reality_check(
        big_pool, n_bootstrap=500, random_state=12
    ).p_value
    # Big pool's p-value should be >= small pool's (allow tiny slack
    # for bootstrap noise; the inequality is the structural claim).
    assert p_big >= p_small - 0.02


def test_rc_benchmark_subtraction_changes_result() -> None:
    """Passing a non-zero benchmark must change the answer vs. zero."""
    rng = np.random.default_rng(13)
    rmat = rng.normal(0.001, 0.01, size=(400, 5))
    bench = rng.normal(0.0008, 0.005, size=400)
    res_zero = whites_reality_check(rmat, n_bootstrap=200, random_state=13)
    res_bench = whites_reality_check(
        rmat, benchmark_returns=bench, n_bootstrap=200, random_state=13
    )
    # Different observed best mean excess => different p-value.
    assert res_zero.best_observed_mean_excess != pytest.approx(
        res_bench.best_observed_mean_excess
    )


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------


def test_rc_same_seed_gives_same_p_value() -> None:
    rmat = _gaussian_matrix(300, 8, mu=0.0, sigma=0.01, seed=20)
    a = whites_reality_check(rmat, n_bootstrap=500, random_state=42)
    b = whites_reality_check(rmat, n_bootstrap=500, random_state=42)
    assert a.p_value == b.p_value


def test_rc_different_seeds_can_differ() -> None:
    """Different seeds should generally give different p-values
    (allowing the rare coincidence)."""
    rmat = _gaussian_matrix(300, 8, mu=0.0, sigma=0.01, seed=21)
    a = whites_reality_check(rmat, n_bootstrap=500, random_state=1)
    b = whites_reality_check(rmat, n_bootstrap=500, random_state=2)
    c = whites_reality_check(rmat, n_bootstrap=500, random_state=3)
    # At least one pair must differ.
    assert not (a.p_value == b.p_value == c.p_value)


# ---------------------------------------------------------------------------
# Input flexibility
# ---------------------------------------------------------------------------


def test_rc_accepts_pandas_dataframe() -> None:
    rmat = _gaussian_matrix(200, 4, mu=0.0, sigma=0.01, seed=30)
    df = pd.DataFrame(rmat, columns=["s1", "s2", "s3", "s4"])
    res = whites_reality_check(df, n_bootstrap=200, random_state=30)
    assert res.n_strategies == 4


def test_rc_accepts_pandas_series_benchmark() -> None:
    rmat = _gaussian_matrix(200, 3, mu=0.0, sigma=0.01, seed=31)
    bench = pd.Series(np.zeros(200))
    res = whites_reality_check(
        rmat, benchmark_returns=bench, n_bootstrap=200, random_state=31
    )
    assert 0.0 <= res.p_value <= 1.0


def test_rc_accepts_1d_input_as_single_strategy() -> None:
    rng = np.random.default_rng(32)
    r = rng.normal(0.0, 0.01, size=200)
    res = whites_reality_check(r, n_bootstrap=200, random_state=32)
    assert res.n_strategies == 1
    assert res.best_strategy_idx == 0


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def test_rc_rejects_too_few_observations() -> None:
    with pytest.raises(ValueError):
        whites_reality_check(np.array([[0.01, 0.02]]), n_bootstrap=10)


def test_rc_rejects_zero_bootstrap() -> None:
    rmat = _gaussian_matrix(100, 3, 0.0, 0.01, seed=40)
    with pytest.raises(ValueError):
        whites_reality_check(rmat, n_bootstrap=0)


def test_rc_rejects_bad_block_length() -> None:
    rmat = _gaussian_matrix(100, 3, 0.0, 0.01, seed=41)
    with pytest.raises(ValueError):
        whites_reality_check(rmat, n_bootstrap=10, block_length=0)
    with pytest.raises(ValueError):
        whites_reality_check(rmat, n_bootstrap=10, block_length=200)


def test_rc_rejects_mismatched_benchmark_length() -> None:
    rmat = _gaussian_matrix(100, 3, 0.0, 0.01, seed=42)
    with pytest.raises(ValueError):
        whites_reality_check(
            rmat, benchmark_returns=np.zeros(50), n_bootstrap=10
        )


def test_rc_rejects_3d_input() -> None:
    with pytest.raises(ValueError):
        whites_reality_check(np.zeros((10, 5, 2)), n_bootstrap=10)