# H018 Trade Violation Policy Decision Record

Decision title: H018 trade violation policy decision record.
Decision identifier: H018-TRADE-VIOLATION-POLICY.
Decision status: Accepted for implementation.
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
Implementation authorization status: accepted for future implementation after focused synthetic tests.
Validation status: not validated.
Live-trading status: not approved.

## Purpose

This decision record chooses the default H018 validation-mode policy for future trade-rule violations.

A trade-rule violation means a future H018 guard determines that a trade is outside the declared validation envelope.

Examples may include:

1. Invalid stop geometry.
2. Minimum stop-distance violation.
3. Maximum notional violation.
4. Maximum leverage violation.
5. Maximum margin-usage violation.
6. Maximum friction-burden violation.
7. Any future account-risk envelope violation.

This decision prevents trade skipping, position clipping, or unmarked continuation from becoming silent repairs to the failed H017 validation.

## Decision

For H018 validation-mode runs, future guard violations must fail closed.

Fail closed means:

1. The run must stop with an explicit error or explicit invalid-run result.
2. The violation must not be silently ignored.
3. The violating trade must not be skipped as if no signal occurred.
4. The violating position must not be clipped to a smaller size.
5. The run must not continue as a valid validation run.
6. The audit output or error message must identify the violated rule and the raw values that caused the violation.

This policy applies to future H018 validation-mode guard violations.

This policy does not choose the guard thresholds themselves.

This policy does not choose a minimum stop-distance threshold.

This policy does not choose a maximum notional threshold.

This policy does not choose a maximum leverage threshold.

This policy does not choose a sizing reference.

This policy does not choose a stop-validity reference.

This policy does not implement code by itself.

This policy does not authorize a real-data rerun.

## Scope

This decision affects future H018 validation-mode behavior for:

1. Trade eligibility violations.
2. Minimum stop-distance violations if a minimum-distance rule is later accepted.
3. Maximum exposure violations if an exposure rule is later accepted.
4. Margin-usage violations if a margin rule is later accepted.
5. Friction-burden violations if a friction rule is later accepted.
6. Audit output for failed validation-mode guard violations.

This decision does not affect:

1. The current H017 failure verdict.
2. The current H017 strict expanded broker-native insolvency result.
3. The current H017 raw-entry invalid-stop guard implementation.
4. Any H018 threshold selection.
5. Any H018 real-data validation authorization.
6. Any live-trading approval.

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

No executable-entry sizing rule has been adopted.

## Chosen Rule

The chosen rule is:

Future H018 validation-mode guard violations fail closed.

The unit of the chosen rule is policy behavior, not price, lots, notional, or leverage.

Affected instruments:

1. USDJPY.
2. XAUUSD.

USDJPY and XAUUSD are handled the same way under this policy.

If a future accepted guard applies to only one instrument, that instrument-specific guard must still use fail-closed behavior in validation mode unless a later decision record supersedes this policy.

This rule affects trade eligibility because a violating trade makes the validation run invalid.

This rule does not clip realized exposure.

This rule does not create a replacement trade.

This rule does not skip a trade and continue as valid.

This rule can change the validation result because the run may stop earlier than a skip-or-clip implementation would.

This rule creates H018 governance behavior rather than repairing H017.

## Rejected Alternatives

### Skip Trade

Rejected for first H018 validation-mode implementation.

Reason:

Skipping changes trade eligibility and trade history.

Skipping can hide the fact that the strategy produced an invalid trade.

Skipping can become hidden optimization.

Skipping may be useful later only if a separate H018 decision explicitly defines untradeable-signal semantics, audit output, and validation rules.

### Clip Position Size

Rejected for first H018 validation-mode implementation.

Reason:

Clipping changes realized exposure and the PnL path.

Clipping may improve results by construction.

Clipping can turn an invalid strategy output into a synthetic safer trade.

Clipping may be useful later only if a separate H018 decision explicitly defines account-risk override semantics, cap calculation, audit output, and validation rules.

### Warn And Continue

Rejected.

Reason:

Warning while continuing as valid validation allows invalid trades to contaminate validation results.

### Log-Only Continuation

Rejected for validation mode.

Reason:

A log-only violation is too easy to ignore in a validation result.

### Diagnostic-Only Continuation

Deferred, not accepted for validation mode.

Reason:

Diagnostic continuation can be useful for counting violations, but it must be a separately labeled diagnostic mode.

If implemented later, diagnostic-only continuation must mark the run invalid for validation and must never be reported as H018 validation success.

### Mixed Policy By Instrument Or Violation Type

Rejected for first implementation.

Reason:

Mixed policies add complexity before the basic H018 guard semantics are proven.

A later decision may supersede this if there is a strong reason for instrument-specific or violation-specific behavior.

## Required Synthetic Tests Before Implementation

Before implementing this policy in code, focused synthetic tests must cover at least:

1. A normal trade with no violation proceeds normally.
2. A long-side guard violation fails closed.
3. A short-side guard violation fails closed.
4. A USDJPY guard violation fails closed.
5. An XAUUSD guard violation fails closed.
6. A minimum-distance violation fails closed if a minimum-distance rule is later implemented.
7. A maximum-exposure violation fails closed if an exposure rule is later implemented.
8. Exact-boundary behavior is explicitly tested for each implemented guard.
9. Below-boundary behavior is explicitly tested for each implemented guard.
10. Above-boundary behavior is explicitly tested for each implemented guard.
11. The error type or invalid-run result is explicit.
12. The error message or audit output identifies the violated rule.
13. The error message or audit output includes raw input values.
14. No trade is silently skipped.
15. No position size is clipped.
16. No validation-mode run continues as valid after a guard violation.
17. Existing H017 raw-entry invalid-stop behavior remains unchanged unless explicitly superseded.
18. Full test count remains at or above the current 537-test anchor unless an explicit test-removal phase exists.

## Required Real-Data Run Classification

No real-data run is authorized by this decision.

A future real-data run after implementing H018 fail-closed guard semantics must be classified as one of:

1. Diagnostic-only run.
2. H018 validation run after a formal H018 claim exists.

A real-data run after H018 semantics changes must never be described as H017 promotion.

A passing real-data run after implementation would not automatically validate H018.

A passing real-data run after implementation would not approve live trading.

A passing real-data run after implementation would not approve Phase 4 execution.

## Required Audit Output If Later Implemented

If this policy is implemented, a failed validation-mode guard violation must preserve or emit enough information to identify:

1. Which violation policy was applied.
2. Which rule produced the violation.
3. Which threshold or boundary was used.
4. Which raw input values were used.
5. Which symbol was evaluated.
6. Which side was evaluated.
7. Which entry reference was used, if relevant.
8. Which stop reference was used, if relevant.
9. Which account equity value was used, if relevant.
10. Which lots value was produced before the guard, if relevant.
11. Which notional or leverage value was produced before the guard, if relevant.
12. Why the run is invalid for validation.
13. That no skip occurred.
14. That no clipping occurred.

## Implementation Gate

This decision is accepted for implementation, but implementation must still be staged safely.

Before code changes begin, the implementation phase must:

1. Inspect actual APIs before calling internal functions.
2. Define focused synthetic tests first.
3. Preserve existing H017 invalid-stop regression tests unless explicitly superseded.
4. Avoid real-data reruns.
5. Avoid H017 tuning.
6. Avoid adding skip or clipping behavior.
7. Preserve the 537-test full-suite anchor.

## Non-Promotion Statement

H017 remains failed.

H017 is not promotable.

This decision does not repair H017.

This decision does not validate H018.

This decision does not approve live trading.

This decision does not approve Phase 4 execution.

Passing future tests after implementation would not automatically approve live trading.

Any future H018 validation must be judged under an explicit H018 claim.

## Current Verdict

The H018 validation-mode trade violation policy is accepted as fail closed.

Skip trade is rejected for first H018 validation-mode implementation.

Position clipping is rejected for first H018 validation-mode implementation.

Warn-and-continue is rejected.

Log-only continuation is rejected for validation mode.

Diagnostic-only continuation is deferred to a separately labeled diagnostic mode.

No minimum stop-distance threshold is chosen.

No maximum notional threshold is chosen.

No maximum leverage threshold is chosen.

No sizing reference is chosen.

No stop-validity reference is chosen.

No code has been implemented by this decision record.

No validation rerun is authorized.

No H018 claim is accepted.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
