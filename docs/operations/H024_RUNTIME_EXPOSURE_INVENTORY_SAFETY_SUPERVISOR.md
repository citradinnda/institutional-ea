# H024 Runtime Exposure And Inventory Safety Supervisor

## Purpose

The H024 runtime exposure and inventory safety supervisor is a read-only broker-inventory safety layer.

It inspects MT5 positions and orders and verifies that any H024 exposure is either absent or is exactly the known standard-demo XAUUSDm canary:

- server: `Exness-MT5Trial6`
- account currency: `USD`
- runtime symbol: `XAUUSDm`
- model symbol: `XAUUSD`
- side: sell
- MT5 position type: `1`
- volume: `0.01`
- magic: `240024`
- ticket/identifier: `4413054432`

It also verifies that no H024 USDJPY exposure or orders exist.

This supervisor does not authorize trading, order checks, order sends, close/modify, or any trading loop.

## Upstream Runtime Safety Dependencies

The packet consumes or references:

- `quantcore.execution.h024_runtime_safety_lockout`
- `quantcore.execution.h024_runtime_safety_heartbeat`
- `quantcore.execution.h024_runtime_tick_spread_safety_supervisor`

The runtime heartbeat and tick/spread supervisor must pass before the exposure/inventory packet can pass.

## Read-Only Boundary

The supervisor may call:

- `MetaTrader5.initialize()` indirectly through upstream heartbeat/tick-spread packets
- `MetaTrader5.account_info()` indirectly through upstream heartbeat
- `MetaTrader5.terminal_info()` indirectly through upstream heartbeat
- `MetaTrader5.symbol_info()` indirectly through upstream tick/spread packet
- `MetaTrader5.symbol_info_tick()` indirectly through upstream tick/spread packet
- `MetaTrader5.positions_get()`
- `MetaTrader5.orders_get()`

It must not call:

- `symbol_select`
- `order_check`
- `order_send`
- any entry path
- any close path
- any modify path
- any trading loop
- any broker mutation path

## Allowed H024 Inventory

The only allowed H024 position, if present, is the exact known XAUUSDm canary:

- `symbol == XAUUSDm`
- model symbol maps to `XAUUSD`
- `magic == 240024`
- `volume == 0.01`
- `type == 1`
- `ticket == 4413054432` or `identifier == 4413054432`

No H024 orders are allowed.

No H024 USDJPY positions are allowed.

No H024 USDJPY orders are allowed.

A flat H024 inventory state is allowed. This means the canary is not observed and no other H024 position/order is observed. A flat state does not authorize any new entry.

## Fail-Closed Conditions

The packet fails closed if any of these conditions occur:

- Runtime safety heartbeat fails.
- Runtime tick/spread supervisor fails.
- Runtime safety lockout reader cannot be referenced.
- `positions_get()` is unavailable or malformed.
- `orders_get()` is unavailable or malformed.
- More than one H024 position is observed.
- Any H024 order is observed.
- Any H024 USDJPY position is observed.
- Any H024 USDJPY order is observed.
- Any H024 XAUUSDm position differs from the exact known canary ticket/identifier, magic, volume, type, or symbol.
- Symbol mapping is unknown or inconsistent for observed H024 inventory.
- Any broker/order/trading authorization is missing or not false.

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

`EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED`

Upstream safety packets passed, inventory was readable, and any H024 inventory was absent or exactly the known XAUUSDm canary. Trading remains unauthorized.

`FAIL_CLOSED_EXPOSURE_INVENTORY_BLOCKED`

One or more upstream safety checks or inventory checks failed. Trading remains unauthorized and blocked.

## Commands

Build packet:

```powershell
python scripts\build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py

Verify packet:

python scripts\verify_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py reports\h024_runtime_exposure_inventory_safety_supervisor.jsonl --require-pass

Focused tests:

python -m pytest tests\test_h024_runtime_exposure_inventory_safety_supervisor.py

Full suite:

python -m pytest
Interpretation

A passing exposure/inventory supervisor packet does not prove strategy edge, live readiness, USDJPY order readiness, or trading-loop readiness. It only proves read-only runtime inventory observability under the expected demo account context, with no unexpected H024 inventory.

The hard boundary remains:

no second H024 entry
no live order
no USDJPY order
no scaling
no order_check
no order_send
no close/modify unless separately governed and exact-ticket locked
no trading loop