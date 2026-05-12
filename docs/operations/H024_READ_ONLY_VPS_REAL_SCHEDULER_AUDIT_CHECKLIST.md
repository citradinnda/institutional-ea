# H024 Read-Only VPS Real Scheduler Audit Checklist And Evidence Bundle

This runbook covers the real VPS scheduler install/audit path for the H024 read-only VPS observer.

It does not authorize trading. It does not authorize close/modify. It does not authorize broker mutation, `order_check`, `order_send`, `symbol_select`, new entries, SL/TP changes, executable request dictionaries, live broker requests, external alert mutation, or an order-capable trading loop.

## Purpose

The goal is to prove, with local evidence, that the read-only VPS observer is operational:

- repository state is known
- scheduled wrapper has produced a recent last-run summary
- latest observer log is available
- healthcheck packet is fresh and PASS
- real scheduled task state packet is fresh and PASS
- recovery drill preview packet is fresh and PASS
- all trading and mutation booleans remain false
- generated evidence remains under `reports/`
- `reports/` remains untracked

This is practical VPS operations work, not a governance-only layer.

## Hard boundary

PASS means the local evidence bundle is coherent for read-only observation only.

PASS does not mean:

- trading is authorized
- close/modify is authorized
- `order_check` is authorized
- `order_send` is authorized
- `symbol_select` is authorized
- a live broker request may be built
- an executable trade request dictionary may be built
- automatic execution is enabled
- external alert mutation is enabled
- scheduler mutation is authorized by the bundle

## Standard real VPS sequence

From the repository root:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

Check the repository state:

git status
git log --oneline -8

If exact-ticket evidence is stale, refresh the exact-ticket stack first:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

Run the scheduled wrapper once manually:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1

Run the healthcheck:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60

Audit the real scheduled task state:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15

Run the recovery drill preview:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60

Build the local evidence bundle:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60

Expected PASS:

H024 read-only VPS observer evidence bundle verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0

The default bundle outputs are:

reports/h024_read_only_vps_observer_evidence_bundle.json
reports/h024_read_only_vps_observer_evidence_bundle.txt

These are generated runtime reports and must remain untracked.

If the scheduled task is missing

First preview the install:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview

Only if the human operator chooses to install the scheduled task:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -IntervalMinutes 5 -Force

Installing the scheduled task still does not authorize trading.

After installation, wait for or manually run the scheduled wrapper, then rerun:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
Optional install-preview capture

If task-state evidence indicates the scheduled task may be missing, the evidence bundle can capture a local install preview without registering anything:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60 -IncludeInstallPreviewIfTaskMissing

This writes:

reports/h024_read_only_vps_observer_install_preview_output.txt

This is local evidence only.

Failure handling

Do not weaken checks to force PASS.

A FAIL_CLOSED bundle is correct when:

a packet is missing
a packet is malformed
a packet is stale
healthcheck is not PASS
task-state is not PASS
recovery drill preview is not PASS
latest log is missing
last-run summary lacks an exit code
last-run summary reports a non-zero exit code
git metadata cannot be read

Operator action is review-only. No automatic remediation is authorized by this bundle.

Commit discipline

Do not add reports/.

Use:

git status
python -m pytest tests\test_h024_read_only_vps_observer_evidence_bundle.py
git add -- scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 docs\operations\H024_READ_ONLY_VPS_REAL_SCHEDULER_AUDIT_CHECKLIST.md tests\test_h024_read_only_vps_observer_evidence_bundle.py
git diff --cached --check
git commit -m "Add H024 read-only VPS observer evidence bundle"
git push
git status

Final git status should show only reports/ untracked, if runtime reports exist.

Do not add `reports/`.

## Explicit non-authorization reminders

The evidence bundle does not authorize `order_check`.
The evidence bundle does not authorize `order_send`.
The evidence bundle does not authorize `symbol_select`.
