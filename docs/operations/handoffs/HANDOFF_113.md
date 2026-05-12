# HANDOFF_113 — Fully Self-Contained H024 Read-Only VPS Task-State / Recovery / Alert Surface Handoff

This handoff supersedes HANDOFF_112, HANDOFF_111, HANDOFF_110, HANDOFF_109, and all older handoffs.

This is the source of truth for the next AI.

It captures the completed H024 read-only VPS task-state audit, restart/recovery drill preview, and operator alert surface milestone, including:

- exact repo state
- pushed milestone commit
- files added
- validation outputs
- hard safety boundaries
- current canary identity
- current operational VPS observer state
- existing H024 stack context
- completed scheduler/healthcheck/log-rotation context from HANDOFF_112
- completed task-state checker behavior
- completed recovery drill preview behavior
- completed local operator alert surface behavior
- final git state
- next recommended read-only operational milestone

This handoff is intentionally redundant. The next AI should not need to infer missing context from older handoffs.

---

## 1. Current Project Direction

The user is tired of endless governance-only milestones.

The project direction is now operational read-only VPS observer infrastructure:

1. Preserve the existing safety/governance stack.
2. Stop inventing abstract governance-only layers unless directly needed.
3. Build practical read-only deployment infrastructure.
4. Get the system running repeatedly as a read-only VPS observer.
5. Make it auditable, recoverable, and operator-visible on a VPS.
6. Keep all trading and broker mutation blocked.

Useful work should remain operational:

- scheduled task installation/preview
- scheduled task disable/uninstall
- scheduled wrapper execution
- healthcheck
- task-state audit
- log capture
- log rotation
- stale-run detection
- boot/restart recovery drill
- local operator alert surface
- operator runbooks
- VPS operational hardening

Do not drift back into governance-only work.

---

## 2. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Treat this handoff as the source of truth.
3. Continue from commit `4b99dc7` or later.
4. Preserve every hard safety boundary.
5. Keep all H024 work read-only unless a future human-directed milestone explicitly says otherwise.
6. Never infer that any PASS packet authorizes trading.
7. Never call broker mutation functions.
8. Never call `order_check`.
9. Never call `order_send`.
10. Never create entries.
11. Never close or modify the current XAUUSDm canary.
12. Never place USDJPY orders.
13. Never place XAUUSD orders.
14. Never scale the existing canary.
15. Never run an order-capable trading loop.
16. Never call `symbol_select` from new safety/governance/observer/deployment code.
17. Never build a live broker request.
18. Never build an executable trade request dictionary.
19. Never treat VPS deployment/readiness/scheduler/health/task-state/recovery/alert status as trading authorization.
20. Keep `reports/` untracked.
21. Fail closed on missing, malformed, stale, ambiguous, inconsistent, unsafe, or unverifiable state.
22. Use focused tests and packet/verifier checks during iteration.
23. Do not ask the user to run the full suite after every small patch.
24. Keep the milestone operational, not governance-only.
25. Give concise suggested next prompts after each milestone.

After each milestone, give:

- concise status summary
- commit hash
- validation output
- final git state
- one concise suggested next prompt

---

## 3. Repository State

Project:

```text
institutional-ea

Local repo path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Remote:

origin/main

Latest confirmed pushed milestone commit before this handoff:

4b99dc7 Add H024 read-only VPS task state recovery audit

Recent confirmed push:

To https://github.com/citradinnda/institutional-ea.git
   5fa4306..4b99dc7  main -> main

Final confirmed git status after pushing 4b99dc7:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime/generated output and must remain untracked.

This HANDOFF_113 file should be committed after 4b99dc7 with a separate handoff commit.

4. Hard Safety Boundary

Current H024 state is post-canary, read-only, no-mutation.

Forbidden:

Do not create a second H024 entry.
Do not place a live order.
Do not place a demo order.
Do not place a USDJPY order.
Do not place a XAUUSD order.
Do not scale the existing XAUUSDm canary.
Do not call order_check.
Do not call order_send.
Do not close the XAUUSDm canary.
Do not modify the XAUUSDm canary.
Do not modify SL/TP.
Do not run an order-capable trading loop.
Do not mutate broker/account/symbol state.
Do not call symbol_select from new code.
Do not build a live broker request.
Do not build an executable trade request dictionary.
Do not treat any readiness/scheduler/healthcheck/task-state/recovery/alert packet as trading permission.
Do not add reports/ to git.
Do not add governance-only layers unless directly required for practical VPS operations.
Do not make external alert integrations that mutate external systems unless explicitly requested later.

Allowed:

Read-only MT5/account/symbol/position introspection if already supported by existing code.
JSON/JSONL packet generation.
Verifiers.
Read-only runner scripts.
Read-only scheduler scripts.
Read-only healthcheck scripts.
Read-only task-state audit scripts.
Read-only recovery drill preview scripts.
Local JSON/text/console operator alert surfaces.
Read-only log capture and rotation.
Operator runbooks.
Fail-closed safety checks.

Interpretation:

PASS means the packet/check is coherent.

PASS does not mean:

trading authorized
close/modify authorized
broker mutation authorized
order_check authorized
order_send authorized
executable request authorized
live broker request authorized
symbol_select authorized
automatic execution authorized
5. Current Known Canary

There is exactly one known H024 standard-demo XAUUSDm canary.

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
Open price: 4728.4490000000005
Stop loss: 4817.394

Latest validated state from prior operational checks:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
Exact ticket: 4413054432
Exact identifier: 4413054432

The canary was observed, but this does not authorize close/modify or trading.

The position being open over three bars remains classified as:

OPERATOR_REPORTED_ONLY

This is non-authorizing context only.

6. Existing H024 Stack Summary
6.1 Runtime Safety Lockout Reader

Commit:

98efc2a Add H024 runtime safety lockout reader

Files:

config/h024_runtime_safety/default_lockout_config.json
quantcore/execution/h024_runtime_safety_lockout.py
scripts/build_h024_runtime_safety_lockout_jsonl.py
scripts/verify_h024_runtime_safety_lockout_jsonl.py
tests/test_h024_runtime_safety_lockout.py

Passing state:

LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Purpose:

Reads default safety config and local lockout state. Supports global no-new-entry, manual override lockout, and per-symbol XAUUSD/USDJPY no-new-entry lockouts.

Non-authorizing.

6.2 Runtime Safety Heartbeat

Commit:

187e9dd Add H024 runtime safety heartbeat packet

Script:

scripts/build_h024_runtime_safety_heartbeat_jsonl.py

Report:

reports/h024_runtime_safety_heartbeat.jsonl

Passing state:

RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED

Purpose:

Read-only MT5 runtime heartbeat. Verifies initialization, account availability, expected server, USD account currency, terminal/account heartbeat freshness where available.

Expected:

Server: Exness-MT5Trial6
Currency: USD

Non-authorizing.

6.3 Runtime Tick/Spread Safety Supervisor

Commit:

abecff8 Add H024 runtime tick and spread safety supervisor

Script:

scripts/build_h024_runtime_tick_spread_safety_supervisor_jsonl.py

Report:

reports/h024_runtime_tick_spread_safety_supervisor.jsonl

Passing state:

TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED

Purpose:

Read-only tick/spread checks for XAUUSDm and USDJPYm.

Important:

Do not call symbol_select.

Non-authorizing.

6.4 Runtime Exposure/Inventory Safety Supervisor

Commit:

0db61fa Add H024 runtime exposure inventory safety supervisor

Script:

scripts/build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py

Report:

reports/h024_runtime_exposure_inventory_safety_supervisor.jsonl

Passing state:

EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED

Purpose:

Read-only inventory supervisor. Allows no H024 inventory or the exact known XAUUSDm canary. Rejects H024 USDJPY position/order, extra H024 position, pending/open H024 orders, mismatched XAUUSDm canary identity.

Allowed canary fields:

symbol: XAUUSDm
ticket/identifier: 4413054432
magic: 240024
volume: 0.01
type: 1

Non-authorizing.

6.5 Runtime Account Risk/Margin Safety Supervisor

Commit:

1c331c6 Add H024 runtime account risk margin safety supervisor

Script:

scripts/build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py

Report:

reports/h024_runtime_account_risk_margin_safety_supervisor.jsonl

Passing state:

ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED

Purpose:

Read-only account risk/margin supervisor. Verifies server, USD account context, balance/equity/margin/free margin/margin level sanity, floating PnL consistency where available, canary boundedness.

Important field-shape lesson:

Downstream consumers should support both:

margin_free
free_margin

Non-authorizing.

6.6 Runtime Safety Aggregate Supervisor

Commit:

8e8979c Add H024 runtime safety aggregate supervisor

Script:

scripts/build_h024_runtime_safety_aggregate_supervisor_jsonl.py

Report:

reports/h024_runtime_safety_aggregate_supervisor.jsonl

Passing state:

RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED

Purpose:

Aggregates runtime heartbeat, tick/spread, exposure/inventory, account risk/margin, and related runtime safety evidence.

Prevents cherry-picking one passing packet while ignoring failures.

Non-authorizing.

6.7 Unified Read-Only Post-Canary Runtime Supervision

Commit:

224371a Add H024 unified read-only runtime supervision

Actual script used by runner:

scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py

Actual report path:

reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl

Passing state:

UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED

Purpose:

Combines one-shot canary supervisory state and runtime safety aggregate.

Non-authorizing.

Important naming lesson:

The actual builder/report names include:

unified_read_only_post_canary_runtime_supervision

Do not assume older candidate names are correct.

6.8 Runtime No-Mutation Safety Gate

Commit:

5249ad1 Add H024 runtime no-mutation safety gate

Script:

scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py

Report:

reports/h024_runtime_no_mutation_safety_gate.jsonl

Passing state:

NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED

Purpose:

Future broker-facing code must check this gate. The current gate proves all broker mutation and order-capable paths remain blocked.

Non-authorizing.

Known frozen legacy exceptions:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

These are historical/pre-gate artifacts only.

7. Exact-Ticket Close/Modify Stack

All exact-ticket close/modify artifacts are read-only and non-authorizing.

7.1 Governance

Current actual script:

scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py

Current actual report:

reports/h024_exact_ticket_canary_close_modify_governance.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED

Purpose:

Defines strict requirements for possible future exact-ticket close/modify consideration.

Does not authorize close/modify.

7.2 Decision Artifact

Current actual script:

scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py

Current actual report:

reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED

Important naming lesson:

The actual report is:

h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

not:

h024_exact_ticket_canary_close_modify_decision_artifact_validator.jsonl

Do not use the wrong filename.

7.3 Pre-Action Evidence Aggregate

Current script:

scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py

Current report:

reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED

Important:

When refreshing for current operator context, use:

--position-open-over-three-bars
7.4 Bar-Age And Exit-Condition Evidence

Current script:

scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py

Current report:

reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED

Current passing classification:

OPERATOR_REPORTED_ONLY

Important:

Must use:

--position-open-over-three-bars

Otherwise it can fail closed with:

INSUFFICIENT_BAR_AGE_EVIDENCE

This is expected fail-closed behavior.

7.5 Manual Approval Gate Preview

Current script:

scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py

Current report:

reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED

Important:

Use:

--position-open-over-three-bars

This builder can internally refresh bar-age evidence. Without the flag, it can overwrite a previously PASS bar-age report with a fail-closed insufficient-evidence packet.

7.6 Operator Decision V2 Preview

Current script:

scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py

Current report:

reports/h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED

Important:

Use:

--position-open-over-three-bars
7.7 Execution Readiness Dry-Run Schema Preview

Current script:

scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py

Current report:

reports/h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED

Important:

Use:

--position-open-over-three-bars

This constructs only a non-executable dry-run schema preview. It constructs no live broker request and authorizes no action.

8. Read-Only Black-Swan Guard

Implementation commit:

f62de7c Add H024 read-only black-swan guard

Fix-forward commit:

67cfc43 Fix H024 black-swan guard validation and timestamp handling

Files:

quantcore/execution/h024_read_only_black_swan_guard.py
scripts/build_h024_read_only_black_swan_guard_jsonl.py
scripts/verify_h024_read_only_black_swan_guard_jsonl.py
tests/test_h024_read_only_black_swan_guard.py
docs/operations/H024_READ_ONLY_BLACK_SWAN_GUARD.md

Report:

reports/h024_read_only_black_swan_guard.jsonl

Passing state:

BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Fail-closed state:

FAIL_CLOSED_BLACK_SWAN_GUARD_ACTIVE_OR_UNVERIFIED_NO_TRADING_AUTHORIZED

Purpose:

Consumes runtime safety and exact-ticket close/modify preview stack, detecting stale/missing/unsafe/extreme conditions while authorizing no action.

Important timestamp lesson:

Timestamp aliases supported:

observed_at_utc
generated_at_utc
created_at_utc
evaluated_at_utc
built_at_utc
timestamp_utc
timestamp

Stale exact-ticket evidence correctly causes fail-closed.

9. VPS Deployment Readiness Aggregate And One-Shot Runner Context

Milestone commit:

0792bad Add H024 read-only VPS deployment readiness aggregate

Files added by that milestone:

docs/operations/H024_READ_ONLY_VPS_DEPLOYMENT_READINESS_AGGREGATE.md
quantcore/execution/h024_read_only_vps_deployment_readiness_aggregate.py
scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
scripts/run_h024_read_only_vps_observer_once.ps1
scripts/verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
tests/test_h024_read_only_vps_deployment_readiness_aggregate.py

Report path:

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Passing readiness state:

READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED

Passing next action:

RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED

Fail-closed readiness state:

FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

The one-shot runner is:

scripts/run_h024_read_only_vps_observer_once.ps1

It refreshes the operational runtime/read-only chain and then verifies:

black-swan guard with --require-pass
VPS readiness aggregate with --require-pass

It does not rerun every exact-ticket builder. It consumes exact-ticket stack reports as upstream evidence. If those reports are stale, missing, malformed, fail-closed, or unsafe, black-swan guard/readiness fail closed.

This design is intentional.

10. Completed HANDOFF_112 Milestone Context

Milestone:

H024 read-only VPS scheduler, healthcheck, and log-rotation path.

Commit:

a61fc95 Add H024 read-only VPS observer scheduler healthcheck

Files added:

docs/operations/H024_READ_ONLY_VPS_SCHEDULER_HEALTHCHECK_RUNBOOK.md
scripts/check_h024_read_only_vps_observer_health.ps1
scripts/install_h024_read_only_vps_observer_task.ps1
scripts/run_h024_read_only_vps_observer_scheduled.ps1
scripts/uninstall_h024_read_only_vps_observer_task.ps1
tests/test_h024_read_only_vps_scheduler_healthcheck.py

Purpose:

Turn the one-shot observer runner into practical VPS operations without enabling trading.

That milestone added:

scheduled wrapper around the existing one-shot observer
Windows Task Scheduler install/preview script
Windows Task Scheduler uninstall/preview script
healthcheck script
last-run summary
log capture
log retention and rotation
stale readiness/black-swan/heartbeat/no-mutation checks
runbook for boot/restart/recovery
focused tests for operational behavior and static no-mutation expectations

This is operational infrastructure, not a new governance-only layer.

10.1 Scheduled Wrapper

Script:

scripts/run_h024_read_only_vps_observer_scheduled.ps1

Purpose:

Runs the existing one-shot observer and captures runtime logs.

Default log directory:

reports/runtime/h024_read_only_vps_observer/logs

Default last-run summary:

reports/runtime/h024_read_only_vps_observer/last_run_summary.json

Default retention:

RetentionCount = 288
RetentionDays = 14

Behavior:

creates runtime state/log directories under reports/runtime/h024_read_only_vps_observer
runs the one-shot read-only observer
captures output to timestamped .log
writes last_run_summary.json
rotates logs by count and age
exits with the observer exit code
does not authorize trading or broker mutation

Important fix:

Machine-readable JSON is written as UTF-8 without BOM using:

[System.IO.File]::WriteAllText(..., New-Object System.Text.UTF8Encoding -ArgumentList $false)

This avoids Python JSON parse failures on Windows PowerShell 5.1.

10.2 Install / Preview Scheduled Task

Script:

scripts/install_h024_read_only_vps_observer_task.ps1

Default task name:

H024 Read Only VPS Observer

Default interval:

5 minutes

Preview mode:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview

Preview does not register a scheduled task.

Install command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -IntervalMinutes 5 -Force

Behavior:

registers a Windows Scheduled Task
uses powershell.exe
calls the scheduled wrapper script
sets repetition interval
uses MultipleInstances IgnoreNew
uses a finite execution time limit
explicitly remains read-only observer infrastructure

It does not call MT5 mutation APIs.

10.3 Uninstall / Preview Scheduled Task

Script:

scripts/uninstall_h024_read_only_vps_observer_task.ps1

Preview mode:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1 -Preview

Uninstall command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1

Behavior:

removes the scheduled task if present
preview mode shows the action without unregistering anything
does not touch trading or broker state
10.4 Healthcheck

Script:

scripts/check_h024_read_only_vps_observer_health.ps1

Default health output:

reports/h024_read_only_vps_observer_healthcheck.json

Default runtime state directory:

reports/runtime/h024_read_only_vps_observer

Reads:

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl
reports/h024_read_only_black_swan_guard.jsonl
reports/h024_runtime_safety_heartbeat.jsonl
reports/h024_runtime_no_mutation_safety_gate.jsonl
reports/runtime/h024_read_only_vps_observer/last_run_summary.json
scheduled wrapper log path from the summary

Passing health state:

READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed health state:

FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_HEALTHCHECK_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Important:

Healthcheck PASS means the observer operational path is healthy for read-only observation only.

Healthcheck PASS does not authorize trading.

11. Completed HANDOFF_113 Milestone

Milestone:

H024 read-only VPS task-state audit, restart/recovery drill preview, and operator alert surface.

Commit:

4b99dc7 Add H024 read-only VPS task state recovery audit

Pushed:

To https://github.com/citradinnda/institutional-ea.git
   5fa4306..4b99dc7  main -> main

Files added:

docs/operations/H024_READ_ONLY_VPS_TASK_STATE_AND_RECOVERY_RUNBOOK.md
scripts/check_h024_read_only_vps_observer_task_state.ps1
scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
tests/test_h024_read_only_vps_task_state_recovery.py

Commit stats:

[main 4b99dc7] Add H024 read-only VPS task state recovery audit
 4 files changed, 1248 insertions(+)
 create mode 100644 docs/operations/H024_READ_ONLY_VPS_TASK_STATE_AND_RECOVERY_RUNBOOK.md
 create mode 100644 scripts/check_h024_read_only_vps_observer_task_state.ps1
 create mode 100644 scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
 create mode 100644 tests/test_h024_read_only_vps_task_state_recovery.py

Purpose:

Move from schedulable observer to practical VPS operational resilience without enabling trading.

This milestone added:

read-only Windows Scheduled Task state audit script
task installed/missing detection
enabled/disabled state detection
trigger interval detection
last run time detection
last task result detection
stale scheduler run detection
local JSON/text/console operator alert surface
restart/recovery drill preview script
recovery evidence freshness checks
focused tests with mock Task Scheduler evidence
runbook for task-state audit and recovery drill
static no-mutation expectations for new scripts

This is operational infrastructure, not a governance-only layer.

12. New Script Behavior From HANDOFF_113
12.1 Task-State Audit Script

Script:

scripts/check_h024_read_only_vps_observer_task_state.ps1

Default task name:

H024 Read Only VPS Observer

Default expected interval:

5 minutes

Default max last-run age:

15 minutes

Default output:

reports/h024_read_only_vps_observer_task_state.json

Default local alert JSON:

reports/h024_read_only_vps_observer_operator_alert.json

Default local alert text:

reports/h024_read_only_vps_observer_operator_alert.txt

Core command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15

Behavior:

reads Windows Scheduled Task metadata using read-only scheduled task cmdlets
detects task not installed
detects task disabled
detects missing task state
detects unexpected task state
detects missing trigger
detects disabled trigger
detects repetition interval mismatch
detects missing last task result
detects non-zero last task result
detects malformed last task result
detects missing last run timestamp
detects stale last run timestamp
detects future/malformed last run timestamp
supports a -MockTaskJsonPath for deterministic tests and offline validation
writes machine-readable JSON as UTF-8 without BOM
writes local JSON/text/console operator alerts only
performs no scheduler mutation
performs no broker mutation
authorizes no trading

PASS state:

READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED

FAIL-CLOSED state:

FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_TASK_STATE_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Important interpretation:

Task-state PASS means the scheduled task metadata is coherent for read-only observer operations only.

Task-state PASS does not authorize trading.

12.2 Operator Alert Surface

The task-state checker writes local-only alert artifacts:

reports/h024_read_only_vps_observer_operator_alert.json
reports/h024_read_only_vps_observer_operator_alert.txt

Alert surface behavior:

local JSON output
local text output
console output
no email
no webhook
no external API
no scheduler mutation
no broker mutation
no automatic remediation

Alert PASS state:

TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED

Alert fail-closed state:

OPERATOR_ALERT_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Safety fields preserved:

read_only_observer_only = true
trading_authorized = false
broker_mutation_authorized = false
order_check_authorized = false
order_send_authorized = false
entry_authorized = false
close_modify_authorized = false
xauusd_order_authorized = false
usdjpy_order_authorized = false
trading_loop_authorized = false
automatic_execution_authorized = false
live_broker_request_constructed = false
executable_trade_request_constructed = false
mt5_request_dictionary_constructed = false
symbol_select_authorized = false
task_state_audit_authorizes_trading = false
12.3 Recovery Drill Preview Script

Script:

scripts/run_h024_read_only_vps_recovery_drill_preview.ps1

Default input evidence:

reports/h024_read_only_vps_observer_task_state.json
reports/h024_read_only_vps_observer_healthcheck.json

Default output:

reports/h024_read_only_vps_recovery_drill_preview.json

Default local alert JSON:

reports/h024_read_only_vps_recovery_drill_operator_alert.json

Default local alert text:

reports/h024_read_only_vps_recovery_drill_operator_alert.txt

Core command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60

Behavior:

validates task-state evidence exists
validates task-state evidence parses
requires task-state verdict PASS
validates task-state evidence freshness
validates healthcheck evidence exists
validates healthcheck evidence parses
requires healthcheck verdict PASS
validates healthcheck evidence freshness
validates required recovery scripts exist
writes recovery drill preview packet
writes local JSON/text/console operator alerts
produces operator recovery steps
performs no scheduler mutation
performs no broker mutation
performs no automatic remediation
authorizes no trading

PASS state:

READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED

FAIL-CLOSED state:

FAIL_CLOSED_READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Recovery drill steps are preview-only. They describe operator procedure, not automatic remediation.

12.4 Recovery Drill Alert Surface

The recovery drill preview writes local-only alert artifacts:

reports/h024_read_only_vps_recovery_drill_operator_alert.json
reports/h024_read_only_vps_recovery_drill_operator_alert.txt

Alert surface behavior:

local JSON output
local text output
console output
no email
no webhook
no external API
no scheduler mutation
no broker mutation
no automatic remediation

Alert PASS state:

RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED

Alert fail-closed state:

RECOVERY_DRILL_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Safety fields preserved:

read_only_observer_only = true
trading_authorized = false
broker_mutation_authorized = false
order_check_authorized = false
order_send_authorized = false
entry_authorized = false
close_modify_authorized = false
xauusd_order_authorized = false
usdjpy_order_authorized = false
trading_loop_authorized = false
automatic_execution_authorized = false
live_broker_request_constructed = false
executable_trade_request_constructed = false
mt5_request_dictionary_constructed = false
symbol_select_authorized = false
recovery_drill_authorizes_trading = false
13. Validation Outputs From Completed HANDOFF_113 Milestone
13.1 Focused Tests

Command:

python -m pytest tests\test_h024_read_only_vps_deployment_readiness_aggregate.py tests\test_h024_read_only_vps_scheduler_healthcheck.py tests\test_h024_read_only_vps_task_state_recovery.py

Result:

=========================================================== test session starts ===========================================================
platform win32 -- Python 3.12.10, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\equin\Documents\institutional-ea
configfile: pyproject.toml
plugins: hypothesis-6.152.4, cov-7.1.0
collected 32 items

tests\test_h024_read_only_vps_deployment_readiness_aggregate.py ................                                                     [ 50%]
tests\test_h024_read_only_vps_scheduler_healthcheck.py ......                                                                        [ 68%]
tests\test_h024_read_only_vps_task_state_recovery.py ..........                                                                      [100%]

=========================================================== 32 passed in 12.27s ===========================================================
13.2 Script-Level Mock Task-State Validation

Command used during milestone:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -MockTaskJsonPath reports\runtime\h024_read_only_vps_observer\mock_validation\mock_task_state_input.json -OutputPath reports\h024_read_only_vps_observer_task_state.json -AlertJsonPath reports\h024_read_only_vps_observer_operator_alert.json -AlertTextPath reports\h024_read_only_vps_observer_operator_alert.txt -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 60

Output:

H024 read-only VPS observer task-state verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Task-state packet: reports\h024_read_only_vps_observer_task_state.json
Operator alert JSON: reports\h024_read_only_vps_observer_operator_alert.json
Operator alert text: reports\h024_read_only_vps_observer_operator_alert.txt

Important:

This validation used mock scheduled-task evidence for deterministic script-level validation. It did not prove that the real Windows Scheduled Task is installed or running on the host. The script can audit the real task when run without -MockTaskJsonPath.

13.3 Script-Level Mock Recovery Drill Validation

Command used during milestone:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -TaskStatePacketPath reports\h024_read_only_vps_observer_task_state.json -HealthPacketPath reports\runtime\h024_read_only_vps_observer\mock_validation\mock_healthcheck.json -OutputPath reports\h024_read_only_vps_recovery_drill_preview.json -AlertJsonPath reports\h024_read_only_vps_recovery_drill_operator_alert.json -AlertTextPath reports\h024_read_only_vps_recovery_drill_operator_alert.txt -MaxEvidenceAgeMinutes 60

Output:

H024 read-only VPS recovery drill preview verdict: PASS
Operator state: READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Recovery drill packet: reports\h024_read_only_vps_recovery_drill_preview.json
Operator alert JSON: reports\h024_read_only_vps_recovery_drill_operator_alert.json
Operator alert text: reports\h024_read_only_vps_recovery_drill_operator_alert.txt

Important:

This validation used mock healthcheck evidence for deterministic script-level validation. For actual VPS operation, run the scheduled wrapper and healthcheck first, then run the task-state checker and recovery drill preview against real local evidence.

13.4 Commit And Push Validation

Commit:

[main 4b99dc7] Add H024 read-only VPS task state recovery audit
 4 files changed, 1248 insertions(+)
 create mode 100644 docs/operations/H024_READ_ONLY_VPS_TASK_STATE_AND_RECOVERY_RUNBOOK.md
 create mode 100644 scripts/check_h024_read_only_vps_observer_task_state.ps1
 create mode 100644 scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
 create mode 100644 tests/test_h024_read_only_vps_task_state_recovery.py

Push:

Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (10/10), done.
Writing objects: 100% (10/10), 11.56 KiB | 3.85 MiB/s, done.
Total 10 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
To https://github.com/citradinnda/institutional-ea.git
   5fa4306..4b99dc7  main -> main

Final git state:

4b99dc7
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
14. Failure History And Lessons From HANDOFF_113
14.1 Generated Python Backslash Syntax Error

Initial generated test file contained:

"task_path": "\",

This caused:

SyntaxError: unterminated string literal

Cause:

Windows root task path backslash was not escaped correctly inside generated Python source.

Fix:

Rewrite the test file from scratch and use the valid Python string:

"task_path": "\\",

Lesson:

When generating Python source from PowerShell, avoid fragile in-place replacements for strings containing backslashes. Prefer full-file rewrite or use a Python writer script with raw triple-quoted content.

14.2 Generated Python Indentation Error

A later patch attempt left the test file structurally corrupted:

IndentationError: expected an indented block after function definition

Cause:

Line-level patching against an already malformed generated file.

Fix:

Overwrite tests/test_h024_read_only_vps_task_state_recovery.py completely with a clean valid version.

Lesson:

If generated Python test code becomes malformed, rewrite the whole file rather than patching one line at a time.

14.3 Mock Validation Versus Real Task Validation

The milestone's script-level validation used:

-MockTaskJsonPath

and mock healthcheck JSON.

This was correct for deterministic tests, but it does not prove the real Windows Scheduled Task is installed or currently running. The real task can be audited by running the task-state checker without -MockTaskJsonPath.

Lesson:

Be precise in status language:

Correct:

The task-state checker is implemented, tested, and committed.
Mock validation passed.
The checker can audit the real Windows Scheduled Task when run without mock input.

Incorrect:

The real VPS scheduled task is installed and healthy.

unless real task-state audit output proves it.

15. Current Operational VPS Observer State

Current implemented operational path:

One-shot read-only observer runner exists.
Scheduled read-only observer wrapper exists.
Windows Task Scheduler install/preview script exists.
Windows Task Scheduler uninstall/preview script exists.
Read-only observer healthcheck exists.
Log capture exists.
Log retention/rotation exists.
Task-state checker exists.
Recovery drill preview exists.
Local operator alert surface exists.
Runbooks exist for scheduler/healthcheck and task-state/recovery.

Current actual deployment reality:

The code path is operational and schedulable.
The task-state checker can audit the real Windows Scheduled Task.
The milestone validation used mock task-state and mock healthcheck evidence for deterministic script-level validation.
The final repo state is pushed and clean except reports/.
It has not been proven in this handoff that the real Windows Scheduled Task is currently installed or enabled on the host.
It has not been proven in this handoff that the task has a recent real last-run timestamp.
It has not been proven in this handoff that real VPS boot/restart occurred.
Live trading remains blocked.

Standard real operational sequence:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60

If the real scheduled task is missing, preview install:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview

If the human operator chooses to install the task:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -IntervalMinutes 5 -Force

Installing the scheduled task still does not authorize trading.

16. Standard Runbook
16.1 Refresh exact-ticket stack if stale

If black-swan guard or readiness fails due stale exact-ticket evidence, run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars
16.2 Run observer once
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1
16.3 Run scheduled wrapper once
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1
16.4 Check observer health
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60

Expected PASS:

H024 read-only VPS observer healthcheck verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
16.5 Audit scheduled task state
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15

Expected PASS if real task is installed/enabled/fresh:

H024 read-only VPS observer task-state verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0

Fail-closed is expected if the task is not installed, disabled, stale, or unverifiable.

16.6 Run recovery drill preview
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60

Expected PASS if task-state and health evidence are fresh PASS:

H024 read-only VPS recovery drill preview verdict: PASS
Operator state: READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
16.7 Preview scheduled task install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview

Expected:

Preview only. No scheduled task was registered.
16.8 Install scheduled task
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -IntervalMinutes 5 -Force

Only do this if the human operator wants the scheduled task installed.

Still does not authorize trading.

16.9 Preview uninstall
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1 -Preview

Expected:

Preview only. No scheduled task was removed.
16.10 Uninstall scheduled task
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1

Only do this if the human operator wants the scheduled task removed.

17. Verification Block For Next AI

Run this first:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

function Run-Native {
    param(
        [Parameter(Mandatory=$true)][string]$Exe,
        [string[]]$Args = @()
    )
    & $Exe @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Exe $($Args -join ' ')"
    }
}

Run-Native git @("status")
Run-Native git @("log","--oneline","-8")

Run-Native python @("-m","pytest","tests\test_h024_read_only_vps_deployment_readiness_aggregate.py","tests\test_h024_read_only_vps_scheduler_healthcheck.py","tests\test_h024_read_only_vps_task_state_recovery.py")

Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\run_h024_read_only_vps_observer_scheduled.ps1")
Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\check_h024_read_only_vps_observer_health.ps1","-MaxAgeMinutes","60")

Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\install_h024_read_only_vps_observer_task.ps1","-Preview")
Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\uninstall_h024_read_only_vps_observer_task.ps1","-Preview")

# Real task-state audit. This may fail closed if the real scheduled task is not installed/enabled/fresh.
Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\check_h024_read_only_vps_observer_task_state.ps1","-ExpectedIntervalMinutes","5","-MaxLastRunAgeMinutes","15")

# Recovery drill preview. This requires fresh PASS healthcheck and task-state evidence.
Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\run_h024_read_only_vps_recovery_drill_preview.ps1","-MaxEvidenceAgeMinutes","60")

Run-Native git @("status")

Expected:

HEAD is 4b99dc7 or later.
Origin is up to date.
Focused tests pass.
Scheduled wrapper completes with exit code 0.
Healthcheck PASS.
Install preview does not register a task.
Uninstall preview does not remove a task.
Real task-state checker PASS only if the real task is installed/enabled/fresh.
Real recovery drill preview PASS only if healthcheck and task-state evidence are fresh PASS.
Final git status shows only reports/ untracked.

If exact-ticket evidence is stale, refresh using Section 16.1.

If the real scheduled task is not installed, task-state audit may correctly fail closed. Do not weaken the checker. Use install preview first, then install only if the human operator wants it.

18. Commit Discipline

Use this pattern:

git status
python -m pytest <focused test file>
python <build script>
python <verify script> <report path> --require-pass
git status
git add -- <only intended tracked files>
git diff --cached --check
git commit -m "<clear commit message>"
git push
git status

Use Run-Native.

Never add reports/.

Never commit if verifier fails under --require-pass.

Never claim success without final git status.

If only git push fails because of DNS/network, do not rerun implementation. Retry git push after network recovers.

19. Static Safety Expectations

Known frozen legacy exceptions:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

These are historical/pre-gate artifacts only.

New observer/deployment/task-state/recovery/alert code must not introduce:

order_send
order_check
symbol_select
live MT5 mutation call sites
trade request construction for close/modify
SL/TP modify requests
close requests
entry requests
order-capable trading loops

Read-only scripts, healthchecks, logs, task previews, task state checks, recovery previews, local alerts, and status summaries are acceptable.

20. Operator Language To Preserve

Use:

read-only observer
OK but trading not authorized
fail closed
operator review required
no broker mutation authorized
observer workflow authorized for operator review only
black-swan guard clear but trading not authorized
VPS readiness coherent for read-only observation only
healthcheck OK but trading not authorized
scheduler operational for read-only observer only
task-state OK but trading not authorized
recovery drill preview OK but trading not authorized
local operator alert only

Avoid:

ready to trade
safe to execute
approved to close
approved to modify
can proceed with order
deployment means trading enabled
production trading enabled
alert sent externally
automatic remediation complete
21. Current Deployment Reality

Current status:

Read-only VPS observer path is operational, schedulable, healthcheckable, auditable, and recoverable by preview/runbook.

Live trading is still blocked.

Implemented:

runtime lockouts
runtime heartbeat
tick/spread supervisor
exposure/inventory supervisor
account risk/margin supervisor
runtime safety aggregate
unified read-only runtime supervision
no-mutation gate
exact-ticket governance
exact-ticket decision artifact
pre-action evidence aggregate
bar-age evidence
manual approval gate preview
operator decision v2 preview
execution readiness dry-run schema preview
black-swan guard
VPS deployment readiness aggregate
one-shot read-only VPS observer runner
scheduled read-only observer wrapper
Windows Task Scheduler install/preview script
Windows Task Scheduler uninstall/preview script
healthcheck script
log capture
log retention/rotation
VPS scheduler/healthcheck runbook
task-state audit script
recovery drill preview script
local operator alert JSON/text/console surface
task-state/recovery runbook

Still not authorized:

order_check
order_send
live broker request construction
executable request dictionary
close/modify
SL/TP modification
new entry
order-capable trading loop
automatic execution
symbol_select from new observer/deployment/task-state/recovery code
external mutation by alert surface
22. Recommended Next Milestone

Next milestone:

H024 read-only VPS real scheduler install/audit dry-run-to-live operator checklist and evidence bundle.

Purpose:

Move from implemented task-state/recovery tooling to a real VPS operational evidence bundle that proves the scheduled observer is installed, enabled, running periodically, producing fresh logs, passing healthcheck, passing task-state audit, and producing recovery drill preview evidence.

This should still be read-only only.

Must include:

A practical operator checklist for real VPS install and audit.
A script that bundles local read-only operational evidence under reports/.
Evidence bundle should include:
git HEAD
git status
scheduled wrapper latest summary
healthcheck packet
task-state packet
recovery drill preview packet
latest log path
latest log tail
install preview output if task missing
explicit safety booleans all false for trading/mutation
Optionally add scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1.
Optionally add docs/operations/H024_READ_ONLY_VPS_REAL_SCHEDULER_AUDIT_CHECKLIST.md.
Tests for evidence bundle generation using mock local packets/logs.
Keep outputs under reports/.
Keep reports/ untracked.
Do not add governance-only layers.
Do not add external alerting yet unless explicitly requested.
Do not enable trading.
Do not close or modify the canary.
Do not build live broker requests.
Do not build executable trade request dictionaries.

Alternative next milestone if the user wants even more operations:

H024 read-only VPS log/health dashboard snapshot as local static HTML/Markdown under reports/, generated from existing packets only.

This should remain local-only and read-only.

23. Suggested Next Prompt

Give the next AI this prompt:

Please read docs/operations/handoffs/HANDOFF_113.md carefully and follow it exactly. It supersedes all older handoffs. Continue from the completed H024 read-only VPS task-state audit, restart/recovery drill preview, and operator alert surface milestone at commit 4b99dc7 or later. Preserve every hard safety boundary.

First verify the base state using the HANDOFF_113 verification block. Then implement the next operational read-only VPS milestone: a real scheduler install/audit operator checklist and local evidence bundle for the read-only VPS observer. This must be practical VPS operations work, not another governance-only packet. Add scripts/runbook/tests to bundle local evidence from git status, latest scheduled wrapper summary, healthcheck packet, task-state packet, recovery drill preview packet, latest log path, latest log tail, and explicit safety booleans. Keep generated outputs under reports/ and keep reports/ untracked. It must remain read-only only: no broker mutation, no order_check, no order_send, no symbol_select, no entries, no close/modify, no executable trade request, no live broker request, no external mutation, and no order-capable trading loop. Use focused tests/verifiers and give concise suggested next prompts after each milestone.
24. Final Reminder

Current posture:

Observe only.
Supervise only.
Run read-only VPS observer only.
Schedule read-only observer only.
Healthcheck read-only observer only.
Audit task state read-only only.
Preview recovery drill only.
Alert locally only.
Fail closed.
Authorize no trading.
Authorize no close/modify.
Authorize no order_check.
Authorize no order_send.
Authorize no symbol_select.
Authorize no live broker request.
Authorize no executable trade request.
Keep reports/ untracked.

The next useful phase is a real VPS scheduler install/audit checklist and evidence bundle for the read-only observer.

Do not trade.

Do not close or modify.

Do not build a live broker request.

Do not build an executable trade request dictionary.

Do not run an order-capable trading loop.
