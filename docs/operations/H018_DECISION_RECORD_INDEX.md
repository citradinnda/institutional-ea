# H018 Decision Record Index

This document indexes future H018 decision records.

Status: governance-only index.
H018 implementation status: not implemented.
H018 validation status: not validated.
H018 promotion status: not promotable.
Live trading status: not approved.
Phase 4 execution status: not approved.

This index does not implement a guard, threshold, sizing reference, validation rule, promotion rule, or live-trading rule.

The reusable decision-record template is documented in docs/operations/H018_DECISION_RECORD_TEMPLATE.md.

## Required decision records

| Decision area | Current status | Required before implementation? | Notes |
|---|---|---:|---|
| H018 hypothesis boundary | Draft | Yes | Must preserve the original H017 failure and define whether H018 is a new hypothesis or a semantics-only successor. |
| Sizing reference | Draft | Yes | Must decide whether sizing uses raw H4 entry, executable entry after spread, both, or another explicitly named reference. |
| Directional stop validity reference | Draft | Yes | Must decide whether long and short stop geometry is checked against raw entry, executable entry, both, or another explicit reference. |
| Minimum stop-distance rule | Draft | Yes | Must decide whether positive near-zero stop distances fail closed and what reference defines the minimum allowed distance. |
| Maximum notional/leverage rule | Draft | Yes | Must decide whether exposure caps are enforced and how exposure is measured. |
| Trade violation policy | Accepted for implementation | Yes | H018 validation-mode guard violations fail closed. Skip and clipping are rejected for first validation-mode implementation. Diagnostic-only continuation is deferred to a separate explicitly labeled diagnostic mode. |
| Real-data rerun classification | Pending | Yes | Must decide whether reruns after execution-semantics changes are diagnostic-only or eligible H018 validation. |
| H018 claim gate | Pending | Yes | Must decide the minimum evidence required before any future H018 claim can be considered. |

## Current non-decisions

No minimum stop-distance threshold has been chosen.

No maximum notional threshold has been chosen.

No maximum leverage threshold has been chosen.

No sizing reference has been chosen.

No stop-validity reference has been chosen.

No real-data validation rerun has been authorized.

No H018 claim has been accepted.

## Current accepted policy decisions

H018 validation-mode guard violations fail closed.

Trade skipping is rejected for first H018 validation-mode guard implementation.

Position clipping is rejected for first H018 validation-mode guard implementation.

Warn-and-continue is rejected.

Log-only continuation is rejected for validation mode.

Diagnostic-only continuation is deferred to a separate explicitly labeled diagnostic mode.

This accepted violation policy does not choose any minimum stop-distance threshold, maximum notional threshold, maximum leverage threshold, sizing reference, stop-validity reference, validation claim, promotion rule, live-trading rule, or Phase 4 execution approval.

## Audit rule

Before any H018 code change, the relevant decision must have a completed decision record based on docs/operations/H018_DECISION_RECORD_TEMPLATE.md.

Before any H018 validation claim, the claim must also satisfy docs/operations/H018_CLAIM_SKELETON.md.

H017 remains failed and not promotable. This index does not alter that verdict.

## Decision records

| Decision record | Status | Policy chosen? | Implementation authorized? | Validation authorized? | Notes |
|---|---|---:|---:|---:|---|
| docs/operations/H018_BOUNDARY_DECISION_RECORD.md | Draft | No | No | No | Draft boundary record only. Preserves H017 failure visibility and states that H018, if pursued, is a successor hypothesis rather than a silent H017 repair. |
| docs/operations/H018_SIZING_REFERENCE_DECISION_RECORD.md | Draft | No | No | No | Draft sizing-reference and stop-validity-reference record only. Does not choose raw entry, executable entry, both-reference, conservative, skip, clip, or rerun policy. |
| docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md | Draft | No | No | No | Draft minimum stop-distance record only. Does not choose spread, ATR, tick, point, friction, combined rule, threshold, fail-closed, skip, clip, diagnostic, or rerun policy. |
| docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md | Draft | No | No | No | Draft maximum notional / leverage record only. Does not choose lots, notional, notional/equity, leverage, margin, friction, threshold, fail-closed, skip, clip, diagnostic, or rerun policy. |
| docs/operations/H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md | Accepted for implementation | Yes | Yes | No | H018 validation-mode guard violations fail closed. Skip and clipping are rejected for first validation-mode implementation. Diagnostic-only continuation is deferred to a separate explicitly labeled diagnostic mode. |
