"""H024 single-demo-order canary human approval artifact.

This artifact approves exactly one later demo-order canary under the already
constructed hard controls. It is still pure Python and non-dispatchable: it does
not construct a broker request, construct an MT5 request, construct an order
payload, dispatch transport, or mutate terminal/broker state.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from quantcore.execution.h024_demo_order_canary_hard_controls_preflight_packet import (
    REQUEST_DECISION as HARD_CONTROLS_PREFLIGHT_REQUEST_DECISION,
    SCHEMA_VERSION as HARD_CONTROLS_PREFLIGHT_SCHEMA_VERSION,
)

SCHEMA_VERSION = "h024_demo_order_canary_human_approval_v1"
KIND = "h024_demo_order_canary_human_approval"
APPROVAL_DECISION = "APPROVE_SINGLE_DEMO_ORDER_CANARY_UNDER_HARD_CONTROLS_NO_DISPATCH"
REFUSAL_DECISION = "REFUSE_SINGLE_DEMO_ORDER_CANARY_APPROVAL"

FALSE_AFTER_CANARY_APPROVAL_FLAGS: tuple[str, ...] = (
    "actual_broker_request_construction_approved",
    "actual_broker_request_constructed",
    "actual_mt5_request_construction_approved",
    "actual_mt5_request_constructed",
    "order_payload_construction_approved",
    "order_payload_constructed",
    "execution_capable_adapter_use_approved",
    "execution_adapter_approved_as_transport",
    "transport_dispatch_attempted",
    "terminal_mutation_approved",
    "terminal_mutated",
    "broker_mutation_approved",
    "broker_state_mutated",
    "demo_order_placement_approved",
    "live_order_placement_approved",
    "execution_approved",
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _as_mapping(value: Mapping[str, Any] | dict[str, Any], *, name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return dict(value)


def _upper_text(value: Any) -> str:
    return str(value or "").strip().upper()


def _violations_from(record: Mapping[str, Any]) -> list[Any]:
    violations = record.get("violations")
    if violations is None:
        return []
    if isinstance(violations, list):
        return violations
    return [violations]


def _record_is_pass(record: Mapping[str, Any]) -> bool:
    if _violations_from(record):
        return False
    markers = {
        _upper_text(record.get("verdict")),
        _upper_text(record.get("status")),
        _upper_text(record.get("decision_status")),
    }
    if markers & {"PASS", "APPROVED", "APPROVED_REVIEW_ONLY", "READY_FOR_HUMAN_DEMO_ORDER_CANARY_APPROVAL_REVIEW"}:
        return True
    if record.get("passed") is True or record.get("approved") is True:
        return True
    return record.get("authority", {}).get("hard_controls_preflight_packet_constructed") is True


def _control_value(controls: Mapping[str, Any], key: str) -> Any:
    value = controls.get(key)
    if isinstance(value, Mapping):
        if "value" in value:
            return value.get("value")
        if "required" in value:
            return value.get("required")
    return value


def _to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _summarize_preflight(record: Mapping[str, Any]) -> dict[str, Any]:
    controls = record.get("required_hard_controls")
    if not isinstance(controls, Mapping):
        controls = {}
    summary = {
        "schema_version": record.get("schema_version"),
        "kind": record.get("kind"),
        "status": record.get("status"),
        "verdict": record.get("verdict"),
        "decision": record.get("decision"),
        "allowed_demo_server": record.get("allowed_demo_server"),
        "expected_runtime_symbol": record.get("expected_runtime_symbol"),
        "runtime_symbol_lock": _control_value(controls, "runtime_symbol_lock"),
        "account_currency_lock": _control_value(controls, "account_currency_lock"),
        "account_context_lock": _control_value(controls, "account_context_lock"),
        "single_canary_order_limit": _control_value(controls, "single_canary_order_limit"),
        "max_lot_cap": controls.get("max_lot_cap"),
    }
    return {key: value for key, value in summary.items() if value not in (None, "")}


def _validate_preflight_controls(
    preflight: Mapping[str, Any],
    *,
    allowed_demo_server: str,
    expected_runtime_symbol: str,
) -> list[str]:
    violations: list[str] = []
    if preflight.get("schema_version") != HARD_CONTROLS_PREFLIGHT_SCHEMA_VERSION:
        violations.append("unexpected_hard_controls_preflight_schema")
    if preflight.get("decision") != HARD_CONTROLS_PREFLIGHT_REQUEST_DECISION:
        violations.append("hard_controls_preflight_decision_not_request_human_canary_approval")
    if not _record_is_pass(preflight):
        violations.append("hard_controls_preflight_not_passed")
    if preflight.get("allowed_demo_server") != allowed_demo_server:
        violations.append("allowed_demo_server_mismatch")
    if preflight.get("expected_runtime_symbol") != expected_runtime_symbol:
        violations.append("expected_runtime_symbol_mismatch")

    controls = preflight.get("required_hard_controls")
    if not isinstance(controls, Mapping):
        return violations + ["required_hard_controls_missing_or_not_mapping"]

    expected_controls: dict[str, Any] = {
        "allowed_demo_server_lock": allowed_demo_server,
        "account_currency_lock": "USD",
        "account_context_lock": "standard_demo_only",
        "runtime_symbol_lock": expected_runtime_symbol,
        "kill_switch_allow_state_required": True,
        "idempotency_ledger_required": True,
        "post_order_audit_required_if_later_approved": True,
        "pre_dispatch_final_audit_required_if_later_approved": True,
        "human_demo_order_canary_approval_required_before_any_order_path": True,
        "live_order_forbidden": True,
    }
    for key, expected in expected_controls.items():
        if _control_value(controls, key) != expected:
            violations.append(f"{key}_mismatch")

    single_limit = controls.get("single_canary_order_limit")
    if not isinstance(single_limit, Mapping) or single_limit.get("value") != 1:
        violations.append("single_canary_order_limit_not_one")

    max_lot_cap = controls.get("max_lot_cap")
    if not isinstance(max_lot_cap, Mapping):
        violations.append("max_lot_cap_missing_or_not_mapping")
    else:
        cap_value = _to_float(max_lot_cap.get("value"))
        upstream_value = _to_float(max_lot_cap.get("upstream_verified_final_lots"))
        if cap_value is None or cap_value <= 0:
            violations.append("max_lot_cap_not_positive")
        if upstream_value is not None and cap_value is not None and cap_value > upstream_value:
            violations.append("max_lot_cap_exceeds_upstream_verified_final_lots")
        if max_lot_cap.get("must_not_exceed_upstream_h020_final_lots") is not True:
            violations.append("max_lot_cap_h020_bound_missing")

    return violations


def build_demo_order_canary_human_approval(
    *,
    hard_controls_preflight_packet: Mapping[str, Any],
    allowed_demo_server: str,
    expected_runtime_symbol: str,
    reviewer: str = "human",
    approval_reference: str = "manual_human_approval",
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    preflight = _as_mapping(hard_controls_preflight_packet, name="hard_controls_preflight_packet")
    violations = _validate_preflight_controls(
        preflight,
        allowed_demo_server=allowed_demo_server,
        expected_runtime_symbol=expected_runtime_symbol,
    )
    approved = not violations

    controls = preflight.get("required_hard_controls")
    if not isinstance(controls, Mapping):
        controls = {}

    authority = {
        "demo_order_canary_approved": approved,
        "single_demo_order_canary_approved_under_hard_controls": approved,
        "final_pre_dispatch_audit_packet_construction_allowed": approved,
        "max_approved_canary_orders": 1 if approved else 0,
        "approved_demo_server": allowed_demo_server if approved else None,
        "approved_runtime_symbol": expected_runtime_symbol if approved else None,
        "review_only_approval_artifact": True,
        "actual_broker_request_construction_approved": False,
        "actual_mt5_request_construction_approved": False,
        "order_payload_construction_approved": False,
        "transport_dispatch_approved": False,
        "terminal_or_broker_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "kind": KIND,
        "generated_at_utc": generated_at_utc or _utc_now_iso(),
        "reviewer": reviewer,
        "approval_reference": approval_reference,
        "decision": APPROVAL_DECISION if approved else REFUSAL_DECISION,
        "status": "APPROVED_SINGLE_CANARY_REVIEW_ONLY" if approved else "BLOCKED",
        "verdict": "PASS" if approved else "FAIL",
        "approved": approved,
        "allowed_demo_server": allowed_demo_server,
        "expected_runtime_symbol": expected_runtime_symbol,
        "input_artifacts": {
            "hard_controls_preflight_packet": _summarize_preflight(preflight),
        },
        "approved_hard_controls": {
            "allowed_demo_server_lock": allowed_demo_server,
            "account_currency_lock": "USD",
            "account_context_lock": "standard_demo_only",
            "runtime_symbol_lock": expected_runtime_symbol,
            "single_canary_order_limit": 1,
            "max_lot_cap": controls.get("max_lot_cap"),
            "kill_switch_allow_state_required": True,
            "idempotency_ledger_required": True,
            "pre_dispatch_final_audit_required": True,
            "post_order_audit_required_if_later_approved": True,
            "live_order_forbidden": True,
        },
        "authority": authority,
        "preserved_false_authority": {flag: False for flag in FALSE_AFTER_CANARY_APPROVAL_FLAGS},
        "safety_boundary": {
            "pure_python_only": True,
            "approval_artifact_only": True,
            "non_dispatchable": True,
            "no_terminal_or_broker_mutation": True,
            "no_demo_or_live_order_placement": True,
            "does_not_construct_actual_broker_request": True,
            "does_not_construct_actual_mt5_request": True,
            "does_not_construct_order_payload": True,
        },
        "next_allowed_artifact": "h024_final_pre_dispatch_audit_packet_v1" if approved else None,
        "violations": violations,
    }


def validate_demo_order_canary_human_approval(
    record: Mapping[str, Any],
    *,
    allowed_demo_server: str,
    expected_runtime_symbol: str,
    require_approved: bool = False,
) -> list[str]:
    candidate = _as_mapping(record, name="record")
    violations: list[str] = []

    if candidate.get("schema_version") != SCHEMA_VERSION:
        violations.append("unexpected_schema_version")
    if candidate.get("kind") != KIND:
        violations.append("unexpected_kind")
    if candidate.get("allowed_demo_server") != allowed_demo_server:
        violations.append("allowed_demo_server_mismatch")
    if candidate.get("expected_runtime_symbol") != expected_runtime_symbol:
        violations.append("expected_runtime_symbol_mismatch")

    embedded = candidate.get("violations")
    if isinstance(embedded, list) and embedded:
        violations.extend(f"embedded:{item}" for item in embedded)
    elif embedded not in (None, []):
        violations.append("embedded_violations_not_a_list")

    if require_approved and candidate.get("approved") is not True:
        violations.append("canary_human_approval_not_approved")
    if require_approved and candidate.get("decision") != APPROVAL_DECISION:
        violations.append("unexpected_decision")
    if require_approved and candidate.get("verdict") != "PASS":
        violations.append("verdict_not_pass")

    authority = candidate.get("authority")
    if not isinstance(authority, Mapping):
        violations.append("authority_missing_or_not_mapping")
        authority = {}
    if require_approved and authority.get("demo_order_canary_approved") is not True:
        violations.append("demo_order_canary_not_approved")
    if require_approved and authority.get("final_pre_dispatch_audit_packet_construction_allowed") is not True:
        violations.append("final_pre_dispatch_audit_packet_construction_not_allowed")
    if authority.get("max_approved_canary_orders") not in (1, 0):
        violations.append("max_approved_canary_orders_invalid")

    false_authority = candidate.get("preserved_false_authority")
    if not isinstance(false_authority, Mapping):
        violations.append("preserved_false_authority_missing_or_not_mapping")
        false_authority = {}
    for flag in FALSE_AFTER_CANARY_APPROVAL_FLAGS:
        if false_authority.get(flag) is not False:
            violations.append(f"{flag}_not_false")

    boundary = candidate.get("safety_boundary")
    if not isinstance(boundary, Mapping):
        violations.append("safety_boundary_missing_or_not_mapping")
        boundary = {}
    for key in (
        "pure_python_only",
        "approval_artifact_only",
        "non_dispatchable",
        "no_terminal_or_broker_mutation",
        "no_demo_or_live_order_placement",
        "does_not_construct_actual_broker_request",
        "does_not_construct_actual_mt5_request",
        "does_not_construct_order_payload",
    ):
        if boundary.get(key) is not True:
            violations.append(f"{key}_not_true")

    if candidate.get("approved_hard_controls") is not None:
        copied = deepcopy(candidate["approved_hard_controls"])
        if copied != candidate["approved_hard_controls"]:
            violations.append("approved_hard_controls_not_copyable")

    return violations


__all__ = [
    "APPROVAL_DECISION",
    "FALSE_AFTER_CANARY_APPROVAL_FLAGS",
    "KIND",
    "SCHEMA_VERSION",
    "build_demo_order_canary_human_approval",
    "validate_demo_order_canary_human_approval",
]