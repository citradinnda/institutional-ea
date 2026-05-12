# H024 Runtime Account Risk And Margin Safety Supervisor

## Purpose

The H024 runtime account risk and margin safety supervisor is a read-only account-state safety layer.

It verifies account cash, equity, margin, free margin, margin level, floating PnL consistency where available, and boundedness of the known canary exposure. It consumes or references the existing runtime safety layers:

- runtime safety lockout reader
- runtime safety heartbeat packet
- runtime tick/spread safety supervisor
- runtime exposure/inventory safety supervisor

This packet does not authorize trading. A passing result only means account risk and margin state are readable and coherent under the current demo context.

## Expected Runtime Context

- Strategy: `H024`
- Server: `Exness-MT5Trial6`
- Account currency: `USD`
- Only allowed H024 exposure, if present: exact XAUUSDm canary ticket/identifier `4413054432`, magic `240024`, volume `0.01`

## Read-Only Boundary

The supervisor may call:

- `MetaTrader5.account_info()`
- upstream read-only safety packets that call account, terminal, symbol, tick, position, and order readers

It must not call:

- `symbol_select`
- `order_check`
- `order_send`
- any entry path
- any close path
- any modify path
- any trading loop
- any broker mutation path

## Default Thresholds

- minimum balance: `0.0 USD`
- minimum equity: `0.0 USD`
- minimum free margin: `0.0 USD`
- minimum margin level when margin is used: `300%`
- maximum total margin used fraction: `0.50`
- maximum account identity difference: `0.10 USD`
- maximum canary volume: `0.01`
- maximum H024 positions: `1`
- maximum H024 orders: `0`

These are runtime safety thresholds, not alpha assumptions.

## Account Consistency Checks

The packet verifies:

- `account_info()` availability
- expected server
- expected account currency
- finite non-negative balance
- finite non-negative equity
- finite non-negative margin
- finite non-negative free margin
- bounded total margin usage
- `margin_free ~= equity - margin`
- `equity ~= balance + credit + profit` where profit is available
- `account profit ~= sum(position.profit)` where position profits are available
- sane margin level when margin is used
- margin level consistency where available

## Canary Boundedness Checks

The packet verifies:

- H024 position count is at most one
- H024 order count is zero
- canary state is either `OBSERVED_EXACT_KNOWN_CANARY` or `NOT_OBSERVED`
- observed canary volume is bounded by `0.01`
- observed canary identity matches the exact known XAUUSDm canary if present
- no H024 USDJPY exposure is present

A flat H024 inventory state is allowed. It does not authorize a new entry.

## Fail-Closed Conditions

The packet fails closed if any of these conditions occur:

- runtime heartbeat fails
- runtime tick/spread supervisor fails
- runtime exposure/inventory supervisor fails
- lockout reader cannot be referenced
- `account_info()` is unavailable
- account server or currency is unexpected
- balance, equity, margin, or free margin is malformed or unsafe
- margin/free-margin identities are inconsistent
- floating PnL consistency fails where data is available
- margin level is compressed or inconsistent
- canary exposure is not bounded
- H024 USDJPY exposure/order exists
- any broker/order/trading authorization is missing or not false

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

`ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED`

Upstream packets passed, account state is coherent, and canary exposure is bounded. Trading remains unauthorized.

`FAIL_CLOSED_ACCOUNT_RISK_MARGIN_BLOCKED`

One or more upstream, account, margin, PnL, or canary boundedness checks failed. Trading remains unauthorized and blocked.

## Commands

Build packet:

```powershell
python scripts\build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py

Verify packet:

python scripts\verify_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py reports\h024_runtime_account_risk_margin_safety_supervisor.jsonl --require-pass

Focused tests:

python -m pytest tests\test_h024_runtime_account_risk_margin_safety_supervisor.py

Full suite:

python -m pytest
Interpretation

A passing account risk/margin supervisor packet does not prove strategy edge, live readiness, USDJPY order readiness, or trading-loop readiness. It only proves read-only account risk and margin observability under the expected demo account context.

The hard boundary remains:

no second H024 entry
no live order
no USDJPY order
no scaling
no order_check
no order_send
no close/modify unless separately governed and exact-ticket locked
no trading loop