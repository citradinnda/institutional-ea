"""Review-only H024 demo-order canary hard-controls preflight packet.

The packet records the controls that would be required before any later human
canary approval. It is inert: it does not create an order payload, construct a
terminal request, dispatch transport, or mutate terminal/broker state.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from quantcore.execution.h024_demo_order_canary_readiness_human_decision import (
    APPROVAL_DECISION as CANARY_READINESS_APPROVAL_DECISION,
    FALSE_AUTHORITY_FLAGS,
    SCHEMA_VERSION as CANARY_READINESS_DECISION_SCHEMA_VERSION,
)

SCHEMA_VERSION = "h024_demo_order_canary_hard_controls_preflight_packet_v1"
KIND = "h024_demo_order_canary_hard_controls_preflight_packet"
REQUEST_DECISION = "REQUEST_HUMAN_DEMO_ORDER_CANARY_APPROVAL_WITH_HARD_CONTROLS_NO_ORDER_PLACEMENT"


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
    if markers & {"PASS", "APPROVED", "APPROVED_REVIEW_ONLY", "READY_FOR_REVIEW"}:
        return True
    if record.get("passed") is True or record.get("approved") is True:
        return True
    return record.get("demo_order_readiness_packet_constructed") is True


def _find_first_by_key(value: Any, keys: set[str]) -> Any | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() in keys and item not in (None, ""):
                return item
        for item in value.values():
            found = _find_first_by_key(item, keys)
            if found not in (None, ""):
                return found
    elif isinstance(value, list):
        for item in value:
            found = _find_first_by_key(item, keys)
            if found not in (None, ""):
                return found
    return None


def _find_first_by_key_in_order(value: Any, keys: tuple[str, ...]) -> Any | None:
    for key in keys:
        found = _find_first_by_key(value, {key})
        if found not in (None, ""):
            return found
    return None


def _to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _summarize_record(record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        "schema_version": record.get("schema_version") or record.get("schema"),
        "kind": record.get("kind"),
        "status": record.get("status"),
        "verdict": record.get("verdict"),
        "decision": record.get("decision"),
        "approved": record.get("approved"),
        "runtime_symbol": _find_first_by_key_in_order(record, ("runtime_symbol", "observed_runtime_symbol", "broker_symbol", "symbol")),
        "server": _find_first_by_key(record, {"server", "demo_server", "allowed_demo_server", "account_server", "broker_server"}),
        "account_currency": _find_first_by_key(record, {"currency", "account_currency", "account_currency_lock"}),
        "idempotency_key": _find_first_by_key(record, {"idempotency_key", "preview_idempotency_key", "draft_idempotency_key"}),
    }
    return {key: value for key, value in summary.items() if value not in (None, "")}


def build_demo_order_canary_hard_controls_preflight_packet(
    *,
    canary_readiness_human_decision: Mapping[str, Any],
    demo_order_readiness_packet: Mapping[str, Any],
    allowed_demo_server: str,
    expected_runtime_symbol: str,
    max_lot_cap: float,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    """Build an inert hard-controls packet for later human canary review only."""

    decision = _as_mapping(canary_readiness_human_decision, name="canary_readiness_human_decision")
    readiness = _as_mapping(demo_order_readiness_packet, name="demo_order_readiness_packet")
    violations: list[str] = []

    if decision.get("schema_version") != CANARY_READINESS_DECISION_SCHEMA_VERSION:
        violations.append("unexpected_canary_readiness_decision_schema")
    if decision.get("decision") != CANARY_READINESS_APPROVAL_DECISION:
        violations.append("canary_readiness_decision_not_review_only_approved")
    if decision.get("approved") is not True or not _record_is_pass(decision):
        violations.append("canary_readiness_decision_not_passed")

    decision_authority = decision.get("authority")
    if not isinstance(decision_authority, Mapping):
        violations.append("canary_readiness_decision_authority_missing")
    elif decision_authority.get("canary_hard_controls_preflight_packet_construction_allowed") is not True:
        violations.append("preflight_packet_construction_not_allowed_by_decision")

    if not _record_is_pass(readiness):
        violations.append("demo_order_readiness_packet_is_not_passed")

    observed_server = _find_first_by_key(readiness, {"server", "demo_server", "allowed_demo_server", "account_server", "broker_server"})
    if observed_server not in (None, "") and str(observed_server) != allowed_demo_server:
        violations.append("demo_order_readiness_packet_server_does_not_match_allowed_demo_server")

    observed_currency = _find_first_by_key(readiness, {"currency", "account_currency", "account_currency_lock"})
    if observed_currency not in (None, "") and str(observed_currency).upper() != "USD":
        violations.append("demo_order_readiness_packet_currency_is_not_usd")

    observed_runtime_symbol = _find_first_by_key_in_order(readiness, ("runtime_symbol", "observed_runtime_symbol", "broker_symbol"))
    locked_symbol = str(observed_runtime_symbol or expected_runtime_symbol)
    if expected_runtime_symbol and locked_symbol != expected_runtime_symbol:
        violations.append("runtime_symbol_lock_does_not_match_expected_runtime_symbol")

    configured_cap = _to_float(max_lot_cap)
    if configured_cap is None or configured_cap <= 0:
        violations.append("max_lot_cap_must_be_positive")
        configured_cap = 0.0

    upstream_final_lots = _to_float(
        _find_first_by_key_in_order(readiness, ("final_lots", "verified_final_lots", "volume_lots", "lots"))
    )
    if upstream_final_lots is not None and configured_cap > upstream_final_lots:
        violations.append("max_lot_cap_exceeds_upstream_verified_final_lots")

    passed = not violations
    controls = {
        "allowed_demo_server_lock": {"required": True, "value": allowed_demo_server},
        "account_currency_lock": {"required": True, "value": "USD"},
        "account_context_lock": {"required": True, "value": "standard_demo_only"},
        "runtime_symbol_lock": {"required": True, "value": locked_symbol},
        "kill_switch_allow_state_required": True,
        "idempotency_ledger_required": True,
        "max_lot_cap": {
            "required": True,
            "value": configured_cap,
            "unit": "lots",
            "must_not_exceed_upstream_h020_final_lots": True,
            "upstream_verified_final_lots": upstream_final_lots,
        },
        "single_canary_order_limit": {"required": True, "value": 1},
        "post_order_audit_required_if_later_approved": True,
        "pre_dispatch_final_audit_required_if_later_approved": True,
        "human_demo_order_canary_approval_required_before_any_order_path": True,
        "live_order_forbidden": True,
    }
    authority = {
        "hard_controls_preflight_packet_constructed": passed,
        "requests_human_demo_order_canary_approval_review": passed,
        "review_only": True,
        "actual_broker_request_construction_approved": False,
        "actual_mt5_request_construction_approved": False,
        "order_payload_construction_approved": False,
        "transport_dispatch_approved": False,
        "terminal_or_broker_mutation_approved": False,
        "demo_order_canary_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "kind": KIND,
        "generated_at_utc": generated_at_utc or _utc_now_iso(),
        "decision": REQUEST_DECISION if passed else "REFUSE_HARD_CONTROLS_PREFLIGHT_PACKET",
        "status": "READY_FOR_HUMAN_DEMO_ORDER_CANARY_APPROVAL_REVIEW" if passed else "BLOCKED",
        "verdict": "PASS" if passed else "FAIL",
        "approved": False,
        "allowed_demo_server": allowed_demo_server,
        "expected_runtime_symbol": expected_runtime_symbol,
        "input_artifacts": {
            "canary_readiness_human_decision": _summarize_record(decision),
            "demo_order_readiness_packet": _summarize_record(readiness),
        },
        "required_hard_controls": controls,
        "authority": authority,
        "preserved_false_authority": {flag: False for flag in FALSE_AUTHORITY_FLAGS},
        "safety_boundary": {
            "pure_python_only": True,
            "review_only": True,
            "non_dispatchable": True,
            "no_terminal_or_broker_mutation": True,
            "no_demo_or_live_order_placement": True,
            "does_not_construct_actual_broker_request": True,
            "does_not_construct_actual_mt5_request": True,
            "does_not_construct_order_payload": True,
        },
        "next_required_gate": "separate_explicit_human_demo_order_canary_approval_artifact",
        "violations": violations,
    }


def validate_demo_order_canary_hard_controls_preflight_packet(
    record: Mapping[str, Any],
    *,
    allowed_demo_server: str,
    expected_runtime_symbol: str,
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

    embedded = candidate.get("violations")
    if isinstance(embedded, list) and embedded:
        violations.extend(f"embedded:{item}" for item in embedded)
    elif embedded not in (None, []):
        violations.append("embedded_violations_not_a_list")

    if require_pass and candidate.get("verdict") != "PASS":
        violations.append("verdict_not_pass")
    if require_pass and candidate.get("decision") != REQUEST_DECISION:
        violations.append("unexpected_decision")
    if candidate.get("approved") is not False:
        violations.append("packet_must_not_approve_canary")

    controls = candidate.get("required_hard_controls")
    if not isinstance(controls, Mapping):
        violations.append("required_hard_controls_missing_or_not_mapping")
        controls = {}

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
        actual = controls.get(key)
        if isinstance(actual, Mapping):
            actual_value = actual.get("value") if "value" in actual else actual.get("required")
        else:
            actual_value = actual
        if actual_value != expected:
            violations.append(f"{key}_mismatch")

    max_lot_cap = controls.get("max_lot_cap")
    if not isinstance(max_lot_cap, Mapping):
        violations.append("max_lot_cap_missing_or_not_mapping")
    else:
        cap_value = _to_float(max_lot_cap.get("value"))
        if cap_value is None or cap_value <= 0:
            violations.append("max_lot_cap_not_positive")
        upstream_value = _to_float(max_lot_cap.get("upstream_verified_final_lots"))
        if upstream_value is not None and cap_value is not None and cap_value > upstream_value:
            violations.append("max_lot_cap_exceeds_upstream_verified_final_lots")
        if max_lot_cap.get("must_not_exceed_upstream_h020_final_lots") is not True:
            violations.append("max_lot_cap_h020_bound_missing")

    single_limit = controls.get("single_canary_order_limit")
    if not isinstance(single_limit, Mapping) or single_limit.get("value") != 1:
        violations.append("single_canary_order_limit_not_one")

    authority = candidate.get("authority")
    if not isinstance(authority, Mapping):
        violations.append("authority_missing_or_not_mapping")
        authority = {}
    if authority.get("review_only") is not True:
        violations.append("review_only_not_true")
    if require_pass and authority.get("requests_human_demo_order_canary_approval_review") is not True:
        violations.append("human_canary_approval_review_not_requested")

    false_authority = candidate.get("preserved_false_authority")
    if not isinstance(false_authority, Mapping):
        violations.append("preserved_false_authority_missing_or_not_mapping")
        false_authority = {}
    for flag in FALSE_AUTHORITY_FLAGS:
        if false_authority.get(flag) is not False:
            violations.append(f"{flag}_not_false")

    boundary = candidate.get("safety_boundary")
    if not isinstance(boundary, Mapping):
        violations.append("safety_boundary_missing_or_not_mapping")
        boundary = {}
    for key in (
        "pure_python_only",
        "review_only",
        "non_dispatchable",
        "no_terminal_or_broker_mutation",
        "no_demo_or_live_order_placement",
        "does_not_construct_actual_broker_request",
        "does_not_construct_actual_mt5_request",
        "does_not_construct_order_payload",
    ):
        if boundary.get(key) is not True:
            violations.append(f"{key}_not_true")

    if candidate.get("required_hard_controls") is not None:
        copied = deepcopy(candidate["required_hard_controls"])
        if copied != candidate["required_hard_controls"]:
            violations.append("required_hard_controls_not_copyable")

    return violations


__all__ = [
    "KIND",
    "REQUEST_DECISION",
    "SCHEMA_VERSION",
    "build_demo_order_canary_hard_controls_preflight_packet",
    "validate_demo_order_canary_hard_controls_preflight_packet",
]