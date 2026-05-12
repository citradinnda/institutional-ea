from __future__ import annotations

import argparse
import importlib
import json
import math
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from quantcore.execution.h024_runtime_account_risk_margin_safety_supervisor import (
    PACKET_TYPE as ACCOUNT_RISK_MARGIN_PACKET_TYPE,
    collect_h024_runtime_account_risk_margin_safety_supervisor,
)
from quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor import (
    PACKET_TYPE as EXPOSURE_INVENTORY_PACKET_TYPE,
    collect_h024_runtime_exposure_inventory_safety_supervisor,
)
from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
    PACKET_TYPE as HEARTBEAT_PACKET_TYPE,
    collect_h024_runtime_safety_heartbeat,
)
from quantcore.execution.h024_runtime_tick_spread_safety_supervisor import (
    PACKET_TYPE as TICK_SPREAD_PACKET_TYPE,
    collect_h024_runtime_tick_spread_safety_supervisor,
)

STRATEGY_ID = "H024"
PACKET_TYPE = "H024_RUNTIME_SAFETY_AGGREGATE_SUPERVISOR"
SCHEMA_VERSION = 1

LOCKOUT_READER_MODULE = "quantcore.execution.h024_runtime_safety_lockout"
HEARTBEAT_MODULE = "quantcore.execution.h024_runtime_safety_heartbeat"
TICK_SPREAD_MODULE = "quantcore.execution.h024_runtime_tick_spread_safety_supervisor"
EXPOSURE_INVENTORY_MODULE = "quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor"
ACCOUNT_RISK_MARGIN_MODULE = "quantcore.execution.h024_runtime_account_risk_margin_safety_supervisor"

DEFAULT_OUTPUT_PATH = Path("reports") / "h024_runtime_safety_aggregate_supervisor.jsonl"
DEFAULT_MAX_UPSTREAM_PACKET_AGE_SECONDS = 300.0
FUTURE_PACKET_TOLERANCE_SECONDS = 60.0

UPSTREAM_PACKET_TYPES: dict[str, str] = {
    "runtime_safety_heartbeat": HEARTBEAT_PACKET_TYPE,
    "runtime_tick_spread_safety_supervisor": TICK_SPREAD_PACKET_TYPE,
    "runtime_exposure_inventory_safety_supervisor": EXPOSURE_INVENTORY_PACKET_TYPE,
    "runtime_account_risk_margin_safety_supervisor": ACCOUNT_RISK_MARGIN_PACKET_TYPE,
}


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _utc_now_iso() -> str:
    return _utc_now().isoformat().replace("+00:00", "Z")


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


def _parse_observed_at_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
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


def _upstream_authorizations_false(record: Mapping[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    authorization_map = record.get("authorizations")
    if not isinstance(authorization_map, Mapping):
        violations.append(
            {
                "code": "UPSTREAM_AUTHORIZATIONS_NOT_OBJECT",
                "message": "Upstream packet authorizations field is not an object.",
                "fail_closed": True,
            }
        )
    else:
        violations.extend(_authorization_violations(authorization_map))

    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        if record.get(key) is not False:
            violations.append(
                {
                    "code": "UPSTREAM_TOP_LEVEL_UNSAFE_AUTHORIZATION",
                    "message": f"Upstream top-level forbidden authorization is not false: {key}",
                    "field": key,
                    "observed": _plain(record.get(key)),
                    "fail_closed": True,
                }
            )
    return violations


def _evaluate_upstream_record(
    *,
    source: str,
    record: Any,
    expected_packet_type: str,
    now_utc: datetime,
    max_age_seconds: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
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
                    "message": f"Aggregate upstream check failed for {source}: {name}",
                    "source": source,
                    "detail": _plain(detail),
                    "fail_closed": True,
                }
            )

    is_mapping = isinstance(record, Mapping)
    add_check("upstream_record_object", is_mapping, {"type": type(record).__name__})
    if not is_mapping:
        return (
            {
                "source": source,
                "expected_packet_type": expected_packet_type,
                "observed_packet_type": None,
                "observed_at_utc": None,
                "age_seconds": None,
                "verdict": None,
                "embedded_violation_count": None,
                "checks": checks,
                "violations": violations,
            },
            violations,
        )

    observed_packet_type = record.get("packet_type")
    observed_strategy = record.get("strategy")
    observed_verdict = record.get("verdict")
    observed_at = record.get("observed_at_utc")
    observed_dt = _parse_observed_at_utc(observed_at)
    age_seconds = None
    if observed_dt is not None:
        age_seconds = (now_utc - observed_dt).total_seconds()

    add_check(
        "upstream_strategy_expected",
        observed_strategy == STRATEGY_ID,
        {"expected": STRATEGY_ID, "observed": observed_strategy},
    )
    add_check(
        "upstream_packet_type_expected",
        observed_packet_type == expected_packet_type,
        {"expected": expected_packet_type, "observed": observed_packet_type},
    )
    add_check(
        "upstream_verdict_pass",
        observed_verdict == "PASS",
        {"observed": observed_verdict},
    )
    add_check(
        "upstream_observed_at_parseable",
        observed_dt is not None,
        {"observed_at_utc": observed_at},
    )
    add_check(
        "upstream_packet_fresh",
        age_seconds is not None and -FUTURE_PACKET_TOLERANCE_SECONDS <= age_seconds <= max_age_seconds,
        {
            "observed_at_utc": observed_at,
            "age_seconds": age_seconds,
            "max_age_seconds": max_age_seconds,
            "future_tolerance_seconds": FUTURE_PACKET_TOLERANCE_SECONDS,
        },
    )
    add_check(
        "upstream_effective_new_entries_blocked",
        record.get("effective_new_entries_blocked") is True,
        {"observed": record.get("effective_new_entries_blocked")},
    )

    auth_violations = _upstream_authorizations_false(record)
    for violation in auth_violations:
        violation["source"] = source
    violations.extend(auth_violations)
    add_check("upstream_authorizations_false", not auth_violations, {"violation_count": len(auth_violations)})

    embedded_violations = record.get("violations", [])
    embedded_violation_count = len(embedded_violations) if isinstance(embedded_violations, list) else None
    embedded_passed = isinstance(embedded_violations, list) and embedded_violation_count == 0
    add_check(
        "upstream_embedded_violations_absent",
        embedded_passed,
        {"embedded_violation_count": embedded_violation_count},
    )
    if isinstance(embedded_violations, list):
        for embedded in embedded_violations:
            violations.append(
                {
                    "code": "UPSTREAM_EMBEDDED_VIOLATION",
                    "message": f"Upstream packet {source} contains an embedded violation.",
                    "source": source,
                    "upstream_violation": _plain(embedded),
                    "fail_closed": True,
                }
            )

    return (
        {
            "source": source,
            "expected_packet_type": expected_packet_type,
            "observed_packet_type": observed_packet_type,
            "observed_at_utc": observed_at,
            "age_seconds": age_seconds,
            "verdict": observed_verdict,
            "embedded_violation_count": embedded_violation_count,
            "checks": checks,
            "violations": violations,
        },
        violations,
    )


def collect_h024_runtime_safety_aggregate_supervisor(
    *,
    mt5_client: Any | None = None,
    expected_server: str = EXPECTED_SERVER,
    expected_currency: str = EXPECTED_ACCOUNT_CURRENCY,
    max_upstream_packet_age_seconds: float = DEFAULT_MAX_UPSTREAM_PACKET_AGE_SECONDS,
) -> dict[str, Any]:
    """Collect a read-only aggregate runtime safety supervisor packet.

    The aggregate supervisor consumes the upstream read-only runtime safety
    packets and produces one fail-closed operator verdict. It never calls
    order_check, order_send, symbol_select, entry, close, modify, or a trading
    loop.
    """

    observed_at_utc = _utc_now_iso()
    now_utc = _utc_now()

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
                    "message": f"Runtime safety aggregate supervisor check failed: {name}",
                    "detail": _plain(detail),
                    "fail_closed": True,
                }
            )

    if mt5_client is None:
        try:
            mt5_client = importlib.import_module("MetaTrader5")
            add_check("mt5_module_importable", True, {"module": "MetaTrader5"})
        except Exception as exc:
            mt5_client = None
            add_check("mt5_module_importable", False, {"error": repr(exc)})
    else:
        add_check("mt5_client_injected", True, {"client_type": type(mt5_client).__name__})

    lockout_reference = _module_reference(LOCKOUT_READER_MODULE)
    heartbeat_reference = _module_reference(HEARTBEAT_MODULE)
    tick_spread_reference = _module_reference(TICK_SPREAD_MODULE)
    exposure_inventory_reference = _module_reference(EXPOSURE_INVENTORY_MODULE)
    account_risk_margin_reference = _module_reference(ACCOUNT_RISK_MARGIN_MODULE)

    add_check("runtime_lockout_reader_referenced", lockout_reference.get("module_importable") is True, lockout_reference)
    add_check("runtime_heartbeat_packet_referenced", heartbeat_reference.get("module_importable") is True, heartbeat_reference)
    add_check("runtime_tick_spread_packet_referenced", tick_spread_reference.get("module_importable") is True, tick_spread_reference)
    add_check(
        "runtime_exposure_inventory_packet_referenced",
        exposure_inventory_reference.get("module_importable") is True,
        exposure_inventory_reference,
    )
    add_check(
        "runtime_account_risk_margin_packet_referenced",
        account_risk_margin_reference.get("module_importable") is True,
        account_risk_margin_reference,
    )

    heartbeat_record = collect_h024_runtime_safety_heartbeat(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )
    tick_spread_record = collect_h024_runtime_tick_spread_safety_supervisor(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )
    exposure_inventory_record = collect_h024_runtime_exposure_inventory_safety_supervisor(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )
    account_risk_margin_record = collect_h024_runtime_account_risk_margin_safety_supervisor(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )

    upstream_records: dict[str, Any] = {
        "runtime_safety_heartbeat": heartbeat_record,
        "runtime_tick_spread_safety_supervisor": tick_spread_record,
        "runtime_exposure_inventory_safety_supervisor": exposure_inventory_record,
        "runtime_account_risk_margin_safety_supervisor": account_risk_margin_record,
    }

    upstream_summaries: list[dict[str, Any]] = []
    for source, expected_packet_type in UPSTREAM_PACKET_TYPES.items():
        summary, upstream_violations = _evaluate_upstream_record(
            source=source,
            record=upstream_records.get(source),
            expected_packet_type=expected_packet_type,
            now_utc=now_utc,
            max_age_seconds=max_upstream_packet_age_seconds,
        )
        upstream_summaries.append(summary)
        violations.extend(upstream_violations)

    upstream_all_passed = all(summary.get("verdict") == "PASS" and not summary.get("violations") for summary in upstream_summaries)
    add_check(
        "all_upstream_packets_passed",
        upstream_all_passed,
        {
            "upstream_count": len(upstream_summaries),
            "failed_sources": [
                summary.get("source")
                for summary in upstream_summaries
                if summary.get("verdict") != "PASS" or summary.get("violations")
            ],
        },
    )

    authorizations = _false_authorizations()
    authorization_violations = _authorization_violations(authorizations)
    violations.extend(authorization_violations)
    add_check("all_runtime_authorizations_false", not authorization_violations, authorizations)

    verdict = "PASS" if not violations else "FAIL"
    operator_state = (
        "RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED"
        if verdict == "PASS"
        else "FAIL_CLOSED_RUNTIME_SAFETY_AGGREGATE_BLOCKED"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "server": expected_server,
            "account_currency": expected_currency,
            "max_upstream_packet_age_seconds": max_upstream_packet_age_seconds,
            "required_upstream_packet_types": dict(UPSTREAM_PACKET_TYPES),
        },
        "module_references": {
            "lockout_reader_reference": lockout_reference,
            "heartbeat_reference": heartbeat_reference,
            "tick_spread_reference": tick_spread_reference,
            "exposure_inventory_reference": exposure_inventory_reference,
            "account_risk_margin_reference": account_risk_margin_reference,
        },
        "upstream_records": _plain(upstream_records),
        "upstream_summaries": upstream_summaries,
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
        "violations": violations,
        "verdict": verdict,
    }


def verify_h024_runtime_safety_aggregate_supervisor_records(
    records: list[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    verification_violations: list[dict[str, Any]] = []
    now_utc = _utc_now()

    if not records:
        verification_violations.append(
            {
                "code": "NO_RECORDS",
                "message": "No H024 runtime safety aggregate supervisor records were found.",
                "fail_closed": True,
            }
        )

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_SCHEMA_VERSION",
                    "message": "Runtime safety aggregate record has an unexpected schema version.",
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
                    "message": "Runtime safety aggregate record has an unexpected strategy.",
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
                    "message": "Runtime safety aggregate record has an unexpected packet type.",
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
                    "message": "Runtime safety aggregate authorizations field is not an object.",
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
                    "message": "Runtime safety aggregate must keep effective_new_entries_blocked true.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        upstream_records = record.get("upstream_records")
        if not isinstance(upstream_records, Mapping):
            verification_violations.append(
                {
                    "code": "UPSTREAM_RECORDS_NOT_OBJECT",
                    "message": "Runtime safety aggregate upstream_records field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            for source, expected_packet_type in UPSTREAM_PACKET_TYPES.items():
                if source not in upstream_records:
                    verification_violations.append(
                        {
                            "code": "UPSTREAM_PACKET_MISSING",
                            "message": "Required upstream packet is missing from aggregate record.",
                            "record_index": index,
                            "source": source,
                            "expected_packet_type": expected_packet_type,
                            "fail_closed": True,
                        }
                    )
                    continue

                upstream_record = upstream_records.get(source)
                summary, upstream_violations = _evaluate_upstream_record(
                    source=source,
                    record=upstream_record,
                    expected_packet_type=expected_packet_type,
                    now_utc=now_utc,
                    max_age_seconds=DEFAULT_MAX_UPSTREAM_PACKET_AGE_SECONDS,
                )
                for violation in upstream_violations:
                    verification_violations.append(
                        {
                            **violation,
                            "record_index": index,
                            "aggregate_source": source,
                        }
                    )
                if require_pass and summary.get("verdict") != "PASS":
                    verification_violations.append(
                        {
                            "code": "UPSTREAM_VERDICT_NOT_PASS",
                            "message": "Require-pass mode requires every upstream packet verdict PASS.",
                            "record_index": index,
                            "source": source,
                            "observed": _plain(summary.get("verdict")),
                            "fail_closed": True,
                        }
                    )

        upstream_summaries = record.get("upstream_summaries")
        if not isinstance(upstream_summaries, list):
            verification_violations.append(
                {
                    "code": "UPSTREAM_SUMMARIES_NOT_LIST",
                    "message": "Runtime safety aggregate upstream_summaries field is not a list.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        module_references = record.get("module_references")
        if not isinstance(module_references, Mapping):
            verification_violations.append(
                {
                    "code": "MODULE_REFERENCES_NOT_OBJECT",
                    "message": "Runtime safety aggregate module_references field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            for key in (
                "lockout_reader_reference",
                "heartbeat_reference",
                "tick_spread_reference",
                "exposure_inventory_reference",
                "account_risk_margin_reference",
            ):
                reference = module_references.get(key)
                if not isinstance(reference, Mapping) or reference.get("module_importable") is not True:
                    verification_violations.append(
                        {
                            "code": "MODULE_REFERENCE_NOT_IMPORTABLE",
                            "message": "Required runtime safety module reference is missing or not importable.",
                            "record_index": index,
                            "reference_key": key,
                            "reference": _plain(reference),
                            "fail_closed": True,
                        }
                    )

        embedded_violations = record.get("violations", [])
        if record.get("verdict") == "PASS" and embedded_violations:
            verification_violations.append(
                {
                    "code": "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS",
                    "message": "Runtime safety aggregate record verdict is PASS but embedded violations are present.",
                    "record_index": index,
                    "embedded_violation_count": len(embedded_violations),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("verdict") != "PASS":
            verification_violations.append(
                {
                    "code": "RECORD_VERDICT_NOT_PASS",
                    "message": "Runtime safety aggregate record verdict is not PASS.",
                    "record_index": index,
                    "observed": _plain(record.get("verdict")),
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
                raise ValueError(f"Malformed JSONL at line {line_number}: {exc}") from exc
    return records


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or verify H024 runtime safety aggregate supervisor JSONL.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    return parser


__all__ = [
    "DEFAULT_MAX_UPSTREAM_PACKET_AGE_SECONDS",
    "DEFAULT_OUTPUT_PATH",
    "PACKET_TYPE",
    "SCHEMA_VERSION",
    "STRATEGY_ID",
    "UPSTREAM_PACKET_TYPES",
    "collect_h024_runtime_safety_aggregate_supervisor",
    "read_jsonl",
    "verify_h024_runtime_safety_aggregate_supervisor_records",
    "write_jsonl",
]