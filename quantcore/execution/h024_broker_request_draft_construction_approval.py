"""H024 inert broker-request draft construction approval.

This module is intentionally pure Python and review-only.  It does not
construct broker requests, MT5 requests, order payloads, or dispatchable
transport messages.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_broker_request_draft_construction_approval_v1"
KIND = "BROKER_REQUEST_DRAFT_CONSTRUCTION_APPROVAL"
STATUS = "BROKER_REQUEST_DRAFT_CONSTRUCTION_APPROVED_NO_DISPATCH_AUTHORITY"
DECISION = "APPROVE_INERT_BROKER_REQUEST_DRAFT_ONLY_NO_MT5_NO_DISPATCH"

REQUIRED_PREVIEW_SCHEMA = "h024_broker_request_preview_envelope_v1"
REQUIRED_PREVIEW_KIND = "BROKER_REQUEST_PREVIEW_ENVELOPE"


@dataclass(frozen=True)
class DraftConstructionApprovalInputs:
    preview_envelope: Mapping[str, Any]
    allowed_demo_server: str


def stable_json_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def _get_bool(record: Mapping[str, Any], *keys: str) -> bool:
    for key in keys:
        value = record.get(key)
        if isinstance(value, bool):
            return value
    return False


def _recursive_values(value: Any, key_name: str) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key) == key_name:
                found.append(child)
            found.extend(_recursive_values(child, key_name))
    elif isinstance(value, list):
        for child in value:
            found.extend(_recursive_values(child, key_name))
    return found


def _require_any_true(record: Mapping[str, Any], key_name: str) -> bool:
    return any(value is True for value in _recursive_values(record, key_name))


def _first_string(record: Mapping[str, Any], *key_names: str) -> str | None:
    for key_name in key_names:
        for value in _recursive_values(record, key_name):
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _validate_preview_envelope(preview_envelope: Mapping[str, Any], allowed_demo_server: str) -> list[str]:
    violations: list[str] = []

    if preview_envelope.get("schema") != REQUIRED_PREVIEW_SCHEMA:
        violations.append("preview_envelope_schema_mismatch")
    if preview_envelope.get("kind") != REQUIRED_PREVIEW_KIND:
        violations.append("preview_envelope_kind_mismatch")

    server = _first_string(preview_envelope, "server", "allowed_demo_server", "broker_server")
    if server is not None and server != allowed_demo_server:
        violations.append("preview_envelope_demo_server_mismatch")

    required_false_keys = (
        "actual_broker_request_constructed",
        "broker_request_constructed",
        "mt5_request_constructed",
        "order_payload_constructed",
        "transport_dispatch_attempted",
        "dispatch_attempted",
        "terminal_mutated",
        "broker_state_mutated",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_approved",
    )
    for key in required_false_keys:
        if any(value is True for value in _recursive_values(preview_envelope, key)):
            violations.append(f"preview_envelope_forbidden_true_{key}")

    required_true_keys = (
        "verified_intent_consumed",
        "h020_sizing_consumed_not_reinterpreted",
        "kill_switch_allow_state_required",
    )
    for key in required_true_keys:
        if not _require_any_true(preview_envelope, key):
            violations.append(f"preview_envelope_missing_true_{key}")

    preview_idempotency_key = _first_string(
        preview_envelope,
        "preview_idempotency_key",
        "idempotency_key",
        "stable_preview_idempotency_key",
    )
    if preview_idempotency_key is None:
        violations.append("preview_envelope_missing_idempotency_key")

    if not _require_any_true(preview_envelope, "not_mt5_request"):
        violations.append("preview_envelope_missing_not_mt5_request")
    if not _require_any_true(preview_envelope, "not_order_payload"):
        violations.append("preview_envelope_missing_not_order_payload")

    return violations


def build_draft_construction_approval(
    inputs: DraftConstructionApprovalInputs,
) -> dict[str, Any]:
    preview_envelope = dict(inputs.preview_envelope)
    violations = _validate_preview_envelope(preview_envelope, inputs.allowed_demo_server)

    approval = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "preview_envelope_schema": preview_envelope.get("schema"),
            "preview_envelope_kind": preview_envelope.get("kind"),
            "preview_envelope_status": preview_envelope.get("status"),
            "preview_envelope_decision": preview_envelope.get("decision"),
            "preview_envelope_digest_sha256": stable_json_digest(preview_envelope),
        },
        "approved_scope": {
            "may_construct_inert_canonical_broker_request_draft_envelope": not violations,
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
        "required_constraints": {
            "preview_envelope_must_be_consumed": True,
            "verified_intent_must_be_consumed": True,
            "h020_sizing_must_be_consumed_not_reinterpreted": True,
            "idempotency_key_must_be_carried_forward": True,
            "kill_switch_allow_state_must_be_required": True,
            "draft_must_be_non_dispatchable": True,
            "draft_must_not_be_mt5_request": True,
            "draft_must_not_be_order_payload": True,
            "no_metatrader5_import_or_call": True,
            "no_transport_dispatch": True,
            "no_terminal_or_broker_mutation": True,
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_preview_construction_approved": True,
            "broker_request_preview_envelope_constructed": True,
            "broker_request_draft_construction_approved": not violations,
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
    return approval


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