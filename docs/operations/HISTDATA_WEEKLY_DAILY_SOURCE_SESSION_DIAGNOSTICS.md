# HistData Weekly and Daily Source-Session Diagnostics

Status: read-only diagnostic completed  
Phase: 3.26-l  
Source status after this diagnostic: not accepted as a research source  
H017 status after this diagnostic: not run, not promotable

## Purpose

This diagnostic inferred provisional weekly and daily source-session behavior from the HistData M1 files.

The diagnostic followed the plan documented in:

- docs/operations/HISTDATA_SOURCE_SESSION_RECONCILIATION_PLAN.md

The goals were to:

1. infer weekly session templates for USDJPY and XAUUSD,
2. quantify Sunday open behavior,
3. quantify Friday close behavior,
4. quantify daily full-hour missing candidates,
5. compare March-July 2023 against the same months in other years,
6. keep all labels provisional,
7. avoid H017,
8. avoid derived-data writes,
9. keep HistData unaccepted.

This was a read-only diagnostic.

No raw files were modified.  
No derived files were written.  
No reusable code was added.  
H017 was not run.  
HistData was not accepted.

## Inputs

Raw HistData files inspected:

- C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Important note:

The folder name `dukascopy_samples` is misleading. These two files are HistData files, not Dukascopy files.

Loader used:

- quantcore.data.histdata_loader.load_histdata_m1_csv

Observed loader API:

- load_histdata_m1_csv(path: str | Path, *, source_tz: str = "UTC", duplicate_policy: DuplicatePolicy = "reject") -> HistDataM1LoadResult

Diagnostic duplicate policy:

- duplicate_policy="drop_exact"

This remains an explicit opt-in diagnostic setting. The default strict policy remains `reject`.

## Loader Results

### USDJPY

- n_input_rows: 1808731
- n_bars: 1808431
- earliest_utc: 2021-01-03 17:00:00+00:00
- latest_utc: 2025-12-31 16:57:00+00:00
- duplicate_policy: drop_exact
- n_duplicate_rows_removed: 300
- n_duplicate_timestamp_values: 300

### XAUUSD

- n_input_rows: 1726549
- n_bars: 1726249
- earliest_utc: 2021-01-03 18:00:00+00:00
- latest_utc: 2025-12-31 16:57:00+00:00
- duplicate_policy: drop_exact
- n_duplicate_rows_removed: 300
- n_duplicate_timestamp_values: 300

## Important Diagnostic Caveat

The diagnostic counted full missing-hour candidates by UTC hour.

These full missing-hour counts include weekend and session-closure periods. Therefore:

1. USDJPY full `17:00 UTC` missing-hour counts in normal years should not be interpreted as a USDJPY daily break by themselves.
2. XAUUSD full `17:00 UTC` missing-hour counts are much more suggestive of a daily metals break because the counts are close to the number of calendar days in the March-July window.
3. All session labels remain provisional.
4. Broker equivalence has not been established.

## March-July Source-Session Comparison

### USDJPY

| Year | Observed Percent | Observed Bars | Missing Minutes | Full Missing 17:00 UTC Days | Full Missing-Hour Days All |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2021 | 70.299110 | 154883 | 65437 | 45 | 1060 |
| 2022 | 70.918664 | 156248 | 64072 | 44 | 1057 |
| 2023 | 50.115287 | 110414 | 109906 | 104 | 1828 |
| 2024 | 70.958606 | 156336 | 63984 | 44 | 1057 |
| 2025 | 71.042121 | 156520 | 63800 | 43 | 1050 |

Interpretation:

USDJPY March-July 2023 remains materially abnormal.

The 2023 observed percent fell to about 50.12 percent, while same-month control years were about 70.30 to 71.04 percent.

The full missing-hour candidate count also increased sharply in 2023:

- normal control range: 1050 to 1060
- 2023: 1828

This supports the earlier conclusion that March-July 2023 is not normal coverage variation.

### XAUUSD

| Year | Observed Percent | Observed Bars | Missing Minutes | Full Missing 17:00 UTC Days | Full Missing-Hour Days All |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2021 | 67.450980 | 148608 | 71712 | 143 | 1195 |
| 2022 | 67.410585 | 148519 | 71801 | 143 | 1195 |
| 2023 | 48.686910 | 107267 | 113053 | 147 | 1883 |
| 2024 | 67.404230 | 148505 | 71815 | 139 | 1195 |
| 2025 | 67.517702 | 148755 | 71565 | 138 | 1191 |

Interpretation:

XAUUSD March-July 2023 remains materially abnormal.

The 2023 observed percent fell to about 48.69 percent, while same-month control years were about 67.40 to 67.52 percent.

The full missing-hour candidate count also increased sharply in 2023:

- normal control range: 1191 to 1195
- 2023: 1883

The full `17:00 UTC` missing-hour count remained high across all years, supporting the existing XAUUSD daily break candidate.

## USDJPY Sunday Open Behavior

### 2021

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 16:00 | 3 |
| 17:00 | 41 |
| 17:01 | 1 |
| 17:02 | 1 |
| 17:03 | 4 |
| 17:04 | 1 |
| 17:05 | 1 |

### 2022

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 16:00 | 2 |
| 16:04 | 1 |
| 17:00 | 35 |
| 17:01 | 1 |
| 17:02 | 1 |
| 17:04 | 3 |
| 17:05 | 4 |
| 17:06 | 1 |
| 17:12 | 2 |
| 17:13 | 1 |
| 17:30 | 1 |

### 2023

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 16:00 | 2 |
| 16:01 | 1 |
| 17:00 | 26 |
| 17:01 | 3 |
| 17:03 | 1 |
| 17:04 | 3 |
| 17:05 | 1 |
| 18:00 | 11 |
| 18:32 | 1 |
| 19:00 | 3 |

### 2024

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 16:00 | 2 |
| 16:03 | 1 |
| 16:04 | 1 |
| 17:00 | 27 |
| 17:01 | 2 |
| 17:02 | 3 |
| 17:03 | 2 |
| 17:04 | 10 |
| 17:05 | 3 |
| 17:06 | 1 |

### 2025

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 16:00 | 4 |
| 17:00 | 24 |
| 17:01 | 6 |
| 17:02 | 2 |
| 17:04 | 15 |
| 17:09 | 1 |

USDJPY interpretation:

USDJPY generally opens on Sunday around `17:00 UTC`, with some `16:00 UTC` observations and some later delayed opens.

The 2023 Sunday open distribution is more dispersed than normal control years, including more `18:00 UTC` and `19:00 UTC` opens.

This is another sign that 2023 has abnormal source-session behavior.

## USDJPY Friday Close Behavior

### 2021

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 15:59 | 3 |
| 16:58 | 3 |
| 16:59 | 46 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2021-03-19 | 00:00 | 15:59 | 959 |
| 2021-03-26 | 00:00 | 15:59 | 960 |
| 2021-11-05 | 00:00 | 15:59 | 960 |

### 2022

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 15:59 | 3 |
| 16:58 | 2 |
| 16:59 | 47 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2022-11-04 | 00:00 | 15:59 | 956 |
| 2022-03-18 | 00:00 | 15:59 | 959 |
| 2022-03-25 | 00:00 | 15:59 | 960 |

### 2023

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 14:59 | 5 |
| 15:59 | 10 |
| 16:58 | 2 |
| 16:59 | 34 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2023-03-24 | 00:00 | 14:59 | 600 |
| 2023-02-24 | 00:00 | 16:59 | 659 |
| 2023-05-26 | 00:00 | 15:59 | 659 |
| 2023-03-03 | 00:00 | 16:59 | 660 |
| 2023-03-10 | 00:00 | 15:59 | 660 |
| 2023-03-17 | 00:00 | 14:59 | 660 |
| 2023-03-31 | 00:00 | 15:59 | 660 |
| 2023-04-21 | 00:00 | 15:59 | 660 |
| 2023-04-28 | 00:00 | 14:59 | 660 |
| 2023-05-05 | 00:00 | 15:59 | 660 |
| 2023-05-12 | 00:00 | 15:59 | 660 |
| 2023-05-19 | 00:00 | 15:59 | 660 |

### 2024

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 15:59 | 4 |
| 16:59 | 48 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2024-03-29 | 00:00 | 15:59 | 950 |
| 2024-03-22 | 00:00 | 15:59 | 959 |
| 2024-03-15 | 00:00 | 15:59 | 960 |
| 2024-11-01 | 00:00 | 15:59 | 960 |

### 2025

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 15:59 | 4 |
| 16:59 | 48 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2025-03-14 | 00:00 | 15:59 | 959 |
| 2025-03-21 | 00:00 | 15:59 | 960 |
| 2025-03-28 | 00:00 | 15:59 | 960 |
| 2025-10-31 | 00:00 | 15:59 | 960 |

USDJPY interpretation:

USDJPY Friday closes are usually around `16:59 UTC`, with recurring `15:59 UTC` early-close-like observations.

The 2023 Friday close behavior is materially more abnormal:

1. more `14:59 UTC` closes,
2. more `15:59 UTC` closes,
3. lower Friday bar counts,
4. repeated 600 to 660 bar Fridays in March-May.

This supports the conclusion that March-July 2023 has abnormal source-session behavior.

## XAUUSD Sunday Open Behavior

### 2021

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 17:00 | 3 |
| 18:00 | 49 |

### 2022

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 17:00 | 3 |
| 18:00 | 47 |
| 18:03 | 1 |

### 2023

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 17:00 | 3 |
| 18:00 | 32 |
| 19:00 | 12 |
| 20:00 | 3 |

### 2024

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 17:00 | 4 |
| 18:00 | 47 |
| 18:01 | 1 |

### 2025

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 17:00 | 4 |
| 18:00 | 46 |
| 18:03 | 1 |
| 18:05 | 1 |

XAUUSD interpretation:

XAUUSD generally opens on Sunday around `18:00 UTC`, with some `17:00 UTC` observations.

The 2023 Sunday open distribution is more dispersed, with `19:00 UTC` and `20:00 UTC` openings appearing more often than in control years.

This supports the conclusion that 2023 has abnormal source-session behavior.

## XAUUSD Friday Close Behavior

### 2021

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 13:43 | 1 |
| 15:59 | 3 |
| 16:58 | 1 |
| 16:59 | 45 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2021-11-26 | 00:00 | 13:43 | 824 |
| 2021-03-19 | 00:00 | 15:59 | 960 |
| 2021-03-26 | 00:00 | 15:59 | 960 |
| 2021-11-05 | 00:00 | 15:59 | 960 |

### 2022

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 13:43 | 1 |
| 15:59 | 3 |
| 16:57 | 1 |
| 16:58 | 1 |
| 16:59 | 45 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2022-11-25 | 00:00 | 13:43 | 824 |
| 2022-11-04 | 00:00 | 15:59 | 956 |
| 2022-03-18 | 00:00 | 15:59 | 960 |
| 2022-03-25 | 00:00 | 15:59 | 960 |

### 2023

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 12:43 | 1 |
| 13:59 | 1 |
| 14:59 | 3 |
| 15:59 | 7 |
| 16:57 | 1 |
| 16:58 | 1 |
| 16:59 | 37 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2023-03-10 | 00:00 | 15:59 | 600 |
| 2023-03-17 | 00:00 | 13:59 | 600 |
| 2023-03-24 | 00:00 | 14:59 | 600 |
| 2023-02-24 | 00:00 | 16:59 | 659 |
| 2023-03-03 | 00:00 | 15:59 | 660 |
| 2023-04-21 | 00:00 | 14:59 | 660 |
| 2023-05-05 | 00:00 | 15:59 | 660 |
| 2023-05-19 | 00:00 | 15:59 | 660 |
| 2023-05-26 | 00:00 | 14:59 | 660 |
| 2023-06-02 | 00:00 | 15:59 | 660 |
| 2023-07-07 | 00:00 | 16:59 | 719 |
| 2023-03-31 | 00:00 | 16:59 | 720 |

### 2024

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 12:59 | 1 |
| 14:43 | 1 |
| 15:59 | 3 |
| 16:59 | 46 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2024-01-12 | 00:00 | 12:59 | 780 |
| 2024-11-29 | 00:00 | 14:43 | 884 |
| 2024-03-15 | 00:00 | 15:59 | 960 |
| 2024-03-22 | 00:00 | 15:59 | 960 |
| 2024-11-01 | 00:00 | 15:59 | 960 |

### 2025

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 10:59 | 1 |
| 12:58 | 1 |
| 14:43 | 1 |
| 15:59 | 4 |
| 16:59 | 44 |

Lowest observed Friday bar counts included:

| Date | First | Last | Bars |
| --- | --- | --- | ---: |
| 2025-12-05 | 00:00 | 10:59 | 660 |
| 2025-07-04 | 00:00 | 12:58 | 779 |
| 2025-11-28 | 00:00 | 14:43 | 870 |
| 2025-03-14 | 00:00 | 15:59 | 960 |
| 2025-03-21 | 00:00 | 15:59 | 960 |
| 2025-03-28 | 00:00 | 15:59 | 960 |
| 2025-10-31 | 00:00 | 15:59 | 960 |

XAUUSD interpretation:

XAUUSD Friday closes are usually around `16:59 UTC`, with recurring early-close-like outliers.

The 2023 Friday close behavior is materially more abnormal than normal years:

1. more early Friday closes,
2. lower Friday observed bar counts,
3. repeated 600 to 720 bar Fridays in March-July.

This supports the conclusion that March-July 2023 is abnormal and not explained by the normal XAUUSD `17:00 UTC` daily break alone.

## XAUUSD 17:00 UTC Break Evidence

The March-July full `17:00 UTC` missing-hour counts were:

| Year | Full 17:00 UTC Missing-Hour Days |
| --- | ---: |
| 2021 | 143 |
| 2022 | 143 |
| 2023 | 147 |
| 2024 | 139 |
| 2025 | 138 |

Interpretation:

XAUUSD has a strong recurring `17:00 UTC` full missing-hour signature.

This supports the prior conclusion that the `17:00 UTC` gap is a metals daily session-break candidate.

However:

1. this is still a source-session inference,
2. it is not yet broker-equivalent,
3. it does not explain the full March-July 2023 anomaly,
4. it does not authorize HistData acceptance,
5. it does not authorize H017 validation.

## All-Years Weekday-Hour Counts

### USDJPY Observed Weekday-Hour Counts

Top observed weekday-hour counts included:

| Weekday | UTC Hour | Count |
| ---: | ---: | ---: |
| 1 | 03 | 15660 |
| 1 | 02 | 15659 |
| 1 | 04 | 15659 |
| 0 | 20 | 15656 |
| 0 | 21 | 15656 |
| 0 | 22 | 15644 |
| 1 | 01 | 15638 |
| 1 | 00 | 15634 |
| 0 | 23 | 15633 |
| 1 | 20 | 15593 |
| 2 | 02 | 15593 |
| 2 | 21 | 15588 |

### USDJPY Missing Weekday-Hour Counts

Top missing weekday-hour counts included:

| Weekday | UTC Hour | Count |
| ---: | ---: | ---: |
| 5 | 06 | 15600 |
| 5 | 05 | 15600 |
| 5 | 04 | 15600 |
| 5 | 03 | 15600 |
| 5 | 02 | 15600 |
| 5 | 01 | 15600 |
| 5 | 08 | 15600 |
| 6 | 08 | 15600 |
| 6 | 09 | 15600 |
| 6 | 10 | 15600 |
| 6 | 11 | 15600 |
| 6 | 12 | 15600 |

### XAUUSD Observed Weekday-Hour Counts

Top observed weekday-hour counts included:

| Weekday | UTC Hour | Count |
| ---: | ---: | ---: |
| 0 | 20 | 15660 |
| 0 | 21 | 15660 |
| 0 | 22 | 15660 |
| 1 | 01 | 15660 |
| 1 | 02 | 15660 |
| 1 | 03 | 15660 |
| 1 | 00 | 15659 |
| 0 | 23 | 15659 |
| 1 | 04 | 15659 |
| 1 | 21 | 15540 |
| 1 | 20 | 15540 |
| 1 | 22 | 15540 |

### XAUUSD Missing Weekday-Hour Counts

Top missing weekday-hour counts included:

| Weekday | UTC Hour | Count |
| ---: | ---: | ---: |
| 5 | 01 | 15600 |
| 5 | 00 | 15600 |
| 6 | 08 | 15600 |
| 6 | 09 | 15600 |
| 6 | 10 | 15600 |
| 6 | 11 | 15600 |
| 6 | 12 | 15600 |
| 6 | 13 | 15600 |
| 6 | 14 | 15600 |
| 6 | 15 | 15600 |
| 6 | 16 | 15600 |
| 6 | 01 | 15600 |

Interpretation:

The all-years weekday-hour counts support the existence of stable weekly closure patterns. They do not by themselves prove broker equivalence.

## Diagnostic Conclusions

### What this diagnostic supports

1. USDJPY has a consistent source-session pattern with Sunday opens mostly around `17:00 UTC`.
2. USDJPY has Friday closes mostly around `16:59 UTC`, with recurring early-close-like outliers.
3. XAUUSD has a consistent source-session pattern with Sunday opens mostly around `18:00 UTC`.
4. XAUUSD has Friday closes mostly around `16:59 UTC`, with recurring early-close-like outliers.
5. XAUUSD has a strong recurring `17:00 UTC` full missing-hour signature.
6. March-July 2023 remains materially abnormal for both symbols.
7. The 2023 abnormality appears in observed coverage, Friday close behavior, Sunday open dispersion, and full missing-hour counts.
8. The 2023 abnormality is not explained solely by normal weekend closure or the XAUUSD `17:00 UTC` break.

### What this diagnostic does not prove

1. It does not prove HistData is acceptable.
2. It does not prove HistData is unusable.
3. It does not prove the XAUUSD `17:00 UTC` break is broker-equivalent.
4. It does not prove Friday early-close-like gaps are broker-equivalent.
5. It does not classify holidays or special closures.
6. It does not assess broker mismatch versus Exness.
7. It does not decide H4 construction rules.
8. It does not authorize derived HistData file creation.
9. It does not authorize H017 validation on HistData.

## Current Decision

HistData remains not accepted as a research source.

The March-July 2023 anomaly remains unresolved.

No H017 validation on HistData is authorized.

No derived HistData files are authorized.

## Recommended Next Sub-Phase

Recommended next sub-phase:

Phase 3.26-m - Broker short-window session diagnostic plan

Purpose:

1. define how to use existing broker-native MT5 M1 exports to infer current Exness session behavior,
2. compare broker-native USDJPY and XAUUSD session behavior against HistData source-session candidates,
3. identify what can and cannot be concluded from the short 2026 broker window,
4. keep analysis read-only,
5. avoid H017,
6. avoid derived-data writes,
7. keep HistData unaccepted.

This should be a documentation plan first before any broker/session diagnostic.

## Safety Confirmation

- raw_files_modified: False
- derived_files_written: False
- reusable_code_written: False
- H017_run: False
- HistData_accepted_as_research_source: False
- session_labels_are_provisional: True
- diagnostic_complete: True
