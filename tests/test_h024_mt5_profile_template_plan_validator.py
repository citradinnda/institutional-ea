from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_h024_mt5_profile_template_plan import (
    EXPECTED_EA_NAME,
    EXPECTED_EA_VERSION,
    EXPECTED_RUNTIME_MODE,
    EXPECTED_SCHEMA_VERSION,
    validate_plan_file,
    validate_plan_payload,
)


def valid_payload(terminal_data_dir: Path) -> dict[str, object]:
    return {
        "terminal_data_dir": str(terminal_data_dir),
        "account_server": "Exness-MT5Trial6",
        "account_company": "Exness Technologies Ltd",
        "account_currency": "USD",
        "ea_name": EXPECTED_EA_NAME,
        "schema_version": EXPECTED_SCHEMA_VERSION,
        "ea_version": EXPECTED_EA_VERSION,
        "runtime_mode": EXPECTED_RUNTIME_MODE,
        "kill_switch_blocked": True,
        "attach_detach_enabled": False,
        "order_send_enabled": False,
        "gui_automation_enabled": False,
        "charts": [
            {
                "symbol": "USDJPYm",
                "timeframe": "H4",
                "ea_name": EXPECTED_EA_NAME,
                "inputs": {
                    "InpKillSwitchBlocked": True,
                    "InpSchemaVersion": EXPECTED_SCHEMA_VERSION,
                    "InpEaVersion": EXPECTED_EA_VERSION,
                    "InpRuntimeMode": EXPECTED_RUNTIME_MODE,
                },
            },
            {
                "symbol": "XAUUSDm",
                "timeframe": "H4",
                "ea_name": EXPECTED_EA_NAME,
                "inputs": {
                    "InpKillSwitchBlocked": True,
                    "InpSchemaVersion": EXPECTED_SCHEMA_VERSION,
                    "InpEaVersion": EXPECTED_EA_VERSION,
                    "InpRuntimeMode": EXPECTED_RUNTIME_MODE,
                },
            },
        ],
    }


def make_terminal_shape(path: Path) -> None:
    (path / "MQL5" / "Experts").mkdir(parents=True)
    (path / "MQL5" / "Files").mkdir(parents=True)


def test_validate_plan_payload_accepts_expected_plan(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)

    result = validate_plan_payload(valid_payload(terminal))

    assert result.passed
    assert result.violations == []


def test_validate_plan_file_accepts_expected_json_plan(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps(valid_payload(terminal)), encoding="utf-8")

    result = validate_plan_file(plan)

    assert result.passed


def test_validate_plan_file_rejects_missing_file(tmp_path: Path) -> None:
    result = validate_plan_file(tmp_path / "missing.json")

    assert not result.passed
    assert "missing plan file" in result.violations[0]


def test_validate_plan_file_rejects_invalid_json(tmp_path: Path) -> None:
    plan = tmp_path / "plan.json"
    plan.write_text("{not-json", encoding="utf-8")

    result = validate_plan_file(plan)

    assert not result.passed
    assert "invalid JSON" in result.violations[0]


def test_validate_plan_payload_rejects_wrong_terminal_shape(tmp_path: Path) -> None:
    result = validate_plan_payload(valid_payload(tmp_path / "missing_terminal"))

    assert not result.passed
    assert any("terminal_data_dir does not exist" in item for item in result.violations)
    assert any("terminal Experts dir does not exist" in item for item in result.violations)
    assert any("terminal Files dir does not exist" in item for item in result.violations)


def test_validate_plan_payload_rejects_wrong_account_server(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)
    payload = valid_payload(terminal)
    payload["account_server"] = "Wrong-Server"

    result = validate_plan_payload(payload)

    assert not result.passed
    assert "account_server does not match expected Exness demo server" in result.violations


def test_validate_plan_payload_rejects_enabled_attach_detach(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)
    payload = valid_payload(terminal)
    payload["attach_detach_enabled"] = True

    result = validate_plan_payload(payload)

    assert not result.passed
    assert "attach_detach_enabled must be false until explicitly approved" in result.violations


def test_validate_plan_payload_rejects_order_send_enabled(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)
    payload = valid_payload(terminal)
    payload["order_send_enabled"] = True

    result = validate_plan_payload(payload)

    assert not result.passed
    assert "order_send_enabled must be false" in result.violations


def test_validate_plan_payload_rejects_wrong_symbols(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)
    payload = valid_payload(terminal)
    charts = payload["charts"]
    assert isinstance(charts, list)
    chart = charts[0]
    assert isinstance(chart, dict)
    chart["symbol"] = "EURUSDm"

    result = validate_plan_payload(payload)

    assert not result.passed
    assert any("unexpected symbol" in item for item in result.violations)
    assert "charts missing required symbols: ['USDJPYm']" in result.violations


def test_validate_plan_payload_rejects_unblocked_kill_switch_input(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)
    payload = valid_payload(terminal)
    charts = payload["charts"]
    assert isinstance(charts, list)
    chart = charts[0]
    assert isinstance(chart, dict)
    inputs = chart["inputs"]
    assert isinstance(inputs, dict)
    inputs["InpKillSwitchBlocked"] = False

    result = validate_plan_payload(payload)

    assert not result.passed
    assert any("InpKillSwitchBlocked must be true" in item for item in result.violations)


def test_validate_plan_payload_rejects_wrong_ea_version_input(tmp_path: Path) -> None:
    terminal = tmp_path / "terminal"
    make_terminal_shape(terminal)
    payload = valid_payload(terminal)
    charts = payload["charts"]
    assert isinstance(charts, list)
    chart = charts[1]
    assert isinstance(chart, dict)
    inputs = chart["inputs"]
    assert isinstance(inputs, dict)
    inputs["InpEaVersion"] = "0.2"

    result = validate_plan_payload(payload)

    assert not result.passed
    assert any("InpEaVersion mismatch" in item for item in result.violations)
