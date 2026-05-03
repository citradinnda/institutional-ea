# Broker Short-Window Session Diagnostic Plan

Status: plan only  
Phase: 3.26-m  
HistData source status after this plan: not accepted as a research source  
H017 status after this plan: not run, not promotable

## Purpose

This document defines the plan for using existing broker-native MT5 M1 exports to infer current broker session behavior.

The immediate reason for this plan is the ongoing HistData source-session investigation.

HistData diagnostics have shown that the HistData M1 files are structurally loadable, but not yet acceptable as a research source because several unresolved issues remain:

1. recurring late-October exact duplicate timestamp groups,
2. large missing-minute counts,
3. XAUUSD recurring `17:00 UTC` source-session break candidate,
4. repeated Friday early-close-like gaps,
5. materially abnormal March-July 2023 behavior,
6. large cross-symbol source-outage candidate buckets,
7. large symbol-specific source-defect candidate buckets,
8. suspicious unclassified gaps,
9. no broker-session reconciliation yet,
10. no H4 construction decision yet.

This plan defines how to use the short broker-native MT5 M1 window to compare current broker sessions against HistData source-session candidates.

This phase is documentation only.

No raw files are modified.  
No derived files are written.  
No reusable code is added.  
MT5 is not connected.  
H017 is not run.  
HistData is not accepted.

## Current Broker Data Context

Known broker-native MT5 exports are local and gitignored:

- C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Known broker timezone:

- Europe/Athens

Meaning:

- winter UTC+2
- summer UTC+3
- DST-aware

Known MT5 loader:

- quantcore.data.mt5_loader.load_mt5_csv

Known intended API from prior work:

- load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

Important workflow rule:

Before writing code that calls the loader, inspect the actual API using:

- inspect.signature(...)
- dataclasses.fields(...)

Do not trust remembered function names or keyword names.

## Known Broker-Native M1 Coverage Limitation

Prior broker-native M1 coverage was short:

### USDJPY

- earliest: 2026-01-26 03:09:00+00:00
- latest: 2026-04-30 07:00:00+00:00

### XAUUSD

- earliest: 2026-01-20 02:22:00+00:00
- latest: 2026-04-30 07:00:00+00:00

This is not enough for research validation.

However, it may still help infer current broker session structure.

## Why Broker Short-Window Diagnostics Matter

HistData source-session diagnostics inferred provisional source behavior:

### USDJPY HistData candidates

1. Sunday opens mostly around `17:00 UTC`.
2. Friday closes mostly around `16:59 UTC`.
3. Some early Friday closes around `15:59 UTC`.
4. March-July 2023 has abnormal Friday closes, including `14:59 UTC`.
5. March-July 2023 has abnormal missing-hour counts and coverage.

### XAUUSD HistData candidates

1. Sunday opens mostly around `18:00 UTC`.
2. Friday closes mostly around `16:59 UTC`.
3. A strong recurring full `17:00 UTC` missing-hour signature.
4. Some early Friday close outliers.
5. March-July 2023 has abnormal Friday closes, Sunday open dispersion, and missing-hour counts.

These are source-session inferences, not broker-equivalence findings.

The broker short-window diagnostic is needed because future execution will occur through MT5, not directly through HistData.

## Core Questions

The broker short-window diagnostic should answer these questions.

### 1. USDJPY Broker Session Behavior

For broker-native USDJPY M1 data, determine:

1. earliest and latest UTC timestamp,
2. observed Sunday open behavior,
3. observed Friday close behavior,
4. whether any daily break pattern exists,
5. whether bars are absent during no-tick periods,
6. whether broker timestamps align with expected Europe/Athens conversion,
7. whether broker sessions resemble HistData USDJPY source-session candidates.

### 2. XAUUSD Broker Session Behavior

For broker-native XAUUSD M1 data, determine:

1. earliest and latest UTC timestamp,
2. observed Sunday open behavior,
3. observed Friday close behavior,
4. whether a daily break exists,
5. whether any daily break aligns with `17:00 UTC`,
6. whether break timing differs because of Europe/Athens DST conversion,
7. whether broker sessions resemble HistData XAUUSD source-session candidates.

### 3. Cross-Symbol Broker Alignment

For the overlapping broker-native M1 window, determine:

1. USDJPY missing minutes,
2. XAUUSD missing minutes,
3. overlapping missing minutes,
4. USDJPY-only missing minutes,
5. XAUUSD-only missing minutes,
6. whether symbol-specific broker gaps are common,
7. whether inner-joining timestamps would remove many otherwise valid minutes.

### 4. HistData Versus Broker Session Compatibility

Using current broker-native evidence, determine whether HistData source sessions appear broadly compatible with broker sessions for:

1. weekly open,
2. weekly close,
3. daily XAUUSD break behavior,
4. Friday close behavior,
5. symbol-specific breaks,
6. cross-symbol alignment.

Important limitation:

The broker-native window is in 2026, while HistData currently covers 2021 through 2025. Therefore, this diagnostic can support current broker-session understanding but cannot prove historical broker equivalence.

## Planned Read-Only Diagnostic

The next diagnostic should be a compact PowerShell here-string script.

It should:

1. inspect the MT5 loader API using `inspect.signature(...)`,
2. inspect the MT5 load result dataclass fields using `dataclasses.fields(...)`,
3. load broker-native M1 files for USDJPY and XAUUSD,
4. print loader metadata,
5. build full-minute indexes between each symbol's earliest and latest UTC timestamps,
6. compute missing minutes,
7. summarize observed bars by weekday and UTC hour,
8. summarize missing minutes by weekday and UTC hour,
9. summarize Sunday first observed bar times,
10. summarize Friday last observed bar times,
11. summarize daily full missing-hour candidates,
12. summarize cross-symbol overlap over the common broker-native window,
13. compare broker observed session candidates to HistData source-session candidates,
14. confirm:
    - no raw files modified,
    - no derived files written,
    - reusable code not written,
    - H017 not run,
    - HistData not accepted.

## Expected Output Should Be Compact

The diagnostic output should include:

### Loader API

- actual `load_mt5_csv` signature,
- actual `MT5LoadResult` fields.

### Per Symbol

For each symbol:

- path,
- row count or bar count,
- earliest UTC,
- latest UTC,
- timezone behavior if available,
- observed weekday-hour counts,
- missing weekday-hour counts,
- Sunday open summary,
- Friday close summary,
- daily full missing-hour candidate summary.

### Cross-Symbol

For the common broker-native window:

- common start UTC,
- common end UTC,
- USDJPY observed minutes,
- XAUUSD observed minutes,
- overlapping observed minutes,
- USDJPY missing minutes,
- XAUUSD missing minutes,
- overlapping missing minutes,
- USDJPY-only missing minutes,
- XAUUSD-only missing minutes.

### Safety

The output must end with:

- raw_files_modified: False
- derived_files_written: False
- reusable_code_written: False
- H017_run: False
- HistData_accepted_as_research_source: False
- broker_short_window_only: True
- diagnostic_complete: True

## What The Diagnostic Can Conclude

The broker short-window diagnostic can support conclusions such as:

1. current broker USDJPY appears to open around a certain UTC time,
2. current broker XAUUSD appears to open around a certain UTC time,
3. current broker XAUUSD does or does not show a daily break,
4. current broker Friday close behavior does or does not resemble HistData,
5. current broker sessions are broadly compatible or incompatible with HistData candidates.

## What The Diagnostic Cannot Conclude

The broker short-window diagnostic cannot prove:

1. that HistData is acceptable,
2. that HistData is unusable,
3. that 2021-2025 HistData exactly matches historical Exness sessions,
4. that March-July 2023 HistData gaps are valid,
5. that H017 should be run on HistData,
6. that derived HistData files should be written,
7. that H4 construction rules are solved.

The broker window is too short for research validation and occurs in 2026, outside the HistData 2021-2025 range.

## H4 Construction Relevance

The broker short-window diagnostic matters for H4 construction because future H4 research bars should not be built on arbitrary source-specific assumptions.

Important questions remain:

1. Should H4 bars be aligned to UTC 4-hour boundaries?
2. Should H4 bars be aligned to broker-server 4-hour boundaries?
3. Should H4 bars attempt to match MT5 H4 exports exactly?
4. Should H4 bars spanning daily XAUUSD session breaks be valid?
5. Should H4 bars spanning Friday/weekend closure be invalid?
6. What M1 completeness threshold is required inside an H4 bar?
7. Should USDJPY and XAUUSD H4 timestamps be inner-joined only after per-symbol validity checks?
8. Should incomplete H4 bars be excluded from both symbols to prevent portfolio alignment bias?

No H4 construction decision is made in this phase.

## Potential Outcomes After The Future Diagnostic

### Outcome 1 - Broker Sessions Broadly Match HistData Candidates

If broker sessions broadly match HistData source-session candidates, HistData may continue to the next investigation stage.

This would not accept HistData yet.

### Outcome 2 - Broker Sessions Partially Match HistData Candidates

If broker sessions partially match HistData, the project may need symbol-specific rules or limited-use rules.

For example:

- HistData might be usable for some M1 stop-resolution windows but not for H4 construction.
- XAUUSD may require explicit daily break handling.
- Friday close behavior may require exclusion rules.

This would require a separate decision document.

### Outcome 3 - Broker Sessions Conflict With HistData Candidates

If broker sessions materially conflict with HistData, HistData may need to be rejected or used only for limited diagnostics.

This would require a separate rejection or limitation decision.

## Current Decision

HistData remains not accepted as a research source.

No H017 validation on HistData is authorized.

No derived HistData files are authorized.

No broker/session diagnostic has been run in this phase.

## Recommended Next Sub-Phase

Recommended next sub-phase:

Phase 3.26-n - Read-only broker short-window session diagnostic

Purpose:

1. load existing broker-native MT5 M1 exports,
2. infer current broker session behavior for USDJPY and XAUUSD,
3. compare current broker session behavior against HistData source-session candidates,
4. quantify cross-symbol broker missingness over the common broker-native window,
5. document limitations of the short 2026 broker window,
6. continue avoiding H017 and derived-data writes,
7. keep HistData unaccepted.

This should be a compact read-only PowerShell here-string diagnostic first.

## Safety Confirmation

- raw_files_modified: False
- derived_files_written: False
- reusable_code_written: False
- MT5_connected: False
- H017_run: False
- HistData_accepted_as_research_source: False
- plan_only: True
