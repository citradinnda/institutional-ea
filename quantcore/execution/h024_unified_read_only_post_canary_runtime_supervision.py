from __future__ import annotations

import argparse
import importlib
import json
import math
import subprocess
import sys
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from quantcore.execution.h024_runtime_safety_aggregate_supervisor import (
    PACKET_TYPE as RUNTIME_SAFETY_AGGREGATE_PACKET_TYPE,
    collect_h024_runtime_safety_aggregate_supervisor,
)
from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
)

STRATEGY_ID = "H024"
PACKET_TYPE = "H024_UNIFIED_READ_ONLY_POST_CANARY_RUNTIME_SUPERVISION"
SCHEMA_VERSION = 1

CANARY_RUNTIME_SYMBOL = "XAUUSDm"
CANARY_MODEL_SYMBOL = "XAUUSD"
CANARY_TICKET_IDENTIFIER = 4413054432
CANARY_ENTRY_DEAL = 3788869526
CANARY_MAGIC = 240024
CANARY_VOLUME = 0.01
CANARY_SIDE = "sell"
CANARY_POSITION_TYPE = 1
CANARY_OPEN_PRICE = 4728.4490000000005
CANARY_STOP_LOSS = 4817.394

CANARY_RUNNER_SCRIPT = Path("scripts") / "run_h024_one_shot_demo_canary_read_only_supervision.py"
CANARY_VERIFIER_SCRIPT = Path("scripts") / "verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py"
CANARY_REPORT_PATH = Path("reports") / "h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl"

LOCKOUT_READER_MODULE = "quantcore.execution.h024_runtime_safety_lockout"
CANARY_SUPERVISION_REFERENCE = "scripts.run_h024_one_shot_demo_canary_read_only_supervision"
RUNTIME_AGGREGATE_MODULE = "quantcore.execution.h024_runtime_safety_aggregate_supervisor"

DEFAULT_OUTPUT_PATH = Path("reports") / "h024_unified_read_only_post_canary_runtime_supervision.jsonl"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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


def _coerce_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


def _coerce_int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


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


def _script_reference(script_path: Path) -> dict[str, Any]:
    root = _repo_root()
    full_path = root / script_path
    return {
        "script_path": str(script_path),
        "script_exists": full_path.exists(),
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Malformed JSONL at {path}:{line_number}: {exc}") from exc
    return records


def _run_subprocess(args: list[str]) -> dict[str, Any]:
    root = _repo_root()
    completed = subprocess.run(
        args,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "args": args,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "succeeded": completed.returncode == 0,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
    }


def _run_canary_read_only_supervision_and_verify() -> dict[str, Any]:
    root = _repo_root()
    report_path = root / CANARY_REPORT_PATH

    runner_result = _run_subprocess([sys.executable, str(CANARY_RUNNER_SCRIPT)])
    verifier_result: dict[str, Any] | None = None
    records: list[dict[str, Any]] = []

    if report_path.exists():
        records = _read_jsonl(report_path)

    if runner_result["succeeded"] and report_path.exists():
        verifier_result = _run_subprocess(
            [
                sys.executable,
                str(CANARY_VERIFIER_SCRIPT),
                str(CANARY_REPORT_PATH),
                "--require-pass",
            ]
        )

    return {
        "runner_invoked": True,
        "report_path": str(CANARY_REPORT_PATH),
        "report_exists": report_path.exists(),
        "runner_result": runner_result,
        "verifier_result": verifier_result,
        "records": records,
    }


def _walk_values(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, Mapping):
        for child in value.values():
            yield from _walk_values(child)
    elif isinstance(value, list | tuple):
        for child in value:
            yield from _walk_values(child)


def _contains_scalar(value: Any, expected: Any) -> bool:
    for observed in _walk_values(value):
        if observed == expected:
            return True
        if isinstance(expected, int):
            coerced = _coerce_int(observed)
            if coerced == expected:
                return True
        if isinstance(expected, float):
            coerced_float = _coerce_float(observed)
            if coerced_float is not None and abs(coerced_float - expected) <= 1e-9:
                return True
    return False


def _find_dicts(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _find_dicts(child)
    elif isinstance(value, list | tuple):
        for child in value:
            yield from _find_dicts(child)


def _extract_exact_canary_observation(*, aggregate_record: Mapping[str, Any] | None, canary_records: list[Mapping[str, Any]]) -> dict[str, Any]:
    search_roots: list[Any] = []
    if aggregate_record is not None:
        search_roots.append(aggregate_record)
    search_roots.extend(canary_records)

    best_match: Mapping[str, Any] | None = None
    for root in search_roots:
        for candidate in _find_dicts(root):
            runtime_symbol = candidate.get("runtime_symbol") or candidate.get("symbol")
            ticket = _coerce_int(candidate.get("ticket"))
            identifier = _coerce_int(candidate.get("identifier"))
            magic = _coerce_int(candidate.get("magic"))
            volume = _coerce_float(candidate.get("volume"))
            position_type = _coerce_int(candidate.get("position_type") if "position_type" in candidate else candidate.get("type"))

            if (
                runtime_symbol == CANARY_RUNTIME_SYMBOL
                and (ticket == CANARY_TICKET_IDENTIFIER or identifier == CANARY_TICKET_IDENTIFIER)
                and (magic in {None, CANARY_MAGIC})
                and (volume is None or abs(volume - CANARY_VOLUME) <= 1e-9)
                and (position_type is None or position_type == CANARY_POSITION_TYPE)
            ):
                best_match = candidate
                break
        if best_match is not None:
            break

    aggregate_canary_state = None
    if aggregate_record is not None:
        for candidate in _find_dicts(aggregate_record):
            if candidate.get("canary_state") in {"OBSERVED_EXACT_KNOWN_CANARY", "NOT_OBSERVED"}:
                aggregate_canary_state = candidate.get("canary_state")
                break

    identity_referenced_in_canary_supervision = all(
        [
            any(_contains_scalar(record, CANARY_TICKET_IDENTIFIER) for record in canary_records),
            any(_contains_scalar(record, CANARY_RUNTIME_SYMBOL) for record in canary_records),
            any(_contains_scalar(record, CANARY_MAGIC) for record in canary_records),
        ]
    )

    observed = best_match is not None
    state = "OBSERVED_EXACT_KNOWN_CANARY" if observed else "NOT_OBSERVED_OR_NOT_EXTRACTED"

    if aggregate_canary_state == "NOT_OBSERVED" and not observed:
        state = "NOT_OBSERVED"

    return {
        "state": state,
        "observed": observed,
        "identity_referenced_in_canary_supervision": identity_referenced_in_canary_supervision,
        "aggregate_canary_state": aggregate_canary_state,
        "expected_identity": {
            "server": EXPECTED_SERVER,
            "account_currency": EXPECTED_ACCOUNT_CURRENCY,
            "runtime_symbol": CANARY_RUNTIME_SYMBOL,
            "model_symbol": CANARY_MODEL_SYMBOL,
            "ticket_or_identifier": CANARY_TICKET_IDENTIFIER,
            "entry_deal": CANARY_ENTRY_DEAL,
            "magic": CANARY_MAGIC,
            "volume": CANARY_VOLUME,
            "side": CANARY_SIDE,
            "position_type": CANARY_POSITION_TYPE,
            "open_price": CANARY_OPEN_PRICE,
            "stop_loss": CANARY_STOP_LOSS,
        },
        "observed_identity": _plain(best_match) if best_match is not None else None,
    }


def _extract_first_value(records: list[Mapping[str, Any]], key: str) -> Any:
    for record in records:
        for candidate in _find_dicts(record):
            if key in candidate:
                return candidate[key]
    return None


def _summarize_canary_supervision(records: list[Mapping[str, Any]], runner_packet: Mapping[str, Any] | None = None) -> dict[str, Any]:
    verdicts = [record.get("verdict") for record in records if isinstance(record, Mapping)]
    embedded_violations = []
    for record in records:
        record_violations = record.get("violations")
        if isinstance(record_violations, list):
            embedded_violations.extend(record_violations)

    runner_succeeded = None
    verifier_succeeded = None
    report_exists = None
    if runner_packet is not None:
        runner_succeeded = bool((runner_packet.get("runner_result") or {}).get("succeeded"))
        verifier = runner_packet.get("verifier_result")
        verifier_succeeded = None if verifier is None else bool(verifier.get("succeeded"))
        report_exists = bool(runner_packet.get("report_exists"))

    return {
        "record_count": len(records),
        "verdicts": verdicts,
        "all_records_passed": bool(records) and all(verdict == "PASS" for verdict in verdicts),
        "embedded_violation_count": len(embedded_violations),
        "operator_next_action": _extract_first_value(records, "operator_next_action"),
        "completed_stages": _extract_first_value(records, "completed_stages"),
        "total_stages": _extract_first_value(records, "total_stages"),
        "first_failed_stage": _extract_first_value(records, "first_failed_stage"),
        "broker_mutation_authorized": _extract_first_value(records, "broker_mutation_authorized"),
        "trading_loop_authorized": _extract_first_value(records, "trading_loop_authorized"),
        "runner_invoked": runner_packet.get("runner_invoked") if runner_packet is not None else False,
        "runner_succeeded": runner_succeeded,
        "verifier_succeeded": verifier_succeeded,
        "report_exists": report_exists,
    }


def _summarize_runtime_aggregate(record: Mapping[str, Any] | None) -> dict[str, Any]:
    if record is None:
        return {
            "present": False,
            "verdict": None,
            "operator_state": None,
            "embedded_violation_count": None,
            "upstream_summaries": [],
        }

    embedded_violations = record.get("violations", [])
    return {
        "present": True,
        "packet_type": record.get("packet_type"),
        "verdict": record.get("verdict"),
        "operator_state": record.get("operator_state"),
        "effective_new_entries_blocked": record.get("effective_new_entries_blocked"),
        "embedded_violation_count": len(embedded_violations) if isinstance(embedded_violations, list) else None,
        "upstream_summaries": _plain(record.get("upstream_summaries", [])),
    }


def collect_h024_unified_read_only_post_canary_runtime_supervision(
    *,
    mt5_client: Any | None = None,
    canary_supervision_records: list[Mapping[str, Any]] | None = None,
    runtime_safety_aggregate_record: Mapping[str, Any] | None = None,
    invoke_canary_runner: bool = True,
    expected_server: str = EXPECTED_SERVER,
    expected_currency: str = EXPECTED_ACCOUNT_CURRENCY,
) -> dict[str, Any]:
    """Collect one operator-facing read-only post-canary runtime supervision packet.

    This packet combines the existing H024 one-shot canary read-only supervision
    runner with the runtime safety aggregate supervisor. It does not authorize
    broker mutation, order_check, order_send, entry, close/modify, USDJPY order,
    XAUUSD new order, or a trading loop.
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
                    "message": f"Unified post-canary runtime supervision check failed: {name}",
                    "detail": _plain(detail),
                    "fail_closed": True,
                }
            )

    lockout_reference = _module_reference(LOCKOUT_READER_MODULE)
    runtime_aggregate_reference = _module_reference(RUNTIME_AGGREGATE_MODULE)
    canary_runner_reference = _script_reference(CANARY_RUNNER_SCRIPT)
    canary_verifier_reference = _script_reference(CANARY_VERIFIER_SCRIPT)

    add_check("runtime_lockout_reader_referenced", lockout_reference.get("module_importable") is True, lockout_reference)
    add_check("runtime_safety_aggregate_module_referenced", runtime_aggregate_reference.get("module_importable") is True, runtime_aggregate_reference)
    add_check("canary_read_only_runner_script_referenced", canary_runner_reference.get("script_exists") is True, canary_runner_reference)
    add_check("canary_read_only_verifier_script_referenced", canary_verifier_reference.get("script_exists") is True, canary_verifier_reference)

    canary_runner_packet: dict[str, Any] | None = None
    if canary_supervision_records is None:
        if invoke_canary_runner:
            canary_runner_packet = _run_canary_read_only_supervision_and_verify()
            canary_supervision_records = canary_runner_packet["records"]
        else:
            canary_supervision_records = []

    canary_records = [dict(record) for record in canary_supervision_records]
    canary_summary = _summarize_canary_supervision(canary_records, canary_runner_packet)

    add_check(
        "canary_supervision_records_present",
        len(canary_records) > 0,
        {"record_count": len(canary_records)},
    )
    add_check(
        "canary_supervision_verdict_pass",
        canary_summary["all_records_passed"] is True,
        canary_summary,
    )
    add_check(
        "canary_supervision_embedded_violations_absent",
        canary_summary["embedded_violation_count"] == 0,
        {"embedded_violation_count": canary_summary["embedded_violation_count"]},
    )
    if canary_runner_packet is not None:
        add_check(
            "canary_runner_invocation_succeeded",
            bool((canary_runner_packet.get("runner_result") or {}).get("succeeded")),
            canary_runner_packet.get("runner_result"),
        )
        add_check(
            "canary_verifier_invocation_succeeded",
            bool((canary_runner_packet.get("verifier_result") or {}).get("succeeded")),
            canary_runner_packet.get("verifier_result"),
        )

    if runtime_safety_aggregate_record is None:
        runtime_safety_aggregate_record = collect_h024_runtime_safety_aggregate_supervisor(
            mt5_client=mt5_client,
            expected_server=expected_server,
            expected_currency=expected_currency,
        )

    runtime_aggregate = dict(runtime_safety_aggregate_record)
    runtime_aggregate_summary = _summarize_runtime_aggregate(runtime_aggregate)

    add_check(
        "runtime_safety_aggregate_present",
        runtime_aggregate_summary["present"] is True,
        runtime_aggregate_summary,
    )
    add_check(
        "runtime_safety_aggregate_packet_type_expected",
        runtime_aggregate.get("packet_type") == RUNTIME_SAFETY_AGGREGATE_PACKET_TYPE,
        {"expected": RUNTIME_SAFETY_AGGREGATE_PACKET_TYPE, "observed": runtime_aggregate.get("packet_type")},
    )
    add_check(
        "runtime_safety_aggregate_verdict_pass",
        runtime_aggregate.get("verdict") == "PASS",
        runtime_aggregate_summary,
    )
    add_check(
        "runtime_safety_aggregate_embedded_violations_absent",
        runtime_aggregate_summary["embedded_violation_count"] == 0,
        {"embedded_violation_count": runtime_aggregate_summary["embedded_violation_count"]},
    )
    add_check(
        "runtime_safety_aggregate_effectively_blocks_entries",
        runtime_aggregate.get("effective_new_entries_blocked") is True,
        {"observed": runtime_aggregate.get("effective_new_entries_blocked")},
    )

    canary_identity = _extract_exact_canary_observation(
        aggregate_record=runtime_aggregate,
        canary_records=canary_records,
    )

    add_check(
        "canary_identity_state_coherent",
        canary_identity["state"] in {"OBSERVED_EXACT_KNOWN_CANARY", "NOT_OBSERVED", "NOT_OBSERVED_OR_NOT_EXTRACTED"},
        canary_identity,
    )
    add_check(
        "observed_canary_identity_exact_when_present",
        canary_identity["state"] != "OBSERVED_EXACT_KNOWN_CANARY"
        or (
            canary_identity["observed"] is True
            and canary_identity["expected_identity"]["ticket_or_identifier"] == CANARY_TICKET_IDENTIFIER
            and canary_identity["expected_identity"]["runtime_symbol"] == CANARY_RUNTIME_SYMBOL
            and canary_identity["expected_identity"]["magic"] == CANARY_MAGIC
            and canary_identity["expected_identity"]["volume"] == CANARY_VOLUME
        ),
        canary_identity,
    )

    authorizations = _false_authorizations()
    authorization_violations = _authorization_violations(authorizations)
    violations.extend(authorization_violations)
    add_check("all_runtime_authorizations_false", not authorization_violations, authorizations)

    verdict = "PASS" if not violations else "FAIL"
    operator_next_action = (
        "READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED"
        if verdict == "PASS"
        else "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "server": expected_server,
            "account_currency": expected_currency,
            "known_canary_identity": {
                "runtime_symbol": CANARY_RUNTIME_SYMBOL,
                "model_symbol": CANARY_MODEL_SYMBOL,
                "ticket_or_identifier": CANARY_TICKET_IDENTIFIER,
                "entry_deal": CANARY_ENTRY_DEAL,
                "magic": CANARY_MAGIC,
                "volume": CANARY_VOLUME,
                "side": CANARY_SIDE,
                "position_type": CANARY_POSITION_TYPE,
                "open_price": CANARY_OPEN_PRICE,
                "stop_loss": CANARY_STOP_LOSS,
            },
        },
        "references": {
            "lockout_reader_reference": lockout_reference,
            "canary_runner_reference": canary_runner_reference,
            "canary_verifier_reference": canary_verifier_reference,
            "runtime_safety_aggregate_reference": runtime_aggregate_reference,
        },
        "canary_read_only_supervision": {
            "runner_packet": _plain(canary_runner_packet),
            "summary": canary_summary,
            "records": _plain(canary_records),
        },
        "runtime_safety_aggregate": {
            "summary": runtime_aggregate_summary,
            "record": _plain(runtime_aggregate),
        },
        "exact_known_canary": canary_identity,
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
        "operator_next_action": operator_next_action,
        "operator_state": (
            "UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED"
            if verdict == "PASS"
            else "FAIL_CLOSED_UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_BLOCKED"
        ),
        "violations": violations,
        "verdict": verdict,
    }


def verify_h024_unified_read_only_post_canary_runtime_supervision_records(
    records: list[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    verification_violations: list[dict[str, Any]] = []

    if not records:
        verification_violations.append(
            {
                "code": "NO_RECORDS",
                "message": "No H024 unified post-canary runtime supervision records were found.",
                "fail_closed": True,
            }
        )

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_SCHEMA_VERSION",
                    "message": "Unified supervision record has an unexpected schema version.",
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
                    "message": "Unified supervision record has an unexpected strategy.",
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
                    "message": "Unified supervision record has an unexpected packet type.",
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
                    "message": "Unified supervision authorizations field is not an object.",
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
                    "message": "Unified supervision must keep effective_new_entries_blocked true.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        canary_section = record.get("canary_read_only_supervision")
        if not isinstance(canary_section, Mapping):
            verification_violations.append(
                {
                    "code": "CANARY_SUPERVISION_SECTION_MISSING",
                    "message": "Unified supervision record is missing canary read-only supervision section.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            canary_summary = canary_section.get("summary")
            if not isinstance(canary_summary, Mapping):
                verification_violations.append(
                    {
                        "code": "CANARY_SUPERVISION_SUMMARY_MISSING",
                        "message": "Unified supervision record is missing canary supervision summary.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            else:
                if canary_summary.get("record_count", 0) <= 0:
                    verification_violations.append(
                        {
                            "code": "CANARY_SUPERVISION_RECORDS_MISSING",
                            "message": "Canary supervision records are missing.",
                            "record_index": index,
                            "fail_closed": True,
                        }
                    )
                if require_pass and canary_summary.get("all_records_passed") is not True:
                    verification_violations.append(
                        {
                            "code": "CANARY_SUPERVISION_NOT_PASS",
                            "message": "Require-pass mode requires canary supervision PASS.",
                            "record_index": index,
                            "summary": _plain(canary_summary),
                            "fail_closed": True,
                        }
                    )
                if canary_summary.get("embedded_violation_count") not in {0, None}:
                    verification_violations.append(
                        {
                            "code": "CANARY_SUPERVISION_EMBEDDED_VIOLATIONS",
                            "message": "Canary supervision contains embedded violations.",
                            "record_index": index,
                            "summary": _plain(canary_summary),
                            "fail_closed": True,
                        }
                    )

        aggregate_section = record.get("runtime_safety_aggregate")
        if not isinstance(aggregate_section, Mapping):
            verification_violations.append(
                {
                    "code": "RUNTIME_AGGREGATE_SECTION_MISSING",
                    "message": "Unified supervision record is missing runtime safety aggregate section.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            aggregate_record = aggregate_section.get("record")
            if not isinstance(aggregate_record, Mapping):
                verification_violations.append(
                    {
                        "code": "RUNTIME_AGGREGATE_RECORD_MISSING",
                        "message": "Unified supervision record is missing runtime safety aggregate record.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            else:
                if aggregate_record.get("packet_type") != RUNTIME_SAFETY_AGGREGATE_PACKET_TYPE:
                    verification_violations.append(
                        {
                            "code": "UNEXPECTED_RUNTIME_AGGREGATE_PACKET_TYPE",
                            "message": "Runtime aggregate packet type is unexpected.",
                            "record_index": index,
                            "observed": _plain(aggregate_record.get("packet_type")),
                            "expected": RUNTIME_SAFETY_AGGREGATE_PACKET_TYPE,
                            "fail_closed": True,
                        }
                    )
                if require_pass and aggregate_record.get("verdict") != "PASS":
                    verification_violations.append(
                        {
                            "code": "RUNTIME_AGGREGATE_NOT_PASS",
                            "message": "Require-pass mode requires runtime safety aggregate PASS.",
                            "record_index": index,
                            "observed": _plain(aggregate_record.get("verdict")),
                            "fail_closed": True,
                        }
                    )
                if aggregate_record.get("effective_new_entries_blocked") is not True:
                    verification_violations.append(
                        {
                            "code": "RUNTIME_AGGREGATE_DOES_NOT_BLOCK_ENTRIES",
                            "message": "Runtime aggregate must preserve effective_new_entries_blocked true.",
                            "record_index": index,
                            "fail_closed": True,
                        }
                    )

        exact_canary = record.get("exact_known_canary")
        if not isinstance(exact_canary, Mapping):
            verification_violations.append(
                {
                    "code": "EXACT_CANARY_SECTION_MISSING",
                    "message": "Unified supervision record is missing exact canary section.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            state = exact_canary.get("state")
            if state not in {"OBSERVED_EXACT_KNOWN_CANARY", "NOT_OBSERVED", "NOT_OBSERVED_OR_NOT_EXTRACTED"}:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_CANARY_STATE",
                        "message": "Unified supervision exact canary state is unexpected.",
                        "record_index": index,
                        "observed": _plain(state),
                        "fail_closed": True,
                    }
                )
            if state == "OBSERVED_EXACT_KNOWN_CANARY":
                expected_identity = exact_canary.get("expected_identity")
                if not isinstance(expected_identity, Mapping):
                    verification_violations.append(
                        {
                            "code": "EXACT_CANARY_EXPECTED_IDENTITY_MISSING",
                            "message": "Observed canary state requires expected identity details.",
                            "record_index": index,
                            "fail_closed": True,
                        }
                    )
                else:
                    if expected_identity.get("ticket_or_identifier") != CANARY_TICKET_IDENTIFIER:
                        verification_violations.append(
                            {
                                "code": "EXACT_CANARY_TICKET_MISMATCH",
                                "message": "Exact canary ticket/identifier mismatch.",
                                "record_index": index,
                                "observed": _plain(expected_identity.get("ticket_or_identifier")),
                                "expected": CANARY_TICKET_IDENTIFIER,
                                "fail_closed": True,
                            }
                        )

        embedded_violations = record.get("violations", [])
        if record.get("verdict") == "PASS" and embedded_violations:
            verification_violations.append(
                {
                    "code": "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS",
                    "message": "Unified supervision record verdict is PASS but embedded violations are present.",
                    "record_index": index,
                    "embedded_violation_count": len(embedded_violations),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("verdict") != "PASS":
            verification_violations.append(
                {
                    "code": "RECORD_VERDICT_NOT_PASS",
                    "message": "Unified supervision record verdict is not PASS.",
                    "record_index": index,
                    "observed": _plain(record.get("verdict")),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("operator_next_action") != "READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED":
            verification_violations.append(
                {
                    "code": "UNEXPECTED_OPERATOR_NEXT_ACTION",
                    "message": "Unified supervision operator next action is not the read-only continue-supervision action.",
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
    return _read_jsonl(Path(path))


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or verify H024 unified read-only post-canary runtime supervision JSONL.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    return parser


__all__ = [
    "DEFAULT_OUTPUT_PATH",
    "PACKET_TYPE",
    "SCHEMA_VERSION",
    "STRATEGY_ID",
    "collect_h024_unified_read_only_post_canary_runtime_supervision",
    "read_jsonl",
    "verify_h024_unified_read_only_post_canary_runtime_supervision_records",
    "write_jsonl",
]