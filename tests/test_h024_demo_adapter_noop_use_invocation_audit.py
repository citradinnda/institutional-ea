from __future__ import annotations

import json

import pytest

from quantcore.execution.h024_demo_adapter_noop_use_invocation_audit import (
    DECISION,
    KIND,
    NOOP_TRANSPORT_DECISION,
    NOOP_TRANSPORT_KIND,
    NOOP_TRANSPORT_SCHEMA,
    NOOP_USE_APPROVAL_DECISION,
    NOOP_USE_APPROVAL_KIND,
    NOOP_USE_APPROVAL_SCHEMA,
    SCHEMA,
    STATUS,
    build_noop_use_invocation_audit_record,
    read_single_jsonl_record,
    verify_noop_use_invocation_audit_record,
    write_single_jsonl_record,
)


def noop_use_approval_record() -> dict:
    return {
        "schema": NOOP_USE_APPROVAL_SCHEMA,
        "kind": NOOP_USE_APPROVAL_KIND,
        "status": "NOOP_ADAPTER_USE_APPROVED_NO_EXECUTION_AUTHORITY",
        "decision": NOOP_USE_APPROVAL_DECISION,
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
    }


def noop_transport_contract_record() -> dict:
    return {
        "schema": NOOP_TRANSPORT_SCHEMA,
        "kind": NOOP_TRANSPORT_KIND,
        "status": "NOOP_TRANSPORT_CONTRACT_READY_REFUSES_EXECUTION",
        "decision": NOOP_TRANSPORT_DECISION,
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
    }


def build_record() -> dict:
    return build_noop_use_invocation_audit_record(
        noop_use_approval=noop_use_approval_record(),
        noop_transport_contract=noop_transport_contract_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )


def test_builds_pass_invocation_audit_from_valid_inputs() -> None:
    record = build_record()

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["violations"] == []


def test_invokes_noop_path_but_refuses_broker_transport() -> None:
    record = build_record()

    assert record["authority"]["noop_adapter_use_approved"] is True
    assert record["invocation"]["noop_adapter_use_invoked"] is True
    assert record["invocation"]["noop_transport_contract_invoked"] is True
    assert record["invocation"]["broker_transport_refused"] is True
    assert record["mutation_safety"]["transport_dispatch_attempted"] is False


@pytest.mark.parametrize(
    "authority_key",
    [
        "execution_adapter_use_approved",
        "execution_adapter_approved",
        "broker_request_approved",
        "mt5_execution_approved",
        "terminal_mutation_approved",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_approved",
    ],
)
def test_fails_if_any_blocked_authority_flag_is_true(authority_key: str) -> None:
    record = build_record()
    record["authority"][authority_key] = True

    result = verify_noop_use_invocation_audit_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(authority_key in violation for violation in result.violations)


@pytest.mark.parametrize(
    "mutation_key",
    [
        "broker_request_constructed",
        "mt5_request_constructed",
        "order_payload_constructed",
        "transport_dispatch_attempted",
        "dispatch_attempted",
        "terminal_mutated",
        "broker_state_mutated",
    ],
)
def test_fails_if_any_mutation_or_dispatch_flag_is_true(mutation_key: str) -> None:
    record = build_record()
    record["mutation_safety"][mutation_key] = True

    result = verify_noop_use_invocation_audit_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(mutation_key in violation for violation in result.violations)


@pytest.mark.parametrize(
    "required_true_key",
    [
        "noop_transport_contract_available",
        "noop_adapter_use_invoked",
        "noop_transport_contract_invoked",
        "broker_transport_refused",
        "request_construction_refused",
    ],
)
def test_fails_if_required_invocation_flag_is_false(required_true_key: str) -> None:
    record = build_record()
    record["invocation"][required_true_key] = False

    result = verify_noop_use_invocation_audit_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(required_true_key in violation for violation in result.violations)


def test_fails_if_invocation_result_changes() -> None:
    record = build_record()
    record["invocation"]["invocation_result"] = "DISPATCHED"

    result = verify_noop_use_invocation_audit_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert "invocation_result must be NOOP_REFUSAL_NO_BROKER_TRANSPORT" in result.violations


def test_fails_if_noop_use_approval_is_not_pass() -> None:
    approval = noop_use_approval_record()
    approval["verdict"] = "FAIL"

    record = build_noop_use_invocation_audit_record(
        noop_use_approval=approval,
        noop_transport_contract=noop_transport_contract_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("noop_use_approval" in violation for violation in record["violations"])


def test_fails_if_noop_transport_contract_decision_changes() -> None:
    contract = noop_transport_contract_record()
    contract["decision"] = "ALLOW"

    record = build_noop_use_invocation_audit_record(
        noop_use_approval=noop_use_approval_record(),
        noop_transport_contract=contract,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("noop_transport_contract" in violation for violation in record["violations"])


def test_verifies_allowed_demo_server() -> None:
    result = verify_noop_use_invocation_audit_record(
        build_record(),
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert result.ok


def test_fails_wrong_allowed_demo_server() -> None:
    result = verify_noop_use_invocation_audit_record(
        build_record(),
        allowed_demo_server="WrongServer",
        require_pass=True,
    )

    assert not result.ok
    assert "allowed demo server not observed: WrongServer" in result.violations


def test_round_trips_jsonl(tmp_path) -> None:
    record = build_record()
    path = tmp_path / "noop_use_invocation_audit.jsonl"

    write_single_jsonl_record(path, record)
    loaded = read_single_jsonl_record(path)

    assert loaded == json.loads(json.dumps(record, sort_keys=True))