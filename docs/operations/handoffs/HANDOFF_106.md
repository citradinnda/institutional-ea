# HANDOFF_106 — Fully Self-Contained H024 Bar-Age Evidence Milestone Handoff

This handoff is the source of truth for the next AI.

It supersedes HANDOFF_105 and all older handoffs. It preserves every hard safety boundary and captures the completed H024 exact-ticket canary close/modify read-only bar-age and exit-condition evidence supervisor milestone.

This document is intentionally redundant and self-contained so the next AI does not need to guess repo state, validation state, safety posture, runtime posture, implementation files, failure history, or the next recommended milestone.

---

## 1. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Preserve every hard safety boundary.
3. Treat all H024 runtime/governance/decision/evidence work as read-only unless a future milestone explicitly says otherwise.
4. Never infer that a passing safety/governance/decision/evidence packet authorizes trading.
5. Never call broker mutation functions.
6. Never call `order_check`.
7. Never call `order_send`.
8. Never create entries.
9. Never close or modify the current XAUUSDm canary.
10. Never place USDJPY orders.
11. Never run a trading loop.
12. Never call `symbol_select` from new safety/governance/evidence code.
13. Never build a live broker request from governance, decision, or evidence packets.
14. Keep `reports/` untracked.
15. Fail closed on missing, malformed, stale, inconsistent, ambiguous, or unsafe state.
16. Include module, verifier, tests, scripts, and docs for every new milestone.
17. Prefer focused tests and packet builder/verifier during iteration. Run full suite once before a major push when practical.
18. After each milestone, give:
    - concise status summary
    - commit hash
    - final git state
    - one concise suggested next prompt

The user likes concise suggested next prompts after each milestone. Keep doing that.

The user is fatigued by long loops and repeated full-suite runs. Do not make them run thousands of tests during every micro-fix. Use focused tests and builder/verifier during iteration, then run full suite only at the end or when explicitly needed.

---

## 2. Repo State At This Handoff

Project:

```text
institutional-ea

Local repo path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Remote:

origin/main

Latest confirmed pushed commit:

8065262 Add H024 exact-ticket close modify bar-age exit-condition evidence

Latest confirmed implementation milestone:

8065262 Add H024 exact-ticket close modify bar-age exit-condition evidence

Expected final git status after commit 8065262:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime/generated output. It must stay untracked.

3. Hard Safety Boundary

The current H024 state is post-canary, read-only, no-mutation.

Do not do any of these:

Do not create a second H024 entry.
Do not place a live order.
Do not place a demo order.
Do not place a USDJPY order.
Do not scale the existing XAUUSDm canary.
Do not call order_check.
Do not call order_send.
Do not close the XAUUSDm canary.
Do not modify the XAUUSDm canary.
Do not modify SL/TP.
Do not run a trading loop.
Do not mutate broker/account/symbol state.
Do not call symbol_select from new safety/governance/decision/evidence code.
Do not build a live broker request from governance, decision, or evidence artifacts.
Do not treat any passing safety/governance/decision/evidence packet as permission to trade.
Do not add reports/ to git.

Close/modify is not authorized. It is not almost authorized. It is not safe because the canary is known. It remains prohibited unless a future exact-ticket governance path is separately specified, reviewed, and still initially read-only.

A PASS means the relevant packet is coherent and all action paths remain blocked.

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

Latest validated runtime/bar-age state from the final HANDOFF_106 milestone log:

Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
H024 position count: 1
H024 order count: 0
H024 position symbol=XAUUSDm ticket=4413054432 identifier=4413054432 magic=240024 volume=0.01 type=1 verdict=PASS

Latest pasted runtime account snapshot during the milestone:

Balance: 10000.0
Equity: 10024.32
Profit: 24.32
Margin: 2.36
Free margin: 10021.96
Margin level: 424759.3220338983
Margin used fraction: 0.00023542744046478964

The position being open over three bars is currently classified as:

OPERATOR_REPORTED_ONLY

This is non-authorizing context only.

It does not authorize:

close
modify
scale
new entry
USDJPY order
order_check
order_send
trading loop
broker request construction
5. Recent Commit Chain

Recent relevant commits, oldest to newest:

98efc2a Add H024 runtime safety lockout reader
187e9dd Add H024 runtime safety heartbeat packet
abecff8 Add H024 runtime tick and spread safety supervisor
0db61fa Add H024 runtime exposure inventory safety supervisor
1c331c6 Add H024 runtime account risk margin safety supervisor
8e8979c Add H024 runtime safety aggregate supervisor
224371a Add H024 unified read-only runtime supervision
5249ad1 Add H024 runtime no-mutation safety gate
69b3028 Add handoff document #102
94d3b96 Add H024 exact-ticket canary close modify governance spec
b82d48c Fix H024 exact-ticket governance canary state evidence
477c7ee Add handoff document #103
9f061c1 Add H024 exact-ticket close modify decision artifact validator
7c2c13f Add handoff document #104
86774c4 Add H024 exact-ticket close modify pre-action evidence aggregate
10b4a14 Fix H024 pre-action evidence aggregate identity validation
e370a60 Fix H024 pre-action aggregate upstream validation path
ee783d4 Add handoff document #105
8065262 Add H024 exact-ticket close modify bar-age exit-condition evidence

Latest confirmed implementation milestone:

8065262 Add H024 exact-ticket close modify bar-age exit-condition evidence
6. Existing H024 Runtime Safety Layer Summary
6.1 Runtime Safety Lockout Reader

Commit:

98efc2a Add H024 runtime safety lockout reader

Purpose:

Read committed default safety config and local lockout state. Supports global no-new-entry, manual override lockout, and per-symbol XAUUSD/USDJPY no-new-entry lockouts.

Passing operator state:

LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Key files:

config/h024_runtime_safety/default_lockout_config.json
quantcore/execution/h024_runtime_safety_lockout.py
scripts/build_h024_runtime_safety_lockout_jsonl.py
scripts/verify_h024_runtime_safety_lockout_jsonl.py
tests/test_h024_runtime_safety_lockout.py
6.2 Runtime Safety Heartbeat Packet

Commit:

187e9dd Add H024 runtime safety heartbeat packet

Purpose:

Read-only MT5 runtime heartbeat. Verifies MT5 initialization, account availability, expected server, USD account currency, and terminal/account heartbeat freshness where available.

Passing operator state:

RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED

Expected server:

Exness-MT5Trial6

Expected currency:

USD
6.3 Runtime Tick/Spread Safety Supervisor

Commit:

abecff8 Add H024 runtime tick and spread safety supervisor

Purpose:

Read-only market-data supervisor. Verifies XAUUSDm and USDJPYm tick availability, bid/ask sanity, ask > bid, positive spread, spread thresholds, tick freshness, and symbol visibility/readability without selecting symbols.

Important:

Do not call symbol_select.

Passing operator state:

TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED
6.4 Runtime Exposure/Inventory Safety Supervisor

Commit:

0db61fa Add H024 runtime exposure inventory safety supervisor

Purpose:

Read-only inventory supervisor. Allows only no H024 inventory or the exact known XAUUSDm canary. Rejects H024 USDJPY position/order, H024 pending/open order, extra H024 position, and mismatched XAUUSDm canary identity.

Known canary allowed fields:

symbol: XAUUSDm
ticket or identifier: 4413054432
magic: 240024
volume: 0.01
type: 1

Passing operator state:

EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED
6.5 Runtime Account Risk/Margin Safety Supervisor

Commit:

1c331c6 Add H024 runtime account risk margin safety supervisor

Purpose:

Read-only account risk/margin supervisor. Verifies server, USD account context, balance sanity, equity sanity, margin sanity, free margin sanity, margin level sanity where available, floating PnL consistency where available, and canary exposure boundedness.

Passing operator state:

ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED
6.6 Runtime Safety Aggregate Supervisor

Commit:

8e8979c Add H024 runtime safety aggregate supervisor

Purpose:

Aggregates all runtime safety packets into one fail-closed operator verdict. Prevents cherry-picking one passing packet while ignoring failing upstream evidence.

Passing operator state:

RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
6.7 Unified Read-Only Post-Canary Runtime Supervision

Commit:

224371a Add H024 unified read-only runtime supervision

Purpose:

Operator-facing wrapper combining one-shot canary read-only supervision and runtime safety aggregate supervisor.

Passing operator state:

UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED

Operator next action:

READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
6.8 Runtime No-Mutation Safety Gate Contract

Commit:

5249ad1 Add H024 runtime no-mutation safety gate

Purpose:

Read-only no-mutation gate contract. Future broker-facing code must check this gate. The gate proves current state blocks broker mutation, entries, close/modify, order_check, order_send, XAUUSD order, USDJPY order, trading loop, and automatic execution.

Passing operator state:

NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED

Important frozen legacy exceptions:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

These are historical/pre-gate artifacts only. They are not current authorization.

7. Exact-Ticket Close/Modify Governance, Decision, And Evidence Layers
7.1 Exact-Ticket Close/Modify Governance Specification Packet

Original commit:

94d3b96 Add H024 exact-ticket canary close modify governance spec

Follow-up fix:

b82d48c Fix H024 exact-ticket governance canary state evidence

Purpose:

Defines read-only governance requirements that must be coherent before any future exact-ticket canary close/modify could even be considered.

It does not authorize close/modify.

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED

Operator next action:

KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW

Key files:

config/h024_runtime_safety/default_exact_ticket_canary_close_modify_governance_decision.json
quantcore/execution/h024_exact_ticket_canary_close_modify_governance.py
scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_governance.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE.md
7.2 Exact-Ticket Close/Modify Decision Artifact Validator

Commit:

9f061c1 Add H024 exact-ticket close modify decision artifact validator

Purpose:

Validates explicit human/operator decision artifact schema for exact-ticket close/modify governance while still authorizing no action.

Default decision status:

NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY

Default requested action:

NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED

Key files:

config/h024_runtime_safety/default_exact_ticket_canary_close_modify_decision_artifact.json
quantcore/execution/h024_exact_ticket_canary_close_modify_decision_artifact.py
scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_decision_artifact.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT.md
7.3 Exact-Ticket Close/Modify Pre-Action Evidence Aggregate

Initial implementation:

86774c4 Add H024 exact-ticket close modify pre-action evidence aggregate

Intermediate fix:

10b4a14 Fix H024 pre-action evidence aggregate identity validation

Final validated fix:

e370a60 Fix H024 pre-action aggregate upstream validation path

Purpose:

Read-only aggregate packet that consumes and cross-checks:

runtime no-mutation safety gate
unified read-only post-canary runtime supervision
exact-ticket close/modify governance packet
exact-ticket decision artifact validator packet
fresh runtime account risk/margin, exposure/inventory, and tick/spread evidence

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED

Key files:

quantcore/execution/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.py
scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE.md
8. Milestone Completed In HANDOFF_106
H024 Exact-Ticket Canary Close/Modify Read-Only Bar-Age And Exit-Condition Evidence Supervisor

Commit:

8065262 Add H024 exact-ticket close modify bar-age exit-condition evidence

Purpose:

Convert the operator statement that the exact XAUUSDm canary has been open for over three bars into a structured, read-only evidence packet while still authorizing no action.

The packet consumes/references:

runtime no-mutation safety gate
unified read-only post-canary runtime supervision
exact-ticket close/modify governance packet
exact-ticket decision artifact validator packet
pre-action evidence aggregate packet
runtime exposure/inventory safety supervisor
runtime account risk/margin safety supervisor
runtime tick/spread safety supervisor

It validates/classifies:

exact ticket/identifier 4413054432
exact XAUUSDm canary identity
position still observed
whether over-three-bars is machine-validated or operator-reported only
current read-only risk/equity/PnL/margin snapshot
current spread/tick freshness snapshot
no extra H024 exposure/order
no H024 USDJPY exposure/order
all action authorizations remain false

Current passing bar-age classification:

OPERATOR_REPORTED_ONLY

This means the user/operator reported the exact canary is open over three bars. It is not machine-validated bar age.

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED

Passing operator next action:

KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_BAR_AGE_EXIT_CONDITION_EVIDENCE_REVIEW

Fail-closed operator state:

FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_BLOCKED

Fail-closed operator next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Key files added:

quantcore/execution/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.py
scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE.md

Report path:

reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl

Important implementation notes:

The packet is read-only.
It imports no MT5 broker mutation logic.
It must not call order_check.
It must not call order_send.
It must not call symbol_select.
It must not build a broker request.
It must not close/modify the canary.
It must not run a trading loop.
It fails closed on missing/stale/malformed/upstream-unsafe evidence.
It treats checks.* metadata carefully:
checks.* passed: true audit wrappers are not effective authorization fields.
checks.* passed: false for blocked invariants fails closed.
effective top-level authorization fields remain strictly enforced.
9. HANDOFF_106 Failure History And Lessons

The bar-age milestone had several frustrating intermediate failures. This history matters because the next AI should not repeat the same mistakes.

9.1 Initial Builder Failure

Initial new packet tests passed and full suite passed, but the bar-age builder returned:

Verdict: FAIL_CLOSED
Violations: 2
decision_artifact: unsafe upstream authorization state
pre_action_evidence_aggregate: unsafe upstream authorization state

Root cause:

The new supervisor recursively scanned checks.effective_new_entries_blocked audit metadata and treated check objects as effective authorization fields.

Example problematic shape:

checks.effective_new_entries_blocked expected true got {'detail': 'effective_new_entries_blocked must be true', 'passed': True}

This was not actually unsafe. It was a passed audit check object.

9.2 PowerShell Heredoc Mistake

One patch block used Bash-style syntax:

python - <<'PY'

This caused PowerShell parser errors.

Do not use Bash heredocs in Windows PowerShell. Use a temporary .py file with Set-Content instead.

9.3 Blind Patch Loop Problem

Several wrapper failures looked identical because Invoke-Checked always printed the same command-failed wrapper message. The real failure was hidden inside the generated JSONL record.

When a builder fails, inspect:

python -c "import json, pathlib; p=pathlib.Path('reports/<packet>.jsonl'); r=json.loads(p.read_text(encoding='utf-8-sig').strip()); print(r.get('verdict')); print(r.get('violations'))"

Do not blindly patch based on the wrapper error.

9.4 Stale Upstream Failure

After parser fixes, the bar-age packet failed closed with 8 violations because upstream reports were stale:

upstream evidence is missing, stale, or future-skewed

The upstream ages were around 778-793 seconds, while the packet requires freshness around 300 seconds.

Fix:

Refresh upstream reports immediately before building the bar-age packet.

9.5 Final Passing State

After refreshing upstream reports, the final bar-age packet passed:

Wrote reports\h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_BAR_AGE_EXIT_CONDITION_EVIDENCE_REVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False
Effective new entries blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False

Verifier also passed:

H024 exact-ticket canary close/modify bar-age exit-condition evidence records: 1
Violations: 0
Record verdict: PASS
Verifier verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_BAR_AGE_EXIT_CONDITION_EVIDENCE_REVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
Effective new entries blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False

Commit/push:

[main 8065262] Add H024 exact-ticket close modify bar-age exit-condition evidence
 5 files changed, 1676 insertions(+)
 create mode 100644 docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE.md
 create mode 100644 quantcore/execution/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.py
 create mode 100644 scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py
 create mode 100644 scripts/verify_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py
 create mode 100644 tests/test_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.py

To https://github.com/citradinnda/institutional-ea.git
   ee783d4..8065262  main -> main

Final status:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
10. Validation Status At HANDOFF_106

Confirmed in final pasted logs before commit:

Upstream no-mutation gate
Verdict: PASS
Violations: 0
Operator state: NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED
Gate opens mutation path: False
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
Exact-ticket governance
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
H024 position count: 1
H024 order count: 0
Exact-ticket decision artifact
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
Decision status: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Requested action: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Exact ticket: 4413054432
Exact identifier: 4413054432
Pre-action evidence aggregate
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
User reported position open over three bars: True
Bar-age and exit-condition evidence
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_BAR_AGE_EXIT_CONDITION_EVIDENCE_REVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False
Effective new entries blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
Test status caveat

During the milestone:

The initial new focused test run passed with 19 tests.
A later focused run after adding wrapper tests showed 22 tests passing.
A full suite run earlier in the milestone showed 1658 tests passing.
A synthetic test failed after one intermediate patch because the patch skipped failed checks.* metadata too broadly.
The implementation was then patched to distinguish passed audit wrappers from failed check wrappers.
The final pasted validation before commit confirms packet builder/verifier PASS and upstream packet builder/verifier PASS.
The final pasted validation does not include a final full-suite rerun after the last tiny parser patch.
Next AI should verify with focused test and, if practical, full suite before the next major milestone.

This caveat is intentional and honest. Do not pretend a final full-suite run happened after the last patch unless the user provides it.

11. Verification Block For The Next AI

The next AI should start by asking the user to run this block:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

git status
git log --oneline -15

python -m pytest tests\test_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.py

python scripts\build_h024_runtime_no_mutation_safety_gate_jsonl.py
python scripts\verify_h024_runtime_no_mutation_safety_gate_jsonl.py reports\h024_runtime_no_mutation_safety_gate.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py reports\h024_exact_ticket_canary_close_modify_governance.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\verify_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py reports\h024_exact_ticket_canary_close_modify_decision_artifact.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\verify_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py reports\h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
python scripts\verify_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py reports\h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl --require-pass

git status

Expected:

Focused bar-age tests pass.
No-mutation gate PASS.
Exact-ticket governance PASS.
Decision artifact PASS.
Pre-action evidence aggregate PASS.
Bar-age exit-condition evidence PASS.
Violations: 0.
All authorizations false.
Final git status shows only reports/ untracked.

If upstream evidence is stale, refresh upstream packets immediately before building dependent packets. Staleness is expected fail-closed behavior and not necessarily a code bug.

12. Core Implementation Pattern For Future Milestones

Every new H024 runtime/governance/decision/evidence milestone should include:

quantcore/execution/<module>.py
scripts/build_<packet>_jsonl.py
scripts/verify_<packet>_jsonl.py
tests/test_<packet>.py
docs/operations/<PACKET_DOC>.md

Every packet should include:

schema_version
strategy = H024
packet_type
observed_at_utc
expected
observed or upstream records
checks
authorizations
effective_new_entries_blocked = True
broker_mutation_authorized = False
order_check_authorized = False
order_send_authorized = False
entry_authorized = False
close_modify_authorized = False
xauusd_order_authorized = False
usdjpy_order_authorized = False
trading_loop_authorized = False
automatic_execution_authorized = False
operator_state
operator_next_action
violations
verdict

Verifier should fail closed on:

missing records
malformed JSONL
wrong schema version
wrong strategy
wrong packet type
missing/malformed upstream
unexpected PASS with embedded violations
any authorization not false
effective_new_entries_blocked not true
--require-pass with record verdict not PASS

Tests should include:

passing happy path
missing input fails closed
malformed input fails closed
wrong strategy or packet type fails closed
unsafe authorization true fails verifier
missing authorization fails verifier
embedded violations fail verifier
--require-pass rejects fail-closed record
static no-mutation checks when relevant
real upstream packet shape regressions when consuming generated packets
13. Commit Discipline

For every milestone:

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

For major milestones, run:

python -m pytest

But do not make the user rerun the full suite after every tiny patch. This caused fatigue during HANDOFF_106. Use focused tests and packet verifiers for iteration.

Never add reports/.

Never commit if the milestone verifier fails under --require-pass.

Expected final status after commit and push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
14. Static Safety Expectations

Known frozen legacy exceptions:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

These are frozen legacy/pre-gate artifacts. They are not authorized by the no-mutation gate.

For decision/governance/evidence code specifically, no new broker mutation call sites are acceptable.

Do not introduce:

order_send
order_check
symbol_select
trade request construction for live close/modify
SL/TP modify requests
close requests
trading loops

Read-only introspection and JSON/JSONL packet construction are acceptable when fail-closed and non-authorizing.

15. Operator Language To Preserve

Use these interpretations consistently:

PASS = read-only safety/governance/decision/evidence packet is coherent
PASS != trading authorized
PASS != close/modify authorized
PASS != order_check authorized
PASS != order_send authorized
PASS != broker mutation authorized
PASS != live broker request authorized

Preferred wording:

OK but trading not authorized
OK but action not authorized
fail closed
read-only observation
operator review required
no broker mutation authorized
current state remains blocked
action not authorized

Avoid wording like:

ready to trade
safe to execute
approved to close
approved to modify
can proceed with order
close approved
modify approved
ready for broker request
16. Recommended Next Milestone

The user is tired of slow evidence-only progress. Do not suggest another vague evidence layer.

Recommended next milestone:

H024 exact-ticket manual close/modify approval gate preview

This should still be read-only first.

Purpose:

Define the exact final manual approval gate preview for closing or modifying only the known XAUUSDm canary ticket/identifier 4413054432, without authorizing or executing action yet.

It should consume:

runtime no-mutation safety gate
unified runtime supervision
exact-ticket close/modify governance packet
exact-ticket decision artifact validator
pre-action evidence aggregate
bar-age and exit-condition evidence packet
runtime exposure/inventory
runtime account risk/margin
runtime tick/spread

It should produce:

exact-ticket manual close/modify approval preview packet
explicit operator approval schema preview
explicit non-ambiguous action intent fields
exact canary identity lock
current PnL/risk/spread snapshot
dry-run request-shape preview only if read-only and non-authorizing
final authorizations all false
broker mutation blocked
order_check blocked
order_send blocked
no entry
no close/modify
no trading loop

It must fail closed on:

missing/stale/malformed upstream packets
any upstream not PASS
any upstream embedded violation
any action authorization true
exact ticket mismatch
exact identifier mismatch
exact canary not observed
H024 USDJPY exposure/order
extra H024 exposure/order
ambiguous operator intent
stale operator decision
machine/bar-age mismatch if claimed
request-shape implying execution authorization
any live broker request construction

Passing state should mean:

manual approval gate preview is coherent for read-only operator review
all action paths remain blocked
no broker mutation is authorized

Passing state must not mean:

close is authorized
modify is authorized
order_check is authorized
order_send is authorized
broker request construction is authorized

Suggested module name:

quantcore/execution/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.py

Suggested scripts:

scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py

Suggested tests:

tests/test_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.py

Suggested docs:

docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW.md

Suggested report path:

reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl

Suggested commit message:

Add H024 exact-ticket close modify manual approval gate preview
17. Suggested Next Prompt

Give the next AI this prompt:

Please read docs/operations/handoffs/HANDOFF_106.md carefully and follow it exactly. It is fully self-contained and supersedes older handoffs. Continue from there, preserve all hard safety boundaries, and keep giving me concise suggested next prompts after each milestone.

First verify the local base state from HANDOFF_106. Then implement the H024 exact-ticket canary close/modify read-only manual approval gate preview. It must consume the no-mutation gate, unified runtime supervision, exact-ticket close/modify governance packet, exact-ticket decision artifact validator, pre-action evidence aggregate, bar-age and exit-condition evidence packet, runtime exposure/inventory, runtime account risk/margin, and runtime tick/spread evidence. It must preserve exact ticket/identifier 4413054432 and exact XAUUSDm canary identity, include current read-only PnL/risk/spread evidence, define a strict explicit operator approval preview schema, and fail closed on missing, malformed, stale, ambiguous, inconsistent, or unsafe evidence. It must not build a live broker request, must not call order_check, must not call order_send, must not close or modify the canary, must not place entries, must not place XAUUSD or USDJPY orders, must not call symbol_select, must not mutate broker state, and must not run a trading loop. Include module, verifier, tests, scripts, and docs. Keep reports/ untracked. Use focused tests and packet verifiers during iteration, and do not make me run the full suite after every tiny patch.
18. How The Next AI Should Start

The next AI should respond:

Understood. Continuing from HANDOFF_106 at validated implementation commit 8065262. Current state is read-only H024 post-canary runtime supervision with a no-mutation gate, exact-ticket close/modify governance specification packet, exact-ticket close/modify decision artifact validator, pre-action evidence aggregate, and bar-age/exit-condition evidence packet. All broker mutation and trading paths remain blocked. Please run the HANDOFF_106 verification block so I can confirm local state before the manual approval gate preview milestone.

Then provide the verification block from Section 11.

19. Final Reminder

Current H024 posture:

Observe only.
Supervise only.
Specify governance only.
Validate decision artifacts only.
Aggregate read-only pre-action evidence only.
Classify bar-age / exit-condition evidence only.
Fail closed.
Authorize nothing.
Keep reports/ untracked.

The user wants real deployment progress. The next milestone should be a read-only manual approval gate preview, not another generic evidence packet.

