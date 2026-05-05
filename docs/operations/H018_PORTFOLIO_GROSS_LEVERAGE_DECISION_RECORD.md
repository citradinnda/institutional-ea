# H018 Portfolio-Wide Gross Leverage Decision Record

Decision identifier: H018-PGLDR-001.
Decision status: Accepted and implemented.
Date: 2026-05-04.
Owner or reviewer: solo retail trader with AI engineering review.

Implementation status: implemented.
Validation status: not validated.
Live-trading status: not approved.
Phase 4 execution status: not approved.

## Decision Summary

H018 validation-mode event execution must enforce a maximum portfolio-wide USD gross leverage guard.

The accepted rule is:

1. Rule name: portfolio_usd_gross_leverage_at_or_below_10x_equity.
2. Exposure basis: sum of all candidate interval trade USD gross notionals divided by interval-start account equity.
3. Maximum portfolio gross leverage: 10.0.
4. Boundary behavior: less than or equal to 10.0 passes.
5. Violation behavior: greater than 10.0 fails closed.

Plain English:

At a single event interval, the total USD-converted gross notional exposure opened by all symbols may not exceed 10 times account equity.

## Accepted Measurement Basis

The guard measures:

portfolio_gross_leverage = portfolio_notional_usd / interval_start_equity_usd

Where:

1. portfolio_notional_usd is the sum of USD-converted gross notional for all non-zero-lot candidate trades in the same event interval.
2. interval_start_equity_usd is the account equity used for sizing at the start of that interval.
3. Gross exposure is summed using absolute notional exposure.
4. Long and short exposures are not netted against each other.
5. USDJPY notional is converted from JPY to USD by dividing notional_quote by entry_raw_price.
6. XAUUSD notional_quote is already USD-denominated.

This guard is portfolio-wide for the event interval.

It is separate from the already implemented per-trade maximum leverage guard.

## Accepted Threshold

The accepted maximum portfolio-wide USD gross leverage is:

10.0

The guard evaluates:

portfolio_gross_leverage = portfolio_notional_usd / interval_start_equity_usd

The interval passes this guard if:

portfolio_gross_leverage <= 10.0

The interval violates this guard if:

portfolio_gross_leverage > 10.0

## Boundary Behavior

The accepted boundary behavior is:

1. portfolio_gross_leverage < 10.0 passes.
2. portfolio_gross_leverage == 10.0 passes.
3. portfolio_gross_leverage > 10.0 fails closed.

Equality passes this guard.

## Accepted Violation Policy

Violations fail closed.

Validation-mode behavior must be:

1. Raise an explicit H018 portfolio-wide gross leverage violation error.
2. Do not silently skip any trade.
3. Do not clip any position size.
4. Do not net long and short notionals.
5. Do not warn and continue.
6. Do not log-only continue.
7. Do not convert the run into a promotable validation result.

This follows the accepted H018 validation-mode trade violation policy.

## Accepted Implementation Placement

The guard must run after preliminary sizing for all symbols in an interval because it requires knowing the candidate non-zero-lot positions for the interval.

The intended event-engine placement is:

1. For each symbol, validate directional stop geometry.
2. For each symbol, validate minimum raw stop distance.
3. For each symbol, compute preliminary PositionSize.
4. For each symbol, validate maximum per-trade USD gross leverage.
5. Collect all non-zero-lot candidate positions for the interval before creating fills.
6. Validate maximum portfolio-wide USD gross leverage across the collected candidate positions.
7. Only then build execution-cost-adjusted entry fills for the interval.

The guard must run before any fill is created for a violating interval.

## Required Audit Fields

The fail-closed error must preserve at least:

1. rule_name = portfolio_usd_gross_leverage_at_or_below_10x_equity.
2. decision_time.
3. entry_time.
4. interval_start_equity_usd.
5. symbols.
6. per_symbol_lots.
7. per_symbol_entry_raw_price.
8. per_symbol_notional_quote.
9. per_symbol_notional_usd.
10. portfolio_notional_usd.
11. portfolio_gross_leverage.
12. maximum_portfolio_gross_leverage = 10.0.
13. threshold_basis = portfolio_usd_gross_notional_divided_by_interval_start_equity.
14. validation_action = fail_closed.

## Required Synthetic Tests Before Or With Implementation

Implementation must include focused synthetic tests for at least:

1. Single-symbol interval below 10.0x passes.
2. Single-symbol interval exactly 10.0x passes.
3. Single-symbol interval above 10.0x fails closed.
4. Two-symbol interval with each trade individually below 10.0x but combined portfolio exposure below 10.0x passes.
5. Two-symbol interval with each trade individually below or equal to 10.0x but combined portfolio exposure exactly 10.0x passes.
6. Two-symbol interval with each trade individually below or equal to 10.0x but combined portfolio exposure above 10.0x fails closed.
7. USDJPY notional is converted from JPY to USD by dividing by entry_raw_price.
8. XAUUSD notional_quote is treated as USD.
9. Long and short notionals are summed gross and not netted.
10. Fail-closed error audit fields are preserved.
11. Existing per-trade maximum leverage behavior remains unchanged.
12. Existing minimum stop-distance behavior remains unchanged.
13. Existing raw-entry invalid-stop behavior remains unchanged.
14. Full pytest count must not drop below the current 552-test anchor unless an explicit test-removal phase exists.

## Rejected Alternatives For First Implementation

### No Portfolio-Wide Gross Leverage Guard

Rejected.

Reason:

The implemented per-trade cap allows each individual trade to remain within 10.0x equity, but simultaneous USDJPY and XAUUSD positions can still create combined account exposure above 10.0x equity.

### Net Exposure Instead Of Gross Exposure

Rejected.

Reason:

Netting long and short notionals can hide broker exposure, margin usage, and forced-liquidation risk. H018 validation-mode account-risk governance must measure gross exposure.

### Higher Portfolio Cap Than Per-Trade Cap

Rejected for first implementation.

Reason:

A portfolio cap higher than the per-trade cap would allow simultaneous trades to exceed the currently accepted account-level exposure envelope.

### Trade Skipping

Rejected for first validation-mode implementation.

Reason:

Skipping changes trade eligibility and can become hidden optimization.

### Position Clipping

Rejected for first validation-mode implementation.

Reason:

Clipping changes realized exposure and can improve backtest results by construction.

### Warn-And-Continue

Rejected.

Reason:

Continuing after a known account-exposure breach would produce a polished but invalid equity curve.

### Log-Only Continuation

Rejected for validation mode.

Reason:

A log-only violation policy is not fail closed and can hide account-risk violations.

### Diagnostic-Only Continuation

Deferred.

Reason:

Diagnostic-only continuation may later be useful to count portfolio exposure violations, but it must be implemented as a separately labeled diagnostic mode and must not be confused with validation.

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

This decision creates an H018 portfolio-level account-risk validation envelope.

It does not repair H017.

It does not erase the original H017 strict expanded broker-native insolvency failure.

It does not tune H017.

It does not change H017 entry signals.

It does not change the cost model.

It does not change the raw-entry sizing reference.

It does not change raw-entry directional stop validity.

It does not change the minimum stop-distance rule.

It does not change the maximum per-trade leverage rule.

It does not choose a broker margin model.

It does not choose a friction-burden cap.

## Non-Promotion Statement

H017 remains failed.

H017 is not promotable.

H018 remains unvalidated.

H018 is not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.

This decision only authorizes implementation of a fail-closed maximum portfolio-wide USD gross leverage guard and its focused synthetic tests.

## Current Verdict

Accepted and implemented.

The accepted rule is:

portfolio_usd_gross_leverage_at_or_below_10x_equity

The accepted maximum portfolio-wide gross leverage is:

10.0

The accepted basis is:

portfolio USD gross notional divided by interval-start equity

The accepted violation policy is:

fail closed

Implementation is authorized only for this narrow guard and its focused synthetic tests.

Real-data validation is not authorized by this decision.

Live trading is not approved.

Phase 4 execution is not approved.
