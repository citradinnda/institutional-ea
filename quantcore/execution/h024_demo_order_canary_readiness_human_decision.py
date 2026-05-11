"""Review-only H024 demo-order canary readiness human decision artifact.

This module is intentionally pure Python and non-mutating. It records a human
review decision that permits construction of a later hard-controls preflight
packet only. It does not approve canary order placement or any terminal/broker
mutation.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "h024_demo_order_canary_approval_readiness_human_decision_v1"
KIND = "h024_demo_order_canary_approval_readiness_human_decision"
APPROVAL_DECISION = "APPROVE_DEMO_ORDER_CANARY_READINESS_REVIEW_ONLY_NO_ORDER_PLACEMENT"
REFUSAL_DECISION = "REFUSE_DEMO_ORDER_CANARY_READINESS_REVIEW"

FALSE_AUTHORITY_FLAGS: tuple[str, ...] = (
    "demo_order_canary_approved",
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


def _summarize_readiness_packet(record: Mapping[str, Any]) -> dict[str, Any]:
    summary_keys = {
        "schema_version": record.get("schema_version") or record.get("schema"),
        "kind": record.get("kind"),
        "status": record.get("status"),
        "verdict": record.get("verdict"),
        "decision": record.get("decision"),
        "server": _find_first_by_key(record, {"server", "demo_server", "allowed_demo_server", "account_server", "broker_server"}),
        "account_currency": _find_first_by_key(record, {"currency", "account_currency", "account_currency_lock"}),
        "runtime_symbol": _find_first_by_key(record, {"runtime_symbol", "observed_runtime_symbol", "broker_symbol", "symbol"}),
        "idempotency_key": _find_first_by_key(record, {"idempotency_key", "preview_idempotency_key", "draft_idempotency_key"}),
    }
    return {key: value for key, value in summary_keys.items() if value not in (None, "")}


def build_demo_order_canary_readiness_human_decision(
    *,
    demo_order_readiness_packet: Mapping[str, Any],
    allowed_demo_server: str,
    reviewer: str = "human",
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    """Build the review-only human-decision artifact."""

    readiness = _as_mapping(demo_order_readiness_packet, name="demo_order_readiness_packet")
    violations: list[str] = []

    if not _record_is_pass(readiness):
        violations.append("demo_order_readiness_packet_is_not_passed")

    observed_server = _find_first_by_key(readiness, {"server", "demo_server", "allowed_demo_server", "account_server", "broker_server"})
    if observed_server not in (None, "") and str(observed_server) != allowed_demo_server:
        violations.append("demo_order_readiness_packet_server_does_not_match_allowed_demo_server")

    approved = not violations
    authority = {
        "demo_order_canary_readiness_review_approved": approved,
        "canary_hard_controls_preflight_packet_construction_allowed": approved,
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

    record = {
        "schema_version": SCHEMA_VERSION,
        "kind": KIND,
        "generated_at_utc": generated_at_utc or _utc_now_iso(),
        "reviewer": reviewer,
        "decision": APPROVAL_DECISION if approved else REFUSAL_DECISION,
        "status": "APPROVED_REVIEW_ONLY" if approved else "BLOCKED",
        "verdict": "PASS" if approved else "FAIL",
        "approved": approved,
        "allowed_demo_server": allowed_demo_server,
        "input_artifacts": {
            "demo_order_readiness_packet": _summarize_readiness_packet(readiness),
        },
        "authority": authority,
        "preserved_false_authority": {flag: False for flag in FALSE_AUTHORITY_FLAGS},
        "next_allowed_artifact": "h024_demo_order_canary_hard_controls_preflight_packet_v1" if approved else None,
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
        "violations": violations,
    }
    return record


def validate_demo_order_canary_readiness_human_decision(
    record: Mapping[str, Any],
    *,
    allowed_demo_server: str,
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

    embedded = candidate.get("violations")
    if isinstance(embedded, list) and embedded:
        violations.extend(f"embedded:{item}" for item in embedded)
    elif embedded not in (None, []):
        violations.append("embedded_violations_not_a_list")

    if require_approved and candidate.get("approved") is not True:
        violations.append("decision_not_approved")
    if require_approved and candidate.get("decision") != APPROVAL_DECISION:
        violations.append("unexpected_decision")
    if require_approved and candidate.get("verdict") != "PASS":
        violations.append("verdict_not_pass")

    authority = candidate.get("authority")
    if not isinstance(authority, Mapping):
        violations.append("authority_missing_or_not_mapping")
        authority = {}
    if authority.get("review_only") is not True:
        violations.append("review_only_not_true")
    if require_approved and authority.get("canary_hard_controls_preflight_packet_construction_allowed") is not True:
        violations.append("preflight_packet_construction_not_allowed")

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

    if candidate.get("preserved_false_authority") is not None:
        copied = deepcopy(candidate["preserved_false_authority"])
        if copied != candidate["preserved_false_authority"]:
            violations.append("preserved_false_authority_not_copyable")

    return violations


__all__ = [
    "APPROVAL_DECISION",
    "FALSE_AUTHORITY_FLAGS",
    "KIND",
    "SCHEMA_VERSION",
    "build_demo_order_canary_readiness_human_decision",
    "validate_demo_order_canary_readiness_human_decision",
]