# H018 Boundary Decision Plan

## Purpose

This document opens the H018 boundary question before any further execution-semantics or account-risk changes are implemented.

H017 has failed strict expanded broker-native event validation by insolvency and remains failed / not promotable. Execution-semantics changes must not be used to retroactively repair or promote H017.

## Current H017 Status

H017 status:

- Failed / not promotable.
- Not live-approved.
- Not Phase 4 approved.
- Not eligible for parameter tuning as a rescue path.
- Not repaired by the raw-entry invalid-stop guard.
- Not repaired by equality invalid-stop tests.
- Not repaired by near-zero stop-distance documentation.

The strict expanded broker-native H017 validation remains historically important because it exposed a pathological sizing failure after a near-zero raw stop distance and a 518.77-lot USDJPY trade.

## Why H018 Boundary Planning Is Required

The remaining open issues are not cosmetic implementation details. They can materially change:

1. Trade eligibility.
2. Position sizing.
3. Realized exposure.
4. Account survivability.
5. Backtest outcome.
6. Hypothesis identity.

Therefore, they must be handled as hypothesis-boundary decisions before code changes.

## Open Boundary Questions

The following questions define the H018 boundary problem.

### 1. Raw Entry Versus Executable Entry Sizing

Current H017 event sizing uses the raw H4 entry open before spread is applied.

Open question:

- Should future sizing use raw H4 entry open, executable entry after spread, or a separately named sizing reference?

Boundary concern:

- Changing the sizing reference can alter lot sizes and invalid-stop detection.
- This may be an execution-semantics change large enough to require H018.

### 2. Directional Stop Validity Reference

Current H017 raw-entry semantics require:

- Long / buy stop below raw H4 entry open.
- Short / sell stop above raw H4 entry open.
- Equality is invalid.

Open question:

- Should future directional validity be checked against raw entry, executable entry, or both?

Boundary concern:

- Changing the validity reference can change which trades are accepted, rejected, skipped, or failed closed.
- This may require H018.

### 3. Minimum Stop-Distance Guard

Current sizing rejects zero and negative stop distances, but any positive stop distance is accepted.

Open question:

- Should future validation require a minimum stop distance?

Possible minimum-distance references include:

- Spread.
- ATR.
- Tick size.
- Broker point.
- All-in friction.
- A combination of the above.

Boundary concern:

- A minimum stop-distance rule can filter trades.
- Trade filtering changes the realized strategy and likely requires H018.

### 4. Maximum Notional / Leverage Guard

Current sizing has no maximum notional guard and no maximum leverage guard.

Open question:

- Should future validation cap notional exposure, leverage, lots, margin usage, or some combination?

Boundary concern:

- Clipping position size changes realized risk.
- Skipping trades changes trade eligibility.
- Either behavior may require H018.

### 5. Fail-Closed Versus Skip Versus Clip

Current invalid directional stop geometry fails closed.

Open question:

- For future guards, should violations fail closed, skip the trade, clip position size, or mark the run invalid?

Boundary concern:

- Skipping or clipping trades can transform validation results.
- These policies must be explicitly documented and tested before any real-data run.

## H017 Versus H018 Boundary

The working boundary is:

1. H017 remains the failed historical hypothesis.
2. H017 must not be rehabilitated by execution-semantics changes.
3. Any change that materially affects trade eligibility or realized exposure should be treated as H018 unless a later decision record explicitly proves otherwise.
4. H018 may inherit H017 alpha logic, but it must explicitly define its execution and account-risk semantics before validation.
5. Any future real-data run under altered semantics is either diagnostic-only or H018 validation, not H017 promotion.

## Required Sequence Before Any Implementation

Before implementing minimum stop-distance, maximum notional/leverage, or executable-entry sizing changes:

1. Write a focused decision plan.
2. Define the intended semantics in plain English.
3. Add synthetic tests first.
4. Run focused tests.
5. Run full `pytest -q`.
6. Document the outcome.
7. Commit and push.
8. Only then consider diagnostic or validation real-data runs.

## Subordinate Decision Plans

Opened subordinate H018 decision plans:

- `docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md`

The minimum stop-distance plan does not choose a threshold, implement a guard, authorize a real-data rerun, or promote H017/H018.

## Real-Data Run Restriction

No broad strict real-data validation rerun is authorized by this document.

Any future rerun must state explicitly whether it is:

1. Diagnostic-only, or
2. H018 validation.

It must not be described as H017 promotion.

## Non-Promotion Statement

This document does not approve live trading.

This document does not approve Phase 4 execution work.

This document does not approve H017 promotion.

This document only opens the boundary-governance plan for deciding whether the next hypothesis should be H018.
