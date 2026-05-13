# HANDOFF_121 - H024 Standard-Demo Existing Path Map Complete; Continue With Existing Path Replay

This handoff supersedes HANDOFF_120 for continuation context, while preserving all HANDOFF_120 hard safety boundaries.

This handoff is intentionally self-contained. The next AI should not require hidden chain-of-thought or previous chat messages.

## 1. Current repository state

Repository:


C:\Users\equin\Documents\institutional-ea


Branch:


main


Latest path-map commit:


9a84604 Add H024 standard-demo existing path map


Expected final git state after this handoff commit:


On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
reports/
docs/operations/INERT_DEMO_ENTRY_REQUEST_PREVIEW_RUNBOOK.md
scripts/build_inert_demo_entry_request_preview_jsonl.py
tests/test_inert_demo_entry_request_preview.py


Important:

- eports/ is generated runtime evidence. Keep it untracked.
- The standalone inert preview scaffold files are intentionally left untracked for now.
- Do not commit the standalone inert preview scaffold unless it is explicitly refactored to consume the real H024 standard-demo path.

## 2. Critical correction

Previous AI made a mistake by inferring a new standalone demo-automation scaffold before inspecting the actual repository path.

The correct instruction for the next AI is:

**Inspect the repo first before implementing.**

Do not infer the trade path from handoffs alone.

The real H024 standard-demo path already exists in the repo under:


quantcore/execution/
docs/operations/H024_STANDARD_DEMO_*
tests/test_h024_*


The newly completed artifact is a read-only repo-inspection packet:


scripts/build_h024_standard_demo_existing_path_map_jsonl.py
tests/test_h024_standard_demo_existing_path_map.py
docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_MAP_RUNBOOK.md


Validation output:


9 passed
H024_STANDARD_DEMO_EXISTING_PATH_MAP verdict: PASS
Operator state: H024_STANDARD_DEMO_EXISTING_PATH_MAP_ACCEPTED
Existing path map state: REAL_H024_STANDARD_DEMO_PATH_IDENTIFIED
Ready for existing path replay: True
Ready for demo order_check gate: False
Next target: H024_STANDARD_DEMO_EXISTING_PATH_REPLAY
Trading authorized: False
Broker mutation authorized: False
Order check authorized: False
Order send authorized: False
Symbol select authorized: False
Executable trade request constructed: False
Violations: 0


## 3. Source-of-truth operational state from HANDOFF_120

The old H024 canary trade was:

- Runtime symbol: XAUUSDm
- Model symbol: XAUUSD
- Side: sell
- Volume: 0.01
- Ticket: 4413054432
- Identifier: 4413054432
- Magic: 240024
- Demo server: Exness-MT5Trial6

It was closed by H025 Stage 4 and verified closed by H025 Stage 5.

Current truth:

- No open H024 canary trade exists.
- Exact ticket 4413054432 is not open.
- H024 position count is 0.
- H024 order count is 0.
- Do not reopen a canary to satisfy old observer assumptions.
- Do not rerun H025 Stage 4.

## 4. Hard safety boundaries

H024 remains read-only unless a new explicit staged scope is authorized.

Do not add or execute:

- mt5.order_check
- mt5.order_send
- mt5.symbol_select
- executable trade request construction
- new entries
- close-all
- automatic close/modify
- unattended loops
- live-money support
- scaling
- martingale
- grid
- automatic position creation

Any future broker mutation requires a new explicit operator authorization and a separate staged scope.

The next step is still read-only:


H024_STANDARD_DEMO_EXISTING_PATH_REPLAY


It must replay the existing H024 path, not create a parallel scaffold.

## 5. Strategy and symbol constraints

The Strategy Graveyard defines the research lineage and symbol restrictions.

Allowed active research/demo symbols:

- USDJPYm / USDJPY
- XAUUSDm / XAUUSD

Banned unless a future pre-registered hypothesis re-tests them:

- EURUSDm
- GBPUSDm
- US500m

Carry-forward strategy/risk principles:

- H024/H020 route is not "model sends order directly."
- Existing path uses intent simulation, dry-run, approval, request-envelope, and safety supervisors.
- Deterministic risk controls are mandatory.
- Cost model assumptions must not be casually changed.
- Portfolio heat matters.
- Do not lower modeled costs to rescue a result.

## 6. Real H024 standard-demo path now identified

The passing path-map packet identifies this shortest existing route:

1. quantcore/execution/h024_order_intent_simulation.py
   - Existing H024 standard-demo action-intent validation using normalized symbols.

2. quantcore/execution/h024_dry_run.py
   - Existing broker-aware dry-run candidate conversion layer.

3. quantcore/execution/h024_dry_run_log.py
   - Existing dry-run action export/log layer.

4. quantcore/execution/h024_runtime_*_safety_supervisor.py
   - Runtime lockout, tick/spread, exposure, account/risk/margin, and safety-spec gates.

5. quantcore/execution/h024_manual_approval_checkpoint.py
   - Existing manual/operator approval checkpoint before any order-capable transition.

6. quantcore/execution/h024_broker_request_draft_envelope.py
   - Existing broker request draft/envelope layer before MT5 request-shape preview.

7. docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md
   - Existing MT5 request-shape preview result.

8. Future demo-only order_check gate
   - Not authorized yet.
   - Requires fresh explicit operator approval.

9. Future one-shot demo-only order_send gate
   - Not authorized yet.
   - Requires separate future operator approval.

## 7. Existing relevant files/docs/tests

Core source files:


quantcore/strategy/h020.py
quantcore/execution/h024_order_intent_simulation.py
quantcore/execution/h024_dry_run.py
quantcore/execution/h024_dry_run_log.py
quantcore/execution/h024_manual_approval_checkpoint.py
quantcore/execution/h024_broker_request_draft_envelope.py


Safety source files:


quantcore/execution/h024_runtime_safety_lockout.py
quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py
quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py
quantcore/execution/h024_safety_supervisor_spec.py


Important standard-demo docs:


docs/operations/H024_DEMO_EXECUTION_ADAPTER_DESIGN_SPEC.md
docs/operations/H024_STANDARD_DEMO_ORDER_INTENT_SIMULATION_RESULT.md
docs/operations/H024_STANDARD_DEMO_ORDER_READINESS_PACKET_RESULT.md
docs/operations/H024_STANDARD_DEMO_MANUAL_APPROVAL_CHECKPOINT_RESULT.md
docs/operations/H024_STANDARD_DEMO_BROKER_REQUEST_DRAFT_ENVELOPE_RESULT.md
docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md
docs/operations/H024_STANDARD_DEMO_ORDER_CANARY_HUMAN_APPROVAL_RESULT.md


Relevant tests:


tests/test_h024_order_intent_simulation.py
tests/test_h024_dry_run_execution.py
tests/test_h024_dry_run_log.py
tests/test_h024_dry_run_action_verifier.py
tests/test_h024_manual_approval_checkpoint.py
tests/test_h024_runtime_safety_lockout.py
tests/test_h024_runtime_tick_spread_safety_supervisor.py
tests/test_h024_runtime_exposure_inventory_safety_supervisor.py
tests/test_h024_safety_supervisor_spec.py


## 8. What was completed after HANDOFF_120

H024 post-close observer/readiness adaptation was completed and committed before this handoff.

The project now accepts the old canary's absence as intentional when H025 post-close verification is PASS.

Key wording:


NO OPEN CANARY - INTENTIONALLY CLOSED BY H025


Then DEMO_AUTOMATION_READINESS_BRIDGE was completed and committed:


862d063 Add demo automation readiness bridge


Bridge result:


DEMO_AUTOMATION_READINESS_BRIDGE verdict: PASS
Operator state: DEMO_AUTOMATION_READINESS_BRIDGE_ACCEPTED
Bridge state: READY_FOR_INERT_DEMO_ENTRY_REQUEST_PREVIEW
Ready for inert demo entry preview: True
Controlled demo automation track open: True
Next target: INERT_DEMO_ENTRY_REQUEST_PREVIEW
Allowed demo symbols: ['USDJPYm', 'XAUUSDm']
Banned symbols: ['EURUSDm', 'GBPUSDm', 'US500m']
Max risk per trade pct: 0.5
Max portfolio heat pct: 1.0
Trading authorized: False
Broker mutation authorized: False
Order check authorized: False
Order send authorized: False
Symbol select authorized: False
Violations: 0


But after repo inventory, we corrected direction:

- Do not continue standalone inert preview as the main path.
- Rejoin the existing H024 standard-demo path.
- The standalone inert preview files are untracked and should stay untracked unless explicitly refactored to use real H024 path outputs.

## 9. Next correct milestone

Next target:


H024_STANDARD_DEMO_EXISTING_PATH_REPLAY


Purpose:

Replay the existing H024 standard-demo chain using existing repo modules and/or existing standard-demo evidence, read-only only.

Acceptance criteria:

- Consume eports/h024_standard_demo_existing_path_map.jsonl.
- Verify path-map verdict PASS.
- Run or statically validate existing tests for:
  - order intent simulation
  - dry run execution
  - dry run log/action verifier
  - manual approval checkpoint
  - broker request draft envelope
  - runtime safety supervisors
- Identify the latest existing artifact before broker mutation.
- Emit a replay packet:
  - eports/h024_standard_demo_existing_path_replay.jsonl
  - eports/h024_standard_demo_existing_path_replay.txt
- Keep:
  - 	rading_authorized: false
  - roker_mutation_authorized: false
  - order_check_authorized: false
  - order_send_authorized: false
  - symbol_select_authorized: false
  - executable_trade_request_constructed: false
- Next target after replay should be:
  - H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN
  - or equivalent exact name, but still read-only until explicit operator approval.

## 10. Required behavior for next AI

Before implementing anything:

1. Run git status --short.
2. Run git log --oneline -10.
3. Inspect the relevant repo files directly.
4. Do not rely only on handoffs.
5. Do not build parallel scaffolding if the repo already has an existing path.
6. Do not commit eports/.
7. Do not commit the standalone inert preview files unless user explicitly asks and they are refactored into the real H024 path.

Suggested inspection commands:


git status --short
git log --oneline -10
git ls-files quantcore/execution | findstr /I "h024"
git ls-files docs/operations | findstr /I "H024_STANDARD_DEMO"
git ls-files tests | findstr /I "h024"
python -m pytest tests/test_h024_standard_demo_existing_path_map.py -q
python scripts/build_h024_standard_demo_existing_path_map_jsonl.py


## 11. Prompt for next AI

Use this exact prompt:

Please continue from HANDOFF_121 on main. HANDOFF_121 supersedes older continuation context but preserves HANDOFF_120 hard safety boundaries.

First inspect the repository before implementing anything:
- run git status --short
- run git log --oneline -10
- inspect quantcore/execution/h024_order_intent_simulation.py
- inspect quantcore/execution/h024_dry_run.py
- inspect quantcore/execution/h024_dry_run_log.py
- inspect quantcore/execution/h024_manual_approval_checkpoint.py
- inspect quantcore/execution/h024_broker_request_draft_envelope.py
- inspect H024 runtime safety supervisor files
- inspect docs/operations/H024_STANDARD_DEMO_*
- inspect related 	ests/test_h024_*

Do not infer architecture from handoffs alone.

Current truth:
- Old H024 canary XAUUSDm sell 0.01, ticket/identifier 4413054432, magic 240024, server Exness-MT5Trial6, is closed.
- H025 Stage 4 closed it.
- H025 Stage 5 verified it closed.
- There is no open H024 canary.
- Do not reopen it.
- Do not rerun H025 Stage 4.

The completed path-map artifact is:
- scripts/build_h024_standard_demo_existing_path_map_jsonl.py
- 	ests/test_h024_standard_demo_existing_path_map.py
- docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_MAP_RUNBOOK.md

It passed:
- 9 passed
- verdict PASS
- operator_state H024_STANDARD_DEMO_EXISTING_PATH_MAP_ACCEPTED
- existing_path_map_state REAL_H024_STANDARD_DEMO_PATH_IDENTIFIED
- ready_for_existing_path_replay True
- ready_for_demo_order_check_gate False
- next_target H024_STANDARD_DEMO_EXISTING_PATH_REPLAY
- trading_authorized False
- broker_mutation_authorized False
- order_check_authorized False
- order_send_authorized False
- symbol_select_authorized False
- executable_trade_request_constructed False

Next task:
Implement H024_STANDARD_DEMO_EXISTING_PATH_REPLAY.

It must use the existing H024 standard-demo path:
1. quantcore/execution/h024_order_intent_simulation.py
2. quantcore/execution/h024_dry_run.py
3. quantcore/execution/h024_dry_run_log.py
4. H024 runtime safety supervisors
5. quantcore/execution/h024_manual_approval_checkpoint.py
6. quantcore/execution/h024_broker_request_draft_envelope.py
7. existing docs/operations/H024_STANDARD_DEMO_* result docs/tests

Do not build standalone scaffold.
Do not add mt5.order_check.
Do not add mt5.order_send.
Do not add mt5.symbol_select.
Do not construct executable trade requests.
Do not authorize trading.
Keep eports/ untracked.

Also keep the untracked standalone inert preview files uncommitted unless explicitly refactored into the real H024 path.

Final expected next output:
- source script
- focused tests
- runbook
- validation output
- final git status with eports/ untracked
