# H018 Minimum Stop-Distance Decision Plan

## Purpose

This document opens the H018 minimum stop-distance decision plan.

It does not choose a minimum stop-distance threshold.

It does not implement a guard.

It does not authorize a real-data rerun.

It does not promote H017 or H018.

## Background

The H017 strict expanded broker-native event validation failed by account insolvency.

A later diagnostic showed that the current sizing API rejects zero and negative stop distances, but accepts any positive stop distance.

That behavior means a positive near-zero stop distance can create extreme broker lots and extreme notional exposure.

The documented H017 fatal geometry included:

- Raw H4 entry open: 110.770000000.
- H017 long stop: 110.770240804.
- Raw stop distance magnitude: approximately 0.000240804.
- Fatal USDJPY size before the invalid-stop guard: 518.77 lots.

The raw-entry directional invalid-stop guard now fails closed when a long stop is at or above the raw H4 entry open, and when a short stop is at or below the raw H4 entry open.

That guard does not solve all positive near-zero stop-distance cases.

A directionally valid stop can still be very close to the sizing reference and create extreme exposure.

## Current Non-Decision

No minimum stop-distance rule has been selected.

No threshold has been selected using:

- Spread.
- ATR.
- Tick size.
- Broker point.
- Commission.
- Slippage.
- All-in friction.
- Fixed price units.
- Fixed percentage of price.
- Broker margin.
- Maximum leverage.
- Maximum notional.

This plan only defines what must be decided before implementation.

## Core Boundary Question

Should H018 require a positive stop distance to also be large enough relative to one or more market, broker, or risk references?

If yes, the project must decide:

1. The reference used to measure minimum acceptable distance.
2. The threshold formula.
3. The action when the threshold is violated.
4. Whether the rule is execution realism, account-risk governance, or strategy logic.
5. Whether the rule belongs in H018 rather than H017.

## Candidate Minimum-Distance References

Possible references include:

### 1. Spread Multiple

A stop distance could be required to exceed a multiple of the spread.

Reason:

- If stop distance is near or below the spread, position sizing can become dominated by execution friction.

Risk:

- Spread-based filtering can change trade eligibility.
- Historical fixed-spread assumptions may understate real spread variation.

### 2. ATR Fraction

A stop distance could be required to exceed a fraction of ATR.

Reason:

- ATR ties the minimum distance to recent volatility.

Risk:

- ATR thresholds can become strategy rules rather than pure execution realism.
- Changing ATR-based eligibility can materially alter the hypothesis.

### 3. Tick Size Or Broker Point Multiple

A stop distance could be required to exceed a number of ticks or broker points.

Reason:

- This prevents mathematically positive but practically negligible stop distances.

Risk:

- Tick or point rules alone may be too small to prevent extreme leverage.
- Symbol-specific handling is required.

### 4. All-In Friction Multiple

A stop distance could be required to exceed a multiple of total expected friction.

Friction may include:

- Spread.
- Commission converted into price-distance equivalent.
- Stop slippage estimate.

Reason:

- This connects minimum distance to expected execution cost.

Risk:

- Converting commission into price distance is symbol-specific.
- The rule may become sensitive to account size, lot size, or conversion price.

### 5. Combined Rule

A stop distance could be required to exceed the maximum of several references, such as:

- spread multiple,
- ATR fraction,
- tick or point multiple,
- friction multiple.

Reason:

- A combined rule can avoid relying on one fragile threshold.

Risk:

- Combined rules are more complex.
- Complexity increases the chance of hidden tuning.

## Candidate Violation Policies

If a future stop-distance threshold is violated, the project must choose one policy.

### 1. Fail Closed

The run raises an explicit error.

Interpretation:

- The strategy generated a structurally invalid event under the declared execution model.

Benefit:

- Avoids silently changing trade history.

Risk:

- Validation may stop early and not summarize all violations.

### 2. Skip Trade

The trade is not opened.

Interpretation:

- The event is untradeable under the declared execution model.

Benefit:

- Allows a full backtest to continue.

Risk:

- Skipping trades changes trade eligibility and can become hidden optimization.
- This likely requires H018.

### 3. Clip Size

The trade is opened with reduced size.

Interpretation:

- Account-risk governance overrides raw strategy sizing.

Benefit:

- Prevents extreme notional exposure.

Risk:

- Clipping changes realized exposure.
- This likely requires a maximum notional/leverage decision plan as well as H018.

### 4. Mark Run Invalid But Continue Diagnostics

The engine records a violation and continues only in a diagnostic mode.

Interpretation:

- Useful for counting violations before deciding policy.

Benefit:

- Provides evidence without pretending the altered run is validation.

Risk:

- Must not be confused with promotable validation.

## Required Synthetic Tests Before Implementation

Before any code change, the project should define synthetic tests covering at least:

1. Directionally valid long stop with normal distance is accepted.
2. Directionally valid short stop with normal distance is accepted.
3. Directionally valid long stop with positive near-zero distance violates the threshold.
4. Directionally valid short stop with positive near-zero distance violates the threshold.
5. Equality remains invalid under raw-entry semantics.
6. Directionally invalid stops still fail closed.
7. The selected violation policy is explicit and tested.
8. Symbol-specific behavior is tested for USDJPY and XAUUSD if the threshold depends on point size, spread, commission, or conversion.
9. Test count does not drop below the current full-test anchor unless an explicit test-removal phase exists.

## Required Documentation Before Real-Data Use

Before any real-data run under a minimum stop-distance rule, the project must document:

1. The selected threshold formula.
2. Why the formula is execution realism, account-risk governance, strategy logic, or a combination.
3. The selected violation policy.
4. Whether the implementation belongs to H018.
5. Whether the run is diagnostic-only or H018 validation.
6. Why the run is not H017 promotion.
7. How the original H017 insolvency result remains visible.

## H017 / H018 Boundary

A minimum stop-distance guard can materially change trade eligibility and realized exposure.

Therefore, the working assumption is:

- Do not add a minimum stop-distance guard to rehabilitate H017.
- Treat a minimum stop-distance guard as H018 unless a later decision record explicitly proves otherwise.
- Any H018 version must define the rule before validation.
- Any real-data run after adopting the rule is diagnostic-only or H018 validation, not H017 promotion.

## Non-Promotion Statement

This plan does not approve live trading.

This plan does not approve Phase 4 execution work.

This plan does not validate H018.

This plan does not repair H017.

This plan only defines the minimum stop-distance governance questions that must be answered before implementation.
