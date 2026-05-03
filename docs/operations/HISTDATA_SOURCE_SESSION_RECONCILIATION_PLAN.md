# HistData Source-Session Reconciliation Plan

Status: plan only  
Phase: 3.26-k  
Source status after this plan: not accepted as a research source  
H017 status after this plan: not run, not promotable

## Purpose

This document defines the plan for reconciling HistData source sessions with the project's future broker execution environment.

The immediate reason for this plan is the sequence of HistData diagnostics showing that the raw HistData files are structurally loadable, but not yet source-accepted.

Known unresolved issues include:

1. recurring exact duplicate timestamp groups around late-October DST-related hours,
2. large missing-minute counts,
3. XAUUSD recurring 17:00 UTC break behavior,
4. repeated Friday early-close-like gaps,
5. a materially abnormal March-July 2023 period,
6. large cross-symbol source-outage candidate buckets,
7. large symbol-specific source-defect candidate buckets,
8. suspicious unclassified gaps.

The goal of this plan is to define what evidence is required before HistData can be accepted, conditionally accepted, partially excluded, or rejected.

This is a documentation-only phase.

No raw files are modified.  
No derived files are written.  
H017 is not run.  
HistData is not accepted.

## Current Context

Project target:

- Research stack: Python `quantcore`
- Execution target: MetaTrader 5
- Future production target: Oracle Cloud Always Free VPS
- Current broker-native export timezone: Europe/Athens
- Broker timezone meaning:
  - winter UTC+2
  - summer UTC+3
  - DST-aware

Current strategy universe:

- USDJPY
- XAUUSD

Current source under investigation:

- HistData M1 CSV files for approximately 2021 through 2025

Raw HistData files inspected:

- C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Important note:

The folder name `dukascopy_samples` is misleading. These two files are HistData files, not Dukascopy files.

Dedicated loader:

- quantcore.data.histdata_loader.load_histdata_m1_csv

Known loader signature:

- load_histdata_m1_csv(path: str | Path, *, source_tz: str = "UTC", duplicate_policy: DuplicatePolicy = "reject") -> HistDataM1LoadResult

Known duplicate policy:

- default: duplicate_policy="reject"
- explicit diagnostic opt-in: duplicate_policy="drop_exact"

The `drop_exact` policy removes only exact duplicate OHLCV rows and rejects conflicting duplicate timestamp groups.

## Why Session Reconciliation Matters

Session reconciliation means comparing the trading-minute schedule implied by one data source against the trading-minute schedule required by the execution environment.

For this project, session reconciliation matters because:

1. H017 uses USDJPY and XAUUSD together.
2. H017 inner-joins timestamps across both symbols.
3. Missing minutes in one symbol can remove otherwise valid timestamps from the portfolio simulation.
4. H4 bars built from incomplete M1 data can distort open, high, low, close, ATR, Donchian signals, chandelier exits, and event-driven stop resolution.
5. Broker execution sessions may differ from vendor historical-data sessions.
6. A strategy validated on source-specific session artifacts may fail when executed on MT5 broker data.
7. A gap that is harmless for one instrument may be harmful for another.
8. A daily XAUUSD metals break should not be assumed to apply to USDJPY.
9. Friday early-close-like patterns may be vendor-session definitions, broker-session definitions, holiday effects, or source defects.
10. A source can be structurally valid and still be unsuitable for research validation.

Therefore, HistData cannot be accepted only because it loads cleanly.

## Existing Evidence Summary

Prior documents:

- docs/operations/HISTDATA_M1_ACQUISITION_INVENTORY.md
- docs/operations/HISTDATA_M1_LOADER_REAL_FILE_CHECK.md
- docs/operations/HISTDATA_M1_DROP_EXACT_REAL_FILE_CHECK.md
- docs/operations/HISTDATA_DERIVED_DATA_PROVENANCE_PLAN.md
- docs/operations/HISTDATA_M1_COVERAGE_SESSION_ANALYSIS_PLAN.md
- docs/operations/HISTDATA_M1_COVERAGE_SESSION_ANALYSIS.md
- docs/operations/HISTDATA_FOCUSED_2023_SESSION_BREAK_ANALYSIS.md
- docs/operations/HISTDATA_MARCH_JULY_2023_ANOMALY_INVESTIGATION.md
- docs/operations/HISTDATA_HOLIDAY_SPECIAL_CLOSURE_CLASSIFICATION_PLAN.md
- docs/operations/HISTDATA_MARCH_JULY_2023_GAP_CANDIDATE_CLASSIFICATION.md

Important findings already documented:

1. USDJPY and XAUUSD raw HistData files are preserved exactly as downloaded.
2. Both files are under `/data/`, so they are gitignored.
3. Both files have exact duplicate timestamp groups around recurring late-October DST-related hours.
4. The duplicate groups are exact OHLCV duplicates, not conflicting rows.
5. Explicit `duplicate_policy="drop_exact"` can produce UTC, monotonic, duplicate-free output.
6. Large naive missing-minute counts are mostly weekend/session related.
7. XAUUSD has a stable recurring 17:00 UTC missingness signature.
8. March-July 2023 is materially abnormal for both symbols.
9. The March-July 2023 anomaly is strongly cross-symbol.
10. Candidate classification identified some holiday, early-close, and session-break patterns.
11. Large cross-symbol source-outage candidate buckets remain.
12. Large symbol-specific source-defect candidate buckets remain.
13. Suspicious unclassified gaps remain material.
14. HistData remains not accepted.

## Source-Session Questions To Answer

The next diagnostics and decisions must answer these questions.

### 1. What sessions does HistData imply for USDJPY?

For USDJPY, determine:

1. normal weekly open time in UTC,
2. normal weekly close time in UTC,
3. normal weekday coverage expectations,
4. whether there are daily breaks,
5. whether Friday early-close-like gaps are systematic,
6. whether March-July 2023 differs from other years,
7. whether USDJPY has source-session gaps that are not plausible for FX,
8. whether source-session rules change around DST.

USDJPY is a major FX pair. It should not automatically inherit metals-style daily breaks.

### 2. What sessions does HistData imply for XAUUSD?

For XAUUSD, determine:

1. normal weekly open time in UTC,
2. normal weekly close time in UTC,
3. daily session break timing,
4. whether 17:00 UTC break behavior is stable across years,
5. whether the daily break is always exactly 60 minutes,
6. whether break timing changes around DST,
7. whether Friday close timing differs from USDJPY,
8. whether XAUUSD has unexplained intraday missingness beyond expected metals-session behavior.

The recurring XAUUSD 17:00 UTC pattern is a strong candidate session break, but it is not yet accepted as broker-equivalent.

### 3. What sessions does Exness MT5 imply?

For the future execution broker environment, determine:

1. server timezone,
2. DST behavior,
3. USDJPY weekly open and close times,
4. XAUUSD weekly open and close times,
5. XAUUSD daily break times,
6. Friday close behavior,
7. holiday and special-closure behavior,
8. whether MT5 bars include placeholder bars during illiquid periods,
9. whether MT5 omits bars when no ticks occur,
10. how broker sessions changed, if at all, from 2021 through 2025.

Known current broker-native export timezone:

- Europe/Athens

This is not enough by itself. Actual symbol trading sessions must be checked.

### 4. Are HistData and broker sessions compatible enough for research?

Compatibility must be assessed separately for:

1. M1 stop-resolution data,
2. H4 bar construction,
3. USDJPY standalone behavior,
4. XAUUSD standalone behavior,
5. cross-symbol portfolio alignment,
6. H017 inner-join behavior,
7. cost model assumptions,
8. event-driven bridge timing.

A source might be usable for one purpose and not another.

## Planned Evidence Sources

The next reconciliation work should use these evidence sources, in order of preference.

### 1. Local MT5 Broker Exports

Use local broker-native exports when available.

Existing broker-native files:

- C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Known limitation:

Current broker-native M1 history is too short for research validation, but it can still help infer live broker session structure.

### 2. MT5 Symbol Specification

Use MT5 symbol specification where possible to inspect:

1. trading sessions by day,
2. quote sessions by day,
3. server time behavior,
4. symbol-specific contract details.

This may require a later script that connects to MT5 locally. That is not part of this documentation phase.

### 3. HistData Observed Session Diagnostics

Use the HistData files to infer source sessions from observed bars and missing bars.

Important:

Inferred source sessions are evidence, not acceptance.

### 4. Holiday and Special-Closure Calendars

Use explicit market holiday calendars for candidate full closes and early closes.

Any holiday evidence must be documented.

### 5. Broker Documentation

Use broker documentation only as supporting evidence, not as a substitute for actual local MT5 data where possible.

## Planned Reconciliation Diagnostics

The next read-only diagnostics should be compact and targeted.

### Diagnostic A - HistData Weekly Session Template

For each symbol and year:

1. compute observed bars by weekday and UTC hour,
2. compute missing bars by weekday and UTC hour,
3. infer common weekly open and close times,
4. summarize Friday close behavior,
5. summarize Sunday open behavior,
6. split by year to detect changes.

Output should include:

- symbol,
- year,
- first commonly observed Sunday UTC hour,
- last commonly observed Friday UTC hour,
- weekday-hour observed counts,
- recurring missing hour candidates,
- unusual deviations.

### Diagnostic B - HistData Daily Break Template

For each symbol and year:

1. scan each calendar day,
2. detect recurring missing blocks by UTC hour,
3. summarize daily break candidates,
4. separate weekdays from weekends,
5. detect whether XAUUSD 17:00 UTC break is stable,
6. detect whether USDJPY has any daily break-like pattern.

Output should include:

- symbol,
- year,
- candidate break start UTC,
- candidate break duration,
- count of days with full break,
- count of days with partial break,
- count of days with no break.

### Diagnostic C - Broker Short-Window Session Template

Using broker-native M1 exports:

1. load USDJPY and XAUUSD with `load_mt5_csv`,
2. infer observed broker sessions from the available short window,
3. compare broker session structure against HistData in the overlapping period, if any,
4. document mismatches.

Known limitation:

The broker-native window is short and starts in 2026, while HistData currently covers 2021 through 2025. This can reveal current broker structure but cannot prove historical equivalence.

### Diagnostic D - Candidate Gap Reconciliation

For March-July 2023 candidate gaps:

1. reclassify using inferred HistData source sessions,
2. identify which gaps are explained by source sessions,
3. identify which remain suspicious,
4. quantify remaining suspicious minutes,
5. decide whether the period is usable, excludable, or source-blocking.

## H4 Construction Implications

Before HistData can be used for H017 validation, the project must decide how to construct H4 bars from M1.

This matters because H017 signals are H4-based, while event-driven fills use M1 inside H4 windows.

Questions to answer:

1. Should H4 bars be built on UTC 4-hour boundaries?
2. Should H4 bars be built on broker-server 4-hour boundaries?
3. Should H4 bars match Exness MT5 H4 bars exactly?
4. How should missing M1 bars inside an H4 bar be handled?
5. What minimum M1 completeness is required for an H4 bar?
6. Should H4 bars spanning session breaks be allowed?
7. Should bars spanning weekend boundaries be excluded?
8. Should symbol-specific missingness invalidate a portfolio timestamp?
9. Should H4 signals use only timestamps where both symbols have valid H4 bars?
10. Should stop-resolution M1 windows require complete minute coverage?

No H4 construction decision has been made yet.

## Compatibility Outcomes

The reconciliation process can lead to several possible outcomes.

### Outcome 1 - HistData Accepted

HistData may be accepted only if:

1. source sessions are explicitly documented,
2. source sessions are compatible with broker execution,
3. holiday and special-closure behavior is classified,
4. suspicious unclassified gaps are immaterial under a documented threshold,
5. H4 construction rules are fixed,
6. broker mismatch is explicitly assessed,
7. source limitations are recorded in a final decision document.

This outcome has not occurred.

### Outcome 2 - HistData Conditionally Accepted With Exclusions

HistData may become conditionally usable if:

1. most years are reconcilable,
2. one period, such as March-July 2023, remains defective,
3. the defective period is explicitly excluded,
4. exclusion does not create lookahead or selection bias,
5. validation windows remain long enough,
6. H4 construction and M1 stop-resolution rules remain conservative.

This outcome has not occurred.

### Outcome 3 - HistData Accepted For M1 Stop Resolution Only

HistData may be useful for M1 intrabar stop-resolution but not for H4 signal construction if:

1. M1 price paths are sufficiently reliable,
2. H4 bars are built from broker-native or separately validated data,
3. timestamp alignment is safe,
4. session mismatches are controlled.

This would require a separate decision. It has not occurred.

### Outcome 4 - HistData Rejected

HistData should be rejected if:

1. source sessions cannot be reconciled,
2. suspicious unclassified gaps remain large,
3. March-July 2023 cannot be explained or safely excluded,
4. source-specific artifacts materially distort H4 bars,
5. broker mismatch is too large,
6. cross-symbol alignment is unreliable,
7. the data would create false confidence in H017.

This outcome has not occurred.

## Acceptance Blockers Remaining

HistData remains blocked by:

1. incomplete source-session reconciliation,
2. incomplete holiday and special-closure classification,
3. unresolved March-July 2023 anomaly,
4. unresolved suspicious unclassified gaps,
5. incomplete broker mismatch assessment versus Exness,
6. missing H4 construction decision,
7. no final source acceptance or rejection decision.

## Explicit Non-Goals

This phase does not:

1. write reusable code,
2. write derived files,
3. modify raw files,
4. repair gaps,
5. fill missing minutes,
6. interpolate prices,
7. resample M1 to H4,
8. run H017,
9. tune H017,
10. accept HistData,
11. reject HistData permanently,
12. change the cost model,
13. change strategy logic,
14. broaden the symbol universe,
15. add machine learning.

## Recommended Next Sub-Phase

Recommended next sub-phase:

Phase 3.26-l - Read-only HistData weekly and daily source-session diagnostics

Purpose:

1. infer HistData weekly session templates for USDJPY and XAUUSD,
2. infer HistData daily break templates by symbol and year,
3. quantify Friday close behavior,
4. quantify Sunday open behavior,
5. check whether March-July 2023 differs from other years,
6. keep labels provisional,
7. continue avoiding H017 and derived-data writes.

This should be a read-only PowerShell here-string diagnostic first.

## Current Decision

HistData remains not accepted as a research source.

No H017 validation on HistData is authorized.

No derived HistData files are authorized.

## Safety Confirmation

- raw_files_modified: False
- derived_files_written: False
- reusable_code_written: False
- H017_run: False
- HistData_accepted_as_research_source: False
- plan_only: True
