# H018 Sizing Reference Decision Record

Decision title: H018 sizing reference and stop-validity reference.
Decision identifier: H018-SRDR-001.
Decision status: Draft.
Date: 2026-05-04.
Related hypothesis: H018 candidate successor hypothesis.
Related documents:

- docs/operations/H017_EXECUTION_SEMANTICS_DECISION_RECORD.md
- docs/operations/H017_NEAR_ZERO_STOP_DISTANCE_DIAGNOSTIC.md
- docs/operations/H018_BOUNDARY_DECISION_PLAN.md
- docs/operations/H018_BOUNDARY_DECISION_RECORD.md
- docs/operations/H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md
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

This draft decision record defines the unresolved H018 sizing-reference and stop-validity-reference question.

It exists to prevent raw-entry versus executable-entry changes from becoming silent repairs to failed H017 evidence.

This draft does not choose a sizing reference.

This draft does not choose a stop-validity reference.

This draft does not choose a minimum stop-distance threshold.

This draft does not choose a maximum notional or leverage threshold.

This draft does not choose a trade skipping rule.

This draft does not choose a trade clipping rule.

This draft does not authorize implementation.

This draft does not authorize a real-data rerun.

This draft does not approve live trading.

This draft does not approve Phase 4 execution work.

## Scope

This decision record affects the following open decision areas:

1. Entry sizing reference.
2. Stop-validity reference.
3. Equality behavior if a new reference is later selected.
4. Real-data validation classification after changed sizing semantics.
5. H017 non-promotion language.
6. H018 claim relationship.

This decision record does not choose a policy for:

1. Minimum stop-distance rule.
2. Minimum stop-distance violation policy.
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

The historically important failure included a pathological USDJPY trade:

1. Symbol: USDJPY.
2. Side: buy.
3. Raw H4 entry open: 110.770000000.
4. H017 long stop: 110.770240804.
5. Executable entry after spread: 110.775000000.
6. Lots before the invalid-stop guard: 518.77.

Before the invalid-stop guard, the event engine sized the trade from the absolute distance between raw H4 entry open and stop price before spread was applied.

That raw stop distance was positive but near zero.

The near-zero denominator created extreme lot sizing and contributed to account insolvency.

Current H017 event sizing uses the raw H4 entry open before spread.

Current H017 raw-entry invalid-stop behavior fails closed for invalid directional geometry:

1. A long or buy stop must be below the raw H4 entry open.
2. A short or sell stop must be above the raw H4 entry open.
3. Equality is invalid.

Invalid directional stops are not skipped silently.

Invalid directional stops are not clipped.

The current invalid-stop guard does not decide whether H018 should size from raw entry, executable entry, both, a conservative reference, or another separately named reference.

Positive near-zero stop distance remains an open execution-semantics and account-risk issue.

No minimum stop-distance threshold has been selected.

No maximum notional threshold has been selected.

No maximum leverage threshold has been selected.

No executable-entry sizing has been adopted.

No H018 implementation exists.

No H018 validation exists.

No H018 claim has been accepted.

## Draft Sizing Reference Question

The unresolved sizing-reference question is:

Should future H018 position sizing use:

1. Raw H4 entry open before spread.
2. Executable entry after spread.
3. Both raw and executable references.
4. A conservative worst-case reference.
5. A separately named sizing reference.
6. Another explicit reference not yet defined.

No option is selected by this draft.

## Draft Stop-Validity Reference Question

The unresolved stop-validity-reference question is:

Should future H018 directional stop validity be checked against:

1. Raw H4 entry open before spread.
2. Executable entry after spread.
3. Both raw and executable entry.
4. A separately named stop-validity reference.
5. Another explicit reference not yet defined.

No option is selected by this draft.

## Candidate Sizing References

### 1. Raw H4 Entry Open

Under this candidate, H018 would continue sizing from the raw broker-native H4 open before spread.

Potential advantage:

1. Preserves the historical H017 sizing convention.
2. Minimizes semantic drift from existing H017 tests.
3. Keeps spread application separate from the sizing denominator.

Potential risk:

1. Raw-entry distance can disagree with executable fill economics.
2. Raw-entry distance can be near zero even when executable-entry distance is larger.
3. Raw-entry sizing may leave positive near-zero stop-distance risk unresolved unless another guard is added.
4. Preserving raw-entry sizing may still require H018 if other execution or account-risk semantics change.

### 2. Executable Entry After Spread

Under this candidate, H018 would size from the simulated executable entry price after spread is applied.

For a buy, the executable entry is typically above the raw open.

For a sell, the executable entry is typically below the raw open.

Potential advantage:

1. Ties position size to the actual simulated entry price.
2. Aligns sizing with realized execution economics.
3. May make entry-to-stop risk more economically interpretable.

Potential risk:

1. Changes lot sizes relative to H017.
2. Changes validation comparability with H017.
3. Can alter trade eligibility if stop validity is also moved to executable-entry semantics.
4. Likely creates H018 rather than repairing H017.

### 3. Both Raw And Executable References

Under this candidate, H018 could require sizing or validity checks against both raw and executable entry references.

Potential advantage:

1. Conservative.
2. Makes raw-versus-executable disagreement explicit.
3. Can prevent cases that look acceptable under one reference but pathological under another.

Potential risk:

1. May reject more trades.
2. May act as a trade filter.
3. May materially change validation results.
4. Requires clear audit output to avoid hidden survivorship.

### 4. Conservative Worst-Case Reference

Under this candidate, H018 could choose the reference that produces the smaller position size or larger risk estimate.

Potential advantage:

1. Reduces exposure blowup risk.
2. Makes risk governance conservative by design.

Potential risk:

1. Is not a neutral implementation detail.
2. Changes realized exposure.
3. Could become a hidden tuning mechanism.
4. Requires separate interaction with maximum notional and leverage governance.

### 5. Separately Named Sizing Reference

Under this candidate, H018 could define a named reference such as:

1. `sizing_reference_price`.
2. `stop_distance_reference_price`.
3. `risk_reference_price`.

Potential advantage:

1. Avoids ambiguous language.
2. Lets tests assert exactly which reference is used.
3. Makes future audit output easier to interpret.

Potential risk:

1. Adds abstraction.
2. Must not become a hidden tuning parameter.
3. Must still define how the reference is computed for buys, sells, USDJPY, and XAUUSD.

## Candidate Stop-Validity References

### 1. Raw-Entry Stop Validity

This is the current implemented H017 invalid-stop guard.

A long or buy stop must be below raw H4 entry open.

A short or sell stop must be above raw H4 entry open.

Equality is invalid.

Potential advantage:

1. Already implemented.
2. Already covered by focused synthetic tests.
3. Preserves current H017 fail-closed behavior.

Potential risk:

1. Does not answer whether executable-entry validity is more appropriate for H018.
2. Does not by itself solve positive near-zero stop-distance risk.
3. May disagree with executable-entry economics.

### 2. Executable-Entry Stop Validity

Under this candidate, H018 could require:

1. A long or buy stop below the executable buy entry.
2. A short or sell stop above the executable sell entry.
3. Equality invalid against the executable entry.

Potential advantage:

1. Checks validity against the simulated fill price.
2. May better match the economic trade being executed.

Potential risk:

1. Can accept cases that raw-entry validity rejects.
2. Can reject cases that raw-entry validity accepts.
3. Changes trade eligibility.
4. Likely belongs to H018 rather than H017.

### 3. Both Raw And Executable Stop Validity

Under this candidate, H018 could require both references to be valid.

For a long or buy trade, the stop would need to be below both raw entry and executable entry.

For a short or sell trade, the stop would need to be above both raw entry and executable entry.

Equality would be invalid against either reference.

Potential advantage:

1. Conservative.
2. Explicitly handles disagreement between raw and executable references.
3. Reduces ambiguous geometry.

Potential risk:

1. Can become a stricter trade filter.
2. May reject otherwise tradable events.
3. Must be treated as an H018 semantics change if adopted.

### 4. Diagnostic Classification Before Policy Choice

Under this candidate, a diagnostic mode could classify each candidate trade as:

1. Valid under raw-entry semantics.
2. Valid under executable-entry semantics.
3. Valid under both.
4. Valid under neither.

Potential advantage:

1. Provides evidence before choosing a policy.
2. Helps quantify how often raw and executable semantics disagree.

Potential risk:

1. Must not be treated as validation.
2. Must not be treated as H017 promotion.
3. Must not silently affect trade eligibility or realized exposure.

## Candidate Violation Policies

If a future sizing or stop-validity reference is violated, the project must choose one explicit violation policy.

No violation policy is chosen here.

Candidate policies include:

1. Fail closed with an explicit error.
2. Skip the trade and continue.
3. Clip the position size and continue.
4. Mark the run invalid but continue diagnostics only.

Skipping and clipping can materially change the realized strategy and must not be introduced without an accepted H018 decision record.

## Draft Non-Decision

This draft makes the following non-decision:

1. No sizing reference is selected.
2. No stop-validity reference is selected.
3. No equality behavior is selected beyond the currently implemented H017 raw-entry guard.
4. No minimum stop-distance threshold is selected.
5. No maximum notional threshold is selected.
6. No maximum leverage threshold is selected.
7. No trade-skip policy is selected.
8. No clipping policy is selected.
9. No diagnostic-continuation policy is selected.
10. No implementation is authorized.
11. No real-data run is authorized.
12. No H018 validation is authorized.
13. No live trading is approved.
14. No Phase 4 execution work is approved.

## Units And Instruments

This draft applies to the current candidate research scope:

1. USDJPY.
2. XAUUSD.
3. Broker-native H4 bars.
4. Broker-native M1 bridge-window execution.
5. Exness demo MT5 exports conditionally accepted only under strict complete-window rules.

Potential price-reference units are instrument price units:

1. USDJPY price distance is measured in JPY per USD.
2. XAUUSD price distance is measured in USD per troy ounce.

This draft does not select numeric thresholds in those units.

This draft does not define notional, leverage, margin, or friction-burden caps.

## Effect On Trade Eligibility

This draft does not change trade eligibility.

No trade is accepted, rejected, skipped, clipped, or failed closed by this draft alone.

Any future accepted decision that changes stop-validity reference can change trade eligibility and must be treated as an H018 semantics change unless separately proven otherwise.

## Effect On Realized Exposure

This draft does not change realized exposure.

No lot size, notional amount, leverage amount, margin amount, or risk fraction is changed by this draft alone.

Any future accepted decision that changes the sizing reference can change realized exposure and must be treated as an H018 semantics change unless separately proven otherwise.

## Effect On PnL Path

This draft does not change the PnL path.

Any future implementation that changes sizing, stop validity, skips, clips, guard behavior, fills, or costs can change the PnL path and must be classified as H018 implementation work or diagnostics, not H017 promotion.

## Rejected Alternatives

The following alternatives are rejected at the draft level:

1. Silently changing from raw-entry sizing to executable-entry sizing.

   Rejected because it would alter execution semantics without a recorded H018 policy.

2. Silently preserving raw-entry sizing as the H018 answer.

   Rejected because preserving the current behavior is still a decision and must be explicit before implementation claims.

3. Treating raw-entry versus executable-entry differences as cosmetic.

   Rejected because the fatal H017 event showed that reference choice can materially affect lot sizing and account survivability.

4. Treating a future rerun after changed sizing semantics as H017 promotion.

   Rejected because altered semantics would not be the original H017 evidence path.

5. Combining sizing-reference choice with minimum stop-distance or maximum leverage thresholds in one silent patch.

   Rejected because each policy affects the strategy differently and requires explicit governance.

## Deferred Alternatives

The following alternatives are deferred to future decision records:

1. Preserve raw-entry sizing.
2. Adopt executable-entry sizing.
3. Require both raw and executable references.
4. Adopt a conservative worst-case reference.
5. Define a separately named sizing reference.
6. Preserve raw-entry stop validity.
7. Adopt executable-entry stop validity.
8. Require both raw and executable stop validity.
9. Add diagnostic classification before choosing a policy.
10. Fail closed on future reference violations.
11. Skip trades on future reference violations.
12. Clip positions on future reference violations.
13. Continue diagnostics after marking a run invalid.

No deferred alternative is chosen here.

## Synthetic Test Requirements

No code implementation is authorized by this draft, so no synthetic tests are required before committing this documentation-only record.

If a later decision record is accepted for implementation, it must define focused synthetic tests before code changes.

At minimum, future sizing-reference implementation records must cover:

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
12. Equality invalidity for each selected reference.
13. The selected violation policy.
14. Regression protection for existing H017 raw-entry invalid-stop behavior if unchanged.
15. Test count preservation against the current full-test anchor unless an explicit test-removal phase exists.

## Real-Data Run Classification

No real-data run is authorized by this draft.

This draft does not authorize:

1. H017 promotion rerun.
2. H018 diagnostic rerun.
3. H018 validation rerun.
4. Phase 4 execution dry run.
5. Live trading.

Any future real-data run after sizing-reference or stop-validity-reference changes must be authorized by a separate accepted decision record or claim document.

A real-data run after changed sizing semantics must never be described as H017 promotion.

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

This draft does not impose implementation audit output because it does not implement a sizing or stop-validity rule.

Future decision records that affect sizing or stop validity must require audit output showing:

1. Which sizing reference was applied.
2. Which stop-validity reference was applied.
3. Raw H4 entry open.
4. Executable entry after spread.
5. Stop price.
6. Raw-entry stop distance.
7. Executable-entry stop distance.
8. Selected stop-distance denominator.
9. Whether equality occurred against any selected reference.
10. Whether the trade was accepted.
11. Whether the trade failed closed.
12. Whether the trade was skipped, if skipping is selected.
13. Whether the trade was clipped, if clipping is selected.
14. Whether the trade continued as diagnostic-only, if diagnostic continuation is selected.
15. Final accepted or rejected lot size if sizing is affected.

## Implementation Gate

No code implementation should begin from this draft.

Before implementing any H018 sizing-reference or stop-validity-reference behavior:

1. The relevant decision record must be accepted for implementation.
2. The selected sizing reference must be explicit.
3. The selected stop-validity reference must be explicit.
4. Equality behavior must be explicit.
5. The selected violation policy must be explicit.
6. Required synthetic tests must be listed.
7. Real-data run classification must be explicit.
8. Non-promotion language must be present.
9. H018 claim relationship must be clear.

## Current Verdict

This is a draft sizing-reference decision record only.

No H018 sizing reference is chosen here.

No H018 stop-validity reference is chosen here.

No H018 guard is implemented here.

No H018 threshold is chosen here.

No H018 real-data run is authorized here.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
