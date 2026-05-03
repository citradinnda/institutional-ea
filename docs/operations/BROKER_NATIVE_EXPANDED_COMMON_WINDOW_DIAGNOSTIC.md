# Broker-Native Expanded Common-Window Diagnostic

Phase: 3.26-ai  
Status: Completed diagnostic  
Scope: Expanded broker-native USDJPY and XAUUSD M1/H4 dense candidate region

## Purpose

This diagnostic quantifies the common usable broker-native window across USDJPY and XAUUSD before any source-acceptance decision.

It checks both M1 timestamp overlap and complete H4/M1 bridge windows.

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

- `docs/operations/BROKER_NATIVE_EXPANDED_COMMON_WINDOW_DIAGNOSTIC_OUTPUT.txt`

## M1 Common-Window Summary

- Common start UTC: `2021-07-01 21:00:00+00:00`
- Common end UTC: `2026-04-30 07:00:00+00:00`
- Calendar minutes inclusive: `2539321`
- USDJPY observed minutes in common span: `1784379`
- XAUUSD observed minutes in common span: `1703974`
- Shared observed minutes: `1695042`
- USDJPY-only observed minutes: `89337`
- XAUUSD-only observed minutes: `8932`
- Neither-symbol calendar minutes: `746010`
- Shared observed percent of calendar: `66.751781`

## Complete H4/M1 Window Summary

### USDJPY

- Candidate H4 windows evaluated: `7779`
- Exact 4-hour next-delta windows: `7515`
- Complete 240-M1 windows: `5701`
- First complete window UTC: `2021-07-02 13:00:00+00:00`
- Last complete window UTC: `2026-04-30 01:00:00+00:00`

### XAUUSD

- Candidate H4 windows evaluated: `7724`
- Exact 4-hour next-delta windows: `7460`
- Complete 240-M1 windows: `6149`
- First complete window UTC: `2021-07-02 13:00:00+00:00`
- Last complete window UTC: `2026-04-30 01:00:00+00:00`

### Cross-symbol common complete H4/M1 windows

- Common complete H4/M1 windows: `5476`
- USDJPY-only complete H4/M1 windows: `225`
- XAUUSD-only complete H4/M1 windows: `673`
- First common complete H4/M1 window UTC: `2021-07-02 13:00:00+00:00`
- Last common complete H4/M1 window UTC: `2026-04-30 01:00:00+00:00`

## Interpretation Guardrails

This diagnostic measures common-window coverage only.

It does not decide whether the source is accepted.

A complete common H4/M1 window is necessary for future bridge-layer validation, but it is not sufficient by itself.

Session behavior, missingness patterns, and source-acceptance criteria must still be reviewed before any H017 validation.

## Non-Acceptance Statement

The expanded broker-native M1 source remains a promising candidate only.

This diagnostic does not authorize H017 validation.

H017 remains alive but not promotable.

Research validation remains blocked pending explicit source acceptance.

Live trading remains unauthorized.
