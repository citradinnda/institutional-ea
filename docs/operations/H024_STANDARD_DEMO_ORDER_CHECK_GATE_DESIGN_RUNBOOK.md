# H024 Standard-Demo Order-Check Gate Design Runbook

## Purpose

`H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN` is a read-only design milestone after `H024_STANDARD_DEMO_EXISTING_PATH_REPLAY`.

It defines the future demo order-check gate contract, packet schema, preconditions, fail-closed rules, and operator authorization requirements.

It does not implement or invoke the future broker preflight call.

## Required input

The design packet consumes:

- `reports/h024_standard_demo_existing_path_replay.jsonl`

The latest replay record must show:

- `verdict: PASS`
- `stage: H024_STANDARD_DEMO_EXISTING_PATH_REPLAY`
- `operator_state: H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_ACCEPTED`
- `existing_path_replay_state: REAL_H024_STANDARD_DEMO_PATH_REPLAYED_READ_ONLY`
- `ready_for_demo_order_check_gate_design: true`
- `ready_for_demo_order_check_gate: false`
- all trading and broker-mutation authorization fields false

## Required existing artifacts

The gate design validates the presence of the existing H024 replay chain, including:

- existing replay builder
- existing replay tests
- existing replay runbook
- existing MT5 request-shape preview envelope result
- existing order-canary human approval result
- existing broker request draft envelope result
- existing broker request draft envelope module
- manual approval checkpoint module
- runtime safety supervisor modules
- no-mutation safety gate module

## Future gate schema

The future gate must require:

- explicit operator authorization packet
- exact authorization scope: `H024_STANDARD_DEMO_ORDER_CHECK_GATE_ONLY`
- authorization ID
- authorization creation and expiry timestamps
- existing path replay PASS report
- broker request draft envelope artifact
- manual approval checkpoint artifact
- fresh runtime safety artifacts
- demo-only account mode
- allowed active demo symbol
- side and volume
- risk and heat limits

## Allowed symbols

Allowed active research/demo symbols:

- `USDJPYm` / `USDJPY`
- `XAUUSDm` / `XAUUSD`

Banned unless future pre-registered research re-tests them:

- `EURUSDm`
- `GBPUSDm`
- `US500m`

## Risk constraints

The future gate contract preserves:

- max risk per trade: `0.5%`
- max portfolio heat: `1.0%`

These values must not be loosened to rescue a blocked trade.

## Fail-closed conditions

The future gate must fail closed for:

- missing or malformed operator authorization
- ambiguous authorization scope
- expired authorization
- authorization scope not exactly matching the gate-only scope
- replay report not PASS
- missing or stale safety artifacts
- missing or failed manual approval checkpoint
- missing or failed broker request draft envelope
- symbol not allowed
- banned symbol
- non-demo account mode
- missing or invalid side/volume
- exceeded risk or heat limits
- any order-send authorization
- any symbol-selection authorization
- any live-money authorization
- any executable dispatch authorization

## Hard safety boundaries

This milestone is design-only.

It does not authorize:

- trading
- broker mutation
- order-check invocation
- order-send invocation
- symbol selection
- executable trade request construction
- new entries
- close or modify actions
- live-money support
- unattended loops
- automatic retries
- automatic dispatch

All output packets must keep:

- `trading_authorized: false`
- `broker_mutation_authorized: false`
- `order_check_authorized: false`
- `order_send_authorized: false`
- `symbol_select_authorized: false`
- `executable_trade_request_constructed: false`

## Commands

From repository root:

```powershell
python scripts/build_h024_standard_demo_existing_path_map_jsonl.py
python scripts/build_h024_standard_demo_existing_path_replay_jsonl.py --run-existing-tests
python -m pytest tests/test_h024_standard_demo_existing_path_replay.py tests/test_h024_standard_demo_order_check_gate_design.py -q
python scripts/build_h024_standard_demo_order_check_gate_design_jsonl.py
Outputs

Runtime evidence:

reports/h024_standard_demo_order_check_gate_design.jsonl
reports/h024_standard_demo_order_check_gate_design.txt

reports/ remains untracked.

Expected PASS state

Expected accepted design state:

verdict: PASS
operator_state: H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_ACCEPTED
order_check_gate_design_state: READ_ONLY_GATE_CONTRACT_DEFINED
ready_for_order_check_gate_design: true
ready_for_order_check_gate_operator_authorization_packet_design: true
ready_for_demo_order_check_gate: false
ready_for_demo_order_check_gate_implementation: false
ready_for_demo_order_check_invocation: false
next_target: H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN
Next milestone

Recommended next milestone:

H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN

That next milestone must also remain read-only unless the operator separately authorizes a staged broker preflight scope.
