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

---

### Run 2026-05-04 — Expanded broker-native strict validation failed by insolvency

#### Operator context

Run date: 2026-05-04

Data source: Exness demo MT5 broker-native H4/M1 exports

Broker/account environment: Exness MT5 demo, broker timezone Europe/Athens

Validation script:

    scripts/run_h017_strict_event_real.py

Detailed result documents:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md
    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt

#### Strict bridge-window preflight

STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True

Accepted strict bridge-window start: 2021-07-02 13:00:00+00:00

Accepted strict bridge-window end: 2026-04-30 01:00:00+00:00

Accepted common complete H4/M1 bridge windows: 5476

Expected M1 bars per H4 window: 240

No M1 imputation, forward-fill, backfill, or synthetic bars were used.

HistData was not used.

Raw broker CSV files remained local and were not committed.

#### Research sufficiency

RESEARCH VALIDATION SUFFICIENT: True

Important qualification:

Research sufficiency means the expanded broker-native source and strict complete-window preflight were sufficient to run event-driven validation. It does not mean H017 passed validation.

#### Event-driven backtest output

H017 STRICT EVENT BACKTEST COMPLETED: False

Failure reason: insolvency

Fatal interval:

    decision_time=2021-07-06 01:00:00+00:00
    entry_time=2021-07-06 05:00:00+00:00
    forced_exit_time=2021-07-06 09:00:00+00:00
    interval_start_equity_usd=9847.56
    interval_pnl_usd=-11835.26
    ending_equity_usd=-1987.71
    interval_return_pct=-120.18
    interval_fills=2

Fatal USDJPY fill summary:

    side=buy
    entry_price=110.775000000
    exit_price=110.765228764
    lots=518.77
    pnl_quote=-506902.42
    commission=7262.78
    exit_reason=stop

Fatal XAUUSD fill summary:

    side=buy
    entry_price=1807.480000000
    exit_price=1809.622000000
    lots=0.02
    pnl_quote=4.28
    commission=0.40
    exit_reason=signal_flip

#### H017 claim output

H017 promotable: False

Live trading approved: False

PSR, DSR, and MinTRL were not reached because strict event validation failed closed by insolvency.

#### Interpretation

Pipeline smoke passed: True

Research-grade validation passed: False

Is this run promotable evidence? No.

If not promotable, why not?

The strict expanded broker-native source preflight passed, but H017 failed event-driven validation by account insolvency on a complete strict bridge window.

This was not a missing-M1 problem.

The immediate pathological event was a USDJPY long sized to 518.77 lots on an account with approximately 9847.56 USD of interval-start equity.

Prior diagnostics localized the sizing pathology to a near-zero raw stop distance:

    raw H4 entry open=110.770000000
    H017 long stop=110.770240804

The current event engine sizes from:

    abs(raw H4 entry open - stop_price)

before entry spread is applied.

This run records H017 failure. It does not silently change sizing semantics, cost semantics, H017 parameters, or strategy logic.

#### Research verdict

STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True

H017 STRICT EVENT BACKTEST COMPLETED: False

H017 VALIDATION FAILED BY INSOLVENCY: True

H017 PROMOTABLE BY CLAIM: False

EXPANDED VALIDATION IS RESEARCH EVIDENCE ONLY: True

LIVE TRADING APPROVED: False

#### Notes

Additional observations:

- H017 is now classified as failed / not promotable under strict expanded broker-native event validation.
- Broker-native source acceptance remains conditional and restricted to complete bridge windows.
- Source acceptance is not strategy promotion.
- The strict expanded result supersedes the earlier short-window baseline interpretation where H017 was alive but not promotable.
- The raw-entry versus executable-entry sizing question remains an explicit future execution-model semantics question, not a silent fix.

Operational issues:

- The strict runner reported insolvency cleanly without a Python traceback.
- The script exit code was 1, as expected for fail-closed validation failure.
- Raw data files remained local and were not committed.
- HistData was not used.
- No derived datasets were written.

Follow-up action:

Do not tune H017.

Do not rerun broad real-data validation as if H017 is alive or promotable.

Do not change raw-entry versus executable-entry sizing semantics without explicit tests and documentation.

Next recommended work is to decide the epistemic response to this failed hypothesis.
