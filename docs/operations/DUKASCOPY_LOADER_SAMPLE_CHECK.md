# Dukascopy Loader Sample Check

Date: 2026-05-03

Phase: 3.22

## Purpose

This document records a loader-based check of the existing tiny local Dukascopy M1 sample files.

The goal was to confirm that the tested Dukascopy CSV loader produces the same mechanical results as the earlier manual inspection.

This is an infrastructure check only.

This does not accept Dukascopy as a research source.

This does not use Dukascopy data as H017 validation evidence.

## Loader Used

Public API:

    from quantcore.data.dukascopy_loader import load_dukascopy_csv

Loader function:

    load_dukascopy_csv(path)

Result type:

    DukascopyLoadResult

## Local Sample Files Checked

The checked files were local raw data files under the gitignored `/data/` directory:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USD-JPY_Minute_2024-01-03_UTC.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAU-USD_Minute_2024-01-03_UTC.csv

These raw CSV files remain uncommitted.

## USDJPY Loader Result

File:

    USD-JPY_Minute_2024-01-03_UTC.csv

Observed loader output:

    n_input_rows: 1440
    n_bars: 1440
    earliest_utc: 2024-01-03 00:00:00+00:00
    latest_utc: 2024-01-03 23:59:00+00:00
    n_missing_minutes: 0
    first_missing_minutes: ()
    columns: ['open', 'high', 'low', 'close', 'volume']
    tz: UTC
    is_monotonic_increasing: True
    has_duplicates: False

Interpretation:

- The loader output matches the earlier manual/mechanical inspection.
- The sample covers a full UTC day from `00:00` through `23:59`.
- The loader produced canonical OHLCV columns.
- The timestamp index is timezone-aware UTC.
- There are no duplicate timestamps.
- There are no missing minutes between the first and last timestamp.

## XAUUSD Loader Result

File:

    XAU-USD_Minute_2024-01-03_UTC.csv

Observed loader output:

    n_input_rows: 1380
    n_bars: 1380
    earliest_utc: 2024-01-03 00:00:00+00:00
    latest_utc: 2024-01-03 23:59:00+00:00
    n_missing_minutes: 60
    first_missing_minutes:
      - 2024-01-03 22:00:00+00:00
      - 2024-01-03 22:01:00+00:00
      - 2024-01-03 22:02:00+00:00
      - 2024-01-03 22:03:00+00:00
      - 2024-01-03 22:04:00+00:00
      - 2024-01-03 22:05:00+00:00
      - 2024-01-03 22:06:00+00:00
      - 2024-01-03 22:07:00+00:00
      - 2024-01-03 22:08:00+00:00
      - 2024-01-03 22:09:00+00:00
    columns: ['open', 'high', 'low', 'close', 'volume']
    tz: UTC
    is_monotonic_increasing: True
    has_duplicates: False

Interpretation:

- The loader output matches the earlier manual/mechanical inspection.
- The sample spans `2024-01-03 00:00:00+00:00` through `2024-01-03 23:59:00+00:00`.
- The loader produced canonical OHLCV columns.
- The timestamp index is timezone-aware UTC.
- There are no duplicate timestamps.
- The loader reports 60 missing minutes.
- The first observed missing minute is `2024-01-03 22:00:00+00:00`.

## Important Caution

The XAUUSD 60-minute missing block may be a normal daily metals trading break.

This is not yet proven.

Do not assume all XAUUSD gaps are acceptable until multi-day inspection confirms the pattern.

## Current Status

Dukascopy remains under evaluation only.

It is not accepted as a research source yet.

The tested loader can parse the observed tiny sample files and report coverage metadata correctly.

## Do-Not Rules Preserved

Do not:

1. Do not use Dukascopy data as H017 validation evidence yet.
2. Do not combine Dukascopy M1 with Exness H4 silently.
3. Do not tune H017 using Dukascopy data.
4. Do not commit raw Dukascopy CSV files.
5. Do not treat the XAUUSD 60-minute gap as acceptable without multi-day evidence.
6. Do not accept Dukascopy without documented provenance, coverage, and validation over a larger sample.
7. Do not start Phase 4 execution code from this result.

## Conclusion

The loader-based sample check passed.

The tested Dukascopy loader reproduces the expected sample-level results for the existing local USDJPY and XAUUSD tiny CSV files.

This improves infrastructure confidence only.

It does not improve H017 research confidence yet.
