# H018 Decision Record Index

This document indexes future H018 decision records.

Status: governance-only index.
H018 implementation status: not implemented.
H018 validation status: not validated.
H018 promotion status: not promotable.
Live trading status: not approved.
Phase 4 execution status: not approved.

This index does not choose any H018 policy. It does not implement a guard, threshold, sizing reference, skip rule, clipping rule, validation rule, promotion rule, or live-trading rule.

The reusable decision-record template is documented in docs/operations/H018_DECISION_RECORD_TEMPLATE.md.

## Required pending decision records

| Decision area | Current status | Required before implementation? | Notes |
|---|---|---:|---|
| H018 hypothesis boundary | Pending | Yes | Must preserve the original H017 failure and define whether H018 is a new hypothesis or a semantics-only successor. |
| Sizing reference | Pending | Yes | Must decide whether sizing uses raw H4 entry, executable entry after spread, both, or another explicitly named reference. |
| Directional stop validity reference | Pending | Yes | Must decide whether long and short stop geometry is checked against raw entry, executable entry, both, or another explicit reference. |
| Minimum stop-distance rule | Pending | Yes | Must decide whether positive near-zero stop distances fail closed and what reference defines the minimum allowed distance. |
| Maximum notional/leverage rule | Pending | Yes | Must decide whether exposure caps are enforced and how exposure is measured. |
| Trade violation policy | Pending | Yes | Must decide whether violations fail closed, skip trades, clip lots, or remain diagnostic-only. |
| Real-data rerun classification | Pending | Yes | Must decide whether reruns after execution-semantics changes are diagnostic-only or eligible H018 validation. |
| H018 claim gate | Pending | Yes | Must decide the minimum evidence required before any future H018 claim can be considered. |

## Current non-decisions

No minimum stop-distance threshold has been chosen.

No maximum notional threshold has been chosen.

No maximum leverage threshold has been chosen.

No sizing reference has been chosen.

No trade-skip policy has been chosen.

No clipping policy has been chosen.

No real-data validation rerun has been authorized.

No H018 claim has been accepted.

## Audit rule

Before any H018 code change, the relevant pending decision must have a completed decision record based on docs/operations/H018_DECISION_RECORD_TEMPLATE.md.

Before any H018 validation claim, the claim must also satisfy docs/operations/H018_CLAIM_SKELETON.md.

H017 remains failed and not promotable. This index does not alter that verdict.

## Draft decision records

| Decision record | Status | Policy chosen? | Implementation authorized? | Validation authorized? | Notes |
|---|---|---:|---:|---:|---|
| docs/operations/H018_BOUNDARY_DECISION_RECORD.md | Draft | No | No | No | Draft boundary record only. Preserves H017 failure visibility and states that H018, if pursued, is a successor hypothesis rather than a silent H017 repair. |

| docs/operations/H018_SIZING_REFERENCE_DECISION_RECORD.md | Draft | No | No | No | Draft sizing-reference and stop-validity-reference record only. Does not choose raw entry, executable entry, both-reference, conservative, skip, clip, or rerun policy. |

| docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md | Draft | No | No | No | Draft minimum stop-distance record only. Does not choose spread, ATR, tick, point, friction, combined rule, threshold, fail-closed, skip, clip, diagnostic, or rerun policy. |

| docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md | Draft | No | No | No | Draft maximum notional / leverage record only. Does not choose lots, notional, notional/equity, leverage, margin, friction, threshold, fail-closed, skip, clip, diagnostic, or rerun policy. |

| docs/operations/H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md | Draft | No | No | No | Draft trade violation policy record only. Does not choose fail-closed, skip, clip, diagnostic-only continuation, mixed policy, implementation, validation, or rerun policy. |
