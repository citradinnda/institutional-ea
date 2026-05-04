# Hypothesis Ledger

## Purpose

This ledger records the lifecycle status of trading hypotheses.

It is intentionally separate from operational run logs. Run logs record what was executed. This ledger records the current epistemic status of each hypothesis.

Status meanings:

- Failed: hypothesis is not promotable under current evidence.
- Alive: hypothesis remains under research but is not promotable.
- Promotable: hypothesis has passed the required validation gates, but still does not imply live-trading approval.
- Live-approved: separate production-readiness approval after validation, operations, monitoring, and risk review.

Live trading is never approved by this ledger alone.

## Current Project Status

Current candidate status:

- H017: Failed / not promotable.

Current boundary-planning status:

- H018 boundary planning is opened for governance only.
- H018 is not validated.
- H018 is not promotable.
- H018 does not approve live trading or Phase 4 execution work.

Current live-trading status:

- Live trading approved: False.

Current validation source status:

- Exness demo MT5 broker-native USDJPY and XAUUSD H4/M1 exports are conditionally accepted only under strict complete-window rules.
- HistData remains rejected for H017 validation under current evidence.

Current strict expanded validation reference:

- docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md
- docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt
- docs/operations/H017_EVENT_VALIDATION_RUN_LOG.md

Current H018 boundary reference:

- docs/operations/H018_BOUNDARY_DECISION_PLAN.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md

## Graveyard Summary Before H017

### H001

Status: Failed.

Reason:

Backtests without intrabar stop-loss and take-profit simulation are fictional for this project. M1 bars are required inside H4 bars to resolve fills conservatively.

### H002-H003

Status: Failed.

Reason:

ATR-based per-symbol stops are mandatory, and trade frequency must be low enough to amortize realistic costs.

### H004a

Status: Failed.

Reason:

Single-seed model results are unreliable. Multi-seed ensembles or equivalent robustness discipline are required before treating model evidence as stable.

### H005

Status: Failed.

Reason:

Stacked multi-symbol models failed on heterogeneous instruments. Per-symbol modeling is required when machine learning is used.

### H006-H007

Status: Failed.

Reason:

Confidence filters are not risk management. Machine learning may choose entries, but deterministic rules must manage risk.

### H008-H010

Status: Failed.

Reason:

High Sharpe with extreme kurtosis is unsafe. Machine learning on basic technical features cannot be trusted as the risk manager.

### H011-H013

Status: Failed / superseded.

Reason:

Deterministic ATR stops, chandelier exits, and volatility-targeted sizing showed edge on USDJPY, but single-asset tail risk remained too high.

### H014-H016

Status: Failed / superseded.

Reason:

Two-asset USDJPY plus XAUUSD reduced kurtosis and improved Sortino, but one percent per-trade risk was not one percent portfolio risk when trades overlapped. Drawdown breached the project risk ceiling.

## H017

### Claim

H017 extends H016 with a portfolio heat governor.

The intended improvement was to cap simultaneous open risk using correlation-adjusted exposure while retaining the USDJPY plus XAUUSD two-asset core.

### Core Mechanics

Symbols:

- USDJPY
- XAUUSD

Core features:

- Donchian breakout entries.
- Wilder ATR.
- Chandelier exits.
- Volatility-targeted sizing.
- Portfolio heat governor.
- Event-driven validation using broker-native H4 decisions and M1 intrabar fill resolution.

### Validation Source

Accepted validation source for the strict expanded run:

- Exness demo MT5 broker-native exports.
- Broker timezone: Europe/Athens.
- Timeframes: broker-native H4 and broker-native M1.
- Symbols: USDJPY and XAUUSD.

Rejected sources for H017 validation:

- HistData.
- HistData-built H4.
- Broker H4 plus HistData M1 hybrid.
- Any incomplete H4/M1 bridge window.
- Any imputed, forward-filled, backfilled, or synthetic M1 bar.

### Strict Expanded Validation Evidence

Strict bridge-window preflight:

- Passed: True.
- Accepted common complete H4/M1 bridge windows: 5476.
- Accepted start: 2021-07-02 13:00:00+00:00.
- Accepted end: 2026-04-30 01:00:00+00:00.
- Required M1 bars per H4 window: 240.
- No M1 imputation, forward-fill, backfill, or synthetic bars were used.

Strict event-driven validation:

- Completed: False.
- Failure reason: insolvency.
- H017 promotable by claim: False.
- Live trading approved: False.

Fatal interval:

- Decision time: 2021-07-06 01:00:00+00:00.
- Entry time: 2021-07-06 05:00:00+00:00.
- Forced exit time: 2021-07-06 09:00:00+00:00.
- Interval start equity: 9847.56 USD.
- Interval PnL: -11835.26 USD.
- Ending equity: -1987.71 USD.
- Interval return: -120.18 percent.
- Interval fills: 2.

Fatal USDJPY fill:

- Side: buy.
- Entry price: 110.775000000.
- Exit price: 110.765228764.
- Lots: 518.77.
- PnL quote: -506902.42.
- Commission: 7262.78.
- Exit reason: stop.

### Interpretation

H017 failed strict expanded broker-native event-driven validation by account insolvency.

This was not a data preflight failure.

This was not a missing-M1 problem.

The fatal interval was a complete strict bridge window.

The immediate pathological event was a USDJPY long sized to 518.77 lots on an account with approximately 9847.56 USD of interval-start equity.

Prior diagnostics localized the sizing pathology to a near-zero raw stop distance:

- Raw H4 entry open: 110.770000000.
- H017 long stop: 110.770240804.

The long stop was slightly above the raw H4 entry open while below the cost-adjusted buy entry.

The current event engine sizes from:

    abs(raw H4 entry open - stop_price)

before entry spread is applied.

This ledger records the failure. It does not change sizing semantics, cost semantics, H017 parameters, or strategy logic.

### Status

H017 status:

- Failed.
- Not promotable.
- Not approved for live trading.

### Follow-Up Boundary

Do not tune H017 to hide this result.

Do not change H017 parameters as a repair.

Do not change cost assumptions casually.

Do not silently change raw-entry versus executable-entry sizing semantics.

Do not use HistData for H017 validation.

Do not broaden to more symbols.

Do not add machine learning.

Any future raw-entry versus executable-entry sizing change must be explicit, tested, documented, and treated as an execution-model semantics decision.

Implemented follow-up execution-validation guard:

- Raw-entry directional invalid-stop guard is implemented in `quantcore/backtest/h017_event.py`.
- Error class: `H017EventInvalidStopError`.
- Under current raw-entry sizing semantics, long/buy stops must be below raw H4 entry open and short/sell stops must be above raw H4 entry open.
- Invalid directional stops fail closed.
- Equality is invalid: long/buy stops equal to raw H4 entry open and short/sell stops equal to raw H4 entry open fail closed.
- Invalid directional stops are not skipped silently and are not clipped.
- This guard does not promote H017.
- This guard does not approve live trading.
- This guard does not authorize a broad real-data rerun.

Any successor strategy should be opened as a new hypothesis, such as H018, rather than treating H017 as repaired without a new hypothesis boundary.
