"""H024 runtime safety configuration and local lockout reader.

This is the first runtime-local safety enforcement layer for H024. It reads a
committed safety config and local lockout-state JSON files. It performs no
broker reads, no broker writes, no order_check, no order_send, no close/modify,
and no trading loop action.

Missing or malformed config/lockout inputs fail closed.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Iterable, Mapping


STRATEGY = "H024"
PACKET_TYPE = "h024_runtime_safety_lockout_reader"
SCHEMA_VERSION = "1.0"
CONFIG_TYPE = "h024_runtime_safety_lockout_config"
DEFAULT_CONFIG_PATH = Path("config/h024_runtime_safety/default_lockout_config.json")

MODEL_SYMBOLS = ("XAUUSD", "USDJPY")
RUNTIME_SYMBOLS = {
    "XAUUSD": "XAUUSDm",
    "USDJPY": "USDJPYm",
}

REQUIRED_LOCKOUTS = (
    "global_no_new_entry",
    "manual_override_lockout",
    "xauusd_no_new_entry",
    "usdjpy_no_new_entry",
)

LOCKOUT_SPECS = {
    "global_no_new_entry": {
        "scope": "global",
        "model_symbol": None,
        "runtime_symbol": None,
    },
    "manual_override_lockout": {
        "scope": "global",
        "model_symbol": None,
        "runtime_symbol": None,
    },
    "xauusd_no_new_entry": {
        "scope": "symbol:XAUUSD",
        "model_symbol": "XAUUSD",
        "runtime_symbol": "XAUUSDm",
    },
    "usdjpy_no_new_entry": {
        "scope": "symbol:USDJPY",
        "model_symbol": "USDJPY",
        "runtime_symbol": "USDJPYm",
    },
}

MUST_BE_FALSE_FIELDS = (
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


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _base_authorizations() -> dict[str, bool]:
    return {
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "xauusd_order_authorized": False,
        "usdjpy_order_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
    }


def _new_base_record(config_path: Path, generated_at_utc: str | None) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "generated_at_utc": generated_at_utc or utc_now_iso(),
        "read_only": True,
        "local_files_only": True,
        "broker_calls_authorized": False,
        "config_path": str(config_path),
        "model_symbols": list(MODEL_SYMBOLS),
        "runtime_symbols": dict(RUNTIME_SYMBOLS),
        "config": None,
        "lockout_states": {},
        "active_lockouts": [],
        "fail_closed_lockouts": [],
        "lockout_inputs_valid": False,
        "lockout_triggered": True,
        "effective_new_entries_blocked": True,
        "effective_per_symbol_new_entries_blocked": {
            "XAUUSD": True,
            "USDJPY": True,
        },
        "operator_state": "FAIL_CLOSED",
        "operator_next_action": "inspect_runtime_safety_lockout_inputs",
        "violations": [],
        "verdict": "FAIL",
    }
    record.update(_base_authorizations())
    return record


def _read_json_mapping(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "missing_json_file"
    if not path.is_file():
        return None, "json_path_is_not_file"
    try:
        with path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except JSONDecodeError:
        return None, "malformed_json_file"
    except OSError:
        return None, "unreadable_json_file"
    if not isinstance(loaded, dict):
        return None, "json_root_not_object"
    return loaded, None


def _resolve_path(path_value: Any, *, base_dir: Path) -> Path | None:
    if not isinstance(path_value, str) or not path_value.strip():
        return None
    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate
    base_candidate = base_dir / candidate
    if base_candidate.exists():
        return base_candidate
    return Path.cwd() / candidate


def _validate_false_authorizations(
    mapping: Mapping[str, Any],
    *,
    prefix: str,
    violations: list[str],
) -> None:
    for field in MUST_BE_FALSE_FIELDS:
        if field in mapping and mapping.get(field) is not False:
            violations.append(f"{prefix}.{field}_must_be_false")


def _validate_config(config: Mapping[str, Any], *, violations: list[str]) -> None:
    if config.get("schema_version") != SCHEMA_VERSION:
        violations.append("config_unexpected_schema_version")
    if config.get("strategy") != STRATEGY:
        violations.append("config_unexpected_strategy")
    if config.get("config_type") != CONFIG_TYPE:
        violations.append("config_unexpected_config_type")

    if config.get("fail_closed_on_missing_config") is not True:
        violations.append("config_must_fail_closed_on_missing_config")
    if config.get("fail_closed_on_missing_lockout_file") is not True:
        violations.append("config_must_fail_closed_on_missing_lockout_file")
    if config.get("fail_closed_on_malformed_lockout_file") is not True:
        violations.append("config_must_fail_closed_on_malformed_lockout_file")
    if config.get("fail_closed_on_unexpected_symbol") is not True:
        violations.append("config_must_fail_closed_on_unexpected_symbol")

    if tuple(config.get("model_symbols", [])) != MODEL_SYMBOLS:
        violations.append("config_unexpected_model_symbols")
    if config.get("runtime_symbols") != RUNTIME_SYMBOLS:
        violations.append("config_unexpected_runtime_symbols")

    if tuple(config.get("required_lockouts", [])) != REQUIRED_LOCKOUTS:
        violations.append("config_unexpected_required_lockouts")

    lockout_state_files = config.get("lockout_state_files")
    if not isinstance(lockout_state_files, Mapping):
        violations.append("config_lockout_state_files_missing")
    else:
        for lockout_name in REQUIRED_LOCKOUTS:
            if lockout_name not in lockout_state_files:
                violations.append(f"config_missing_lockout_state_file_{lockout_name}")

    authorizations = config.get("authorizations")
    if not isinstance(authorizations, Mapping):
        violations.append("config_authorizations_missing")
    else:
        _validate_false_authorizations(authorizations, prefix="config.authorizations", violations=violations)


def _validate_lockout_state(
    *,
    lockout_name: str,
    lockout_path: Path,
    lockout_data: Mapping[str, Any],
    violations: list[str],
) -> dict[str, Any]:
    spec = LOCKOUT_SPECS[lockout_name]
    state_violations: list[str] = []

    if lockout_data.get("schema_version") != SCHEMA_VERSION:
        state_violations.append("unexpected_schema_version")
    if lockout_data.get("strategy") != STRATEGY:
        state_violations.append("unexpected_strategy")
    if lockout_data.get("lockout_name") != lockout_name:
        state_violations.append("unexpected_lockout_name")
    if lockout_data.get("scope") != spec["scope"]:
        state_violations.append("unexpected_scope")
    if lockout_data.get("model_symbol") != spec["model_symbol"]:
        state_violations.append("unexpected_model_symbol")
    if lockout_data.get("runtime_symbol") != spec["runtime_symbol"]:
        state_violations.append("unexpected_runtime_symbol")
    if not isinstance(lockout_data.get("active"), bool):
        state_violations.append("active_must_be_boolean")
    if not isinstance(lockout_data.get("reason"), str) or not lockout_data.get("reason", "").strip():
        state_violations.append("reason_required")
    if not isinstance(lockout_data.get("updated_at_utc"), str) or not lockout_data.get("updated_at_utc", "").strip():
        state_violations.append("updated_at_utc_required")
    if not isinstance(lockout_data.get("updated_by"), str) or not lockout_data.get("updated_by", "").strip():
        state_violations.append("updated_by_required")

    for state_violation in state_violations:
        violations.append(f"{lockout_name}_{state_violation}")

    valid = not state_violations
    active = lockout_data.get("active") if isinstance(lockout_data.get("active"), bool) else True

    return {
        "lockout_name": lockout_name,
        "path": str(lockout_path),
        "present": True,
        "parsed": True,
        "valid": valid,
        "active": active,
        "fail_closed_active": not valid,
        "scope": lockout_data.get("scope"),
        "model_symbol": lockout_data.get("model_symbol"),
        "runtime_symbol": lockout_data.get("runtime_symbol"),
        "reason": lockout_data.get("reason"),
        "updated_at_utc": lockout_data.get("updated_at_utc"),
        "updated_by": lockout_data.get("updated_by"),
        "expires_at_utc": lockout_data.get("expires_at_utc"),
        "violations": state_violations,
        "new_entries_blocked_by_this_lockout": bool(active) or not valid,
    }


def _missing_or_malformed_lockout_state(
    *,
    lockout_name: str,
    lockout_path: Path | None,
    error: str,
) -> dict[str, Any]:
    return {
        "lockout_name": lockout_name,
        "path": None if lockout_path is None else str(lockout_path),
        "present": False if error == "missing_json_file" or lockout_path is None else True,
        "parsed": False,
        "valid": False,
        "active": True,
        "fail_closed_active": True,
        "scope": LOCKOUT_SPECS[lockout_name]["scope"],
        "model_symbol": LOCKOUT_SPECS[lockout_name]["model_symbol"],
        "runtime_symbol": LOCKOUT_SPECS[lockout_name]["runtime_symbol"],
        "reason": f"Fail-closed due to {error}",
        "updated_at_utc": None,
        "updated_by": None,
        "expires_at_utc": None,
        "violations": [error],
        "new_entries_blocked_by_this_lockout": True,
    }


def _derive_operator_state(record: dict[str, Any]) -> None:
    violations = record["violations"]
    lockout_states = record["lockout_states"]

    active_lockouts = [
        name
        for name, state in lockout_states.items()
        if state.get("active") is True and state.get("valid") is True
    ]
    fail_closed_lockouts = [
        name
        for name, state in lockout_states.items()
        if state.get("fail_closed_active") is True
    ]

    record["active_lockouts"] = active_lockouts
    record["fail_closed_lockouts"] = fail_closed_lockouts
    record["lockout_inputs_valid"] = not violations
    record["lockout_triggered"] = bool(active_lockouts or fail_closed_lockouts)

    xauusd_blocked_by_lockout = bool(
        "global_no_new_entry" in active_lockouts
        or "manual_override_lockout" in active_lockouts
        or "xauusd_no_new_entry" in active_lockouts
        or fail_closed_lockouts
    )
    usdjpy_blocked_by_lockout = bool(
        "global_no_new_entry" in active_lockouts
        or "manual_override_lockout" in active_lockouts
        or "usdjpy_no_new_entry" in active_lockouts
        or fail_closed_lockouts
    )

    record["per_symbol_lockout_state"] = {
        "XAUUSD": {
            "runtime_symbol": "XAUUSDm",
            "blocked_by_lockout": xauusd_blocked_by_lockout,
            "entry_authorized": False,
            "order_check_authorized": False,
            "order_send_authorized": False,
        },
        "USDJPY": {
            "runtime_symbol": "USDJPYm",
            "blocked_by_lockout": usdjpy_blocked_by_lockout,
            "entry_authorized": False,
            "order_check_authorized": False,
            "order_send_authorized": False,
        },
    }

    record["effective_new_entries_blocked"] = True
    record["effective_per_symbol_new_entries_blocked"] = {
        "XAUUSD": True,
        "USDJPY": True,
    }

    if violations:
        record["operator_state"] = "FAIL_CLOSED"
        record["operator_next_action"] = "repair_or_restore_runtime_safety_lockout_inputs"
        record["verdict"] = "FAIL"
    elif active_lockouts:
        record["operator_state"] = "LOCKED_BY_ACTIVE_LOCKOUT"
        record["operator_next_action"] = "respect_active_lockout_and_do_not_enter"
        record["verdict"] = "PASS"
    else:
        record["operator_state"] = "LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED"
        record["operator_next_action"] = "continue_read_only_supervision"
        record["verdict"] = "PASS"


def build_h024_runtime_safety_lockout_record(
    *,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    """Read local safety config + lockout files and emit a fail-closed packet."""

    resolved_config_path = Path(config_path)
    record = _new_base_record(resolved_config_path, generated_at_utc)
    violations: list[str] = record["violations"]

    config, config_error = _read_json_mapping(resolved_config_path)
    if config_error:
        violations.append(f"config_{config_error}")
        _derive_operator_state(record)
        return record

    record["config"] = config
    _validate_config(config, violations=violations)

    lockout_state_files = config.get("lockout_state_files")
    if not isinstance(lockout_state_files, Mapping):
        _derive_operator_state(record)
        return record

    base_dir = resolved_config_path.parent
    for lockout_name in REQUIRED_LOCKOUTS:
        path_value = lockout_state_files.get(lockout_name)
        lockout_path = _resolve_path(path_value, base_dir=base_dir)
        if lockout_path is None:
            violations.append(f"{lockout_name}_lockout_path_missing_or_invalid")
            record["lockout_states"][lockout_name] = _missing_or_malformed_lockout_state(
                lockout_name=lockout_name,
                lockout_path=None,
                error="lockout_path_missing_or_invalid",
            )
            continue

        lockout_data, lockout_error = _read_json_mapping(lockout_path)
        if lockout_error:
            violations.append(f"{lockout_name}_{lockout_error}")
            record["lockout_states"][lockout_name] = _missing_or_malformed_lockout_state(
                lockout_name=lockout_name,
                lockout_path=lockout_path,
                error=lockout_error,
            )
            continue

        assert lockout_data is not None
        record["lockout_states"][lockout_name] = _validate_lockout_state(
            lockout_name=lockout_name,
            lockout_path=lockout_path,
            lockout_data=lockout_data,
            violations=violations,
        )

    _derive_operator_state(record)
    return record


def _walk_mappings(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _walk_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_mappings(child)


def _verify_false_authorizations(record: Mapping[str, Any], violations: list[str]) -> None:
    for mapping in _walk_mappings(record):
        name = mapping.get("lockout_name") or mapping.get("packet_type") or mapping.get("model_symbol") or "mapping"
        for field in MUST_BE_FALSE_FIELDS:
            if field in mapping and mapping.get(field) is not False:
                violations.append(f"{name}.{field}_must_be_false")


def verify_h024_runtime_safety_lockout_records(
    records: Iterable[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    loaded = [dict(record) for record in records]
    violations: list[str] = []

    if len(loaded) != 1:
        violations.append("expected_exactly_one_runtime_safety_lockout_record")

    record = loaded[0] if loaded else {}

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append("unexpected_schema_version")
    if record.get("strategy") != STRATEGY:
        violations.append("unexpected_strategy")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append("unexpected_packet_type")
    if record.get("read_only") is not True:
        violations.append("read_only_must_be_true")
    if record.get("local_files_only") is not True:
        violations.append("local_files_only_must_be_true")
    if record.get("broker_calls_authorized") is not False:
        violations.append("broker_calls_authorized_must_be_false")

    if tuple(record.get("model_symbols", [])) != MODEL_SYMBOLS:
        violations.append("unexpected_model_symbols")
    if record.get("runtime_symbols") != RUNTIME_SYMBOLS:
        violations.append("unexpected_runtime_symbols")

    _verify_false_authorizations(record, violations)

    if record.get("effective_new_entries_blocked") is not True:
        violations.append("effective_new_entries_blocked_must_be_true")

    per_symbol_blocked = record.get("effective_per_symbol_new_entries_blocked")
    if per_symbol_blocked != {"XAUUSD": True, "USDJPY": True}:
        violations.append("effective_per_symbol_new_entries_blocked_must_block_both_symbols")

    lockout_states = record.get("lockout_states")
    if not isinstance(lockout_states, Mapping):
        violations.append("lockout_states_missing")
        lockout_states = {}
    for lockout_name in REQUIRED_LOCKOUTS:
        state = lockout_states.get(lockout_name)
        if not isinstance(state, Mapping):
            violations.append(f"missing_lockout_state_{lockout_name}")
            continue
        if state.get("lockout_name") != lockout_name:
            violations.append(f"{lockout_name}_unexpected_lockout_name")
        if state.get("new_entries_blocked_by_this_lockout") not in (True, False):
            violations.append(f"{lockout_name}_new_entries_blocked_by_this_lockout_must_be_boolean")

    embedded_violations = record.get("violations", [])
    if not isinstance(embedded_violations, list):
        violations.append("embedded_violations_not_list")
        embedded_violations = []

    if require_pass and record.get("verdict") != "PASS":
        violations.append("record_verdict_not_pass")
    if require_pass and embedded_violations:
        violations.append("record_contains_embedded_violations")

    return {
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "record_count": len(loaded),
        "record_verdict": record.get("verdict"),
        "embedded_violations": embedded_violations,
        "operator_state": record.get("operator_state"),
        "active_lockouts": record.get("active_lockouts", []),
        "fail_closed_lockouts": record.get("fail_closed_lockouts", []),
        "lockout_inputs_valid": record.get("lockout_inputs_valid"),
        "lockout_triggered": record.get("lockout_triggered"),
        "effective_new_entries_blocked": record.get("effective_new_entries_blocked"),
        "broker_mutation_authorized": record.get("broker_mutation_authorized"),
        "order_check_authorized": record.get("order_check_authorized"),
        "order_send_authorized": record.get("order_send_authorized"),
        "entry_authorized": record.get("entry_authorized"),
        "close_modify_authorized": record.get("close_modify_authorized"),
        "xauusd_order_authorized": record.get("xauusd_order_authorized"),
        "usdjpy_order_authorized": record.get("usdjpy_order_authorized"),
        "trading_loop_authorized": record.get("trading_loop_authorized"),
        "automatic_execution_authorized": record.get("automatic_execution_authorized"),
    }


def write_jsonl(record: Mapping[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    return path


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records