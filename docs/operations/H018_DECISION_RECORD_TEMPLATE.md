# H018 Decision Record Template

Status: template only.

This template defines the required structure for future H018 execution-semantics and account-risk decision records.

It does not make any decision.

It does not implement H018.

It does not validate H018.

It does not promote H017.

It does not choose thresholds.

It does not choose a sizing reference.

It does not approve live trading.

It does not approve Phase 4 execution work.

## Purpose

H018 decision records must prevent execution-semantics changes from becoming silent H017 repairs.

Any future decision that changes sizing, stop validity, minimum stop distance, maximum exposure, trade skipping, or clipping must be documented before implementation.

## Required Header

Each future H018 decision record should include:

1. Decision title.
2. Decision identifier.
3. Decision status.
4. Date.
5. Related hypothesis.
6. Related documents.
7. Owner or reviewer.
8. Implementation status.
9. Validation status.
10. Live-trading status.

## Required Status Values

Use one of these decision statuses:

1. Draft.
2. Proposed.
3. Accepted for implementation.
4. Rejected.
5. Superseded.
6. Deferred.

Accepted for implementation does not mean validated.

Accepted for implementation does not mean live-approved.

## Required Scope Section

The decision record must state whether it affects:

1. H018 hypothesis boundary.
2. Entry sizing reference.
3. Stop-validity reference.
4. Equality behavior.
5. Minimum stop-distance rule.
6. Minimum stop-distance violation policy.
7. Maximum notional or leverage rule.
8. Maximum exposure violation policy.
9. Trade skipping.
10. Trade clipping.
11. Audit output.
12. Real-data validation classification.

## Required Current Behavior Section

The decision record must summarize the current behavior before the change.

At minimum, it should state:

1. H017 remains failed and not promotable.
2. H018 remains unvalidated unless separately proven.
3. Current H017 event sizing uses raw H4 entry open before spread.
4. Current raw-entry invalid-stop behavior fails closed for invalid directional geometry.
5. Equality is invalid under current raw-entry stop validity.
6. Positive near-zero stop distance remains an open account-risk issue.
7. No minimum stop-distance threshold has been selected unless the decision explicitly selects one.
8. No maximum notional or leverage threshold has been selected unless the decision explicitly selects one.
9. No executable-entry sizing has been adopted unless the decision explicitly adopts it.

## Required Decision Section

The decision record must state the chosen rule in plain English.

It must specify:

1. The exact rule.
2. The units used.
3. The instruments affected.
4. Whether USDJPY and XAUUSD are handled differently.
5. Whether the rule affects trade eligibility.
6. Whether the rule affects realized exposure.
7. Whether the rule changes the PnL path.
8. Whether the rule creates H018 rather than repairing H017.

## Required Rejected Alternatives Section

The decision record must list rejected alternatives and why they were rejected.

Examples:

1. Preserve raw-entry sizing.
2. Use executable-entry sizing.
3. Require both raw and executable stop validity.
4. Fail closed on minimum-distance violations.
5. Skip trades on minimum-distance violations.
6. Clip trade size on exposure violations.
7. Continue as diagnostic-only on guard violations.

## Required Synthetic Test Section

The decision record must define focused synthetic tests before implementation.

At minimum, include relevant cases for:

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

## Required Real-Data Run Classification

The decision record must classify any future real-data run as one of:

1. No real-data run authorized.
2. Diagnostic-only run.
3. H018 validation run after a formal H018 claim exists.

A real-data run after H018 semantics changes must never be described as H017 promotion.

## Required Non-Promotion Language

Each H018 decision record must state:

1. H017 remains failed.
2. H017 is not promotable.
3. This decision does not repair H017.
4. This decision does not validate H018.
5. This decision does not approve live trading.
6. This decision does not approve Phase 4 execution.
7. Passing tests after implementation would not automatically approve live trading.
8. Any future H018 validation must be judged under an explicit H018 claim.

## Required Audit Section

If the decision affects trade eligibility or exposure, it must require audit output showing:

1. Which rule was applied.
2. Which trades were accepted.
3. Which trades failed closed.
4. Which trades were skipped, if skipping is selected.
5. Which trades were clipped, if clipping is selected.
6. Which trades continued as diagnostic-only, if diagnostic continuation is selected.
7. The raw input values used by the rule.
8. The derived threshold or cap.
9. The final accepted or rejected value.

## Required Implementation Gate

No code implementation should begin until the decision record states:

1. Decision status is accepted for implementation.
2. Required synthetic tests are listed.
3. Real-data run classification is explicit.
4. Non-promotion language is present.
5. H018 claim relationship is clear.

## Current Verdict

This is a template only.

No H018 rule is chosen here.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
