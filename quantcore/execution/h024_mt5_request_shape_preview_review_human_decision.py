"""H024 MT5 request-shape preview review human decision.

This artifact approves review of the inert MT5 request-shape preview and
preparation of a demo-order readiness packet. It does not approve demo order
placement, live order placement, dispatch, terminal mutation, broker mutation,
or execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_mt5_request_shape_preview_review_human_decision_v1"
KIND = "MT5_REQUEST_SHAPE_PREVIEW_REVIEW_HUMAN_DECISION"
STATUS = "MT5_REQUEST_SHAPE_PREVIEW_REVIEW_APPROVED_NO_ORDER_AUTHORITY"
DECISION = "APPROVE_MT5_REQUEST_SHAPE_PREVIEW_REVIEW_ONLY_NO_DEMO_ORDER_NO_DISPATCH"

SHAPE_PREVIEW_SCHEMA = "h024_mt5_request_shape_preview_envelope_v1"


@dataclass(frozen=True)
class Mt5RequestShapePreviewReviewHumanDecisionInputs:
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


def _validate_shape_preview(shape_preview: Mapping[str, Any], allowed_demo_server: str) -> list[str]:
    violations: list[str] = []

    if shape_preview.get("schema") != SHAPE_PREVIEW_SCHEMA:
        violations.append("shape_preview_schema_mismatch")
    if shape_preview.get("verdict") != "PASS":
        violations.append("shape_preview_not_pass")
    if shape_preview.get("allowed_demo_server") != allowed_demo_server:
        violations.append("shape_preview_demo_server_mismatch")

    required_consumption_true = (
        "design_review_packet_consumed",
        "reviewed_draft_summary_consumed",
        "h020_sizing_consumed_not_reinterpreted",
        "kill_switch_allow_state_required",
        "idempotency_key_carried_forward",
    )
    for key in required_consumption_true:
        if _nested_bool(shape_preview, "consumption_flags", key) is not True:
            violations.append(f"shape_preview_missing_consumption_{key}")

    required_shape_true = (
        "shape_preview_envelope_constructed",
        "shape_preview_only",
        "not_actual_mt5_request",
        "not_actual_broker_request",
        "not_order_payload",
        "not_dispatchable",
        "contains_no_transport_instruction",
        "contains_no_terminal_mutation_instruction",
    )
    for key in required_shape_true:
        if _nested_bool(shape_preview, "shape_preview_flags", key) is not True:
            violations.append(f"shape_preview_missing_flag_{key}")

    identity = _nested_mapping(shape_preview, "identity")
    if not identity.get("shape_preview_idempotency_key"):
        violations.append("shape_preview_missing_idempotency_key")

    authority_true = (
        "phase4_approved",
        "broker_request_draft_review_approved",
        "mt5_request_shape_design_review_packet_constructed",
        "mt5_request_shape_construction_approved",
        "mt5_request_shape_preview_envelope_constructed",
    )
    for key in authority_true:
        if _nested_bool(shape_preview, "authority_flags", key) is not True:
            violations.append(f"shape_preview_missing_authority_true_{key}")

    authority_false = (
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
        if _nested_bool(shape_preview, "authority_flags", key) is not False:
            violations.append(f"shape_preview_forbidden_authority_not_false_{key}")

    return violations


def build_mt5_request_shape_preview_review_human_decision(
    inputs: Mt5RequestShapePreviewReviewHumanDecisionInputs,
) -> dict[str, Any]:
    shape_preview = dict(inputs.shape_preview_envelope)
    violations = _validate_shape_preview(shape_preview, inputs.allowed_demo_server)

    return {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "shape_preview_schema": shape_preview.get("schema"),
            "shape_preview_kind": shape_preview.get("kind"),
            "shape_preview_status": shape_preview.get("status"),
            "shape_preview_decision": shape_preview.get("decision"),
            "shape_preview_digest_sha256": stable_json_digest(shape_preview),
        },
        "approved_scope": {
            "may_review_inert_mt5_request_shape_preview": not violations,
            "may_prepare_demo_order_readiness_packet": not violations,
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
        "required_next_gate_constraints": {
            "demo_order_readiness_packet_review_only": True,
            "no_demo_order_approval": True,
            "no_live_order_approval": True,
            "no_mt5_request_construction": True,
            "no_order_payload_construction": True,
            "no_metatrader5_import_or_call": True,
            "no_transport_dispatch": True,
            "no_terminal_or_broker_mutation": True,
            "separate_human_canary_approval_required_before_any_demo_order": True,
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_draft_review_approved": True,
            "mt5_request_shape_design_review_packet_constructed": True,
            "mt5_request_shape_construction_approved": True,
            "mt5_request_shape_preview_envelope_constructed": True,
            "mt5_request_shape_preview_review_approved": not violations,
            "demo_order_readiness_packet_allowed": not violations,
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