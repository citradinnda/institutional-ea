# HANDOFF_115 — Fully Self-Contained H024 Local Windows Read-Only Observer Continuity Evidence Handoff

This handoff supersedes HANDOFF_114, HANDOFF_113, HANDOFF_112, HANDOFF_111, HANDOFF_110, and all older handoffs.

This is the source of truth for the next AI.

It is intentionally redundant. The next AI should not need to infer missing context from older handoffs.

---

## 1. Executive Summary

The project is H024 inside the `institutional-ea` repository.

The current phase is **free local Windows recurring read-only observer proof**, not Oracle VPS and not paid VPS.

The user does **not** currently have an Oracle VPS account. Nothing has been proven on Oracle VPS. The deployment target remains the user's existing local Windows machine using:

- Windows Task Scheduler
- PowerShell
- local MT5
- local Python virtual environment
- local Git repository
- local generated `reports/` evidence

The current free-first plan is:

1. Prove repeated local Windows read-only observer operation for free.
2. Keep every broker mutation and trading path blocked.
3. Avoid paid VPS until local recurring observer evidence is fully useful and stable.
4. Consider Oracle Always Free later only if it can remain free and only if the deployment path is compatible.
5. Do not drift into abstract governance-only work.
6. Do not convert the system into an order-capable EA under this handoff.

Current status after HANDOFF_114 and the subsequent milestones:

- `HANDOFF_114` was expanded and committed at `51cf544 Expand handoff document #114`.
- Timestamp alias blocker was fixed at `beafd0f Fix H024 read-only observer timestamp aliases`.
- Local observer continuity summary builder was added at `a7a377b Add H024 read-only observer continuity summary`.
- Continuity summary tests and runbook were added at `bc62c83 Add H024 read-only observer continuity tests and runbook`.
- `bc62c83` is the latest known HEAD before writing HANDOFF_115.
- Branch `main` was up to date with `origin/main` after `bc62c83`.
- Final git state before HANDOFF_115: clean except `reports/` untracked.
- `reports/` is generated runtime evidence and must remain untracked.

Operational PASS state already achieved:

- Local scheduled wrapper completed with exit code `0`.
- Healthcheck: PASS, 0 violations.
- Task-state: PASS, 0 violations.
- Recovery drill preview: PASS, 0 violations.
- Evidence bundle: PASS, 0 violations.
- Continuity summary: PASS, 0 violations.
- Continuity summary focused tests: 4 passed.
- Timestamp-alias focused tests: 16 passed.
- Safety booleans remained false and non-authorizing.

The most recent milestone is **operational proof quality**, not trading. The local Windows read-only observer now has a continuity summary builder that consumes existing wrapper summary/logs and local evidence packets, then emits a PASS/FAIL_CLOSED summary under `reports/`.

---

## 2. Repository State

Project:

```text
institutional-ea

Local repository path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Remote:

origin/main

Latest known commit before HANDOFF_115:

bc62c83 Add H024 read-only observer continuity tests and runbook

Recent git log before HANDOFF_115:

bc62c83 (HEAD -> main, origin/main, origin/HEAD) Add H024 read-only observer continuity tests and runbook
a7a377b Add H024 read-only observer continuity summary
beafd0f Fix H024 read-only observer timestamp aliases
51cf544 Expand handoff document #114
5a1c4cf Add H024 read-only VPS observer evidence bundle
6364053 Add handoff document #113
4b99dc7 Add H024 read-only VPS task state recovery audit

Final git status before HANDOFF_115:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Important rule:

reports/ must remain untracked.

The only file this handoff command should add is:

docs/operations/handoffs/HANDOFF_115.md
3. User Direction And Free-First Constraint

The user explicitly clarified that the current target is not Oracle VPS and not paid VPS.

The correct interpretation:

No Oracle VPS exists for this user right now.
No Oracle VPS has been used.
Current work is local Windows only.
Output paths such as C:\Users\equin\Documents\institutional-ea prove local Windows execution.
The project should continue proving local Windows recurring observer operation first because it costs nothing.
Do not tell the user to buy a Windows VPS.
Do not assume an Oracle account exists.
Do not build Linux/Oracle deployment tooling unless explicitly requested later.

Current free-first architecture:

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
A Linux Oracle Always Free VM would likely require a separate Linux-compatible observer path.
Do not rewrite for Linux yet.
Do not move to paid VPS yet.
4. Critical Safety Boundary

The project remains read-only.

Do not enable trading.

Do not add any of the following:

order_check
order_send
live broker request construction
executable trade request construction
automatic entries
automatic close/modify
SL/TP modification
broker mutation
symbol_select
order-capable trading loops
MT5 request dictionaries for execution
code paths that close the canary
code paths that modify the canary
code paths that scale the canary
code paths that place XAUUSD orders
code paths that place USDJPY orders

Do not treat PASS as trading authorization.

Explicit interpretation rule:

PASS = packet/check/evidence is coherent for read-only observation only.
PASS != authorization to trade.
PASS != authorization to close or modify.
PASS != authorization to call order_check/order_send.
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
read-only continuity evidence scripts
local JSON/text/console alerts
log capture and rotation
local evidence bundle generation
local continuity summaries
operator runbooks
focused tests
fail-closed behavior

Forbidden action remains forbidden even after all observer evidence is PASS.

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
Older open price: 4728.4490000000005
Older stop loss: 4817.394

Current observed state during local evidence runs:

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

This is expected under the current read-only safety rules.

The code path must not close it.

If the user personally wants to close it, the safe path is manual close in MT5 outside this project code. The project itself remains observer-only.

6. Existing Read-Only Runtime Stack

This section summarizes the existing stack so the next AI does not need older handoffs.

6.1 Runtime Safety Lockout Reader

Purpose:

Reads committed default safety config and local lockout state.
Supports global no-new-entry, manual override lockout, and per-symbol XAUUSD/USDJPY no-new-entry lockouts.
Authorizes no trading.

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
6.2 Runtime Safety Heartbeat

Purpose:

Read-only MT5 runtime heartbeat.
Verifies MT5 initialization, account availability, expected server, USD account currency, terminal connected state.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED
MT5 initialized: True
Account server: Exness-MT5Trial6
Account currency: USD
Terminal connected: True
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
6.3 Tick/Spread Supervisor

Purpose:

Read-only tick/spread supervisor for XAUUSDm and USDJPYm.
Must not call symbol_select.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED
Effective new entries blocked: True
Symbol select authorized: False
Broker mutation authorized: False
Order check authorized: False
Order send authorized: False
Entry authorized: False
Close/modify authorized: False
XAUUSD order authorized: False
USDJPY order authorized: False
Trading loop authorized: False
Automatic execution authorized: False

Recent symbol examples:

Symbol USDJPYm: verdict=PASS bid=157.562 ask=157.572 spread_points=9.999999999990905
Symbol XAUUSDm: verdict=PASS bid=4693.467 ask=4693.775 spread_points=307.9999999999927
6.4 Exposure/Inventory Supervisor

Purpose:

Read-only position/order inventory supervisor.
Allows no H024 inventory or the exact known XAUUSDm canary only.
Rejects H024 USDJPY position/order, extra H024 position, pending/open H024 orders, mismatched XAUUSDm identity.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
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
H024 position symbol=XAUUSDm ticket=4413054432 identifier=4413054432 magic=240024 volume=0.01 type=1 verdict=PASS
6.5 Account Risk/Margin Supervisor

Purpose:

Read-only account risk/margin supervisor.
Verifies server, USD account context, balance/equity/margin/free margin/margin level sanity, canary boundedness.
Authorizes no trading.

Recent observed account context:

Account server: Exness-MT5Trial6
Account currency: USD
Balance: 10000.0
Equity: 10034.55
Profit: 34.55
Margin: 2.36
Free margin: 10032.19
Margin level: 425192.79661016946
Margin used fraction: 0.00023518742743820103
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
6.6 Runtime Safety Aggregate

Purpose:

Aggregates heartbeat, tick/spread, exposure/inventory, and account risk/margin.
Prevents cherry-picking a passing packet while ignoring failures.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
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
6.7 Unified Read-Only Runtime Supervision

Purpose:

Combines canary supervision and runtime aggregate.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
Canary supervision records: 1
Canary supervision all records passed: True
Runtime aggregate verdict: PASS
Runtime aggregate operator state: RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
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
6.8 Runtime No-Mutation Safety Gate

Purpose:

Proves mutation/order-capable paths remain blocked.
Future broker-facing code must check the gate.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED
Operator next action: KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION
Unified supervision verdict: PASS
Gate opens mutation path: False
Future broker-facing code must check gate: True
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

All exact-ticket close/modify artifacts remain read-only and non-authorizing.

Important: despite the artifact names, these artifacts do not permit closing or modifying the canary.

7.1 Governance

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
Effective new entries blocked: True
Broker Mutation Authorized: False
Order Check Authorized: False
Order Send Authorized: False
Entry Authorized: False
Close Modify Authorized: False
Xauusd Order Authorized: False
Usdjpy Order Authorized: False
Trading Loop Authorized: False
Automatic Execution Authorized: False
7.2 Decision Artifact

Script:

scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_DECISION_ARTIFACT_REVIEW
Decision status: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Requested action: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Exact ticket: 4413054432
Exact identifier: 4413054432
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
7.3 Pre-Action Evidence Aggregate

Script:

scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl

Important flag:

--position-open-over-three-bars

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_PRE_ACTION_EVIDENCE_REVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
User reported position open over three bars: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
7.4 Bar-Age And Exit-Condition Evidence

Script:

scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl

Important flag:

--position-open-over-three-bars

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_BAR_AGE_EXIT_CONDITION_EVIDENCE_REVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
7.5 Manual Approval Gate Preview

Script:

scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py

Report:

reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl

Important flag:

--position-open-over-three-bars

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_MANUAL_APPROVAL_GATE_PREVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
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

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_OPERATOR_DECISION_V2_PREVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
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

Recent passing state:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
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
execution_readiness_dry_run_schema_preview_constructed: True
execution_readiness_dry_run_schema_preview_authorizes_execution: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
8. Black-Swan Guard And Deployment Readiness
8.1 Black-Swan Guard

Script:

scripts/build_h024_read_only_black_swan_guard_jsonl.py

Report:

reports/h024_read_only_black_swan_guard.jsonl

Purpose:

Consumes runtime safety and exact-ticket stack evidence.
Fails closed on stale/missing/malformed/fail-closed/unsafe evidence.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
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
8.2 Read-Only VPS Deployment Readiness Aggregate

The name still says VPS because earlier milestones used that naming, but the current target is local Windows free recurring observer proof.

Script:

scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py

Report:

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Purpose:

Verifies read-only observer workflow readiness.
Authorizes observer review only.
Authorizes no trading.

Recent passing state:

Verdict: PASS
Violations: 0
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
9. Scheduler / Healthcheck / Log Rotation Context

Key files from prior scheduler milestone:

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

Recent wrapper outputs:

H024 read-only VPS observer scheduled wrapper finished.
Status: COMPLETED
Exit code: 0
Log: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\logs\h024_read_only_vps_observer_20260512T131103636Z.log
Summary: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\last_run_summary.json

And the second run:

H024 read-only VPS observer scheduled wrapper finished.
Status: COMPLETED
Exit code: 0
Log: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\logs\h024_read_only_vps_observer_20260512T131114021Z.log
Summary: C:\Users\equin\Documents\institutional-ea\reports\runtime\h024_read_only_vps_observer\last_run_summary.json
9.2 Scheduled Task Install

Script:

scripts/install_h024_read_only_vps_observer_task.ps1

Known installed task:

Task name: H024 Read Only VPS Observer
Interval minutes: 5
Wrapper: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled.ps1

The task is local Windows Task Scheduler, not Oracle VPS.

9.3 Healthcheck

Script:

scripts/check_h024_read_only_vps_observer_health.ps1

Report:

reports/h024_read_only_vps_observer_healthcheck.json

Important packet shape:

The healthcheck packet uses:

checked_at_utc

not necessarily:

generated_at_utc

Recent passing state after timestamp-alias fix:

H024 read-only VPS observer healthcheck verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Health packet: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_healthcheck.json
10. Task-State / Recovery / Evidence Bundle Context
10.1 Task-State Audit

Script:

scripts/check_h024_read_only_vps_observer_task_state.ps1

Report:

reports/h024_read_only_vps_observer_task_state.json

Local alert outputs:

reports/h024_read_only_vps_observer_operator_alert.json
reports/h024_read_only_vps_observer_operator_alert.txt

Recent passing state:

H024 read-only VPS observer task-state verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Task-state packet: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_task_state.json
Operator alert JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_operator_alert.json
Operator alert text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_operator_alert.txt

This proves local Windows scheduler metadata is coherent for read-only observation only.

10.2 Recovery Drill Preview

Script:

scripts/run_h024_read_only_vps_recovery_drill_preview.ps1

Report:

reports/h024_read_only_vps_recovery_drill_preview.json

Local alert outputs:

reports/h024_read_only_vps_recovery_drill_operator_alert.json
reports/h024_read_only_vps_recovery_drill_operator_alert.txt

Historical blocker:

Recovery drill preview used to fail closed because the healthcheck packet had checked_at_utc.
Recovery drill preview timestamp aliases did not accept checked_at_utc.
It produced violation healthcheck_evidence_timestamp_missing.

Fix commit:

beafd0f Fix H024 read-only observer timestamp aliases

Recent passing state after fix:

H024 read-only VPS recovery drill preview verdict: PASS
Operator state: READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Recovery drill packet: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_recovery_drill_preview.json
Operator alert JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_recovery_drill_operator_alert.json
Operator alert text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_recovery_drill_operator_alert.txt

Recovery drill preview remains non-authorizing:

read-only only
preview only
no scheduler mutation
no broker mutation
no automatic remediation
no trading authorization
10.3 Evidence Bundle

Script:

scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1

Default outputs:

reports/h024_read_only_vps_observer_evidence_bundle.json
reports/h024_read_only_vps_observer_evidence_bundle.txt

Historical blocker:

Evidence bundle also failed because it did not accept checked_at_utc for the healthcheck packet.
It also failed because recovery drill preview was fail-closed.
Once checked_at_utc alias handling was fixed in both recovery and evidence bundle paths, evidence bundle passed.

Fix commit:

beafd0f Fix H024 read-only observer timestamp aliases

Recent passing state:

H024 read-only VPS observer evidence bundle verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Evidence bundle JSON: reports/h024_read_only_vps_observer_evidence_bundle.json
Evidence bundle text: reports/h024_read_only_vps_observer_evidence_bundle.txt
11. Commit beafd0f — Timestamp Alias Fix

Commit:

beafd0f Fix H024 read-only observer timestamp aliases

Purpose:

Fix the narrow blocker from HANDOFF_114.
Add checked_at_utc timestamp alias handling in:
scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1
Add focused tests proving healthcheck packets with checked_at_utc are accepted.
Keep all safety logic intact.
Do not relax PASS requirements.
Do not bypass freshness checks.
Do not enable trading.

Files changed:

scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1
scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
tests/test_h024_read_only_vps_observer_evidence_bundle.py
tests/test_h024_read_only_vps_task_state_recovery.py

Focused test output:

tests/test_h024_read_only_vps_task_state_recovery.py ...........
tests/test_h024_read_only_vps_observer_evidence_bundle.py .....
16 passed in 11.83s

Local evidence sequence after fix:

Scheduled wrapper:
Status: COMPLETED
Exit code: 0

Healthcheck:
PASS
Violations: 0

Task-state:
PASS
Violations: 0

Recovery drill preview:
PASS
Violations: 0

Evidence bundle:
PASS
Violations: 0

Final git state after beafd0f:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Safety boundary after beafd0f:

order_check authorized: False
order_send authorized: False
entry authorized: False
close/modify authorized: False
symbol_select authorized: False
broker mutation authorized: False
live broker request constructed: False
executable trade request constructed: False
trading loop authorized: False
12. Commit a7a377b — Continuity Summary Builder

Commit:

a7a377b Add H024 read-only observer continuity summary

Purpose:

Add a local operational proof quality builder.
Consume existing scheduled wrapper summary/logs and existing observer packets.
Prove multi-run read-only observer continuity.
Emit JSON/text continuity evidence under reports/.
Fail closed on missing/stale/non-PASS evidence.
Fail closed on unsafe true flags.
Authorize no trading.

File committed in a7a377b:

scripts/build_h024_read_only_vps_observer_continuity_summary.ps1

Important detail:

The initial commit a7a377b only committed the builder script. The test and runbook were accidentally left untracked. This was fixed in commit bc62c83.

Builder:

scripts/build_h024_read_only_vps_observer_continuity_summary.ps1

Default outputs:

reports/h024_read_only_vps_observer_continuity_summary.json
reports/h024_read_only_vps_observer_continuity_summary.txt

Inputs read by the builder:

reports/runtime/h024_read_only_vps_observer/last_run_summary.json
reports/runtime/h024_read_only_vps_observer/logs/*.log
reports/h024_read_only_vps_observer_healthcheck.json
reports/h024_read_only_vps_observer_task_state.json
reports/h024_read_only_vps_recovery_drill_preview.json
reports/h024_read_only_vps_observer_evidence_bundle.json

Recent build output:

H024 read-only VPS observer continuity summary verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Continuity JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_continuity_summary.json
Continuity text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_continuity_summary.txt

Continuity summary PASS means:

The local observer continuity evidence is coherent for read-only supervision.

Continuity summary PASS does not authorize:

trading
broker mutation
live execution
automatic remediation
order_check
order_send
entries
close/modify
symbol_select
order-capable loops
13. Commit bc62c83 — Continuity Tests And Runbook

Commit:

bc62c83 Add H024 read-only observer continuity tests and runbook

Purpose:

Fix-forward the incomplete a7a377b commit.
Add the missing continuity summary tests.
Add the missing continuity summary runbook.
Keep reports/ untracked.

Files committed:

docs/operations/H024_READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_RUNBOOK.md
tests/test_h024_read_only_vps_observer_continuity_summary.py

Focused validation output before commit:

tests/test_h024_read_only_vps_observer_continuity_summary.py .... [100%]
4 passed in 4.64s

Commit output:

[main bc62c83] Add H024 read-only observer continuity tests and runbook
 2 files changed, 237 insertions(+)
 create mode 100644 docs/operations/H024_READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_RUNBOOK.md
 create mode 100644 tests/test_h024_read_only_vps_observer_continuity_summary.py

Push output:

To https://github.com/citradinnda/institutional-ea.git
   a7a377b..bc62c83  main -> main

Final git state after bc62c83:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Recent log after bc62c83:

bc62c83 (HEAD -> main, origin/main, origin/HEAD) Add H024 read-only observer continuity tests and runbook
a7a377b Add H024 read-only observer continuity summary
beafd0f Fix H024 read-only observer timestamp aliases
51cf544 Expand handoff document #114
5a1c4cf Add H024 read-only VPS observer evidence bundle
6364053 Add handoff document #113
4b99dc7 Add H024 read-only VPS task state recovery audit
14. Continuity Summary Behavior And Tests

Test file:

tests/test_h024_read_only_vps_observer_continuity_summary.py

Builder script:

scripts/build_h024_read_only_vps_observer_continuity_summary.ps1

Runbook:

docs/operations/H024_READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_RUNBOOK.md

Test coverage:

PASS with healthcheck checked_at_utc alias.
FAIL_CLOSED when completed run count is insufficient.
FAIL_CLOSED when healthcheck checked_at_utc is stale.
FAIL_CLOSED on unsafe true flag.

Focused test output:

collected 4 items

tests/test_h024_read_only_vps_observer_continuity_summary.py .... [100%]

4 passed in 4.64s

The continuity summary intentionally reads existing evidence. It should not cause scheduler mutation, broker mutation, or account mutation.

Current continuity builder parameters:

-Root
-MinRunCount
-MaxPacketAgeMinutes
-MaxLatestRunAgeMinutes
-LogTailLines
-OutputJson
-OutputText

Typical command:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60

Expected PASS output:

H024 read-only VPS observer continuity summary verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Continuity JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_continuity_summary.json
Continuity text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_continuity_summary.txt
15. Most Recent Local Evidence Sequence

The latest local evidence sequence included:

Refresh exact-ticket read-only upstream evidence.
Run local read-only observer twice to establish multi-run continuity evidence.
Refresh local observer packets.
Build continuity summary.
Run focused continuity test.
Commit/push source/test/runbook.
Confirm final git state clean except reports/.

Commands used conceptually:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60

Observed PASS summary:

Healthcheck: PASS, 0 violations.
Task-state: PASS, 0 violations.
Recovery drill preview: PASS, 0 violations.
Evidence bundle: PASS, 0 violations.
Continuity summary: PASS, 0 violations.

Observed non-authorizing safety summary:

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
16. Current Operational State

Current system state:

Local Windows scheduled read-only observer installed: yes
Scheduled task name: H024 Read Only VPS Observer
Scheduled wrapper: working
Scheduled wrapper exit code: 0
Healthcheck: PASS
Task-state: PASS
Recovery drill preview: PASS
Evidence bundle: PASS
Continuity summary: PASS
Final git state before HANDOFF_115: clean except reports/ untracked

Current operational meaning:

The local Windows read-only observer path is coherent.
The recurring local scheduler has been installed.
The wrapper can run successfully.
Healthcheck confirms recent wrapper execution and local runtime evidence.
Task-state confirms Windows Task Scheduler state.
Recovery drill preview can evaluate health/task/readiness without mutating scheduler or broker state.
Evidence bundle can consolidate observer evidence.
Continuity summary can evaluate multiple local observer runtime logs plus upstream packets.
The system is still not authorized to trade.

Current operational limitation:

The project has not yet proven multi-hour or multi-day unattended scheduler continuity.
The latest continuity summary was built after manually running the wrapper twice to establish two fresh logs.
That is valid for the milestone, but the next operational proof should focus on passive scheduled-run cadence over time.
17. Final Git State At Handoff Start

Before writing HANDOFF_115, final git state was:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Before writing HANDOFF_115, recent log was:

bc62c83 (HEAD -> main, origin/main, origin/HEAD) Add H024 read-only observer continuity tests and runbook
a7a377b Add H024 read-only observer continuity summary
beafd0f Fix H024 read-only observer timestamp aliases
51cf544 Expand handoff document #114
5a1c4cf Add H024 read-only VPS observer evidence bundle
6364053 Add handoff document #113
4b99dc7 Add H024 read-only VPS task state recovery audit

After this handoff command runs successfully, the next expected commit should be:

Add handoff document #115

The exact commit hash will be created by the local Git command.

Expected final git status after HANDOFF_115 commit and push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
18. Recommended Validation Commands For Next AI

Start with:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Sanity check current continuity builder tests:

python -m pytest tests\test_h024_read_only_vps_observer_continuity_summary.py

Broader focused observer tests:

python -m pytest `
  tests\test_h024_read_only_vps_task_state_recovery.py `
  tests\test_h024_read_only_vps_observer_evidence_bundle.py `
  tests\test_h024_read_only_vps_observer_continuity_summary.py

Refresh local read-only observer evidence:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60

Expected current outputs:

Healthcheck verdict: PASS
Task-state verdict: PASS
Recovery drill preview verdict: PASS
Evidence bundle verdict: PASS
Continuity summary verdict: PASS
Violations: 0

Do not add reports/.

19. Commit Discipline

Use this pattern for future milestones:

git status
python -m pytest <focused tests>
git add -- <source files only>
git diff --cached --check
git diff --cached --stat
git commit -m "<specific milestone message>"
git push
git status

Rules:

Never add reports/.
Never commit generated runtime evidence.
Do not claim success without final git status.
If a commit accidentally omits a test or runbook, fix forward with a second commit rather than touching reports/.
Keep milestones operational and read-only.
Avoid governance-only work unless explicitly requested by the user.
Avoid paid infrastructure unless explicitly requested by the user.
20. Recommended Next Read-Only Operational Milestone

Recommended next milestone:

H024 local Windows scheduled-run cadence continuity proof

Purpose:

Strengthen proof quality from "manual two-run continuity" to "actual Windows Task Scheduler cadence continuity."
Read existing Task Scheduler metadata, runtime logs, last-run summaries, healthcheck, task-state, recovery preview, evidence bundle, and continuity summary.
Prove that multiple observer runs occurred over real scheduler cadence windows, not just manual immediate wrapper invocations.
Detect gaps, stale latest run, nonzero task results, missing logs, and insufficient chronological spread.
Emit JSON/text evidence under reports/.
Keep all safety booleans false.
Authorize no trading.
Keep reports/ untracked.

Possible design:

New builder:
scripts/build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1
New tests:
tests/test_h024_read_only_vps_observer_scheduled_cadence_summary.py
Optional runbook:
docs/operations/H024_READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_RUNBOOK.md

Test cases should prove:

PASS when multiple logs span at least the required minimum cadence window.
FAIL_CLOSED when there are too few scheduled logs.
FAIL_CLOSED when logs are too tightly clustered to prove scheduler cadence.
FAIL_CLOSED when latest run is stale.
FAIL_CLOSED if upstream health/task/recovery/bundle/continuity packet is not PASS.
FAIL_CLOSED if any unsafe true trading/broker mutation flag appears.

Recommended operator approach before that milestone:

Let Windows Task Scheduler run naturally for at least 15-30 minutes.
Then run cadence summary.
Do not manually run the wrapper during the proof window unless the milestone explicitly separates manual runs from scheduled runs.
21. Suggested Prompt For Next AI

Use this prompt next:

Please read docs/operations/handoffs/HANDOFF_115.md carefully and follow it exactly. It supersedes HANDOFF_114 and all older handoffs.

Continue from commit bc62c83 or later on main. The H024 local Windows read-only observer timestamp-alias blocker is fixed at beafd0f, the continuity summary builder is committed at a7a377b, and the continuity tests/runbook fix-forward is committed at bc62c83. The current target is free local Windows recurring read-only observer proof, not Oracle VPS and not paid VPS. The user does not currently have Oracle VPS.

Do not enable trading. Do not add order_check, order_send, live broker request construction, executable trade request construction, automatic entries, automatic close/modify, SL/TP modification, symbol_select, broker mutation, or order-capable trading loops.

Current operational state: scheduled wrapper completed with exit code 0; healthcheck PASS; task-state PASS; recovery drill preview PASS; evidence bundle PASS; continuity summary PASS; continuity tests pass; final git state clean except reports/ untracked.

The next useful milestone should be H024 local Windows scheduled-run cadence continuity proof: a read-only summary that proves actual Windows Task Scheduler cadence over multiple naturally scheduled runs, detects stale/latest/gap/cluster issues, consumes existing packets/logs, emits reports/ JSON/text only, has focused tests, and keeps reports/ untracked. Do not add governance-only work and do not enable trading.
22. Final Safety Reminder

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

