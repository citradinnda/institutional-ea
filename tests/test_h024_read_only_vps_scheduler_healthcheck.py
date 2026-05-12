from __future__ import annotations

import json
import shutil
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = [
    REPO_ROOT / "scripts" / "run_h024_read_only_vps_observer_scheduled.ps1",
    REPO_ROOT / "scripts" / "install_h024_read_only_vps_observer_task.ps1",
    REPO_ROOT / "scripts" / "uninstall_h024_read_only_vps_observer_task.ps1",
    REPO_ROOT / "scripts" / "check_h024_read_only_vps_observer_health.ps1",
]


def _ps_exe() -> str:
    exe = shutil.which("powershell") or shutil.which("pwsh")
    if not exe:
        pytest.skip("PowerShell is required for H024 VPS scheduler healthcheck tests")
    return exe


def _run_ps(script: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = [
        _ps_exe(),
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        *map(str, args),
    ]
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_jsonl_record(path: Path, *, ts: datetime, verdict: str = "PASS") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema_version": 1,
        "strategy": "H024",
        "verdict": verdict,
        "operator_state": "TEST_STATE_OK_BUT_TRADING_NOT_AUTHORIZED",
        "generated_at_utc": _iso(ts),
        "violations": [],
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "live_execution_authorized": False,
    }
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")


def _seed_health_root(root: Path, *, ts: datetime) -> Path:
    reports = root / "reports"
    _write_jsonl_record(
        reports / "h024_read_only_vps_deployment_readiness_aggregate.jsonl",
        ts=ts,
    )
    _write_jsonl_record(
        reports / "h024_read_only_black_swan_guard.jsonl",
        ts=ts,
    )
    _write_jsonl_record(
        reports / "h024_runtime_safety_heartbeat.jsonl",
        ts=ts,
    )
    _write_jsonl_record(
        reports / "h024_runtime_no_mutation_safety_gate.jsonl",
        ts=ts,
    )

    state = reports / "runtime" / "h024_read_only_vps_observer"
    logs = state / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log_path = logs / "sample.log"
    log_path.write_text("sample read-only observer log\n", encoding="utf-8")

    summary = {
        "schema_version": 1,
        "strategy": "H024",
        "component": "read_only_vps_observer_scheduled_wrapper",
        "status": "COMPLETED",
        "exit_code": 0,
        "completed_at_utc": _iso(ts),
        "log_path": str(log_path),
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "live_execution_authorized": False,
    }
    (state / "last_run_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    return reports / "h024_read_only_vps_observer_healthcheck.json"


def test_scheduler_healthcheck_scripts_exist() -> None:
    for script in SCRIPTS:
        assert script.exists(), script


def test_new_scripts_do_not_contain_mutating_api_identifiers() -> None:
    forbidden = [
        "order" + "_send",
        "order" + "_check",
        "symbol" + "_select",
        "TRADE" + "_ACTION",
        "Position" + "Close",
    ]

    for script in SCRIPTS:
        text = script.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, f"{token} unexpectedly present in {script}"


def test_install_and_uninstall_preview_are_non_mutating() -> None:
    install = REPO_ROOT / "scripts" / "install_h024_read_only_vps_observer_task.ps1"
    uninstall = REPO_ROOT / "scripts" / "uninstall_h024_read_only_vps_observer_task.ps1"

    install_result = _run_ps(install, "-Root", str(REPO_ROOT), "-Preview")
    assert "Preview only" in install_result.stdout
    assert "H024 Read Only VPS Observer" in install_result.stdout

    uninstall_result = _run_ps(uninstall, "-Preview")
    assert "Preview only" in uninstall_result.stdout


def test_healthcheck_passes_with_fresh_evidence(tmp_path: Path) -> None:
    health_script = REPO_ROOT / "scripts" / "check_h024_read_only_vps_observer_health.ps1"
    health_path = _seed_health_root(tmp_path, ts=datetime.now(timezone.utc))

    result = _run_ps(
        health_script,
        "-Root",
        str(tmp_path),
        "-MaxAgeMinutes",
        "60",
        "-HealthOutPath",
        str(health_path),
    )

    assert "healthcheck verdict: PASS" in result.stdout

    packet = json.loads(health_path.read_text(encoding="utf-8"))
    assert packet["verdict"] == "PASS"
    assert packet["violations"] == []
    assert packet["read_only_observer_healthcheck_authorizes_trading"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["live_execution_authorized"] is False


def test_healthcheck_fails_closed_on_stale_readiness(tmp_path: Path) -> None:
    health_script = REPO_ROOT / "scripts" / "check_h024_read_only_vps_observer_health.ps1"
    stale_ts = datetime.now(timezone.utc) - timedelta(hours=3)
    health_path = _seed_health_root(tmp_path, ts=stale_ts)

    result = _run_ps(
        health_script,
        "-Root",
        str(tmp_path),
        "-MaxAgeMinutes",
        "30",
        "-HealthOutPath",
        str(health_path),
        "-NoFailExit",
    )

    assert "FAIL_CLOSED" in result.stdout

    packet = json.loads(health_path.read_text(encoding="utf-8"))
    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("STALE" in item for item in packet["violations"])


def test_scheduled_wrapper_writes_summary_and_rotates_logs(tmp_path: Path) -> None:
    wrapper = REPO_ROOT / "scripts" / "run_h024_read_only_vps_observer_scheduled.ps1"

    fake = tmp_path / "scripts" / "fake_observer.ps1"
    fake.parent.mkdir(parents=True, exist_ok=True)
    fake.write_text('Write-Output "fake observer completed"\nexit 0\n', encoding="utf-8")

    for _ in range(2):
        _run_ps(
            wrapper,
            "-Root",
            str(tmp_path),
            "-ObserverScriptPath",
            str(fake),
            "-RetentionCount",
            "1",
            "-RetentionDays",
            "999",
        )
        time.sleep(0.05)

    state = tmp_path / "reports" / "runtime" / "h024_read_only_vps_observer"
    logs = sorted((state / "logs").glob("*.log"))
    assert len(logs) == 1

    summary = json.loads((state / "last_run_summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "COMPLETED"
    assert summary["exit_code"] == 0
    assert summary["read_only_observer_only"] is True
    assert summary["trading_authorized"] is False
    assert summary["broker_mutation_authorized"] is False
    assert summary["live_execution_authorized"] is False
    assert Path(summary["log_path"]).exists()
