# H018 Maximum Notional / Leverage Decision Record

Status: Accepted and implemented

## Decision Summary

H018 validation-mode event execution must enforce a maximum per-trade USD gross leverage guard.

The accepted rule is:

- Rule name: per_trade_usd_gross_leverage_at_or_below_10x_equity
- Exposure basis: per-trade USD gross notional divided by account equity
- Maximum gross leverage: 10.0
- Boundary behavior: less than or equal to 10.0 passes
- Violation behavior: greater than 10.0 fails closed

Plain English:

A single trade may not create more than 10 times account equity in USD-converted gross notional exposure.

## Accepted Measurement Basis

The guard measures:

notional_usd / equity_usd

Where:

- notional_usd is the USD-converted gross notional of the preliminary position size.
- equity_usd is the account equity used for sizing at the start of the event interval.

This guard is per trade.

This decision does not choose a portfolio-wide gross leverage cap.

This decision does not choose a broker margin model.

This decision does not choose a friction-burden cap.

## Instrument Handling

### XAUUSD

For XAUUSD, the current PositionSize.notional_quote value is already USD-denominated because the quote currency is USD.

Therefore:

notional_usd = position_size.notional_quote

### USDJPY

For USDJPY, the current PositionSize.notional_quote value is JPY-denominated because the quote currency is JPY.

Because USDJPY price is JPY per 1 USD, JPY notional is converted to USD using the raw entry price:

notional_usd = position_size.notional_quote / entry_raw_price

This follows the existing project convention used by quote_pnl_to_usd for JPY quote-currency conversion.

## Accepted Threshold

The accepted maximum per-trade USD gross leverage is:

10.0

The guard evaluates:

gross_leverage = notional_usd / equity_usd

The trade passes this guard if:

gross_leverage <= 10.0

The trade violates this guard if:

gross_leverage > 10.0

## Boundary Behavior

The accepted boundary behavior is:

1. gross_leverage < 10.0 passes.
2. gross_leverage == 10.0 passes.
3. gross_leverage > 10.0 fails closed.

Equality passes this guard.

## Accepted Violation Policy

Violations fail closed.

Validation-mode behavior must be:

1. Raise an explicit H018 maximum leverage violation error.
2. Do not silently skip the trade.
3. Do not clip the position size.
4. Do not warn and continue.
5. Do not log-only continue.
6. Do not convert the run into a promotable validation result.

This follows the already accepted H018 validation-mode trade violation policy.

## Accepted Implementation Placement

The guard must run after preliminary position sizing because it requires the computed lot size and notional.

In the H017/H018 event engine, the intended placement is:

1. Validate raw-entry directional stop geometry.
2. Validate minimum raw stop distance.
3. Compute preliminary PositionSize with size_position_from_risk.
4. Validate maximum per-trade USD gross leverage.
5. Only then build the execution-cost-adjusted entry fill.

The guard must run before any fill is created for the violating trade.

## Required Audit Fields

The fail-closed error must preserve at least:

1. rule_name = per_trade_usd_gross_leverage_at_or_below_10x_equity
2. symbol
3. side
4. decision_time
5. entry_time
6. entry_raw_price
7. stop_price
8. raw_stop_distance
9. equity_usd
10. lots
11. contract_size
12. quote_currency
13. notional_quote
14. notional_usd
15. gross_leverage
16. maximum_gross_leverage = 10.0
17. threshold_basis = per_trade_usd_gross_notional_divided_by_equity
18. validation_action = fail_closed

## Required Synthetic Tests Before Or With Implementation

Implementation must include focused synthetic tests for at least:

1. USDJPY below 10.0x passes.
2. USDJPY exactly 10.0x passes.
3. USDJPY above 10.0x fails closed.
4. XAUUSD below 10.0x passes.
5. XAUUSD exactly 10.0x passes.
6. XAUUSD above 10.0x fails closed.
7. Fail-closed error audit fields are preserved.
8. Existing raw-entry invalid-stop behavior remains unchanged.
9. Existing H018 minimum stop-distance behavior remains unchanged.
10. Full pytest count must not drop below the current 545-test anchor unless an explicit test-removal phase exists.

## Rejected Alternatives For First Implementation

### No Maximum Exposure Guard

Rejected for first H018 validation-mode implementation.

Reason:

The accepted minimum stop-distance rule blocks sub-spread raw stop distances, but a trade exactly one modeled spread away can still create large leverage.

Representative read-only inspection showed:

- USDJPY, 10000 USD equity, 0.01 stop distance: approximately 150.0x gross leverage.
- XAUUSD, 10000 USD equity, 0.30 stop distance: approximately 66.6x gross leverage.

A maximum exposure guard is therefore still required before any future H018 real-data validation attempt.

### Broker-Lot Cap Only

Rejected for first implementation.

Reason:

A lot cap is simple but does not normalize economic exposure across USDJPY and XAUUSD, and it does not scale with account equity.

### Quote-Currency Notional Cap Without USD Conversion

Rejected for first implementation.

Reason:

USDJPY notional_quote is JPY while XAUUSD notional_quote is USD. Comparing quote-currency notionals directly would mix currencies and produce false risk conclusions.

### Position Clipping

Rejected for first validation-mode implementation.

Reason:

Clipping changes realized exposure and can improve backtest results by construction. The accepted validation-mode policy is fail closed rather than clip.

### Trade Skipping

Rejected for first validation-mode implementation.

Reason:

Skipping changes trade eligibility and can become hidden optimization. The accepted validation-mode policy is fail closed rather than skip.

### Warn-And-Continue

Rejected.

Reason:

Continuing after a known validation-envelope breach would produce a polished but invalid equity curve.

### Log-Only Continuation

Rejected for validation mode.

Reason:

A log-only violation policy is not fail closed and can hide account-risk violations.

### Diagnostic-Only Continuation

Deferred.

Reason:

Diagnostic-only continuation may later be useful to count exposure violations, but it must be implemented as a separately labeled diagnostic mode and must not be confused with validation.

## Real-Data Run Classification

This decision does not authorize a real-data rerun.

After implementation, any real-data run must be classified as one of:

1. Diagnostic-only run.
2. H018 validation run after a formal H018 claim exists.

A run after this implementation must not be described as H017 promotion.

A passing run after this implementation would not automatically validate H018.

A passing run after this implementation would not approve live trading.

A passing run after this implementation would not approve Phase 4 execution.

## H018 Hypothesis Boundary

This decision creates an H018 account-risk validation envelope.

It does not repair H017.

It does not erase the original H017 strict expanded broker-native insolvency failure.

It does not tune H017.

It does not change H017 entry signals.

It does not change the cost model.

It does not change the minimum stop-distance rule.

It does not change raw-entry directional stop validity.

It does not choose executable-entry sizing.

It does not choose a portfolio-wide leverage cap.

## Non-Promotion Statement

H017 remains failed.

H017 is not promotable.

H018 remains unvalidated.

H018 is not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.

This decision only authorizes implementation of a fail-closed maximum per-trade USD gross leverage guard.

## Current Verdict

Accepted and implemented.

The accepted rule is:

per_trade_usd_gross_leverage_at_or_below_10x_equity

The accepted maximum gross leverage is:

10.0

The accepted basis is:

per-trade USD gross notional divided by equity

The accepted violation policy is:

fail closed

Implementation was authorized only for this narrow guard and its focused synthetic tests, and that implementation has been completed.

Real-data validation is not authorized by this decision.

Live trading is not approved.

Phase 4 execution is not approved.
