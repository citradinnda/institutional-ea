# H024 Free Local Read-Only Demo Deployment Readiness Runbook

## Purpose

This is the capstone local demo-readiness packet for H024.

It answers one narrow question:

```text
Is the free local Windows no-console read-only observer demo-ready for status observation?

It does not authorize trading.

It does not authorize broker mutation.

It does not authorize request construction.

It does not move the project to Oracle VPS or paid VPS.

Inputs validated

The builder consumes the existing local observer proof stack:

Windows Task Scheduler action:
  Execute = wscript.exe
  Argument = scripts/run_h024_read_only_vps_observer_scheduled_hidden.vbs

Scheduler cadence:
  expected interval = 5 minutes

Observer packets:
  reports/h024_read_only_vps_observer_healthcheck.json
  reports/h024_read_only_vps_observer_task_state.json
  reports/h024_read_only_vps_recovery_drill_preview.json
  reports/h024_read_only_vps_observer_evidence_bundle.json
  reports/h024_read_only_vps_observer_continuity_summary.json
  reports/h024_read_only_vps_observer_scheduled_cadence_summary.json

Runtime summary:
  reports/runtime/h024_read_only_vps_observer/last_run_summary.json

The strict cadence requirement is:

MinScheduledRunCount = 12
MinScheduledSpanMinutes = 55
ExpectedIntervalMinutes = 5
Command
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify_h024_free_local_read_only_demo_deployment_readiness.ps1
Outputs
reports/h024_free_local_read_only_demo_deployment_readiness.json
reports/h024_free_local_read_only_demo_deployment_readiness.txt

Do not commit reports/.

reports/ is generated runtime evidence only.

PASS meaning

PASS means:

The free local Windows no-console read-only observer is demo-ready for status observation only.

PASS does not authorize trading.

PASS does not authorize broker mutation.

PASS does not authorize order checks.

PASS does not authorize order sends.

PASS does not authorize symbol selection.

PASS does not authorize live broker request construction.

PASS does not authorize executable trade request construction.

PASS does not authorize entries.

PASS does not authorize close/modify.

PASS does not authorize SL/TP modification.

PASS does not authorize an order-capable trading loop.

FAIL_CLOSED meaning

FAIL_CLOSED means one or more proof inputs is missing, stale, malformed, non-PASS, unsafe, or insufficient.

Correct response:

inspect violations
refresh read-only evidence if needed
do not bypass
do not trade
do not mutate broker state
Infrastructure boundary

This milestone is free local Windows only.

No Oracle VPS.

No paid VPS.

No Linux migration.

No SSH workflow.

No trading EA deployment.

Commit discipline

Commit only source, tests, scripts, and docs.

Never commit:

reports/
