# HANDOFF_111 — Fully Self-Contained H024 Operational Read-Only VPS Observer Handoff

This handoff supersedes HANDOFF_110, HANDOFF_109, and all older handoffs.

This is the source of truth for the next AI.

It captures the completed H024 read-only VPS deployment readiness aggregate and observer runner path, including:

- exact repo state
- pushed commits
- current canary identity
- hard safety boundaries
- full H024 stack context
- operational runner path
- readiness aggregate behavior
- validation outputs
- failure history
- lessons learned
- exact runbooks
- commit discipline
- next deployment-focused milestone

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

The project has now moved from pure governance into operational read-only VPS observer infrastructure.

Next useful work must be operational:

- scheduler install/uninstall
- healthcheck
- log capture
- log rotation
- stale-run detection
- VPS restart/recovery runbook

Do not drift back into governance-only work.

---

## 2. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Treat this handoff as the source of truth.
3. Continue from commit `094cb7b` or later.
4. Preserve every hard safety boundary.
5. Keep all H024 work read-only unless a future milestone explicitly says otherwise.
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
19. Never treat VPS deployment/readiness as trading authorization.
20. Keep `reports/` untracked.
21. Fail closed on missing, malformed, stale, ambiguous, inconsistent, unsafe, or unverifiable state.
22. Use focused tests and packet verifiers during iteration.
23. Do not ask the user to run the full suite after every small patch.
24. Give concise suggested next prompts after each milestone.

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

`094cb7b Add handoff document #110`

Completed operational milestone commit:

`0792bad Add H024 read-only VPS deployment readiness aggregate`

Important recent history:

```text
094cb7b Add handoff document #110
0792bad Add H024 read-only VPS deployment readiness aggregate
d88cbe1 Add handoff document #109
5de0187 Add handoff document #109
67cfc43 Fix H024 black-swan guard validation and timestamp handling
f62de7c Add H024 read-only black-swan guard
1a8ec4f Add H024 exact-ticket close modify execution readiness dry-run schema preview
ba9692b Add handoff document #108
e0921f2 Add H024 exact-ticket close modify operator decision v2 preview
9f6e65c Add handoff document #107
8761a57 Add H024 exact-ticket close modify manual approval gate preview
d974191 Add handoff document #106
e370a60 Fix H024 pre-action aggregate upstream validation path
9f061c1 Add H024 exact-ticket close modify decision artifact validator
5249ad1 Add H024 runtime no-mutation safety gate
224371a Add H024 unified read-only runtime supervision
8e8979c Add H024 runtime safety aggregate supervisor
1c331c6 Add H024 runtime account risk margin safety supervisor
0db61fa Add H024 runtime exposure inventory safety supervisor
abecff8 Add H024 runtime tick and spread safety supervisor
187e9dd Add H024 runtime safety heartbeat packet
98efc2a Add H024 runtime safety lockout reader

Final confirmed git status after HANDOFF_110 commit:

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
Do not treat any readiness packet as trading permission.
Do not add reports/ to git.

Allowed:

Read-only MT5/account/symbol/position introspection if already supported by existing code.
JSON/JSONL packet generation.
Verifiers.
Read-only runner scripts.
Read-only scheduler/healthcheck/logging infrastructure.
Operator runbooks.
Fail-closed safety checks.

Interpretation:

PASS means the packet is coherent.

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

Latest validated state from the observer/readiness milestone:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
Exact ticket: 4413054432
Exact identifier: 4413054432

The canary was observed, but this does not authorize close/modify or trading.

The position being open over three bars is classified as:

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

run/build script: scripts/build_h024_runtime_safety_heartbeat_jsonl.py

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

9. Completed HANDOFF_111 Milestone Context
Milestone

H024 read-only VPS deployment readiness aggregate and observer runner.

Main milestone commit:

0792bad Add H024 read-only VPS deployment readiness aggregate

Handoff commit already pushed before this superseding handoff:

094cb7b Add handoff document #110

This HANDOFF_111 is being added because the user correctly judged HANDOFF_110 insufficiently self-contained.

Files added by milestone commit 0792bad
docs/operations/H024_READ_ONLY_VPS_DEPLOYMENT_READINESS_AGGREGATE.md
quantcore/execution/h024_read_only_vps_deployment_readiness_aggregate.py
scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
scripts/run_h024_read_only_vps_observer_once.ps1
scripts/verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
tests/test_h024_read_only_vps_deployment_readiness_aggregate.py
Report path

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Passing readiness state

READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED

Passing next action

RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED

Fail-closed readiness state

FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed next action

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

10. What The VPS Readiness Aggregate Checks

The aggregate consumes the latest JSONL evidence for:

Runtime heartbeat.
Runtime lockout reader.
Tick/spread supervisor.
Exposure/inventory supervisor.
Account risk/margin supervisor.
Runtime safety aggregate.
Unified read-only runtime supervision.
Runtime no-mutation safety gate.
Exact-ticket close/modify governance.
Exact-ticket decision artifact.
Exact-ticket pre-action evidence aggregate.
Exact-ticket bar-age exit-condition evidence.
Exact-ticket manual approval gate preview.
Exact-ticket operator decision v2 preview.
Execution readiness dry-run schema preview.
Read-only black-swan guard.

It checks:

upstream report exists
upstream JSONL is well formed
upstream verdict is PASS
upstream embedded violations are absent
upstream timestamp is fresh
expected strategy where represented
all authorization fields remain false
effective new entries remain blocked
no executable/live request payload exists
exact canary identity remains locked
black-swan guard is clear
environment assumptions are coherent
reports directory exists and is writable
venv is active or Python is under .venv
MetaTrader5 package is importable unless explicitly allowed by CLI override
operator runbook commands do not contain forbidden mutation tokens

It intentionally authorizes no trading.

11. What The VPS Observer Runner Does

Runner:

scripts/run_h024_read_only_vps_observer_once.ps1

The final runner is intentionally simple and operational.

It refreshes the runtime/read-only operational chain:

runtime heartbeat
runtime lockout reader
tick/spread supervisor
exposure/inventory supervisor
account risk/margin supervisor
runtime safety aggregate
unified read-only runtime supervision
runtime no-mutation safety gate
read-only black-swan guard
VPS readiness aggregate

It then verifies:

black-swan guard --require-pass
VPS readiness aggregate --require-pass

It does not search legacy builder names.

It does not rerun every exact-ticket builder.

It consumes exact-ticket stack reports as upstream evidence. If those reports are stale, missing, malformed, fail-closed, or unsafe, black-swan guard/readiness fail closed.

This design is intentional.

Operational runner should be predictable, not a legacy orchestration engine.

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
12.3 Verify readiness directly
python scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass

Expected PASS:

H024 read-only VPS deployment readiness records: 1
Violations: 0
Verifier verdict: PASS
Record verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
13. Final Validation Outputs From Completed Milestone
13.1 Focused test

Focused test file:

tests/test_h024_read_only_vps_deployment_readiness_aggregate.py

Result:

collected 16 items
tests\test_h024_read_only_vps_deployment_readiness_aggregate.py ................ [100%]
16 passed
13.2 Exact-ticket refresh

Final successful refresh included:

Wrote reports\h024_exact_ticket_canary_close_modify_decision_artifact.jsonl
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
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

Bar-age evidence:

Wrote reports\h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False

Manual approval gate:

Wrote reports\h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
manual_approval_gate_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False

Operator decision v2:

Wrote reports\h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl
Verdict: PASS
Violations: 0
operator_decision_v2_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False

Execution readiness dry-run schema preview:

Wrote reports\h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl
Verdict: PASS
Violations: 0
execution_readiness_dry_run_schema_preview_constructed: True
execution_readiness_dry_run_schema_preview_authorizes_execution: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
13.3 Black-swan guard

Builder:

Wrote reports\h024_read_only_black_swan_guard.jsonl
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

Verifier:

H024 read-only black-swan guard records: 1
Violations: 0
Verifier verdict: PASS
Record verdict: PASS
Operator state: BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED
13.4 VPS readiness aggregate

Builder:

Wrote reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl
Verdict: PASS
Violations: 0
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
read_only_observer_workflow_authorized_for_operator_review: True
effective_new_entries_blocked: True
broker mutation authorized: False
order check authorized: False
order send authorized: False
entry authorized: False
close modify authorized: False
xauusd order authorized: False
usdjpy order authorized: False
trading loop authorized: False
automatic execution authorized: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
symbol_select_authorized: False
vps_deployment_readiness_authorizes_trading: False

Verifier:

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
13.5 Observer runner

Final runner completion:

H024 read-only VPS observer run complete.
No trading, broker mutation, order_check, order_send, symbol_select, entry, close/modify, executable trade request, live broker request, or order-capable trading loop was authorized.
13.6 Commit and push

Milestone commit:

[main 0792bad] Add H024 read-only VPS deployment readiness aggregate
 6 files changed, 1341 insertions(+)
 create mode 100644 docs/operations/H024_READ_ONLY_VPS_DEPLOYMENT_READINESS_AGGREGATE.md
 create mode 100644 quantcore/execution/h024_read_only_vps_deployment_readiness_aggregate.py
 create mode 100644 scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
 create mode 100644 scripts/run_h024_read_only_vps_observer_once.ps1
 create mode 100644 scripts/verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
 create mode 100644 tests/test_h024_read_only_vps_deployment_readiness_aggregate.py

Push:

To https://github.com/citradinnda/institutional-ea.git
   d88cbe1..0792bad  main -> main

HANDOFF_110 commit:

[main 094cb7b] Add handoff document #110
 1 file changed, 842 insertions(+)
 create mode 100644 docs/operations/handoffs/HANDOFF_110.md

HANDOFF_110 push:

To https://github.com/citradinnda/institutional-ea.git
   0792bad..094cb7b  main -> main

Final git status after HANDOFF_110:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
14. Failure History And Lessons
14.1 Initial runner tried too much

Problem:

Initial VPS runner tried to discover many legacy builder names and rerun exact-ticket/governance builders.

Symptoms:

missing unified builder name
missing decision artifact validator name
governance builder refreshed runtime reports internally
confusing output
increased fragility

Resolution:

Simplified runner. It now refreshes operational runtime chain, black-swan guard, and readiness aggregate only. It consumes exact-ticket stack reports as upstream evidence.

Lesson:

Operational runner should be predictable and narrow.

14.2 Actual unified builder name

The real unified runtime supervision builder is:

scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py

The real report is:

reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl

Do not assume older names.

14.3 Actual decision artifact name

The real decision artifact builder is:

scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py

The real report is:

reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

Do not use:

decision_artifact_validator.jsonl

14.4 PowerShell interpolation bug

Failure:

Variable reference is not valid. ':' was not followed by a valid variable name character.

Cause:

PowerShell parsed $Name: incorrectly.

Fix:

Use ${Name}:.

Lesson:

In PowerShell strings, use ${Variable} before punctuation.

14.5 Black-swan guard stale evidence failure was correct

Black-swan guard failed closed because exact-ticket evidence was stale beyond 3600 seconds.

This is correct.

Do not loosen freshness checks casually.

Refresh upstream evidence instead.

14.6 Bar-age flag must be preserved

Manual approval and downstream exact-ticket builders can internally refresh bar-age evidence.

If called without:

--position-open-over-three-bars

the bar-age packet can become:

INSUFFICIENT_BAR_AGE_EVIDENCE

and fail closed.

Always preserve the flag for current operator-reported bar-age context.

14.7 Readiness aggregate over-strictness fixed

Initial readiness aggregate failed because:

It required newer construction flags in older upstream packets.
It treated *_absent: True safety checks as executable request objects.
It looked for the wrong decision artifact report.

Final fixes:

Missing construction flags in older upstream packets are tolerated.
Unsafe non-false construction flags still fail.
Actual request object payloads still fail.
*_absent, *_blocked, *_constructed, and *_authorized safety fields are not treated as request payloads.
Correct decision artifact report path is first.

Safety was not weakened.

15. Verification Block For Next AI

Run this first:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

function Run-Native {
    param(
        [Parameter(Mandatory=$true)][string]$Exe,
        [Parameter(ValueFromRemainingArguments=$true)][string[]]$Args
    )
    & $Exe @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Exe $($Args -join ' ')"
    }
}

Run-Native git status
Run-Native git log --oneline -10

Run-Native python -m pytest tests\test_h024_read_only_vps_deployment_readiness_aggregate.py

Run-Native powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1

Run-Native python scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass

Run-Native git status

Expected:

HEAD is 094cb7b or later.
Focused readiness tests pass.
Observer runner completes.
Black-swan guard PASS.
VPS readiness aggregate PASS.
Verifier PASS.
Violations 0.
All trading/action authorization fields false.
symbol_select_authorized false.
vps_deployment_readiness_authorizes_trading false.
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

Read-only scripts and status checks are acceptable.

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

Read-only VPS observer path is operational.

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
20. Recommended Next Milestone

Next milestone:

H024 read-only VPS scheduler, healthcheck, and log rotation path

Purpose:

Turn the one-shot observer runner into practical VPS operations without enabling trading.

Must include:

scheduler install or preview script for Windows Task Scheduler
scheduler disable/uninstall script
healthcheck script
last observer run timestamp summary
latest readiness verdict
latest black-swan verdict
latest heartbeat status
latest no-mutation gate status
reports/log path checks
stale readiness detection
log output path under untracked runtime directory
log retention/rotation
operator runbook for VPS boot/restart/recovery
fail-closed behavior for missing/stale health evidence

Suggested files:

scripts/install_h024_read_only_vps_observer_task.ps1
scripts/uninstall_h024_read_only_vps_observer_task.ps1
scripts/check_h024_read_only_vps_observer_health.ps1
docs/operations/H024_READ_ONLY_VPS_SCHEDULER_HEALTHCHECK_RUNBOOK.md
tests/test_h024_read_only_vps_scheduler_healthcheck.py

Optional Python packet if needed:

quantcore/execution/h024_read_only_vps_observer_healthcheck.py
scripts/build_h024_read_only_vps_observer_healthcheck_jsonl.py
scripts/verify_h024_read_only_vps_observer_healthcheck_jsonl.py
reports/h024_read_only_vps_observer_healthcheck.jsonl

Keep it operational.

Do not create another abstract governance layer.

21. Suggested Next Prompt

Give the next AI this prompt:

Please read docs/operations/handoffs/HANDOFF_111.md carefully and follow it exactly. It supersedes all older handoffs. Continue from the completed H024 operational read-only VPS observer milestone at commit 094cb7b or later. Preserve every hard safety boundary.

First verify the base state using the HANDOFF_111 verification block. Then implement the H024 read-only VPS scheduler, healthcheck, and log rotation path. This must be practical VPS operations work, not another governance-only packet. Add scripts/runbook to install or preview a Windows Task Scheduler entry for the read-only observer, disable/uninstall it, check observer health, summarize latest readiness/black-swan/heartbeat/no-mutation status, verify report/log paths, detect stale readiness, and rotate or limit logs. It must remain read-only only: no broker mutation, no order_check, no order_send, no symbol_select, no entries, no close/modify, no executable trade request, no live broker request, and no order-capable trading loop. Keep reports/ untracked. Use focused tests/verifiers and give concise suggested next prompts after each milestone.
22. Final Reminder

Current posture:

Observe only.
Supervise only.
Run read-only VPS observer only.
Fail closed.
Authorize no trading.
Authorize no close/modify.
Authorize no order_check.
Authorize no order_send.
Authorize no symbol_select.
Authorize no live broker request.
Authorize no executable trade request.
Keep reports/ untracked.

The next useful phase is scheduler/healthcheck/logging for the read-only observer.

Do not trade.

Do not close or modify.

Do not build a live broker request.

Do not build an executable trade request dictionary.

Do not run an order-capable trading loop.