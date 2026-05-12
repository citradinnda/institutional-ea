# HANDOFF_116 — Fully Self-Contained H024 Local Windows Read-Only Observer Cadence, No-Console Launcher, And Operational Continuity Handoff

This handoff supersedes HANDOFF_115, HANDOFF_114, HANDOFF_113, HANDOFF_112, HANDOFF_111, HANDOFF_110, and all older handoffs.

This is the source of truth for the next AI.

It is intentionally redundant. The next AI should not need to infer missing context from older handoffs, hidden chain-of-thought, chat history, or generated `reports/`.

---

## 1. Executive Summary

The project is H024 inside the `institutional-ea` repository.

The current phase is:

**free local Windows recurring read-only observer proof**

It is not Oracle VPS and not paid VPS.

The user does not currently have Oracle VPS. Nothing has been proven on Oracle VPS. Do not assume an Oracle account exists.

The deployment target remains the user's existing local Windows machine using:

* Windows Task Scheduler
* local PowerShell
* local MT5
* local Python virtual environment
* local Git repository
* local generated `reports/` runtime/evidence files

Current strategic direction:

1. Prove repeated local Windows read-only observer operation for free.
2. Keep every broker mutation and trading path blocked.
3. Avoid paid VPS until local recurring observer evidence is stable and useful.
4. Consider Oracle Always Free later only if it remains free and compatible.
5. Do not drift into abstract governance-only work.
6. Do not convert this into an order-capable EA.

The latest operational work completed before this handoff:

* A scheduled cadence summary builder was added.
* The scheduled cadence summary builder initially had a BOM-output bug and was fixed.
* The builder then incorrectly judged all historical logs, including old manual clustered runs and old gaps.
* That was fixed so it scores the latest contiguous cadence-compatible segment.
* A no-console VBS launcher was introduced to suppress the visible PowerShell popup from Windows Task Scheduler.
* The task action was switched to `wscript.exe` with a raw VBS launcher path argument.
* Healthcheck reached PASS after upstream black-swan/deployment readiness evidence was refreshed.
* Task-state reached PASS with the no-console launcher task action.
* The interval remains 5 minutes.
* `reports/` remains untracked and must stay untracked.

Important usability context:

The user complained that the 5-minute observer popup interrupted work. The first attempt used:

```text
powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "<wrapper>"

That still flashed briefly.

The current preferred launch shape is:

Execute: wscript.exe
Arguments: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs

This avoids a visible PowerShell console while preserving the wrapper exit code and read-only fail-closed behavior.

2. Absolute Safety Boundary

The project remains read-only.

Do not enable trading.

Do not add any of the following:

order_check
order_send
live broker request construction
executable trade request construction
MT5 trade request dictionaries
automatic entries
automatic close/modify
manual-approval code that actually closes/modifies
SL/TP modification
broker mutation
symbol_select
order-capable trading loops
code paths that close the canary
code paths that modify the canary
code paths that scale the canary
code paths that place XAUUSD orders
code paths that place USDJPY orders

Do not treat PASS as trading authorization.

Interpretation rule:

PASS = evidence/check/packet is coherent for read-only observation only.
PASS != authorization to trade.
PASS != authorization to close.
PASS != authorization to modify.
PASS != authorization to call order_check.
PASS != authorization to call order_send.
PASS != authorization to construct broker requests.
PASS != authorization to run an order-capable loop.

Allowed work:

read-only MT5/account/symbol/position introspection
JSON/JSONL packet generation
verifiers
read-only local runner scripts
read-only scheduler scripts
read-only healthcheck scripts
read-only task-state audit scripts
read-only recovery drill preview scripts
read-only evidence bundle scripts
read-only continuity summary scripts
read-only scheduled cadence summary scripts
local JSON/text/console alerts
log capture and rotation
local evidence aggregation
local operator runbooks
focused tests
fail-closed behavior

Forbidden action remains forbidden even after every observer evidence packet is PASS.

3. User Direction And Free-First Constraint

The user explicitly clarified that the current target is not Oracle VPS and not paid VPS.

Correct interpretation:

No Oracle VPS currently exists for the user.
No Oracle VPS has been used.
Do not tell the user to buy Windows VPS.
Do not assume any VPS credential, SSH target, or Oracle tenancy exists.
Do not build Linux/Oracle deployment tooling unless the user explicitly requests it later.
Current work is local Windows only.
Paths such as C:\Users\equin\Documents\institutional-ea prove local Windows execution.

Current free-first architecture:

Local Windows PC
+ MT5 already installed/logged in
+ Python venv
+ Git repo
+ PowerShell
+ Windows Task Scheduler
+ local reports/
= free recurring read-only observer proof

Possible future cloud path:

Oracle Always Free may be explored later.
Current scripts are Windows Task Scheduler + PowerShell + local MT5 oriented.
A Linux Oracle Always Free VM would likely require a separate Linux-compatible observer path.
Do not rewrite for Linux now.
Do not move to paid VPS unless user explicitly changes direction.
4. Repository State

Project path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Remote:

origin/main

Important generated evidence directory:

reports/

reports/ is generated runtime evidence and must remain untracked.

Known recent commit history before this handoff sequence:

5814450 Fix H024 scheduled cadence latest segment proof
3b26baf Fix H024 read-only observer scheduled cadence summary
e385819 Add H024 read-only observer scheduled cadence summary
bc62c83 Add H024 read-only observer continuity tests and runbook
a7a377b Add H024 read-only observer continuity summary
beafd0f Fix H024 read-only observer timestamp aliases
51cf544 Expand handoff document #114
5a1c4cf Add H024 read-only VPS observer evidence bundle
6364053 Add handoff document #113
4b99dc7 Add H024 read-only VPS task state recovery audit

Important note about this handoff command:

Before writing this handoff, there may have been a lingering modified file:

tests/test_h024_read_only_vps_observer_hidden_launcher.py

This command commits any pending no-console launcher source/test/docs delta first with message:

Fix H024 read-only observer no-console launcher validation

Then it writes and commits this handoff with message:

Add handoff document #116

If that pre-handoff no-console commit is created, its exact hash is generated locally and should appear immediately before the HANDOFF_116 commit in git log.

Expected final git status after this command:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
5. Commit Timeline And What Each Commit Means
5.1 4b99dc7 Add H024 read-only VPS task state recovery audit

Completed task-state/recovery/alert surface milestone.

Despite VPS naming, current usage is local Windows.

Key capabilities:

task-state audit
recovery drill preview
local operator alert surface
no trading authorization
5.2 5a1c4cf Add H024 read-only VPS observer evidence bundle

Added observer evidence bundle.

Known after this: evidence bundle initially depended on timestamp expectations that later needed alias handling.

5.3 51cf544 Expand handoff document #114

Expanded prior handoff.

5.4 beafd0f Fix H024 read-only observer timestamp aliases

Fixed the narrow HANDOFF_114 blocker.

Problem:

healthcheck packet used checked_at_utc
recovery drill and evidence bundle expected generated_at_utc
result was fail-closed timestamp violations

Fix:

accepted checked_at_utc as a valid timestamp alias in recovery drill and evidence bundle paths
preserved freshness checks
did not bypass PASS requirements
did not enable trading

Focused validation:

tests/test_h024_read_only_vps_task_state_recovery.py ...........
tests/test_h024_read_only_vps_observer_evidence_bundle.py .....
16 passed
5.5 a7a377b Add H024 read-only observer continuity summary

Added continuity summary builder:

scripts/build_h024_read_only_vps_observer_continuity_summary.ps1

Purpose:

consume scheduled wrapper summary/logs and observer packets
prove multi-run read-only observer continuity
emit JSON/text under reports/
authorize no trading

Initial issue:

this commit only added the builder script
tests/runbook were accidentally left out
5.6 bc62c83 Add H024 read-only observer continuity tests and runbook

Fix-forward for a7a377b.

Added:

docs/operations/H024_READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_RUNBOOK.md
tests/test_h024_read_only_vps_observer_continuity_summary.py

Validation:

tests/test_h024_read_only_vps_observer_continuity_summary.py .... [100%]
4 passed
5.7 e385819 Add H024 read-only observer scheduled cadence summary

Added initial scheduled cadence summary builder:

scripts/build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1

Issue:

committed too early
focused tests failed 6/6
generated JSON used UTF-8 BOM, but Python test read with utf-8
tests and runbook were not committed in this commit

This is a known bad/intermediate commit. It was fixed forward, not rewritten.

5.8 3b26baf Fix H024 read-only observer scheduled cadence summary

Fixed:

PowerShell JSON/text output writing without UTF-8 BOM
added scheduled cadence tests
added scheduled cadence runbook

Files:

scripts/build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1
tests/test_h024_read_only_vps_observer_scheduled_cadence_summary.py
docs/operations/H024_READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_RUNBOOK.md

Validation:

focused scheduled cadence tests: 6 passed
broader observer tests: 26 passed
5.9 5814450 Fix H024 scheduled cadence latest segment proof

Fixed:

builder incorrectly scored all historical logs
old manual runs and historical gaps caused false FAIL_CLOSED

Observed false-fail stats before fix:

Observed run count: 27
First observed run UTC: 2026-05-12T11:25:49.4530000Z
Latest observed run UTC: 2026-05-12T14:09:51.0990000Z
Observed span minutes: 164.027
Min observed gap minutes: 0.119
Max observed gap minutes: 46.885
Violations:
* scheduled_log_gap_too_large
* scheduled_log_clustered

Correct behavior after fix:

score latest contiguous cadence-compatible segment
ignore older manual cluster/gap noise outside the current proof segment
still require current segment to satisfy freshness, minimum count, minimum span, and gap constraints

Validation:

focused scheduled cadence tests: 7 passed
broader read-only observer tests: 27 passed
5.10 Potential pre-HANDOFF_116 no-console launcher validation commit

This handoff command may create:

Fix H024 read-only observer no-console launcher validation

This commit, if created, should include only source/test/docs for:

scripts/run_h024_read_only_vps_observer_scheduled_hidden.vbs
docs/operations/H024_READ_ONLY_VPS_OBSERVER_NO_CONSOLE_LAUNCHER_RUNBOOK.md
tests/test_h024_read_only_vps_observer_hidden_launcher.py

Do not include reports/.

6. Current Known Canary

There is exactly one known H024 demo canary.

Identity:

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
Older open price: 4728.4490000000005
Older stop loss: 4817.394

Recent observed state:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
H024 position symbol: XAUUSDm
ticket: 4413054432
identifier: 4413054432
magic: 240024
volume: 0.01
type: 1
verdict: PASS

Recent account/risk examples observed during local read-only evidence refresh:

Account server: Exness-MT5Trial6
Account currency: USD
Balance: 10000.0
Equity: approximately 10041-10042 during recent runs
Profit: approximately 41-42 during recent runs
Margin: 2.36
Free margin: approximately 10039-10040
Margin level: approximately 425k
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0

The user said the MT5 trade is still open.

This is expected.

The code path must not close it.

If the user personally wants to close it, the safe path is manual close in MT5 outside this project code. The project remains observer-only.

7. Existing Read-Only Runtime Stack

This section summarizes the existing stack so the next AI does not need older handoffs.

7.1 Runtime Safety Lockout Reader

Purpose:

reads committed default safety config and local lockout state
supports global no-new-entry, manual override lockout, and per-symbol XAUUSD/USDJPY no-new-entry lockouts
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Lockout inputs valid: True
Lockout triggered: False
Active lockouts: 0
Fail-closed lockouts: 0
Effective new entries blocked: True
Broker mutation authorized: False
Order check authorized: False
Order send authorized: False
Entry authorized: False
Close/modify authorized: False
XAUUSD order authorized: False
USDJPY order authorized: False
Trading loop authorized: False
Automatic execution authorized: False
7.2 Runtime Safety Heartbeat

Purpose:

read-only MT5 runtime heartbeat
verifies MT5 initialization, account availability, expected server, USD account currency, terminal connected state
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED
MT5 initialized: True
Account server: Exness-MT5Trial6
Account currency: USD
Terminal connected: True
7.3 Tick/Spread Supervisor

Purpose:

read-only tick/spread supervisor for XAUUSDm and USDJPYm
must not call symbol_select
authorizes no trading

Recent symbol examples:

USDJPYm: PASS, bid around 157.60, ask around 157.61, spread about 10 points
XAUUSDm: PASS, bid around 4685-4686, ask around 4685-4686, spread around 280-308 points
Symbol select authorized: False
7.4 Exposure/Inventory Supervisor

Purpose:

read-only position/order inventory supervisor
allows no H024 inventory or the exact known XAUUSDm canary only
rejects H024 USDJPY position/order, extra H024 position, pending/open H024 orders, mismatched XAUUSDm identity
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
7.5 Account Risk/Margin Supervisor

Purpose:

read-only account risk/margin supervisor
verifies server, USD account context, balance/equity/margin/free margin/margin level sanity, canary boundedness
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED
Account server: Exness-MT5Trial6
Account currency: USD
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
7.6 Runtime Safety Aggregate

Purpose:

aggregates heartbeat, tick/spread, exposure/inventory, and account risk/margin
prevents cherry-picking a passing packet while ignoring failures
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
7.7 Unified Read-Only Runtime Supervision

Purpose:

combines canary supervision and runtime aggregate
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
Canary supervision records: 1
Canary supervision all records passed: True
Runtime aggregate verdict: PASS
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
7.8 Runtime No-Mutation Safety Gate

Purpose:

proves mutation/order-capable paths remain blocked
future broker-facing code must check the gate
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED
Operator next action: KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION
Gate opens mutation path: False
Future broker-facing code must check gate: True
automatic_execution_blocked: True
broker_mutation_blocked: True
close_modify_blocked: True
entry_blocked: True
order_check_blocked: True
order_send_blocked: True
trading_loop_blocked: True
usdjpy_order_blocked: True
xauusd_order_blocked: True
8. Exact-Ticket Close/Modify Stack Context

All exact-ticket close/modify artifacts remain read-only and non-authorizing.

Despite the artifact names, none of these permit closing or modifying the canary.

8.1 Governance

Script:

scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_governance.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW
Gate verdict: PASS
Gate opens mutation path: False
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
H024 position count: 1
H024 order count: 0
Human decision: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
8.2 Decision Artifact

Script:

scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
Decision status: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Requested action: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Exact ticket: 4413054432
Exact identifier: 4413054432
8.3 Pre-Action Evidence Aggregate

Script:

scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars

Report:

reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
User reported position open over three bars: True
8.4 Bar-Age And Exit-Condition Evidence

Script:

scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars

Report:

reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False
8.5 Manual Approval Gate Preview

Script:

scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars

Report:

reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
manual_approval_gate_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False
8.6 Operator Decision V2 Preview

Script:

scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars

Report:

reports/h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
operator_decision_v2_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False
8.7 Execution Readiness Dry-Run Schema Preview

Script:

scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

Report:

reports/h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
execution_readiness_dry_run_schema_preview_constructed: True
execution_readiness_dry_run_schema_preview_authorizes_execution: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
9. Black-Swan Guard And Deployment Readiness
9.1 Black-Swan Guard

Script:

scripts/build_h024_read_only_black_swan_guard_jsonl.py

Report:

reports/h024_read_only_black_swan_guard.jsonl

Purpose:

consumes runtime safety and exact-ticket stack evidence
fails closed on stale/missing/malformed/fail-closed/unsafe evidence
authorizes no trading

Recent passing state:

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

Important operational lesson:

If healthcheck reports:

black_swan:UPSTREAM_NOT_PASS
black_swan:UPSTREAM_VIOLATIONS_PRESENT

Do not suppress or bypass it.

Correct response:

Refresh exact-ticket stack.
Refresh black-swan guard.
Refresh deployment readiness.
Run observer.
Re-run healthcheck.
9.2 Read-Only VPS Deployment Readiness Aggregate

Historical name says VPS, but current target is local Windows.

Script:

scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py

Report:

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Purpose:

verifies read-only observer workflow readiness
authorizes observer review only
authorizes no trading

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED
read_only_observer_workflow_authorized_for_operator_review: True
vps_deployment_readiness_authorizes_trading: False
10. Scheduler, Healthcheck, Recovery, Evidence Bundle, Continuity, And Cadence
10.1 Scheduled Wrapper

Script:

scripts/run_h024_read_only_vps_observer_scheduled.ps1

Purpose:

runs one-shot read-only observer
captures runtime logs
writes last-run summary
rotates logs by retention count and age
exits with observer exit code
authorizes no trading

Default runtime directory:

reports/runtime/h024_read_only_vps_observer

Default logs:

reports/runtime/h024_read_only_vps_observer/logs

Default last-run summary:

reports/runtime/h024_read_only_vps_observer/last_run_summary.json
10.2 Windows Scheduled Task

Task name:

H024 Read Only VPS Observer

Current task action after no-console launcher:

Execute: wscript.exe
Arguments: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs

Current interval:

5 minutes

Do not change interval unless explicitly requested.

If interval changes later:

update task-state expected interval
update cadence max/latest/gap windows
document the reason
do not claim continuity proof under old assumptions
10.3 No-Console Launcher

Launcher:

scripts/run_h024_read_only_vps_observer_scheduled_hidden.vbs

Purpose:

suppress visible PowerShell popup from Windows Task Scheduler
delegate to existing scheduled wrapper
preserve exit code
keep failure fail-closed
no MT5 calls
no trading APIs
no broker mutation

Expected content:

Option Explicit

Dim shell
Dim repoRoot
Dim wrapperPath
Dim command
Dim exitCode

Set shell = CreateObject("WScript.Shell")

repoRoot = "C:\Users\equin\Documents\institutional-ea"
wrapperPath = repoRoot & "\scripts\run_h024_read_only_vps_observer_scheduled.ps1"

shell.CurrentDirectory = repoRoot

command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File " & Chr(34) & wrapperPath & Chr(34)

exitCode = shell.Run(command, 0, True)

WScript.Quit exitCode

Runbook:

docs/operations/H024_READ_ONLY_VPS_OBSERVER_NO_CONSOLE_LAUNCHER_RUNBOOK.md

Test:

tests/test_h024_read_only_vps_observer_hidden_launcher.py

The test had a temporary indentation error during development. It should now validate:

launcher exists
delegates to scheduled wrapper
uses hidden shell.Run(command, 0, True)
preserves exit with WScript.Quit exitCode
contains no trading/broker mutation terms
runbook documents non-authorizing safety boundary
10.4 Healthcheck

Script:

scripts/check_h024_read_only_vps_observer_health.ps1

Report:

reports/h024_read_only_vps_observer_healthcheck.json

Important packet timestamp field:

checked_at_utc

This is accepted after beafd0f.

Recent failure and recovery:

Healthcheck failed when the latest observer run had exit code 1 due to upstream black-swan evidence not PASS.
After refreshing upstream read-only evidence and running the observer again, healthcheck PASS was observed.

Recent PASS:

H024 read-only VPS observer healthcheck verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
10.5 Task-State Audit

Script:

scripts/check_h024_read_only_vps_observer_task_state.ps1

Report:

reports/h024_read_only_vps_observer_task_state.json

Alert outputs:

reports/h024_read_only_vps_observer_operator_alert.json
reports/h024_read_only_vps_observer_operator_alert.txt

Current PASS after raw VBS path fix:

H024 read-only VPS observer task-state verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
task_name: H024 Read Only VPS Observer
source_mode: windows_task_scheduler
task_exists: True
state: Ready
expected_interval_minutes: 5
last_run_time_utc: 2026-05-12T14:34:49.0000000Z
last_task_result: 0

Important quoting lesson:

This failed:

New-ScheduledTaskAction -Execute "wscript.exe" -Argument ""$LauncherPath""

This worked:

$Action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument $LauncherPath
Set-ScheduledTask -TaskName $TaskName -Action $Action | Out-Null
10.6 Recovery Drill Preview

Script:

scripts/run_h024_read_only_vps_recovery_drill_preview.ps1

Report:

reports/h024_read_only_vps_recovery_drill_preview.json

Purpose:

preview recovery readiness without scheduler mutation
no automatic remediation
no broker mutation
no trading authorization

Known historical blocker:

failed on healthcheck checked_at_utc timestamp alias
fixed in beafd0f

Expected PASS after healthcheck/task-state PASS:

H024 read-only VPS recovery drill preview verdict: PASS
Violations: 0
10.7 Evidence Bundle

Script:

scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1

Outputs:

reports/h024_read_only_vps_observer_evidence_bundle.json
reports/h024_read_only_vps_observer_evidence_bundle.txt

Known historical blocker:

did not accept healthcheck checked_at_utc
fixed in beafd0f

Expected PASS after upstream packets fresh:

H024 read-only VPS observer evidence bundle verdict: PASS
Violations: 0
10.8 Continuity Summary

Script:

scripts/build_h024_read_only_vps_observer_continuity_summary.ps1

Outputs:

reports/h024_read_only_vps_observer_continuity_summary.json
reports/h024_read_only_vps_observer_continuity_summary.txt

Purpose:

consumes existing wrapper summary/logs and existing observer packets
proves multi-run read-only observer continuity
fails closed on missing/stale/non-PASS evidence
fails closed on unsafe true flags
authorizes no trading

Tests:

tests/test_h024_read_only_vps_observer_continuity_summary.py

Runbook:

docs/operations/H024_READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_RUNBOOK.md

Typical command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60
10.9 Scheduled Cadence Summary

Script:

scripts/build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1

Outputs:

reports/h024_read_only_vps_observer_scheduled_cadence_summary.json
reports/h024_read_only_vps_observer_scheduled_cadence_summary.txt

Tests:

tests/test_h024_read_only_vps_observer_scheduled_cadence_summary.py

Runbook:

docs/operations/H024_READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_RUNBOOK.md

Purpose:

prove actual Windows Task Scheduler cadence-compatible runs
detect too few logs
detect stale latest run
detect clustered manual runs
detect gaps too large
consume upstream health/task/recovery/bundle/continuity packets
emit JSON/text under reports/
authorize no trading

Key behavior after 5814450:

score latest contiguous cadence-compatible log segment
not all historical logs

Typical command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1 `
  -Root "C:\Users\equin\Documents\institutional-ea" `
  -ExpectedIntervalMinutes 5 `
  -MinRunCount 4 `
  -MinCadenceWindowMinutes 15 `
  -MaxLatestRunAgeMinutes 30 `
  -MaxPacketAgeMinutes 60 `
  -MaxAllowedGapMinutes 10 `
  -MinInterRunGapMinutes 3
11. Current Validation Outputs To Preserve

Known source/test validation:

After 3b26baf:
focused scheduled cadence tests: 6 passed
broader observer tests: 26 passed

After 5814450:
focused scheduled cadence tests: 7 passed
broader read-only observer tests: 27 passed

Known live operational validation from recent run:

black-swan guard: PASS, 0 violations
deployment readiness aggregate: PASS, 0 violations
healthcheck: PASS, 0 violations
task-state: PASS, 0 violations after using wscript.exe raw VBS path

Known non-authorizing safety flags from recent evidence:

Effective new entries blocked: True
Broker mutation authorized: False
Order check authorized: False
Order send authorized: False
Entry authorized: False
Close/modify authorized: False
XAUUSD order authorized: False
USDJPY order authorized: False
Trading loop authorized: False
Automatic execution authorized: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
symbol_select_authorized: False
black_swan_guard_authorizes_trading: False
vps_deployment_readiness_authorizes_trading: False
12. Exact Commands For Next AI To Start Safely

Start:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -12

Verify no-console launcher task action:

(Get-ScheduledTask -TaskName "H024 Read Only VPS Observer").Actions | Format-List *

Expected:

Execute: wscript.exe
Arguments: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs

Validate source/tests:

python -m pytest tests\test_h024_read_only_vps_observer_hidden_launcher.py

python -m pytest `
  tests\test_h024_read_only_vps_scheduler_healthcheck.py `
  tests\test_h024_read_only_vps_task_state_recovery.py `
  tests\test_h024_read_only_vps_observer_evidence_bundle.py `
  tests\test_h024_read_only_vps_observer_continuity_summary.py `
  tests\test_h024_read_only_vps_observer_scheduled_cadence_summary.py `
  tests\test_h024_read_only_vps_observer_hidden_launcher.py

Refresh upstream read-only evidence if needed:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_read_only_black_swan_guard_jsonl.py
python scripts\build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py

Refresh observer packets:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 30
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1 `
  -Root "C:\Users\equin\Documents\institutional-ea" `
  -ExpectedIntervalMinutes 5 `
  -MinRunCount 4 `
  -MinCadenceWindowMinutes 15 `
  -MaxLatestRunAgeMinutes 30 `
  -MaxPacketAgeMinutes 60 `
  -MaxAllowedGapMinutes 10 `
  -MinInterRunGapMinutes 3

Expected:

healthcheck PASS
task-state PASS
recovery drill preview PASS
evidence bundle PASS
continuity summary PASS
scheduled cadence summary PASS
violations 0

If any packet fails closed, inspect violations. Do not bypass safety failures.

13. Known Pitfalls And Fixes
13.1 PowerShell BOM issue

Symptom:

json.decoder.JSONDecodeError: Unexpected UTF-8 BOM

Cause:

PowerShell wrote JSON with UTF-8 BOM.

Fix:

Use .NET System.Text.UTF8Encoding($false) writer in the builder.

Resolved in:

3b26baf
13.2 Historical logs polluting cadence proof

Symptom:

scheduled_log_gap_too_large
scheduled_log_clustered

Cause:

Builder scored all historical logs including old manual clustered runs and old gaps.

Fix:

Score latest contiguous cadence-compatible segment.

Resolved in:

5814450
13.3 Healthcheck black-swan upstream failure

Symptom:

black_swan:UPSTREAM_NOT_PASS
black_swan:UPSTREAM_VIOLATIONS_PRESENT
last_run:LAST_RUN_NOT_COMPLETED
last_run:LAST_RUN_EXIT_NONZERO

Cause:

Observer wrapper failed because upstream black-swan/deployment evidence was stale or not PASS.

Correct fix:

Refresh upstream exact-ticket stack, black-swan guard, deployment readiness, then rerun observer.

Do not suppress healthcheck.

13.4 -WindowStyle Hidden still flashes

Symptom:

Visible PowerShell console briefly appears every 5 minutes.

Correct fix:

Use VBS no-console launcher via wscript.exe.

13.5 Fragile New-ScheduledTaskAction -Argument quoting

Bad:

-Argument ""$LauncherPath""

Can produce empty argument or parser errors.

Good:

$Action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument $LauncherPath
Set-ScheduledTask -TaskName $TaskName -Action $Action | Out-Null
13.6 Hidden launcher test indentation error

Symptom:

IndentationError: expected an indented block after function definition

Cause:

Generated test file was malformed.

Fix:

Overwrite tests/test_h024_read_only_vps_observer_hidden_launcher.py with correctly indented tests.

14. Commit Discipline

Use this pattern:

git status
python -m pytest <focused tests>
git add -- <source/test/docs only>
git diff --cached --check
git diff --cached --stat
git commit -m "<specific milestone message>"
git push
git status

Rules:

Never add reports/.
Never commit generated runtime evidence.
Do not claim success without final git status.
Fix forward rather than rewriting pushed history.
Keep milestones operational and read-only.
Avoid governance-only work unless explicitly requested.
Avoid paid infrastructure unless explicitly requested.
Keep giving the user concise suggested next prompts after each milestone.
15. Recommended Next Read-Only Operational Milestone

Recommended next milestone:

H024 local Windows no-console scheduled observer natural-run proof

Purpose:

Confirm the wscript.exe no-console launcher eliminates the popup during natural scheduled runs.
Let Windows Task Scheduler run naturally for at least 15-20 minutes.
Refresh healthcheck, task-state, recovery drill preview, evidence bundle, continuity summary, and scheduled cadence summary.
Confirm PASS from real natural no-console scheduler runs.
Keep interval at 5 minutes unless the user explicitly asks to change it.
Do not commit reports/.

If the user still sees a popup, inspect the source before changing interval:

scheduled task action
wrapper script subprocesses
powershell.exe child processes
Python subprocesses
MT5 focus behavior
Windows notification/UAC/antivirus behavior

Do not trade.

Do not add broker mutation.

Do not add order-capable code.

16. Suggested Prompt For Next AI

Use this prompt next:

Please read docs/operations/handoffs/HANDOFF_116.md carefully and follow it exactly. It supersedes HANDOFF_115 and all older handoffs.

Continue from commit 5814450 or later on main. The current target is free local Windows recurring read-only observer proof, not Oracle VPS and not paid VPS. The user does not currently have Oracle VPS.

Hard safety boundaries remain absolute: do not enable trading; do not add order_check, order_send, live broker request construction, executable trade request construction, automatic entries, automatic close/modify, SL/TP modification, symbol_select, broker mutation, or order-capable trading loops.

Current operational context: the scheduled cadence builder is fixed to score the latest contiguous cadence-compatible segment. Focused cadence tests passed 7/7 and broader observer tests passed 27/27 at commit 5814450. A no-console VBS launcher was introduced so Windows Task Scheduler can run the observer through wscript.exe instead of flashing a PowerShell window. The scheduled task action should be Execute=wscript.exe and Arguments=C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs. The 5-minute interval remains unchanged. Use the raw VBS path as the scheduled-task argument; do not use fragile nested quote escaping.

Latest observed operational state: after refreshing upstream exact-ticket, black-swan, and deployment readiness evidence, healthcheck PASS and task-state PASS were observed. Task-state passed with violations 0, last_task_result 0, state Ready, expected interval 5, and the wscript.exe/VBS action. reports/ must remain untracked.

Next milestone: let the no-console scheduled task run naturally for at least 15-20 minutes, then refresh healthcheck, task-state, recovery drill preview, evidence bundle, continuity summary, and scheduled cadence summary. Verify PASS from real natural no-console scheduler runs. Do not commit reports/. If all PASS, summarize the operational state and give me the next concise read-only milestone prompt.
17. Final Safety Reminder

The next AI must not help convert this into an unrestricted EA.

Do not trade.

Do not close or modify the canary through code.

Do not make the EA open trades.

Do not make the EA close trades.

Do not build live broker requests.

Do not build executable trade request dictionaries.

Do not run an order-capable trading loop.

Do not call order_check.

Do not call order_send.

Do not call symbol_select.

Do not mutate broker/account/symbol state.

The next useful milestone is operational proof quality for local Windows read-only scheduled observation only.
