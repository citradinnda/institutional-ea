# HANDOFF 30 - Self-Contained Continuation After Expanded Broker-Native H017 Validation Preflight Plan

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_30 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research: Python quantcore
- Execution: MetaTrader 5 later
- Production target: Oracle Cloud Always Free VPS later
- Monitoring: self-hosted free-tier stack later
- Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in `.venv`

Do not rush into strategy validation or live trading. The project is still in research-validation infrastructure work.

## Non-Negotiable Workflow Rules

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
- No WSL
- No Linux/macOS shell assumptions

Important PowerShell rule:

Do not use Linux/macOS heredoc syntax like:

    python - <<'PY'

PowerShell does not support that.

Use PowerShell here-strings instead:

    @'
    python code here
    '@ | python -

Tone and workflow:

1. Step-by-step.
2. Numbered steps.
3. Explicit Windows paths.
4. Plain English.
5. Define technical terms inline when needed.
6. Never write code without saying exactly where the file goes and how to run it.
7. One sub-phase per response.
8. Never skip git commits.
9. Never continue while local commits are unpushed.
10. Always read git status.
11. If tests pass but the count drops, treat it as a regression.
12. Do not propose switching to another AI chat unless the user asks.
13. For documentation-only phases, it is okay to provide one consolidated PowerShell block, as long as it includes status, tests, commit, push, final status, git ls-files, and recent log.
14. For code or diagnostics, be more cautious: inspect APIs first and split if needed.

Before writing code that calls internal functions, inspect actual APIs with:

    inspect.signature(...)
    dataclasses.fields(...)

Do not trust remembered function names or keyword names.

After each sub-phase:

1. Run focused tests if applicable.
2. Run full `pytest -q`.
3. Check git status.
4. Commit.
5. Push.
6. Check git status.
7. Run `git ls-files` on touched files or directories.
8. Read the output before continuing.

After each response, offer exactly:

    ✅ done
    ⚠️ error — paste it
    🤔 question

## Repository State

Repository root:

    C:\Users\equin\Documents\institutional-ea

Virtual environment:

    C:\Users\equin\Documents\institutional-ea\.venv

Branch:

    main

GitHub remote:

    https://github.com/citradinnda/institutional-ea.git

Latest committed project/handoff state before HANDOFF_30:

    671c347 Document expanded broker-native H017 validation preflight plan

Expected latest commit after this handoff is committed:

    Add handoff document #30 after expanded broker-native H017 preflight plan

Recent commits at time of handoff creation:

    671c347 Document expanded broker-native H017 validation preflight plan
    52ec123 Add handoff document #29 after expanded broker-native source acceptance
    5df6868 Add expanded broker-native source acceptance checkpoint
    4cecd97 Document expanded broker-native missingness time-bucket diagnostic
    0b0a923 Document expanded broker-native common-window diagnostic
    135e3e1 Document expanded broker-native session boundary diagnostic
    e559dcb Document expanded broker-native session diagnostic preflight
    4f50d92 Add expanded broker-native session common-window diagnostic plan
    8f0bded Add handoff document #28 after expanded broker-native M1 diagnostics
    4bc05f7 Add handoff document #28 after expanded broker-native M1 diagnostics

Known note:

There are duplicate consecutive handoff commit messages for HANDOFF_28. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    514 passed

Important test-count rule:

- Previous anchor after Phase 3.25 was 509 passed.
- Phase 3.26-b deliberately added 5 HistData duplicate-policy tests.
- Current correct anchor is 514 passed.
- If tests pass but the count drops below 514 without a deliberate test-removal phase, treat it as a regression.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification only.

Ask the user to run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -15
    pytest -q

Expected status after this handoff is committed and pushed:

- On branch main
- Your branch is up to date with origin/main.
- nothing to commit, working tree clean

Expected latest commit:

    Add handoff document #30 after expanded broker-native H017 preflight plan

Expected previous commit:

    671c347 Document expanded broker-native H017 validation preflight plan

Expected tests:

    514 passed

Read the output before continuing.

## Gitignore / Raw Data Rules

Important `.gitignore` rule:

The repo uses root-anchored:

    /data/

Do not change it to unanchored:

    data/

Reason:

An unanchored `data/` rule previously risked excluding:

    quantcore/data/

Raw data files under `/data/` are gitignored and must not be committed.

Do not commit raw M1/H4 data.

Do not commit large derived data files unless there is an explicit plan saying to do so.

Current rule:

- do not commit raw data,
- do not commit large derived data,
- do not write derived data before explicit authorization,
- do not modify raw vendor/broker files.

## Current Important Paths

Code:

    C:\Users\equin\Documents\institutional-ea\quantcore
    C:\Users\equin\Documents\institutional-ea\scripts
    C:\Users\equin\Documents\institutional-ea\tests

Important data modules:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\loaders.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\mt5_loader.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\dukascopy_loader.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\coverage.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\preflight.py

Important backtest/strategy modules:

    C:\Users\equin\Documents\institutional-ea\quantcore\strategy\h017.py
    C:\Users\equin\Documents\institutional-ea\quantcore\strategy\h017_claim.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_event.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\fill_engine.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\portfolio.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\cost_model.py

Important tests:

    C:\Users\equin\Documents\institutional-ea\tests\test_mt5_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_dukascopy_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_coverage.py
    C:\Users\equin\Documents\institutional-ea\tests\test_preflight.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017_claim.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017_event.py
    C:\Users\equin\Documents\institutional-ea\tests\test_fill_engine.py
    C:\Users\equin\Documents\institutional-ea\tests\test_portfolio.py
    C:\Users\equin\Documents\institutional-ea\tests\test_cost_model.py

Existing real-data scripts:

    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_real.py

## Most Recent Documents

Most recent completed document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H017_VALIDATION_RUN_PLAN_PREFLIGHT.md

Added in commit:

    671c347 Document expanded broker-native H017 validation preflight plan

Important recent expanded broker-native docs:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SOURCE_ACCEPTANCE_CHECKPOINT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_MISSINGNESS_BY_TIME_BUCKET_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_MISSINGNESS_BY_TIME_BUCKET_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_COMMON_WINDOW_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_COMMON_WINDOW_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_BOUNDARY_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_BOUNDARY_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_DIAGNOSTIC_PREFLIGHT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_DIAGNOSTIC_PREFLIGHT_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_RAW_INVENTORY.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_LOADER_TIMESTAMP_SHAPE_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_LOADER_TIMESTAMP_SHAPE_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_M1_COVERAGE_DENSITY_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_M1_COVERAGE_DENSITY_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H4_M1_AGGREGATION_COMPATIBILITY_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H4_M1_AGGREGATION_COMPATIBILITY_DIAGNOSTIC_OUTPUT.txt

Decision docs:

    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-001-m1-data-acquisition.md
    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-002-external-m1-data-source-evaluation.md
    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-003-histdata-duplicate-handling.md

## Strategy / Validation Background

The project uses strict hypothesis discipline because many prior strategies failed.

Immutable strategy graveyard summary:

- H001: Backtest without intrabar SL/TP simulation is fiction. Must use M1 inside H4 bars to resolve fills.
- H002-H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
- H004a: Single-seed models unreliable; use multi-seed ensembles.
- H005: Stacked multi-symbol models fail on heterogeneous instruments; use per-symbol models.
- H006-H007: Confidence filters are not risk management. ML chooses entries; deterministic rules manage risk.
- H008-H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals cannot be risk manager.
- H011-H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk ceiling remained.
- H014-H016: Two-asset USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1 percent per-trade risk was not 1 percent portfolio risk when trades overlapped. Drawdown breach was -19.43 percent.
- H015: Diversification into negative-edge instruments destroys the portfolio.
- H017: H016 plus portfolio heat governor. Alive but not promotable.

Do not broaden to more symbols yet.
Do not add machine learning yet.
Do not tune H017.

## Core Strategy Conventions

ATR:

- Wilder RMA, not SMA.
- First true range is high - low.
- Seed at index window - 1 with simple mean of first window true ranges.
- Recurrence:

    ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n

Chandelier Exit:

- Long:

    highest_high(lookback) - multiplier * ATR

- Short:

    lowest_low(lookback) + multiplier * ATR

Defaults:

    multiplier = 3.0
    lookback = 22

Vol Target:

- Realized vol at bar t uses returns through t-1 only:

    returns.shift(1).rolling(lookback)

- No lookahead.
- For H4 bars:

    periods_per_year = 1512

Signals:

- Donchian breakout.
- Long:

    close[t] > max(high[t-N ... t-1])

- Short:

    close[t] < min(low[t-N ... t-1])

- Channel uses prior N bars:

    shift(1).rolling(N)

H017:

- Inner-joins USDJPY and XAUUSD timestamps.
- Computes close-to-close returns.
- Uses same returns for vol targeting and heat governor.
- Position is signed risk exposure:

    signal * per_trade_risk * vol_mult * heat_mult

Heat governor:

- Combined heat:

    sqrt(w' (r^2 * C) w)

Defaults:

    cap = 0.015
    per_trade_risk = 0.01
    correlation_window = 120
    correlation_floor = 0.0

## Phase 3 Event-Driven Backtest Conventions

Phase 3.1 fill rule:

If stop and take-profit are both touched in the same M1 bar, stop wins.

Reason:

M1 OHLC does not reveal tick order inside the minute, so stop-first is conservative.

Phase 3.2 cost model defaults:

USDJPY:

    spread_price = 0.01
    commission_usd_per_lot_per_fill = 7.0
    stop_slippage_atr_fraction = 0.05

XAUUSD:

    spread_price = 0.30
    commission_usd_per_lot_per_fill = 10.0
    stop_slippage_atr_fraction = 0.05

Commission is per fill. A round trip charges entry and exit.

Portfolio P&L:

- XAUUSD P&L is already USD.
- USDJPY P&L is JPY and must be divided by USDJPY conversion price to become USD.

Event bridge timing:

1. H017 decides at H4 timestamp t.
2. Trade opens on next H4 bar open t+1.
3. M1 bars inside [t+1, t+2) resolve stops.
4. If no stop is hit, exposure closes at t+2 open as signal_flip.
5. This is a bridge-layer simplification.

## H017 Current Status

H017 remains:

- alive,
- not promotable,
- not ready for live trading,
- not validated on the expanded broker-native source yet.

Existing realistic event-driven result from the previous broker-native short M1 window:

    fills=470
    starting_equity_usd=10000.00
    ending_equity_usd=16145.60
    total_return_pct=61.46
    max_drawdown_pct=-33.65
    annualized_sharpe=1.3218

Claim result:

    PSR: 0.8662, failed threshold 0.95
    MinTRL feasible: True
    MinTRL required n: 1034
    MinTRL observed n: 470
    DSR: Skipped
    H017 promotable: False

Operational verdict from the old short-window run:

    PIPELINE SMOKE PASSED: True
    RESEARCH VALIDATION SUFFICIENT: False

Interpretation:

1. The event pipeline worked.
2. The old short broker-native M1 history was too short.
3. Do not trust the short-window +61.46 percent return as validated edge.
4. The -33.65 percent drawdown is a serious risk signal.
5. H017 is alive but not promotable.

## MT5 / Broker Data State

Broker:

    Exness

Account environment reported by user:

    Demo

Server reported by user:

    MT5

Broker timezone used by loader:

    Europe/Athens

Meaning:

- Winter UTC+2
- Summer UTC+3
- DST-aware

MT5 loader:

    load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

MT5LoadResult fields verified:

    bars
    n_bars
    n_input_rows
    earliest_utc
    latest_utc
    broker_tz

Loaded `bars` shape verified:

- pandas DataFrame
- DatetimeIndex
- index name: `dt`
- timezone: UTC
- columns: `open`, `high`, `low`, `close`, `volume`

Expanded broker-native raw exports are local and gitignored:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Reported exact MT5 symbols:

    USDJPYm
    XAUUSDm

Do not commit these raw files.

## Expanded Broker-Native Source Diagnostics Summary

### Loader timestamp-shape diagnostic

USDJPY M1:

    n_input_rows: 1785312
    n_bars: 1785312
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps_after_load: 0

USDJPY H4:

    n_input_rows: 8713
    n_bars: 8713
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-30 05:00:00+00:00
    duplicate_timestamps_after_load: 0

XAUUSD M1:

    n_input_rows: 1704907
    n_bars: 1704907
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps_after_load: 0

XAUUSD H4:

    n_input_rows: 8658
    n_bars: 8658
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 05:00:00+00:00
    duplicate_timestamps_after_load: 0

### Coverage-density diagnostic

The expanded files have a sparse daily-like prefix from 2018 through 2021-06.

The dense M1 candidate region starts at 2021-07 for both symbols.

Do not treat 2018 through 2021-06 as dense M1 history.

### H4/M1 aggregation compatibility diagnostic

On every fully covered comparable H4 window, broker-native M1 aggregation exactly reproduced broker-native H4 OHLCV.

USDJPY:

    compared_full_m1_windows: 5701
    matched_bars: 5701
    mismatched_bars: 0
    first_full_m1_window_utc: 2021-07-02 13:00:00+00:00
    last_full_m1_window_utc: 2026-04-30 01:00:00+00:00

XAUUSD:

    compared_full_m1_windows: 6149
    matched_bars: 6149
    mismatched_bars: 0
    first_full_m1_window_utc: 2021-07-02 13:00:00+00:00
    last_full_m1_window_utc: 2026-04-30 01:00:00+00:00

### Cross-symbol common-window diagnostic

Common M1 span:

    2021-07-01 21:00:00+00:00 through 2026-04-30 07:00:00+00:00

Common complete H4/M1 windows:

    common_complete_h4_m1_windows: 5476
    USDJPY_only_complete_h4_m1_windows: 225
    XAUUSD_only_complete_h4_m1_windows: 673
    first_common_complete_h4_window_utc: 2021-07-02 13:00:00+00:00
    last_common_complete_h4_window_utc: 2026-04-30 01:00:00+00:00

### Missingness-by-time-bucket diagnostic

Interpretation:

- XAUUSD missingness is dominated by expected-looking daily breaks and closures.
- USDJPY has many tiny missing clusters.
- This is acceptable only under a strict complete-H4/M1-window rule.
- Do not assume continuous M1 availability.
- Do not impute.

## Current Source Acceptance Status

Expanded broker-native USDJPY and XAUUSD M1/H4 data is conditionally accepted for a future H017 validation phase.

This conditional acceptance has strict restrictions.

Accepted source:

    Exness demo MT5 broker-native exports

Accepted symbols:

    USDJPY
    XAUUSD

Accepted timeframes:

    Broker-native H4
    Broker-native M1

Accepted future validation bridge-window range:

    first possible common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
    last possible common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00

Accepted future bridge-window count:

    5476 common complete H4/M1 windows

Required future H017 bridge-window rule:

A common complete H4/M1 bridge window means:

1. USDJPY has a broker-native H4 bar at the H4 timestamp.
2. XAUUSD has a broker-native H4 bar at the same H4 timestamp.
3. For each symbol, the next H4 timestamp is exactly four hours later.
4. For each symbol, the M1 window `[H4 timestamp, H4 timestamp + 4 hours)` contains exactly 240 M1 bars.
5. No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

This checkpoint does not itself run H017.

This checkpoint does not imply that H017 will pass validation.

This checkpoint does not approve live trading.

## HistData State

HistData remains rejected for H017 validation under current evidence.

HistData raw files may remain available for diagnostic reference only.

Current statuses:

1. HistData as H017 validation source: rejected under current evidence.
2. HistData as accepted research source: not accepted.
3. HistData-built H4: not accepted.
4. Broker H4 plus HistData M1 hybrid: not accepted.
5. Derived HistData files: not authorized.
6. H017 validation on HistData: not authorized.
7. Broker-native expanded source is conditionally accepted for future H017 validation.
8. H017 status: alive but not promotable.

Allowed HistData uses:

- explicitly planned diagnostics only,
- documentation,
- source-quality comparison,
- raw inventory metadata preservation.

Not allowed:

- H017 validation,
- strategy tuning,
- derived production datasets,
- derived H4 files for H017 validation,
- broker-H4 plus HistData-M1 hybrid validation,
- silent deduplication,
- raw file modification,
- raw file commits.

## Phase 3.26-al Completed Immediately Before This Handoff

Completed phase:

    Phase 3.26-al - Expanded broker-native H017 validation run plan and preflight

Commit:

    671c347 Document expanded broker-native H017 validation preflight plan

Document created:

    docs/operations/BROKER_NATIVE_EXPANDED_H017_VALIDATION_RUN_PLAN_PREFLIGHT.md

Full tests passed:

    514 passed

Purpose of the completed phase:

1. Inspect actual existing H017/event-bridge/backtest APIs.
2. Confirm whether existing event code enforces strict complete H4/M1 windows.
3. Document a run plan before executing H017.
4. Do not run H017.
5. Do not tune H017.
6. Do not change the cost model.
7. Do not write derived datasets.

## API Inspection Findings From Phase 3.26-al

Strategy layer inspected:

- `quantcore.strategy.h017.H017Config`
- `quantcore.strategy.h017.H017Result`
- `quantcore.strategy.h017.run_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None)`
- `quantcore.strategy.h017_claim.H017BacktestResult`
- `quantcore.strategy.h017_claim.H017Claim`
- `quantcore.strategy.h017_claim.backtest_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None)`
- `quantcore.strategy.h017_claim.build_h017_claim(...)`

Event-driven backtest layer inspected:

- `quantcore.backtest.h017_event.H017EventBacktestResult`
- `quantcore.backtest.h017_event.backtest_h017_event_driven(...)`
- `quantcore.backtest.h017_event.backtest_h017_event_from_result(...)`

Execution/accounting layer inspected:

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

Data/preflight layer inspected:

- `quantcore.data.mt5_loader.MT5LoadResult`
- `quantcore.data.mt5_loader.load_mt5_csv(path, broker_tz="Europe/Athens")`
- `quantcore.data.preflight.require_existing_files(...)`
- `quantcore.data.coverage.CoverageAssessment`
- `quantcore.data.coverage.assess_m1_research_coverage(...)`
- `quantcore.data.leakage.LeakageScan`
- `quantcore.data.leakage.detect_d1_leakage(...)`
- `quantcore.data.leakage.trim_to_common_start(...)`

Important API corrections found:

The portfolio module does not expose:

- `lots_for_risk`
- `instrument_spec`
- `position_size_lots`

Actual names:

- `get_default_instrument_spec`
- `size_position_from_risk`
- `PositionSize`

The cost model module does not expose:

- `ExecutionCostSpec`
- `ExecutionCostResult`
- `default_execution_costs`

Actual names:

- `SymbolCostSpec`
- `ExecutionCost`
- `get_default_cost_spec`

## Existing Event Script Finding

Existing script:

    scripts/run_h017_event_real.py

This script loads the four MT5 exports, applies existing H4 leakage trimming, trims to a broad common H4/M1 window, runs `backtest_h017_event_driven(...)`, then builds an H017 claim.

It is useful as an older operational smoke path.

However, it is not sufficient for the expanded broker-native validation run because the inspected logic does not enforce:

- the accepted common complete bridge-window range,
- exactly 5476 common complete windows,
- exactly 240 M1 bars for USDJPY inside every included H4 interval,
- exactly 240 M1 bars for XAUUSD inside every included H4 interval,
- exclusion of incomplete bridge windows before event execution.

Therefore, do not run `scripts/run_h017_event_real.py` blindly as the expanded broker-native validation run.

## Existing Event Engine Finding

Existing event engine:

    quantcore/backtest/h017_event.py

It validates H4 frame shape, H017 panel shape, decision index ordering, and execution/accounting assumptions.

Existing fill engine:

    quantcore/backtest/fill_engine.py

It validates M1 columns, timezone-aware UTC DatetimeIndex, monotonic order, and no duplicate M1 timestamps.

The M1 scan-window selection currently requires only a non-empty scan window:

    _select_scan_window(...)

It does not require exactly 240 M1 bars.

This is acceptable for unit tests and general event mechanics, but not sufficient for the expanded broker-native validation protocol.

Therefore, strict complete-window enforcement must happen in a dedicated preflight/filter layer before the validation event backtest is run.

## State At The Moment The User Asked For This Handoff

After committing Phase 3.26-al, the user asked for a self-contained handoff because token context was nearing its end.

Immediately before creating this handoff, a read-only inspection was performed for the likely next implementation area.

Read-only files inspected:

    tests/test_preflight.py
    tests/test_coverage.py
    tests/test_mt5_loader.py
    quantcore/data/preflight.py
    quantcore/data/coverage.py
    quantcore/data/__init__.py

Findings:

1. `tests/test_preflight.py` currently covers required-file checks only.
2. `tests/test_coverage.py` covers high-level research coverage sufficiency only.
3. `tests/test_mt5_loader.py` uses synthetic temporary MT5 CSV fixtures and explicitly notes tests cannot depend on real `/data/raw/` files.
4. `quantcore/data/preflight.py` currently contains:
   - `RequiredFileStatus`
   - `RequiredFilesReport`
   - `assess_required_files`
   - `require_existing_files`
5. `quantcore/data/coverage.py` currently contains:
   - `CoverageAssessment`
   - `assess_m1_research_coverage`
6. `quantcore/data/__init__.py` currently exports checksums and leakage objects only.
7. Git was clean and up to date after this read-only inspection.

## Practical Next Path

The next logical work is:

    Phase 3.26-am - strict expanded broker-native complete-window preflight/filter implementation

But the next AI must not write code immediately. It must first do hygiene verification.

Recommended implementation direction after hygiene:

1. Decide where the strict complete-window preflight belongs.
2. Likely location:
   - new module: `quantcore/data/bridge_windows.py`
   - new tests: `tests/test_bridge_windows.py`
3. Use synthetic pandas DataFrames only in tests.
4. Do not depend on real raw `/data/` files in tests.
5. Implement dataclasses for complete-window diagnostics.
6. Implement a pure function that accepts already-loaded H4/M1 DataFrames and returns accepted common complete H4 timestamps plus counts/reasons.
7. Do not load files inside this pure function.
8. Do not write derived data.
9. Do not run H017 in this phase.
10. Do not change H017 parameters.
11. Do not change the cost model.

A reasonable future API shape, subject to inspection/design before coding, could be:

    assess_common_complete_h4_m1_windows(
        usdjpy_h4: pd.DataFrame,
        xauusd_h4: pd.DataFrame,
        usdjpy_m1: pd.DataFrame,
        xauusd_m1: pd.DataFrame,
        expected_m1_bars_per_h4: int = 240,
        expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
    ) -> CommonCompleteBridgeWindowAssessment

But this is only a suggestion. The next AI should design carefully and keep names clear.

Potential dataclass fields:

- `accepted_timestamps`
- `accepted_count`
- `first_accepted_timestamp`
- `last_accepted_timestamp`
- `candidate_common_h4_count`
- `usdjpy_complete_count`
- `xauusd_complete_count`
- `common_complete_count`
- `usdjpy_only_complete_count`
- `xauusd_only_complete_count`
- `rejected_count`
- reasons/counts for missing H4, non-4-hour next H4 delta, M1 count not equal to 240

Need not implement all fields at once, but future validation run must be auditable enough to prove the 5476 accepted-window count and boundaries.

## Required Future Complete-Window Preflight Behavior

The future strict preflight/filter must:

1. Accept already-loaded broker-native H4 and M1 DataFrames.
2. Require timezone-aware UTC DatetimeIndexes.
3. Require sorted ascending indexes.
4. Require no duplicate H4 or M1 timestamps.
5. Require canonical OHLC columns.
6. Construct candidate common H4 timestamps from the intersection of USDJPY and XAUUSD H4 indexes.
7. For each symbol, require the next H4 timestamp to be exactly four hours later.
8. For each symbol, count M1 bars in `[timestamp, timestamp + 4 hours)`.
9. Require exactly 240 M1 bars for USDJPY.
10. Require exactly 240 M1 bars for XAUUSD.
11. Intersect valid timestamps across both symbols.
12. Return the accepted common complete timestamps without writing files.
13. Do not impute.
14. Do not forward-fill.
15. Do not backfill.
16. Do not synthesize bars.
17. Do not silently deduplicate.
18. Do not use HistData.

Future real-data validation must assert:

    accepted_count == 5476
    first_accepted_timestamp == 2021-07-02 13:00:00+00:00
    last_accepted_timestamp == 2026-04-30 01:00:00+00:00

Do not run H017 until that preflight/filter exists, is tested, committed, and pushed.

## Absolute Do-Not Rules At HANDOFF_30

Do not:

1. Do not run H017 without committed strict complete-window preflight/filter code and tests.
2. Do not run `scripts/run_h017_event_real.py` as the expanded validation run.
3. Do not tune H017.
4. Do not change H017 parameters.
5. Do not change the cost model.
6. Do not use HistData for H017 validation.
7. Do not accept HistData as a research source.
8. Do not build HistData H4 for H017 validation.
9. Do not combine broker H4 with HistData M1.
10. Do not use the sparse 2018 through 2021-06 broker-native prefix.
11. Do not include incomplete H4/M1 windows in validation.
12. Do not use any H4/M1 window where either symbol has fewer or more than exactly 240 M1 bars.
13. Do not impute missing M1 bars.
14. Do not forward-fill or backfill M1 bars.
15. Do not synthesize bars.
16. Do not modify raw broker files.
17. Do not commit raw MT5 CSV files.
18. Do not commit raw HistData CSV files.
19. Do not change `.gitignore` from `/data/` to `data/`.
20. Do not broaden to more symbols.
21. Do not add machine learning.
22. Do not start Phase 4 execution code.
23. Do not start live trading.
24. Do not ignore the previous -33.65 percent drawdown.
25. Do not continue development while local commits are unpushed.
26. Do not let git status go unread.
27. Do not use Linux/macOS shell syntax in PowerShell.
28. Do not silently deduplicate vendor data.
29. Do not write derived data files without an explicit phase authorizing it.
30. Do not treat source acceptance as H017 promotion.
31. Do not treat future validation as live-trading approval.
32. Do not skip full pytest.
33. Do not allow test count to drop below 514 without an explicit test-removal phase.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

1. `.gitignore` once had unrooted `data/`, which risked excluding `quantcore/data/`.
2. Some older commits missed files because `git add` was incomplete.
3. An empty `HANDOFF_16.md` was accidentally committed once; verify handoff file size and preview before committing.
4. Markdown code fences have been damaged by paste before; avoid nested markdown fences in command blocks.
5. PowerShell does not support Linux heredocs.
6. VS Code can keep unsaved buffers that overwrite edits.
7. If terminal output shows command echo ambiguity, verify with `Select-String` or file previews before proceeding.
8. Always run tests.
9. Always inspect git status.
10. Always push commits.
11. Always verify `git ls-files` after commits.
12. Treat test-count drops as regressions.
13. If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.
14. If `git commit` says nothing to commit, immediately run recovery status/log/ls-files checks before continuing.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after Phase 3.26-al and HANDOFF_30.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is 514 passed.
3. Latest expected handoff commit is `Add handoff document #30 after expanded broker-native H017 preflight plan`.
4. Latest expected pre-handoff commit is `671c347 Document expanded broker-native H017 validation preflight plan`.
5. Expanded broker-native USDJPY + XAUUSD M1/H4 is conditionally accepted for future H017 validation only under strict complete-window rules.
6. The accepted future bridge-window range is `2021-07-02 13:00:00+00:00` through `2026-04-30 01:00:00+00:00`.
7. There are expected to be exactly `5476` common complete H4/M1 windows.
8. Each future validation window must have exactly 240 M1 bars per symbol inside `[H4 timestamp, H4 timestamp + 4 hours)`.
9. No imputation, forward-fill, backfill, synthetic bars, or HistData are allowed.
10. H017 is still alive but not promotable.
11. No H017 run should happen before strict complete-window preflight/filter code and tests are committed and pushed.
12. The existing `scripts/run_h017_event_real.py` is not sufficient for expanded validation because it does not enforce the 5476 strict complete-window rule.
13. The existing fill engine only requires a non-empty M1 scan window, not exactly 240 bars.
14. Do not tune H017.
15. Do not change the cost model.
16. Do not start live trading or Phase 4 execution.
17. The next logical sub-phase is Phase 3.26-am: strict expanded broker-native complete-window preflight/filter implementation.
18. First task is hygiene verification only. No new code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -15
    pytest -q

Then paste the full output.

✅ done
⚠️ error — paste it
🤔 question
