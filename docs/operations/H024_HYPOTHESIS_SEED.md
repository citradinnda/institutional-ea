# H024 Hypothesis Seed - Regime-Conditioned Pullback Continuation

## Status

Pre-registered research hypothesis.

H024 is not implemented.
H024 is not validated.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 is not approved.

## Motivation

H020, H021, H022, and H023 collectively showed that the current Donchian/Chandelier-derived entry stack does not have validated positive expectancy.

H023 specifically failed to find robust forward directional edge in the H020 bridge-compatible entry source across completed 1, 2, 3, and 4 H4 forward horizons.

Therefore H024 must not be a rescue attempt for the failed entry stack.

## Hypothesis

A regime-conditioned pullback-continuation entry may have better forward expectancy than breakout-style Donchian/Chandelier entries on USDJPY and XAUUSD H4 data.

The hypothesis is that continuation after a controlled pullback inside an established directional regime may avoid some of the destructive late-breakout and tight-stop behavior observed in prior hypotheses.

## Entry Concept

For each symbol independently:

1. Define directional regime using slow H4 trend state.
2. Wait for a pullback against that regime.
3. Enter only if price resumes in the regime direction after the pullback.
4. Do not use H021 time/session buckets.
5. Do not reuse Donchian breakout entry as the trigger.
6. Do not tune parameters against full-period performance without pre-registration.

Candidate regime features may include:

- slow moving-average slope
- price location relative to slow moving average
- recent H4 return persistence
- ATR-normalized distance from trend anchor

Candidate pullback features may include:

- ATR-normalized retracement
- short-term counter-regime candle sequence
- compression after retracement
- resumption close in regime direction

## Required Validation Discipline

H024 must be evaluated as research only.

Initial diagnostic should report:

- accepted bridge-window count
- executed/skipped counts
- total return
- max drawdown
- profit factor
- win rate
- gross profit/loss
- symbol split
- side split
- chronological halves
- chronological thirds
- comparison against H020/H023 failure baselines

Pass criteria are not relaxed:

- full-period profit factor >= 1.15
- positive full-period return after modeled costs
- no catastrophic drawdown
- temporal splits must not show obvious collapse
- no hidden reliance on one symbol, one side, or one short time segment

## Data Rules

Use only:

- Exness demo MT5 broker-native exports
- USDJPY and XAUUSD
- broker-native H4 and M1
- strict complete H4/M1 bridge windows
- Europe/Athens broker-time handling
- no imputation, forward-fill, backfill, or synthetic bars

Do not use:

- HistData
- broker H4 plus HistData M1 combinations
- sparse broker-native prefix as dense M1
- incomplete bridge windows
- raw broker files committed to git

## Guard Rules

H018 hard guards remain mandatory.

Do not weaken:

- invalid stop geometry failure
- minimum stop distance checks
- 10.0x max per-trade gross leverage
- 10.0x max portfolio gross leverage
- fail-closed violation behavior

## Explicit Non-Goals

H024 is not:

- a Donchian/Chandelier rescue
- H021 positive-bucket mining
- a time/session filter
- a parameter sweep
- an ML project
- deployment work
- demo trading preparation
- live trading preparation

## Next Engineering Step

Before any real-data diagnostic run, implement a small synthetic/unit-tested H024 signal prototype and reporting shell.

Real-data execution requires explicit user authorization.
