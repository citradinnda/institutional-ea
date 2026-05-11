"""H024 demo-order readiness packet.

This packet requests human review for a future tightly controlled demo-order
canary. It is not demo-order approval and it performs no request construction,
payload construction, dispatch, terminal mutation, broker mutation, or
execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_demo_order_readiness_packet_v1"
KIND = "DEMO_ORDER_READINESS_PACKET_REVIEW_ONLY"
STATUS = "READY_FOR_HUMAN_DEMO_ORDER_CANARY_REVIEW_NO_ORDER_AUTHORITY"
DECISION = "REQUEST_HUMAN_DEMO_ORDER_CANARY_REVIEW_NO_ORDER_PLACEMENT_AUTHORITY"

HUMAN_DECISION_SCHEMA = "h024_mt5_request_shape_preview_review_human_decision_v1"
SHAPE_PREVIEW_SCHEMA = "h024_mt5_request_shape_preview_envelope_v1"


@dataclass(frozen=True)
class DemoOrderReadinessPacketInputs:
    shape_preview_review_human_decision: Mapping[str, Any]
    shape_preview_envelope: Mapping[str, Any]
    allowed_demo_server: str


def stable_json_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def _nested_bool(record: Mapping[str, Any], section: str, key: str) -> bool | None:
    value = record.get(section)
    if isinstance(value, Mapping):
        nested = value.get(key)
        if isinstance(nested, bool):
            return nested
    return None


def _nested_mapping(record: Mapping[str, Any], section: str) -> Mapping[str, Any]:
    value = record.get(section)
    return value if isinstance(value, Mapping) else {}


def _validate_human_decision(decision: Mapping[str, Any], allowed_demo_server: str) -> list[str]:
    violations: list[str] = []

    if decision.get("schema") != HUMAN_DECISION_SCHEMA:
        violations.append("shape_preview_review_human_decision_schema_mismatch")
    if decision.get("verdict") != "PASS":
        violations.append("shape_preview_review_human_decision_not_pass")
    if decision.get("allowed_demo_server") != allowed_demo_server:
        violations.append("shape_preview_review_human_decision_demo_server_mismatch")
    if _nested_bool(decision, "approved_scope", "may_prepare_demo_order_readiness_packet") is not True:
        violations.append("demo_order_readiness_not_allowed")

    forbidden_scope = (
        "may_construct_actual_broker_request",
        "may_construct_mt5_request",
        "may_construct_order_payload",
        "may_dispatch_transport",
        "may_place_demo_order",
        "may_place_live_order",
        "may_mutate_terminal_state",
        "may_mutate_broker_state",
        "may_execute",
    )
    for key in forbidden_scope:
        if _nested_bool(decision, "approved_scope", key) is not False:
            violations.append(f"human_decision_forbidden_scope_not_false_{key}")

    return violations


def _validate_shape_preview(shape_preview: Mapping[str, Any], allowed_demo_server: str) -> list[str]:
    violations: list[str] = []

    if shape_preview.get("schema") != SHAPE_PREVIEW_SCHEMA:
        violations.append("shape_preview_schema_mismatch")
    if shape_preview.get("verdict") != "PASS":
        violations.append("shape_preview_not_pass")
    if shape_preview.get("allowed_demo_server") != allowed_demo_server:
        violations.append("shape_preview_demo_server_mismatch")

    for key in (
        "shape_preview_envelope_constructed",
        "shape_preview_only",
        "not_actual_mt5_request",
        "not_actual_broker_request",
        "not_order_payload",
        "not_dispatchable",
    ):
        if _nested_bool(shape_preview, "shape_preview_flags", key) is not True:
            violations.append(f"shape_preview_missing_flag_{key}")

    for key in (
        "h020_sizing_consumed_not_reinterpreted",
        "kill_switch_allow_state_required",
        "idempotency_key_carried_forward",
    ):
        if _nested_bool(shape_preview, "consumption_flags", key) is not True:
            violations.append(f"shape_preview_missing_consumption_{key}")

    preview = _nested_mapping(shape_preview, "inert_terminal_request_shape_preview")
    if preview.get("field_set_kind") != "INERT_TERMINAL_REQUEST_SHAPE_REVIEW_FIELDS_NOT_SENDABLE":
        violations.append("shape_preview_field_set_kind_mismatch")

    authority_false = (
        "actual_broker_request_construction_approved",
        "actual_broker_request_constructed",
        "mt5_request_construction_approved",
        "mt5_request_constructed",
        "order_payload_construction_approved",
        "order_payload_constructed",
        "transport_dispatch_attempted",
        "dispatch_attempted",
        "terminal_mutated",
        "broker_state_mutated",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_approved",
    )
    for key in authority_false:
        if _nested_bool(shape_preview, "authority_flags", key) is not False:
            violations.append(f"shape_preview_forbidden_authority_not_false_{key}")

    return violations


def build_demo_order_readiness_packet(
    inputs: DemoOrderReadinessPacketInputs,
) -> dict[str, Any]:
    human_decision = dict(inputs.shape_preview_review_human_decision)
    shape_preview = dict(inputs.shape_preview_envelope)

    violations: list[str] = []
    violations.extend(_validate_human_decision(human_decision, inputs.allowed_demo_server))
    violations.extend(_validate_shape_preview(shape_preview, inputs.allowed_demo_server))

    preview = _nested_mapping(shape_preview, "inert_terminal_request_shape_preview")
    identity = _nested_mapping(shape_preview, "identity")

    readiness_summary = {
        "source_shape_preview_idempotency_key": identity.get("shape_preview_idempotency_key"),
        "shape_preview_field_set_kind": preview.get("field_set_kind"),
        "instrument_identity_review": preview.get("instrument_identity_review"),
        "direction_review": preview.get("direction_review"),
        "quantity_review": preview.get("quantity_review"),
        "price_reference_review": preview.get("price_reference_review"),
        "transport_review": preview.get("transport_review"),
    }

    return {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "shape_preview_review_human_decision_schema": human_decision.get("schema"),
            "shape_preview_review_human_decision_kind": human_decision.get("kind"),
            "shape_preview_review_human_decision_digest_sha256": stable_json_digest(human_decision),
            "shape_preview_envelope_schema": shape_preview.get("schema"),
            "shape_preview_envelope_kind": shape_preview.get("kind"),
            "shape_preview_envelope_digest_sha256": stable_json_digest(shape_preview),
        },
        "readiness_scope": {
            "packet_is_review_only": True,
            "requests_human_demo_order_canary_review": True,
            "approves_demo_order_canary": False,
            "approves_demo_order_placement": False,
            "approves_live_order_placement": False,
            "constructs_actual_broker_request": False,
            "constructs_mt5_request": False,
            "constructs_order_payload": False,
            "dispatches_transport": False,
            "mutates_terminal_or_broker_state": False,
            "approves_execution": False,
        },
        "required_canary_controls_for_later_approval": {
            "separate_explicit_human_canary_approval_required": True,
            "allowed_demo_server_lock_required": True,
            "symbol_lock_required": True,
            "kill_switch_allow_state_required": True,
            "idempotency_ledger_required": True,
            "max_lot_cap_required": True,
            "single_canary_order_limit_required": True,
            "post_order_audit_required_if_later_approved": True,
            "live_order_placement_remains_forbidden": True,
        },
        "readiness_summary_from_shape_preview": readiness_summary,
        "authority_flags": {
            "phase4_approved": True,
            "mt5_request_shape_preview_review_approved": not violations,
            "demo_order_readiness_packet_constructed": not violations,
            "demo_order_canary_review_requested": not violations,
            "demo_order_canary_approved": False,
            "actual_broker_request_construction_approved": False,
            "actual_broker_request_constructed": False,
            "mt5_request_construction_approved": False,
            "mt5_request_constructed": False,
            "order_payload_construction_approved": False,
            "order_payload_constructed": False,
            "execution_capable_adapter_use_approved": False,
            "transport_dispatch_attempted": False,
            "dispatch_attempted": False,
            "terminal_mutated": False,
            "broker_state_mutated": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_approved": False,
        },
    }


def load_single_jsonl_record(path: str | Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    if len(records) != 1:
        raise ValueError(f"expected exactly one JSONL record in {path}, found {len(records)}")
    return records[0]


def write_single_jsonl_record(path: str | Path, record: Mapping[str, Any]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False))
        handle.write("\n")