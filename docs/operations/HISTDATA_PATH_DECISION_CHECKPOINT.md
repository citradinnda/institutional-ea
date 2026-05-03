# HistData Path Decision Checkpoint

Date created: 2026-05-03T22:54:04+09:00

## Purpose

This document records Phase 3.26-x: HistData path decision checkpoint.

The purpose is to make a bounded operational decision about the current HistData path after the broker H4/M1 loaded-shape inspection, broker-only H4/M1 alignment diagnostic, and H4 construction decision checkpoint.

This document does not load HistData, does not run H017, does not write derived data, and does not modify raw files.

## Decision summary

HistData is rejected for H017 validation under the current evidence.

HistData raw files may remain available for diagnostic reference only.

Current statuses:

1. HistData as H017 validation source: rejected under current evidence.
2. HistData as accepted research source: not accepted.
3. HistData-built H4: not accepted.
4. Broker H4 plus HistData M1 hybrid: not accepted.
5. Derived HistData files: not authorized.
6. H017 validation on HistData: not authorized.
7. Long-history H017 validation source: none accepted.
8. H017 status: alive but not promotable.

## What this decision means

This decision means:

1. We should stop treating HistData as the likely path to H017 validation.
2. We should not spend additional strategy-validation effort trying to force H017 onto HistData.
3. We should not build H4 bars from HistData for H017 validation.
4. We should not combine broker-native H4 with HistData M1 for event-driven validation.
5. We should keep the raw HistData files unchanged and gitignored.
6. We may still use HistData for source-quality diagnostics, documentation, or comparison if explicitly planned.

This decision does not mean:

1. HistData raw files should be deleted.
2. HistData raw files should be modified.
3. HistData should be committed.
4. Any derived HistData file should be written.
5. Broker-native short M1 history is sufficient for research validation.
6. H017 is validated.
7. H017 is promotable.
8. Live trading is authorized.

## Evidence considered

### HistData raw inventory

HistData files were inventoried and preserved as downloaded.

USDJPY raw HistData file:

C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

Known inventory:

1. size_bytes: 115758784.
2. sha256: 2aa2840918404b4665f8c79e31ea4a0b691ef85e878f683021cc3c4f7980a29e.
3. line_count: 1808731.
4. first observed timestamp row: 2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0.
5. last observed timestamp row: 2025.12.31,16:57,156.683000,156.685000,156.668000,156.671000,0.

XAUUSD raw HistData file:

C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Known inventory:

1. size_bytes: 117405332.
2. sha256: e11187138f6aa0b9bbcb75f8fc9423bde6b909a2e9afade01ed952cf6a7b2e13.
3. line_count: 1726549.
4. first observed timestamp row: 2021.01.03,18:00,1904.998000,1910.898000,1903.288000,1909.718000,0.
5. last observed timestamp row: 2025.12.31,16:57,4318.069000,4318.459000,4317.029000,4318.379000,0.

Important naming caution:

The raw files are currently under a misleading folder name containing dukascopy_samples, but these files are HistData-format files, not Dukascopy files.

### HistData loader and duplicate policy

A dedicated HistData loader exists at:

C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py

The loader is intentionally strict by default:

load_histdata_m1_csv(..., duplicate_policy="reject")

Duplicate policy status:

1. Strict duplicate rejection remains the default.
2. Explicit drop_exact policy exists only for exact duplicate OHLCV rows.
3. Conflicting duplicate timestamp groups remain fatal.
4. Raw files are not modified.
5. Derived files are not written.

Known duplicate finding:

1. Both USDJPY and XAUUSD had 300 duplicate timestamp values.
2. Each duplicated timestamp had exactly two rows.
3. Duplicate blocks occurred around recurring late-October daylight-saving-time transition windows.
4. The duplicate rows were exact OHLCV duplicates.
5. This finding was documented but did not constitute source acceptance.

### March-July 2023 anomaly

March-July 2023 remains a major unresolved source-quality blocker.

USDJPY March-July comparison:

1. 2021 observed_pct: 70.299110.
2. 2022 observed_pct: 70.918664.
3. 2023 observed_pct: 50.115287.
4. 2024 observed_pct: 70.958606.
5. 2025 observed_pct: 71.042121.

XAUUSD March-July comparison:

1. 2021 observed_pct: 67.450980.
2. 2022 observed_pct: 67.410585.
3. 2023 observed_pct: 48.686910.
4. 2024 observed_pct: 67.404230.
5. 2025 observed_pct: 67.517702.

Interpretation:

1. March-July 2023 is materially abnormal relative to same-month control years.
2. The anomaly affects both USDJPY and XAUUSD.
3. The anomaly is not explained by weekends alone.
4. The anomaly is not explained by the XAUUSD daily break alone.
5. This remains incompatible with research-grade H017 validation.

### Broker short-window session diagnostic

The broker-native 2026 short-window diagnostic showed material session behavior differences from HistData source-session candidates.

USDJPY broker-native M1:

1. n_bars: 97907.
2. earliest_utc: 2026-01-26 03:09:00+00:00.
3. latest_utc: 2026-04-30 07:00:00+00:00.
4. missing_minutes_inside_symbol_range: 37685.

XAUUSD broker-native M1:

1. n_bars: 97966.
2. earliest_utc: 2026-01-20 02:22:00+00:00.
3. latest_utc: 2026-04-30 07:00:00+00:00.
4. missing_minutes_inside_symbol_range: 46313.

Broker mismatch interpretation:

1. Broker-native USDJPY sessions differ materially from HistData USDJPY source-session candidates.
2. Broker-native XAUUSD sessions differ materially from HistData XAUUSD source-session candidates.
3. Broker-native XAUUSD has additional symbol-specific missingness relative to USDJPY.
4. The broker common timeline is constrained by XAUUSD availability.
5. The broker short window is useful for session inference but insufficient for research validation.
6. The 2026 broker window cannot prove historical broker equivalence for 2021-2025, but it does establish material mismatch risk.

### Broker H4/M1 loaded-shape inspection

Document:

C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_LOADED_SHAPE_INSPECTION.md

Commit:

6a48870 Document broker H4 M1 loaded shape inspection

Result:

1. USDJPY H4 was classified as H4-spaced.
2. XAUUSD H4 was classified as H4-spaced.
3. USDJPY H4 four-hour delta pct: 86.252441.
4. XAUUSD H4 four-hour delta pct: 86.173039.
5. USDJPY M1 one-minute delta pct: 99.911139.
6. XAUUSD M1 one-minute delta pct: 99.919359.

### Broker-only H4/M1 alignment diagnostic

Document:

C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_DIAGNOSTIC.md

Commit:

3cdeaca Document broker H4 M1 alignment diagnostic

Result:

1. Broker-native H4 aligned exactly with broker-native M1 aggregation on all full M1-covered H4 windows tested.
2. USDJPY compared windows: 338.
3. USDJPY matched bars: 338.
4. USDJPY mismatched bars: 0.
5. XAUUSD compared windows: 354.
6. XAUUSD matched bars: 354.
7. XAUUSD mismatched bars: 0.

### H4 construction decision checkpoint

Document:

C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_DECISION_CHECKPOINT.md

Commit:

b43dfe5 Document H4 construction decision checkpoint

Decision:

1. Broker-native H4 is accepted as the reference H4 signal timeframe for broker-aligned diagnostics.
2. HistData-built H4 is not accepted.
3. Broker H4 plus HistData M1 hybrid is not accepted.
4. HistData remains not accepted.
5. No long-history H017 validation source is currently accepted.

## Final current HistData path decision

HistData is rejected for H017 validation under current evidence.

The reason is not a single issue. It is the combination of:

1. Duplicate timestamp handling required special documented policy.
2. March-July 2023 is materially abnormal for both symbols.
3. Source-session reconciliation remains unresolved.
4. Broker mismatch assessment remains adverse.
5. Broker-native H4 is now the accepted H4 reference for broker-aligned diagnostics.
6. HistData-built H4 remains unaccepted.
7. Broker H4 plus HistData M1 hybrid remains unaccepted.
8. Using HistData for H017 would risk validating against a source whose session structure and execution bars may not represent the broker.

## Remaining allowed uses of HistData

HistData may still be used for explicitly planned diagnostics only.

Allowed examples:

1. Documenting why it was rejected for H017 validation.
2. Comparing session calendars for source-quality research.
3. Building small, temporary, read-only diagnostic summaries that do not claim H017 validation.
4. Preserving raw inventory metadata.

Not allowed:

1. H017 validation.
2. Strategy tuning.
3. Derived production datasets.
4. Derived H4 files for H017 validation.
5. Broker-H4 plus HistData-M1 hybrid validation.
6. Silent deduplication.
7. Raw file modification.
8. Raw file commits.

## Current project state after this decision

Accepted H4 reference for broker-aligned diagnostics:

Broker-native H4.

Accepted M1 source for broker-only alignment diagnostics:

Broker-native M1.

Accepted long-history M1 validation source:

None.

Accepted H017 validation source:

None.

HistData status:

Not accepted; rejected for H017 validation under current evidence; diagnostic-reference only.

H017 status:

Alive but not promotable.

Research validation status:

Blocked.

## Practical next paths

The project now has three practical paths:

1. Try to acquire longer broker-native M1 history from the broker or another broker-equivalent source.
2. Search for a better non-broker M1 source and subject it to the same source-acceptance discipline.
3. Pause long event-driven validation until better data exists, while keeping H017 as a non-promotable pipeline smoke result.

The preferred next data path is to pursue longer broker-native or broker-equivalent M1 data, because broker-native H4 is now the accepted signal-timeframe reference for broker-aligned diagnostics.

## Guardrails preserved

1. No HistData was loaded for this checkpoint.
2. H017 was not run.
3. No raw broker files were modified.
4. No raw HistData files were modified.
5. No derived data files were written.
6. HistData was not accepted as a research source.
7. No H017 validation source was accepted.
8. No live-trading readiness was claimed.
9. The current full-test anchor remains 514 passed.
