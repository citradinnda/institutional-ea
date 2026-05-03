# HistData M1 Loader Real-File Check

Date: 2026-05-03

Phase: 3.25-c

## Purpose

This document records the first loader-based check of the real local HistData M1 files.

This is infrastructure and source-quality evidence only.

This does not accept HistData as a research source.

This does not authorize H017 validation.

This does not combine HistData M1 with Exness H4.

This does not modify, rename, move, deduplicate, or rewrite the raw HistData files.

## Context

Phase 3.25 added a dedicated tested HistData M1 CSV loader:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py

Tests were added at:

    C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py

Focused test result:

    15 passed

Full test result after adding the loader:

    509 passed

The full-test anchor increased deliberately from `494 passed` to `509 passed` because 15 focused HistData loader tests were added.

## Loader API

Public loader:

    from quantcore.data.histdata_loader import load_histdata_m1_csv

Function:

    load_histdata_m1_csv(path: str | Path, *, source_tz: str = "UTC") -> HistDataM1LoadResult

Result fields:

    bars
    n_bars
    n_input_rows
    earliest_utc
    latest_utc
    source_tz
    n_missing_minutes
    missing_minutes

## Observed Raw Format

The real local HistData files use the observed no-header comma-separated format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

Example:

    2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0

This is distinct from the observed Dukascopy format:

    UTC,Open,High,Low,Close,Volume

The dedicated HistData loader must remain separate from the Dukascopy loader.

## Raw Files Checked

The files checked are local raw files under the gitignored `/data/` directory:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Important:

The directory name `dukascopy_samples` is misleading because it currently contains both Dukascopy sample files and HistData files.

The files were not moved or renamed during this phase.

The raw files remain uncommitted.

## Loader Result On Real Files

Running:

    load_histdata_m1_csv(path)

on the USDJPY real HistData file failed with:

    ValueError: HistData M1 CSV at C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv has duplicate timestamps.

This is expected protective behavior.

The loader rejects duplicate timestamps before canonicalization because the shared canonical helper would otherwise silently drop duplicate timestamps.

After the USDJPY duplicate failure, a read-only duplicate diagnostic was run on both files.

## Duplicate Timestamp Diagnostic Summary

### USDJPY

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

Summary:

    n_rows: 1808731
    n_unique_timestamp_text: 1808431
    n_duplicate_rows_in_duplicate_groups: 600
    n_duplicate_timestamp_values: 300
    n_conflicting_duplicate_timestamp_values: 0
    all_duplicate_groups_have_identical_ohlcv: True
    timestamp_parse_ok: True
    parsed_first: 2021-01-03 17:00:00
    parsed_last: 2025-12-31 16:57:00
    parsed_is_monotonic_increasing: False
    parsed_has_duplicates: True
    n_non_monotonic_backward_steps: 5

Duplicate rows by date:

    2021.10.31: rows=120, first_dt=2021.10.31 19:00, last_dt=2021.10.31 19:59, line_span=305072-305191
    2022.10.30: rows=120, first_dt=2022.10.30 19:00, last_dt=2022.10.30 19:59, line_span=677606-677725
    2023.10.29: rows=120, first_dt=2023.10.29 19:00, last_dt=2023.10.29 19:59, line_span=1001472-1001591
    2024.10.27: rows=120, first_dt=2024.10.27 19:00, last_dt=2024.10.27 19:59, line_span=1371399-1371518
    2025.10.26: rows=120, first_dt=2025.10.26 19:00, last_dt=2025.10.26 19:59, line_span=1741003-1741122

Example duplicate timestamp groups:

    2021.10.31 19:00: n_rows=2, n_unique_ohlcv=1, line_numbers=(305072, 305132)
    2021.10.31 19:01: n_rows=2, n_unique_ohlcv=1, line_numbers=(305073, 305133)
    2021.10.31 19:02: n_rows=2, n_unique_ohlcv=1, line_numbers=(305074, 305134)

There were no conflicting duplicate groups.

### XAUUSD

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Summary:

    n_rows: 1726549
    n_unique_timestamp_text: 1726249
    n_duplicate_rows_in_duplicate_groups: 600
    n_duplicate_timestamp_values: 300
    n_conflicting_duplicate_timestamp_values: 0
    all_duplicate_groups_have_identical_ohlcv: True
    timestamp_parse_ok: True
    parsed_first: 2021-01-03 18:00:00
    parsed_last: 2025-12-31 16:57:00
    parsed_is_monotonic_increasing: False
    parsed_has_duplicates: True
    n_non_monotonic_backward_steps: 5

Duplicate rows by date:

    2021.10.31: rows=120, first_dt=2021.10.31 19:00, last_dt=2021.10.31 19:59, line_span=293249-293368
    2022.10.30: rows=120, first_dt=2022.10.30 19:00, last_dt=2022.10.30 19:59, line_span=647802-647921
    2023.10.29: rows=120, first_dt=2023.10.29 19:00, last_dt=2023.10.29 19:59, line_span=956710-956829
    2024.10.27: rows=120, first_dt=2024.10.27 19:00, last_dt=2024.10.27 19:59, line_span=1309624-1309743
    2025.10.26: rows=120, first_dt=2025.10.26 19:00, last_dt=2025.10.26 19:59, line_span=1662652-1662771

Example duplicate timestamp groups:

    2021.10.31 19:00: n_rows=2, n_unique_ohlcv=1, line_numbers=(293249, 293309)
    2021.10.31 19:01: n_rows=2, n_unique_ohlcv=1, line_numbers=(293250, 293310)
    2021.10.31 19:02: n_rows=2, n_unique_ohlcv=1, line_numbers=(293251, 293311)

There were no conflicting duplicate groups.

## Interpretation

Both HistData files contain duplicate timestamp blocks.

The duplicate rows are exact OHLCV duplicates, not conflicting bars.

The duplicate timestamp blocks occur on five annual dates:

    2021.10.31
    2022.10.30
    2023.10.29
    2024.10.27
    2025.10.26

On each date, the duplicated timestamp range is:

    19:00 through 19:59

Each duplicated timestamp has exactly two rows.

This pattern strongly suggests a recurring daylight-saving-time related duplicate hour, but that is not yet accepted as a final explanation.

A future phase may design an explicit, audited repair or normalization step for exact duplicate rows, but this phase does not do that.

## Current Status

HistData is still not accepted as a research source.

The raw files have not been altered.

The current dedicated loader correctly refuses to load these raw files because duplicate timestamps are present.

No H017 validation has been run on HistData.

No HistData M1 data has been combined with Exness H4 data.

No tuning has been performed.

## Required Future Work Before Any HistData Research Use

Before HistData can be used as H017 validation evidence, the project still needs:

1. A documented decision on exact duplicate handling.
2. Tests for any approved duplicate-handling behavior.
3. A derived-data provenance plan if repaired files are created.
4. Coverage checks after duplicate handling.
5. Missing-minute block analysis.
6. Weekend behavior analysis.
7. Metals daily break behavior analysis.
8. Timezone/source-session reconciliation.
9. Broker mismatch analysis versus Exness.
10. Explicit acceptance or rejection decision.

## Do-Not Rules Preserved

Do not:

1. Do not run H017 validation on HistData yet.
2. Do not combine HistData M1 with Exness H4 silently.
3. Do not tune H017 using HistData.
4. Do not commit raw HistData files.
5. Do not rename or move raw files before that is explicitly planned.
6. Do not call HistData files Dukascopy files.
7. Do not silently deduplicate raw vendor data.
8. Do not accept HistData as a research source until loader validation, provenance, repair/coverage policy, and coverage checks are complete.
