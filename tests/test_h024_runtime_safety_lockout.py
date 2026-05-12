from __future__ import annotations

import ast
import json
from pathlib import Path

from quantcore.execution.h024_runtime_safety_lockout import (
    DEFAULT_CONFIG_PATH,
    REQUIRED_LOCKOUTS,
    build_h024_runtime_safety_lockout_record,
    verify_h024_runtime_safety_lockout_records,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def _lockout_payload(lockout_name: str, *, active: bool = False) -> dict:
    specs = {
        "global_no_new_entry": ("global", None, None),
        "manual_override_lockout": ("global", None, None),
        "xauusd_no_new_entry": ("symbol:XAUUSD", "XAUUSD", "XAUUSDm"),
        "usdjpy_no_new_entry": ("symbol:USDJPY", "USDJPY", "USDJPYm"),
    }
    scope, model_symbol, runtime_symbol = specs[lockout_name]
    return {
        "schema_version": "1.0",
        "strategy": "H024",
        "lockout_name": lockout_name,
        "scope": scope,
        "model_symbol": model_symbol,
        "runtime_symbol": runtime_symbol,
        "active": active,
        "reason": "test lockout state",
        "updated_at_utc": "2026-05-12T00:00:00Z",
        "updated_by": "test",
        "expires_at_utc": None,
    }


def _config_payload(lockout_paths: dict[str, str]) -> dict:
    return {
        "schema_version": "1.0",
        "strategy": "H024",
        "config_type": "h024_runtime_safety_lockout_config",
        "fail_closed_on_missing_config": True,
        "fail_closed_on_missing_lockout_file": True,
        "fail_closed_on_malformed_lockout_file": True,
        "fail_closed_on_unexpected_symbol": True,
        "model_symbols": ["XAUUSD", "USDJPY"],
        "runtime_symbols": {"XAUUSD": "XAUUSDm", "USDJPY": "USDJPYm"},
        "required_lockouts": list(REQUIRED_LOCKOUTS),
        "lockout_state_files": lockout_paths,
        "authorizations": {
            "broker_mutation_authorized": False,
            "order_check_authorized": False,
            "order_send_authorized": False,
            "entry_authorized": False,
            "close_modify_authorized": False,
            "xauusd_order_authorized": False,
            "usdjpy_order_authorized": False,
            "trading_loop_authorized": False,
            "automatic_execution_authorized": False,
        },
    }


def _write_config_tree(tmp_path: Path, *, active: dict[str, bool] | None = None) -> Path:
    active = active or {}
    lockout_paths = {}
    for lockout_name in REQUIRED_LOCKOUTS:
        path = tmp_path / "lockouts" / f"{lockout_name}.json"
        _write_json(path, _lockout_payload(lockout_name, active=active.get(lockout_name, False)))
        lockout_paths[lockout_name] = str(path)
    config_path = tmp_path / "default_lockout_config.json"
    _write_json(config_path, _config_payload(lockout_paths))
    return config_path


def test_committed_default_config_builds_pass_but_authorizes_nothing():
    record = build_h024_runtime_safety_lockout_record(config_path=DEFAULT_CONFIG_PATH, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["operator_state"] == "LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED"
    assert record["lockout_inputs_valid"] is True
    assert record["lockout_triggered"] is False
    assert record["effective_new_entries_blocked"] is True
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["entry_authorized"] is False
    assert record["close_modify_authorized"] is False
    assert record["xauusd_order_authorized"] is False
    assert record["usdjpy_order_authorized"] is False
    assert record["trading_loop_authorized"] is False
    assert record["automatic_execution_authorized"] is False


def test_verifier_accepts_default_record_when_require_pass():
    record = build_h024_runtime_safety_lockout_record(config_path=DEFAULT_CONFIG_PATH)

    summary = verify_h024_runtime_safety_lockout_records([record], require_pass=True)

    assert summary["verdict"] == "PASS"
    assert summary["violations"] == []


def test_missing_config_fails_closed(tmp_path):
    missing = tmp_path / "missing_config.json"

    record = build_h024_runtime_safety_lockout_record(config_path=missing)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED"
    assert record["effective_new_entries_blocked"] is True
    assert "config_missing_json_file" in record["violations"]


def test_malformed_config_fails_closed(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text("{not-json", encoding="utf-8")

    record = build_h024_runtime_safety_lockout_record(config_path=config_path)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED"
    assert "config_malformed_json_file" in record["violations"]


def test_missing_lockout_file_fails_closed(tmp_path):
    config_path = _write_config_tree(tmp_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    missing_lockout_path = tmp_path / "lockouts" / "missing_global.json"
    config["lockout_state_files"]["global_no_new_entry"] = str(missing_lockout_path)
    _write_json(config_path, config)

    record = build_h024_runtime_safety_lockout_record(config_path=config_path)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED"
    assert record["effective_new_entries_blocked"] is True
    assert "global_no_new_entry_missing_json_file" in record["violations"]
    assert "global_no_new_entry" in record["fail_closed_lockouts"]


def test_malformed_lockout_file_fails_closed(tmp_path):
    config_path = _write_config_tree(tmp_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    malformed_path = tmp_path / "lockouts" / "manual_override_lockout.json"
    malformed_path.write_text("[", encoding="utf-8")
    config["lockout_state_files"]["manual_override_lockout"] = str(malformed_path)
    _write_json(config_path, config)

    record = build_h024_runtime_safety_lockout_record(config_path=config_path)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED"
    assert "manual_override_lockout_malformed_json_file" in record["violations"]
    assert "manual_override_lockout" in record["fail_closed_lockouts"]


def test_active_global_lockout_passes_but_blocks_entries(tmp_path):
    config_path = _write_config_tree(tmp_path, active={"global_no_new_entry": True})

    record = build_h024_runtime_safety_lockout_record(config_path=config_path)

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["operator_state"] == "LOCKED_BY_ACTIVE_LOCKOUT"
    assert record["lockout_triggered"] is True
    assert "global_no_new_entry" in record["active_lockouts"]
    assert record["effective_new_entries_blocked"] is True
    assert record["entry_authorized"] is False


def test_active_usdjpy_symbol_lockout_blocks_usdjpy_lockout_state(tmp_path):
    config_path = _write_config_tree(tmp_path, active={"usdjpy_no_new_entry": True})

    record = build_h024_runtime_safety_lockout_record(config_path=config_path)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == "LOCKED_BY_ACTIVE_LOCKOUT"
    assert "usdjpy_no_new_entry" in record["active_lockouts"]
    assert record["per_symbol_lockout_state"]["USDJPY"]["blocked_by_lockout"] is True
    assert record["per_symbol_lockout_state"]["USDJPY"]["entry_authorized"] is False


def test_invalid_active_type_fails_closed(tmp_path):
    config_path = _write_config_tree(tmp_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    lockout_path = Path(config["lockout_state_files"]["xauusd_no_new_entry"])
    payload = json.loads(lockout_path.read_text(encoding="utf-8"))
    payload["active"] = "false"
    _write_json(lockout_path, payload)

    record = build_h024_runtime_safety_lockout_record(config_path=config_path)

    assert record["verdict"] == "FAIL"
    assert "xauusd_no_new_entry_active_must_be_boolean" in record["violations"]
    assert "xauusd_no_new_entry" in record["fail_closed_lockouts"]


def test_config_authorization_true_fails_closed(tmp_path):
    config_path = _write_config_tree(tmp_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["authorizations"]["order_send_authorized"] = True
    _write_json(config_path, config)

    record = build_h024_runtime_safety_lockout_record(config_path=config_path)

    assert record["verdict"] == "FAIL"
    assert "config.authorizations.order_send_authorized_must_be_false" in record["violations"]


def test_verifier_rejects_mutation_authorization_even_if_record_says_pass():
    record = build_h024_runtime_safety_lockout_record(config_path=DEFAULT_CONFIG_PATH)
    record["broker_mutation_authorized"] = True

    summary = verify_h024_runtime_safety_lockout_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "h024_runtime_safety_lockout_reader.broker_mutation_authorized_must_be_false" in summary["violations"]


def test_module_has_no_metatrader5_or_broker_calls():
    source_path = Path("quantcore/execution/h024_runtime_safety_lockout.py")
    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    imported_names = set()
    called_attributes = set()
    called_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_names.add(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                called_attributes.add(node.func.attr)
            elif isinstance(node.func, ast.Name):
                called_names.add(node.func.id)

    assert "MetaTrader5" not in imported_names
    assert "mt5" not in imported_names
    assert "order_check" not in called_attributes
    assert "order_send" not in called_attributes
    assert "positions_get" not in called_attributes
    assert "orders_get" not in called_attributes
    assert "initialize" not in called_attributes
    assert "shutdown" not in called_attributes
    assert "copy_rates_from_pos" not in called_attributes
    assert "symbol_info_tick" not in called_attributes
    assert "account_info" not in called_attributes
    assert "subprocess" not in imported_names
    assert "system" not in called_names