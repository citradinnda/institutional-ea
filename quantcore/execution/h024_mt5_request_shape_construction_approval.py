"""H024 MT5 request-shape construction approval.

This approval permits only an inert request-shape preview envelope. It does
not approve executable request construction, order payload construction,
transport dispatch, terminal mutation, broker mutation, demo orders, live
orders, or execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_mt5_request_shape_construction_approval_v1"
KIND = "MT5_REQUEST_SHAPE_CONSTRUCTION_APPROVAL"
STATUS = "MT5_REQUEST_SHAPE_PREVIEW_CONSTRUCTION_APPROVED_NO_REQUEST_NO_DISPATCH"
DECISION = "APPROVE_INERT_MT5_REQUEST_SHAPE_PREVIEW_ONLY_NO_REQUEST_NO_DISPATCH"

DESIGN_PACKET_SCHEMA = "h024_mt5_request_shape_design_review_packet_v1"


@dataclass(frozen=True)
class Mt5RequestShapeConstructionApprovalInputs:
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


def _validate_design_packet(packet: Mapping[str, Any], allowed_demo_server: str) -> list[str]:
    violations: list[str] = []

    if packet.get("schema") != DESIGN_PACKET_SCHEMA:
        violations.append("design_packet_schema_mismatch")
    if packet.get("verdict") != "PASS":
        violations.append("design_packet_not_pass")
    if packet.get("allowed_demo_server") != allowed_demo_server:
        violations.append("design_packet_demo_server_mismatch")

    design_true = (
        "design_review_only",
        "describes_future_request_shape_constraints",
    )
    for key in design_true:
        if _nested_bool(packet, "design_scope", key) is not True:
            violations.append(f"design_scope_missing_true_{key}")

    design_false = (
        "constructs_mt5_request",
        "constructs_order_payload",
        "constructs_actual_broker_request",
        "dispatches_transport",
        "mutates_terminal_or_broker_state",
        "approves_execution",
    )
    for key in design_false:
        if _nested_bool(packet, "design_scope", key) is not False:
            violations.append(f"design_scope_forbidden_not_false_{key}")

    constraints_true = (
        "must_be_derived_only_from_reviewed_draft_envelope",
        "must_carry_idempotency_forward",
        "must_consume_h020_sizing_without_reinterpretation",
        "must_require_kill_switch_allow_state",
        "must_remain_inert_until_separately_approved",
        "must_not_import_or_call_metatrader5",
        "must_not_dispatch",
        "must_not_mutate_terminal_or_broker_state",
        "must_not_place_demo_or_live_order",
    )
    for key in constraints_true:
        if _nested_bool(packet, "future_shape_constraints", key) is not True:
            violations.append(f"future_constraint_missing_true_{key}")

    source = _nested_mapping(packet, "source_conceptual_draft_summary")
    for key in (
        "normalized_symbol",
        "runtime_symbol",
        "conceptual_side",
        "h020_final_lots",
        "entry_reference_price",
        "protective_stop_reference_price",
        "sizing_source",
        "execution_shape",
    ):
        if source.get(key) in (None, ""):
            violations.append(f"source_conceptual_field_missing_{key}")

    authority_true = (
        "phase4_approved",
        "broker_request_draft_review_approved",
        "mt5_request_shape_design_review_packet_constructed",
    )
    for key in authority_true:
        if _nested_bool(packet, "authority_flags", key) is not True:
            violations.append(f"authority_missing_true_{key}")

    authority_false = (
        "mt5_request_shape_construction_approved",
        "actual_broker_request_construction_approved",
        "actual_broker_request_constructed",
        "mt5_request_construction_approved",
        "mt5_request_constructed",
        "order_payload_construction_approved",
        "order_payload_constructed",
        "execution_capable_adapter_use_approved",
        "transport_dispatch_attempted",
        "dispatch_attempted",
        "terminal_mutated",
        "broker_state_mutated",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_approved",
    )
    for key in authority_false:
        if _nested_bool(packet, "authority_flags", key) is not False:
            violations.append(f"authority_forbidden_not_false_{key}")

    return violations


def build_mt5_request_shape_construction_approval(
    inputs: Mt5RequestShapeConstructionApprovalInputs,
) -> dict[str, Any]:
    packet = dict(inputs.design_review_packet)
    violations = _validate_design_packet(packet, inputs.allowed_demo_server)

    return {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "design_review_packet_schema": packet.get("schema"),
            "design_review_packet_kind": packet.get("kind"),
            "design_review_packet_status": packet.get("status"),
            "design_review_packet_decision": packet.get("decision"),
            "design_review_packet_digest_sha256": stable_json_digest(packet),
        },
        "approved_scope": {
            "may_construct_inert_mt5_request_shape_preview_envelope": not violations,
            "may_construct_actual_broker_request": False,
            "may_construct_mt5_request": False,
            "may_construct_order_payload": False,
            "may_dispatch_transport": False,
            "may_place_demo_order": False,
            "may_place_live_order": False,
            "may_mutate_terminal_state": False,
            "may_mutate_broker_state": False,
            "may_execute": False,
        },
        "required_preview_constraints": {
            "must_consume_design_review_packet": True,
            "must_consume_reviewed_draft_summary": True,
            "must_carry_idempotency_forward": True,
            "must_consume_h020_sizing_without_reinterpretation": True,
            "must_require_kill_switch_allow_state": True,
            "must_remain_non_dispatchable": True,
            "must_not_import_or_call_metatrader5": True,
            "must_not_be_actual_mt5_request": True,
            "must_not_be_order_payload": True,
            "must_not_mutate_terminal_or_broker_state": True,
            "must_not_place_demo_or_live_order": True,
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_preview_construction_approved": True,
            "broker_request_preview_envelope_constructed": True,
            "broker_request_draft_construction_approved": True,
            "broker_request_draft_envelope_constructed": True,
            "broker_request_draft_review_approved": True,
            "mt5_request_shape_design_review_packet_constructed": True,
            "mt5_request_shape_construction_approved": not violations,
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