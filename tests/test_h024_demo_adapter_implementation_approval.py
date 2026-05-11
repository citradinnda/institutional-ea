from __future__ import annotations

import json
from pathlib import Path

import pytest

from quantcore.execution.h024_demo_adapter_implementation_approval import (
    DemoAdapterImplementationApprovalError,
    DemoAdapterImplementationApprovalInputs,
    build_demo_adapter_implementation_approval,
    verify_demo_adapter_implementation_approval_jsonl,
    write_jsonl_record,
)


def _valid_phase4_human_decision() -> dict:
    return {
        "schema": "h024_phase4_human_decision_v1",
        "kind": "PHASE4_HUMAN_DECISION_REVIEW_ONLY",
        "status": "PHASE4_APPROVED_NO_EXECUTION_AUTHORITY",
        "decision": "APPROVE_PHASE4_NO_EXECUTION",
        "allowed_demo_server": "Exness-MT5Trial6",
        "operator_id": "operator",
        "operator_statement": "Approve Phase 4 only.",
        "phase4_approved": True,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_implementation_approved": False,
        "execution_adapter_approved": False,
        "execution_approved": False,
        "execution_boundary": {
            "mt5_access_approved": False,
            "broker_request_construction_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_adapter_implementation_approved": False,
            "execution_adapter_approved": False,
            "order_send_approved": False,
            "order_check_approved": False,
            "execution_approved": False,
        },
    }


def _inputs(tmp_path: Path) -> DemoAdapterImplementationApprovalInputs:
    path = tmp_path / "reports" / "h024_standard_demo_phase4_human_decision.jsonl"
    write_jsonl_record(path, _valid_phase4_human_decision())
    return DemoAdapterImplementationApprovalInputs(phase4_human_decision_jsonl=path)


def test_build_approved_demo_adapter_implementation_without_execution_approval(tmp_path: Path) -> None:
    record = build_demo_adapter_implementation_approval(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve implementation only; no order placement.",
        decided_utc="2026-05-11T00:00:00Z",
    )

    assert record["schema"] == "h024_demo_adapter_implementation_approval_v1"
    assert record["kind"] == "DEMO_ADAPTER_IMPLEMENTATION_APPROVAL_REVIEW_ONLY"
    assert record["decision"] == "APPROVE_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT"
    assert record["status"] == "DEMO_ADAPTER_IMPLEMENTATION_APPROVED_NO_ORDER_AUTHORITY"
    assert record["phase4_approved"] is True
    assert record["demo_execution_adapter_implementation_approved"] is True
    assert record["execution_adapter_implementation_approved"] is True
    assert record["execution_adapter_approved"] is False
    assert record["demo_order_placement_approved"] is False
    assert record["live_order_placement_approved"] is False
    assert record["execution_approved"] is False
    assert record["implementation_scope"]["fail_closed_adapter_skeleton_allowed"] is True
    assert record["implementation_scope"]["mt5_import_allowed"] is False
    assert record["execution_boundary"]["order_send_approved"] is False


def test_build_rejected_demo_adapter_implementation(tmp_path: Path) -> None:
    record = build_demo_adapter_implementation_approval(
        _inputs(tmp_path),
        decision="reject",
        operator_id="operator",
        operator_statement="Reject implementation.",
        decided_utc="2026-05-11T00:00:00Z",
    )

    assert record["decision"] == "REJECT_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT"
    assert record["status"] == "DEMO_ADAPTER_IMPLEMENTATION_REJECTED_NO_ORDER_AUTHORITY"
    assert record["demo_execution_adapter_implementation_approved"] is False
    assert record["execution_adapter_implementation_approved"] is False
    assert record["execution_approved"] is False


def test_build_requires_phase4_approval(tmp_path: Path) -> None:
    phase4 = _valid_phase4_human_decision()
    phase4["phase4_approved"] = False
    path = tmp_path / "phase4.jsonl"
    write_jsonl_record(path, phase4)

    with pytest.raises(DemoAdapterImplementationApprovalError, match="Phase 4 human decision verifier failed"):
        build_demo_adapter_implementation_approval(
            DemoAdapterImplementationApprovalInputs(phase4_human_decision_jsonl=path),
            decision="approve",
            operator_id="operator",
            operator_statement="Approve implementation only.",
        )


def test_build_requires_operator_statement(tmp_path: Path) -> None:
    with pytest.raises(DemoAdapterImplementationApprovalError, match="operator_statement"):
        build_demo_adapter_implementation_approval(
            _inputs(tmp_path),
            decision="approve",
            operator_id="operator",
            operator_statement=" ",
        )


def test_verify_accepts_required_approved_record(tmp_path: Path) -> None:
    record = build_demo_adapter_implementation_approval(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve implementation only.",
        decided_utc="2026-05-11T00:00:00Z",
    )
    output = tmp_path / "approval.jsonl"
    write_jsonl_record(output, record)

    records, violations = verify_demo_adapter_implementation_approval_jsonl(
        output,
        allowed_demo_server="Exness-MT5Trial6",
        require_approved=True,
    )

    assert len(records) == 1
    assert violations == []


def test_verify_rejects_demo_order_approval(tmp_path: Path) -> None:
    record = build_demo_adapter_implementation_approval(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve implementation only.",
        decided_utc="2026-05-11T00:00:00Z",
    )
    record["demo_order_placement_approved"] = True
    output = tmp_path / "approval.jsonl"
    write_jsonl_record(output, record)

    _, violations = verify_demo_adapter_implementation_approval_jsonl(output, require_approved=True)

    assert any("demo_order_placement_approved" in violation for violation in violations)


def test_verify_rejects_forbidden_execution_like_field(tmp_path: Path) -> None:
    record = build_demo_adapter_implementation_approval(
        _inputs(tmp_path),
        decision="approve",
        operator_id="operator",
        operator_statement="Approve implementation only.",
        decided_utc="2026-05-11T00:00:00Z",
    )
    record["broker_request"] = {}
    output = tmp_path / "approval.jsonl"
    write_jsonl_record(output, record)

    _, violations = verify_demo_adapter_implementation_approval_jsonl(output, require_approved=True)

    assert any("forbidden execution-like field" in violation for violation in violations)