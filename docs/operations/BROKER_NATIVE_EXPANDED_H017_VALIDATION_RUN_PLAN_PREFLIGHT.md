# Broker-Native Expanded H017 Validation Run Plan and Preflight

Phase: 3.26-al

Status: run plan / preflight only

This document intentionally does not run H017.

It records the preflight findings needed before any expanded broker-native H017 validation run is allowed.

## Purpose

The expanded broker-native USDJPY and XAUUSD M1/H4 source has been conditionally accepted for a future H017 validation phase.

That source acceptance is not the same thing as strategy validation.

This phase defines the required run plan before executing H017 on the expanded broker-native data.

## Source Status

Accepted source for the future validation run:

- Exness demo MT5 broker-native exports
- USDJPY
- XAUUSD
- Broker-native H4
- Broker-native M1

Raw local files:

- data/raw/USDJPY/H4.csv
- data/raw/USDJPY/M1.csv
- data/raw/XAUUSD/H4.csv
- data/raw/XAUUSD/M1.csv

These files are gitignored by the root-anchored `/data/` rule and must not be committed.

HistData remains rejected for H017 validation under current evidence.

## Accepted Expanded Validation Window

The future validation run may only use common complete H4/M1 bridge windows.

Accepted future bridge-window range:

- first possible common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
- last possible common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00

Expected common complete H4/M1 bridge-window count:

- 5476

The sparse broker-native prefix from 2018 through 2021-06 remains excluded.

## Required Common Complete H4/M1 Bridge-Window Rule

A valid future H017 bridge window must satisfy all of the following:

1. USDJPY has a broker-native H4 bar at the H4 timestamp.
2. XAUUSD has a broker-native H4 bar at the same H4 timestamp.
3. For each symbol, the next H4 timestamp is exactly four hours later.
4. For USDJPY, the M1 window `[H4 timestamp, H4 timestamp + 4 hours)` contains exactly 240 M1 bars.
5. For XAUUSD, the M1 window `[H4 timestamp, H4 timestamp + 4 hours)` contains exactly 240 M1 bars.
6. No M1 imputation is used.
7. No M1 forward-fill is used.
8. No M1 backfill is used.
9. No synthetic bar insertion is used.
10. No HistData is used.

Any H4/M1 bridge window failing this rule must be excluded before H017 validation.

## APIs Inspected

The following existing APIs were inspected before this plan was written.

Strategy layer:

- `quantcore.strategy.h017.H017Config`
- `quantcore.strategy.h017.H017Result`
- `quantcore.strategy.h017.run_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None)`
- `quantcore.strategy.h017_claim.H017BacktestResult`
- `quantcore.strategy.h017_claim.H017Claim`
- `quantcore.strategy.h017_claim.backtest_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None)`
- `quantcore.strategy.h017_claim.build_h017_claim(...)`

Event-driven backtest layer:

- `quantcore.backtest.h017_event.H017EventBacktestResult`
- `quantcore.backtest.h017_event.backtest_h017_event_driven(...)`
- `quantcore.backtest.h017_event.backtest_h017_event_from_result(...)`

Execution and accounting layer:

- `quantcore.backtest.fill_engine.Fill`
- `quantcore.backtest.fill_engine.simulate_bracket_trade(...)`
- `quantcore.backtest.portfolio.InstrumentSpec`
- `quantcore.backtest.portfolio.PositionSize`
- `quantcore.backtest.portfolio.PortfolioResult`
- `quantcore.backtest.portfolio.get_default_instrument_spec(symbol)`
- `quantcore.backtest.portfolio.size_position_from_risk(...)`
- `quantcore.backtest.portfolio.fill_pnl_usd(...)`
- `quantcore.backtest.portfolio.build_portfolio_result(...)`
- `quantcore.backtest.cost_model.SymbolCostSpec`
- `quantcore.backtest.cost_model.ExecutionCost`
- `quantcore.backtest.cost_model.get_default_cost_spec(symbol)`
- `quantcore.backtest.cost_model.price_with_execution_costs(...)`

Data and preflight layer:

- `quantcore.data.mt5_loader.MT5LoadResult`
- `quantcore.data.mt5_loader.load_mt5_csv(path, broker_tz="Europe/Athens")`
- `quantcore.data.preflight.require_existing_files(...)`
- `quantcore.data.coverage.CoverageAssessment`
- `quantcore.data.coverage.assess_m1_research_coverage(...)`
- `quantcore.data.leakage.LeakageScan`
- `quantcore.data.leakage.detect_d1_leakage(...)`
- `quantcore.data.leakage.trim_to_common_start(...)`

## Important API Corrections Found During Inspection

Earlier remembered names were not all correct.

The portfolio module does not expose:

- `lots_for_risk`
- `instrument_spec`
- `position_size_lots`

The actual relevant names are:

- `get_default_instrument_spec`
- `size_position_from_risk`
- `PositionSize`

The cost model module does not expose:

- `ExecutionCostSpec`
- `ExecutionCostResult`
- `default_execution_costs`

The actual relevant names are:

- `SymbolCostSpec`
- `ExecutionCost`
- `get_default_cost_spec`

This confirms that future implementation must inspect actual APIs and must not rely on remembered names.

## Existing Event Script Finding

The existing script:

- `scripts/run_h017_event_real.py`

loads the four MT5 exports, applies existing H4 leakage trimming, trims to a broad common H4/M1 window, runs `backtest_h017_event_driven(...)`, then builds an H017 claim.

This script is useful as an older operational smoke path.

However, it is not sufficient for the expanded broker-native validation run because the inspected visible logic does not enforce the strict common complete H4/M1 bridge-window rule.

Specifically, it does not prove enforcement of:

- the accepted common complete bridge-window range,
- exactly 5476 common complete windows,
- exactly 240 M1 bars for USDJPY inside every included H4 interval,
- exactly 240 M1 bars for XAUUSD inside every included H4 interval,
- exclusion of incomplete bridge windows before event execution.

Therefore, the existing real-data event script must not be used blindly as the expanded broker-native H017 validation run.

## Existing Event Engine Finding

The event engine:

- `quantcore/backtest/h017_event.py`

currently validates H4 frame shape, H017 panel shape, decision index ordering, and execution/accounting assumptions.

The fill engine:

- `quantcore/backtest/fill_engine.py`

validates M1 columns, timezone-aware UTC DatetimeIndex, monotonic order, and no duplicate M1 timestamps.

The M1 scan-window selection currently requires a non-empty scan window. It does not require exactly 240 M1 bars.

This is acceptable for unit tests and general event mechanics, but it is not sufficient for the expanded broker-native validation protocol.

Therefore, the strict complete-window rule must be enforced in a dedicated preflight/filter layer before the validation event backtest is run.

## Required Next Implementation Plan

Before running H017, a future implementation phase must add a controlled preflight/filter path that:

1. Loads the accepted broker-native MT5 files with `load_mt5_csv(...)`.
2. Confirms loader metadata for all four files.
3. Constructs candidate H4 bridge windows from common USDJPY/XAUUSD H4 timestamps.
4. Requires the next H4 timestamp for each symbol to be exactly four hours later.
5. For each symbol and each candidate H4 timestamp, slices M1 bars in `[timestamp, timestamp + 4 hours)`.
6. Requires exactly 240 M1 bars for USDJPY.
7. Requires exactly 240 M1 bars for XAUUSD.
8. Intersects valid windows across both symbols.
9. Confirms the final common complete window count is exactly 5476.
10. Confirms the first valid common complete H4 timestamp is `2021-07-02 13:00:00+00:00`.
11. Confirms the last valid common complete H4 timestamp is `2026-04-30 01:00:00+00:00`.
12. Builds H4 panels using only the accepted common complete H4 timestamps.
13. Builds M1 panels containing only M1 rows needed for accepted complete windows.
14. Does not impute, forward-fill, backfill, synthesize, or silently deduplicate.
15. Does not write derived data files unless a later explicit phase authorizes it.
16. Does not use HistData.
17. Does not tune H017.
18. Does not change the cost model.
19. Runs H017 only after the preflight confirms the accepted window count and boundaries.
20. Prints enough diagnostics that the run can be audited and documented.

## Validation Output Requirements For Future Run

The future expanded broker-native H017 validation run must report at minimum:

- raw file paths used,
- loader row and bar counts,
- loader earliest/latest UTC timestamps,
- broker timezone,
- accepted first complete H4 bridge-window UTC,
- accepted last complete H4 bridge-window UTC,
- accepted complete bridge-window count,
- rejected/incomplete candidate-window counts by reason,
- H017 `n_bars`,
- fill count,
- starting equity,
- ending equity,
- total return percent,
- max drawdown percent,
- annualized Sharpe,
- PSR,
- MinTRL feasible flag,
- MinTRL required observations,
- MinTRL observed observations,
- DSR status,
- promotable flag,
- operational verdict,
- research validation verdict.

The future run result must be documented before any further interpretation.

## Explicit Non-Goals

This phase does not:

- run H017,
- tune H017,
- modify H017 parameters,
- modify the cost model,
- approve HistData,
- create derived datasets,
- commit raw data,
- start Phase 4,
- approve live trading.

## Current Decision

Expanded broker-native USDJPY and XAUUSD M1/H4 remains conditionally accepted for future H017 validation only under the strict complete-window rule.

H017 remains alive but not promotable.

Research validation remains pending.

Live trading remains unauthorized.

## Next Authorized Step

The next authorized step is an implementation phase for a strict expanded broker-native H017 validation preflight/filter.

That implementation phase should add tests first or alongside the preflight code.

It should not execute the validation run until the preflight code and tests are committed and pushed.
