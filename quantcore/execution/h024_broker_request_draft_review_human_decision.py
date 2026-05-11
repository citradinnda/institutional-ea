"""H024 broker-request draft review human decision.

This artifact approves review of the inert canonical draft only. It does not
approve actual broker-request construction, MT5 request construction, order
payload construction, dispatch, demo/live order placement, or execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_broker_request_draft_review_human_decision_v1"
KIND = "BROKER_REQUEST_DRAFT_REVIEW_HUMAN_DECISION"
STATUS = "BROKER_REQUEST_DRAFT_REVIEW_APPROVED_NO_EXECUTION_AUTHORITY"
DECISION = "APPROVE_BROKER_REQUEST_DRAFT_REVIEW_ONLY_NO_MT5_NO_DISPATCH"

DRAFT_ENVELOPE_SCHEMA = "h024_broker_request_draft_envelope_v1"


@dataclass(frozen=True)
class DraftReviewHumanDecisionInputs:
    draft_envelope: Mapping[str, Any]
    allowed_demo_server: str


def stable_json_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def _nested_bool(record: Mapping[str, Any], section: str, key: str) -> bool | None:
    section_value = record.get(section)
    if isinstance(section_value, Mapping):
        value = section_value.get(key)
        if isinstance(value, bool):
            return value
    return None


def _nested_mapping(record: Mapping[str, Any], section: str) -> Mapping[str, Any]:
    value = record.get(section)
    return value if isinstance(value, Mapping) else {}


def _validate_draft_envelope(draft_envelope: Mapping[str, Any], allowed_demo_server: str) -> list[str]:
    violations: list[str] = []

    if draft_envelope.get("schema") != DRAFT_ENVELOPE_SCHEMA:
        violations.append("draft_envelope_schema_mismatch")
    if draft_envelope.get("verdict") != "PASS":
        violations.append("draft_envelope_not_pass")
    if draft_envelope.get("allowed_demo_server") != allowed_demo_server:
        violations.append("draft_envelope_demo_server_mismatch")

    required_consumption_true = (
        "preview_envelope_consumed",
        "verified_intent_consumed",
        "h020_sizing_consumed_not_reinterpreted",
        "kill_switch_allow_state_required",
        "idempotency_key_carried_forward",
    )
    for key in required_consumption_true:
        if _nested_bool(draft_envelope, "consumption_flags", key) is not True:
            violations.append(f"draft_envelope_missing_consumption_{key}")

    required_draft_true = (
        "draft_is_non_dispatchable",
        "not_mt5_request",
        "not_broker_request",
        "not_order_payload",
        "review_envelope_only",
    )
    for key in required_draft_true:
        if _nested_bool(draft_envelope, "draft_flags", key) is not True:
            violations.append(f"draft_envelope_missing_draft_flag_{key}")

    authority_true = (
        "phase4_approved",
        "broker_request_preview_construction_approved",
        "broker_request_preview_envelope_constructed",
        "broker_request_draft_construction_approved",
        "broker_request_draft_envelope_constructed",
    )
    for key in authority_true:
        if _nested_bool(draft_envelope, "authority_flags", key) is not True:
            violations.append(f"draft_envelope_missing_authority_true_{key}")

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
        if _nested_bool(draft_envelope, "authority_flags", key) is not False:
            violations.append(f"draft_envelope_forbidden_authority_not_false_{key}")

    identity = _nested_mapping(draft_envelope, "identity")
    if not identity.get("preview_idempotency_key_carried_forward"):
        violations.append("draft_envelope_missing_carried_preview_idempotency_key")
    if not identity.get("draft_idempotency_key"):
        violations.append("draft_envelope_missing_draft_idempotency_key")

    return violations


def build_draft_review_human_decision(
    inputs: DraftReviewHumanDecisionInputs,
) -> dict[str, Any]:
    draft_envelope = dict(inputs.draft_envelope)
    violations = _validate_draft_envelope(draft_envelope, inputs.allowed_demo_server)

    return {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "draft_envelope_schema": draft_envelope.get("schema"),
            "draft_envelope_kind": draft_envelope.get("kind"),
            "draft_envelope_status": draft_envelope.get("status"),
            "draft_envelope_decision": draft_envelope.get("decision"),
            "draft_envelope_digest_sha256": stable_json_digest(draft_envelope),
        },
        "approved_scope": {
            "may_review_inert_canonical_broker_request_draft": not violations,
            "may_prepare_mt5_request_shape_design_review": not violations,
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
            "mt5_request_shape_design_review_only": True,
            "no_mt5_request_construction": True,
            "no_order_payload_construction": True,
            "no_metatrader5_import_or_call": True,
            "no_transport_dispatch": True,
            "no_terminal_or_broker_mutation": True,
            "human_approval_required_before_any_inert_mt5_request_preview": True,
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_preview_construction_approved": True,
            "broker_request_preview_envelope_constructed": True,
            "broker_request_draft_construction_approved": True,
            "broker_request_draft_envelope_constructed": True,
            "broker_request_draft_review_approved": not violations,
            "mt5_request_shape_design_review_allowed": not violations,
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