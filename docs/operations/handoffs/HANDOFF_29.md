# HANDOFF 29 - Self-Contained Continuation After Expanded Broker-Native Source Acceptance Checkpoint

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_29 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

* Research: Python quantcore
* Execution: MetaTrader 5 later
* Production target: Oracle Cloud Always Free VPS later
* Monitoring: self-hosted free-tier stack later
* Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in `.venv`

Do not rush into strategy validation or live trading. The project is still in research-validation infrastructure work.

## Non-Negotiable Workflow Rules

Use:

* Windows
* PowerShell
* VS Code
* Python 3.12.10
* `.venv`
* No WSL
* No Linux/macOS shell assumptions

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

Latest project commit immediately before this handoff is committed:

    5df6868 Add expanded broker-native source acceptance checkpoint

Expected latest commit after this handoff is committed:

    Add handoff document #29 after expanded broker-native source acceptance

Recent commits:

    5df6868 Add expanded broker-native source acceptance checkpoint
    4cecd97 Document expanded broker-native missingness time-bucket diagnostic
    0b0a923 Document expanded broker-native common-window diagnostic
    135e3e1 Document expanded broker-native session boundary diagnostic
    e559dcb Document expanded broker-native session diagnostic preflight
    4f50d92 Add expanded broker-native session common-window diagnostic plan
    8f0bded Add handoff document #28 after expanded broker-native M1 diagnostics
    4bc05f7 Add handoff document #28 after expanded broker-native M1 diagnostics
    61b822e Document expanded broker-native H4 M1 aggregation diagnostic
    66faeb3 Document expanded broker-native M1 coverage density diagnostic
    66d7100 Document expanded broker-native loader timestamp diagnostic
    3d1c67f Document broker-native expanded raw inventory

Known note:

There are duplicate consecutive handoff commit messages for HANDOFF_28. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    514 passed

Important test-count rule:

* Previous anchor after Phase 3.25 was 509 passed.
* Phase 3.26-b deliberately added 5 HistData duplicate-policy tests.
* Current correct anchor is 514 passed.
* If tests pass but the count drops below 514 without a deliberate test-removal phase, treat it as a regression.

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

* On branch main
* Your branch is up to date with origin/main.
* nothing to commit, working tree clean

Expected latest commit:

    Add handoff document #29 after expanded broker-native source acceptance

Expected project commit before handoff:

    5df6868 Add expanded broker-native source acceptance checkpoint

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

* do not commit raw data,
* do not commit large derived data,
* do not write derived data before explicit authorization,
* do not modify raw vendor/broker files.

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

## Recent Key Documents

Documents added after HANDOFF_28:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_COMMON_WINDOW_DIAGNOSTIC_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_DIAGNOSTIC_PREFLIGHT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_DIAGNOSTIC_PREFLIGHT_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_BOUNDARY_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SESSION_BOUNDARY_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_COMMON_WINDOW_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_COMMON_WINDOW_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_MISSINGNESS_BY_TIME_BUCKET_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_MISSINGNESS_BY_TIME_BUCKET_DIAGNOSTIC_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SOURCE_ACCEPTANCE_CHECKPOINT.md

Important earlier expanded broker-native docs:

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

* H001: Backtest without intrabar SL/TP simulation is fiction. Must use M1 inside H4 bars to resolve fills.
* H002-H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
* H004a: Single-seed models unreliable; use multi-seed ensembles.
* H005: Stacked multi-symbol models fail on heterogeneous instruments; use per-symbol models.
* H006-H007: Confidence filters are not risk management. ML chooses entries; deterministic rules manage risk.
* H008-H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals cannot be risk manager.
* H011-H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk ceiling remained.
* H014-H016: Two-asset USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1 percent per-trade risk was not 1 percent portfolio risk when trades overlapped. Drawdown breach was -19.43 percent.
* H015: Diversification into negative-edge instruments destroys the portfolio.
* H017: H016 plus portfolio heat governor. Alive but not promotable.

Do not broaden to more symbols yet.
Do not add machine learning yet.
Do not tune H017.

## Core Strategy Conventions

ATR:

* Wilder RMA, not SMA.
* First true range is high - low.
* Seed at index window - 1 with simple mean of first window true ranges.
* Recurrence:

    ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n

Chandelier Exit:

* Long:

    highest_high(lookback) - multiplier * ATR

* Short:

    lowest_low(lookback) + multiplier * ATR

Defaults:

    multiplier = 3.0
    lookback = 22

Vol Target:

* Realized vol at bar t uses returns through t-1 only:

    returns.shift(1).rolling(lookback)

* No lookahead.
* For H4 bars:

    periods_per_year = 1512

Signals:

* Donchian breakout.
* Long:

    close[t] > max(high[t-N ... t-1])

* Short:

    close[t] < min(low[t-N ... t-1])

* Channel uses prior N bars:

    shift(1).rolling(N)

H017:

* Inner-joins USDJPY and XAUUSD timestamps.
* Computes close-to-close returns.
* Uses same returns for vol targeting and heat governor.
* Position is signed risk exposure:

    signal * per_trade_risk * vol_mult * heat_mult

Heat governor:

* Combined heat:

    sqrt(w' (r^2 * C) w)

* Defaults:

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

* XAUUSD P&L is already USD.
* USDJPY P&L is JPY and must be divided by USDJPY conversion price to become USD.

Event bridge timing:

1. H017 decides at H4 timestamp t.
2. Trade opens on next H4 bar open t+1.
3. M1 bars inside [t+1, t+2) resolve stops.
4. If no stop is hit, exposure closes at t+2 open as signal_flip.
5. This is a bridge-layer simplification.

## H017 Current Status

H017 remains:

* alive,
* not promotable,
* not ready for live trading,
* not validated on the expanded broker-native source yet.

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

* Winter UTC+2
* Summer UTC+3
* DST-aware

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

* pandas DataFrame
* DatetimeIndex
* index name: `dt`
* timezone: UTC
* columns: `open`, `high`, `low`, `close`, `volume`

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

### Raw inventory

USDJPY M1:

    size_bytes: 108190060
    sha256: 679bb6f153a24aac8fc27238ad1ba7f5fb121a759baea759c8b59ac1b18b2619
    line_count: 1785313

USDJPY H4:

    size_bytes: 548819
    sha256: 72a6db90e42b53338ff5a57e5362be32c77caca290c90800c8cf60ce342e7651
    line_count: 8714

XAUUSD M1:

    size_bytes: 113195272
    sha256: dc08ef307f9eb6566e4dfdb88cd1bcaaf473f26ab5b30724230ef2fd2b52e609
    line_count: 1704908

XAUUSD H4:

    size_bytes: 594386
    sha256: ae9280b257bedd889152392339c32eb957a8aa4549649ac343a73e2663ac8b74
    line_count: 8659

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

### Session-boundary diagnostic

Dense-region rule used:

    2021-07-01 00:00:00+00:00

USDJPY:

    dense_region_bars: 1784379
    first_utc: 2021-07-01 21:00:00+00:00
    last_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps: False
    observed_utc_dates: 1518
    gap_events_gt_1_minute: 11277
    most_common_gap_duration: 0 days 00:02:00
    largest_gap_duration: 3 days 00:11:00
    daily_break_like_gaps_30_to_90_minutes: 3
    small_intraday_gaps_2_to_29_minutes: 11005

XAUUSD:

    dense_region_bars: 1703974
    first_utc: 2021-07-01 21:00:00+00:00
    last_utc: 2026-04-30 07:00:00+00:00
    duplicate_timestamps: False
    observed_utc_dates: 1510
    gap_events_gt_1_minute: 1428
    most_common_gap_duration: 0 days 01:04:00
    largest_gap_duration: 3 days 01:08:00
    daily_break_like_gaps_30_to_90_minutes: 958
    small_intraday_gaps_2_to_29_minutes: 167

Important note:

There are a small number of Saturday single bars in early July/August 2021. Treat this as a source-quality note, not as justification to weaken validation rules.

### Cross-symbol common-window diagnostic

Common M1 span:

    2021-07-01 21:00:00+00:00 through 2026-04-30 07:00:00+00:00

Counts:

    calendar_minutes_inclusive: 2539321
    USDJPY_observed_minutes: 1784379
    XAUUSD_observed_minutes: 1703974
    shared_observed_minutes: 1695042
    USDJPY_only_observed_minutes: 89337
    XAUUSD_only_observed_minutes: 8932
    neither_symbol_calendar_minutes: 746010
    shared_observed_pct_of_calendar: 66.751781

Complete H4/M1 windows:

USDJPY:

    candidate_h4_windows_evaluated: 7779
    exact_4h_next_delta_windows: 7515
    complete_240_m1_windows: 5701

XAUUSD:

    candidate_h4_windows_evaluated: 7724
    exact_4h_next_delta_windows: 7460
    complete_240_m1_windows: 6149

Cross-symbol common complete windows:

    common_complete_h4_m1_windows: 5476
    USDJPY_only_complete_h4_m1_windows: 225
    XAUUSD_only_complete_h4_m1_windows: 673
    first_common_complete_h4_window_utc: 2021-07-02 13:00:00+00:00
    last_common_complete_h4_window_utc: 2026-04-30 01:00:00+00:00

### Missingness-by-time-bucket diagnostic

Common calendar span:

    2021-07-01 21:00:00+00:00 through 2026-04-30 07:00:00+00:00

Calendar minutes inclusive:

    2539321

USDJPY:

    observed_minutes: 1784379
    missing_calendar_minutes: 754942
    observed_pct_of_calendar: 70.269926
    missing_cluster_count: 11277
    largest_missing_cluster_minutes: 4330
    single_minute_missing_clusters: 7941
    small_2_to_29_minute_missing_clusters: 3064
    daily_break_like_30_to_90_minute_missing_clusters: 3
    weekend_or_longer_721_plus_missing_clusters: 264

XAUUSD:

    observed_minutes: 1703974
    missing_calendar_minutes: 835347
    observed_pct_of_calendar: 67.103529
    missing_cluster_count: 1428
    largest_missing_cluster_minutes: 4387
    single_minute_missing_clusters: 107
    small_2_to_29_minute_missing_clusters: 60
    daily_break_like_30_to_90_minute_missing_clusters: 958
    weekend_or_longer_721_plus_missing_clusters: 264

Interpretation:

* XAUUSD missingness is dominated by expected-looking daily breaks and closures.
* USDJPY has many tiny missing clusters.
* This is acceptable only under a strict complete-H4/M1-window rule.
* Do not assume continuous M1 availability.
* Do not impute.

## Current Source Acceptance Status

As of commit:

    5df6868 Add expanded broker-native source acceptance checkpoint

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

* explicitly planned diagnostics only,
* documentation,
* source-quality comparison,
* raw inventory metadata preservation.

Not allowed:

* H017 validation,
* strategy tuning,
* derived production datasets,
* derived H4 files for H017 validation,
* broker-H4 plus HistData-M1 hybrid validation,
* silent deduplication,
* raw file modification,
* raw file commits.

## Current Source Status After HANDOFF_29

Accepted H4 reference for broker-aligned diagnostics:

    Broker-native H4

Accepted M1 source for future H017 validation:

    Expanded broker-native M1, conditionally accepted under strict complete-window rules.

Accepted long-history M1 validation source:

    Expanded broker-native M1, conditionally accepted only for USDJPY and XAUUSD and only inside common complete H4/M1 windows.

Accepted H017 validation source:

    Expanded broker-native USDJPY + XAUUSD M1/H4, conditionally accepted for a future validation phase only.

HistData status:

    Rejected for H017 validation under current evidence.
    Diagnostic-reference only.

H017 status:

    Alive but not promotable.

Research validation status:

    Still pending actual H017 validation run on the conditionally accepted source.

Live trading status:

    Not authorized.

## Practical Next Path

The next logical work is not to run H017 blindly.

Recommended next sub-phase:

    Phase 3.26-al - Expanded broker-native H017 validation run plan and preflight

Purpose:

1. Inspect actual existing H017/event-bridge/backtest APIs.
2. Confirm how to enforce the common complete H4/M1 bridge-window rule.
3. Confirm the exact files/modules/scripts involved.
4. Write a run plan before executing H017.
5. Do not tune H017.
6. Do not change the cost model.
7. Do not write derived datasets unless explicitly planned.
8. Do not start live trading.
9. Do not start Phase 4 execution.

Before any validation run, inspect APIs with:

    inspect.signature(...)
    dataclasses.fields(...)

Likely code areas to inspect, but do not assume names:

    C:\Users\equin\Documents\institutional-ea\quantcore
    C:\Users\equin\Documents\institutional-ea\scripts
    C:\Users\equin\Documents\institutional-ea\tests

Use grep/Search only with Windows/PowerShell compatible commands.

Suggested first diagnostic for Phase 3.26-al:

1. `git status`
2. Search for H017/event bridge/backtest entry points.
3. Inspect signatures and dataclasses.
4. Document a run plan.
5. Do not run H017 until the run plan is committed and pushed.

## Absolute Do-Not Rules At HANDOFF_29

Do not:

1. Do not run H017 without a committed run plan/preflight.
2. Do not tune H017.
3. Do not change H017 parameters.
4. Do not change the cost model.
5. Do not use HistData for H017 validation.
6. Do not accept HistData as a research source.
7. Do not build HistData H4 for H017 validation.
8. Do not combine broker H4 with HistData M1.
9. Do not use the sparse 2018 through 2021-06 broker-native prefix.
10. Do not include incomplete H4/M1 windows in validation.
11. Do not use any H4/M1 window where either symbol has fewer or more than exactly 240 M1 bars.
12. Do not impute missing M1 bars.
13. Do not forward-fill or backfill M1 bars.
14. Do not synthesize bars.
15. Do not modify raw broker files.
16. Do not commit raw MT5 CSV files.
17. Do not commit raw HistData CSV files.
18. Do not change `.gitignore` from `/data/` to `data/`.
19. Do not broaden to more symbols.
20. Do not add machine learning.
21. Do not start Phase 4 execution code.
22. Do not start live trading.
23. Do not ignore the previous -33.65 percent drawdown.
24. Do not continue development while local commits are unpushed.
25. Do not let git status go unread.
26. Do not use Linux/macOS shell syntax in PowerShell.
27. Do not silently deduplicate vendor data.
28. Do not write derived data files without an explicit phase authorizing it.
29. Do not treat source acceptance as H017 promotion.
30. Do not treat future validation as live-trading approval.
31. Do not skip full pytest.
32. Do not allow test count to drop below 514 without an explicit test-removal phase.

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

Understood. I am continuing after Phase 3.26-ak and HANDOFF_29.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is 514 passed.
3. Latest expected handoff commit is `Add handoff document #29 after expanded broker-native source acceptance`.
4. Latest expected project commit before the handoff is `5df6868 Add expanded broker-native source acceptance checkpoint`.
5. Broker-native expanded raw files are local under `/data/` and must not be committed.
6. The sparse broker-native prefix from 2018 through 2021-06 remains excluded.
7. Expanded broker-native USDJPY + XAUUSD M1/H4 is conditionally accepted for future H017 validation only under strict complete-window rules.
8. The future accepted bridge-window range is `2021-07-02 13:00:00+00:00` through `2026-04-30 01:00:00+00:00`.
9. There are `5476` common complete H4/M1 windows.
10. Each future validation window must have exactly 240 M1 bars per symbol inside `[H4 timestamp, H4 timestamp + 4 hours)`.
11. No imputation, forward-fill, backfill, synthetic bars, or HistData are allowed.
12. H017 is still alive but not promotable.
13. No H017 run should happen before a committed run plan/preflight.
14. Do not tune H017.
15. Do not change the cost model.
16. Do not start live trading or Phase 4 execution.
17. The next logical sub-phase is Phase 3.26-al: expanded broker-native H017 validation run plan and preflight.
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
