from __future__ import annotations

import json

import pytest

from quantcore.execution.h024_phase4_demo_adapter_use_readiness_human_decision import (
    DECISION,
    KIND,
    PACKET_DECISION,
    PACKET_KIND,
    PACKET_SCHEMA,
    SCHEMA,
    STATUS,
    build_adapter_use_readiness_human_decision_record,
    read_single_jsonl_record,
    verify_adapter_use_readiness_human_decision_record,
    write_single_jsonl_record,
)


def packet_record() -> dict:
    return {
        "schema": PACKET_SCHEMA,
        "kind": PACKET_KIND,
        "status": "READY_FOR_HUMAN_ADAPTER_USE_REVIEW_NO_EXECUTION",
        "decision": PACKET_DECISION,
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
    }


def build_record() -> dict:
    return build_adapter_use_readiness_human_decision_record(
        adapter_use_readiness_packet=packet_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )


def test_builds_pass_human_decision_from_valid_packet() -> None:
    record = build_record()

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["violations"] == []


def test_approves_adapter_use_readiness_review_only() -> None:
    record = build_record()

    assert record["authority"]["adapter_use_readiness_review_approved"] is True
    assert record["decision_scope"]["approved_scope"] == "adapter_use_readiness_review_only"
    assert record["authority"]["execution_adapter_use_approved"] is False
    assert record["authority"]["execution_approved"] is False


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

    result = verify_adapter_use_readiness_human_decision_record(
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

    result = verify_adapter_use_readiness_human_decision_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(mutation_key in violation for violation in result.violations)


def test_fails_if_packet_is_not_pass() -> None:
    packet = packet_record()
    packet["verdict"] = "FAIL"

    record = build_adapter_use_readiness_human_decision_record(
        adapter_use_readiness_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("adapter_use_readiness_packet" in violation for violation in record["violations"])


def test_fails_if_packet_decision_changes() -> None:
    packet = packet_record()
    packet["decision"] = "ALLOW"

    record = build_adapter_use_readiness_human_decision_record(
        adapter_use_readiness_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("adapter_use_readiness_packet" in violation for violation in record["violations"])


def test_fails_if_approved_scope_changes() -> None:
    record = build_record()
    record["decision_scope"]["approved_scope"] = "adapter_use"

    result = verify_adapter_use_readiness_human_decision_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert "approved_scope must be adapter_use_readiness_review_only" in result.violations


def test_verifies_allowed_demo_server() -> None:
    result = verify_adapter_use_readiness_human_decision_record(
        build_record(),
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert result.ok


def test_fails_wrong_allowed_demo_server() -> None:
    result = verify_adapter_use_readiness_human_decision_record(
        build_record(),
        allowed_demo_server="WrongServer",
        require_pass=True,
    )

    assert not result.ok
    assert "allowed demo server not observed: WrongServer" in result.violations


def test_round_trips_jsonl(tmp_path) -> None:
    record = build_record()
    path = tmp_path / "adapter_use_readiness_human_decision.jsonl"

    write_single_jsonl_record(path, record)
    loaded = read_single_jsonl_record(path)

    assert loaded == json.loads(json.dumps(record, sort_keys=True))