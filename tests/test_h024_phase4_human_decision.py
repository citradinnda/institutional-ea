from __future__ import annotations

import json
from pathlib import Path

import pytest

from quantcore.execution.h024_phase4_human_decision import (
    Phase4HumanDecisionError,
    Phase4HumanDecisionInputs,
    build_phase4_human_decision,
    verify_phase4_human_decision_jsonl,
    write_jsonl_record,
)


def _valid_review_packet() -> dict:
    return {
        "schema": "h024_phase4_review_packet_v1",
        "kind": "PHASE4_REVIEW_PACKET_REVIEW_ONLY",
        "status": "READY_FOR_HUMAN_PHASE4_REVIEW",
        "allowed_demo_server": "Exness-MT5Trial6",
        "human_review_required": True,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "execution_approved": False,
        "stable_intent_id": "af20bcb4a54f6b51aafadeb15a65320bf9c448dbae20cf33066da3cd5adb4363",
        "execution_boundary": {
            "mt5_access_approved": False,
            "broker_request_construction_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_adapter_approved": False,
            "order_send_approved": False,
            "order_check_approved": False,
            "explicit_allow_state_is_execution_approval": False,
        },
        "required_artifacts": [{}, {}, {}, {}, {}],
        "gate_checks": {
            "phase4_readiness_review_ready": True,
            "execution_safety_controls_design_verified": True,
            "default_missing_kill_switch_blocks": True,
            "operator_control_state_snapshot_verified": True,
            "explicit_allow_state_preflight_passes_review_only": True,
            "all_approval_flags_false": True,
            "no_execution_like_fields_present": True,
        },
    }


def _inputs(tmp_path: Path) -> Phase4HumanDecisionInputs:
    path = tmp_path / "reports" / "h024_standard_demo_phase4_review_packet.jsonl"
    write_jsonl_record(path, _valid_review_packet())
    return Phase4HumanDecisionInputs(review_packet_jsonl=path)


def test_build_approved_phase4_human_decision_without_execution_approval(tmp_path: Path) -> None:
    record = build_phase4_human_decision(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve Phase 4 only; no execution permission.",
        decided_utc="2026-05-11T00:00:00Z",
    )

    assert record["schema"] == "h024_phase4_human_decision_v1"
    assert record["kind"] == "PHASE4_HUMAN_DECISION_REVIEW_ONLY"
    assert record["decision"] == "APPROVE_PHASE4_NO_EXECUTION"
    assert record["status"] == "PHASE4_APPROVED_NO_EXECUTION_AUTHORITY"
    assert record["phase4_approved"] is True
    assert record["demo_order_placement_approved"] is False
    assert record["live_order_placement_approved"] is False
    assert record["execution_adapter_implementation_approved"] is False
    assert record["execution_approved"] is False
    assert record["execution_boundary"]["order_send_approved"] is False


def test_build_rejected_phase4_human_decision(tmp_path: Path) -> None:
    record = build_phase4_human_decision(
        _inputs(tmp_path),
        decision="reject",
        operator_id="operator",
        operator_statement="Reject Phase 4.",
        decided_utc="2026-05-11T00:00:00Z",
    )

    assert record["decision"] == "REJECT_PHASE4_NO_EXECUTION"
    assert record["status"] == "PHASE4_REJECTED_NO_EXECUTION_AUTHORITY"
    assert record["phase4_approved"] is False
    assert record["execution_approved"] is False


def test_build_requires_operator_statement(tmp_path: Path) -> None:
    with pytest.raises(Phase4HumanDecisionError, match="operator_statement"):
        build_phase4_human_decision(
            _inputs(tmp_path),
            decision="approve",
            operator_id="operator",
            operator_statement=" ",
        )


def test_build_rejects_invalid_review_packet(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    write_jsonl_record(path, {"schema": "wrong"})
    inputs = Phase4HumanDecisionInputs(review_packet_jsonl=path)

    with pytest.raises(Phase4HumanDecisionError, match="review packet verifier failed"):
        build_phase4_human_decision(
            inputs,
            decision="approve",
            operator_id="operator",
            operator_statement="Approve Phase 4 only.",
        )


def test_verify_accepts_required_approved_record(tmp_path: Path) -> None:
    record = build_phase4_human_decision(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve Phase 4 only.",
        decided_utc="2026-05-11T00:00:00Z",
    )
    output = tmp_path / "decision.jsonl"
    write_jsonl_record(output, record)

    records, violations = verify_phase4_human_decision_jsonl(
        output,
        allowed_demo_server="Exness-MT5Trial6",
        require_approved=True,
    )

    assert len(records) == 1
    assert violations == []


def test_verify_rejects_execution_approval(tmp_path: Path) -> None:
    record = build_phase4_human_decision(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve Phase 4 only.",
        decided_utc="2026-05-11T00:00:00Z",
    )
    record["execution_approved"] = True
    output = tmp_path / "decision.jsonl"
    write_jsonl_record(output, record)

    _, violations = verify_phase4_human_decision_jsonl(output, require_approved=True)

    assert any("execution_approved" in violation for violation in violations)


def test_verify_rejects_forbidden_execution_like_field(tmp_path: Path) -> None:
    record = build_phase4_human_decision(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve Phase 4 only.",
        decided_utc="2026-05-11T00:00:00Z",
    )
    record["mql_trade_request"] = {}
    output = tmp_path / "decision.jsonl"
    write_jsonl_record(output, record)

    _, violations = verify_phase4_human_decision_jsonl(output, require_approved=True)

    assert any("forbidden execution-like field" in violation for violation in violations)