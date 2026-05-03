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
