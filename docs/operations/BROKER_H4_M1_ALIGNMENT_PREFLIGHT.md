# Broker H4/M1 Alignment Diagnostic Preflight

Phase: 3.26-t

Status: Preflight complete

Purpose: Record the preflight checks before implementing a broker-native H4/M1 alignment diagnostic.

This document records file-existence checks, raw-file previews, loader API inspection, and implementation cautions.

This document does not implement diagnostics.

This document does not build H4 bars.

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

The current H4 construction decision remains:

    No H4 construction method is accepted yet.

The current allowed use of HistData remains:

    Exploratory diagnostics only.

The broker H4/M1 alignment diagnostic remains necessary before any later HistData comparison.

## 2. Preflight Git Hygiene

Initial repository state was clean.

Observed status:

    On branch main
    Your branch is up to date with 'origin/main'.
    nothing to commit, working tree clean

Final repository state after preflight was also clean.

No files were modified during the read-only preflight.

## 3. Broker Raw File Existence Check

The following expected broker raw files were found.

### 3.1 USDJPY H4

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv

Observed metadata:

    size_bytes=548498
    last_write_time=05/03/2026 10:35:35

### 3.2 USDJPY M1

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv

Observed metadata:

    size_bytes=5978537
    last_write_time=05/03/2026 14:10:25

### 3.3 XAUUSD H4

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv

Observed metadata:

    size_bytes=594386
    last_write_time=05/03/2026 10:35:13

### 3.4 XAUUSD M1

Path:

    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Observed metadata:

    size_bytes=6556675
    last_write_time=05/03/2026 14:10:53

## 4. Raw File Preview

The raw broker CSV files use MetaTrader-style tabular export format with header fields:

    <DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>

### 4.1 USDJPY H4 Preview

First observed rows:

    <DATE>  <TIME>  <OPEN>  <HIGH>  <LOW>   <CLOSE> <TICKVOL>       <VOL>   <SPREAD>
    2018.07.03      00:00:00        110.877 111.124 110.378 110.411 50944   0       0
    2018.07.04      00:00:00        110.410 110.549 110.274 110.499 44662   0       0

### 4.2 USDJPY M1 Preview

First observed rows:

    <DATE>  <TIME>  <OPEN>  <HIGH>  <LOW>   <CLOSE> <TICKVOL>       <VOL>   <SPREAD>
    2026.01.26      05:09:00        153.991 154.022 153.982 154.018 62      0       10
    2026.01.26      05:10:00        154.018 154.044 154.009 154.044 91      0       10

### 4.3 XAUUSD H4 Preview

First observed rows:

    <DATE>  <TIME>  <OPEN>  <HIGH>  <LOW>   <CLOSE> <TICKVOL>       <VOL>   <SPREAD>
    2018.06.28      00:00:00        1252.884        1254.229        1245.910        1248.581        81353   0       0
    2018.06.29      00:00:00        1248.551        1255.573        1245.978        1252.533        79160   0       0

### 4.4 XAUUSD M1 Preview

First observed rows:

    <DATE>  <TIME>  <OPEN>  <HIGH>  <LOW>   <CLOSE> <TICKVOL>       <VOL>   <SPREAD>
    2026.01.20      04:22:00        4682.628        4683.252        4682.133        4682.378        113     0       160
    2026.01.20      04:23:00        4682.308        4682.914        4682.062        4682.741        143     0       160

## 5. Important H4 Preview Caution

The first two visible rows of both broker H4 files show `00:00:00` on consecutive dates.

This may indicate one of several possibilities:

1. The preview only happened to show daily boundary rows.
2. The broker H4 export may have unusual timestamp spacing.
3. The file may not actually contain H4 bars despite the file name.
4. The export settings may have selected the wrong timeframe.
5. The loader or diagnostic must inspect timestamp deltas before assuming the timeframe.

Current status:

    Unresolved.

Required next check:

    Inspect loaded H4 timestamp deltas and time-of-day distribution for both symbols.

Do not assume the H4 files are valid H4 bars until this is checked.

## 6. Loader API Inspection

The actual MT5 loader API was inspected before implementation.

Observed signature:

    load_mt5_csv(path: 'str | Path', broker_tz: 'str' = 'Europe/Athens') -> 'MT5LoadResult'

Observed module:

    quantcore.data.mt5_loader

Observed `MT5LoadResult` dataclass fields:

    bars: pd.DataFrame
    n_bars: int
    n_input_rows: int
    earliest_utc: pd.Timestamp
    latest_utc: pd.Timestamp
    broker_tz: str

This confirms that future diagnostic code may call `load_mt5_csv` with:

    broker_tz="Europe/Athens"

## 7. Implementation Requirements For Next Phase

Before writing the broker H4/M1 alignment diagnostic script, the next phase should inspect loaded data shape.

Required read-only checks:

1. Load each broker CSV with `load_mt5_csv`.
2. Print `n_bars`, `n_input_rows`, `earliest_utc`, and `latest_utc`.
3. Print `bars` columns.
4. Print index type and timezone.
5. Print first and last rows.
6. Print timestamp delta distribution.
7. Print time-of-day distribution for H4 files.
8. Confirm whether H4 files contain true H4 spacing.
9. Stop if H4 files appear to be daily or otherwise not H4.
10. Write no derived data.

## 8. Relationship To HistData

This preflight did not use HistData.

HistData remains not accepted as a research source.

The misleading local folder name remains:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

No HistData raw files were modified.

No HistData derived files were written.

## 9. Relationship To H017

This preflight did not run H017.

This preflight did not validate H017.

This preflight did not change H017 parameters.

This preflight did not change the cost model.

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

## 10. Recommended Next Phase

Recommended next phase:

    Phase 3.26-u - Broker H4/M1 loaded-shape inspection

Purpose:

1. Load broker-native H4 and M1 CSVs using the verified MT5 loader API.
2. Inspect loaded DataFrame shape, columns, index, timestamp deltas, and time-of-day distribution.
3. Verify whether the files named H4 are actually H4-spaced.
4. Keep the diagnostic read-only.
5. Write no derived data.
6. Avoid HistData.
7. Avoid H017.
8. Commit a result document before implementing any reusable diagnostic script.

## 11. Non-Actions In This Phase

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
