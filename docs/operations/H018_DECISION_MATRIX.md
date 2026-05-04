# H018 Decision Matrix

Status: governance draft only.

This document consolidates the currently open H018 execution-semantics and account-risk decisions.

It does not choose thresholds.

It does not implement any guard.

It does not tune H017.

It does not promote H017.

It does not validate H018.

It does not approve live trading.

It does not approve Phase 4 execution work.

## Purpose

H017 failed strict expanded broker-native event validation by account insolvency. The immediate pathology was a near-zero raw-entry stop distance that produced extreme USDJPY size before the raw-entry invalid-stop guard existed.

The current H017 raw-entry invalid-stop guard now fails closed when directional stop geometry is invalid under raw H4 entry-open semantics. Equality is also invalid. This guard is a safety improvement, not H017 promotion.

H018 planning exists because several possible changes would alter trade eligibility, realized exposure, or execution semantics. Those changes must be governed explicitly before implementation.

## Current H017 Baseline

| Area | Current H017 behavior |
|---|---|
| Hypothesis status | Failed / not promotable |
| Live trading | Not approved |
| Phase 4 execution | Not approved |
| Data source for strict validation | Exness demo MT5 broker-native USDJPY and XAUUSD M1/H4 only, under strict complete-window rules |
| Entry decision timing | H017 decides at H4 timestamp `t` |
| Execution bridge | Opens at next H4 open `t+1`; M1 bars in `[t+1, t+2)` resolve stops; otherwise closes at `t+2` open |
| Entry sizing reference | Raw H4 entry open before spread |
| Directional stop validity | Long/buy stop must be below raw H4 entry open; short/sell stop must be above raw H4 entry open |
| Equality stop validity | Invalid |
| Invalid stop policy | Fail closed with `H017EventInvalidStopError` |
| Positive near-zero stop distance | Still an open execution-semantics/account-risk issue |
| Minimum stop-distance threshold | Accepted and implemented: raw_stop_distance must be at least one modeled spread; USDJPY 0.01, XAUUSD 0.30 |
| Maximum notional/leverage threshold | Accepted and implemented: per-trade USD gross leverage must be at or below 10.0x equity |
| Executable-entry sizing | Not adopted |
| Trade skipping/clipping | Not authorized as a silent patch |
| Portfolio-wide gross leverage threshold | Accepted for implementation: interval-level portfolio USD gross leverage must be at or below 10.0x equity, summed gross across candidate non-zero-lot trades without netting |

## Consolidated Decision Matrix

| Decision area | Current H017 behavior | H018 options under discussion | Main risk of option | Required synthetic tests before implementation | Changes trade eligibility? | Changes realized exposure? | Likely requires H018? | Real-data run classification |
|---|---|---|---|---|---|---|---|---|
| Hypothesis boundary | H017 failed and remains failed | Define H018 as a new hypothesis that may inherit H017 alpha logic but changes execution/account-risk semantics | Blurring failed H017 evidence with new semantics | Documentation test is not applicable; code tests required only after implementation | Possibly | Possibly | Yes | H018 validation or diagnostic-only, never H017 promotion |
| Entry sizing reference | Size from raw H4 entry open before spread | Preserve raw entry; use executable entry after spread; require both raw and executable checks; use conservative worst-case reference; use named separate sizing reference | Silent semantic drift can make old and new results incomparable | Long/short sizing cases where spread moves executable entry relative to stop; exact lot expectations; regression against raw-entry baseline where unchanged | Possibly | Yes | Yes | Diagnostic-only or H018 validation |
| Stop-validity reference | Validate stop against raw H4 entry open | Validate against raw entry; executable entry; both; or classify diagnostics separately | A stop can be valid under one reference and invalid under another | Long stop below/at/above raw entry; long stop below/at/above executable entry; mirrored short cases; equality cases | Yes | Possibly | Yes | Diagnostic-only or H018 validation |
| Minimum stop distance | Only requires positive stop distance after directional validity | Threshold based on spread, ATR, tick size, broker point, all-in friction, or maximum of several references | Too loose leaves near-zero exposure risk; too strict may delete trades and become strategy filtering | Zero, negative, positive-near-zero, threshold-minus-epsilon, threshold-exact, threshold-plus-epsilon cases for USDJPY and XAUUSD | Yes if fail/skip; possibly if clip | Yes if clip; no if pure fail | Yes | Diagnostic-only or H018 validation |
| Minimum-distance violation policy | No minimum-distance guard | Fail closed; skip trade; clip to minimum distance; continue as diagnostic-only | Skipping/clipping can act like unvalidated strategy tuning | Fail policy raises/records error; skip policy records no fill; clip policy produces deterministic adjusted size; diagnostic policy preserves audit fields | Yes for fail/skip; no for diagnostic-only | Yes for clip | Yes | Diagnostic-only or H018 validation |
| Maximum notional/leverage | No maximum notional or leverage guard | Limit lots; notional; notional/equity; per-trade leverage; portfolio leverage; margin usage; friction burden | A cap may hide insolvency mechanisms or create artificial survivorship | USDJPY conversion tests; XAUUSD notional tests; per-trade and portfolio cap boundary tests; exact cap equality tests | Yes if reject/skip | Yes if clip | Yes | Diagnostic-only or H018 validation |
| Maximum-exposure violation policy | No exposure cap | Fail closed; skip trade; clip lots; continue as diagnostic-only | Clipping changes P&L path and can become a new strategy | Over-cap, at-cap, under-cap synthetic cases; commission impact after clipping; multi-symbol overlap tests | Yes for fail/skip | Yes for clip | Yes | Diagnostic-only or H018 validation |
| Original H017 insolvency visibility | Insolvency remains part of the research record | Preserve record in docs; classify altered reruns separately; add diagnostics without overwriting original verdict | New fail-closed behavior could obscure why H017 originally failed | Regression tests for invalid-stop fail-closed behavior; documentation references to original insolvency result | No | No | No if docs only; yes if behavior changes | Diagnostic-only if rerun |
| Strict bridge-window source rule | Complete common H4/M1 windows only, exactly 240 M1 bars per symbol | Preserve as mandatory for H018 validation | Relaxing source rules would contaminate validation | Preflight tests for missing M1, extra M1, non-four-hour H4 deltas, symbol asymmetry | Yes, at data-window level | Possibly | Required for any H018 validation | H018 validation only if all strict rules pass |
| H018 claim standard | No H018 claim exists yet | Require strict source preflight, event validation, exposure guards, explicit execution semantics, and no live approval by default | Weak claim lets strategy advance on incomplete evidence | Claim object or decision-record tests after claim implementation | No by itself | No by itself | Yes | H018 validation only |

## Required Decision Records Before Code Changes

Before implementing any H018 execution/account-risk behavior, at least one explicit decision record should choose the intended policy for:

The reusable decision-record structure is documented in docs/operations/H018_DECISION_RECORD_TEMPLATE.md. The pending decision inventory is documented in docs/operations/H018_DECISION_RECORD_INDEX.md. The template and index are governance-only and do not choose a policy by themselves.

1. H018 hypothesis boundary.
2. Sizing reference.
3. Stop-validity reference.
4. Minimum stop-distance rule.
5. Minimum stop-distance violation policy.
6. Maximum notional/leverage rule.
7. Maximum exposure violation policy.
8. Original H017 insolvency preservation.
9. Strict bridge-window validation scope.
10. H018 claim standard.

## Minimum Synthetic Test Families

Any implementation should be preceded by focused synthetic tests covering:

1. Long and short stop geometry under raw-entry semantics.
2. Long and short stop geometry under executable-entry semantics if adopted.
3. Equality invalidity for all selected references.
4. Positive near-zero stop distances that are directionally valid.
5. Minimum-distance boundary behavior:
   - below threshold,
   - exactly at threshold,
   - above threshold.
6. Maximum-exposure boundary behavior:
   - below cap,
   - exactly at cap,
   - above cap.
7. USDJPY quote-to-USD conversion when exposure or P&L uses notional.
8. XAUUSD USD-denominated exposure behavior.
9. Multi-symbol overlapping exposure if a portfolio-level cap is introduced.
10. Audit output proving whether a trade was failed, skipped, clipped, or only diagnosed.

## Non-Promotion Rule

Any future run after changing execution semantics, stop-distance rules, sizing reference, or exposure guards must not be called H017 promotion.

It must be classified as one of:

1. H018 diagnostic-only run.
2. H018 validation run after a formal H018 claim exists.
3. Separate execution-semantics diagnostic.

## Current Verdict

H018 remains unimplemented.

H018 remains unvalidated.

H018 is not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.

## H018 claim skeleton reference

The validation-gate structure for any future H018 claim is documented in docs/operations/H018_CLAIM_SKELETON.md. The claim skeleton must be resolved before any H018 validation run is treated as more than diagnostic-only.


