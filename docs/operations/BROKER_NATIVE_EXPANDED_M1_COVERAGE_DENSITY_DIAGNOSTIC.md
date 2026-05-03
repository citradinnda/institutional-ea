# Broker-Native Expanded M1 Coverage-Density Diagnostic

Phase: 3.26-ad  
Status: read-only diagnostic  
Date: 2026-05-03

## Purpose

This document records a read-only coverage-density diagnostic for the expanded broker-native M1 exports.

The previous loader timestamp-shape diagnostic showed that the expanded M1 files loaded successfully and were mostly one-minute-spaced overall.

However, the first loaded rows appeared sparse and daily-like at the beginning of the files.

This diagnostic therefore checks density by year and month to determine whether the apparent 2018 start represents true dense M1 history or a sparse prefix followed by denser M1 history later.

## Files Inspected

- C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

The files are under the root /data/ directory and are gitignored.

Raw data files were not committed.

## Boundaries

This phase did not:

1. Run H017.
2. Validate H017.
3. Accept the expanded broker-native M1 source.
4. Accept any long-history M1 validation source.
5. Modify raw data files.
6. Write derived datasets.
7. Use HistData.
8. Tune strategy logic.
9. Change the cost model.
10. Start Phase 4 execution.
11. Start live trading.

## Diagnostic Output

The raw diagnostic output is committed as a companion text file:

- docs/operations/BROKER_NATIVE_EXPANDED_M1_COVERAGE_DENSITY_DIAGNOSTIC_OUTPUT.txt

## Interpretation Rules

This diagnostic uses calendar-minute density as a rough screening measure.

Calendar-minute density means:

- observed loaded bars divided by all calendar minutes in the period.

This is not the same as trading-session coverage.

A healthy FX/CFD M1 source is not expected to show 100 percent calendar-minute coverage because weekends, market closures, and symbol-specific breaks exist.

However, extremely low calendar-minute density in early years would indicate that the apparent 2018 start is not truly dense M1 history.

This diagnostic is only a screening diagnostic. It is not source acceptance.

## Required Future Diagnostics

Even if dense M1 candidate regions are found, required future diagnostics still include:

1. Broker H4/M1 aggregation compatibility over the expanded overlap.
2. Session-boundary analysis.
3. Cross-symbol common-window analysis.
4. Missingness analysis by symbol, year, month, hour, and shared timeline.
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
