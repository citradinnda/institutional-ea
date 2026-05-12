# HANDOFF_118 - Fully Self-Contained H024 Local Read-Only Demo Dashboard, Scheduler Staleness Incident, And New Dry-Run Trading-Enablement Boundary

This handoff supersedes HANDOFF_117 and all older handoffs.

This is the current source of truth for the next AI.

It is intentionally redundant. The next AI should not need hidden chain-of-thought, older handoffs, chat history, or generated `reports/` files to understand:

1. What project this is.
2. What has been completed.
3. What broke.
4. Why it broke.
5. What remains forbidden in H024.
6. What is newly authorized in the next separate trading-enablement phase.
7. What exact source fix should happen next.
8. What commands should be run.
9. What must remain untracked.

---

## 1. Project Identity

Project:

```text
institutional-ea

Repository path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

User's current operating system/context:

Local Windows PC
PowerShell
Windows Task Scheduler
Local Python virtual environment
Local MT5 terminal
Local Git repository
Generated reports/

The current target has been:

free local Windows recurring read-only observer proof and dashboard demo

This is not Oracle VPS.

This is not paid VPS.

No Oracle VPS is assumed to exist.

No paid VPS should be introduced unless the user explicitly changes direction.

2. Current User Mood And Required Style

The user is frustrated by:

too many packet/governance steps
readiness checks repeatedly failing on stale internal evidence
dashboard UX not being visually polished
not yet reaching trading capability

The next AI should be direct and operational.

Do not make the user run huge exploratory blocks unless necessary.

Do not add more packet layers unless they directly unblock:

1. fixing the read-only scheduled observer loop,
2. restoring clean dashboard readiness,
3. starting the new dry-run trading-enablement phase.

The user likes concise suggested next prompts after each milestone.

3. Recent Commit Timeline

Known recent commits on main:

047fcf7 Add H024 local read-only demo dashboard
3261878 Add H024 free local read-only demo readiness packet
5abbc0a or nearby prior state from HANDOFF_117 continuation
5814450 Fix H024 scheduled cadence latest segment proof
3b26baf Fix H024 read-only observer scheduled cadence summary
e385819 Add H024 read-only observer scheduled cadence summary
bc62c83 Add H024 read-only observer continuity tests and runbook
a7a377b Add H024 read-only observer continuity summary
beafd0f Fix H024 read-only observer timestamp aliases
5a1c4cf Add H024 read-only VPS observer evidence bundle
4b99dc7 Add H024 read-only VPS task state recovery audit

Do not rewrite pushed history.

Fix forward.

4. Final Known Git State Before This Handoff

After dashboard commit 047fcf7, final git state was:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is generated runtime/demo evidence.

Never commit reports/.

5. What HANDOFF_117 Proved Before This Work

HANDOFF_117 established:

H024 local Windows no-console scheduled observer natural-run proof: PASS

The scheduled task action was verified as:

Execute:   wscript.exe
Arguments: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs

The task cadence was intended to remain:

5 minutes

The scheduled observer uses:

Windows Task Scheduler
-> wscript.exe
-> scripts/run_h024_read_only_vps_observer_scheduled_hidden.vbs
-> scripts/run_h024_read_only_vps_observer_scheduled.ps1
-> scripts/run_h024_read_only_vps_observer_once.ps1

The VBS hidden launcher exists to avoid visible PowerShell popups every 5 minutes.

The previous proven operational packets were:

healthcheck               PASS 0 violations
task_state                PASS 0 violations
recovery_drill_preview    PASS 0 violations
evidence_bundle           PASS 0 violations
continuity_summary        PASS 0 violations
scheduled_cadence_summary PASS 0 violations

Important: those PASS states never authorized trading.

6. H024 Absolute Read-Only Safety Boundary

H024 remains a read-only observer/demo track.

Inside the existing H024 observer, scheduler, readiness, and dashboard stack, do not add:

order_check
order_send
live broker request construction
executable trade request construction
automatic entries
automatic close/modify
manual approval code that actually closes/modifies
SL/TP modification
broker mutation
symbol_select
order-capable trading loops
code paths that close the canary
code paths that modify the canary
code paths that scale the canary
code paths that place XAUUSD orders
code paths that place USDJPY orders

Interpretation rule:

PASS = evidence/check/packet/dashboard status is coherent for read-only observation only.
PASS != authorization to trade.
PASS != authorization to close.
PASS != authorization to modify.
PASS != authorization to call order_check.
PASS != authorization to call order_send.
PASS != authorization to construct live broker requests.
PASS != authorization to run an order-capable loop.

If every H024 packet says PASS, H024 still does not trade.

7. Completed Milestone: Free Local Read-Only Demo Readiness Packet

Commit:

3261878 Add H024 free local read-only demo readiness packet

Added files:

scripts/build_h024_free_local_read_only_demo_deployment_readiness.ps1
scripts/verify_h024_free_local_read_only_demo_deployment_readiness.ps1
tests/test_h024_free_local_read_only_demo_deployment_readiness.py
docs/operations/H024_FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_RUNBOOK.md

Focused tests passed after a builder patch:

9 passed

Verifier successful output when evidence was clean:

H024 free local read-only demo deployment readiness verdict: PASS
Operator state: FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Read-only demo ready: True
Trading authorized: False
Broker mutation authorized: False

The readiness packet aggregates:

scheduled task Execute=wscript.exe
scheduled task argument points to hidden VBS launcher
5-minute interval unchanged
healthcheck PASS
task-state PASS
recovery drill preview PASS
evidence bundle PASS
continuity summary PASS
strict scheduled cadence summary PASS with at least 12 runs and at least 55 minutes span
latest run summary COMPLETED with exit_code 0
unsafe authorization flags all false
reports/ not tracked in git

It does not authorize trading.

8. Completed Milestone: Local Read-Only Demo Dashboard

Commit:

047fcf7 Add H024 local read-only demo dashboard

Added files:

scripts/start_h024_local_read_only_demo_dashboard.ps1
tests/test_h024_local_read_only_demo_dashboard.py
docs/operations/H024_LOCAL_READ_ONLY_DEMO_DASHBOARD_RUNBOOK.md

Focused tests passed:

7 passed

Generated dashboard path:

reports/demo/h024_local_read_only_demo_dashboard.html

Dashboard launch command:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start_h024_local_read_only_demo_dashboard.ps1

Open already-generated dashboard:

cd C:\Users\equin\Documents\institutional-ea
Start-Process .\reports\demo\h024_local_read_only_demo_dashboard.html

The dashboard displays a visible boundary:

READ-ONLY DEMO ONLY - NO TRADING AUTHORIZED

The actual generated HTML uses a Unicode em dash in the banner, but the PowerShell source keeps the script ASCII-safe using:

[char]0x2014

This was necessary because Windows PowerShell misread an em dash literal and caused parser failures.

Dashboard implementation issues already fixed

The following bugs were encountered and fixed before commit 047fcf7:

Join-Path was incorrectly used inside an array, producing:
Cannot convert 'System.Object[]' to the type 'System.String' required by parameter 'ChildPath'

Fixed by building candidate file names first and piping them into Join-Path.

The exact Unicode banner literal broke PowerShell parsing:
Unexpected token 'NO' in expression or statement.

Fixed by using ASCII-safe source and [char]0x2014.

Helper function H collided with PowerShell's built-in h alias / history behavior, causing:
Cannot bind parameter 'Id'. Cannot convert value "healthcheck" to type "System.Int64".

Fixed by renaming the helper to:

HtmlSafe
The dashboard originally aborted when readiness failed. It was patched into a fail-safe dashboard that still generates HTML and reports failure.

This is correct operator-console behavior.

9. Current Dashboard Behavior

When readiness is clean, the dashboard shows readiness PASS.

When readiness refresh fails, the dashboard still generates HTML and shows:

Readiness refresh status: FAILED
Readiness verdict: FAIL_CLOSED
Read-only demo ready: False
Trading authorized: False
Broker mutation authorized: False

This is correct.

It should not hide failures.

It should not force readiness PASS.

It should not delete logs.

It should not suppress violations.

It should not authorize trading.

10. Current Incident: Why Readiness Is Still Not Clean

The user ran the dashboard/readiness after the dashboard commit.

Initial task-state failed because the scheduled wrapper had failed:

H024 read-only VPS observer task-state verdict: FAIL_CLOSED
Operator state: FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_TASK_STATE_UNVERIFIED_NO_TRADING_AUTHORIZED
Violations: 1
scheduled_task_last_result_nonzero

Observed scheduled task info during this period:

LastRunTime           : 13/05/2026 00.59.49
LastTaskResult        : 1
NextRunTime           : 13/05/2026 01.04.48
NumberOfMissedRuns    : 0

The wrapper summary showed:

{
  "status": "FAILED",
  "exit_code": 1,
  "read_only_observer_only": true,
  "trading_authorized": false,
  "broker_mutation_authorized": false,
  "live_execution_authorized": false
}

The wrapper itself failed because the black-swan guard failed closed.

The black-swan guard failed closed because exact-ticket close/modify upstream evidence became stale after the max age of 3600 seconds.

11. Exact Root Cause: Stale Exact-Ticket Evidence Feeding Black-Swan Guard

The scheduled observer one-shot currently says:

=== exact-ticket stack ===
Using existing exact-ticket governance/decision/evidence/preview reports as upstream evidence.
The readiness aggregate and black-swan guard fail closed if those reports are missing, stale, malformed, fail-closed, or unsafe.

This means it uses existing exact-ticket evidence reports instead of refreshing them during every scheduled observer run.

Those reports become stale after about 3600 seconds.

When stale, the black-swan guard fails closed.

Example violations from failed logs:

VIOLATION: record 1: embedded violation: exact_ticket_close_modify_governance: upstream evidence stale: age_seconds=3867.431 max=3600
VIOLATION: record 1: embedded violation: exact_ticket_decision_artifact_validator: upstream evidence stale: age_seconds=3865.856 max=3600
VIOLATION: record 1: embedded violation: pre_action_evidence_aggregate: upstream evidence stale: age_seconds=3865.809 max=3600
VIOLATION: record 1: embedded violation: bar_age_exit_condition_evidence: upstream evidence stale: age_seconds=3864.175 max=3600
VIOLATION: record 1: embedded violation: manual_approval_gate_preview: upstream evidence stale: age_seconds=3862.772 max=3600
VIOLATION: record 1: embedded violation: operator_decision_v2_preview: upstream evidence stale: age_seconds=3862.600 max=3600
VIOLATION: record 1: embedded violation: execution_readiness_dry_run_schema_preview: upstream evidence stale: age_seconds=3862.190 max=3600
VIOLATION: record 1: --require-pass rejects verdict FAIL_CLOSED

Later examples:

age_seconds=4076.285 max=3600
age_seconds=4163.353 max=3600

This was not a broker problem.

This was not a task-scheduler structural problem.

This was not a MT5 connectivity problem.

The runtime read-only observer components were passing.

The specific failure was stale exact-ticket evidence.

12. Manual Refresh Proved The Root Cause

The user refreshed exact-ticket read-only evidence manually.

Commands used in principle:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

After refreshing, the black-swan guard passed:

=== read-only black-swan guard ===
Verdict: PASS
Violations: 0
Operator state: BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Operator next action: CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
black_swan_guard_clear: True
black_swan_guard_triggered: False
black_swan_guard_authorizes_trading: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False

The deployment readiness aggregate passed:

=== read-only VPS deployment readiness aggregate ===
Verdict: PASS
Violations: 0
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED
read_only_observer_workflow_authorized_for_operator_review: True
vps_deployment_readiness_authorizes_trading: False

The scheduled wrapper then completed:

H024 read-only VPS observer run complete.
No trading, broker mutation, order_check, order_send, symbol_select, entry, close/modify, executable trade request, live broker request, or order-capable trading loop was authorized.

H024 read-only VPS observer scheduled wrapper finished.
Status: COMPLETED
Exit code: 0

Therefore the durable fix is obvious:

Refresh exact-ticket read-only evidence inside scripts/run_h024_read_only_vps_observer_once.ps1 before black-swan guard runs.
13. Task-State Recovery

After the stale-evidence incident, Task Scheduler retained a nonzero result.

The user then started the scheduled task through Windows Task Scheduler:

Start-ScheduledTask -TaskName "H024 Read Only VPS Observer"

Observed:

State=Running LastTaskResult=267009 LastRunTime=05/13/2026 01:08:46
State=Running LastTaskResult=0 LastRunTime=05/13/2026 01:08:46
State=Ready LastTaskResult=0 LastRunTime=05/13/2026 01:08:46

Final task info:

LastRunTime        : 13/05/2026 01.08.46
LastTaskResult     : 0
NextRunTime        : 13/05/2026 01.09.48
NumberOfMissedRuns : 0

Task-state then passed:

H024 read-only VPS observer task-state verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0

Important distinction:

Manual wrapper run success does not update Windows Task Scheduler LastTaskResult.
Only a task run through Windows Task Scheduler updates LastTaskResult.
14. Continuity Recovery

After task-state recovered, readiness still failed because continuity summary saw failed logs from the stale-evidence incident.

Continuity violations:

runtime_log_completion_marker_missing:
  h024_read_only_vps_observer_20260512T160450490Z.log
runtime_log_completion_marker_missing:
  h024_read_only_vps_observer_20260512T160323723Z.log
runtime_log_completion_marker_missing:
  h024_read_only_vps_observer_20260512T155950497Z.log

insufficient_completed_observer_runs:
  Only 3 completed observer runtime logs were found in the newest window; required at least 6.

The user then let natural scheduled runs continue.

Continuity recovered naturally:

attempt 1:
  continuity_verdict: FAIL_CLOSED
  violations: 3

attempt 2:
  continuity_verdict: FAIL_CLOSED
  violations: 2

attempt 3:
  continuity_verdict: PASS
  violations: 0

H024 read-only VPS observer continuity summary verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0

Do not delete logs to force a pass.

Letting the continuity window recover naturally was correct.

15. Current Remaining Readiness Blocker

After continuity recovered, the user ran readiness/dashboard again.

Healthcheck passed:

H024 read-only VPS observer healthcheck verdict: PASS
Violations: 0

Task-state passed:

H024 read-only VPS observer task-state verdict: PASS
Violations: 0

Recovery drill passed:

H024 read-only VPS recovery drill preview verdict: PASS
Violations: 0

Evidence bundle passed:

H024 read-only VPS observer evidence bundle verdict: PASS
Violations: 0

Continuity passed:

H024 read-only VPS observer continuity summary verdict: PASS
Violations: 0

Scheduled cadence summary failed:

H024 read-only VPS observer scheduled cadence summary verdict: FAIL_CLOSED
Operator state: FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_UNVERIFIED_NO_TRADING_AUTHORIZED
Violations: 4

Dashboard therefore generated fail-safe HTML:

Readiness refresh status: FAILED
Readiness verdict: FAIL_CLOSED
Read-only demo ready: False
Trading authorized: False
Broker mutation authorized: False
Generated under reports/demo/. Do not commit reports/.

This is the current known state at handoff.

The exact scheduled cadence violations after the latest failure were not pasted. The next AI must inspect:

reports/h024_read_only_vps_observer_scheduled_cadence_summary.json

Look specifically at:

verdict
violations
observed_run_count
observed_span_minutes
min_observed_gap_minutes
max_observed_gap_minutes
observed_logs
latest_observed_run_at_utc

Likely cause:

The newest cadence-compatible segment was disturbed by the stale-evidence failure window and/or manual/scheduled clustered runs.

But do not guess. Inspect the JSON.

16. Current Operational Interpretation

This is not many unrelated problems.

It is one stale-evidence incident propagating through multiple readiness layers.

Correct mental model:

1. Exact-ticket evidence aged beyond 3600 seconds.
2. Black-swan guard failed closed.
3. Scheduled wrapper exited 1.
4. Task Scheduler recorded LastTaskResult 1.
5. Dashboard readiness failed.
6. Task-state recovered after a Windows Task Scheduler run returned 0.
7. Continuity recovered after enough natural successful runs.
8. Scheduled cadence summary is now the remaining readiness blocker.
9. Durable source fix is still needed so exact-ticket evidence refreshes before black-swan guard in each scheduled observer run.
17. Immediate Next Source Fix

Patch:

scripts/run_h024_read_only_vps_observer_once.ps1

Goal:

Refresh exact-ticket read-only evidence before black-swan guard runs.

The observer currently says it is using existing exact-ticket reports as upstream evidence. That must change.

Expected exact-ticket refresh commands to run before black-swan guard:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

Important: use the repo's actual Python invocation style inside PowerShell. Existing wrappers may use:

$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
& $Python scripts\...

Follow the existing style.

These builders are read-only and non-authorizing.

No trading is authorized by refreshing them.

18. Tests To Add For The Source Fix

Add a focused test file such as:

tests/test_h024_read_only_observer_exact_ticket_refresh_before_black_swan.py

Tests should prove:

scripts/run_h024_read_only_vps_observer_once.ps1 exists
the exact-ticket governance builder appears before black-swan guard
the decision artifact builder appears before black-swan guard
the pre-action evidence aggregate builder appears before black-swan guard
the bar-age exit-condition evidence builder appears before black-swan guard
the manual approval gate preview builder appears before black-swan guard
the operator decision v2 preview builder appears before black-swan guard
the execution readiness dry-run schema preview builder appears before black-swan guard
the observer still prints/declares no trading authorization
the observer does not contain order_send(
the observer does not contain .order_send
the observer does not contain order_check(
the observer does not contain .order_check
the observer does not contain symbol_select(
the observer does not contain .symbol_select
the observer does not contain TRADE_ACTION
the observer does not contain ORDER_TYPE_BUY
the observer does not contain ORDER_TYPE_SELL
the observer does not contain MqlTradeRequest

Do not use a brittle test that depends on exact line numbers.

Use substring order checks.

19. Validation Commands After Source Fix

After patching scripts/run_h024_read_only_vps_observer_once.ps1, run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

python -m pytest tests\test_h024_read_only_observer_exact_ticket_refresh_before_black_swan.py -q
python -m pytest tests\test_h024_local_read_only_demo_dashboard.py tests\test_h024_free_local_read_only_demo_deployment_readiness.py -q

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 30

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start_h024_local_read_only_demo_dashboard.ps1 -NoOpen

If task-state fails because Windows Task Scheduler still has an old nonzero result, run through Task Scheduler:

$TaskName = "H024 Read Only VPS Observer"
Start-ScheduledTask -TaskName $TaskName

do {
    Start-Sleep -Seconds 5
    $Task = Get-ScheduledTask -TaskName $TaskName
    $Info = Get-ScheduledTaskInfo -TaskName $TaskName
    Write-Host "State=$($Task.State) LastTaskResult=$($Info.LastTaskResult) LastRunTime=$($Info.LastRunTime)"
} while ($Task.State -eq "Running")

Get-ScheduledTaskInfo -TaskName $TaskName | Format-List LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns

Then rerun task-state and dashboard.

If continuity fails because old failed logs are still in the newest continuity window, let natural successful scheduled runs accumulate. Do not delete logs.

If scheduled cadence fails, inspect:

$Cadence = Get-Content -Raw reports\h024_read_only_vps_observer_scheduled_cadence_summary.json | ConvertFrom-Json
$Cadence | Select-Object verdict, operator_state, observed_run_count, observed_span_minutes, min_observed_gap_minutes, max_observed_gap_minutes, latest_observed_run_at_utc | Format-List
$Cadence.violations | Format-List *
$Cadence.observed_logs | Format-Table observed_run_at_utc,file_name -AutoSize

Do not bypass cadence failures.

20. Commit Discipline For The Source Fix

Never commit reports/.

After source fix:

git status --short

git add -- `
  scripts\run_h024_read_only_vps_observer_once.ps1 `
  tests\test_h024_read_only_observer_exact_ticket_refresh_before_black_swan.py

git reset -- reports 2>$null

git diff --cached --check
git diff --cached --stat

git commit -m "Refresh H024 exact-ticket evidence before black-swan guard"
git push

git status --short
git status

If docs are updated, include only docs.

21. Known Canary State

Known H024 demo canary:

Server: Exness-MT5Trial6
Account currency: USD
Runtime symbol: XAUUSDm
Model symbol: XAUUSD
Side: sell
MT5 position type: 1
Volume: 0.01
Magic: 240024
Ticket: 4413054432
Identifier: 4413054432
Entry deal: 3788869526

Recent observed state:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0

Recent account examples from logs:

Account server: Exness-MT5Trial6
Account currency: USD
Balance: 10000.0
Equity: approximately 10057
Profit: approximately 57
Margin: 2.36
Free margin: approximately 10055
Margin level: approximately 426150

The user has said the trade is still open.

Do not close it through project code.

If the user wants it closed before any trading-enablement phase, the safe current path is manual close inside MT5 outside this project code.

22. Known Existing File Map
Scheduler and observer
scripts/run_h024_read_only_vps_observer_scheduled_hidden.vbs
scripts/run_h024_read_only_vps_observer_scheduled.ps1
scripts/run_h024_read_only_vps_observer_once.ps1
Existing local demo readiness
scripts/build_h024_free_local_read_only_demo_deployment_readiness.ps1
scripts/verify_h024_free_local_read_only_demo_deployment_readiness.ps1
tests/test_h024_free_local_read_only_demo_deployment_readiness.py
docs/operations/H024_FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_RUNBOOK.md
Dashboard
scripts/start_h024_local_read_only_demo_dashboard.ps1
tests/test_h024_local_read_only_demo_dashboard.py
docs/operations/H024_LOCAL_READ_ONLY_DEMO_DASHBOARD_RUNBOOK.md
reports/demo/h024_local_read_only_demo_dashboard.html
Runtime safety stack
scripts/build_h024_runtime_safety_heartbeat_jsonl.py
scripts/build_h024_runtime_safety_lockout_jsonl.py
scripts/build_h024_runtime_tick_spread_safety_supervisor_jsonl.py
scripts/build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
scripts/build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
scripts/build_h024_runtime_safety_aggregate_supervisor_jsonl.py
scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py
Exact-ticket close/modify read-only stack
scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py
Black-swan and read-only deployment readiness
scripts/build_h024_read_only_black_swan_guard_jsonl.py
scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
Observer operational checks
scripts/check_h024_read_only_vps_observer_health.ps1
scripts/check_h024_read_only_vps_observer_task_state.ps1
scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1
scripts/build_h024_read_only_vps_observer_continuity_summary.ps1
scripts/build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1
23. Current Readiness Recovery Commands

To inspect scheduled cadence current blocker:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

$Cadence = Get-Content -Raw reports\h024_read_only_vps_observer_scheduled_cadence_summary.json | ConvertFrom-Json

$Cadence | Select-Object `
  verdict,
  operator_state,
  operator_next_action,
  observed_run_count,
  observed_span_minutes,
  min_observed_gap_minutes,
  max_observed_gap_minutes,
  latest_observed_run_at_utc |
  Format-List

$Cadence.violations | Format-List *

$Cadence.observed_logs |
  Select-Object observed_run_at_utc,file_name |
  Format-Table -AutoSize

To open the dashboard regardless of readiness:

cd C:\Users\equin\Documents\institutional-ea
Start-Process .\reports\demo\h024_local_read_only_demo_dashboard.html

To regenerate dashboard fail-safe:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start_h024_local_read_only_demo_dashboard.ps1 -NoOpen
24. New Authorization: Separate Trading-Enablement Phase

The user explicitly wants to move beyond endless read-only packets.

This handoff authorizes a new, separate trading-enablement phase, but not live trading yet.

Recommended phase name:

H025 controlled demo trading enablement

Alternative if repo naming prefers H024 continuity:

H024-TEN trading enablement design and dry-run quarantine

The next AI may choose a naming convention, but must keep it separate from the H024 read-only observer/demo stack.

24.1 What is now authorized in the new phase

The next phase may implement non-broker-mutating trading enablement scaffolding:

offline request-shape simulation
inert trade intent objects
dry-run order plan JSON
schema-only trade intent validation
risk-limit configuration
max-volume configuration
symbol whitelist configuration
demo-account-only checks
manual operator confirmation artifacts
broker API quarantine module
kill-switch configuration
preflight checklist
unit tests for rejection behavior
unit tests proving no live broker mutation
documentation for staged progression

Allowed language in the new phase:

trade intent
dry-run request shape
simulated order intent
offline order plan
execution quarantine
manual approval
demo-account scope
risk cap
kill switch
24.2 What remains forbidden until later explicit authorization

Do not add live broker mutation yet.

Still forbidden for now:

actual mt5.order_send(...)
actual mt5.order_check(...)
actual mt5.symbol_select(...)
live broker request submission
automatic live entries
automatic live close/modify
SL/TP live modification
unattended order-capable trading loop
any code that can mutate broker/account/symbol state
24.3 Request-shape nuance

Previous handoffs prohibited all request construction because H024 was strictly read-only.

HANDOFF_118 relaxes that only for the new separate phase and only as inert/offline simulation.

Allowed in new phase:

plain JSON objects for dry-run review
schema-only simulated order plans
objects that cannot be submitted to MT5
objects intentionally quarantined away from MetaTrader5 API calls

Not allowed yet:

passing a request to mt5.order_send
passing a request to mt5.order_check
calling mt5.symbol_select
any live broker mutation

The next AI must preserve this distinction.

25. Recommended Next Sequence

Do these in order:

Step 1 - Fix H024 stale exact-ticket scheduler bug

Patch:

scripts/run_h024_read_only_vps_observer_once.ps1

So exact-ticket read-only evidence refreshes before black-swan guard.

Add focused tests.

Run wrapper/task-state/dashboard.

Commit and push source/test/docs only.

Step 2 - Restore clean dashboard readiness

If continuity/cadence still fail due old failed logs, let natural scheduled runs rebuild clean evidence.

Do not delete logs.

Do not bypass.

Step 3 - Start separate dry-run trading-enablement phase

After read-only local demo readiness is clean again, start:

H025 controlled demo trading enablement

First milestone should be:

offline trade intent schema and broker API quarantine

No live order_send.

No live order_check.

No symbol_select.

26. Suggested Next Prompt For The Next AI

Use this prompt:

Please continue from HANDOFF_118 on main. HANDOFF_118 supersedes HANDOFF_117 and all older handoffs. It is the current source of truth.

Current completed commits: 3261878 added the H024 free local read-only demo readiness packet, and 047fcf7 added the H024 local read-only demo dashboard. reports/ remains untracked and must remain untracked.

Current issue: local dashboard works as a fail-safe operator console, but readiness is still not clean. The stale exact-ticket evidence incident caused black-swan guard failures, wrapper exit_code 1, Task Scheduler LastTaskResult 1, continuity pollution, and then scheduled cadence summary failure. Task-state recovered after running the observer through Windows Task Scheduler. Continuity recovered naturally after enough successful scheduled runs. The remaining blocker is scheduled cadence summary; inspect reports/h024_read_only_vps_observer_scheduled_cadence_summary.json for exact violations.

First source fix: patch scripts/run_h024_read_only_vps_observer_once.ps1 so it refreshes exact-ticket read-only evidence before black-swan guard. Keep H024 strictly read-only: no order_check, no order_send, no symbol_select, no broker mutation, no live broker request construction, no entries, no close/modify. Add focused tests proving exact-ticket evidence refresh happens before black-swan guard and proving no order-capable calls exist. Run focused tests, run wrapper, run task-state, run dashboard, inspect scheduled cadence if needed, commit and push source/test/docs only, keep reports/ untracked.

After the H024 read-only scheduler loop is fixed and local dashboard readiness is clean again, start the new separate dry-run trading-enablement phase authorized by HANDOFF_118. Do not silently weaken H024. The new phase may implement inert/offline trade intent schemas, dry-run request-shape simulation, broker API quarantine, manual approval artifacts, demo-account-only checks, symbol/volume limits, and kill switches. Still do not add actual mt5.order_send, mt5.order_check, mt5.symbol_select, live broker mutation, automatic live entries, live close/modify, or an unattended order-capable trading loop until later explicit authorization.
27. Final Safety Reminder

H024 remains read-only.

The new trading-enablement phase is only dry-run and quarantined at first.

No trading is authorized yet.

No broker mutation is authorized yet.

No order-capable loop is authorized yet.

The user wants progress, not more abstract governance. Fix the stale evidence scheduler bug, restore clean dashboard readiness, then move to practical dry-run trading enablement.