# H024 Unified Read-Only Post-Canary Runtime Supervision

## Purpose

The H024 unified read-only post-canary runtime supervision packet is the operator-facing wrapper for the post-canary runtime state.

It combines:

- the existing H024 one-shot demo canary read-only supervision runner
- the H024 runtime safety aggregate supervisor

It emits one JSONL packet with one fail-closed operator verdict and one operator next action.

This packet does not authorize trading.

## Inputs

The unified packet consumes or references:

- `scripts/run_h024_one_shot_demo_canary_read_only_supervision.py`
- `scripts/verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py`
- `quantcore.execution.h024_runtime_safety_aggregate_supervisor`
- `quantcore.execution.h024_runtime_safety_lockout`

The canary supervision runner remains the source for canary lifecycle/supervision state.

The runtime safety aggregate remains the source for runtime safety state.

## Expected Known Canary Identity

The known standard-demo canary identity is:

- server: `Exness-MT5Trial6`
- account currency: `USD`
- runtime symbol: `XAUUSDm`
- model symbol: `XAUUSD`
- side: sell
- MT5 position type: `1`
- volume: `0.01`
- magic: `240024`
- ticket/identifier: `4413054432`
- entry deal: `3788869526`
- open price: `4728.4490000000005`
- stop loss: `4817.394`

If the canary is observed, it must be this exact canary. A flat H024 inventory state can pass only if all upstream read-only supervision and safety packets pass. A flat state does not authorize a new entry.

## Read-Only Boundary

The unified runner may run or consume the existing read-only canary supervision runner and the read-only runtime safety aggregate supervisor.

It must not call:

- `symbol_select`
- `order_check`
- `order_send`
- any entry path
- any close path
- any modify path
- any trading loop
- any broker mutation path

## Fail-Closed Conditions

The packet fails closed if any of these conditions occur:

- canary read-only supervision records are missing
- canary read-only supervision does not pass
- canary read-only supervision contains embedded violations
- runtime safety aggregate packet is missing
- runtime safety aggregate packet type is unexpected
- runtime safety aggregate verdict is not `PASS`
- runtime safety aggregate contains embedded violations
- runtime safety aggregate does not preserve `effective_new_entries_blocked=True`
- observed canary identity is inconsistent
- any broker/order/trading authorization is missing or not false
- the operator next action is not the read-only continue-supervision action under require-pass verification

## Authorization Semantics

These fields must remain false:

- `broker_mutation_authorized`
- `order_check_authorized`
- `order_send_authorized`
- `entry_authorized`
- `close_modify_authorized`
- `xauusd_order_authorized`
- `usdjpy_order_authorized`
- `trading_loop_authorized`
- `automatic_execution_authorized`

`effective_new_entries_blocked` must remain true.

## Operator States

`UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED`

Canary read-only supervision passed, runtime safety aggregate passed, exact known canary identity was coherent if observed, and all execution authorizations remained false.

`FAIL_CLOSED_UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_BLOCKED`

At least one canary supervision, runtime aggregate, identity, or authorization check failed.

## Operator Next Actions

`READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED`

The only passing next action. It means continue observation only. It does not authorize entries, exits, close/modify, USDJPY order, XAUUSD new order, live deployment, or a trading loop.

`FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED`

The fail-closed next action. It means human review is required and trading remains unauthorized.

## Commands

Build packet:

```powershell
python scripts\build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py

Verify packet:

python scripts\verify_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py reports\h024_unified_read_only_post_canary_runtime_supervision.jsonl --require-pass

Focused tests:

python -m pytest tests\test_h024_unified_read_only_post_canary_runtime_supervision.py

Full suite:

python -m pytest
Interpretation

A passing unified packet does not prove strategy edge, live readiness, USDJPY order readiness, close/modify readiness, or trading-loop readiness. It only proves that the read-only post-canary supervision state and runtime safety aggregate are coherent at one observation point.

The hard boundary remains:

no second H024 entry
no live order
no USDJPY order
no scaling
no order_check
no order_send
no close/modify unless separately governed and exact-ticket locked
no trading loop