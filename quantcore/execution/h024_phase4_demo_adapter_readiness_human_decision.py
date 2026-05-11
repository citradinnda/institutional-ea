from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "h024_phase4_demo_adapter_readiness_human_decision_v1"
KIND = "PHASE4_DEMO_ADAPTER_READINESS_HUMAN_DECISION"
STATUS = "ADAPTER_READINESS_REVIEW_APPROVED_NO_EXECUTION_AUTHORITY"
DECISION = "APPROVE_ADAPTER_READINESS_REVIEW_NO_EXECUTION"

READINESS_PACKET_SCHEMA = "h024_phase4_demo_adapter_readiness_packet_v1"
READINESS_PACKET_KIND = "PHASE4_DEMO_ADAPTER_READINESS_PACKET_REVIEW_ONLY"
READINESS_PACKET_STATUS = "READY_FOR_HUMAN_ADAPTER_READINESS_REVIEW_NO_EXECUTION"
READINESS_PACKET_DECISION = "REVIEW_ONLY_NO_EXECUTION_AUTHORITY"

FALSE_AUTHORITY_FLAGS = (
    "execution_adapter_use_approved",
    "execution_adapter_approved",
    "broker_request_approved",
    "mt5_execution_approved",
    "terminal_mutation_approved",
    "demo_order_placement_approved",
    "live_order_placement_approved",
    "execution_approved",
)

FALSE_MUTATION_FLAGS = (
    "broker_request_constructed",
    "mt5_request_constructed",
    "order_payload_constructed",
    "dispatch_attempted",
    "terminal_mutated",
    "broker_state_mutated",
)

REQUIRED_TRUE_PACKET_FLAGS = (
    "phase4_approved",
    "demo_execution_adapter_implementation_approved",
    "execution_adapter_implementation_approved",
    "fail_closed_skeleton_verified",
    "real_intent_refusal_audit_verified",
    "adapter_boundary_static_verified",
    "execution_authority_remains_absent",
    "readiness_packet_ready",
)

REQUIRED_REFUSAL_REASONS = (
    "execution_adapter_use_not_approved",
    "demo_order_placement_not_approved",
    "execution_not_approved",
)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(p.read_text(encoding="utf-8-sig").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{p}:{line_number}: invalid JSONL: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{p}:{line_number}: expected JSON object, got {type(value).__name__}")
        records.append(value)
    return records


def write_jsonl(path: str | Path, records: Sequence[Mapping[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "allow", "allowed", "approved", "pass"}
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value == 1
    return False


def _walk_values_by_key(value: Any, key: str) -> Iterable[Any]:
    if isinstance(value, Mapping):
        for current_key, current_value in value.items():
            if current_key == key:
                yield current_value
            yield from _walk_values_by_key(current_value, key)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_values_by_key(item, key)


def _any_truthy(records: Iterable[Mapping[str, Any]], key: str) -> bool:
    return any(_truthy(value) for record in records for value in _walk_values_by_key(record, key))


def _coerce_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            if isinstance(item, str):
                result.append(item)
            elif item is not None:
                result.append(str(item))
        return result
    return [str(value)]


def _server_values(record: Mapping[str, Any]) -> list[str]:
    values: set[str] = set()

    for key in ("server", "account_server", "broker_server", "mt5_server"):
        for value in _walk_values_by_key(record, key):
            if isinstance(value, str) and value:
                values.add(value)

    for value in _walk_values_by_key(record, "server_values"):
        if isinstance(value, str) and value:
            values.add(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item:
                    values.add(item)

    return sorted(values)


def _source_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        key: record.get(key)
        for key in ("schema", "kind", "status", "decision", "verdict")
        if key in record
    }
    servers = _server_values(record)
    if servers:
        summary["server_values"] = servers
    return summary


def _validate_readiness_packet(packet: Mapping[str, Any]) -> list[str]:
    violations: list[str] = []

    expected = {
        "schema": READINESS_PACKET_SCHEMA,
        "kind": READINESS_PACKET_KIND,
        "status": READINESS_PACKET_STATUS,
        "decision": READINESS_PACKET_DECISION,
        "verdict": "PASS",
    }
    for key, expected_value in expected.items():
        if packet.get(key) != expected_value:
            violations.append(f"readiness_packet_{key}_mismatch")

    for key in REQUIRED_TRUE_PACKET_FLAGS:
        if packet.get(key) is not True:
            violations.append(f"readiness_packet_{key}_not_true")

    for key in FALSE_AUTHORITY_FLAGS + FALSE_MUTATION_FLAGS:
        if packet.get(key) is not False:
            violations.append(f"readiness_packet_{key}_not_false")

    if packet.get("upstream_artifact_count") != 3:
        violations.append("readiness_packet_upstream_artifact_count_mismatch")

    refusal_reasons = set(_coerce_str_list(packet.get("refusal_reasons")))
    for reason in REQUIRED_REFUSAL_REASONS:
        if reason not in refusal_reasons:
            violations.append(f"readiness_packet_missing_refusal_reason:{reason}")

    if packet.get("violations"):
        violations.append("readiness_packet_builder_violations_present")

    return violations


def build_human_decision_record(
    readiness_packet_record: Mapping[str, Any],
    *,
    decision: str = DECISION,
    decided_by: str = "human_operator",
    source_path: str | None = None,
) -> dict[str, Any]:
    violations = _validate_readiness_packet(readiness_packet_record)

    if decision != DECISION:
        violations.append("unsupported_decision_for_adapter_readiness_human_gate")
    if not decided_by:
        violations.append("decided_by_missing")

    record: dict[str, Any] = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": decision,
        "decided_by": decided_by,
        "source_summary": _source_summary(readiness_packet_record),
        "phase4_approved": readiness_packet_record.get("phase4_approved") is True,
        "demo_execution_adapter_implementation_approved": readiness_packet_record.get(
            "demo_execution_adapter_implementation_approved"
        )
        is True,
        "execution_adapter_implementation_approved": readiness_packet_record.get(
            "execution_adapter_implementation_approved"
        )
        is True,
        "adapter_readiness_review_approved": decision == DECISION and not violations,
        "execution_adapter_use_approved": False,
        "execution_adapter_approved": False,
        "broker_request_approved": False,
        "mt5_execution_approved": False,
        "terminal_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "broker_request_constructed": False,
        "mt5_request_constructed": False,
        "order_payload_constructed": False,
        "dispatch_attempted": False,
        "terminal_mutated": False,
        "broker_state_mutated": False,
        "approval_scope": "adapter_readiness_review_only_no_execution_authority",
        "explicit_non_authorizations": {
            "adapter_use": False,
            "broker_request_construction": False,
            "mt5_execution": False,
            "terminal_mutation": False,
            "demo_order_placement": False,
            "live_order_placement": False,
            "execution": False,
        },
        "violations": violations,
    }

    if source_path:
        record["source_path"] = source_path

    record["verdict"] = "PASS" if not violations else "FAIL"
    return record


def build_human_decision_records(
    readiness_packet_records: Sequence[dict[str, Any]],
    *,
    decision: str = DECISION,
    decided_by: str = "human_operator",
    source_path: str | None = None,
) -> list[dict[str, Any]]:
    violations: list[str] = []
    if not readiness_packet_records:
        readiness_packet_record: dict[str, Any] = {}
        violations.append("readiness_packet_missing")
    else:
        readiness_packet_record = readiness_packet_records[0]
        if len(readiness_packet_records) != 1:
            violations.append(f"readiness_packet_expected_one_record_got_{len(readiness_packet_records)}")

    record = build_human_decision_record(
        readiness_packet_record,
        decision=decision,
        decided_by=decided_by,
        source_path=source_path,
    )
    if violations:
        record["violations"] = sorted(set(record["violations"] + violations))
        record["adapter_readiness_review_approved"] = False
        record["verdict"] = "FAIL"
    return [record]


def build_human_decision_records_from_file(
    readiness_packet_jsonl: str | Path,
    *,
    decision: str = DECISION,
    decided_by: str = "human_operator",
) -> list[dict[str, Any]]:
    return build_human_decision_records(
        read_jsonl(readiness_packet_jsonl),
        decision=decision,
        decided_by=decided_by,
        source_path=str(readiness_packet_jsonl),
    )


def verify_human_decision_records(
    records: Sequence[Mapping[str, Any]],
    *,
    allowed_demo_server: str | None = None,
    require_approved: bool = True,
) -> list[str]:
    violations: list[str] = []

    if not records:
        return ["no_records"]
    if len(records) != 1:
        violations.append(f"expected_one_record_got_{len(records)}")

    for index, record in enumerate(records):
        prefix = f"record_{index}"

        expected = {
            "schema": SCHEMA,
            "kind": KIND,
            "status": STATUS,
            "decision": DECISION,
        }
        if require_approved:
            expected["verdict"] = "PASS"

        for key, expected_value in expected.items():
            if record.get(key) != expected_value:
                violations.append(f"{prefix}_{key}_mismatch")

        for key in (
            "phase4_approved",
            "demo_execution_adapter_implementation_approved",
            "execution_adapter_implementation_approved",
            "adapter_readiness_review_approved",
        ):
            if record.get(key) is not True:
                violations.append(f"{prefix}_{key}_not_true")

        for key in FALSE_AUTHORITY_FLAGS + FALSE_MUTATION_FLAGS:
            if record.get(key) is not False:
                violations.append(f"{prefix}_{key}_not_false")

        explicit_non_authorizations = record.get("explicit_non_authorizations")
        if not isinstance(explicit_non_authorizations, Mapping):
            violations.append(f"{prefix}_explicit_non_authorizations_missing")
        else:
            for key, value in explicit_non_authorizations.items():
                if value is not False:
                    violations.append(f"{prefix}_explicit_non_authorization_{key}_not_false")

        if record.get("approval_scope") != "adapter_readiness_review_only_no_execution_authority":
            violations.append(f"{prefix}_approval_scope_mismatch")

        if record.get("violations"):
            violations.append(f"{prefix}_builder_violations_present")

        source_summary = record.get("source_summary")
        if not isinstance(source_summary, Mapping):
            violations.append(f"{prefix}_source_summary_missing")
        else:
            if source_summary.get("schema") != READINESS_PACKET_SCHEMA:
                violations.append(f"{prefix}_source_summary_schema_mismatch")
            if source_summary.get("kind") != READINESS_PACKET_KIND:
                violations.append(f"{prefix}_source_summary_kind_mismatch")
            if source_summary.get("status") != READINESS_PACKET_STATUS:
                violations.append(f"{prefix}_source_summary_status_mismatch")
            if source_summary.get("decision") != READINESS_PACKET_DECISION:
                violations.append(f"{prefix}_source_summary_decision_mismatch")
            if source_summary.get("verdict") != "PASS":
                violations.append(f"{prefix}_source_summary_verdict_not_pass")

        if allowed_demo_server:
            observed_servers = _server_values(record)
            if observed_servers and allowed_demo_server not in observed_servers:
                violations.append(
                    f"{prefix}_allowed_demo_server_mismatch:"
                    f"expected={allowed_demo_server};observed={','.join(observed_servers)}"
                )

    return violations


def format_verification_summary(records: Sequence[Mapping[str, Any]], violations: Sequence[str]) -> str:
    lines = [
        f"H024 Phase 4 demo adapter readiness human decision records: {len(records)}",
        f"Violations: {len(violations)}",
    ]
    if violations:
        lines.extend(f"- {violation}" for violation in violations)
    lines.append(f"Verdict: {'PASS' if not violations else 'FAIL'}")
    return "\n".join(lines)