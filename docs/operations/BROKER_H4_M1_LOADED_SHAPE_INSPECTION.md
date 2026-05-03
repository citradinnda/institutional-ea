# Broker H4/M1 Loaded-Shape Inspection

Date created: 2026-05-03T22:35:34+09:00

## Purpose

This document records Phase 3.26-u: broker H4/M1 loaded-shape inspection.

The purpose was to load broker-native MT5 CSV exports through the verified MT5 loader and inspect loaded DataFrame shape, timestamp index, timestamp deltas, and H4 time-of-day distribution before assuming files named H4.csv are actually H4-spaced.

## Scope

This was a read-only broker data-shape diagnostic.

In scope:

1. Broker-native USDJPY H4 CSV.
2. Broker-native USDJPY M1 CSV.
3. Broker-native XAUUSD H4 CSV.
4. Broker-native XAUUSD M1 CSV.
5. MT5 loader API inspection.
6. Loaded DataFrame shape, index, timestamp deltas, and H4-specific spacing checks.

Out of scope:

1. HistData loading.
2. H017 validation.
3. Strategy tuning.
4. Raw data modification.
5. Derived data writing.
6. Any source-acceptance decision.

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
LOADING USDJPY H4
====================================================================================================
symbol: USDJPY
timeframe_label_from_file_name: H4
path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
path_exists: True
size_bytes: 548498

--- MT5LoadResult metadata ---
n_input_rows: 8708
n_bars: 8708
earliest_utc: 2018-07-02 21:00:00+00:00
latest_utc: 2026-04-29 09:00:00+00:00
broker_tz: Europe/Athens

--- DataFrame shape and index ---
bars.shape: (8708, 5)
bars.columns: ['open', 'high', 'low', 'close', 'volume']
index_type: <class 'pandas.DatetimeIndex'>
index_name: dt
index_timezone: UTC
index_is_monotonic_increasing: True
index_has_duplicates: False

--- First 5 rows ---
                              open     high      low    close   volume
dt                                                                    
2018-07-02 21:00:00+00:00  110.877  111.124  110.378  110.411  50944.0
2018-07-03 21:00:00+00:00  110.410  110.549  110.274  110.499  44662.0
2018-07-04 21:00:00+00:00  110.498  110.715  110.286  110.559  50143.0
2018-07-05 21:00:00+00:00  110.562  110.780  110.377  110.440  40301.0
2018-07-07 21:00:00+00:00  110.387  110.460  110.373  110.437   3374.0

--- Last 5 rows ---
                              open     high      low    close  volume
dt                                                                   
2026-04-28 17:00:00+00:00  159.651  159.660  159.437  159.554  2387.0
2026-04-28 21:00:00+00:00  159.551  159.660  159.514  159.614  5846.0
2026-04-29 01:00:00+00:00  159.613  159.736  159.600  159.666  5107.0
2026-04-29 05:00:00+00:00  159.669  159.850  159.633  159.841  6400.0
2026-04-29 09:00:00+00:00  159.843  160.200  159.811  160.182  9710.0

--- Timestamp delta diagnostics: USDJPY H4 ---
Top timestamp deltas:
  0 days 04:00:00: 7510
  1 days 00:00:00: 771
  2 days 00:00:00: 389
  1 days 04:00:00: 7
  0 days 20:00:00: 7
  2 days 01:00:00: 5
  1 days 23:00:00: 5
  3 days 00:00:00: 4
  1 days 01:00:00: 3
  0 days 23:00:00: 3
  2 days 04:00:00: 2
  0 days 12:00:00: 1
min_delta: 0 days 04:00:00
median_delta: 0 days 04:00:00
max_delta: 3 days 00:00:00
dominant_delta: 0 days 04:00:00
dominant_delta_count: 7510
dominant_delta_pct: 86.252441
one_minute_delta_count: 0
four_hour_delta_count: 7510
one_day_delta_count: 771
one_minute_delta_pct: 0.000000
four_hour_delta_pct: 86.252441
one_day_delta_pct: 8.854944

--- H4-specific diagnostics: USDJPY ---
UTC time-of-day distribution:
  01:00:00: 718
  02:00:00: 534
  05:00:00: 718
  06:00:00: 534
  09:00:00: 719
  10:00:00: 534
  13:00:00: 718
  14:00:00: 534
  17:00:00: 862
  18:00:00: 644
  21:00:00: 1269
  22:00:00: 924
dominant_delta_is_exactly_4_hours: True
dominant_delta_is_exactly_1_day: False
four_hour_delta_pct: 86.252441
one_day_delta_pct: 8.854944
CLASSIFICATION: H4 file appears primarily H4-spaced, subject to weekend/session gaps.

====================================================================================================
LOADING USDJPY M1
====================================================================================================
symbol: USDJPY
timeframe_label_from_file_name: M1
path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
path_exists: True
size_bytes: 5978537

--- MT5LoadResult metadata ---
n_input_rows: 97907
n_bars: 97907
earliest_utc: 2026-01-26 03:09:00+00:00
latest_utc: 2026-04-30 07:00:00+00:00
broker_tz: Europe/Athens

--- DataFrame shape and index ---
bars.shape: (97907, 5)
bars.columns: ['open', 'high', 'low', 'close', 'volume']
index_type: <class 'pandas.DatetimeIndex'>
index_name: dt
index_timezone: UTC
index_is_monotonic_increasing: True
index_has_duplicates: False

--- First 5 rows ---
                              open     high      low    close  volume
dt                                                                   
2026-01-26 03:09:00+00:00  153.991  154.022  153.982  154.018    62.0
2026-01-26 03:10:00+00:00  154.018  154.044  154.009  154.044    91.0
2026-01-26 03:11:00+00:00  154.043  154.054  154.020  154.042    96.0
2026-01-26 03:12:00+00:00  154.041  154.064  154.028  154.057    82.0
2026-01-26 03:13:00+00:00  154.055  154.061  154.046  154.053    57.0

--- Last 5 rows ---
                              open     high      low    close  volume
dt                                                                   
2026-04-30 06:56:00+00:00  159.334  159.393  159.334  159.393    82.0
2026-04-30 06:57:00+00:00  159.390  159.420  159.377  159.406   122.0
2026-04-30 06:58:00+00:00  159.405  159.405  159.356  159.362   106.0
2026-04-30 06:59:00+00:00  159.358  159.366  159.331  159.339    72.0
2026-04-30 07:00:00+00:00  159.339  159.350  159.326  159.333   105.0

--- Timestamp delta diagnostics: USDJPY M1 ---
Top timestamp deltas:
  0 days 00:01:00: 97819
  0 days 00:02:00: 33
  0 days 00:06:00: 16
  2 days 00:07:00: 9
  0 days 00:03:00: 7
  0 days 00:11:00: 7
  0 days 00:04:00: 5
  0 days 00:07:00: 3
  0 days 00:10:00: 3
  2 days 00:08:00: 1
  1 days 23:28:00: 1
  1 days 23:07:00: 1
  2 days 00:15:00: 1
min_delta: 0 days 00:01:00
median_delta: 0 days 00:01:00
max_delta: 2 days 00:15:00
dominant_delta: 0 days 00:01:00
dominant_delta_count: 97819
dominant_delta_pct: 99.911139
one_minute_delta_count: 97819
four_hour_delta_count: 0
one_day_delta_count: 0
one_minute_delta_pct: 99.911139
four_hour_delta_pct: 0.000000
one_day_delta_pct: 0.000000

====================================================================================================
LOADING XAUUSD H4
====================================================================================================
symbol: XAUUSD
timeframe_label_from_file_name: H4
path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
path_exists: True
size_bytes: 594386

--- MT5LoadResult metadata ---
n_input_rows: 8658
n_bars: 8658
earliest_utc: 2018-06-27 21:00:00+00:00
latest_utc: 2026-04-30 05:00:00+00:00
broker_tz: Europe/Athens

--- DataFrame shape and index ---
bars.shape: (8658, 5)
bars.columns: ['open', 'high', 'low', 'close', 'volume']
index_type: <class 'pandas.DatetimeIndex'>
index_name: dt
index_timezone: UTC
index_is_monotonic_increasing: True
index_has_duplicates: False

--- First 5 rows ---
                               open      high       low     close   volume
dt                                                                        
2018-06-27 21:00:00+00:00  1252.884  1254.229  1245.910  1248.581  81353.0
2018-06-28 21:00:00+00:00  1248.551  1255.573  1245.978  1252.533  79160.0
2018-06-30 21:00:00+00:00  1253.020  1254.149  1252.785  1253.365   2202.0
2018-07-01 21:00:00+00:00  1253.329  1253.576  1239.648  1242.103  75367.0
2018-07-02 21:00:00+00:00  1242.105  1256.819  1237.914  1254.923  76943.0

--- Last 5 rows ---
                               open      high       low     close   volume
dt                                                                        
2026-04-29 13:00:00+00:00  4547.794  4564.972  4517.951  4547.032  75284.0
2026-04-29 17:00:00+00:00  4546.938  4562.086  4539.271  4561.717  22487.0
2026-04-29 21:00:00+00:00  4561.621  4582.525  4555.500  4556.017  46829.0
2026-04-30 01:00:00+00:00  4555.991  4605.493  4540.766  4598.212  42231.0
2026-04-30 05:00:00+00:00  4598.271  4646.985  4597.267  4629.938  62255.0

--- Timestamp delta diagnostics: XAUUSD H4 ---
Top timestamp deltas:
  0 days 04:00:00: 7460
  1 days 00:00:00: 768
  2 days 00:00:00: 375
  3 days 00:00:00: 13
  1 days 04:00:00: 9
  0 days 20:00:00: 7
  2 days 04:00:00: 7
  2 days 01:00:00: 5
  1 days 23:00:00: 4
  1 days 01:00:00: 3
  0 days 23:00:00: 3
  4 days 00:00:00: 1
  0 days 12:00:00: 1
  2 days 23:00:00: 1
min_delta: 0 days 04:00:00
median_delta: 0 days 04:00:00
max_delta: 4 days 00:00:00
dominant_delta: 0 days 04:00:00
dominant_delta_count: 7460
dominant_delta_pct: 86.173039
one_minute_delta_count: 0
four_hour_delta_count: 7460
one_day_delta_count: 768
one_minute_delta_pct: 0.000000
four_hour_delta_pct: 86.173039
one_day_delta_pct: 8.871434

--- H4-specific diagnostics: XAUUSD ---
UTC time-of-day distribution:
  01:00:00: 715
  02:00:00: 530
  05:00:00: 715
  06:00:00: 530
  09:00:00: 715
  10:00:00: 530
  13:00:00: 715
  14:00:00: 530
  17:00:00: 858
  18:00:00: 634
  21:00:00: 1266
  22:00:00: 920
dominant_delta_is_exactly_4_hours: True
dominant_delta_is_exactly_1_day: False
four_hour_delta_pct: 86.173039
one_day_delta_pct: 8.871434
CLASSIFICATION: H4 file appears primarily H4-spaced, subject to weekend/session gaps.

====================================================================================================
LOADING XAUUSD M1
====================================================================================================
symbol: XAUUSD
timeframe_label_from_file_name: M1
path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
path_exists: True
size_bytes: 6556675

--- MT5LoadResult metadata ---
n_input_rows: 97966
n_bars: 97966
earliest_utc: 2026-01-20 02:22:00+00:00
latest_utc: 2026-04-30 07:00:00+00:00
broker_tz: Europe/Athens

--- DataFrame shape and index ---
bars.shape: (97966, 5)
bars.columns: ['open', 'high', 'low', 'close', 'volume']
index_type: <class 'pandas.DatetimeIndex'>
index_name: dt
index_timezone: UTC
index_is_monotonic_increasing: True
index_has_duplicates: False

--- First 5 rows ---
                               open      high       low     close  volume
dt                                                                       
2026-01-20 02:22:00+00:00  4682.628  4683.252  4682.133  4682.378   113.0
2026-01-20 02:23:00+00:00  4682.308  4682.914  4682.062  4682.741   143.0
2026-01-20 02:24:00+00:00  4682.751  4684.513  4682.734  4683.684   173.0
2026-01-20 02:25:00+00:00  4683.651  4685.416  4683.520  4684.029   247.0
2026-01-20 02:26:00+00:00  4684.061  4685.207  4684.061  4685.010   234.0

--- Last 5 rows ---
                               open      high       low     close  volume
dt                                                                       
2026-04-30 06:56:00+00:00  4625.743  4626.172  4624.509  4624.716   132.0
2026-04-30 06:57:00+00:00  4624.631  4625.416  4624.420  4624.946   134.0
2026-04-30 06:58:00+00:00  4624.889  4625.384  4623.375  4624.865   192.0
2026-04-30 06:59:00+00:00  4624.779  4626.112  4624.231  4624.962   158.0
2026-04-30 07:00:00+00:00  4625.030  4627.281  4625.030  4626.687   199.0

--- Timestamp delta diagnostics: XAUUSD M1 ---
Top timestamp deltas:
  0 days 00:01:00: 97886
  0 days 01:04:00: 29
  0 days 01:03:00: 18
  2 days 01:04:00: 8
  0 days 01:05:00: 5
  0 days 00:02:00: 4
  2 days 01:05:00: 2
  0 days 00:03:00: 1
  0 days 01:13:00: 1
  0 days 00:05:00: 1
  0 days 00:09:00: 1
  0 days 03:32:00: 1
  0 days 01:06:00: 1
  0 days 00:06:00: 1
  0 days 01:08:00: 1
min_delta: 0 days 00:01:00
median_delta: 0 days 00:01:00
max_delta: 3 days 01:04:00
dominant_delta: 0 days 00:01:00
dominant_delta_count: 97886
dominant_delta_pct: 99.919359
one_minute_delta_count: 97886
four_hour_delta_count: 0
one_day_delta_count: 0
one_minute_delta_pct: 99.919359
four_hour_delta_pct: 0.000000
one_day_delta_pct: 0.000000

====================================================================================================
DIAGNOSTIC CONCLUSION REMINDER
====================================================================================================
This diagnostic is read-only.
No HistData was loaded.
H017 was not run.
No raw files were modified.
No derived data files were written.

====================================================================================================
H4 DECISION CHECKPOINT
====================================================================================================
USDJPY H4 loaded-shape classification: h4_spaced
XAUUSD H4 loaded-shape classification: h4_spaced
NEXT_STEP: Both broker H4 files appear H4-spaced. Proceed next to broker-only H4/M1 alignment diagnostic.

END DIAGNOSTIC OUTPUT

## Interpretation checkpoint

This document intentionally records loaded-shape evidence before any broker-only H4/M1 alignment diagnostic or H4 construction decision.

Decision rule for the next step:

1. If either H4.csv is not actually H4-spaced, stop and re-export broker H4 data.
2. If both H4.csv files are H4-spaced, proceed to a broker-only H4/M1 alignment diagnostic.
3. If broker H4/M1 does not align, fix broker export interpretation before any research validation.
4. If broker H4/M1 aligns, use that evidence in the later H4 construction and HistData source-acceptance decision.

## Guardrails preserved

1. HistData remains not accepted as a research source.
2. H017 remains alive but not promotable.
3. No H017 validation was run on HistData.
4. No HistData was loaded in this diagnostic.
5. No raw broker files were modified.
6. No raw HistData files were modified.
7. No derived data files were written.
8. No H4 construction method is accepted by this document.
