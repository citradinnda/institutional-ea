from __future__ import annotations

from pathlib import Path

import pytest

from quantcore.execution.h024_demo_execution_adapter_skeleton import (
    DemoExecutionAdapterSkeletonError,
    DemoExecutionAdapterSkeletonInputs,
    build_demo_execution_adapter_skeleton,
    evaluate_refusal_reasons,
    verify_demo_execution_adapter_skeleton_jsonl,
    write_jsonl_record,
)
from quantcore.execution.h024_demo_execution_adapter_skeleton import DemoExecutionAdapterAuthority


def _valid_implementation_approval() -> dict:
    return {
        "schema": "h024_demo_adapter_implementation_approval_v1",
        "kind": "DEMO_ADAPTER_IMPLEMENTATION_APPROVAL_REVIEW_ONLY",
        "status": "DEMO_ADAPTER_IMPLEMENTATION_APPROVED_NO_ORDER_AUTHORITY",
        "decision": "APPROVE_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT",
        "operator_id": "operator",
        "operator_statement": "Approve implementation only.",
        "allowed_demo_server": "Exness-MT5Trial6",
        "phase4_approved": True,
        "demo_execution_adapter_implementation_approved": True,
        "execution_adapter_implementation_approved": True,
        "execution_adapter_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "implementation_scope": {
            "demo_only": True,
            "pure_python_contracts_allowed": True,
            "fail_closed_adapter_skeleton_allowed": True,
            "mt5_import_allowed": False,
            "terminal_mutation_allowed": False,
            "broker_request_construction_allowed": False,
            "order_placement_allowed": False,
            "live_trading_allowed": False,
            "execution_allowed": False,
        },
        "execution_boundary": {
            "mt5_access_approved": False,
            "terminal_mutation_approved": False,
            "broker_request_construction_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_adapter_approved": False,
            "order_send_approved": False,
            "order_check_approved": False,
            "execution_approved": False,
        },
    }


def _inputs(tmp_path: Path) -> DemoExecutionAdapterSkeletonInputs:
    path = tmp_path / "reports" / "h024_standard_demo_demo_adapter_implementation_approval.jsonl"
    write_jsonl_record(path, _valid_implementation_approval())
    return DemoExecutionAdapterSkeletonInputs(implementation_approval_jsonl=path)


def test_build_fail_closed_demo_execution_adapter_skeleton(tmp_path: Path) -> None:
    record = build_demo_execution_adapter_skeleton(
        _inputs(tmp_path),
        created_utc="2026-05-11T00:00:00Z",
    )

    assert record["schema"] == "h024_demo_execution_adapter_skeleton_v1"
    assert record["kind"] == "DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED"
    assert record["status"] == "DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED"
    assert record["decision"] == "REFUSE_DISPATCH_NO_ORDER_AUTHORITY"
    assert record["phase4_approved"] is True
    assert record["demo_execution_adapter_implementation_approved"] is True
    assert record["execution_adapter_approved"] is False
    assert record["demo_order_placement_approved"] is False
    assert record["execution_approved"] is False
    assert "execution_adapter_use_not_approved" in record["refusal_reasons"]
    assert "demo_order_placement_not_approved" in record["refusal_reasons"]
    assert "execution_not_approved" in record["refusal_reasons"]
    assert record["transport_result"]["dispatch_attempted"] is False
    assert record["transport_result"]["terminal_mutated"] is False
    assert record["transport_result"]["broker_state_mutated"] is False
    assert record["adapter_boundary"]["pure_python_only"] is True
    assert record["adapter_boundary"]["mt5_imported"] is False


def test_build_requires_implementation_approval(tmp_path: Path) -> None:
    approval = _valid_implementation_approval()
    approval["execution_adapter_implementation_approved"] = False
    path = tmp_path / "approval.jsonl"
    write_jsonl_record(path, approval)

    with pytest.raises(DemoExecutionAdapterSkeletonError, match="implementation approval verifier failed"):
        build_demo_execution_adapter_skeleton(
            DemoExecutionAdapterSkeletonInputs(implementation_approval_jsonl=path)
        )


def test_refusal_reasons_remain_fail_closed_even_if_all_flags_true() -> None:
    authority = DemoExecutionAdapterAuthority(
        phase4_approved=True,
        demo_execution_adapter_implementation_approved=True,
        execution_adapter_implementation_approved=True,
        execution_adapter_approved=True,
        demo_order_placement_approved=True,
        live_order_placement_approved=False,
        execution_approved=True,
    )

    reasons = evaluate_refusal_reasons(authority)

    assert reasons == ["dispatch_disabled_by_fail_closed_skeleton"]


def test_verify_accepts_single_refusal_record(tmp_path: Path) -> None:
    record = build_demo_execution_adapter_skeleton(
        _inputs(tmp_path),
        created_utc="2026-05-11T00:00:00Z",
    )
    output = tmp_path / "skeleton.jsonl"
    write_jsonl_record(output, record)

    records, violations = verify_demo_execution_adapter_skeleton_jsonl(
        output,
        allowed_demo_server="Exness-MT5Trial6",
        require_refusal=True,
    )

    assert len(records) == 1
    assert violations == []


def test_verify_rejects_dispatch_attempt(tmp_path: Path) -> None:
    record = build_demo_execution_adapter_skeleton(
        _inputs(tmp_path),
        created_utc="2026-05-11T00:00:00Z",
    )
    record["transport_result"]["dispatch_attempted"] = True
    output = tmp_path / "skeleton.jsonl"
    write_jsonl_record(output, record)

    _, violations = verify_demo_execution_adapter_skeleton_jsonl(output, require_refusal=True)

    assert any("dispatch_attempted" in violation for violation in violations)


def test_verify_rejects_demo_order_approval(tmp_path: Path) -> None:
    record = build_demo_execution_adapter_skeleton(
        _inputs(tmp_path),
        created_utc="2026-05-11T00:00:00Z",
    )
    record["demo_order_placement_approved"] = True
    output = tmp_path / "skeleton.jsonl"
    write_jsonl_record(output, record)

    _, violations = verify_demo_execution_adapter_skeleton_jsonl(output, require_refusal=True)

    assert any("demo_order_placement_approved" in violation for violation in violations)


def test_verify_rejects_forbidden_execution_like_field(tmp_path: Path) -> None:
    record = build_demo_execution_adapter_skeleton(
        _inputs(tmp_path),
        created_utc="2026-05-11T00:00:00Z",
    )
    record["trade_request"] = {}
    output = tmp_path / "skeleton.jsonl"
    write_jsonl_record(output, record)

    _, violations = verify_demo_execution_adapter_skeleton_jsonl(output, require_refusal=True)

    assert any("forbidden execution-like field" in violation for violation in violations)