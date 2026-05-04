# H018 Maximum Notional / Leverage Decision Plan

## Purpose

This document opens the H018 maximum notional / leverage decision plan.

It does not choose a maximum notional threshold.

It does not choose a maximum leverage threshold.

It does not implement a guard.

It does not authorize a real-data rerun.

It does not promote H017 or H018.

## Background

The H017 strict expanded broker-native event validation failed by account insolvency.

The fatal validation interval exposed a pathological USDJPY position size:

- Symbol: USDJPY.
- Side: buy.
- Lots before the invalid-stop guard: 518.77.
- Interval-start equity: approximately 9847.56 USD.
- Interval P&L: approximately -11835.26 USD.
- Ending equity: approximately -1987.71 USD.

A later read-only diagnostic showed that positive near-zero stop distances can generate extreme broker lots and extreme notional exposure even when the stop distance is technically greater than zero.

The H018 minimum stop-distance decision plan addresses whether the stop-distance denominator should have a lower bound.

This document addresses a separate but related question:

Should H018 also limit the resulting position exposure?

## Current Non-Decision

No maximum exposure rule has been selected.

No threshold has been selected using:

- Maximum broker lots.
- Maximum notional.
- Maximum notional divided by equity.
- Maximum gross leverage.
- Maximum per-symbol leverage.
- Maximum portfolio leverage.
- Maximum margin usage.
- Maximum risk-per-trade after costs.
- Maximum commission burden.
- Maximum expected loss under stop plus friction.
- Broker-specific leverage or margin approximations.

This plan only defines what must be decided before implementation.

## Core Boundary Question

Should H018 reject, clip, skip, or otherwise govern trades whose resulting exposure is too large relative to account equity or broker constraints?

If yes, the project must decide:

1. The exposure measure.
2. The threshold formula.
3. Whether thresholds are global or symbol-specific.
4. Whether thresholds apply before or after spread, commission, and slippage assumptions.
5. Whether thresholds apply per trade, per symbol, or portfolio-wide.
6. The action when the threshold is violated.
7. Whether the rule is execution realism, account-risk governance, broker-margin approximation, strategy logic, or a combination.
8. Whether the rule belongs in H018 rather than H017.

## Candidate Exposure Measures

### 1. Maximum Lots

A trade could be rejected or governed if broker lots exceed a fixed maximum.

Reason:

- Directly prevents extreme broker-order size.

Risk:

- Lot limits are symbol-specific.
- A lot cap alone may not reflect account equity, price, conversion, or portfolio exposure.
- A fixed lot cap can become an implicit strategy parameter.

### 2. Maximum Notional

A trade could be rejected or governed if notional exposure exceeds a fixed amount.

Reason:

- Directly controls gross exposure.

Risk:

- Fixed notional thresholds do not scale with account equity unless explicitly defined that way.
- USDJPY notional and XAUUSD notional require careful unit interpretation.

### 3. Maximum Notional Divided By Equity

A trade could be governed if notional exposure divided by account equity exceeds a threshold.

Reason:

- This scales exposure control with account size.

Risk:

- The project must define notional consistently across symbols.
- USDJPY conversion to USD must be explicit.
- XAUUSD contract conventions must be explicit.

### 4. Maximum Per-Trade Gross Leverage

A trade could be governed if a single trade exceeds a leverage multiple of equity.

Reason:

- This prevents a single trade from dominating the account.

Risk:

- Leverage limits can interact with strategy sizing and become account-risk rules rather than pure execution realism.

### 5. Maximum Portfolio Gross Leverage

A trade could be governed if total open exposure after adding the trade exceeds a portfolio leverage threshold.

Reason:

- H017 was explicitly portfolio-aware through a heat governor, but the fatal event showed exposure can still become pathological.

Risk:

- Portfolio leverage rules require precise timing and open-position accounting.
- This may materially change multi-symbol behavior and should be treated as H018 unless proven otherwise.

### 6. Maximum Margin Usage

A trade could be governed using an approximate broker-margin model.

Reason:

- Retail execution is constrained by margin.

Risk:

- Broker margin rules vary by account, symbol, time, and regulatory setting.
- A simplified margin model can create false precision.
- If used, it must be documented as an approximation, not as guaranteed broker behavior.

### 7. Maximum Friction Burden

A trade could be governed if spread, commission, and expected slippage consume too much of intended risk.

Reason:

- The H017 fatal event was strongly affected by huge commission from extreme lots.

Risk:

- Friction-burden rules require symbol-specific conversion and may overlap with minimum stop-distance logic.

## Candidate Violation Policies

If a future maximum notional / leverage rule is violated, the project must choose one policy.

### 1. Fail Closed

The run raises an explicit error.

Interpretation:

- The strategy produced exposure outside the declared validation envelope.

Benefit:

- Prevents silent changes to the strategy’s trade history.

Risk:

- Validation may stop early and not summarize all exposure violations.

### 2. Skip Trade

The trade is not opened.

Interpretation:

- The event is untradeable under the declared account-risk model.

Benefit:

- Allows the backtest to continue.

Risk:

- Skipping trades changes trade eligibility.
- This can become hidden optimization.
- This likely requires H018.

### 3. Clip Position Size

The trade is opened at the maximum allowed exposure.

Interpretation:

- Account-risk governance overrides raw strategy sizing.

Benefit:

- Prevents extreme exposure while preserving partial participation.

Risk:

- Clipping changes realized exposure and P&L distribution.
- Clipping may improve backtest outcomes by construction.
- This likely requires H018 and must not be treated as H017 repair.

### 4. Mark Run Invalid But Continue Diagnostics

The engine records the exposure violation and continues only in diagnostic mode.

Interpretation:

- Useful for counting how often violations occur before choosing a policy.

Benefit:

- Provides evidence without treating the altered run as validation.

Risk:

- Diagnostic continuation must not be confused with promotable validation.

## Required Synthetic Tests Before Implementation

Before any code change, the project should define synthetic tests covering at least:

1. Normal USDJPY exposure under the selected threshold is accepted.
2. Normal XAUUSD exposure under the selected threshold is accepted.
3. Extreme USDJPY exposure violates the selected threshold.
4. Extreme XAUUSD exposure violates the selected threshold.
5. The selected violation policy is explicit and tested.
6. If fail-closed is selected, the error type and message are explicit.
7. If skip is selected, skipped trades are counted and reported.
8. If clipping is selected, clipped trades are counted and reported.
9. If a leverage calculation is used, USDJPY conversion to USD is tested.
10. If a leverage calculation is used, XAUUSD notional interpretation is tested.
11. If portfolio exposure is used, overlapping positions are tested.
12. If a margin approximation is used, the approximation is documented and tested.
13. Test count does not drop below the current full-test anchor unless an explicit test-removal phase exists.

## Required Documentation Before Real-Data Use

Before any real-data run under a maximum notional / leverage rule, the project must document:

1. The selected exposure measure.
2. The selected threshold formula.
3. Whether the threshold is per-trade, per-symbol, or portfolio-wide.
4. Whether the threshold is fixed or equity-scaled.
5. Whether the threshold is broker-specific or strategy-general.
6. The selected violation policy.
7. Whether the implementation belongs to H018.
8. Whether the run is diagnostic-only or H018 validation.
9. Why the run is not H017 promotion.
10. How the original H017 insolvency result remains visible.

## Relationship To Minimum Stop-Distance Planning

Minimum stop-distance and maximum exposure controls are related but not identical.

A minimum stop-distance rule controls whether the sizing denominator is acceptable.

A maximum notional / leverage rule controls whether the resulting exposure is acceptable.

Both may be needed.

However, adopting either rule can materially change trade eligibility, realized exposure, or validation outcome.

Therefore, both should be presumed to belong to H018 unless a later decision record explicitly proves otherwise.

## H017 / H018 Boundary

A maximum notional / leverage guard can materially change realized exposure.

Therefore, the working assumption is:

- Do not add a maximum notional / leverage guard to rehabilitate H017.
- Treat maximum notional / leverage clipping or skipping as H018 unless a later decision record explicitly proves otherwise.
- Any H018 version must define the rule before validation.
- Any real-data run after adopting the rule is diagnostic-only or H018 validation, not H017 promotion.

## Non-Promotion Statement

This plan does not approve live trading.

This plan does not approve Phase 4 execution work.

This plan does not validate H018.

This plan does not repair H017.

This plan only defines the maximum notional / leverage governance questions that must be answered before implementation.
