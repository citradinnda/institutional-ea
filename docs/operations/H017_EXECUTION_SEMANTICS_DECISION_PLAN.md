# H017 Execution Semantics Decision Plan

## Purpose

This document defines the decision work required after the H017 strict expanded broker-native event validation failure.

It is a plan only.

It does not repair H017.

It does not change strategy parameters.

It does not change cost assumptions.

It does not change event-engine sizing semantics.

It does not approve live trading.

## Background

H017 failed strict expanded broker-native event-driven validation by account insolvency.

The strict bridge-window preflight passed, and the fatal interval occurred on a complete strict bridge window.

Fatal interval:

- Decision time: 2021-07-06 01:00:00+00:00.
- Entry time: 2021-07-06 05:00:00+00:00.
- Forced exit time: 2021-07-06 09:00:00+00:00.
- Interval start equity: 9847.56 USD.
- Interval PnL: -11835.26 USD.
- Ending equity: -1987.71 USD.
- Interval return: -120.18 percent.

Fatal USDJPY fill:

- Side: buy.
- Entry price: 110.775000000.
- Exit price: 110.765228764.
- Lots: 518.77.
- Commission: 7262.78.
- Exit reason: stop.

Prior diagnostics localized the immediate sizing pathology to a near-zero raw stop distance:

- Raw H4 entry open: 110.770000000.
- H017 long stop: 110.770240804.

For the fatal long trade, the stop was slightly above the raw H4 entry open but below the cost-adjusted executable buy entry.

The current event engine sizes from:

    abs(raw H4 entry open - stop_price)

before entry spread is applied.

This produced a collapsed sizing denominator, a pathological lot size, and account insolvency.

## Current Status

H017 status:

- Failed.
- Not promotable.
- Not live-approved.

Live trading status:

- False.

Phase 4 execution status:

- Not approved.

Broker-native source status:

- Exness demo MT5 broker-native USDJPY and XAUUSD H4/M1 exports are conditionally accepted only under strict complete-window rules.

HistData status:

- Rejected for H017 validation under current evidence.

## Non-Goals

This phase must not:

1. Tune H017 parameters.
2. Change H017 signal logic.
3. Change H017 ATR, chandelier, volatility targeting, or heat-governor parameters.
4. Change cost assumptions casually.
5. Add machine learning.
6. Broaden to more symbols.
7. Use HistData.
8. Rerun broad validation as if H017 is still alive.
9. Treat source acceptance as strategy promotion.
10. Treat any future passing test as live-trading approval.

## Core Decision Questions

The next technical response must answer these questions explicitly before implementation.

### 1. Entry reference for sizing

Should event-engine sizing use:

- raw H4 entry open,
- executable entry price after spread,
- or a separate declared reference price?

Current behavior:

- raw H4 entry open.

Open issue:

- raw-entry sizing can produce pathological size when the stop is very close to the raw open, especially if the executable entry after spread is materially different.

### 2. Directional stop validity

For a long trade, should the stop be required to be below:

- the raw H4 entry open,
- the executable buy entry,
- or both?

For a short trade, should the stop be required to be above:

- the raw H4 entry open,
- the executable sell entry,
- or both?

Current behavior:

- no explicit documented directional-validity gate at the execution-semantics level.

Open issue:

- a long stop above the raw entry but below the executable entry creates ambiguous risk semantics.

### 3. Minimum stop distance

Should there be a minimum stop distance before sizing is allowed?

Possible reference units:

- absolute price distance,
- spread multiple,
- ATR fraction,
- tick size or broker point size,
- estimated all-in entry friction.

Open issue:

- without a minimum distance, a near-zero denominator can create extreme notional exposure.

### 4. Maximum leverage or notional guard

Should the event engine have an explicit maximum leverage or notional guard?

Possible interpretations:

- execution-realism constraint,
- account-risk constraint,
- strategy rule,
- broker-margin approximation,
- fail-closed validation guard.

Open issue:

- if the guard skips or clips trades, that may materially change the strategy and should likely require a new hypothesis boundary.

### 5. Skip versus fail-closed behavior

If a trade has invalid execution semantics, should the backtest:

- skip the trade,
- clip the size,
- reject the interval,
- fail closed,
- or record a validation error?

Open issue:

- skipping invalid trades can become hidden strategy optimization unless governed carefully.

### 6. H017 versus H018 boundary

If any new guard changes trade eligibility, sizing, or realized exposure, should the result be treated as:

- an H017 execution-engine correction,
- an H017 validation semantics clarification,
- or a new H018 hypothesis?

Default governance position:

- H017 remains failed.
- Any material change that prevents the fatal trade from occurring should be presumed to require a new hypothesis boundary unless explicitly justified otherwise.

## Candidate Future Work Packages

### Work Package A — Synthetic tests for invalid directional stops

Purpose:

- Confirm that long stops above the selected entry reference and short stops below the selected entry reference are handled explicitly.

Expected output:

- focused unit tests,
- documented behavior,
- no real-data validation yet.

### Work Package B — Synthetic tests for executable-entry sizing

Purpose:

- Compare raw-entry sizing and executable-entry sizing on controlled fixtures.

Expected output:

- tests that prove the lot-size difference,
- explicit documentation of the chosen sizing reference,
- no tuning.

### Work Package C — Minimum stop-distance research plan

Purpose:

- Define whether a minimum stop distance is an execution-realism rule or a strategy-risk rule.

Expected output:

- decision record,
- test plan,
- no parameter fitting.

### Work Package D — Maximum leverage/notional guard research plan

Purpose:

- Decide whether account-level exposure guards belong in the event engine, the strategy, or a future production risk layer.

Expected output:

- decision record,
- synthetic tests if implemented,
- explicit H017/H018 boundary decision.

### Work Package E — Open H018 hypothesis

Purpose:

- Preserve H017 as failed and start a successor hypothesis with explicit execution semantics.

Expected output:

- hypothesis ledger update,
- H018 claim definition,
- explicit validation gates,
- no live trading.

## Recommended Next Step

The safest next step is documentation plus synthetic tests, not real-data reruns.

Recommended sequence:

1. Decide the execution-semantics policy in writing.
2. Add focused synthetic tests for the chosen policy.
3. Update documentation and the hypothesis ledger.
4. Only then consider a new H018 validation path.

Do not use the strict expanded broker-native real-data run as a tuning loop.

Do not attempt to make H017 pass by changing only enough behavior to avoid the known fatal interval.

## Required Evidence Before Any Future Real-Data Validation

Before any future real-data validation under altered semantics, the repository should contain:

1. A decision record explaining the chosen sizing reference.
2. Synthetic tests for long and short directional stop validity.
3. Synthetic tests for near-zero stop-distance behavior.
4. Synthetic tests for spread-adjusted entry behavior.
5. Documentation stating whether the altered behavior is H017-compatible or requires H018.
6. Full test suite passing without a count regression.

Current full-test anchor:

    533 passed

## Current Verdict

This plan records that the project is in execution-semantics decision mode.

H017 remains failed.

No live trading is approved.

No implementation change is authorized by this document alone.
