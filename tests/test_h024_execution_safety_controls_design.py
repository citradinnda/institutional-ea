from __future__ import annotations

from copy import deepcopy

from quantcore.execution.h024_execution_safety_controls_design import (
    DESIGN_STATUS,
    EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
    EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
    build_h024_execution_safety_controls_design,
    verify_h024_execution_safety_controls_design_record,
)
from quantcore.execution.h024_order_intent_simulation import REVIEW_ONLY_MODE
from quantcore.execution.h024_phase4_readiness_review import (
    PHASE4_READINESS_REVIEW_KIND,
    PHASE4_READINESS_REVIEW_SCHEMA,
    READY_STATUS,
    REQUIRED_ARTIFACT_KEYS,
)


ALLOWED_SERVER = "Exness-MT5Trial6"


def _phase4_review_record() -> dict:
    return {
        "schema": PHASE4_READINESS_REVIEW_SCHEMA,
        "kind": PHASE4_READINESS_REVIEW_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "review_request_status": READY_STATUS,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "source_manual_checkpoint_schema": "h024_manual_approval_checkpoint_v1",
        "source_manual_checkpoint_kind": "MANUAL_APPROVAL_CHECKPOINT_REVIEW_ONLY",
        "source_manual_approval_status": "PENDING_MANUAL_APPROVAL",
        "source_manual_approval_granted": False,
        "source_demo_execution_adapter_design_schema": "h024_demo_execution_adapter_design_v1",
        "source_demo_execution_adapter_design_kind": "DEMO_EXECUTION_ADAPTER_DESIGN_REVIEW_ONLY",
        "source_demo_execution_adapter_design_status": "DESIGN_SPEC_ONLY_NOT_IMPLEMENTED",
        "artifact_counts": {key: 1 for key in REQUIRED_ARTIFACT_KEYS},
        "artifact_verifications": {
            key: {
                "verdict": "PASS",
                "record_count": 1,
                "verifier": f"verify_{key}.py",
                "return_code": 0,
            }
            for key in REQUIRED_ARTIFACT_KEYS
        },
        "readiness_checks": {
            "all_independent_artifact_verifiers_passed": True,
            "exactly_one_record_per_required_artifact": True,
            "manual_checkpoint_pending_not_granted": True,
            "demo_adapter_design_spec_only_not_implemented": True,
            "phase4_not_approved": True,
            "demo_order_placement_not_approved": True,
            "live_order_placement_not_approved": True,
            "execution_adapter_not_approved": True,
            "execution_not_approved": True,
            "human_review_still_required": True,
            "no_execution_like_fields_detected": True,
        },
        "source_chain_summary": {
            "server": ALLOWED_SERVER,
            "account_currency": "USD",
            "symbol": "XAUUSDm",
            "normalized_symbol": "XAUUSD",
            "side": "short",
            "review_only_intent_action": "SELL_MARKET_REVIEW_ONLY",
            "risk_fraction": 0.01,
            "risk_usd": 100.0,
            "estimated_loss_usd": 89.027,
            "source_timestamp": "2026.05.11 07:45:49",
            "source_reason": "h024_fixture_would_open",
        },
        "approval_boundary": {
            "this_artifact_is_not_phase4_approval": True,
            "this_artifact_is_not_demo_order_approval": True,
            "this_artifact_is_not_live_order_approval": True,
            "this_artifact_is_not_execution_adapter_approval": True,
            "this_artifact_is_not_adapter_implementation_approval": True,
            "this_artifact_is_not_execution_approval": True,
            "future_human_phase4_review_required": True,
            "future_separate_adapter_implementation_approval_required": True,
            "future_separate_demo_order_placement_approval_required": True,
            "future_separate_live_order_placement_approval_required": True,
        },
    }


def test_build_execution_safety_controls_design_passes_without_approval() -> None:
    record = build_h024_execution_safety_controls_design(
        _phase4_review_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["schema"] == EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA
    assert record["kind"] == EXECUTION_SAFETY_CONTROLS_DESIGN_KIND
    assert record["verdict"] == "PASS"
    assert record["design_status"] == DESIGN_STATUS
    assert record["phase4_approved"] is False
    assert record["demo_order_placement_approved"] is False
    assert record["live_order_placement_approved"] is False
    assert record["execution_adapter_approved"] is False
    assert record["adapter_implementation_approved"] is False
    assert record["execution_approved"] is False
    assert record["human_review_still_required"] is True
    assert record["kill_switch_contract"]["must_fail_closed_on_missing_or_invalid_state"] is True
    assert record["idempotency_contract"]["must_define_stable_intent_id"] is True
    assert record["immutable_audit_log_contract"]["must_append_only"] is True

    assert verify_h024_execution_safety_controls_design_record(record, allowed_demo_servers=[ALLOWED_SERVER]) == []


def test_build_execution_safety_controls_design_rejects_phase4_approval_flip() -> None:
    source = _phase4_review_record()
    source["phase4_approved"] = True

    record = build_h024_execution_safety_controls_design(source, allowed_demo_servers=[ALLOWED_SERVER])

    assert record["verdict"] == "FAIL"
    assert any("phase4_approved_must_be_false" in violation for violation in record["violations"])
    assert record["execution_approved"] is False


def test_build_execution_safety_controls_design_rejects_not_ready_source() -> None:
    source = _phase4_review_record()
    source["review_request_status"] = "NOT_READY_FOR_PHASE4_REVIEW_REQUEST"

    record = build_h024_execution_safety_controls_design(source, allowed_demo_servers=[ALLOWED_SERVER])

    assert record["verdict"] == "FAIL"
    assert any("source_phase4_review_not_ready" in violation for violation in record["violations"])


def test_verify_execution_safety_controls_design_rejects_missing_kill_switch_flag() -> None:
    record = build_h024_execution_safety_controls_design(
        _phase4_review_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(record)
    mutated["kill_switch_contract"]["must_support_global_disable"] = False

    violations = verify_h024_execution_safety_controls_design_record(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert "kill_switch_contract_flag_mismatch:must_support_global_disable" in violations


def test_verify_execution_safety_controls_design_rejects_missing_idempotency_component() -> None:
    record = build_h024_execution_safety_controls_design(
        _phase4_review_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(record)
    mutated["idempotency_contract"]["stable_intent_id_components"].remove("source_timestamp")

    violations = verify_h024_execution_safety_controls_design_record(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert any(violation.startswith("stable_intent_id_components_missing:") for violation in violations)


def test_verify_execution_safety_controls_design_rejects_execution_like_keys() -> None:
    record = build_h024_execution_safety_controls_design(
        _phase4_review_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(record)
    mutated["broker_request"] = {"symbol": "XAUUSDm"}

    violations = verify_h024_execution_safety_controls_design_record(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert any(violation.startswith("record_contains_execution_like_fields:") for violation in violations)