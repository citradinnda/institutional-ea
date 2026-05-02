"""
White's Reality Check for data-snooping bias.

WHY this module exists
----------------------
When you try K candidate strategies and report the one with the highest
mean excess return, that maximum is upward-biased even if every strategy
is worthless. The classical t-test on the winner is invalid: it ignores
the K-1 strategies you discarded. White's Reality Check (White 2000)
fixes this by bootstrapping the JOINT distribution of all K mean excess
returns under the null "no strategy beats the benchmark" and asking how
often the bootstrap maximum exceeds the observed maximum.

This is the multiple-comparison companion to the Deflated Sharpe Ratio
(Phase 1.10). DSR deflates a single Sharpe; RC computes a formal p-value
on the best of many strategies. Together they catch the failure mode
that produced graveyard hypotheses H008-H010 (high-Sharpe-but-fragile
results emerging from search across many variants).

Method
------
1. Compute observed mean excess return for each of K strategies:
       d_k = mean(r_k - r_benchmark)
   The observed test statistic is V_bar = max_k d_k * sqrt(T).
2. Recenter: subtract d_k from each excess-return series, so each
   strategy's recentered series has mean ZERO. This enforces the null
   "no strategy beats the benchmark" inside the bootstrap world.
3. Stationary bootstrap (Politis-Romano 1994): draw B bootstrap samples
   of length T from the recentered MATRIX (all K columns sampled at the
   SAME time-indices to preserve cross-strategy dependence).
4. For each bootstrap b, compute V_bar_b = max_k mean(recentered_k[b]) *
   sqrt(T).
5. p-value = (1/B) * #{ b : V_bar_b >= V_bar }.

References
----------
White, H. (2000). "A Reality Check for Data Snooping."
    Econometrica, 68(5), 1097-1126.
Politis, D. N., and Romano, J. P. (1994). "The Stationary Bootstrap."
    Journal of the American Statistical Association, 89(428), 1303-1313.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

__all__ = [
    "RealityCheckResult",
    "whites_reality_check",
]


@dataclass(frozen=True)
class RealityCheckResult:
    """
    Result of White's Reality Check.

    Attributes
    ----------
    p_value : float
        Bootstrap p-value in [0, 1] for the null "no strategy in the
        candidate pool beats the benchmark on average." Small p-value
        => reject the null => the best strategy's edge is statistically
        meaningful AFTER accounting for data snooping.
    best_strategy_idx : int
        Column index of the strategy with the highest observed mean
        excess return.
    best_observed_mean_excess : float
        Per-period mean excess return of the best strategy (NOT scaled
        by sqrt(T); this is the raw mean, for human inspection).
    n_bootstrap : int
        Number of bootstrap replications performed.
    n_strategies : int
        K, number of candidate strategies tested.
    n_observations : int
        T, number of per-period observations per strategy.
    block_length : int
        Expected block length used by the stationary bootstrap. Block
        starts are geometrically distributed with mean = block_length.
    """

    p_value: float
    best_strategy_idx: int
    best_observed_mean_excess: float
    n_bootstrap: int
    n_strategies: int
    n_observations: int
    block_length: int


def _to_2d_array(returns_matrix: np.ndarray | pd.DataFrame) -> np.ndarray:
    """Coerce returns matrix to a 2D float64 numpy array.

    WHY: pandas DataFrame and numpy 2D array should be interchangeable
    at the API boundary; downstream code only needs raw values.
    """
    if isinstance(returns_matrix, pd.DataFrame):
        arr = returns_matrix.to_numpy(dtype=float)
    else:
        arr = np.asarray(returns_matrix, dtype=float)
    if arr.ndim == 1:
        # Single strategy: reshape to (T, 1). Reality Check on K=1 is
        # degenerate but well-defined (collapses to a one-sample bootstrap).
        arr = arr.reshape(-1, 1)
    if arr.ndim != 2:
        raise ValueError(
            f"returns_matrix must be 1D or 2D; got shape {arr.shape}"
        )
    return arr


def _to_1d_benchmark(
    benchmark_returns: np.ndarray | pd.Series | None,
    n_observations: int,
) -> np.ndarray:
    """Coerce benchmark to a 1D float64 numpy array of length T.

    WHY: None means "raw returns" (zero benchmark). A scalar would
    silently broadcast; we forbid it to keep the contract explicit.
    """
    if benchmark_returns is None:
        return np.zeros(n_observations, dtype=float)
    if isinstance(benchmark_returns, pd.Series):
        arr = benchmark_returns.to_numpy(dtype=float)
    else:
        arr = np.asarray(benchmark_returns, dtype=float)
    if arr.ndim != 1:
        raise ValueError(
            f"benchmark_returns must be 1D; got shape {arr.shape}"
        )
    if arr.size != n_observations:
        raise ValueError(
            f"benchmark_returns length {arr.size} != returns_matrix rows "
            f"{n_observations}"
        )
    return arr


def _stationary_bootstrap_indices(
    n_observations: int,
    block_length: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Generate one stationary-bootstrap index sequence of length T.

    WHY stationary (vs. fixed-block) bootstrap: with geometric block
    lengths the resampled series is itself stationary, which gives
    valid inference for any stationary input -- crucial because trading
    returns are autocorrelated and non-iid.

    Algorithm (Politis-Romano 1994):
    - Start at a uniformly random index in [0, T).
    - At each step, with probability p = 1/block_length, JUMP to a new
      uniformly random start; otherwise advance by 1 (mod T).
    """
    p = 1.0 / block_length
    indices = np.empty(n_observations, dtype=np.int64)
    # First draw is always uniform.
    indices[0] = rng.integers(0, n_observations)
    # Pre-draw all the "should we jump?" Bernoulli outcomes and the
    # candidate jump destinations -- vectorized for speed at large T.
    jump_mask = rng.random(n_observations - 1) < p
    jump_dests = rng.integers(0, n_observations, size=n_observations - 1)
    for t in range(1, n_observations):
        if jump_mask[t - 1]:
            indices[t] = jump_dests[t - 1]
        else:
            indices[t] = (indices[t - 1] + 1) % n_observations
    return indices


def whites_reality_check(
    returns_matrix: np.ndarray | pd.DataFrame,
    benchmark_returns: np.ndarray | pd.Series | None = None,
    n_bootstrap: int = 2000,
    block_length: int | None = None,
    random_state: int | None = None,
) -> RealityCheckResult:
    """
    White's Reality Check (White 2000) with stationary bootstrap.

    Tests the null hypothesis "no strategy in the candidate pool beats
    the benchmark on average," correcting for data snooping across the
    K candidates.

    Parameters
    ----------
    returns_matrix : array-like of shape (T, K)
        Per-period returns for K candidate strategies. Each column is
        one strategy's return series. A 1D input is treated as K=1.
    benchmark_returns : array-like of shape (T,), optional
        Per-period benchmark returns. If None, treated as zeros (i.e.
        raw returns are tested against zero, not excess returns).
    n_bootstrap : int, default 2000
        Number of bootstrap replications. Larger => more stable p-value
        but slower. 2000 is a sensible default per White (2000).
    block_length : int, optional
        Expected block length for the stationary bootstrap. Defaults to
        max(1, round(T**(1/3))), matching the Phase 1.6 metrics module.
    random_state : int, optional
        Seed for reproducibility. None => OS entropy.

    Returns
    -------
    RealityCheckResult
        Frozen dataclass. `p_value` is the proportion of bootstrap
        replications whose maximum recentered mean equals or exceeds
        the observed maximum mean excess.
    """
    if n_bootstrap < 1:
        raise ValueError("n_bootstrap must be >= 1.")

    rmat = _to_2d_array(returns_matrix)
    n_obs, n_strat = rmat.shape
    if n_obs < 2:
        raise ValueError("Reality Check needs at least 2 observations.")
    if n_strat < 1:
        raise ValueError("Need at least 1 strategy.")

    bench = _to_1d_benchmark(benchmark_returns, n_obs)

    # Excess returns: shape (T, K). We subtract benchmark column-wise.
    excess = rmat - bench[:, None]

    # Observed per-strategy mean excess returns: shape (K,).
    d_obs = excess.mean(axis=0)

    # Test statistic: V_bar = sqrt(T) * max_k d_k.
    # WHY sqrt(T) scaling: matches White's formulation and gives the
    # bootstrap distribution a finite, non-degenerate limit. The scaling
    # is monotonic so it does not affect ranking, but we keep it for
    # fidelity to the paper.
    sqrt_t = np.sqrt(n_obs)
    v_obs = sqrt_t * d_obs.max()
    best_idx = int(np.argmax(d_obs))

    # Recenter: under the null, each strategy's mean excess is zero.
    # We subtract the OBSERVED mean from each column so the recentered
    # series has empirical mean exactly zero, then bootstrap from that.
    recentered = excess - d_obs[None, :]

    # Block length default per stationary bootstrap convention (n^(1/3)).
    if block_length is None:
        bl = max(1, int(round(n_obs ** (1.0 / 3.0))))
    else:
        if block_length < 1:
            raise ValueError("block_length must be >= 1.")
        if block_length > n_obs:
            raise ValueError(
                f"block_length {block_length} > n_observations {n_obs}."
            )
        bl = int(block_length)

    rng = np.random.default_rng(random_state)

    # Bootstrap loop. We sample row-indices ONCE per replication and
    # apply them to ALL K columns, preserving cross-strategy dependence.
    n_ge = 0  # count of bootstrap reps with V_bar_b >= V_bar
    for _ in range(n_bootstrap):
        idx = _stationary_bootstrap_indices(n_obs, bl, rng)
        # Mean across time of recentered[idx, :], shape (K,).
        d_boot = recentered[idx, :].mean(axis=0)
        v_boot = sqrt_t * d_boot.max()
        if v_boot >= v_obs:
            n_ge += 1

    p_value = n_ge / n_bootstrap

    return RealityCheckResult(
        p_value=p_value,
        best_strategy_idx=best_idx,
        best_observed_mean_excess=float(d_obs[best_idx]),
        n_bootstrap=n_bootstrap,
        n_strategies=n_strat,
        n_observations=n_obs,
        block_length=bl,
    )