# HistData M1 Coverage and Session Analysis

Date: 2026-05-03

## Purpose

This document records the first read-only coverage and session diagnostic for the real HistData M1 files.

This analysis was performed after:

1. raw HistData inventory,
2. dedicated HistData loader implementation,
3. explicit duplicate-handling decision record,
4. tested `drop_exact` duplicate policy,
5. real-file `drop_exact` loader check,
6. derived-data provenance plan,
7. coverage/session analysis plan.

This analysis does not accept HistData as a research source.

This analysis does not reject HistData as a research source.

This analysis does not write derived data files.

This analysis does not modify raw HistData files.

This analysis does not run H017.

## Source Files

USDJPY raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

XAUUSD raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Important path note:

The directory name `dukascopy_samples` is misleading. These are HistData files, not Dukascopy files.

## Loader API Inspection

The diagnostic inspected the actual loader API before calling it.

Observed signature:

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

The diagnostic used explicit duplicate handling:

    duplicate_policy="drop_exact"

The strict default remains:

    duplicate_policy="reject"

## Duplicate Timestamp Result

Both symbols loaded with the same duplicate timestamp ranges after explicit exact-duplicate handling.

Duplicate timestamp ranges for both symbols:

    2021-10-31 19:00:00+00:00 through 2021-10-31 19:59:00+00:00
    2022-10-30 19:00:00+00:00 through 2022-10-30 19:59:00+00:00
    2023-10-29 19:00:00+00:00 through 2023-10-29 19:59:00+00:00
    2024-10-27 19:00:00+00:00 through 2024-10-27 19:59:00+00:00
    2025-10-26 19:00:00+00:00 through 2025-10-26 19:59:00+00:00

Each range contains 60 duplicate timestamp values.

For each symbol:

    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300

Interpretation:

The duplicate pattern remains consistent with the earlier DST-like annual duplicate-hour observation. This observation does not by itself accept the data source.

## USDJPY Structural Summary

USDJPY result:

    n_input_rows: 1808731
    n_bars: 1808431
    full_continuous_minute_count: 2625118
    earliest_utc: 2021-01-03 17:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    source_tz: UTC
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 816687
    computed_missing_minutes: 816687
    coverage_pct_naive_full_range: 68.889513
    columns: ['open', 'high', 'low', 'close', 'volume']
    tz: UTC
    is_monotonic_increasing: True
    has_duplicates: False
    zero_volume_rows: 1808431

USDJPY structurally loaded as UTC, monotonic, duplicate-free M1 bars after explicit exact-duplicate removal.

All volume rows are zero.

## XAUUSD Structural Summary

XAUUSD result:

    n_input_rows: 1726549
    n_bars: 1726249
    full_continuous_minute_count: 2625058
    earliest_utc: 2021-01-03 18:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    source_tz: UTC
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 898809
    computed_missing_minutes: 898809
    coverage_pct_naive_full_range: 65.760414
    columns: ['open', 'high', 'low', 'close', 'volume']
    tz: UTC
    is_monotonic_increasing: True
    has_duplicates: False
    zero_volume_rows: 1726249

XAUUSD structurally loaded as UTC, monotonic, duplicate-free M1 bars after explicit exact-duplicate removal.

All volume rows are zero.

## Provisional Weekend Classification

The diagnostic used a provisional weekend rule:

    Friday 22:00 UTC through Sunday 21:59 UTC

This was diagnostic only.

It is not a final trading-session definition.

USDJPY:

    missing_minutes_total: 816687
    missing_minutes_provisional_weekend: 674547
    missing_minutes_provisional_non_weekend: 142140
    missing_weekend_pct_of_missing: 82.595535
    missing_non_weekend_pct_of_missing: 17.404465

XAUUSD:

    missing_minutes_total: 898809
    missing_minutes_provisional_weekend: 688151
    missing_minutes_provisional_non_weekend: 210658
    missing_weekend_pct_of_missing: 76.56254
    missing_non_weekend_pct_of_missing: 23.43746

Interpretation:

Most naive missing minutes are explained by provisional weekend or market-closure time.

The remaining provisional non-weekend missing minutes still require classification before HistData can be accepted.

## Observed Bars by Year

USDJPY:

    2021: 369333
    2022: 372536
    2023: 322896
    2024: 372023
    2025: 371643

XAUUSD:

    2021: 353386
    2022: 354568
    2023: 308752
    2024: 355592
    2025: 353951

Interpretation:

Both symbols show materially lower observed bar counts in 2023.

This is a source-quality warning requiring further analysis. It may reflect source/session behavior, vendor history issues, holiday/session changes, or another artifact. It must not be ignored.

## Missing Minutes by Year

USDJPY:

    2021: 152367
    2022: 153064
    2023: 202704
    2024: 155017
    2025: 153535

XAUUSD:

    2021: 168254
    2022: 171032
    2023: 216848
    2024: 171448
    2025: 171227

Interpretation:

The elevated 2023 missing-minute count appears in both symbols.

This requires a follow-up focused year/month analysis before source acceptance.

## Observed Bars by Weekday

USDJPY:

    Monday: 360398
    Tuesday: 363375
    Wednesday: 362110
    Thursday: 361524
    Friday: 255365
    Saturday: 0
    Sunday: 105659

XAUUSD:

    Monday: 341811
    Tuesday: 350093
    Wednesday: 348054
    Thursday: 345507
    Friday: 249056
    Saturday: 0
    Sunday: 91728

Interpretation:

The weekday pattern is plausible for FX/metals data with no Saturday trading, partial Friday sessions, and Sunday open behavior.

This does not prove research acceptability.

## Observed Bars by UTC Hour

USDJPY observed bars by UTC hour:

    0: 77724
    1: 77767
    2: 77859
    3: 77755
    4: 77551
    5: 76788
    6: 74380
    7: 74268
    8: 74518
    9: 74199
    10: 74790
    11: 74081
    12: 73935
    13: 74075
    14: 73871
    15: 73900
    16: 73118
    17: 68474
    18: 73742
    19: 74137
    20: 77945
    21: 77928
    22: 77853
    23: 77773

XAUUSD observed bars by UTC hour:

    0: 77332
    1: 77337
    2: 77335
    3: 77262
    4: 77158
    5: 76317
    6: 73922
    7: 73799
    8: 74452
    9: 73548
    10: 74375
    11: 73495
    12: 73715
    13: 73211
    14: 72127
    15: 71692
    16: 67056
    17: 4790
    18: 73536
    19: 74217
    20: 77382
    21: 77400
    22: 77398
    23: 77393

Interpretation:

XAUUSD has a very strong missingness concentration at UTC hour 17.

This is consistent with a recurring metals session or maintenance break. It should be investigated and documented separately from suspicious outages.

USDJPY is much more continuous by UTC hour, though UTC hour 17 has fewer observed bars than neighboring hours.

## Daily Observed Bar Count Summary

USDJPY:

    n_calendar_days: 1824
    n_days_with_zero_bars: 262
    n_days_with_1_to_100_bars: 0
    n_days_with_101_to_500_bars: 263
    n_days_with_501_to_1000_bars: 48
    n_days_with_more_than_1000_bars: 1251

XAUUSD:

    n_calendar_days: 1824
    n_days_with_zero_bars: 270
    n_days_with_1_to_100_bars: 0
    n_days_with_101_to_500_bars: 265
    n_days_with_501_to_1000_bars: 91
    n_days_with_more_than_1000_bars: 1198

Interpretation:

The zero-bar days are mostly expected to be Saturdays and full market closures, but this must be verified.

USDJPY has many full 1440-bar days.

XAUUSD maximum daily count is 1380 bars, consistent with a recurring 60-minute daily break.

## Missing Gap Summary

USDJPY:

    n_missing_gaps: 7609
    mean_gap_duration_minutes: 107.331712
    median_gap_duration_minutes: 1
    75th_percentile_gap_duration_minutes: 2
    90th_percentile_gap_duration_minutes: 60
    95th_percentile_gap_duration_minutes: 60
    99th_percentile_gap_duration_minutes: 2883.92
    max_gap_duration_minutes: 4321

XAUUSD:

    n_missing_gaps: 2181
    mean_gap_duration_minutes: 412.108666
    median_gap_duration_minutes: 60
    75th_percentile_gap_duration_minutes: 60
    90th_percentile_gap_duration_minutes: 2940
    95th_percentile_gap_duration_minutes: 2940
    99th_percentile_gap_duration_minutes: 3060
    max_gap_duration_minutes: 4441

Interpretation:

USDJPY has many short missing gaps, including many one-minute gaps. These may reflect no-tick sparse minutes, but that must be verified against expected HistData behavior and broker comparison.

XAUUSD has fewer missing gaps, but its median gap is 60 minutes. This supports the observed recurring metals break pattern.

## Longest Missing Gaps

USDJPY longest missing gaps were mostly weekend or holiday-style gaps. The longest observed gap was:

    2023-12-29 16:59:00+00:00 through 2024-01-01 16:59:00+00:00
    duration_minutes: 4321

Other long USDJPY gaps include Good Friday/Easter-style or weekend-style closures.

XAUUSD longest missing gaps were also mostly weekend or holiday-style gaps. The longest observed gap was:

    2024-03-28 15:59:00+00:00 through 2024-03-31 17:59:00+00:00
    duration_minutes: 4441

Other long XAUUSD gaps include Christmas/New Year, Easter-style closures, and Friday-to-Sunday closures.

Interpretation:

The longest gaps are not immediately disqualifying because they appear consistent with weekend and holiday closures. However, holiday/session classification still needs to be formalized.

## Cross-Symbol Missing Minute Overlap

Cross-symbol result:

    USDJPY_missing_minutes: 816687
    XAUUSD_missing_minutes: 898809
    overlapping_missing_minutes: 790807
    USDJPY_only_missing_minutes: 25880
    XAUUSD_only_missing_minutes: 108002
    overlap_pct_of_USDJPY_missing: 96.831099
    overlap_pct_of_XAUUSD_missing: 87.983876

Interpretation:

Most USDJPY missing minutes overlap with XAUUSD missing minutes.

XAUUSD has a much larger symbol-specific missing component.

This is consistent with XAUUSD having additional metals-specific session breaks or closures beyond common FX market closures.

## Preliminary Findings

The diagnostic suggests:

1. the large naive missing-minute counts are mostly driven by expected non-trading periods,
2. USDJPY appears relatively continuous during many trading days,
3. XAUUSD appears to have a recurring 60-minute daily session break,
4. both symbols show elevated missingness in 2023,
5. most long gaps look like weekend or holiday closures,
6. all volume values are zero,
7. source acceptance still requires more work.

## Current Interpretation

This analysis reduces concern about the raw magnitude of the missing-minute counts, because most naive missingness appears related to weekends, market closures, and instrument session behavior.

However, HistData is still not accepted because several unresolved issues remain:

1. the elevated 2023 missingness must be explained,
2. USDJPY short one-minute gaps must be classified,
3. XAUUSD daily session break must be confirmed and documented,
4. holiday and special-closure behavior must be identified,
5. timezone/source-session assumptions must be reconciled,
6. broker mismatch versus Exness must be assessed,
7. H4 construction rules must be decided before any H017 validation.

## Explicit Non-Actions

This analysis did not:

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

## Current Status

HistData remains not accepted as a research source.

H017 remains alive but not promotable.

H017 has not been run on HistData.

## Recommended Next Work

Recommended next sub-phase:

    Phase 3.26-g - Focused HistData 2023 and session-break analysis

Purpose:

1. explain elevated 2023 missingness,
2. classify USDJPY short missing gaps,
3. confirm the XAUUSD recurring 17:00 UTC break pattern,
4. summarize suspicious non-weekend gaps,
5. continue avoiding H017 and derived-data writes.
