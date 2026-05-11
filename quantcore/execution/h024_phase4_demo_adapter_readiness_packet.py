from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "h024_phase4_demo_adapter_readiness_packet_v1"
KIND = "PHASE4_DEMO_ADAPTER_READINESS_PACKET_REVIEW_ONLY"
STATUS = "READY_FOR_HUMAN_ADAPTER_READINESS_REVIEW_NO_EXECUTION"
DECISION = "REVIEW_ONLY_NO_EXECUTION_AUTHORITY"

SKELETON_SCHEMA = "h024_demo_execution_adapter_skeleton_v1"
SKELETON_KIND = "DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED"
SKELETON_STATUS = "DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED"

INTENT_REFUSAL_SCHEMA = "h024_demo_adapter_intent_refusal_audit_v1"
INTENT_REFUSAL_KIND = "DEMO_ADAPTER_INTENT_REFUSAL_AUDIT"
INTENT_REFUSAL_STATUS = "ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY"

BOUNDARY_STATIC_SCHEMA = "h024_demo_adapter_boundary_static_verifier_v1"
BOUNDARY_STATIC_KIND = "DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER"
BOUNDARY_STATIC_STATUS = "ADAPTER_IMPLEMENTATION_BOUNDARY_STATIC_VERIFIED"
BOUNDARY_STATIC_DECISION = "ALLOW_IMPLEMENTATION_SURFACE_REVIEW_ONLY_NO_EXECUTION"

REFUSAL_DECISION = "REFUSE_DISPATCH_NO_ORDER_AUTHORITY"

REQUIRED_REFUSAL_REASONS = (
    "execution_adapter_use_not_approved",
    "demo_order_placement_not_approved",
    "execution_not_approved",
)

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

SOURCE_EXPECTATIONS = {
    "demo_execution_adapter_skeleton": {
        "schema": SKELETON_SCHEMA,
        "kind": SKELETON_KIND,
        "status": SKELETON_STATUS,
        "decision": REFUSAL_DECISION,
    },
    "demo_adapter_intent_refusal_audit": {
        "schema": INTENT_REFUSAL_SCHEMA,
        "kind": INTENT_REFUSAL_KIND,
        "status": INTENT_REFUSAL_STATUS,
        "decision": REFUSAL_DECISION,
    },
    "demo_adapter_boundary_static_verifier": {
        "schema": BOUNDARY_STATIC_SCHEMA,
        "kind": BOUNDARY_STATIC_KIND,
        "status": BOUNDARY_STATIC_STATUS,
        "decision": BOUNDARY_STATIC_DECISION,
    },
}


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
        return value.strip().lower() in {"1", "true", "yes", "y", "allow", "allowed", "pass"}
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


def _collect_reasons(record: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    for key in ("refusal_reasons", "blocked_reasons", "reasons"):
        for value in _walk_values_by_key(record, key):
            reasons.extend(_coerce_str_list(value))
    return sorted(set(reasons))


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


def _first_record(records: Sequence[dict[str, Any]], source_name: str, violations: list[str]) -> dict[str, Any]:
    if not records:
        violations.append(f"{source_name}_missing")
        return {}
    if len(records) != 1:
        violations.append(f"{source_name}_expected_one_record_got_{len(records)}")
    return records[0]


def _source_record_passed(record: Mapping[str, Any]) -> bool:
    verdict = record.get("verdict")
    return (verdict is None or verdict == "PASS") and not record.get("violations")


def _source_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        key: record.get(key)
        for key in ("schema", "kind", "status", "decision", "verdict")
        if key in record
    }
    if "verdict" not in summary and not record.get("violations"):
        summary["verdict"] = "PASS"

    server_values = _server_values(record)
    if server_values:
        summary["server_values"] = server_values

    return summary


def _validate_source_record(
    *,
    source_name: str,
    record: Mapping[str, Any],
    violations: list[str],
) -> None:
    expectations = SOURCE_EXPECTATIONS[source_name]
    for key, expected_value in expectations.items():
        if record.get(key) != expected_value:
            violations.append(f"{source_name}_{key}_mismatch")

    verdict = record.get("verdict")
    if verdict is not None and verdict != "PASS":
        violations.append(f"{source_name}_verdict_not_pass")

    builder_violations = record.get("violations")
    if builder_violations:
        violations.append(f"{source_name}_builder_violations_present")

    for flag in FALSE_AUTHORITY_FLAGS:
        if _any_truthy([record], flag):
            violations.append(f"{source_name}_{flag}_unexpectedly_true")

    for flag in FALSE_MUTATION_FLAGS:
        if _any_truthy([record], flag):
            violations.append(f"{source_name}_{flag}_unexpectedly_true")


def build_readiness_packet_record(
    *,
    skeleton_record: Mapping[str, Any],
    intent_refusal_record: Mapping[str, Any],
    boundary_static_record: Mapping[str, Any],
    source_paths: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    source_records = [skeleton_record, intent_refusal_record, boundary_static_record]
    violations: list[str] = []

    _validate_source_record(
        source_name="demo_execution_adapter_skeleton",
        record=skeleton_record,
        violations=violations,
    )
    _validate_source_record(
        source_name="demo_adapter_intent_refusal_audit",
        record=intent_refusal_record,
        violations=violations,
    )
    _validate_source_record(
        source_name="demo_adapter_boundary_static_verifier",
        record=boundary_static_record,
        violations=violations,
    )

    skeleton_reasons = set(_collect_reasons(skeleton_record))
    intent_reasons = set(_collect_reasons(intent_refusal_record))
    for reason in REQUIRED_REFUSAL_REASONS:
        if reason not in skeleton_reasons:
            violations.append(f"demo_execution_adapter_skeleton_missing_refusal_reason:{reason}")
        if reason not in intent_reasons:
            violations.append(f"demo_adapter_intent_refusal_audit_missing_refusal_reason:{reason}")

    if intent_refusal_record.get("adapter_intent_ingested") is not True:
        violations.append("demo_adapter_intent_refusal_audit_adapter_intent_ingested_not_true")
    if intent_refusal_record.get("intent_envelope_constructed") is not True:
        violations.append("demo_adapter_intent_refusal_audit_intent_envelope_constructed_not_true")

    if boundary_static_record.get("adapter_boundary_static_verified") is not True:
        violations.append("demo_adapter_boundary_static_verifier_adapter_boundary_static_verified_not_true")
    if boundary_static_record.get("prohibited_finding_count") != 0:
        violations.append("demo_adapter_boundary_static_verifier_prohibited_finding_count_nonzero")
    target_count = boundary_static_record.get("target_count")
    if not isinstance(target_count, int) or target_count <= 0:
        violations.append("demo_adapter_boundary_static_verifier_target_count_invalid")

    phase4_approved = _any_truthy(source_records, "phase4_approved")
    demo_impl_approved = _any_truthy(
        source_records, "demo_execution_adapter_implementation_approved"
    ) or _any_truthy(source_records, "execution_adapter_implementation_approved")
    adapter_impl_approved = _any_truthy(source_records, "execution_adapter_implementation_approved") or demo_impl_approved

    if not phase4_approved:
        violations.append("phase4_not_approved")
    if not demo_impl_approved:
        violations.append("demo_execution_adapter_implementation_not_approved")
    if not adapter_impl_approved:
        violations.append("execution_adapter_implementation_not_approved")

    fail_closed_skeleton_verified = _source_record_passed(skeleton_record)
    real_intent_refusal_audit_verified = _source_record_passed(intent_refusal_record)
    adapter_boundary_static_verified = (
        _source_record_passed(boundary_static_record)
        and boundary_static_record.get("adapter_boundary_static_verified") is True
        and boundary_static_record.get("prohibited_finding_count") == 0
    )

    record: dict[str, Any] = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "source_summaries": {
            "demo_execution_adapter_skeleton": _source_summary(skeleton_record),
            "demo_adapter_intent_refusal_audit": _source_summary(intent_refusal_record),
            "demo_adapter_boundary_static_verifier": _source_summary(boundary_static_record),
        },
        "upstream_artifact_count": 3,
        "phase4_approved": phase4_approved,
        "demo_execution_adapter_implementation_approved": demo_impl_approved,
        "execution_adapter_implementation_approved": adapter_impl_approved,
        "execution_adapter_use_approved": False,
        "execution_adapter_approved": False,
        "broker_request_approved": False,
        "mt5_execution_approved": False,
        "terminal_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "fail_closed_skeleton_verified": fail_closed_skeleton_verified,
        "real_intent_refusal_audit_verified": real_intent_refusal_audit_verified,
        "adapter_boundary_static_verified": adapter_boundary_static_verified,
        "execution_authority_remains_absent": True,
        "readiness_packet_ready": not violations
        and fail_closed_skeleton_verified
        and real_intent_refusal_audit_verified
        and adapter_boundary_static_verified,
        "broker_request_constructed": False,
        "mt5_request_constructed": False,
        "order_payload_constructed": False,
        "dispatch_attempted": False,
        "terminal_mutated": False,
        "broker_state_mutated": False,
        "refusal_reasons": sorted(skeleton_reasons.union(intent_reasons)),
        "violations": violations,
    }

    if source_paths:
        record["source_paths"] = dict(source_paths)

    record["verdict"] = "PASS" if record["readiness_packet_ready"] and not violations else "FAIL"
    return record


def build_readiness_packet_records(
    *,
    skeleton_records: Sequence[dict[str, Any]],
    intent_refusal_records: Sequence[dict[str, Any]],
    boundary_static_records: Sequence[dict[str, Any]],
    source_paths: Mapping[str, str] | None = None,
) -> list[dict[str, Any]]:
    violations: list[str] = []
    skeleton_record = _first_record(
        skeleton_records,
        "demo_execution_adapter_skeleton_records",
        violations,
    )
    intent_refusal_record = _first_record(
        intent_refusal_records,
        "demo_adapter_intent_refusal_audit_records",
        violations,
    )
    boundary_static_record = _first_record(
        boundary_static_records,
        "demo_adapter_boundary_static_verifier_records",
        violations,
    )

    packet = build_readiness_packet_record(
        skeleton_record=skeleton_record,
        intent_refusal_record=intent_refusal_record,
        boundary_static_record=boundary_static_record,
        source_paths=source_paths,
    )

    if violations:
        packet["violations"] = sorted(set(packet["violations"] + violations))
        packet["readiness_packet_ready"] = False
        packet["verdict"] = "FAIL"

    return [packet]


def build_readiness_packet_records_from_files(
    *,
    skeleton_jsonl: str | Path,
    intent_refusal_audit_jsonl: str | Path,
    boundary_static_verifier_jsonl: str | Path,
) -> list[dict[str, Any]]:
    return build_readiness_packet_records(
        skeleton_records=read_jsonl(skeleton_jsonl),
        intent_refusal_records=read_jsonl(intent_refusal_audit_jsonl),
        boundary_static_records=read_jsonl(boundary_static_verifier_jsonl),
        source_paths={
            "demo_execution_adapter_skeleton": str(skeleton_jsonl),
            "demo_adapter_intent_refusal_audit": str(intent_refusal_audit_jsonl),
            "demo_adapter_boundary_static_verifier": str(boundary_static_verifier_jsonl),
        },
    )


def verify_readiness_packet_records(
    records: Sequence[Mapping[str, Any]],
    *,
    allowed_demo_server: str | None = None,
    require_ready: bool = True,
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
        if require_ready:
            expected["verdict"] = "PASS"

        for key, expected_value in expected.items():
            if record.get(key) != expected_value:
                violations.append(f"{prefix}_{key}_mismatch")

        if require_ready:
            for key in (
                "phase4_approved",
                "demo_execution_adapter_implementation_approved",
                "execution_adapter_implementation_approved",
                "fail_closed_skeleton_verified",
                "real_intent_refusal_audit_verified",
                "adapter_boundary_static_verified",
                "execution_authority_remains_absent",
                "readiness_packet_ready",
            ):
                if record.get(key) is not True:
                    violations.append(f"{prefix}_{key}_not_true")

        for key in FALSE_AUTHORITY_FLAGS + FALSE_MUTATION_FLAGS:
            if record.get(key) is not False:
                violations.append(f"{prefix}_{key}_not_false")

        if record.get("upstream_artifact_count") != 3:
            violations.append(f"{prefix}_upstream_artifact_count_mismatch")

        refusal_reasons = set(_coerce_str_list(record.get("refusal_reasons")))
        for reason in REQUIRED_REFUSAL_REASONS:
            if reason not in refusal_reasons:
                violations.append(f"{prefix}_missing_refusal_reason:{reason}")

        source_summaries = record.get("source_summaries")
        if not isinstance(source_summaries, Mapping):
            violations.append(f"{prefix}_source_summaries_missing")
        else:
            for source_name, source_expected in SOURCE_EXPECTATIONS.items():
                source_summary = source_summaries.get(source_name)
                if not isinstance(source_summary, Mapping):
                    violations.append(f"{prefix}_{source_name}_source_summary_missing")
                    continue
                for key, expected_value in source_expected.items():
                    if source_summary.get(key) != expected_value:
                        violations.append(f"{prefix}_{source_name}_{key}_mismatch")
                source_verdict = source_summary.get("verdict")
                if source_verdict is not None and source_verdict != "PASS":
                    violations.append(f"{prefix}_{source_name}_verdict_not_pass")

        builder_violations = record.get("violations")
        if builder_violations:
            violations.append(f"{prefix}_builder_violations_present")

        if allowed_demo_server:
            observed_servers = _server_values(record)
            if observed_servers and allowed_demo_server not in observed_servers:
                violations.append(
                    f"{prefix}_allowed_demo_server_mismatch:"
                    f"expected={allowed_demo_server};observed={','.join(observed_servers)}"
                )

    return violations


def format_verification_summary(records: Sequence[Mapping[str, Any]], violations: Sequence[str]) -> str:
    upstream_count = records[0].get("upstream_artifact_count", 0) if records else 0
    lines = [
        f"H024 Phase 4 demo adapter readiness packet records: {len(records)}",
        f"Upstream artifacts summarized: {upstream_count}",
        f"Violations: {len(violations)}",
    ]
    if violations:
        lines.extend(f"- {violation}" for violation in violations)
    lines.append(f"Verdict: {'PASS' if not violations else 'FAIL'}")
    return "\n".join(lines)