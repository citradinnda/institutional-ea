# HistData Derived-Data Provenance Plan

Date: 2026-05-03

## Purpose

This document defines the provenance rules that must be followed before writing any cleaned, canonical, or otherwise derived HistData files.

This is a planning document only.

No derived HistData files are created by this phase.

HistData remains not accepted as a research source.

H017 must not be run on HistData yet.

## Background

The project has raw HistData M1 files for USDJPY and XAUUSD covering approximately 2021 through 2025.

The raw files are stored under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\

Important note:

The folder name `dukascopy_samples` is misleading. The relevant files are HistData files, not Dukascopy files.

The raw HistData files are gitignored by the root-anchored `/data/` rule and must not be committed.

The dedicated HistData loader exists at:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py

The loader supports:

    duplicate_policy="reject"

and explicit opt-in:

    duplicate_policy="drop_exact"

The strict default policy remains duplicate rejection.

## Raw Files

USDJPY raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

Recorded inventory:

    size_bytes: 115758784
    sha256: 2aa2840918404b4665f8c79e31ea4a0b691ef85e878f683021cc3c4f7980a29e
    line_count: 1808731
    first observed timestamp row: 2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0
    last observed timestamp row: 2025.12.31,16:57,156.683000,156.685000,156.668000,156.671000,0

XAUUSD raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Recorded inventory:

    size_bytes: 117405332
    sha256: e11187138f6aa0b9bbcb75f8fc9423bde6b909a2e9afade01ed952cf6a7b2e13
    line_count: 1726549
    first observed timestamp row: 2021.01.03,18:00,1904.998000,1910.898000,1903.288000,1909.718000,0
    last observed timestamp row: 2025.12.31,16:57,4318.069000,4318.459000,4317.029000,4318.379000,0

## Non-Negotiable Rules

1. Raw HistData files must remain unchanged.
2. Raw HistData files must not be committed.
3. Large derived HistData files must not be committed.
4. Derived files may only be written after this provenance plan exists.
5. Derived files must record the exact raw input files used.
6. Derived files must record raw input SHA256 hashes.
7. Derived files must record the loader API and duplicate policy used.
8. Derived files must record the git commit that produced them.
9. Derived files must record row counts before and after duplicate handling.
10. Derived files must record duplicate timestamp metadata.
11. Derived files must record coverage and missing-minute metadata.
12. Derived files must not silently merge HistData with Exness broker data.
13. Derived files must not imply HistData is accepted as a research source.
14. H017 must not be run on derived HistData until source acceptance is explicitly decided.

## Proposed Derived Data Location

If derived HistData files are later written, they should live under `/data/` so they remain gitignored.

Proposed location:

    C:\Users\equin\Documents\institutional-ea\data\derived\histdata_m1\

Proposed per-run structure:

    C:\Users\equin\Documents\institutional-ea\data\derived\histdata_m1\YYYYMMDD_HHMMSS_<git_short_sha>\

Example only:

    C:\Users\equin\Documents\institutional-ea\data\derived\histdata_m1\20260503_120000_bba281a\

This phase does not create that directory.

## Proposed Derived File Names

If canonical per-symbol files are later written, proposed names are:

    USDJPY_M1_HistData_2021_2025_UTC_drop_exact.parquet
    XAUUSD_M1_HistData_2021_2025_UTC_drop_exact.parquet

A metadata sidecar should be written next to the derived data.

Proposed metadata file:

    MANIFEST.json

This phase does not create these files.

## Required Manifest Fields

Every future derived-data manifest must include at least:

    manifest_schema_version
    created_at_utc
    created_by_phase
    git_commit
    git_branch
    repository_status_before_write
    repository_status_after_write
    python_version
    pandas_version
    source_name
    source_files
    symbol
    timeframe
    source_timezone_assumption
    output_timezone
    loader_module
    loader_function
    loader_duplicate_policy
    raw_file_path
    raw_file_size_bytes
    raw_file_sha256
    raw_file_line_count
    n_input_rows
    n_output_bars
    earliest_utc
    latest_utc
    n_duplicate_rows_removed
    n_duplicate_timestamp_values
    duplicate_timestamp_ranges
    n_missing_minutes
    first_missing_minutes_sample
    last_missing_minutes_sample
    columns
    index_timezone
    index_is_monotonic_increasing
    index_has_duplicates
    non_positive_ohlc_rows
    bad_ohlc_rows
    negative_volume_rows
    zero_volume_rows
    notes
    acceptance_status

The `acceptance_status` field must explicitly say:

    not_accepted_as_research_source

until a later documented source-acceptance decision changes that status.

## Required Per-Symbol Metadata

Each symbol must have separate metadata.

USDJPY and XAUUSD must not be treated as interchangeable because they have different trading sessions, liquidity behavior, missing-minute patterns, and instrument mechanics.

## Duplicate Policy Requirements

The manifest must record the duplicate policy exactly.

Allowed values currently are:

    reject
    drop_exact

For the known real HistData files, strict duplicate rejection fails because both symbols contain duplicate timestamp groups.

If `drop_exact` is used, the manifest must record:

    n_duplicate_rows_removed
    n_duplicate_timestamp_values
    duplicate_timestamp_ranges

Conflicting duplicate timestamp groups remain fatal and must not be resolved automatically.

## Coverage Requirements Before Research Use

Before HistData can be accepted as a research source, the project still needs:

1. missing-minute coverage analysis,
2. weekend behavior analysis,
3. XAUUSD metals session-break analysis,
4. timezone and source-session reconciliation,
5. broker mismatch assessment versus Exness,
6. final source acceptance or rejection decision.

The existence of derived data does not satisfy these requirements by itself.

## H4 and M1 Alignment Warning

HistData M1 must not be silently combined with Exness H4 bars.

Before any combined H4/M1 research run, the project must explicitly decide how H4 bars are produced.

Acceptable future options may include:

1. derive H4 bars from the same HistData M1 source,
2. compare HistData-derived H4 bars against Exness H4 bars,
3. reject HistData if source-session mismatch is unacceptable.

No such decision is made in this document.

## Git and Storage Policy

The root `.gitignore` rule must remain root-anchored:

    /data/

It must not be changed to unanchored:

    data/

Reason:

An unanchored `data/` rule risks excluding source code under:

    quantcore/data/

Raw and large derived data files under `/data/` must remain untracked.

Small documentation files under `docs/` should be committed.

## Current Status

As of this document:

1. HistData raw files are inventoried.
2. A dedicated HistData loader exists.
3. Strict duplicate rejection remains the default.
4. Explicit `drop_exact` duplicate handling is tested.
5. Real-file `drop_exact` loader output is documented.
6. No derived HistData files have been written.
7. HistData remains not accepted as a research source.
8. H017 has not been run on HistData.

## Next Recommended Work

The next recommended sub-phase is to design and run a coverage/session analysis that explains the large missing-minute counts without yet accepting HistData for research validation.

Potential next document or code phase:

    Phase 3.26-e - HistData M1 coverage and session analysis plan

That phase should remain analytical and should not run H017.
