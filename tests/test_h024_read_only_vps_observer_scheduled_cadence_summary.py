from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1"


def _powershell() -> str:
    configured = os.environ.get("POWERSHELL_EXE")
    if configured:
        return configured

    for candidate in ("pwsh", "powershell"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved

    raise AssertionError("No PowerShell executable found.")


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _base_packet(now: datetime) -> dict[str, Any]:
    return {
        "verdict": "PASS",
        "generated_at_utc": _iso(now),
        "operator_state": "TEST_READ_ONLY_OK_BUT_TRADING_NOT_AUTHORIZED",
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
        "live_broker_request_constructed": False,
        "executable_trade_request_constructed": False,
        "mt5_request_dictionary_constructed": False,
        "symbol_select_authorized": False,
    }


def _stamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S") + "000Z"


def _make_fixture(
    root: Path,
    *,
    run_offsets_minutes: list[int] | None = None,
    packet_name_to_override: dict[str, dict[str, Any]] | None = None,
) -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    offsets = run_offsets_minutes if run_offsets_minutes is not None else [18, 13, 8, 3]
    run_times = [now - timedelta(minutes=offset) for offset in offsets]

    reports = root / "reports"
    runtime = reports / "runtime" / "h024_read_only_vps_observer"
    logs = runtime / "logs"
    logs.mkdir(parents=True, exist_ok=True)

    for run_time in run_times:
        (logs / f"h024_read_only_vps_observer_{_stamp(run_time)}.log").write_text(
            "H024 read-only VPS observer scheduled wrapper finished.\n"
            "Status: COMPLETED\n"
            "Exit code: 0\n",
            encoding="utf-8",
        )

    _write_json(
        runtime / "last_run_summary.json",
        {
            "status": "COMPLETED",
            "exit_code": 0,
            "completed_at_utc": _iso(max(run_times)),
        },
    )

    packet_specs = {
        "healthcheck": reports / "h024_read_only_vps_observer_healthcheck.json",
        "task_state": reports / "h024_read_only_vps_observer_task_state.json",
        "recovery_drill": reports / "h024_read_only_vps_recovery_drill_preview.json",
        "evidence_bundle": reports / "h024_read_only_vps_observer_evidence_bundle.json",
        "continuity_summary": reports / "h024_read_only_vps_observer_continuity_summary.json",
    }

    overrides = packet_name_to_override or {}

    for name, path in packet_specs.items():
        packet = _base_packet(now)
        if name == "healthcheck":
            packet.pop("generated_at_utc")
            packet["checked_at_utc"] = _iso(now)
        if name == "task_state":
            packet["task_name"] = "H024 Read Only VPS Observer"
            packet["last_task_result"] = 0
        packet.update(overrides.get(name, {}))
        _write_json(path, packet)


def _run_builder(root: Path, *, success: bool) -> dict[str, Any]:
    cmd = [
        _powershell(),
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCRIPT),
        "-Root",
        str(root),
        "-TaskName",
        "H024 Read Only VPS Observer",
        "-ExpectedIntervalMinutes",
        "5",
        "-MinRunCount",
        "4",
        "-MinCadenceWindowMinutes",
        "15",
        "-MaxLatestRunAgeMinutes",
        "30",
        "-MaxPacketAgeMinutes",
        "60",
        "-MaxAllowedGapMinutes",
        "10",
        "-MinInterRunGapMinutes",
        "3",
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)

    if success:
        assert result.returncode == 0, result.stdout + result.stderr
    else:
        assert result.returncode != 0, result.stdout + result.stderr

    output = root / "reports" / "h024_read_only_vps_observer_scheduled_cadence_summary.json"
    assert output.exists()
    return json.loads(output.read_text(encoding="utf-8"))


def _violation_codes(packet: dict[str, Any]) -> set[str]:
    return {item["code"] for item in packet["violations"]}


def test_scheduled_cadence_summary_passes_with_real_cadence_span(tmp_path: Path) -> None:
    _make_fixture(tmp_path)
    packet = _run_builder(tmp_path, success=True)

    assert packet["verdict"] == "PASS"
    assert packet["observed_run_count"] == 4
    assert packet["effective_new_entries_blocked"] is True
    assert packet["broker_mutation_authorized"] is False
    assert packet["order_check_authorized"] is False
    assert packet["order_send_authorized"] is False
    assert packet["entry_authorized"] is False
    assert packet["close_modify_authorized"] is False
    assert packet["symbol_select_authorized"] is False
    assert packet["scheduled_cadence_summary_authorizes_trading"] is False


def test_scheduled_cadence_summary_fails_closed_when_too_few_logs(tmp_path: Path) -> None:
    _make_fixture(tmp_path, run_offsets_minutes=[13, 8, 3])
    packet = _run_builder(tmp_path, success=False)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert "scheduled_log_count_insufficient" in _violation_codes(packet)


def test_scheduled_cadence_summary_fails_closed_when_logs_are_clustered(tmp_path: Path) -> None:
    _make_fixture(tmp_path, run_offsets_minutes=[6, 5, 4, 3])
    packet = _run_builder(tmp_path, success=False)

    assert packet["verdict"] == "FAIL_CLOSED"
    codes = _violation_codes(packet)
    assert "scheduled_log_span_insufficient" in codes
    assert "scheduled_log_clustered" in codes


def test_scheduled_cadence_summary_fails_closed_when_latest_run_is_stale(tmp_path: Path) -> None:
    _make_fixture(tmp_path, run_offsets_minutes=[80, 75, 70, 65])
    packet = _run_builder(tmp_path, success=False)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert "scheduled_latest_run_stale" in _violation_codes(packet)


def test_scheduled_cadence_summary_fails_closed_when_upstream_packet_not_pass(tmp_path: Path) -> None:
    _make_fixture(
        tmp_path,
        packet_name_to_override={
            "recovery_drill": {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_TEST",
            }
        },
    )
    packet = _run_builder(tmp_path, success=False)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert "recovery_drill_evidence_verdict_not_pass" in _violation_codes(packet)


def test_scheduled_cadence_summary_fails_closed_on_unsafe_true_flag(tmp_path: Path) -> None:
    _make_fixture(
        tmp_path,
        packet_name_to_override={
            "evidence_bundle": {
                "order_send_authorized": True,
            }
        },
    )
    packet = _run_builder(tmp_path, success=False)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert "evidence_bundle_unsafe_true_flag" in _violation_codes(packet)

def test_scheduled_cadence_summary_uses_latest_cadence_segment_despite_older_noise(tmp_path: Path) -> None:
    _make_fixture(
        tmp_path,
        run_offsets_minutes=[
            170,
            123,
            70,
            69,
            59,
            54,
            49,
            44,
            39,
            34,
            29,
            24,
            19,
            14,
            9,
            4,
        ],
    )
    packet = _run_builder(tmp_path, success=True)

    assert packet["verdict"] == "PASS"
    assert packet["raw_observed_run_count"] == 16
    assert packet["observed_run_count"] >= 4
    assert packet["min_observed_gap_minutes"] >= 3
    assert packet["max_observed_gap_minutes"] <= 10
    assert packet["scheduled_cadence_summary_authorizes_trading"] is False
