from __future__ import annotations

import copy

from quantcore.execution.h024_demo_adapter_intent_refusal_audit import (
    DECISION,
    KIND,
    SCHEMA,
    STATUS,
    build_audit_record,
    build_audit_records_from_files,
    read_jsonl,
    verify_audit_records,
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
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "refusal_reasons": [
            "execution_adapter_use_not_approved",
            "demo_order_placement_not_approved",
            "execution_not_approved",
        ],
        "dispatch_attempted": False,
        "terminal_mutated": False,
        "broker_state_mutated": False,
        "verdict": "PASS",
    }


def _intent_record() -> dict:
    return {
        "schema": "h024_order_intent_simulation_v1",
        "kind": "ORDER_INTENT_SIMULATION",
        "status": "ORDER_INTENT_SIMULATED_REVIEW_ONLY",
        "verdict": "PASS",
        "account_server": "Exness-MT5Trial6",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "timeframe": "H4",
        "side": "short",
        "entry": 4930.041,
        "stop": 5019.068,
        "risk_usd": 100.0,
        "final_lots": 0.01,
        "intent": {
            "closed_h4_time": "2026.03.18 08:00:00",
            "tick_size": 0.001,
            "tick_value_usd_per_lot": 0.1,
        },
    }


def _safety_record() -> dict:
    return {
        "schema": "h024_execution_safety_controls_preflight_v1",
        "kind": "EXECUTION_SAFETY_CONTROLS_ALLOW_STATE_PREFLIGHT",
        "status": "PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL",
        "phase4_approved": True,
        "execution_approved": False,
        "verdict": "PASS",
    }


def test_builds_pass_record_for_realistic_intent_refusal_context() -> None:
    record = build_audit_record(
        _skeleton_record(),
        _intent_record(),
        safety_preflight_record=_safety_record(),
    )

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["adapter_intent_ingested"] is True
    assert record["broker_request_constructed"] is False
    assert record["dispatch_attempted"] is False
    assert record["terminal_mutated"] is False
    assert record["broker_state_mutated"] is False
    assert verify_audit_records([record], allowed_demo_server="Exness-MT5Trial6", require_refusal=True) == []


def test_missing_phase4_approval_fails_closed() -> None:
    skeleton = _skeleton_record()
    skeleton["phase4_approved"] = False

    record = build_audit_record(skeleton, _intent_record())

    assert record["verdict"] == "FAIL"
    assert "phase4_not_approved" in record["violations"]


def test_execution_approval_in_source_is_rejected() -> None:
    intent = _intent_record()
    intent["execution_approved"] = True

    record = build_audit_record(_skeleton_record(), intent)

    assert record["verdict"] == "FAIL"
    assert "execution_approved_unexpectedly_true" in record["violations"]


def test_source_broker_or_mt5_payload_is_not_copied_into_audit_envelope() -> None:
    intent = _intent_record()
    intent["broker_request"] = {"symbol": "XAUUSDm"}
    intent["mt5_request"] = {"symbol": "XAUUSDm"}

    record = build_audit_record(_skeleton_record(), intent)

    assert record["verdict"] == "PASS"
    assert "broker_request" not in record["intent_envelope"]["context"]
    assert "mt5_request" not in record["intent_envelope"]["context"]
    assert verify_audit_records([record], allowed_demo_server="Exness-MT5Trial6", require_refusal=True) == []


def test_verifier_rejects_any_dispatch_or_mutation_claim() -> None:
    record = build_audit_record(_skeleton_record(), _intent_record())
    record["dispatch_attempted"] = True

    violations = verify_audit_records([record], require_refusal=True)

    assert "record_0_dispatch_attempted_not_false" in violations


def test_file_round_trip_builds_and_verifies(tmp_path) -> None:
    skeleton_path = tmp_path / "skeleton.jsonl"
    intent_path = tmp_path / "intent.jsonl"
    safety_path = tmp_path / "safety.jsonl"
    output_path = tmp_path / "audit.jsonl"

    write_jsonl(skeleton_path, [_skeleton_record()])
    write_jsonl(intent_path, [_intent_record()])
    write_jsonl(safety_path, [_safety_record()])

    records = build_audit_records_from_files(
        skeleton_jsonl=skeleton_path,
        order_intent_simulation_jsonl=intent_path,
        safety_preflight_jsonl=safety_path,
    )
    write_jsonl(output_path, records)
    loaded = read_jsonl(output_path)

    assert len(loaded) == 1
    assert verify_audit_records(loaded, allowed_demo_server="Exness-MT5Trial6", require_refusal=True) == []


def test_allowed_demo_server_mismatch_is_a_violation() -> None:
    record = build_audit_record(_skeleton_record(), _intent_record())

    violations = verify_audit_records([record], allowed_demo_server="Other-Demo-Server", require_refusal=True)

    assert any("allowed_demo_server_mismatch" in violation for violation in violations)


def test_verifier_rejects_prohibited_payload_key_in_output() -> None:
    record = build_audit_record(_skeleton_record(), _intent_record())
    mutated = copy.deepcopy(record)
    mutated["intent_envelope"]["broker_request"] = {"symbol": "XAUUSDm"}

    violations = verify_audit_records([mutated], require_refusal=True)

    assert "record_0_prohibited_payload_key:intent_envelope.broker_request" in violations