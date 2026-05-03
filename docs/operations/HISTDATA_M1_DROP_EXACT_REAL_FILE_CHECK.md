# HistData M1 `drop_exact` Real-File Loader Check

Date: 2026-05-03

## Purpose

This document records a read-only real-file check of the dedicated HistData M1 loader using the explicit opt-in duplicate policy:

```python
duplicate_policy="drop_exact"
This check was performed after the duplicate-handling decision record and tested loader update.

This check does not accept HistData as a research source.

Scope
Files checked:

text
C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv
C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv
Important path note:

The directory name dukascopy_samples is misleading. These two files are HistData files, not Dukascopy files.

Raw files were not modified.

No derived files were written.

H017 was not run.

Loader API Used
python
from quantcore.data.histdata_loader import load_histdata_m1_csv

result = load_histdata_m1_csv(path, duplicate_policy="drop_exact")
The default loader behavior remains strict duplicate rejection:

python
duplicate_policy="reject"
The drop_exact policy is explicit opt-in behavior. It removes only exact duplicate OHLCV rows and rejects conflicting duplicate timestamp groups.

USDJPY Result
Path:

text
C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv
Observed result:

text
exists: True
n_input_rows: 1808731
n_bars: 1808431
earliest_utc: 2021-01-03 17:00:00+00:00
latest_utc: 2025-12-31 16:57:00+00:00
source_tz: UTC
duplicate_policy: drop_exact
n_duplicate_rows_removed: 300
n_duplicate_timestamp_values: 300
n_missing_minutes: 816687
columns: ['open', 'high', 'low', 'close', 'volume']
tz: UTC
is_monotonic_increasing: True
has_duplicates: False
non_positive_ohlc_rows: 0
bad_ohlc_rows: 0
negative_volume_rows: 0
zero_volume_rows: 1808431
Duplicate timestamp ranges:

text
2021-10-31 19:00:00+00:00 through 2021-10-31 19:59:00+00:00: 60 duplicate timestamp values
2022-10-30 19:00:00+00:00 through 2022-10-30 19:59:00+00:00: 60 duplicate timestamp values
2023-10-29 19:00:00+00:00 through 2023-10-29 19:59:00+00:00: 60 duplicate timestamp values
2024-10-27 19:00:00+00:00 through 2024-10-27 19:59:00+00:00: 60 duplicate timestamp values
2025-10-26 19:00:00+00:00 through 2025-10-26 19:59:00+00:00: 60 duplicate timestamp values
First 20 missing minutes reported by the loader:

text
2021-01-03 17:17:00+00:00
2021-01-03 17:20:00+00:00
2021-01-03 17:23:00+00:00
2021-01-03 17:25:00+00:00
2021-01-04 16:27:00+00:00
2021-01-04 17:02:00+00:00
2021-01-04 17:09:00+00:00
2021-01-04 17:14:00+00:00
2021-01-04 17:17:00+00:00
2021-01-04 17:22:00+00:00
2021-01-04 17:23:00+00:00
2021-01-04 17:24:00+00:00
2021-01-04 17:28:00+00:00
2021-01-04 17:55:00+00:00
2021-01-05 17:02:00+00:00
2021-01-05 17:12:00+00:00
2021-01-05 17:13:00+00:00
2021-01-05 17:23:00+00:00
2021-01-05 17:40:00+00:00
2021-01-05 17:44:00+00:00
Last 20 missing minutes reported by the loader:

text
2025-12-28 16:54:00+00:00
2025-12-28 16:55:00+00:00
2025-12-28 16:56:00+00:00
2025-12-28 16:57:00+00:00
2025-12-28 16:58:00+00:00
2025-12-28 16:59:00+00:00
2025-12-28 17:00:00+00:00
2025-12-28 17:01:00+00:00
2025-12-28 17:02:00+00:00
2025-12-28 17:03:00+00:00
2025-12-29 17:01:00+00:00
2025-12-29 17:02:00+00:00
2025-12-29 17:03:00+00:00
2025-12-30 16:34:00+00:00
2025-12-30 17:01:00+00:00
2025-12-30 17:02:00+00:00
2025-12-30 17:03:00+00:00
2025-12-30 18:02:00+00:00
2025-12-30 18:08:00+00:00
2025-12-30 18:24:00+00:00
XAUUSD Result
Path:

text
C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv
Observed result:

text
exists: True
n_input_rows: 1726549
n_bars: 1726249
earliest_utc: 2021-01-03 18:00:00+00:00
latest_utc: 2025-12-31 16:57:00+00:00
source_tz: UTC
duplicate_policy: drop_exact
n_duplicate_rows_removed: 300
n_duplicate_timestamp_values: 300
n_missing_minutes: 898809
columns: ['open', 'high', 'low', 'close', 'volume']
tz: UTC
is_monotonic_increasing: True
has_duplicates: False
non_positive_ohlc_rows: 0
bad_ohlc_rows: 0
negative_volume_rows: 0
zero_volume_rows: 1726249
Duplicate timestamp ranges:

text
2021-10-31 19:00:00+00:00 through 2021-10-31 19:59:00+00:00: 60 duplicate timestamp values
2022-10-30 19:00:00+00:00 through 2022-10-30 19:59:00+00:00: 60 duplicate timestamp values
2023-10-29 19:00:00+00:00 through 2023-10-29 19:59:00+00:00: 60 duplicate timestamp values
2024-10-27 19:00:00+00:00 through 2024-10-27 19:59:00+00:00: 60 duplicate timestamp values
2025-10-26 19:00:00+00:00 through 2025-10-26 19:59:00+00:00: 60 duplicate timestamp values
First 20 missing minutes reported by the loader:

text
2021-01-04 17:00:00+00:00
2021-01-04 17:01:00+00:00
2021-01-04 17:02:00+00:00
2021-01-04 17:03:00+00:00
2021-01-04 17:04:00+00:00
2021-01-04 17:05:00+00:00
2021-01-04 17:06:00+00:00
2021-01-04 17:07:00+00:00
2021-01-04 17:08:00+00:00
2021-01-04 17:09:00+00:00
2021-01-04 17:10:00+00:00
2021-01-04 17:11:00+00:00
2021-01-04 17:12:00+00:00
2021-01-04 17:13:00+00:00
2021-01-04 17:14:00+00:00
2021-01-04 17:15:00+00:00
2021-01-04 17:16:00+00:00
2021-01-04 17:17:00+00:00
2021-01-04 17:18:00+00:00
2021-01-04 17:19:00+00:00
Last 20 missing minutes reported by the loader:

text
2025-12-30 17:40:00+00:00
2025-12-30 17:41:00+00:00
2025-12-30 17:42:00+00:00
2025-12-30 17:43:00+00:00
2025-12-30 17:44:00+00:00
2025-12-30 17:45:00+00:00
2025-12-30 17:46:00+00:00
2025-12-30 17:47:00+00:00
2025-12-30 17:48:00+00:00
2025-12-30 17:49:00+00:00
2025-12-30 17:50:00+00:00
2025-12-30 17:51:00+00:00
2025-12-30 17:52:00+00:00
2025-12-30 17:53:00+00:00
2025-12-30 17:54:00+00:00
2025-12-30 17:55:00+00:00
2025-12-30 17:56:00+00:00
2025-12-30 17:57:00+00:00
2025-12-30 17:58:00+00:00
2025-12-30 17:59:00+00:00
Interpretation
The explicit drop_exact policy successfully loaded both real HistData files after removing exact duplicate OHLCV rows.

For both symbols:

duplicate metadata matched prior diagnostics,
output index was UTC,
output index was monotonic increasing,
output index had no duplicates,
OHLC values were structurally valid,
no non-positive OHLC rows were found,
no bad OHLC rows were found,
no negative volume rows were found.
However, the missing-minute counts are large:

text
USDJPY missing minutes: 816687
XAUUSD missing minutes: 898809
Also, all observed volume values are zero:

text
USDJPY zero-volume rows: 1808431
XAUUSD zero-volume rows: 1726249
These findings require further coverage, session, and source-quality analysis before HistData can be accepted as a research source.

Current Status
HistData remains not accepted as a research source.

This check only establishes that the dedicated HistData loader can read the two real raw files with the explicit audited duplicate policy.

Explicit Non-Actions
This phase did not:

modify raw HistData files,
write derived data files,
run H017,
combine HistData M1 with Exness H4,
tune strategy parameters,
change the cost model,
accept HistData as a research source.
Recommended Next Work
Before any H017 validation on HistData, the project still needs:

derived-data provenance plan,
missing-minute coverage analysis,
weekend behavior analysis,
XAUUSD metals session-break analysis,
timezone/source-session reconciliation,
broker mismatch assessment versus Exness,
final HistData source acceptance or rejection decision.
