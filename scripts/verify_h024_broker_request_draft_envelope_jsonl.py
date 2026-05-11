from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

EXPECTED_SCHEMA = "h024_broker_request_draft_envelope_v1"
EXPECTED_KIND = "BROKER_REQUEST_DRAFT_ENVELOPE"
EXPECTED_STATUS = "INERT_BROKER_REQUEST_DRAFT_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH"
EXPECTED_DECISION = "CONSTRUCT_INERT_BROKER_REQUEST_DRAFT_ONLY_REFUSE_DISPATCH"


def load_records(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def nested_bool(record: Mapping[str, Any], section: str, key: str) -> bool | None:
    value = record.get(section)
    if isinstance(value, Mapping):
        nested = value.get(key)
        if isinstance(nested, bool):
            return nested
    return None


def nested_mapping(record: Mapping[str, Any], section: str) -> Mapping[str, Any]:
    value = record.get(section)
    return value if isinstance(value, Mapping) else {}


def verify_record(record: Mapping[str, Any], allowed_demo_server: str | None, require_pass: bool) -> list[str]:
    violations: list[str] = []

    if record.get("schema") != EXPECTED_SCHEMA:
        violations.append("schema_mismatch")
    if record.get("kind") != EXPECTED_KIND:
        violations.append("kind_mismatch")
    if record.get("status") != EXPECTED_STATUS:
        violations.append("status_mismatch")
    if record.get("decision") != EXPECTED_DECISION:
        violations.append("decision_mismatch")
    if require_pass and record.get("verdict") != "PASS":
        violations.append("verdict_not_pass")
    if record.get("violations") not in ([], None):
        violations.append("record_contains_violations")
    if allowed_demo_server is not None and record.get("allowed_demo_server") != allowed_demo_server:
        violations.append("allowed_demo_server_mismatch")

    required_consumption_true = (
        "preview_envelope_consumed",
        "verified_intent_consumed",
        "h020_sizing_consumed_not_reinterpreted",
        "kill_switch_allow_state_required",
        "idempotency_key_carried_forward",
    )
    for key in required_consumption_true:
        if nested_bool(record, "consumption_flags", key) is not True:
            violations.append(f"consumption_missing_true_{key}")

    required_draft_true = (
        "draft_is_non_dispatchable",
        "not_mt5_request",
        "not_broker_request",
        "not_order_payload",
        "review_envelope_only",
        "contains_no_transport_instruction",
        "contains_no_terminal_mutation_instruction",
    )
    for key in required_draft_true:
        if nested_bool(record, "draft_flags", key) is not True:
            violations.append(f"draft_flag_missing_true_{key}")

    identity = nested_mapping(record, "identity")
    if not isinstance(identity.get("preview_idempotency_key_carried_forward"), str) or not identity.get("preview_idempotency_key_carried_forward"):
        violations.append("missing_preview_idempotency_key_carried_forward")
    if not isinstance(identity.get("draft_idempotency_key"), str) or len(identity.get("draft_idempotency_key", "")) != 64:
        violations.append("invalid_draft_idempotency_key")

    conceptual = nested_mapping(record, "canonical_conceptual_review_fields")
    for key in (
        "field_set_kind",
        "normalized_symbol",
        "runtime_symbol",
        "conceptual_side",
        "h020_final_lots",
        "entry_reference_price",
        "protective_stop_reference_price",
        "sizing_source",
        "execution_shape",
    ):
        if conceptual.get(key) in (None, ""):
            violations.append(f"missing_conceptual_field_{key}")
    if conceptual.get("field_set_kind") != "CANONICAL_CONCEPTUAL_REVIEW_FIELDS_NOT_EXECUTABLE_REQUEST":
        violations.append("conceptual_field_set_kind_mismatch")
    if conceptual.get("sizing_source") != "H020_CONSUMED_NOT_REINTERPRETED":
        violations.append("sizing_source_mismatch")
    if conceptual.get("execution_shape") != "NOT_MT5_REQUEST_NOT_ORDER_PAYLOAD_NOT_DISPATCHABLE":
        violations.append("execution_shape_mismatch")

    forbidden_execution_fields_absent = nested_mapping(record, "forbidden_execution_fields_absent_by_design")
    for key in ("action", "type", "volume", "price", "sl", "tp", "deviation", "magic", "comment", "type_time", "type_filling"):
        if key not in forbidden_execution_fields_absent:
            violations.append(f"missing_forbidden_absent_marker_{key}")

    authority_true = (
        "phase4_approved",
        "broker_request_preview_construction_approved",
        "broker_request_preview_envelope_constructed",
        "broker_request_draft_construction_approved",
        "broker_request_draft_envelope_constructed",
    )
    for key in authority_true:
        if nested_bool(record, "authority_flags", key) is not True:
            violations.append(f"authority_missing_true_{key}")

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
        if nested_bool(record, "authority_flags", key) is not False:
            violations.append(f"authority_forbidden_not_false_{key}")

    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--allowed-demo-server")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    records = load_records(args.path)
    violations: list[str] = []

    if len(records) != 1:
        violations.append(f"expected_one_record_found_{len(records)}")
    else:
        violations.extend(verify_record(records[0], args.allowed_demo_server, args.require_pass))

    print(f"H024 broker-request draft envelope records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if not violations else 'FAIL'}")

    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())