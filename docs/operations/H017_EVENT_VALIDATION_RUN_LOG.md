# H017 Event Validation Run Log

## Purpose

This document records real-data H017 event-driven validation attempts after local MetaTrader 5 M1 export updates.

The goal is to preserve operational evidence, not to tune the strategy.

Each run should answer one question:

Did the available M1 data become sufficient for research-grade event-driven validation?

## When to add a new entry

Add a new entry after each attempt to improve or refresh the local MT5 M1 exports, especially after replacing either of these files:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Raw data files must remain local and must not be committed to git.

## Command to run

From the repository root:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    python scripts\run_h017_event_real.py

## Required success marker

The important research sufficiency line is:

    RESEARCH VALIDATION SUFFICIENT: True

If the output says:

    RESEARCH VALIDATION SUFFICIENT: False

then the run may show that the pipeline works, but it is not promotable research evidence.

## Important warnings

Do not tune H017 parameters to fit a short M1 window.

Do not treat a profitable short-window result as validated edge.

Do not silently switch data vendors.

If a different broker, account environment, export format, or data vendor is used, record it clearly. A material vendor change may require a separate decision record and loader-validation phase.

Do not commit raw MT5 export files.

## Run entry template

Copy this template for each new real-data event validation attempt.

### Run YYYY-MM-DD

#### Operator context

Run date:

Data source:

Broker/account environment:

MT5 terminal source:

Notes on export process:

#### Local file coverage

USDJPY M1 earliest timestamp:

USDJPY M1 latest timestamp:

XAUUSD M1 earliest timestamp:

XAUUSD M1 latest timestamp:

#### Clean common event window

Clean common event window start:

Clean common event window end:

Common H4 bar count:

Minimum required H4 bars:

#### Research sufficiency

RESEARCH VALIDATION SUFFICIENT:

Coverage failure reasons, if any:

#### Event-driven backtest output

Fill count:

Starting equity:

Ending equity:

Total return percent:

Max drawdown:

Sharpe:

#### H017 claim output

PSR:

MinTRL feasible:

MinTRL required n:

MinTRL observed n:

DSR:

H017 promotable:

#### Interpretation

Pipeline smoke passed:

Research-grade validation passed:

Is this run promotable evidence?

If not promotable, why not?

#### Notes

Additional observations:

Operational issues:

Follow-up action:

## Interpretation guide

If RESEARCH VALIDATION SUFFICIENT is False, classify the run as pipeline evidence only.

If RESEARCH VALIDATION SUFFICIENT is True but H017 promotable is False, classify the run as research-grade non-promotion evidence.

If RESEARCH VALIDATION SUFFICIENT is True and H017 promotable is True, do not immediately go live. That result should trigger a separate review phase covering drawdown, costs, robustness, operational failure modes, and production readiness.

---

### Run 2026-05-03 — Baseline before additional M1 acquisition

#### Operator context

Run date: 2026-05-03

Data source: Local MetaTrader 5 exports

Broker/account environment: Exness MT5, broker timezone Europe/Athens

MT5 terminal source: Local Windows MT5 terminal

Notes on export process: Baseline run using existing local H4 and M1 files before any additional M1 history acquisition.

#### Local file coverage

USDJPY M1 earliest timestamp: 2026-01-26 03:09:00+00:00

USDJPY M1 latest timestamp: 2026-04-30 07:00:00+00:00

XAUUSD M1 earliest timestamp: 2026-01-20 02:22:00+00:00

XAUUSD M1 latest timestamp: 2026-04-30 07:00:00+00:00

#### Clean common event window

Clean common event window start: 2026-01-26 03:09:00+00:00

Clean common event window end: 2026-04-29 09:00:00+00:00

Common H4 bar count: 411

Minimum required H4 bars: 1512

#### Research sufficiency

RESEARCH VALIDATION SUFFICIENT: False

Coverage failure reasons, if any:

- M1 common start is later than the desired clean H4 start. Desired start was 2021-07-02 00:00:00+00:00. Actual common start was 2026-01-26 03:09:00+00:00.
- Common H4 sample is shorter than one approximate H4 trading year. Minimum required H4 bars were 1512. Actual common H4 bars were 411.

#### Event-driven backtest output

Fill count: 470

Starting equity: 10000.00 USD

Ending equity: 16145.60 USD

Total return percent: 61.46

Max drawdown: -33.65 percent

Sharpe: 1.3218 annualized

#### H017 claim output

PSR: 0.8662, failed threshold 0.95

MinTRL feasible: True

MinTRL required n: 1034

MinTRL observed n: 470

DSR: Skipped, no sr_estimates provided

H017 promotable: False

#### Interpretation

Pipeline smoke passed: True

Research-grade validation passed: False

Is this run promotable evidence? No.

If not promotable, why not?

The event-driven pipeline works, but the available M1 history is too short for research-grade validation. The profitable short-window result must not be treated as validated edge.

The -33.65 percent drawdown is a serious risk signal, but this short M1 window is still not sufficient for a full research conclusion.

#### Notes

Additional observations:

- H4 data still requires leakage trimming because the early H4 export contains daily bars disguised as H4 bars before 2021-07-02.
- The current clean common event window starts in 2026, which is much later than the desired clean H4 start of 2021-07-02.
- H017 remains alive but not promotable.

Operational issues:

- No script failure.
- No missing file preflight failure.
- Raw data files remained local and were not committed.

Follow-up action:

Acquire longer broker-native M1 exports for USDJPY and XAUUSD, then rerun:

    python scripts\run_h017_event_real.py

Only consider the run research-grade if the output eventually reports:

    RESEARCH VALIDATION SUFFICIENT: True
