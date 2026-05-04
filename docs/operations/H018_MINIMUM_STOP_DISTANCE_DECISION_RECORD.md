# H018 Minimum Stop-Distance Decision Record

Decision title: H018 minimum stop-distance rule.
Decision identifier: H018-MSDR-001.
Decision status: Draft.
Date: 2026-05-04.
Related hypothesis: H018 candidate successor hypothesis.
Related documents:

- docs/operations/H017_EXECUTION_SEMANTICS_DECISION_RECORD.md
- docs/operations/H017_NEAR_ZERO_STOP_DISTANCE_DIAGNOSTIC.md
- docs/operations/H018_BOUNDARY_DECISION_PLAN.md
- docs/operations/H018_BOUNDARY_DECISION_RECORD.md
- docs/operations/H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md
- docs/operations/H018_SIZING_REFERENCE_DECISION_RECORD.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md
- docs/operations/H018_DECISION_MATRIX.md
- docs/operations/H018_CLAIM_SKELETON.md
- docs/operations/H018_DECISION_RECORD_TEMPLATE.md
- docs/operations/H018_DECISION_RECORD_INDEX.md

Owner or reviewer: solo retail trader with AI engineering review.
Implementation status: not implemented.
Validation status: not validated.
Live-trading status: not approved.
Phase 4 execution status: not approved.

## Purpose

This draft decision record defines the unresolved H018 minimum stop-distance question.

It exists to prevent positive near-zero stop-distance handling from becoming a silent repair to failed H017 evidence.

This draft does not choose a minimum stop-distance rule.

This draft does not choose a numeric threshold.

This draft does not choose spread, ATR, tick size, broker point, all-in friction, or a combined maximum as the reference.

This draft does not choose fail-closed, skip, clip, or diagnostic-continuation behavior.

This draft does not authorize implementation.

This draft does not authorize a real-data rerun.

This draft does not approve live trading.

This draft does not approve Phase 4 execution work.

## Scope

This decision record affects the following open decision areas:

1. Minimum stop-distance rule.
2. Minimum stop-distance threshold reference.
3. Minimum stop-distance violation policy.
4. Real-data validation classification after any future minimum-distance rule.
5. H017 non-promotion language.
6. H018 claim relationship.

This decision record does not choose a policy for:

1. Entry sizing reference.
2. Stop-validity reference.
3. Maximum notional or leverage rule.
4. Maximum exposure violation policy.
5. Trade skipping.
6. Trade clipping.
7. Portfolio-level exposure caps.
8. Margin approximation.
9. Live deployment.

Those subjects require separate H018 decision records before implementation.

## Current Behavior

H017 remains failed and not promotable.

H017 failed strict expanded broker-native event validation by insolvency on a complete strict bridge window.

The historically important failure included a pathological USDJPY trade caused by a near-zero raw-entry stop-distance denominator before the invalid-stop guard existed.

Current H017 event sizing uses the raw H4 entry open before spread.

Current H017 raw-entry invalid-stop behavior fails closed for invalid directional geometry:

1. A long or buy stop must be below the raw H4 entry open.
2. A short or sell stop must be above the raw H4 entry open.
3. Equality is invalid.

Invalid directional stops are not skipped silently.

Invalid directional stops are not clipped.

The current sizing API rejects zero and negative stop distances.

The current sizing API does not reject positive near-zero stop distances solely because they are near zero.

Positive near-zero stop distance remains an open execution-semantics and account-risk issue.

No minimum stop-distance threshold has been selected.

No minimum stop-distance violation policy has been selected.

No maximum notional threshold has been selected.

No maximum leverage threshold has been selected.

No executable-entry sizing has been adopted.

No H018 implementation exists.

No H018 validation exists.

No H018 claim has been accepted.

## Draft Minimum Stop-Distance Question

The unresolved minimum stop-distance question is:

Should future H018 require a positive stop distance to also be large enough relative to one or more market, broker, or risk references?

If yes, a future accepted decision record must define:

1. The stop-distance reference.
2. The threshold formula.
3. The threshold units.
4. The instruments affected.
5. Whether USDJPY and XAUUSD are handled differently.
6. The selected violation policy.
7. Whether the rule changes trade eligibility.
8. Whether the rule changes realized exposure.
9. Whether the rule changes the PnL path.
10. Whether the rule creates H018 rather than repairing H017.

No option is selected by this draft.

## Candidate Minimum-Distance References

### 1. Spread Multiple

Under this candidate, stop distance would need to exceed a multiple of spread.

Potential advantage:

1. Links minimum distance to entry friction.
2. Prevents sizing from being dominated by a distance smaller than the quoted spread.
3. Is simple to explain.

Potential risk:

1. Fixed historical spread assumptions may understate real spread variation.
2. Spread-based filtering can change trade eligibility.
3. Symbol-specific spread conventions are required.
4. It may not be sufficient to prevent extreme notional exposure.

### 2. ATR Fraction

Under this candidate, stop distance would need to exceed a fraction of ATR.

Potential advantage:

1. Links minimum distance to recent volatility.
2. Adapts to instrument regime changes.
3. Can prevent stops that are tiny relative to normal price movement.

Potential risk:

1. ATR thresholds can become strategy logic rather than pure execution realism.
2. ATR calculation choices can affect eligibility.
3. Changing ATR-based eligibility can materially alter the hypothesis.
4. It likely requires H018 if adopted.

### 3. Tick Size Or Broker Point Multiple

Under this candidate, stop distance would need to exceed a number of ticks or broker points.

Potential advantage:

1. Prevents mathematically positive but practically negligible stop distances.
2. Aligns with broker precision.
3. Can be tested deterministically.

Potential risk:

1. Tick or point rules alone may be too small to prevent extreme leverage.
2. Symbol-specific point definitions are required.
3. Broker metadata may differ across account types.
4. It may need to be combined with another rule.

### 4. All-In Friction Multiple

Under this candidate, stop distance would need to exceed a multiple of expected all-in friction.

Friction may include:

1. Spread.
2. Commission converted into price-distance equivalent.
3. Stop slippage estimate.

Potential advantage:

1. Connects minimum distance to expected execution cost.
2. Can prevent trades where friction dominates the intended risk.
3. Makes cost burden visible.

Potential risk:

1. Commission-to-price-distance conversion is symbol-specific.
2. The formula may depend on lot size, account equity, or conversion price.
3. Circularity can occur if lot size is needed before the threshold can be computed.
4. Complexity can hide tuning.

### 5. Combined Maximum Rule

Under this candidate, stop distance would need to exceed the maximum of several references, such as:

1. Spread multiple.
2. ATR fraction.
3. Tick or point multiple.
4. All-in friction multiple.

Potential advantage:

1. Avoids relying on one fragile threshold.
2. Can be conservative across different market regimes.
3. Can handle both broker precision and volatility scale.

Potential risk:

1. More complex than a single-reference rule.
2. Requires careful audit output.
3. Can reject more trades.
4. Can become hidden strategy filtering if not governed explicitly.

## Candidate Violation Policies

If a future minimum stop-distance rule is violated, the project must choose one explicit violation policy.

No violation policy is chosen here.

Candidate policies include:

1. Fail closed with an explicit error.
2. Skip the trade and continue.
3. Clip or resize the position and continue.
4. Mark the run invalid but continue diagnostics only.

Skipping and clipping can materially change the realized strategy and must not be introduced without an accepted H018 decision record.

## Draft Non-Decision

This draft makes the following non-decision:

1. No minimum stop-distance rule is selected.
2. No minimum stop-distance threshold is selected.
3. No spread multiple is selected.
4. No ATR fraction is selected.
5. No tick-size multiple is selected.
6. No broker-point multiple is selected.
7. No all-in friction multiple is selected.
8. No combined maximum rule is selected.
9. No minimum-distance violation policy is selected.
10. No fail-closed policy is selected for a new H018 minimum-distance rule.
11. No trade-skip policy is selected.
12. No clipping policy is selected.
13. No diagnostic-continuation policy is selected.
14. No implementation is authorized.
15. No real-data run is authorized.
16. No H018 validation is authorized.
17. No live trading is approved.
18. No Phase 4 execution work is approved.

## Units And Instruments

This draft applies to the current candidate research scope:

1. USDJPY.
2. XAUUSD.
3. Broker-native H4 bars.
4. Broker-native M1 bridge-window execution.
5. Exness demo MT5 exports conditionally accepted only under strict complete-window rules.

Potential stop-distance units are instrument price units:

1. USDJPY price distance is measured in JPY per USD.
2. XAUUSD price distance is measured in USD per troy ounce.

Potential threshold references may use:

1. Spread price distance.
2. ATR price distance.
3. Tick size.
4. Broker point.
5. Commission converted into price distance.
6. Slippage converted into price distance.
7. A maximum of multiple references.

This draft does not select any numeric value in those units.

This draft does not define notional, leverage, margin, or friction-burden caps.

## Effect On Trade Eligibility

This draft does not change trade eligibility.

No trade is accepted, rejected, skipped, clipped, or failed closed by this draft alone.

Any future accepted decision that adds a minimum stop-distance rule can change trade eligibility and must be treated as an H018 semantics change unless separately proven otherwise.

## Effect On Realized Exposure

This draft does not change realized exposure.

No lot size, notional amount, leverage amount, margin amount, or risk fraction is changed by this draft alone.

Any future accepted decision that clips or resizes trades after a minimum-distance violation can change realized exposure and must be treated as an H018 semantics change unless separately proven otherwise.

## Effect On PnL Path

This draft does not change the PnL path.

Any future implementation that changes stop-distance eligibility, sizing, skips, clips, guard behavior, fills, or costs can change the PnL path and must be classified as H018 implementation work or diagnostics, not H017 promotion.

## Rejected Alternatives

The following alternatives are rejected at the draft level:

1. Silently accepting all positive near-zero stop distances as solved.

   Rejected because positive near-zero stop distance remains an open account-risk issue.

2. Silently adding a minimum stop-distance guard as an H017 repair.

   Rejected because H017 already failed strict expanded broker-native event validation by insolvency.

3. Choosing a threshold without a decision record.

   Rejected because threshold choice can change trade eligibility and validation outcome.

4. Treating skip or clip behavior as a harmless implementation detail.

   Rejected because skipping changes trade eligibility and clipping changes realized exposure.

5. Treating a future rerun after a minimum-distance rule as H017 promotion.

   Rejected because altered semantics would not be the original H017 evidence path.

## Deferred Alternatives

The following alternatives are deferred to future decision records:

1. Use a spread multiple.
2. Use an ATR fraction.
3. Use a tick-size multiple.
4. Use a broker-point multiple.
5. Use an all-in friction multiple.
6. Use a combined maximum rule.
7. Fail closed on minimum-distance violations.
8. Skip trades on minimum-distance violations.
9. Clip or resize trades on minimum-distance violations.
10. Mark the run invalid but continue diagnostics.
11. Define symbol-specific thresholds for USDJPY and XAUUSD.
12. Define one shared threshold formula for both symbols.
13. Require audit output for minimum-distance classification.

No deferred alternative is chosen here.

## Synthetic Test Requirements

No code implementation is authorized by this draft, so no synthetic tests are required before committing this documentation-only record.

If a later decision record is accepted for implementation, it must define focused synthetic tests before code changes.

At minimum, future minimum stop-distance implementation records must cover:

1. Directionally valid long stop with normal distance.
2. Directionally valid short stop with normal distance.
3. Directionally valid long stop with positive near-zero distance.
4. Directionally valid short stop with positive near-zero distance.
5. Stop distance below the selected threshold.
6. Stop distance exactly at the selected threshold.
7. Stop distance above the selected threshold.
8. Long-side behavior.
9. Short-side behavior.
10. USDJPY symbol-specific behavior if point, spread, commission, ATR, or conversion is used.
11. XAUUSD symbol-specific behavior if point, spread, commission, ATR, or conversion is used.
12. Equality remains invalid under the selected stop-validity semantics.
13. Directionally invalid stops still fail closed if the existing H017 invalid-stop behavior is unchanged.
14. The selected violation policy.
15. Audit output for accepted, failed, skipped, clipped, or diagnostic-only trades.
16. Test count preservation against the current full-test anchor unless an explicit test-removal phase exists.

## Real-Data Run Classification

No real-data run is authorized by this draft.

This draft does not authorize:

1. H017 promotion rerun.
2. H018 diagnostic rerun.
3. H018 validation rerun.
4. Phase 4 execution dry run.
5. Live trading.

Any future real-data run after minimum stop-distance changes must be authorized by a separate accepted decision record or claim document.

A real-data run after changed minimum-distance semantics must never be described as H017 promotion.

## Non-Promotion Language

H017 remains failed.

H017 is not promotable.

This draft does not repair H017.

This draft does not validate H018.

This draft does not approve live trading.

This draft does not approve Phase 4 execution.

Passing tests after any future implementation would not automatically approve live trading.

Any future H018 validation must be judged under an explicit H018 claim.

## Audit Requirements

This draft does not impose implementation audit output because it does not implement a minimum stop-distance rule.

Future decision records that affect minimum stop distance must require audit output showing:

1. Which minimum-distance rule was applied.
2. Which threshold reference was used.
3. Raw H4 entry open.
4. Executable entry after spread if applicable.
5. Stop price.
6. Selected stop-distance denominator.
7. Spread distance if used.
8. ATR distance if used.
9. Tick or point distance if used.
10. Friction distance if used.
11. Combined threshold if used.
12. Whether the trade was accepted.
13. Whether the trade failed closed.
14. Whether the trade was skipped, if skipping is selected.
15. Whether the trade was clipped, if clipping is selected.
16. Whether the trade continued as diagnostic-only, if diagnostic continuation is selected.
17. Final accepted or rejected lot size if sizing is affected.

## Implementation Gate

No code implementation should begin from this draft.

Before implementing any H018 minimum stop-distance behavior:

1. The relevant decision record must be accepted for implementation.
2. The selected threshold reference must be explicit.
3. The selected threshold formula must be explicit.
4. The selected units must be explicit.
5. USDJPY and XAUUSD handling must be explicit.
6. The selected violation policy must be explicit.
7. Required synthetic tests must be listed.
8. Real-data run classification must be explicit.
9. Non-promotion language must be present.
10. H018 claim relationship must be clear.

## Current Verdict

This is a draft minimum stop-distance decision record only.

No H018 minimum stop-distance rule is chosen here.

No H018 minimum stop-distance threshold is chosen here.

No H018 minimum-distance violation policy is chosen here.

No H018 guard is implemented here.

No H018 real-data run is authorized here.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
