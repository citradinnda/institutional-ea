"""
Probabilistic Sharpe Ratio (PSR) and Deflated Sharpe Ratio (DSR).

WHY this module exists
----------------------
The classical Sharpe ratio is a point estimate with no uncertainty
quantification. Two strategies with the same SR can have wildly different
statistical confidence: one might be backed by 1000 daily observations of
near-Gaussian returns, the other by 100 observations of skewed, fat-tailed
returns. The PSR (Bailey and Lopez de Prado 2012) gives the probability
that the TRUE Sharpe exceeds a benchmark, accounting for sample
size, skewness, and kurtosis. The Minimum Track Record Length
(MinTRL, same paper) inverts the question: how many observations
are needed before we can claim, with given confidence, that the
true SR exceeds the benchmark? The DSR (Bailey and Lopez de Prado
2014) goes further: it deflates the benchmark by the expected
maximum SR under the null, given the number of strategy trials
searched. DSR is the antidote to backtest overfitting and
multiple-testing selection bias -- exactly the failure mode that
produced graveyard hypotheses H008-H010 (high-Sharpe-but-fragile).
MinTRL is the antidote to "looks great but the backtest is too
short to prove it" -- a separate failure mode worth its own gate.

References
----------
Bailey, D. H., and Lopez de Prado, M. (2012).
    "The Sharpe Ratio Efficient Frontier." Journal of Risk, 15(2), 3-44.
Bailey, D. H., and Lopez de Prado, M. (2014).
    "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest
    Overfitting, and Non-Normality." Journal of Portfolio Management,
    40(5), 94-107.

Annualization convention
------------------------
PSR/DSR formulas are derived in terms of the PER-PERIOD Sharpe ratio.
We compute the probability on per-period SR internally. The
`observed_sr` field exposed in PSRResult/DSRResult is the ANNUALIZED
SR (matching `quantcore.validation.metrics.sharpe_ratio`) for
human-readable display only. The `sr_benchmark` argument is annualized
and translated to per-period internally as
    sr_benchmark_pp = sr_benchmark / sqrt(periods_per_year).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import norm

from quantcore.validation.metrics import sharpe_ratio

__all__ = [
    "PSRResult",
    "DSRResult",
    "MinTRLResult",
    "probabilistic_sharpe_ratio",
    "deflated_sharpe_ratio",
    "min_track_record_length",
    "min_track_record_length_from_returns",
    "expected_max_sharpe",
]

# Euler-Mascheroni constant, used in the expected-max-SR approximation.
_EULER_MASCHERONI = 0.5772156649015329


@dataclass(frozen=True)
class PSRResult:
    """
    Result of a Probabilistic Sharpe Ratio calculation.

    Attributes
    ----------
    psr : float
        Probability in [0, 1] that the true (per-period) Sharpe exceeds
        the (per-period) benchmark, given the observed sample.
    observed_sr : float
        ANNUALIZED observed Sharpe ratio (for display).
    skew : float
        Sample skewness of returns.
    kurtosis : float
        Sample EXCESS kurtosis of returns (Gaussian = 0).
    n : int
        Number of return observations.
    sr_benchmark : float
        Annualized benchmark SR supplied by the caller (echoed back).
    """

    psr: float
    observed_sr: float
    skew: float
    kurtosis: float
    n: int
    sr_benchmark: float


@dataclass(frozen=True)
class DSRResult:
    """
    Result of a Deflated Sharpe Ratio calculation.

    Attributes
    ----------
    dsr : float
        Probability in [0, 1] that the true SR exceeds the deflated
        benchmark (i.e. the expected maximum SR under the null across
        `n_trials` independent strategy attempts).
    observed_sr : float
        ANNUALIZED observed Sharpe ratio (for display).
    skew : float
        Sample skewness of returns.
    kurtosis : float
        Sample EXCESS kurtosis of returns.
    n : int
        Number of return observations.
    expected_max_sr : float
        Per-period expected maximum SR under the null, given `n_trials`
        and the variance of `sr_estimates`.
    n_trials : int
        Number of independent SR estimates supplied (the multiple-testing
        breadth).
    sr_benchmark_deflated : float
        Per-period deflated benchmark actually used in the DSR z-score
        (i.e. user benchmark + expected_max_sr, both per-period).
    """

    dsr: float
    observed_sr: float
    skew: float
    kurtosis: float
    n: int
    expected_max_sr: float
    n_trials: int
    sr_benchmark_deflated: float


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _to_1d_array(returns: np.ndarray | pd.Series) -> np.ndarray:
    """Coerce returns to a 1D float64 numpy array, dropping NaNs.

    WHY: PSR/DSR formulas assume a clean 1D sample; pandas Series and
    numpy arrays should be interchangeable at the API boundary.
    """
    if isinstance(returns, pd.Series):
        arr = returns.to_numpy(dtype=float)
    else:
        arr = np.asarray(returns, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"returns must be 1D; got shape {arr.shape}")
    arr = arr[~np.isnan(arr)]
    return arr


def _per_period_sharpe(returns: np.ndarray) -> float:
    """Per-period (un-annualized) Sharpe = mean / std (ddof=1).

    WHY: PSR's variance formula is derived for the per-period SR. We
    deliberately do NOT reuse `metrics.sharpe_ratio` here because that
    function annualizes; we use it only to populate the display field.
    """
    if returns.size < 2:
        raise ValueError("Need at least 2 observations for Sharpe.")
    std = float(np.std(returns, ddof=1))
    if std < 1e-12:
        raise ValueError("Returns have ~zero variance; SR undefined.")
    return float(np.mean(returns) / std)


def _sample_skew(returns: np.ndarray) -> float:
    """Bias-uncorrected sample skewness (population formula on sample).

    WHY: Bailey/Lopez de Prado use the population-style moment estimator
    (third central moment / sigma^3), not the bias-corrected (g1) form.
    """
    n = returns.size
    mu = float(np.mean(returns))
    sigma = float(np.std(returns, ddof=0))
    if sigma < 1e-12:
        return 0.0
    m3 = float(np.mean((returns - mu) ** 3))
    return m3 / (sigma**3)


def _sample_excess_kurtosis(returns: np.ndarray) -> float:
    """Population-style EXCESS kurtosis (Gaussian = 0).

    WHY: matches the convention used in the PSR/DSR variance formula
    (kurtosis term enters as `kurt - 1` where kurt is excess; this
    function returns excess kurtosis directly).
    """
    n = returns.size
    mu = float(np.mean(returns))
    sigma = float(np.std(returns, ddof=0))
    if sigma < 1e-12:
        return 0.0
    m4 = float(np.mean((returns - mu) ** 4))
    return m4 / (sigma**4) - 3.0


def _psr_from_moments(
    sr_pp: float,
    sr_benchmark_pp: float,
    n: int,
    skew: float,
    excess_kurt: float,
) -> float:
    """Core PSR z-score -> normal CDF.

    Formula (Bailey and Lopez de Prado 2012):
        PSR(SR*) = Phi( (SR_hat - SR*) * sqrt(n - 1) /
                        sqrt(1 - skew*SR_hat + ((kurt-1)/4)*SR_hat^2) )
    where `kurt` is EXCESS kurtosis and SRs are per-period.
    """
    if n < 2:
        raise ValueError("PSR needs n >= 2.")
    denom_sq = 1.0 - skew * sr_pp + (excess_kurt / 4.0) * (sr_pp**2)
    # Guard: denominator under sqrt must stay positive. For sane samples
    # with |SR_hat| not absurd this holds; if it goes negative the moments
    # are pathological and we refuse rather than return a fake number.
    if denom_sq <= 0.0:
        raise ValueError(
            "PSR variance term non-positive; sample moments are pathological "
            f"(1 - skew*SR + (kurt-1)/4 * SR^2 = {denom_sq:.6g})."
        )
    z = (sr_pp - sr_benchmark_pp) * np.sqrt(n - 1) / np.sqrt(denom_sq)
    return float(norm.cdf(z))


def expected_max_sharpe(n_trials: int, sr_variance: float) -> float:
    """
    Expected maximum SR under the null across `n_trials` independent
    strategy attempts, in PER-PERIOD units.

    Formula (Bailey and Lopez de Prado 2014, eq. for E[max{SR_n}]):
        E[max] ~= sqrt(V[SR]) * ( (1 - gamma) * Phi^{-1}(1 - 1/N)
                                 +   gamma   * Phi^{-1}(1 - 1/(N*e)) )
    where gamma is the Euler-Mascheroni constant and N = n_trials.

    WHY: When you search across many strategy variants and report only
    the best, the best SR is upward-biased even when no real edge exists.
    This is the multiple-testing correction baked into DSR.

    Parameters
    ----------
    n_trials : int
        Number of independent SR estimates considered (>= 1).
    sr_variance : float
        Variance of those per-period SR estimates (>= 0).

    Returns
    -------
    float
        Per-period expected maximum SR under the null. Returns 0.0
        when `n_trials == 1` (no multiple-testing inflation possible)
        or when `sr_variance == 0` (no dispersion to inflate).
    """
    if n_trials < 1:
        raise ValueError("n_trials must be >= 1.")
    if sr_variance < 0.0:
        raise ValueError("sr_variance must be >= 0.")
    if n_trials == 1 or sr_variance < 1e-24:
        return 0.0
    n = float(n_trials)
    # ppf(1 - 1/N) and ppf(1 - 1/(N*e)) are well-defined for N >= 2.
    z1 = float(norm.ppf(1.0 - 1.0 / n))
    z2 = float(norm.ppf(1.0 - 1.0 / (n * np.e)))
    em = np.sqrt(sr_variance) * (
        (1.0 - _EULER_MASCHERONI) * z1 + _EULER_MASCHERONI * z2
    )
    return float(em)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def probabilistic_sharpe_ratio(
    returns: np.ndarray | pd.Series,
    sr_benchmark: float = 0.0,
    periods_per_year: int = 252,
) -> PSRResult:
    """
    Probabilistic Sharpe Ratio (Bailey and Lopez de Prado 2012).

    PSR is the probability that the TRUE (per-period) Sharpe exceeds the
    benchmark, given the observed sample's SR, length, skewness, and
    excess kurtosis. It is robust to non-normal returns.

    WHY: A point-estimate SR with no uncertainty band is the kind of
    statistic that produced graveyard hypotheses H008-H010. PSR forces
    sample size and tail behaviour into the conclusion.

    Parameters
    ----------
    returns : array-like of shape (n,)
        Per-period returns (e.g. daily, hourly). NaNs are dropped.
    sr_benchmark : float, default 0.0
        ANNUALIZED benchmark SR. Internally translated to per-period as
        `sr_benchmark / sqrt(periods_per_year)`.
    periods_per_year : int, default 252
        Annualization factor for display and benchmark translation.

    Returns
    -------
    PSRResult
        Frozen dataclass with `psr` in [0, 1] plus diagnostic fields.
    """
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be >= 1.")
    arr = _to_1d_array(returns)
    n = arr.size
    if n < 2:
        raise ValueError("PSR needs at least 2 observations.")

    sr_pp = _per_period_sharpe(arr)
    skew = _sample_skew(arr)
    ekurt = _sample_excess_kurtosis(arr)

    sr_benchmark_pp = sr_benchmark / np.sqrt(periods_per_year)
    psr = _psr_from_moments(sr_pp, sr_benchmark_pp, n, skew, ekurt)

    # Annualized observed SR for display, computed via the canonical
    # metrics function so we do not drift from the rest of the codebase.
    observed_sr_annual = float(sharpe_ratio(arr, periods_per_year=periods_per_year))

    return PSRResult(
        psr=psr,
        observed_sr=observed_sr_annual,
        skew=skew,
        kurtosis=ekurt,
        n=n,
        sr_benchmark=sr_benchmark,
    )


def deflated_sharpe_ratio(
    returns: np.ndarray | pd.Series,
    sr_estimates: np.ndarray | pd.Series,
    sr_benchmark: float = 0.0,
    periods_per_year: int = 252,
) -> DSRResult:
    """
    Deflated Sharpe Ratio (Bailey and Lopez de Prado 2014).

    DSR is PSR evaluated against a benchmark that has been INFLATED by
    the expected maximum SR under the null across `n_trials` independent
    strategy attempts. It corrects for backtest selection bias.

    WHY: If you tested 200 strategy variants and report only the best,
    its SR is upward-biased even with no true edge. DSR estimates how
    much of the observed SR is "free" from luck-of-the-draw inflation.

    Parameters
    ----------
    returns : array-like of shape (n,)
        Per-period returns of the SELECTED (best) strategy.
    sr_estimates : array-like of shape (n_trials,)
        ALL per-period SR estimates considered during the search
        (including the selected one). Used only for `Var[SR]` and the
        count `n_trials`. Must be PER-PERIOD SRs; if you have annualized
        SRs, divide by sqrt(periods_per_year) before passing them in.
    sr_benchmark : float, default 0.0
        ANNUALIZED user benchmark SR (additional to the deflation).
    periods_per_year : int, default 252
        Annualization factor for display and benchmark translation.

    Returns
    -------
    DSRResult
        Frozen dataclass with `dsr` in [0, 1] plus diagnostic fields.
    """
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be >= 1.")
    arr = _to_1d_array(returns)
    n = arr.size
    if n < 2:
        raise ValueError("DSR needs at least 2 return observations.")

    if isinstance(sr_estimates, pd.Series):
        sr_arr = sr_estimates.to_numpy(dtype=float)
    else:
        sr_arr = np.asarray(sr_estimates, dtype=float)
    if sr_arr.ndim != 1:
        raise ValueError(f"sr_estimates must be 1D; got shape {sr_arr.shape}")
    sr_arr = sr_arr[~np.isnan(sr_arr)]
    n_trials = int(sr_arr.size)
    if n_trials < 1:
        raise ValueError("Need at least one SR estimate.")

    sr_pp = _per_period_sharpe(arr)
    skew = _sample_skew(arr)
    ekurt = _sample_excess_kurtosis(arr)

    # Variance of the SR estimates across trials (ddof=1 for n>=2).
    if n_trials >= 2:
        sr_var = float(np.var(sr_arr, ddof=1))
    else:
        sr_var = 0.0

    expected_max = expected_max_sharpe(n_trials, sr_var)

    sr_benchmark_pp = sr_benchmark / np.sqrt(periods_per_year)
    sr_benchmark_deflated = sr_benchmark_pp + expected_max

    dsr = _psr_from_moments(sr_pp, sr_benchmark_deflated, n, skew, ekurt)

    observed_sr_annual = float(sharpe_ratio(arr, periods_per_year=periods_per_year))

    return DSRResult(
        dsr=dsr,
        observed_sr=observed_sr_annual,
        skew=skew,
        kurtosis=ekurt,
        n=n,
        expected_max_sr=expected_max,
        n_trials=n_trials,
        sr_benchmark_deflated=sr_benchmark_deflated,
    )

# ---------------------------------------------------------------------------
# Minimum Track Record Length (MinTRL)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MinTRLResult:
    """
    Result of a Minimum Track Record Length calculation.

    MinTRL answers: how many per-period observations are needed before
    we can claim, with the given confidence, that the TRUE Sharpe ratio
    exceeds the benchmark? It is the algebraic inverse of PSR.

    Attributes
    ----------
    min_n : int
        Minimum number of per-period observations required. Set to -1
        when `feasible == False` (i.e. observed SR <= benchmark, in
        which case no finite n suffices).
    min_n_years : float
        `min_n / periods_per_year` for human-readable display. Set to
        `float('inf')` in the infeasible case.
    feasible : bool
        True iff observed SR strictly exceeds the benchmark. When
        False, no finite track record can establish the claim because
        the point estimate is already on the wrong side of the bench.
    observed_sr : float
        ANNUALIZED observed Sharpe ratio (echoed back, for display).
    sr_benchmark : float
        ANNUALIZED benchmark SR supplied by the caller (echoed back).
    confidence : float
        Confidence level in (0, 1) supplied by the caller.
    skew : float
        Sample skewness used in the calculation.
    kurtosis : float
        Sample EXCESS kurtosis used in the calculation.
    """

    min_n: int
    min_n_years: float
    feasible: bool
    observed_sr: float
    sr_benchmark: float
    confidence: float
    skew: float
    kurtosis: float


def min_track_record_length(
    observed_sr: float,
    skew: float,
    kurtosis: float,
    sr_benchmark: float = 0.0,
    confidence: float = 0.95,
    periods_per_year: int = 252,
) -> MinTRLResult:
    """
    Minimum Track Record Length (Bailey and Lopez de Prado 2012).

    Solves PSR(SR*) >= confidence for n. Closed form:

        n_min = 1 + (1 - skew*SR + ((kurt-1)/4)*SR^2) * (z / (SR - SR*))^2

    where:
        SR  = observed PER-PERIOD Sharpe ratio
        SR* = PER-PERIOD benchmark Sharpe ratio
        kurt = EXCESS kurtosis
        z   = Phi^{-1}(confidence)

    WHY a separate gate from PSR: A backtest with PSR = 0.99 on only
    60 daily bars is statistically meaningless even though the number
    looks great -- the variance of the Sharpe estimator is huge at
    n = 60. MinTRL forces sample-size adequacy into the conclusion.
    A high PSR on a sub-MinTRL track record is the same trap that
    produced graveyard hypotheses H008-H010.

    Parameters
    ----------
    observed_sr : float
        ANNUALIZED observed Sharpe ratio. Translated to per-period as
        `observed_sr / sqrt(periods_per_year)` internally.
    skew : float
        Sample skewness of returns (population-style, matching PSR).
    kurtosis : float
        Sample EXCESS kurtosis of returns (Gaussian = 0).
    sr_benchmark : float, default 0.0
        ANNUALIZED benchmark SR.
    confidence : float, default 0.95
        Required confidence level, in (0, 1).
    periods_per_year : int, default 252
        Annualization factor.

    Returns
    -------
    MinTRLResult
        Frozen dataclass. When `observed_sr <= sr_benchmark` the result
        is infeasible: `min_n = -1`, `min_n_years = inf`,
        `feasible = False`.
    """
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be >= 1.")
    if not (0.0 < confidence < 1.0):
        raise ValueError("confidence must be in (0, 1) strict.")

    sr_pp = observed_sr / math.sqrt(periods_per_year)
    sr_bench_pp = sr_benchmark / math.sqrt(periods_per_year)

    # Infeasible: point estimate is already at or below the benchmark.
    # No finite n can flip the inequality -- the formula's denominator
    # would be <= 0. Return the explicit sentinel rather than raise.
    if sr_pp - sr_bench_pp <= 1e-12:
        return MinTRLResult(
            min_n=-1,
            min_n_years=float("inf"),
            feasible=False,
            observed_sr=observed_sr,
            sr_benchmark=sr_benchmark,
            confidence=confidence,
            skew=skew,
            kurtosis=kurtosis,
        )

    # Variance term from PSR (must stay positive for sane moments).
    var_term = 1.0 - skew * sr_pp + (kurtosis / 4.0) * (sr_pp**2)
    if var_term <= 0.0:
        raise ValueError(
            "MinTRL variance term non-positive; sample moments are "
            f"pathological (1 - skew*SR + (kurt-1)/4 * SR^2 = {var_term:.6g})."
        )

    z = float(norm.ppf(confidence))
    n_min_real = 1.0 + var_term * (z / (sr_pp - sr_bench_pp)) ** 2
    # ceil because n must be an integer count of observations and we
    # want the SMALLEST n that satisfies the inequality, not one less.
    n_min = int(math.ceil(n_min_real))

    return MinTRLResult(
        min_n=n_min,
        min_n_years=n_min / periods_per_year,
        feasible=True,
        observed_sr=observed_sr,
        sr_benchmark=sr_benchmark,
        confidence=confidence,
        skew=skew,
        kurtosis=kurtosis,
    )


def min_track_record_length_from_returns(
    returns: np.ndarray | pd.Series,
    sr_benchmark: float = 0.0,
    confidence: float = 0.95,
    periods_per_year: int = 252,
) -> MinTRLResult:
    """
    Convenience wrapper: derive observed SR, skew, and kurtosis from a
    return series, then call `min_track_record_length`.

    WHY: most callers have a return series, not pre-computed moments.
    This avoids forcing every caller to recompute the same statistics
    that PSR already computes internally.

    Parameters
    ----------
    returns : array-like of shape (n,)
        Per-period returns. NaNs are dropped.
    sr_benchmark : float, default 0.0
        ANNUALIZED benchmark SR.
    confidence : float, default 0.95
        Required confidence level, in (0, 1).
    periods_per_year : int, default 252
        Annualization factor.

    Returns
    -------
    MinTRLResult
    """
    arr = _to_1d_array(returns)
    if arr.size < 2:
        raise ValueError("MinTRL needs at least 2 return observations.")

    # Reuse the same moment helpers PSR uses, so MinTRL and PSR can never
    # disagree on what SR/skew/kurtosis the same sample produces.
    observed_sr_annual = float(sharpe_ratio(arr, periods_per_year=periods_per_year))
    skew = _sample_skew(arr)
    ekurt = _sample_excess_kurtosis(arr)

    return min_track_record_length(
        observed_sr=observed_sr_annual,
        skew=skew,
        kurtosis=ekurt,
        sr_benchmark=sr_benchmark,
        confidence=confidence,
        periods_per_year=periods_per_year,
    )