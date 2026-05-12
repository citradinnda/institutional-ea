from __future__ import annotations

import ast
import copy
from pathlib import Path

from quantcore.execution.h024_runtime_no_mutation_safety_gate import (
    GATE_BLOCK_FLAGS,
    collect_h024_runtime_no_mutation_safety_gate,
    verify_h024_runtime_no_mutation_safety_gate_records,
)
from quantcore.execution.h024_runtime_safety_heartbeat import FORBIDDEN_AUTHORIZATION_KEYS
from quantcore.execution.h024_unified_read_only_post_canary_runtime_supervision import (
    PACKET_TYPE as UNIFIED_PACKET_TYPE,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

BROKER_MUTATION_CALLS = {
    "order_check",
    "order_send",
    "OrderCheck",
    "OrderSend",
    "position_close",
    "position_modify",
    "positions_close",
    "PositionClose",
    "PositionModify",
    "symbol_select",
    "SymbolSelect",
}

LEGACY_EXEMPT_PATH_NAMES = {
    "run_h024_one_shot_demo_canary.py",
    "h024_one_shot_demo_canary.py",
    "log_h024_mt5_terminal_preflight.py",
}


def unified_record(*, verdict: str = "PASS") -> dict[str, object]:
    return {
        "schema_version": 1,
        "strategy": "H024",
        "packet_type": UNIFIED_PACKET_TYPE,
        "observed_at_utc": "2026-05-12T00:00:00Z",
        "verdict": verdict,
        "violations": [] if verdict == "PASS" else [{"code": "SYNTHETIC_UNIFIED_FAILURE"}],
        "operator_state": (
            "UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED"
            if verdict == "PASS"
            else "FAIL_CLOSED_UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_BLOCKED"
        ),
        "operator_next_action": (
            "READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED"
            if verdict == "PASS"
            else "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
        ),
        "effective_new_entries_blocked": True,
        "authorizations": {key: False for key in FORBIDDEN_AUTHORIZATION_KEYS},
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "xauusd_order_authorized": False,
        "usdjpy_order_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
        "exact_known_canary": {
            "state": "OBSERVED_EXACT_KNOWN_CANARY",
            "observed": True,
        },
        "runtime_safety_aggregate": {
            "summary": {"verdict": "PASS", "operator_state": "RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED"},
            "record": {"verdict": "PASS"},
        },
        "canary_read_only_supervision": {
            "summary": {"record_count": 1, "all_records_passed": True, "embedded_violation_count": 0},
            "records": [{"verdict": "PASS", "violations": []}],
        },
    }


def test_gate_contract_passes_with_trusted_unified_supervision_but_authorizes_nothing() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == "NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED"
    assert record["gate_result"]["gate_opens_any_mutation_path"] is False
    assert record["gate_result"]["future_broker_facing_code_must_check_gate"] is True
    assert record["effective_new_entries_blocked"] is True
    for flag in GATE_BLOCK_FLAGS:
        assert record["gate_result"][flag] is True
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        assert record["authorizations"][key] is False
        assert record[key] is False


def test_gate_fails_closed_on_missing_unified_supervision() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=None,
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )

    assert record["verdict"] == "FAIL"
    assert record["operator_next_action"] == "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    assert any(check["name"] == "unified_supervision_record_object" and not check["passed"] for check in record["checks"])


def test_gate_fails_closed_on_malformed_unified_supervision() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record="malformed",  # type: ignore[arg-type]
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "unified_supervision_record_object" and not check["passed"] for check in record["checks"])


def test_gate_fails_closed_on_untrusted_unified_supervision_source() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="untrusted_clipboard",
        invoke_unified_supervision=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "unified_supervision_source_trusted" and not check["passed"] for check in record["checks"])


def test_gate_fails_closed_on_failed_unified_supervision() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(verdict="FAIL"),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "unified_supervision_verdict_pass" and not check["passed"] for check in record["checks"])


def test_gate_fails_closed_if_unified_operator_action_is_not_read_only() -> None:
    supplied = unified_record()
    supplied["operator_next_action"] = "UNSAFE_MUTATE"

    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=supplied,
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(
        check["name"] == "unified_supervision_operator_next_action_read_only" and not check["passed"]
        for check in record["checks"]
    )


def test_gate_fails_closed_if_unified_authorizes_order_send() -> None:
    supplied = unified_record()
    supplied["authorizations"]["order_send_authorized"] = True  # type: ignore[index]

    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=supplied,
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(
        check["name"] == "unified_supervision_authorizations_false" and not check["passed"]
        for check in record["checks"]
    )


def test_verifier_rejects_gate_that_opens_mutation_path() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )
    record["gate_result"]["gate_opens_any_mutation_path"] = True

    verification = verify_h024_runtime_no_mutation_safety_gate_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "GATE_OPENS_MUTATION_PATH"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_gate_block_flag_false() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )
    record["gate_result"]["order_send_blocked"] = False

    verification = verify_h024_runtime_no_mutation_safety_gate_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "GATE_BLOCK_FLAG_NOT_TRUE"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_missing_gate_contract() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )
    del record["gate_contract"]

    verification = verify_h024_runtime_no_mutation_safety_gate_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "GATE_CONTRACT_NOT_OBJECT"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_unified_supervision_section_missing() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )
    del record["unified_supervision"]

    verification = verify_h024_runtime_no_mutation_safety_gate_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNIFIED_SUPERVISION_SECTION_MISSING"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_top_level_authorization_true() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )
    record["order_send_authorized"] = True

    verification = verify_h024_runtime_no_mutation_safety_gate_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "TOP_LEVEL_UNSAFE_AUTHORIZATION"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_pass_record_with_embedded_violation() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=unified_record(),
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )
    record["violations"] = [{"code": "SHOULD_NOT_BE_IN_PASS_RECORD"}]

    verification = verify_h024_runtime_no_mutation_safety_gate_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_fail_closed_record_under_require_pass() -> None:
    record = collect_h024_runtime_no_mutation_safety_gate(
        unified_supervision_record=None,
        unified_supervision_source="test_fixture",
        invoke_unified_supervision=False,
    )

    verification = verify_h024_runtime_no_mutation_safety_gate_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RECORD_VERDICT_NOT_PASS"
        for violation in verification["verification_violations"]
    )


def _mutation_calls_in_file(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    calls: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in BROKER_MUTATION_CALLS:
            calls.append(func.attr)
        elif isinstance(func, ast.Name) and func.id in BROKER_MUTATION_CALLS:
            calls.append(func.id)
    return calls


def test_static_current_execution_code_has_no_unexempted_broker_mutation_call_sites() -> None:
    """Current non-exempt execution code must not contain direct broker mutation calls.

    Legacy exemptions are frozen pre-gate artifacts. They are not authorized by
    this gate and must not be treated as current execution adapters.
    """

    search_roots = [REPO_ROOT / "quantcore" / "execution", REPO_ROOT / "scripts"]
    violations: list[str] = []

    for root in search_roots:
        for path in root.rglob("*.py"):
            relative = path.relative_to(REPO_ROOT)
            if "tests" in relative.parts:
                continue
            if path.name in LEGACY_EXEMPT_PATH_NAMES:
                continue
            calls = _mutation_calls_in_file(path)
            if calls:
                violations.append(f"{relative}: {sorted(set(calls))}")

    assert violations == []


def test_static_gate_contract_module_itself_contains_no_broker_mutation_call_sites() -> None:
    path = REPO_ROOT / "quantcore" / "execution" / "h024_runtime_no_mutation_safety_gate.py"
    assert _mutation_calls_in_file(path) == []