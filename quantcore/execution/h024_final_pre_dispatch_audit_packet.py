"""H024 final inert pre-dispatch audit packet for one demo canary.

This artifact is the final pure-Python audit packet before implementing a
one-shot execution-capable demo path. It remains inert and non-dispatchable.
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
from quantcore.execution.h024_demo_order_canary_human_approval import (
    APPROVAL_DECISION as CANARY_HUMAN_APPROVAL_DECISION,
    FALSE_AFTER_CANARY_APPROVAL_FLAGS,
    SCHEMA_VERSION as CANARY_HUMAN_APPROVAL_SCHEMA_VERSION,
)

SCHEMA_VERSION = "h024_final_pre_dispatch_audit_packet_v1"
KIND = "h024_final_pre_dispatch_audit_packet"
AUDIT_DECISION = "COMPLETE_FINAL_INERT_PRE_DISPATCH_AUDIT_FOR_ONE_DEMO_CANARY_NO_DISPATCH"


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
    if markers & {
        "PASS",
        "APPROVED",
        "APPROVED_SINGLE_CANARY_REVIEW_ONLY",
        "READY_FOR_HUMAN_DEMO_ORDER_CANARY_APPROVAL_REVIEW",
    }:
        return True
    if record.get("passed") is True or record.get("approved") is True:
        return True
    return False


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


def _summary(record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        "schema_version": record.get("schema_version"),
        "kind": record.get("kind"),
        "status": record.get("status"),
        "verdict": record.get("verdict"),
        "decision": record.get("decision"),
        "approved": record.get("approved"),
        "allowed_demo_server": record.get("allowed_demo_server"),
        "expected_runtime_symbol": record.get("expected_runtime_symbol"),
    }
    return {key: value for key, value in summary.items() if value not in (None, "")}


def _preflight_control_violations(
    preflight: Mapping[str, Any],
    *,
    allowed_demo_server: str,
    expected_runtime_symbol: str,
    max_lot_cap: float,
) -> list[str]:
    violations: list[str] = []
    if preflight.get("schema_version") != HARD_CONTROLS_PREFLIGHT_SCHEMA_VERSION:
        violations.append("unexpected_hard_controls_preflight_schema")
    if preflight.get("decision") != HARD_CONTROLS_PREFLIGHT_REQUEST_DECISION:
        violations.append("hard_controls_preflight_decision_mismatch")
    if not _record_is_pass(preflight):
        violations.append("hard_controls_preflight_not_passed")
    if preflight.get("allowed_demo_server") != allowed_demo_server:
        violations.append("preflight_allowed_demo_server_mismatch")
    if preflight.get("expected_runtime_symbol") != expected_runtime_symbol:
        violations.append("preflight_expected_runtime_symbol_mismatch")

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

    max_lot = controls.get("max_lot_cap")
    if not isinstance(max_lot, Mapping):
        violations.append("max_lot_cap_missing_or_not_mapping")
    else:
        cap_value = _to_float(max_lot.get("value"))
        upstream_value = _to_float(max_lot.get("upstream_verified_final_lots"))
        if cap_value != float(max_lot_cap):
            violations.append("max_lot_cap_mismatch")
        if cap_value is None or cap_value <= 0:
            violations.append("max_lot_cap_not_positive")
        if upstream_value is not None and cap_value is not None and cap_value > upstream_value:
            violations.append("max_lot_cap_exceeds_upstream_verified_final_lots")
        if max_lot.get("must_not_exceed_upstream_h020_final_lots") is not True:
            violations.append("max_lot_cap_h020_bound_missing")

    return violations


def _approval_violations(
    approval: Mapping[str, Any],
    *,
    allowed_demo_server: str,
    expected_runtime_symbol: str,
) -> list[str]:
    violations: list[str] = []
    if approval.get("schema_version") != CANARY_HUMAN_APPROVAL_SCHEMA_VERSION:
        violations.append("unexpected_canary_human_approval_schema")
    if approval.get("decision") != CANARY_HUMAN_APPROVAL_DECISION:
        violations.append("canary_human_approval_decision_mismatch")
    if approval.get("approved") is not True or not _record_is_pass(approval):
        violations.append("canary_human_approval_not_passed")
    if approval.get("allowed_demo_server") != allowed_demo_server:
        violations.append("approval_allowed_demo_server_mismatch")
    if approval.get("expected_runtime_symbol") != expected_runtime_symbol:
        violations.append("approval_expected_runtime_symbol_mismatch")

    authority = approval.get("authority")
    if not isinstance(authority, Mapping):
        violations.append("canary_human_approval_authority_missing")
    else:
        if authority.get("demo_order_canary_approved") is not True:
            violations.append("demo_order_canary_not_approved_by_human_approval")
        if authority.get("final_pre_dispatch_audit_packet_construction_allowed") is not True:
            violations.append("final_pre_dispatch_audit_packet_construction_not_allowed")

    return violations


def build_final_pre_dispatch_audit_packet(
    *,
    canary_human_approval: Mapping[str, Any],
    hard_controls_preflight_packet: Mapping[str, Any],
    allowed_demo_server: str,
    expected_runtime_symbol: str,
    max_lot_cap: float,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    approval = _as_mapping(canary_human_approval, name="canary_human_approval")
    preflight = _as_mapping(hard_controls_preflight_packet, name="hard_controls_preflight_packet")

    violations = []
    violations.extend(
        _approval_violations(
            approval,
            allowed_demo_server=allowed_demo_server,
            expected_runtime_symbol=expected_runtime_symbol,
        )
    )
    violations.extend(
        _preflight_control_violations(
            preflight,
            allowed_demo_server=allowed_demo_server,
            expected_runtime_symbol=expected_runtime_symbol,
            max_lot_cap=max_lot_cap,
        )
    )

    passed = not violations
    authority = {
        "final_pre_dispatch_audit_passed": passed,
        "demo_order_canary_approved": approval.get("approved") is True and passed,
        "one_shot_execution_capable_demo_path_implementation_allowed": passed,
        "max_approved_canary_orders": 1 if passed else 0,
        "approved_demo_server": allowed_demo_server if passed else None,
        "approved_runtime_symbol": expected_runtime_symbol if passed else None,
        "approved_max_lot_cap": float(max_lot_cap) if passed else None,
        "actual_broker_request_construction_approved": False,
        "actual_broker_request_constructed": False,
        "actual_mt5_request_construction_approved": False,
        "actual_mt5_request_constructed": False,
        "order_payload_construction_approved": False,
        "order_payload_constructed": False,
        "transport_dispatch_approved": False,
        "transport_dispatch_attempted": False,
        "terminal_mutation_approved": False,
        "terminal_mutated": False,
        "broker_mutation_approved": False,
        "broker_state_mutated": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "kind": KIND,
        "generated_at_utc": generated_at_utc or _utc_now_iso(),
        "decision": AUDIT_DECISION if passed else "REFUSE_FINAL_PRE_DISPATCH_AUDIT",
        "status": "FINAL_INERT_PRE_DISPATCH_AUDIT_PASS" if passed else "BLOCKED",
        "verdict": "PASS" if passed else "FAIL",
        "approved": False,
        "pre_dispatch_audit_passed": passed,
        "allowed_demo_server": allowed_demo_server,
        "expected_runtime_symbol": expected_runtime_symbol,
        "max_lot_cap": float(max_lot_cap),
        "input_artifacts": {
            "canary_human_approval": _summary(approval),
            "hard_controls_preflight_packet": _summary(preflight),
        },
        "verified_controls": {
            "allowed_demo_server_lock": allowed_demo_server,
            "account_currency_lock": "USD",
            "account_context_lock": "standard_demo_only",
            "runtime_symbol_lock": expected_runtime_symbol,
            "kill_switch_allow_state_required": True,
            "idempotency_ledger_required": True,
            "single_canary_order_limit": 1,
            "max_lot_cap": float(max_lot_cap),
            "pre_dispatch_final_audit_required": True,
            "post_order_audit_required_if_later_approved": True,
            "live_order_forbidden": True,
        },
        "authority": authority,
        "preserved_false_authority": {flag: False for flag in FALSE_AFTER_CANARY_APPROVAL_FLAGS},
        "safety_boundary": {
            "pure_python_only": True,
            "audit_artifact_only": True,
            "non_dispatchable": True,
            "no_terminal_or_broker_mutation": True,
            "no_demo_or_live_order_placement": True,
            "does_not_construct_actual_broker_request": True,
            "does_not_construct_actual_mt5_request": True,
            "does_not_construct_order_payload": True,
        },
        "next_allowed_engineering_step": (
            "implement_one_shot_execution_capable_demo_path_under_verified_locks_with_no_automatic_invocation"
            if passed
            else None
        ),
        "violations": violations,
    }


def validate_final_pre_dispatch_audit_packet(
    record: Mapping[str, Any],
    *,
    allowed_demo_server: str,
    expected_runtime_symbol: str,
    max_lot_cap: float,
    require_pass: bool = False,
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
    if _to_float(candidate.get("max_lot_cap")) != float(max_lot_cap):
        violations.append("max_lot_cap_mismatch")

    embedded = candidate.get("violations")
    if isinstance(embedded, list) and embedded:
        violations.extend(f"embedded:{item}" for item in embedded)
    elif embedded not in (None, []):
        violations.append("embedded_violations_not_a_list")

    if require_pass and candidate.get("verdict") != "PASS":
        violations.append("verdict_not_pass")
    if require_pass and candidate.get("decision") != AUDIT_DECISION:
        violations.append("unexpected_decision")
    if require_pass and candidate.get("pre_dispatch_audit_passed") is not True:
        violations.append("pre_dispatch_audit_not_passed")
    if candidate.get("approved") is not False:
        violations.append("packet_must_not_itself_approve_order_placement")

    controls = candidate.get("verified_controls")
    if not isinstance(controls, Mapping):
        violations.append("verified_controls_missing_or_not_mapping")
        controls = {}
    expected_controls: dict[str, Any] = {
        "allowed_demo_server_lock": allowed_demo_server,
        "account_currency_lock": "USD",
        "account_context_lock": "standard_demo_only",
        "runtime_symbol_lock": expected_runtime_symbol,
        "kill_switch_allow_state_required": True,
        "idempotency_ledger_required": True,
        "single_canary_order_limit": 1,
        "max_lot_cap": float(max_lot_cap),
        "pre_dispatch_final_audit_required": True,
        "post_order_audit_required_if_later_approved": True,
        "live_order_forbidden": True,
    }
    for key, expected in expected_controls.items():
        if controls.get(key) != expected:
            violations.append(f"{key}_mismatch")

    authority = candidate.get("authority")
    if not isinstance(authority, Mapping):
        violations.append("authority_missing_or_not_mapping")
        authority = {}
    if require_pass and authority.get("final_pre_dispatch_audit_passed") is not True:
        violations.append("authority_final_pre_dispatch_audit_not_passed")
    if require_pass and authority.get("one_shot_execution_capable_demo_path_implementation_allowed") is not True:
        violations.append("one_shot_execution_capable_demo_path_implementation_not_allowed")
    if authority.get("demo_order_placement_approved") is not False:
        violations.append("demo_order_placement_approved_not_false")
    if authority.get("execution_approved") is not False:
        violations.append("execution_approved_not_false")

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
        "audit_artifact_only",
        "non_dispatchable",
        "no_terminal_or_broker_mutation",
        "no_demo_or_live_order_placement",
        "does_not_construct_actual_broker_request",
        "does_not_construct_actual_mt5_request",
        "does_not_construct_order_payload",
    ):
        if boundary.get(key) is not True:
            violations.append(f"{key}_not_true")

    if candidate.get("verified_controls") is not None:
        copied = deepcopy(candidate["verified_controls"])
        if copied != candidate["verified_controls"]:
            violations.append("verified_controls_not_copyable")

    return violations


__all__ = [
    "AUDIT_DECISION",
    "KIND",
    "SCHEMA_VERSION",
    "build_final_pre_dispatch_audit_packet",
    "validate_final_pre_dispatch_audit_packet",
]