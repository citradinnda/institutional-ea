from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

EXPECTED_SCHEMA = "h024_mt5_request_shape_design_review_packet_v1"
EXPECTED_KIND = "MT5_REQUEST_SHAPE_DESIGN_REVIEW_PACKET"
EXPECTED_STATUS = "READY_FOR_HUMAN_MT5_REQUEST_SHAPE_REVIEW_NO_REQUEST_CONSTRUCTION"
EXPECTED_DECISION = "REQUEST_HUMAN_MT5_REQUEST_SHAPE_REVIEW_NO_MT5_NO_DISPATCH"


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

    design_true = (
        "design_review_only",
        "describes_future_request_shape_constraints",
    )
    for key in design_true:
        if nested_bool(record, "design_scope", key) is not True:
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
        if nested_bool(record, "design_scope", key) is not False:
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
        if nested_bool(record, "future_shape_constraints", key) is not True:
            violations.append(f"future_constraint_missing_true_{key}")

    source = nested_mapping(record, "source_conceptual_draft_summary")
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
            violations.append(f"missing_source_conceptual_field_{key}")

    authority_true = (
        "phase4_approved",
        "broker_request_preview_construction_approved",
        "broker_request_preview_envelope_constructed",
        "broker_request_draft_construction_approved",
        "broker_request_draft_envelope_constructed",
        "broker_request_draft_review_approved",
        "mt5_request_shape_design_review_packet_constructed",
    )
    for key in authority_true:
        if nested_bool(record, "authority_flags", key) is not True:
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

    print(f"H024 MT5 request-shape design review packet records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if not violations else 'FAIL'}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())