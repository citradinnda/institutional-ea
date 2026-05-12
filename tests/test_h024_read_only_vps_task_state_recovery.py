from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _ps_exe() -> str:
    for candidate in ("powershell", "powershell.exe", "pwsh", "pwsh.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    pytest.skip("PowerShell executable is unavailable")


def _run_ps(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_ps_exe(), "-NoProfile", "-ExecutionPolicy", "Bypass", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _fresh_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stale_iso() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat()


def _mock_task_payload(**overrides: object) -> dict:
    payload: dict = {
        "task_exists": True,
        "task_name": "H024 Read Only VPS Observer",
        "task_path": "\\",
        "state": "Ready",
        "triggers": [
            {
                "enabled": True,
                "repetition_interval": "PT5M",
                "start_boundary": _fresh_iso(),
            }
        ],
        "last_run_time_utc": _fresh_iso(),
        "last_task_result": 0,
    }
    payload.update(overrides)
    return payload


def _assert_no_bom(path: Path) -> None:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")


def test_task_state_checker_passes_with_fresh_mock_task(tmp_path: Path) -> None:
    mock_task = tmp_path / "mock_task.json"
    output = tmp_path / "reports" / "task_state.json"
    alert_json = tmp_path / "reports" / "alert.json"
    alert_text = tmp_path / "reports" / "alert.txt"
    _write_json(mock_task, _mock_task_payload())

    result = _run_ps(
        [
            "-File",
            str(ROOT / "scripts" / "check_h024_read_only_vps_observer_task_state.ps1"),
            "-Root",
            str(ROOT),
            "-MockTaskJsonPath",
            str(mock_task),
            "-OutputPath",
            str(output),
            "-AlertJsonPath",
            str(alert_json),
            "-AlertTextPath",
            str(alert_text),
            "-ExpectedIntervalMinutes",
            "5",
            "-MaxLastRunAgeMinutes",
            "60",
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    packet = json.loads(output.read_text(encoding="utf-8"))
    alert = json.loads(alert_json.read_text(encoding="utf-8"))

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == "READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert packet["task_state"]["task_exists"] is True
    assert packet["task_state"]["triggers"][0]["repetition_interval_minutes"] == 5
    assert packet["safety"]["trading_authorized"] is False
    assert packet["safety"]["broker_mutation_authorized"] is False
    assert packet["safety"]["live_broker_request_constructed"] is False
    assert packet["safety"]["executable_trade_request_constructed"] is False
    assert alert["external_notification_sent"] is False
    assert alert["external_mutation_performed"] is False
    assert "Trading authorized: false" in alert_text.read_text(encoding="utf-8")
    _assert_no_bom(output)
    _assert_no_bom(alert_json)
    _assert_no_bom(alert_text)


@pytest.mark.parametrize(
    ("override", "expected_code"),
    [
        ({"state": "Disabled"}, "scheduled_task_disabled"),
        ({"last_run_time_utc": _stale_iso()}, "scheduled_task_last_run_stale"),
        ({"last_task_result": 1}, "scheduled_task_last_result_nonzero"),
        ({"task_exists": False}, "scheduled_task_not_installed"),
        ({"triggers": [{"enabled": True, "repetition_interval": "PT10M"}]}, "scheduled_task_trigger_interval_mismatch"),
    ],
)
def test_task_state_checker_fails_closed_for_bad_scheduler_state(
    tmp_path: Path, override: dict, expected_code: str
) -> None:
    mock_task = tmp_path / "mock_task.json"
    output = tmp_path / "reports" / "task_state.json"
    alert_json = tmp_path / "reports" / "alert.json"
    alert_text = tmp_path / "reports" / "alert.txt"
    _write_json(mock_task, _mock_task_payload(**override))

    result = _run_ps(
        [
            "-File",
            str(ROOT / "scripts" / "check_h024_read_only_vps_observer_task_state.ps1"),
            "-Root",
            str(ROOT),
            "-MockTaskJsonPath",
            str(mock_task),
            "-OutputPath",
            str(output),
            "-AlertJsonPath",
            str(alert_json),
            "-AlertTextPath",
            str(alert_text),
            "-ExpectedIntervalMinutes",
            "5",
            "-MaxLastRunAgeMinutes",
            "60",
        ]
    )

    assert result.returncode != 0
    packet = json.loads(output.read_text(encoding="utf-8"))
    codes = {violation["code"] for violation in packet["violations"]}

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["operator_state"] == "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_TASK_STATE_UNVERIFIED_NO_TRADING_AUTHORIZED"
    assert expected_code in codes
    assert packet["safety"]["trading_authorized"] is False
    assert packet["safety"]["broker_mutation_authorized"] is False
    assert packet["operator_alert_surface"]["severity"] == "CRITICAL"


def test_recovery_drill_preview_passes_with_fresh_local_evidence(tmp_path: Path) -> None:
    mock_task = tmp_path / "mock_task.json"
    task_state = tmp_path / "reports" / "task_state.json"
    health = tmp_path / "reports" / "health.json"
    recovery = tmp_path / "reports" / "recovery.json"
    recovery_alert_json = tmp_path / "reports" / "recovery_alert.json"
    recovery_alert_text = tmp_path / "reports" / "recovery_alert.txt"

    _write_json(mock_task, _mock_task_payload())
    task_result = _run_ps(
        [
            "-File",
            str(ROOT / "scripts" / "check_h024_read_only_vps_observer_task_state.ps1"),
            "-Root",
            str(ROOT),
            "-MockTaskJsonPath",
            str(mock_task),
            "-OutputPath",
            str(task_state),
            "-ExpectedIntervalMinutes",
            "5",
            "-MaxLastRunAgeMinutes",
            "60",
        ]
    )
    assert task_result.returncode == 0, task_result.stdout + task_result.stderr

    _write_json(
        health,
        {
            "generated_at_utc": _fresh_iso(),
            "verdict": "PASS",
            "operator_state": "READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED",
            "violations": [],
            "safety": {
                "trading_authorized": False,
                "broker_mutation_authorized": False,
            },
        },
    )

    recovery_result = _run_ps(
        [
            "-File",
            str(ROOT / "scripts" / "run_h024_read_only_vps_recovery_drill_preview.ps1"),
            "-Root",
            str(ROOT),
            "-TaskStatePacketPath",
            str(task_state),
            "-HealthPacketPath",
            str(health),
            "-OutputPath",
            str(recovery),
            "-AlertJsonPath",
            str(recovery_alert_json),
            "-AlertTextPath",
            str(recovery_alert_text),
            "-MaxEvidenceAgeMinutes",
            "60",
        ]
    )

    assert recovery_result.returncode == 0, recovery_result.stdout + recovery_result.stderr
    packet = json.loads(recovery.read_text(encoding="utf-8"))

    assert packet["verdict"] == "PASS"
    assert packet["preview_only"] is True
    assert packet["operator_state"] == "READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert packet["safety"]["trading_authorized"] is False
    assert packet["safety"]["broker_mutation_authorized"] is False
    assert packet["safety"]["recovery_drill_authorizes_trading"] is False
    assert len(packet["recovery_drill_steps"]) >= 6
    assert all(step["read_only"] is True for step in packet["recovery_drill_steps"])
    assert all(step["broker_mutation"] is False for step in packet["recovery_drill_steps"])
    _assert_no_bom(recovery)
    _assert_no_bom(recovery_alert_json)
    _assert_no_bom(recovery_alert_text)


def test_recovery_drill_preview_fails_closed_for_stale_health_evidence(tmp_path: Path) -> None:
    mock_task = tmp_path / "mock_task.json"
    task_state = tmp_path / "reports" / "task_state.json"
    health = tmp_path / "reports" / "health.json"
    recovery = tmp_path / "reports" / "recovery.json"

    _write_json(mock_task, _mock_task_payload())
    task_result = _run_ps(
        [
            "-File",
            str(ROOT / "scripts" / "check_h024_read_only_vps_observer_task_state.ps1"),
            "-Root",
            str(ROOT),
            "-MockTaskJsonPath",
            str(mock_task),
            "-OutputPath",
            str(task_state),
            "-ExpectedIntervalMinutes",
            "5",
            "-MaxLastRunAgeMinutes",
            "60",
        ]
    )
    assert task_result.returncode == 0, task_result.stdout + task_result.stderr

    _write_json(
        health,
        {
            "generated_at_utc": _stale_iso(),
            "verdict": "PASS",
            "operator_state": "READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED",
            "violations": [],
        },
    )

    recovery_result = _run_ps(
        [
            "-File",
            str(ROOT / "scripts" / "run_h024_read_only_vps_recovery_drill_preview.ps1"),
            "-Root",
            str(ROOT),
            "-TaskStatePacketPath",
            str(task_state),
            "-HealthPacketPath",
            str(health),
            "-OutputPath",
            str(recovery),
            "-MaxEvidenceAgeMinutes",
            "60",
        ]
    )

    assert recovery_result.returncode != 0
    packet = json.loads(recovery.read_text(encoding="utf-8"))
    codes = {violation["code"] for violation in packet["violations"]}

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["operator_state"] == "FAIL_CLOSED_READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_UNVERIFIED_NO_TRADING_AUTHORIZED"
    assert "healthcheck_evidence_stale" in codes
    assert packet["safety"]["trading_authorized"] is False
    assert packet["operator_alert_surface"]["severity"] == "CRITICAL"


def test_new_vps_task_state_recovery_scripts_do_not_call_mutating_broker_paths() -> None:
    paths = [
        ROOT / "scripts" / "check_h024_read_only_vps_observer_task_state.ps1",
        ROOT / "scripts" / "run_h024_read_only_vps_recovery_drill_preview.ps1",
    ]

    forbidden_call_patterns = [
        r"\border_send\s*\(",
        r"\.order_send\s*\(",
        r"\border_check\s*\(",
        r"\.order_check\s*\(",
        r"\bsymbol_select\s*\(",
        r"\.symbol_select\s*\(",
        r"TRADE_ACTION_",
        r"ORDER_TYPE_BUY",
        r"ORDER_TYPE_SELL",
        r"position_by",
        r"deviation\s*=",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in forbidden_call_patterns:
            assert not re.search(pattern, text, flags=re.IGNORECASE), f"{path} matched {pattern}"


def test_runbook_preserves_operational_not_trading_language() -> None:
    text = (ROOT / "docs" / "operations" / "H024_READ_ONLY_VPS_TASK_STATE_AND_RECOVERY_RUNBOOK.md").read_text(
        encoding="utf-8"
    )

    assert "read-only VPS observer" in text
    assert "task-state audit" in text
    assert "recovery drill preview" in text.lower()
    assert "PASS does not authorize trading or close/modify" in text
    assert "reports/" in text
