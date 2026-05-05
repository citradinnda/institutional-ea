# H018 Decision Record Index

This document indexes future H018 decision records.

Status: governance-only index.
H018 implementation status: partial validation-mode guard implementation completed.
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
| Sizing reference | Accepted and implemented | Yes | First H018 validation-mode implementation preserves raw H4 entry open as the sizing reference. Executable-entry sizing is not adopted. |
| Directional stop validity reference | Accepted and implemented | Yes | First H018 validation-mode implementation preserves raw H4 entry open as the stop-validity reference. Equality is invalid. |
| Minimum stop-distance rule | Accepted and implemented | Yes | Raw-entry stop distance must be greater than or equal to one modeled spread for the symbol. Validation-mode violations fail closed. |
| Maximum notional/leverage rule | Accepted and implemented | Yes | Maximum per-trade USD gross leverage is capped at 10.0x equity. Validation-mode violations fail closed. |
| Trade violation policy | Accepted for implementation | Yes | H018 validation-mode guard violations fail closed. Skip and clipping are rejected for first validation-mode implementation. Diagnostic-only continuation is deferred to a separate explicitly labeled diagnostic mode. |
| Real-data rerun classification | Pending | Yes | Must decide whether reruns after execution-semantics changes are diagnostic-only or eligible H018 validation. |
| H018 claim gate | Pending | Yes | Must decide the minimum evidence required before any future H018 claim can be considered. |
| Portfolio-wide gross leverage rule | Accepted and implemented | Yes | Maximum interval-level portfolio USD gross leverage is capped at 10.0x equity. Gross notionals are summed across candidate non-zero-lot trades without netting. Validation-mode violations fail closed. |

## Current non-decisions

No real-data validation rerun has been authorized.

No H018 claim has been accepted.

## Current accepted policy decisions

H018 validation-mode guard violations fail closed.

Trade skipping is rejected for first H018 validation-mode guard implementation.

Position clipping is rejected for first H018 validation-mode guard implementation.

Warn-and-continue is rejected.

Log-only continuation is rejected for validation mode.

Diagnostic-only continuation is deferred to a separate explicitly labeled diagnostic mode.

H018 minimum stop-distance rule is accepted for future implementation:

1. raw_stop_distance is abs(raw_h4_entry_open - stop_price).
2. minimum_stop_distance is one modeled spread for the symbol.
3. USDJPY minimum raw-entry stop distance is 0.01.
4. XAUUSD minimum raw-entry stop distance is 0.30.
5. raw_stop_distance less than minimum_stop_distance fails closed.
6. raw_stop_distance equal to minimum_stop_distance passes this guard.
7. raw_stop_distance greater than minimum_stop_distance passes this guard.
8. This rule is implemented.
9. This rule does not authorize real-data validation.

These accepted policies do not choose any validation claim, promotion rule, live-trading rule, Phase 4 execution approval, broker margin model or friction-burden cap.

## Audit rule

Before any H018 code change, the relevant decision must have a completed decision record based on docs/operations/H018_DECISION_RECORD_TEMPLATE.md.

Before any H018 validation claim, the claim must also satisfy docs/operations/H018_CLAIM_SKELETON.md.

H017 remains failed and not promotable. This index does not alter that verdict.

## Decision records

| Decision record | Status | Policy chosen? | Implementation authorized? | Validation authorized? | Notes |
|---|---|---:|---:|---:|---|
| docs/operations/H018_BOUNDARY_DECISION_RECORD.md | Draft | No | No | No | Draft boundary record only. Preserves H017 failure visibility and states that H018, if pursued, is a successor hypothesis rather than a silent H017 repair. |
| docs/operations/H018_SIZING_REFERENCE_DECISION_RECORD.md | Accepted and implemented | Yes | Yes | No | First H018 validation-mode implementation preserves raw H4 entry open as both sizing reference and directional stop-validity reference. Executable-entry sizing, both-reference validity, conservative worst-case sizing, skipping, clipping, and real-data validation are not authorized. |
| docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md | Accepted and implemented | Yes | Yes | No | Raw-entry stop distance must be greater than or equal to one modeled spread for the symbol. USDJPY threshold is 0.01. XAUUSD threshold is 0.30. Validation-mode violations fail closed. No real-data validation is authorized. |
| docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md | Accepted and implemented | Yes | Yes | No | Maximum per-trade USD gross leverage is capped at 10.0x equity. XAUUSD notional_quote is treated as USD. USDJPY notional_quote is converted to USD by dividing by entry_raw_price. Violations fail closed. No real-data validation is authorized. |
| docs/operations/H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md | Accepted for implementation | Yes | Yes | No | H018 validation-mode guard violations fail closed. Skip and clipping are rejected for first validation-mode implementation. Diagnostic-only continuation is deferred to a separate explicitly labeled diagnostic mode. |
| docs/operations/H018_PORTFOLIO_GROSS_LEVERAGE_DECISION_RECORD.md | Accepted and implemented | Yes | Yes | No | Maximum interval-level portfolio USD gross leverage is capped at 10.0x equity. USD-converted gross notionals are summed across candidate non-zero-lot trades without netting. Violations fail closed. No real-data validation is authorized. |

<!-- H018_MAX_NOTIONAL_LEVERAGE_ACCEPTED_START -->
## H018 Maximum Notional / Leverage Decision Record

Status: Accepted and implemented

Path:

docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md

Accepted policy:

1. Maximum per-trade USD gross leverage is capped at 10.0x equity.
2. Exposure basis is per-trade USD gross notional divided by account equity.
3. XAUUSD PositionSize.notional_quote is treated as USD notional.
4. USDJPY PositionSize.notional_quote is converted from JPY to USD by dividing by entry_raw_price.
5. gross_leverage < 10.0 passes.
6. gross_leverage == 10.0 passes.
7. gross_leverage > 10.0 fails closed.
8. Violations are not skipped.
9. Violations are not clipped.
10. Violations are not warn-and-continue.
11. Violations are not log-only continuation.
12. Diagnostic-only continuation remains deferred to a separately labeled diagnostic mode.
13. This decision does not authorize a real-data rerun.
14. This decision does not promote H017.
15. This decision does not validate H018.
16. This decision does not approve live trading.
17. This decision does not approve Phase 4 execution.
<!-- H018_MAX_NOTIONAL_LEVERAGE_ACCEPTED_END -->

