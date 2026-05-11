from __future__ import annotations

import copy

from quantcore.execution.h024_phase4_demo_adapter_readiness_packet import (
    DECISION,
    KIND,
    SCHEMA,
    STATUS,
    build_readiness_packet_record,
    build_readiness_packet_records_from_files,
    read_jsonl,
    verify_readiness_packet_records,
    write_jsonl,
)


def _skeleton_record() -> dict:
    return {
        "schema": "h024_demo_execution_adapter_skeleton_v1",
        "kind": "DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED",
        "status": "DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED",
        "decision": "REFUSE_DISPATCH_NO_ORDER_AUTHORITY",
        "phase4_approved": True,
        "demo_execution_adapter_implementation_approved": True,
        "execution_adapter_implementation_approved": True,
        "execution_adapter_use_approved": False,
        "execution_adapter_approved": False,
        "broker_request_approved": False,
        "mt5_execution_approved": False,
        "terminal_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "dispatch_attempted": False,
        "terminal_mutated": False,
        "broker_state_mutated": False,
        "refusal_reasons": [
            "execution_adapter_use_not_approved",
            "demo_order_placement_not_approved",
            "execution_not_approved",
        ],
        "violations": [],
        "verdict": "PASS",
    }


def _intent_refusal_record() -> dict:
    return {
        "schema": "h024_demo_adapter_intent_refusal_audit_v1",
        "kind": "DEMO_ADAPTER_INTENT_REFUSAL_AUDIT",
        "status": "ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY",
        "decision": "REFUSE_DISPATCH_NO_ORDER_AUTHORITY",
        "phase4_approved": True,
        "demo_execution_adapter_implementation_approved": True,
        "execution_adapter_implementation_approved": True,
        "execution_adapter_use_approved": False,
        "execution_adapter_approved": False,
        "broker_request_approved": False,
        "mt5_execution_approved": False,
        "terminal_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "adapter_intent_ingested": True,
        "intent_envelope_constructed": True,
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
        "intent_envelope": {
            "context": {
                "account_server": "Exness-MT5Trial6",
                "normalized_symbol": "XAUUSD",
                "side": "short",
                "final_lots": 0.01,
            }
        },
        "violations": [],
        "verdict": "PASS",
    }


def _boundary_static_record() -> dict:
    return {
        "schema": "h024_demo_adapter_boundary_static_verifier_v1",
        "kind": "DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER",
        "status": "ADAPTER_IMPLEMENTATION_BOUNDARY_STATIC_VERIFIED",
        "decision": "ALLOW_IMPLEMENTATION_SURFACE_REVIEW_ONLY_NO_EXECUTION",
        "phase4_approved": True,
        "demo_execution_adapter_implementation_approved": True,
        "execution_adapter_implementation_approved": True,
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
        "adapter_boundary_static_verified": True,
        "target_count": 6,
        "prohibited_finding_count": 0,
        "target_files": [{"path": "quantcore/execution/h024_demo_execution_adapter_skeleton.py", "exists": True}],
        "violations": [],
        "verdict": "PASS",
    }


def test_builds_ready_review_only_packet() -> None:
    record = build_readiness_packet_record(
        skeleton_record=_skeleton_record(),
        intent_refusal_record=_intent_refusal_record(),
        boundary_static_record=_boundary_static_record(),
    )

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["readiness_packet_ready"] is True
    assert record["fail_closed_skeleton_verified"] is True
    assert record["real_intent_refusal_audit_verified"] is True
    assert record["adapter_boundary_static_verified"] is True
    assert record["execution_approved"] is False
    assert record["demo_order_placement_approved"] is False
    assert verify_readiness_packet_records(
        [record],
        allowed_demo_server="Exness-MT5Trial6",
        require_ready=True,
    ) == []


def test_valid_skeleton_without_top_level_verdict_is_allowed() -> None:
    skeleton = _skeleton_record()
    skeleton.pop("verdict")

    record = build_readiness_packet_record(
        skeleton_record=skeleton,
        intent_refusal_record=_intent_refusal_record(),
        boundary_static_record=_boundary_static_record(),
    )

    assert record["verdict"] == "PASS"
    assert record["fail_closed_skeleton_verified"] is True
    assert record["source_summaries"]["demo_execution_adapter_skeleton"]["verdict"] == "PASS"
    assert verify_readiness_packet_records(
        [record],
        allowed_demo_server="Exness-MT5Trial6",
        require_ready=True,
    ) == []


def test_skeleton_verdict_failure_blocks_packet() -> None:
    skeleton = _skeleton_record()
    skeleton["verdict"] = "FAIL"

    record = build_readiness_packet_record(
        skeleton_record=skeleton,
        intent_refusal_record=_intent_refusal_record(),
        boundary_static_record=_boundary_static_record(),
    )

    assert record["verdict"] == "FAIL"
    assert "demo_execution_adapter_skeleton_verdict_not_pass" in record["violations"]


def test_missing_required_refusal_reason_blocks_packet() -> None:
    intent = _intent_refusal_record()
    intent["refusal_reasons"] = ["execution_adapter_use_not_approved"]

    record = build_readiness_packet_record(
        skeleton_record=_skeleton_record(),
        intent_refusal_record=intent,
        boundary_static_record=_boundary_static_record(),
    )

    assert record["verdict"] == "FAIL"
    assert "demo_adapter_intent_refusal_audit_missing_refusal_reason:demo_order_placement_not_approved" in record["violations"]


def test_execution_authority_true_blocks_packet() -> None:
    intent = _intent_refusal_record()
    intent["execution_approved"] = True

    record = build_readiness_packet_record(
        skeleton_record=_skeleton_record(),
        intent_refusal_record=intent,
        boundary_static_record=_boundary_static_record(),
    )

    assert record["verdict"] == "FAIL"
    assert "demo_adapter_intent_refusal_audit_execution_approved_unexpectedly_true" in record["violations"]


def test_adapter_intent_not_ingested_blocks_packet() -> None:
    intent = _intent_refusal_record()
    intent["adapter_intent_ingested"] = False

    record = build_readiness_packet_record(
        skeleton_record=_skeleton_record(),
        intent_refusal_record=intent,
        boundary_static_record=_boundary_static_record(),
    )

    assert record["verdict"] == "FAIL"
    assert "demo_adapter_intent_refusal_audit_adapter_intent_ingested_not_true" in record["violations"]


def test_boundary_static_finding_blocks_packet() -> None:
    boundary = _boundary_static_record()
    boundary["prohibited_finding_count"] = 1
    boundary["adapter_boundary_static_verified"] = False
    boundary["verdict"] = "FAIL"

    record = build_readiness_packet_record(
        skeleton_record=_skeleton_record(),
        intent_refusal_record=_intent_refusal_record(),
        boundary_static_record=boundary,
    )

    assert record["verdict"] == "FAIL"
    assert "demo_adapter_boundary_static_verifier_prohibited_finding_count_nonzero" in record["violations"]


def test_verifier_rejects_mutated_execution_flag() -> None:
    record = build_readiness_packet_record(
        skeleton_record=_skeleton_record(),
        intent_refusal_record=_intent_refusal_record(),
        boundary_static_record=_boundary_static_record(),
    )
    mutated = copy.deepcopy(record)
    mutated["demo_order_placement_approved"] = True

    violations = verify_readiness_packet_records([mutated], require_ready=True)

    assert "record_0_demo_order_placement_approved_not_false" in violations


def test_allowed_demo_server_mismatch_is_violation() -> None:
    record = build_readiness_packet_record(
        skeleton_record=_skeleton_record(),
        intent_refusal_record=_intent_refusal_record(),
        boundary_static_record=_boundary_static_record(),
    )

    violations = verify_readiness_packet_records(
        [record],
        allowed_demo_server="Other-Demo-Server",
        require_ready=True,
    )

    assert any("allowed_demo_server_mismatch" in violation for violation in violations)


def test_file_round_trip_builds_and_verifies(tmp_path) -> None:
    skeleton_path = tmp_path / "skeleton.jsonl"
    intent_path = tmp_path / "intent_refusal.jsonl"
    boundary_path = tmp_path / "boundary.jsonl"
    packet_path = tmp_path / "packet.jsonl"

    write_jsonl(skeleton_path, [_skeleton_record()])
    write_jsonl(intent_path, [_intent_refusal_record()])
    write_jsonl(boundary_path, [_boundary_static_record()])

    records = build_readiness_packet_records_from_files(
        skeleton_jsonl=skeleton_path,
        intent_refusal_audit_jsonl=intent_path,
        boundary_static_verifier_jsonl=boundary_path,
    )
    write_jsonl(packet_path, records)

    loaded = read_jsonl(packet_path)

    assert loaded == records
    assert verify_readiness_packet_records(
        loaded,
        allowed_demo_server="Exness-MT5Trial6",
        require_ready=True,
    ) == []