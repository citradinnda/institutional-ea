"""
Multiple-testing corrections: Bonferroni, Holm, Benjamini-Hochberg.

WHY this module exists
----------------------
When you run K hypothesis tests at level alpha each, the probability
that AT LEAST ONE of them is a false positive is much larger than alpha
(approximately 1 - (1-alpha)^K for independent tests). This is the
"family-wise error" problem. Without correction, with K=20 and alpha=0.05
you have a 64% chance of at least one false discovery even when every
null is true.

This module provides three corrections, in order of increasing power
(and decreasing strictness):

  Bonferroni       -- FWER control. Reject p_i if p_i <= alpha / K.
                      Simplest, most conservative.
  Holm-Bonferroni  -- FWER control. Step-down: sort p-values ascending,
                      reject p_(i) if p_(i) <= alpha / (K - i + 1).
                      Uniformly more powerful than Bonferroni.
  Benjamini-       -- FDR control. Step-up: sort p-values ascending,
  Hochberg            find largest i with p_(i) <= (i/K)*alpha, reject
                      all p_(j) for j <= i. Controls EXPECTED false
                      discovery PROPORTION, not family-wise error.

FWER vs FDR -- which to pick?
    FWER (Bonferroni, Holm): "I want at most alpha probability of ANY
        false positive." Strict. Use when even one false positive is
        catastrophic (e.g. greenlighting a strategy for live trading).
    FDR (BH): "I want at most alpha PROPORTION of my discoveries to
        be false." Permissive. Use for screening / exploration where
        a few false positives are tolerable in exchange for power.

For this project: Bonferroni or Holm for the final go/no-go gate on a
candidate strategy. BH for early-stage feature screening.

References
----------
Bonferroni, C. E. (1936). "Teoria statistica delle classi e calcolo
    delle probabilita."
Holm, S. (1979). "A Simple Sequentially Rejective Multiple Test
    Procedure." Scandinavian Journal of Statistics, 6(2), 65-70.
Benjamini, Y., and Hochberg, Y. (1995). "Controlling the False
    Discovery Rate: A Practical and Powerful Approach to Multiple
    Testing." Journal of the Royal Statistical Society B, 57(1),
    289-300.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

__all__ = [
    "MultipleTestingResult",
    "bonferroni_correction",
    "holm_correction",
    "benjamini_hochberg",
]


@dataclass(frozen=True)
class MultipleTestingResult:
    """
    Result of a multiple-testing correction.

    Attributes
    ----------
    p_values_raw : np.ndarray
        Original (unadjusted) p-values, shape (K,), order preserved
        from the input.
    p_values_adjusted : np.ndarray
        Adjusted p-values, shape (K,), order preserved from the input.
        Compare these directly to alpha to make accept/reject decisions
        without re-running the correction.
    rejected : np.ndarray
        Boolean array, shape (K,), True where the null is rejected at
        level `alpha`. Equivalent to `p_values_adjusted <= alpha` for
        all three methods implemented here.
    alpha : float
        Significance level used for the rejection decisions.
    method : str
        Identifier: "bonferroni", "holm", or "benjamini_hochberg".
    n_tests : int
        Number of tests, K.
    """

    p_values_raw: np.ndarray
    p_values_adjusted: np.ndarray
    rejected: np.ndarray
    alpha: float
    method: str
    n_tests: int


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _to_1d_pvalues(p_values: np.ndarray | pd.Series | list[float]) -> np.ndarray:
    """Coerce to a 1D float64 numpy array and validate range.

    WHY: a stray NaN or out-of-range p-value silently corrupts the
    adjusted output. Better to fail loudly at the boundary.
    """
    if isinstance(p_values, pd.Series):
        arr = p_values.to_numpy(dtype=float)
    else:
        arr = np.asarray(p_values, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"p_values must be 1D; got shape {arr.shape}")
    if arr.size == 0:
        raise ValueError("p_values must not be empty.")
    if np.any(np.isnan(arr)):
        raise ValueError("p_values must not contain NaN.")
    if np.any(arr < 0.0) or np.any(arr > 1.0):
        raise ValueError("p_values must lie in [0, 1].")
    return arr


def _validate_alpha(alpha: float) -> None:
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"alpha must be in (0, 1) strict; got {alpha}.")


# ---------------------------------------------------------------------------
# Bonferroni
# ---------------------------------------------------------------------------


def bonferroni_correction(
    p_values: np.ndarray | pd.Series | list[float],
    alpha: float = 0.05,
) -> MultipleTestingResult:
    """
    Bonferroni correction. Controls Family-Wise Error Rate (FWER).

    Adjusted p-value: p_adj_i = min(K * p_i, 1.0).
    Reject null i iff p_adj_i <= alpha (equivalently, p_i <= alpha / K).

    WHY clip at 1.0: probabilities cannot exceed 1. Clipping makes the
    adjusted values directly comparable to alpha without surprises.

    Parameters
    ----------
    p_values : array-like of shape (K,)
        Raw p-values in [0, 1].
    alpha : float, default 0.05
        Significance level for the rejection decisions, in (0, 1).

    Returns
    -------
    MultipleTestingResult
    """
    _validate_alpha(alpha)
    raw = _to_1d_pvalues(p_values)
    k = raw.size
    adjusted = np.minimum(raw * k, 1.0)
    rejected = adjusted <= alpha
    return MultipleTestingResult(
        p_values_raw=raw,
        p_values_adjusted=adjusted,
        rejected=rejected,
        alpha=alpha,
        method="bonferroni",
        n_tests=k,
    )


# ---------------------------------------------------------------------------
# Holm-Bonferroni
# ---------------------------------------------------------------------------


def holm_correction(
    p_values: np.ndarray | pd.Series | list[float],
    alpha: float = 0.05,
) -> MultipleTestingResult:
    """
    Holm-Bonferroni step-down correction. Controls FWER.

    Algorithm:
        1. Sort p-values ascending: p_(1) <= p_(2) <= ... <= p_(K).
        2. Reject p_(i) iff p_(j) <= alpha / (K - j + 1) for all j <= i.
        3. Equivalently, adjusted p_(i) = max over j <= i of
           (K - j + 1) * p_(j), clipped to 1.0. This monotone form
           guarantees adjusted p-values are non-decreasing in sorted
           order and lets callers compare directly to alpha.

    WHY "step-down": once we fail to reject at position i, we accept
    everything from i onward. This sequential structure is what makes
    Holm uniformly more powerful than Bonferroni at the same FWER.

    Parameters
    ----------
    p_values : array-like of shape (K,)
        Raw p-values in [0, 1].
    alpha : float, default 0.05
        Significance level, in (0, 1).

    Returns
    -------
    MultipleTestingResult
    """
    _validate_alpha(alpha)
    raw = _to_1d_pvalues(p_values)
    k = raw.size

    # Sort indices ascending by p-value; remember original positions
    # so we can return adjusted p-values in the caller's order.
    order = np.argsort(raw, kind="stable")
    sorted_p = raw[order]

    # Step-down adjusted p-values in sorted order:
    # adj_(i) = max( (K - j + 1) * p_(j) for j <= i ), clipped to 1.
    # Using j = 1..K (1-indexed) => multiplier = (K - j + 1).
    multipliers = np.arange(k, 0, -1, dtype=float)  # K, K-1, ..., 1
    raw_adj_sorted = sorted_p * multipliers
    # Cumulative max enforces monotone non-decreasing adjusted p-values,
    # which is what makes the "compare to alpha" shortcut valid.
    monotone_sorted = np.maximum.accumulate(raw_adj_sorted)
    adjusted_sorted = np.minimum(monotone_sorted, 1.0)

    # Un-sort back to caller's order.
    adjusted = np.empty_like(adjusted_sorted)
    adjusted[order] = adjusted_sorted
    rejected = adjusted <= alpha

    return MultipleTestingResult(
        p_values_raw=raw,
        p_values_adjusted=adjusted,
        rejected=rejected,
        alpha=alpha,
        method="holm",
        n_tests=k,
    )


# ---------------------------------------------------------------------------
# Benjamini-Hochberg
# ---------------------------------------------------------------------------


def benjamini_hochberg(
    p_values: np.ndarray | pd.Series | list[float],
    alpha: float = 0.05,
) -> MultipleTestingResult:
    """
    Benjamini-Hochberg step-up procedure. Controls False Discovery Rate.

    Algorithm:
        1. Sort p-values ascending: p_(1) <= ... <= p_(K).
        2. Find the largest i such that p_(i) <= (i / K) * alpha.
        3. Reject all p_(j) for j <= i.
        4. Adjusted p_(i) = min over j >= i of (K / j) * p_(j), clipped
           to 1.0. The reverse-cumulative-min enforces monotonicity in
           sorted order; comparing adjusted to alpha then matches the
           original step-up rule.

    WHY "step-up" (vs Holm's step-down): BH walks from the LARGEST
    p-value down, looking for the first one that passes the threshold;
    once found, EVERYTHING below it is rejected. This is what gives BH
    much higher power than FWER methods at the cost of allowing a
    bounded EXPECTED PROPORTION of false discoveries (rather than zero
    false-discovery probability).

    FDR vs FWER: BH controls E[V/R] (false discoveries over total
    discoveries). With alpha=0.05 and 100 rejections, you expect ~5
    false. FWER methods control P(V >= 1) instead -- much stricter.

    Parameters
    ----------
    p_values : array-like of shape (K,)
        Raw p-values in [0, 1].
    alpha : float, default 0.05
        FDR control level, in (0, 1).

    Returns
    -------
    MultipleTestingResult
    """
    _validate_alpha(alpha)
    raw = _to_1d_pvalues(p_values)
    k = raw.size

    order = np.argsort(raw, kind="stable")
    sorted_p = raw[order]

    # Adjusted p-values in sorted order:
    #   adj_(i) = min over j >= i of (K / j) * p_(j), clipped to 1.
    # We compute (K/j)*p_(j) for j=1..K, then take a reverse-cumulative
    # minimum so that adj is non-decreasing in sorted order.
    ranks = np.arange(1, k + 1, dtype=float)
    raw_adj_sorted = sorted_p * (k / ranks)
    # Reverse cumulative min: walk from the end backwards.
    rev_cummin = np.minimum.accumulate(raw_adj_sorted[::-1])[::-1]
    adjusted_sorted = np.minimum(rev_cummin, 1.0)

    adjusted = np.empty_like(adjusted_sorted)
    adjusted[order] = adjusted_sorted
    rejected = adjusted <= alpha

    return MultipleTestingResult(
        p_values_raw=raw,
        p_values_adjusted=adjusted,
        rejected=rejected,
        alpha=alpha,
        method="benjamini_hochberg",
        n_tests=k,
    )