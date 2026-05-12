# H024 Read-Only VPS Observer Continuity Summary Runbook

## Purpose

This runbook describes the local Windows read-only observer continuity summary.

The continuity summary is operational evidence only. It reads existing local observer runtime logs and evidence packets under `reports/` and emits a JSON/text summary proving that repeated local observer runs are coherent.

It does not authorize trading, broker mutation, live execution, automatic remediation, or any account-changing action.

## Builder

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60

Default outputs:

reports/h024_read_only_vps_observer_continuity_summary.json
reports/h024_read_only_vps_observer_continuity_summary.txt
Inputs

The builder reads:

reports/runtime/h024_read_only_vps_observer/last_run_summary.json
reports/runtime/h024_read_only_vps_observer/logs/*.log
reports/h024_read_only_vps_observer_healthcheck.json
reports/h024_read_only_vps_observer_task_state.json
reports/h024_read_only_vps_recovery_drill_preview.json
reports/h024_read_only_vps_observer_evidence_bundle.json
PASS Meaning

PASS means the local observer continuity evidence is coherent for read-only supervision.

PASS does not authorize trading or live execution.

FAIL_CLOSED Meaning

FAIL_CLOSED means an operator must review the local observer evidence before relying on continuity proof. It still does not authorize trading or live execution.
