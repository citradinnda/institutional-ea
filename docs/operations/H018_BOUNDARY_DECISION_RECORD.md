# H018 Boundary Decision Record

Decision title: H018 hypothesis boundary.
Decision identifier: H018-BDR-001.
Decision status: Draft.
Date: 2026-05-04.
Related hypothesis: H018 candidate successor hypothesis.
Related documents:

- docs/operations/H017_EXECUTION_SEMANTICS_DECISION_RECORD.md
- docs/operations/H017_NEAR_ZERO_STOP_DISTANCE_DIAGNOSTIC.md
- docs/operations/H018_BOUNDARY_DECISION_PLAN.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md
- docs/operations/H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md
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

This draft decision record defines the boundary between failed H017 evidence and any future H018 successor work.

It exists to prevent execution-semantics and account-risk changes from becoming silent H017 repairs.

This draft does not choose any sizing reference, stop-distance threshold, leverage threshold, notional cap, skip rule, clipping rule, or validation rule.

This draft does not authorize implementation.

This draft does not authorize a real-data rerun.

This draft does not approve live trading.

This draft does not approve Phase 4 execution work.

## Scope

This decision record affects:

1. H018 hypothesis boundary.
2. Real-data validation classification.
3. H017 non-promotion language.
4. H018 claim relationship.

This decision record does not affect:

1. Entry sizing reference.
2. Stop-validity reference.
3. Equality behavior.
4. Minimum stop-distance rule.
5. Minimum stop-distance violation policy.
6. Maximum notional or leverage rule.
7. Maximum exposure violation policy.
8. Trade skipping.
9. Trade clipping.
10. Audit output requirements for a specific guard.

Those subjects require separate H018 decision records before implementation.

## Current Behavior

H017 remains failed and not promotable.

H017 failed strict expanded broker-native event validation by insolvency on a complete strict bridge window.

The historical H017 failure remains visible and must not be overwritten by later fail-closed behavior, guard implementation, reruns, or documentation cleanup.

Current H017 event sizing uses the raw H4 entry open before spread.

Current raw-entry invalid-stop behavior fails closed for invalid directional geometry:

1. A long or buy stop must be below the raw H4 entry open.
2. A short or sell stop must be above the raw H4 entry open.
3. Equality is invalid.

Invalid directional stops are not skipped silently.

Invalid directional stops are not clipped.

Positive near-zero stop distance remains an open execution-semantics and account-risk issue.

No minimum stop-distance threshold has been selected.

No maximum notional threshold has been selected.

No maximum leverage threshold has been selected.

No executable-entry sizing reference has been adopted.

No H018 implementation exists.

No H018 validation exists.

No H018 claim has been accepted.

## Draft Boundary Decision

The draft boundary is:

1. H017 is the failed historical hypothesis.
2. H017 must remain failed and not promotable under the original strict expanded broker-native evidence.
3. H017 must not be rehabilitated by later execution-semantics or account-risk changes.
4. Any future change that materially affects trade eligibility, position sizing, realized exposure, account survivability, or PnL path should be treated as H018 unless a later accepted decision record explicitly proves otherwise.
5. H018 may inherit H017 alpha logic, but it must define its own execution and account-risk semantics before validation.
6. Any future real-data run under changed semantics must be classified as diagnostic-only or H018 validation.
7. No future real-data run under changed semantics may be described as H017 promotion.

This is a draft boundary only.

It is not accepted for implementation.

## Units And Instruments

This draft boundary applies to the current candidate research scope:

1. USDJPY.
2. XAUUSD.
3. Broker-native H4 bars.
4. Broker-native M1 bridge-window execution.
5. Exness demo MT5 exports conditionally accepted only under strict complete-window rules.

This draft does not define numeric units for minimum stop distance, notional exposure, leverage, margin, or friction burden.

Those units must be defined in separate decision records if those policies are pursued.

## Effect On Trade Eligibility

This draft does not change trade eligibility.

No trade is accepted, rejected, skipped, clipped, or failed closed by this draft alone.

## Effect On Realized Exposure

This draft does not change realized exposure.

No lot size, notional amount, leverage amount, margin amount, or risk fraction is changed by this draft alone.

## Effect On PnL Path

This draft does not change the PnL path.

Any future implementation that changes trade eligibility, sizing, fills, costs, skips, clips, or guard behavior must be treated as a separate H018 implementation candidate.

## Rejected Alternatives

The following alternatives are rejected at the draft-boundary level:

1. Treating future execution-semantics changes as H017 repairs.

   Rejected because H017 already failed strict expanded broker-native event validation by insolvency.

2. Treating a fail-closed guard as H017 promotion.

   Rejected because a guard can change failure mode visibility but does not erase the original failed validation evidence.

3. Treating H018 as validated before implementation and real-data validation.

   Rejected because H018 has no implemented policy, no accepted claim, and no validation result.

4. Treating future strict real-data reruns as H017 promotion.

   Rejected because any rerun after changed semantics would no longer be the original H017 evidence path.

5. Choosing thresholds inside the boundary record.

   Rejected because minimum stop distance, maximum notional, maximum leverage, skipping, and clipping each require separate decision records.

## Deferred Alternatives

The following alternatives are deferred to future decision records:

1. Preserve raw-entry sizing.
2. Use executable-entry sizing.
3. Use both raw and executable references.
4. Require both raw and executable stop validity.
5. Fail closed on minimum-distance violations.
6. Skip trades on minimum-distance violations.
7. Clip trade size on exposure violations.
8. Fail closed on exposure violations.
9. Continue as diagnostic-only on guard violations.
10. Apply maximum notional or leverage limits.
11. Define a formal H018 claim gate.

No deferred alternative is chosen here.

## Synthetic Test Requirements

No code implementation is authorized by this draft, so no synthetic tests are required before committing this documentation-only record.

If this draft is later promoted to accepted-for-implementation status and used to authorize code, the relevant implementation decision records must define focused synthetic tests before code changes.

At minimum, future implementation-specific records must cover:

1. Below-boundary behavior.
2. Exact-boundary behavior.
3. Above-boundary behavior.
4. Long-side behavior.
5. Short-side behavior.
6. USDJPY conversion behavior if exposure or PnL is affected.
7. XAUUSD USD-denominated exposure behavior if exposure is affected.
8. Multi-symbol overlap behavior if portfolio-level exposure is affected.
9. Audit output for accepted, failed, skipped, clipped, or diagnostic-only trades.
10. Regression protection for existing H017 invalid-stop behavior if unchanged.

## Real-Data Run Classification

No real-data run is authorized by this draft.

This draft does not authorize:

1. H017 promotion rerun.
2. H018 diagnostic rerun.
3. H018 validation rerun.
4. Phase 4 execution dry run.
5. Live trading.

Any future real-data run must be authorized by a separate decision record or claim document.

A real-data run after H018 semantics changes must never be described as H017 promotion.

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

This draft does not impose implementation audit output because it does not implement a guard.

Future decision records that affect trade eligibility or exposure must require audit output showing:

1. Which rule was applied.
2. Which trades were accepted.
3. Which trades failed closed.
4. Which trades were skipped, if skipping is selected.
5. Which trades were clipped, if clipping is selected.
6. Which trades continued as diagnostic-only, if diagnostic continuation is selected.
7. The raw input values used by the rule.
8. The derived threshold or cap.
9. The final accepted or rejected value.

## Implementation Gate

No code implementation should begin from this draft.

Before implementation of any H018 boundary-affecting behavior:

1. The relevant decision record must be accepted for implementation.
2. Required synthetic tests must be listed.
3. Real-data run classification must be explicit.
4. Non-promotion language must be present.
5. H018 claim relationship must be clear.

## Current Verdict

This is a draft boundary decision record only.

No H018 rule is chosen here.

No H018 guard is implemented here.

No H018 threshold is chosen here.

No H018 sizing reference is chosen here.

No H018 real-data run is authorized here.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
