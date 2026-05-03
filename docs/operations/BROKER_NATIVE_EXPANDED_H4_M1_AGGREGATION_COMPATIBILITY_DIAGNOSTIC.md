# Broker-Native Expanded H4/M1 Aggregation Compatibility Diagnostic

Phase: 3.26-ae  
Status: read-only diagnostic  
Date: 2026-05-03

## Purpose

This document records a read-only H4/M1 aggregation compatibility diagnostic for the expanded broker-native MT5 exports.

The diagnostic compares broker-native H4 bars against broker-native M1 bars aggregated over the same H4 windows.

## Files Inspected

USDJPY:

- H4: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
- M1: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv

XAUUSD:

- H4: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
- M1: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

The files are under the root /data/ directory and are gitignored.

Raw data files were not committed.

## Method

For each symbol:

1. Load broker-native H4 and M1 files with load_mt5_csv(..., broker_tz="Europe/Athens").
2. Sort loaded bars by UTC timestamp.
3. Consider only H4 bars whose next H4 timestamp is exactly 4 hours later.
4. Define the M1 aggregation window as [H4 timestamp, H4 timestamp + 4 hours).
5. Require exactly 240 M1 bars inside the window.
6. Aggregate M1 as:
   - open = first M1 open,
   - high = max M1 high,
   - low = min M1 low,
   - close = last M1 close,
   - volume = sum M1 volume.
7. Compare aggregated M1 OHLCV to broker-native H4 OHLCV.
8. Count matches, mismatches, incomplete windows, and skipped windows.

## Boundaries

This phase did not:

1. Run H017.
2. Validate H017.
3. Accept the expanded broker-native source.
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

- docs/operations/BROKER_NATIVE_EXPANDED_H4_M1_AGGREGATION_COMPATIBILITY_DIAGNOSTIC_OUTPUT.txt

## Current Interpretation

This diagnostic is necessary source-acceptance evidence, but it is not sufficient by itself.

If the expanded broker-native H4 bars align with M1 aggregation on all fully covered windows, that supports continued broker-native source diagnostics.

However, source acceptance still requires:

1. Session-boundary analysis.
2. Cross-symbol common-window analysis.
3. Missingness analysis by symbol, year, month, hour, and shared timeline.
4. Explicit source-acceptance or source-rejection checkpoint.

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
