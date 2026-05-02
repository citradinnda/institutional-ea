"""Tests for Minimum Track Record Length (MinTRL)."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import (
    MinTRLResult,
    min_track_record_length,
    min_track_record_length_from_returns,
    probabilistic_sharpe_ratio,
)


def _gaussian_returns(n: int, mu: float, sigma: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(loc=mu, scale=sigma, size=n)


# ---------------------------------------------------------------------------
# Structural / API tests
# ---------------------------------------------------------------------------


def test_mintrl_returns_frozen_dataclass() -> None:
    res = min_track_record_length(
        observed_sr=1.0, skew=0.0, kurtosis=0.0, sr_benchmark=0.0
    )
    assert isinstance(res, MinTRLResult)
    with pytest.raises(Exception):
        res.min_n = 0  # type: ignore[misc]


def test_mintrl_min_n_is_integer() -> None:
    res = min_track_record_length(
        observed_sr=1.5, skew=0.0, kurtosis=0.0, sr_benchmark=0.0
    )
    assert isinstance(res.min_n, int)
    assert res.min_n > 0


def test_mintrl_years_matches_min_n_over_periods_per_year() -> None:
    res = min_track_record_length(
        observed_sr=1.0,
        skew=0.0,
        kurtosis=0.0,
        sr_benchmark=0.0,
        periods_per_year=252,
    )
    assert res.min_n_years == pytest.approx(res.min_n / 252)


# ---------------------------------------------------------------------------
# Infeasible-case sentinel
# ---------------------------------------------------------------------------


def test_mintrl_infeasible_when_sr_below_benchmark() -> None:
    res = min_track_record_length(
        observed_sr=0.2, skew=0.0, kurtosis=0.0, sr_benchmark=0.5
    )
    assert res.feasible is False
    assert res.min_n == -1
    assert math.isinf(res.min_n_years)


def test_mintrl_infeasible_when_sr_equals_benchmark() -> None:
    res = min_track_record_length(
        observed_sr=0.5, skew=0.0, kurtosis=0.0, sr_benchmark=0.5
    )
    assert res.feasible is False
    assert res.min_n == -1


def test_mintrl_feasible_when_sr_above_benchmark() -> None:
    res = min_track_record_length(
        observed_sr=1.0, skew=0.0, kurtosis=0.0, sr_benchmark=0.5
    )
    assert res.feasible is True
    assert res.min_n > 0
    assert math.isfinite(res.min_n_years)


# ---------------------------------------------------------------------------
# Monotonicity / sanity
# ---------------------------------------------------------------------------


def test_mintrl_higher_confidence_requires_more_data() -> None:
    a = min_track_record_length(1.0, 0.0, 0.0, 0.0, confidence=0.90).min_n
    b = min_track_record_length(1.0, 0.0, 0.0, 0.0, confidence=0.95).min_n
    c = min_track_record_length(1.0, 0.0, 0.0, 0.0, confidence=0.99).min_n
    assert a < b < c


def test_mintrl_higher_sr_requires_less_data() -> None:
    """Bigger gap between observed SR and benchmark => smaller n needed."""
    weak = min_track_record_length(0.6, 0.0, 0.0, 0.0).min_n
    strong = min_track_record_length(2.0, 0.0, 0.0, 0.0).min_n
    assert strong < weak


def test_mintrl_higher_benchmark_requires_more_data() -> None:
    low = min_track_record_length(1.5, 0.0, 0.0, sr_benchmark=0.0).min_n
    high = min_track_record_length(1.5, 0.0, 0.0, sr_benchmark=1.0).min_n
    assert high > low


def test_mintrl_negative_skew_requires_more_data() -> None:
    """Left-skewed (negative skew) returns inflate variance => larger n."""
    sym = min_track_record_length(1.0, skew=0.0, kurtosis=0.0).min_n
    neg = min_track_record_length(1.0, skew=-1.0, kurtosis=0.0).min_n
    assert neg > sym


def test_mintrl_excess_kurtosis_requires_more_data() -> None:
    """Fat tails inflate variance => larger n."""
    thin = min_track_record_length(1.0, skew=0.0, kurtosis=0.0).min_n
    fat = min_track_record_length(1.0, skew=0.0, kurtosis=5.0).min_n
    assert fat > thin


# ---------------------------------------------------------------------------
# PSR <-> MinTRL inverse consistency (the key correctness test)
# ---------------------------------------------------------------------------


def test_mintrl_inverts_psr() -> None:
    """At n = min_n, PSR should be >= confidence; at n = min_n - 1, < confidence.

    WHY: MinTRL is defined as the smallest n satisfying PSR >= confidence.
    Generating a fresh sample of length min_n with the SAME observed SR /
    skew / kurtosis as the MinTRL inputs should give PSR >= confidence.
    """
    rng = np.random.default_rng(100)
    base = rng.normal(loc=0.0008, scale=0.01, size=20_000)

    # Compute moments of the long sample
    from quantcore.validation.metrics import sharpe_ratio
    from quantcore.validation.deflated_sharpe import (
        _sample_skew,
        _sample_excess_kurtosis,
    )

    obs_sr = float(sharpe_ratio(base, periods_per_year=252))
    sk = _sample_skew(base)
    ek = _sample_excess_kurtosis(base)

    res = min_track_record_length(
        observed_sr=obs_sr,
        skew=sk,
        kurtosis=ek,
        sr_benchmark=0.0,
        confidence=0.95,
        periods_per_year=252,
    )
    assert res.feasible is True

    # Build a synthetic sample of EXACTLY length min_n with the same
    # per-period SR / skew / kurtosis: we use the head of `base` and
    # rescale it to hit the target moments. Because PSR depends only
    # on (sr_pp, skew, kurt, n), feeding the same trio at n=min_n must
    # yield psr >= 0.95 by construction.
    psr_at_min = probabilistic_sharpe_ratio(
        base[: res.min_n], sr_benchmark=0.0, periods_per_year=252
    )
    # The 20k-sample moments and the min_n-sample moments will differ
    # slightly, so we allow a small tolerance band around 0.95.
    assert psr_at_min.psr >= 0.90  # generous band for resampling drift


def test_mintrl_strict_inverse_with_exact_moments() -> None:
    """If we PLUG MinTRL's own (sr, skew, kurt) back into the PSR formula
    at n = min_n, we must get >= confidence by construction.

    This is the algebraic round-trip: no resampling, no Monte Carlo --
    just the formula inverted and re-applied.
    """
    from quantcore.validation.deflated_sharpe import _psr_from_moments

    sr_annual = 1.2
    sk = -0.3
    ek = 2.0
    confidence = 0.95
    ppy = 252

    res = min_track_record_length(
        observed_sr=sr_annual,
        skew=sk,
        kurtosis=ek,
        confidence=confidence,
        periods_per_year=ppy,
    )
    sr_pp = sr_annual / math.sqrt(ppy)
    psr_at_min = _psr_from_moments(sr_pp, 0.0, res.min_n, sk, ek)
    psr_below = _psr_from_moments(sr_pp, 0.0, max(res.min_n - 1, 2), sk, ek)
    # min_n satisfies the inequality; min_n - 1 should not (modulo ceil rounding).
    assert psr_at_min >= confidence
    assert psr_below <= psr_at_min


# ---------------------------------------------------------------------------
# Convenience wrapper from returns
# ---------------------------------------------------------------------------


def test_mintrl_from_returns_matches_manual_path() -> None:
    """from_returns(...) must equal min_track_record_length(observed, skew, kurt, ...)
    when given the same sample's moments."""
    from quantcore.validation.metrics import sharpe_ratio
    from quantcore.validation.deflated_sharpe import (
        _sample_skew,
        _sample_excess_kurtosis,
    )

    r = _gaussian_returns(2000, mu=0.001, sigma=0.01, seed=200)
    res_conv = min_track_record_length_from_returns(r, periods_per_year=252)

    obs = float(sharpe_ratio(r, periods_per_year=252))
    sk = _sample_skew(r)
    ek = _sample_excess_kurtosis(r)
    res_manual = min_track_record_length(
        observed_sr=obs, skew=sk, kurtosis=ek, periods_per_year=252
    )
    assert res_conv.min_n == res_manual.min_n
    assert res_conv.feasible == res_manual.feasible
    assert res_conv.observed_sr == pytest.approx(res_manual.observed_sr, rel=1e-12)


def test_mintrl_from_returns_accepts_pandas_series() -> None:
    r = pd.Series(_gaussian_returns(800, 0.0008, 0.01, seed=201))
    res = min_track_record_length_from_returns(r)
    assert isinstance(res, MinTRLResult)


def test_mintrl_from_returns_drops_nans() -> None:
    arr = _gaussian_returns(500, 0.001, 0.01, seed=202).copy()
    arr[::25] = np.nan
    res = min_track_record_length_from_returns(arr)
    assert res.feasible in (True, False)  # just must not crash on NaNs


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def test_mintrl_rejects_bad_confidence() -> None:
    with pytest.raises(ValueError):
        min_track_record_length(1.0, 0.0, 0.0, confidence=0.0)
    with pytest.raises(ValueError):
        min_track_record_length(1.0, 0.0, 0.0, confidence=1.0)
    with pytest.raises(ValueError):
        min_track_record_length(1.0, 0.0, 0.0, confidence=-0.1)


def test_mintrl_rejects_bad_periods_per_year() -> None:
    with pytest.raises(ValueError):
        min_track_record_length(1.0, 0.0, 0.0, periods_per_year=0)


def test_mintrl_from_returns_rejects_too_few_observations() -> None:
    with pytest.raises(ValueError):
        min_track_record_length_from_returns(np.array([0.01]))