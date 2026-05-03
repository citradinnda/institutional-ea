# Broker-Native Expanded Session-Boundary Diagnostic

Phase: 3.26-ah  
Status: Completed diagnostic  
Scope: Expanded broker-native USDJPY and XAUUSD M1 dense candidate region

## Purpose

This diagnostic reviews broker-native M1 session behavior before any source-acceptance decision.

It focuses on the dense candidate region only and intentionally excludes the sparse 2018 through 2021-06 prefix from validation thinking.

## Restrictions

No H017 validation was run.

No strategy tuning was performed.

No derived M1 or H4 datasets were written.

No raw broker-native files were modified.

No raw broker-native files were committed.

This diagnostic does not accept expanded broker-native M1 as an H017 validation source.

## Dense Region Rule

The diagnostic applies a dense-region start rule of `2021-07-01 00:00:00+00:00`.

The sparse prefix from 2018 through 2021-06 remains excluded.

## Output

Detailed output is stored in:

- `docs/operations/BROKER_NATIVE_EXPANDED_SESSION_BOUNDARY_DIAGNOSTIC_OUTPUT.txt`

## Summary

### USDJPY

- Dense-region bars: `1784379`
- Dense-region first UTC timestamp: `2021-07-01 21:00:00+00:00`
- Dense-region last UTC timestamp: `2026-04-30 07:00:00+00:00`
- Duplicate timestamps in dense region: `False`
- Observed UTC dates: `1518`
- Gap events greater than one minute: `11277`
- Most common gap duration: `0 days 00:02:00`
- Largest gap duration: `3 days 00:11:00`
- Daily-break-like gaps between 30 and 90 minutes: `3`
- Small intraday gaps between 2 and 29 minutes: `11005`

Top Sunday first-observed UTC minute times:
  - `18:05`: 75
  - `20:05`: 56
  - `18:06`: 30
  - `20:06`: 19
  - `19:05`: 13

Top Friday last-observed UTC minute times:
  - `17:58`: 141
  - `19:58`: 81
  - `18:58`: 15
  - `19:57`: 7
  - `18:57`: 3

### XAUUSD

- Dense-region bars: `1703974`
- Dense-region first UTC timestamp: `2021-07-01 21:00:00+00:00`
- Dense-region last UTC timestamp: `2026-04-30 07:00:00+00:00`
- Duplicate timestamps in dense region: `False`
- Observed UTC dates: `1510`
- Gap events greater than one minute: `1428`
- Most common gap duration: `0 days 01:04:00`
- Largest gap duration: `3 days 01:08:00`
- Daily-break-like gaps between 30 and 90 minutes: `958`
- Small intraday gaps between 2 and 29 minutes: `167`

Top Sunday first-observed UTC minute times:
  - `19:05`: 127
  - `21:05`: 68
  - `20:05`: 15
  - `21:01`: 10
  - `19:00`: 9

Top Friday last-observed UTC minute times:
  - `17:57`: 118
  - `19:57`: 62
  - `17:58`: 19
  - `19:58`: 15
  - `18:57`: 13

## Interpretation Guardrails

Session gaps are not automatically defects.

They become defects only if they contradict expected broker/instrument trading behavior or create unexplained holes inside active sessions.

XAUUSD and USDJPY may have structurally different session behavior.

This diagnostic should be read together with the planned cross-symbol common-window diagnostic before any source-acceptance checkpoint.

## Non-Acceptance Statement

The expanded broker-native M1 source remains a promising candidate only.

This diagnostic does not authorize H017 validation.

H017 remains alive but not promotable.

Research validation remains blocked pending explicit source acceptance.

Live trading remains unauthorized.
