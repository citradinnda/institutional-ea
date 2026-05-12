# H024 Runtime Tick And Spread Safety Supervisor

## Purpose

The H024 runtime tick and spread safety supervisor is a read-only market-data safety layer for the current H024 runtime universe:

- `XAUUSDm` mapped to model symbol `XAUUSD`
- `USDJPYm` mapped to model symbol `USDJPY`

It consumes or references the runtime safety heartbeat packet and runtime safety lockout reader. It verifies that both runtime symbols are readable, already visible/selection-ready, have valid bid/ask ticks, have positive spreads, stay within configured spread thresholds, and have fresh tick timestamps where available.

This supervisor does not authorize trading. A passing packet only means that current market-data observations are coherent enough for a read-only safety layer.

## Upstream Runtime Safety Dependencies

The packet references:

- `quantcore.execution.h024_runtime_safety_lockout`
- `quantcore.execution.h024_runtime_safety_heartbeat`

The runtime heartbeat must pass before tick/spread checks are considered safe to evaluate.

## Read-Only Boundary

The supervisor may call:

- `MetaTrader5.initialize()` indirectly through the heartbeat
- `MetaTrader5.account_info()` indirectly through the heartbeat
- `MetaTrader5.terminal_info()` indirectly through the heartbeat
- `MetaTrader5.last_error()` indirectly through the heartbeat
- `MetaTrader5.version()` indirectly through the heartbeat
- `MetaTrader5.symbol_info()`
- `MetaTrader5.symbol_info_tick()`

The supervisor must not call:

- `symbol_select`
- `order_check`
- `order_send`
- any entry path
- any close path
- any modify path
- any trading loop
- any broker mutation path

If a symbol is not already visible/readable, the supervisor fails closed. It does not attempt to select or repair the symbol state.

## Default Thresholds

`XAUUSDm`:

- model symbol: `XAUUSD`
- max spread: `5000.0` points
- max tick age: `3600.0` seconds

`USDJPYm`:

- model symbol: `USDJPY`
- max spread: `500.0` points
- max tick age: `3600.0` seconds

These are operational safety thresholds, not alpha or edge assumptions.

## Fail-Closed Conditions

The packet fails closed if any of these conditions occur:

- Runtime safety heartbeat fails.
- Runtime safety lockout reader cannot be referenced.
- Runtime safety heartbeat module cannot be referenced.
- Required symbol set is not exactly `XAUUSDm` and `USDJPYm`.
- `symbol_info()` is unavailable for either symbol.
- `symbol_info_tick()` is unavailable for either symbol.
- Symbol is not already visible/readable.
- Point size is missing, non-finite, or non-positive.
- Bid is missing, non-finite, or non-positive.
- Ask is missing, non-finite, or non-positive.
- Ask is not above bid.
- Spread is not positive.
- Spread exceeds configured threshold.
- Tick timestamp is unavailable.
- Tick timestamp is stale beyond threshold.
- Any broker/order/trading authorization is missing or not false.

## Authorization Semantics

These fields must remain false:

- `symbol_select_authorized`
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

`TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED`

The heartbeat and symbol market-data checks passed. Trading remains unauthorized.

`FAIL_CLOSED_TICK_SPREAD_SUPERVISOR_BLOCKED`

One or more runtime market-data safety checks failed or upstream heartbeat failed. Trading remains unauthorized and blocked.

## Commands

Build packet:

```powershell
python scripts\build_h024_runtime_tick_spread_safety_supervisor_jsonl.py

Verify packet:

python scripts\verify_h024_runtime_tick_spread_safety_supervisor_jsonl.py reports\h024_runtime_tick_spread_safety_supervisor.jsonl --require-pass

Focused tests:

python -m pytest tests\test_h024_runtime_tick_spread_safety_supervisor.py

Full suite:

python -m pytest
Interpretation

A passing tick/spread supervisor packet does not prove strategy edge, live readiness, USDJPY order readiness, or trading-loop readiness. It only proves read-only runtime tick and spread observability under the expected demo account context.

The hard boundary remains:

no second H024 entry
no live order
no USDJPY order
no scaling
no symbol_select repair path
no order_check
no order_send
no close/modify unless separately governed and exact-ticket locked
no trading loop