# H024 Dry-Run EA Safety Plan

Research/preparation only. No demo trading is approved. No live trading is approved. Phase 4 execution is not approved.

## Purpose

Define the minimum safety constraints for a future H024 dry-run/log-only EA path.

This document exists because H024 now has enough research evidence to justify execution-preparation design, but not enough execution safety evidence to justify demo deployment.

## Current Status

H024 is not demo-ready.

Completed evidence includes:

- preliminary fixed lifecycle diagnostic
- targeted robustness diagnostic
- chronological validation
- trade-ledger audit
- direction-flip negative control
- ledger-level permutation control
- broker symbol/spec audit
- observed broker cost rerun
- static MT5 order behavior audit

Remaining blockers include:

- no dry-run/log-only EA path
- no hard kill switch
- no execution adapter safety checks
- no order-send prevention invariant
- no account/server/symbol preflight gate
- no EA-side position sizing audit logs
- no MT5 order placement/modification/rejection behavior reconciliation
- no explicit Phase 4 authorization

## Non-Negotiable Dry-Run Rule

Dry-run/log-only mode must not place, modify, close, or delete orders.

In dry-run/log-only mode, the code must not call any live MT5 order-sending function.

The dry-run path may calculate intended actions and write logs only.

Any accidental call path capable of placing an order is a fail-closed defect.

## Explicit Deployment Boundary

The following remain forbidden until separately authorized:

- demo order placement
- live order placement
- Phase 4 execution
- automatic position opening
- automatic position closing
- stop-loss modification
- take-profit modification
- pending order placement
- manual bypass of the kill switch

## Required Dry-Run Safety Gates

### 1. Hard Kill Switch

The EA must include a hard kill switch.

Minimum behavior:

- default state is disabled/no-trade
- if missing, malformed, or false, no execution-capable path may run
- dry-run may still log that the kill switch blocks execution
- execution-capable mode must fail closed if the kill switch is unavailable

### 2. Mode Separation

The EA must distinguish at least:

- `dry_run`
- `demo_execution`
- `live_execution`

Only `dry_run` may be implemented first.

`demo_execution` and `live_execution` must remain unavailable until explicitly authorized.

### 3. Symbol Mapping

Model symbols:

- USDJPY
- XAUUSD

Observed Exness symbols:

- USDJPYm
- XAUUSDm

The EA must log both model symbol and broker symbol for every decision.

Approved mapping:

| Model Symbol | Broker Symbol |
|---|---|
| USDJPY | USDJPYm |
| XAUUSD | XAUUSDm |

Missing or unexpected symbols must fail closed.

### 4. Account And Server Preflight

Dry-run logs must include:

- account login
- server name
- account currency
- leverage
- trade allowed flag, if available
- terminal connected flag
- timestamp
- broker symbols selected/visible
- symbol trade mode
- execution mode
- filling mode
- order mode
- volume min/max/step
- stops level
- freeze level
- point
- digits
- spread/floating spread fields

Unknown or missing required fields must be logged as blockers.

### 5. Signal Decision Logs

For every decision timestamp, dry-run logs must include:

- timestamp
- model symbol
- broker symbol
- H024 regime state
- pullback state
- continuation trigger state
- side: buy/sell/flat
- raw H4 prices used
- ATR used
- stop candidate
- reason for no trade, if flat
- reason for trade candidate, if non-flat

### 6. Position Sizing Audit Logs

For every non-flat candidate, dry-run logs must include:

- interval/account equity used
- signed risk fraction
- raw entry price
- raw stop price
- raw stop distance
- contract size
- quote currency
- calculated lots before broker normalization
- normalized lots after volume-step rounding
- notional quote
- notional USD
- per-trade gross leverage
- portfolio gross leverage
- H018 guard pass/fail result

No silent clipping is allowed. If normalization changes lots, log it.

### 7. Stop And Volume Normalization Logs

Dry-run logs must include:

- raw stop
- normalized stop, if any
- point
- digits
- stops level
- freeze level
- minimum stop-distance check
- volume min
- volume max
- volume step
- raw lots
- normalized lots
- final intended lots

If normalized lots are below minimum or above maximum, fail closed for that candidate and log the reason.

### 8. No-Order Invariant

Dry-run must emit intended action records only.

Allowed dry-run outputs:

- `WOULD_OPEN`
- `WOULD_CLOSE`
- `WOULD_MODIFY_STOP`
- `NO_ACTION`
- `BLOCKED`

Forbidden dry-run outputs:

- actual order ticket
- actual position ticket
- successful order-send result
- order modification result

If any order ticket appears in dry-run logs, dry-run safety failed.

### 9. Rejected-Action Logging

Dry-run must explicitly log blocked actions.

Examples:

- blocked by kill switch
- blocked by unsupported symbol
- blocked by missing account metadata
- blocked by invalid stop geometry
- blocked by minimum stop distance
- blocked by per-trade leverage
- blocked by portfolio leverage
- blocked by volume normalization
- blocked by unsupported filling mode
- blocked by unsupported order mode
- blocked because execution mode is not authorized

### 10. 2023 Weakness Must Remain Visible

No dry-run or execution-preparation work may hide 2023 weakness.

Known observed-broker-cost 2023 result:

- PnL: -622.90
- PF: 0.793006
- stop rate: 18.8889%

Do not add:

- 2023 exclusion
- time/session filters
- year filters
- parameter tuning
- H021 time bucket mining

Any such change becomes a new hypothesis, not H024.

## Minimum Implementation Sequence

1. Implement dry-run/log-only EA path with no order-send capability.
2. Add tests proving dry-run cannot call an order-send function.
3. Add tests proving kill switch defaults to no-trade.
4. Add tests proving symbol mapping fails closed on unknown symbols.
5. Add tests proving volume and stop normalization are logged.
6. Add tests proving H018 guard violations are blocked and logged.
7. Run dry-run against historical/latest terminal data without placing orders.
8. Review logs manually before any demo-execution design.

## Required Authorization Before Demo Execution

Before any demo order can be placed, the user must explicitly authorize demo execution after reviewing:

- dry-run logs
- kill-switch behavior
- no-order invariant tests
- symbol/account preflight logs
- position sizing logs
- stop/volume normalization logs
- proposed demo execution scope
- maximum allowed risk
- maximum allowed symbols
- maximum allowed duration
- emergency stop procedure

Without explicit authorization, no demo order placement is approved.

## Current Decision

H024 is promising enough for dry-run/log-only EA preparation.

H024 is not approved for demo deployment.

H024 is not approved for live deployment.

Phase 4 execution is not approved.
