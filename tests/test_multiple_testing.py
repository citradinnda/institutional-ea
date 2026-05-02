"""Tests for multiple-testing corrections."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import (
    MultipleTestingResult,
    benjamini_hochberg,
    bonferroni_correction,
    holm_correction,
)


# ---------------------------------------------------------------------------
# Bonferroni
# ---------------------------------------------------------------------------


def test_bonferroni_returns_frozen_dataclass() -> None:
    res = bonferroni_correction([0.01, 0.02, 0.03])
    assert isinstance(res, MultipleTestingResult)
    with pytest.raises(Exception):
        res.alpha = 0.1  # type: ignore[misc]


def test_bonferroni_adjusted_equals_k_times_raw_clipped() -> None:
    raw = np.array([0.01, 0.02, 0.5])
    res = bonferroni_correction(raw, alpha=0.05)
    expected = np.minimum(raw * 3, 1.0)
    np.testing.assert_array_almost_equal(res.p_values_adjusted, expected)


def test_bonferroni_rejects_correctly() -> None:
    """K=4, alpha=0.05 => threshold per test = 0.0125."""
    raw = [0.001, 0.01, 0.02, 0.5]
    res = bonferroni_correction(raw, alpha=0.05)
    # Adjusted = [0.004, 0.04, 0.08, 1.0]; reject where <= 0.05.
    np.testing.assert_array_equal(res.rejected, [True, True, False, False])


def test_bonferroni_metadata_fields() -> None:
    res = bonferroni_correction([0.01, 0.02, 0.03], alpha=0.05)
    assert res.method == "bonferroni"
    assert res.n_tests == 3
    assert res.alpha == 0.05


def test_bonferroni_preserves_input_order() -> None:
    """Adjusted p-values must align with the caller's ordering, not sorted."""
    raw = np.array([0.5, 0.001, 0.02])
    res = bonferroni_correction(raw)
    assert res.p_values_adjusted[1] < res.p_values_adjusted[0]
    assert res.p_values_adjusted[1] < res.p_values_adjusted[2]


# ---------------------------------------------------------------------------
# Holm
# ---------------------------------------------------------------------------


def test_holm_returns_frozen_dataclass() -> None:
    res = holm_correction([0.01, 0.02, 0.03])
    assert isinstance(res, MultipleTestingResult)
    assert res.method == "holm"


def test_holm_uniformly_at_least_as_powerful_as_bonferroni() -> None:
    """For the same p-values, Holm rejects a SUPERSET of Bonferroni's
    rejections. This is the defining property."""
    rng = np.random.default_rng(0)
    raw = rng.uniform(0, 1, size=50)
    bonf = bonferroni_correction(raw, alpha=0.05)
    holm = holm_correction(raw, alpha=0.05)
    # Holm rejects everywhere Bonferroni does.
    assert np.all(holm.rejected[bonf.rejected])


def test_holm_smallest_p_uses_full_K_multiplier() -> None:
    """The smallest p-value's adjusted form is K * p_(1) (clipped),
    same as Bonferroni for that one."""
    raw = np.array([0.001, 0.5, 0.7])
    res = holm_correction(raw, alpha=0.05)
    smallest_idx = int(np.argmin(raw))
    assert res.p_values_adjusted[smallest_idx] == pytest.approx(
        min(0.001 * 3, 1.0)
    )


def test_holm_known_example() -> None:
    """Worked example: p = [0.005, 0.01, 0.04, 0.5], alpha=0.05.
    Sorted multipliers: 4, 3, 2, 1.
    raw*mult sorted: [0.02, 0.03, 0.08, 0.5].
    cummax: [0.02, 0.03, 0.08, 0.5]. Clipped: same.
    Reject where adjusted <= 0.05 => first two only."""
    raw = [0.005, 0.01, 0.04, 0.5]
    res = holm_correction(raw, alpha=0.05)
    np.testing.assert_array_almost_equal(
        res.p_values_adjusted, [0.02, 0.03, 0.08, 0.5]
    )
    np.testing.assert_array_equal(res.rejected, [True, True, False, False])


def test_holm_monotonic_in_sorted_order() -> None:
    """Adjusted p-values, when sorted by raw p-value, must be non-decreasing."""
    rng = np.random.default_rng(1)
    raw = rng.uniform(0, 1, size=30)
    res = holm_correction(raw)
    order = np.argsort(raw)
    sorted_adj = res.p_values_adjusted[order]
    assert np.all(np.diff(sorted_adj) >= -1e-12)


# ---------------------------------------------------------------------------
# Benjamini-Hochberg
# ---------------------------------------------------------------------------


def test_bh_returns_frozen_dataclass() -> None:
    res = benjamini_hochberg([0.01, 0.02, 0.03])
    assert isinstance(res, MultipleTestingResult)
    assert res.method == "benjamini_hochberg"


def test_bh_known_example() -> None:
    """Worked example: p = [0.001, 0.008, 0.039, 0.041, 0.042], K=5,
    alpha=0.05. Threshold (i/K)*alpha = [0.01, 0.02, 0.03, 0.04, 0.05].
    Largest i with p_(i) <= threshold_i: i=5 (0.042 <= 0.05).
    => Reject all five.

    Adjusted (sorted): (K/i) * p_(i) =
        [5*0.001, 5/2*0.008, 5/3*0.039, 5/4*0.041, 5/5*0.042]
      = [0.005, 0.020, 0.065, 0.05125, 0.042]
    Reverse cummin clamps non-monotone inflation:
        [0.005, 0.020, 0.042, 0.042, 0.042]
    """
    raw = [0.001, 0.008, 0.039, 0.041, 0.042]
    res = benjamini_hochberg(raw, alpha=0.05)
    expected_adj = [0.005, 0.020, 0.042, 0.042, 0.042]
    np.testing.assert_array_almost_equal(
        res.p_values_adjusted, expected_adj, decimal=6
    )
    assert np.all(res.rejected)


def test_bh_uniformly_at_least_as_powerful_as_holm() -> None:
    """BH rejects a SUPERSET of Holm at the same alpha (FDR is more
    permissive than FWER). This is the defining trade-off."""
    rng = np.random.default_rng(2)
    raw = rng.uniform(0, 1, size=100)
    holm = holm_correction(raw, alpha=0.1)
    bh = benjamini_hochberg(raw, alpha=0.1)
    assert np.all(bh.rejected[holm.rejected])


def test_bh_monotonic_in_sorted_order() -> None:
    rng = np.random.default_rng(3)
    raw = rng.uniform(0, 1, size=40)
    res = benjamini_hochberg(raw)
    order = np.argsort(raw)
    sorted_adj = res.p_values_adjusted[order]
    assert np.all(np.diff(sorted_adj) >= -1e-12)


def test_bh_all_zeros_rejects_all() -> None:
    res = benjamini_hochberg([0.0, 0.0, 0.0, 0.0], alpha=0.05)
    assert np.all(res.rejected)
    np.testing.assert_array_equal(res.p_values_adjusted, np.zeros(4))


def test_bh_all_ones_rejects_none() -> None:
    res = benjamini_hochberg([1.0, 1.0, 1.0], alpha=0.5)
    assert not np.any(res.rejected)


# ---------------------------------------------------------------------------
# Cross-method invariants
# ---------------------------------------------------------------------------


def test_all_methods_preserve_input_order() -> None:
    raw = np.array([0.7, 0.001, 0.04, 0.5, 0.02])
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        res = fn(raw, alpha=0.05)
        np.testing.assert_array_equal(res.p_values_raw, raw)


def test_all_methods_accept_pandas_series() -> None:
    raw = pd.Series([0.01, 0.02, 0.03])
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        res = fn(raw)
        assert res.n_tests == 3


def test_all_methods_accept_lists() -> None:
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        res = fn([0.01, 0.02, 0.03])
        assert res.n_tests == 3


def test_all_methods_single_pvalue_passthrough() -> None:
    """K=1 => no correction needed; adjusted == raw."""
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        res = fn([0.03], alpha=0.05)
        assert res.p_values_adjusted[0] == pytest.approx(0.03)
        assert res.rejected[0] == True  # noqa: E712


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def test_rejects_empty_input() -> None:
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        with pytest.raises(ValueError):
            fn([])


def test_rejects_nan_pvalues() -> None:
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        with pytest.raises(ValueError):
            fn([0.01, np.nan, 0.03])


def test_rejects_out_of_range_pvalues() -> None:
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        with pytest.raises(ValueError):
            fn([0.01, 1.5, 0.03])
        with pytest.raises(ValueError):
            fn([0.01, -0.1, 0.03])


def test_rejects_bad_alpha() -> None:
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        with pytest.raises(ValueError):
            fn([0.01, 0.02], alpha=0.0)
        with pytest.raises(ValueError):
            fn([0.01, 0.02], alpha=1.0)
        with pytest.raises(ValueError):
            fn([0.01, 0.02], alpha=-0.1)


def test_rejects_2d_input() -> None:
    for fn in (bonferroni_correction, holm_correction, benjamini_hochberg):
        with pytest.raises(ValueError):
            fn(np.zeros((3, 2)))