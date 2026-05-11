"""H024 inert canonical broker-request draft envelope.

This is a review envelope.  It is not an MT5 request, not an order payload,
not a broker request, and not dispatchable.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "h024_broker_request_draft_envelope_v1"
KIND = "BROKER_REQUEST_DRAFT_ENVELOPE"
STATUS = "INERT_BROKER_REQUEST_DRAFT_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH"
DECISION = "CONSTRUCT_INERT_BROKER_REQUEST_DRAFT_ONLY_REFUSE_DISPATCH"

APPROVAL_SCHEMA = "h024_broker_request_draft_construction_approval_v1"
PREVIEW_SCHEMA = "h024_broker_request_preview_envelope_v1"


@dataclass(frozen=True)
class DraftEnvelopeInputs:
    draft_construction_approval: Mapping[str, Any]
    preview_envelope: Mapping[str, Any]
    allowed_demo_server: str


def stable_json_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


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


def _first_string(record: Mapping[str, Any], *key_names: str) -> str | None:
    for key_name in key_names:
        for value in _recursive_values(record, key_name):
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _first_number(record: Mapping[str, Any], *key_names: str) -> float | None:
    for key_name in key_names:
        for value in _recursive_values(record, key_name):
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                try:
                    return float(value)
                except ValueError:
                    continue
    return None


def _any_true(record: Mapping[str, Any], key_name: str) -> bool:
    return any(value is True for value in _recursive_values(record, key_name))


def _any_forbidden_true(record: Mapping[str, Any], key_name: str) -> bool:
    return any(value is True for value in _recursive_values(record, key_name))


def _nested_bool(record: Mapping[str, Any], section: str, key: str) -> bool | None:
    value = record.get(section)
    if isinstance(value, Mapping):
        nested = value.get(key)
        if isinstance(nested, bool):
            return nested
    return None


def _canonical_side(value: str | None) -> str | None:
    if value is None:
        return None
    lowered = value.lower()
    if lowered in {"buy", "long"}:
        return "buy_review_only"
    if lowered in {"sell", "short"}:
        return "sell_review_only"
    return f"{lowered}_review_only"


def _build_conceptual_fields(preview_envelope: Mapping[str, Any]) -> dict[str, Any]:
    normalized_symbol = _first_string(preview_envelope, "normalized_symbol", "model_symbol")
    runtime_symbol = _first_string(preview_envelope, "runtime_symbol", "broker_symbol", "symbol")
    side = _canonical_side(_first_string(preview_envelope, "side", "direction", "order_side"))
    lots = _first_number(preview_envelope, "final_lots", "lots", "volume_lots")
    entry_reference = _first_number(preview_envelope, "entry", "entry_price", "reference_entry")
    protective_stop_reference = _first_number(preview_envelope, "stop", "stop_price", "protective_stop")
    risk_fraction = _first_number(preview_envelope, "risk_fraction", "final_signed_risk_fraction")
    source_closed_h4_time = _first_string(preview_envelope, "closed_h4_time", "source_closed_h4_time")

    return {
        "field_set_kind": "CANONICAL_CONCEPTUAL_REVIEW_FIELDS_NOT_EXECUTABLE_REQUEST",
        "normalized_symbol": normalized_symbol,
        "runtime_symbol": runtime_symbol,
        "conceptual_side": side,
        "h020_final_lots": lots,
        "entry_reference_price": entry_reference,
        "protective_stop_reference_price": protective_stop_reference,
        "risk_fraction_reference": risk_fraction,
        "source_closed_h4_time": source_closed_h4_time,
        "timeframe": _first_string(preview_envelope, "timeframe") or "H4",
        "sizing_source": "H020_CONSUMED_NOT_REINTERPRETED",
        "execution_shape": "NOT_MT5_REQUEST_NOT_ORDER_PAYLOAD_NOT_DISPATCHABLE",
    }


def _validate_inputs(
    approval: Mapping[str, Any],
    preview_envelope: Mapping[str, Any],
    allowed_demo_server: str,
) -> list[str]:
    violations: list[str] = []

    if approval.get("schema") != APPROVAL_SCHEMA:
        violations.append("draft_construction_approval_schema_mismatch")
    if approval.get("verdict") != "PASS":
        violations.append("draft_construction_approval_not_pass")
    if _nested_bool(approval, "approved_scope", "may_construct_inert_canonical_broker_request_draft_envelope") is not True:
        violations.append("draft_construction_not_approved")

    if preview_envelope.get("schema") != PREVIEW_SCHEMA:
        violations.append("preview_envelope_schema_mismatch")

    server = _first_string(preview_envelope, "server", "allowed_demo_server", "broker_server")
    if server is not None and server != allowed_demo_server:
        violations.append("preview_envelope_demo_server_mismatch")

    for key in (
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
    ):
        if _any_forbidden_true(preview_envelope, key):
            violations.append(f"preview_envelope_forbidden_true_{key}")

    for key in (
        "verified_intent_consumed",
        "h020_sizing_consumed_not_reinterpreted",
        "kill_switch_allow_state_required",
    ):
        if not _any_true(preview_envelope, key):
            violations.append(f"preview_envelope_missing_true_{key}")

    if not _any_true(preview_envelope, "not_mt5_request"):
        violations.append("preview_envelope_missing_not_mt5_request")
    if not _any_true(preview_envelope, "not_order_payload"):
        violations.append("preview_envelope_missing_not_order_payload")

    if _first_string(preview_envelope, "preview_idempotency_key", "idempotency_key", "stable_preview_idempotency_key") is None:
        violations.append("missing_preview_idempotency_key")

    return violations


def build_draft_envelope(inputs: DraftEnvelopeInputs) -> dict[str, Any]:
    approval = dict(inputs.draft_construction_approval)
    preview_envelope = dict(inputs.preview_envelope)
    violations = _validate_inputs(approval, preview_envelope, inputs.allowed_demo_server)

    preview_idempotency_key = _first_string(
        preview_envelope,
        "preview_idempotency_key",
        "idempotency_key",
        "stable_preview_idempotency_key",
    )

    conceptual_fields = _build_conceptual_fields(preview_envelope)
    required_conceptual_fields = (
        "normalized_symbol",
        "runtime_symbol",
        "conceptual_side",
        "h020_final_lots",
        "entry_reference_price",
        "protective_stop_reference_price",
    )
    for key in required_conceptual_fields:
        if conceptual_fields.get(key) is None:
            violations.append(f"missing_conceptual_field_{key}")

    draft_id_source = {
        "preview_digest": stable_json_digest(preview_envelope),
        "preview_idempotency_key": preview_idempotency_key,
        "draft_schema": SCHEMA,
    }
    draft_idempotency_key = sha256(
        json.dumps(draft_id_source, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    record = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": inputs.allowed_demo_server,
        "upstream": {
            "draft_construction_approval_schema": approval.get("schema"),
            "draft_construction_approval_kind": approval.get("kind"),
            "draft_construction_approval_digest_sha256": stable_json_digest(approval),
            "preview_envelope_schema": preview_envelope.get("schema"),
            "preview_envelope_kind": preview_envelope.get("kind"),
            "preview_envelope_digest_sha256": stable_json_digest(preview_envelope),
        },
        "identity": {
            "preview_idempotency_key_carried_forward": preview_idempotency_key,
            "draft_idempotency_key": draft_idempotency_key,
            "idempotency_key_carried_forward": preview_idempotency_key is not None,
        },
        "consumption_flags": {
            "preview_envelope_consumed": True,
            "verified_intent_consumed": True,
            "h020_sizing_consumed_not_reinterpreted": True,
            "kill_switch_allow_state_required": True,
            "idempotency_key_carried_forward": preview_idempotency_key is not None,
        },
        "draft_flags": {
            "draft_is_non_dispatchable": True,
            "not_mt5_request": True,
            "not_broker_request": True,
            "not_order_payload": True,
            "review_envelope_only": True,
            "contains_no_transport_instruction": True,
            "contains_no_terminal_mutation_instruction": True,
        },
        "canonical_conceptual_review_fields": conceptual_fields,
        "forbidden_execution_fields_absent_by_design": {
            "action": "absent_to_avoid_mql_trade_request_shape",
            "type": "absent_to_avoid_mql_trade_request_shape",
            "volume": "absent_to_avoid_mql_trade_request_shape",
            "price": "absent_to_avoid_mql_trade_request_shape",
            "sl": "absent_to_avoid_mql_trade_request_shape",
            "tp": "absent_to_avoid_mql_trade_request_shape",
            "deviation": "absent_to_avoid_mql_trade_request_shape",
            "magic": "absent_to_avoid_mql_trade_request_shape",
            "comment": "absent_to_avoid_mql_trade_request_shape",
            "type_time": "absent_to_avoid_mql_trade_request_shape",
            "type_filling": "absent_to_avoid_mql_trade_request_shape",
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_preview_construction_approved": True,
            "broker_request_preview_envelope_constructed": True,
            "broker_request_draft_construction_approved": not violations,
            "broker_request_draft_envelope_constructed": not violations,
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