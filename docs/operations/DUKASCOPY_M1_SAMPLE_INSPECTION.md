# Dukascopy M1 Sample Inspection

## Purpose

This document records the first controlled inspection of tiny Dukascopy M1 sample files.

The goal is not to accept Dukascopy as a research source yet.

The goal is to inspect the actual exported file format before deciding whether a dedicated Dukascopy loader is justified.

## Phase

Phase 3.18 — Acquire and inspect small Dukascopy M1 sample files.

## Local sample location

Raw sample files were stored locally under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

These files are intentionally not committed because the repository root has this gitignore rule:

    /data/

## Sample files inspected

Two one-day CSV samples were acquired from Dukascopy / JForex historical export tooling:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USD-JPY_Minute_2024-01-03_UTC.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAU-USD_Minute_2024-01-03_UTC.csv

Sample date:

    2024-01-03

Timeframe:

    M1 / 1 minute

Export timezone indicated by filename and timestamp text:

    UTC

## Observed CSV schema

Both files used the same header:

    UTC,Open,High,Low,Close,Volume

Observed timestamp format:

    dd.mm.yyyy HH:MM:SS.mmm UTC

Example:

    03.01.2024 00:00:00.000 UTC

Observed columns:

- UTC
- Open
- High
- Low
- Close
- Volume

## Manual first-line inspection

USDJPY first observed data row:

    03.01.2024 00:00:00.000 UTC,142.174,142.174,142.132,142.155,112.74

XAUUSD first observed data row:

    03.01.2024 00:00:00.000 UTC,2059.475,2059.545,2059.155,2059.155,0.00416

No metadata rows were observed before the header.

## Mechanical inspection summary

### USDJPY sample

File:

    USD-JPY_Minute_2024-01-03_UTC.csv

Observed results:

    rows=1440
    first_timestamp=2024-01-03 00:00:00+00:00
    last_timestamp=2024-01-03 23:59:00+00:00
    is_monotonic_increasing=True
    duplicate_timestamps=0
    expected_minutes_between_first_and_last=1440
    missing_minutes_between_first_and_last=0
    bad_ohlc_rows=0
    non_positive_price_rows=0
    negative_volume_rows=0
    zero_volume_rows=0

Interpretation:

The USDJPY sample is mechanically clean for this one day.

### XAUUSD sample

File:

    XAU-USD_Minute_2024-01-03_UTC.csv

Observed results:

    rows=1380
    first_timestamp=2024-01-03 00:00:00+00:00
    last_timestamp=2024-01-03 23:59:00+00:00
    is_monotonic_increasing=True
    duplicate_timestamps=0
    expected_minutes_between_first_and_last=1440
    missing_minutes_between_first_and_last=60
    bad_ohlc_rows=0
    non_positive_price_rows=0
    negative_volume_rows=0
    zero_volume_rows=0

First missing minutes observed:

    2024-01-03 22:00:00+00:00
    2024-01-03 22:01:00+00:00
    2024-01-03 22:02:00+00:00
    2024-01-03 22:03:00+00:00
    2024-01-03 22:04:00+00:00
    2024-01-03 22:05:00+00:00
    2024-01-03 22:06:00+00:00
    2024-01-03 22:07:00+00:00
    2024-01-03 22:08:00+00:00
    2024-01-03 22:09:00+00:00

Interpretation:

The XAUUSD sample is mechanically clean for observed rows, but it has a 60-minute gap beginning at 22:00 UTC.

This may be a normal daily metals trading break, but this document does not treat that as proven.

A future multi-day inspection should confirm whether this gap is systematic and expected.

## Preliminary conclusions

The sample inspection supports the following limited conclusions:

1. Dukascopy CSV export can produce simple M1 files with a stable apparent schema.
2. The timestamp column explicitly includes UTC text.
3. Both sample files use the same columns.
4. The observed OHLC values are internally consistent.
5. The observed timestamps are monotonic and have no duplicates.
6. USDJPY showed full 24-hour minute coverage for the inspected day.
7. XAUUSD showed a 60-minute missing block beginning at 22:00 UTC.
8. Volume exists, but its meaning should not be assumed to match MT5 tick volume or broker volume.

## Non-conclusions

This inspection does not prove:

1. Dukascopy is accepted as a research-grade source.
2. Dukascopy XAUUSD is equivalent to Exness XAUUSD.
3. Dukascopy volume is comparable to MT5 tick volume.
4. The XAUUSD 22:00 UTC gap is always expected.
5. The files are safe to use in H017 validation.
6. A loader has been validated.
7. Broker mismatch risk has been solved.

## Next recommended action

The next recommended sub-phase is to create a dedicated Dukascopy loader only after confirming the intended canonical schema.

A loader phase should include tests for:

1. Required columns.
2. Timestamp parsing.
3. UTC timezone handling.
4. Canonical OHLCV output.
5. Duplicate timestamp rejection.
6. OHLC integrity rejection.
7. Non-positive price rejection.
8. Negative volume rejection.
9. Missing-minute reporting without automatically treating all gaps as errors.

Raw Dukascopy files must remain uncommitted.

Dukascopy data must not be used as H017 research evidence until the loader and acceptance criteria are documented and tested.
