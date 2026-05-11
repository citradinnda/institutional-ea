from __future__ import annotations

import copy

from quantcore.execution.h024_phase4_demo_adapter_readiness_human_decision import (
    DECISION,
    KIND,
    SCHEMA,
    STATUS,
    build_human_decision_record,
    build_human_decision_records_from_file,
    read_jsonl,
    verify_human_decision_records,
    write_jsonl,
)


def _readiness_packet() -> dict:
    return {
        "schema": "h024_phase4_demo_adapter_readiness_packet_v1",
        "kind": "PHASE4_DEMO_ADAPTER_READINESS_PACKET_REVIEW_ONLY",
        "status": "READY_FOR_HUMAN_ADAPTER_READINESS_REVIEW_NO_EXECUTION",
        "decision": "REVIEW_ONLY_NO_EXECUTION_AUTHORITY",
        "verdict": "PASS",
        "upstream_artifact_count": 3,
        "phase4_approved": True,
        "demo_execution_adapter_implementation_approved": True,
        "execution_adapter_implementation_approved": True,
        "fail_closed_skeleton_verified": True,
        "real_intent_refusal_audit_verified": True,
        "adapter_boundary_static_verified": True,
        "execution_authority_remains_absent": True,
        "readiness_packet_ready": True,
        "execution_adapter_use_approved": False,
        "execution_adapter_approved": False,
        "broker_request_approved": False,
        "mt5_execution_approved": False,
        "terminal_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "broker_request_constructed": False,
        "mt5_request_constructed": False,
        "order_payload_constructed": False,
        "dispatch_attempted": False,
        "terminal_mutated": False,
        "broker_state_mutated": False,
        "refusal_reasons": [
            "execution_adapter_use_not_approved",
            "demo_order_placement_not_approved",
            "execution_not_approved",
        ],
        "source_summaries": {
            "demo_adapter_intent_refusal_audit": {
                "server_values": ["Exness-MT5Trial6"],
            }
        },
        "violations": [],
    }


def test_builds_review_only_human_decision_without_execution_authority() -> None:
    record = build_human_decision_record(_readiness_packet(), decided_by="operator")

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["adapter_readiness_review_approved"] is True
    assert record["execution_adapter_use_approved"] is False
    assert record["demo_order_placement_approved"] is False
    assert record["execution_approved"] is False
    assert verify_human_decision_records(
        [record],
        allowed_demo_server="Exness-MT5Trial6",
        require_approved=True,
    ) == []


def test_rejects_wrong_decision() -> None:
    record = build_human_decision_record(
        _readiness_packet(),
        decision="APPROVE_ADAPTER_USE",
    )

    assert record["verdict"] == "FAIL"
    assert "unsupported_decision_for_adapter_readiness_human_gate" in record["violations"]


def test_rejects_not_ready_packet() -> None:
    packet = _readiness_packet()
    packet["readiness_packet_ready"] = False

    record = build_human_decision_record(packet)

    assert record["verdict"] == "FAIL"
    assert "readiness_packet_readiness_packet_ready_not_true" in record["violations"]


def test_rejects_packet_with_demo_order_approval() -> None:
    packet = _readiness_packet()
    packet["demo_order_placement_approved"] = True

    record = build_human_decision_record(packet)

    assert record["verdict"] == "FAIL"
    assert "readiness_packet_demo_order_placement_approved_not_false" in record["violations"]


def test_rejects_packet_with_dispatch_attempt() -> None:
    packet = _readiness_packet()
    packet["dispatch_attempted"] = True

    record = build_human_decision_record(packet)

    assert record["verdict"] == "FAIL"
    assert "readiness_packet_dispatch_attempted_not_false" in record["violations"]


def test_rejects_missing_refusal_reason() -> None:
    packet = _readiness_packet()
    packet["refusal_reasons"] = ["execution_not_approved"]

    record = build_human_decision_record(packet)

    assert record["verdict"] == "FAIL"
    assert "readiness_packet_missing_refusal_reason:demo_order_placement_not_approved" in record["violations"]


def test_verifier_rejects_mutated_output_execution_flag() -> None:
    record = build_human_decision_record(_readiness_packet())
    mutated = copy.deepcopy(record)
    mutated["execution_approved"] = True

    violations = verify_human_decision_records([mutated], require_approved=True)

    assert "record_0_execution_approved_not_false" in violations


def test_verifier_rejects_mutated_non_authorization() -> None:
    record = build_human_decision_record(_readiness_packet())
    mutated = copy.deepcopy(record)
    mutated["explicit_non_authorizations"]["adapter_use"] = True

    violations = verify_human_decision_records([mutated], require_approved=True)

    assert "record_0_explicit_non_authorization_adapter_use_not_false" in violations


def test_allowed_demo_server_mismatch_is_violation() -> None:
    record = build_human_decision_record(_readiness_packet())

    violations = verify_human_decision_records(
        [record],
        allowed_demo_server="Other-Demo-Server",
        require_approved=True,
    )

    assert any("allowed_demo_server_mismatch" in violation for violation in violations)


def test_file_round_trip_builds_and_verifies(tmp_path) -> None:
    packet_path = tmp_path / "packet.jsonl"
    decision_path = tmp_path / "decision.jsonl"

    write_jsonl(packet_path, [_readiness_packet()])

    records = build_human_decision_records_from_file(
        packet_path,
        decision=DECISION,
        decided_by="operator",
    )
    write_jsonl(decision_path, records)
    loaded = read_jsonl(decision_path)

    assert loaded == records
    assert verify_human_decision_records(
        loaded,
        allowed_demo_server="Exness-MT5Trial6",
        require_approved=True,
    ) == []