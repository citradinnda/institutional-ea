# HANDOFF 31 - Self-Contained Continuation After Strict H017 Event Wrapper Implementation

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_31 wins.

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

Latest expected committed project state before this handoff is committed:

    06de306 Add strict H017 event wrapper

Expected latest commit after this handoff is committed:

    Add handoff document #31 after strict H017 event wrapper

Recent commits at time of handoff creation:

    06de306 Add strict H017 event wrapper
    0c56c8d Document strict bridge-window contiguity diagnostic
    72ae6c1 Document strict bridge-window real-data preflight result
    56dcc56 Add strict common bridge-window preflight
    cdca565 Add handoff document #30 after expanded broker-native H017 preflight plan
    671c347 Document expanded broker-native H017 validation preflight plan
    52ec123 Add handoff document #29 after expanded broker-native source acceptance
    5df6868 Add expanded broker-native source acceptance checkpoint
    4cecd97 Document expanded broker-native missingness time-bucket diagnostic
    0b0a923 Document expanded broker-native common-window diagnostic

Known note:

There are duplicate consecutive handoff commit messages for HANDOFF_28. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    532 passed

Important test-count rule:

- Previous anchor after HANDOFF_30 start was 514 passed.
- Phase 3.26-am added 9 bridge-window tests, increasing to 523 passed.
- Phase 3.26-ap added 9 strict H017 event wrapper tests, increasing to 532 passed.
- Current correct anchor is 532 passed.
- If tests pass but the count drops below 532 without a deliberate test-removal phase, treat it as a regression.

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

    Add handoff document #31 after strict H017 event wrapper

Expected previous commit:

    06de306 Add strict H017 event wrapper

Expected tests:

    532 passed

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
    C:\Users\equin\Documents\institutional-ea\quantcore\data\bridge_windows.py

Important backtest/strategy modules:

    C:\Users\equin\Documents\institutional-ea\quantcore\strategy\h017.py
    C:\Users\equin\Documents\institutional-ea\quantcore\strategy\h017_claim.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_event.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_strict_event.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\fill_engine.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\portfolio.py
    C:\Users\equin\Documents\institutional-ea\quantcore\backtest\cost_model.py

Important tests:

    C:\Users\equin\Documents\institutional-ea\tests\test_mt5_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_dukascopy_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_coverage.py
    C:\Users\equin\Documents\institutional-ea\tests\test_preflight.py
    C:\Users\equin\Documents\institutional-ea\tests\test_bridge_windows.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017_claim.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017_event.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017_strict_event.py
    C:\Users\equin\Documents\institutional-ea\tests\test_fill_engine.py
    C:\Users\equin\Documents\institutional-ea\tests\test_portfolio.py
    C:\Users\equin\Documents\institutional-ea\tests\test_cost_model.py

Existing real-data scripts:

    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_real.py

## Most Recent Documents

Most recent completed documents:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H017_VALIDATION_RUN_PLAN_PREFLIGHT.md

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

## Work Completed Since HANDOFF_30

### Phase 3.26-am - Strict expanded broker-native complete-window preflight/filter implementation

Commit:

    56dcc56 Add strict common bridge-window preflight

Files added:

    quantcore/data/bridge_windows.py
    tests/test_bridge_windows.py

Full tests after this phase:

    523 passed

Purpose:

1. Add a pure strict complete-window preflight/filter.
2. Accept already-loaded H4/M1 DataFrames.
3. Require timezone-aware UTC DatetimeIndexes.
4. Require sorted ascending indexes.
5. Require no duplicate H4 or M1 timestamps.
6. Require canonical OHLC columns.
7. Construct candidate common H4 timestamps from the intersection of USDJPY and XAUUSD H4 indexes.
8. For each symbol, require next H4 timestamp exactly four hours later.
9. For each symbol, require exactly 240 M1 bars in `[timestamp, timestamp + 4 hours)`.
10. Return accepted common complete timestamps and diagnostics.
11. Write no files.
12. Run no H017 validation.
13. Use synthetic tests only.

Key API added:

    assess_common_complete_h4_m1_windows(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        expected_m1_bars_per_h4=240,
        expected_h4_delta=pd.Timedelta(hours=4),
    ) -> CommonCompleteBridgeWindowAssessment

Dataclasses added:

    BridgeWindowRejectionCount
    CommonCompleteBridgeWindowAssessment

### Real-data strict bridge-window preflight diagnostic

Read-only diagnostic was run on the four real local MT5 exports.

Result:

    STRICT BRIDGE-WINDOW PREFLIGHT: PASSED

Confirmed values:

    candidate_common_h4_count: 8654
    usdjpy_complete_count: 5685
    xauusd_complete_count: 6149
    common_complete_count: 5476
    accepted_count: 5476
    first_accepted_timestamp: 2021-07-02 13:00:00+00:00
    last_accepted_timestamp: 2026-04-30 01:00:00+00:00
    usdjpy_only_complete_count: 209
    xauusd_only_complete_count: 673
    rejected_count: 3178

Rejection counts:

    usdjpy_m1_count_not_expected: 2969
    usdjpy_missing_next_h4_timestamp: 1
    usdjpy_non_4h_next_h4_delta: 1179
    xauusd_m1_count_not_expected: 2505
    xauusd_missing_next_h4_timestamp: 1
    xauusd_non_4h_next_h4_delta: 1193

No H017 run was performed.

No files were written during the diagnostic.

### Phase 3.26-an - Document strict bridge-window real-data preflight result

Commit:

    72ae6c1 Document strict bridge-window real-data preflight result

Files added:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT.md
    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT_OUTPUT.txt

Full tests:

    523 passed

### Phase 3.26-ao - Strict bridge-window contiguity diagnostic and documentation

Commit:

    0c56c8d Document strict bridge-window contiguity diagnostic

Files added:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC.md
    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC_OUTPUT.txt

Full tests:

    523 passed

Critical diagnostic result:

    accepted_count: 5476
    adjacent_deltas_checked: 5475
    four_hour_adjacent_deltas: 4148
    non_four_hour_adjacent_deltas: 1327

Event-engine implication:

    safe_intervals_if_h4_filtered_to_accepted_only: 4148
    unsafe_gap_intervals_if_h4_filtered_to_accepted_only: 1327

Critical design conclusion:

Do not implement the strict runner by simply filtering H4 to accepted_timestamps.

Reason:

The existing event engine uses adjacent H4/H017 rows as:

    decision_time = index[i - 1]
    entry_time = index[i]
    forced_exit_time = index[i + 1]

If H4 is filtered to accepted timestamps only, the next retained timestamp may be 8 hours, 12 hours, weekend gap, or more later. That would create invalid forced exits.

Required future runner design:

1. Preserve native H4 interval semantics.
2. Execute only intervals whose entry_time is in the strict accepted bridge-window set.
3. Also require forced_exit_time == entry_time + 4 hours.
4. Skip or force flat invalid intervals.
5. Do not impute.
6. Do not synthesize bars.

### Phase 3.26-ap - Strict H017 event wrapper implementation with synthetic tests only

Commit:

    06de306 Add strict H017 event wrapper

Files added/modified:

    quantcore/backtest/h017_strict_event.py
    tests/test_h017_strict_event.py
    quantcore/backtest/__init__.py

Focused tests:

    tests/test_h017_strict_event.py: 9 passed

Related tests:

    tests/test_h017_event.py and tests/test_bridge_windows.py: 19 passed

Full tests:

    532 passed

Purpose:

1. Add a strict wrapper around the existing H017 event engine.
2. Do not modify the existing event engine.
3. Preserve the native H4/H017 index.
4. Run or accept an H017 result.
5. Zero out H017 positions for intervals whose entry_time is not in the strict accepted entry set.
6. Also skip intervals where forced_exit_time is not exactly entry_time + 4 hours.
7. Then call `backtest_h017_event_from_result(...)`.
8. Use synthetic tests only.
9. Do not load real raw data.
10. Do not run expanded real-data H017 validation.

New wrapper module:

    quantcore/backtest/h017_strict_event.py

New dataclass:

    StrictH017EventBacktestResult

Fields:

    backtest
    accepted_entry_times
    executed_entry_times
    skipped_entry_times
    accepted_entry_count
    executed_entry_count
    skipped_entry_count
    expected_h4_delta

New functions:

    backtest_h017_strict_event_driven(...)
    backtest_h017_strict_event_from_result(...)

Important behavior:

`backtest_h017_strict_event_from_result(...)` accepts an existing H017Result and strict accepted entry times.

It preserves the full native decision index.

For each event-engine interval:

    decision_time = decision_index[i - 1]
    entry_time = decision_index[i]
    forced_exit_time = decision_index[i + 1]

It executes only when:

    entry_time in accepted_entry_times
    and forced_exit_time - entry_time == expected_h4_delta

Otherwise it forces that interval flat by zeroing the decision exposure for the corresponding decision_time.

This is designed to avoid the invalid H4-filtering problem discovered in Phase 3.26-ao.

Package exports updated:

    quantcore/backtest/__init__.py

New exported names:

    StrictH017EventBacktestResult
    backtest_h017_strict_event_driven
    backtest_h017_strict_event_from_result

## Current API Snapshot

Verified by inspection:

Strategy:

    quantcore.strategy.h017.H017Config
    quantcore.strategy.h017.H017Result
    quantcore.strategy.h017.run_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None)

H017 claim:

    quantcore.strategy.h017_claim.H017BacktestResult
    quantcore.strategy.h017_claim.H017Claim
    quantcore.strategy.h017_claim.build_h017_claim(
        returns,
        periods_per_year=1512,
        sr_benchmark=0.0,
        confidence=0.95,
        psr_threshold=0.95,
        sr_estimates=None,
        dsr_threshold=0.95,
    )

Event engine:

    quantcore.backtest.h017_event.H017EventBacktestResult
    quantcore.backtest.h017_event.backtest_h017_event_driven(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        config=None,
        starting_equity_usd=10000.0,
        slippage_atr_by_symbol=None,
    )

    quantcore.backtest.h017_event.backtest_h017_event_from_result(
        *,
        h017_result,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        starting_equity_usd=10000.0,
        slippage_atr_by_symbol=None,
    )

Strict event wrapper:

    quantcore.backtest.h017_strict_event.StrictH017EventBacktestResult

    quantcore.backtest.h017_strict_event.backtest_h017_strict_event_driven(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        accepted_entry_times,
        config=None,
        starting_equity_usd=10000.0,
        slippage_atr_by_symbol=None,
        expected_h4_delta=pd.Timedelta(hours=4),
    )

    quantcore.backtest.h017_strict_event.backtest_h017_strict_event_from_result(
        *,
        h017_result,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        accepted_entry_times,
        starting_equity_usd=10000.0,
        slippage_atr_by_symbol=None,
        expected_h4_delta=pd.Timedelta(hours=4),
    )

Bridge-window preflight:

    quantcore.data.bridge_windows.CommonCompleteBridgeWindowAssessment

    quantcore.data.bridge_windows.assess_common_complete_h4_m1_windows(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        expected_m1_bars_per_h4=240,
        expected_h4_delta=pd.Timedelta(hours=4),
    )

MT5 loader:

    quantcore.data.mt5_loader.load_mt5_csv(path, broker_tz="Europe/Athens")

Preflight:

    quantcore.data.preflight.require_existing_files(paths, label="Required file")

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

Do not run `scripts/run_h017_event_real.py` blindly as the expanded broker-native validation run.

## Existing Event Engine Finding

Existing event engine:

        quantcore/backtest/h017_event.py
        
        core/backtest/h017_event.py

It validates H4 frame shape, H017 panel shape, decision index ordering, and execution/accounting assumptions.

Existing fill engine:

    quantcore/backtest/fill_engine.py

It validates M1 columns, timezone-aware UTC DatetimeIndex, monotonic order, and no duplicate M1 timestamps.

The M1 scan-window selection currently requires only a non-empty scan window.

It does not require exactly 240 M1 bars.

This is acceptable for unit tests and general event mechanics, but not sufficient for the expanded broker-native validation protocol by itself.

The strict validation protocol is now enforced through:

    quantcore/data/bridge_windows.py
    quantcore/backtest/h017_strict_event.py

## Strict Bridge-Window Preflight Implementation

Implemented in:

    quantcore/data/bridge_windows.py

Tests:

    tests/test_bridge_windows.py

Commit:

    56dcc56 Add strict common bridge-window preflight

Full tests after implementation:

    523 passed

Main API:

    assess_common_complete_h4_m1_windows(
        *,
        usdjpy_h4: pd.DataFrame,
        xauusd_h4: pd.DataFrame,
        usdjpy_m1: pd.DataFrame,
        xauusd_m1: pd.DataFrame,
        expected_m1_bars_per_h4: int = 240,
        expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
    ) -> CommonCompleteBridgeWindowAssessment

Dataclasses:

    BridgeWindowRejectionCount
    CommonCompleteBridgeWindowAssessment

CommonCompleteBridgeWindowAssessment fields:

    accepted_timestamps
    accepted_count
    first_accepted_timestamp
    last_accepted_timestamp
    candidate_common_h4_count
    usdjpy_complete_count
    xauusd_complete_count
    common_complete_count
    usdjpy_only_complete_count
    xauusd_only_complete_count
    rejected_count
    rejection_counts

Behavior:

1. Accepts already-loaded H4 and M1 DataFrames.
2. Requires pandas DataFrames.
3. Requires timezone-aware UTC DatetimeIndexes.
4. Requires sorted ascending indexes.
5. Requires no duplicate timestamps.
6. Requires canonical OHLC columns: `open`, `high`, `low`, `close`.
7. Constructs candidate common H4 timestamps from the intersection of USDJPY and XAUUSD H4 indexes.
8. For each symbol, requires the next H4 timestamp to be exactly four hours later.
9. For each symbol, counts M1 bars in `[timestamp, timestamp + 4 hours)`.
10. Requires exactly 240 M1 bars for USDJPY.
11. Requires exactly 240 M1 bars for XAUUSD.
12. Intersects valid timestamps across both symbols.
13. Returns accepted common complete timestamps.
14. Writes no files.
15. Does not impute.
16. Does not forward-fill.
17. Does not backfill.
18. Does not synthesize bars.
19. Does not silently deduplicate.
20. Does not use HistData.
21. Does not run H017.

## Strict Bridge-Window Real-Data Preflight Result

Documented in:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT.md
    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT_OUTPUT.txt

Commit:

    72ae6c1 Document strict bridge-window real-data preflight result

Full tests:

    523 passed

Read-only diagnostic loaded the four real local MT5 exports:

    data/raw/USDJPY/H4.csv
    data/raw/USDJPY/M1.csv
    data/raw/XAUUSD/H4.csv
    data/raw/XAUUSD/M1.csv

No files were written.

No H017 run was performed.

Result:

    STRICT BRIDGE-WINDOW PREFLIGHT: PASSED

Confirmed loaded MT5 export counts:

USDJPY H4:

    n_input_rows: 8713
    n_bars: 8713
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-30 05:00:00+00:00
    broker_tz: Europe/Athens

USDJPY M1:

    n_input_rows: 1785312
    n_bars: 1785312
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    broker_tz: Europe/Athens

XAUUSD H4:

    n_input_rows: 8658
    n_bars: 8658
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 05:00:00+00:00
    broker_tz: Europe/Athens

XAUUSD M1:

    n_input_rows: 1704907
    n_bars: 1704907
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    broker_tz: Europe/Athens

Strict assessment counts:

    candidate_common_h4_count: 8654
    usdjpy_complete_count: 5685
    xauusd_complete_count: 6149
    common_complete_count: 5476
    accepted_count: 5476
    first_accepted_timestamp: 2021-07-02 13:00:00+00:00
    last_accepted_timestamp: 2026-04-30 01:00:00+00:00
    usdjpy_only_complete_count: 209
    xauusd_only_complete_count: 673
    rejected_count: 3178

Rejection counts:

    usdjpy_m1_count_not_expected: 2969
    usdjpy_missing_next_h4_timestamp: 1
    usdjpy_non_4h_next_h4_delta: 1179
    xauusd_m1_count_not_expected: 2505
    xauusd_missing_next_h4_timestamp: 1
    xauusd_non_4h_next_h4_delta: 1193

This confirmed the future expanded broker-native H017 validation must use exactly:

    accepted_count == 5476
    first_accepted_timestamp == 2021-07-02 13:00:00+00:00
    last_accepted_timestamp == 2026-04-30 01:00:00+00:00

## Strict Bridge-Window Contiguity Diagnostic

Documented in:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC.md
    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC_OUTPUT.txt

Commit:

    0c56c8d Document strict bridge-window contiguity diagnostic

Full tests:

    523 passed

Purpose:

The strict bridge-window preflight accepts timestamps whose following four-hour M1 window is complete. But the existing event engine uses adjacent H4/H017 rows as execution timing anchors.

The diagnostic checked whether accepted strict bridge-window timestamps can be used by simply filtering H4 to `accepted_timestamps`.

They cannot.

Accepted strict bridge-window summary:

    accepted_count: 5476
    first_accepted_timestamp: 2021-07-02 13:00:00+00:00
    last_accepted_timestamp: 2026-04-30 01:00:00+00:00

Accepted timestamp contiguity:

    adjacent_deltas_checked: 5475
    four_hour_adjacent_deltas: 4148
    non_four_hour_adjacent_deltas: 1327

Event-engine implication:

    strict_entry_times_from_preflight: 5476
    safe_intervals_if_h4_filtered_to_accepted_only: 4148
    unsafe_gap_intervals_if_h4_filtered_to_accepted_only: 1327

Critical conclusion:

Do not implement strict expanded validation by simply filtering H4 to `accepted_timestamps`.

Reason:

The existing event engine uses:

    decision_time = index[i - 1]
    entry_time = index[i]
    forced_exit_time = index[i + 1]

If H4 is filtered only to accepted timestamps, `index[i + 1]` may be 8 hours, 12 hours, a weekend gap, or more later. That would create incorrect forced exits.

Required future runner behavior:

1. Preserve native H4 interval semantics.
2. Execute only intervals where `entry_time` is in the accepted strict bridge-window set.
3. Also require `forced_exit_time == entry_time + 4 hours`.
4. Skip or force flat invalid intervals.
5. Do not impute.
6. Do not synthesize bars.

## Strict H017 Event Wrapper Implementation

Implemented in:

    quantcore/backtest/h017_strict_event.py

Tests:

    tests/test_h017_strict_event.py

Exports updated in:

    quantcore/backtest/__init__.py

Commit:

    06de306 Add strict H017 event wrapper

Focused tests:

    tests/test_h017_strict_event.py
    9 passed

Related tests:

    tests/test_h017_event.py tests/test_bridge_windows.py
    19 passed

Full tests:

    532 passed

New dataclass:

    StrictH017EventBacktestResult

Fields:

    backtest
    accepted_entry_times
    executed_entry_times
    skipped_entry_times
    accepted_entry_count
    executed_entry_count
    skipped_entry_count
    expected_h4_delta

New functions:

    backtest_h017_strict_event_driven(...)
    backtest_h017_strict_event_from_result(...)

Public signatures verified at time of implementation:

    backtest_h017_strict_event_driven(
        *,
        usdjpy_h4: pd.DataFrame,
        xauusd_h4: pd.DataFrame,
        usdjpy_m1: pd.DataFrame,
        xauusd_m1: pd.DataFrame,
        accepted_entry_times: Iterable[pd.Timestamp],
        config: H017Config | None = None,
        starting_equity_usd: float = 10000.0,
        slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
        expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
    ) -> StrictH017EventBacktestResult

    backtest_h017_strict_event_from_result(
        *,
        h017_result: H017Result,
        usdjpy_h4: pd.DataFrame,
        xauusd_h4: pd.DataFrame,
        usdjpy_m1: pd.DataFrame,
        xauusd_m1: pd.DataFrame,
        accepted_entry_times: Iterable[pd.Timestamp],
        starting_equity_usd: float = 10000.0,
        slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
        expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
    ) -> StrictH017EventBacktestResult

Wrapper behavior:

1. The wrapper does not modify the existing event engine.
2. It preserves the native H4/H017 decision index.
3. It accepts either:
   - raw H4 frames and runs `run_h017(...)`, or
   - an already-built `H017Result`.
4. It validates accepted entry timestamps:
   - timezone-aware UTC,
   - sorted ascending,
   - no duplicates.
5. For each native event-engine interval:
   - `decision_time = decision_index[i - 1]`
   - `entry_time = decision_index[i]`
   - `forced_exit_time = decision_index[i + 1]`
6. It executes only if:
   - `entry_time in accepted_entry_times`
   - `forced_exit_time - entry_time == expected_h4_delta`
7. Otherwise, it forces the interval flat by zeroing the corresponding decision exposure.
8. Then it calls `backtest_h017_event_from_result(...)`.
9. It records accepted, executed, and skipped entry timestamps.
10. It writes no files.
11. It does not load real data by itself.

Why this exists:

The strict bridge-window timestamps are not contiguous. The wrapper prevents invalid forced exits across gaps while still preserving the native H4 index.

## Current API Snapshot

Before using these in new code, inspect again with `inspect.signature(...)` and `dataclasses.fields(...)`.

Strategy layer:

    quantcore.strategy.h017.H017Config
    quantcore.strategy.h017.H017Result
    quantcore.strategy.h017.run_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None)

H017 claim:

    quantcore.strategy.h017_claim.H017BacktestResult
    quantcore.strategy.h017_claim.H017Claim
    quantcore.strategy.h017_claim.build_h017_claim(
        returns,
        periods_per_year=1512,
        sr_benchmark=0.0,
        confidence=0.95,
        psr_threshold=0.95,
        sr_estimates=None,
        dsr_threshold=0.95,
    )

Event engine:

    quantcore.backtest.h017_event.H017EventBacktestResult
    quantcore.backtest.h017_event.backtest_h017_event_driven(...)
    quantcore.backtest.h017_event.backtest_h017_event_from_result(...)

Strict event wrapper:

    quantcore.backtest.h017_strict_event.StrictH017EventBacktestResult
    quantcore.backtest.h017_strict_event.backtest_h017_strict_event_driven(...)
    quantcore.backtest.h017_strict_event.backtest_h017_strict_event_from_result(...)

Bridge-window preflight:

    quantcore.data.bridge_windows.BridgeWindowRejectionCount
    quantcore.data.bridge_windows.CommonCompleteBridgeWindowAssessment
    quantcore.data.bridge_windows.assess_common_complete_h4_m1_windows(...)

MT5 loader:

    quantcore.data.mt5_loader.MT5LoadResult
    quantcore.data.mt5_loader.load_mt5_csv(path, broker_tz="Europe/Athens")

Preflight:

    quantcore.data.preflight.RequiredFileStatus
    quantcore.data.preflight.RequiredFilesReport
    quantcore.data.preflight.assess_required_files(...)
    quantcore.data.preflight.require_existing_files(...)

## Existing Real-Data Script Status

Existing script:

    scripts/run_h017_event_real.py

This is the older smoke path.

It:

1. Loads the four MT5 exports.
2. Applies existing H4 leakage trimming.
3. Trims to a broad common H4/M1 window.
4. Runs `backtest_h017_event_driven(...)`.
5. Builds an H017 claim.

It is useful as an operational smoke reference, but it is not sufficient for expanded validation because it does not enforce:

1. The strict accepted common complete bridge-window set.
2. Exactly 5476 accepted common windows.
3. Exactly 240 M1 bars for USDJPY in every included H4 execution interval.
4. Exactly 240 M1 bars for XAUUSD in every included H4 execution interval.
5. Exclusion or forced-flat behavior for incomplete bridge windows.
6. Native H4 interval preservation while skipping invalid windows.

Do not run `scripts/run_h017_event_real.py` as the expanded validation run.

## Recommended Next Path

Next logical sub-phase:

    Phase 3.26-aq - Strict expanded broker-native H017 validation runner preflight/design inspection

Do not run H017 immediately.

First do a read-only inspection of:

    quantcore/backtest/h017_strict_event.py
    tests/test_h017_strict_event.py
    quantcore/data/bridge_windows.py
    scripts/run_h017_event_real.py
    quantcore/strategy/h017_claim.py
    quantcore/backtest/__init__.py

Suggested command pattern:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    @'
    import dataclasses
    import inspect
    from quantcore.backtest import h017_strict_event
    from quantcore.data import bridge_windows
    from quantcore.strategy import h017_claim
    ...
    '@ | python -

After inspection, likely implementation target:

    scripts/run_h017_strict_event_real.py

The new strict real-data validation script should:

1. Load four broker-native MT5 exports.
2. Use `require_existing_files(...)` before loading.
3. Use `load_mt5_csv(...)`.
4. Run `assess_common_complete_h4_m1_windows(...)`.
5. Assert:
       accepted_count == 5476
       first_accepted_timestamp == 2021-07-02 13:00:00+00:00
       last_accepted_timestamp == 2026-04-30 01:00:00+00:00
6. Preserve native H4 frames.
7. Do not filter H4 only to accepted timestamps.
8. Pass `assessment.accepted_timestamps` as `accepted_entry_times` to `backtest_h017_strict_event_driven(...)`.
9. Build a claim using `build_h017_claim(result.backtest.portfolio.returns, periods_per_year=1512)`.
10. Print loader summaries.
11. Print strict bridge-window assessment.
12. Print accepted/executed/skipped counts from the strict wrapper.
13. Print backtest metrics.
14. Print claim summary.
15. Print explicit verdict:
    - H017 is not automatically promotable.
    - Expanded validation is research evidence only.
    - Live trading is not approved.
16. Do not write derived datasets.
17. Do not change H017 config.
18. Do not change the cost model.
19. Do not use HistData.

Consider whether to add synthetic tests for reusable helper functions if logic is placed outside the script.

If the script remains manual-only, still run full tests before commit.

## Critical Caution Before Real H017 Run

The strict wrapper now exists and is tested synthetically.

But no expanded broker-native strict H017 real-data validation run has been performed yet.

Before performing the run:

1. Verify hygiene.
2. Inspect APIs.
3. Decide script shape.
4. Implement the strict script.
5. Run focused tests if any.
6. Run full `pytest -q`.
7. Commit and push script.
8. Only after committed/pushed script exists should the real-data strict H017 run be executed.
9. Document the output in `docs/operations`.
10. Commit and push the documentation.

Do not combine too many steps if output is large.

## Absolute Do-Not Rules At HANDOFF_31

Do not:

1. Do not tune H017.
2. Do not change H017 parameters.
3. Do not change the cost model.
4. Do not add ML.
5. Do not broaden to more symbols.
6. Do not start Phase 4 execution.
7. Do not live trade.
8. Do not use HistData for H017 validation.
9. Do not accept HistData as a research source.
10. Do not build HistData H4 for H017 validation.
11. Do not combine broker H4 with HistData M1.
12. Do not use sparse 2018 through 2021-06 broker-native prefix as dense M1.
13. Do not include incomplete H4/M1 windows.
14. Do not use any bridge window where either symbol has fewer or more than exactly 240 M1 bars.
15. Do not impute missing M1 bars.
16. Do not forward-fill or backfill M1 bars.
17. Do not synthesize bars.
18. Do not modify raw broker files.
19. Do not commit raw MT5 CSV files.
20. Do not commit raw HistData files.
21. Do not change `.gitignore` from `/data/` to `data/`.
22. Do not run old `scripts/run_h017_event_real.py` as expanded validation.
23. Do not filter H4 to accepted timestamps only.
24. Do not ignore the 1327 accepted timestamp gaps found in the contiguity diagnostic.
25. Do not treat source acceptance as H017 promotion.
26. Do not treat future validation as live-trading approval.
27. Do not ignore the previous -33.65 percent drawdown.
28. Do not continue development while local commits are unpushed.
29. Do not let git status go unread.
30. Do not skip full pytest.
31. Do not allow test count to drop below 532 without explicit test-removal phase.

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

Understood. I am continuing after Phase 3.26-ap and HANDOFF_31.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is 532 passed.
3. Latest expected handoff commit is `Add handoff document #31 after strict H017 event wrapper`.
4. Latest expected pre-handoff commit is `06de306 Add strict H017 event wrapper`.
5. Expanded broker-native USDJPY + XAUUSD M1/H4 is conditionally accepted for future H017 validation only under strict complete-window rules.
6. The strict bridge-window preflight exists in `quantcore/data/bridge_windows.py`.
7. Real-data strict preflight confirmed exactly 5476 accepted windows.
8. Accepted bridge-window range is `2021-07-02 13:00:00+00:00` through `2026-04-30 01:00:00+00:00`.
9. Every accepted execution window must have exactly 240 M1 bars per symbol inside `[H4 timestamp, H4 timestamp + 4 hours)`.
10. Accepted timestamps are not contiguous enough to filter H4 directly.
11. There are 1327 non-four-hour gaps between accepted timestamps.
12. The strict event wrapper exists in `quantcore/backtest/h017_strict_event.py`.
13. The wrapper preserves the native H4/H017 index and executes only accepted +4h entry intervals.
14. H017 is still alive but not promotable.
15. No H017 expanded real-data validation run has happened yet.
16. The old `scripts/run_h017_event_real.py` is not sufficient for expanded validation.
17. Do not tune H017.
18. Do not change the cost model.
19. Do not use HistData.
20. Do not live trade or start Phase 4 execution.
21. The next logical sub-phase is Phase 3.26-aq: strict expanded broker-native H017 validation runner preflight/design inspection.
22. First task is hygiene verification only. No new code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -15
    pytest -q

Then paste the full output.

✅ done, proceed
⚠️ error — paste it
🤔 question