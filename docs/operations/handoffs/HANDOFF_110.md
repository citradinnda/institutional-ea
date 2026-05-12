# HANDOFF_110 — Fully Self-Contained H024 Read-Only VPS Observer Deployment Readiness Handoff

This handoff supersedes HANDOFF_109 and all older handoffs.

It captures the completed H024 read-only VPS deployment readiness aggregate and observer runner milestone, including the operational read-only VPS observer path, runner commands, validation outputs, hard safety boundaries, current canary state, final git state, failure history, and the next deployment-focused milestone.

This document is intentionally redundant and self-contained so the next AI does not need to guess repo state, validation state, runtime posture, safety posture, implementation files, failure history, or next steps.

---

## 1. Required Behavior For The Next AI

The next AI must:

1. Treat this handoff as the source of truth.
2. Preserve every hard safety boundary.
3. Continue from commit `0792bad` or a later handoff commit.
4. Keep all H024 runtime/deployment-readiness work read-only unless a future milestone explicitly changes scope.
5. Never infer that a passing readiness, guard, governance, evidence, preview, or observer packet authorizes trading.
6. Never call broker mutation functions.
7. Never call `order_check`.
8. Never call `order_send`.
9. Never create entries.
10. Never close or modify the current XAUUSDm canary.
11. Never place USDJPY orders.
12. Never place XAUUSD orders.
13. Never scale the existing canary.
14. Never run an order-capable trading loop.
15. Never call `symbol_select` from new safety/governance/observer/deployment code.
16. Never build a live broker request from governance, decision, evidence, preview, guard, observer, or deployment-readiness artifacts.
17. Never build an executable trade request dictionary.
18. Keep `reports/` untracked.
19. Fail closed on missing, malformed, stale, inconsistent, ambiguous, unsafe, or unverifiable state.
20. Prefer focused tests and packet verifiers during iteration. Do not run the full suite after every tiny patch.
21. After each milestone, give:
    - concise status summary
    - commit hash
    - final git state
    - one concise suggested next prompt

Important operator preference:

The user is tired of endless governance-only milestones. The project direction is operationalization. Do not invent another abstract governance, preview, simulator, or schema layer unless it directly unlocks deployment progress.

---

## 2. Repo State At This Handoff

Project:

`institutional-ea`

Local repo path:

`C:\Users\equin\Documents\institutional-ea`

Branch:

`main`

Remote:

`origin/main`

Latest confirmed pushed commit:

`0792bad Add H024 read-only VPS deployment readiness aggregate`

Relevant immediate history:

```text
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

Final confirmed git status after commit and push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is generated runtime output and must remain untracked.

3. Hard Safety Boundary

Current H024 state is post-canary, read-only, no-mutation.

Do not do any of these:

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
Do not call symbol_select from new safety/governance/decision/evidence/preview/guard/observer/deployment-readiness code.
Do not build a live broker request from governance, decision, evidence, preview, guard, observer, or deployment-readiness artifacts.
Do not build an executable trade request dictionary.
Do not treat any PASS packet as permission to trade.
Do not add reports/ to git.

Close/modify is not authorized.

It is not almost authorized.

It is not authorized because the canary is known.

It remains prohibited unless a future exact-ticket governance path is separately specified, reviewed, and still initially read-only.

A PASS means the relevant read-only packet is coherent.

PASS does not authorize action.

Any unsafe ambiguity must fail closed.

4. Current Known Canary

There is exactly one known H024 standard-demo XAUUSDm canary.

Known identity:

Server: Exness-MT5Trial6
Account currency: USD
Runtime symbol: XAUUSDm
Model symbol: XAUUSD
Side: sell
MT5 position type: 1
Volume: 0.01
Magic: 240024
Ticket/identifier: 4413054432
Entry deal: 3788869526
Open price: 4728.4490000000005
Stop loss: 4817.394

Latest validated observer/readiness state confirms:

Exact ticket: 4413054432
Exact identifier: 4413054432
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
Broker mutation authorized: False
Order check authorized: False
Order send authorized: False
Entry authorized: False
Close/modify authorized: False
XAUUSD order authorized: False
USDJPY order authorized: False
Trading loop authorized: False
Automatic execution authorized: False

The position being open over three bars remains classified as:

OPERATOR_REPORTED_ONLY

This is non-authorizing context only.

5. Existing H024 Stack Summary

The following stack existed before this milestone and remains active:

Runtime safety lockout reader.
Runtime safety heartbeat.
Runtime tick/spread safety supervisor.
Runtime exposure/inventory safety supervisor.
Runtime account risk/margin safety supervisor.
Runtime safety aggregate supervisor.
Unified read-only post-canary runtime supervision.
Runtime no-mutation safety gate.
Exact-ticket close/modify governance.
Exact-ticket close/modify decision artifact.
Exact-ticket close/modify pre-action evidence aggregate.
Exact-ticket bar-age and exit-condition evidence.
Exact-ticket manual approval gate preview.
Exact-ticket operator decision v2 preview.
Exact-ticket execution readiness dry-run schema preview.
Read-only black-swan guard.

Important: all of this is still read-only and non-authorizing.

6. Milestone Completed In HANDOFF_110
H024 Read-Only VPS Deployment Readiness Aggregate And Observer Runner

Commit:

0792bad Add H024 read-only VPS deployment readiness aggregate

Purpose:

Move H024 from mature read-only runtime supervision toward actual VPS-compatible read-only automation.

This milestone added a practical read-only observer deployment path that can be run repeatedly on a VPS to refresh runtime packets, verify black-swan guard, build a VPS readiness aggregate, and verify the readiness aggregate.

It does not enable trading.

It does not create an order-capable loop.

It does not call order_check.

It does not call order_send.

It does not call symbol_select.

It does not build a live broker request.

It does not build an executable trade request dictionary.

Key files added
quantcore/execution/h024_read_only_vps_deployment_readiness_aggregate.py
scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
scripts/verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
scripts/run_h024_read_only_vps_observer_once.ps1
tests/test_h024_read_only_vps_deployment_readiness_aggregate.py
docs/operations/H024_READ_ONLY_VPS_DEPLOYMENT_READINESS_AGGREGATE.md
Report path

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Passing operator state

READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED

Passing operator next action

RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED

Fail-closed operator state

FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed operator next action

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

7. What The Read-Only VPS Observer Runner Does

Runner:

scripts/run_h024_read_only_vps_observer_once.ps1

The runner performs read-only packet generation only.

It runs:

scripts/build_h024_runtime_safety_heartbeat_jsonl.py
scripts/build_h024_runtime_safety_lockout_jsonl.py
scripts/build_h024_runtime_tick_spread_safety_supervisor_jsonl.py
scripts/build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
scripts/build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
scripts/build_h024_runtime_safety_aggregate_supervisor_jsonl.py
scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py
scripts/build_h024_read_only_black_swan_guard_jsonl.py
scripts/verify_h024_read_only_black_swan_guard_jsonl.py reports/h024_read_only_black_swan_guard.jsonl --require-pass
scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
scripts/verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass

The runner intentionally does not rerun every legacy exact-ticket builder. It consumes the existing exact-ticket governance/decision/evidence/preview stack as upstream evidence, and black-swan guard plus the readiness aggregate fail closed if those reports are missing, stale, malformed, fail-closed, or unsafe.

Important operational lesson:

Before running the observer after exact-ticket evidence stales, refresh the exact-ticket stack with the bar-age operator flag preserved:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

Then run:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1
8. Validation Outputs
8.1 Exact-ticket refresh

The final successful refresh produced PASS for:

Governance
Decision artifact
Pre-action evidence aggregate
Bar-age and exit-condition evidence
Manual approval gate preview
Operator decision v2 preview
Execution readiness dry-run schema preview

Representative passing bar-age evidence:

Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False
8.2 Black-swan guard

Final black-swan guard builder:

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

Final black-swan guard verifier:

H024 read-only black-swan guard records: 1
Violations: 0
Verifier verdict: PASS
Record verdict: PASS
Operator state: BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED
8.3 VPS deployment readiness aggregate

Final readiness builder:

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

Final readiness verifier:

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
8.4 Observer runner

Final runner ended with:

H024 read-only VPS observer run complete.
No trading, broker mutation, order_check, order_send, symbol_select, entry, close/modify, executable trade request, live broker request, or order-capable trading loop was authorized.
8.5 Commit and push

Commit:

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

Final git status:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
9. Failure History And Lessons From This Milestone
9.1 First runner design was too brittle

The first runner tried to discover many possible legacy builder names and rerun more of the historical stack than needed.

Problem:

It failed on missing exact builder names.
It reran governance builders that refreshed runtime reports internally.
It created confusing outputs and instability.

Resolution:

The runner was simplified to refresh only the operational read-only runtime chain, black-swan guard, and VPS readiness aggregate. It consumes exact-ticket stack reports as upstream evidence.

Lesson:

Deployment runner should be operational and predictable. It should not be a legacy-builder search engine.

9.2 PowerShell interpolation bug

Failure:

Variable reference is not valid. ':' was not followed by a valid variable name character.

Cause:

PowerShell parsed $Name: as an invalid scoped variable.

Fix:

Use ${Name}: when interpolating before a colon.

Lesson:

Always use ${Variable} in PowerShell strings when punctuation follows the variable.

9.3 Black-swan guard correctly failed closed on stale exact-ticket evidence

Failure:

Black-swan guard reported stale evidence for:

decision artifact
pre-action evidence aggregate
bar-age evidence
manual approval gate preview
operator decision v2 preview

Cause:

Exact-ticket stack reports were older than the black-swan guard freshness window.

Resolution:

Refresh exact-ticket reports before black-swan guard when needed.

Lesson:

This was correct fail-closed behavior, not a bug.

9.4 Bar-age flag must be preserved through dependent builders

Failure:

Manual approval gate builder internally reran bar-age evidence without --position-open-over-three-bars, causing:

Bar-age classification: INSUFFICIENT_BAR_AGE_EVIDENCE
Verdict: FAIL_CLOSED

Resolution:

Run dependent exact-ticket builders with --position-open-over-three-bars.

Lesson:

Any path that refreshes bar-age-dependent exact-ticket evidence must preserve the operator-reported bar-age flag, or it will fail closed.

9.5 Readiness aggregate was initially over-strict

Initial readiness aggregate problems:

It required older upstream packets to expose newer construction flags:
live_broker_request_constructed
executable_trade_request_constructed
mt5_request_dictionary_constructed

It falsely treated safety check keys such as:

executable_trade_request_absent: True
live_broker_request_absent: True
mt5_request_dictionary_absent: True

as executable request objects.

It looked for the wrong decision artifact report name:
expected wrong: h024_exact_ticket_canary_close_modify_decision_artifact_validator.jsonl
actual report: h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

Fixes:

Missing construction flags in older upstream packets no longer fail readiness by themselves.
Unsafe true/non-false construction flags still fail.
*_absent, *_blocked, *_constructed, and *_authorized safety fields are not treated as request payloads.
The real decision artifact report path is consumed first.

Lesson:

Aggregates must consume real upstream packet shapes robustly without weakening safety semantics.

10. Current Operational Runbook
10.1 Standard read-only VPS observer run

From repo root:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1

Expected result:

H024 read-only VPS observer run complete.
No trading, broker mutation, order_check, order_send, symbol_select, entry, close/modify, executable trade request, live broker request, or order-capable trading loop was authorized.
10.2 Direct readiness verification
python scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass

Expected:

H024 read-only VPS deployment readiness records: 1
Violations: 0
Verifier verdict: PASS
Record verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
10.3 If black-swan guard fails due stale exact-ticket evidence

Refresh exact-ticket stack first:

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars

Then run:

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1
11. Verification Block For The Next AI

The next AI should start with:

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

HEAD is 0792bad or a later handoff commit.
Focused readiness tests pass.
Runtime observer runner completes.
Black-swan guard PASS.
VPS readiness aggregate PASS.
Verifier verdict PASS.
Violations 0.
All action authorization fields false.
symbol_select_authorized false.
vps_deployment_readiness_authorizes_trading false.
Final git status shows only reports/ untracked, unless a new handoff has just been created.

If the runner fails due stale exact-ticket evidence, refresh the exact-ticket stack with --position-open-over-three-bars as shown above.

12. Commit Discipline

For every future milestone:

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

Use Run-Native for native commands.

Never add reports/.

Never commit if the milestone verifier fails under --require-pass.

Expected final status after commit and push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
13. Static Safety Expectations

Known frozen legacy exceptions remain:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

These are historical/pre-gate artifacts only.

For current observer/deployment-readiness code, no new broker mutation call sites are acceptable.

Do not introduce:

order_send
order_check
symbol_select
MetaTrader5 mutation call sites
live close/modify request construction
SL/TP modify requests
close requests
order-capable trading loops

Read-only introspection and JSON/JSONL packet construction are acceptable when fail-closed and non-authorizing.

14. Operator Language To Preserve

Use these interpretations consistently:

PASS = read-only packet is coherent.
PASS != trading authorized.
PASS != close/modify authorized.
PASS != order_check authorized.
PASS != order_send authorized.
PASS != broker mutation authorized.
PASS != live broker request authorized.
VPS observer readiness = okay for read-only observation only.

Preferred wording:

read-only observer
OK but trading not authorized
fail closed
no broker mutation authorized
current state remains blocked
observer workflow authorized for operator review only
black-swan guard clear but trading not authorized
VPS read-only observer readiness coherent

Avoid wording like:

ready to trade
safe to execute
approved to close
approved to modify
can proceed with order
deployment means trading enabled
production trading enabled
15. Deployment Reality Check

The project now has a working read-only VPS observer path.

Current realistic status:

Read-only VPS deployment/monitoring mode is now operationally close.

Live broker-affecting trading is still deliberately not close.

Already implemented:

runtime lockouts
runtime heartbeat
tick/spread supervisor
exposure/inventory supervisor
account risk/margin supervisor
runtime safety aggregate
unified read-only runtime supervision
no-mutation gate
exact-ticket close/modify governance packet
decision artifact packet
pre-action evidence aggregate
bar-age/exit-condition evidence
manual approval gate preview
operator decision v2 preview
execution readiness dry-run schema preview
read-only black-swan guard
read-only VPS deployment readiness aggregate
read-only VPS observer runner

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
16. Recommended Next Deployment-Focused Milestone

Recommended next milestone:

H024 read-only VPS scheduler, healthcheck, and log rotation path

Purpose:

Turn the one-shot read-only VPS observer runner into an operational VPS routine without enabling trading.

This should add:

a read-only scheduler install preview or operator-run installer for Windows Task Scheduler
a read-only scheduler disable/uninstall command
a healthcheck script that summarizes:
last observer run timestamp
latest readiness verdict
latest black-swan verdict
latest heartbeat status
latest no-mutation gate status
whether reports/ is writable
whether expected JSONL reports exist
log output path under an untracked runtime directory, for example logs/ or reports/observer_logs/
log rotation or max-file retention
operator runbook for VPS boot/restart/recovery
fail-closed behavior if latest readiness is stale or missing
no broker mutation
no order_check
no order_send
no symbol_select
no executable trade request
no live broker request
no order-capable trading loop

Suggested files:

scripts/install_h024_read_only_vps_observer_task.ps1
scripts/uninstall_h024_read_only_vps_observer_task.ps1
scripts/check_h024_read_only_vps_observer_health.ps1
docs/operations/H024_READ_ONLY_VPS_SCHEDULER_HEALTHCHECK_RUNBOOK.md
focused tests for any Python health packet if needed

Important:

This should be operational infrastructure, not another abstract governance layer.

17. Suggested Next Prompt

Give the next AI this prompt:

Please read docs/operations/handoffs/HANDOFF_110.md carefully and follow it exactly. It supersedes older handoffs. Continue from the completed H024 read-only VPS deployment readiness aggregate milestone at commit 0792bad. Preserve all hard safety boundaries.

Do not invent another governance-only packet. The next deployment-focused milestone is the H024 read-only VPS scheduler, healthcheck, and log rotation path. Implement practical scripts/runbook to install or preview a Windows Task Scheduler entry for the read-only observer, uninstall/disable it, check observer health, summarize latest readiness/black-swan/heartbeat/no-mutation status, verify report/log paths, and rotate or limit logs. It must remain read-only only: no broker mutation, no order_check, no order_send, no symbol_select, no entries, no close/modify, no executable trade request, no live broker request, and no order-capable trading loop. Keep reports/ untracked. Use focused tests/verifiers, and give concise suggested next prompts after each milestone.
18. Final Reminder

Current H024 posture:

Observe only.
Supervise only.
Run read-only VPS observer only.
Fail closed.
Authorize no trading.
Authorize no close/modify.
Authorize no order_check/order_send.
Authorize no symbol_select.
Authorize no live broker request.
Authorize no executable trade request.
Keep reports/ untracked.

The project has now moved beyond pure governance into operational read-only VPS observer infrastructure.

Next useful work is scheduler/healthcheck/logging for the read-only observer path.

Do not trade.

Do not close or modify.

Do not build a live broker request.

Do not build an executable trade request dictionary.

Do not run an order-capable trading loop.