# HANDOFF_122 - H024 Standard-Demo Order-Check Gate Design Complete; Continue With Operator Authorization Packet Design

This handoff supersedes HANDOFF_121 for continuation context, while preserving all HANDOFF_120 and HANDOFF_121 hard safety boundaries.

This handoff is intentionally self-contained. The next AI should not require hidden chain-of-thought or prior chat messages.

## 1. Repository state

Repository:

```text
C:\Users\equin\Documents\institutional-ea

Branch:

main

Latest committed state after this handoff sequence:

29cfa90 Track H024 standard-demo order-check gate design tests and runbook
29d7e55 Add H024 standard-demo order-check gate design
d5a9430 Track H024 standard-demo existing path replay tests and runbook
d0255e2 Add H024 standard-demo existing path replay
bc532e6 Add handoff document #121
9a84604 Add H024 standard-demo existing path map
862d063 Add demo automation readiness bridge

Expected final git status before adding this handoff:

?? docs/operations/INERT_DEMO_ENTRY_REQUEST_PREVIEW_RUNBOOK.md
?? reports/
?? scripts/build_inert_demo_entry_request_preview_jsonl.py
?? tests/test_inert_demo_entry_request_preview.py

Important:

reports/ is generated runtime evidence. Keep it untracked.
The standalone inert preview scaffold files are intentionally untracked:
docs/operations/INERT_DEMO_ENTRY_REQUEST_PREVIEW_RUNBOOK.md
scripts/build_inert_demo_entry_request_preview_jsonl.py
tests/test_inert_demo_entry_request_preview.py
Do not commit the standalone inert preview scaffold unless explicitly refactored to consume the real H024 standard-demo path.
Do not build a parallel scaffold when the real H024 standard-demo path already exists.
2. Critical correction carried forward

A previous AI incorrectly inferred a new standalone demo-automation scaffold before inspecting the actual repository path.

Correct rule:

Inspect the repository first before implementing.
Do not infer architecture from handoffs alone.
Use the existing H024 standard-demo path.
Do not create a parallel path.

The real H024 standard-demo path exists under:

quantcore/execution/
docs/operations/H024_STANDARD_DEMO_*
tests/test_h024_*
3. Source-of-truth operational state

The old H024 canary trade was:

Runtime symbol : XAUUSDm
Model symbol   : XAUUSD
Side           : sell
Volume         : 0.01
Ticket         : 4413054432
Identifier     : 4413054432
Magic          : 240024
Demo server    : Exness-MT5Trial6

It was closed by H025 Stage 4 and verified closed by H025 Stage 5.

Current truth:

No open H024 canary trade exists.
Exact ticket 4413054432 is not open.
H024 position count is 0.
H024 order count is 0.

Do not reopen a canary to satisfy old observer assumptions.

Do not rerun H025 Stage 4.

4. Hard safety boundaries

H024 remains read-only unless a new explicit staged scope is authorized.

Do not add or execute:

mt5.order_check
mt5.order_send
mt5.symbol_select
executable trade request construction
new entries
close-all
automatic close/modify
unattended loops
live-money support
scaling
martingale
grid
automatic position creation

Any future broker mutation requires a new explicit operator authorization and a separate staged scope.

The next target is still read-only:

H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN

This next milestone must design the authorization packet schema only. It must not call mt5.order_check.

5. Strategy and symbol constraints

Allowed active research/demo symbols:

USDJPYm / USDJPY
XAUUSDm / XAUUSD

Banned unless a future pre-registered hypothesis re-tests them:

EURUSDm
GBPUSDm
US500m

Carry-forward strategy/risk principles:

H024/H020 route is not "model sends order directly."
Existing path uses intent simulation, dry-run, approval, request-envelope, and safety supervisors.
Deterministic risk controls are mandatory.
Cost model assumptions must not be casually changed.
Portfolio heat matters.
Do not lower modeled costs to rescue a result.
Max risk per trade remains 0.5%.
Max portfolio heat remains 1.0%.
6. Completed milestone: existing path replay

Completed across:

d0255e2 Add H024 standard-demo existing path replay
d5a9430 Track H024 standard-demo existing path replay tests and runbook

Tracked files:

scripts/build_h024_standard_demo_existing_path_replay_jsonl.py
tests/test_h024_standard_demo_existing_path_replay.py
docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_RUNBOOK.md

Validation:

17 passed
95 passed

Replay result:

verdict                                           : PASS
stage                                             : H024_STANDARD_DEMO_EXISTING_PATH_REPLAY
operator_state                                    : H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_ACCEPTED
existing_path_replay_state                        : REAL_H024_STANDARD_DEMO_PATH_REPLAYED_READ_ONLY
operator_next_action                              : PROCEED_TO_H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_READ_ONLY
consumed_path_map_report                          : reports\h024_standard_demo_existing_path_map.jsonl
path_map_verdict                                  : PASS
path_map_operator_state                           : H024_STANDARD_DEMO_EXISTING_PATH_MAP_ACCEPTED
path_map_existing_path_map_state                  : REAL_H024_STANDARD_DEMO_PATH_IDENTIFIED
latest_existing_artifact_before_broker_mutation   : docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md
latest_existing_artifact_exists                   : True
ready_for_existing_path_replay                    : True
ready_for_demo_order_check_gate                   : False
ready_for_demo_order_check_gate_design            : True
next_target                                       : H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN
trading_authorized                                : False
broker_mutation_authorized                        : False
order_check_authorized                            : False
order_send_authorized                             : False
symbol_select_authorized                          : False
executable_trade_request_constructed              : False
new_entry_authorized                              : False
close_modify_authorized                           : False
read_only_replay_only                             : True
violation_count                                   : 0

Existing path sequence confirmed:

quantcore/execution/h024_order_intent_simulation.py
quantcore/execution/h024_dry_run.py
quantcore/execution/h024_dry_run_log.py
quantcore/execution/h024_runtime_safety_lockout.py
quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py
quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py
quantcore/execution/h024_safety_supervisor_spec.py
quantcore/execution/h024_manual_approval_checkpoint.py
quantcore/execution/h024_broker_request_draft_envelope.py
7. Completed milestone: order-check gate design

Completed across:

29d7e55 Add H024 standard-demo order-check gate design
29cfa90 Track H024 standard-demo order-check gate design tests and runbook

Tracked files:

scripts/build_h024_standard_demo_order_check_gate_design_jsonl.py
tests/test_h024_standard_demo_order_check_gate_design.py
docs/operations/H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_RUNBOOK.md

Validation:

8 passed
16 passed
95 passed

Design result:

verdict                                                : PASS
stage                                                  : H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN
operator_state                                         : H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_ACCEPTED
order_check_gate_design_state                          : READ_ONLY_GATE_CONTRACT_DEFINED
operator_next_action                                   : PROCEED_TO_H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN
consumed_existing_path_replay_report                   : reports\h024_standard_demo_existing_path_replay.jsonl
existing_path_replay_verdict                           : PASS
existing_path_replay_operator_state                    : H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_ACCEPTED
existing_path_replay_state                             : REAL_H024_STANDARD_DEMO_PATH_REPLAYED_READ_ONLY
latest_existing_artifact_before_broker_mutation        : docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md
ready_for_order_check_gate_design                      : True
ready_for_order_check_gate_authorization_packet_design : True
ready_for_demo_order_check_gate                        : False
ready_for_demo_order_check_gate_implementation         : False
ready_for_demo_order_check_invocation                  : False
next_target                                            : H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN
trading_authorized                                     : False
broker_mutation_authorized                             : False
order_check_authorized                                 : False
order_send_authorized                                  : False
symbol_select_authorized                               : False
executable_trade_request_constructed                   : False
new_entry_authorized                                   : False
close_modify_authorized                                : False
read_only_design_only                                  : True
violation_count                                        : 0

Required existing artifacts confirmed present:

scripts/build_h024_standard_demo_existing_path_replay_jsonl.py
tests/test_h024_standard_demo_existing_path_replay.py
docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_RUNBOOK.md
docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md
docs/operations/H024_STANDARD_DEMO_ORDER_CANARY_HUMAN_APPROVAL_RESULT.md
docs/operations/H024_STANDARD_DEMO_BROKER_REQUEST_DRAFT_ENVELOPE_RESULT.md
quantcore/execution/h024_broker_request_draft_envelope.py
quantcore/execution/h024_manual_approval_checkpoint.py
quantcore/execution/h024_runtime_safety_lockout.py
quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py
quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py
quantcore/execution/h024_runtime_account_risk_margin_safety_supervisor.py
quantcore/execution/h024_runtime_no_mutation_safety_gate.py
quantcore/execution/h024_safety_supervisor_spec.py

The design packet defined the future gate schema, including:

operator_authorization_packet
operator_authorization_id
authorization_scope
authorization_created_at_utc
authorization_expires_at_utc
existing_path_replay_report
broker_request_draft_envelope_artifact
manual_approval_checkpoint_artifact
runtime_safety_lockout_artifact
runtime_tick_spread_safety_artifact
runtime_exposure_inventory_safety_artifact
runtime_account_risk_margin_safety_artifact
runtime_no_mutation_safety_gate_artifact
symbol
model_symbol
runtime_symbol
side
volume
demo_server
account_mode
max_risk_per_trade_pct
max_portfolio_heat_pct

The required future authorization scope was defined as:

H024_STANDARD_DEMO_ORDER_CHECK_GATE_ONLY

The design explicitly does not permit:

order-check invocation
order-send invocation
symbol selection
position creation
position close
position modification
live-money support
unattended loop
automatic retry
automatic dispatch
8. Current reports generated but untracked

The following runtime evidence is generated and should remain untracked:

reports/h024_standard_demo_existing_path_map.jsonl
reports/h024_standard_demo_existing_path_replay.jsonl
reports/h024_standard_demo_existing_path_replay.txt
reports/h024_standard_demo_order_check_gate_design.jsonl
reports/h024_standard_demo_order_check_gate_design.txt

Do not commit reports/.

9. Next correct milestone

Next target:

H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN

Purpose:

Design the explicit operator authorization packet required before any future demo-only order_check gate can be implemented or invoked.

This is still design/read-only only.

It must not call:

mt5.order_check
mt5.order_send
mt5.symbol_select

It must not construct an executable trade request.

It must define and validate an authorization packet schema for a future staged scope only.

10. Acceptance criteria for next milestone

The next milestone should add:

scripts/build_h024_standard_demo_order_check_gate_operator_authorization_packet_design_jsonl.py
tests/test_h024_standard_demo_order_check_gate_operator_authorization_packet_design.py
docs/operations/H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN_RUNBOOK.md

The packet should consume:

reports/h024_standard_demo_order_check_gate_design.jsonl

It should require the consumed design report to be PASS with:

stage: H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN
operator_state: H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_ACCEPTED
order_check_gate_design_state: READ_ONLY_GATE_CONTRACT_DEFINED
ready_for_order_check_gate_operator_authorization_packet_design: True
ready_for_demo_order_check_gate: False
ready_for_demo_order_check_gate_implementation: False
ready_for_demo_order_check_invocation: False
trading_authorized: False
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
symbol_select_authorized: False
executable_trade_request_constructed: False
read_only_design_only: True

The new authorization packet design should define:

exact schema name, e.g. h024_standard_demo_order_check_gate_operator_authorization_packet_v1
required scope: H024_STANDARD_DEMO_ORDER_CHECK_GATE_ONLY
required operator identity field
required authorization ID
required human-readable authorization statement
required created timestamp
required expiry timestamp
required target symbol fields
required account mode demo_only
required max risk per trade 0.5%
required max portfolio heat 1.0%
required reference to existing path replay report
required reference to order-check gate design report
required non-authorization of order_send
required non-authorization of symbol_select
required non-authorization of live-money
required non-authorization of automatic retries
required non-authorization of unattended loops
fail-closed behavior for missing, malformed, stale, expired, ambiguous, widened, or contradictory authorization

Expected output reports:

reports/h024_standard_demo_order_check_gate_operator_authorization_packet_design.jsonl
reports/h024_standard_demo_order_check_gate_operator_authorization_packet_design.txt

Expected accepted state:

verdict: PASS
stage: H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN
operator_state: H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN_ACCEPTED
authorization_packet_design_state: READ_ONLY_AUTHORIZATION_PACKET_CONTRACT_DEFINED
ready_for_order_check_gate_authorization_packet_design: True
ready_for_demo_order_check_gate: False
ready_for_demo_order_check_gate_implementation: False
ready_for_demo_order_check_invocation: False
trading_authorized: False
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
symbol_select_authorized: False
executable_trade_request_constructed: False
read_only_design_only: True
violation_count: 0
next_target: H024_STANDARD_DEMO_ORDER_CHECK_GATE_AUTHORIZATION_PACKET_VALIDATOR
11. Required behavior for next AI

Before implementing anything:

git status --short
git log --oneline -10
git ls-files scripts | findstr /I "h024_standard_demo"
git ls-files tests | findstr /I "h024_standard_demo"
git ls-files docs/operations | findstr /I "H024_STANDARD_DEMO"

Then inspect:

scripts/build_h024_standard_demo_existing_path_map_jsonl.py
scripts/build_h024_standard_demo_existing_path_replay_jsonl.py
scripts/build_h024_standard_demo_order_check_gate_design_jsonl.py
tests/test_h024_standard_demo_existing_path_map.py
tests/test_h024_standard_demo_existing_path_replay.py
tests/test_h024_standard_demo_order_check_gate_design.py
docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_MAP_RUNBOOK.md
docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_RUNBOOK.md
docs/operations/H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_RUNBOOK.md

Do not infer architecture from handoffs alone.

Do not commit:

reports/
docs/operations/INERT_DEMO_ENTRY_REQUEST_PREVIEW_RUNBOOK.md
scripts/build_inert_demo_entry_request_preview_jsonl.py
tests/test_inert_demo_entry_request_preview.py

unless explicitly instructed and refactored into the real H024 path.

12. Exact prompt for next AI

Use this prompt:

Please continue from HANDOFF_122 on main. HANDOFF_122 supersedes older continuation context while preserving all HANDOFF_120 and HANDOFF_121 hard safety boundaries.

First inspect the repository before implementing anything:
- run git status --short
- run git log --oneline -10
- inspect scripts/build_h024_standard_demo_existing_path_map_jsonl.py
- inspect scripts/build_h024_standard_demo_existing_path_replay_jsonl.py
- inspect scripts/build_h024_standard_demo_order_check_gate_design_jsonl.py
- inspect tests/test_h024_standard_demo_existing_path_map.py
- inspect tests/test_h024_standard_demo_existing_path_replay.py
- inspect tests/test_h024_standard_demo_order_check_gate_design.py
- inspect docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_MAP_RUNBOOK.md
- inspect docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_RUNBOOK.md
- inspect docs/operations/H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_RUNBOOK.md
- inspect relevant quantcore/execution/h024_* safety and broker envelope modules

Do not infer architecture from handoffs alone.

Current truth:
- Old H024 canary XAUUSDm sell 0.01, ticket/identifier 4413054432, magic 240024, server Exness-MT5Trial6, is closed.
- H025 Stage 4 closed it.
- H025 Stage 5 verified it closed.
- There is no open H024 canary.
- Do not reopen it.
- Do not rerun H025 Stage 4.

Completed milestones:
- H024_STANDARD_DEMO_EXISTING_PATH_MAP is PASS.
- H024_STANDARD_DEMO_EXISTING_PATH_REPLAY is PASS.
- H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN is PASS.

Latest commits:
- 29cfa90 Track H024 standard-demo order-check gate design tests and runbook
- 29d7e55 Add H024 standard-demo order-check gate design
- d5a9430 Track H024 standard-demo existing path replay tests and runbook
- d0255e2 Add H024 standard-demo existing path replay
- bc532e6 Add handoff document #121
- 9a84604 Add H024 standard-demo existing path map

Current untracked files should remain untracked:
- reports/
- docs/operations/INERT_DEMO_ENTRY_REQUEST_PREVIEW_RUNBOOK.md
- scripts/build_inert_demo_entry_request_preview_jsonl.py
- tests/test_inert_demo_entry_request_preview.py

Next task:
Implement H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN.

This is read-only design only.

It must consume:
- reports/h024_standard_demo_order_check_gate_design.jsonl

It must verify that order-check gate design is PASS and that:
- trading_authorized is False
- broker_mutation_authorized is False
- order_check_authorized is False
- order_send_authorized is False
- symbol_select_authorized is False
- executable_trade_request_constructed is False
- ready_for_demo_order_check_gate is False
- ready_for_demo_order_check_gate_implementation is False
- ready_for_demo_order_check_invocation is False

It must define the future operator authorization packet schema for the exact future scope:
- H024_STANDARD_DEMO_ORDER_CHECK_GATE_ONLY

It must require:
- operator identity field
- authorization ID
- explicit scope field
- human-readable authorization statement
- created timestamp
- expiry timestamp
- target demo account mode
- target symbol fields
- risk and heat limits
- references to replay and order-check gate design artifacts
- explicit non-authorization of order_send
- explicit non-authorization of symbol_select
- explicit non-authorization of live-money
- explicit non-authorization of unattended loops
- explicit non-authorization of automatic retries

It must fail closed for missing, malformed, stale, expired, ambiguous, widened, or contradictory authorization.

Do not add mt5.order_check.
Do not add mt5.order_send.
Do not add mt5.symbol_select.
Do not construct executable trade requests.
Do not authorize trading.
Do not commit reports/.
Do not commit the standalone inert preview scaffold.

Final expected output:
- scripts/build_h024_standard_demo_order_check_gate_operator_authorization_packet_design_jsonl.py
- tests/test_h024_standard_demo_order_check_gate_operator_authorization_packet_design.py
- docs/operations/H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN_RUNBOOK.md
- validation output
- final git status with reports/ and inert scaffold untracked

