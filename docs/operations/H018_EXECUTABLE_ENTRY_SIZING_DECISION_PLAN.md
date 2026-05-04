# H018 Executable-Entry Sizing Decision Plan

## Purpose

This document opens the H018 executable-entry sizing decision plan.

It does not choose executable-entry sizing.

It does not choose raw-entry sizing.

It does not choose a separate sizing reference.

It does not change stop-validity semantics.

It does not implement code.

It does not authorize a real-data rerun.

It does not promote H017 or H018.

## Background

The H017 strict expanded broker-native event validation failed by account insolvency.

The fatal USDJPY trade exposed an execution-semantics boundary problem:

- Symbol: USDJPY.
- Side: buy.
- Raw H4 entry open: 110.770000000.
- H017 long stop: 110.770240804.
- Executable entry after spread: 110.775000000.
- Lots before the invalid-stop guard: 518.77.

The stop was slightly above the raw H4 entry open but below the executable buy entry.

Before the invalid-stop guard, the event engine sized using:

- absolute distance between raw H4 entry open and stop price,

before entry spread was applied and without directional validation.

That collapsed the sizing denominator and contributed to extreme lots and account insolvency.

A raw-entry directional invalid-stop guard is now implemented:

- Long / buy stops must be below raw H4 entry open.
- Short / sell stops must be above raw H4 entry open.
- Equality is invalid.
- Invalid directional stops fail closed.
- Invalid stops are not skipped silently and are not clipped.

That guard does not decide whether future H018 sizing should use raw entry, executable entry, or a separately named sizing reference.

## Current Non-Decision

No future sizing reference has been selected.

The project has not decided whether H018 should size from:

- Raw H4 entry open.
- Executable entry after spread.
- Mid-like reference.
- Stop-validation reference.
- A separately named sizing reference.
- A broker-order reference.
- A conservative worst-case reference.

The project has not decided whether directional stop validity should be checked against:

- Raw H4 entry open.
- Executable entry after spread.
- Both raw and executable entry.
- A separate stop-validity reference.

This plan only defines what must be decided before implementation.

## Core Boundary Question

Should H018 position sizing and directional stop validation be based on raw H4 entry open, executable entry after spread, both, or a separate declared reference?

If yes, the project must decide:

1. The sizing reference.
2. The directional stop-validity reference.
3. Whether sizing and validity use the same reference.
4. Whether long and short trades require asymmetric spread handling.
5. Whether the rule is execution realism, account-risk governance, strategy logic, or a combination.
6. Whether violations fail closed, skip trades, clip trades, or mark diagnostic-only violations.
7. Whether the rule belongs in H018 rather than H017.

## Candidate Sizing References

### 1. Raw H4 Entry Open

Sizing continues to use the raw broker-native H4 open before spread.

Reason:

- This preserves the historical H017 sizing convention.
- It avoids changing the meaning of old synthetic tests without an explicit migration.

Risk:

- Raw-entry sizing may understate the economic distance for buys and sells after spread.
- Raw-entry sizing can disagree with executable stop geometry.
- Near-zero raw-entry distances can still generate extreme exposure unless separately governed.

### 2. Executable Entry After Spread

Sizing uses the actual executable entry price after applying the cost model spread.

For a buy:

- Executable entry is typically above the raw open.

For a sell:

- Executable entry is typically below the raw open.

Reason:

- This ties sizing to the price at which the simulated trade is actually entered.
- It may better represent realized entry economics.

Risk:

- It changes lot sizes relative to H017.
- It can change which stop distances appear valid or invalid.
- It may materially change validation outcome.
- It likely requires H018.

### 3. Both Raw And Executable References

A future engine could require stop validity against both raw and executable entry references.

Reason:

- This is conservative.
- It can prevent cases where a stop looks acceptable under one reference but pathological under another.

Risk:

- It may reject more trades.
- It may act as a trade filter.
- It likely changes hypothesis identity.

### 4. Separate Named Sizing Reference

The project could define an explicit sizing reference separate from raw H4 open and executable fill.

Examples:

- `sizing_reference_price`.
- `stop_distance_reference_price`.
- `risk_reference_price`.

Reason:

- This avoids ambiguous language.
- Tests can assert exactly which reference is used.

Risk:

- A separate reference adds complexity.
- It must not become a hidden tuning parameter.

### 5. Conservative Worst-Case Reference

The project could choose the reference that produces the larger risk estimate or smaller position size.

Reason:

- Conservative sizing can reduce exposure blowups.

Risk:

- This is a risk-management rule, not a neutral implementation detail.
- It may materially change realized exposure and should be treated as H018 unless proven otherwise.

## Candidate Directional Stop-Validity Policies

### 1. Raw-Entry Validity

Current implemented H017 guard:

- Long stop must be below raw H4 entry open.
- Short stop must be above raw H4 entry open.
- Equality is invalid.

Benefit:

- Already implemented and tested.

Risk:

- Does not decide executable-entry semantics for future H018.

### 2. Executable-Entry Validity

A future H018 could require:

- Long stop below executable buy entry.
- Short stop above executable sell entry.
- Equality invalid.

Benefit:

- Validity is checked against simulated executable entry.

Risk:

- It may accept cases that raw-entry validity rejects.
- It may reject cases that raw-entry validity accepts.
- It changes trade eligibility.

### 3. Both Raw And Executable Validity

A future H018 could require both:

- Long stop below raw entry and below executable buy entry.
- Short stop above raw entry and above executable sell entry.
- Equality invalid against either reference.

Benefit:

- Conservative and explicit.

Risk:

- Can become a stricter trade filter.
- Likely changes validation outcome.

### 4. Diagnostic Classification

A future diagnostic mode could classify each event as:

- valid under raw-entry semantics,
- valid under executable-entry semantics,
- valid under both,
- valid under neither.

Benefit:

- Provides evidence before choosing a policy.

Risk:

- Diagnostic classification must not be treated as validation or promotion.

## Candidate Violation Policies

If a future sizing or validity rule is violated, the project must choose one policy.

### 1. Fail Closed

The run raises an explicit error.

Interpretation:

- The strategy produced an event outside the declared execution model.

Benefit:

- Prevents silent strategy changes.

Risk:

- Validation may stop early.

### 2. Skip Trade

The trade is not opened.

Interpretation:

- The event is untradeable under the declared execution model.

Benefit:

- Allows a full backtest to continue.

Risk:

- Skipping trades changes trade eligibility.
- This likely requires H018.

### 3. Clip Position Size

The trade is opened with reduced size.

Interpretation:

- Account-risk governance overrides raw sizing.

Benefit:

- Prevents extreme exposure.

Risk:

- Clipping changes realized exposure.
- This likely requires H018 and must coordinate with the maximum notional/leverage plan.

### 4. Mark Run Invalid But Continue Diagnostics

The engine records the violation and continues only in diagnostic mode.

Interpretation:

- Useful for counting cases before choosing a validation policy.

Benefit:

- Generates evidence without claiming validity.

Risk:

- Must not be confused with promotable validation.

## Required Synthetic Tests Before Implementation

Before any code change, the project should define synthetic tests covering at least:

1. Long trade where raw and executable references both agree the stop is valid.
2. Short trade where raw and executable references both agree the stop is valid.
3. Long stop above raw entry but below executable buy entry.
4. Long stop equal to raw entry.
5. Long stop equal to executable buy entry.
6. Short stop below raw entry but above executable sell entry.
7. Short stop equal to raw entry.
8. Short stop equal to executable sell entry.
9. Case where raw-entry sizing and executable-entry sizing produce materially different lots.
10. Case where executable-entry sizing would reduce lots relative to raw-entry sizing.
11. Case where executable-entry sizing would increase lots relative to raw-entry sizing.
12. The selected violation policy is explicit and tested.
13. If diagnostic classification is used, each class is counted and reported.
14. Test count does not drop below the current full-test anchor unless an explicit test-removal phase exists.

## Required Documentation Before Real-Data Use

Before any real-data run under changed sizing-reference semantics, the project must document:

1. The selected sizing reference.
2. The selected directional stop-validity reference.
3. Whether the references are raw, executable, both, or separately named.
4. The selected violation policy.
5. Whether the implementation belongs to H018.
6. Whether the run is diagnostic-only or H018 validation.
7. Why the run is not H017 promotion.
8. How the original H017 insolvency result remains visible.

## Relationship To Other H018 Decision Plans

Executable-entry sizing is linked to:

- Minimum stop-distance governance.
- Maximum notional / leverage governance.
- Invalid-stop behavior.
- Cost model semantics.
- Broker margin approximation.

Changing the sizing reference can change both the stop-distance denominator and the resulting exposure.

Therefore, executable-entry sizing should not be implemented independently as a quick fix.

## H017 / H018 Boundary

Changing raw-entry versus executable-entry sizing can materially change lot sizes, trade eligibility, realized exposure, and validation outcome.

Therefore, the working assumption is:

- Do not change sizing-reference semantics to rehabilitate H017.
- Treat executable-entry sizing adoption as H018 unless a later decision record explicitly proves otherwise.
- Any H018 version must define the sizing and validity references before validation.
- Any real-data run after adopting changed sizing-reference semantics is diagnostic-only or H018 validation, not H017 promotion.

## Non-Promotion Statement

This plan does not approve live trading.

This plan does not approve Phase 4 execution work.

This plan does not validate H018.

This plan does not repair H017.

This plan only defines the executable-entry sizing governance questions that must be answered before implementation.
