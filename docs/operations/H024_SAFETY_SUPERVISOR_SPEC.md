# H024 Safety Supervisor / Kill-Switch Specification

## Purpose

This document defines the mandatory H024 safety supervisor and kill-switch layer that must exist before any automated trading loop can be considered.

This layer is currently specification-only and read-only. It does not import MetaTrader5, does not query the broker, does not place orders, does not close or modify positions, and does not authorize a trading loop.

## Current Status

- Strategy: `H024`
- Model symbols: `XAUUSD`, `USDJPY`
- Runtime symbols: `XAUUSDm`, `USDJPYm`
- Status: `specified_not_runtime_enforced`
- Broker mutation authorized: `false`
- Order check authorized: `false`
- Order send authorized: `false`
- Entry authorized: `false`
- Close/modify authorized: `false`
- XAUUSD order authorized: `false`
- USDJPY order authorized: `false`
- Trading loop authorized: `false`
- Automatic execution authorized: `false`

## Required Global Guards

The supervisor specification defines these required global guards:

1. `global_no_new_entry_switch`
2. `manual_override_lockout_file`
3. `daily_loss_lockout`
4. `max_floating_loss_lockout`
5. `spread_shock_guard`
6. `stale_tick_guard`
7. `disconnected_terminal_guard`
8. `margin_compression_guard`
9. `volatility_expansion_black_swan_guard`
10. `unexpected_position_order_lockout`

Every guard must fail closed if required inputs are unavailable, unreadable, stale, malformed, or threshold-breaching.

## Required Per-Symbol Circuit Breakers

The supervisor specification defines per-symbol circuit breakers for:

- `XAUUSD` / `XAUUSDm`
- `USDJPY` / `USDJPYm`

Each symbol must define:

1. `symbol_no_new_entry_breaker`
2. `symbol_max_floating_loss_breaker`
3. `symbol_spread_shock_breaker`
4. `symbol_stale_tick_breaker`
5. `symbol_volatility_expansion_black_swan_breaker`
6. `symbol_unexpected_position_order_breaker`

## Integration Requirements

Before any trading loop exists, runtime implementations must consume this safety contract or a stricter successor. Minimum runtime layers still required:

1. Configuration schema for thresholds and lockout paths.
2. Read-only lockout file reader.
3. Read-only account and terminal state heartbeat.
4. Read-only per-symbol tick freshness and spread supervisor.
5. Read-only margin and floating-P/L supervisor.
6. Read-only broker-native volatility expansion supervisor.
7. Read-only position/order reconciliation supervisor.
8. Fail-closed aggregate supervisor verifier.

## Commands

Build the local JSONL packet:

```powershell
python scripts\build_h024_safety_supervisor_spec_jsonl.py

Verify the local JSONL packet:

python scripts\verify_h024_safety_supervisor_spec_jsonl.py reports\h024_safety_supervisor_spec.jsonl --require-pass

Run focused tests:

python -m pytest -q tests\test_h024_safety_supervisor_spec.py
Runtime Artifact

The generated JSONL is local only:

reports\h024_safety_supervisor_spec.jsonl

Do not commit reports/.