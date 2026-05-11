from __future__ import annotations

import json

import pytest

from quantcore.execution.h024_demo_adapter_noop_transport_contract import (
    DECISION,
    INTENT_REFUSAL_AUDIT_DECISION,
    INTENT_REFUSAL_AUDIT_KIND,
    INTENT_REFUSAL_AUDIT_SCHEMA,
    KIND,
    READINESS_HUMAN_DECISION_DECISION,
    READINESS_HUMAN_DECISION_KIND,
    READINESS_HUMAN_DECISION_SCHEMA,
    REQUIRED_REFUSAL_REASONS,
    SCHEMA,
    STATUS,
    build_noop_transport_contract_record,
    read_single_jsonl_record,
    verify_noop_transport_contract_record,
    write_single_jsonl_record,
)


def readiness_record() -> dict:
    return {
        "schema": READINESS_HUMAN_DECISION_SCHEMA,
        "kind": READINESS_HUMAN_DECISION_KIND,
        "status": "ADAPTER_READINESS_REVIEW_APPROVED_NO_EXECUTION_AUTHORITY",
        "decision": READINESS_HUMAN_DECISION_DECISION,
        "verdict": "PASS",
        "violations": 0,
        "account": {"server": "Exness-MT5Trial6"},
    }


def intent_record() -> dict:
    return {
        "schema": INTENT_REFUSAL_AUDIT_SCHEMA,
        "kind": INTENT_REFUSAL_AUDIT_KIND,
        "status": "ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY",
        "decision": INTENT_REFUSAL_AUDIT_DECISION,
        "verdict": "PASS",
        "violations": 0,
        "account": {"server": "Exness-MT5Trial6"},
        "mutation_safety": {
            "broker_request_constructed": False,
            "mt5_request_constructed": False,
            "order_payload_constructed": False,
            "dispatch_attempted": False,
            "terminal_mutated": False,
            "broker_state_mutated": False,
        },
    }


def build_record() -> dict:
    return build_noop_transport_contract_record(
        readiness_human_decision=readiness_record(),
        intent_refusal_audit=intent_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )


def test_builds_pass_record_from_valid_inputs() -> None:
    record = build_record()

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["violations"] == []


def test_refuses_transport_because_adapter_use_is_not_approved() -> None:
    record = build_record()

    assert record["authority"]["execution_adapter_use_approved"] is False
    assert record["contract"]["transport_decision"] == "REFUSE"
    assert "execution_adapter_use_not_approved" in record["contract"]["refusal_reasons"]


@pytest.mark.parametrize(
    "authority_key",
    [
        "execution_adapter_use_approved",
        "demo_order_placement_approved",
        "execution_approved",
        "broker_request_approved",
        "mt5_execution_approved",
        "terminal_mutation_approved",
        "live_order_placement_approved",
    ],
)
def test_fails_if_blocked_authority_flag_is_unexpectedly_true(authority_key: str) -> None:
    record = build_record()
    record["authority"][authority_key] = True

    result = verify_noop_transport_contract_record(
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

    result = verify_noop_transport_contract_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(mutation_key in violation for violation in result.violations)


def test_fails_if_required_refusal_reasons_are_missing() -> None:
    record = build_record()
    record["contract"]["refusal_reasons"] = ["execution_adapter_use_not_approved"]

    result = verify_noop_transport_contract_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert "missing refusal reason: demo_order_placement_not_approved" in result.violations
    assert "missing refusal reason: execution_not_approved" in result.violations


def test_verifies_allowed_demo_server() -> None:
    record = build_record()

    result = verify_noop_transport_contract_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert result.ok


def test_fails_wrong_allowed_demo_server() -> None:
    record = build_record()

    result = verify_noop_transport_contract_record(
        record,
        allowed_demo_server="WrongServer",
        require_pass=True,
    )

    assert not result.ok
    assert "allowed demo server not observed: WrongServer" in result.violations


def test_round_trips_jsonl(tmp_path) -> None:
    record = build_record()
    path = tmp_path / "contract.jsonl"

    write_single_jsonl_record(path, record)
    loaded = read_single_jsonl_record(path)

    assert loaded == json.loads(json.dumps(record, sort_keys=True))


def test_fails_if_upstream_readiness_decision_is_not_approval() -> None:
    readiness = readiness_record()
    readiness["decision"] = "PENDING"

    record = build_noop_transport_contract_record(
        readiness_human_decision=readiness,
        intent_refusal_audit=intent_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("readiness_human_decision" in violation for violation in record["violations"])


def test_fails_if_upstream_intent_refusal_is_not_refusal() -> None:
    intent = intent_record()
    intent["decision"] = "ALLOW"

    record = build_noop_transport_contract_record(
        readiness_human_decision=readiness_record(),
        intent_refusal_audit=intent,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("intent_refusal_audit" in violation for violation in record["violations"])


def test_required_refusal_reasons_constant_matches_contract() -> None:
    record = build_record()

    assert tuple(record["contract"]["refusal_reasons"]) == REQUIRED_REFUSAL_REASONS