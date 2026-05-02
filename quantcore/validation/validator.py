"""
Validator orchestrator — composes Phase 1.10–1.13 gates into one pass/fail
battery. Each gate catches a different failure mode:

    PSR    — sample-size adequacy + non-normality of returns (Bailey & López
             de Prado 2012). Catches "Sharpe looks good but is statistically
             indistinguishable from the benchmark given skew/kurtosis".
    MinTRL — track-record adequacy. Answers "how many bars do we still need
             to confirm SR > SR* at the given confidence?". Infeasible when
             the realized SR is at or below benchmark.
    DSR    — selection bias on Sharpe across N trials (Bailey & López de
             Prado 2014). Required whenever you picked the best of N strategies.
    RC     — White's Reality Check (2000). Selection bias on RAW excess returns
             across K candidates via stationary bootstrap.
    MT     — Bonferroni / Holm / Benjamini-Hochberg p-value corrections for
             a pre-registered family of hypothesis tests (not a "best-of"
             selection — RC/DSR are for that).

Why one orchestrator: solo retail traders skip gates. Forcing the gate set into
a single object — with each gate auto-running based on inputs provided — makes
the gate battery self-documenting and impossible to silently bypass. Anything
missing is explicit in `n_gates_run` and the summary string.

References (cited fully in their respective modules):
    Bailey & López de Prado (2012, 2014); White (2000); Politis & Romano (1994);
    Bonferroni (1936); Holm (1979); Benjamini & Hochberg (1995).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike

from quantcore.validation.deflated_sharpe import (
    DSRResult,
    MinTRLResult,
    PSRResult,
    deflated_sharpe_ratio,
    min_track_record_length_from_returns,
    probabilistic_sharpe_ratio,
)
from quantcore.validation.multiple_testing import (
    MultipleTestingResult,
    benjamini_hochberg,
    bonferroni_correction,
    holm_correction,
)
from quantcore.validation.reality_check import (
    RealityCheckResult,
    whites_reality_check,
)

MTMethod = Literal["bonferroni", "holm", "bh"]


@dataclass(frozen=True)
class ValidatorReport:
    """
    Aggregate verdict from a Validator.run() call.

    Each gate's full result object is preserved so callers can drill in. The
    *_passed booleans are gate-level verdicts; `all_passed` is the AND of every
    gate that actually ran. Optional gates that didn't run carry `None` and do
    NOT enter the AND.

    Why frozen: validator reports are evidence artifacts. They get logged,
    serialized, and referenced months later in governance reviews. They must
    not mutate after construction.
    """

    psr: PSRResult
    psr_passed: bool

    min_trl: MinTRLResult
    min_trl_passed: bool

    dsr: DSRResult | None
    dsr_passed: bool | None

    reality_check: RealityCheckResult | None
    reality_check_passed: bool | None

    multiple_testing: MultipleTestingResult | None
    multiple_testing_passed: bool | None

    all_passed: bool
    n_gates_run: int
    summary: str


class Validator:
    """
    Composes PSR / MinTRL / DSR / Reality Check / multiple-testing into a
    single pass/fail battery.

    Configuration is constructor-bound (alpha, periods_per_year, etc.). Gate
    inputs are passed to .run(). PSR and MinTRL are mandatory; DSR / RC / MT
    are opt-in based on which inputs are provided to .run().

    Why two-stage (config in __init__, data in run): the validator is meant to
    be reused across many candidate strategies in the same study. Pinning alpha
    once at construction prevents accidental alpha-shopping per-call.
    """

    def __init__(
        self,
        periods_per_year: int = 252,
        alpha: float = 0.05,
        sr_benchmark: float = 0.0,
        confidence: float = 0.95,
        n_bootstrap: int = 2000,
        random_state: int | None = None,
    ) -> None:
        if not (0.0 < alpha < 1.0):
            raise ValueError(f"alpha must be in (0, 1); got {alpha}")
        if not (0.0 < confidence < 1.0):
            raise ValueError(f"confidence must be in (0, 1); got {confidence}")
        if periods_per_year <= 0:
            raise ValueError(
                f"periods_per_year must be positive; got {periods_per_year}"
            )
        if n_bootstrap <= 0:
            raise ValueError(f"n_bootstrap must be positive; got {n_bootstrap}")

        self.periods_per_year = periods_per_year
        self.alpha = alpha
        self.sr_benchmark = sr_benchmark
        self.confidence = confidence
        self.n_bootstrap = n_bootstrap
        self.random_state = random_state

    def run(
        self,
        returns: pd.Series,
        sr_estimates: ArrayLike | None = None,
        candidate_returns_matrix: pd.DataFrame | None = None,
        p_values: ArrayLike | None = None,
        mt_method: MTMethod = "holm",
    ) -> ValidatorReport:
        """
        Run all applicable gates and return an aggregate report.

        Parameters
        ----------
        returns : pd.Series
            Per-period excess returns of the candidate strategy (mandatory).
        sr_estimates : array-like, optional
            Sharpe ratios of all trials in the selection family. If provided,
            DSR runs.
        candidate_returns_matrix : pd.DataFrame, optional
            (T, K) per-period returns of K competing strategies. If provided,
            White's Reality Check runs.
        p_values : array-like, optional
            Raw p-values from a family of hypothesis tests. If provided,
            multiple-testing correction runs.
        mt_method : {"bonferroni", "holm", "bh"}
            Which correction to apply when `p_values` is given.
        """
        if not isinstance(returns, pd.Series):
            raise TypeError("returns must be a pandas Series")
        if len(returns) < 2:
            raise ValueError(
                f"returns must have at least 2 observations; got {len(returns)}"
            )

        n_obs = len(returns)
        gates_run = 0
        gates_passed = 0

        # --- Gate 1: PSR (mandatory) -----------------------------------------
        psr = probabilistic_sharpe_ratio(
            returns,
            sr_benchmark=self.sr_benchmark,
            periods_per_year=self.periods_per_year,
        )
        psr_passed = bool(psr.psr >= 1.0 - self.alpha)
        gates_run += 1
        gates_passed += int(psr_passed)

        # --- Gate 2: MinTRL (mandatory) --------------------------------------
        min_trl = min_track_record_length_from_returns(
            returns,
            sr_benchmark=self.sr_benchmark,
            confidence=self.confidence,
            periods_per_year=self.periods_per_year,
        )
        min_trl_passed = bool(min_trl.feasible and min_trl.min_n <= n_obs)
        gates_run += 1
        gates_passed += int(min_trl_passed)

        # --- Gate 3: DSR (optional) ------------------------------------------
        dsr: DSRResult | None = None
        dsr_passed: bool | None = None
        if sr_estimates is not None:
            dsr = deflated_sharpe_ratio(
                returns,
                sr_estimates=np.asarray(sr_estimates, dtype=float),
                periods_per_year=self.periods_per_year,
            )
            dsr_passed = bool(dsr.dsr >= 1.0 - self.alpha)
            gates_run += 1
            gates_passed += int(dsr_passed)

        # --- Gate 4: White's Reality Check (optional) ------------------------
        rc: RealityCheckResult | None = None
        rc_passed: bool | None = None
        if candidate_returns_matrix is not None:
            if not isinstance(candidate_returns_matrix, pd.DataFrame):
                raise TypeError(
                    "candidate_returns_matrix must be a pandas DataFrame"
                )
            rc = whites_reality_check(
                candidate_returns_matrix,
                n_bootstrap=self.n_bootstrap,
                random_state=self.random_state,
            )
            rc_passed = bool(rc.p_value <= self.alpha)
            gates_run += 1
            gates_passed += int(rc_passed)

        # --- Gate 5: Multiple-testing correction (optional) ------------------
        mt: MultipleTestingResult | None = None
        mt_passed: bool | None = None
        if p_values is not None:
            mt = self._run_multiple_testing(p_values, mt_method, self.alpha)
            mt_passed = bool(np.any(mt.rejected))
            gates_run += 1
            gates_passed += int(mt_passed)

        all_passed = gates_passed == gates_run

        summary = self._build_summary(
            psr=psr,
            psr_passed=psr_passed,
            min_trl=min_trl,
            min_trl_passed=min_trl_passed,
            n_obs=n_obs,
            dsr=dsr,
            dsr_passed=dsr_passed,
            rc=rc,
            rc_passed=rc_passed,
            mt=mt,
            mt_passed=mt_passed,
            mt_method=mt_method,
            gates_passed=gates_passed,
            gates_run=gates_run,
            all_passed=all_passed,
        )

        return ValidatorReport(
            psr=psr,
            psr_passed=psr_passed,
            min_trl=min_trl,
            min_trl_passed=min_trl_passed,
            dsr=dsr,
            dsr_passed=dsr_passed,
            reality_check=rc,
            reality_check_passed=rc_passed,
            multiple_testing=mt,
            multiple_testing_passed=mt_passed,
            all_passed=all_passed,
            n_gates_run=gates_run,
            summary=summary,
        )

    @staticmethod
    def _run_multiple_testing(
        p_values: ArrayLike, method: MTMethod, alpha: float
    ) -> MultipleTestingResult:
        if method == "bonferroni":
            return bonferroni_correction(p_values, alpha=alpha)
        if method == "holm":
            return holm_correction(p_values, alpha=alpha)
        if method == "bh":
            return benjamini_hochberg(p_values, alpha=alpha)
        raise ValueError(
            f"mt_method must be 'bonferroni', 'holm', or 'bh'; got {method!r}"
        )

    @staticmethod
    def _build_summary(
        *,
        psr: PSRResult,
        psr_passed: bool,
        min_trl: MinTRLResult,
        min_trl_passed: bool,
        n_obs: int,
        dsr: DSRResult | None,
        dsr_passed: bool | None,
        rc: RealityCheckResult | None,
        rc_passed: bool | None,
        mt: MultipleTestingResult | None,
        mt_passed: bool | None,
        mt_method: MTMethod,
        gates_passed: int,
        gates_run: int,
        all_passed: bool,
    ) -> str:
        parts: list[str] = []
        parts.append(f"PSR={psr.psr:.3f}{'+' if psr_passed else '-'}")
        if min_trl.feasible:
            parts.append(
                f"MinTRL={min_trl.min_n}/{n_obs}"
                f"{'+' if min_trl_passed else '-'}"
            )
        else:
            parts.append("MinTRL=infeasible-")
        if dsr is not None:
            parts.append(f"DSR={dsr.dsr:.3f}{'+' if dsr_passed else '-'}")
        else:
            parts.append("DSR=skipped")
        if rc is not None:
            parts.append(f"RC_p={rc.p_value:.3f}{'+' if rc_passed else '-'}")
        else:
            parts.append("RC=skipped")
        if mt is not None:
            n_rej = int(np.sum(mt.rejected))
            parts.append(
                f"MT[{mt_method}]={n_rej}/{mt.n_tests}"
                f"{'+' if mt_passed else '-'}"
            )
        else:
            parts.append("MT=skipped")

        verdict = "PASS" if all_passed else "FAIL"
        return (
            f"Validator: {gates_passed}/{gates_run} gates passed "
            f"({', '.join(parts)}). Verdict: {verdict}."
        )