# HistData March-July 2023 Gap Candidate Classification

Status: read-only diagnostic completed  
Phase: 3.26-j  
Source status after this diagnostic: not accepted as a research source  
H017 status after this diagnostic: not run, not promotable

## Purpose

This diagnostic applied provisional candidate labels to March-July 2023 HistData missing gaps.

The classification was based on the plan documented in:

- docs/operations/HISTDATA_HOLIDAY_SPECIAL_CLOSURE_CLASSIFICATION_PLAN.md

The focus window was:

- 2023-03-01 00:00 UTC through 2023-07-31 23:59 UTC

This diagnostic was designed to separate missingness candidates into broad provisional buckets:

1. provisional weekend,
2. daily session-break candidate,
3. holiday full-close candidate,
4. holiday early-close candidate,
5. cross-symbol source-outage candidate,
6. symbol-specific source-defect candidate,
7. suspicious unclassified gap.

All labels in this diagnostic are provisional candidate labels.

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

## Provisional Classification Rules Used

The diagnostic used these provisional rules.

### Provisional Weekend

A missing gap was labelled:

- NORMAL_WEEKEND_PROVISIONAL

when all minutes in the gap fell inside the provisional weekend closure rule:

- Friday 22:00 UTC through Sunday 21:59 UTC

This is still a triage rule only.

### Holiday Full-Close Candidate

A gap was labelled:

- HOLIDAY_FULL_CLOSE_CANDIDATE

when the gap contained a weekday where both USDJPY and XAUUSD had zero observed bars.

This is not an acceptance label. It only identifies a candidate for explicit holiday review.

### Daily Session-Break Candidate

A gap was labelled:

- DAILY_SESSION_BREAK_CANDIDATE

only for XAUUSD when all non-weekend missing minutes were inside one day's 17:00 UTC hour and the gap length was no more than 60 non-weekend minutes.

This is not broker-equivalence acceptance.

### Holiday Early-Close Candidate

A gap was labelled:

- HOLIDAY_EARLY_CLOSE_CANDIDATE

when the non-weekend portion:

1. occurred on a Friday,
2. ended at 21:59 UTC,
3. started before the provisional weekend boundary,
4. lasted at least 180 non-weekend minutes.

This identifies early-close-like behavior but does not prove a real market holiday or broker-equivalent session.

### Cross-Symbol Source-Outage Candidate

A gap was labelled:

- CROSS_SYMBOL_SOURCE_OUTAGE_CANDIDATE

when:

1. the non-weekend portion was at least 60 minutes,
2. at least 80 percent of that non-weekend portion overlapped with missing minutes in the other symbol.

This is a source-wide candidate label, not proof of a vendor outage.

### Symbol-Specific Source-Defect Candidate

A gap was labelled:

- SYMBOL_SPECIFIC_SOURCE_DEFECT_CANDIDATE

when:

1. the non-weekend portion was at least 60 minutes,
2. no more than 20 percent of that non-weekend portion overlapped with missing minutes in the other symbol.

This is a symbol-specific defect candidate label, not a final defect finding.

### Suspicious Unclassified Gap

A gap was labelled:

- SUSPICIOUS_UNCLASSIFIED_GAP

when it did not fit the above provisional candidate rules.

Unclassified suspicious gaps remain blockers until reviewed or until a conservative threshold is explicitly defined.

No such threshold has been accepted.

## Zero-Bar Weekday Findings

In the March-July 2023 focus window:

### USDJPY

- zero-bar weekdays: 1
- date:
  - 2023-04-07

### XAUUSD

- zero-bar weekdays: 1
- date:
  - 2023-04-07

### Both Symbols

- zero-bar weekdays shared by both symbols: 1
- date:
  - 2023-04-07

Interpretation:

2023-04-07 is a holiday full-close candidate. It is not yet accepted as a valid market closure for this project until explicitly classified.

## Candidate Category Summary

### USDJPY

| Category | Gaps | Total Minutes | Non-Weekend Minutes | Overlap Non-Weekend Minutes | Manual Review Gaps |
| --- | ---: | ---: | ---: | ---: | ---: |
| CROSS_SYMBOL_SOURCE_OUTAGE_CANDIDATE | 313 | 19741 | 19741 | 19741 | 313 |
| SYMBOL_SPECIFIC_SOURCE_DEFECT_CANDIDATE | 251 | 15426 | 15426 | 28 | 251 |
| HOLIDAY_EARLY_CLOSE_CANDIDATE | 21 | 62291 | 7440 | 6900 | 21 |
| SUSPICIOUS_UNCLASSIFIED_GAP | 169 | 6992 | 6992 | 3552 | 169 |
| HOLIDAY_FULL_CLOSE_CANDIDATE | 1 | 4260 | 1560 | 1560 | 1 |
| NORMAL_WEEKEND_PROVISIONAL | 55 | 1196 | 0 | 0 | 0 |

Interpretation:

The candidate classification explains some recurring early-close-like behavior, but USDJPY still has substantial cross-symbol, symbol-specific, and suspicious unclassified missingness.

### XAUUSD

| Category | Gaps | Total Minutes | Non-Weekend Minutes | Overlap Non-Weekend Minutes | Manual Review Gaps |
| --- | ---: | ---: | ---: | ---: | ---: |
| CROSS_SYMBOL_SOURCE_OUTAGE_CANDIDATE | 242 | 15360 | 15360 | 15360 | 242 |
| SUSPICIOUS_UNCLASSIFIED_GAP | 123 | 14223 | 14223 | 6986 | 123 |
| SYMBOL_SPECIFIC_SOURCE_DEFECT_CANDIDATE | 219 | 13389 | 13389 | 17 | 219 |
| HOLIDAY_EARLY_CLOSE_CANDIDATE | 21 | 63480 | 7200 | 6901 | 21 |
| HOLIDAY_FULL_CLOSE_CANDIDATE | 1 | 4441 | 1741 | 1564 | 1 |
| DAILY_SESSION_BREAK_CANDIDATE | 29 | 1740 | 1740 | 953 | 29 |
| NORMAL_WEEKEND_PROVISIONAL | 7 | 420 | 0 | 0 | 0 |

Interpretation:

The XAUUSD 17:00 UTC daily-break candidate bucket exists but is small relative to the remaining suspicious, cross-symbol, and symbol-specific buckets. Therefore the March-July 2023 anomaly is not explained by the XAUUSD daily break alone.

## Largest Holiday Full-Close Candidates

### USDJPY

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| 2023-04-06 20:00 | 2023-04-09 18:59 | 4260 | 1560 | 1560 | 1.000 |

### XAUUSD

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| 2023-04-06 16:59 | 2023-04-09 18:59 | 4441 | 1741 | 1564 | 0.898 |

Interpretation:

The April 6-9 gap around the 2023-04-07 zero-bar weekday is a strong holiday full-close candidate. It still requires explicit holiday/session classification before acceptance.

## Friday Early-Close-Like Candidate Comparison

Definition used:

- same-Friday missing gap ending at 21:59 UTC,
- at least 180 non-weekend missing minutes.

These are candidate counts only, not acceptance labels.

### USDJPY March-July Early-Close-Like Candidates by Year

| Year | Gaps | Non-Weekend Minutes |
| --- | ---: | ---: |
| 2021 | 22 | 6720 |
| 2022 | 22 | 6721 |
| 2023 | 21 | 7440 |
| 2024 | 22 | 6780 |
| 2025 | 21 | 6480 |

### XAUUSD March-July Early-Close-Like Candidates by Year

| Year | Gaps | Non-Weekend Minutes |
| --- | ---: | ---: |
| 2021 | 21 | 6420 |
| 2022 | 21 | 6420 |
| 2023 | 21 | 7200 |
| 2024 | 21 | 6420 |
| 2025 | 20 | 6421 |

Interpretation:

Friday early-close-like gaps are recurring across years. This suggests a stable vendor/session pattern rather than a purely 2023-only event.

However, 2023 has somewhat elevated non-weekend minutes in this bucket for both symbols. This pattern still requires source-session and broker-session reconciliation.

## Representative Early-Close Candidates

### USDJPY Examples

Large examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-03-24 15:00 | 2023-03-26 17:59 | 3060 | 420 | 1.000 |
| 2023-04-28 15:00 | 2023-04-30 17:59 | 3060 | 420 | 0.857 |
| 2023-06-09 15:00 | 2023-06-11 17:59 | 3060 | 420 | 0.714 |
| 2023-07-28 15:00 | 2023-07-30 16:59 | 3000 | 420 | 0.714 |
| 2023-03-17 15:00 | 2023-03-19 16:00 | 2941 | 420 | 1.000 |

### XAUUSD Examples

Large examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-03-17 14:00 | 2023-03-19 16:59 | 3060 | 480 | 0.875 |
| 2023-04-21 15:00 | 2023-04-23 18:59 | 3120 | 420 | 0.857 |
| 2023-05-26 15:00 | 2023-05-28 18:59 | 3120 | 420 | 0.860 |
| 2023-03-24 15:00 | 2023-03-26 17:59 | 3060 | 420 | 1.000 |
| 2023-05-05 16:00 | 2023-05-07 19:59 | 3120 | 360 | 1.000 |

Interpretation:

Many early-close-like candidates span a Friday-to-Sunday missing interval. Their total duration includes weekend minutes, while the non-weekend count isolates the pre-weekend early-close portion.

These patterns may reflect HistData session definitions. They are not automatically broker-equivalent.

## Cross-Symbol Source-Outage Candidates

### USDJPY

- gaps: 313
- total_minutes: 19741
- non_weekend_minutes: 19741
- overlap_non_weekend_minutes: 19741

Representative examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-03-01 14:00 | 2023-03-01 15:59 | 120 | 120 | 1.000 |
| 2023-03-07 15:00 | 2023-03-07 16:59 | 120 | 120 | 1.000 |
| 2023-03-14 16:00 | 2023-03-14 17:59 | 120 | 120 | 1.000 |
| 2023-03-15 08:00 | 2023-03-15 09:59 | 120 | 120 | 1.000 |
| 2023-03-21 16:00 | 2023-03-21 17:59 | 120 | 120 | 1.000 |

### XAUUSD

- gaps: 242
- total_minutes: 15360
- non_weekend_minutes: 15360
- overlap_non_weekend_minutes: 15360

Representative examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-03-01 14:00 | 2023-03-01 15:59 | 120 | 120 | 1.000 |
| 2023-03-15 08:00 | 2023-03-15 09:59 | 120 | 120 | 1.000 |
| 2023-03-21 16:00 | 2023-03-21 17:59 | 120 | 120 | 1.000 |
| 2023-03-27 12:00 | 2023-03-27 13:59 | 120 | 120 | 1.000 |
| 2023-03-30 16:00 | 2023-03-30 17:59 | 120 | 120 | 1.000 |

Interpretation:

The cross-symbol candidate bucket is large and important. These gaps are not explained by XAUUSD-only session behavior. They remain a major source-quality concern.

## Symbol-Specific Source-Defect Candidates

### USDJPY

- gaps: 251
- total_minutes: 15426
- non_weekend_minutes: 15426
- overlap_non_weekend_minutes: 28

Representative examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-03-28 12:00 | 2023-03-28 13:59 | 120 | 120 | 0.000 |
| 2023-03-30 07:00 | 2023-03-30 08:59 | 120 | 120 | 0.000 |
| 2023-05-12 13:00 | 2023-05-12 14:59 | 120 | 120 | 0.000 |
| 2023-07-12 09:00 | 2023-07-12 10:59 | 120 | 120 | 0.000 |
| 2023-07-14 07:00 | 2023-07-14 08:59 | 120 | 120 | 0.000 |

### XAUUSD

- gaps: 219
- total_minutes: 13389
- non_weekend_minutes: 13389
- overlap_non_weekend_minutes: 17

Representative examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-03-01 10:00 | 2023-03-01 11:59 | 120 | 120 | 0.000 |
| 2023-03-21 12:00 | 2023-03-21 13:59 | 120 | 120 | 0.000 |
| 2023-03-30 11:00 | 2023-03-30 12:59 | 120 | 120 | 0.000 |
| 2023-06-28 09:00 | 2023-06-28 10:59 | 120 | 120 | 0.000 |
| 2023-03-09 08:52 | 2023-03-09 09:59 | 68 | 68 | 0.191 |

Interpretation:

Both symbols have substantial symbol-specific missingness. This matters because H017 inner-joins USDJPY and XAUUSD timestamps. Symbol-specific gaps can bias the shared simulation timeline.

## Suspicious Unclassified Gaps

### USDJPY

- gaps: 169
- total_minutes: 6992
- non_weekend_minutes: 6992
- overlap_non_weekend_minutes: 3552

Representative examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-03-30 16:00 | 2023-03-30 19:59 | 240 | 240 | 0.500 |
| 2023-05-22 08:00 | 2023-05-22 10:59 | 180 | 180 | 0.667 |
| 2023-06-28 12:00 | 2023-06-28 14:59 | 180 | 180 | 0.333 |
| 2023-03-01 06:00 | 2023-03-01 07:59 | 120 | 120 | 0.500 |
| 2023-03-15 16:00 | 2023-03-15 17:59 | 120 | 120 | 0.500 |

### XAUUSD

- gaps: 123
- total_minutes: 14223
- non_weekend_minutes: 14223
- overlap_non_weekend_minutes: 6986

Representative examples included:

| Start UTC | End UTC | Duration Minutes | Non-Weekend Minutes | Overlap Ratio |
| --- | --- | ---: | ---: | ---: |
| 2023-07-12 12:00 | 2023-07-12 17:59 | 360 | 360 | 0.500 |
| 2023-03-07 14:00 | 2023-03-07 18:59 | 300 | 300 | 0.400 |
| 2023-04-25 14:00 | 2023-04-25 17:59 | 240 | 240 | 0.500 |
| 2023-06-06 15:00 | 2023-06-06 18:59 | 240 | 240 | 0.517 |
| 2023-06-19 14:00 | 2023-06-19 17:59 | 240 | 240 | 0.529 |

Interpretation:

The suspicious unclassified bucket remains too large to ignore. These gaps block source acceptance unless future evidence classifies them or a conservative exclusion policy is defined.

## Cross-Symbol Focus Missing-Minute Totals

For the March-July 2023 focus window:

- USDJPY_focus_missing_minutes: 109906
- XAUUSD_focus_missing_minutes: 113053
- overlapping_focus_missing_minutes: 89928
- USDJPY_only_focus_missing_minutes: 19978
- XAUUSD_only_focus_missing_minutes: 23125
- overlap_pct_of_USDJPY_focus_missing: 81.822648
- overlap_pct_of_XAUUSD_focus_missing: 79.544992

Interpretation:

The March-July 2023 issue remains strongly cross-symbol. The candidate classification does not eliminate the broader source-quality concern.

## Diagnostic Conclusions

### What this diagnostic supports

1. 2023-04-07 is a strong full-holiday candidate because both symbols had zero observed bars.
2. Friday early-close-like gaps are recurring across multiple years.
3. The 2023 early-close-like bucket is somewhat larger in non-weekend minutes than comparable years for both symbols.
4. XAUUSD has a measurable daily 17:00 UTC session-break candidate bucket, but this bucket is not large enough to explain the full anomaly.
5. The cross-symbol source-outage candidate bucket is large for both symbols.
6. The symbol-specific source-defect candidate bucket is also large for both symbols.
7. The suspicious unclassified bucket remains material.
8. The March-July 2023 anomaly remains unresolved.

### What this diagnostic does not prove

1. It does not prove HistData is unusable.
2. It does not prove HistData is acceptable.
3. It does not prove that 2023-04-07 should be accepted as a valid closure.
4. It does not prove the Friday early-close-like gaps are broker-equivalent.
5. It does not prove XAUUSD 17:00 UTC breaks are broker-equivalent.
6. It does not prove the cross-symbol candidate gaps are vendor outages.
7. It does not prove the symbol-specific candidate gaps are vendor defects.
8. It does not authorize H017 validation on HistData.
9. It does not authorize derived HistData file creation.

## Current Decision

HistData remains not accepted as a research source.

The March-July 2023 anomaly remains a major unresolved source-quality blocker.

Before HistData can be accepted, the project still needs:

1. explicit holiday and special-closure classification,
2. source-session reconciliation,
3. broker mismatch assessment versus Exness,
4. H4 construction decision,
5. final HistData source acceptance or rejection decision.

## Recommended Next Sub-Phase

Recommended next sub-phase:

Phase 3.26-k - HistData source-session reconciliation plan

Purpose:

1. define the expected trading/session hours for HistData USDJPY and XAUUSD,
2. compare those sessions with the project's future broker execution environment,
3. decide how to treat repeated Friday early-close-like gaps,
4. decide how to treat XAUUSD 17:00 UTC daily breaks,
5. define whether March-July 2023 can be reconciled or must be excluded/rejected,
6. continue avoiding H017 and derived-data writes.

The next step should be a documentation plan first, not strategy validation.

## Safety Confirmation

- raw_files_modified: False
- derived_files_written: False
- reusable_code_written: False
- H017_run: False
- HistData_accepted_as_research_source: False
- classification_labels_are_provisional: True
- diagnostic_complete: True
