# Broker H4/M1 Alignment Diagnostic

Date created: 2026-05-03T22:49:22+09:00

## Purpose

This document records Phase 3.26-v: broker-only H4/M1 alignment diagnostic.

The purpose was to verify whether broker-native H4 OHLCV bars align with broker-native M1 bars aggregated into the same H4 windows, using only local broker MT5 CSV exports.

## Scope

This was a read-only broker-only diagnostic.

In scope:

1. Broker-native USDJPY H4 CSV.
2. Broker-native USDJPY M1 CSV.
3. Broker-native XAUUSD H4 CSV.
4. Broker-native XAUUSD M1 CSV.
5. H4-to-M1 OHLCV comparison for fully covered H4 windows.

Out of scope:

1. HistData loading.
2. H017 validation.
3. Strategy tuning.
4. Raw data modification.
5. Derived data writing.
6. Any final source-acceptance decision.
7. Any final H4 construction decision.

## Comparison method

For each symbol, the diagnostic loaded broker H4 and M1 files with the verified MT5 loader.

An H4 bar was eligible for comparison only when:

1. The next H4 timestamp was exactly 4 hours later.
2. The full M1 window was inside the M1 export range.
3. The M1 window contained exactly 240 one-minute bars.
4. The M1 index exactly matched every minute in the interval from the H4 timestamp through H4 timestamp plus 4 hours, excluding the endpoint.

M1 aggregation rule:

1. Open: first M1 open in the window.
2. High: maximum M1 high in the window.
3. Low: minimum M1 low in the window.
4. Close: last M1 close in the window.
5. Volume: sum of M1 volume in the window.

## Files inspected

1. C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
2. C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
3. C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
4. C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

The raw files are under /data/, are gitignored, and were not modified or committed.

## Diagnostic output

BEGIN DIAGNOSTIC OUTPUT


====================================================================================================
API INSPECTION
====================================================================================================
load_mt5_csv signature: (path: 'str | Path', broker_tz: 'str' = 'Europe/Athens') -> 'MT5LoadResult'
MT5LoadResult dataclass fields:
  bars: pd.DataFrame
  n_bars: int
  n_input_rows: int
  earliest_utc: pd.Timestamp
  latest_utc: pd.Timestamp
  broker_tz: str

====================================================================================================
DIAGNOSTIC RULES
====================================================================================================
This is a read-only broker-only diagnostic.
Only broker-native MT5 H4 and M1 CSV files are loaded.
HistData is not loaded.
H017 is not run.
Raw files are not modified.
No derived data files are written.
Each compared H4 window must have a next H4 timestamp exactly 4 hours later.
Each compared H4 window must have exactly 240 one-minute bars covering [H4 timestamp, H4 timestamp + 4 hours).
OHLCV comparison uses M1 aggregation: first open, max high, min low, last close, sum volume.

====================================================================================================
LOAD USDJPY
====================================================================================================
symbol: USDJPY
h4_path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
h4_path_exists: True
h4_size_bytes: 548498
m1_path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
m1_path_exists: True
m1_size_bytes: 5978537

--- H4 metadata ---
h4_n_input_rows: 8708
h4_n_bars: 8708
h4_earliest_utc: 2018-07-02 21:00:00+00:00
h4_latest_utc: 2026-04-29 09:00:00+00:00
h4_broker_tz: Europe/Athens
h4_index_timezone: UTC
h4_index_monotonic: True
h4_index_has_duplicates: False

--- M1 metadata ---
m1_n_input_rows: 97907
m1_n_bars: 97907
m1_earliest_utc: 2026-01-26 03:09:00+00:00
m1_latest_utc: 2026-04-30 07:00:00+00:00
m1_broker_tz: Europe/Athens
m1_index_timezone: UTC
m1_index_monotonic: True
m1_index_has_duplicates: False

====================================================================================================
ALIGNMENT DIAGNOSTIC USDJPY
====================================================================================================
total_h4_bars: 8708
candidate_exact_4h_bars: 7510
candidates_inside_m1_range: 403
compared_full_m1_windows: 338
skipped_non_4h_next_delta: 1198
skipped_outside_m1_range: 7107
skipped_incomplete_m1_window: 65

--- Match summary ---
matched_bars: 338
mismatched_bars: 0
matched_pct_of_compared: 100.000000
mismatch_pct_of_compared: 0.000000

--- Mismatch by column ---
open_mismatch_count: 0
open_max_abs_diff: 0.0
high_mismatch_count: 0
high_max_abs_diff: 0.0
low_mismatch_count: 0
low_max_abs_diff: 0.0
close_mismatch_count: 0
close_max_abs_diff: 0.0
volume_mismatch_count: 0
volume_max_abs_diff: 0.0

--- First matched examples ---
  2026-01-26 06:00:00+00:00: open=154.246, high=154.344, low=153.301, close=153.732, volume=33790.0
  2026-01-26 10:00:00+00:00: open=153.73, high=154.339, low=153.612, close=153.811, volume=21929.0
  2026-01-26 14:00:00+00:00: open=153.813, high=154.274, low=153.712, close=154.038, volume=15654.0
  2026-01-26 22:00:00+00:00: open=154.382, high=154.467, low=154.083, close=154.412, volume=15205.0
  2026-01-27 02:00:00+00:00: open=154.415, high=154.761, low=154.366, close=154.728, volume=12260.0

--- First incomplete-window examples ---
  2026-01-26 18:00:00+00:00: actual_m1_count=235, missing_count_vs_240=5, actual_first=2026-01-26 18:00:00+00:00, actual_last=2026-01-26 21:59:00+00:00
  2026-01-27 18:00:00+00:00: actual_m1_count=235, missing_count_vs_240=5, actual_first=2026-01-27 18:00:00+00:00, actual_last=2026-01-27 21:59:00+00:00
  2026-01-28 18:00:00+00:00: actual_m1_count=235, missing_count_vs_240=5, actual_first=2026-01-28 18:00:00+00:00, actual_last=2026-01-28 21:59:00+00:00
  2026-01-29 18:00:00+00:00: actual_m1_count=230, missing_count_vs_240=10, actual_first=2026-01-29 18:00:00+00:00, actual_last=2026-01-29 21:59:00+00:00
  2026-02-01 18:00:00+00:00: actual_m1_count=115, missing_count_vs_240=125, actual_first=2026-02-01 20:05:00+00:00, actual_last=2026-02-01 21:59:00+00:00
  2026-02-02 18:00:00+00:00: actual_m1_count=237, missing_count_vs_240=3, actual_first=2026-02-02 18:00:00+00:00, actual_last=2026-02-02 21:59:00+00:00
  2026-02-03 18:00:00+00:00: actual_m1_count=235, missing_count_vs_240=5, actual_first=2026-02-03 18:00:00+00:00, actual_last=2026-02-03 21:59:00+00:00
  2026-02-04 18:00:00+00:00: actual_m1_count=239, missing_count_vs_240=1, actual_first=2026-02-04 18:00:00+00:00, actual_last=2026-02-04 21:59:00+00:00
  2026-02-05 18:00:00+00:00: actual_m1_count=233, missing_count_vs_240=7, actual_first=2026-02-05 18:00:00+00:00, actual_last=2026-02-05 21:59:00+00:00
  2026-02-08 18:00:00+00:00: actual_m1_count=113, missing_count_vs_240=127, actual_first=2026-02-08 20:05:00+00:00, actual_last=2026-02-08 21:59:00+00:00

--- First mismatch examples ---
  None

ALIGNMENT_CLASSIFICATION: aligned_on_all_full_m1_windows

====================================================================================================
LOAD XAUUSD
====================================================================================================
symbol: XAUUSD
h4_path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
h4_path_exists: True
h4_size_bytes: 594386
m1_path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
m1_path_exists: True
m1_size_bytes: 6556675

--- H4 metadata ---
h4_n_input_rows: 8658
h4_n_bars: 8658
h4_earliest_utc: 2018-06-27 21:00:00+00:00
h4_latest_utc: 2026-04-30 05:00:00+00:00
h4_broker_tz: Europe/Athens
h4_index_timezone: UTC
h4_index_monotonic: True
h4_index_has_duplicates: False

--- M1 metadata ---
m1_n_input_rows: 97966
m1_n_bars: 97966
m1_earliest_utc: 2026-01-20 02:22:00+00:00
m1_latest_utc: 2026-04-30 07:00:00+00:00
m1_broker_tz: Europe/Athens
m1_index_timezone: UTC
m1_index_monotonic: True
m1_index_has_duplicates: False

====================================================================================================
ALIGNMENT DIAGNOSTIC XAUUSD
====================================================================================================
total_h4_bars: 8658
candidate_exact_4h_bars: 7460
candidates_inside_m1_range: 426
compared_full_m1_windows: 354
skipped_non_4h_next_delta: 1198
skipped_outside_m1_range: 7034
skipped_incomplete_m1_window: 72

--- Match summary ---
matched_bars: 354
mismatched_bars: 0
matched_pct_of_compared: 100.000000
mismatch_pct_of_compared: 0.000000

--- Mismatch by column ---
open_mismatch_count: 0
open_max_abs_diff: 0.0
high_mismatch_count: 0
high_max_abs_diff: 0.0
low_mismatch_count: 0
low_max_abs_diff: 0.0
close_mismatch_count: 0
close_max_abs_diff: 0.0
volume_mismatch_count: 0
volume_max_abs_diff: 0.0

--- First matched examples ---
  2026-01-20 06:00:00+00:00: open=4716.195, high=4737.424, low=4714.966, close=4733.029, volume=54738.0
  2026-01-20 10:00:00+00:00: open=4732.985, high=4751.171, low=4715.232, close=4737.495, volume=146109.0
  2026-01-20 14:00:00+00:00: open=4737.464, high=4766.367, low=4729.064, close=4760.696, volume=74004.0
  2026-01-20 22:00:00+00:00: open=4775.829, high=4849.968, low=4770.751, close=4845.003, volume=99732.0
  2026-01-21 02:00:00+00:00: open=4845.003, high=4888.495, low=4832.476, close=4855.166, volume=98614.0

--- First incomplete-window examples ---
  2026-01-20 18:00:00+00:00: actual_m1_count=178, missing_count_vs_240=62, actual_first=2026-01-20 18:00:00+00:00, actual_last=2026-01-20 21:59:00+00:00
  2026-01-21 18:00:00+00:00: actual_m1_count=177, missing_count_vs_240=63, actual_first=2026-01-21 18:00:00+00:00, actual_last=2026-01-21 21:59:00+00:00
  2026-01-22 18:00:00+00:00: actual_m1_count=178, missing_count_vs_240=62, actual_first=2026-01-22 18:00:00+00:00, actual_last=2026-01-22 21:59:00+00:00
  2026-01-25 18:00:00+00:00: actual_m1_count=57, missing_count_vs_240=183, actual_first=2026-01-25 21:01:00+00:00, actual_last=2026-01-25 21:59:00+00:00
  2026-01-26 18:00:00+00:00: actual_m1_count=177, missing_count_vs_240=63, actual_first=2026-01-26 18:00:00+00:00, actual_last=2026-01-26 21:59:00+00:00
  2026-01-27 18:00:00+00:00: actual_m1_count=168, missing_count_vs_240=72, actual_first=2026-01-27 18:00:00+00:00, actual_last=2026-01-27 21:59:00+00:00
  2026-01-28 18:00:00+00:00: actual_m1_count=173, missing_count_vs_240=67, actual_first=2026-01-28 18:00:00+00:00, actual_last=2026-01-28 21:59:00+00:00
  2026-01-29 18:00:00+00:00: actual_m1_count=177, missing_count_vs_240=63, actual_first=2026-01-29 18:00:00+00:00, actual_last=2026-01-29 21:59:00+00:00
  2026-02-01 18:00:00+00:00: actual_m1_count=50, missing_count_vs_240=190, actual_first=2026-02-01 21:01:00+00:00, actual_last=2026-02-01 21:59:00+00:00
  2026-02-02 18:00:00+00:00: actual_m1_count=177, missing_count_vs_240=63, actual_first=2026-02-02 18:00:00+00:00, actual_last=2026-02-02 21:59:00+00:00

--- First mismatch examples ---
  None

ALIGNMENT_CLASSIFICATION: aligned_on_all_full_m1_windows

====================================================================================================
FINAL DECISION CHECKPOINT
====================================================================================================
USDJPY_classification: aligned_on_all_full_m1_windows
USDJPY_compared_full_m1_windows: 338
USDJPY_matched_bars: 338
USDJPY_mismatched_bars: 0
USDJPY_skipped_incomplete_m1_window: 65
XAUUSD_classification: aligned_on_all_full_m1_windows
XAUUSD_compared_full_m1_windows: 354
XAUUSD_matched_bars: 354
XAUUSD_mismatched_bars: 0
XAUUSD_skipped_incomplete_m1_window: 72
NEXT_STEP: Broker H4/M1 aligns on all full M1-covered H4 windows. Use this evidence in the later H4 construction decision.

END DIAGNOSTIC OUTPUT

## Interpretation checkpoint

This document records broker-only H4/M1 alignment evidence. It does not accept HistData, does not validate H017, and does not choose a final H4 construction method.

Decision rule:

1. If broker H4/M1 aligns on all full M1-covered H4 windows, use this evidence in the later H4 construction decision.
2. If broker H4/M1 mismatches, stop and inspect broker export interpretation before research validation.
3. If no full M1-covered H4 windows exist, obtain better broker exports before using this alignment diagnostic.
4. Regardless of outcome, HistData remains blocked until separate source-acceptance and H4 construction decisions are complete.

## Guardrails preserved

1. HistData remains not accepted as a research source.
2. H017 remains alive but not promotable.
3. No H017 validation was run on HistData.
4. No HistData was loaded in this diagnostic.
5. No raw broker files were modified.
6. No raw HistData files were modified.
7. No derived data files were written.
8. No H4 construction method is accepted by this document.
