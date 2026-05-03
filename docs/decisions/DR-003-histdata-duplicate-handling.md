# DR-003: HistData Exact Duplicate Timestamp Handling

Date: 2026-05-03

Status: Proposed

## Context

The project acquired approximately five years of HistData M1 data for:

1. USDJPY
2. XAUUSD

The raw files are local and gitignored under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

This directory name is currently misleading because it contains both Dukascopy sample files and HistData files.

The original HistData files were preserved exactly as downloaded.

Phase 3.24 inventoried the files.

Phase 3.25 added a dedicated tested HistData M1 loader:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py

The loader supports the observed no-header HistData format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

The loader is intentionally separate from the Dukascopy loader because the schemas and source identities differ.

## Current Finding

Running the strict HistData loader on the real local HistData files fails because both files contain duplicate timestamps.

The failure is intentional protective behavior.

The shared canonical helper would silently drop duplicate timestamps, so the HistData loader rejects duplicates before canonicalization.

## Duplicate Diagnostic Summary

Both USDJPY and XAUUSD contain the same duplicate timestamp pattern.

Each file has:

    n_duplicate_rows_in_duplicate_groups: 600
    n_duplicate_timestamp_values: 300
    n_conflicting_duplicate_timestamp_values: 0
    all_duplicate_groups_have_identical_ohlcv: True

The duplicate blocks occur on:

    2021.10.31 19:00 through 19:59
    2022.10.30 19:00 through 19:59
    2023.10.29 19:00 through 19:59
    2024.10.27 19:00 through 19:59
    2025.10.26 19:00 through 19:59

Each duplicated timestamp has exactly two rows.

The duplicate rows are exact OHLCV duplicates, not conflicting bars.

This pattern strongly suggests a recurring daylight-saving-time related duplicate hour, but that explanation is not yet sufficient by itself to accept the source.

## Decision

Exact duplicate timestamp rows may be removed only through an explicit audited repair path.

The raw HistData files must remain unchanged.

The strict loader behavior should remain the default:

1. Duplicate timestamps are fatal by default.
2. Non-monotonic timestamps are fatal by default.
3. Conflicting duplicate timestamp groups are always fatal.
4. Silent deduplication is not allowed.
5. Any deduplication must be explicit, tested, and documented.

A future implementation may add an explicit repair mode or separate repair utility that permits dropping exact duplicate OHLCV rows only when all rows in each duplicate timestamp group are identical across:

    open
    high
    low
    close
    volume

The repair path must preserve audit metadata, including:

1. input file path,
2. input file SHA256,
3. input row count,
4. output row count,
5. number of duplicate rows removed,
6. number of duplicate timestamp values,
7. duplicate timestamp ranges,
8. confirmation that no conflicting duplicates existed,
9. source timezone assumption,
10. code version or commit used to create the derived output.

## Rationale

Duplicate timestamps are dangerous because event-driven backtests assume a unique ordered time index.

Silently dropping duplicate rows would hide vendor data defects and could create non-reproducible research.

However, exact duplicate OHLCV rows are different from conflicting duplicate bars.

If duplicate rows are exact copies, then removing one copy may be a defensible normalization step, but only if it is explicit, tested, and recorded as derived data.

The raw files must remain untouched so future checks can reproduce the provenance chain.

## Consequences

HistData remains unaccepted as a research source.

The current strict loader remains correct.

No H017 validation may use HistData until duplicate handling, provenance, and coverage checks are complete.

A future phase may add one of the following, after tests are designed:

1. an explicit loader parameter such as `duplicate_policy="reject"` by default, with an audited exact-duplicate mode, or
2. a separate repair/normalization utility that writes derived files under `/data/derived/`.

The project should prefer the option that provides the clearest audit trail.

## Do-Not Rules

Do not:

1. Do not modify raw HistData files.
2. Do not silently deduplicate vendor data.
3. Do not allow conflicting duplicate timestamps.
4. Do not run H017 validation on HistData yet.
5. Do not combine HistData M1 with Exness H4 yet.
6. Do not tune H017 using HistData.
7. Do not commit raw or derived large data files.
8. Do not accept HistData as a research source based only on exact duplicate removability.
9. Do not change `.gitignore` from `/data/` to `data/`.

## Required Follow-Up Before HistData Research Use

Before HistData can be used as H017 validation evidence, the project still needs:

1. Tested duplicate-handling implementation.
2. Derived-data provenance plan.
3. Coverage checks after duplicate handling.
4. Missing-minute block analysis.
5. Weekend behavior analysis.
6. XAUUSD metals-break behavior analysis.
7. Timezone/session reconciliation.
8. Broker mismatch assessment versus Exness.
9. Explicit final source acceptance or rejection decision.
