# HANDOFF 28 - Self-Contained Continuation After Expanded Broker-Native M1 Diagnostics

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_28 wins.

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

Do not rush into strategy validation or live trading. The project remains in data infrastructure and research-validation work.

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

Current latest project commit immediately before this handoff is committed:

    61b822e Document expanded broker-native H4 M1 aggregation diagnostic

Expected latest commit after this handoff is committed:

    Add handoff document #28 after expanded broker-native M1 diagnostics

Recent commit context:

    61b822e Document expanded broker-native H4 M1 aggregation diagnostic
    66faeb3 Document expanded broker-native M1 coverage density diagnostic
    66d7100 Document expanded broker-native loader timestamp diagnostic
    3d1c67f Document broker-native expanded raw inventory
    4364ab7 Add broker-native M1 acquisition attempt log template
    0b522a8 Add broker-native M1 acquisition action plan
    394712b Document long broker-native M1 acquisition options checkpoint
    f6b93c8 Add handoff document #27 after HistData path decision checkpoint
    b8f58c5 Document HistData path decision checkpoint
    b43dfe5 Document H4 construction decision checkpoint
    3cdeaca Document broker H4 M1 alignment diagnostic
    6a48870 Document broker H4 M1 loaded shape inspection
    545b5c7 Add handoff document #26 after broker H4 M1 preflight
    82c68fa Document broker H4 M1 alignment preflight
    043de0d Add broker H4 M1 alignment diagnostic plan

Known note:

There are two older consecutive commits with the message `Add handoff document #23 after HistData duplicate policy`. This is known and not blocking. Do not rewrite history.

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

    Add handoff document #28 after expanded broker-native M1 diagnostics

Expected project commit before handoff:

    61b822e Document expanded broker-native H4 M1 aggregation diagnostic

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

Important tests:

    C:\Users\equin\Documents\institutional-ea\tests\test_mt5_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_dukascopy_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_coverage.py
    C:\Users\equin\Documents\institutional-ea\tests\test_preflight.py

## Current Key Documents

Recent docs added after HANDOFF_27:

    C:\Users\equin\Documents\institutional-ea\docs\operations\LONG_BROKER_NATIVE_M1_ACQUISITION_OPTIONS_CHECKPOINT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_M1_ACQUISITION_ACTION_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_M1_ACQUISITION_ATTEMPT_LOG_TEMPLATE.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_RAW_INVENTORY.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_LOADER_TIMESTAMP_SHAPE_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_LOADER_TIMESTAMP_SHAPE_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_M1_COVERAGE_DENSITY_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_M1_COVERAGE_DENSITY_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H4_M1_AGGREGATION_COMPATIBILITY_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H4_M1_AGGREGATION_COMPATIBILITY_DIAGNOSTIC_OUTPUT.txt

Important earlier docs:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_PATH_DECISION_CHECKPOINT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_DECISION_CHECKPOINT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_LOADED_SHAPE_INSPECTION.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_PREFLIGHT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_MISMATCH_ASSESSMENT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_SHORT_WINDOW_SESSION_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md

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
Do not tune H017 to vendor quirks or short-window results.

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

- Defaults:

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
- not authorized for HistData validation,
- not yet authorized for expanded broker-native validation,
- pending explicit source acceptance for the expanded broker-native dense M1 region.

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

Operational verdict:

    PIPELINE SMOKE PASSED: True
    RESEARCH VALIDATION SUFFICIENT: False

Interpretation:

1. The event pipeline works.
2. The previous short broker-native M1 history was too short.
3. Do not trust the short-window +61.46 percent return as validated edge.
4. The -33.65 percent drawdown is a serious risk signal.
5. H017 is alive but not promotable.

Do not run H017 until source acceptance explicitly allows it.

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

Expanded broker-native raw exports are local and gitignored:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Reported exact MT5 symbols:

    USDJPYm
    XAUUSDm

Do not commit these raw files.

## Expanded Broker-Native Raw Inventory Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_RAW_INVENTORY.md

Commit:

    3d1c67f Document broker-native expanded raw inventory

Status:

- Read-only.
- Broker-native only.
- No HistData used.
- No H017 run.
- No derived data written.
- No raw files committed.

Inventory:

USDJPY M1:

    path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    size_bytes: 108190060
    sha256: 679bb6f153a24aac8fc27238ad1ba7f5fb121a759baea759c8b59ac1b18b2619
    line_count: 1785313

USDJPY H4:

    path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    size_bytes: 548819
    sha256: 72a6db90e42b53338ff5a57e5362be32c77caca290c90800c8cf60ce342e7651
    line_count: 8714

XAUUSD M1:

    path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
    size_bytes: 113195272
    sha256: dc08ef307f9eb6566e4dfdb88cd1bcaaf473f26ab5b30724230ef2fd2b52e609
    line_count: 1704908

XAUUSD H4:

    path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    size_bytes: 594386
    sha256: ae9280b257bedd889152392339c32eb957a8aa4549649ac343a73e2663ac8b74
    line_count: 8659

Important observation:

The raw files appear to start around 2018, but later diagnostics proved that 2018 through 2021-06 is sparse/daily-like, not dense M1 history.

## Expanded Broker-Native Loader Timestamp-Shape Diagnostic Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_LOADER_TIMESTAMP_SHAPE_DIAGNOSTIC.md

Output:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_LOADER_TIMESTAMP_SHAPE_DIAGNOSTIC_OUTPUT.txt

Commit:

    66d7100 Document expanded broker-native loader timestamp diagnostic

Status:

- Read-only.
- Broker-native only.
- No HistData used.
- No H017 run.
- No derived data written.
- No raw files committed.

API inspection:

    load_mt5_csv_signature: (path: 'str | Path', broker_tz: 'str' = 'Europe/Athens') -> 'MT5LoadResult'

Key results:

USDJPY M1:

    n_input_rows: 1785312
    n_bars: 1785312
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps_after_load: 0
    expected_delta: 1 minute
    expected_delta_pct: 99.316086
    classification: expected_timeframe_spaced

USDJPY H4:

    n_input_rows: 8713
    n_bars: 8713
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-30 05:00:00+00:00
    duplicate_timestamps_after_load: 0
    expected_delta: 4 hours
    expected_delta_pct: 86.260331
    classification: expected_timeframe_spaced

XAUUSD M1:

    n_input_rows: 1704907
    n_bars: 1704907
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps_after_load: 0
    expected_delta: 1 minute
    expected_delta_pct: 99.861517
    classification: expected_timeframe_spaced

XAUUSD H4:

    n_input_rows: 8658
    n_bars: 8658
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 05:00:00+00:00
    duplicate_timestamps_after_load: 0
    expected_delta: 4 hours
    expected_delta_pct: 86.173039
    classification: expected_timeframe_spaced

Important nuance:

The aggregate one-minute spacing looked good overall because the later dense region dominates the count. The first rows were daily-like, so coverage-density diagnostics were required.

## Expanded Broker-Native M1 Coverage-Density Diagnostic Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_M1_COVERAGE_DENSITY_DIAGNOSTIC.md

Output:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_M1_COVERAGE_DENSITY_DIAGNOSTIC_OUTPUT.txt

Commit:

    66faeb3 Document expanded broker-native M1 coverage density diagnostic

Status:

- Read-only.
- Broker-native only.
- No HistData used.
- No H017 run.
- No derived data written.
- No raw files committed.

Key result:

The expanded files have a sparse daily-like prefix from 2018 through 2021-06, then become dense M1 candidates starting in 2021-07.

USDJPY M1:

    n_input_rows: 1785312
    n_bars: 1785312
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps_after_load: 0
    monotonic_increasing: True
    one_minute_delta_pct: 99.316086
    first_month_observed_pct_ge_50: 2021-07
    first_month_observed_pct_ge_40: 2021-07
    first_month_observed_pct_ge_25: 2021-07
    n_months_total: 94
    n_months_very_sparse_lt_10_pct: 36
    n_months_dense_ge_50_pct: 58
    classification: has_dense_m1_candidate_region
    prefix_or_gap_note: sparse_prefix_or_gaps_present

USDJPY yearly calendar density:

    2018: 0.059102 percent
    2019: 0.059170 percent
    2020: 0.059199 percent
    2021: 34.306507 percent
    2022: 69.908295 percent
    2023: 70.312405 percent
    2024: 70.892532 percent
    2025: 70.829338 percent
    2026: 70.617822 percent

XAUUSD M1:

    n_input_rows: 1704907
    n_bars: 1704907
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps_after_load: 0
    monotonic_increasing: True
    one_minute_delta_pct: 99.861517
    first_month_observed_pct_ge_50: 2021-07
    first_month_observed_pct_ge_40: 2021-07
    first_month_observed_pct_ge_25: 2021-07
    n_months_total: 95
    n_months_very_sparse_lt_10_pct: 37
    n_months_dense_ge_50_pct: 58
    classification: has_dense_m1_candidate_region
    prefix_or_gap_note: sparse_prefix_or_gaps_present

XAUUSD yearly calendar density:

    2018: 0.059007 percent
    2019: 0.058790 percent
    2020: 0.059009 percent
    2021: 33.721081 percent
    2022: 67.143075 percent
    2023: 66.950723 percent
    2024: 67.232658 percent
    2025: 67.183029 percent
    2026: 66.733806 percent

Interpretation:

1. Do not treat 2018-2021-06 as dense M1 history.
2. Dense candidate region starts at 2021-07 for both symbols.
3. This is promising but not source acceptance.
4. H017 still must not be run.

## Expanded Broker-Native H4/M1 Aggregation Compatibility Diagnostic Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H4_M1_AGGREGATION_COMPATIBILITY_DIAGNOSTIC.md

Output:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_H4_M1_AGGREGATION_COMPATIBILITY_DIAGNOSTIC_OUTPUT.txt

Commit:

    61b822e Document expanded broker-native H4 M1 aggregation diagnostic

Status:

- Read-only.
- Broker-native only.
- No HistData used.
- No H017 run.
- No derived data written.
- No raw files committed.

Method:

1. Load broker-native H4 and M1 files with `load_mt5_csv(..., broker_tz="Europe/Athens")`.
2. Sort loaded bars by UTC timestamp.
3. Consider only H4 bars whose next H4 timestamp is exactly 4 hours later.
4. Define M1 aggregation window as `[H4 timestamp, H4 timestamp + 4 hours)`.
5. Require exactly 240 M1 bars inside the window.
6. Aggregate M1 as:
   - open = first M1 open,
   - high = max M1 high,
   - low = min M1 low,
   - close = last M1 close,
   - volume = sum M1 volume.
7. Compare aggregated M1 OHLCV to broker-native H4 OHLCV.

USDJPY result:

    total_h4_bars: 8713
    candidate_exact_4h_bars: 7515
    skipped_non_4h_next_delta: 1197
    skipped_outside_m1_range: 0
    skipped_incomplete_m1_window: 1814
    compared_full_m1_windows: 5701
    matched_bars: 5701
    mismatched_bars: 0
    first_full_m1_window_utc: 2021-07-02 13:00:00+00:00
    last_full_m1_window_utc: 2026-04-30 01:00:00+00:00
    first_matched_window_utc: 2021-07-02 13:00:00+00:00
    last_matched_window_utc: 2026-04-30 01:00:00+00:00
    classification: aligned_on_all_full_m1_windows

USDJPY yearly full windows matched:

    2021: 326
    2022: 1035
    2023: 1170
    2024: 1366
    2025: 1377
    2026: 427

XAUUSD result:

    total_h4_bars: 8658
    candidate_exact_4h_bars: 7460
    skipped_non_4h_next_delta: 1197
    skipped_outside_m1_range: 0
    skipped_incomplete_m1_window: 1311
    compared_full_m1_windows: 6149
    matched_bars: 6149
    mismatched_bars: 0
    first_full_m1_window_utc: 2021-07-02 13:00:00+00:00
    last_full_m1_window_utc: 2026-04-30 01:00:00+00:00
    first_matched_window_utc: 2021-07-02 13:00:00+00:00
    last_matched_window_utc: 2026-04-30 01:00:00+00:00
    classification: aligned_on_all_full_m1_windows

XAUUSD yearly full windows matched:

    2021: 640
    2022: 1271
    2023: 1271
    2024: 1281
    2025: 1271
    2026: 415

Interpretation:

1. On every fully covered comparable H4 window, broker-native M1 aggregation exactly reproduces broker-native H4 OHLCV.
2. This is strong evidence that the expanded broker-native M1 dense candidate region is internally compatible with broker-native H4.
3. The first full comparable window is 2021-07-02 13:00:00 UTC for both symbols.
4. The dense candidate region is not equivalent to the raw earliest timestamp.
5. This diagnostic is necessary but still not sufficient for source acceptance.
6. H017 remains not authorized.

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
7. Long-history H017 validation source: none accepted yet.
8. H017 status: alive but not promotable.

Reason for HistData rejection:

1. Duplicate timestamp handling required special documented policy.
2. March-July 2023 was materially abnormal for both symbols.
3. Source-session reconciliation remained unresolved.
4. Broker mismatch assessment was adverse.
5. Broker-native H4 became the accepted H4 reference for broker-aligned diagnostics.
6. HistData-built H4 remained unaccepted.
7. Broker H4 plus HistData M1 hybrid remained unaccepted.
8. Using HistData for H017 would risk validating against a source whose session structure and execution bars may not represent the broker.

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

## Current Source Status After HANDOFF_28

Accepted H4 reference for broker-aligned diagnostics:

    Broker-native H4

Accepted M1 source for broker-only diagnostics:

    Expanded broker-native M1 is a candidate source with strong diagnostics but is not yet formally accepted.

Accepted long-history M1 validation source:

    None yet

Accepted H017 validation source:

    None yet

Expanded broker-native M1 status:

    Promising candidate.
    Dense candidate region starts at 2021-07.
    Sparse daily-like prefix exists before 2021-07.
    H4/M1 aggregation aligns exactly on all fully covered windows tested.
    Still needs session/common-window/source-acceptance checkpoint before H017 validation.

HistData status:

    Rejected for H017 validation under current evidence.
    Diagnostic-reference only.

H017 status:

    Alive but not promotable.

Research validation status:

    Still blocked pending explicit source acceptance.

Live trading status:

    Not authorized.

## Practical Next Paths

The expanded broker-native data materially improves the situation.

The next logical work is still source-acceptance diagnostics, not strategy validation.

Recommended next sub-phase:

    Phase 3.26-af - Expanded broker-native session and common-window diagnostic plan

Purpose:

1. Plan remaining diagnostics before source acceptance.
2. Focus on dense candidate region from 2021-07 onward.
3. Document that 2018 through 2021-06 is sparse/daily-like and must not be treated as dense M1.
4. Do not run H017.
5. Do not write derived datasets.
6. Do not accept the source yet.

After that, likely diagnostics:

1. Expanded broker-native session-boundary analysis:
   - Sunday opens,
   - Friday closes,
   - XAUUSD daily breaks,
   - DST transition behavior.
2. Expanded cross-symbol common-window analysis:
   - common dense region,
   - overlapping observed minutes,
   - USDJPY-only missing minutes,
   - XAUUSD-only missing minutes,
   - shared missingness.
3. Missingness analysis by:
   - symbol,
   - year,
   - month,
   - UTC hour,
   - weekday,
   - session windows.
4. Explicit expanded broker-native source-acceptance checkpoint.

Only after explicit acceptance should H017 validation be considered.

## Absolute Do-Not Rules At HANDOFF_28

Do not:

1. Do not run H017 yet.
2. Do not run H017 on HistData.
3. Do not run H017 on expanded broker-native M1 before explicit source acceptance.
4. Do not accept expanded broker-native data implicitly.
5. Do not treat 2018-2021-06 as dense M1 history.
6. Do not ignore the sparse daily-like prefix.
7. Do not include sparse prefix in any future validation window.
8. Do not use HistData for H017 validation.
9. Do not accept HistData as a research source.
10. Do not build HistData H4 for H017 validation.
11. Do not combine broker H4 with HistData M1.
12. Do not tune H017.
13. Do not change the cost model.
14. Do not commit raw HistData CSV files.
15. Do not commit raw MT5 CSV files.
16. Do not call HistData files Dukascopy files.
17. Do not use the Dukascopy loader as the official HistData loader.
18. Do not change `.gitignore` from `/data/` to `data/`.
19. Do not start Phase 4 execution code.
20. Do not start live trading.
21. Do not ignore the previous -33.65 percent drawdown.
22. Do not broaden to more symbols yet.
23. Do not add machine learning yet.
24. Do not continue development while local commits are unpushed.
25. Do not let git status go unread.
26. Do not use Linux/macOS shell syntax in PowerShell.
27. Do not silently deduplicate vendor data.
28. Do not modify raw HistData files.
29. Do not modify raw MT5 files.
30. Do not write derived data files before source acceptance and a specific derived-data write phase.
31. Do not treat broker-native H4 acceptance for diagnostics as H017 validation.
32. Do not treat broker-native H4/M1 alignment as automatic source acceptance.
33. Do not treat good H4/M1 aggregation as sufficient alone.
34. Do not skip session and common-window diagnostics.
35. Do not skip full pytest.
36. Do not allow test count to drop below 514 without an explicit test-removal phase.

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

Understood. I am continuing after Phase 3.26-ae and HANDOFF_28.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is 514 passed.
3. Latest expected handoff commit is `Add handoff document #28 after expanded broker-native M1 diagnostics`.
4. Latest expected project commit before the handoff is `61b822e Document expanded broker-native H4 M1 aggregation diagnostic`.
5. Broker-native expanded raw files are local under `/data/` and must not be committed.
6. Expanded broker-native M1 has a sparse daily-like prefix from 2018 through 2021-06.
7. Dense broker-native M1 candidate region starts at 2021-07 for both USDJPY and XAUUSD.
8. Expanded broker-native H4/M1 aggregation aligned exactly on all fully covered windows:
   - USDJPY: 5701 matched, 0 mismatched.
   - XAUUSD: 6149 matched, 0 mismatched.
9. The expanded broker-native source is promising but not yet formally accepted.
10. H017 is still alive but not promotable.
11. H017 must not be run until explicit source acceptance.
12. HistData remains rejected for H017 validation.
13. Do not tune H017.
14. Do not start live trading or Phase 4 execution.
15. The next logical sub-phase is Phase 3.26-af: expanded broker-native session and common-window diagnostic plan.
16. First task is hygiene verification only. No new code yet.

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
