"""
Probabilistic Sharpe Ratio (PSR) and Deflated Sharpe Ratio (DSR).

WHY this module exists
----------------------
The classical Sharpe ratio is a point estimate with no uncertainty
quantification. Two strategies with the same SR can have wildly different
statistical confidence: one might be backed by 1000 daily observations of
near-Gaussian returns, the other by 100 observations of skewed, fat-tailed
returns. The PSR (Bailey and Lopez de Prado 2012) gives the probability
that the TRUE Sharpe exceeds a benchmark, accounting for sample size,
skewness, and kurtosis. The DSR (Bailey and Lopez de Prado 2014) goes
further: it deflates the benchmark by the expected maximum SR under the
null, given the number of strategy trials searched. DSR is the antidote
to backtest overfitting and multiple-testing selection bias -- exactly
the failure mode that produced graveyard hypotheses H008-H010
(high-Sharpe-but-fragile).

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

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import norm

from quantcore.validation.metrics import sharpe_ratio

__all__ = [
    "PSRResult",
    "DSRResult",
    "probabilistic_sharpe_ratio",
    "deflated_sharpe_ratio",
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