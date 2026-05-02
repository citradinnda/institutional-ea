"""
Tests for the Phase 1.14 Validator orchestrator.

Strategy:
    - Use small, deterministic synthetic returns so PSR/MinTRL pass or fail
      predictably.
    - Use small `n_bootstrap` for Reality Check tests (<= 200) for speed;
      production callers use 2000+ per HANDOFF section 5.
    - Verify gate WIRING (which inputs trigger which gates), not numerical
      correctness of each underlying gate (already covered by the per-module
      test files: 31 + 19 + 19 + 25 = 94 tests).
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError, fields

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import Validator, ValidatorReport
from quantcore.validation.deflated_sharpe import (
    DSRResult,
    MinTRLResult,
    PSRResult,
)
from quantcore.validation.multiple_testing import MultipleTestingResult
from quantcore.validation.reality_check import RealityCheckResult


# ---------- helpers ---------------------------------------------------------

def _winning_returns(n: int = 1000, seed: int = 7) -> pd.Series:
    """Strong-edge daily returns: ~Sharpe 2.5 annualized. PSR/MinTRL pass."""
    rng = np.random.default_rng(seed)
    daily = rng.normal(loc=0.0010, scale=0.006, size=n)
    idx = pd.date_range("2020-01-01", periods=n, freq="B")
    return pd.Series(daily, index=idx, name="ret")


def _losing_returns(n: int = 500, seed: int = 11) -> pd.Series:
    """
    Decisively negative-edge returns: true mean is ~9 standard errors below
    zero, so the sample SR is reliably <= 0 across seeds. This guarantees
    MinTRL is infeasible (SR - SR_benchmark <= 0) per the Phase 1.11 spec.
    """
    rng = np.random.default_rng(seed)
    daily = rng.normal(loc=-0.002, scale=0.005, size=n)
    idx = pd.date_range("2020-01-01", periods=n, freq="B")
    return pd.Series(daily, index=idx, name="ret")


def _candidate_matrix(
    n_rows: int = 200, n_cols: int = 4, seed: int = 13, edge: float = 0.0008
) -> pd.DataFrame:
    """K candidate strategies. First column is the 'best' by construction."""
    rng = np.random.default_rng(seed)
    data = rng.normal(loc=0.0, scale=0.005, size=(n_rows, n_cols))
    data[:, 0] += edge  # plant edge in column 0
    idx = pd.date_range("2021-01-01", periods=n_rows, freq="B")
    cols = [f"strat_{i}" for i in range(n_cols)]
    return pd.DataFrame(data, index=idx, columns=cols)


# ---------- structural tests (3) -------------------------------------------

def test_validator_report_is_frozen_dataclass() -> None:
    r = Validator().run(_winning_returns())
    with pytest.raises(FrozenInstanceError):
        r.all_passed = False  # type: ignore[misc]


def test_validator_report_has_expected_fields() -> None:
    expected = {
        "psr",
        "psr_passed",
        "min_trl",
        "min_trl_passed",
        "dsr",
        "dsr_passed",
        "reality_check",
        "reality_check_passed",
        "multiple_testing",
        "multiple_testing_passed",
        "all_passed",
        "n_gates_run",
        "summary",
    }
    actual = {f.name for f in fields(ValidatorReport)}
    assert actual == expected


def test_validator_report_field_types_are_correct() -> None:
    r = Validator(n_bootstrap=100, random_state=0).run(
        _winning_returns(),
        sr_estimates=np.array([1.0, 1.5, 2.0]),
        candidate_returns_matrix=_candidate_matrix(),
        p_values=[0.001, 0.04, 0.30],
        mt_method="holm",
    )
    assert isinstance(r.psr, PSRResult)
    assert isinstance(r.min_trl, MinTRLResult)
    assert isinstance(r.dsr, DSRResult)
    assert isinstance(r.reality_check, RealityCheckResult)
    assert isinstance(r.multiple_testing, MultipleTestingResult)
    assert isinstance(r.summary, str) and len(r.summary) > 0


# ---------- mandatory-only tests (2) ---------------------------------------

def test_mandatory_only_run_executes_two_gates() -> None:
    r = Validator().run(_winning_returns())
    assert r.n_gates_run == 2
    assert r.dsr is None
    assert r.dsr_passed is None
    assert r.reality_check is None
    assert r.reality_check_passed is None
    assert r.multiple_testing is None
    assert r.multiple_testing_passed is None


def test_mandatory_only_winning_strategy_passes() -> None:
    r = Validator().run(_winning_returns())
    assert r.psr_passed is True
    assert r.min_trl_passed is True
    assert r.all_passed is True


# ---------- DSR opt-in tests (2) -------------------------------------------

def test_dsr_runs_when_sr_estimates_provided() -> None:
    sr = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
    r = Validator().run(_winning_returns(), sr_estimates=sr)
    assert r.dsr is not None
    assert r.dsr_passed is not None
    assert r.n_gates_run == 3


def test_dsr_skipped_when_sr_estimates_none() -> None:
    r = Validator().run(_winning_returns(), sr_estimates=None)
    assert r.dsr is None
    assert r.dsr_passed is None


# ---------- Reality Check opt-in tests (2) ---------------------------------

def test_reality_check_runs_when_matrix_provided() -> None:
    r = Validator(n_bootstrap=100, random_state=42).run(
        _winning_returns(),
        candidate_returns_matrix=_candidate_matrix(),
    )
    assert r.reality_check is not None
    assert r.reality_check_passed is not None
    assert r.n_gates_run == 3


def test_reality_check_rejects_non_dataframe() -> None:
    bad = np.zeros((100, 3))  # ndarray, not DataFrame
    with pytest.raises(TypeError, match="DataFrame"):
        Validator(n_bootstrap=50).run(
            _winning_returns(),
            candidate_returns_matrix=bad,  # type: ignore[arg-type]
        )


# ---------- Multiple-testing opt-in tests (3) ------------------------------

def test_multiple_testing_runs_with_bonferroni() -> None:
    r = Validator().run(
        _winning_returns(),
        p_values=[0.001, 0.20, 0.40],
        mt_method="bonferroni",
    )
    assert r.multiple_testing is not None
    assert r.multiple_testing.method == "bonferroni"
    assert r.multiple_testing_passed is True  # 0.001 * 3 = 0.003 < 0.05


def test_multiple_testing_runs_with_holm() -> None:
    r = Validator().run(
        _winning_returns(),
        p_values=[0.001, 0.20, 0.40],
        mt_method="holm",
    )
    assert r.multiple_testing is not None
    assert r.multiple_testing.method == "holm"
    assert r.multiple_testing_passed is True


def test_multiple_testing_runs_with_bh() -> None:
    r = Validator().run(
        _winning_returns(),
        p_values=[0.001, 0.20, 0.40],
        mt_method="bh",
    )
    assert r.multiple_testing is not None
    assert r.multiple_testing.method == "benjamini_hochberg"
    assert r.multiple_testing_passed is True


# ---------- end-to-end smoke tests (2) -------------------------------------

def test_all_gates_on_smoke() -> None:
    r = Validator(n_bootstrap=100, random_state=42).run(
        _winning_returns(),
        sr_estimates=np.array([1.0, 1.5, 2.0, 2.5]),
        candidate_returns_matrix=_candidate_matrix(),
        p_values=[0.001, 0.02, 0.30, 0.50],
        mt_method="holm",
    )
    assert r.n_gates_run == 5
    # Mandatory gates always populated
    assert r.psr is not None
    assert r.min_trl is not None
    # Optional gates all populated
    assert r.dsr is not None
    assert r.reality_check is not None
    assert r.multiple_testing is not None


def test_summary_string_mentions_gate_count() -> None:
    r = Validator(n_bootstrap=100, random_state=0).run(_winning_returns())
    assert "2/2" in r.summary or "0/2" in r.summary or "1/2" in r.summary
    assert "Verdict:" in r.summary


# ---------- pass / fail scenario tests (3) ---------------------------------

def test_winning_strategy_passes_all_mandatory_gates() -> None:
    r = Validator().run(_winning_returns())
    assert r.psr_passed is True
    assert r.min_trl_passed is True
    assert r.all_passed is True
    assert "PASS" in r.summary


def test_losing_strategy_fails_min_trl_gate() -> None:
    r = Validator().run(_losing_returns())
    # Losing strategy: SR <= benchmark => MinTRL infeasible.
    assert r.min_trl.feasible is False
    assert r.min_trl_passed is False
    assert r.all_passed is False
    assert "FAIL" in r.summary


def test_all_high_p_values_fails_mt_gate() -> None:
    # All p-values well above alpha => no rejections under any method.
    r = Validator().run(
        _winning_returns(),
        p_values=[0.40, 0.60, 0.80, 0.95],
        mt_method="holm",
    )
    assert r.multiple_testing_passed is False
    assert r.all_passed is False


# ---------- aggregation logic tests (2) ------------------------------------

def test_all_passed_is_and_of_run_gates_only() -> None:
    # Mandatory gates pass; provide a multiple-testing input that FAILS.
    r = Validator().run(
        _winning_returns(),
        p_values=[0.50, 0.60, 0.70],
        mt_method="holm",
    )
    assert r.psr_passed is True
    assert r.min_trl_passed is True
    assert r.multiple_testing_passed is False
    # Optional gates that did NOT run must not drag AND down.
    assert r.dsr_passed is None
    assert r.reality_check_passed is None
    # But the gate that DID run and failed should fail the aggregate.
    assert r.all_passed is False


def test_n_gates_run_counts_only_executed_gates() -> None:
    # Just the two mandatory gates.
    r1 = Validator().run(_winning_returns())
    assert r1.n_gates_run == 2

    # Add DSR.
    r2 = Validator().run(
        _winning_returns(), sr_estimates=np.array([1.0, 2.0])
    )
    assert r2.n_gates_run == 3

    # Add MT too.
    r3 = Validator().run(
        _winning_returns(),
        sr_estimates=np.array([1.0, 2.0]),
        p_values=[0.01, 0.5],
    )
    assert r3.n_gates_run == 4


# ---------- input validation test (1) --------------------------------------

def test_validator_rejects_bad_construction_args() -> None:
    with pytest.raises(ValueError, match="alpha"):
        Validator(alpha=0.0)
    with pytest.raises(ValueError, match="alpha"):
        Validator(alpha=1.5)
    with pytest.raises(ValueError, match="confidence"):
        Validator(confidence=0.0)
    with pytest.raises(ValueError, match="periods_per_year"):
        Validator(periods_per_year=0)
    with pytest.raises(ValueError, match="n_bootstrap"):
        Validator(n_bootstrap=0)

    v = Validator()
    with pytest.raises(TypeError, match="Series"):
        v.run(returns=np.array([0.01, 0.02, 0.03]))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least 2"):
        v.run(returns=pd.Series([0.01]))
    with pytest.raises(ValueError, match="mt_method"):
        v.run(_winning_returns(), p_values=[0.1, 0.2], mt_method="bogus")  # type: ignore[arg-type]