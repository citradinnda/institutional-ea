# Broker-Native Expanded Strict Bridge-Window Preflight Result

Date: 2026-05-03

Phase: 3.26-an

## Purpose

This document records the read-only real-data verification of the strict common H4/M1 bridge-window preflight implemented in:

- `quantcore/data/bridge_windows.py`
- `tests/test_bridge_windows.py`

The preflight is required before any expanded broker-native H017 event-driven validation run.

## Scope

Accepted source under test:

- Broker: Exness demo MT5 export
- Symbols: USDJPY and XAUUSD
- Timeframes: broker-native H4 and broker-native M1
- Loader timezone: `Europe/Athens`, converted to UTC by `load_mt5_csv`

Raw local files checked:

- `data/raw/USDJPY/H4.csv`
- `data/raw/USDJPY/M1.csv`
- `data/raw/XAUUSD/H4.csv`
- `data/raw/XAUUSD/M1.csv`

These raw files are gitignored and were not committed.

## Strict Bridge-Window Rule

A bridge window is accepted only when all of the following are true:

1. USDJPY has a broker-native H4 bar at the H4 timestamp.
2. XAUUSD has a broker-native H4 bar at the same H4 timestamp.
3. USDJPY's next H4 timestamp is exactly four hours later.
4. XAUUSD's next H4 timestamp is exactly four hours later.
5. USDJPY has exactly 240 M1 bars in `[H4 timestamp, H4 timestamp + 4 hours)`.
6. XAUUSD has exactly 240 M1 bars in `[H4 timestamp, H4 timestamp + 4 hours)`.
7. No imputation is used.
8. No forward-fill is used.
9. No backfill is used.
10. No synthetic bars are inserted.
11. No silent deduplication is performed.
12. HistData is not used.

## Result

The strict common complete H4/M1 bridge-window preflight passed.

Expected values were confirmed:

- accepted common complete bridge windows: `5476`
- first accepted timestamp UTC: `2021-07-02 13:00:00+00:00`
- last accepted timestamp UTC: `2026-04-30 01:00:00+00:00`

## Loaded MT5 Export Counts

USDJPY H4:

- input rows: `8713`
- loaded bars: `8713`
- earliest UTC: `2018-07-02 21:00:00+00:00`
- latest UTC: `2026-04-30 05:00:00+00:00`

USDJPY M1:

- input rows: `1785312`
- loaded bars: `1785312`
- earliest UTC: `2018-07-02 21:00:00+00:00`
- latest UTC: `2026-04-30 07:00:00+00:00`

XAUUSD H4:

- input rows: `8658`
- loaded bars: `8658`
- earliest UTC: `2018-06-27 21:00:00+00:00`
- latest UTC: `2026-04-30 05:00:00+00:00`

XAUUSD M1:

- input rows: `1704907`
- loaded bars: `1704907`
- earliest UTC: `2018-06-27 21:00:00+00:00`
- latest UTC: `2026-04-30 07:00:00+00:00`

## Strict Assessment Counts

- candidate common H4 timestamps: `8654`
- USDJPY complete windows: `5685`
- XAUUSD complete windows: `6149`
- common complete windows: `5476`
- accepted windows: `5476`
- first accepted timestamp UTC: `2021-07-02 13:00:00+00:00`
- last accepted timestamp UTC: `2026-04-30 01:00:00+00:00`
- USDJPY-only complete windows: `209`
- XAUUSD-only complete windows: `673`
- rejected common candidate timestamps: `3178`

## Rejection Counts

Rejection reasons are diagnostic only. A single candidate timestamp can have more than one rejection reason.

- `usdjpy_m1_count_not_expected`: `2969`
- `usdjpy_missing_next_h4_timestamp`: `1`
- `usdjpy_non_4h_next_h4_delta`: `1179`
- `xauusd_m1_count_not_expected`: `2505`
- `xauusd_missing_next_h4_timestamp`: `1`
- `xauusd_non_4h_next_h4_delta`: `1193`

## Interpretation

The expanded broker-native source now has a tested strict preflight/filter that identifies the exact accepted common complete H4/M1 bridge-window set required for future expanded H017 validation.

This result means the data window filter is ready for integration into a future validation runner.

This result does not mean H017 is promotable.

This result does not approve live trading.

This result does not authorize HistData for H017 validation.

## Operational Restrictions Still In Force

Do not run H017 expanded validation until the future validation runner consumes this strict accepted timestamp set and refuses incomplete windows.

Do not use `scripts/run_h017_event_real.py` as the expanded validation run unless it is updated or wrapped to enforce the strict complete-window set.

Do not tune H017.

Do not change the cost model.

Do not use HistData.

Do not impute missing M1 bars.

Do not forward-fill or backfill M1 bars.

Do not synthesize bars.

Do not commit raw data.

## Execution Note

The diagnostic was read-only.

No H017 run was performed.

No derived datasets were written.

Raw files were not modified.
