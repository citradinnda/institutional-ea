# Dukascopy Coverage Check Plan

Date: 2026-05-03

Phase: 3.23

## Purpose

This document defines the next controlled coverage-check step for Dukascopy M1 data.

Dukascopy is currently an external M1 data candidate only.

The tested loader can parse the observed tiny sample files, but that is not enough to accept Dukascopy as a research source.

The next step is to inspect a small multi-day sample before any large export or research validation run.

This is a planning document only.

No bulk data is accepted by this document.

No H017 validation is authorized by this document.

## Current Status Before This Plan

Completed infrastructure and inspection work:

1. A tiny one-day USDJPY sample was manually inspected.
2. A tiny one-day XAUUSD sample was manually inspected.
3. The observed Dukascopy CSV schema was documented as:

       UTC,Open,High,Low,Close,Volume

4. The observed timestamp format was documented as:

       dd.mm.yyyy HH:MM:SS.mmm UTC

5. A tested Dukascopy CSV loader was added.
6. The tested loader reproduced the expected tiny-sample results.
7. XAUUSD showed a 60-minute missing block beginning at `2024-01-03 22:00:00+00:00`.

Current interpretation:

- The loader works on the tiny observed samples.
- The tiny samples are not enough to prove coverage quality.
- The XAUUSD missing block may be a normal metals daily break, but that is not yet proven.
- Dukascopy remains under evaluation only.

## Symbols To Check

The next controlled coverage check should remain limited to the project's current two instruments:

1. USDJPY
2. XAUUSD

Do not broaden to additional symbols during this phase.

## Recommended First Multi-Day Window

The first multi-day coverage check should use a small window only.

Recommended first window:

    2024-01-02 through 2024-01-08 UTC

Rationale:

- It is short enough to inspect quickly.
- It includes several normal weekdays.
- It includes a weekend boundary.
- It is close to the already inspected `2024-01-03` tiny samples.
- It can help distinguish normal market closures from suspicious data gaps.

If the data source interface makes this exact window inconvenient, choose the nearest equivalent small window and document the exact dates.

## Local Raw Data Location

Any downloaded raw Dukascopy CSV files must remain under the gitignored `/data/` directory.

Recommended local directory:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_coverage_check

Raw CSV files must not be committed.

## Required Measurements

For each symbol and each file, record:

1. File path
2. Symbol
3. Date range requested
4. Date range actually present
5. CSV header
6. Timestamp format
7. Number of input rows
8. Number of canonical bars loaded
9. Earliest UTC timestamp
10. Latest UTC timestamp
11. Whether the timestamp index is timezone-aware UTC
12. Whether timestamps are strictly monotonic increasing
13. Whether duplicate timestamps exist
14. Number of missing minutes between first and last timestamp
15. First 20 missing minutes, if any
16. Missing-minute blocks summarized by start, end, and duration
17. Count of non-positive OHLC price rows
18. Count of structurally invalid OHLC rows
19. Count of negative volume rows
20. Count of zero-volume rows

## Required Cross-Day Checks

The multi-day check must specifically inspect whether gaps are explained by expected market structure.

Required questions:

1. Does USDJPY show normal weekend closure behavior?
2. Does USDJPY have unexpected weekday gaps?
3. Does XAUUSD show a recurring daily break?
4. If XAUUSD shows a daily break, does it occur at the same UTC time each day?
5. Is the observed `22:00` UTC XAUUSD missing block repeated on other weekdays?
6. Are there any gaps outside expected weekend or metals-break windows?
7. Are all timestamps consistently UTC?
8. Does the schema remain stable across files and symbols?

## Missing-Minute Block Definition

A missing-minute block means one or more consecutive expected one-minute timestamps are absent between the first and last loaded timestamp.

Example:

    2024-01-03 22:00:00+00:00
    2024-01-03 22:01:00+00:00
    2024-01-03 22:02:00+00:00

These would be summarized as a single block if they are consecutive.

The summary should report:

- block start
- block end
- number of missing minutes in the block

## Acceptance Criteria For This Coverage Check

Passing this coverage check would not fully accept Dukascopy yet.

It would only allow a later larger coverage/provenance phase.

The small multi-day check should be considered acceptable only if:

1. The loader successfully parses all selected files.
2. The schema is stable.
3. Timestamps are UTC and timezone semantics remain explicit.
4. There are no duplicate timestamps.
5. There are no non-monotonic timestamp sequences.
6. There are no non-positive OHLC prices.
7. There are no structurally invalid OHLC rows.
8. There are no negative volume rows.
9. Missing-minute patterns are explainable as weekend closures or documented instrument trading breaks.
10. Any XAUUSD daily break pattern is consistent across multiple weekdays.

## Failure Conditions

The small multi-day check should fail if any of the following occur:

1. The loader cannot parse the files.
2. Required columns are missing.
3. Timestamp format changes without explanation.
4. Timestamps are not UTC.
5. Duplicate timestamps exist.
6. Timestamps are non-monotonic.
7. OHLC prices are non-positive.
8. OHLC rows are structurally invalid.
9. Volume is negative.
10. Unexpected weekday gaps appear.
11. XAUUSD missing-minute blocks are inconsistent or unexplained.
12. Provenance cannot be documented.

## Provenance To Record

For any future downloaded files, record:

1. Data source name
2. Data source interface used
3. Download date
4. Symbol name exactly as exported
5. Requested timeframe
6. Requested timezone
7. Requested date range
8. Exported file names
9. Any manual settings used during export
10. Any observed limitations or warnings from the data source

Provenance means the documented origin and handling history of the data.

Without provenance, the data cannot be accepted for research validation.

## Do-Not Rules

Do not:

1. Do not use Dukascopy data as H017 validation evidence yet.
2. Do not combine Dukascopy M1 with Exness H4 silently.
3. Do not tune H017 using Dukascopy data.
4. Do not change the cost model.
5. Do not commit raw Dukascopy CSV files.
6. Do not broaden to more symbols yet.
7. Do not start Phase 4 execution code.
8. Do not treat the short-window 2026 event result as validated edge.
9. Do not ignore the `-33.65%` drawdown.
10. Do not accept Dukascopy based only on tiny samples.
11. Do not proceed to large exports until the small multi-day check is documented.

## Recommended Next Sub-Phase

The next sub-phase should be:

    Phase 3.24 - Acquire a tiny multi-day Dukascopy coverage sample

That phase should be operational only.

It should download or export only the small planned window, save raw files under the gitignored `/data/` directory, and then stop for inspection.

No raw CSV files should be committed.

## Conclusion

This plan defines the minimum checks needed before Dukascopy can advance beyond tiny-sample loader validation.

Passing the future small multi-day coverage check would improve data-source confidence.

It would still not automatically make Dukascopy an accepted research source.

A larger documented coverage and provenance phase would still be required before H017 validation could use Dukascopy-derived M1 data.
