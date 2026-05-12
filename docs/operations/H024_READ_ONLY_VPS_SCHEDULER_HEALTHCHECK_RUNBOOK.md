# H024 Read-Only VPS Scheduler, Healthcheck, and Log Rotation Runbook

This runbook operationalizes the H024 read-only VPS observer path. It does not authorize trading, broker mutation, entries, close/modify actions, live execution payloads, or an order-capable trading loop.

## Purpose

The VPS observer already has a one-shot read-only runner. This milestone adds:

- a scheduled wrapper around the existing one-shot observer
- Windows Task Scheduler install/preview script
- Windows Task Scheduler disable/uninstall script
- healthcheck script
- last-run summary
- log capture
- log retention and rotation
- stale evidence detection
- VPS boot/restart/recovery operator workflow

## Files

- `scripts/run_h024_read_only_vps_observer_scheduled.ps1`
- `scripts/install_h024_read_only_vps_observer_task.ps1`
- `scripts/uninstall_h024_read_only_vps_observer_task.ps1`
- `scripts/check_h024_read_only_vps_observer_health.ps1`

Runtime outputs remain untracked under:

- `reports/runtime/h024_read_only_vps_observer/logs/`
- `reports/runtime/h024_read_only_vps_observer/last_run_summary.json`
- `reports/h024_read_only_vps_observer_healthcheck.json`

## Base verification

From the repo root:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
python -m pytest tests\test_h024_read_only_vps_deployment_readiness_aggregate.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1
python scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass

If exact-ticket evidence is stale, refresh the exact-ticket stack using the current operator-reported bar-age flag, then rerun the observer.

Run scheduled wrapper once
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1

Expected:

one observer log under reports/runtime/h024_read_only_vps_observer/logs/
last_run_summary.json updated
existing observer/readiness safety boundaries preserved
Healthcheck
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1

The healthcheck reads:

latest VPS readiness aggregate
latest black-swan guard
latest heartbeat packet
latest no-mutation gate packet
latest scheduled wrapper summary
latest scheduled wrapper log path

It fails closed when evidence is missing, malformed, stale, failed, or internally reports violations.

Preview scheduled task install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview
Install scheduled task
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -IntervalMinutes 5 -Force

Default behavior:

task name: H024 Read Only VPS Observer
interval: every 5 minutes
target: scheduled wrapper script
log retention: latest 288 logs or 14 days
Preview uninstall
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1 -Preview
Uninstall
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1
VPS boot/restart recovery

After VPS boot or restart:

Confirm MetaTrader terminal and the Python virtual environment are available.
Run the scheduled wrapper once manually.
Run the healthcheck.
Confirm the scheduled task exists.
Confirm logs are rotating under the untracked runtime report directory.
If healthcheck fails closed, inspect the violations and refresh stale upstream evidence only when appropriate.
Safety posture

PASS means the observer path is coherent for read-only monitoring.

PASS does not authorize live execution, broker mutation, entries, close/modify actions, or an order-capable trading loop.
