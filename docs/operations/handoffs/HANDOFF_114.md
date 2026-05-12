# HANDOFF_114 — Fully Self-Contained H024 Local Windows Recurring Read-Only Observer Evidence Handoff

This handoff supersedes HANDOFF_113, HANDOFF_112, HANDOFF_111, HANDOFF_110, and all older handoffs.

This is the source of truth for the next AI.

It is intentionally redundant. The next AI should not need to infer missing context from older handoffs.

---

## 1. Executive Summary

The project is H024 inside the `institutional-ea` repository.

The current phase is **local Windows recurring read-only observer deployment evidence**, not live trading.

The user does **not** currently have an Oracle VPS account. Therefore, nothing has been proven on Oracle VPS. The current deployment target is the user's existing local Windows machine, using Windows Task Scheduler, PowerShell, MT5, Python, Git, and local `reports/` evidence.

The correct free-first plan is:

1. Prove repeated local Windows read-only observer operation for free.
2. Keep every broker mutation and trading path blocked.
3. Avoid paying for VPS until local recurring observer evidence is fully PASS.
4. Consider Oracle Always Free later only if it can remain free and if the deployment path is compatible.
5. Do not drift into more abstract governance-only work.
6. Do not convert this system into an order-capable EA in this handoff.

Current status:

- Latest code milestone committed and pushed: `5a1c4cf Add H024 read-only VPS observer evidence bundle`
- Latest handoff before this replacement: `6364053 Add handoff document #113`
- Local Windows Scheduled Task has been installed.
- Scheduled task is named `H024 Read Only VPS Observer`.
- Windows task state is now `Ready`.
- Windows `LastTaskResult` became `0`.
- Task-state audit now passes.
- Scheduled wrapper has completed with exit code `0`.
- Healthcheck passes.
- Black-swan guard passes after exact-ticket evidence refresh.
- Read-only deployment readiness passes.
- Recovery drill preview still fails closed.
- Evidence bundle still fails closed.
- The current remaining blocker is **not trading logic** and **not VPS availability**.
- The current remaining blocker is **timestamp alias handling**: healthcheck packets use `checked_at_utc`, while recovery drill preview and evidence bundle freshness readers treat the healthcheck packet as missing a timestamp.

Current remaining technical fix:

- Add `checked_at_utc` to timestamp aliases in:
  - `scripts/run_h024_read_only_vps_recovery_drill_preview.ps1`
  - `scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1`
- Add focused tests that prove healthcheck packets with `checked_at_utc` are accepted.
- Rerun local evidence sequence.
- Expected final result: healthcheck PASS, task-state PASS, recovery drill preview PASS, evidence bundle PASS, and `reports/` still untracked.

---

## 2. Repository State

Project:

```text
institutional-ea

Local repo path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Remote:

origin/main

Latest known HEAD before writing this replacement handoff:

5a1c4cf Add H024 read-only VPS observer evidence bundle

Recent git log observed:

5a1c4cf (HEAD -> main, origin/main, origin/HEAD) Add H024 read-only VPS observer evidence bundle
6364053 Add handoff document #113
4b99dc7 Add H024 read-only VPS task state recovery audit
5fa4306 Add handoff document #112
a61fc95 Add H024 read-only VPS observer scheduler healthcheck

Final git status repeatedly observed after milestone commit:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime/generated evidence and must remain untracked.

3. User Direction And Constraint: Free-First

The user asked why we were not just trying it immediately on Oracle VPS, then clarified they do not currently have an Oracle VPS account.

Correct interpretation:

No Oracle VPS has been used.
Output paths like C:\Users\equin\Documents\institutional-ea prove current work is on the local Windows machine.
The project should proceed on the current Windows machine first because that costs nothing.
Do not tell the user they need a paid Windows VPS now.
Do not assume Oracle VPS exists.
Do not build Linux/Oracle deployment tooling unless explicitly requested later.

Current free-first plan:

Local Windows PC
+ MT5 already installed/logged in
+ Python venv
+ Git repo
+ PowerShell
+ Windows Task Scheduler
+ local reports/
= free recurring read-only observer proof

Potential future cloud path:

Oracle Always Free may be explored later.
Current code is Windows Task Scheduler + PowerShell + MT5 oriented.
A Linux Oracle Always Free VM would likely need a separate Linux-compatible observer approach.
Do not rewrite the project for Linux yet.
4. Critical Safety Boundary

The user became frustrated and asked to change the handoff to authorize all trading constraints and make the EA open trades, close trades, and everything.

Do not do that.

The project must remain read-only unless a separate deliberate, reviewed, explicitly scoped transition is created later.

Current hard safety constraints:

Do not call order_check.
Do not call order_send.
Do not create entries.
Do not close the canary.
Do not modify the canary.
Do not modify SL/TP.
Do not scale the canary.
Do not place XAUUSD orders.
Do not place USDJPY orders.
Do not run an order-capable trading loop.
Do not construct a live broker request.
Do not construct an executable trade request dictionary.
Do not construct an MT5 request dictionary for trade execution.
Do not call symbol_select from new observer/deployment/recovery code.
Do not mutate broker/account/symbol state.
Do not treat PASS as trading authorization.
Do not treat readiness as trading authorization.
Do not treat scheduler health as trading authorization.
Do not treat recovery preview as trading authorization.
Do not treat evidence bundle PASS as trading authorization.
Do not add reports/ to git.

Allowed work:

read-only MT5/account/symbol/position introspection
JSON/JSONL packet generation
verifiers
read-only local runner scripts
read-only scheduler scripts
read-only healthcheck scripts
read-only task-state audit scripts
read-only recovery drill preview scripts
local JSON/text/console alerts
log capture and rotation
local evidence bundle generation
operator runbooks
focused tests
fail-closed behavior

Interpretation rule:

PASS = packet/check/evidence is coherent for read-only observation only.
PASS != authorization to trade.
PASS != authorization to close or modify.
PASS != authorization to call order_check/order_send.
5. Current Known Canary

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
Open price from older handoff: 4728.4490000000005
Stop loss from older handoff: 4817.394

Current observed state in recent local output:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
H024 position symbol=XAUUSDm
ticket=4413054432
identifier=4413054432
magic=240024
volume=0.01
type=1
verdict=PASS

The user said the MT5 trade is still open.

This is expected under current safety rules.

The code path must not close it.

If the user personally wants to close it, the current safe option is manual close in MT5 outside the project code. The project itself remains observer-only.

6. Existing H024 Read-Only Stack Context

This section summarizes the stack so the next AI does not need older handoffs.

6.1 Runtime Safety Lockout Reader

Purpose:

Reads committed default safety config and local lockout state.
Supports global no-new-entry, manual override lockout, and per-symbol XAUUSD/USDJPY no-new-entry lockouts.
Authorizes no trading.

Known passing state:

LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Current output showed:

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
6.2 Runtime Safety Heartbeat

Purpose:

Read-only MT5 runtime heartbeat.
Verifies MT5 initialization, account availability, expected server, USD account currency, terminal connected state.
Authorizes no trading.

Current output showed:

Verdict: PASS
Violations: 0
Operator state: RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED
MT5 initialized: True
Account server: Exness-MT5Trial6
Account currency: USD
Terminal connected: True
6.3 Tick/Spread Supervisor

Purpose:

Read-only tick/spread supervisor for XAUUSDm and USDJPYm.
Must not call symbol_select.
Authorizes no trading.

Current output showed:

Verdict: PASS
Operator state: TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED
Symbol select authorized: False

Example current ticks:

Symbol USDJPYm: verdict=PASS bid=157.578 ask=157.588 spread_points=9.999999999990905
Symbol XAUUSDm: verdict=PASS bid=4699.047 ask=4699.355 spread_points=307.9999999999927
6.4 Exposure/Inventory Supervisor

Purpose:

Read-only position/order inventory supervisor.
Allows no H024 inventory or the exact known XAUUSDm canary only.
Rejects H024 USDJPY position/order, extra H024 position, pending/open H024 orders, mismatched XAUUSDm identity.
Authorizes no trading.

Current output showed:

Verdict: PASS
Operator state: EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
6.5 Account Risk/Margin Supervisor

Purpose:

Read-only account risk/margin supervisor.
Verifies server, USD account context, balance/equity/margin/free margin/margin level sanity, canary boundedness.
Authorizes no trading.

Current output examples:

Account server: Exness-MT5Trial6
Account currency: USD
Balance: 10000.0
Equity: 10028.98
Profit: 28.98
Margin: 2.36
Free margin: 10026.62
Margin level: 424956.77966101695
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
6.6 Runtime Safety Aggregate

Purpose:

Aggregates heartbeat, tick/spread, exposure/inventory, account risk/margin.
Prevents cherry-picking one passing packet while ignoring failures.
Authorizes no trading.

Current output:

Verdict: PASS
Violations: 0
Operator state: RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
6.7 Unified Read-Only Runtime Supervision

Purpose:

Combines canary supervision and runtime aggregate.
Authorizes no trading.

Current output:

Verdict: PASS
Operator state: UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
6.8 Runtime No-Mutation Safety Gate

Purpose:

Proves mutation/order-capable paths remain blocked.
Future broker-facing code must check the gate.
Authorizes no trading.

Current output:

Verdict: PASS
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
7. Exact-Ticket Close/Modify Stack Context

All exact-ticket close/modify artifacts are read-only and non-authorizing.

Important: despite the names, these artifacts do not permit closing/modifying the canary.

7.1 Governance

Script:

scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_governance.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED

Current output:

Verdict: PASS
Violations: 0
Human decision: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Gate opens mutation path: False
7.2 Decision Artifact

Script:

scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

Passing state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED

Current output:

Decision status: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Requested action: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Exact ticket: 4413054432
Exact identifier: 4413054432
7.3 Pre-Action Evidence Aggregate

Script:

scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl

Important flag:

--position-open-over-three-bars

Current output:

Verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED
User reported position open over three bars: True
7.4 Bar-Age And Exit-Condition Evidence

Script:

scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl

Important flag:

--position-open-over-three-bars

Current output:

Verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False
7.5 Manual Approval Gate Preview

Script:

scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl

Important flag:

--position-open-over-three-bars

Current output:

Verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
manual_approval_gate_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False
7.6 Operator Decision V2 Preview

Script:

scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl

Important flag:

--position-open-over-three-bars

Current output:

Verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
operator_decision_v2_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False
7.7 Execution Readiness Dry-Run Schema Preview

Script:

scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl

Important flag:

--position-open-over-three-bars

Current output:

Verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
execution_readiness_dry_run_schema_preview_constructed: True
execution_readiness_dry_run_schema_preview_authorizes_execution: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
8. Black-Swan Guard And Deployment Readiness Context
8.1 Black-Swan Guard

Script:

scripts/build_h024_read_only_black_swan_guard_jsonl.py

Report:

reports/h024_read_only_black_swan_guard.jsonl

Purpose:

Consumes runtime safety and exact-ticket stack evidence.
Fails closed on stale/missing/malformed/fail-closed/unsafe evidence.
Authorizes no trading.

Important known behavior:

It rejected exact-ticket evidence when stale by about 4260 seconds with max age 3600.
After refreshing exact-ticket evidence, it passed.

Current output after refresh:

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
8.2 VPS Deployment Readiness Aggregate

Script:

scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py

Report:

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Purpose:

Verifies read-only observer workflow readiness.
Authorizes observer review only.
Authorizes no trading.

Current output:

Verdict: PASS
Violations: 0
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED
read_only_observer_workflow_authorized_for_operator_review: True
vps_deployment_readiness_authorizes_trading: False
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
trading_loop_authorized: False
9. Scheduler / Healthcheck / Log Rotation Context

Milestone from HANDOFF_112:

a61fc95 Add H024 read-only VPS observer scheduler healthcheck

Key files:

docs/operations/H024_READ_ONLY_VPS_SCHEDULER_HEALTHCHECK_RUNBOOK.md
scripts/check_h024_read_only_vps_observer_health.ps1
scripts/install_h024_read_only_vps_observer_task.ps1
scripts/run_h024_read_only_vps_observer_scheduled.ps1
scripts/uninstall_h024_read_only_vps_observer_task.ps1
tests/test_h024_read_only_vps_scheduler_healthcheck.py
9.1 Scheduled Wrapper

Script:

scripts/run_h024_read_only_vps_observer_scheduled.ps1

Purpose:

Runs the one-shot read-only observer.
Captures runtime logs.
Writes last-run summary.
Rotates logs by retention count and age.
Exits with observer exit code.
Authorizes no trading.

Default runtime state:

reports/runtime/h024_read_only_vps_observer

Default logs:

reports/runtime/h024_read_only_vps_observer/logs

Default last-run summary:

reports/runtime/h024_read_only_vps_observer/last_run_summary.json

Recent successful wrapper output:

H024 read-only VPS observer scheduled wrapper finished.
Status: COMPLETED
Exit code: 0
Log: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\logs\h024_read_only_vps_observer_20260512T123811165Z.log
Summary: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\last_run_summary.json
9.2 Scheduled Task Install

Script:

scripts/install_h024_read_only_vps_observer_task.ps1

Preview output observed:

{
  "task_name": "H024 Read Only VPS Observer",
  "root": "C:\\Users\\equin\\Documents\\institutional-ea",
  "executable": "powershell.exe",
  "argument": "-NoProfile -ExecutionPolicy Bypass -File \"C:\\Users\\equin\\Documents\\institutional-ea\\scripts\\run_h024_read_only_vps_observer_scheduled.ps1\" -Root \"C:\\Users\\equin\\Documents\\institutional-ea\" -RetentionCount 288 -RetentionDays 14",
  "interval_minutes": 5,
  "retention_count": 288,
  "retention_days": 14,
  "preview_only": true,
  "read_only_observer_only": true,
  "trading_authorized": false,
  "broker_mutation_authorized": false,
  "live_execution_authorized": false
}

Actual install output observed:

Registered scheduled task: H024 Read Only VPS Observer
Interval minutes: 5
Wrapper: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled.ps1
9.3 Healthcheck

Script:

scripts/check_h024_read_only_vps_observer_health.ps1

Report:

reports/h024_read_only_vps_observer_healthcheck.json

Current healthcheck output:

H024 read-only VPS observer healthcheck verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0

Important packet shape:

The healthcheck packet uses:

checked_at_utc

not:

generated_at_utc

Example healthcheck packet core:

{
  "schema_version": 1,
  "strategy": "H024",
  "component": "read_only_vps_observer_healthcheck",
  "checked_at_utc": "2026-05-12T12:38:19.6925801Z",
  "verdict": "PASS",
  "operator_state": "READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED",
  "operator_next_action": "CONTINUE_READ_ONLY_VPS_OBSERVER_NO_TRADING_AUTHORIZED",
  "max_age_minutes": 60,
  "violations": [],
  "read_only_observer_healthcheck_authorizes_trading": false,
  "trading_authorized": false,
  "broker_mutation_authorized": false,
  "live_execution_authorized": false
}

This checked_at_utc timestamp field is the root of the current remaining bug.

10. Task-State / Recovery / Alert Surface Context

Milestone from HANDOFF_113:

4b99dc7 Add H024 read-only VPS task state recovery audit

Key files:

docs/operations/H024_READ_ONLY_VPS_TASK_STATE_AND_RECOVERY_RUNBOOK.md
scripts/check_h024_read_only_vps_observer_task_state.ps1
scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
tests/test_h024_read_only_vps_task_state_recovery.py
10.1 Task-State Audit

Script:

scripts/check_h024_read_only_vps_observer_task_state.ps1

Report:

reports/h024_read_only_vps_observer_task_state.json

Local alert outputs:

reports/h024_read_only_vps_observer_operator_alert.json
reports/h024_read_only_vps_observer_operator_alert.txt

Earlier task-state failure:

last_task_result=1
scheduled_task_last_result_nonzero

Then Windows Task Scheduler ran again and latest task info became:

LastRunTime: 12/05/2026 21.39.49
LastTaskResult: 0
NextRunTime: 12/05/2026 21.44.48
NumberOfMissedRuns: 0

After rerun, task-state passed:

H024 read-only VPS observer task-state verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0

Task-state packet core:

generated_at_utc: 2026-05-12T12:45:10.7064764+00:00
verdict: PASS
operator_state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
operator_next_action: CONTINUE_READ_ONLY_OBSERVER_SCHEDULER_SUPERVISION_NO_TRADING_AUTHORIZED
task_name: H024 Read Only VPS Observer
task_path: \
source_mode: windows_task_scheduler
task_exists: True
state: Ready
expected_interval_minutes: 5
max_last_run_age_minutes: 15
trigger_count: 1
last_run_time_utc: 2026-05-12T12:44:49.0000000Z
last_task_result: 0

This proves local Windows recurring scheduler metadata is coherent for read-only observation only.

10.2 Recovery Drill Preview

Script:

scripts/run_h024_read_only_vps_recovery_drill_preview.ps1

Report:

reports/h024_read_only_vps_recovery_drill_preview.json

Local alert outputs:

reports/h024_read_only_vps_recovery_drill_operator_alert.json
reports/h024_read_only_vps_recovery_drill_operator_alert.txt

Current failure:

H024 read-only VPS recovery drill preview verdict: FAIL_CLOSED
Operator state: FAIL_CLOSED_READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_UNVERIFIED_NO_TRADING_AUTHORIZED
Violations: 1

Current violation:

{
  "code": "healthcheck_evidence_timestamp_missing",
  "severity": "ERROR",
  "message": "healthcheck evidence timestamp is missing or malformed."
}

Root cause:

Recovery drill expects healthcheck evidence timestamp under aliases that do not include checked_at_utc.
Healthcheck packet has checked_at_utc.
Therefore recovery drill incorrectly treats a valid fresh PASS healthcheck as missing timestamp.
10.3 Recovery Drill Is Non-Authorizing

Even when fixed and PASS, recovery drill preview must remain:

read-only only
preview only
no scheduler mutation
no broker mutation
no automatic remediation
no trading authorization
11. Evidence Bundle Context

Milestone commit:

5a1c4cf Add H024 read-only VPS observer evidence bundle

Files added:

docs/operations/H024_READ_ONLY_VPS_REAL_SCHEDULER_AUDIT_CHECKLIST.md
scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1
tests/test_h024_read_only_vps_observer_evidence_bundle.py

Focused tests passed:

tests/test_h024_read_only_vps_observer_evidence_bundle.py .... [100%]
4 passed in 2.62s

Purpose:

Bundle local read-only operational evidence under reports/.
Give the operator one local packet/text summary showing repo status, wrapper summary, healthcheck, task-state, recovery preview, latest log, log tail, and safety booleans.
Authorizes no trading.

Default outputs:

reports/h024_read_only_vps_observer_evidence_bundle.json
reports/h024_read_only_vps_observer_evidence_bundle.txt

Current failure after task-state passed:

H024 read-only VPS observer evidence bundle verdict: FAIL_CLOSED
Operator state: FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_UNVERIFIED_NO_TRADING_AUTHORIZED
Violations: 2

Current evidence bundle violations:

observer healthcheck packet evidence is not fresh: missing timestamp
recovery drill preview packet verdict is not PASS: FAIL_CLOSED

Root cause:

Evidence bundle timestamp alias logic also does not include checked_at_utc.
Recovery drill still fails due to same healthcheck timestamp alias bug.
Therefore evidence bundle has two violations:
healthcheck timestamp missing
recovery drill not PASS

Fix:

Add checked_at_utc to evidence bundle timestamp aliases.
Fix recovery drill timestamp alias.
Rerun recovery and evidence bundle.
Expected evidence bundle result: PASS.
12. Current Exact Validation Trail
12.1 Git State

Current observed git state:

?? reports/
5a1c4cf (HEAD -> main, origin/main, origin/HEAD) Add H024 read-only VPS observer evidence bundle
6364053 Add handoff document #113
4b99dc7 Add H024 read-only VPS task state recovery audit
5fa4306 Add handoff document #112
a61fc95 Add H024 read-only VPS observer scheduler healthcheck
12.2 Exact-Ticket Evidence Refresh

The user refreshed exact-ticket evidence with these commands:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

All refreshed exact-ticket components passed and remained non-authorizing.

12.3 Local Observer Run

The user then ran:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
git status

Result summary:

Scheduled wrapper: COMPLETED, exit code 0
Healthcheck: PASS, 0 violations
Task-state: initially FAIL_CLOSED due last_task_result=1, later PASS after scheduled task last result became 0
Recovery drill preview: FAIL_CLOSED due healthcheck timestamp alias bug
Evidence bundle: FAIL_CLOSED due healthcheck timestamp alias bug and recovery drill FAIL_CLOSED
Git status: clean except reports/
13. Exact Remaining Problem To Fix

Problem:

healthcheck packet uses checked_at_utc
recovery drill preview does not accept checked_at_utc
evidence bundle does not accept checked_at_utc

Observed healthcheck packet:

{
  "checked_at_utc": "2026-05-12T12:38:19.6925801Z",
  "verdict": "PASS",
  "operator_state": "READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED",
  "violations": []
}

Observed recovery violation:

{
  "code": "healthcheck_evidence_timestamp_missing",
  "severity": "ERROR",
  "message": "healthcheck evidence timestamp is missing or malformed."
}

Observed evidence bundle violations:

observer healthcheck packet evidence is not fresh: missing timestamp
recovery drill preview packet verdict is not PASS: FAIL_CLOSED

This is a timestamp alias bug only.

Do not change safety logic.

Do not relax PASS requirements.

Do not weaken fail-closed behavior.

Do not bypass freshness checks.

Do not enable trading.

Just add the correct timestamp alias.

14. Recommended Next Implementation Milestone

Milestone name:

H024 local Windows recurring read-only observer timestamp-alias fix and final evidence PASS

Scope:

Patch scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
Add checked_at_utc to timestamp alias handling for evidence freshness.
Patch scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1
Add checked_at_utc to Get-TimestampValue.
Add/update focused tests:
tests/test_h024_read_only_vps_task_state_recovery.py
tests/test_h024_read_only_vps_observer_evidence_bundle.py
Tests must prove:
healthcheck packet with checked_at_utc is accepted as fresh
recovery drill preview can PASS with healthcheck checked_at_utc
evidence bundle can PASS with healthcheck checked_at_utc
safety booleans remain false
Rerun focused tests.
Rerun local evidence sequence.
Confirm final:
scheduled wrapper COMPLETED exit code 0
healthcheck PASS
task-state PASS
recovery drill preview PASS
evidence bundle PASS
final git status only reports/ untracked

Do not implement any trading.

15. Recommended Validation Commands For Next AI

Start with:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

After patching timestamp alias logic:

python -m pytest tests\test_h024_read_only_vps_task_state_recovery.py tests\test_h024_read_only_vps_observer_evidence_bundle.py

Then run the local evidence sequence:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
git status

Expected final result after fix:

H024 read-only VPS observer scheduled wrapper finished.
Status: COMPLETED
Exit code: 0

H024 read-only VPS observer healthcheck verdict: PASS
Violations: 0

H024 read-only VPS observer task-state verdict: PASS
Violations: 0

H024 read-only VPS recovery drill preview verdict: PASS
Violations: 0

H024 read-only VPS observer evidence bundle verdict: PASS
Violations: 0

git status:
only reports/ untracked
16. Commit Discipline

Use this pattern:

git status
python -m pytest tests\test_h024_read_only_vps_task_state_recovery.py tests\test_h024_read_only_vps_observer_evidence_bundle.py
git add -- scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 tests\test_h024_read_only_vps_task_state_recovery.py tests\test_h024_read_only_vps_observer_evidence_bundle.py
git diff --cached --check
git commit -m "Fix H024 read-only observer timestamp aliases"
git push
git status

Never add reports/.

Never commit generated runtime evidence.

Do not claim success without final git status.

17. Suggested Prompt For Next AI

Give the next AI this prompt:

Please read docs/operations/handoffs/HANDOFF_114.md carefully and follow it exactly. It supersedes all older handoffs and is fully self-contained.

Continue from commit 5a1c4cf or later. The current target is free local Windows recurring read-only observer proof, not Oracle VPS and not paid VPS. The user does not currently have Oracle VPS.

Do not add governance-only work. Do not enable trading. Do not add order_check, order_send, live broker request construction, executable trade request construction, automatic entries, automatic close/modify, SL/TP modification, symbol_select, broker mutation, or order-capable trading loops.

The local Windows scheduled read-only observer is installed. The scheduled wrapper, healthcheck, black-swan guard, deployment readiness, and task-state evidence now pass. The current remaining blocker is narrow: recovery drill preview and evidence bundle fail closed because the healthcheck packet uses checked_at_utc instead of generated_at_utc. Patch timestamp alias handling to accept checked_at_utc in the recovery drill preview and evidence bundle paths, add focused tests, rerun the local evidence sequence, and verify final PASS while reports/ remains untracked.

After the milestone, give a concise status summary, commit hash, validation output, final git state, and one suggested next prompt.
18. Final Safety Reminder

The next AI must not help convert this into an unrestricted EA.

Do not trade.

Do not close or modify the canary through code.

Do not make the EA open trades.

Do not make the EA close trades.

Do not build live broker requests.

Do not build executable trade request dictionaries.

Do not run an order-capable trading loop.

The next useful milestone is a timestamp alias fix that should convert the current almost-complete local recurring read-only observer deployment evidence from FAIL_CLOSED to PASS.
