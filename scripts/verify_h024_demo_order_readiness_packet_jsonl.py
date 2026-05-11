from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

EXPECTED_SCHEMA = "h024_demo_order_readiness_packet_v1"
EXPECTED_KIND = "DEMO_ORDER_READINESS_PACKET_REVIEW_ONLY"
EXPECTED_STATUS = "READY_FOR_HUMAN_DEMO_ORDER_CANARY_REVIEW_NO_ORDER_AUTHORITY"
EXPECTED_DECISION = "REQUEST_HUMAN_DEMO_ORDER_CANARY_REVIEW_NO_ORDER_PLACEMENT_AUTHORITY"


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

    readiness_true = (
        "packet_is_review_only",
        "requests_human_demo_order_canary_review",
    )
    for key in readiness_true:
        if nested_bool(record, "readiness_scope", key) is not True:
            violations.append(f"readiness_scope_missing_true_{key}")

    readiness_false = (
        "approves_demo_order_canary",
        "approves_demo_order_placement",
        "approves_live_order_placement",
        "constructs_actual_broker_request",
        "constructs_mt5_request",
        "constructs_order_payload",
        "dispatches_transport",
        "mutates_terminal_or_broker_state",
        "approves_execution",
    )
    for key in readiness_false:
        if nested_bool(record, "readiness_scope", key) is not False:
            violations.append(f"readiness_scope_forbidden_not_false_{key}")

    required_controls = (
        "separate_explicit_human_canary_approval_required",
        "allowed_demo_server_lock_required",
        "symbol_lock_required",
        "kill_switch_allow_state_required",
        "idempotency_ledger_required",
        "max_lot_cap_required",
        "single_canary_order_limit_required",
        "post_order_audit_required_if_later_approved",
        "live_order_placement_remains_forbidden",
    )
    for key in required_controls:
        if nested_bool(record, "required_canary_controls_for_later_approval", key) is not True:
            violations.append(f"required_canary_control_missing_true_{key}")

    authority_true = (
        "phase4_approved",
        "mt5_request_shape_preview_review_approved",
        "demo_order_readiness_packet_constructed",
        "demo_order_canary_review_requested",
    )
    for key in authority_true:
        if nested_bool(record, "authority_flags", key) is not True:
            violations.append(f"authority_missing_true_{key}")

    authority_false = (
        "demo_order_canary_approved",
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

    print(f"H024 demo-order readiness packet records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if not violations else 'FAIL'}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())