# H024 Runtime Safety Aggregate Supervisor

## Purpose

The H024 runtime safety aggregate supervisor is the read-only single aggregate operator verdict for the current H024 runtime safety stack.

It consumes or references:

- runtime safety lockout reader
- runtime safety heartbeat packet
- runtime tick/spread safety supervisor
- runtime exposure/inventory safety supervisor
- runtime account risk/margin safety supervisor

The aggregate supervisor exists to prevent cherry-picking a single passing packet while another runtime safety packet is failing. It requires every upstream packet to pass, verifies upstream freshness, merges embedded violations, and preserves all no-execution boundaries.

This packet does not authorize trading.

## Read-Only Boundary

The aggregate supervisor may call upstream read-only safety packet builders.

Through those upstream packets, it may read:

- account information
- terminal information
- symbol information
- ticks
- positions
- orders

It must not call:

- `symbol_select`
- `order_check`
- `order_send`
- any entry path
- any close path
- any modify path
- any trading loop
- any broker mutation path

## Required Upstream Packets

The aggregate requires:

- `H024_RUNTIME_SAFETY_HEARTBEAT`
- `H024_RUNTIME_TICK_SPREAD_SAFETY_SUPERVISOR`
- `H024_RUNTIME_EXPOSURE_INVENTORY_SAFETY_SUPERVISOR`
- `H024_RUNTIME_ACCOUNT_RISK_MARGIN_SAFETY_SUPERVISOR`

It also references the local runtime lockout reader module:

- `quantcore.execution.h024_runtime_safety_lockout`

## Fail-Closed Conditions

The packet fails closed if any of these conditions occur:

- a required upstream module cannot be referenced
- a required upstream packet is missing
- a required upstream packet is malformed
- a required upstream packet has the wrong strategy
- a required upstream packet has the wrong packet type
- a required upstream packet verdict is not `PASS`
- a required upstream packet is stale
- a required upstream packet contains embedded violations
- a required upstream packet does not preserve `effective_new_entries_blocked=True`
- a required upstream packet has any broker/order/trading authorization missing or not false
- the aggregate itself has any broker/order/trading authorization missing or not false

## Freshness

The default maximum upstream packet age is `300` seconds.

A small future timestamp tolerance of `60` seconds is allowed to absorb MT5/runtime clock jitter and local collection ordering.

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

`RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED`

All upstream runtime safety packets passed, were fresh, contained no embedded violations, and preserved no-execution boundaries. Trading remains unauthorized.

`FAIL_CLOSED_RUNTIME_SAFETY_AGGREGATE_BLOCKED`

At least one upstream or aggregate safety check failed. Trading remains unauthorized and blocked.

## Commands

Build packet:

```powershell
python scripts\build_h024_runtime_safety_aggregate_supervisor_jsonl.py

Verify packet:

python scripts\verify_h024_runtime_safety_aggregate_supervisor_jsonl.py reports\h024_runtime_safety_aggregate_supervisor.jsonl --require-pass

Focused tests:

python -m pytest tests\test_h024_runtime_safety_aggregate_supervisor.py

Full suite:

python -m pytest
Interpretation

A passing aggregate supervisor packet does not prove strategy edge, live readiness, USDJPY order readiness, or trading-loop readiness. It only proves that the current read-only runtime safety stack is coherent at one observation point.

The hard boundary remains:

no second H024 entry
no live order
no USDJPY order
no scaling
no order_check
no order_send
no close/modify unless separately governed and exact-ticket locked
no trading loop