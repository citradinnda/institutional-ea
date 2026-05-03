# MT5 M1 Acquisition Attempts

## Purpose

This document records attempts to acquire longer broker-native M1 history from MetaTrader 5.

The goal is to preserve operational evidence about what was tried, what changed, and what still blocks research-grade H017 event validation.

This log is separate from the H017 event validation run log.

- This file records data acquisition attempts.
- The H017 event validation run log records script outputs after data is available.

## Current blocker

H017 event-driven validation currently requires longer M1 history for both USDJPY and XAUUSD.

The desired M1 start is tied to the clean H4 start discovered by the leakage scan:

    2021-07-02 00:00:00+00:00

Current available M1 coverage remains much later than that.

As of the baseline validation run on 2026-05-03:

    USDJPY M1 earliest timestamp: 2026-01-26 03:09:00+00:00
    USDJPY M1 latest timestamp: 2026-04-30 07:00:00+00:00

    XAUUSD M1 earliest timestamp: 2026-01-20 02:22:00+00:00
    XAUUSD M1 latest timestamp: 2026-04-30 07:00:00+00:00

    Clean common event window start: 2026-01-26 03:09:00+00:00
    Clean common event window end: 2026-04-29 09:00:00+00:00

    Common H4 bar count: 411
    Minimum required H4 bars: 1512

    RESEARCH VALIDATION SUFFICIENT: False

## Rules

Do not commit raw MT5 export files.

The local raw M1 files are:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

These files are intentionally ignored by git.

Do not tune H017 parameters to fit the current short M1 window.

Do not treat the current profitable short-window event result as validated edge.

Do not silently switch brokers, account servers, export formats, or data vendors.

If a material data source change is made, record it explicitly and consider a separate decision record plus loader-validation phase.

## Attempt log

### Attempt 2026-05-03 — Broker-native MT5 M1 refresh attempt

#### Method

Used local MetaTrader 5 broker-native history/export workflow to attempt to obtain longer M1 history for:

- USDJPY
- XAUUSD

The intended target files were:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

#### Result

The attempt did not improve effective M1 coverage.

After the attempt, the H017 real event script still reported:

    USDJPY M1 earliest timestamp: 2026-01-26 03:09:00+00:00
    USDJPY M1 latest timestamp: 2026-04-30 07:00:00+00:00

    XAUUSD M1 earliest timestamp: 2026-01-20 02:22:00+00:00
    XAUUSD M1 latest timestamp: 2026-04-30 07:00:00+00:00

    Clean common event window start: 2026-01-26 03:09:00+00:00
    Clean common event window end: 2026-04-29 09:00:00+00:00

    Common H4 bar count: 411
    Minimum required H4 bars: 1512

    RESEARCH VALIDATION SUFFICIENT: False

#### Interpretation

The broker terminal currently appears to expose only this amount of M1 history for these symbols, account, and server.

This attempt did not create new research-grade evidence.

The existing event pipeline still works, but H017 remains blocked by insufficient M1 coverage.

#### Repository impact

No raw data files were committed.

Git status remained clean before and after the validation run.

#### Follow-up options

Possible next actions are:

1. Try a different broker account server within the same broker, if available.
2. Try another broker-native MT5 source, but only with explicit documentation.
3. Create a data-vendor decision record before using any non-broker data source.
4. Add loader-validation tests before accepting a new vendor format.
5. Keep H017 marked alive but not promotable until research-grade event validation is available.

## New attempt template

Copy this section for future data acquisition attempts.

### Attempt YYYY-MM-DD — Short description

#### Method

Data source:

Broker:

Account/server environment:

Symbols attempted:

Files targeted:

Export method:

#### Result

Did local M1 files change?

USDJPY M1 earliest timestamp after attempt:

USDJPY M1 latest timestamp after attempt:

XAUUSD M1 earliest timestamp after attempt:

XAUUSD M1 latest timestamp after attempt:

Clean common event window start after attempt:

Clean common event window end after attempt:

Common H4 bar count after attempt:

Minimum required H4 bars:

RESEARCH VALIDATION SUFFICIENT:

#### Interpretation

Did coverage improve?

Is this research-grade evidence?

Does H017 remain blocked?

#### Repository impact

Was git status clean before the attempt?

Was git status clean after the attempt?

Were raw data files kept out of git?

#### Follow-up action

Next action:
