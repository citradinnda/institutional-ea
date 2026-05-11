from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

EXPECTED_SCHEMA = "h024_broker_request_draft_construction_approval_v1"
EXPECTED_KIND = "BROKER_REQUEST_DRAFT_CONSTRUCTION_APPROVAL"
EXPECTED_STATUS = "BROKER_REQUEST_DRAFT_CONSTRUCTION_APPROVED_NO_DISPATCH_AUTHORITY"
EXPECTED_DECISION = "APPROVE_INERT_BROKER_REQUEST_DRAFT_ONLY_NO_MT5_NO_DISPATCH"


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


def verify_record(record: Mapping[str, Any], allowed_demo_server: str | None, require_approved: bool) -> list[str]:
    violations: list[str] = []

    if record.get("schema") != EXPECTED_SCHEMA:
        violations.append("schema_mismatch")
    if record.get("kind") != EXPECTED_KIND:
        violations.append("kind_mismatch")
    if record.get("status") != EXPECTED_STATUS:
        violations.append("status_mismatch")
    if record.get("decision") != EXPECTED_DECISION:
        violations.append("decision_mismatch")
    if record.get("verdict") != "PASS":
        violations.append("verdict_not_pass")
    if record.get("violations") not in ([], None):
        violations.append("record_contains_violations")
    if allowed_demo_server is not None and record.get("allowed_demo_server") != allowed_demo_server:
        violations.append("allowed_demo_server_mismatch")

    approved_scope_true = (
        "may_construct_inert_canonical_broker_request_draft_envelope",
    )
    for key in approved_scope_true:
        if nested_bool(record, "approved_scope", key) is not True:
            violations.append(f"approved_scope_missing_true_{key}")

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
        if nested_bool(record, "approved_scope", key) is not False:
            violations.append(f"approved_scope_forbidden_not_false_{key}")

    required_constraints = (
        "preview_envelope_must_be_consumed",
        "verified_intent_must_be_consumed",
        "h020_sizing_must_be_consumed_not_reinterpreted",
        "idempotency_key_must_be_carried_forward",
        "kill_switch_allow_state_must_be_required",
        "draft_must_be_non_dispatchable",
        "draft_must_not_be_mt5_request",
        "draft_must_not_be_order_payload",
        "no_metatrader5_import_or_call",
        "no_transport_dispatch",
        "no_terminal_or_broker_mutation",
    )
    for key in required_constraints:
        if nested_bool(record, "required_constraints", key) is not True:
            violations.append(f"required_constraint_missing_true_{key}")

    authority_true = (
        "phase4_approved",
        "broker_request_preview_construction_approved",
        "broker_request_preview_envelope_constructed",
        "broker_request_draft_construction_approved",
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

    if require_approved and nested_bool(record, "approved_scope", "may_construct_inert_canonical_broker_request_draft_envelope") is not True:
        violations.append("required_approval_missing")

    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--allowed-demo-server")
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    records = load_records(args.path)
    violations: list[str] = []

    if len(records) != 1:
        violations.append(f"expected_one_record_found_{len(records)}")
    else:
        violations.extend(verify_record(records[0], args.allowed_demo_server, args.require_approved))

    print(f"H024 broker-request draft construction approval records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if not violations else 'FAIL'}")

    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())