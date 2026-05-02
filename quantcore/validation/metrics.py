from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np
import pandas as pd

# Annualization factors. We expose a default for daily returns
# (the most common research timeframe) but every metric accepts
# `periods_per_year` so the same code works for H4, H1, M15, etc.
TRADING_DAYS_PER_YEAR = 252


# --------------------------------------------------------------------------- #
# Result containers
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class BootstrapCI:
    """A point estimate paired with its bootstrap confidence interval.

    Why a dataclass and not a tuple: when this gets logged into MLflow
    or written to a hypothesis YAML in `governance/hypotheses/`, the
    field names must be self-describing. (Sharpe, 0.6, 3.4) is opaque.
    BootstrapCI(point=2.1, lower=0.6, upper=3.4, ...) is auditable.
    """

    point: float
    lower: float
    upper: float
    confidence: float          # e.g. 0.95
    n_resamples: int
    expected_block_length: float
    metric_name: str

    def __str__(self) -> str:
        return (
            f"{self.metric_name} = {self.point:.4f} "
            f"[{self.lower:.4f}, {self.upper:.4f}] "
            f"({int(self.confidence * 100)}% CI, "
            f"n={self.n_resamples}, block≈{self.expected_block_length:.1f})"
        )


# --------------------------------------------------------------------------- #
# Input normalization
# --------------------------------------------------------------------------- #

def _to_numpy_returns(returns: pd.Series | np.ndarray | Sequence[float]) -> np.ndarray:
    """Normalize a returns input to a 1-D float64 ndarray, dropping NaNs.

    Why drop NaNs here: a NaN return is ambiguous (no trade? missing bar?
    flat day?). Each metric would otherwise have to handle NaNs the same
    way; centralizing it here avoids inconsistency.
    """
    if isinstance(returns, pd.Series):
        arr = returns.to_numpy(dtype=float, copy=False)
    else:
        arr = np.asarray(returns, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"returns must be 1-D, got shape {arr.shape}")
    arr = arr[~np.isnan(arr)]
    return arr


# --------------------------------------------------------------------------- #
# Point-estimate metrics
# --------------------------------------------------------------------------- #

def sharpe_ratio(
    returns: pd.Series | np.ndarray,
    *,
    risk_free: float = 0.0,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """Annualized Sharpe ratio.

    `risk_free` is the per-period risk-free rate (already in the same
    frequency as `returns`). For research with sub-daily bars this is
    almost always 0 — the relevant alternative is "do nothing," which
    earns the broker's overnight rate, ≈0 over the bar.
    """
    r = _to_numpy_returns(returns)
    if len(r) < 2:
        return float("nan")
    excess = r - risk_free
    std = excess.std(ddof=1)
    # Why a tolerance instead of `== 0`: numpy's std on a constant
    # array returns ~1e-19, not exact zero, due to two-pass cancellation.
    # 1e-12 is well below any economically meaningful per-period vol
    # (USDJPY 1-min realized vol is ~1e-4 even on quiet sessions).
    if not np.isfinite(std) or std < 1e-12:
        return float("nan")
    return float(excess.mean() / std * np.sqrt(periods_per_year))


def sortino_ratio(
    returns: pd.Series | np.ndarray,
    *,
    target: float = 0.0,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """Annualized Sortino ratio: penalises only downside deviation.

    Why this matters for the project: the H011–H014 strategies had
    Sortino significantly above Sharpe, indicating asymmetric upside.
    That asymmetry is exactly what we want to measure and protect.
    """
    r = _to_numpy_returns(returns)
    if len(r) < 2:
        return float("nan")
    downside = np.minimum(r - target, 0.0)
    # Use mean of squared downside (NOT std of downside subset) — this is
    # the canonical Sortino denominator, equivalent to a target-semideviation.
    dd = np.sqrt(np.mean(downside**2))
    if not np.isfinite(dd) or dd < 1e-12:
        return float("nan")
    return float((r.mean() - target) / dd * np.sqrt(periods_per_year))


def max_drawdown(returns: pd.Series | np.ndarray) -> float:
    """Maximum peak-to-trough drawdown of the cumulative return curve.

    Returned as a NEGATIVE number (e.g. -0.1943 for the H016 graveyard
    entry's -19.43% breach). Negative-as-loss is the convention used
    throughout the project so signs always agree across metrics.
    """
    r = _to_numpy_returns(returns)
    if len(r) == 0:
        return float("nan")
    equity = np.cumprod(1.0 + r)
    peaks = np.maximum.accumulate(equity)
    dd = equity / peaks - 1.0
    return float(dd.min())


def calmar_ratio(
    returns: pd.Series | np.ndarray,
    *,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """Annualized return divided by absolute max drawdown.

    Calmar is intuitive ("how many years of returns does my worst
    drawdown cost me?") and is the metric the eventual VPS dashboard
    will display most prominently. Drawdown is the thing that ends
    careers, so it deserves to be in the denominator of the headline.
    """
    r = _to_numpy_returns(returns)
    if len(r) < 2:
        return float("nan")
    ann_return = (1.0 + r.mean()) ** periods_per_year - 1.0
    mdd = abs(max_drawdown(r))
    if mdd == 0 or not np.isfinite(mdd):
        return float("nan")
    return float(ann_return / mdd)


def profit_factor(returns: pd.Series | np.ndarray) -> float:
    """Sum of positive returns divided by absolute sum of negative returns.

    Independent of sample size in a way Sharpe is not — useful for
    comparing strategies that trade at very different frequencies.
    """
    r = _to_numpy_returns(returns)
    if len(r) == 0:
        return float("nan")
    gains = r[r > 0].sum()
    losses = -r[r < 0].sum()
    if losses == 0:
        return float("inf") if gains > 0 else float("nan")
    return float(gains / losses)


def tail_ratio(
    returns: pd.Series | np.ndarray,
    *,
    upper_q: float = 0.95,
    lower_q: float = 0.05,
) -> float:
    """Ratio of the upper-tail return magnitude to the lower-tail magnitude.

    >1 means right-tail dominant (good — big wins outsize big losses).
    <1 means left-tail dominant (the H008–H010 disaster signature:
    high Sharpe paired with a fat left tail that eats you alive).
    """
    r = _to_numpy_returns(returns)
    if len(r) == 0:
        return float("nan")
    hi = np.quantile(r, upper_q)
    lo = np.quantile(r, lower_q)
    if lo == 0 or not np.isfinite(lo):
        return float("nan")
    return float(abs(hi) / abs(lo))


# --------------------------------------------------------------------------- #
# Stationary bootstrap (Politis & Romano 1994)
# --------------------------------------------------------------------------- #

def _politis_white_block_length(n: int) -> float:
    """Default expected block length when caller doesn't specify one.

    Uses the simple n^(1/3) rule, which is the asymptotic optimal rate
    (up to a constant) for the stationary bootstrap. The Politis-White
    automatic data-driven rule is more accurate but adds dependencies
    we don't want yet. n^(1/3) is the documented compromise.
    """
    return max(1.0, float(n) ** (1.0 / 3.0))


def stationary_bootstrap_indices(
    n: int,
    expected_block_length: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate one bootstrap resample's worth of indices into [0, n).

    Algorithm (Politis & Romano 1994):
      1. Start at a uniform-random index in [0, n).
      2. With probability p = 1/expected_block_length, restart at a
         new uniform-random index. Otherwise advance by 1 (mod n).
      3. Repeat for n steps.

    The resulting block lengths are geometrically distributed with
    mean = expected_block_length, which makes the bootstrap
    *stationary* (the joint distribution of any resample is invariant
    to time-shifts), hence the name.

    Why mod n (circular wraparound): without it, blocks starting near
    the end of the series would be systematically truncated, biasing
    estimates that depend on the tails (which is most of them).
    """
    if expected_block_length < 1.0:
        raise ValueError(
            f"expected_block_length must be >= 1, got {expected_block_length}"
        )
    p = 1.0 / expected_block_length
    idx = np.empty(n, dtype=np.int64)
    idx[0] = rng.integers(0, n)
    # Vectorize the restart decisions for speed.
    restarts = rng.random(n - 1) < p
    fresh_starts = rng.integers(0, n, size=n - 1)
    for t in range(1, n):
        if restarts[t - 1]:
            idx[t] = fresh_starts[t - 1]
        else:
            idx[t] = (idx[t - 1] + 1) % n
    return idx


def bootstrap_metric(
    returns: pd.Series | np.ndarray,
    metric_fn: Callable[[np.ndarray], float],
    *,
    n_resamples: int = 2000,
    expected_block_length: float | None = None,
    confidence: float = 0.95,
    seed: int | None = None,
    metric_name: str = "metric",
) -> BootstrapCI:
    """Compute a stationary-bootstrap confidence interval for any metric.

    Args:
        returns: per-period returns.
        metric_fn: a callable that takes a 1-D ndarray of returns and
            returns a scalar. Use `lambda r: sharpe_ratio(r)` etc.
        n_resamples: number of bootstrap draws. 2000 is the standard
            default for 95% CIs; 10000 for 99% or for publication-grade.
        expected_block_length: mean block length. None → n^(1/3) rule.
        confidence: e.g. 0.95 for a 95% CI.
        seed: RNG seed for reproducibility. None → fresh entropy.
        metric_name: label that gets carried into the BootstrapCI.

    Why we return percentile CIs and not BCa (bias-corrected and
    accelerated): BCa is more accurate but requires a jackknife step
    that scales O(n) per resample, doubling cost. Percentile CIs are
    the conservative, standard choice and adequate at our sample sizes.

    NaN bootstrap samples (e.g. zero-variance resample → undefined
    Sharpe) are dropped before computing percentiles. If too many
    resamples produce NaN (>10%), the returned CI is NaN — that's
    a signal the metric is undefined for this distribution.
    """
    r = _to_numpy_returns(returns)
    n = len(r)
    if n < 2:
        nan = float("nan")
        return BootstrapCI(nan, nan, nan, confidence, n_resamples,
                           float("nan"), metric_name)
    if not (0.0 < confidence < 1.0):
        raise ValueError(f"confidence must be in (0, 1), got {confidence}")
    if n_resamples < 100:
        raise ValueError(
            f"n_resamples={n_resamples} is too small for a meaningful CI; "
            "use at least 100 (recommended >=1000)."
        )

    block_len = (
        float(expected_block_length)
        if expected_block_length is not None
        else _politis_white_block_length(n)
    )
    rng = np.random.default_rng(seed)

    point = float(metric_fn(r))

    samples = np.empty(n_resamples, dtype=float)
    for i in range(n_resamples):
        idx = stationary_bootstrap_indices(n, block_len, rng)
        samples[i] = float(metric_fn(r[idx]))

    finite = samples[np.isfinite(samples)]
    if len(finite) < 0.9 * n_resamples:
        nan = float("nan")
        return BootstrapCI(point, nan, nan, confidence, n_resamples,
                           block_len, metric_name)

    alpha = (1.0 - confidence) / 2.0
    lower = float(np.quantile(finite, alpha))
    upper = float(np.quantile(finite, 1.0 - alpha))

    return BootstrapCI(
        point=point,
        lower=lower,
        upper=upper,
        confidence=confidence,
        n_resamples=n_resamples,
        expected_block_length=block_len,
        metric_name=metric_name,
    )