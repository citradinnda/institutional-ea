"""H024 inert MT5 request-shape preview envelope.

This envelope is a review-only shape preview. It intentionally avoids being a
sendable terminal request or order payload.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_mt5_request_shape_preview_envelope_v1"
KIND = "MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE"
STATUS = "INERT_MT5_REQUEST_SHAPE_PREVIEW_CONSTRUCTED_NO_REQUEST_NO_DISPATCH"
DECISION = "CONSTRUCT_INERT_MT5_REQUEST_SHAPE_PREVIEW_ONLY_REFUSE_DISPATCH"

APPROVAL_SCHEMA = "h024_mt5_request_shape_construction_approval_v1"
DESIGN_PACKET_SCHEMA = "h024_mt5_request_shape_design_review_packet_v1"


@dataclass(frozen=True)
class Mt5RequestShapePreviewEnvelopeInputs:
    construction_approval: Mapping[str, Any]
    design_review_packet: Mapping[str, Any]
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


def _validate_inputs(
    approval: Mapping[str, Any],
    design_packet: Mapping[str, Any],
    allowed_demo_server: str,
) -> list[str]:
    violations: list[str] = []

    if approval.get("schema") != APPROVAL_SCHEMA:
        violations.append("construction_approval_schema_mismatch")
    if approval.get("verdict") != "PASS":
        violations.append("construction_approval_not_pass")
    if approval.get("allowed_demo_server") != allowed_demo_server:
        violations.append("construction_approval_demo_server_mismatch")
    if _nested_bool(approval, "approved_scope", "may_construct_inert_mt5_request_shape_preview_envelope") is not True:
        violations.append("shape_preview_construction_not_approved")

    if design_packet.get("schema") != DESIGN_PACKET_SCHEMA:
        violations.append("design_packet_schema_mismatch")
    if design_packet.get("verdict") != "PASS":
        violations.append("design_packet_not_pass")
    if design_packet.get("allowed_demo_server") != allowed_demo_server:
        violations.append("design_packet_demo_server_mismatch")

    for key in (
        "constructs_mt5_request",
        "constructs_order_payload",
        "constructs_actual_broker_request",
        "dispatches_transport",
        "mutates_terminal_or_broker_state",
        "approves_execution",
    ):
        if _nested_bool(design_packet, "design_scope", key) is not False:
            violations.append(f"design_scope_forbidden_not_false_{key}")

    source = _nested_mapping(design_packet, "source_conceptual_draft_summary")
    for key in (
        "normalized_symbol",
        "runtime_symbol",
        "conceptual_side",
        "h020_final_lots",
        "entry_reference_price",
        "protective_stop_reference_price",
    ):
        if source.get(key) in (None, ""):
            violations.append(f"source_conceptual_field_missing_{key}")

    return violations


def _side_preview(conceptual_side: Any) -> str | None:
    if not isinstance(conceptual_side, str):
        return None
    lowered = conceptual_side.lower()
    if "sell" in lowered or "short" in lowered:
        return "SELL_DIRECTION_REVIEW_ONLY"
    if "buy" in lowered or "long" in lowered:
        return "BUY_DIRECTION_REVIEW_ONLY"
    return "UNKNOWN_DIRECTION_REVIEW_ONLY"


def build_mt5_request_shape_preview_envelope(
    inputs: Mt5RequestShapePreviewEnvelopeInputs,
) -> dict[str, Any]:
    approval = dict(inputs.construction_approval)
    design_packet = dict(inputs.design_review_packet)
    violations = _validate_inputs(approval, design_packet, inputs.allowed_demo_server)

    source = _nested_mapping(design_packet, "source_conceptual_draft_summary")
    preview_identity_source = {
        "approval_digest": stable_json_digest(approval),
        "design_packet_digest": stable_json_digest(design_packet),
        "schema": SCHEMA,
    }
    shape_preview_idempotency_key = sha256(
        json.dumps(preview_identity_source, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    shape_preview = {
        "field_set_kind": "INERT_TERMINAL_REQUEST_SHAPE_REVIEW_FIELDS_NOT_SENDABLE",
        "instrument_identity_review": {
            "normalized_symbol": source.get("normalized_symbol"),
            "runtime_symbol": source.get("runtime_symbol"),
        },
        "direction_review": {
            "source_conceptual_side": source.get("conceptual_side"),
            "terminal_direction_label_review_only": _side_preview(source.get("conceptual_side")),
        },
        "quantity_review": {
            "h020_final_lots": source.get("h020_final_lots"),
            "sizing_source": "H020_CONSUMED_NOT_REINTERPRETED",
        },
        "price_reference_review": {
            "entry_reference_price": source.get("entry_reference_price"),
            "protective_stop_reference_price": source.get("protective_stop_reference_price"),
            "reference_only_not_sendable_instruction": True,
        },
        "idempotency_review": {
            "shape_preview_idempotency_key": shape_preview_idempotency_key,
            "must_be_carried_to_any_later_preview": True,
        },
        "transport_review": {
            "dispatch_instruction_absent": True,
            "non_dispatchable": True,
        },
    }

    record = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "construction_approval_schema": approval.get("schema"),
            "construction_approval_kind": approval.get("kind"),
            "construction_approval_digest_sha256": stable_json_digest(approval),
            "design_review_packet_schema": design_packet.get("schema"),
            "design_review_packet_kind": design_packet.get("kind"),
            "design_review_packet_digest_sha256": stable_json_digest(design_packet),
        },
        "identity": {
            "shape_preview_idempotency_key": shape_preview_idempotency_key,
            "idempotency_key_carried_forward": True,
        },
        "consumption_flags": {
            "design_review_packet_consumed": True,
            "reviewed_draft_summary_consumed": True,
            "h020_sizing_consumed_not_reinterpreted": True,
            "kill_switch_allow_state_required": True,
            "idempotency_key_carried_forward": True,
        },
        "shape_preview_flags": {
            "shape_preview_envelope_constructed": not violations,
            "shape_preview_only": True,
            "not_actual_mt5_request": True,
            "not_actual_broker_request": True,
            "not_order_payload": True,
            "not_dispatchable": True,
            "contains_no_transport_instruction": True,
            "contains_no_terminal_mutation_instruction": True,
        },
        "inert_terminal_request_shape_preview": shape_preview,
        "forbidden_sendable_field_names_absent_by_design": {
            "action": "absent_to_keep_preview_non_sendable",
            "type": "absent_to_keep_preview_non_sendable",
            "volume": "absent_to_keep_preview_non_sendable",
            "price": "absent_to_keep_preview_non_sendable",
            "sl": "absent_to_keep_preview_non_sendable",
            "tp": "absent_to_keep_preview_non_sendable",
            "deviation": "absent_to_keep_preview_non_sendable",
            "magic": "absent_to_keep_preview_non_sendable",
            "comment": "absent_to_keep_preview_non_sendable",
            "type_time": "absent_to_keep_preview_non_sendable",
            "type_filling": "absent_to_keep_preview_non_sendable",
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_draft_review_approved": True,
            "mt5_request_shape_design_review_packet_constructed": True,
            "mt5_request_shape_construction_approved": not violations,
            "mt5_request_shape_preview_envelope_constructed": not violations,
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
    return record


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