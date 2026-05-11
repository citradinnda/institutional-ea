from __future__ import annotations

from copy import deepcopy

from quantcore.execution.h024_execution_safety_controls import (
    CONTROL_DECISION_BLOCK,
    CONTROL_DECISION_PASS_REVIEW_ONLY,
    build_h024_execution_safety_controls_preflight,
)
from quantcore.execution.h024_execution_safety_controls_design import (
    DESIGN_STATUS,
    EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
    EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
)
from quantcore.execution.h024_operator_control_state import (
    OPERATOR_CONTROL_STATE_SNAPSHOT_KIND,
    OPERATOR_CONTROL_STATE_SNAPSHOT_SCHEMA,
    SNAPSHOT_STATUS,
    build_h024_operator_control_state_snapshot,
    verify_h024_operator_control_state_snapshot,
)
from quantcore.execution.h024_order_intent_simulation import REVIEW_ONLY_MODE


ALLOWED_SERVER = "Exness-MT5Trial6"


def _design_record() -> dict:
    return {
        "schema": EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
        "kind": EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "design_status": DESIGN_STATUS,
        "source_phase4_readiness_schema": "h024_phase4_readiness_review_v1",
        "source_phase4_readiness_kind": "PHASE4_READINESS_REVIEW_REQUEST_REVIEW_ONLY",
        "source_phase4_readiness_status": "READY_FOR_PHASE4_REVIEW_REQUEST",
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "scope_boundary": {
            "design_only": True,
            "implementation_present": False,
            "mt5_access_present": False,
            "broker_mutation_present": False,
            "broker_request_construction_present": False,
            "execution_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_adapter_approved": False,
            "adapter_implementation_approved": False,
            "human_review_still_required": True,
        },
        "required_control_sections": [
            "scope_boundary",
            "kill_switch_contract",
            "idempotency_contract",
            "immutable_audit_log_contract",
            "operator_workflow_contract",
            "failure_modes",
            "future_phase4_review_requirements",
        ],
        "source_chain_summary": {
            "strategy": "H024",
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
        "kill_switch_contract": {
            "must_default_to_blocked_until_explicitly_enabled": True,
            "must_support_global_disable": True,
            "must_support_symbol_disable": True,
            "must_support_strategy_disable": True,
            "must_support_max_orders_per_session_guard": True,
            "must_support_max_daily_loss_guard": True,
            "must_fail_closed_on_missing_or_invalid_state": True,
            "must_emit_reason_for_every_block": True,
        },
        "idempotency_contract": {
            "must_define_stable_intent_id": True,
            "intent_id_must_include_strategy_symbol_side_entry_stop_volume_source_timestamp": True,
            "must_reject_duplicate_pending_intent": True,
            "must_reject_duplicate_completed_intent": True,
            "must_fail_closed_on_ambiguous_prior_state": True,
            "must_never_retry_without_recorded_terminal_state": True,
            "stable_intent_id_components": [
                "strategy",
                "server",
                "symbol",
                "normalized_symbol",
                "side",
                "review_only_intent_action",
                "risk_fraction",
                "source_timestamp",
            ],
        },
        "immutable_audit_log_contract": {
            "must_append_only": True,
            "must_record_source_phase4_readiness_reference": True,
            "must_record_operator_decision": True,
            "must_record_preflight_snapshot": True,
            "must_record_idempotency_key": True,
            "must_record_kill_switch_state": True,
            "must_record_all_rejections": True,
            "must_be_readable_without_mt5": True,
        },
        "operator_workflow_contract": {
            "must_require_human_review_before_adapter_implementation": True,
            "must_require_human_review_before_demo_order_placement": True,
            "must_require_human_review_before_live_order_placement": True,
            "must_surface_all_blocking_reasons": True,
            "must_not_auto_promote_from_readiness_to_execution": True,
        },
        "failure_modes": {
            "reject_missing_kill_switch_state": True,
            "reject_invalid_kill_switch_state": True,
            "reject_duplicate_intent_id": True,
            "reject_missing_audit_log_sink": True,
            "reject_non_append_only_audit_log": True,
            "reject_any_execution_like_payload": True,
            "fail_closed_on_unhandled_exception": True,
        },
        "future_phase4_review_requirements": {
            "requires_kill_switch_implementation_before_adapter": True,
            "requires_idempotency_implementation_before_adapter": True,
            "requires_immutable_audit_log_implementation_before_adapter": True,
            "requires_static_source_verification": True,
            "requires_full_test_suite": True,
            "requires_separate_human_approval_for_adapter_implementation": True,
            "requires_separate_human_approval_for_demo_order": True,
            "requires_separate_human_approval_for_live_order": True,
        },
    }


def test_build_operator_control_state_snapshot_passes_without_approval() -> None:
    snapshot = build_h024_operator_control_state_snapshot(
        _design_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert snapshot["schema"] == OPERATOR_CONTROL_STATE_SNAPSHOT_SCHEMA
    assert snapshot["kind"] == OPERATOR_CONTROL_STATE_SNAPSHOT_KIND
    assert snapshot["snapshot_status"] == SNAPSHOT_STATUS
    assert snapshot["verdict"] == "PASS"
    assert snapshot["kill_switch_state"]["global_enabled"] is True
    assert snapshot["kill_switch_state"]["strategy_enabled"]["H024"] is True
    assert snapshot["kill_switch_state"]["symbol_enabled"]["XAUUSD"] is True
    assert snapshot["idempotency_ledger"]["pending_intent_ids"] == []
    assert snapshot["idempotency_ledger"]["completed_intent_ids"] == []
    assert snapshot["phase4_approved"] is False
    assert snapshot["execution_approved"] is False

    assert verify_h024_operator_control_state_snapshot(snapshot, allowed_demo_servers=[ALLOWED_SERVER]) == []


def test_default_missing_kill_switch_still_blocks() -> None:
    snapshot = build_h024_operator_control_state_snapshot(
        _design_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    preflight = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=None,
        idempotency_ledger=snapshot["idempotency_ledger"],
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert preflight["control_decision"] == CONTROL_DECISION_BLOCK
    assert "missing_kill_switch_state" in preflight["blocked_reasons"]
    assert preflight["execution_approved"] is False


def test_explicit_allow_state_makes_preflight_pass_review_only() -> None:
    snapshot = build_h024_operator_control_state_snapshot(
        _design_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    preflight = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=snapshot["kill_switch_state"],
        idempotency_ledger=snapshot["idempotency_ledger"],
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert preflight["control_decision"] == CONTROL_DECISION_PASS_REVIEW_ONLY
    assert preflight["blocked_reasons"] == []
    assert preflight["phase4_approved"] is False
    assert preflight["demo_order_placement_approved"] is False
    assert preflight["live_order_placement_approved"] is False
    assert preflight["execution_approved"] is False


def test_operator_snapshot_rejects_approval_flip() -> None:
    snapshot = build_h024_operator_control_state_snapshot(
        _design_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(snapshot)
    mutated["execution_approved"] = True

    violations = verify_h024_operator_control_state_snapshot(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert "execution_approved_must_be_false" in violations


def test_operator_snapshot_rejects_stale_pending_intent() -> None:
    snapshot = build_h024_operator_control_state_snapshot(
        _design_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(snapshot)
    mutated["idempotency_ledger"]["pending_intent_ids"] = [snapshot["stable_intent_id"]]

    violations = verify_h024_operator_control_state_snapshot(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert "idempotency_ledger:stable_intent_id_already_pending" in violations


def test_operator_snapshot_rejects_kill_switch_disabled() -> None:
    snapshot = build_h024_operator_control_state_snapshot(
        _design_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(snapshot)
    mutated["kill_switch_state"]["global_enabled"] = False

    violations = verify_h024_operator_control_state_snapshot(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert "kill_switch_state:global_enabled_must_be_true" in violations


def test_operator_snapshot_rejects_execution_like_keys() -> None:
    snapshot = build_h024_operator_control_state_snapshot(
        _design_record(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(snapshot)
    mutated["mt5_request"] = {"symbol": "XAUUSDm"}

    violations = verify_h024_operator_control_state_snapshot(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert any(violation.startswith("record_contains_execution_like_fields:") for violation in violations)