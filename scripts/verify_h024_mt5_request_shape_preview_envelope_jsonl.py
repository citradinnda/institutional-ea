from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

EXPECTED_SCHEMA = "h024_mt5_request_shape_preview_envelope_v1"
EXPECTED_KIND = "MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE"
EXPECTED_STATUS = "INERT_MT5_REQUEST_SHAPE_PREVIEW_CONSTRUCTED_NO_REQUEST_NO_DISPATCH"
EXPECTED_DECISION = "CONSTRUCT_INERT_MT5_REQUEST_SHAPE_PREVIEW_ONLY_REFUSE_DISPATCH"


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

    consumption_true = (
        "design_review_packet_consumed",
        "reviewed_draft_summary_consumed",
        "h020_sizing_consumed_not_reinterpreted",
        "kill_switch_allow_state_required",
        "idempotency_key_carried_forward",
    )
    for key in consumption_true:
        if nested_bool(record, "consumption_flags", key) is not True:
            violations.append(f"consumption_missing_true_{key}")

    preview_flags_true = (
        "shape_preview_envelope_constructed",
        "shape_preview_only",
        "not_actual_mt5_request",
        "not_actual_broker_request",
        "not_order_payload",
        "not_dispatchable",
        "contains_no_transport_instruction",
        "contains_no_terminal_mutation_instruction",
    )
    for key in preview_flags_true:
        if nested_bool(record, "shape_preview_flags", key) is not True:
            violations.append(f"shape_preview_flag_missing_true_{key}")

    identity = nested_mapping(record, "identity")
    if not isinstance(identity.get("shape_preview_idempotency_key"), str) or len(identity.get("shape_preview_idempotency_key", "")) != 64:
        violations.append("invalid_shape_preview_idempotency_key")

    preview = nested_mapping(record, "inert_terminal_request_shape_preview")
    if preview.get("field_set_kind") != "INERT_TERMINAL_REQUEST_SHAPE_REVIEW_FIELDS_NOT_SENDABLE":
        violations.append("field_set_kind_mismatch")

    forbidden_markers = nested_mapping(record, "forbidden_sendable_field_names_absent_by_design")
    for key in ("action", "type", "volume", "price", "sl", "tp", "deviation", "magic", "comment", "type_time", "type_filling"):
        if key not in forbidden_markers:
            violations.append(f"missing_forbidden_absent_marker_{key}")

    authority_true = (
        "phase4_approved",
        "broker_request_draft_review_approved",
        "mt5_request_shape_design_review_packet_constructed",
        "mt5_request_shape_construction_approved",
        "mt5_request_shape_preview_envelope_constructed",
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

    print(f"H024 MT5 request-shape preview envelope records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if not violations else 'FAIL'}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())