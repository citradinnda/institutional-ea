# Broker-Native Expanded Strict Bridge-Window Contiguity Diagnostic

Date: 2026-05-03

Phase: 3.26-ao

## Purpose

This document records a read-only diagnostic performed after implementing and verifying the strict common H4/M1 bridge-window preflight.

The goal was to determine whether the accepted strict bridge-window timestamps can be used by simply filtering the H4 dataframes before calling the existing event-driven H017 backtest.

They cannot.

## Background

The strict bridge-window preflight accepts a timestamp only when:

1. USDJPY and XAUUSD both have a broker-native H4 bar at that timestamp.
2. Both symbols have the next H4 timestamp exactly four hours later.
3. Both symbols have exactly 240 M1 bars in `[timestamp, timestamp + 4 hours)`.
4. No imputation, forward-fill, backfill, synthetic bars, or HistData are used.

The accepted strict bridge-window set was previously verified as:

- accepted windows: `5476`
- first accepted timestamp UTC: `2021-07-02 13:00:00+00:00`
- last accepted timestamp UTC: `2026-04-30 01:00:00+00:00`

## Event Engine Timing Constraint

The existing event engine in `quantcore/backtest/h017_event.py` executes intervals using three adjacent H4 timestamps from the H017 decision index:

- `decision_time = index[i - 1]`
- `entry_time = index[i]`
- `forced_exit_time = index[i + 1]`

This means the event engine assumes the next row in the H4/H017 index is the next executable H4 bar.

If H4 data is filtered down to only accepted strict bridge-window timestamps, the next retained timestamp may be more than four hours later. That would create incorrect forced-exit intervals.

## Diagnostic Result

Accepted strict bridge-window summary:

- accepted count: `5476`
- first accepted timestamp UTC: `2021-07-02 13:00:00+00:00`
- last accepted timestamp UTC: `2026-04-30 01:00:00+00:00`

Accepted timestamp contiguity:

- adjacent deltas checked: `5475`
- four-hour adjacent deltas: `4148`
- non-four-hour adjacent deltas: `1327`

Event-engine interval implication:

- strict entry times from preflight: `5476`
- safe intervals if H4 were filtered to accepted timestamps only: `4148`
- unsafe gap intervals if H4 were filtered to accepted timestamps only: `1327`

## Gap Distribution

Non-four-hour accepted timestamp gaps:

- `0 days 08:00:00`: `836`
- `0 days 12:00:00`: `106`
- `0 days 16:00:00`: `44`
- `0 days 20:00:00`: `55`
- `1 days 00:00:00`: `23`
- `1 days 04:00:00`: `4`
- `1 days 08:00:00`: `3`
- `1 days 12:00:00`: `2`
- `1 days 20:00:00`: `1`
- `2 days 07:00:00`: `3`
- `2 days 08:00:00`: `174`
- `2 days 09:00:00`: `3`
- `2 days 11:00:00`: `1`
- `2 days 12:00:00`: `27`
- `2 days 13:00:00`: `1`
- `2 days 16:00:00`: `7`
- `2 days 17:00:00`: `1`
- `2 days 20:00:00`: `17`
- `3 days 00:00:00`: `6`
- `3 days 07:00:00`: `1`
- `3 days 08:00:00`: `7`
- `3 days 12:00:00`: `1`
- `3 days 20:00:00`: `2`
- `4 days 00:00:00`: `1`
- `6 days 00:00:00`: `1`

## Interpretation

The accepted strict bridge-window timestamps are not contiguous enough to be used as a simple filtered H4 index for the existing event engine.

A future strict expanded H017 validation runner must preserve native four-hour interval semantics.

## Required Future Runner Design Constraint

Do not implement the strict runner by simply doing:

- H4 equals H4 filtered to `accepted_timestamps`
- M1 equals M1 filtered broadly to the accepted range
- then calling `backtest_h017_event_driven(...)`

That would create invalid forced-exit intervals across gaps.

The future runner must instead use one of these safer designs:

1. Preserve the native H4 index and modify/prepare the decision exposure so non-accepted execution-entry windows produce no fills.
2. Add a strict wrapper around `backtest_h017_event_from_result(...)` that executes only intervals whose `entry_time` is in the accepted strict bridge-window set and whose `forced_exit_time` is exactly `entry_time + 4 hours`.
3. Add a dedicated strict event runner that explicitly skips invalid intervals while preserving the original native H4 timestamps for entry and forced-exit prices.

The preferred direction should be decided in a separate implementation phase after inspecting tests and APIs.

## Restrictions Still In Force

This diagnostic did not run H017.

This diagnostic did not write derived datasets.

This diagnostic did not modify raw data.

This diagnostic does not promote H017.

This diagnostic does not approve live trading.

HistData remains rejected for H017 validation.

Do not tune H017.

Do not change the cost model.
