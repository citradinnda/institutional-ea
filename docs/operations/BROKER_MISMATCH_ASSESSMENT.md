# Broker Mismatch Assessment

Phase: 3.26-p

Status: Assessment complete for current evidence

Purpose: Apply the broker mismatch assessment plan to the currently available HistData source-session evidence and the 2026 broker-native short-window evidence.

This document does not accept HistData as a research source.

This document does not reject HistData permanently.

This document documents that HistData remains blocked for H017 validation under current evidence.

No H017 validation is run in this phase.

No H4 bars are built in this phase.

No derived data is written in this phase.

No raw data is modified in this phase.

## 1. Decision Summary

Current assessment result:

    HistData remains not accepted as a research source.

Current operational classification:

    HistData may remain useful for exploratory diagnostics, loader testing, coverage analysis, and source-quality investigation.

Current blocked uses:

1. H017 research validation.
2. H017 promotability claims.
3. Final performance claims.
4. Broker-equivalent H4 signal construction.
5. Broker-equivalent M1 stop-resolution.
6. Hybrid broker-H4 plus HistData-M1 validation.
7. Live-trading justification.

Current reason:

    The available evidence shows material current-session mismatch between HistData source-session candidates and the broker-native 2026 short-window behavior. The mismatch is large enough to block research validation until additional broker evidence and an H4 construction decision exist.

Important limitation:

    The broker evidence is from 2026 only, while HistData covers 2021-2025. Therefore this assessment can identify current incompatibility risk and acceptance blockers, but it cannot prove the broker's full historical 2021-2025 session behavior.

## 2. Evidence Used

### 2.1 HistData Evidence

HistData raw files are located under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

This folder name is misleading because it contains HistData files as well as earlier Dukascopy sample files.

HistData files assessed:

1. USDJPY_2021_2025_Raw_HistData.csv
2. XAUUSD_2021_2025_Raw_HistData.csv

HistData observed source format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

Dedicated loader:

    quantcore\data\histdata_loader.py

Official loader API:

    load_histdata_m1_csv(path, *, source_tz="UTC", duplicate_policy="reject")

Duplicate policy status:

1. Default behavior is strict reject.
2. Explicit opt-in `drop_exact` removes only exact duplicate OHLCV rows.
3. Conflicting duplicate timestamp groups remain fatal.
4. No raw files are modified.

### 2.2 Broker Evidence

Broker-native CSV exports are local MT5 exports under:

    C:\Users\equin\Documents\institutional-ea\data\raw

Broker timezone:

    Europe/Athens

Broker timezone interpretation:

1. Winter: UTC+2
2. Summer: UTC+3
3. DST-aware

MT5 loader API:

    load_mt5_csv(path, broker_tz="Europe/Athens")

Broker short-window evidence is from 2026 only.

MT5 was not connected during the diagnostic.

Local CSV exports were used.

H017 was not run.

HistData was not accepted.

## 3. Broker Short-Window Baseline

### 3.1 USDJPY Broker Baseline

Broker-native USDJPY M1 evidence:

- Earliest UTC: 2026-01-26 03:09:00+00:00
- Latest UTC: 2026-04-30 07:00:00+00:00
- Bars: 97,907
- Missing minutes inside symbol range: 37,685

USDJPY broker observed Sunday open clusters:

- 20:05 UTC
- 19:05 UTC
- 18:05 UTC

USDJPY broker observed Friday close clusters:

- 19:58 UTC
- 18:58 UTC
- 17:58 UTC

### 3.2 XAUUSD Broker Baseline

Broker-native XAUUSD M1 evidence:

- Earliest UTC: 2026-01-20 02:22:00+00:00
- Latest UTC: 2026-04-30 07:00:00+00:00
- Bars: 97,966
- Missing minutes inside symbol range: 46,313

XAUUSD broker observed Sunday open clusters:

- 21:01 UTC
- 20:01 UTC
- 19:01 UTC

XAUUSD broker observed Friday close clusters:

- 19:57 UTC
- 18:57 UTC
- 17:57 UTC

XAUUSD broker additional symbol-specific missingness:

- XAUUSD-only missing common minutes: 5,496
- Main UTC-hour clusters: 18, 19, 20

### 3.3 Broker Common Window

Broker common window:

- Common start UTC: 2026-01-26 03:09:00+00:00
- Common end UTC: 2026-04-30 07:00:00+00:00
- Common full minutes: 135,592
- USDJPY observed common minutes: 97,907
- XAUUSD observed common minutes: 92,411
- Overlapping observed common minutes: 92,411
- USDJPY missing common minutes: 37,685
- XAUUSD missing common minutes: 43,181
- Overlapping missing common minutes: 37,685
- USDJPY-only missing common minutes: 0
- XAUUSD-only missing common minutes: 5,496
- USDJPY common observed percent: 72.207062
- XAUUSD common observed percent: 68.153726
- Overlapping observed percent of common full minutes: 68.153726

## 4. HistData Source-Session Baseline

### 4.1 USDJPY HistData Baseline

USDJPY HistData source-session candidates:

1. Sunday opens mostly around 17:00 UTC.
2. Some Sunday open variants around 16:00, 18:00, and 19:00 UTC.
3. Friday closes mostly around 16:59 UTC.
4. Recurring Friday early-close-like observations around 15:59 UTC.
5. 2023 has abnormal 14:59 and 15:59 UTC Friday closes.
6. 2023 Sunday opens are more dispersed than other years.

### 4.2 XAUUSD HistData Baseline

XAUUSD HistData source-session candidates:

1. Sunday opens mostly around 18:00 UTC.
2. Some Sunday open variants around 17:00, 19:00, and 20:00 UTC.
3. Friday closes mostly around 16:59 UTC.
4. Early-close-like Friday outliers are present.
5. A strong recurring full missing-hour signature appears around 17:00 UTC.

XAUUSD 17:00 UTC full missing-hour counts:

- 2021: 143
- 2022: 143
- 2023: 147
- 2024: 139
- 2025: 138

The XAUUSD 17:00 UTC missing-hour signature remains a source-session candidate only.

It is not accepted as broker-equivalent behavior.

USDJPY must not inherit XAUUSD metals-session assumptions.

## 5. Mismatch Category Assessment

### 5.1 Weekly Open Mismatch

Assessment:

    Material mismatch observed under current evidence.

USDJPY comparison:

- HistData USDJPY Sunday opens mostly around 17:00 UTC.
- Broker USDJPY Sunday open clusters in the 2026 short window appear around 18:05, 19:05, and 20:05 UTC.

XAUUSD comparison:

- HistData XAUUSD Sunday opens mostly around 18:00 UTC.
- Broker XAUUSD Sunday open clusters in the 2026 short window appear around 19:01, 20:01, and 21:01 UTC.

Interpretation:

1. The current broker opens appear later than the dominant HistData source-session candidates.
2. The mismatch is not a few seconds or a single missing minute.
3. The mismatch is large enough to affect weekly open H4 bars.
4. The mismatch is large enough to affect first-session M1 stop-resolution.
5. The mismatch is a blocker for broker-equivalent validation.

Current status:

    Blocking.

Reason for blocking status:

    H017 signals and event execution depend on H4 timestamp structure and M1 availability. Weekly open mismatch can change both.

### 5.2 Weekly Close Mismatch

Assessment:

    Material mismatch observed under current evidence.

USDJPY comparison:

- HistData USDJPY Friday closes mostly around 16:59 UTC, with recurring early-close-like observations.
- Broker USDJPY Friday close clusters in the 2026 short window appear around 17:58, 18:58, and 19:58 UTC.

XAUUSD comparison:

- HistData XAUUSD Friday closes mostly around 16:59 UTC, with early-close-like outliers.
- Broker XAUUSD Friday close clusters in the 2026 short window appear around 17:57, 18:57, and 19:57 UTC.

Interpretation:

1. The current broker closes appear later than the dominant HistData source-session candidates.
2. Friday close behavior affects final weekly H4 bars.
3. Friday close behavior affects whether M1 stop-resolution windows are tradeable.
4. This mismatch could alter weekend exposure assumptions and forced-close behavior.

Current status:

    Blocking.

Reason for blocking status:

    H017 cannot rely on a source that closes materially earlier than the current broker without an explicit H4 and M1 alignment rule.

### 5.3 Daily Break Mismatch

Assessment:

    Material unresolved mismatch, especially for XAUUSD.

HistData XAUUSD evidence:

- Strong recurring 17:00 UTC full missing-hour signature.
- Counts are stable across 2021-2025, but stability alone does not prove broker equivalence.

Broker XAUUSD evidence:

- Additional XAUUSD-only missingness relative to USDJPY.
- XAUUSD-only missingness clusters mainly around UTC hours 18, 19, and 20 in the 2026 short window.

Interpretation:

1. XAUUSD has symbol-specific session behavior in both sources.
2. The hour signatures do not currently align cleanly.
3. The observed broker window suggests the current broker's XAUUSD break behavior may be shifted relative to HistData.
4. This matters directly for stop and take-profit detection.

Current status:

    Blocking.

Reason for blocking status:

    XAUUSD daily-break mismatch can create false fills, missed fills, or incorrect no-fill outcomes in M1 stop-resolution.

### 5.4 DST and Session-Regime Mismatch

Assessment:

    Unresolved and potentially material.

HistData duplicate timestamp evidence:

Exact duplicate timestamp blocks appear annually around late October:

- 2021-10-31 19:00 through 19:59
- 2022-10-30 19:00 through 19:59
- 2023-10-29 19:00 through 19:59
- 2024-10-27 19:00 through 19:59
- 2025-10-26 19:00 through 19:59

Duplicate characteristics:

1. Each duplicated timestamp has exactly two rows.
2. Duplicate groups are identical across OHLCV.
3. No conflicting duplicate timestamp groups were observed.
4. The pattern is consistent with a daylight-saving-time-related duplicate hour.
5. This is an observation, not acceptance.

Broker evidence:

The broker timezone is Europe/Athens and DST-aware.

The 2026 short window is not enough to fully characterize 2021-2025 DST behavior.

Interpretation:

1. HistData contains a recurring annual duplicate-hour feature.
2. The loader can safely drop exact duplicates only by explicit opt-in.
3. A duplicate-hour policy does not solve broker-equivalence.
4. DST behavior can move H4 boundaries and session windows.
5. Broker historical DST behavior remains unproven for 2021-2025.

Current status:

    Blocking until H4 construction and DST alignment are decided.

### 5.5 Symbol-Specific Missingness Mismatch

Assessment:

    Material unresolved mismatch.

Broker evidence:

1. USDJPY-only missing common minutes: 0
2. XAUUSD-only missing common minutes: 5,496
3. XAUUSD-only missingness clusters mainly around UTC hours 18, 19, and 20

HistData evidence:

1. XAUUSD has a strong recurring 17:00 UTC daily break candidate.
2. USDJPY does not have the same metals daily-break pattern.
3. March-July 2023 contains abnormal missingness affecting both symbols.
4. March-July 2023 also contains symbol-specific and suspicious unclassified gap buckets.

Interpretation:

1. XAUUSD cannot be treated as having the same session as USDJPY.
2. Source-specific missingness affects portfolio alignment.
3. Symbol-specific missingness can distort H017 heat-governor state.
4. Current evidence is not sufficient to declare the HistData missingness broker-compatible.

Current status:

    Blocking.

### 5.6 Cross-Symbol Alignment Mismatch

Assessment:

    Material unresolved mismatch.

H017 uses both USDJPY and XAUUSD.

H017 inner-joins timestamps.

Broker common-window evidence shows that XAUUSD constrains the overlapping observed timeline.

Broker common-window facts:

- USDJPY observed common minutes: 97,907
- XAUUSD observed common minutes: 92,411
- Overlapping observed common minutes: 92,411
- XAUUSD-only missing common minutes: 5,496

Interpretation:

1. XAUUSD availability constrains the two-symbol broker timeline.
2. HistData cross-symbol alignment must be assessed against broker behavior before use.
3. If HistData creates a different common timeline, H017's return stream, volatility targeting, and heat governor can differ materially.
4. A higher sample size from HistData would not automatically be better if the sample is not broker-compatible.

Current status:

    Blocking.

### 5.7 H4 Boundary Mismatch

Assessment:

    Critical unresolved blocker.

Current fact:

    No H4 construction decision has been made.

Risk:

    HistData M1 source sessions and broker-native sessions appear materially different under current evidence.

Therefore, H4 bars built from HistData M1 may not match broker-native H4 bars.

H017 depends on H4 bars for:

1. Donchian breakout signals.
2. ATR.
3. Chandelier exits.
4. Realized volatility.
5. Heat-governor inputs.
6. Entry timing.
7. Exit timing.

Interpretation:

1. H4 signal construction cannot proceed from HistData until boundary rules are explicitly decided.
2. Broker-native H4 bars and HistData-built H4 bars must not be silently mixed.
3. A hybrid-source design would require a separate decision record.
4. H4 mismatch alone is enough to keep H017 blocked.

Current status:

    Blocking.

### 5.8 Stop-Resolution M1 Coverage Mismatch

Assessment:

    Critical unresolved blocker.

Phase 3 event-driven backtesting requires M1 bars inside H4 execution windows.

Existing fill convention:

    If stop and take-profit are both touched in the same M1 bar, stop wins.

That conservative rule handles intrabar ordering ambiguity.

It does not solve source-session mismatch.

Risk cases:

1. HistData has M1 bars during intervals where the broker would not trade.
2. HistData lacks M1 bars during intervals where the broker would trade.
3. HistData has a daily break at a different UTC hour than the broker.
4. HistData weekly opens differ from broker weekly opens.
5. HistData weekly closes differ from broker weekly closes.
6. HistData holiday closures differ from broker holiday closures.

Interpretation:

1. Stop-resolution is directly sensitive to M1 availability.
2. A session mismatch can alter whether stops or take-profits appear to be hit.
3. This can change fills, P&L, drawdown, Sharpe, PSR, MinTRL, and DSR.
4. HistData cannot be used for H017 stop-resolution until compatibility is proven or restrictions are defined.

Current status:

    Blocking.

### 5.9 Holiday and Special-Closure Mismatch

Assessment:

    Unresolved blocker.

Known issue:

    March-July 2023 was materially abnormal for both symbols.

Zero-bar weekday candidate:

    2023-04-07

Current provisional classification:

    Holiday full-close candidate, not accepted.

March-July 2023 candidate classification includes:

1. Cross-symbol source outage candidates.
2. Symbol-specific source defect candidates.
3. Holiday early-close candidates.
4. Holiday full-close candidates.
5. Suspicious unclassified gaps.
6. Normal weekend provisional gaps.
7. XAUUSD daily session-break candidates.

Interpretation:

1. Some missingness may be legitimate holiday behavior.
2. Some missingness may be source outage behavior.
3. Some missingness remains suspicious and unclassified.
4. The 2023 anomaly cannot be treated as harmless.
5. Holiday classification remains necessary before validation.

Current status:

    Blocking.

## 6. Acceptability Assessment

### 6.1 Accepted Mismatches

None.

No mismatch category is currently accepted as harmless.

### 6.2 Conditionally Acceptable Candidates

The following may become conditionally acceptable later, but are not accepted now:

1. XAUUSD recurring daily break behavior, if broker specifications or additional broker exports confirm equivalent behavior.
2. Exact duplicate HistData rows around autumn DST transitions, if explicit `drop_exact` policy is used and H4 boundaries remain valid.
3. Holiday full-close and early-close periods, if independently confirmed and excluded or modeled explicitly.
4. Limited use of HistData for exploratory diagnostics.

Current status:

    Diagnostic use only.

### 6.3 Unacceptable For Current H017 Validation

Under current evidence, the following are unacceptable for H017 validation:

1. Weekly open mismatch.
2. Weekly close mismatch.
3. XAUUSD daily-break mismatch.
4. Unresolved DST/session-regime mismatch.
5. Symbol-specific missingness mismatch.
6. Cross-symbol alignment mismatch.
7. H4 boundary uncertainty.
8. M1 stop-resolution coverage uncertainty.
9. Holiday and special-closure uncertainty.
10. March-July 2023 anomaly uncertainty.

## 7. Current Outcome Classification

Current outcome:

    Use HistData only for exploratory diagnostics until further evidence exists.

Explicitly allowed for now:

1. Loader tests.
2. Coverage diagnostics.
3. Source-session diagnostics.
4. Duplicate-policy diagnostics.
5. Gap classification diagnostics.
6. Documentation and decision planning.

Explicitly not allowed for now:

1. H017 validation.
2. Promotability claims.
3. H4 signal construction for validation.
4. M1 stop-resolution for validation.
5. Derived research dataset creation.
6. Silent source mixing.
7. Parameter tuning.
8. Cost-model changes.
9. Live-trading decisions.

## 8. Required Additional Evidence Before Any Source Acceptance

### 8.1 Broker Symbol Specification Evidence

Required if available from MT5 or broker documentation:

1. Broker server timezone.
2. USDJPY trading sessions.
3. XAUUSD trading sessions.
4. XAUUSD daily break schedule.
5. Weekend open and close schedule.
6. Holiday schedule behavior.
7. Contract size.
8. Tick size.
9. Tick value.
10. Digits.
11. Minimum lot.
12. Lot step.
13. Spread metadata if available.

### 8.2 Additional Broker Data Exports

Useful additional broker exports:

1. More USDJPY M1 history.
2. More XAUUSD M1 history.
3. Broker-native USDJPY H4.
4. Broker-native XAUUSD H4.
5. DST transition weeks.
6. Good Friday weeks.
7. Christmas and New Year weeks.
8. Normal control weeks.
9. Weeks around known Friday early closes.
10. Weeks around broker maintenance windows.

Minimum next broker export targets if available:

1. One spring DST transition window.
2. One autumn DST transition window.
3. One ordinary non-holiday month.
4. One holiday-heavy period.
5. One XAUUSD-focused daily-break sample window.

### 8.3 H4 Boundary Evidence

Before HistData can be used for signal construction, constructed HistData H4 bars must be compared against broker-native H4 bars.

Required comparisons:

1. Timestamp boundaries.
2. Open.
3. High.
4. Low.
5. Close.
6. Missing bars.
7. Extra bars.
8. Weekly open bars.
9. Weekly close bars.
10. XAUUSD daily-break-adjacent bars.
11. DST transition bars.
12. Holiday bars.

No H4 construction rule is accepted in this document.

## 9. Implications For H017

H017 remains:

1. Alive.
2. Not promotable.
3. Not ready for live trading.
4. Blocked by insufficient research-grade M1 history.
5. Blocked by source-acceptance uncertainty.
6. Not authorized for HistData validation.

Existing broker-native short-window result remains a pipeline smoke result only:

- Fills: 470
- Starting equity: 10000.00 USD
- Ending equity: 16145.60 USD
- Total return: 61.46 percent
- Max drawdown: -33.65 percent
- Annualized Sharpe: 1.3218

Existing claim result:

- PSR: 0.8662
- Threshold: 0.95
- MinTRL feasible: True
- MinTRL required n: 1034
- MinTRL observed n: 470
- DSR: Skipped
- H017 promotable: False

Interpretation:

1. The event-driven pipeline works.
2. The broker-native M1 window is too short.
3. The positive short-window result is not validated edge.
4. The -33.65 percent drawdown remains a serious risk signal.
5. HistData cannot be used to bypass the evidence gap.

## 10. Assessment Verdict

Verdict:

    HistData remains blocked for H017 validation.

Current source status:

    Not accepted.

Current allowed status:

    Exploratory diagnostics only.

Reason:

    Current evidence shows material mismatch between HistData source-session candidates and the broker-native 2026 short-window behavior. The mismatch affects weekly opens, weekly closes, XAUUSD daily breaks, cross-symbol alignment, H4 boundary construction, and M1 stop-resolution reliability.

Important caveat:

    The 2026 broker short-window evidence does not prove the broker's full 2021-2025 historical behavior. It does, however, establish enough current broker mismatch risk to block acceptance until more broker evidence and an H4 construction decision exist.

## 11. Recommended Next Phase

Recommended next phase:

    Phase 3.26-q - H4 construction decision plan

Purpose:

1. Define possible H4 construction choices.
2. Decide what evidence is needed to compare broker-native H4 bars with M1-built H4 bars.
3. Prevent silent mixing of HistData M1 and broker H4.
4. Define whether a hybrid-source design could ever be acceptable.
5. Keep HistData unaccepted.
6. Keep H017 blocked.
7. Avoid writing derived data until a source and construction decision exist.

## 12. Non-Actions In This Phase

This phase did not:

1. Accept HistData.
2. Permanently reject HistData.
3. Run H017.
4. Build H4 bars.
5. Write derived data.
6. Modify raw data.
7. Modify the HistData loader.
8. Modify the MT5 loader.
9. Modify duplicate handling.
10. Modify `.gitignore`.
11. Change the cost model.
12. Tune strategy parameters.
13. Broaden the symbol universe.
14. Add machine learning.
15. Start Phase 4 execution work.
