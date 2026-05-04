# H018 Claim Skeleton

Status: governance skeleton only.

This document defines the minimum structure required before any future H018 claim can be treated as ready for validation.

It does not implement H018.

It does not validate H018.

It does not promote H017.

It does not choose thresholds.

It does not choose a sizing reference.

It does not approve live trading.

It does not approve Phase 4 execution work.

## Purpose

H017 failed strict expanded broker-native event validation by account insolvency.

The original H017 failure remains part of the research record and must not be erased by later execution-semantics changes.

H018 may become a new hypothesis only if it has:

1. An explicit claim.
2. Explicit execution semantics.
3. Explicit account-risk guards.
4. Focused synthetic tests.
5. Strict broker-native event validation.
6. Clear non-promotion language preserving the failed H017 record.

This skeleton prevents H018 from becoming an informal patch set.

## Current Status

1. No H018 claim exists yet.
2. H018 is not implemented.
3. H018 is not validated.
4. H018 is not promotable.
5. H017 remains failed and not promotable.
6. Live trading is not approved.
7. Phase 4 execution work is not approved.

## Required Claim Header

A future H018 claim must include:

1. Claim identifier.
2. Claim title.
3. Claim status.
4. Parent hypothesis relationship.
5. Explicit statement that H017 remains failed.
6. Live-trading status, defaulting to not approved.
7. Phase 4 execution status, defaulting to not approved.
8. Data source scope.
9. Validation window scope.
10. Execution semantics version.
11. Account-risk semantics version.
12. Required focused synthetic tests.
13. Full-suite test anchor.
14. Validation classification.
15. Promotion criteria.

## Required Boundary Decisions Before H018 Validation

Before any H018 validation run, governance must resolve:

1. H018 hypothesis boundary.
2. Sizing reference.
3. Stop-validity reference.
4. Equality behavior.
5. Minimum stop-distance rule, if used.
6. Minimum stop-distance violation policy, if used.
7. Maximum notional or leverage rule, if used.
8. Maximum exposure violation policy, if used.
9. Original H017 insolvency preservation.
10. Strict bridge-window validation scope.
11. Real-data run classification.

Any real-data run must be classified as diagnostic-only or H018 validation.

It must never be described as H017 promotion.

## Required Synthetic Test Gate

No H018 real-data validation run should occur until focused synthetic tests cover the selected semantics.

At minimum, the selected test plan should cover:

1. Long stop below entry.
2. Long stop equal to entry.
3. Long stop above entry.
4. Short stop above entry.
5. Short stop equal to entry.
6. Short stop below entry.
7. Executable-entry spread adjustment if executable-entry semantics are selected.
8. Positive near-zero stop distance that is directionally valid.
9. Minimum-distance boundary behavior if a minimum-distance rule is selected.
10. Maximum-exposure boundary behavior if an exposure cap is selected.
11. USDJPY conversion behavior.
12. XAUUSD USD-denominated exposure behavior.
13. Multi-symbol overlap behavior if portfolio-level exposure control is selected.
14. Audit fields showing whether a trade was accepted, failed, skipped, clipped, or classified as diagnostic-only.

Current full-test anchor: 537 passed.

## Required Source Gate

Any future H018 validation run must use strict broker-native complete-window source rules.

The source preflight must prove:

1. USDJPY broker-native H4 exists at the bridge timestamp.
2. XAUUSD broker-native H4 exists at the same bridge timestamp.
3. Each symbol has a next H4 timestamp exactly four hours later.
4. Each symbol has exactly 240 M1 bars in the H4 bridge window.
5. No M1 imputation is used.
6. No forward-fill is used.
7. No backfill is used.
8. No synthetic bars are inserted.
9. Incomplete windows are excluded.
10. Source acceptance is not treated as strategy promotion.

Accepted common complete H4/M1 windows remain: 5476.

## Required Event-Validation Gate

A future H018 validation run must report:

1. Whether strict bridge-window preflight passed.
2. Whether the event-driven backtest completed.
3. Whether insolvency occurred.
4. Starting equity.
5. Ending equity.
6. Maximum drawdown.
7. Per-symbol fills.
8. Per-symbol PnL.
9. Commission.
10. Slippage.
11. Trade eligibility failures.
12. Guard-trigger counts.
13. Skipped-trade counts if skipping is selected.
14. Clipped-trade counts if clipping is selected.
15. Diagnostic-only classifications if diagnostic continuation is selected.
16. Whether H018 is promotable under its own claim.
17. Whether live trading is approved, defaulting to false.
18. Whether Phase 4 execution is approved, defaulting to false.

## Required Non-Promotion Language

Every H018 claim and validation result should explicitly state:

1. H017 remains failed.
2. H017 is not promotable.
3. H018 results do not repair H017.
4. H018 validation is new-hypothesis validation.
5. Passing source preflight does not imply strategy validity.
6. Passing synthetic tests does not imply strategy validity.
7. Passing event validation does not automatically approve live trading.
8. Live trading requires a separate governance phase.

## Current Verdict

This document is a skeleton only.

H018 remains unimplemented.

H018 remains unvalidated.

H018 remains not promotable.

H017 remains failed and not promotable.

Live trading remains not approved.

Phase 4 execution remains not approved.
