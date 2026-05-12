# HANDOFF_103 — Fully Self-Contained H024 Exact-Ticket Canary Close/Modify Governance Spec Handoff

This handoff is the source of truth for the next AI.

It supersedes HANDOFF_102 and all older handoffs. It preserves the same hard safety posture and adds the completed H024 exact-ticket canary close/modify governance specification packet.

This document is deliberately redundant and self-contained so the next AI does not need to guess repo state, validation state, safety posture, or the next milestone.

---

## 1. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Preserve every hard safety boundary.
3. Treat all H024 runtime/governance work as read-only unless a future milestone explicitly says otherwise.
4. Never infer that a passing safety/governance packet authorizes trading.
5. Never call broker mutation functions.
6. Never call `order_check`.
7. Never call `order_send`.
8. Never create entries.
9. Never close or modify the current XAUUSDm canary.
10. Never place USDJPY orders.
11. Never run a trading loop.
12. Never call `symbol_select` from new safety/governance code.
13. Keep `reports/` untracked.
14. Fail closed on missing, malformed, stale, inconsistent, ambiguous, or unsafe state.
15. Include module, verifier, tests, scripts, and docs for every new milestone.
16. Run focused tests, full suite, packet builder, packet verifier, `git diff --cached --check`, commit, push, and final `git status`.
17. After each milestone, give:
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
```

Local repo path:

```text
C:\Users\equin\Documents\institutional-ea
```

Branch:

```text
main
```

Remote:

```text
origin/main
```

Latest confirmed pushed commit:

```text
b82d48c Fix H024 exact-ticket governance canary state evidence
```

The original exact-ticket governance spec commit was:

```text
94d3b96 Add H024 exact-ticket canary close modify governance spec
```

Important note:

`94d3b96` was committed after tests passed but before the runtime governance packet verifier passed. It failed closed, so no unsafe authorization opened, but the commit needed a follow-up compatibility fix.

The follow-up fix commit is:

```text
b82d48c Fix H024 exact-ticket governance canary state evidence
```

`b82d48c` is the currently clean source-of-truth commit for HANDOFF_103.

Expected final working tree state:

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
```

`reports/` is runtime/generated output. It must stay untracked.

---

## 3. Latest Confirmed Validation At This Handoff

Validation was performed after applying the v3 follow-up fix and before commit `b82d48c`.

Focused exact-ticket governance tests:

```text
23 passed
```

Full suite:

```text
1574 passed
```

No-mutation safety gate packet:

```text
Wrote reports\h024_runtime_no_mutation_safety_gate.jsonl
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
```

No-mutation safety gate verifier:

```text
H024 runtime no-mutation safety gate records: 1
Violations: 0
Embedded violations: 0
Record verdict: PASS
Verifier verdict: PASS
```

Runtime lockout packet:

```text
Wrote reports\h024_runtime_safety_lockout.jsonl
Verdict: PASS
Violations: 0
Operator state: LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Lockout inputs valid: True
Lockout triggered: False
Active lockouts: 0
Fail-closed lockouts: 0
```

Runtime heartbeat packet:

```text
Wrote reports\h024_runtime_safety_heartbeat.jsonl
Verdict: PASS
Violations: 0
Operator state: RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED
MT5 initialized: True
Account server: Exness-MT5Trial6
Account currency: USD
Terminal connected: True
```

Runtime tick/spread safety supervisor packet:

```text
Wrote reports\h024_runtime_tick_spread_safety_supervisor.jsonl
Verdict: PASS
Violations: 0
Operator state: TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED
Symbol select authorized: False
Symbol USDJPYm: verdict=PASS bid=157.629 ask=157.639 spread_points=10.000000000019327 tick_age_seconds=-0.7684204578399658
Symbol XAUUSDm: verdict=PASS bid=4719.661 ask=4719.969 spread_points=307.9999999999927 tick_age_seconds=-0.4524204730987549
```

Runtime exposure/inventory safety supervisor packet:

```text
Wrote reports\h024_runtime_exposure_inventory_safety_supervisor.jsonl
Verdict: PASS
Violations: 0
Operator state: EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
H024 position symbol=XAUUSDm ticket=4413054432 identifier=4413054432 magic=240024 volume=0.01 type=1 verdict=PASS
```

Runtime account risk/margin safety supervisor packet:

```text
Wrote reports\h024_runtime_account_risk_margin_safety_supervisor.jsonl
Verdict: PASS
Violations: 0
Operator state: ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED
Account server: Exness-MT5Trial6
Account currency: USD
Balance: 10000.0
Equity: 10008.48
Profit: 8.48
Margin: 2.36
Free margin: 10006.12
Margin level: 424088.13559322036
Margin used fraction: 0.0002358000415647531
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
```

Runtime safety aggregate supervisor packet:

```text
Wrote reports\h024_runtime_safety_aggregate_supervisor.jsonl
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
```

Unified read-only post-canary runtime supervision packet:

```text
Wrote reports\h024_unified_read_only_post_canary_runtime_supervision.jsonl
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
```

Exact-ticket canary close/modify governance packet:

```text
Wrote reports\h024_exact_ticket_canary_close_modify_governance.jsonl
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
```

Exact-ticket governance verifier:

```text
H024 exact-ticket canary close/modify governance records: 1
Violations: 0
Embedded violations: 0
Record verdict: PASS
Verifier verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW
```

Final git state after commit and push:

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
```

---

## 4. Absolutely Hard Safety Boundary

The current H024 state is post-canary, read-only, no-mutation.

Do not do any of these:

- Do not create a second H024 entry.
- Do not place a live order.
- Do not place a demo order.
- Do not place a USDJPY order.
- Do not scale the existing XAUUSDm canary.
- Do not call `order_check`.
- Do not call `order_send`.
- Do not close the XAUUSDm canary.
- Do not modify the XAUUSDm canary.
- Do not modify SL/TP.
- Do not run a trading loop.
- Do not mutate broker/account/symbol state.
- Do not call `symbol_select` from new safety/governance code.
- Do not treat any passing safety/governance packet as permission to trade.
- Do not add `reports/` to git.

Close/modify is not authorized. It is not “almost authorized.” It is not “safe because the canary is known.” It remains prohibited unless a future exact-ticket governance path is separately specified, reviewed, and still initially read-only.

The new exact-ticket governance packet is a specification/coherence packet only. A PASS means the governance specification is coherent and the exact known canary evidence is consistent. PASS does not authorize action.

Any unsafe ambiguity must fail closed.

---

## 5. Current Known Canary

There is exactly one known H024 standard-demo XAUUSDm canary.

Known identity:

```text
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
```

Latest confirmed runtime result through the unified supervision and exact-ticket governance chain:

```text
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
H024 position count: 1
H024 order count: 0
```

This observation does not authorize:

- close
- modify
- scale
- new entry
- USDJPY order
- `order_check`
- `order_send`
- trading loop

---

## 6. Current Recent Commit Chain

Recent relevant commits, oldest to newest:

```text
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
```

Latest confirmed commit is:

```text
b82d48c Fix H024 exact-ticket governance canary state evidence
```

---

## 7. Runtime Safety Layer Summary

### 7.1 H024 Runtime Safety Lockout Reader

Commit:

```text
98efc2a Add H024 runtime safety lockout reader
```

Intent:

Define committed default runtime safety lockout config. Read local lockout state. Support global no-new-entry, manual override lockout, per-symbol XAUUSD no-new-entry lockout, and per-symbol USDJPY no-new-entry lockout. Fail closed on missing/malformed unsafe inputs.

Passing operator state:

```text
LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED
```

Important semantics:

Even if lockouts are clear, trading is not authorized.

Key files:

```text
config/h024_runtime_safety/default_lockout_config.json
quantcore/execution/h024_runtime_safety_lockout.py
scripts/build_h024_runtime_safety_lockout_jsonl.py
scripts/verify_h024_runtime_safety_lockout_jsonl.py
tests/test_h024_runtime_safety_lockout.py
```

### 7.2 H024 Runtime Safety Heartbeat Packet

Commit:

```text
187e9dd Add H024 runtime safety heartbeat packet
```

Intent:

Read-only MT5 runtime heartbeat. Verify MT5 initialization, account availability, expected server, USD account currency, and terminal/account heartbeat freshness where available. Reference runtime safety lockout reader. Fail closed on unavailable/inconsistent runtime state.

Expected server:

```text
Exness-MT5Trial6
```

Expected currency:

```text
USD
```

Passing operator state:

```text
RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED
```

Forbidden:

- `order_check`
- `order_send`
- entry
- close
- modify
- trading loop
- broker mutation

Key files:

```text
quantcore/execution/h024_runtime_safety_heartbeat.py
scripts/build_h024_runtime_safety_heartbeat_jsonl.py
scripts/verify_h024_runtime_safety_heartbeat_jsonl.py
tests/test_h024_runtime_safety_heartbeat.py
docs/operations/H024_RUNTIME_SAFETY_HEARTBEAT_PACKET.md
```

### 7.3 H024 Runtime Tick/Spread Safety Supervisor

Commit:

```text
abecff8 Add H024 runtime tick and spread safety supervisor
```

Intent:

Read-only market-data safety layer. Consume/reference runtime lockout reader and heartbeat. Verify XAUUSDm and USDJPYm tick availability, bid/ask sanity, ask > bid, positive spread, spread thresholds, tick freshness, and symbol visibility/readability without selecting symbols.

Important design decision:

Do not call `symbol_select`.

If a symbol is not already readable/visible, fail closed.

Runtime symbols:

```text
XAUUSDm -> model symbol XAUUSD
USDJPYm -> model symbol USDJPY
```

Passing operator state:

```text
TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED
```

Key files:

```text
quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py
scripts/build_h024_runtime_tick_spread_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_tick_spread_safety_supervisor_jsonl.py
tests/test_h024_runtime_tick_spread_safety_supervisor.py
docs/operations/H024_RUNTIME_TICK_SPREAD_SAFETY_SUPERVISOR.md
```

### 7.4 H024 Runtime Exposure/Inventory Safety Supervisor

Commit:

```text
0db61fa Add H024 runtime exposure inventory safety supervisor
```

Intent:

Read-only inventory supervisor. Consume/reference lockout, heartbeat, tick/spread. Inspect MT5 positions/orders without mutation. Allow only no H024 inventory or the exact known XAUUSDm canary. Reject any H024 USDJPY position/order, any H024 pending/open order, any extra H024 position, and any mismatched XAUUSDm canary identity.

Known canary allowed fields:

```text
symbol: XAUUSDm
ticket or identifier: 4413054432
magic: 240024
volume: 0.01
type: 1
```

Known passing result at this handoff:

```text
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
```

Flat state is allowed by this packet:

```text
Canary state: NOT_OBSERVED
H024 position count: 0
H024 order count: 0
```

But flat state does not authorize a new entry.

Passing operator state:

```text
EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED
```

Key files:

```text
quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py
scripts/build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
tests/test_h024_runtime_exposure_inventory_safety_supervisor.py
docs/operations/H024_RUNTIME_EXPOSURE_INVENTORY_SAFETY_SUPERVISOR.md
```

### 7.5 H024 Runtime Account Risk/Margin Safety Supervisor

Commit:

```text
1c331c6 Add H024 runtime account risk margin safety supervisor
```

Intent:

Read-only account risk/margin supervisor. Consume/reference lockout, heartbeat, tick/spread, exposure/inventory. Inspect account_info without mutation. Verify server, USD account context, balance sanity, equity sanity, margin sanity, free margin sanity, margin level sanity where available, floating PnL consistency where available, and canary exposure boundedness. Fail closed on margin compression or inconsistent account state.

Passing operator state:

```text
ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED
```

Key files:

```text
quantcore/execution/h024_runtime_account_risk_margin_safety_supervisor.py
scripts/build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
tests/test_h024_runtime_account_risk_margin_safety_supervisor.py
docs/operations/H024_RUNTIME_ACCOUNT_RISK_MARGIN_SAFETY_SUPERVISOR.md
```

### 7.6 H024 Runtime Safety Aggregate Supervisor

Commit:

```text
8e8979c Add H024 runtime safety aggregate supervisor
```

Intent:

Read-only aggregate supervisor. Combine all runtime safety packets into one fail-closed operator verdict. Prevent future code from cherry-picking one passing packet while ignoring another failing packet. Require every upstream packet to pass. Verify upstream packet freshness. Merge embedded violations. Verify all no-execution authorizations remain false.

Consumes/references:

- lockout reader
- heartbeat
- tick/spread
- exposure/inventory
- account risk/margin

Passing operator state:

```text
RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
```

Key files:

```text
quantcore/execution/h024_runtime_safety_aggregate_supervisor.py
scripts/build_h024_runtime_safety_aggregate_supervisor_jsonl.py
scripts/verify_h024_runtime_safety_aggregate_supervisor_jsonl.py
tests/test_h024_runtime_safety_aggregate_supervisor.py
docs/operations/H024_RUNTIME_SAFETY_AGGREGATE_SUPERVISOR.md
```

### 7.7 H024 Unified Read-Only Post-Canary Runtime Supervision

Commit:

```text
224371a Add H024 unified read-only runtime supervision
```

Intent:

Operator-facing wrapper. Combine existing one-shot canary read-only supervision runner and runtime safety aggregate supervisor. Produce one JSONL packet for operator review. Report canary lifecycle/supervision state, runtime aggregate state, upstream packet summaries, exact known canary identity if observed, and a single fail-closed operator next action.

Known passing result at this handoff:

```text
Verdict: PASS
Violations: 0
Operator state: UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
```

Key files:

```text
quantcore/execution/h024_unified_read_only_post_canary_runtime_supervision.py
scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
scripts/verify_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
tests/test_h024_unified_read_only_post_canary_runtime_supervision.py
docs/operations/H024_UNIFIED_READ_ONLY_POST_CANARY_RUNTIME_SUPERVISION.md
```

### 7.8 H024 Runtime No-Mutation Safety Gate Contract

Commit:

```text
5249ad1 Add H024 runtime no-mutation safety gate
```

Intent:

Read-only no-mutation gate contract. Consume/reference unified read-only post-canary runtime supervision. Define the mandatory fail-closed gate interface future broker-facing code must check. Prove the current state still blocks broker mutation, entries, close/modify, `order_check`, `order_send`, XAUUSD order, USDJPY order, trading loop, and automatic execution. Reject missing/malformed/untrusted unified supervision. Include static tests showing current non-exempt execution-related code has no direct broker mutation call sites.

Known passing result at this handoff:

```text
Verdict: PASS
Violations: 0
Operator state: NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED
Operator next action: KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION
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
```

Frozen legacy exceptions documented:

- historical one-shot canary send path
- historical MT5 terminal preflight helper that may call `symbol_select`

These are not authorized by the gate. They are frozen historical/pre-gate artifacts only.

Key files:

```text
quantcore/execution/h024_runtime_no_mutation_safety_gate.py
scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py
scripts/verify_h024_runtime_no_mutation_safety_gate_jsonl.py
tests/test_h024_runtime_no_mutation_safety_gate.py
docs/operations/H024_RUNTIME_NO_MUTATION_SAFETY_GATE.md
```

---

## 8. New Milestone Completed In HANDOFF_103

### 8.1 H024 Exact-Ticket Canary Close/Modify Governance Specification Packet

Original commit:

```text
94d3b96 Add H024 exact-ticket canary close modify governance spec
```

Follow-up fix commit:

```text
b82d48c Fix H024 exact-ticket governance canary state evidence
```

Intent:

Read-only exact-ticket canary close/modify governance specification packet. It defines the governance requirements that must be coherent before any future close/modify of the exact known XAUUSDm canary could even be considered.

This packet does not authorize close/modify. It explicitly keeps all action paths blocked.

It requires:

1. Exact ticket/identifier lock:
   - ticket or identifier must be `4413054432`.

2. Exact canary identity:
   - runtime symbol `XAUUSDm`
   - model symbol `XAUUSD`
   - side `sell`
   - MT5 type `1`
   - volume `0.01`
   - magic `240024`

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
   - stale/missing/malformed/ambiguous decision fails closed
   - default artifact is non-authorizing

7. Pre-close risk snapshot:
   - account risk/margin snapshot
   - exposure/inventory snapshot
   - tick/spread snapshot
   - missing/malformed/stale snapshot fails closed

8. No current authorization:
   - broker mutation false
   - `order_check` false
   - `order_send` false
   - entry false
   - close/modify false
   - XAUUSD order false
   - USDJPY order false
   - trading loop false
   - automatic execution false

Passing operator state:

```text
EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED
```

Passing operator next action:

```text
KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW
```

Fail-closed operator state:

```text
FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_BLOCKED
```

Fail-closed operator next action:

```text
FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED
```

Key files:

```text
config/h024_runtime_safety/default_exact_ticket_canary_close_modify_governance_decision.json
quantcore/execution/h024_exact_ticket_canary_close_modify_governance.py
scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_governance.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE.md
```

Report path:

```text
reports/h024_exact_ticket_canary_close_modify_governance.jsonl
```

Known passing result:

```text
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
```

Verifier known passing result:

```text
H024 exact-ticket canary close/modify governance records: 1
Violations: 0
Embedded violations: 0
Record verdict: PASS
Verifier verdict: PASS
```

### 8.2 What Went Wrong In The First Exact-Ticket Governance Commit

Commit `94d3b96` created the packet, docs, tests, builder, verifier, and default decision artifact. Focused tests and full suite passed, but the live runtime packet verifier failed under `--require-pass`.

Failure symptoms included:

- no-mutation gate identity/mutation-path fields were not read correctly from actual runtime report shape
- unified post-canary runtime supervision was not loaded correctly
- exact canary state was not extracted correctly
- USDJPY blocked flag was initially misinterpreted as exposure evidence

The packet failed closed and opened no mutation path.

### 8.3 What The Follow-Up Fix Did

Commit `b82d48c` fixed runtime evidence compatibility without loosening safety.

The final fix:

- preserves fail-closed behavior
- builds required read-only upstream evidence reports before governance packet generation
- reads actual runtime report field aliases correctly
- resolves the exact canary state from unified/exposure/account evidence
- preserves the requirement that all action authorizations remain false
- keeps PASS as “governance spec coherent but action not authorized”

---

## 9. Latest Verification Commands For The Next AI

A new AI should ask the user to run this block first:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

git status
git log --oneline -10

python -m pytest tests\test_h024_exact_ticket_canary_close_modify_governance.py
python -m pytest

python scripts\build_h024_runtime_no_mutation_safety_gate_jsonl.py
python scripts\verify_h024_runtime_no_mutation_safety_gate_jsonl.py reports\h024_runtime_no_mutation_safety_gate.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py reports\h024_exact_ticket_canary_close_modify_governance.jsonl --require-pass

git status
```

Expected:

```text
Focused tests: 23 passed
Full suite: 1574 passed
No-mutation gate packet: PASS
No-mutation gate verifier: PASS
Exact-ticket governance packet: PASS
Exact-ticket governance verifier: PASS
Violations: 0
All action authorizations: false
Final git status: only reports/ untracked
```

If this does not pass, stop and diagnose. Do not implement the next milestone on an unverified base.

---

## 10. Core Implementation Pattern For Future Milestones

Every new H024 runtime/governance safety milestone should include:

1. `quantcore/execution/<module>.py`
2. `scripts/build_<packet>_jsonl.py`
3. `scripts/verify_<packet>_jsonl.py`
4. `tests/test_<packet>.py`
5. `docs/operations/<PACKET_DOC>.md`

Every packet should include:

```text
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
```

Verifier should fail closed on:

- missing records
- malformed JSONL
- wrong schema version
- wrong strategy
- wrong packet type
- missing/malformed upstream
- unexpected PASS with embedded violations
- any authorization not false
- `effective_new_entries_blocked` not true
- `--require-pass` with record verdict not PASS

Tests should include:

- passing happy path
- missing input fails closed
- malformed input fails closed
- wrong strategy or packet type fails closed
- unsafe authorization true fails verifier
- missing authorization fails verifier
- embedded violations fail verifier
- `--require-pass` rejects fail-closed record
- static no-mutation checks when relevant

---

## 11. Commit Discipline

For every milestone:

```powershell
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
```

Never add `reports/`.

Never commit if the milestone verifier fails under `--require-pass`.

Expected final status after commit and push:

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
```

---

## 12. Static Safety Expectations

The no-mutation gate includes static checks for direct broker mutation call sites in current non-exempt execution-related code.

Known frozen legacy exceptions:

```text
run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py
```

Interpretation:

These are frozen legacy/pre-gate artifacts. They are not authorized by the no-mutation gate. They must not be treated as current execution adapters. Do not add new exceptions casually. If a future exception is proposed, fail closed and require explicit documentation.

---

## 13. Operator Language To Preserve

Use these interpretations consistently:

```text
PASS = read-only safety/governance packet is coherent
PASS != trading authorized
PASS != close/modify authorized
PASS != order_check authorized
PASS != order_send authorized
PASS != broker mutation authorized
```

Preferred wording:

- OK but trading not authorized
- fail closed
- read-only observation
- operator review required
- no broker mutation authorized
- current state remains blocked
- action not authorized

Avoid wording like:

- ready to trade
- safe to execute
- approved to close
- approved to modify
- can proceed with order

---

## 14. If Something Fails

If tests or verifier fail:

1. Do not continue to commit.
2. Diagnose exact failure.
3. Patch narrowly.
4. Rerun focused tests.
5. Rerun full suite.
6. Rerun builder/verifier.
7. Commit only after clean validation.

If live/runtime data changes, such as:

- canary absent
- canary PnL changed
- tick age changed
- spread changed
- margin changed

Do not assume failure is bad. Read verifier semantics. Flat inventory may be allowed by some upstream packets, but no packet authorizes a new entry.

For the exact-ticket close/modify governance packet specifically, a flat/no-canary state may be safe operationally but does not satisfy exact-ticket canary identity matching for close/modify governance. It must fail closed for exact-ticket governance unless the governance spec is explicitly changed in a future read-only milestone.

---

## 15. Recommended Next Milestone

Next milestone should be:

```text
H024 exact-ticket canary close/modify dry-run operator decision artifact validator
```

This must be read-only only.

It must not:

- close the canary
- modify the canary
- build a live broker request
- call `order_check`
- call `order_send`
- call close/modify helpers
- call `symbol_select`
- mutate MT5 state
- run a trading loop

Purpose:

Create a stricter validator for the human/operator decision artifact referenced by the exact-ticket governance packet. The current default artifact is deliberately non-authorizing:

```text
NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
```

The next packet should define and validate the schema for a future explicit human decision artifact while still authorizing no action. It should make clear that even a well-formed explicit decision artifact does not itself authorize close/modify unless a later separate read-only pre-action packet is implemented and passes.

Suggested module name:

```text
quantcore/execution/h024_exact_ticket_canary_close_modify_decision_artifact.py
```

Suggested scripts:

```text
scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
```

Suggested tests:

```text
tests/test_h024_exact_ticket_canary_close_modify_decision_artifact.py
```

Suggested docs:

```text
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT.md
```

Suggested report path:

```text
reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl
```

Suggested commit message:

```text
Add H024 exact-ticket close modify decision artifact validator
```

Suggested next prompt:

```text
Let’s implement the H024 exact-ticket canary close/modify decision artifact validator. It must be read-only only and must not close or modify anything. It should define and validate the explicit human/operator decision artifact schema referenced by the exact-ticket governance packet while still authorizing no action. It must require exact ticket/identifier 4413054432, exact XAUUSDm canary identity, decision freshness, explicit non-ambiguous operator intent fields, operator attestation fields, and fail-closed behavior for missing, malformed, stale, ambiguous, or unsafe artifacts. It must not build a broker request and must authorize no broker mutation, no order_check, no order_send, no entries, no close/modify, no XAUUSD order, no USDJPY order, and no trading loop. Include module, verifier, tests, scripts, and docs. Keep reports/ untracked.
```

---

## 16. Explicit Next-Milestone Failure Modes

The exact-ticket canary close/modify decision artifact validator must fail closed if:

- decision artifact missing
- decision artifact malformed
- wrong strategy
- wrong packet type
- wrong schema version
- decision stale
- decision timestamp missing
- decision identity ambiguous
- exact ticket/identifier mismatch
- runtime symbol mismatch
- model symbol mismatch
- side/type mismatch
- volume mismatch
- magic mismatch
- operator intent missing
- operator intent ambiguous
- operator attestation missing
- operator attestation contradicts no-mutation posture
- artifact implies immediate close/modify authorization
- artifact implies `order_check` authorization
- artifact implies `order_send` authorization
- artifact implies broker mutation authorization
- artifact implies trading loop authorization
- any authorization true
- `effective_new_entries_blocked` not true

It must pass only as a read-only artifact schema/coherence validator. PASS should mean:

```text
the decision artifact is syntactically and semantically coherent
all action paths remain blocked
no broker mutation is authorized
```

It must not mean:

```text
close is authorized
modify is authorized
order_check is authorized
order_send is authorized
```

---

## 17. How The Next AI Should Start

The next AI should respond:

```text
Understood. Continuing from HANDOFF_103 at commit b82d48c. Current state is read-only H024 post-canary runtime supervision with a no-mutation gate and an exact-ticket close/modify governance specification packet; all broker mutation and trading paths remain blocked. Please run the HANDOFF_103 verification block so I can confirm local state before the next read-only milestone.
```

Then provide the verification block from Section 9.

---

## 18. Final Reminder

This handoff is deliberately conservative.

Current H024 posture:

```text
Observe only.
Supervise only.
Specify governance only.
Fail closed.
Authorize nothing.
Keep reports/ untracked.
```
