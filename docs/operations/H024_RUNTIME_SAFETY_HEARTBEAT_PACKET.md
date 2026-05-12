# H024 Runtime Safety Heartbeat Packet

## Purpose

The H024 runtime safety heartbeat packet is a read-only runtime observation layer. It verifies that the local MetaTrader 5 Python bridge can initialize, that `account_info()` and `terminal_info()` are readable, that the connected account is the expected Exness standard-demo context, and that the runtime safety lockout reader is present.

This packet does not authorize trading. A passing heartbeat only means the runtime/account observation path is coherent enough to read. It does not mean entries are allowed.

## Expected Runtime Context

- Strategy: `H024`
- Server: `Exness-MT5Trial6`
- Account currency: `USD`
- Lockout reader module: `quantcore.execution.h024_runtime_safety_lockout`
- Lockout config: `config/h024_runtime_safety/default_lockout_config.json`

## Read-Only Boundary

The heartbeat may call:

- `MetaTrader5.initialize()`
- `MetaTrader5.account_info()`
- `MetaTrader5.terminal_info()`
- `MetaTrader5.last_error()`
- `MetaTrader5.version()`

It must not call:

- `order_check`
- `order_send`
- any entry path
- any close path
- any modify path
- any trading loop
- any broker mutation path

## Fail-Closed Conditions

The packet fails closed if any of these conditions occur:

- MetaTrader5 module is unavailable.
- MT5 initialization fails.
- `account_info()` is unavailable.
- Account server is not `Exness-MT5Trial6`.
- Account currency is not `USD`.
- `terminal_info()` is unavailable.
- Terminal connected state is not explicitly true.
- Collection takes longer than the configured freshness bound.
- Runtime safety lockout reader module cannot be imported.
- Committed runtime safety lockout config cannot be found.
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

`RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED`

The runtime/account heartbeat was readable and coherent. Trading remains unauthorized.

`FAIL_CLOSED_RUNTIME_HEARTBEAT_BLOCKED`

The runtime/account heartbeat was unavailable or inconsistent. Trading remains unauthorized and blocked.

## Commands

Build packet:

```powershell
python scripts\build_h024_runtime_safety_heartbeat_jsonl.py

Verify packet:

python scripts\verify_h024_runtime_safety_heartbeat_jsonl.py reports\h024_runtime_safety_heartbeat.jsonl --require-pass

Focused tests:

python -m pytest tests\test_h024_runtime_safety_heartbeat.py

Full suite:

python -m pytest
Interpretation

A passing heartbeat does not prove strategy edge, live readiness, or trading-loop readiness. It only proves read-only runtime/account observability under the expected demo account context.

The hard boundary remains:

no second H024 entry
no live order
no USDJPY order
no scaling
no order check
no order send
no close/modify unless separately governed and exact-ticket locked
no trading loop