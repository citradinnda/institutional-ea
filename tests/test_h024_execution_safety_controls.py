from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from quantcore.execution.h024_execution_safety_controls import (
    CONTROL_DECISION_BLOCK,
    CONTROL_DECISION_PASS_REVIEW_ONLY,
    CONTROL_STATUS_BLOCKED,
    CONTROL_STATUS_PASS,
    IDEMPOTENCY_LEDGER_SCHEMA,
    KILL_SWITCH_STATE_SCHEMA,
    append_h024_execution_safety_audit_event,
    build_h024_execution_safety_controls_preflight,
    verify_h024_execution_safety_audit_event,
    verify_h024_execution_safety_controls_preflight_record,
)
from quantcore.execution.h024_execution_safety_controls_design import (
    DESIGN_STATUS,
    EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
    EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
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


def _enabled_kill_switch_state() -> dict:
    return {
        "schema": KILL_SWITCH_STATE_SCHEMA,
        "global_enabled": True,
        "strategy_enabled": {"H024": True},
        "symbol_enabled": {"XAUUSD": True},
        "max_orders_per_session": 1,
        "orders_this_session": 0,
        "daily_loss_limit_usd": 1000.0,
        "realized_loss_today_usd": 0.0,
    }


def _empty_ledger() -> dict:
    return {
        "schema": IDEMPOTENCY_LEDGER_SCHEMA,
        "pending_intent_ids": [],
        "completed_intent_ids": [],
    }


def test_missing_kill_switch_state_blocks_by_default_but_keeps_record_valid() -> None:
    record = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=None,
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["verdict"] == "PASS"
    assert record["control_status"] == CONTROL_STATUS_BLOCKED
    assert record["control_decision"] == CONTROL_DECISION_BLOCK
    assert "missing_kill_switch_state" in record["blocked_reasons"]
    assert record["execution_approved"] is False
    assert verify_h024_execution_safety_controls_preflight_record(record, allowed_demo_servers=[ALLOWED_SERVER]) == []


def test_enabled_controls_pass_review_only_without_execution_approval() -> None:
    record = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=_enabled_kill_switch_state(),
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["control_status"] == CONTROL_STATUS_PASS
    assert record["control_decision"] == CONTROL_DECISION_PASS_REVIEW_ONLY
    assert record["blocked_reasons"] == []
    assert record["phase4_approved"] is False
    assert record["execution_approved"] is False
    assert verify_h024_execution_safety_controls_preflight_record(record, allowed_demo_servers=[ALLOWED_SERVER]) == []


def test_duplicate_pending_intent_blocks() -> None:
    first = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=_enabled_kill_switch_state(),
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    ledger = _empty_ledger()
    ledger["pending_intent_ids"] = [first["stable_intent_id"]]

    second = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=_enabled_kill_switch_state(),
        idempotency_ledger=ledger,
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert second["control_decision"] == CONTROL_DECISION_BLOCK
    assert "duplicate_pending_intent_id" in second["blocked_reasons"]


def test_daily_loss_limit_blocks() -> None:
    state = _enabled_kill_switch_state()
    state["realized_loss_today_usd"] = 1000.0

    record = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=state,
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["control_decision"] == CONTROL_DECISION_BLOCK
    assert "daily_loss_limit_reached" in record["blocked_reasons"]


def test_verify_rejects_execution_approval_flip() -> None:
    record = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=None,
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(record)
    mutated["execution_approved"] = True

    violations = verify_h024_execution_safety_controls_preflight_record(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert "execution_approved_must_be_false" in violations


def test_verify_rejects_execution_like_keys() -> None:
    record = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=None,
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(record)
    mutated["order_send_result"] = {"retcode": 0}

    violations = verify_h024_execution_safety_controls_preflight_record(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert any(violation.startswith("record_contains_execution_like_fields:") for violation in violations)


def test_audit_event_hash_is_verified() -> None:
    record = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=None,
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert verify_h024_execution_safety_audit_event(
        record["immutable_audit_log_event"],
        expected_stable_intent_id=record["stable_intent_id"],
    ) == []

    mutated = deepcopy(record["immutable_audit_log_event"])
    mutated["control_decision"] = CONTROL_DECISION_PASS_REVIEW_ONLY

    violations = verify_h024_execution_safety_audit_event(
        mutated,
        expected_stable_intent_id=record["stable_intent_id"],
    )

    assert "event_hash_mismatch" in violations


def test_append_audit_event_appends_jsonl(tmp_path: Path) -> None:
    record = build_h024_execution_safety_controls_preflight(
        _design_record(),
        kill_switch_state=None,
        idempotency_ledger=_empty_ledger(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    path = tmp_path / "audit.jsonl"

    append_h024_execution_safety_audit_event(path, record["immutable_audit_log_event"])
    append_h024_execution_safety_audit_event(path, record["immutable_audit_log_event"])

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["event_hash"] == record["immutable_audit_log_event"]["event_hash"]
    assert json.loads(lines[1])["event_hash"] == record["immutable_audit_log_event"]["event_hash"]