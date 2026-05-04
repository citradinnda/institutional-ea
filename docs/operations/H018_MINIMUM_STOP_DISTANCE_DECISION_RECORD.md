# H018 Minimum Stop-Distance Decision Record

Decision title: H018 minimum stop-distance rule.
Decision identifier: H018-MSDR-001.
Decision status: Accepted for implementation.
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
- docs/operations/H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md
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

This decision record accepts the first H018 minimum stop-distance policy.

The purpose is to prevent positive near-zero stop-distance denominators from creating unrealistic or account-destructive position sizes during validation-mode event backtesting.

This is not an H017 repair.

H017 remains failed and not promotable.

This decision creates an H018 execution-semantics requirement for future implementation.

This decision does not authorize a real-data rerun.

This decision does not validate H018.

This decision does not approve live trading.

This decision does not approve Phase 4 execution work.

## Accepted Minimum Stop-Distance Policy

For first H018 validation-mode implementation, a candidate trade must have a raw-entry stop distance greater than or equal to one modeled spread for that symbol.

The selected rule is:

1. Compute raw_stop_distance as the absolute difference between the raw H4 entry open and the selected stop price.
2. Compute minimum_stop_distance as the modeled spread price for the symbol.
3. If raw_stop_distance is less than minimum_stop_distance, fail closed.
4. If raw_stop_distance is equal to minimum_stop_distance, pass this guard.
5. If raw_stop_distance is greater than minimum_stop_distance, pass this guard.

Formula:

    raw_stop_distance = abs(raw_h4_entry_open - stop_price)
    minimum_stop_distance = modeled_spread_price_for_symbol

    raw_stop_distance < minimum_stop_distance  -> fail closed
    raw_stop_distance >= minimum_stop_distance -> pass this guard

## Selected Thresholds

The selected minimum stop-distance threshold is one modeled spread.

Current modeled spreads:

| Symbol | Modeled spread price | Minimum raw-entry stop distance |
|---|---:|---:|
| USDJPY | 0.01 | 0.01 JPY price distance |
| XAUUSD | 0.30 | 0.30 USD price distance |

These values come from the current cost-model assumptions already used by the event engine.

This decision does not choose floating historical spreads.

This decision does not choose ATR-based minimum distance.

This decision does not choose tick-size-only minimum distance.

This decision does not choose all-in friction conversion.

This decision does not choose a combined maximum rule.

Those alternatives remain deferred unless later accepted by a separate decision record.

## Reference Basis

The accepted minimum-distance reference is the raw H4 entry open.

For this first H018 minimum-distance policy:

1. The entry reference is raw_h4_entry_open.
2. The stop reference is the strategy-emitted stop price for the same decision.
3. The stop distance is measured before spread-adjusted executable entry is applied.
4. The rule is applied after directional stop geometry is checked.
5. The rule is applied before position sizing.

This matches the current event-engine sizing denominator basis and directly guards the denominator used by size_position_from_risk.

This decision does not choose executable-entry sizing.

This decision does not choose executable-entry stop-validity reference.

Executable-entry sizing and stop-validity reference remain separate unresolved H018 decisions.

## Violation Policy

The accepted violation policy is fail closed in validation mode.

If the minimum stop-distance rule is violated:

1. The validation run must stop.
2. The violation must not be silently ignored.
3. The trade must not be skipped as if no signal occurred.
4. The position must not be clipped or resized.
5. The run must not continue as a valid validation run.
6. The error or invalid-run output must identify the violated rule and raw values that caused the violation.

This follows the accepted H018 trade violation policy in:

- docs/operations/H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md

## Boundary Behavior

Boundary behavior is explicit:

1. raw_stop_distance less than minimum_stop_distance fails closed.
2. raw_stop_distance equal to minimum_stop_distance passes this guard.
3. raw_stop_distance greater than minimum_stop_distance passes this guard.

Equality passes the minimum-distance guard because the accepted rule is a floor of at least one modeled spread.

This does not override directional stop validity.

Directional stop validity remains separate:

1. A long or buy stop must be below the selected entry validity reference.
2. A short or sell stop must be above the selected entry validity reference.
3. Equality at the directional stop-validity reference remains invalid under the current H017 raw-entry guard unless a later H018 stop-validity decision changes that rule.

## Instruments And Units

This accepted policy applies to the current H018 candidate scope only:

1. USDJPY.
2. XAUUSD.
3. Broker-native H4 bars.
4. Broker-native M1 bridge-window execution.
5. Exness demo MT5 exports conditionally accepted only under strict complete-window rules.

Units:

1. USDJPY stop distance is measured in JPY price units.
2. XAUUSD stop distance is measured in USD price units.
3. The threshold is symbol-specific because modeled spread price is symbol-specific.

## Rationale

The original strict expanded broker-native H017 validation failed by insolvency.

The historically important failure included a pathological USDJPY size caused by a near-zero raw-entry stop-distance denominator.

The fatal diagnostic raw distance was approximately:

    0.000240804

The current modeled USDJPY spread is:

    0.01

A stop-distance denominator smaller than the modeled spread is not credible for validation-mode position sizing because the intended risk denominator is smaller than the modeled transaction-cost uncertainty.

This rule directly blocks that known near-zero denominator class without tuning Donchian parameters, ATR parameters, heat-governor parameters, symbol universe, or machine-learning logic.

The rule is intentionally simple and auditable.

It is not claimed to be sufficient by itself.

A separate maximum notional or leverage guard is still required before any real-data validation attempt.

## Effect On Trade Eligibility

This decision changes future H018 trade eligibility.

A trade that is directionally valid but has raw_stop_distance less than one modeled spread will be invalid in H018 validation mode.

This must be treated as H018 implementation work.

It must not be described as H017 promotion.

## Effect On Realized Exposure

This decision does not clip or resize exposure.

It only defines a future fail-closed invalid-trade condition.

If implemented, trades that violate the rule stop the validation run rather than being resized, skipped, or allowed.

This decision does not define maximum notional exposure.

This decision does not define maximum leverage.

This decision does not define margin requirements.

## Effect On PnL Path

This decision can affect the future H018 validation path because a rule violation stops the run.

It does not create a new PnL path by skipping or clipping trades.

A validation-mode fail-closed result is an invalid-run or failed-validation state, not an alternate equity curve.

## Required Audit Fields

A future implementation must expose enough information to audit a minimum-distance violation.

At minimum, the error or invalid-run output must include:

1. Rule name.
2. Symbol.
3. Side.
4. Decision time.
5. Entry time.
6. Raw H4 entry open.
7. Stop price.
8. Raw stop distance.
9. Minimum stop-distance threshold.
10. Threshold basis, which is one modeled spread.
11. Modeled spread price.
12. Boundary comparison result.
13. Validation-mode action, which is fail closed.

## Synthetic Test Requirements

Before implementation is accepted, focused synthetic tests must cover at least:

1. Directionally valid long stop with raw distance below one spread fails closed.
2. Directionally valid short stop with raw distance below one spread fails closed.
3. Directionally valid long stop with raw distance exactly equal to one spread passes the minimum-distance guard.
4. Directionally valid short stop with raw distance exactly equal to one spread passes the minimum-distance guard.
5. Directionally valid long stop with raw distance above one spread passes the minimum-distance guard.
6. Directionally valid short stop with raw distance above one spread passes the minimum-distance guard.
7. USDJPY uses 0.01 as the minimum raw-entry stop distance.
8. XAUUSD uses 0.30 as the minimum raw-entry stop distance.
9. Minimum-distance violation error includes raw H4 entry open, stop price, raw stop distance, threshold, symbol, side, decision time, and entry time.
10. Existing invalid directional stop tests remain valid.
11. Existing equality invalid-stop tests remain valid for directional stop geometry.
12. No skip behavior is introduced for minimum-distance violations.
13. No clipping behavior is introduced for minimum-distance violations.
14. Full pytest count must not drop below the current anchor unless an explicit test-removal phase exists.

## Rejected Alternatives

The following alternatives are rejected for first H018 validation-mode implementation:

1. Silently accepting all positive near-zero stop distances.

   Rejected because positive near-zero stop distance remains an account-risk issue.

2. Skipping trades that violate the minimum-distance rule.

   Rejected because skipping changes trade eligibility and can create a different strategy path.

3. Clipping or resizing trades that violate the minimum-distance rule.

   Rejected because clipping changes realized exposure and can hide invalid sizing.

4. Warn-and-continue.

   Rejected because validation mode must not continue as valid after a guard violation.

5. Log-only continuation.

   Rejected because validation mode must fail closed.

6. ATR-based threshold as the first implementation.

   Deferred because ATR thresholding can become strategy filtering and requires additional governance.

7. Combined maximum rule as the first implementation.

   Deferred because it is more complex and should not be introduced before the simpler spread-floor guard and maximum exposure guard are separately governed.

8. Treating this rule as H017 repair.

   Rejected because H017 already failed strict expanded broker-native event validation by insolvency.

## Deferred Decisions

The following decisions remain unresolved:

1. Maximum notional threshold.
2. Maximum leverage threshold.
3. Exposure measurement basis.
4. Sizing reference.
5. Stop-validity reference.
6. Executable-entry sizing.
7. Real-data rerun classification.
8. H018 claim gate.
9. Diagnostic-only continuation mode.
10. Live deployment criteria.

## Real-Data Run Classification

No real-data run is authorized by this decision.

This decision does not authorize:

1. H017 promotion rerun.
2. H018 diagnostic rerun.
3. H018 validation rerun.
4. Phase 4 execution dry run.
5. Live trading.

Any future real-data run after implementation of this rule must be separately authorized and classified.

A real-data run after this rule is implemented must never be described as H017 promotion.

## Non-Promotion Language

H017 remains failed.

H017 is not promotable.

This decision does not repair H017.

This decision does not validate H018.

This decision does not approve live trading.

This decision does not approve Phase 4 execution.

Passing tests after future implementation will not approve live trading.

Any future H018 validation must be judged under an explicit H018 claim.

## Implementation Gate

This decision is accepted for future implementation, but implementation must not begin until the next implementation phase explicitly defines the exact code changes and tests.

Before code changes:

1. Inspect the relevant APIs again if needed.
2. Define the new error type or invalid-run representation.
3. Define exact synthetic tests.
4. Confirm modeled spread constants are imported from the existing cost model or otherwise referenced without duplication.
5. Preserve existing H017 invalid-stop tests.
6. Run focused tests.
7. Run full pytest.
8. Preserve the current full-test anchor unless a deliberate test-removal phase exists.
9. Commit and push.

## Current Verdict

The H018 minimum stop-distance policy is accepted for future implementation.

The accepted rule is:

    raw_stop_distance must be greater than or equal to one modeled spread for the symbol.

The accepted violation policy is validation-mode fail closed.

No code is implemented by this decision record.

No H018 validation is authorized by this decision record.

No real-data run is authorized by this decision record.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
