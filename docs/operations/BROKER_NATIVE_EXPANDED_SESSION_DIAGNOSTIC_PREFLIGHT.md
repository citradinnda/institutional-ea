# Broker-Native Expanded Session Diagnostic Preflight

Phase: 3.26-ag  
Status: Completed preflight  
Scope: Expanded broker-native USDJPY and XAUUSD M1/H4 loader and dataframe-shape inspection

## Purpose

This preflight inspects the actual MT5 loader API and loaded dataframe shape before writing the expanded broker-native session-boundary diagnostic.

This avoids guessing internal function signatures, dataclass fields, dataframe indexes, or column names.

## Restrictions

This preflight is read-only with respect to raw broker-native files.

No H017 validation was run.

No strategy tuning was performed.

No derived M1 or H4 datasets were written.

No raw broker files were modified.

No raw broker files were committed.

## Inputs

The preflight inspects these local gitignored files:

- data/raw/USDJPY/M1.csv
- data/raw/USDJPY/H4.csv
- data/raw/XAUUSD/M1.csv
- data/raw/XAUUSD/H4.csv

## Output

Detailed preflight output is stored in:

- docs/operations/BROKER_NATIVE_EXPANDED_SESSION_DIAGNOSTIC_PREFLIGHT_OUTPUT.txt

## Intended Use

The next diagnostic should use this preflight output to write the expanded broker-native session-boundary analysis without guessing:

1. The `load_mt5_csv(...)` signature.
2. The `MT5LoadResult` dataclass fields.
3. The loaded `bars` dataframe index.
4. The loaded `bars` dataframe columns.
5. Timestamp monotonicity and duplicate behavior.
6. Basic delta patterns for M1 and H4 files.

## Non-Acceptance Statement

This preflight does not accept expanded broker-native M1 as an H017 validation source.

The source remains a promising candidate only.

H017 remains unauthorized until an explicit source-acceptance checkpoint.
