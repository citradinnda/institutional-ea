# HistData M1 Acquisition Inventory

Date: 2026-05-03

Phase: 3.24

## Purpose

This document records the first read-only inventory of newly acquired HistData M1 files.

This is a provenance and file-fingerprint record only.

This does not accept HistData as a research source.

This does not authorize H017 validation.

This does not combine HistData M1 with Exness H4.

## Context

The project was evaluating Dukascopy as the first external M1 data candidate.

During that work, a new development occurred: five years of M1 data were downloaded from HistData for the project symbols.

The original HistData files were preserved exactly as downloaded.

This is important because it preserves a provenance chain:

1. Original HistData files.
2. Any later converted/derived files.
3. Any later loader output.

## Current Location

The inspected files are currently stored under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

This folder name is now misleading because it contains both Dukascopy sample files and HistData files.

The files are still under the repository root-anchored `/data/` directory, which is gitignored.

Raw data must not be committed.

## Files Inspected

### USDJPY

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

Read-only fingerprint:

    exists: True
    size_bytes: 115758784
    sha256: 2aa2840918404b4665f8c79e31ea4a0b691ef85e878f683021cc3c4f7980a29e
    line_count: 1808731

First 5 lines:

    2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0
    2021.01.03,17:01,103.161000,103.161000,103.160000,103.161000,0
    2021.01.03,17:02,103.161000,103.197000,103.161000,103.197000,0
    2021.01.03,17:03,103.181000,103.186000,103.181000,103.182000,0
    2021.01.03,17:04,103.184000,103.196000,103.184000,103.195000,0

Last 5 lines:

    2025.12.31,16:53,156.688000,156.691000,156.687000,156.688000,0
    2025.12.31,16:54,156.692000,156.692000,156.681000,156.687000,0
    2025.12.31,16:55,156.683000,156.687000,156.676000,156.683000,0
    2025.12.31,16:56,156.683000,156.687000,156.678000,156.683000,0
    2025.12.31,16:57,156.683000,156.685000,156.668000,156.671000,0

### XAUUSD

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Read-only fingerprint:

    exists: True
    size_bytes: 117405332
    sha256: e11187138f6aa0b9bbcb75f8fc9423bde6b909a2e9afade01ed952cf6a7b2e13
    line_count: 1726549

First 5 lines:

    2021.01.03,18:00,1904.998000,1910.898000,1903.288000,1909.718000,0
    2021.01.03,18:01,1909.728000,1909.728000,1907.298000,1908.618000,0
    2021.01.03,18:02,1908.528000,1910.408000,1908.378000,1910.238000,0
    2021.01.03,18:03,1910.258000,1910.638000,1909.808000,1910.208000,0
    2021.01.03,18:04,1910.198000,1910.488000,1907.794000,1908.850000,0

Last 5 lines:

    2025.12.31,16:53,4314.255000,4316.469000,4314.009000,4316.029000,0
    2025.12.31,16:54,4315.635000,4317.119000,4314.868000,4316.855000,0
    2025.12.31,16:55,4317.095000,4318.349000,4316.548000,4316.829000,0
    2025.12.31,16:56,4316.585000,4318.169000,4316.525000,4318.079000,0
    2025.12.31,16:57,4318.069000,4318.459000,4317.029000,4318.379000,0

## Observed Format

The inspected files appear to use a HistData-style no-header CSV format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

Example:

    2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0

This is not the same as the observed Dukascopy CSV schema:

    UTC,Open,High,Low,Close,Volume

Therefore these files should not be treated as Dukascopy files.

They should be described as HistData raw files.

## Important Status

HistData is not accepted as a research source yet.

The files have only been inventoried.

They have not yet been loaded into canonical OHLCV format.

They have not yet been checked for:

1. timezone correctness,
2. duplicate timestamps,
3. non-monotonic timestamps,
4. missing-minute patterns,
5. OHLC integrity,
6. non-positive prices,
7. negative volume,
8. zero-volume meaning,
9. weekend behavior,
10. metals daily break behavior,
11. broker mismatch versus Exness.

## Strategic Interpretation

The HistData files may be important because they appear to cover a much longer M1 window than broker-native MT5 currently provides.

However, they must go through the same source-acceptance discipline as any other external data source.

The fact that the date range is long does not make the data research-grade by itself.

## Do-Not Rules

Do not:

1. Do not run H017 validation on HistData yet.
2. Do not combine HistData M1 with Exness H4 silently.
3. Do not tune H017 using HistData.
4. Do not commit raw HistData files.
5. Do not rename or move raw files before documenting the current state.
6. Do not call these files Dukascopy files.
7. Do not accept HistData as a research source until loader validation, provenance, and coverage checks are complete.

## Recommended Next Step

The next development step should be:

    Phase 3.25 - Inspect HistData raw format and design a dedicated HistData loader

That phase should first inspect existing loader APIs and then add a tested loader only after confirming the intended API.

A dedicated HistData loader is preferred over forcing these files through the Dukascopy loader because the raw schema is different and provenance must remain explicit.
