# HANDOFF_112 — Fully Self-Contained H024 Read-Only VPS Scheduler / Healthcheck / Log-Rotation Handoff

This handoff supersedes HANDOFF_111, HANDOFF_110, HANDOFF_109, and all older handoffs.

This is the source of truth for the next AI.

It captures the completed H024 read-only VPS scheduler, healthcheck, and log-rotation milestone, including:

- exact repo state
- pushed commit
- current canary identity
- hard safety boundaries
- full H024 stack context
- read-only VPS observer runner path
- scheduled wrapper behavior
- Windows Task Scheduler install/preview behavior
- Windows Task Scheduler uninstall/preview behavior
- healthcheck behavior
- log capture and retention behavior
- validation outputs
- failure/fix history
- final git state
- next recommended operational read-only VPS milestone

This handoff is intentionally redundant. The next AI should not need to infer missing context from older handoffs.

---

## 1. Current Project Direction

The user is tired of endless governance-only milestones.

The project direction is now:

1. Preserve the already-strong safety/governance stack.
2. Stop inventing abstract governance layers unless directly needed.
3. Build practical read-only deployment infrastructure.
4. Get the system running repeatedly as a read-only VPS observer.
5. Keep all trading and broker mutation blocked.
6. Make operational progress toward a VPS-running observer: scheduling, healthchecking, logs, restart/recovery, and operator runbooks.

The project is now in operational read-only VPS observer infrastructure.

Useful work should remain operational:

- scheduled task installation/preview
- scheduled task disable/uninstall
- scheduled wrapper execution
- healthcheck
- log capture
- log rotation
- stale-run detection
- boot/restart recovery runbook
- task-state auditing
- failure/alert surface for operator review

Do not drift back into governance-only work.

---

## 2. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Treat this handoff as the source of truth.
3. Continue from commit `a61fc95` or later.
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
19. Never treat VPS deployment/readiness/scheduler health as trading authorization.
20. Keep `reports/` untracked.
21. Fail closed on missing, malformed, stale, ambiguous, inconsistent, unsafe, or unverifiable state.
22. Use focused tests and packet verifiers during iteration.
23. Do not ask the user to run the full suite after every small patch.
24. Keep the milestone operational, not governance-only.
25. Give concise suggested next prompts after each milestone.

After each milestone, give:

- concise status summary
- commit hash
- final git state
- one concise suggested next prompt

---

## 3. Repository State

Project:

`institutional-ea`

Local repo path:

`C:\Users\equin\Documents\institutional-ea`

Branch:

`main`

Remote:

`origin/main`

Latest confirmed pushed commit:

`a61fc95 Add H024 read-only VPS observer scheduler healthcheck`

Recent confirmed history:

```text
a61fc95 Add H024 read-only VPS observer scheduler healthcheck
8e65943 Add handoff document #111
094cb7b Add handoff document #110
0792bad Add H024 read-only VPS deployment readiness aggregate
d88cbe1 Add handoff document #109

Confirmed final git status after pushing a61fc95:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime/generated output and must remain untracked.

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
Do not treat any readiness/scheduler/healthcheck packet as trading permission.
Do not add reports/ to git.

Allowed:

Read-only MT5/account/symbol/position introspection if already supported by existing code.
JSON/JSONL packet generation.
Verifiers.
Read-only runner scripts.
Read-only scheduler scripts.
Read-only healthcheck scripts.
Read-only log capture and rotation.
Operator runbooks.
Fail-closed safety checks.

Interpretation:

PASS means the packet or healthcheck is coherent.

PASS does not mean:

trading authorized
close/modify authorized
broker mutation authorized
order_check authorized
order_send authorized
executable request authorized
live broker request authorized
symbol_select authorized
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

Latest validated state from this milestone:

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

Do not assume older handoff candidate names are correct.

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

10. Completed HANDOFF_112 Milestone

Milestone:

H024 read-only VPS scheduler, healthcheck, and log-rotation path.

Commit:

a61fc95 Add H024 read-only VPS observer scheduler healthcheck

Pushed:

To https://github.com/citradinnda/institutional-ea.git
   8e65943..a61fc95  main -> main

Files added:

docs/operations/H024_READ_ONLY_VPS_SCHEDULER_HEALTHCHECK_RUNBOOK.md
scripts/check_h024_read_only_vps_observer_health.ps1
scripts/install_h024_read_only_vps_observer_task.ps1
scripts/run_h024_read_only_vps_observer_scheduled.ps1
scripts/uninstall_h024_read_only_vps_observer_task.ps1
tests/test_h024_read_only_vps_scheduler_healthcheck.py

Commit stats:

[main a61fc95] Add H024 read-only VPS observer scheduler healthcheck
 6 files changed, 919 insertions(+)
 create mode 100644 docs/operations/H024_READ_ONLY_VPS_SCHEDULER_HEALTHCHECK_RUNBOOK.md
 create mode 100644 scripts/check_h024_read_only_vps_observer_health.ps1
 create mode 100644 scripts/install_h024_read_only_vps_observer_task.ps1
 create mode 100644 scripts/run_h024_read_only_vps_observer_scheduled.ps1
 create mode 100644 scripts/uninstall_h024_read_only_vps_observer_task.ps1
 create mode 100644 tests/test_h024_read_only_vps_scheduler_healthcheck.py

Purpose:

Turn the one-shot observer runner into practical VPS operations without enabling trading.

This milestone added:

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

11. New Script Behavior
11.1 Scheduled Wrapper

Script:

scripts/run_h024_read_only_vps_observer_scheduled.ps1

Purpose:

Runs the existing one-shot observer and captures runtime logs.

Default root:

repo root, resolved from script location unless -Root is provided.

Default observer script:

scripts/run_h024_read_only_vps_observer_once.ps1

Default log directory:

reports/runtime/h024_read_only_vps_observer/logs

Default last-run summary:

reports/runtime/h024_read_only_vps_observer/last_run_summary.json

Default retention:

RetentionCount = 288
RetentionDays = 14

Behavior:

Creates runtime state/log directories under reports/runtime/h024_read_only_vps_observer.
Runs the one-shot read-only observer.
Captures output to timestamped .log.
Writes last_run_summary.json.
Rotates logs by count and age.
Exits with the observer's exit code.
Does not authorize trading or broker mutation.

Important fix:

Machine-readable JSON is written as UTF-8 without BOM using:

[System.IO.File]::WriteAllText(..., New-Object System.Text.UTF8Encoding -ArgumentList $false)

This avoids Python JSON parse failures on Windows PowerShell 5.1.

11.2 Install / Preview Scheduled Task

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

Registers a Windows Scheduled Task.
Uses powershell.exe.
Calls the scheduled wrapper script.
Sets repetition interval.
Uses MultipleInstances IgnoreNew.
Uses a finite execution time limit.
Explicitly remains read-only observer infrastructure.

It does not call MT5 mutation APIs.

11.3 Uninstall / Preview Scheduled Task

Script:

scripts/uninstall_h024_read_only_vps_observer_task.ps1

Preview mode:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1 -Preview

Uninstall command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1

Behavior:

Removes the scheduled task if present.
Preview mode shows the action without unregistering anything.
Does not touch trading or broker state.
11.4 Healthcheck

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

Checks:

upstream report exists
upstream JSONL parses
upstream verdict is PASS
upstream embedded violations are absent
timestamp exists and parses
evidence age is within -MaxAgeMinutes
last scheduled run exists
last scheduled run status is COMPLETED
last scheduled run exit code is 0
last scheduled log path exists
log directory exists

Passing health state:

READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed health state:

FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_HEALTHCHECK_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Important:

Healthcheck PASS means the observer operational path is healthy for read-only observation only.

Healthcheck PASS does not authorize trading.

12. Current Standard Runbook
12.1 Refresh exact-ticket stack if stale

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
12.2 Run observer once
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1
12.3 Run scheduled wrapper once
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1
12.4 Check observer health
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60

Expected PASS:

H024 read-only VPS observer healthcheck verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
12.5 Preview scheduled task install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview

Expected:

JSON preview is printed.
Preview only. No scheduled task was registered.
12.6 Install scheduled task
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -IntervalMinutes 5 -Force
12.7 Preview uninstall
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1 -Preview

Expected:

JSON preview is printed.
Preview only. No scheduled task was removed.
12.8 Uninstall scheduled task
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1
13. Final Validation Outputs From Completed HANDOFF_112 Milestone
13.1 Scheduler/healthcheck focused tests

Command:

python -m pytest tests\test_h024_read_only_vps_scheduler_healthcheck.py

Result:

collected 6 items

tests\test_h024_read_only_vps_scheduler_healthcheck.py ...... [100%]

6 passed in 4.30s
13.2 Combined focused tests

Command:

python -m pytest tests\test_h024_read_only_vps_deployment_readiness_aggregate.py tests\test_h024_read_only_vps_scheduler_healthcheck.py

Result:

collected 22 items

tests\test_h024_read_only_vps_deployment_readiness_aggregate.py ................ [ 72%]
tests\test_h024_read_only_vps_scheduler_healthcheck.py ...... [100%]

22 passed in 5.53s
13.3 One-shot observer runner validation

Command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1

Final output included:

H024 read-only VPS observer run complete.
No trading, broker mutation, order_check, order_send, symbol_select, entry, close/modify, executable trade request, live broker request, or order-capable trading loop was authorized.
13.4 Black-swan guard validation

Verifier output:

H024 read-only black-swan guard records: 1
Violations: 0
Verifier verdict: PASS
Record verdict: PASS
Operator state: BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Operator next action: CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
black_swan_guard_clear: True
black_swan_guard_triggered: False
effective_new_entries_blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
black_swan_guard_authorizes_trading: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
13.5 VPS readiness aggregate validation

Verifier output:

H024 read-only VPS deployment readiness records: 1
Violations: 0
Verifier verdict: PASS
Record verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
read_only_observer_workflow_authorized_for_operator_review: True
effective_new_entries_blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
symbol_select_authorized: False
vps_deployment_readiness_authorizes_trading: False
13.6 Scheduled wrapper validation

Command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1

Output:

H024 read-only VPS observer scheduled wrapper finished.
Status: COMPLETED
Exit code: 0
Log: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\logs\h024_read_only_vps_observer_20260512T112549453Z.log
Summary: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\last_run_summary.json
13.7 Healthcheck validation

Command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60

Output:

H024 read-only VPS observer healthcheck verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Health packet: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_healthcheck.json
13.8 Install preview validation

Command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview

Output included:

"task_name":  "H024 Read Only VPS Observer"
"preview_only":  true
"read_only_observer_only":  true
"trading_authorized":  false
"broker_mutation_authorized":  false
"live_execution_authorized":  false
Preview only. No scheduled task was registered.
13.9 Uninstall preview validation

Command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\uninstall_h024_read_only_vps_observer_task.ps1 -Preview

Output included:

"task_name":  "H024 Read Only VPS Observer"
"preview_only":  true
"action":  "unregister_if_present"
"read_only_observer_only":  true
"trading_authorized":  false
"broker_mutation_authorized":  false
"live_execution_authorized":  false
Preview only. No scheduled task was removed.
13.10 Commit and push validation

Commit:

[main a61fc95] Add H024 read-only VPS observer scheduler healthcheck
 6 files changed, 919 insertions(+)
 create mode 100644 docs/operations/H024_READ_ONLY_VPS_SCHEDULER_HEALTHCHECK_RUNBOOK.md
 create mode 100644 scripts/check_h024_read_only_vps_observer_health.ps1
 create mode 100644 scripts/install_h024_read_only_vps_observer_task.ps1
 create mode 100644 scripts/run_h024_read_only_vps_observer_scheduled.ps1
 create mode 100644 scripts/uninstall_h024_read_only_vps_observer_task.ps1
 create mode 100644 tests/test_h024_read_only_vps_scheduler_healthcheck.py

Push:

To https://github.com/citradinnda/institutional-ea.git
   8e65943..a61fc95  main -> main

Final git status:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
14. Failure History And Lessons From HANDOFF_112
14.1 Black-swan guard fail-closed during first attempt

Initial observer run failed on:

scripts\verify_h024_read_only_black_swan_guard_jsonl.py reports\h024_read_only_black_swan_guard.jsonl --require-pass

Cause:

Likely stale exact-ticket evidence.

This was not an implementation safety defect. It was expected fail-closed behavior. The exact-ticket stack was refreshed using the required --position-open-over-three-bars flag where needed, then the observer passed.

Lesson:

Do not loosen freshness checks casually. Refresh stale upstream evidence.

14.2 Python test indentation bug

Initial generated tests/test_h024_read_only_vps_scheduler_healthcheck.py had an indentation error after _ps_exe.

Cause:

Bad generated file content.

Fix:

Rewrote the test file cleanly.

Lesson:

When producing generated files through PowerShell blocks, ensure Python indentation is preserved exactly.

14.3 UTF-8 BOM JSON failure

Tests failed because PowerShell 5.1 Set-Content -Encoding UTF8 wrote UTF-8 with BOM. Python json.loads(path.read_text(encoding="utf-8")) rejected the BOM.

Cause:

Windows PowerShell 5.1 behavior.

Fix:

Machine-readable JSON outputs in:

scripts/run_h024_read_only_vps_observer_scheduled.ps1
scripts/check_h024_read_only_vps_observer_health.ps1

now use:

$utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
[System.IO.File]::WriteAllText($Path, ($Json + [Environment]::NewLine), $utf8NoBom)

Lesson:

For machine-readable JSON emitted from PowerShell scripts, write UTF-8 without BOM.

14.4 First git push failed due DNS/network

Initial git push failed with:

Could not resolve host: github.com

Cause:

Network/DNS issue, not repo/code.

Resolution:

Push succeeded later:

8e65943..a61fc95  main -> main

Lesson:

Do not rerun implementation when push alone fails. Retry push after network/DNS recovers.

15. Verification Block For Next AI

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

Run-Native python @("-m","pytest","tests\test_h024_read_only_vps_deployment_readiness_aggregate.py","tests\test_h024_read_only_vps_scheduler_healthcheck.py")

Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\run_h024_read_only_vps_observer_scheduled.ps1")
Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\check_h024_read_only_vps_observer_health.ps1","-MaxAgeMinutes","60")

Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\install_h024_read_only_vps_observer_task.ps1","-Preview")
Run-Native powershell @("-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\uninstall_h024_read_only_vps_observer_task.ps1","-Preview")

Run-Native git @("status")

Expected:

HEAD is a61fc95 or later.
Origin is up to date.
Focused tests pass.
Scheduled wrapper completes with exit code 0.
Healthcheck PASS.
Install preview does not register a task.
Uninstall preview does not remove a task.
Final git status shows only reports/ untracked.

If exact-ticket evidence is stale, refresh using the exact-ticket refresh block from Section 12.1.

16. Commit Discipline

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

17. Static Safety Expectations

Known frozen legacy exceptions:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

These are historical/pre-gate artifacts only.

New observer/deployment code must not introduce:

order_send
order_check
symbol_select
live MT5 mutation call sites
trade request construction for close/modify
SL/TP modify requests
close requests
entry requests
order-capable trading loops

Read-only scripts, healthchecks, logs, task previews, task state checks, and status summaries are acceptable.

18. Operator Language To Preserve

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

Avoid:

ready to trade
safe to execute
approved to close
approved to modify
can proceed with order
deployment means trading enabled
production trading enabled
19. Current Deployment Reality

Current status:

Read-only VPS observer path is operational and now schedulable.

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
symbol_select from new observer/deployment code
20. Recommended Next Milestone

Next milestone:

H024 read-only VPS task-state audit, restart/recovery drill, and operator alert surface.

Purpose:

Move from schedulable observer to operational VPS resilience without enabling trading.

Must include:

read-only scheduled task state checker
verify task exists, enabled/disabled state, trigger interval, last run time, last task result
detect task not installed, disabled, failing, or stale
optionally inspect Windows Task Scheduler metadata without modifying the task
integrate task-state summary with healthcheck or add a separate operational checker
add VPS restart/recovery drill script or runbook section
add operator alert surface as local JSON/text/console output only, not external mutation
keep logs and runtime outputs under reports/
fail closed for missing/stale task/health evidence
keep all trading and broker mutation authorization false
do not add a governance-only packet unless directly required by the operational checker

Suggested files:

scripts/check_h024_read_only_vps_observer_task_state.ps1
scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
docs/operations/H024_READ_ONLY_VPS_TASK_STATE_AND_RECOVERY_RUNBOOK.md
tests/test_h024_read_only_vps_task_state_recovery.py

Optional integration:

extend scripts/check_h024_read_only_vps_observer_health.ps1 to include task-state evidence when requested by a flag such as -RequireTaskInstalled

Do not enable trading.

Do not close or modify the canary.

Do not build live broker requests.

Do not build executable trade request dictionaries.

21. Suggested Next Prompt

Give the next AI this prompt:

Please read docs/operations/handoffs/HANDOFF_112.md carefully and follow it exactly. It supersedes all older handoffs. Continue from the completed H024 read-only VPS scheduler/healthcheck/log-rotation milestone at commit a61fc95 or later. Preserve every hard safety boundary.

First verify the base state using the HANDOFF_112 verification block. Then implement the next operational read-only VPS milestone: task-state audit, restart/recovery drill, and operator alert surface. This must be practical VPS operations work, not another governance-only packet. Add scripts/runbook/tests to check the Windows Scheduled Task state read-only, summarize enabled/disabled status, trigger interval, last run time/result, detect not-installed/disabled/failing/stale scheduler state, and provide a VPS restart/recovery drill preview. Keep outputs local under reports/ and keep reports/ untracked. It must remain read-only only: no broker mutation, no order_check, no order_send, no symbol_select, no entries, no close/modify, no executable trade request, no live broker request, and no order-capable trading loop. Use focused tests/verifiers and give concise suggested next prompts after each milestone.
22. Final Reminder

Current posture:

Observe only.

Supervise only.

Run read-only VPS observer only.

Schedule read-only observer only.

Healthcheck read-only observer only.

Fail closed.

Authorize no trading.

Authorize no close/modify.

Authorize no order_check.

Authorize no order_send.

Authorize no symbol_select.

Authorize no live broker request.

Authorize no executable trade request.

Keep reports/ untracked.

The next useful phase is task-state audit and VPS restart/recovery drill for the read-only observer.

Do not trade.

Do not close or modify.

Do not build a live broker request.

Do not build an executable trade request dictionary.

Do not run an order-capable trading loop.
