# H024 Read-Only VPS Observer Scheduled Cadence Summary Runbook

This runbook is for the local Windows read-only observer path. The historical file names still use `vps`, but the current target is the user's local Windows machine, Windows Task Scheduler, local MT5, local PowerShell, local Python, and local `reports/`.

## Purpose

`scripts/build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1` strengthens the observer proof from immediate/manual two-run continuity to cadence-compatible Windows Task Scheduler continuity.

It reads existing local evidence only:

- `reports/runtime/h024_read_only_vps_observer/last_run_summary.json`
- `reports/runtime/h024_read_only_vps_observer/logs/*.log`
- `reports/h024_read_only_vps_observer_healthcheck.json`
- `reports/h024_read_only_vps_observer_task_state.json`
- `reports/h024_read_only_vps_recovery_drill_preview.json`
- `reports/h024_read_only_vps_observer_evidence_bundle.json`
- `reports/h024_read_only_vps_observer_continuity_summary.json`

It emits generated evidence only:

- `reports/h024_read_only_vps_observer_scheduled_cadence_summary.json`
- `reports/h024_read_only_vps_observer_scheduled_cadence_summary.txt`

`reports/` must remain untracked.

## Safety Boundary

This script is read-only. It does not call MT5 trading APIs. It does not call `order_check`, `order_send`, or `symbol_select`. It does not construct live broker requests, executable request dictionaries, entries, closes, modifies, SL/TP changes, or trading loops.

A PASS verdict means the scheduled-cadence evidence is coherent for read-only observer monitoring only.

A PASS verdict does not authorize trading.

## Typical Use

Refresh upstream evidence first:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60

Then build scheduled-cadence summary:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1 -ExpectedIntervalMinutes 5 -MinRunCount 4 -MinCadenceWindowMinutes 15 -MaxLatestRunAgeMinutes 30 -MaxPacketAgeMinutes 60

Expected PASS output:

H024 read-only VPS observer scheduled cadence summary verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Fail-Closed Conditions

The summary fails closed when any of these are true:

Required upstream packet is missing.
Required upstream packet is stale.
Required upstream packet verdict is not PASS.
Any unsafe trading or broker mutation flag is true.
Last-run summary is missing.
Last-run summary reports a nonzero exit code.
Too few observer logs are present.
Logs are too tightly clustered to prove cadence.
Logs do not span the minimum cadence window.
Latest observed run is stale.
Observed log gaps are too large.
Validation

Focused tests:

python -m pytest tests\test_h024_read_only_vps_observer_scheduled_cadence_summary.py

Broader observer tests:

python -m pytest `
  tests\test_h024_read_only_vps_task_state_recovery.py `
  tests\test_h024_read_only_vps_observer_evidence_bundle.py `
  tests\test_h024_read_only_vps_observer_continuity_summary.py `
  tests\test_h024_read_only_vps_observer_scheduled_cadence_summary.py

## Latest Cadence Segment Rule

The summary scores the latest contiguous cadence-compatible log segment, not every historical log in the runtime log directory.

This is intentional. Older manual wrapper runs, old startup gaps, and historical interruptions should not contaminate the current scheduled-cadence proof window. The latest segment must still satisfy run count, span, freshness, and gap requirements.

The script remains read-only and non-authorizing.
