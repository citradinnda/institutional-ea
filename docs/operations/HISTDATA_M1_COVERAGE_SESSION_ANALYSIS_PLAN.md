# HistData M1 Coverage and Session Analysis Plan

Date: 2026-05-03

## Purpose

This document defines the next analysis required to interpret the large missing-minute counts reported by the dedicated HistData M1 loader.

This is a planning document only.

This phase does not run H017.

This phase does not accept HistData as a research source.

This phase does not write derived data files.

This phase does not modify raw HistData files.

## Background

The dedicated HistData loader can now load the real USDJPY and XAUUSD HistData files with explicit duplicate handling:

    duplicate_policy="drop_exact"

The real-file loader check showed structurally valid canonical outputs:

1. UTC index,
2. monotonic increasing timestamps,
3. no duplicate timestamps after explicit exact-duplicate removal,
4. no non-positive OHLC rows,
5. no bad OHLC rows,
6. no negative volume rows.

However, the naive missing-minute counts are large:

    USDJPY missing minutes: 816687
    XAUUSD missing minutes: 898809

These counts are based on a continuous minute grid between the first and last observed timestamps.

A continuous minute grid includes weekends, market closures, holiday closures, and instrument-specific session breaks. Therefore, the naive missing-minute count is not enough to decide whether the data is acceptable or unacceptable.

The next analysis must separate expected non-trading minutes from suspicious missing trading minutes.

## Source Files

USDJPY raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

XAUUSD raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Important path note:

The directory name `dukascopy_samples` is misleading. These are HistData files, not Dukascopy files.

## Current Known Loader Results

USDJPY:

    n_input_rows: 1808731
    n_bars: 1808431
    earliest_utc: 2021-01-03 17:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 816687
    zero_volume_rows: 1808431

XAUUSD:

    n_input_rows: 1726549
    n_bars: 1726249
    earliest_utc: 2021-01-03 18:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 898809
    zero_volume_rows: 1726249

Duplicate timestamp ranges for both symbols:

    2021-10-31 19:00:00+00:00 through 2021-10-31 19:59:00+00:00
    2022-10-30 19:00:00+00:00 through 2022-10-30 19:59:00+00:00
    2023-10-29 19:00:00+00:00 through 2023-10-29 19:59:00+00:00
    2024-10-27 19:00:00+00:00 through 2024-10-27 19:59:00+00:00
    2025-10-26 19:00:00+00:00 through 2025-10-26 19:59:00+00:00

## Key Principle

Do not interpret every missing minute as a data defect.

First classify missing minutes into categories:

1. expected weekend or market-closure minutes,
2. expected daily session-break minutes,
3. holiday or special-closure minutes,
4. sparse but plausible low-liquidity no-tick minutes,
5. suspicious holes during expected active trading windows,
6. vendor/source artifacts.

Only categories 5 and 6 are immediately concerning for research-grade M1 validation.

## Required Analysis Questions

The next analytical phase must answer:

1. What percentage of the naive missing minutes are weekends?
2. What recurring daily UTC hours have systematic missingness?
3. Do USDJPY and XAUUSD have different missingness patterns?
4. Does XAUUSD show a recurring metals session break?
5. Are there long gaps during expected active trading days?
6. Are missing minutes concentrated around daily rollover?
7. Are missing minutes concentrated around Sunday open or Friday close?
8. Are there year-specific or month-specific outages?
9. Are there suspicious single-symbol outages?
10. Are there overlapping holes in both USDJPY and XAUUSD?
11. Does the observed session structure look stable from 2021 through 2025?
12. Is the source timezone assumption of UTC still plausible?
13. Would deriving H4 bars from this M1 data produce stable, complete H4 bars?
14. Is the data structurally adequate for event-driven M1 stop simulation?
15. What additional source documentation or broker comparison is needed before acceptance?

## Planned Metrics

The next analysis should compute, for each symbol:

1. observed bar count,
2. naive full-range minute count,
3. naive missing-minute count,
4. observed coverage percentage over the full continuous range,
5. missing minutes by year,
6. missing minutes by month,
7. missing minutes by weekday,
8. missing minutes by UTC hour,
9. observed bars by weekday,
10. observed bars by UTC hour,
11. longest missing gaps,
12. distribution of missing-gap lengths,
13. first and last observed timestamp per trading day,
14. daily observed bar counts,
15. days with unusually low observed bar counts,
16. days with no observed bars,
17. overlapping missing gaps between USDJPY and XAUUSD,
18. symbol-specific missing gaps,
19. missing minutes around duplicate timestamp ranges,
20. recurring daily session-break candidates.

## Planned Gap Classification

The analysis should group consecutive missing minutes into missing intervals.

For each missing interval, record:

1. start_utc,
2. end_utc,
3. duration_minutes,
4. start_weekday,
5. end_weekday,
6. start_hour_utc,
7. end_hour_utc,
8. symbol,
9. whether the gap overlaps a weekend,
10. whether the gap resembles a recurring daily break,
11. whether the gap is symbol-specific,
12. whether the gap occurs in both symbols,
13. notes.

This will reduce millions of individual missing minutes into interpretable gaps.

## Weekend Handling

The first pass should use a simple UTC weekend classification only as a diagnostic, not as a final trading-session definition.

A provisional weekend interval can be treated as:

    Friday 22:00 UTC through Sunday 21:59 UTC

This is only a starting diagnostic assumption.

It must not be treated as a final source-acceptance rule.

The final acceptance decision must account for actual source behavior, symbol behavior, and broker-session mismatch risk.

## XAUUSD Metals Session Break

XAUUSD may have instrument-specific maintenance breaks or session gaps that differ from USDJPY.

The analysis must not assume USDJPY and XAUUSD share identical sessions.

The XAUUSD analysis must separately identify recurring daily missing intervals and compare them against USDJPY.

If XAUUSD has stable recurring gaps that look like expected metals session breaks, those gaps should be documented separately from suspicious outages.

## Timezone and Session Warning

The current HistData loader assumes:

    source_tz="UTC"

This remains an explicit assumption.

Coverage/session analysis must look for evidence that supports or challenges the UTC assumption.

Examples of evidence:

1. recurring opens/closes at plausible UTC times,
2. annual DST-like duplicate behavior,
3. stable weekday/hour patterns,
4. mismatch between expected and observed session boundaries.

No timezone conclusion should be made until the analysis is documented.

## H4 Alignment Warning

HistData M1 must not be silently combined with Exness H4 bars.

Before any H017 validation, the project must decide how H4 bars are produced.

Possible future options include:

1. derive H4 bars from HistData M1,
2. compare HistData-derived H4 bars against Exness H4 bars,
3. reject HistData if session mismatch is unacceptable.

This analysis plan does not make that decision.

## Proposed Output Document for the Future Analysis

The future coverage/session analysis should be documented in:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_COVERAGE_SESSION_ANALYSIS.md

That future document should include:

1. command used,
2. git commit used,
3. raw file paths,
4. raw file SHA256 hashes,
5. loader duplicate policy,
6. summary tables,
7. gap classification summary,
8. interpretation,
9. remaining blockers,
10. explicit statement that HistData is or is not accepted.

Unless a later decision changes the project policy, the expected status after the next analysis is still likely:

    HistData remains not accepted as a research source.

## Proposed Implementation Approach

The next phase may use a temporary read-only PowerShell here-string script first.

If the logic becomes useful and repeatable, then it should be promoted into tested code later.

Any reusable code should go under:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\

Any tests should go under:

    C:\Users\equin\Documents\institutional-ea\tests\

Before writing reusable code, inspect actual internal APIs with:

    inspect.signature(...)
    dataclasses.fields(...)

Do not rely on remembered function signatures.

## Explicit Non-Actions

This plan does not:

1. accept HistData,
2. reject HistData,
3. write derived data,
4. modify raw data,
5. run H017,
6. tune H017,
7. change the cost model,
8. combine HistData M1 with Exness H4,
9. change `.gitignore`,
10. add machine learning,
11. broaden the symbol universe.

## Success Criteria for the Future Analysis

A successful future coverage/session analysis should make the large missing-minute counts interpretable.

It should clearly distinguish:

1. expected market-closure gaps,
2. recurring session-break gaps,
3. suspicious data holes,
4. symbol-specific gaps,
5. source-wide gaps.

It should produce enough evidence to decide whether the project can proceed to a formal HistData source-acceptance decision.

## Current Status

After this plan:

1. raw HistData remains preserved,
2. duplicate handling is documented and tested,
3. real-file `drop_exact` loader behavior is documented,
4. derived-data provenance rules are documented,
5. coverage/session analysis is planned,
6. HistData remains not accepted,
7. H017 remains not promotable and has not been run on HistData.
