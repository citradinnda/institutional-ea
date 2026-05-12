import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "build_h024_read_only_vps_observer_evidence_bundle.ps1"
DOC = REPO_ROOT / "docs" / "operations" / "H024_READ_ONLY_VPS_REAL_SCHEDULER_AUDIT_CHECKLIST.md"


def _powershell_exe() -> str:
    for candidate in ("powershell", "pwsh"):
        found = shutil.which(candidate)
        if found:
            return found
    raise AssertionError("PowerShell executable not found")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_evidence_bundle_script_exists_and_preserves_static_safety_boundaries():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED" in text
    assert "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_UNVERIFIED_NO_TRADING_AUTHORIZED" in text
    assert "trading_authorized = $false" in text
    assert "broker_mutation_authorized = $false" in text
    assert "order_check_authorized = $false" in text
    assert "order_send_authorized = $false" in text
    assert "entry_authorized = $false" in text
    assert "close_modify_authorized = $false" in text
    assert "xauusd_order_authorized = $false" in text
    assert "usdjpy_order_authorized = $false" in text
    assert "live_broker_request_constructed = $false" in text
    assert "executable_trade_request_constructed = $false" in text
    assert "symbol_select_authorized = $false" in text
    assert "external_alert_mutation_authorized = $false" in text
    assert "scheduler_mutation_authorized = $false" in text

    forbidden_call_tokens = [
        "MetaTrader5",
        "mt5.",
        "order_send(",
        "order_check(",
        "symbol_select(",
        "Register-ScheduledTask",
        "Unregister-ScheduledTask",
        "Set-ScheduledTask",
        "Start-ScheduledTask",
        "Stop-ScheduledTask",
        "Send-MailMessage",
        "Invoke-RestMethod",
        "Invoke-WebRequest",
    ]

    for token in forbidden_call_tokens:
        assert token not in text


def test_real_scheduler_audit_checklist_documents_operations_and_boundaries():
    text = DOC.read_text(encoding="utf-8")

    assert "real VPS scheduler install/audit path" in text
    assert "practical VPS operations work" in text
    assert "reports/h024_read_only_vps_observer_evidence_bundle.json" in text
    assert "Do not add `reports/`." in text
    assert "does not authorize trading" in text
    assert "does not authorize close/modify" in text
    assert "does not authorize broker mutation" in text
    assert "does not authorize `order_check`" in text
    assert "does not authorize `order_send`" in text
    assert "does not authorize `symbol_select`" in text


def test_evidence_bundle_generates_pass_packet_from_mock_local_evidence(tmp_path):
    now = _utc_now()
    runtime_dir = tmp_path / "runtime"
    log_dir = runtime_dir / "logs"
    log_dir.mkdir(parents=True)
    log_path = log_dir / "observer.log"
    log_path.write_text("line 1\nline 2\nline 3\n", encoding="utf-8")

    last_run = tmp_path / "last_run_summary.json"
    health = tmp_path / "healthcheck.json"
    task_state = tmp_path / "task_state.json"
    recovery = tmp_path / "recovery.json"
    output = tmp_path / "bundle.json"
    text_output = tmp_path / "bundle.txt"

    _write_json(
        last_run,
        {
            "generated_at_utc": now,
            "exit_code": 0,
            "log_path": str(log_path),
        },
    )
    _write_json(
        health,
        {
            "generated_at_utc": now,
            "verdict": "PASS",
            "operator_state": "READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED",
            "violations": [],
        },
    )
    _write_json(
        task_state,
        {
            "generated_at_utc": now,
            "verdict": "PASS",
            "operator_state": "READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED",
            "violations": [],
        },
    )
    _write_json(
        recovery,
        {
            "generated_at_utc": now,
            "verdict": "PASS",
            "operator_state": "READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED",
            "violations": [],
        },
    )

    cmd = [
        _powershell_exe(),
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCRIPT),
        "-RuntimeStateDirectory",
        str(runtime_dir),
        "-LastRunSummaryPath",
        str(last_run),
        "-HealthPacketPath",
        str(health),
        "-TaskStatePacketPath",
        str(task_state),
        "-RecoveryDrillPacketPath",
        str(recovery),
        "-OutputPath",
        str(output),
        "-TextOutputPath",
        str(text_output),
        "-MaxPacketAgeMinutes",
        "60",
        "-LogTailLines",
        "2",
    ]

    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["verdict"] == "PASS"
    assert payload["operator_state"] == "READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert payload["evidence_bundle_authorizes_trading"] is False
    assert payload["safety"]["trading_authorized"] is False
    assert payload["safety"]["broker_mutation_authorized"] is False
    assert payload["safety"]["order_check_authorized"] is False
    assert payload["safety"]["order_send_authorized"] is False
    assert payload["safety"]["entry_authorized"] is False
    assert payload["safety"]["close_modify_authorized"] is False
    assert payload["safety"]["live_broker_request_constructed"] is False
    assert payload["safety"]["executable_trade_request_constructed"] is False
    assert payload["safety"]["symbol_select_authorized"] is False
    assert payload["latest_log"]["exists"] is True
    assert payload["latest_log"]["tail"] == ["line 2", "line 3"]
    assert payload["violations"] == []

    text = text_output.read_text(encoding="utf-8")
    assert "H024 read-only VPS observer evidence bundle verdict: PASS" in text
    assert "trading_authorized: false" in text


def test_evidence_bundle_fails_closed_on_missing_task_state_packet(tmp_path):
    now = _utc_now()
    runtime_dir = tmp_path / "runtime"
    log_dir = runtime_dir / "logs"
    log_dir.mkdir(parents=True)
    log_path = log_dir / "observer.log"
    log_path.write_text("observer ok\n", encoding="utf-8")

    last_run = tmp_path / "last_run_summary.json"
    health = tmp_path / "healthcheck.json"
    missing_task_state = tmp_path / "missing_task_state.json"
    recovery = tmp_path / "recovery.json"
    output = tmp_path / "bundle.json"
    text_output = tmp_path / "bundle.txt"

    _write_json(last_run, {"generated_at_utc": now, "exit_code": 0, "log_path": str(log_path)})
    _write_json(health, {"generated_at_utc": now, "verdict": "PASS", "violations": []})
    _write_json(recovery, {"generated_at_utc": now, "verdict": "PASS", "violations": []})

    cmd = [
        _powershell_exe(),
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCRIPT),
        "-RuntimeStateDirectory",
        str(runtime_dir),
        "-LastRunSummaryPath",
        str(last_run),
        "-HealthPacketPath",
        str(health),
        "-TaskStatePacketPath",
        str(missing_task_state),
        "-RecoveryDrillPacketPath",
        str(recovery),
        "-OutputPath",
        str(output),
        "-TextOutputPath",
        str(text_output),
        "-MaxPacketAgeMinutes",
        "60",
    ]

    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["verdict"] == "FAIL_CLOSED"
    assert payload["operator_state"] == "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_UNVERIFIED_NO_TRADING_AUTHORIZED"
    assert any("observer task-state packet missing" in violation for violation in payload["violations"])
    assert payload["safety"]["trading_authorized"] is False
    assert payload["safety"]["broker_mutation_authorized"] is False
