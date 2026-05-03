# HistData March-July 2023 Anomaly Investigation

Status: read-only diagnostic completed  
Phase: 3.26-h  
Source status after this diagnostic: not accepted as a research source  
H017 status after this diagnostic: not run, not promotable

## Purpose

This diagnostic investigated the elevated 2023 HistData missingness identified in the prior coverage and session analysis.

The focus window was:

- 2023-03-01 00:00 UTC through 2023-07-31 23:59 UTC

The goals were to determine whether the March-July 2023 issue appeared to be:

1. isolated to one symbol,
2. source-wide across both USDJPY and XAUUSD,
3. explainable by obvious weekend closure only,
4. potentially explainable by holidays or special closures,
5. a blocker for future HistData source acceptance.

This was a read-only diagnostic.

No raw files were modified.  
No derived files were written.  
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

Duplicate policy used:

- duplicate_policy="drop_exact"

This remains an explicit opt-in diagnostic setting. The default strict duplicate policy remains `reject`.

## Provisional Weekend Rule

The diagnostic used the same provisional weekend closure rule as the previous analysis:

- Friday 22:00 UTC through Sunday 21:59 UTC

This is only a provisional rule for missingness triage. It is not a final broker-session or source-session acceptance rule.

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

## Period Comparison

### USDJPY

| Period | Observed Bars | Missing Minutes | Non-Weekend Missing Minutes | Observed Percent |
| --- | ---: | ---: | ---: | ---: |
| 2023 Jan-Feb control | 57489 | 27471 | 5546 | 67.665960 |
| 2023 Mar-Jul focus | 110414 | 109906 | 51159 | 50.115287 |
| 2023 Aug-Dec control | 154993 | 65327 | 8097 | 70.349038 |
| 2021 Mar-Jul control | 154883 | 65437 | 9508 | 70.299110 |
| 2022 Mar-Jul control | 156248 | 64072 | 7172 | 70.918664 |
| 2024 Mar-Jul control | 156336 | 63984 | 7228 | 70.958606 |
| 2025 Mar-Jul control | 156520 | 63800 | 7081 | 71.042121 |

Interpretation:

USDJPY March-July 2023 coverage was materially worse than all same-month control periods. The focus period observed percent was about 50.12 percent, while the same-month controls were about 70.30 to 71.04 percent.

### XAUUSD

| Period | Observed Bars | Missing Minutes | Non-Weekend Missing Minutes | Observed Percent |
| --- | ---: | ---: | ---: | ---: |
| 2023 Jan-Feb control | 53660 | 31300 | 8800 | 63.159134 |
| 2023 Mar-Jul focus | 107267 | 113053 | 53653 | 48.686910 |
| 2023 Aug-Dec control | 147825 | 72495 | 13992 | 67.095588 |
| 2021 Mar-Jul control | 148608 | 71712 | 14772 | 67.450980 |
| 2022 Mar-Jul control | 148519 | 71801 | 13781 | 67.410585 |
| 2024 Mar-Jul control | 148505 | 71815 | 13855 | 67.404230 |
| 2025 Mar-Jul control | 148755 | 71565 | 13719 | 67.517702 |

Interpretation:

XAUUSD March-July 2023 coverage was materially worse than all same-month control periods. The focus period observed percent was about 48.69 percent, while the same-month controls were about 67.40 to 67.52 percent.

## Focus Window Monthly Counts

### USDJPY Observed Bars by Month

| Month | Observed Bars |
| --- | ---: |
| 2023-03 | 22987 |
| 2023-04 | 19952 |
| 2023-05 | 23229 |
| 2023-06 | 22033 |
| 2023-07 | 22213 |

### USDJPY Missing Minutes by Month

| Month | Total Missing Minutes | Non-Weekend Missing Minutes |
| --- | ---: | ---: |
| 2023-03 | 21653 | 11022 |
| 2023-04 | 23248 | 9868 |
| 2023-05 | 21411 | 10762 |
| 2023-06 | 21167 | 10298 |
| 2023-07 | 22427 | 9209 |

### USDJPY Non-Weekend Missing Gaps by Month

| Month | Non-Weekend Missing Gaps |
| --- | ---: |
| 2023-03 | 159 |
| 2023-04 | 132 |
| 2023-05 | 160 |
| 2023-06 | 166 |
| 2023-07 | 138 |

### XAUUSD Observed Bars by Month

| Month | Observed Bars |
| --- | ---: |
| 2023-03 | 22608 |
| 2023-04 | 19311 |
| 2023-05 | 22586 |
| 2023-06 | 21412 |
| 2023-07 | 21350 |

### XAUUSD Missing Minutes by Month

| Month | Total Missing Minutes | Non-Weekend Missing Minutes |
| --- | ---: | ---: |
| 2023-03 | 22032 | 11232 |
| 2023-04 | 23889 | 10509 |
| 2023-05 | 22054 | 11194 |
| 2023-06 | 21788 | 10808 |
| 2023-07 | 23290 | 9910 |

### XAUUSD Non-Weekend Missing Gaps by Month

| Month | Non-Weekend Missing Gaps |
| --- | ---: |
| 2023-03 | 125 |
| 2023-04 | 114 |
| 2023-05 | 135 |
| 2023-06 | 136 |
| 2023-07 | 125 |

## Cross-Symbol Missingness

For the March-July 2023 focus window:

- USDJPY_focus_missing_minutes: 109906
- XAUUSD_focus_missing_minutes: 113053
- overlapping_focus_missing_minutes: 89928
- USDJPY_only_focus_missing_minutes: 19978
- XAUUSD_only_focus_missing_minutes: 23125
- overlap_pct_of_USDJPY_focus_missing: 81.822648
- overlap_pct_of_XAUUSD_focus_missing: 79.544992

Interpretation:

The anomaly is strongly cross-symbol. Roughly 80 percent of each symbol's missing minutes overlapped with the other symbol. This suggests a source-wide or calendar/session-definition issue rather than a simple isolated instrument defect.

### Overlapping Missing Minutes by Month

| Month | Overlapping Missing Minutes |
| --- | ---: |
| 2023-03 | 18061 |
| 2023-04 | 19346 |
| 2023-05 | 17808 |
| 2023-06 | 16066 |
| 2023-07 | 18647 |

### Symbol-Specific Missing Minutes by Month

| Month | USDJPY-Only Missing Minutes | XAUUSD-Only Missing Minutes |
| --- | ---: | ---: |
| 2023-03 | 3592 | 3971 |
| 2023-04 | 3902 | 4543 |
| 2023-05 | 3603 | 4246 |
| 2023-06 | 5101 | 5722 |
| 2023-07 | 3780 | 4643 |

### Non-Weekend Cross-Symbol Missingness

- overlap_focus_non_weekend_missing_minutes: 31781
- USDJPY_only_focus_non_weekend_missing_minutes: 19378
- XAUUSD_only_focus_non_weekend_missing_minutes: 21872

Interpretation:

Even after applying the provisional weekend rule, the focus window still contains substantial non-weekend missingness. This remains a source-quality blocker.

## UTC Hour Clustering

### USDJPY Non-Weekend Missing-Minute UTC Hour Clusters

Top hours:

| UTC Hour | Missing Minutes |
| ---: | ---: |
| 17 | 4183 |
| 19 | 3841 |
| 18 | 3669 |
| 11 | 3420 |
| 09 | 3365 |
| 14 | 3365 |
| 12 | 3360 |
| 16 | 3320 |
| 07 | 3240 |
| 08 | 3180 |

### XAUUSD Non-Weekend Missing-Minute UTC Hour Clusters

Top hours:

| UTC Hour | Missing Minutes |
| ---: | ---: |
| 17 | 6300 |
| 18 | 3673 |
| 19 | 3666 |
| 09 | 3660 |
| 11 | 3600 |
| 07 | 3420 |
| 12 | 3420 |
| 14 | 3391 |
| 16 | 3308 |
| 15 | 3183 |

### Overlapping Non-Weekend Missing-Minute UTC Hour Clusters

Top hours:

| UTC Hour | Missing Minutes |
| ---: | ---: |
| 17 | 4123 |
| 19 | 2647 |
| 18 | 2467 |
| 11 | 2100 |
| 09 | 1985 |
| 12 | 1980 |
| 16 | 1818 |
| 14 | 1803 |
| 07 | 1740 |
| 15 | 1688 |

Interpretation:

The missingness clusters heavily around 17:00 UTC, 18:00 UTC, and 19:00 UTC, but it is not confined to the previously identified XAUUSD 17:00 UTC metals break. The focus-period anomaly also affects USDJPY and appears across many trading hours.

## Largest Non-Weekend Gaps

### USDJPY Largest Focus-Window Non-Weekend Gaps

Largest observed gaps included:

| Start UTC | End UTC | Duration Minutes | Start Hour UTC |
| --- | --- | ---: | ---: |
| 2023-04-06 20:00 | 2023-04-07 21:59 | 1560 | 20 |
| 2023-03-17 15:00 | 2023-03-17 21:59 | 420 | 15 |
| 2023-03-24 15:00 | 2023-03-24 21:59 | 420 | 15 |
| 2023-04-28 15:00 | 2023-04-28 21:59 | 420 | 15 |
| 2023-06-09 15:00 | 2023-06-09 21:59 | 420 | 15 |
| 2023-07-28 15:00 | 2023-07-28 21:59 | 420 | 15 |
| 2023-03-10 16:00 | 2023-03-10 21:59 | 360 | 16 |
| 2023-03-31 16:00 | 2023-03-31 21:59 | 360 | 16 |
| 2023-04-21 16:00 | 2023-04-21 21:59 | 360 | 16 |
| 2023-05-05 16:00 | 2023-05-05 21:59 | 360 | 16 |

### XAUUSD Largest Focus-Window Non-Weekend Gaps

Largest observed gaps included:

| Start UTC | End UTC | Duration Minutes | Start Hour UTC |
| --- | --- | ---: | ---: |
| 2023-04-06 16:59 | 2023-04-07 21:59 | 1741 | 16 |
| 2023-03-17 14:00 | 2023-03-17 21:59 | 480 | 14 |
| 2023-03-24 15:00 | 2023-03-24 21:59 | 420 | 15 |
| 2023-04-21 15:00 | 2023-04-21 21:59 | 420 | 15 |
| 2023-05-26 15:00 | 2023-05-26 21:59 | 420 | 15 |
| 2023-03-03 16:00 | 2023-03-03 21:59 | 360 | 16 |
| 2023-03-10 16:00 | 2023-03-10 21:59 | 360 | 16 |
| 2023-04-28 16:00 | 2023-04-28 21:59 | 360 | 16 |
| 2023-05-05 16:00 | 2023-05-05 21:59 | 360 | 16 |
| 2023-05-19 16:00 | 2023-05-19 21:59 | 360 | 16 |

Interpretation:

Many of the largest gaps end at 21:59 UTC, immediately before the provisional weekend closure boundary. This pattern may indicate vendor session-definition artifacts or early-close handling, but it is not automatically acceptable.

The April 6-7 gap is especially large and should be treated as a holiday or special-closure candidate requiring explicit classification before any source acceptance decision.

## Daily Observed Bar Issues

### USDJPY

Zero-bar weekdays in the focus window:

- 2023-04-07: 0 bars

Lowest nonzero weekdays below 1000 bars included:

| Date | Observed Bars |
| --- | ---: |
| 2023-03-24 | 600 |
| 2023-05-26 | 659 |
| 2023-03-17 | 660 |
| 2023-03-03 | 660 |
| 2023-03-31 | 660 |
| 2023-05-05 | 660 |
| 2023-04-21 | 660 |
| 2023-03-10 | 660 |
| 2023-05-19 | 660 |
| 2023-05-12 | 660 |

### XAUUSD

Zero-bar weekdays in the focus window:

- 2023-04-07: 0 bars

Lowest nonzero weekdays below 1000 bars included:

| Date | Observed Bars |
| --- | ---: |
| 2023-03-10 | 600 |
| 2023-03-17 | 600 |
| 2023-03-24 | 600 |
| 2023-03-03 | 660 |
| 2023-04-21 | 660 |
| 2023-05-19 | 660 |
| 2023-05-26 | 660 |
| 2023-05-05 | 660 |
| 2023-06-02 | 660 |
| 2023-04-06 | 719 |

Interpretation:

The focus window contains repeated low-bar weekdays, especially Fridays. These may represent early closes or source session truncation, but the same pattern must be reconciled against an explicit holiday/session calendar and against the intended broker execution environment before HistData can be accepted.

## Diagnostic Conclusions

### What this diagnostic supports

1. March-July 2023 is materially abnormal relative to same-month control periods from 2021, 2022, 2024, and 2025.
2. The anomaly affects both USDJPY and XAUUSD.
3. The anomaly is strongly cross-symbol, with about 80 percent missing-minute overlap.
4. The problem is not explained by the provisional weekend rule alone.
5. The problem is not limited to the already documented XAUUSD 17:00 UTC session break.
6. Many large gaps resemble early-close or session-definition behavior, especially Friday gaps ending at 21:59 UTC.
7. Some gaps may be holiday or special-closure candidates, but they have not yet been explicitly classified.
8. HistData remains blocked pending session reconciliation, holiday classification, and broker mismatch assessment.

### What this diagnostic does not prove

1. It does not prove HistData is unusable.
2. It does not prove the gaps are vendor errors.
3. It does not prove the gaps are valid market closures.
4. It does not prove broker equivalence with Exness.
5. It does not accept XAUUSD 17:00 UTC behavior as broker-equivalent.
6. It does not authorize H017 validation on HistData.
7. It does not authorize derived HistData file creation.

## Current Decision

HistData is still not accepted as a research source.

The March-July 2023 anomaly remains a major unresolved source-quality blocker.

Before HistData can be accepted, the project still needs:

1. explicit holiday and special-closure classification,
2. source-session reconciliation,
3. broker mismatch assessment versus Exness,
4. an H4 construction decision,
5. a final HistData source acceptance or rejection decision.

## Safety Confirmation

- raw_files_modified: False
- derived_files_written: False
- H017_run: False
- HistData_accepted_as_research_source: False
- diagnostic_complete: True
