# HANDOFF_102 — Fully Self-Contained H024 Post-Canary Runtime Safety + No-Mutation Gate Handoff

This handoff is the source of truth for the next AI.

It supersedes HANDOFF_101 and all older handoffs. Do not rely on older handoffs unless explicitly cross-checking repo history. This document is intentionally redundant and self-contained so the next AI does not need to guess where the project stands.

---

## 1. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Preserve every hard safety boundary.
3. Treat all H024 runtime work as read-only unless a future milestone explicitly says otherwise.
4. Never infer that a passing safety packet authorizes trading.
5. Never call broker mutation functions.
6. Never call `order_check`.
7. Never call `order_send`.
8. Never create entries.
9. Never close or modify the current XAUUSDm canary.
10. Never place USDJPY orders.
11. Never run a trading loop.
12. Keep `reports/` untracked.
13. Fail closed on missing, malformed, stale, inconsistent, or unsafe state.
14. Include module, verifier, tests, scripts, and docs for every new milestone.
15. Run focused tests, full suite, packet builder, packet verifier, `git diff --cached --check`, commit, push, and final `git status`.
16. After each milestone, give:
    - concise status summary
    - commit hash
    - final git state
    - one concise suggested next prompt

The user likes concise suggested next prompts after each milestone. Keep doing that.

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

5249ad1 Add H024 runtime no-mutation safety gate

Latest confirmed validation:

Focused no-mutation safety gate tests: 16 passed
Full suite: 1551 passed
No-mutation safety gate packet: PASS
No-mutation safety gate verifier: PASS
Violations: 0
Final git status: clean except untracked reports/

Expected final working tree state:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime/generated output. It must stay untracked.

3. Absolutely Hard Safety Boundary

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
Do not call symbol_select from new safety code.
Do not treat any passing safety packet as permission to trade.
Do not add reports/ to git.

Close/modify is not authorized. It is not “almost authorized.” It is not “safe because the canary is known.” It remains prohibited unless a future exact-ticket governance path is separately specified, reviewed, and still initially read-only.

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

Last confirmed runtime result through the latest unified supervision and no-mutation gate chain:

Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
H024 position count: 1
H024 order count: 0

This observation does not authorize:

close
modify
scale
new entry
USDJPY order
order_check
order_send
trading loop
5. Important Historical Context

This project has progressed through a careful safety-first H024 sequence.

Earlier H024 work included:

broker metadata/readiness packets
dry-run/noop execution contracts
human approval artifacts
one-shot canary readiness and final pre-dispatch audit
one controlled demo canary
read-only post-canary monitoring
lifecycle decision packets
observation analysis
supervisory state packets
USDJPY readiness packet
safety supervisor spec
runtime lockouts
runtime heartbeat
runtime tick/spread
exposure/inventory
account risk/margin
aggregate supervisor
unified post-canary supervision
no-mutation safety gate

The current safety posture is stronger than HANDOFF_101. We now have an explicit no-mutation gate contract requiring future broker-facing code to check the gate while still opening no mutation path today.

6. Current Recent Commit Chain

Recent relevant commits, oldest to newest:

98efc2a Add H024 runtime safety lockout reader
187e9dd Add H024 runtime safety heartbeat packet
abecff8 Add H024 runtime tick and spread safety supervisor
0db61fa Add H024 runtime exposure inventory safety supervisor
1c331c6 Add H024 runtime account risk margin safety supervisor
8e8979c Add H024 runtime safety aggregate supervisor
224371a Add H024 unified read-only runtime supervision
5249ad1 Add H024 runtime no-mutation safety gate

Latest confirmed commit is:

5249ad1 Add H024 runtime no-mutation safety gate
7. Runtime Safety Layer Details
7.1 H024 Runtime Safety Lockout Reader

Commit:

98efc2a Add H024 runtime safety lockout reader

Intent:

Define committed default runtime safety lockout config.
Read local lockout state.
Support:
global no-new-entry
manual override lockout
per-symbol XAUUSD no-new-entry lockout
per-symbol USDJPY no-new-entry lockout
Fail closed on missing/malformed unsafe inputs.

Known operator state when passing:

LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Important semantics:

Even if lockouts are clear, trading is not authorized.

Expected authorizations:

broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False

Key files:

config/h024_runtime_safety/default_lockout_config.json
quantcore/execution/h024_runtime_safety_lockout.py
scripts/build_h024_runtime_safety_lockout_jsonl.py
scripts/verify_h024_runtime_safety_lockout_jsonl.py
tests/test_h024_runtime_safety_lockout.py
7.2 H024 Runtime Safety Heartbeat Packet

Commit:

187e9dd Add H024 runtime safety heartbeat packet

Intent:

Read-only MT5 runtime heartbeat.
Verify MT5 initialization.
Verify account_info() availability.
Verify expected server.
Verify USD account currency.
Verify terminal/account heartbeat freshness where available.
Reference runtime safety lockout reader.
Fail closed on unavailable/inconsistent runtime state.

Expected server:

Exness-MT5Trial6

Expected currency:

USD

Passing operator state:

RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed operator state:

FAIL_CLOSED_RUNTIME_HEARTBEAT_BLOCKED

Allowed reads:

MetaTrader5.initialize()
MetaTrader5.account_info()
MetaTrader5.terminal_info()
MetaTrader5.last_error()
MetaTrader5.version()

Forbidden:

order_check
order_send
entry
close
modify
trading loop
broker mutation

Key files:

quantcore/execution/h024_runtime_safety_heartbeat.py
scripts/build_h024_runtime_safety_heartbeat_jsonl.py
scripts/verify_h024_runtime_safety_heartbeat_jsonl.py
tests/test_h024_runtime_safety_heartbeat.py
docs/operations/H024_RUNTIME_SAFETY_HEARTBEAT_PACKET.md
7.3 H024 Runtime Tick/Spread Safety Supervisor

Commit:

abecff8 Add H024 runtime tick and spread safety supervisor

Intent:

Read-only market-data safety layer.
Consume/reference runtime lockout reader and heartbeat.
Verify XAUUSDm and USDJPYm.
Verify tick availability.
Verify bid/ask sanity.
Verify ask > bid.
Verify positive spread.
Verify spread thresholds.
Verify tick freshness.
Verify symbol visibility/readability without selecting symbols.

Important design decision:

Do not call symbol_select.

If a symbol is not already readable/visible, fail closed.

Runtime symbols:

XAUUSDm -> model symbol XAUUSD
USDJPYm -> model symbol USDJPY

Default threshold intent:

XAUUSDm max spread points: intentionally operational/safety threshold, not alpha edge.
USDJPYm max spread points: operational/safety threshold.
Tick age threshold: fail closed if stale.

Passing operator state:

TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed operator state:

FAIL_CLOSED_TICK_SPREAD_SUPERVISOR_BLOCKED

Key files:

quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py
scripts/build_h024_runtime_tick_spread_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_tick_spread_safety_supervisor_jsonl.py
tests/test_h024_runtime_tick_spread_safety_supervisor.py
docs/operations/H024_RUNTIME_TICK_SPREAD_SAFETY_SUPERVISOR.md

Known passing runtime from prior milestone included:

USDJPYm tick/spread PASS
XAUUSDm tick/spread PASS
small negative tick ages tolerated due to future-tick clock tolerance
7.4 H024 Runtime Exposure/Inventory Safety Supervisor

Commit:

0db61fa Add H024 runtime exposure inventory safety supervisor

Intent:

Read-only inventory supervisor.
Consume/reference lockout, heartbeat, tick/spread.
Inspect MT5 positions/orders without mutation.
Allow only:
no H024 inventory, or
exact known XAUUSDm canary.
Reject:
any H024 USDJPY position
any H024 USDJPY order
any H024 pending/open order
any extra H024 position
any mismatched XAUUSDm canary identity

Known canary allowed fields:

symbol: XAUUSDm
ticket or identifier: 4413054432
magic: 240024
volume: 0.01
type: 1

Known passing result:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
H024 position symbol=XAUUSDm ticket=4413054432 identifier=4413054432 magic=240024 volume=0.01 type=1 verdict=PASS

Flat state is allowed:

Canary state: NOT_OBSERVED
H024 position count: 0
H024 order count: 0

But flat state does not authorize a new entry.

Passing operator state:

EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed operator state:

FAIL_CLOSED_EXPOSURE_INVENTORY_BLOCKED

Key files:

quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py
scripts/build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
tests/test_h024_runtime_exposure_inventory_safety_supervisor.py
docs/operations/H024_RUNTIME_EXPOSURE_INVENTORY_SAFETY_SUPERVISOR.md
7.5 H024 Runtime Account Risk/Margin Safety Supervisor

Commit:

1c331c6 Add H024 runtime account risk margin safety supervisor

Intent:

Read-only account risk/margin supervisor.
Consume/reference lockout, heartbeat, tick/spread, exposure/inventory.
Inspect account_info without mutation.
Verify:
server
USD account context
balance sanity
equity sanity
margin sanity
free margin sanity
margin level sanity where available
floating PnL consistency where available
canary exposure boundedness
Fail closed on margin compression or inconsistent account state.

Known passing runtime result:

Account server: Exness-MT5Trial6
Account currency: USD
Balance: 10000.0
Equity: 9998.75
Profit: -1.25
Margin: 2.36
Free margin: 9996.39
Margin level: 423675.8474576271
Margin used fraction: 0.00023602950368796098
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0

Passing operator state:

ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed operator state:

FAIL_CLOSED_ACCOUNT_RISK_MARGIN_BLOCKED

Key files:

quantcore/execution/h024_runtime_account_risk_margin_safety_supervisor.py
scripts/build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
tests/test_h024_runtime_account_risk_margin_safety_supervisor.py
docs/operations/H024_RUNTIME_ACCOUNT_RISK_MARGIN_SAFETY_SUPERVISOR.md
7.6 H024 Runtime Safety Aggregate Supervisor

Commit:

8e8979c Add H024 runtime safety aggregate supervisor

Intent:

Read-only aggregate supervisor.
Combine all runtime safety packets into one fail-closed operator verdict.
Prevent future code from cherry-picking one passing packet while ignoring another failing packet.
Require every upstream packet to pass.
Verify upstream packet freshness.
Merge embedded violations.
Verify all no-execution authorizations remain false.

Consumes/references:

lockout reader
heartbeat
tick/spread
exposure/inventory
account risk/margin

Known passing aggregate result:

Verdict: PASS
Violations: 0
Operator state: RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
Effective new entries blocked: True
runtime_safety_heartbeat: PASS
runtime_tick_spread_safety_supervisor: PASS
runtime_exposure_inventory_safety_supervisor: PASS
runtime_account_risk_margin_safety_supervisor: PASS
Embedded upstream violations: 0

Passing operator state:

RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED

Fail-closed operator state:

FAIL_CLOSED_RUNTIME_SAFETY_AGGREGATE_BLOCKED

Key files:

quantcore/execution/h024_runtime_safety_aggregate_supervisor.py
scripts/build_h024_runtime_safety_aggregate_supervisor_jsonl.py
scripts/verify_h024_runtime_safety_aggregate_supervisor_jsonl.py
tests/test_h024_runtime_safety_aggregate_supervisor.py
docs/operations/H024_RUNTIME_SAFETY_AGGREGATE_SUPERVISOR.md
7.7 H024 Unified Read-Only Post-Canary Runtime Supervision

Commit:

224371a Add H024 unified read-only runtime supervision

Intent:

Operator-facing wrapper.
Combine:
existing one-shot canary read-only supervision runner
runtime safety aggregate supervisor
Produce one JSONL packet for operator review.
Report:
canary lifecycle/supervision state
runtime aggregate state
upstream packet summaries
exact known canary identity if observed
a single fail-closed operator next action

Known passing result:

Verdict: PASS
Violations: 0
Operator state: UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
Canary supervision records: 1
Canary supervision all records passed: True
Canary operator next action: read_supervisory_state_and_continue_observation
Runtime aggregate verdict: PASS
Runtime aggregate operator state: RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True

Passing operator next action:

READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED

Fail-closed operator next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Key files:

quantcore/execution/h024_unified_read_only_post_canary_runtime_supervision.py
scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
scripts/verify_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
tests/test_h024_unified_read_only_post_canary_runtime_supervision.py
docs/operations/H024_UNIFIED_READ_ONLY_POST_CANARY_RUNTIME_SUPERVISION.md
7.8 H024 Runtime No-Mutation Safety Gate Contract

Commit:

5249ad1 Add H024 runtime no-mutation safety gate

Intent:

Read-only no-mutation gate contract.
Consume/reference unified read-only post-canary runtime supervision.
Define the mandatory fail-closed gate interface future broker-facing code must check.
Prove the current state still blocks:
broker mutation
entries
close/modify
order_check
order_send
XAUUSD order
USDJPY order
trading loop
automatic execution
Reject missing/malformed/untrusted unified supervision.
Include static tests showing current non-exempt execution-related code has no direct broker mutation call sites.

Known passing result:

Verdict: PASS
Violations: 0
Operator state: NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED
Operator next action: KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION
Unified supervision verdict: PASS
Unified operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
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

Passing operator state:

NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED

Passing operator next action:

KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION

Fail-closed operator state:

FAIL_CLOSED_NO_MUTATION_GATE_CONTRACT_BLOCKED

Fail-closed next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Frozen legacy exceptions documented:

historical one-shot canary send path
historical MT5 terminal preflight helper that may call symbol_select

These are not authorized by the gate. They are frozen historical/pre-gate artifacts only.

Key files:

quantcore/execution/h024_runtime_no_mutation_safety_gate.py
scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py
scripts/verify_h024_runtime_no_mutation_safety_gate_jsonl.py
tests/test_h024_runtime_no_mutation_safety_gate.py
docs/operations/H024_RUNTIME_NO_MUTATION_SAFETY_GATE.md
8. Existing Canary Read-Only Supervision Runner

Existing read-only runner:

scripts/run_h024_one_shot_demo_canary_read_only_supervision.py

Verifier:

scripts/verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py

Report path:

reports/h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl

Known passing output:

Verdict: PASS
Violations: 0
Completed stages: 8 / 8
First failed stage: None
Operator next action: read_supervisory_state_and_continue_observation
Broker mutation authorized: False
Trading loop authorized: False
USDJPY separate readiness required: True
Kill switches required before trading loop: True
Black-swan guards required before trading loop: True

This runner is read-only and does not authorize:

entries
close/modify
order_check
order_send
trading loop
9. Latest Verification Commands

A new AI should ask the user to run this block first:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

git status
git log --oneline -25

python -m pytest tests\test_h024_runtime_no_mutation_safety_gate.py
python -m pytest

python scripts\build_h024_runtime_no_mutation_safety_gate_jsonl.py
python scripts\verify_h024_runtime_no_mutation_safety_gate_jsonl.py reports\h024_runtime_no_mutation_safety_gate.jsonl --require-pass

Expected:

Focused tests: 16 passed
Full suite: 1551 passed
No-mutation gate packet: PASS
No-mutation gate verifier: PASS
Violations: 0
Final git status: only reports/ untracked

If this does not pass, stop and diagnose. Do not implement the next milestone on an unverified base.

10. Core Implementation Pattern For Future Milestones

Every new H024 runtime safety milestone should include:

1. quantcore/execution/<module>.py
2. scripts/build_<packet>_jsonl.py
3. scripts/verify_<packet>_jsonl.py
4. tests/test_<packet>.py
5. docs/operations/<PACKET_DOC>.md

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
operator_next_action when applicable
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
require-pass with record verdict not PASS

Tests should include:

passing happy path
missing input fails closed
malformed input fails closed
wrong strategy or packet type fails closed
unsafe authorization true fails verifier
missing authorization fails verifier
embedded violations fail verifier
require-pass rejects fail-closed record
static no-mutation checks when relevant
11. Commit Discipline

For every milestone:

git status

python -m pytest <focused test file>
python -m pytest

python <build script>
python <verify script> <report path> --require-pass

git status
git add -- <only intended tracked files>
git diff --cached --check
git commit -m "<clear commit message>"
git push
git status

Never add reports/.

Expected final status after commit and push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
12. The Recommended Next Milestone

Next milestone should be:

H024 exact-ticket canary close/modify governance specification packet

This must be read-only only.

It must not:

close the canary
modify the canary
build a live broker request
call order_check
call order_send
call close/modify helpers
call symbol_select
mutate MT5 state
run a trading loop

Purpose:

Define the governance requirements that would be necessary before any future close/modify could even be considered for the exact known XAUUSDm canary ticket/identifier 4413054432.

The governance packet should require:

1. Exact ticket/identifier lock:
   - ticket or identifier must be 4413054432

2. Exact canary identity:
   - symbol XAUUSDm
   - model symbol XAUUSD
   - side sell
   - type 1
   - volume 0.01
   - magic 240024

3. Runtime no-mutation safety gate PASS:
   - gate must be trusted
   - gate must still block all mutation
   - gate must not open any mutation path

4. No USDJPY H024 exposure/order:
   - no USDJPYm position/order with H024 magic/comment/identity

5. No additional H024 exposure/order:
   - no additional H024 XAUUSDm position
   - no H024 pending/open order

6. Explicit human decision artifact:
   - separate artifact must exist
   - decision must be explicit
   - stale/missing/malformed decision fails closed
   - this milestone should define schema, not approve action by default

7. Pre-close risk snapshot:
   - account risk/margin snapshot
   - exposure/inventory snapshot
   - tick/spread snapshot
   - fail closed on missing/malformed/stale snapshot

8. No current authorization:
   - broker mutation false
   - order_check false
   - order_send false
   - entry false
   - close_modify false
   - xauusd_order false
   - usdjpy_order false
   - trading_loop false
   - automatic_execution false

Suggested module name:

quantcore/execution/h024_exact_ticket_canary_close_modify_governance.py

Suggested scripts:

scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py

Suggested tests:

tests/test_h024_exact_ticket_canary_close_modify_governance.py

Suggested docs:

docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE.md

Suggested report path:

reports/h024_exact_ticket_canary_close_modify_governance.jsonl

Suggested commit message:

Add H024 exact-ticket canary close modify governance spec

Suggested next prompt:

Let’s implement the H024 exact-ticket canary close/modify governance specification packet. It should be read-only only and must not close or modify anything. It should define the separate governance requirements needed before any future close/modify can even be considered for the exact known XAUUSDm canary ticket/identifier 4413054432. It must require exact-ticket locking, current canary identity match, no USDJPY exposure/order, no additional H024 exposure/order, runtime no-mutation gate PASS, explicit human decision artifact, pre-close risk snapshot, and fail-closed behavior. It must authorize no broker mutation, no order_check, no order_send, no entries, no close/modify, no USDJPY order, and no trading loop. Include module, verifier, tests, scripts, and docs. Keep reports/ untracked.
13. Explicit Next-Milestone Failure Modes

The exact-ticket canary close/modify governance packet must fail closed if:

runtime no-mutation safety gate missing
runtime no-mutation safety gate malformed
runtime no-mutation safety gate not PASS
runtime no-mutation safety gate opens mutation path
unified supervision missing
unified supervision not PASS
canary not exact ticket/identifier 4413054432 when observed
canary magic mismatch
canary volume mismatch
canary symbol mismatch
canary type/side mismatch
USDJPY H024 exposure present
USDJPY H024 order present
additional H024 XAUUSDm position present
any H024 pending/open order present
human decision artifact missing
human decision artifact malformed
human decision artifact stale
human decision artifact ambiguous
pre-close risk snapshot missing
pre-close risk snapshot malformed
pre-close risk snapshot stale
any authorization true
effective_new_entries_blocked not true

It must pass only as a read-only governance specification packet. A PASS should mean:

governance specification state is coherent
all close/modify paths remain blocked
no action is authorized

It must not mean:

close is authorized
modify is authorized
order_check is authorized
order_send is authorized
14. Static Safety Expectations

The latest no-mutation gate has static checks for direct broker mutation call sites in current non-exempt execution-related code.

Known frozen legacy exceptions:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

Interpretation:

These are frozen legacy/pre-gate artifacts.
They are not authorized by the no-mutation gate.
They must not be treated as current execution adapters.
Do not add new exceptions casually.
If a future exception is proposed, fail closed and require explicit documentation.
15. Operator Language To Preserve

Use these interpretations consistently:

PASS = read-only safety/governance packet is coherent
PASS != trading authorized
PASS != close/modify authorized
PASS != order_check authorized
PASS != order_send authorized

Preferred wording:

"OK but trading not authorized"
"fail closed"
"read-only observation"
"operator review required"
"no broker mutation authorized"
"current state remains blocked"

Avoid wording like:

"ready to trade"
"safe to execute"
"approved to close"
"approved to modify"
"can proceed with order"
16. If Something Fails

If tests or verifier fail:

Do not continue to commit.
Diagnose exact failure.
Patch narrowly.
Rerun focused tests.
Rerun full suite.
Rerun builder/verifier.
Commit only after clean validation.

If live/runtime data changes, such as:

canary absent
canary PnL changed
tick age changed
spread changed
margin changed

Do not assume failure is bad. Read the verifier semantics. Flat inventory may be allowed by some packets, but no packet authorizes a new entry.

17. How The Next AI Should Start

The next AI should respond:

Understood. Continuing from HANDOFF_102 at commit 5249ad1. Current state is read-only H024 post-canary runtime supervision with a no-mutation safety gate; all broker mutation and trading paths remain blocked. Please run the verification block from the handoff so I can confirm local state before the next read-only milestone.

Then provide the verification block from Section 9.

18. Final Reminder

This handoff is deliberately conservative.

Current H024 posture:

Observe only.
Supervise only.
Fail closed.
Authorize nothing.
Keep reports/ untracked.