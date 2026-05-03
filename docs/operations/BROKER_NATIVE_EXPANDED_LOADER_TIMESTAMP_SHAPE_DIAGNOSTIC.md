# Broker-Native Expanded Loader Timestamp-Shape Diagnostic

Phase: 3.26-ac  
Status: read-only diagnostic  
Date: 2026-05-03

## Purpose

This document records a read-only loader smoke test and timestamp-shape diagnostic for the expanded broker-native MT5 exports.

The expanded files inventoried in the prior phase were:

- USDJPY M1
- USDJPY H4
- XAUUSD M1
- XAUUSD H4

This diagnostic checks whether the files load through the existing MT5 loader and whether their timestamp spacing matches the expected timeframe shape.

## Boundaries

This phase did not:

1. Run H017.
2. Validate H017.
3. Accept the expanded broker-native data source.
4. Accept any new long-history M1 validation source.
5. Modify raw data files.
6. Write derived datasets.
7. Use HistData.
8. Tune strategy logic.
9. Change the cost model.
10. Start Phase 4 execution.
11. Start live trading.

## Diagnostic Output

The raw diagnostic output is committed as a companion text file:

- docs/operations/BROKER_NATIVE_EXPANDED_LOADER_TIMESTAMP_SHAPE_DIAGNOSTIC_OUTPUT.txt

## Current Interpretation

This diagnostic is limited to loader behavior, timestamp uniqueness, and timestamp spacing shape.

If M1 files classify as expected 1-minute-spaced and H4 files classify as expected 4-hour-spaced, that is useful evidence for continuing broker-native source diagnostics.

However, this diagnostic alone is not sufficient for source acceptance.

Required future diagnostics still include:

1. Expanded broker H4/M1 aggregation compatibility.
2. Expanded broker M1 coverage analysis.
3. Session-boundary analysis.
4. Cross-symbol common-window analysis.
5. Explicit source-acceptance or source-rejection checkpoint.

## Explicit Non-Approval

This document does not approve:

1. H017 validation.
2. H017 validation on expanded broker-native files.
3. HistData validation.
4. Source acceptance.
5. Derived data generation.
6. Strategy tuning.
7. Cost model changes.
8. New instruments.
9. Machine learning.
10. Phase 4 execution.
11. Live trading.
