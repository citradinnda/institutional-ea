# Broker-Native Expanded Missingness-by-Time-Bucket Diagnostic

Phase: 3.26-aj  
Status: Completed diagnostic  
Scope: Expanded broker-native USDJPY and XAUUSD M1 dense candidate region

## Purpose

This diagnostic quantifies broker-native M1 missingness by time bucket before any source-acceptance decision.

It uses the common dense calendar span shared by USDJPY and XAUUSD.

## Restrictions

No H017 validation was run.

No strategy tuning was performed.

No derived M1 or H4 datasets were written.

No raw broker-native files were modified.

No raw broker-native files were committed.

This diagnostic does not accept expanded broker-native M1 as an H017 validation source.

## Dense Region and Calendar Scope

- Dense-region start rule: `2021-07-01 00:00:00+00:00`
- Common calendar start UTC: `2021-07-01 21:00:00+00:00`
- Common calendar end UTC: `2026-04-30 07:00:00+00:00`
- Calendar minutes inclusive: `2539321`

The sparse prefix from 2018 through 2021-06 remains excluded.

## Output

Detailed output is stored in:

- `docs/operations/BROKER_NATIVE_EXPANDED_MISSINGNESS_BY_TIME_BUCKET_DIAGNOSTIC_OUTPUT.txt`

## Summary

### USDJPY

- Dense observed bars: `1784379`
- First observed UTC timestamp: `2021-07-01 21:00:00+00:00`
- Last observed UTC timestamp: `2026-04-30 07:00:00+00:00`
- Calendar minutes: `2539321`
- Observed minutes: `1784379`
- Missing calendar minutes: `754942`
- Observed percent of calendar: `70.269926`
- Missing percent of calendar: `29.730074`
- Missing cluster count: `11277`
- Largest missing cluster in minutes: `4330`
- Single-minute missing clusters: `7941`
- Small 2-to-29-minute missing clusters: `3064`
- Daily-break-like 30-to-90-minute missing clusters: `3`
- Weekend-or-longer missing clusters, 721+ minutes: `264`

### XAUUSD

- Dense observed bars: `1703974`
- First observed UTC timestamp: `2021-07-01 21:00:00+00:00`
- Last observed UTC timestamp: `2026-04-30 07:00:00+00:00`
- Calendar minutes: `2539321`
- Observed minutes: `1703974`
- Missing calendar minutes: `835347`
- Observed percent of calendar: `67.103529`
- Missing percent of calendar: `32.896471`
- Missing cluster count: `1428`
- Largest missing cluster in minutes: `4387`
- Single-minute missing clusters: `107`
- Small 2-to-29-minute missing clusters: `60`
- Daily-break-like 30-to-90-minute missing clusters: `958`
- Weekend-or-longer missing clusters, 721+ minutes: `264`

## Interpretation Guardrails

Calendar missingness is not automatically a data defect.

Weekend closures, holidays, XAUUSD daily breaks, and instrument-session differences may be legitimate.

This diagnostic should be interpreted together with:

1. The expanded session-boundary diagnostic.
2. The expanded common-window diagnostic.
3. The earlier H4/M1 aggregation compatibility diagnostic.

A future source-acceptance checkpoint must decide whether any missingness pattern is acceptable for H017 validation.

## Non-Acceptance Statement

The expanded broker-native M1 source remains a promising candidate only.

This diagnostic does not authorize H017 validation.

H017 remains alive but not promotable.

Research validation remains blocked pending explicit source acceptance.

Live trading remains unauthorized.
