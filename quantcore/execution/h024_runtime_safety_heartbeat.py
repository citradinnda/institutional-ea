from __future__ import annotations

import argparse
import importlib
import json
import time
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STRATEGY_ID = "H024"
PACKET_TYPE = "H024_RUNTIME_SAFETY_HEARTBEAT"
SCHEMA_VERSION = 1

EXPECTED_SERVER = "Exness-MT5Trial6"
EXPECTED_ACCOUNT_CURRENCY = "USD"

LOCKOUT_READER_MODULE = "quantcore.execution.h024_runtime_safety_lockout"
DEFAULT_LOCKOUT_CONFIG_PATH = Path("config") / "h024_runtime_safety" / "default_lockout_config.json"

FORBIDDEN_AUTHORIZATION_KEYS = (
    "broker_mutation_authorized",
    "order_check_authorized",
    "order_send_authorized",
    "entry_authorized",
    "close_modify_authorized",
    "xauusd_order_authorized",
    "usdjpy_order_authorized",
    "trading_loop_authorized",
    "automatic_execution_authorized",
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _plain(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
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


def _field(value: Any, name: str) -> Any:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return value.get(name)
    return getattr(value, name, None)


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


def _safe_call(client: Any, method_name: str) -> tuple[Any, str | None]:
    method = getattr(client, method_name, None)
    if method is None:
        return None, f"missing method: {method_name}"
    try:
        return method(), None
    except Exception as exc:  # pragma: no cover - defensive runtime boundary
        return None, repr(exc)


def _build_lockout_reader_reference(lockout_config_path: Path) -> dict[str, Any]:
    reference: dict[str, Any] = {
        "reader_module": LOCKOUT_READER_MODULE,
        "reader_module_importable": False,
        "config_path": str(lockout_config_path),
        "config_path_exists": False,
        "adapter_mode": "import_and_config_reference",
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
    }

    try:
        module = importlib.import_module(LOCKOUT_READER_MODULE)
        reference["reader_module_importable"] = True
        reference["reader_module_file"] = getattr(module, "__file__", None)
        reference["module_default_config_path"] = str(getattr(module, "DEFAULT_CONFIG_PATH", ""))
    except Exception as exc:
        reference["reader_module_error"] = repr(exc)

    reference["config_path_exists"] = lockout_config_path.exists()
    return reference


def collect_h024_runtime_safety_heartbeat(
    *,
    mt5_client: Any | None = None,
    expected_server: str = EXPECTED_SERVER,
    expected_currency: str = EXPECTED_ACCOUNT_CURRENCY,
    lockout_config_path: str | Path = DEFAULT_LOCKOUT_CONFIG_PATH,
    max_collection_elapsed_seconds: float = 5.0,
) -> dict[str, Any]:
    """Collect a read-only H024 runtime safety heartbeat.

    This function may initialize/read the MetaTrader5 Python bridge, but it never
    calls order_check, order_send, position modification, close, entry, or any
    trading-loop function.
    """

    started_monotonic = time.monotonic()
    observed_at_utc = _utc_now_iso()
    lockout_config = Path(lockout_config_path)

    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: Any = None) -> None:
        check = {
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "passed": bool(passed),
            "detail": _plain(detail),
            "fail_closed_on_failure": True,
        }
        checks.append(check)
        if not passed:
            violations.append(
                {
                    "code": name.upper(),
                    "message": f"Heartbeat check failed: {name}",
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

    initialize_result = None
    initialize_error = None
    account_info = None
    account_error = None
    terminal_info = None
    terminal_error = None
    last_error = None
    version_info = None

    if mt5_client is not None:
        initialize_result, initialize_error = _safe_call(mt5_client, "initialize")
        initialize_passed = bool(initialize_result) and initialize_error is None
        add_check(
            "mt5_initialize_succeeded",
            initialize_passed,
            {"result": _plain(initialize_result), "error": initialize_error},
        )

        if initialize_passed:
            account_info, account_error = _safe_call(mt5_client, "account_info")
            terminal_info, terminal_error = _safe_call(mt5_client, "terminal_info")
            last_error, _ = _safe_call(mt5_client, "last_error")
            version_info, _ = _safe_call(mt5_client, "version")
        else:
            account_error = "mt5 initialization failed"
            terminal_error = "mt5 initialization failed"

    account_plain = _plain(account_info)
    terminal_plain = _plain(terminal_info)

    account_available = account_info is not None and account_error is None
    terminal_available = terminal_info is not None and terminal_error is None

    add_check("account_info_available", account_available, {"error": account_error, "account": account_plain})
    add_check("terminal_info_available", terminal_available, {"error": terminal_error, "terminal": terminal_plain})

    observed_server = _field(account_info, "server")
    observed_currency = _field(account_info, "currency")

    add_check(
        "account_server_expected",
        account_available and observed_server == expected_server,
        {"expected": expected_server, "observed": observed_server},
    )
    add_check(
        "account_currency_expected",
        account_available and observed_currency == expected_currency,
        {"expected": expected_currency, "observed": observed_currency},
    )

    terminal_connected = _field(terminal_info, "connected")
    add_check(
        "terminal_connected",
        terminal_available and terminal_connected is True,
        {"observed": terminal_connected, "terminal": terminal_plain},
    )

    elapsed_seconds = time.monotonic() - started_monotonic
    add_check(
        "heartbeat_collection_elapsed_fresh",
        elapsed_seconds <= max_collection_elapsed_seconds,
        {"elapsed_seconds": elapsed_seconds, "max_collection_elapsed_seconds": max_collection_elapsed_seconds},
    )

    lockout_reference = _build_lockout_reader_reference(lockout_config)
    add_check(
        "runtime_lockout_reader_referenced",
        lockout_reference["reader_module_importable"] is True and lockout_reference["config_path_exists"] is True,
        lockout_reference,
    )

    authorizations = _false_authorizations()
    authorization_violations = _authorization_violations(authorizations)
    violations.extend(authorization_violations)
    add_check("all_runtime_authorizations_false", not authorization_violations, authorizations)

    verdict = "PASS" if not violations else "FAIL"
    operator_state = (
        "RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED"
        if verdict == "PASS"
        else "FAIL_CLOSED_RUNTIME_HEARTBEAT_BLOCKED"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "server": expected_server,
            "account_currency": expected_currency,
            "lockout_config_path": str(lockout_config),
        },
        "observed": {
            "mt5_initialize_result": _plain(initialize_result),
            "mt5_initialize_error": initialize_error,
            "account": account_plain,
            "terminal": terminal_plain,
            "last_error": _plain(last_error),
            "version": _plain(version_info),
            "collection_elapsed_seconds": elapsed_seconds,
        },
        "checks": checks,
        "lockout_reader": lockout_reference,
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


def verify_h024_runtime_safety_heartbeat_records(
    records: list[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    verification_violations: list[dict[str, Any]] = []

    if not records:
        verification_violations.append(
            {
                "code": "NO_RECORDS",
                "message": "No H024 runtime safety heartbeat records were found.",
                "fail_closed": True,
            }
        )

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_SCHEMA_VERSION",
                    "message": "Heartbeat record has an unexpected schema version.",
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
                    "message": "Heartbeat record has an unexpected strategy.",
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
                    "message": "Heartbeat record has an unexpected packet type.",
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
                    "message": "Heartbeat record authorizations field is not an object.",
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
                    "message": "Heartbeat must keep effective_new_entries_blocked true.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        lockout_reader = record.get("lockout_reader")
        if not isinstance(lockout_reader, Mapping):
            verification_violations.append(
                {
                    "code": "LOCKOUT_READER_NOT_OBJECT",
                    "message": "Heartbeat lockout_reader field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            if lockout_reader.get("reader_module") != LOCKOUT_READER_MODULE:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_LOCKOUT_READER_MODULE",
                        "message": "Heartbeat references an unexpected lockout reader module.",
                        "record_index": index,
                        "observed": _plain(lockout_reader.get("reader_module")),
                        "expected": LOCKOUT_READER_MODULE,
                        "fail_closed": True,
                    }
                )
            if lockout_reader.get("reader_module_importable") is not True:
                verification_violations.append(
                    {
                        "code": "LOCKOUT_READER_NOT_IMPORTABLE",
                        "message": "Heartbeat did not successfully reference the runtime lockout reader module.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            if lockout_reader.get("config_path_exists") is not True:
                verification_violations.append(
                    {
                        "code": "LOCKOUT_CONFIG_MISSING",
                        "message": "Heartbeat did not find the committed runtime safety lockout config.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )

        embedded_violations = record.get("violations", [])
        if record.get("verdict") == "PASS" and embedded_violations:
            verification_violations.append(
                {
                    "code": "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS",
                    "message": "Heartbeat record verdict is PASS but embedded violations are present.",
                    "record_index": index,
                    "embedded_violation_count": len(embedded_violations),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("verdict") != "PASS":
            verification_violations.append(
                {
                    "code": "RECORD_VERDICT_NOT_PASS",
                    "message": "Heartbeat record verdict is not PASS.",
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
    parser = argparse.ArgumentParser(description="Build or verify H024 runtime safety heartbeat JSONL.")
    parser.add_argument("path", nargs="?", default="reports/h024_runtime_safety_heartbeat.jsonl")
    parser.add_argument("--require-pass", action="store_true")
    return parser


__all__ = [
    "DEFAULT_LOCKOUT_CONFIG_PATH",
    "EXPECTED_ACCOUNT_CURRENCY",
    "EXPECTED_SERVER",
    "FORBIDDEN_AUTHORIZATION_KEYS",
    "PACKET_TYPE",
    "SCHEMA_VERSION",
    "STRATEGY_ID",
    "collect_h024_runtime_safety_heartbeat",
    "read_jsonl",
    "verify_h024_runtime_safety_heartbeat_records",
    "write_jsonl",
]