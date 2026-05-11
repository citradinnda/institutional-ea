"""H024 MT5 request-shape design review packet.

This packet is design-only. It does not construct an MT5 request, does not
construct an order payload, and does not dispatch anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_mt5_request_shape_design_review_packet_v1"
KIND = "MT5_REQUEST_SHAPE_DESIGN_REVIEW_PACKET"
STATUS = "READY_FOR_HUMAN_MT5_REQUEST_SHAPE_REVIEW_NO_REQUEST_CONSTRUCTION"
DECISION = "REQUEST_HUMAN_MT5_REQUEST_SHAPE_REVIEW_NO_MT5_NO_DISPATCH"

DRAFT_DECISION_SCHEMA = "h024_broker_request_draft_review_human_decision_v1"
DRAFT_ENVELOPE_SCHEMA = "h024_broker_request_draft_envelope_v1"


@dataclass(frozen=True)
class Mt5RequestShapeDesignReviewInputs:
    draft_review_human_decision: Mapping[str, Any]
    draft_envelope: Mapping[str, Any]
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

    if decision.get("schema") != DRAFT_DECISION_SCHEMA:
        violations.append("draft_review_human_decision_schema_mismatch")
    if decision.get("verdict") != "PASS":
        violations.append("draft_review_human_decision_not_pass")
    if decision.get("allowed_demo_server") != allowed_demo_server:
        violations.append("draft_review_human_decision_demo_server_mismatch")
    if _nested_bool(decision, "approved_scope", "may_prepare_mt5_request_shape_design_review") is not True:
        violations.append("mt5_request_shape_design_review_not_allowed")

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


def _validate_draft_envelope(draft_envelope: Mapping[str, Any], allowed_demo_server: str) -> list[str]:
    violations: list[str] = []

    if draft_envelope.get("schema") != DRAFT_ENVELOPE_SCHEMA:
        violations.append("draft_envelope_schema_mismatch")
    if draft_envelope.get("verdict") != "PASS":
        violations.append("draft_envelope_not_pass")
    if draft_envelope.get("allowed_demo_server") != allowed_demo_server:
        violations.append("draft_envelope_demo_server_mismatch")

    for key in (
        "draft_is_non_dispatchable",
        "not_mt5_request",
        "not_broker_request",
        "not_order_payload",
        "review_envelope_only",
    ):
        if _nested_bool(draft_envelope, "draft_flags", key) is not True:
            violations.append(f"draft_envelope_missing_draft_flag_{key}")

    for key in (
        "actual_broker_request_constructed",
        "mt5_request_constructed",
        "order_payload_constructed",
        "dispatch_attempted",
        "terminal_mutated",
        "broker_state_mutated",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_approved",
    ):
        if _nested_bool(draft_envelope, "authority_flags", key) is not False:
            violations.append(f"draft_envelope_forbidden_authority_not_false_{key}")

    conceptual = _nested_mapping(draft_envelope, "canonical_conceptual_review_fields")
    for key in (
        "normalized_symbol",
        "runtime_symbol",
        "conceptual_side",
        "h020_final_lots",
        "entry_reference_price",
        "protective_stop_reference_price",
    ):
        if conceptual.get(key) in (None, ""):
            violations.append(f"draft_envelope_missing_conceptual_field_{key}")

    return violations


def build_mt5_request_shape_design_review_packet(
    inputs: Mt5RequestShapeDesignReviewInputs,
) -> dict[str, Any]:
    human_decision = dict(inputs.draft_review_human_decision)
    draft_envelope = dict(inputs.draft_envelope)

    violations = []
    violations.extend(_validate_human_decision(human_decision, inputs.allowed_demo_server))
    violations.extend(_validate_draft_envelope(draft_envelope, inputs.allowed_demo_server))

    conceptual = _nested_mapping(draft_envelope, "canonical_conceptual_review_fields")

    return {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "draft_review_human_decision_schema": human_decision.get("schema"),
            "draft_review_human_decision_kind": human_decision.get("kind"),
            "draft_review_human_decision_digest_sha256": stable_json_digest(human_decision),
            "draft_envelope_schema": draft_envelope.get("schema"),
            "draft_envelope_kind": draft_envelope.get("kind"),
            "draft_envelope_digest_sha256": stable_json_digest(draft_envelope),
        },
        "design_scope": {
            "design_review_only": True,
            "describes_future_request_shape_constraints": True,
            "constructs_mt5_request": False,
            "constructs_order_payload": False,
            "constructs_actual_broker_request": False,
            "dispatches_transport": False,
            "mutates_terminal_or_broker_state": False,
            "approves_execution": False,
        },
        "source_conceptual_draft_summary": {
            "normalized_symbol": conceptual.get("normalized_symbol"),
            "runtime_symbol": conceptual.get("runtime_symbol"),
            "conceptual_side": conceptual.get("conceptual_side"),
            "h020_final_lots": conceptual.get("h020_final_lots"),
            "entry_reference_price": conceptual.get("entry_reference_price"),
            "protective_stop_reference_price": conceptual.get("protective_stop_reference_price"),
            "sizing_source": conceptual.get("sizing_source"),
            "execution_shape": conceptual.get("execution_shape"),
        },
        "future_shape_constraints": {
            "must_be_derived_only_from_reviewed_draft_envelope": True,
            "must_carry_idempotency_forward": True,
            "must_consume_h020_sizing_without_reinterpretation": True,
            "must_require_kill_switch_allow_state": True,
            "must_remain_inert_until_separately_approved": True,
            "must_not_import_or_call_metatrader5": True,
            "must_not_dispatch": True,
            "must_not_mutate_terminal_or_broker_state": True,
            "must_not_place_demo_or_live_order": True,
        },
        "non_executable_mapping_review": {
            "instrument_identity": "conceptual mapping only from normalized/runtime symbol fields",
            "side_identity": "conceptual mapping only from reviewed side field",
            "lot_quantity": "conceptual mapping only from H020 final lots",
            "entry_reference": "reference price only, not a sendable price instruction",
            "protective_stop_reference": "reference stop only, not a sendable stop instruction",
            "idempotency": "must be carried forward before any later preview can exist",
            "dispatch": "explicitly absent",
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_preview_construction_approved": True,
            "broker_request_preview_envelope_constructed": True,
            "broker_request_draft_construction_approved": True,
            "broker_request_draft_envelope_constructed": True,
            "broker_request_draft_review_approved": not violations,
            "mt5_request_shape_design_review_packet_constructed": not violations,
            "mt5_request_shape_construction_approved": False,
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