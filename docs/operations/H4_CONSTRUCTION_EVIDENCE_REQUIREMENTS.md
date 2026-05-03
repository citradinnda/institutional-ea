# H4 Construction Evidence Requirements

Phase: 3.26-r

Status: Requirements only

Purpose: Define the compact evidence required before deciding whether H4 bars can be built from HistData M1, broker-native H4, another source, or a documented hybrid design.

This document does not accept HistData as a research source.

This document does not reject HistData permanently.

This document does not build H4 bars.

This document does not write derived data.

This document does not run H017.

This document does not authorize H017 validation on HistData.

This document does not implement diagnostics.

## 1. Current Decision State

HistData remains not accepted as a research source.

H017 remains alive but not promotable.

H017 remains blocked for validation.

The current accepted use of HistData is:

    Exploratory diagnostics only.

The current H4 construction decision is:

    No H4 construction method is accepted yet.

The previous phase documented possible H4 construction options:

1. Broker-native H4 for signals only.
2. HistData-built H4 for signals and M1 stop-resolution.
3. Hybrid broker-native H4 signals plus HistData M1 stop-resolution.
4. Reject HistData for H4 and M1 validation.

No option has been accepted.

This phase defines the evidence required before any option can be accepted or rejected responsibly.

## 2. Core Evidence Question

The core evidence question is:

    Can candidate H4 bars be shown to match, or be explicitly and safely reconciled with, broker-native H4 behavior closely enough for H017 research validation?

This question must be answered separately for:

1. USDJPY.
2. XAUUSD.
3. Ordinary trading weeks.
4. Weekly opens.
5. Weekly closes.
6. DST transition periods.
7. Holiday and special-closure periods.
8. XAUUSD daily-break-adjacent periods.
9. Cross-symbol common timestamps.
10. H017 indicator sensitivity.

A candidate H4 method cannot be accepted just because it produces bars.

It must produce bars that are compatible with the intended execution environment.

## 3. Evidence Sources

### 3.1 Broker-Native H4 Exports

Broker-native H4 exports are required because they are the closest available representation of the broker chart used for H017 signals.

Expected local raw paths include:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv

These files are raw data.

They are gitignored.

They must not be committed.

Required broker H4 evidence:

1. Earliest UTC timestamp.
2. Latest UTC timestamp.
3. Number of H4 bars.
4. Timestamp distribution.
5. Weekly open bar timestamps.
6. Weekly close bar timestamps.
7. Missing H4 bars.
8. Extra or irregular H4 bars.
9. DST-adjacent bar behavior.
10. Holiday-adjacent bar behavior.
11. XAUUSD daily-break-adjacent bar behavior.

### 3.2 Broker-Native M1 Exports

Broker-native M1 exports remain useful for checking how broker H4 bars relate to broker M1 sessions.

Expected local raw paths include:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

These files are raw data.

They are gitignored.

They must not be committed.

Required broker M1 evidence:

1. M1 coverage inside broker H4 bars.
2. Missing M1 minutes inside broker H4 intervals.
3. Weekly open M1 behavior.
4. Weekly close M1 behavior.
5. XAUUSD daily-break behavior.
6. DST transition behavior if covered.
7. Holiday and special-closure behavior if covered.

### 3.3 HistData M1 Files

HistData raw files are currently under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

This folder name is misleading because it contains HistData files as well as earlier Dukascopy sample files.

Current HistData files:

1. USDJPY_2021_2025_Raw_HistData.csv
2. XAUUSD_2021_2025_Raw_HistData.csv

These files are raw data.

They are gitignored.

They must not be modified.

They must not be committed.

Dedicated HistData loader:

    quantcore\data\histdata_loader.py

Official loader API:

    load_histdata_m1_csv(path, *, source_tz="UTC", duplicate_policy="reject")

Default duplicate policy:

    duplicate_policy="reject"

Explicit opt-in exact duplicate policy:

    duplicate_policy="drop_exact"

HistData must not be silently deduplicated.

Any use of `drop_exact` must be explicit and documented.

## 4. Required API Inspection Before Any Future Diagnostic Code

Before writing any future code that calls existing project functions, inspect actual APIs.

Required checks:

1. Inspect `load_mt5_csv`.
2. Inspect `load_histdata_m1_csv`.
3. Inspect MT5 result dataclass fields.
4. Inspect HistData result dataclass fields.
5. Inspect any existing coverage or preflight helpers before reuse.

Required PowerShell pattern:

    @'
    import inspect
    import dataclasses

    from quantcore.data.mt5_loader import load_mt5_csv
    from quantcore.data.histdata_loader import load_histdata_m1_csv, HistDataM1LoadResult
    from quantcore.data.mt5_loader import MT5LoadResult

    print("load_mt5_csv:", inspect.signature(load_mt5_csv))
    print("load_histdata_m1_csv:", inspect.signature(load_histdata_m1_csv))

    print("MT5LoadResult fields:")
    for field in dataclasses.fields(MT5LoadResult):
        print(" ", field.name)

    print("HistDataM1LoadResult fields:")
    for field in dataclasses.fields(HistDataM1LoadResult):
        print(" ", field.name)
    '@ | python -

Do not use Linux or macOS heredoc syntax.

Do not trust remembered function names or keyword names.

## 5. Required Compact Comparison Windows

Future diagnostics should start with small, read-only windows.

They should not create full derived datasets.

### 5.1 Broker Short-Window Common Period

Use the known broker common period:

    2026-01-26 03:09:00+00:00 through 2026-04-30 07:00:00+00:00

Purpose:

1. Compare broker H4 timestamps against broker M1 coverage.
2. Identify broker H4 partial bars.
3. Identify broker weekly open and close behavior.
4. Identify XAUUSD-only missingness effects.
5. Establish current broker behavior without overclaiming historical equivalence.

Limitation:

    HistData covers 2021-2025, so this 2026 window cannot directly compare HistData prices.

### 5.2 Ordinary Control Weeks

Required ordinary control weeks should avoid:

1. Major holidays.
2. DST transitions.
3. Known early closes.
4. Known source anomalies.
5. Year-end periods.

Purpose:

1. Establish normal H4 boundary behavior.
2. Establish normal M1-to-H4 aggregation expectations.
3. Compare USDJPY and XAUUSD alignment under ordinary conditions.

### 5.3 Spring DST Transition Windows

Required if broker historical exports or alternative evidence are available.

Purpose:

1. Detect one-hour shifts.
2. Check H4 timestamp continuity.
3. Check weekly open and close changes.
4. Check whether broker and vendor sessions shift together or separately.

### 5.4 Autumn DST Transition Windows

Required because HistData has recurring duplicate timestamp blocks around late October.

Known HistData duplicate timestamp blocks:

1. 2021-10-31 19:00 through 19:59.
2. 2022-10-30 19:00 through 19:59.
3. 2023-10-29 19:00 through 19:59.
4. 2024-10-27 19:00 through 19:59.
5. 2025-10-26 19:00 through 19:59.

Purpose:

1. Confirm duplicate handling implications.
2. Confirm H4 aggregation behavior around duplicate hours.
3. Confirm whether `drop_exact` is safe for H4 construction.
4. Confirm whether candidate H4 bars remain broker-compatible.

### 5.5 Good Friday And Easter Windows

Known zero-bar weekday candidate:

    2023-04-07

Current provisional classification:

    Holiday full-close candidate, not accepted.

Purpose:

1. Distinguish legitimate holiday closure from source outage.
2. Compare holiday behavior across symbols.
3. Determine whether affected windows should be excluded or modeled.
4. Prevent false validation from source defects.

### 5.6 Christmas And New Year Windows

Purpose:

1. Check year-end closures.
2. Check early closes.
3. Check late opens.
4. Check partial H4 bars.
5. Check symbol-specific differences.
6. Check whether weekend and holiday behavior interact.

### 5.7 March-July 2023 Anomaly Windows

March-July 2023 remains materially abnormal in HistData for both symbols.

Purpose:

1. Determine whether H4 construction would be corrupted by missing M1 bars.
2. Determine whether the anomaly affects signal-generation bars.
3. Determine whether M1 stop-resolution windows are incomplete.
4. Determine whether affected periods require exclusion or source rejection.

Current status:

    Blocking.

No diagnostic should treat this period as harmless without evidence.

## 6. Required Output Fields For Future H4 Comparison Diagnostics

A future compact diagnostic should report at least these fields per symbol and per comparison window.

### 6.1 Source Metadata

Required fields:

1. symbol
2. source_name
3. raw_file_path
4. loader_name
5. loader_options
6. duplicate_policy
7. source_timezone
8. broker_timezone
9. n_input_rows
10. n_loaded_bars
11. earliest_utc
12. latest_utc

### 6.2 H4 Timestamp Comparison

Required fields:

1. candidate_h4_timestamp
2. broker_h4_timestamp
3. timestamp_match
4. timestamp_delta_minutes
5. candidate_only_h4_count
6. broker_only_h4_count
7. overlapping_h4_count
8. first_mismatch_utc
9. last_mismatch_utc

### 6.3 OHLC Comparison

Required fields for overlapping H4 timestamps:

1. open_candidate
2. open_broker
3. open_abs_diff
4. high_candidate
5. high_broker
6. high_abs_diff
7. low_candidate
8. low_broker
9. low_abs_diff
10. close_candidate
11. close_broker
12. close_abs_diff
13. max_ohlc_abs_diff

### 6.4 M1 Completeness Inside H4 Bars

Required fields:

1. h4_timestamp
2. h4_window_start_utc
3. h4_window_end_utc
4. expected_m1_minutes
5. observed_m1_minutes
6. missing_m1_minutes
7. missing_m1_pct
8. first_missing_m1_utc
9. last_missing_m1_utc
10. missing_minutes_in_known_nontradeable_window
11. missing_minutes_unexplained

### 6.5 Session-Specific Flags

Required flags:

1. is_weekly_open_bar
2. is_weekly_close_bar
3. is_dst_transition_bar
4. is_holiday_candidate_bar
5. is_special_closure_candidate_bar
6. is_xauusd_daily_break_adjacent_bar
7. is_march_july_2023_anomaly_bar
8. is_partial_bar_candidate

### 6.6 H017 Indicator Sensitivity Fields

Future diagnostics should report whether H4 differences could alter H017 indicators.

Required fields:

1. donchian_signal_changed
2. atr_changed
3. chandelier_exit_changed
4. close_to_close_return_changed
5. realized_vol_changed
6. heat_governor_input_changed
7. entry_timing_changed
8. exit_timing_changed

No strategy validation should be run during the evidence-requirements phase.

These fields are requirements for a later diagnostic, not an implementation in this phase.

## 7. Required Acceptance Gates

No H4 construction method can be accepted until the following gates are passed or explicitly waived in a decision record.

### 7.1 Gate 1 - Source Provenance

Required:

1. Raw files inventoried.
2. Hashes recorded where applicable.
3. File paths documented.
4. Source format documented.
5. Timezone assumption documented.
6. Duplicate policy documented.
7. Raw files preserved unchanged.

Current status:

    Partially complete for HistData.

### 7.2 Gate 2 - Session Compatibility

Required:

1. Weekly open behavior assessed.
2. Weekly close behavior assessed.
3. Daily breaks assessed.
4. DST behavior assessed.
5. Holiday behavior assessed.
6. Symbol-specific missingness assessed.
7. Cross-symbol alignment assessed.

Current status:

    Not passed.

Reason:

    Broker mismatch assessment found material current-session mismatch risk.

### 7.3 Gate 3 - H4 Boundary Compatibility

Required:

1. Candidate H4 timestamps compared against broker-native H4 timestamps.
2. Candidate H4 OHLC compared against broker-native H4 OHLC.
3. Ordinary weeks compared.
4. Weekly open and close weeks compared.
5. DST weeks compared if available.
6. Holiday weeks compared if available.
7. XAUUSD daily-break-adjacent windows compared.
8. Mismatches classified.

Current status:

    Not passed.

### 7.4 Gate 4 - M1 Stop-Resolution Compatibility

Required:

1. Candidate M1 coverage checked inside execution windows.
2. Missing M1 minutes classified.
3. Extra non-broker-tradeable M1 minutes identified.
4. Daily breaks reconciled.
5. Weekly opens reconciled.
6. Weekly closes reconciled.
7. Holidays reconciled.
8. DST behavior reconciled.

Current status:

    Not passed.

### 7.5 Gate 5 - Statistical Sufficiency After Exclusions

Required if any exclusions are applied:

1. Exclusion windows documented.
2. Remaining sample size counted.
3. Fill count recomputed.
4. PSR applicability reassessed.
5. MinTRL observed count reassessed.
6. DSR applicability reassessed.
7. Drawdown assessed.
8. Tail behavior assessed.

Current status:

    Not evaluated.

Reason:

    H017 must not be run yet.

## 8. Explicit Non-Requirements For The Next Diagnostic

The next diagnostic does not need to solve everything.

It should not attempt full validation.

The next diagnostic should not:

1. Run H017.
2. Build full 2021-2025 derived H4 datasets.
3. Write parquet, CSV, or database outputs.
4. Modify raw files.
5. Modify loader behavior.
6. Add silent deduplication.
7. Tune strategy parameters.
8. Change cost model assumptions.
9. Broaden the symbol universe.
10. Add machine learning.
11. Start execution code.

The next diagnostic should be compact, read-only, and evidence-focused.

## 9. Recommended Minimal Future Diagnostic

Recommended next implementation-style phase after this requirements document:

    Phase 3.26-s - Broker H4/M1 alignment diagnostic plan

Purpose:

1. Define a read-only diagnostic for broker-native H4 versus broker-native M1 alignment.
2. Use only broker CSV exports at first.
3. Avoid HistData initially.
4. Establish what the broker itself does before comparing third-party data.
5. Inspect APIs before code.
6. Avoid writing derived files.
7. Avoid H017.
8. Document results before any source decision.

Why broker-only first:

1. Broker H4 and broker M1 should be internally consistent if the exports are valid.
2. If broker H4 and broker M1 are not internally consistent, the problem must be solved before comparing HistData.
3. Broker-only alignment gives the baseline for later HistData comparison.
4. It avoids prematurely forcing HistData into the workflow.

## 10. Current Decision

Current H4 evidence decision:

    Evidence requirements are defined, but no H4 construction method is accepted.

Current HistData decision:

    HistData remains not accepted as a research source.

Current H017 decision:

    H017 remains blocked and not promotable.

Current allowed activity:

    Documentation, source diagnostics, loader tests, and compact read-only evidence gathering.

Current prohibited activity:

    H017 validation on HistData, derived dataset creation, silent source mixing, raw-file modification, and live-trading justification.

## 11. Why H017 Remains Blocked

H017 remains blocked because:

1. Broker-native M1 history is too short.
2. HistData is not accepted as a research source.
3. Broker mismatch assessment found material current-session mismatch risk.
4. H4 construction rules are not accepted.
5. M1 stop-resolution compatibility is not proven.
6. Holiday and special-closure classification is incomplete.
7. March-July 2023 anomaly remains unresolved.
8. The short-window broker result failed the PSR threshold and MinTRL observed-count requirement.
9. The short-window max drawdown of -33.65 percent remains a serious risk signal.

Existing broker-native short-window result remains a pipeline smoke result only:

- Fills: 470
- Starting equity: 10000.00 USD
- Ending equity: 16145.60 USD
- Total return: 61.46 percent
- Max drawdown: -33.65 percent
- Annualized Sharpe: 1.3218

Existing claim result:

- PSR: 0.8662
- PSR threshold: 0.95
- MinTRL feasible: True
- MinTRL required n: 1034
- MinTRL observed n: 470
- DSR: Skipped
- H017 promotable: False

## 12. Non-Actions In This Phase

This phase did not:

1. Accept HistData.
2. Reject HistData permanently.
3. Build H4 bars.
4. Write derived data.
5. Modify raw data.
6. Modify the HistData loader.
7. Modify the MT5 loader.
8. Modify duplicate handling.
9. Modify `.gitignore`.
10. Run H017.
11. Tune strategy parameters.
12. Change the cost model.
13. Broaden the symbol universe.
14. Add machine learning.
15. Start Phase 4 execution work.
16. Implement diagnostics.
