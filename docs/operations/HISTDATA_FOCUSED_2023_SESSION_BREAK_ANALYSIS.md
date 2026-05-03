# HistData Focused 2023 and Session-Break Analysis

Date: 2026-05-03

## Purpose

This document records a focused read-only diagnostic of the HistData M1 files after the first coverage/session analysis.

The diagnostic focused on:

1. elevated 2023 missingness,
2. USDJPY short non-weekend gaps,
3. XAUUSD 17:00 UTC session-break behavior,
4. suspicious non-weekend gaps,
5. cross-symbol missing-minute overlap in 2023.

This document does not accept HistData as a research source.

This document does not reject HistData as a research source.

This diagnostic did not run H017.

This diagnostic did not write derived files.

This diagnostic did not modify raw files.

## Source Files

USDJPY raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

XAUUSD raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Important path note:

The directory name `dukascopy_samples` is misleading. These are HistData files, not Dukascopy files.

## Loader API Inspection

Observed loader signature:

    load_histdata_m1_csv(path: 'str | Path', *, source_tz: 'str' = 'UTC', duplicate_policy: 'DuplicatePolicy' = 'reject') -> 'HistDataM1LoadResult'

Observed `HistDataM1LoadResult` fields:

    bars
    n_bars
    n_input_rows
    earliest_utc
    latest_utc
    source_tz
    duplicate_policy
    n_duplicate_rows_removed
    n_duplicate_timestamp_values
    duplicate_timestamp_ranges
    n_missing_minutes
    missing_minutes

The diagnostic used:

    duplicate_policy="drop_exact"

The strict default remains:

    duplicate_policy="reject"

## USDJPY Compact Load Summary

USDJPY result:

    n_input_rows: 1808731
    n_bars: 1808431
    full_continuous_minute_count: 2625118
    coverage_pct_naive_full_range: 68.889513
    earliest_utc: 2021-01-03 17:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 816687
    n_missing_gaps: 7609
    index_tz: UTC
    index_is_monotonic_increasing: True
    index_has_duplicates: False
    zero_volume_rows: 1808431

USDJPY remained structurally valid after explicit exact-duplicate handling.

All volume rows are zero.

## XAUUSD Compact Load Summary

XAUUSD result:

    n_input_rows: 1726549
    n_bars: 1726249
    full_continuous_minute_count: 2625058
    coverage_pct_naive_full_range: 65.760414
    earliest_utc: 2021-01-03 18:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 898809
    n_missing_gaps: 2181
    index_tz: UTC
    index_is_monotonic_increasing: True
    index_has_duplicates: False
    zero_volume_rows: 1726249

XAUUSD remained structurally valid after explicit exact-duplicate handling.

All volume rows are zero.

## USDJPY Non-Weekend Gap Summary

Using the provisional weekend rule from the prior analysis:

    Friday 22:00 UTC through Sunday 21:59 UTC

USDJPY non-weekend gap result:

    n_non_weekend_gaps: 6359
    n_non_weekend_gaps_longer_than_60_minutes: 93

USDJPY non-weekend gap duration buckets:

    1 minute: 4385
    2 minutes: 723
    3-5 minutes: 522
    6-15 minutes: 48
    16-60 minutes: 588
    61-240 minutes: 86
    241-1440 minutes: 6
    >1440 minutes: 1

USDJPY non-weekend gaps by year:

    2021: 2669
    2022: 849
    2023: 1171
    2024: 813
    2025: 857

Interpretation:

Most USDJPY non-weekend gaps are short. The diagnostic found that 5630 of 6359 non-weekend gaps were 1-5 minutes, or 88.535933 percent.

This supports the possibility that many USDJPY short gaps are sparse no-tick minutes rather than large source outages.

However, this is not yet enough to accept the source. The longer non-weekend gaps still require classification.

## USDJPY Short Non-Weekend Gap Summary

USDJPY short non-weekend gaps:

    n_usdjpy_non_weekend_gaps: 6359
    n_usdjpy_short_non_weekend_gaps_duration_1_to_5: 5630
    pct_short_of_non_weekend_gaps: 88.535933

Short gap counts by duration:

    1 minute: 4385
    2 minutes: 723
    3 minutes: 339
    4 minutes: 137
    5 minutes: 46

Short gap counts by year:

    2021: 2657
    2022: 842
    2023: 494
    2024: 794
    2025: 843

Short gap counts by start hour UTC were concentrated around:

    16 UTC: 852
    17 UTC: 2309
    18 UTC: 621

Interpretation:

The short USDJPY gaps are heavily concentrated around the 16:00-18:00 UTC region, especially 17:00 UTC. This could reflect rollover/session behavior, sparse vendor ticks, or source-specific conventions.

This pattern must be reconciled before source acceptance.

## USDJPY Longest Non-Weekend Gaps

Top USDJPY non-weekend gaps included:

    2024-12-31 16:59:00+00:00 through 2025-01-01 17:03:00+00:00
    duration_minutes: 1445

    2021-05-31 00:00:00+00:00 through 2021-05-31 19:59:00+00:00
    duration_minutes: 1200

    2023-12-25 02:59:00+00:00 through 2023-12-25 17:03:00+00:00
    duration_minutes: 845

    2024-12-25 03:00:00+00:00 through 2024-12-25 17:03:00+00:00
    duration_minutes: 844

    2025-12-25 02:59:00+00:00 through 2025-12-25 16:59:00+00:00
    duration_minutes: 841

Interpretation:

Several long non-weekend USDJPY gaps look like holiday or special-closure behavior, such as Christmas and New Year. These should be classified separately from suspicious source outages.

Some other gaps, including 2023 March-July intervals, need more investigation.

## XAUUSD Non-Weekend Gap Summary

XAUUSD non-weekend gap result:

    n_non_weekend_gaps: 1895
    n_non_weekend_gaps_longer_than_60_minutes: 165

XAUUSD non-weekend gap duration buckets:

    1 minute: 279
    2 minutes: 27
    3-5 minutes: 17
    6-15 minutes: 3
    16-60 minutes: 1404
    61-240 minutes: 151
    241-1440 minutes: 11
    >1440 minutes: 3

XAUUSD non-weekend gaps by year:

    2021: 234
    2022: 259
    2023: 919
    2024: 253
    2025: 230

Interpretation:

XAUUSD has far fewer total gaps than USDJPY, but many more 16-60 minute gaps. This is consistent with the observed recurring daily metals break pattern.

The 2023 XAUUSD count is materially elevated and remains a source-quality warning.

## XAUUSD 17:00 UTC Break Candidate Summary

The diagnostic checked the 17:00-17:59 UTC hour across calendar days.

Result:

    n_calendar_days_checked: 1822
    n_full_60_minute_17utc_break_days: 1742
    n_partial_17utc_break_days: 6
    n_no_17utc_break_days: 74

Break summary by year:

    2021:
        full_60_minute_break: 347
        partial_break: 0
        no_break: 15

    2022:
        full_60_minute_break: 350
        partial_break: 2
        no_break: 13

    2023:
        full_60_minute_break: 354
        partial_break: 1
        no_break: 10

    2024:
        full_60_minute_break: 347
        partial_break: 2
        no_break: 17

    2025:
        full_60_minute_break: 344
        partial_break: 1
        no_break: 19

Break summary by weekday:

    Monday:
        full_60_minute_break: 246
        partial_break: 2
        no_break: 13

    Tuesday:
        full_60_minute_break: 246
        partial_break: 2
        no_break: 13

    Wednesday:
        full_60_minute_break: 243
        partial_break: 0
        no_break: 17

    Thursday:
        full_60_minute_break: 244
        partial_break: 2
        no_break: 14

    Friday:
        full_60_minute_break: 260
        partial_break: 0
        no_break: 0

    Saturday:
        full_60_minute_break: 260
        partial_break: 0
        no_break: 0

    Sunday:
        full_60_minute_break: 243
        partial_break: 0
        no_break: 17

Exact gap rows starting at 17:00, lasting 60 minutes, and ending at 17:59:

    n_exact_gap_rows_start_17_00_duration_60_end_17_59: 866

Exact 17:00 UTC 60-minute gap rows by year:

    2021: 188
    2022: 187
    2023: 136
    2024: 180
    2025: 175

Interpretation:

XAUUSD has a very strong recurring 17:00 UTC session-break signature.

This appears stable across years, but not perfectly uniform in the exact gap-table representation because some longer closures include the 17:00 hour as part of a larger gap.

This pattern should be treated as a likely metals session break candidate, not as suspicious missingness by itself.

## XAUUSD Longest Non-Weekend Gaps

Top XAUUSD non-weekend gaps included:

    2025-12-24 13:44:00+00:00 through 2025-12-25 18:03:00+00:00
    duration_minutes: 1700

    2024-12-24 13:44:00+00:00 through 2024-12-25 17:59:00+00:00
    duration_minutes: 1696

    2024-12-31 16:58:00+00:00 through 2025-01-01 17:59:00+00:00
    duration_minutes: 1502

    2021-05-31 00:00:00+00:00 through 2021-05-31 19:59:00+00:00
    duration_minutes: 1200

    2023-07-12 12:00:00+00:00 through 2023-07-12 17:59:00+00:00
    duration_minutes: 360

Interpretation:

Several long XAUUSD non-weekend gaps look like holiday or special-closure behavior, especially Christmas and New Year periods.

Some 2023 gaps remain suspicious and require more focused investigation.

## 2023 Daily Count Summary

USDJPY 2023:

    total_observed_bars: 322896
    mean_daily_bars: 884.647
    median_daily_bars: 1019.0
    zero_bar_days: 54
    days_over_1000: 229
    max_daily_bars: 1440

USDJPY 2023 monthly observed bars:

    January: 31883
    February: 25606
    March: 22987
    April: 19952
    May: 23229
    June: 22033
    July: 22213
    August: 33036
    September: 29645
    October: 32075
    November: 31535
    December: 28702

XAUUSD 2023:

    total_observed_bars: 308752
    mean_daily_bars: 845.896
    median_daily_bars: 1018.0
    zero_bar_days: 56
    days_over_1000: 189
    max_daily_bars: 1380

XAUUSD 2023 monthly observed bars:

    January: 28914
    February: 24746
    March: 22608
    April: 19311
    May: 22586
    June: 21412
    July: 21350
    August: 31674
    September: 28330
    October: 30764
    November: 29824
    December: 27233

Interpretation:

The elevated 2023 issue is concentrated most strongly from March through July.

Both symbols improve markedly from August 2023 onward.

This pattern is a major unresolved source-quality issue.

## 2023 Cross-Symbol Missing Overlap

2023 missing overlap:

    USDJPY_2023_missing_minutes: 202704
    XAUUSD_2023_missing_minutes: 216848
    overlap_2023_missing_minutes: 181172
    USDJPY_only_2023_missing_minutes: 21532
    XAUUSD_only_2023_missing_minutes: 35676
    overlap_pct_of_USDJPY_2023_missing: 89.377615
    overlap_pct_of_XAUUSD_2023_missing: 83.547923

2023 overlapping missing minutes by month:

    January: 12757
    February: 13331
    March: 18061
    April: 19346
    May: 17808
    June: 16066
    July: 18647
    August: 11581
    September: 13509
    October: 12507
    November: 11628
    December: 15931

2023 USDJPY-only missing minutes by month:

    February: 1383
    March: 3592
    April: 3902
    May: 3603
    June: 5101
    July: 3780
    August: 23
    September: 46
    October: 58
    November: 37
    December: 7

2023 XAUUSD-only missing minutes by month:

    January: 2969
    February: 2243
    March: 3971
    April: 4543
    May: 4246
    June: 5722
    July: 4643
    August: 1385
    September: 1361
    October: 1369
    November: 1748
    December: 1476

Interpretation:

The 2023 issue is mostly cross-symbol, not isolated to one instrument.

March through July 2023 have elevated missingness in both symbols and elevated symbol-specific missingness.

This suggests a source-wide or session-definition issue during that period, not merely normal XAUUSD metals breaks.

## Preliminary Conclusions

The focused diagnostic supports these conclusions:

1. USDJPY has many short non-weekend gaps, mostly 1-5 minutes.
2. USDJPY short gaps are concentrated around 16:00-18:00 UTC, especially 17:00 UTC.
3. XAUUSD has a strong recurring 17:00 UTC 60-minute break candidate.
4. XAUUSD 17:00 UTC missingness appears stable across the full sample.
5. Many long non-weekend gaps correspond to likely holiday or special-closure behavior.
6. 2023 remains abnormal, especially March through July.
7. The 2023 issue affects both symbols.
8. HistData is not yet acceptable for H017 validation.

## Current Status

HistData remains not accepted as a research source.

H017 remains alive but not promotable.

H017 has not been run on HistData.

No derived HistData files have been written.

## Remaining Blockers

Before source acceptance, the project still needs:

1. focused explanation of March-July 2023 missingness,
2. explicit holiday and special-closure classification,
3. source-session reconciliation,
4. XAUUSD metals break confirmation,
5. broker mismatch assessment versus Exness,
6. decision on how to construct H4 bars,
7. formal HistData source acceptance or rejection decision.

## Explicit Non-Actions

This diagnostic did not:

1. modify raw HistData files,
2. write derived HistData files,
3. run H017,
4. combine HistData M1 with Exness H4,
5. tune strategy parameters,
6. change the cost model,
7. accept HistData as a research source,
8. reject HistData as a research source,
9. change `.gitignore`,
10. broaden the symbol universe,
11. add machine learning.

## Recommended Next Work

Recommended next sub-phase:

    Phase 3.26-h - Focused March-July 2023 HistData anomaly investigation

Purpose:

1. identify whether the March-July 2023 issue is source-wide,
2. list the largest 2023 non-weekend gaps,
3. compare daily observed bar counts before, during, and after the anomaly,
4. decide whether this anomaly blocks source acceptance,
5. continue avoiding H017 and derived-data writes.
