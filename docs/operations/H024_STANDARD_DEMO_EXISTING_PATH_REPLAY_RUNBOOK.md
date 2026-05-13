# H024 Standard-Demo Existing Path Replay Runbook

## Purpose

`H024_STANDARD_DEMO_EXISTING_PATH_REPLAY` is a read-only continuation milestone after `H024_STANDARD_DEMO_EXISTING_PATH_MAP`.

It verifies that the repository already contains a real H024 standard-demo path and replays that path as an evidence packet without creating a standalone parallel scaffold.

## Inputs

The replay consumes:

- `reports/h024_standard_demo_existing_path_map.jsonl`

The latest JSONL record must show:

- `verdict: PASS`
- `operator_state: H024_STANDARD_DEMO_EXISTING_PATH_MAP_ACCEPTED`
- `existing_path_map_state: REAL_H024_STANDARD_DEMO_PATH_IDENTIFIED`
- `ready_for_existing_path_replay: true`
- `ready_for_demo_order_check_gate: false`
- all broker/trading authorization fields false

## Existing path sequence

The replay validates the presence of the existing H024 path:

1. `quantcore/execution/h024_order_intent_simulation.py`
2. `quantcore/execution/h024_dry_run.py`
3. `quantcore/execution/h024_dry_run_log.py`
4. `quantcore/execution/h024_runtime_safety_lockout.py`
5. `quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py`
6. `quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py`
7. `quantcore/execution/h024_safety_supervisor_spec.py`
8. `quantcore/execution/h024_manual_approval_checkpoint.py`
9. `quantcore/execution/h024_broker_request_draft_envelope.py`

The replay also validates the standard-demo result documents and focused existing H024 tests.

## Latest existing artifact before broker mutation

The replay identifies this as the latest existing standard-demo artifact before any future broker mutation gate:

- `docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md`

This is still not an execution authorization.

## Hard safety boundaries

This milestone is read-only only.

It does not add, call, or authorize:

- MT5 order-check execution
- MT5 order-send execution
- MT5 symbol selection
- executable trade request construction
- new entries
- close-all
- automatic close/modify
- unattended trading loops
- live-money support
- scaling
- martingale
- grid
- automatic position creation

All emitted packets must keep:

- `trading_authorized: false`
- `broker_mutation_authorized: false`
- `order_check_authorized: false`
- `order_send_authorized: false`
- `symbol_select_authorized: false`
- `executable_trade_request_constructed: false`

## Commands

From the repository root:

```powershell
python scripts/build_h024_standard_demo_existing_path_map_jsonl.py
python -m pytest tests/test_h024_standard_demo_existing_path_map.py tests/test_h024_standard_demo_existing_path_replay.py -q
python scripts/build_h024_standard_demo_existing_path_replay_jsonl.py --run-existing-tests
Outputs

Generated runtime evidence:

reports/h024_standard_demo_existing_path_replay.jsonl
reports/h024_standard_demo_existing_path_replay.txt

reports/ remains untracked.

Expected PASS state

Expected accepted replay state:

verdict: PASS
operator_state: H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_ACCEPTED
existing_path_replay_state: REAL_H024_STANDARD_DEMO_PATH_REPLAYED_READ_ONLY
ready_for_existing_path_replay: true
ready_for_demo_order_check_gate: false
ready_for_demo_order_check_gate_design: true
next_target: H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN
Next milestone

Next recommended milestone:

H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN

That milestone must remain read-only unless the operator separately authorizes a new staged scope.
