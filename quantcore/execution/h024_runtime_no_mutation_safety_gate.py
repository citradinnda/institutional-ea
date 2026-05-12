from __future__ import annotations

import argparse
import importlib
import json
import math
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from quantcore.execution.h024_runtime_safety_heartbeat import (
    FORBIDDEN_AUTHORIZATION_KEYS,
)
from quantcore.execution.h024_unified_read_only_post_canary_runtime_supervision import (
    PACKET_TYPE as UNIFIED_SUPERVISION_PACKET_TYPE,
    collect_h024_unified_read_only_post_canary_runtime_supervision,
)

STRATEGY_ID = "H024"
PACKET_TYPE = "H024_RUNTIME_NO_MUTATION_SAFETY_GATE_CONTRACT"
SCHEMA_VERSION = 1

LOCKOUT_READER_MODULE = "quantcore.execution.h024_runtime_safety_lockout"
UNIFIED_SUPERVISION_MODULE = "quantcore.execution.h024_unified_read_only_post_canary_runtime_supervision"

DEFAULT_OUTPUT_PATH = Path("reports") / "h024_runtime_no_mutation_safety_gate.jsonl"

TRUSTED_UNIFIED_SUPERVISION_SOURCES = {
    "runtime_collector",
    "verified_jsonl",
    "test_fixture",
}

EXPECTED_UNIFIED_OPERATOR_NEXT_ACTION = "READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED"

GATE_REQUIRED_FOR_ACTIONS = (
    "broker_mutation",
    "order_check",
    "order_send",
    "entry",
    "close_modify",
    "xauusd_order",
    "usdjpy_order",
    "trading_loop",
    "automatic_execution",
)

GATE_BLOCK_FLAGS = (
    "broker_mutation_blocked",
    "order_check_blocked",
    "order_send_blocked",
    "entry_blocked",
    "close_modify_blocked",
    "xauusd_order_blocked",
    "usdjpy_order_blocked",
    "trading_loop_blocked",
    "automatic_execution_blocked",
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _plain(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        if isinstance(value, float) and not math.isfinite(value):
            return repr(value)
        return value
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "_asdict"):
        return {str(k): _plain(v) for k, v in value._asdict().items()}
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_plain(v) for v in value]
    if hasattr(value, "__dict__"):
        return {str(k): _plain(v) for k, v in vars(value).items() if not str(k).startswith("_")}
    return repr(value)


def _false_authorizations() -> dict[str, bool]:
    return {key: False for key in FORBIDDEN_AUTHORIZATION_KEYS}


def _authorization_violations(authorizations: Mapping[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        if key not in authorizations:
            violations.append(
                {
                    "code": "MISSING_AUTHORIZATION_KEY",
                    "message": f"Required authorization key is missing: {key}",
                    "field": key,
                    "fail_closed": True,
                }
            )
        elif authorizations[key] is not False:
            violations.append(
                {
                    "code": "UNSAFE_AUTHORIZATION_TRUE",
                    "message": f"Forbidden runtime authorization is not false: {key}",
                    "field": key,
                    "observed": _plain(authorizations[key]),
                    "fail_closed": True,
                }
            )
    return violations


def _module_reference(module_name: str) -> dict[str, Any]:
    reference: dict[str, Any] = {
        "module": module_name,
        "module_importable": False,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
    }
    try:
        module = importlib.import_module(module_name)
        reference["module_importable"] = True
        reference["module_file"] = getattr(module, "__file__", None)
    except Exception as exc:
        reference["module_error"] = repr(exc)
    return reference


def _gate_result_block_all() -> dict[str, Any]:
    result = {
        "gate_contract_name": PACKET_TYPE,
        "gate_mode": "NO_MUTATION_CONTRACT_ONLY",
        "gate_opens_any_mutation_path": False,
        "future_broker_facing_code_must_check_gate": True,
        "future_broker_facing_code_must_reject_if_gate_missing": True,
        "future_broker_facing_code_must_reject_if_gate_verdict_not_pass": True,
        "future_broker_facing_code_must_reject_if_any_block_flag_is_false": True,
        "required_before_actions": list(GATE_REQUIRED_FOR_ACTIONS),
    }
    for flag in GATE_BLOCK_FLAGS:
        result[flag] = True
    return result


def _validate_unified_supervision_record(
    record: Any,
    *,
    source: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "passed": bool(passed),
                "detail": _plain(detail),
                "fail_closed_on_failure": True,
            }
        )
        if not passed:
            violations.append(
                {
                    "code": name.upper(),
                    "message": f"No-mutation gate unified supervision check failed: {name}",
                    "detail": _plain(detail),
                    "fail_closed": True,
                }
            )

    add_check(
        "unified_supervision_source_trusted",
        source in TRUSTED_UNIFIED_SUPERVISION_SOURCES,
        {"source": source, "trusted_sources": sorted(TRUSTED_UNIFIED_SUPERVISION_SOURCES)},
    )

    is_mapping = isinstance(record, Mapping)
    add_check("unified_supervision_record_object", is_mapping, {"type": type(record).__name__})
    if not is_mapping:
        return checks, violations

    add_check(
        "unified_supervision_strategy_expected",
        record.get("strategy") == STRATEGY_ID,
        {"expected": STRATEGY_ID, "observed": record.get("strategy")},
    )
    add_check(
        "unified_supervision_packet_type_expected",
        record.get("packet_type") == UNIFIED_SUPERVISION_PACKET_TYPE,
        {"expected": UNIFIED_SUPERVISION_PACKET_TYPE, "observed": record.get("packet_type")},
    )
    add_check(
        "unified_supervision_verdict_pass",
        record.get("verdict") == "PASS",
        {"observed": record.get("verdict")},
    )
    add_check(
        "unified_supervision_operator_next_action_read_only",
        record.get("operator_next_action") == EXPECTED_UNIFIED_OPERATOR_NEXT_ACTION,
        {"expected": EXPECTED_UNIFIED_OPERATOR_NEXT_ACTION, "observed": record.get("operator_next_action")},
    )
    add_check(
        "unified_supervision_effectively_blocks_entries",
        record.get("effective_new_entries_blocked") is True,
        {"observed": record.get("effective_new_entries_blocked")},
    )

    embedded_violations = record.get("violations", [])
    add_check(
        "unified_supervision_embedded_violations_absent",
        isinstance(embedded_violations, list) and len(embedded_violations) == 0,
        {"embedded_violation_count": len(embedded_violations) if isinstance(embedded_violations, list) else None},
    )

    authorizations = record.get("authorizations")
    if not isinstance(authorizations, Mapping):
        add_check("unified_supervision_authorizations_object", False, {"type": type(authorizations).__name__})
    else:
        authorization_violations = _authorization_violations(authorizations)
        add_check(
            "unified_supervision_authorizations_false",
            not authorization_violations,
            {"authorization_violation_count": len(authorization_violations)},
        )
        for violation in authorization_violations:
            violations.append({**violation, "source": "unified_supervision_authorizations"})

    top_level_authorization_violations = []
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        if record.get(key) is not False:
            top_level_authorization_violations.append(
                {
                    "code": "UNIFIED_SUPERVISION_TOP_LEVEL_UNSAFE_AUTHORIZATION",
                    "message": f"Unified supervision top-level forbidden authorization is not false: {key}",
                    "field": key,
                    "observed": _plain(record.get(key)),
                    "fail_closed": True,
                }
            )
    add_check(
        "unified_supervision_top_level_authorizations_false",
        not top_level_authorization_violations,
        {"violation_count": len(top_level_authorization_violations)},
    )
    violations.extend(top_level_authorization_violations)

    canary_section = record.get("exact_known_canary")
    add_check(
        "unified_supervision_exact_canary_section_present",
        isinstance(canary_section, Mapping),
        {"type": type(canary_section).__name__},
    )
    if isinstance(canary_section, Mapping):
        add_check(
            "unified_supervision_canary_state_allowed",
            canary_section.get("state") in {"OBSERVED_EXACT_KNOWN_CANARY", "NOT_OBSERVED", "NOT_OBSERVED_OR_NOT_EXTRACTED"},
            {"observed": canary_section.get("state")},
        )

    runtime_aggregate = record.get("runtime_safety_aggregate")
    add_check(
        "unified_supervision_runtime_aggregate_section_present",
        isinstance(runtime_aggregate, Mapping),
        {"type": type(runtime_aggregate).__name__},
    )
    if isinstance(runtime_aggregate, Mapping):
        aggregate_summary = runtime_aggregate.get("summary")
        aggregate_record = runtime_aggregate.get("record")
        add_check(
            "unified_supervision_runtime_aggregate_summary_pass",
            isinstance(aggregate_summary, Mapping) and aggregate_summary.get("verdict") == "PASS",
            _plain(aggregate_summary),
        )
        add_check(
            "unified_supervision_runtime_aggregate_record_pass",
            isinstance(aggregate_record, Mapping) and aggregate_record.get("verdict") == "PASS",
            _plain(aggregate_record) if isinstance(aggregate_record, Mapping) else {"type": type(aggregate_record).__name__},
        )

    canary_supervision = record.get("canary_read_only_supervision")
    add_check(
        "unified_supervision_canary_read_only_section_present",
        isinstance(canary_supervision, Mapping),
        {"type": type(canary_supervision).__name__},
    )
    if isinstance(canary_supervision, Mapping):
        canary_summary = canary_supervision.get("summary")
        add_check(
            "unified_supervision_canary_read_only_summary_pass",
            isinstance(canary_summary, Mapping) and canary_summary.get("all_records_passed") is True,
            _plain(canary_summary),
        )

    return checks, violations


def collect_h024_runtime_no_mutation_safety_gate(
    *,
    mt5_client: Any | None = None,
    unified_supervision_record: Mapping[str, Any] | None = None,
    unified_supervision_source: str = "runtime_collector",
    invoke_unified_supervision: bool = True,
) -> dict[str, Any]:
    """Collect a read-only H024 no-mutation safety gate contract packet.

    The contract validates a trusted unified read-only post-canary supervision
    packet, then emits a fail-closed gate result that blocks every broker-facing
    mutation pathway. A passing gate-contract packet still authorizes no trading.
    """

    observed_at_utc = _utc_now_iso()
    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "passed": bool(passed),
                "detail": _plain(detail),
                "fail_closed_on_failure": True,
            }
        )
        if not passed:
            violations.append(
                {
                    "code": name.upper(),
                    "message": f"No-mutation safety gate check failed: {name}",
                    "detail": _plain(detail),
                    "fail_closed": True,
                }
            )

    lockout_reference = _module_reference(LOCKOUT_READER_MODULE)
    unified_reference = _module_reference(UNIFIED_SUPERVISION_MODULE)

    add_check("runtime_lockout_reader_referenced", lockout_reference.get("module_importable") is True, lockout_reference)
    add_check("unified_supervision_module_referenced", unified_reference.get("module_importable") is True, unified_reference)

    if unified_supervision_record is None and invoke_unified_supervision:
        unified_supervision_record = collect_h024_unified_read_only_post_canary_runtime_supervision(mt5_client=mt5_client)

    unified_checks, unified_violations = _validate_unified_supervision_record(
        unified_supervision_record,
        source=unified_supervision_source,
    )
    checks.extend(unified_checks)
    violations.extend(unified_violations)

    gate_result = _gate_result_block_all()
    block_flags_all_true = all(gate_result.get(flag) is True for flag in GATE_BLOCK_FLAGS)
    add_check(
        "gate_blocks_all_mutation_paths",
        block_flags_all_true and gate_result.get("gate_opens_any_mutation_path") is False,
        gate_result,
    )
    add_check(
        "future_broker_facing_code_must_check_gate",
        gate_result.get("future_broker_facing_code_must_check_gate") is True,
        gate_result,
    )

    authorizations = _false_authorizations()
    authorization_violations = _authorization_violations(authorizations)
    violations.extend(authorization_violations)
    add_check("all_runtime_authorizations_false", not authorization_violations, authorizations)

    verdict = "PASS" if not violations else "FAIL"
    operator_state = (
        "NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED"
        if verdict == "PASS"
        else "FAIL_CLOSED_NO_MUTATION_GATE_CONTRACT_BLOCKED"
    )

    operator_next_action = (
        "KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION"
        if verdict == "PASS"
        else "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "trusted_unified_supervision_sources": sorted(TRUSTED_UNIFIED_SUPERVISION_SOURCES),
            "expected_unified_packet_type": UNIFIED_SUPERVISION_PACKET_TYPE,
            "expected_unified_operator_next_action": EXPECTED_UNIFIED_OPERATOR_NEXT_ACTION,
            "gate_required_for_actions": list(GATE_REQUIRED_FOR_ACTIONS),
        },
        "references": {
            "lockout_reader_reference": lockout_reference,
            "unified_supervision_reference": unified_reference,
        },
        "unified_supervision": {
            "source": unified_supervision_source,
            "record": _plain(unified_supervision_record),
        },
        "gate_contract": {
            "version": SCHEMA_VERSION,
            "required_for_future_broker_facing_code": True,
            "current_scope": "contract_only_no_mutation_authorized",
            "missing_gate_must_fail_closed": True,
            "malformed_gate_must_fail_closed": True,
            "untrusted_unified_supervision_must_fail_closed": True,
            "passing_unified_supervision_is_not_execution_permission": True,
        },
        "gate_result": gate_result,
        "checks": checks,
        "authorizations": authorizations,
        "effective_new_entries_blocked": True,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "xauusd_order_authorized": False,
        "usdjpy_order_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
        "operator_state": operator_state,
        "operator_next_action": operator_next_action,
        "violations": violations,
        "verdict": verdict,
    }


def verify_h024_runtime_no_mutation_safety_gate_records(
    records: list[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    verification_violations: list[dict[str, Any]] = []

    if not records:
        verification_violations.append(
            {
                "code": "NO_RECORDS",
                "message": "No H024 runtime no-mutation safety gate records were found.",
                "fail_closed": True,
            }
        )

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_SCHEMA_VERSION",
                    "message": "No-mutation gate record has an unexpected schema version.",
                    "record_index": index,
                    "observed": _plain(record.get("schema_version")),
                    "expected": SCHEMA_VERSION,
                    "fail_closed": True,
                }
            )

        if record.get("strategy") != STRATEGY_ID:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_STRATEGY",
                    "message": "No-mutation gate record has an unexpected strategy.",
                    "record_index": index,
                    "observed": _plain(record.get("strategy")),
                    "expected": STRATEGY_ID,
                    "fail_closed": True,
                }
            )

        if record.get("packet_type") != PACKET_TYPE:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_PACKET_TYPE",
                    "message": "No-mutation gate record has an unexpected packet type.",
                    "record_index": index,
                    "observed": _plain(record.get("packet_type")),
                    "expected": PACKET_TYPE,
                    "fail_closed": True,
                }
            )

        authorization_map = record.get("authorizations")
        if not isinstance(authorization_map, Mapping):
            verification_violations.append(
                {
                    "code": "AUTHORIZATIONS_NOT_OBJECT",
                    "message": "No-mutation gate authorizations field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            for violation in _authorization_violations(authorization_map):
                violation["record_index"] = index
                verification_violations.append(violation)

        for key in FORBIDDEN_AUTHORIZATION_KEYS:
            if record.get(key) is not False:
                verification_violations.append(
                    {
                        "code": "TOP_LEVEL_UNSAFE_AUTHORIZATION",
                        "message": f"Top-level forbidden authorization is not false: {key}",
                        "record_index": index,
                        "field": key,
                        "observed": _plain(record.get(key)),
                        "fail_closed": True,
                    }
                )

        if record.get("effective_new_entries_blocked") is not True:
            verification_violations.append(
                {
                    "code": "NEW_ENTRIES_NOT_EFFECTIVELY_BLOCKED",
                    "message": "No-mutation gate must keep effective_new_entries_blocked true.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        gate_result = record.get("gate_result")
        if not isinstance(gate_result, Mapping):
            verification_violations.append(
                {
                    "code": "GATE_RESULT_NOT_OBJECT",
                    "message": "No-mutation gate result is missing or malformed.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            if gate_result.get("gate_opens_any_mutation_path") is not False:
                verification_violations.append(
                    {
                        "code": "GATE_OPENS_MUTATION_PATH",
                        "message": "No-mutation gate result must not open any mutation path.",
                        "record_index": index,
                        "observed": _plain(gate_result.get("gate_opens_any_mutation_path")),
                        "fail_closed": True,
                    }
                )
            for flag in GATE_BLOCK_FLAGS:
                if gate_result.get(flag) is not True:
                    verification_violations.append(
                        {
                            "code": "GATE_BLOCK_FLAG_NOT_TRUE",
                            "message": f"No-mutation gate block flag is not true: {flag}",
                            "record_index": index,
                            "field": flag,
                            "observed": _plain(gate_result.get(flag)),
                            "fail_closed": True,
                        }
                    )
            if gate_result.get("future_broker_facing_code_must_check_gate") is not True:
                verification_violations.append(
                    {
                        "code": "FUTURE_CODE_NOT_REQUIRED_TO_CHECK_GATE",
                        "message": "Future broker-facing code must be required to check the gate.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )

        unified_section = record.get("unified_supervision")
        if not isinstance(unified_section, Mapping):
            verification_violations.append(
                {
                    "code": "UNIFIED_SUPERVISION_SECTION_MISSING",
                    "message": "No-mutation gate record is missing unified supervision section.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            source = unified_section.get("source")
            unified_record = unified_section.get("record")
            _, unified_violations = _validate_unified_supervision_record(unified_record, source=str(source))
            for violation in unified_violations:
                verification_violations.append(
                    {
                        **violation,
                        "record_index": index,
                        "aggregate_source": "unified_supervision",
                    }
                )

        gate_contract = record.get("gate_contract")
        if not isinstance(gate_contract, Mapping):
            verification_violations.append(
                {
                    "code": "GATE_CONTRACT_NOT_OBJECT",
                    "message": "No-mutation gate contract is missing or malformed.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            required_contract_booleans = (
                "required_for_future_broker_facing_code",
                "missing_gate_must_fail_closed",
                "malformed_gate_must_fail_closed",
                "untrusted_unified_supervision_must_fail_closed",
                "passing_unified_supervision_is_not_execution_permission",
            )
            for key in required_contract_booleans:
                if gate_contract.get(key) is not True:
                    verification_violations.append(
                        {
                            "code": "GATE_CONTRACT_REQUIRED_BOOLEAN_NOT_TRUE",
                            "message": f"Required gate contract boolean is not true: {key}",
                            "record_index": index,
                            "field": key,
                            "observed": _plain(gate_contract.get(key)),
                            "fail_closed": True,
                        }
                    )

        embedded_violations = record.get("violations", [])
        if record.get("verdict") == "PASS" and embedded_violations:
            verification_violations.append(
                {
                    "code": "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS",
                    "message": "No-mutation gate record verdict is PASS but embedded violations are present.",
                    "record_index": index,
                    "embedded_violation_count": len(embedded_violations),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("verdict") != "PASS":
            verification_violations.append(
                {
                    "code": "RECORD_VERDICT_NOT_PASS",
                    "message": "No-mutation gate record verdict is not PASS.",
                    "record_index": index,
                    "observed": _plain(record.get("verdict")),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("operator_next_action") != "KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION":
            verification_violations.append(
                {
                    "code": "UNEXPECTED_OPERATOR_NEXT_ACTION",
                    "message": "No-mutation gate operator next action is unexpected under require-pass verification.",
                    "record_index": index,
                    "observed": _plain(record.get("operator_next_action")),
                    "fail_closed": True,
                }
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": f"{PACKET_TYPE}_VERIFICATION",
        "record_count": len(records),
        "require_pass": require_pass,
        "verification_violations": verification_violations,
        "verifier_verdict": "PASS" if not verification_violations else "FAIL",
    }


def write_jsonl(path: str | Path, records: list[Mapping[str, Any]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Malformed JSONL at {path}:{line_number}: {exc}") from exc
    return records


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or verify H024 runtime no-mutation safety gate JSONL.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    return parser


__all__ = [
    "DEFAULT_OUTPUT_PATH",
    "GATE_BLOCK_FLAGS",
    "GATE_REQUIRED_FOR_ACTIONS",
    "PACKET_TYPE",
    "SCHEMA_VERSION",
    "STRATEGY_ID",
    "TRUSTED_UNIFIED_SUPERVISION_SOURCES",
    "collect_h024_runtime_no_mutation_safety_gate",
    "read_jsonl",
    "verify_h024_runtime_no_mutation_safety_gate_records",
    "write_jsonl",
]