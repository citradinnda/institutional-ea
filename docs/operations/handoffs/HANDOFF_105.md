# HANDOFF_105 — Fully Self-Contained H024 Exact-Ticket Close/Modify Pre-Action Evidence Aggregate Handoff

This handoff is the source of truth for the next AI.

It supersedes HANDOFF_104 and all older handoffs. It preserves the same hard safety posture and adds the completed, validated H024 exact-ticket canary close/modify read-only pre-action evidence aggregate supervisor milestone.

This document is deliberately redundant and self-contained so the next AI does not need to guess repo state, validation state, safety posture, runtime posture, implementation files, failed intermediate history, or the next recommended milestone.

---

## 1. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Preserve every hard safety boundary.
3. Treat all H024 runtime/governance/decision/pre-action evidence work as read-only unless a future milestone explicitly says otherwise.
4. Never infer that a passing safety/governance/decision/pre-action evidence packet authorizes trading.
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
17. Run focused tests, full suite, packet builder, packet verifier, `git diff --cached --check`, commit, push, and final `git status`.
18. After each milestone, give:
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

Latest confirmed pushed handoff before this document:

7c2c13f Add handoff document #104

Latest confirmed implementation milestone before this handoff:

e370a60 Fix H024 pre-action aggregate upstream validation path

Important: the validated milestone is the final fix-forward commit e370a60, not the earlier intermediate commits 86774c4 or 10b4a14.

Expected working tree state before writing HANDOFF_105:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime/generated output. It must stay untracked.

After HANDOFF_105 is committed and pushed, the latest repo commit will be the handoff commit, but the latest confirmed implementation milestone remains:

e370a60 Fix H024 pre-action aggregate upstream validation path
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

The exact-ticket governance packet is a specification/coherence packet only.

The exact-ticket decision artifact validator is a decision artifact schema/coherence packet only.

The exact-ticket pre-action evidence aggregate is an evidence coherence packet only.

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

Latest validated runtime/pre-action aggregate state at this handoff:

Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
H024 position count: 1
H024 order count: 0
H024 position symbol=XAUUSDm ticket=4413054432 identifier=4413054432 magic=240024 volume=0.01 type=1 verdict=PASS

The user reported that the position has been open for over 3 bars. The pre-action evidence aggregate records this as:

User reported position open over three bars: True

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

Latest confirmed implementation milestone:

e370a60 Fix H024 pre-action aggregate upstream validation path
6. Runtime Safety Layer Summary
6.1 H024 Runtime Safety Lockout Reader

Commit:

98efc2a Add H024 runtime safety lockout reader

Intent:

Define committed default runtime safety lockout config. Read local lockout state. Support global no-new-entry, manual override lockout, per-symbol XAUUSD no-new-entry lockout, and per-symbol USDJPY no-new-entry lockout. Fail closed on missing/malformed unsafe inputs.

Passing operator state:

LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Important semantics:

Even if lockouts are clear, trading is not authorized.

Key files:

config/h024_runtime_safety/default_lockout_config.json
quantcore/execution/h024_runtime_safety_lockout.py
scripts/build_h024_runtime_safety_lockout_jsonl.py
scripts/verify_h024_runtime_safety_lockout_jsonl.py
tests/test_h024_runtime_safety_lockout.py
6.2 H024 Runtime Safety Heartbeat Packet

Commit:

187e9dd Add H024 runtime safety heartbeat packet

Intent:

Read-only MT5 runtime heartbeat. Verify MT5 initialization, account availability, expected server, USD account currency, and terminal/account heartbeat freshness where available. Reference runtime safety lockout reader. Fail closed on unavailable/inconsistent runtime state.

Expected server:

Exness-MT5Trial6

Expected currency:

USD

Passing operator state:

RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED

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
6.3 H024 Runtime Tick/Spread Safety Supervisor

Commit:

abecff8 Add H024 runtime tick and spread safety supervisor

Intent:

Read-only market-data safety layer. Consume/reference runtime lockout reader and heartbeat. Verify XAUUSDm and USDJPYm tick availability, bid/ask sanity, ask > bid, positive spread, spread thresholds, tick freshness, and symbol visibility/readability without selecting symbols.

Important design decision:

Do not call symbol_select.

If a symbol is not already readable/visible, fail closed.

Runtime symbols:

XAUUSDm -> model symbol XAUUSD
USDJPYm -> model symbol USDJPY

Passing operator state:

TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED

Key files:

quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py
scripts/build_h024_runtime_tick_spread_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_tick_spread_safety_supervisor_jsonl.py
tests/test_h024_runtime_tick_spread_safety_supervisor.py
docs/operations/H024_RUNTIME_TICK_SPREAD_SAFETY_SUPERVISOR.md
6.4 H024 Runtime Exposure/Inventory Safety Supervisor

Commit:

0db61fa Add H024 runtime exposure inventory safety supervisor

Intent:

Read-only inventory supervisor. Consume/reference lockout, heartbeat, tick/spread. Inspect MT5 positions/orders without mutation. Allow only no H024 inventory or the exact known XAUUSDm canary. Reject any H024 USDJPY position/order, any H024 pending/open order, any extra H024 position, and any mismatched XAUUSDm canary identity.

Known canary allowed fields:

symbol: XAUUSDm
ticket or identifier: 4413054432
magic: 240024
volume: 0.01
type: 1

Known passing result at this handoff:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0

Flat state is allowed by this packet:

Canary state: NOT_OBSERVED
H024 position count: 0
H024 order count: 0

But flat state does not authorize a new entry.

Passing operator state:

EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED

Key files:

quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py
scripts/build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py
tests/test_h024_runtime_exposure_inventory_safety_supervisor.py
docs/operations/H024_RUNTIME_EXPOSURE_INVENTORY_SAFETY_SUPERVISOR.md
6.5 H024 Runtime Account Risk/Margin Safety Supervisor

Commit:

1c331c6 Add H024 runtime account risk margin safety supervisor

Intent:

Read-only account risk/margin supervisor. Consume/reference lockout, heartbeat, tick/spread, exposure/inventory. Inspect account_info without mutation. Verify server, USD account context, balance sanity, equity sanity, margin sanity, free margin sanity, margin level sanity where available, floating PnL consistency where available, and canary exposure boundedness. Fail closed on margin compression or inconsistent account state.

Passing operator state:

ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED

Key files:

quantcore/execution/h024_runtime_account_risk_margin_safety_supervisor.py
scripts/build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
scripts/verify_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py
tests/test_h024_runtime_account_risk_margin_safety_supervisor.py
docs/operations/H024_RUNTIME_ACCOUNT_RISK_MARGIN_SAFETY_SUPERVISOR.md
6.6 H024 Runtime Safety Aggregate Supervisor

Commit:

8e8979c Add H024 runtime safety aggregate supervisor

Intent:

Read-only aggregate supervisor. Combine all runtime safety packets into one fail-closed operator verdict. Prevent future code from cherry-picking one passing packet while ignoring another failing packet. Require every upstream packet to pass. Verify upstream packet freshness. Merge embedded violations. Verify all no-execution authorizations remain false.

Consumes/references:

lockout reader
heartbeat
tick/spread
exposure/inventory
account risk/margin

Passing operator state:

RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED

Key files:

quantcore/execution/h024_runtime_safety_aggregate_supervisor.py
scripts/build_h024_runtime_safety_aggregate_supervisor_jsonl.py
scripts/verify_h024_runtime_safety_aggregate_supervisor_jsonl.py
tests/test_h024_runtime_safety_aggregate_supervisor.py
docs/operations/H024_RUNTIME_SAFETY_AGGREGATE_SUPERVISOR.md
6.7 H024 Unified Read-Only Post-Canary Runtime Supervision

Commit:

224371a Add H024 unified read-only runtime supervision

Intent:

Operator-facing wrapper. Combine existing one-shot canary read-only supervision runner and runtime safety aggregate supervisor. Produce one JSONL packet for operator review. Report canary lifecycle/supervision state, runtime aggregate state, upstream packet summaries, exact known canary identity if observed, and a single fail-closed operator next action.

Known passing result:

Verdict: PASS
Violations: 0
Operator state: UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True

Key files:

quantcore/execution/h024_unified_read_only_post_canary_runtime_supervision.py
scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
scripts/verify_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py
tests/test_h024_unified_read_only_post_canary_runtime_supervision.py
docs/operations/H024_UNIFIED_READ_ONLY_POST_CANARY_RUNTIME_SUPERVISION.md
6.8 H024 Runtime No-Mutation Safety Gate Contract

Commit:

5249ad1 Add H024 runtime no-mutation safety gate

Intent:

Read-only no-mutation gate contract. Consume/reference unified read-only post-canary runtime supervision. Define the mandatory fail-closed gate interface future broker-facing code must check. Prove the current state still blocks broker mutation, entries, close/modify, order_check, order_send, XAUUSD order, USDJPY order, trading loop, and automatic execution. Reject missing/malformed/untrusted unified supervision. Include static tests showing current non-exempt execution-related code has no direct broker mutation call sites.

Known passing result:

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
7. Exact-Ticket Close/Modify Governance And Decision Layers
7.1 H024 Exact-Ticket Canary Close/Modify Governance Specification Packet

Original commit:

94d3b96 Add H024 exact-ticket canary close modify governance spec

Follow-up fix commit:

b82d48c Fix H024 exact-ticket governance canary state evidence

Intent:

Read-only exact-ticket canary close/modify governance specification packet. It defines the governance requirements that must be coherent before any future close/modify of the exact known XAUUSDm canary could even be considered.

This packet does not authorize close/modify. It explicitly keeps all action paths blocked.

It requires:

Exact ticket/identifier:
  ticket or identifier must be 4413054432.

Exact canary identity:
  runtime symbol XAUUSDm
  model symbol XAUUSD
  side sell
  MT5 type 1
  volume 0.01
  magic 240024

Runtime no-mutation safety gate PASS:
  gate must be trusted
  gate must still block all mutation
  gate must not open any mutation path

No USDJPY H024 exposure/order:
  no USDJPYm position/order with H024 magic/comment/identity

No additional H024 exposure/order:
  no additional H024 XAUUSDm position
  no H024 pending/open order

Explicit human decision artifact:
  separate artifact must exist
  decision must be explicit
  stale/missing/malformed/ambiguous decision fails closed
  default artifact is non-authorizing

Pre-close risk snapshot:
  account risk/margin snapshot
  exposure/inventory snapshot
  tick/spread snapshot
  missing/malformed/stale snapshot fails closed

No current authorization:
  broker mutation false
  order_check false
  order_send false
  entry false
  close/modify false
  XAUUSD order false
  USDJPY order false
  trading loop false
  automatic execution false

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED

Passing operator next action:

KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW

Fail-closed operator state:

FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_BLOCKED

Fail-closed operator next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Key files:

config/h024_runtime_safety/default_exact_ticket_canary_close_modify_governance_decision.json
quantcore/execution/h024_exact_ticket_canary_close_modify_governance.py
scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_governance.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE.md

Report path:

reports/h024_exact_ticket_canary_close_modify_governance.jsonl

Known passing result:

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

Verifier known passing result:

H024 exact-ticket canary close/modify governance records: 1
Violations: 0
Embedded violations: 0
Record verdict: PASS
Verifier verdict: PASS
7.2 H024 Exact-Ticket Canary Close/Modify Decision Artifact Validator

Commit:

9f061c1 Add H024 exact-ticket close modify decision artifact validator

Intent:

Read-only exact-ticket canary close/modify decision artifact validator. It defines and validates the explicit human/operator decision artifact schema referenced by the exact-ticket governance packet while still authorizing no action.

The milestone validates that a decision artifact is syntactically and semantically coherent, exact-ticket locked, exact-canary locked, fresh enough, non-ambiguous, and aligned with the no-mutation posture.

This packet does not authorize close/modify.

It does not build a broker request.

It does not call order_check.

It does not call order_send.

It does not call close/modify helpers.

It does not call symbol_select.

It does not mutate MT5 state.

It does not run a trading loop.

Default decision artifact:

config/h024_runtime_safety/default_exact_ticket_canary_close_modify_decision_artifact.json

Default decision status:

NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY

Default requested action:

NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED

Passing operator next action:

KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_DECISION_ARTIFACT_REVIEW

Fail-closed semantics:

Any malformed, stale, missing, ambiguous, contradictory, or unsafe decision artifact fails closed.

A PASS means:

the decision artifact is syntactically and semantically coherent
all action paths remain blocked
no broker mutation is authorized

A PASS does not mean:

close is authorized
modify is authorized
order_check is authorized
order_send is authorized
broker mutation is authorized

Key files:

config/h024_runtime_safety/default_exact_ticket_canary_close_modify_decision_artifact.json
quantcore/execution/h024_exact_ticket_canary_close_modify_decision_artifact.py
scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_decision_artifact.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT.md

Report path:

reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl

Known passing result:

Wrote reports\h024_exact_ticket_canary_close_modify_decision_artifact.jsonl
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_DECISION_ARTIFACT_REVIEW
Decision status: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Requested action: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
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

Verifier known passing result:

H024 exact-ticket canary close/modify decision artifact records: 1
Violations: 0
Embedded violations: 0
Record verdict: PASS
Verifier verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_DECISION_ARTIFACT_REVIEW
Requested action: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Effective new entries blocked: True
automatic_execution_authorized: False
broker_mutation_authorized: False
close_modify_authorized: False
entry_authorized: False
order_check_authorized: False
order_send_authorized: False
trading_loop_authorized: False
usdjpy_order_authorized: False
xauusd_order_authorized: False

Focused tests:

36 passed

Full suite at HANDOFF_104 base:

1612 passed
8. New Milestone Completed In HANDOFF_105
8.1 H024 Exact-Ticket Canary Close/Modify Read-Only Pre-Action Evidence Aggregate Supervisor

Initial implementation commit:

86774c4 Add H024 exact-ticket close modify pre-action evidence aggregate

First fix-forward commit:

10b4a14 Fix H024 pre-action evidence aggregate identity validation

Final validated fix-forward commit:

e370a60 Fix H024 pre-action aggregate upstream validation path

Only e370a60 is the validated implementation state.

Intent:

Create a read-only aggregate packet that consumes and cross-checks:

Runtime no-mutation safety gate
Unified read-only post-canary runtime supervision
Exact-ticket canary close/modify governance specification packet
Exact-ticket canary close/modify decision artifact validator packet
Fresh runtime account risk/margin, exposure/inventory, and tick/spread evidence via existing upstream packets

Purpose:

Make it impossible for a future tool/operator to cherry-pick the decision artifact validator while ignoring the no-mutation gate, governance packet, runtime supervision, stale evidence, inconsistent canary evidence, or unsafe authorizations.

The aggregate passes only when:

all upstream packets PASS
all upstream packets are fresh
all upstream packets are mutually consistent
exact ticket/identifier 4413054432 is preserved
exact XAUUSDm canary identity is preserved
exact canary is observed when required
no USDJPY H024 exposure/order is observed
no additional H024 exposure/order is observed
all action authorizations remain false
effective_new_entries_blocked is true

Passing state means:

the pre-action evidence bundle is coherent for read-only operator review
all action paths remain blocked
no broker mutation is authorized

Passing state does not mean:

close is authorized
modify is authorized
order_check is authorized
order_send is authorized
broker request construction is authorized

This packet does not:

close the canary
modify the canary
build a live broker request
call order_check
call order_send
call close/modify helpers
call symbol_select
mutate MT5 state
run a trading loop

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED

Passing operator next action:

KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_PRE_ACTION_EVIDENCE_REVIEW

Fail-closed operator state:

FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_BLOCKED

Fail-closed operator next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Key files:

quantcore/execution/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.py
scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE.md

Report path:

reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl

Suggested original commit message used:

Add H024 exact-ticket close modify pre-action evidence aggregate

Final validated fix-forward commit message:

Fix H024 pre-action aggregate upstream validation path
9. Failed Intermediate History For The Pre-Action Aggregate

This section is important. The implementation history includes two pushed intermediate commits that were not validated by the runtime builder/verifier. They are superseded by the final fix-forward commit e370a60.

9.1 Initial Script Wrapper Failure Before First Commit

The first installer script failed due to malformed PowerShell wrapper quoting:

throw \"Command failed: $File $($Args -join ' ')\"

and incorrect use of $Args, which conflicted with PowerShell automatic argument behavior. This caused git to run without the intended subcommand.

This was wrapper failure only, not a safety boundary failure.

9.2 Commit 86774c4 Was Pushed But Not Validated

Commit:

86774c4 Add H024 exact-ticket close modify pre-action evidence aggregate

The focused and full tests passed at that time:

Focused aggregate tests: 23 passed
Full suite: 1635 passed

But the aggregate builder/verifier failed closed due to over-broad identity extraction. It scanned nested upstream market-data records and treated legitimate USDJPYm tick/spread symbol coverage as an XAUUSDm canary identity mismatch.

Representative failure:

Verdict: FAIL_CLOSED
Violations: 23
Verifier verdict: FAIL

Root cause:

The aggregate scanned every nested identity-like field across upstream packets, including unrelated runtime tick/spread expected symbols such as USDJPYm.

This commit is not the validated milestone.

9.3 Commit 10b4a14 Was Pushed But Still Not Validated

Commit:

10b4a14 Fix H024 pre-action evidence aggregate identity validation

The focused and full tests passed at that time:

Focused aggregate tests: 25 passed
Full suite: 1637 passed

But the aggregate builder/verifier still failed closed.

Remaining violations:

unified_runtime_supervision: exact canary observed is not true
decision_artifact: missing required decision_status NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
decision_artifact: missing required requested_action NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY

Root cause:

The aggregate still did not correctly extract exact-canary-observed evidence and decision intent fields from the real upstream packet shape.

This commit is not the validated milestone.

9.4 Final Fix-Forward Commit e370a60 Is Validated

Commit:

e370a60 Fix H024 pre-action aggregate upstream validation path

This commit fixed the real upstream validation path.

It added handling for:

exact_canary_observed/canary_observed true
exact_canary_state/canary_state equal to OBSERVED_EXACT_KNOWN_CANARY
decision_status and requested_action fields discovered by normalized key across the decision-artifact packet
nested expected/observed/passed check wrappers interpreted through observed value
strictly scoped exact canary identity extraction so USDJPYm tick/spread market-data evidence is not treated as canary identity

This is the validated milestone.

10. Final Validated Outputs At HANDOFF_105

Focused aggregate tests:

tests\test_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.py
27 passed

Full suite:

1639 passed

Aggregate builder:

Wrote reports\h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_PRE_ACTION_EVIDENCE_REVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
User reported position open over three bars: True
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
Upstream no_mutation_gate: verdict=PASS age_seconds=6.69072 embedded_violations=0
Upstream unified_runtime_supervision: verdict=PASS age_seconds=1.768749 embedded_violations=0
Upstream exact_ticket_governance: verdict=PASS age_seconds=8.463114 embedded_violations=0
Upstream decision_artifact: verdict=PASS age_seconds=0.057596 embedded_violations=0

Aggregate verifier:

H024 exact-ticket canary close/modify pre-action evidence aggregate records: 1
Violations: 0
Record verdict: PASS
Verifier verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_PRE_ACTION_EVIDENCE_REVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
Effective new entries blocked: True
automatic_execution_authorized: False
broker_mutation_authorized: False
close_modify_authorized: False
entry_authorized: False
order_check_authorized: False
order_send_authorized: False
trading_loop_authorized: False
usdjpy_order_authorized: False
xauusd_order_authorized: False

Commit and push:

[main e370a60] Fix H024 pre-action aggregate upstream validation path
 3 files changed, 101 insertions(+), 31 deletions(-)

To https://github.com/citradinnda/institutional-ea.git
   10b4a14..e370a60  main -> main

Final git status after validated commit:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
11. Latest Verification Commands For The Next AI

A new AI should ask the user to run this block first:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

git status
git log --oneline -15

python -m pytest tests\test_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.py
python -m pytest

python scripts\build_h024_runtime_no_mutation_safety_gate_jsonl.py
python scripts\verify_h024_runtime_no_mutation_safety_gate_jsonl.py reports\h024_runtime_no_mutation_safety_gate.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py reports\h024_exact_ticket_canary_close_modify_governance.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\verify_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py reports\h024_exact_ticket_canary_close_modify_decision_artifact.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\verify_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py reports\h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl --require-pass

git status

Expected:

Focused aggregate tests: 27 passed
Full suite: 1639 passed
No-mutation gate packet/verifier: PASS
Exact-ticket governance packet/verifier: PASS
Exact-ticket decision-artifact packet/verifier: PASS
Pre-action evidence aggregate packet/verifier: PASS
Violations: 0
All action authorizations: false
Final git status: only reports/ untracked

If this does not pass, stop and diagnose. Do not implement the next milestone on an unverified base.

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

Never commit if the milestone verifier fails under --require-pass.

Expected final status after commit and push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Important lesson from HANDOFF_105:

Do not allow a script to commit after a builder or verifier failure. Use checked command wrappers or manually stop before commit.

14. Static Safety Expectations

The no-mutation gate includes static checks for direct broker mutation call sites in current non-exempt execution-related code.

Known frozen legacy exceptions:

run_h024_one_shot_demo_canary.py
h024_one_shot_demo_canary.py
log_h024_mt5_terminal_preflight.py

Interpretation:

These are frozen legacy/pre-gate artifacts. They are not authorized by the no-mutation gate. They must not be treated as current execution adapters. Do not add new exceptions casually. If a future exception is proposed, fail closed and require explicit documentation.

For decision/governance/evidence code specifically, no new broker mutation call sites are acceptable.

Do not introduce:

order_send
order_check
positions_get mutation helpers
orders_get mutation helpers
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

Do not assume failure is bad. Read verifier semantics. Flat inventory may be allowed by some upstream packets, but no packet authorizes a new entry.

For exact-ticket close/modify governance and pre-action evidence specifically, a flat/no-canary state may be safe operationally but does not satisfy exact-ticket canary identity matching for close/modify governance/evidence review. It must fail closed unless the spec is explicitly changed in a future read-only milestone.

For the exact-ticket decision artifact validator specifically, a well-formed decision artifact only validates artifact coherence. It does not authorize action. Any artifact that implies immediate action authorization must fail closed.

For the pre-action evidence aggregate specifically, a PASS only confirms that the pre-action evidence bundle is coherent for read-only review and all action paths remain blocked.

17. Recommended Next Milestone

Next milestone should be:

H024 exact-ticket canary close/modify read-only bar-age and exit-condition evidence supervisor

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

Convert the operator statement that the exact XAUUSDm canary has been open for over 3 bars into a structured, read-only evidence packet, while still authorizing no action.

The packet should consume/reference:

Runtime no-mutation safety gate
Unified read-only post-canary runtime supervision
Exact-ticket close/modify governance packet
Exact-ticket decision artifact validator packet
Pre-action evidence aggregate packet
Fresh runtime exposure/inventory evidence
Fresh runtime account risk/margin evidence
Fresh runtime tick/spread evidence

It should validate or explicitly classify:

exact ticket/identifier 4413054432
exact XAUUSDm canary identity
position still observed
position open time if available
bar timeframe used for age calculation
whether over-three-bars is machine-validated
whether over-three-bars is operator-reported only
current unrealized PnL snapshot
current spread/tick freshness snapshot
account risk/margin snapshot
no extra H024 exposure/order
no H024 USDJPY exposure/order
all action authorizations remain false

If bar-age cannot be machine-validated from read-only data, the packet may record operator-reported over-three-bars evidence but must clearly mark it as operator-reported, not machine-validated.

Passing state should mean:

bar-age / exit-condition evidence is coherent for read-only operator review
all action paths remain blocked
no broker mutation is authorized

Passing state must not mean:

close is authorized
modify is authorized
order_check is authorized
order_send is authorized
broker request construction is authorized

Suggested module name:

quantcore/execution/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.py

Suggested scripts:

scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py

Suggested tests:

tests/test_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.py

Suggested docs:

docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE.md

Suggested report path:

reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl

Suggested commit message:

Add H024 exact-ticket close modify bar-age exit-condition evidence

Suggested next prompt:

Let’s implement the H024 exact-ticket canary close/modify read-only bar-age and exit-condition evidence supervisor. It must consume the no-mutation gate, unified runtime supervision, exact-ticket close/modify governance packet, exact-ticket decision artifact validator, and pre-action evidence aggregate. It must preserve exact ticket/identifier 4413054432 and exact XAUUSDm canary identity, classify whether the position being open for over 3 bars is machine-validated or operator-reported only, include current read-only PnL/risk/spread evidence, and fail closed on missing, malformed, stale, ambiguous, inconsistent, or unsafe evidence. It must not build a broker request and must authorize no broker mutation, no order_check, no order_send, no entries, no close/modify, no XAUUSD order, no USDJPY order, and no trading loop. Include module, verifier, tests, scripts, and docs. Keep reports/ untracked.
18. Explicit Next-Milestone Failure Modes

The bar-age and exit-condition evidence supervisor must fail closed if:

no-mutation gate packet missing
no-mutation gate packet malformed
no-mutation gate packet not PASS
no-mutation gate opens mutation path
unified runtime supervision packet missing
unified runtime supervision packet malformed
unified runtime supervision packet not PASS
exact-ticket governance packet missing
exact-ticket governance packet malformed
exact-ticket governance packet not PASS
exact-ticket decision artifact packet missing
exact-ticket decision artifact packet malformed
exact-ticket decision artifact packet not PASS
pre-action evidence aggregate packet missing
pre-action evidence aggregate packet malformed
pre-action evidence aggregate packet not PASS
any upstream packet stale
any upstream packet has embedded violations
any upstream packet has authorization true
upstream exact ticket mismatch
upstream exact identifier mismatch
upstream runtime symbol mismatch
upstream model symbol mismatch
upstream side/type mismatch
upstream volume mismatch
upstream magic mismatch
exact canary not observed when required
H024 USDJPY exposure/order observed
additional H024 exposure/order observed
bar timeframe missing or malformed if machine validation is claimed
machine-validated bar age claimed without sufficient read-only evidence
operator-reported over-three-bars evidence treated as machine-validated without proof
decision artifact implies current close/modify authorization
governance packet implies current close/modify authorization
pre-action aggregate implies current close/modify authorization
bar-age packet implies current close/modify authorization
bar-age packet implies order_check authorization
bar-age packet implies order_send authorization
bar-age packet implies broker mutation authorization
bar-age packet implies trading loop authorization
bar-age packet implies automatic execution authorization
any authorization true
effective_new_entries_blocked not true
malformed JSONL
wrong schema version
wrong strategy
wrong packet type
--require-pass with record verdict not PASS

It must pass only as a read-only evidence packet. PASS should mean:

bar-age / exit-condition evidence is coherent for operator review
all action paths remain blocked
no broker mutation is authorized

It must not mean:

close is authorized
modify is authorized
order_check is authorized
order_send is authorized
broker request construction is authorized
19. How The Next AI Should Start

The next AI should respond:

Understood. Continuing from HANDOFF_105 at validated implementation commit e370a60. Current state is read-only H024 post-canary runtime supervision with a no-mutation gate, exact-ticket close/modify governance specification packet, exact-ticket close/modify decision artifact validator, and exact-ticket close/modify pre-action evidence aggregate; all broker mutation and trading paths remain blocked. Please run the HANDOFF_105 verification block so I can confirm local state before the next read-only milestone.

Then provide the verification block from Section 11.

20. Final Reminder

This handoff is deliberately conservative.

Current H024 posture:

Observe only.
Supervise only.
Specify governance only.
Validate decision artifacts only.
Aggregate read-only pre-action evidence only.
Fail closed.
Authorize nothing.
Keep reports/ untracked.

