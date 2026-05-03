# Broker H4/M1 Alignment Diagnostic Plan

Phase: 3.26-s

Status: Plan only

Purpose: Define a compact read-only diagnostic to test whether broker-native H4 CSV exports are internally consistent with broker-native M1 CSV exports.

This document does not implement diagnostics.

This document does not build derived H4 datasets.

This document does not write derived data.

This document does not modify raw data.

This document does not use HistData.

This document does not accept HistData as a research source.

This document does not run H017.

This document does not authorize H017 validation.

## 1. Current Decision State

HistData remains not accepted as a research source.

H017 remains alive but not promotable.

H017 remains blocked for validation.

The current allowed use of HistData remains:

    Exploratory diagnostics only.

The current H4 construction decision remains:

    No H4 construction method is accepted yet.

The previous evidence-requirements phase recommended a broker-only diagnostic first.

Reason:

    Before comparing third-party HistData M1 against broker-native H4 bars, the project must first understand whether broker-native H4 and broker-native M1 exports are internally aligned.

## 2. Scope Of This Planned Diagnostic

The planned diagnostic is broker-only.

Inputs:

1. Broker-native USDJPY H4 CSV.
2. Broker-native USDJPY M1 CSV.
3. Broker-native XAUUSD H4 CSV.
4. Broker-native XAUUSD M1 CSV.

Expected local raw paths:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

These files are raw data.

They are gitignored.

They must not be modified.

They must not be committed.

Broker timezone:

    Europe/Athens

Broker timezone meaning:

1. Winter: UTC+2.
2. Summer: UTC+3.
3. DST-aware.

## 3. Non-Scope

The planned diagnostic must not:

1. Load HistData.
2. Accept HistData.
3. Reject HistData permanently.
4. Build full derived H4 datasets.
5. Write parquet files.
6. Write CSV outputs.
7. Write database outputs.
8. Modify raw broker CSV files.
9. Modify raw HistData CSV files.
10. Modify loaders.
11. Modify duplicate handling.
12. Modify `.gitignore`.
13. Run H017.
14. Tune H017.
15. Change the cost model.
16. Broaden the symbol universe.
17. Add machine learning.
18. Start Phase 4 execution work.

## 4. Why Broker-Only Comes First

Broker-only alignment must come first because broker-native H4 bars are the current closest representation of the chart used for H017 signal generation.

If broker H4 and broker M1 exports are internally consistent, then broker H4 can become the baseline for later comparison.

If broker H4 and broker M1 exports are not internally consistent, then the project must resolve broker export interpretation before comparing any third-party source.

Broker-only alignment answers these questions:

1. Do broker H4 timestamps correspond to expected H4 intervals?
2. Are broker M1 bars available inside broker H4 intervals?
3. Can broker H4 OHLC be reconstructed from broker M1 for overlapping windows?
4. Are weekly open bars partial?
5. Are Friday close bars partial?
6. Is XAUUSD missingness visible inside broker H4 windows?
7. Does broker M1 coverage explain broker H4 bars?
8. Are there broker H4 bars that cannot be supported by available broker M1 history?

## 5. Required API Inspection Before Implementation

Before writing future diagnostic code, inspect actual APIs.

Use PowerShell here-strings only.

Required inspection command for a future implementation phase:

    @'
    import inspect
    import dataclasses

    from quantcore.data.mt5_loader import load_mt5_csv, MT5LoadResult

    print("load_mt5_csv:", inspect.signature(load_mt5_csv))

    print("MT5LoadResult fields:")
    for field in dataclasses.fields(MT5LoadResult):
        print(" ", field.name)
    '@ | python -

Do not use Linux/macOS heredoc syntax.

Do not trust remembered function names or keyword names.

## 6. Planned Read-Only Diagnostic Method

The future diagnostic should:

1. Load broker-native H4 CSVs using `load_mt5_csv`.
2. Load broker-native M1 CSVs using `load_mt5_csv`.
3. Use `broker_tz="Europe/Athens"` explicitly.
4. Find the overlapping H4/M1 UTC range for each symbol.
5. For each broker H4 bar in the overlapping range, infer the likely H4 interval.
6. Count M1 bars inside that H4 interval.
7. Reconstruct temporary in-memory OHLC from M1 bars for that interval.
8. Compare reconstructed M1-derived OHLC against broker H4 OHLC.
9. Flag mismatches.
10. Print compact summaries to the terminal.
11. Write no files.

The diagnostic should be read-only.

Any reconstructed H4 bars must exist only in memory.

## 7. Initial Interval Convention To Test

The future diagnostic should test the following interval convention first:

    H4 bar timestamp t represents the interval [t, t + 4 hours)

Meaning:

1. Include M1 bars at or after timestamp t.
2. Exclude M1 bars at or after timestamp t + 4 hours.
3. Reconstructed open is the first M1 open in the interval.
4. Reconstructed high is the max M1 high in the interval.
5. Reconstructed low is the min M1 low in the interval.
6. Reconstructed close is the last M1 close in the interval.

This is a test convention, not yet an accepted project rule.

If this convention fails materially, the diagnostic should report that and not silently try many alternatives until one fits.

Any alternative interval convention must be planned and documented.

## 8. Required Per-Symbol Output

The future diagnostic should report the following per symbol.

### 8.1 Source Summary

Required fields:

1. symbol
2. h4_path
3. m1_path
4. broker_tz
5. h4_n_bars
6. m1_n_bars
7. h4_earliest_utc
8. h4_latest_utc
9. m1_earliest_utc
10. m1_latest_utc
11. overlap_start_utc
12. overlap_end_utc

### 8.2 H4/M1 Coverage Summary

Required fields:

1. h4_bars_in_overlap
2. h4_bars_with_any_m1
3. h4_bars_with_no_m1
4. h4_bars_with_full_240_m1_count
5. h4_bars_with_partial_m1_count
6. min_m1_count_inside_h4
7. median_m1_count_inside_h4
8. max_m1_count_inside_h4

Important:

    A full H4 interval may not always have 240 M1 bars if the interval overlaps weekly open, weekly close, holiday closure, broker maintenance, or XAUUSD daily break.

Therefore, low M1 count is a flag for classification, not automatically a failure.

### 8.3 OHLC Match Summary

Required fields:

1. overlapping_h4_bars_tested
2. open_matches
3. high_matches
4. low_matches
5. close_matches
6. full_ohlc_matches
7. open_mismatch_count
8. high_mismatch_count
9. low_mismatch_count
10. close_mismatch_count
11. max_open_abs_diff
12. max_high_abs_diff
13. max_low_abs_diff
14. max_close_abs_diff

Tolerance must be explicit.

Initial planned tolerance:

    1e-9 absolute price units

If broker export formatting causes tiny representation differences, a later plan may choose symbol-specific tolerances.

This phase does not choose final tolerances.

### 8.4 Session Flags

Each tested H4 interval should be classified with flags:

1. is_weekly_open_candidate
2. is_weekly_close_candidate
3. is_partial_m1_candidate
4. is_xauusd_daily_break_adjacent_candidate
5. is_dst_adjacent_candidate
6. is_holiday_candidate
7. is_first_available_h4_bar
8. is_last_available_h4_bar

The first implementation may use simple provisional flags.

Any provisional flag must be named as provisional.

## 9. Required Compact Examples

The future diagnostic should print compact examples, not huge dumps.

Required example sections:

1. First 10 H4 bars in overlap per symbol.
2. Last 10 H4 bars in overlap per symbol.
3. First 10 H4 bars with no M1 inside interval.
4. First 10 H4 bars with partial M1 count.
5. First 10 OHLC mismatches.
6. Weekly open candidate rows if present.
7. Weekly close candidate rows if present.
8. XAUUSD daily-break-adjacent candidate rows if present.

If output is too large, rerun with narrower windows.

Do not continue blindly from truncated terminal output.

## 10. Expected Interpretation Categories

The future diagnostic should classify each symbol into one of these categories.

### 10.1 Internally Aligned

Meaning:

1. Broker H4 timestamps are explainable.
2. Broker M1 coverage supports broker H4 bars.
3. M1-derived OHLC matches broker H4 OHLC for ordinary complete intervals.
4. Partial intervals are explainable by session boundaries or known missingness.

This would support using broker H4 as a baseline for later comparisons.

It would not accept HistData.

### 10.2 Mostly Aligned With Explainable Exceptions

Meaning:

1. Most ordinary intervals match.
2. Mismatches cluster around session boundaries.
3. Exceptions can be documented.
4. Further focused diagnostics are needed.

This would support additional broker-only diagnostic work.

It would not accept HistData.

### 10.3 Not Internally Aligned

Meaning:

1. Broker H4 and M1 exports do not reconcile under the tested convention.
2. Mismatches are widespread.
3. M1 coverage does not explain H4 bars.
4. Timestamp interpretation may be wrong.
5. Broker export format assumptions may be wrong.

This would block later HistData comparison until broker export interpretation is resolved.

### 10.4 Inconclusive

Meaning:

1. Broker M1 history does not overlap enough broker H4 history.
2. Terminal output was insufficient.
3. Required raw files are missing.
4. Diagnostic failed due to file or loader issue.
5. More data exports are needed.

## 11. Required Stop Conditions

The future implementation must stop and report if:

1. Any expected raw file is missing.
2. Loader API differs from assumptions.
3. `load_mt5_csv` fails on any broker CSV.
4. H4 or M1 data has no overlap for a symbol.
5. Required columns are missing.
6. Datetime index assumptions are wrong.
7. Output becomes too large to review.
8. Tests fail.
9. Test count drops below 514.

Do not patch around these silently.

## 12. Relationship To HistData

This planned diagnostic does not use HistData.

The reason is deliberate:

1. Broker behavior must be understood first.
2. Broker H4/M1 internal alignment becomes the baseline.
3. Only after broker baseline is understood should HistData be compared.
4. HistData remains blocked regardless of this broker-only diagnostic outcome.
5. A successful broker-only diagnostic is necessary but not sufficient for HistData acceptance.

HistData remains not accepted as a research source.

## 13. Relationship To H017

This diagnostic does not run H017.

This diagnostic does not validate H017.

This diagnostic does not change H017 parameters.

This diagnostic does not change the cost model.

H017 remains blocked because:

1. Broker-native M1 history is too short.
2. HistData is not accepted.
3. Broker mismatch assessment found material current-session mismatch risk.
4. H4 construction is undecided.
5. M1 stop-resolution compatibility is unproven.
6. Holiday and special-closure classification is incomplete.
7. March-July 2023 anomaly remains unresolved.
8. The short-window broker result failed the PSR threshold and MinTRL observed-count requirement.
9. The short-window max drawdown of -33.65 percent remains a serious risk signal.

## 14. Planned Deliverable For Future Implementation Phase

A future implementation phase should produce:

1. A small read-only diagnostic script or PowerShell here-string diagnostic.
2. Terminal output summarizing broker H4/M1 alignment.
3. A committed operations document recording the results.
4. No derived data files.
5. No raw data modifications.
6. No H017 run.

Suggested next phase:

    Phase 3.26-t - Broker H4/M1 alignment diagnostic implementation

The implementation phase must inspect actual APIs first.

It must run focused checks if tests are added.

It must run full `pytest -q`.

It must preserve the `514 passed` test anchor unless a deliberate test-removal phase occurs.

## 15. Current Decision

Current decision:

    Broker H4/M1 alignment diagnostic is planned but not implemented.

Current H4 construction status:

    No H4 construction method is accepted yet.

Current HistData status:

    HistData remains not accepted as a research source.

Current H017 status:

    H017 remains blocked and not promotable.

## 16. Non-Actions In This Phase

This phase did not:

1. Implement diagnostics.
2. Accept HistData.
3. Reject HistData permanently.
4. Load HistData.
5. Build H4 bars.
6. Write derived data.
7. Modify raw data.
8. Modify the HistData loader.
9. Modify the MT5 loader.
10. Modify duplicate handling.
11. Modify `.gitignore`.
12. Run H017.
13. Tune strategy parameters.
14. Change the cost model.
15. Broaden the symbol universe.
16. Add machine learning.
17. Start Phase 4 execution work.
