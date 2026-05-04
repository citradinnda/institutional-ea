# H018 Trade Violation Policy Decision Record

Decision title: H018 trade violation policy decision record.
Decision identifier: H018-TRADE-VIOLATION-POLICY.
Decision status: Draft.
Date: 2026-05-04.
Related hypothesis: H018.
Related documents:

- docs/operations/H018_BOUNDARY_DECISION_PLAN.md
- docs/operations/H018_BOUNDARY_DECISION_RECORD.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md
- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md
- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md
- docs/operations/H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md
- docs/operations/H018_SIZING_REFERENCE_DECISION_RECORD.md
- docs/operations/H018_DECISION_MATRIX.md
- docs/operations/H018_CLAIM_SKELETON.md
- docs/operations/H018_DECISION_RECORD_TEMPLATE.md
- docs/operations/H018_DECISION_RECORD_INDEX.md
- docs/operations/H017_EXECUTION_SEMANTICS_DECISION_RECORD.md
- docs/operations/H017_NEAR_ZERO_STOP_DISTANCE_DIAGNOSTIC.md

Owner or reviewer: solo research owner.
Implementation status: not implemented.
Validation status: not validated.
Live-trading status: not approved.

## Purpose

This draft decision record captures the H018 trade violation policy question.

A trade violation policy defines what the research engine should do when a future H018 rule rejects or challenges a trade.

Examples include:

1. Invalid stop geometry.
2. Minimum stop-distance violation.
3. Maximum notional violation.
4. Maximum leverage violation.
5. Maximum margin-usage violation.
6. Maximum friction-burden violation.
7. Any future account-risk envelope violation.

This record exists to prevent trade skipping, position clipping, fail-closed behavior, or diagnostic-only continuation from becoming silent repairs to the failed H017 validation.

This record is Draft only.

It does not choose fail closed.

It does not choose skip trade.

It does not choose clip position size.

It does not choose diagnostic-only continuation.

It does not choose any minimum stop-distance rule.

It does not choose any maximum notional or leverage rule.

It does not implement code.

It does not authorize a real-data rerun.

It does not validate H018.

It does not repair H017.

It does not approve live trading.

It does not approve Phase 4 execution work.

## Scope

This draft decision record concerns possible H018 behavior after a trade violates a declared rule.

It may later affect:

1. Trade eligibility.
2. Trade rejection.
3. Trade skipping.
4. Position clipping.
5. Diagnostic-only continuation.
6. Audit output.
7. Real-data validation classification.
8. H018 hypothesis boundary.
9. PnL path comparability.

This draft record does not currently affect:

1. Entry sizing reference.
2. Stop-validity reference.
3. Equality behavior.
4. Minimum stop-distance threshold.
5. Maximum notional threshold.
6. Maximum leverage threshold.
7. Existing H017 raw-entry invalid-stop behavior.

Those topics remain governed by separate H018 decision records or plans.

## Current Behavior

H017 remains failed and not promotable.

H018 remains unimplemented, unvalidated, and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.

The strict expanded broker-native H017 event validation failed by account insolvency.

The fatal validation interval included a pathological USDJPY position size of 518.77 lots before the later raw-entry invalid-stop guard was implemented.

Current H017 event sizing uses the raw H4 entry open before spread when computing the stop-distance denominator.

Current raw-entry invalid-stop behavior fails closed for invalid directional stop geometry.

Under current raw-entry stop validity, long or buy stops must be below the raw H4 entry open.

Under current raw-entry stop validity, short or sell stops must be above the raw H4 entry open.

Equality is invalid under current raw-entry stop validity.

Invalid directional stop geometry is not skipped silently and is not clipped.

Positive near-zero stop distance remains an open account-risk issue.

No minimum stop-distance threshold has been selected.

No maximum notional threshold has been selected.

No maximum leverage threshold has been selected.

No trade-skip policy has been selected.

No clipping policy has been selected.

No diagnostic-only continuation policy has been selected.

No future H018 violation policy has been selected.

## Draft Non-Decision

This draft does not select a violation policy.

No policy is chosen for:

1. Fail closed.
2. Skip trade.
3. Clip position size.
4. Mark run invalid but continue diagnostics.
5. Warn and continue.
6. Log-only continuation.
7. Mixed policy by violation type.
8. Mixed policy by instrument.
9. Mixed policy by validation mode.

No rule is chosen for whether different violation types should share one common policy or use separate policies.

No rule is chosen for whether USDJPY and XAUUSD should have the same violation policy.

No rule is chosen for whether a violation should stop the whole run, stop only the current symbol, reject only the trade, clip only the lots, or continue only for diagnostics.

No rule is chosen for whether a violation policy belongs to execution realism, account-risk governance, broker-margin approximation, strategy logic, or a combination.

## Candidate Decision Questions

A future accepted decision must answer at least these questions before implementation:

1. What violation types are governed by the policy?
2. Is the same policy used for invalid stop geometry, minimum-distance violations, maximum-exposure violations, and margin or friction violations?
3. Should a violation fail closed?
4. Should a violation skip the trade?
5. Should a violation clip position size?
6. Should a violation mark the run invalid but continue diagnostics?
7. Should policy differ between research diagnostics and validation?
8. Should policy differ between USDJPY and XAUUSD?
9. Should policy differ between per-trade and portfolio-level violations?
10. Should a violation change trade eligibility?
11. Should a violation change realized exposure?
12. Should a violation change the PnL path?
13. What audit output is mandatory?
14. What synthetic tests must pass before implementation?
15. What real-data run classification is permitted after implementation?
16. Does the selected policy create H018 rather than repairing H017?

## Candidate Violation Policies Not Yet Chosen

### Fail Closed

A future rule could raise an explicit error when a violation occurs.

This is not chosen.

Interpretation if later selected:

- The strategy produced a trade outside the declared validation envelope.

Benefit:

- It prevents silent trade-history mutation.
- It keeps the invalid condition visible.
- It avoids pretending that skipped or clipped trades are the original strategy.

Risk:

- It may stop validation early.
- It may not summarize all later violations unless a separate diagnostic mode exists.

### Skip Trade

A future rule could skip the violating trade.

This is not chosen.

Interpretation if later selected:

- The trade is considered untradeable under the declared H018 account-risk or execution model.

Benefit:

- It allows the backtest to continue.
- It can represent a rule that certain trades are ineligible.

Risk:

- Skipping changes trade eligibility.
- Skipping changes the trade history.
- Skipping can become hidden optimization.
- Skipping likely creates H018 rather than repairing H017.

### Clip Position Size

A future rule could reduce the position size to the maximum allowed value.

This is not chosen.

Interpretation if later selected:

- Account-risk governance overrides raw strategy sizing.

Benefit:

- It can prevent pathological exposure while preserving partial participation.

Risk:

- Clipping changes realized exposure.
- Clipping changes the PnL path.
- Clipping may improve backtest outcomes by construction.
- Clipping likely creates H018 rather than repairing H017.

### Diagnostic-Only Continuation

A future rule could mark the run invalid but continue only to count and audit violations.

This is not chosen.

Interpretation if later selected:

- The run becomes evidence-gathering only and is not promotable validation.

Benefit:

- It can show how often violations occur before choosing a production-like policy.
- It preserves visibility into the strategy's failure modes.

Risk:

- Diagnostic continuation must not be confused with validation.
- Diagnostic output must not be used as live-trading evidence.

## Rejected Alternatives

No alternative is rejected by this draft.

This is intentional.

Because the record is Draft, it preserves the decision space instead of selecting or rejecting policies prematurely.

A later Proposed or Accepted decision must explicitly list rejected alternatives and the reason each alternative was rejected.

## Required Synthetic Tests Before Any Implementation

No implementation is authorized by this draft.

If a later decision becomes Accepted for implementation, it must define focused synthetic tests before code changes.

Required cases should include at least:

1. A normal trade with no violation is accepted.
2. A long-side violation triggers the selected policy.
3. A short-side violation triggers the selected policy.
4. A USDJPY violation triggers the selected policy.
5. An XAUUSD violation triggers the selected policy.
6. An exact-boundary case triggers the documented exact-boundary behavior.
7. A below-boundary case triggers the documented below-boundary behavior.
8. An above-boundary case triggers the documented above-boundary behavior.
9. If fail closed is selected, the error type and message are explicit.
10. If skip is selected, skipped trades are counted and reported.
11. If clipping is selected, clipped trades are counted and reported.
12. If diagnostic-only continuation is selected, the run is clearly marked invalid for validation.
13. If portfolio-level violations are governed, overlapping USDJPY and XAUUSD positions are tested.
14. Audit output identifies the rule, raw values, derived threshold, violation type, and selected action.
15. Regression protection confirms existing H017 raw-entry invalid-stop behavior remains unchanged unless explicitly superseded.
16. Full test count remains at or above the current 537-test anchor unless an explicit test-removal phase exists.

## Required Real-Data Run Classification

No real-data run is authorized by this draft.

A future real-data run after trade violation policy semantics are changed must be classified as one of:

1. Diagnostic-only run.
2. H018 validation run after a formal H018 claim exists.

A real-data run after H018 semantics changes must never be described as H017 promotion.

A passing real-data run after implementation would not automatically validate H018.

A passing real-data run after implementation would not approve live trading.

A passing real-data run after implementation would not approve Phase 4 execution.

## Required Audit Output If Later Implemented

If a future accepted decision affects trade eligibility or exposure, implementation must emit or preserve audit output showing:

1. Which violation policy was applied.
2. Which rule produced the violation.
3. Which threshold or boundary was used.
4. Which raw input values were used.
5. Which symbol was evaluated.
6. Which side was evaluated.
7. Which entry reference was used, if relevant.
8. Which stop reference was used, if relevant.
9. Which account equity value was used, if relevant.
10. Which lots value was produced before the policy, if relevant.
11. Which lots value was accepted after the policy, if relevant.
12. Which notional or leverage value was produced before the policy, if relevant.
13. Which trades were accepted.
14. Which trades failed closed.
15. Which trades were skipped, if skipping is selected.
16. Which trades were clipped, if clipping is selected.
17. Which trades continued as diagnostic-only, if diagnostic continuation is selected.
18. Whether the run remains eligible for validation after the policy action.
19. The final accepted, rejected, skipped, clipped, or diagnostic-only value.

## Implementation Gate

No code implementation should begin from this draft.

Implementation remains blocked until a later decision record states:

1. Decision status is Accepted for implementation.
2. The exact violation types governed by the policy are selected.
3. The exact violation policy is selected.
4. Any instrument-specific differences are selected.
5. Any validation-mode differences are selected.
6. Required synthetic tests are listed.
7. Required audit output is listed.
8. Real-data run classification is explicit.
9. Non-promotion language is present.
10. The H018 claim relationship is clear.

## Non-Promotion Statement

H017 remains failed.

H017 is not promotable.

This draft does not repair H017.

This draft does not validate H018.

This draft does not approve live trading.

This draft does not approve Phase 4 execution.

Passing future tests after implementation would not automatically approve live trading.

Any future H018 validation must be judged under an explicit H018 claim.

## Current Verdict

This is a Draft decision record only.

No fail-closed policy is chosen for future H018 violations.

No skip policy is chosen.

No clipping policy is chosen.

No diagnostic-only continuation policy is chosen.

No mixed violation policy is chosen.

No implementation is authorized.

No validation rerun is authorized.

No H018 claim is accepted.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
