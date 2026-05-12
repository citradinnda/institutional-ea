# H024 Read-Only VPS Task-State Audit And Recovery Runbook

This runbook covers the H024 read-only VPS observer task-state audit, restart/recovery drill preview, and operator alert surface.

This is operational VPS resilience work only. It does not authorize trading, broker mutation, entries, close/modify, executable request construction, live broker request construction, or an order-capable trading loop.

## Scope

Implemented operational checks:

- read-only Windows Scheduled Task state audit
- task installed / missing detection
- enabled / disabled state detection
- trigger interval detection
- last run time detection
- last task result detection
- stale scheduler run detection
- local operator alert JSON/text/console surface
- restart/recovery drill preview using local evidence only

Runtime/generated outputs stay under `reports/` and must remain untracked.

## Scripts

### Task-state audit

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15

Default output:

reports/h024_read_only_vps_observer_task_state.json
reports/h024_read_only_vps_observer_operator_alert.json
reports/h024_read_only_vps_observer_operator_alert.txt

PASS state:

READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed state:

FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_TASK_STATE_UNVERIFIED_NO_TRADING_AUTHORIZED

Common fail-closed causes:

task not installed
task disabled
missing trigger
trigger interval mismatch
missing last run time
stale last run time
non-zero last task result
scheduled task cmdlets unavailable
Recovery drill preview
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60

Default output:

reports/h024_read_only_vps_recovery_drill_preview.json
reports/h024_read_only_vps_recovery_drill_operator_alert.json
reports/h024_read_only_vps_recovery_drill_operator_alert.txt

PASS state:

READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed state:

FAIL_CLOSED_READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_UNVERIFIED_NO_TRADING_AUTHORIZED

The recovery drill preview validates local evidence from:

reports/h024_read_only_vps_observer_task_state.json
reports/h024_read_only_vps_observer_healthcheck.json

It does not modify the scheduled task, install anything, unregister anything, or contact an external alerting system.

Standard restart/recovery drill

Run from the repository root:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

git status
git log --oneline -8

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60

If the task is missing, preview the install command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview

Only a human operator should decide whether to install or repair the scheduled task. The preview does not register a task.

Hard safety boundary

Every task-state and recovery output must preserve:

trading_authorized: false
broker_mutation_authorized: false
order_check_authorized: false
order_send_authorized: false
entry_authorized: false
close_modify_authorized: false
xauusd_order_authorized: false
usdjpy_order_authorized: false
trading_loop_authorized: false
automatic_execution_authorized: false
live_broker_request_constructed: false
executable_trade_request_constructed: false
mt5_request_dictionary_constructed: false
symbol_select_authorized: false

PASS means operational evidence is coherent for read-only observation only.

PASS does not authorize trading or close/modify.