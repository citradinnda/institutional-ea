# H018 Maximum Notional / Leverage Decision Record

Decision title: H018 maximum notional / leverage decision record.
Decision identifier: H018-MAX-NOTIONAL-LEVERAGE.
Decision status: Draft.
Date: 2026-05-04.
Related hypothesis: H018.
Related documents:

- docs/operations/H018_BOUNDARY_DECISION_PLAN.md
- docs/operations/H018_BOUNDARY_DECISION_RECORD.md
- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md
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

This draft decision record captures the H018 maximum notional / leverage governance question.

It exists to prevent future exposure caps, leverage caps, margin approximations, trade skipping, or trade clipping from becoming silent repairs to the failed H017 validation.

This record is Draft only.

It does not choose a maximum notional threshold.

It does not choose a maximum leverage threshold.

It does not choose an exposure measurement basis.

It does not choose a violation policy.

It does not implement code.

It does not authorize a real-data rerun.

It does not validate H018.

It does not repair H017.

It does not approve live trading.

It does not approve Phase 4 execution work.

## Scope

This draft decision record concerns possible H018 account-risk and exposure governance.

It may later affect:

1. Maximum notional or leverage rule.
2. Maximum exposure violation policy.
3. Trade eligibility.
4. Trade clipping.
5. Trade skipping.
6. Diagnostic-only continuation.
7. Audit output.
8. Real-data validation classification.
9. H018 hypothesis boundary.

This draft record does not currently affect:

1. Entry sizing reference.
2. Stop-validity reference.
3. Equality behavior.
4. Minimum stop-distance rule.
5. Minimum stop-distance violation policy.
6. Existing H017 invalid-stop behavior.

Those topics remain governed by separate H018 decision records or plans.

## Current Behavior

H017 remains failed and not promotable.

H018 remains unimplemented, unvalidated, and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.

The strict expanded broker-native H017 event validation failed by account insolvency.

The fatal validation interval included a pathological USDJPY position size of 518.77 lots before the later raw-entry invalid-stop guard was implemented.

Current H017 event sizing uses the raw H4 entry open before spread when computing the stop-distance denominator.

Current raw-entry invalid-stop behavior fails closed for invalid directional geometry.

Under current raw-entry stop validity, long or buy stops must be below the raw H4 entry open.

Under current raw-entry stop validity, short or sell stops must be above the raw H4 entry open.

Equality is invalid under current raw-entry stop validity.

Invalid directional stop geometry is not skipped silently and is not clipped.

Positive near-zero stop distance remains an open account-risk issue.

No minimum stop-distance threshold has been selected.

No maximum notional threshold has been selected.

No maximum leverage threshold has been selected.

No executable-entry sizing rule has been adopted.

No exposure cap has been implemented.

No maximum-margin-usage approximation has been implemented.

No friction-burden cap has been implemented.

## Draft Non-Decision

This draft does not select any maximum exposure rule.

No threshold is chosen for:

1. Broker lots.
2. Fixed notional.
3. Notional divided by equity.
4. Per-trade gross leverage.
5. Per-symbol gross leverage.
6. Portfolio gross leverage.
7. Broker margin usage.
8. Spread burden.
9. Commission burden.
10. Expected slippage burden.
11. Stop-loss plus all-in friction burden.

No measurement basis is chosen for:

1. Lots.
2. Quote-currency notional.
3. USD-converted notional.
4. Notional divided by equity.
5. Per-trade leverage.
6. Per-symbol leverage.
7. Portfolio leverage.
8. Margin usage.
9. Friction burden.
10. Expected loss under stop plus friction.

No instrument-specific exposure convention is chosen for:

1. USDJPY.
2. XAUUSD.

No rule is chosen for whether USDJPY and XAUUSD should share one threshold or use symbol-specific thresholds.

No rule is chosen for whether exposure should be measured before spread, after spread, after commission, after slippage, or under an all-in executable reference.

No rule is chosen for whether an exposure guard is execution realism, account-risk governance, broker-margin approximation, strategy logic, or a combination.

## Candidate Decision Questions

A future accepted decision must answer at least these questions before implementation:

1. Should H018 enforce any maximum notional or leverage rule?
2. If yes, what exact exposure measure is used?
3. What exact threshold formula is used?
4. Is the threshold fixed or equity-scaled?
5. Is the threshold global, symbol-specific, per-trade, per-symbol, or portfolio-wide?
6. Is USDJPY notional converted to USD before comparison?
7. How is XAUUSD notional interpreted?
8. Are spread, commission, and slippage included in the exposure or burden calculation?
9. Is margin usage approximated?
10. If margin usage is approximated, what broker assumptions are used?
11. What happens when the rule is violated?
12. Does the selected rule create H018 rather than repairing H017?
13. What audit output is required?
14. What synthetic tests must pass before implementation?
15. What real-data run classification is permitted after implementation?

## Candidate Exposure Measures Not Yet Chosen

### Broker Lots

A future rule could cap broker lots directly.

This is not chosen.

Reason to consider:

- It directly prevents extreme order sizes.

Risk:

- Lot limits are symbol-specific.
- Lot limits alone do not normalize by account equity.
- Lot limits alone do not represent USDJPY and XAUUSD economic exposure consistently.

### Fixed Notional

A future rule could cap fixed notional exposure.

This is not chosen.

Reason to consider:

- It directly limits gross exposure.

Risk:

- Fixed notional limits do not scale with equity unless explicitly designed to do so.
- USDJPY quote-currency notional and XAUUSD USD-denominated exposure require careful convention definitions.

### Notional Divided By Equity

A future rule could cap notional exposure divided by account equity.

This is not chosen.

Reason to consider:

- It scales with account size.

Risk:

- The project must define notional consistently across instruments.
- USDJPY conversion to USD must be explicit.
- XAUUSD contract interpretation must be explicit.

### Per-Trade Gross Leverage

A future rule could cap leverage from a single trade.

This is not chosen.

Reason to consider:

- It prevents one trade from dominating the account.

Risk:

- It can materially alter realized exposure.
- It can become a strategy-level account-risk rule rather than pure execution realism.

### Portfolio Gross Leverage

A future rule could cap total open exposure after adding a trade.

This is not chosen.

Reason to consider:

- H017 was portfolio-aware but still produced pathological exposure.
- Overlapping positions can create portfolio-level exposure risk that per-trade rules may miss.

Risk:

- It requires precise open-position accounting.
- It can materially change multi-symbol behavior.
- It likely belongs to H018 unless later proven otherwise.

### Margin Usage

A future rule could approximate broker margin usage.

This is not chosen.

Reason to consider:

- Retail accounts are constrained by margin.

Risk:

- Broker margin rules vary by account, symbol, time, leverage setting, and regulatory environment.
- A simplified margin model may create false precision.
- Any approximation must be labeled as an approximation.

### Friction Burden

A future rule could cap spread, commission, and expected slippage burden relative to intended risk or equity.

This is not chosen.

Reason to consider:

- The H017 fatal event was strongly affected by huge commission from extreme lots.

Risk:

- Friction-burden rules overlap with minimum stop-distance logic.
- They require symbol-specific conversion and cost conventions.
- They may materially alter trade eligibility.

## Candidate Violation Policies Not Yet Chosen

### Fail Closed

A future rule could raise an explicit error when exposure exceeds the selected threshold.

This is not chosen.

Interpretation if later selected:

- The strategy produced exposure outside the declared validation envelope.

Benefit:

- It prevents silent trade-history mutation.

Risk:

- It may stop validation early and fail to summarize all later violations.

### Skip Trade

A future rule could skip the violating trade.

This is not chosen.

Interpretation if later selected:

- The trade is considered untradeable under the declared account-risk model.

Benefit:

- It lets the backtest continue.

Risk:

- Skipping changes trade eligibility.
- Skipping can become hidden optimization.
- Skipping likely creates H018 rather than repairing H017.

### Clip Position Size

A future rule could reduce position size to the selected exposure cap.

This is not chosen.

Interpretation if later selected:

- Account-risk governance overrides raw strategy sizing.

Benefit:

- It prevents extreme exposure while preserving partial participation.

Risk:

- Clipping changes realized exposure and the PnL path.
- Clipping may improve backtest outcomes by construction.
- Clipping likely creates H018 rather than repairing H017.

### Diagnostic-Only Continuation

A future rule could mark the run invalid but continue only to count and audit exposure violations.

This is not chosen.

Interpretation if later selected:

- The output is evidence-gathering only and not validation.

Benefit:

- It can measure how often violations occur before choosing a policy.

Risk:

- Diagnostic continuation must not be confused with promotable validation.

## Rejected Alternatives

No alternative is rejected by this draft.

This is intentional.

Because the record is Draft, it preserves the decision space instead of selecting or rejecting policies prematurely.

A later Proposed or Accepted decision must explicitly list rejected alternatives and the reason each alternative was rejected.

## Required Synthetic Tests Before Any Implementation

No implementation is authorized by this draft.

If a later decision becomes Accepted for implementation, it must define focused synthetic tests before code changes.

Required cases should include at least:

1. Normal USDJPY exposure below the selected threshold.
2. Normal XAUUSD exposure below the selected threshold.
3. Extreme USDJPY exposure above the selected threshold.
4. Extreme XAUUSD exposure above the selected threshold.
5. Exact-boundary behavior.
6. Below-boundary behavior.
7. Above-boundary behavior.
8. Long-side behavior.
9. Short-side behavior.
10. USDJPY conversion behavior if notional, leverage, margin, or friction burden is measured in USD.
11. XAUUSD USD-denominated exposure behavior if exposure is measured.
12. Multi-symbol overlap behavior if portfolio exposure is measured.
13. Audit output for accepted trades.
14. Audit output for fail-closed violations if fail-closed is selected.
15. Audit output for skipped trades if skipping is selected.
16. Audit output for clipped trades if clipping is selected.
17. Audit output for diagnostic-only continuation if diagnostic continuation is selected.
18. Regression protection for existing H017 raw-entry invalid-stop behavior if unchanged.
19. Full test count protection against dropping below the current 537-test anchor unless an explicit test-removal phase exists.

## Required Real-Data Run Classification

No real-data run is authorized by this draft.

A future real-data run after maximum notional / leverage semantics are changed must be classified as one of:

1. Diagnostic-only run.
2. H018 validation run after a formal H018 claim exists.

A real-data run after H018 semantics changes must never be described as H017 promotion.

A passing real-data run after implementation would not automatically validate H018.

A passing real-data run after implementation would not approve live trading.

A passing real-data run after implementation would not approve Phase 4 execution.

## Required Audit Output If Later Implemented

If a future accepted decision affects exposure or trade eligibility, implementation must emit or preserve audit output showing:

1. Which exposure rule was applied.
2. Which threshold formula was applied.
3. Which threshold value was derived.
4. Which raw input values were used.
5. Which symbol was evaluated.
6. Which side was evaluated.
7. Which entry reference was used.
8. Which account equity value was used.
9. Which lots value was produced before the exposure rule.
10. Which notional value was produced before the exposure rule.
11. Which leverage value was produced before the exposure rule, if leverage is selected.
12. Which margin value was produced before the exposure rule, if margin is selected.
13. Which friction-burden value was produced before the exposure rule, if friction burden is selected.
14. Which trades were accepted.
15. Which trades failed closed.
16. Which trades were skipped, if skipping is selected.
17. Which trades were clipped, if clipping is selected.
18. Which trades continued as diagnostic-only, if diagnostic continuation is selected.
19. The final accepted, rejected, skipped, clipped, or diagnostic-only value.

## Implementation Gate

No code implementation should begin from this draft.

Implementation remains blocked until a later decision record states:

1. Decision status is Accepted for implementation.
2. The exact maximum notional or leverage rule is selected.
3. The exact measurement basis is selected.
4. The exact threshold formula is selected.
5. The exact violation policy is selected.
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

No maximum notional threshold is chosen.

No maximum leverage threshold is chosen.

No exposure measurement basis is chosen.

No violation policy is chosen.

No implementation is authorized.

No validation rerun is authorized.

No H018 claim is accepted.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
