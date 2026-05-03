# Broker-Native Expanded Session and Common-Window Diagnostic Plan

Phase: 3.26-af  
Status: Plan only  
Scope: Expanded broker-native USDJPY and XAUUSD M1/H4 source-acceptance diagnostics  
Created after: HANDOFF_28 and expanded broker-native H4/M1 aggregation compatibility diagnostic

## Purpose

This document defines the remaining broker-native source-acceptance diagnostics that must be completed before any H017 validation run is authorized on the expanded broker-native M1 files.

The expanded broker-native M1 files are promising, but they are not yet formally accepted as an H017 validation source.

This phase is intentionally documentation-only.

No H017 run is authorized by this document.

No derived datasets are authorized by this document.

No raw broker files may be modified by this document.

## Current Source State

Broker: Exness  
Reported account environment: Demo  
Reported server: MT5  
Broker timezone used by loader: Europe/Athens

Raw broker-native files are local and gitignored under:

- data/raw/USDJPY/H4.csv
- data/raw/USDJPY/M1.csv
- data/raw/XAUUSD/H4.csv
- data/raw/XAUUSD/M1.csv

These raw files must not be committed.

The accepted H4 reference for broker-aligned diagnostics is broker-native H4.

The expanded broker-native M1 source is a candidate source only.

HistData remains rejected for H017 validation under current evidence.

## Established Findings Before This Plan

The expanded broker-native raw inventory established local files for USDJPY and XAUUSD H4/M1.

The expanded loader timestamp-shape diagnostic established that the loader can parse the files with no duplicate timestamps after load.

The expanded M1 coverage-density diagnostic established that both symbols have a sparse daily-like prefix from 2018 through 2021-06.

The dense M1 candidate region starts at 2021-07 for both USDJPY and XAUUSD.

The expanded H4/M1 aggregation compatibility diagnostic established that broker-native M1 aggregation exactly reproduces broker-native H4 OHLCV on all fully covered comparable H4 windows:

- USDJPY: 5701 matched bars, 0 mismatched bars
- XAUUSD: 6149 matched bars, 0 mismatched bars

The first full comparable H4/M1 window is:

- 2021-07-02 13:00:00 UTC for USDJPY
- 2021-07-02 13:00:00 UTC for XAUUSD

These results are strong but not sufficient for formal source acceptance.

## Non-Acceptance Statement

The expanded broker-native M1 source is not accepted yet.

Broker-native H4/M1 aggregation alignment proves internal compatibility on complete windows.

It does not prove that the M1 history is sufficient for H017 validation.

The following still need to be understood before source acceptance:

1. Session boundaries.
2. Weekend and daily break behavior.
3. DST transition behavior.
4. Cross-symbol common-window coverage.
5. Missingness by time bucket.
6. Whether the usable dense region is long enough and clean enough for H017 validation.

## Dense Region Boundary Rule

The sparse prefix must not be used for H017 validation.

The following period is not dense M1 history and must not be treated as such:

- 2018 through 2021-06

The candidate dense region begins at:

- 2021-07

Future diagnostics should focus on the dense candidate region, with special attention to the first fully comparable H4/M1 window:

- 2021-07-02 13:00:00 UTC

Any future H017 validation window, if eventually authorized, must exclude the sparse prefix.

## Planned Diagnostic 1: Session-Boundary Analysis

Purpose:

Confirm that observed M1 bars are consistent with expected broker session behavior for USDJPY and XAUUSD.

Questions to answer:

1. What are the typical Sunday open times in UTC?
2. What are the typical Friday close times in UTC?
3. Are there broker-specific early opens or early closes?
4. Does XAUUSD show expected daily trading breaks?
5. Are USDJPY and XAUUSD breaks structurally different?
6. Are gaps consistent across years?
7. Are holiday closures visible and plausible?
8. Are DST transitions handled cleanly after Europe/Athens conversion to UTC?

Required output should include, at minimum:

1. First observed minute by symbol, date, and UTC weekday.
2. Last observed minute by symbol, date, and UTC weekday.
3. Observed minutes by UTC weekday and UTC hour.
4. Gap distribution by symbol.
5. Largest gaps by symbol.
6. Recurring daily break windows, especially for XAUUSD.
7. Sunday open summary by year and month.
8. Friday close summary by year and month.
9. DST transition spot checks.

Expected interpretation standard:

Session gaps are not automatically defects.

They become defects only if they contradict expected broker/instrument trading behavior or create unexplained holes inside active sessions.

## Planned Diagnostic 2: Cross-Symbol Common-Window Analysis

Purpose:

Determine the common usable M1 window across USDJPY and XAUUSD.

Questions to answer:

1. What is the first timestamp where both symbols have dense M1 candidate coverage?
2. What is the last timestamp where both symbols have M1 coverage?
3. How many observed M1 timestamps are shared by both symbols?
4. How many observed M1 timestamps are USDJPY-only?
5. How many observed M1 timestamps are XAUUSD-only?
6. How much missingness is explained by normal instrument-session differences?
7. What common H4 decision windows have complete M1 coverage for both symbols?

Required output should include, at minimum:

1. Common dense start timestamp.
2. Common dense end timestamp.
3. Per-symbol observed minute counts inside the common dense span.
4. Intersection count of observed minutes.
5. USDJPY-only minute count.
6. XAUUSD-only minute count.
7. Neither-symbol calendar-minute count, if a calendar grid is used.
8. Shared complete H4/M1 windows.
9. Symbol-specific incomplete H4/M1 windows.
10. Common complete H4/M1 windows suitable for a future bridge-layer validation, if source acceptance is later granted.

Expected interpretation standard:

The H017 portfolio bridge uses both symbols.

Therefore, source acceptance must reason about the common usable window, not just each symbol independently.

## Planned Diagnostic 3: Missingness by Time Bucket

Purpose:

Quantify missingness patterns in the dense candidate region.

Questions to answer:

1. Is missingness mostly explained by weekends, daily breaks, and holidays?
2. Are there unexplained holes inside active sessions?
3. Are missing minutes concentrated in particular years?
4. Are missing minutes concentrated in particular months?
5. Are missing minutes concentrated around certain UTC hours?
6. Are missing minutes concentrated around DST transitions?
7. Are there asymmetric symbol-specific outages?

Required output should include, at minimum:

1. Missingness by symbol and year.
2. Missingness by symbol and month.
3. Missingness by symbol and UTC weekday.
4. Missingness by symbol and UTC hour.
5. Missingness by symbol, UTC weekday, and UTC hour.
6. Top gap clusters by symbol.
7. Top dates by missing observed minutes during expected active sessions, if such an expected-session mask is defined.

Expected interpretation standard:

Calendar density alone is not sufficient because legitimate market closures reduce calendar-minute coverage.

The diagnostic should distinguish structural sessions from unexplained gaps as much as possible.

## Planned Diagnostic 4: DST Behavior Review

Purpose:

Confirm that Europe/Athens timezone conversion does not create incorrect UTC session artifacts.

Questions to answer:

1. Do UTC session boundaries shift as expected around European DST transitions?
2. Are there duplicated UTC timestamps around fall-back transitions?
3. Are there missing or malformed timestamps around spring-forward transitions?
4. Do H4 boundaries remain internally compatible with M1 aggregation across DST transitions?
5. Are the observed changes consistent between USDJPY and XAUUSD?

Required output should include, at minimum:

1. DST transition dates inspected.
2. Windowed minute counts around each transition.
3. H4/M1 aggregation spot checks around selected transitions.
4. Duplicate timestamp checks after load.
5. Any anomalous gaps or bars.

Expected interpretation standard:

DST-related UTC shifts may be normal.

Duplicate timestamps, malformed bars, or aggregation failures would require further investigation.

## Planned Diagnostic 5: Source-Acceptance Checkpoint

Purpose:

Create an explicit decision document after the planned diagnostics are complete.

The checkpoint must decide whether expanded broker-native M1 is accepted, rejected, or conditionally accepted for H017 validation.

The checkpoint must not be implicit.

Required decision states:

1. Accepted for H017 validation.
2. Conditionally accepted for H017 validation with a restricted window.
3. Rejected for H017 validation.
4. Deferred pending more evidence.

The checkpoint must specify:

1. Accepted symbols.
2. Accepted timeframe.
3. Accepted UTC start timestamp.
4. Accepted UTC end timestamp.
5. Excluded sparse prefix.
6. Excluded gap windows, if any.
7. Whether H4/M1 aggregation compatibility is sufficient within the accepted region.
8. Whether session behavior is acceptable.
9. Whether cross-symbol common-window coverage is acceptable.
10. Whether H017 validation is authorized after the checkpoint.

## Explicit H017 Restriction

H017 must not be run during these diagnostics.

H017 must not be run on HistData.

H017 must not be run on expanded broker-native M1 until a later source-acceptance checkpoint explicitly authorizes it.

No strategy tuning is authorized.

No cost-model changes are authorized.

No live trading or Phase 4 execution work is authorized.

## Raw and Derived Data Restrictions

Raw broker-native files must not be modified.

Raw broker-native files must not be committed.

Raw HistData files must not be modified.

Raw HistData files must not be committed.

No derived M1 datasets may be written before explicit authorization.

No derived H4 datasets may be written before explicit authorization.

No large derived files may be committed without an explicit plan.

## Proposed Future Sequence

Recommended next sequence after this plan:

1. Expanded broker-native session-boundary diagnostic.
2. Expanded broker-native cross-symbol common-window diagnostic.
3. Expanded broker-native missingness-by-time-bucket diagnostic.
4. Expanded broker-native DST behavior review, if not already covered by the session diagnostic.
5. Expanded broker-native source-acceptance checkpoint.
6. Only if explicitly accepted, consider a later H017 validation phase.

## Current Verdict

The expanded broker-native data is promising.

The sparse 2018 through 2021-06 prefix remains excluded from any future validation thinking.

The dense candidate region begins at 2021-07.

The exact H4/M1 aggregation match on all fully covered windows is strong evidence of internal consistency.

However, source acceptance remains blocked until session behavior and cross-symbol common-window coverage are explicitly diagnosed and documented.

H017 remains alive but not promotable.

Research validation remains blocked.

Live trading remains unauthorized.
