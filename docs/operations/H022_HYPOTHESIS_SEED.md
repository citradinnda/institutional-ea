# H022 Hypothesis Seed - Risk/Lifecycle Reset

## Status

Pre-registered research hypothesis only.

No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.

## Background

H020 survived strict guard validation but failed performance badly.

H021 diagnostics showed useful structural clues:

- Signal-flip exits were profitable in aggregate.
- Stop exits were deeply destructive.
- Stop-outs concentrated by tight stop distance, high estimated gross leverage, symbol, and decision hour.
- Simple exclusions improved losses but did not reveal a profitable retained core.
- In-sample positive buckets failed temporal stability.
- Fixed lifecycle variants from 1 to 4 H4 bars all failed.

Therefore H021 is not promotable.

## H022 Core Hypothesis

The current Donchian/Chandelier entry stack may contain weak directional value, but the existing risk and lifecycle contract destroys it.

H022 will test whether a structurally different risk/lifecycle contract can preserve directional value while reducing stop-driven ruin.

This is not bucket-mining and not a direct implementation of H021 positive buckets.

## Non-Negotiable Constraints

H022 must preserve:

- Exness broker-native USDJPY/XAUUSD data only.
- Broker-native H4/M1 strict bridge windows only.
- No HistData.
- No M1 imputation, forward-fill, backfill, or synthetic bars.
- H018 hard guards unchanged.
- Modeled costs unchanged unless separately justified before testing.
- No demo or live deployment.

## Candidate Structural Direction

H022 should focus on risk/lifecycle structure, not session buckets.

Allowed design ideas:

- Lower strategy-level portfolio gross exposure cap than H020.
- Lower per-trade gross exposure cap than H020.
- Explicit fixed-fractional risk budget per trade.
- Lifecycle rules that reduce destructive stop exposure without removing stops.
- Non-overlapping portfolio accounting where applicable.
- Explicit skip rules based on risk geometry, not in-sample PnL buckets.

Disallowed design ideas:

- Implementing H021 positive time/session buckets as rules.
- Removing stops.
- Weakening H018 hard guards.
- Raising leverage limits.
- Lowering modeled costs to rescue results.
- Adding symbols.
- Adding ML.
- Tuning casually until profitable.

## Minimum Pass Criteria

A tested H022 variant is not promotable unless all are true:

- Full-period profit factor >= 1.15.
- Full-period total return positive after modeled costs.
- Max drawdown better than -25%.
- No chronological third has profit factor below 0.95.
- At least two of three chronological thirds have profit factor >= 1.05.
- First half and second half are both positive or near-flat, with neither below -5%.
- No single symbol contributes more than 75% of total net profit.
- Stop rate does not rise into structurally dangerous territory without compensating PF improvement.
- Full test suite remains at least 661 passed unless test removal is explicitly planned.

## Initial Verdict

H022 is authorized for research design only.

No H022 code is approved by this document alone.
No execution adapter work is approved.
No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.
