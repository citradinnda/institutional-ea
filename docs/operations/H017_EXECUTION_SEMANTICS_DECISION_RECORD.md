# H017 Execution Semantics Decision Record

## Status

Implemented partial decision record.

This document records the execution-semantics policy after inspecting the current H017 event backtest API.

The raw-entry directional stop-validity guard has been implemented and tested.

Executable-entry sizing, minimum stop distance, and maximum notional/leverage guards remain undecided.

It does not repair H017.

It does not approve live trading.

## Source Inspection Summary

Relevant event bridge:

    quantcore/backtest/h017_event.py

Relevant sizing function:

    quantcore/backtest/portfolio.py::size_position_from_risk

Current H017 event bridge behavior:

1. Read the H4 raw open at the entry timestamp.
2. Read the H017 stop from the long or short stop panel.
3. Compute:

       stop_distance_price = abs(entry_raw_price - stop_price)

4. Size the position from:

       entry_price=entry_raw_price
       stop_distance_price=stop_distance_price

5. Apply entry execution costs after sizing.
6. Simulate the M1 bracket trade using the cost-adjusted entry price.
7. Apply exit execution costs after the raw M1 exit is resolved.

Current behavior does not explicitly reject directionally invalid stops at the event-semantics layer.

For a long trade, a stop above raw entry can still be sized if the absolute distance is positive.

For a short trade, a stop below raw entry can still be sized if the absolute distance is positive.

## Problem Statement

The strict expanded broker-native H017 validation failed by insolvency.

The fatal USDJPY trade was a long trade with:

- Raw H4 entry open: 110.770000000.
- H017 long stop: 110.770240804.
- Executable entry after spread: 110.775000000.
- Lots: 518.77.

The stop was slightly above the raw H4 entry open but below the executable buy entry.

Because the event engine sized from absolute raw-entry distance before spread, the stop-distance denominator collapsed.

This produced a pathological lot size and account insolvency.

## Decision Principles

### Principle 1 — H017 remains failed

H017 failed strict expanded broker-native event-driven validation.

This decision record must not reinterpret that failure as a pass.

### Principle 2 — No silent fixes

Changing raw-entry versus executable-entry sizing semantics is not a small patch.

It changes the execution model and may change realized exposure, trade eligibility, and validation outcomes.

### Principle 3 — Directional stop semantics must be explicit

A stop-loss is directional.

For a long trade, the stop should represent adverse price movement below the selected entry reference.

For a short trade, the stop should represent adverse price movement above the selected entry reference.

Using absolute distance alone can hide invalid or ambiguous stop geometry.

### Principle 4 — Synthetic tests before real-data reruns

The next implementation work should use small synthetic fixtures.

Real-data reruns must not become a tuning loop around the known fatal interval.

### Principle 5 — H018 boundary is likely required

If a new rule skips invalid stops, clips position size, changes the sizing reference, or adds a maximum notional/leverage guard, it should be presumed to require a successor hypothesis boundary such as H018.

H017 should remain failed unless a separate governance decision explicitly says otherwise.

## Implemented Partial Policy

This section records the implemented raw-entry directional stop-validity policy and the remaining open decisions.

### 1. Entry reference policy

The execution model should distinguish at least two prices:

- raw entry reference,
- executable entry price after spread.

The decision record does not yet choose a final sizing reference.

However, any future implementation must name the chosen reference explicitly in code and documentation.

### 2. Directional stop-validity policy

Implemented for current raw-entry sizing semantics.

The event bridge no longer uses absolute stop distance before validating stop direction against the raw H4 entry open.

Implemented strict policy:

- Long trade:
  - stop must be below the raw H4 entry open.
- Short trade:
  - stop must be above the raw H4 entry open.

If the stop geometry is invalid, the event bridge raises:

    H017EventInvalidStopError

This is fail-closed behavior. It does not skip the trade silently and does not clip size.

Open decision:

- whether a future H018 should use executable-entry sizing, raw-entry sizing, or a separate declared sizing reference.

### 3. Invalid-stop behavior policy

Implemented for raw-entry directional invalid stops.

Invalid directional stop geometry is not silently converted into a trade.

Current behavior:

- fail closed with a clear validation error,
- do not skip the trade,
- do not clip the size,
- do not treat the resulting code change as H017 promotion.

Reason:

Skipping invalid trades can accidentally become hidden optimization. A future strategy that skips invalid stops should be opened under a new hypothesis boundary unless explicitly justified otherwise.

### 4. Minimum stop-distance policy

Near-zero stop distance should be explicitly governed.

Candidate minimum-distance references:

- full spread,
- half spread,
- ATR fraction,
- tick size,
- broker point size,
- all-in friction estimate.

This record does not choose a numeric threshold.

Any threshold would be a material strategy or execution-model decision and must be separately justified.

### 5. Maximum notional or leverage policy

A maximum notional or leverage guard may be realistic, but it is not a neutral change.

If it clips or rejects trades, it changes realized exposure.

Recommended default:

- document the need,
- test the behavior synthetically,
- treat any trade-clipping or trade-skipping version as H018 unless explicitly justified otherwise.

## Implemented Tests

Focused synthetic tests were added before any real-data rerun.

Implemented tests:

1. Long stop above raw entry fails closed.
2. Short stop below raw entry fails closed.
3. Long stop equal to raw entry fails closed.
4. Short stop equal to raw entry fails closed.
5. Existing valid long and short cases continue to pass under the full suite.

Test location:

    tests/test_h017_event.py

Implementation location:

    quantcore/backtest/h017_event.py

The generic portfolio sizing API was not modified:

    quantcore/backtest/portfolio.py

Current full-test anchor after equality invalid-stop tests:

    537 passed

Remaining future tests, if authorized:

1. Long stop above raw entry but below executable entry is explicitly governed under any future executable-entry policy.
2. Near-zero positive stop distance is explicitly governed.
3. Spread-adjusted sizing behavior is explicitly governed.
4. Maximum notional/leverage guard behavior is explicitly governed.

## H017/H018 Boundary

H017 remains:

- failed,
- not promotable,
- not live-approved.

A successor H018 should be opened if the project chooses any of these:

1. executable-entry sizing,
2. directional invalid-stop skipping instead of fail-closed validation,
3. minimum stop-distance trade filtering,
4. maximum notional/leverage clipping,
5. any other rule that materially changes trade eligibility or realized exposure.

The implemented raw-entry directional fail-closed guard is documented as an execution-validation guard. It does not revive H017 and does not authorize new real-data validation as a promotion attempt.

## Current Verdict

The project has implemented and tested the first synthetic execution-semantics guard: fail closed on raw-entry directional invalid stops.

H017 remains failed.

No real-data rerun is authorized by this document alone.

No live trading is approved.
