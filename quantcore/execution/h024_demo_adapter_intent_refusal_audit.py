from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "h024_demo_adapter_intent_refusal_audit_v1"
KIND = "DEMO_ADAPTER_INTENT_REFUSAL_AUDIT"
STATUS = "ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY"
DECISION = "REFUSE_DISPATCH_NO_ORDER_AUTHORITY"

SKELETON_SCHEMA = "h024_demo_execution_adapter_skeleton_v1"
SKELETON_KIND = "DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED"
SKELETON_STATUS = "DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED"
INTENT_SCHEMA_PREFIX = "h024_order_intent_simulation"

REQUIRED_REFUSAL_REASONS = (
    "execution_adapter_use_not_approved",
    "demo_order_placement_not_approved",
    "execution_not_approved",
)

FALSE_AUTHORITY_FLAGS = (
    "execution_adapter_use_approved",
    "execution_adapter_approved",
    "demo_order_placement_approved",
    "live_order_placement_approved",
    "execution_approved",
    "broker_request_approved",
    "mt5_execution_approved",
    "terminal_mutation_approved",
)

PROHIBITED_PAYLOAD_KEYS = frozenset(
    {
        "broker_request",
        "mt5_request",
        "mql_trade_request",
        "mql_trade_result",
        "order_payload",
        "order_send_payload",
        "trade_request",
        "trade_result",
        "terminal_mutation_payload",
        "broker_mutation_payload",
    }
)

SAFE_INTENT_CONTEXT_FIELDS = (
    "schema",
    "kind",
    "status",
    "decision",
    "verdict",
    "intent_id",
    "stable_intent_id",
    "source_intent_id",
    "runtime_timestamp",
    "timestamp",
    "symbol",
    "broker_symbol",
    "model_symbol",
    "normalized_symbol",
    "timeframe",
    "closed_h4_time",
    "closed_bar_time",
    "action",
    "side",
    "direction",
    "entry",
    "entry_price",
    "stop",
    "stop_price",
    "stop_distance",
    "stop_distance_price",
    "tick_size",
    "tick_value",
    "tick_value_usd_per_lot",
    "account_balance",
    "account_balance_usd",
    "account_equity",
    "account_equity_usd",
    "risk_fraction",
    "risk_usd",
    "raw_lots",
    "final_lots",
    "lots",
    "volume_min",
    "min_volume",
    "volume_max",
    "max_volume",
    "volume_step",
    "volume_digits",
    "server",
    "account_server",
    "broker_server",
    "company",
    "broker_company",
    "currency",
    "account_currency",
    "leverage",
)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Read a UTF-8/UTF-8-BOM JSONL file into dictionary records."""
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
    """Write JSONL deterministically without a BOM."""
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
        return value.strip().lower() in {"1", "true", "yes", "y", "allow", "allowed"}
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


def _first_record(records: Sequence[dict[str, Any]], source_name: str, violations: list[str]) -> dict[str, Any]:
    if not records:
        violations.append(f"{source_name}_missing")
        return {}
    if len(records) > 1:
        violations.append(f"{source_name}_expected_one_record_got_{len(records)}")
    return records[0]


def _source_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: record[key]
        for key in ("schema", "kind", "status", "decision", "verdict")
        if key in record and _is_safe_scalar(record[key])
    }


def _is_safe_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _merge_safe_context(target: dict[str, Any], source: Mapping[str, Any]) -> None:
    for key in SAFE_INTENT_CONTEXT_FIELDS:
        if key in source and key not in target and _is_safe_scalar(source[key]):
            target[key] = source[key]


def _intent_envelope(intent_record: Mapping[str, Any]) -> dict[str, Any]:
    context: dict[str, Any] = {}
    _merge_safe_context(context, intent_record)

    for nested_key in (
        "intent",
        "order_intent",
        "simulated_intent",
        "source_intent",
        "sizing",
        "risk",
        "account",
        "broker",
    ):
        nested_value = intent_record.get(nested_key)
        if isinstance(nested_value, Mapping):
            _merge_safe_context(context, nested_value)

    return {
        "source_summary": _source_summary(intent_record),
        "context": context,
    }


def _find_prohibited_payload_keys(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    hits: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = path + (str(key),)
            if key in PROHIBITED_PAYLOAD_KEYS:
                hits.append(".".join(child_path))
            hits.extend(_find_prohibited_payload_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(_find_prohibited_payload_keys(child, path + (str(index),)))
    return hits


def build_audit_record(
    skeleton_record: Mapping[str, Any],
    intent_record: Mapping[str, Any],
    *,
    safety_preflight_record: Mapping[str, Any] | None = None,
    source_paths: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build one non-executing adapter intent-ingestion/refusal audit record."""
    source_records: list[Mapping[str, Any]] = [skeleton_record, intent_record]
    if safety_preflight_record is not None:
        source_records.append(safety_preflight_record)

    violations: list[str] = []

    if skeleton_record.get("schema") != SKELETON_SCHEMA:
        violations.append("skeleton_schema_mismatch")
    if skeleton_record.get("kind") != SKELETON_KIND:
        violations.append("skeleton_kind_mismatch")
    if skeleton_record.get("status") != SKELETON_STATUS:
        violations.append("skeleton_status_mismatch")
    if skeleton_record.get("decision") != DECISION:
        violations.append("skeleton_decision_not_refusal")

    intent_schema = intent_record.get("schema")
    if isinstance(intent_schema, str) and not intent_schema.startswith(INTENT_SCHEMA_PREFIX):
        violations.append("intent_schema_not_order_intent_simulation")
    if not intent_record:
        violations.append("intent_record_missing")

    phase4_approved = _any_truthy(source_records, "phase4_approved")
    demo_impl_approved = _any_truthy(
        source_records, "demo_execution_adapter_implementation_approved"
    ) or _any_truthy(source_records, "execution_adapter_implementation_approved")
    execution_adapter_implementation_approved = _any_truthy(
        source_records, "execution_adapter_implementation_approved"
    ) or demo_impl_approved

    if not phase4_approved:
        violations.append("phase4_not_approved")
    if not demo_impl_approved:
        violations.append("demo_execution_adapter_implementation_not_approved")
    if not execution_adapter_implementation_approved:
        violations.append("execution_adapter_implementation_not_approved")

    true_forbidden_flags = sorted(flag for flag in FALSE_AUTHORITY_FLAGS if _any_truthy(source_records, flag))
    for flag in true_forbidden_flags:
        violations.append(f"{flag}_unexpectedly_true")

    skeleton_refusal_reasons = _collect_reasons(skeleton_record)
    missing_reasons = sorted(set(REQUIRED_REFUSAL_REASONS).difference(skeleton_refusal_reasons))
    for reason in missing_reasons:
        violations.append(f"missing_refusal_reason:{reason}")

    if _truthy(skeleton_record.get("dispatch_attempted")):
        violations.append("skeleton_dispatch_attempted")
    if _truthy(skeleton_record.get("terminal_mutated")):
        violations.append("skeleton_terminal_mutated")
    if _truthy(skeleton_record.get("broker_state_mutated")):
        violations.append("skeleton_broker_state_mutated")

    record: dict[str, Any] = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "source_summaries": {
            "demo_execution_adapter_skeleton": _source_summary(skeleton_record),
            "order_intent_simulation": _source_summary(intent_record),
        },
        "phase4_approved": phase4_approved,
        "demo_execution_adapter_implementation_approved": demo_impl_approved,
        "execution_adapter_implementation_approved": execution_adapter_implementation_approved,
        "execution_adapter_use_approved": False,
        "execution_adapter_approved": False,
        "broker_request_approved": False,
        "mt5_execution_approved": False,
        "terminal_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "adapter_intent_ingested": bool(intent_record),
        "intent_envelope_constructed": bool(intent_record),
        "broker_request_constructed": False,
        "mt5_request_constructed": False,
        "order_payload_constructed": False,
        "dispatch_attempted": False,
        "terminal_mutated": False,
        "broker_state_mutated": False,
        "refusal_reasons": skeleton_refusal_reasons,
        "intent_envelope": _intent_envelope(intent_record),
        "violations": violations,
    }

    if safety_preflight_record is not None:
        record["source_summaries"]["execution_safety_controls_preflight"] = _source_summary(
            safety_preflight_record
        )

    if source_paths:
        record["source_paths"] = dict(source_paths)

    record["verdict"] = "PASS" if not violations else "FAIL"
    return record


def build_audit_records(
    *,
    skeleton_records: Sequence[dict[str, Any]],
    intent_records: Sequence[dict[str, Any]],
    safety_preflight_records: Sequence[dict[str, Any]] | None = None,
    source_paths: Mapping[str, str] | None = None,
) -> list[dict[str, Any]]:
    violations: list[str] = []
    skeleton_record = _first_record(skeleton_records, "skeleton_records", violations)
    intent_record = _first_record(intent_records, "intent_records", violations)
    safety_record: dict[str, Any] | None = None

    if safety_preflight_records is not None:
        safety_record = _first_record(safety_preflight_records, "safety_preflight_records", violations)

    audit_record = build_audit_record(
        skeleton_record,
        intent_record,
        safety_preflight_record=safety_record,
        source_paths=source_paths,
    )
    if violations:
        audit_record["violations"] = sorted(set(audit_record["violations"] + violations))
        audit_record["verdict"] = "FAIL"
    return [audit_record]


def build_audit_records_from_files(
    *,
    skeleton_jsonl: str | Path,
    order_intent_simulation_jsonl: str | Path,
    safety_preflight_jsonl: str | Path | None = None,
) -> list[dict[str, Any]]:
    safety_records = read_jsonl(safety_preflight_jsonl) if safety_preflight_jsonl is not None else None
    source_paths = {
        "demo_execution_adapter_skeleton": str(skeleton_jsonl),
        "order_intent_simulation": str(order_intent_simulation_jsonl),
    }
    if safety_preflight_jsonl is not None:
        source_paths["execution_safety_controls_preflight"] = str(safety_preflight_jsonl)

    return build_audit_records(
        skeleton_records=read_jsonl(skeleton_jsonl),
        intent_records=read_jsonl(order_intent_simulation_jsonl),
        safety_preflight_records=safety_records,
        source_paths=source_paths,
    )


def verify_audit_records(
    records: Sequence[Mapping[str, Any]],
    *,
    allowed_demo_server: str | None = None,
    require_refusal: bool = True,
) -> list[str]:
    violations: list[str] = []

    if not records:
        return ["no_records"]
    if len(records) != 1:
        violations.append(f"expected_one_record_got_{len(records)}")

    for index, record in enumerate(records):
        prefix = f"record_{index}"

        expected_fields = {
            "schema": SCHEMA,
            "kind": KIND,
            "status": STATUS,
            "decision": DECISION,
            "verdict": "PASS",
        }
        for key, expected in expected_fields.items():
            if record.get(key) != expected:
                violations.append(f"{prefix}_{key}_mismatch")

        true_required_flags = (
            "phase4_approved",
            "demo_execution_adapter_implementation_approved",
            "execution_adapter_implementation_approved",
            "adapter_intent_ingested",
            "intent_envelope_constructed",
        )
        for key in true_required_flags:
            if record.get(key) is not True:
                violations.append(f"{prefix}_{key}_not_true")

        false_required_flags = (
            "execution_adapter_use_approved",
            "execution_adapter_approved",
            "broker_request_approved",
            "mt5_execution_approved",
            "terminal_mutation_approved",
            "demo_order_placement_approved",
            "live_order_placement_approved",
            "execution_approved",
            "broker_request_constructed",
            "mt5_request_constructed",
            "order_payload_constructed",
            "dispatch_attempted",
            "terminal_mutated",
            "broker_state_mutated",
        )
        for key in false_required_flags:
            if record.get(key) is not False:
                violations.append(f"{prefix}_{key}_not_false")

        if require_refusal:
            refusal_reasons = set(_coerce_str_list(record.get("refusal_reasons")))
            for reason in REQUIRED_REFUSAL_REASONS:
                if reason not in refusal_reasons:
                    violations.append(f"{prefix}_missing_refusal_reason:{reason}")

        builder_violations = record.get("violations")
        if builder_violations:
            violations.append(f"{prefix}_builder_violations_present")

        prohibited_hits = _find_prohibited_payload_keys(record)
        for hit in prohibited_hits:
            violations.append(f"{prefix}_prohibited_payload_key:{hit}")

        if allowed_demo_server:
            server_values = sorted(
                {
                    str(value)
                    for key in ("server", "account_server", "broker_server", "mt5_server")
                    for value in _walk_values_by_key(record, key)
                    if isinstance(value, str) and value
                }
            )
            if server_values and allowed_demo_server not in server_values:
                violations.append(
                    f"{prefix}_allowed_demo_server_mismatch:"
                    f"expected={allowed_demo_server};observed={','.join(server_values)}"
                )

    return violations


def format_verification_summary(records: Sequence[Mapping[str, Any]], violations: Sequence[str]) -> str:
    lines = [
        f"H024 demo adapter intent refusal audit records: {len(records)}",
        f"Violations: {len(violations)}",
    ]
    if violations:
        lines.extend(f"- {violation}" for violation in violations)
    lines.append(f"Verdict: {'PASS' if not violations else 'FAIL'}")
    return "\n".join(lines)