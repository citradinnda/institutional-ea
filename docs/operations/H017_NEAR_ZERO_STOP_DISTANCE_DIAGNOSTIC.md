# H017 Near-Zero Stop-Distance Diagnostic

## Purpose

This document records a read-only diagnostic of the current H017 portfolio sizing behavior for positive near-zero stop distances.

It does not change code.

It does not add a minimum stop-distance guard.

It does not add a maximum notional or leverage guard.

It does not repair H017.

It does not promote H017.

It does not approve live trading.

It does not authorize a broad real-data rerun.

## Context

The strict expanded broker-native H017 event validation failed by insolvency.

The fatal event was localized to pathological USDJPY sizing caused by a near-zero raw stop distance:

- Raw H4 entry open: 110.770000000.
- H017 long stop: 110.770240804.
- Absolute raw distance: 0.000240804.

A raw-entry directional invalid-stop guard has since been implemented. Under current raw-entry sizing semantics:

- Long/buy stops must be below raw H4 entry open.
- Short/sell stops must be above raw H4 entry open.
- Equality is invalid.
- Invalid directional stops fail closed.

However, positive directionally valid near-zero stop distances remain an open execution-semantics question.

## Current Sizing Behavior

Current sizing API:

    quantcore.backtest.portfolio.size_position_from_risk

Current signature:

    size_position_from_risk(
        *,
        symbol: str,
        signed_risk_fraction: float,
        equity_usd: float,
        entry_price: float,
        stop_distance_price: float,
        instrument_spec: InstrumentSpec | None = None,
    ) -> PositionSize

Current behavior:

1. `stop_distance_price` must be greater than zero.
2. There is no minimum stop-distance threshold beyond positive.
3. There is no maximum notional guard.
4. There is no maximum leverage guard.
5. Lot size is rounded down to the broker lot step.
6. If the rounded size is below minimum lot, zero lots are returned.

## Read-Only Diagnostic Output

The diagnostic used `size_position_from_risk` directly with controlled inputs.

### XAUUSD normal 10.0 USD stop

- Symbol: XAUUSD.
- Equity: 10000.00 USD.
- Signed risk fraction: 0.010000.
- Entry price: 2000.000000000.
- Stop distance: 10.000000000.
- Target risk: 100.000000 USD.
- Actual risk: 100.000000 USD.
- Lots: 0.100000.
- Notional quote: 20000.000000.
- Notional quote divided by equity: 2.000000.

### XAUUSD small 0.01 USD stop

- Symbol: XAUUSD.
- Equity: 10000.00 USD.
- Signed risk fraction: 0.010000.
- Entry price: 2000.000000000.
- Stop distance: 0.010000000.
- Target risk: 100.000000 USD.
- Actual risk: 100.000000 USD.
- Lots: 100.000000.
- Notional quote: 20000000.000000.
- Notional quote divided by equity: 2000.000000.

### XAUUSD near-zero 0.0001 USD stop

- Symbol: XAUUSD.
- Equity: 10000.00 USD.
- Signed risk fraction: 0.010000.
- Entry price: 2000.000000000.
- Stop distance: 0.000100000.
- Target risk: 100.000000 USD.
- Actual risk: 100.000000 USD.
- Lots: 10000.000000.
- Notional quote: 2000000000.000000.
- Notional quote divided by equity: 200000.000000.

### USDJPY normal 1.0 JPY stop

- Symbol: USDJPY.
- Equity: 10000.00 USD.
- Signed risk fraction: 0.010000.
- Entry price: 150.000000000.
- Stop distance: 1.000000000.
- Target risk: 100.000000 USD.
- Actual risk: 100.000000 USD.
- Lots: 0.150000.
- Notional quote: 2250000.000000.
- Notional quote divided by equity: 225.000000.

### USDJPY fatal-geometry-sized raw distance from H017 insolvency diagnostic

- Symbol: USDJPY.
- Equity: 9847.56 USD.
- Signed risk fraction: 0.010000.
- Entry price: 110.770000000.
- Stop distance: 0.000240804.
- Target risk: 98.475600 USD.
- Actual risk: 98.473771 USD.
- Lots: 452.980000.
- Notional quote: 5017659460.000000.
- Notional quote divided by equity: 509533.271186.

## Zero And Negative Stop-Distance Checks

The sizing API rejects non-positive stop distances:

- `stop_distance_price=0.0`: `ValueError: stop_distance_price must be > 0.0`.
- `stop_distance_price=-0.01`: `ValueError: stop_distance_price must be > 0.0`.

## Interpretation

The current sizing API correctly rejects zero and negative stop distances.

However, any positive stop distance, even extremely small, is accepted.

This means a directionally valid near-zero stop distance can still create extreme broker lots and extreme notional exposure.

This is not a source-data preflight issue.

This is not a strategy-promotion result.

This is an execution-semantics and account-risk governance issue.

## Open Decisions

The project has not yet decided:

1. Whether to add a minimum stop-distance guard.
2. Whether that guard should be based on spread, ATR fraction, tick size, broker point size, all-in friction, or another reference.
3. Whether to add a maximum notional or leverage guard.
4. Whether any such guard should fail closed, skip trades, clip trades, or open a successor hypothesis.
5. Whether any trade-skipping or clipping behavior requires H018.

## Governance Boundary

Do not silently patch H017 to avoid near-zero stop-distance failures.

Do not tune H017 parameters to hide the issue.

Do not implement trade skipping or clipping without an explicit H017/H018 boundary decision.

Do not treat any future passing result under altered stop-distance or notional semantics as H017 promotion unless explicitly governed.

Current status remains:

- H017 failed.
- H017 not promotable.
- Live trading approved: False.
- Phase 4 execution work: not approved.
