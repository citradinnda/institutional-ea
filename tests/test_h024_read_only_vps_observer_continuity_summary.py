from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_h024_read_only_vps_observer_continuity_summary.ps1"


def _powershell() -> str | None:
    return shutil.which("powershell") or shutil.which("pwsh")


def _timestamp(delta_minutes: int = 0) -> str:
    value = datetime.now(timezone.utc) + timedelta(minutes=delta_minutes)
    return value.isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_packet(
    reports: Path,
    name: str,
    *,
    timestamp_field: str = "generated_at_utc",
    timestamp_delta_minutes: int = 0,
    verdict: str = "PASS",
    extra: dict | None = None,
) -> None:
    payload = {
        "schema_version": 1,
        "strategy": "H024",
        "component": name,
        timestamp_field: _timestamp(timestamp_delta_minutes),
        "verdict": verdict,
        "operator_state": f"{name.upper()}_OK_BUT_TRADING_NOT_AUTHORIZED",
        "operator_next_action": "CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED",
        "violations": [],
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "live_execution_authorized": False,
    }
    if extra:
        payload.update(extra)

    file_names = {
        "healthcheck": "h024_read_only_vps_observer_healthcheck.json",
        "task_state": "h024_read_only_vps_observer_task_state.json",
        "recovery_drill_preview": "h024_read_only_vps_recovery_drill_preview.json",
        "evidence_bundle": "h024_read_only_vps_observer_evidence_bundle.json",
    }
    _write_json(reports / file_names[name], payload)


def _write_runtime(root: Path, *, log_count: int = 2) -> None:
    runtime = root / "reports" / "runtime" / "h024_read_only_vps_observer"
    logs = runtime / "logs"
    logs.mkdir(parents=True, exist_ok=True)

    _write_json(
        runtime / "last_run_summary.json",
        {
            "status": "COMPLETED",
            "exit_code": 0,
            "completed_at_utc": _timestamp(),
        },
    )

    content = "\n".join(
        [
            "H024 read-only VPS observer starting.",
            "Mode: read-only packet generation only.",
            "Verifier verdict: PASS",
            "H024 read-only VPS observer run complete.",
            "No trading or broker mutation was authorized.",
        ]
    )

    now_epoch = datetime.now(timezone.utc).timestamp()
    for index in range(log_count):
        log_path = logs / f"h024_read_only_vps_observer_20260512T13000{index}Z.log"
        log_path.write_text(content, encoding="utf-8")
        os.utime(log_path, (now_epoch - index, now_epoch - index))


def _write_all_packets(root: Path, *, health_delta_minutes: int = 0, recovery_extra: dict | None = None) -> None:
    reports = root / "reports"
    _write_packet(
        reports,
        "healthcheck",
        timestamp_field="checked_at_utc",
        timestamp_delta_minutes=health_delta_minutes,
    )
    _write_packet(reports, "task_state")
    _write_packet(reports, "recovery_drill_preview", extra=recovery_extra)
    _write_packet(reports, "evidence_bundle")


def _run_builder(root: Path, *, min_run_count: int = 2) -> subprocess.CompletedProcess[str]:
    ps = _powershell()
    if ps is None:
        pytest.skip("PowerShell is required for this test.")

    command = [
        ps,
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCRIPT),
        "-Root",
        str(root),
        "-MinRunCount",
        str(min_run_count),
        "-MaxPacketAgeMinutes",
        "60",
        "-MaxLatestRunAgeMinutes",
        "60",
    ]

    return subprocess.run(command, text=True, capture_output=True, check=False)


def _read_output(root: Path) -> dict:
    output = root / "reports" / "h024_read_only_vps_observer_continuity_summary.json"
    assert output.exists(), f"Expected output packet at {output}"
    return json.loads(output.read_text(encoding="utf-8-sig"))


def test_continuity_summary_passes_with_healthcheck_checked_at_utc_alias(tmp_path: Path) -> None:
    _write_runtime(tmp_path, log_count=2)
    _write_all_packets(tmp_path)

    result = _run_builder(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    packet = _read_output(tmp_path)

    assert packet["verdict"] == "PASS"
    assert packet["completed_runtime_log_count_evaluated"] >= 2
    assert packet["read_only_observer_continuity_authorizes_trading"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["live_execution_authorized"] is False

    healthcheck = next(item for item in packet["upstream_packets"] if item["component"] == "healthcheck")
    assert healthcheck["verdict"] == "PASS"
    assert healthcheck["timestamp_utc"]


def test_continuity_summary_fails_closed_when_completed_runs_are_insufficient(tmp_path: Path) -> None:
    _write_runtime(tmp_path, log_count=1)
    _write_all_packets(tmp_path)

    result = _run_builder(tmp_path, min_run_count=2)

    assert result.returncode != 0
    packet = _read_output(tmp_path)

    assert packet["verdict"] == "FAIL_CLOSED"
    codes = {violation["code"] for violation in packet["violations"]}
    assert "insufficient_runtime_logs" in codes
    assert "insufficient_completed_observer_runs" in codes


def test_continuity_summary_fails_closed_when_healthcheck_checked_at_utc_is_stale(tmp_path: Path) -> None:
    _write_runtime(tmp_path, log_count=2)
    _write_all_packets(tmp_path, health_delta_minutes=-120)

    result = _run_builder(tmp_path)

    assert result.returncode != 0
    packet = _read_output(tmp_path)

    assert packet["verdict"] == "FAIL_CLOSED"
    codes = {violation["code"] for violation in packet["violations"]}
    assert "healthcheck_packet_stale" in codes


def test_continuity_summary_fails_closed_on_unsafe_true_flag(tmp_path: Path) -> None:
    _write_runtime(tmp_path, log_count=2)
    _write_all_packets(tmp_path, recovery_extra={"trading_authorized": True})

    result = _run_builder(tmp_path)

    assert result.returncode != 0
    packet = _read_output(tmp_path)

    assert packet["verdict"] == "FAIL_CLOSED"
    codes = {violation["code"] for violation in packet["violations"]}
    assert "recovery_drill_preview_unsafe_true_flag" in codes
