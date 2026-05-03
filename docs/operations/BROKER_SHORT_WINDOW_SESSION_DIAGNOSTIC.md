# Broker Short-Window Session Diagnostic

Status: read-only diagnostic completed  
Phase: 3.26-n  
HistData source status after this diagnostic: not accepted as a research source  
H017 status after this diagnostic: not run, not promotable

## Purpose

This diagnostic used existing local broker-native MT5 M1 CSV exports to infer current broker session behavior for USDJPY and XAUUSD.

The diagnostic followed the plan documented in:

- docs/operations/BROKER_SHORT_WINDOW_SESSION_DIAGNOSTIC_PLAN.md

The goals were to:

1. inspect the actual MT5 loader API before calling it,
2. load existing broker-native M1 exports,
3. infer current broker session behavior,
4. compare current broker-session candidates against HistData source-session candidates,
5. quantify cross-symbol broker missingness over the common short window,
6. keep the analysis read-only,
7. avoid MT5 connection,
8. avoid derived-data writes,
9. avoid H017,
10. keep HistData unaccepted.

This diagnostic used local CSV exports only.

No raw files were modified.  
No derived files were written.  
No reusable code was added.  
MT5 was not connected.  
H017 was not run.  
HistData was not accepted.

## Inputs

Broker-native MT5 M1 files inspected:

- C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

These files are under `/data/` and remain gitignored.

Broker timezone used:

- Europe/Athens

Meaning:

- winter UTC+2
- summer UTC+3
- DST-aware

## MT5 Loader API Inspection

Observed loader:

- quantcore.data.mt5_loader.load_mt5_csv

Observed signature:

- load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

Observed `MT5LoadResult` fields:

- bars
- n_bars
- n_input_rows
- earliest_utc
- latest_utc
- broker_tz

## Broker-Native Coverage

### USDJPY

- n_bars: 97907
- index_tz: UTC
- earliest_utc: 2026-01-26 03:09:00+00:00
- latest_utc: 2026-04-30 07:00:00+00:00
- missing_minutes_inside_symbol_range: 37685
- n_input_rows: 97907
- broker_tz: Europe/Athens

### XAUUSD

- n_bars: 97966
- index_tz: UTC
- earliest_utc: 2026-01-20 02:22:00+00:00
- latest_utc: 2026-04-30 07:00:00+00:00
- missing_minutes_inside_symbol_range: 46313
- n_input_rows: 97966
- broker_tz: Europe/Athens

## Important Coverage Limitation

This broker-native M1 window is short and current:

- USDJPY starts on 2026-01-26.
- XAUUSD starts on 2026-01-20.
- Both end on 2026-04-30 07:00 UTC.

This window is not sufficient for research validation.

It can only help infer current broker session behavior.

It cannot prove historical broker-session equivalence for the 2021-2025 HistData files.

## USDJPY Broker Session Findings

### Sunday Observed Opens

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 18:05 | 4 |
| 18:10 | 1 |
| 19:05 | 2 |
| 19:26 | 1 |
| 20:05 | 4 |
| 20:06 | 1 |

Observed Sundays:

| Date | First UTC | Last UTC | Bars |
| --- | --- | --- | ---: |
| 2026-02-01 | 20:05 | 23:59 | 235 |
| 2026-02-08 | 20:05 | 23:59 | 233 |
| 2026-02-15 | 20:06 | 23:59 | 233 |
| 2026-02-22 | 20:05 | 23:59 | 235 |
| 2026-03-01 | 20:05 | 23:59 | 235 |
| 2026-03-08 | 19:26 | 23:59 | 274 |
| 2026-03-15 | 19:05 | 23:59 | 295 |
| 2026-03-22 | 19:05 | 23:59 | 295 |
| 2026-03-29 | 18:05 | 23:59 | 355 |
| 2026-04-05 | 18:10 | 23:59 | 350 |
| 2026-04-12 | 18:05 | 23:59 | 355 |
| 2026-04-19 | 18:05 | 23:59 | 355 |
| 2026-04-26 | 18:05 | 23:59 | 355 |

Interpretation:

Broker-native USDJPY Sunday opens vary across the short window, with observed clusters around:

- `20:05 UTC`
- `19:05 UTC`
- `18:05 UTC`

This appears consistent with DST/session-regime shifts, but it is only a short-window observation.

It differs materially from the HistData USDJPY source-session candidate, where Sunday opens were mostly around `17:00 UTC`.

### Friday Observed Closes

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 17:55 | 1 |
| 17:58 | 3 |
| 18:58 | 3 |
| 19:58 | 6 |

Observed Fridays:

| Date | First UTC | Last UTC | Bars |
| --- | --- | --- | ---: |
| 2026-01-30 | 00:00 | 19:58 | 1199 |
| 2026-02-06 | 00:00 | 19:58 | 1199 |
| 2026-02-13 | 00:00 | 19:58 | 1199 |
| 2026-02-20 | 00:00 | 19:58 | 1199 |
| 2026-02-27 | 00:00 | 19:58 | 1199 |
| 2026-03-06 | 00:00 | 19:58 | 1199 |
| 2026-03-13 | 00:00 | 18:58 | 1139 |
| 2026-03-20 | 00:00 | 18:58 | 1139 |
| 2026-03-27 | 00:00 | 18:58 | 1139 |
| 2026-04-03 | 00:00 | 17:55 | 1076 |
| 2026-04-10 | 00:00 | 17:58 | 1079 |
| 2026-04-17 | 00:00 | 17:58 | 1079 |
| 2026-04-24 | 00:00 | 17:58 | 1079 |

Interpretation:

Broker-native USDJPY Friday closes vary across the short window, with observed clusters around:

- `19:58 UTC`
- `18:58 UTC`
- `17:58 UTC`

This differs materially from the HistData USDJPY source-session candidate, where Friday closes were mostly around `16:59 UTC`.

This is a broker mismatch topic, not a final rejection by itself.

## XAUUSD Broker Session Findings

### Sunday Observed Opens

First observed Sunday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 19:01 | 2 |
| 19:02 | 1 |
| 19:04 | 1 |
| 19:06 | 1 |
| 20:01 | 2 |
| 20:03 | 1 |
| 21:01 | 5 |
| 21:02 | 1 |

Observed Sundays:

| Date | First UTC | Last UTC | Bars |
| --- | --- | --- | ---: |
| 2026-01-25 | 21:01 | 23:59 | 177 |
| 2026-02-01 | 21:01 | 23:59 | 170 |
| 2026-02-08 | 21:02 | 23:59 | 178 |
| 2026-02-15 | 21:01 | 23:59 | 178 |
| 2026-02-22 | 21:01 | 23:59 | 179 |
| 2026-03-01 | 21:01 | 23:59 | 173 |
| 2026-03-08 | 20:03 | 23:59 | 237 |
| 2026-03-15 | 20:01 | 23:59 | 239 |
| 2026-03-22 | 20:01 | 23:59 | 239 |
| 2026-03-29 | 19:04 | 23:59 | 296 |
| 2026-04-05 | 19:01 | 23:59 | 299 |
| 2026-04-12 | 19:06 | 23:59 | 294 |
| 2026-04-19 | 19:01 | 23:59 | 298 |
| 2026-04-26 | 19:02 | 23:59 | 298 |

Interpretation:

Broker-native XAUUSD Sunday opens vary across the short window, with observed clusters around:

- `21:01 UTC`
- `20:01 UTC`
- `19:01 UTC`

This differs materially from the HistData XAUUSD source-session candidate, where Sunday opens were mostly around `18:00 UTC`.

### Friday Observed Closes

Last observed Friday HH:MM counts:

| HH:MM | Count |
| --- | ---: |
| 17:57 | 3 |
| 18:57 | 3 |
| 19:57 | 7 |

Observed Fridays:

| Date | First UTC | Last UTC | Bars |
| --- | --- | --- | ---: |
| 2026-01-23 | 00:00 | 19:57 | 1198 |
| 2026-01-30 | 00:00 | 19:57 | 1198 |
| 2026-02-06 | 00:00 | 19:57 | 1198 |
| 2026-02-13 | 00:00 | 19:57 | 1198 |
| 2026-02-20 | 00:00 | 19:57 | 1198 |
| 2026-02-27 | 00:00 | 19:57 | 1198 |
| 2026-03-06 | 00:00 | 19:57 | 1198 |
| 2026-03-13 | 00:00 | 18:57 | 1138 |
| 2026-03-20 | 00:00 | 18:57 | 1138 |
| 2026-03-27 | 00:00 | 18:57 | 1138 |
| 2026-04-10 | 00:00 | 17:57 | 1078 |
| 2026-04-17 | 00:00 | 17:57 | 1078 |
| 2026-04-24 | 00:00 | 17:57 | 1078 |

Interpretation:

Broker-native XAUUSD Friday closes vary across the short window, with observed clusters around:

- `19:57 UTC`
- `18:57 UTC`
- `17:57 UTC`

This differs materially from the HistData XAUUSD source-session candidate, where Friday closes were mostly around `16:59 UTC`.

## Broker XAUUSD Additional Missingness

Broker cross-symbol common-window analysis showed:

- USDJPY_only_missing_common_minutes: 0
- XAUUSD_only_missing_common_minutes: 5496

XAUUSD-only missing weekday-hour clusters included:

| Weekday | UTC Hour | Missing Minutes |
| ---: | ---: | ---: |
| 3 | 20 | 383 |
| 2 | 20 | 345 |
| 0 | 18 | 342 |
| 1 | 20 | 337 |
| 0 | 20 | 330 |
| 2 | 18 | 285 |
| 1 | 18 | 279 |
| 6 | 20 | 276 |
| 6 | 18 | 270 |
| 0 | 19 | 238 |
| 3 | 19 | 236 |
| 3 | 18 | 221 |
| 2 | 19 | 207 |
| 1 | 19 | 189 |
| 6 | 19 | 159 |
| 3 | 21 | 69 |

Interpretation:

In the broker short window, XAUUSD has additional symbol-specific missingness relative to USDJPY.

The clusters are mainly around UTC hours `18`, `19`, and `20`, rather than only HistData's `17:00 UTC` source-session break candidate.

This does not prove HistData is wrong, but it shows broker-session reconciliation is necessary before using HistData for H017.

## Cross-Symbol Broker Common Window

Common broker-native window:

- common_start_utc: 2026-01-26 03:09:00+00:00
- common_end_utc: 2026-04-30 07:00:00+00:00

Common-window counts:

| Metric | Value |
| --- | ---: |
| common_full_minutes | 135592 |
| USDJPY_observed_common_minutes | 97907 |
| XAUUSD_observed_common_minutes | 92411 |
| overlapping_observed_common_minutes | 92411 |
| USDJPY_missing_common_minutes | 37685 |
| XAUUSD_missing_common_minutes | 43181 |
| overlapping_missing_common_minutes | 37685 |
| USDJPY_only_missing_common_minutes | 0 |
| XAUUSD_only_missing_common_minutes | 5496 |
| USDJPY_common_observed_pct | 72.207062 |
| XAUUSD_common_observed_pct | 68.153726 |
| overlapping_observed_pct_of_common_full | 68.153726 |

Interpretation:

Within the broker common window:

1. Every USDJPY missing minute was also missing for XAUUSD.
2. XAUUSD had 5496 additional missing minutes where USDJPY had observations.
3. The overlapping observed common timeline equals XAUUSD's observed common timeline.
4. A portfolio inner join on broker M1 timestamps would be constrained by XAUUSD availability in this short window.

This is important because H017 inner-joins USDJPY and XAUUSD timestamps.

## Broker Versus HistData Provisional Comparison

### USDJPY

HistData source-session candidate:

- Sunday open mostly around `17:00 UTC`
- Friday close mostly around `16:59 UTC`

Broker short-window observation:

- Sunday opens around `20:05`, `19:05`, and `18:05 UTC`
- Friday closes around `19:58`, `18:58`, and `17:58 UTC`

Interpretation:

There is a material apparent session timing mismatch.

This may be due to broker-specific server/session rules, DST, vendor conventions, or instrument schedule definitions.

It must be investigated before any HistData acceptance decision.

### XAUUSD

HistData source-session candidate:

- Sunday open mostly around `18:00 UTC`
- Friday close mostly around `16:59 UTC`
- daily `17:00 UTC` full missing-hour candidate

Broker short-window observation:

- Sunday opens around `21:01`, `20:01`, and `19:01 UTC`
- Friday closes around `19:57`, `18:57`, and `17:57 UTC`
- XAUUSD-only missingness clusters around `18`, `19`, and `20 UTC`

Interpretation:

There is a material apparent session timing mismatch.

Broker XAUUSD also has additional symbol-specific missingness relative to USDJPY.

This must be reconciled before HistData can be used for H017 validation.

## Diagnostic Conclusions

### What this diagnostic supports

1. Current broker-native USDJPY sessions differ materially from HistData USDJPY source-session candidates.
2. Current broker-native XAUUSD sessions differ materially from HistData XAUUSD source-session candidates.
3. Current broker-native XAUUSD has additional symbol-specific missingness relative to USDJPY.
4. The broker common timeline is constrained by XAUUSD availability.
5. Broker-session reconciliation is now a major acceptance blocker for HistData.
6. The short broker window remains useful for session inference but insufficient for research validation.

### What this diagnostic does not prove

1. It does not prove HistData is unusable.
2. It does not prove HistData is acceptable.
3. It does not prove 2021-2025 HistData matches or conflicts with historical Exness sessions.
4. It does not prove current 2026 broker sessions were identical in 2021-2025.
5. It does not classify holidays or special closures.
6. It does not decide H4 construction rules.
7. It does not authorize derived HistData file creation.
8. It does not authorize H017 validation on HistData.

## Current Decision

HistData remains not accepted as a research source.

The broker mismatch assessment is now an explicit blocker.

No H017 validation on HistData is authorized.

No derived HistData files are authorized.

## Recommended Next Sub-Phase

Recommended next sub-phase:

Phase 3.26-o - Broker mismatch assessment plan

Purpose:

1. define how to assess whether HistData source sessions are compatible with the broker execution environment,
2. decide what mismatch is acceptable or unacceptable,
3. decide whether HistData can be used at all, used with exclusions, or rejected,
4. include implications for H4 construction and M1 stop-resolution,
5. keep the work documentation-first,
6. avoid H017,
7. avoid derived-data writes,
8. keep HistData unaccepted.

## Safety Confirmation

- raw_files_modified: False
- derived_files_written: False
- reusable_code_written: False
- MT5_connected: False
- H017_run: False
- HistData_accepted_as_research_source: False
- broker_short_window_only: True
- diagnostic_complete: True
