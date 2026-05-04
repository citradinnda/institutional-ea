# HANDOFF 32 - Self-Contained Continuation After Strict Expanded H017 Runner Crash Localization

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_32 wins.

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
13. For documentation-only phases, one consolidated PowerShell block is okay if it includes status, tests, commit, push, final status, git ls-files, and recent log.
14. For code or diagnostics, inspect APIs first and split cautiously.
15. Before writing code that calls internal functions, inspect actual APIs with `inspect.signature(...)` and `dataclasses.fields(...)`.
16. After each sub-phase, run focused tests if applicable, run full `pytest -q`, check status, commit, push, check status, run `git ls-files` on touched files/directories, and read the output.

After each response, offer exactly:

    ✅ done
    ⚠️ error — paste it
    🤔 question

## Repository State At This Handoff

Repository root:

    C:\Users\equin\Documents\institutional-ea

Virtual environment:

    C:\Users\equin\Documents\institutional-ea\.venv

Branch:

    main

GitHub remote:

    https://github.com/citradinnda/institutional-ea.git

Latest expected commit before this HANDOFF_32 document is committed:

    47f80a8 Add strict expanded H017 validation runner

Expected latest commit after this handoff is committed:

    Add handoff document #32 after strict expanded H017 crash localization

Recent commits at the time this handoff was written:

    47f80a8 Add strict expanded H017 validation runner
    756c014 Add handoff document #31 after strict H017 event wrapper
    737ec19 Add handoff document #31 after strict H017 event wrapper
    06de306 Add strict H017 event wrapper
    0c56c8d Document strict bridge-window contiguity diagnostic
    72ae6c1 Document strict bridge-window real-data preflight result
    56dcc56 Add strict common bridge-window preflight
    cdca565 Add handoff document #30 after expanded broker-native H017 preflight plan

Known note:

There are duplicate consecutive HANDOFF_31 commits. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    532 passed

Important test-count rule:

- Current correct full-test anchor is 532 passed.
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

    Add handoff document #32 after strict expanded H017 crash localization

Expected previous commit:

    47f80a8 Add strict expanded H017 validation runner

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

Strict runner added in the latest code phase:

    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_strict_event_real.py

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

    C:\Users\equin\Documents\institutional-ea\tests\test_h017_strict_event.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017_event.py
    C:\Users\equin\Documents\institutional-ea\tests\test_bridge_windows.py
    C:\Users\equin\Documents\institutional-ea\tests\test_fill_engine.py
    C:\Users\equin\Documents\institutional-ea\tests\test_portfolio.py
    C:\Users\equin\Documents\institutional-ea\tests\test_cost_model.py

Existing real-data scripts:

    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_real.py
    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_strict_event_real.py

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
- H017: H016 plus portfolio heat governor. Alive but not promotable before this handoff.

Important current interpretation after HANDOFF_32 diagnostics:

H017 may now have a serious expanded broker-native execution failure, but do not declare final strategy death until the event-engine pathology is handled epistemically correctly.

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

## Event-Driven Backtest Conventions

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

Loader timestamp-shape diagnostic:

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

Coverage-density diagnostic:

The expanded files have a sparse daily-like prefix from 2018 through 2021-06.

The dense M1 candidate region starts at 2021-07 for both symbols.

Do not treat 2018 through 2021-06 as dense M1 history.

H4/M1 aggregation compatibility diagnostic:

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

Cross-symbol common-window diagnostic:

Common M1 span:

    2021-07-01 21:00:00+00:00 through 2026-04-30 07:00:00+00:00

Common complete H4/M1 windows:

    common_complete_h4_m1_windows: 5476
    USDJPY_only_complete_h4_m1_windows: 225
    XAUUSD_only_complete_h4_m1_windows: 673
    first_common_complete_h4_window_utc: 2021-07-02 13:00:00+00:00
    last_common_complete_h4_window_utc: 2026-04-30 01:00:00+00:00

Missingness-by-time-bucket diagnostic:

- XAUUSD missingness is dominated by expected-looking daily breaks and closures.
- USDJPY has many tiny missing clusters.
- This is acceptable only under a strict complete-H4/M1-window rule.
- Do not assume continuous M1 availability.
- Do not impute.

## Current Source Acceptance Status

Expanded broker-native USDJPY and XAUUSD M1/H4 data is conditionally accepted for H017 validation only under strict restrictions.

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

Accepted bridge-window count:

    5476 common complete H4/M1 windows

Required bridge-window rule:

A common complete H4/M1 bridge window means:

1. USDJPY has a broker-native H4 bar at the H4 timestamp.
2. XAUUSD has a broker-native H4 bar at the same H4 timestamp.
3. For each symbol, the next H4 timestamp is exactly four hours later.
4. For each symbol, the M1 window `[H4 timestamp, H4 timestamp + 4 hours)` contains exactly 240 M1 bars.
5. No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

## HistData State

HistData remains rejected for H017 validation under current evidence.

Current statuses:

1. HistData as H017 validation source: rejected under current evidence.
2. HistData as accepted research source: not accepted.
3. HistData-built H4: not accepted.
4. Broker H4 plus HistData M1 hybrid: not accepted.
5. Derived HistData files: not authorized.
6. H017 validation on HistData: not authorized.
7. Broker-native expanded source is conditionally accepted for strict validation only.
8. H017 status must remain conservative pending fail-closed event-engine decision.

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

## Work Completed Since HANDOFF_31

### Phase 3.26-aq - Hygiene and API/design inspection

Verified hygiene:

- Branch `main`.
- Up to date with origin.
- Working tree clean.
- Full tests: 532 passed.

Observed duplicate HANDOFF_31 commits:

    756c014 Add handoff document #31 after strict H017 event wrapper
    737ec19 Add handoff document #31 after strict H017 event wrapper

Known and not blocking. Do not rewrite history.

Inspected APIs using `inspect.signature(...)` and `dataclasses.fields(...)`.

Key signatures verified:

    run_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None) -> H017Result

    backtest_h017_event_driven(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        config=None,
        starting_equity_usd=10000.0,
        slippage_atr_by_symbol=None,
    ) -> H017EventBacktestResult

    backtest_h017_event_from_result(
        *,
        h017_result,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        starting_equity_usd=10000.0,
        slippage_atr_by_symbol=None,
    ) -> H017EventBacktestResult

    backtest_h017_strict_event_driven(
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
    ) -> StrictH017EventBacktestResult

    backtest_h017_strict_event_from_result(
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
    ) -> StrictH017EventBacktestResult

    assess_common_complete_h4_m1_windows(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        expected_m1_bars_per_h4=240,
        expected_h4_delta=pd.Timedelta(hours=4),
    ) -> CommonCompleteBridgeWindowAssessment

    build_h017_claim(
        returns,
        *,
        periods_per_year=1512,
        sr_benchmark=0.0,
        confidence=0.95,
        psr_threshold=0.95,
        sr_estimates=None,
        dsr_threshold=0.95,
    ) -> H017Claim

Old script finding:

    scripts/run_h017_event_real.py

It has a UTF-8 BOM. When inspecting it with Python AST, read it using `encoding="utf-8-sig"`.

The old script is still only a smoke path. It does not enforce strict accepted bridge windows and must not be used as expanded validation.

### Phase 3.26-ar - Add strict expanded H017 validation runner

Commit:

    47f80a8 Add strict expanded H017 validation runner

File added:

    scripts/run_h017_strict_event_real.py

Compile check:

    python -m py_compile scripts\run_h017_strict_event_real.py

Full tests:

    532 passed

Purpose of new script:

1. Load four broker-native MT5 exports.
2. Use `require_existing_files(...)` before loading.
3. Use `load_mt5_csv(...)`.
4. Run `assess_common_complete_h4_m1_windows(...)`.
5. Assert:
       accepted_count == 5476
       first_accepted_timestamp == 2021-07-02 13:00:00+00:00
       last_accepted_timestamp == 2026-04-30 01:00:00+00:00
6. Preserve native H4 frames.
7. Do not filter H4 directly to accepted timestamps.
8. Pass `assessment.accepted_timestamps` to `backtest_h017_strict_event_driven(...)`.
9. Build a claim with `build_h017_claim(...)`.
10. Print loader summaries, strict bridge-window assessment, strict wrapper counts, backtest metrics, claim summary, and research verdict.
11. Write no derived datasets.
12. Do not tune H017.
13. Do not change the cost model.
14. Do not use HistData.
15. Do not approve live trading.

Important: The script was committed and pushed before the first real-data strict run, as required.

## Strict Expanded Real-Data H017 Run Result

### Phase 3.26-as - First strict expanded real-data script run

Command run:

    python scripts\run_h017_strict_event_real.py

The script successfully loaded the four real local broker-native MT5 CSVs and passed strict bridge-window preflight.

Raw MT5 export summaries printed by the script:

USDJPY H4:

    n_input_rows=8713
    n_bars=8713
    earliest_utc=2018-07-02 21:00:00+00:00
    latest_utc=2026-04-30 05:00:00+00:00
    broker_tz=Europe/Athens

XAUUSD H4:

    n_input_rows=8658
    n_bars=8658
    earliest_utc=2018-06-27 21:00:00+00:00
    latest_utc=2026-04-30 05:00:00+00:00
    broker_tz=Europe/Athens

USDJPY M1:

    n_input_rows=1785312
    n_bars=1785312
    earliest_utc=2018-07-02 21:00:00+00:00
    latest_utc=2026-04-30 07:00:00+00:00
    broker_tz=Europe/Athens

XAUUSD M1:

    n_input_rows=1704907
    n_bars=1704907
    earliest_utc=2018-06-27 21:00:00+00:00
    latest_utc=2026-04-30 07:00:00+00:00
    broker_tz=Europe/Athens

Strict bridge-window preflight printed by the script:

    expected_m1_bars_per_h4=240
    expected_h4_delta=0 days 04:00:00
    candidate_common_h4_count=8654
    usdjpy_complete_count=5685
    xauusd_complete_count=6149
    common_complete_count=5476
    accepted_count=5476
    first_accepted_timestamp=2021-07-02 13:00:00+00:00
    last_accepted_timestamp=2026-04-30 01:00:00+00:00
    usdjpy_only_complete_count=209
    xauusd_only_complete_count=673
    rejected_count=3178

Rejection counts:

    usdjpy_m1_count_not_expected: 2969
    usdjpy_missing_next_h4_timestamp: 1
    usdjpy_non_4h_next_h4_delta: 1179
    xauusd_m1_count_not_expected: 2505
    xauusd_missing_next_h4_timestamp: 1
    xauusd_non_4h_next_h4_delta: 1193

The run then crashed before producing final backtest/claim output.

Crash traceback:

    ValueError: equity_usd must be > 0.0

Crash location:

    quantcore/backtest/portfolio.py
    size_position_from_risk(...)
    _validate_positive("equity_usd", equity_usd)

Interpretation at that moment:

The strict bridge-window preflight is good. The strict expanded event backtest reached non-positive equity during execution before completing.

Do not document this as a final validation result yet without the failure-mode diagnosis below.

## Crash Localization Diagnostics Completed

### Phase 3.26-at - Read-only failure triage

Inspected event-engine and portfolio internals.

Important implementation facts:

In `quantcore/backtest/h017_event.py`, `backtest_h017_event_from_result(...)`:

1. Initializes:

       current_equity = starting_equity_usd

2. For each native H4 interval:

       decision_time = index[i - 1]
       entry_time = index[i]
       forced_exit_time = index[i + 1]
       interval_start_equity = current_equity

3. Builds fills for USDJPY and XAUUSD using the same `interval_start_equity`.

4. Adds both symbols' P&L to `current_equity` after the interval.

The crash occurred because a later interval tried to size a nonzero position with `current_equity <= 0`.

### Phase 3.26-au - Read-only strict expanded crash localization

A read-only diagnostic replayed the strict path manually and stopped around the first non-positive equity event.

Strict preflight reconfirmed:

    accepted_count=5476
    first_accepted_timestamp=2021-07-02 13:00:00+00:00
    last_accepted_timestamp=2026-04-30 01:00:00+00:00

H017 native decision index:

    decision_index_len=8654
    decision_index_first=2018-07-02 21:00:00+00:00
    decision_index_last=2026-04-30 05:00:00+00:00

Strict mask prepared:

    executed_entry_count=5476
    skipped_entry_count=3176
    first_executed_entry_time=2021-07-02 13:00:00+00:00
    last_executed_entry_time=2026-04-30 01:00:00+00:00

Equity became non-positive here:

    loop_i=943
    decision_time=2021-07-06 01:00:00+00:00
    entry_time=2021-07-06 05:00:00+00:00
    forced_exit_time=2021-07-06 09:00:00+00:00
    interval_start_equity=9847.56
    interval_pnl=-11835.26
    current_equity=-1987.71
    drawdown=-119.88%

Nonzero positions at the fatal interval:

    USDJPY: 0.01145217973850406
    XAUUSD: 0.007505335695394608

Fatal interval fills:

USDJPY:

    symbol=USDJPY
    side=buy
    entry=2021-07-06 05:00:00+00:00
    exit=2021-07-06 05:00:00+00:00
    entry_price=110.775000
    exit_price=110.765229
    lots=518.77
    pnl_usd=-11839.15
    commission=7262.78
    slippage=0.000012
    exit_reason=stop

XAUUSD:

    symbol=XAUUSD
    side=buy
    entry=2021-07-06 05:00:00+00:00
    exit=2021-07-06 09:00:00+00:00
    entry_price=1807.480000
    exit_price=1809.622000
    lots=0.02
    pnl_usd=3.88
    commission=0.40
    slippage=0.000000
    exit_reason=signal_flip

Summary before stop:

    fills_built=16
    intervals_with_fills=8
    current_equity=-1987.71
    peak_equity=10000.00
    max_drawdown=-119.88%

Important interpretation:

This is not ordinary market loss. It is a pathological USDJPY sizing event with an enormous 518.77-lot trade on a roughly \$9.8k account.

### Phase 3.26-av - Read-only pathological USDJPY stop/sizing inspection

The diagnostic inspected the exact fatal USDJPY event.

Core event facts:

    symbol=USDJPY
    decision_time=2021-07-06 01:00:00+00:00
    entry_time=2021-07-06 05:00:00+00:00
    forced_exit_time=2021-07-06 09:00:00+00:00
    interval_start_equity=9847.56
    signed_risk_fraction=0.011452179738504060
    side=buy
    entry_raw_price=110.770000000
    forced_exit_raw_price=110.651000000
    stop_price=110.770240804
    stop_distance_raw_abs=0.000240804025
    stop_minus_entry_raw=0.000240804025
    entry_raw_minus_stop=-0.000240804025

Critical fact:

For a long trade, the H017 long stop was slightly above the raw H4 entry open:

    raw_long_stop_below_raw_entry=False

This means the raw stop was directionally invalid relative to the raw entry open, but only by a tiny amount.

H017 decision row:

Positions:

    USDJPY    0.011452
    XAUUSD    0.007505

Signals:

    USDJPY    1.0
    XAUUSD    1.0

Stops long:

    USDJPY     110.770241
    XAUUSD    1774.115767

Stops short:

    USDJPY     111.298759
    XAUUSD    1785.592233

Vol multipliers:

    USDJPY    1.145218
    XAUUSD    0.750534

Heat multipliers:

    USDJPY    1.0
    XAUUSD    1.0

Heat:

    heat_pre=0.01414213562373095
    heat_post=0.01414213562373095
    heat_binding=False

USDJPY H4 bars around event:

    2021-07-05 21:00 UTC open=110.914 high=110.926 low=110.783 close=110.840
    2021-07-06 01:00 UTC open=110.840 high=110.911 low=110.743 close=110.771
    2021-07-06 05:00 UTC open=110.770 high=110.854 low=110.604 close=110.650
    2021-07-06 09:00 UTC open=110.651 high=110.798 low=110.514 close=110.654

Raw-entry sizing math used by the current event engine:

    target_risk_usd=112.776027106
    risk_per_lot_quote_raw=24.080402468
    risk_per_lot_usd_raw=0.217391013
    raw_lots_unrounded=518.770420837

Current position-size result:

    lots=518.77
    target_risk_usd=112.77602710570304
    actual_risk_usd=112.775935619535
    notional_quote=5746415290.0

Entry cost:

    fill_price=110.775000000
    spread_paid_price=0.005
    commission_usd=3631.39

Cost-adjusted distance comparison, not changing engine:

    entry_cost_fill_price=110.775000000
    stop_price=110.770240804
    cost_adjusted_stop_distance_abs=0.004759195975
    entry_cost_fill_minus_stop=0.004759195975
    risk_per_lot_quote_cost_adjusted=475.919597531
    risk_per_lot_usd_cost_adjusted=4.296272602
    cost_adjusted_lots_unrounded=26.249737282

Directional stop validity checks:

    raw_long_stop_below_raw_entry=False
    raw_long_stop_below_cost_adjusted_entry=True
    raw_stop_was_above_raw_entry_by=0.000240804025
    cost_adjusted_entry_was_above_stop_by=0.004759195975

M1 window summary:

    m1_count=240
    first_m1=2021-07-06 05:00:00+00:00
    last_m1=2021-07-06 08:59:00+00:00
    window_low_min=110.604000000
    window_high_max=110.854000000
    touch_count=125

Important interpretation:

The fatal event is not due to missing M1 bars. It occurs in a complete strict window.

The fatal event is caused by the current event engine sizing with:

    abs(raw H4 entry open - H017 stop)

before entry spread is applied.

Because the raw entry and stop are almost equal, the denominator collapses, lot size explodes, commissions explode, and equity becomes negative.

A cost-adjusted-entry distance would have produced much smaller, though still large, sizing:

    around 26.25 unrounded lots instead of 518.77 lots

However, do not immediately patch this by changing costs or tuning strategy. It needs a principled event-engine decision.

### Phase 3.26-aw - Read-only cost/slippage implementation inspection

Inspected:

    quantcore/backtest/cost_model.py
    quantcore/backtest/h017_event.py
    quantcore/backtest/fill_engine.py
    quantcore/backtest/portfolio.py

Key implementation facts:

`price_with_execution_costs(...)` signature:

    price_with_execution_costs(
        *,
        symbol,
        side,
        action,
        raw_price,
        lots,
        cost_spec=None,
        exit_reason=None,
        atr=None,
    ) -> ExecutionCost

`ExecutionCost` fields:

    symbol
    side
    action
    raw_price
    fill_price
    lots
    spread_paid_price
    slippage_price
    commission_usd

Cost model:

- Entries pay half-spread:
  - buy entry: raw + half spread
  - sell entry: raw - half spread
- Exits pay half-spread:
  - buy exit: raw - half spread
  - sell exit: raw + half spread
- Stop slippage applies only to stop exits.
- If exit reason is stop, ATR is required.
- In the current event engine, if no explicit ATR series is supplied, `_atr_for_slippage(...)` returns `stop_distance_price`.

Important current event-engine behavior in `h017_event.py`:

1. It computes:

       stop_distance_price = abs(entry_raw_price - stop_price)

2. It sizes position from that raw absolute distance.

3. It then computes entry cost and executes at cost-adjusted entry.

4. It simulates stop/forced exit.

5. It computes ATR-for-slippage using the same raw stop distance if no ATR series is supplied.

Potential issue:

The event engine does not explicitly validate directional stop placement before sizing.

For a long trade, a stop should generally be below the executable entry.
For a short trade, a stop should generally be above the executable entry.

The fatal raw event had:

    long stop above raw entry open

But after spread-adjusted entry, the stop was below executable entry.

This creates an ambiguity:

1. Sizing based on raw entry says the stop distance is almost zero and creates a huge position.
2. Sizing based on executable entry says the stop distance is larger due to spread.
3. A fail-closed validation rule might reject/skip trades whose stop is not directionally valid relative to raw entry before costs.
4. Another fail-closed rule might enforce a minimum effective stop distance or maximum leverage/notional cap.
5. Another realism correction might size from cost-adjusted entry rather than raw entry.

Do not decide silently. This needs explicit tests and documentation.

## Current H017 Status

Before strict expanded run:

- H017 was alive but not promotable.
- Old short-window event-driven smoke result was:
  - fills=470
  - ending_equity_usd=16145.60
  - total_return_pct=61.46
  - max_drawdown_pct=-33.65
  - annualized_sharpe=1.3218
  - PSR=0.8662 below threshold 0.95
  - MinTRL observed n=470 below required n=1034
  - promotable=False

After strict expanded run attempt:

- Strict preflight passes.
- Full strict expanded validation script crashes due to non-positive equity.
- Crash is localized to a pathological USDJPY event caused by near-zero raw stop distance and huge sizing.
- H017 is definitely not promotable.
- Do not approve live trading.
- Do not tune H017.
- Do not change cost model assumptions casually.
- Do not declare final validation result until event-engine failure semantics are handled.

## Existing Strict Components

### Strict bridge-window preflight

Implemented in:

    quantcore/data/bridge_windows.py

Tests:

    tests/test_bridge_windows.py

Main API:

    assess_common_complete_h4_m1_windows(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        expected_m1_bars_per_h4=240,
        expected_h4_delta=pd.Timedelta(hours=4),
    ) -> CommonCompleteBridgeWindowAssessment

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

### Strict event wrapper

Implemented in:

    quantcore/backtest/h017_strict_event.py

Tests:

    tests/test_h017_strict_event.py

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

Wrapper behavior:

1. The wrapper does not modify the existing event engine.
2. It preserves the native H4/H017 decision index.
3. It accepts either raw H4 frames and runs `run_h017(...)`, or an already-built `H017Result`.
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

## Strict Expanded Runner

Implemented in:

    scripts/run_h017_strict_event_real.py

Commit:

    47f80a8 Add strict expanded H017 validation runner

Current behavior:

1. Loads the four local broker-native MT5 raw CSVs.
2. Runs strict preflight.
3. Asserts exact expected accepted bridge-window contract.
4. Runs `backtest_h017_strict_event_driven(...)`.
5. Builds `H017Claim`.
6. Prints verdict.

Current problem:

On real expanded data, it crashes when the underlying event engine attempts to size a new position after equity has gone non-positive.

This is not yet gracefully reported by the script.

## Recommended Next Path

Next logical sub-phase:

    Phase 3.26-ax - Decide and implement fail-closed handling for pathological event-engine sizing/insolvency semantics

Do not patch blindly.

First action for the next AI after hygiene:

1. Inspect current APIs again:
   - `quantcore/backtest/h017_event.py`
   - `quantcore/backtest/h017_strict_event.py`
   - `quantcore/backtest/cost_model.py`
   - `quantcore/backtest/portfolio.py`
   - `tests/test_h017_event.py`
   - `tests/test_h017_strict_event.py`
   - `tests/test_cost_model.py`
   - `tests/test_portfolio.py`

2. Decide the most epistemically honest behavior.

Likely acceptable design direction:

A. The event engine should fail closed or terminate gracefully when equity becomes non-positive, rather than crashing later inside sizing.

B. The backtest result may need a field indicating insolvency or ruin, but adding fields will require updating tests and any users of the dataclass.

C. Alternatively, the strict runner can catch `ValueError("equity_usd must be > 0.0")` and document the validation as failed due to account ruin, but this is weaker because it does not localize result state.

D. A separate diagnostic/reporting helper could replay until ruin and print a fatal validation result without changing core event engine semantics.

E. The raw-entry stop-distance pathology should be tested with synthetic data before any behavior change.

F. Consider whether event-engine sizing should use executable entry price instead of raw H4 open. This is a realism question, not a tuning question. It must be tested and documented if changed.

G. Consider a directional stop-validity guard:
   - long trades require stop < sizing entry price,
   - short trades require stop > sizing entry price.
   But be careful: if using cost-adjusted entry, the fatal event is directionally valid; if using raw entry, it is not.

H. Consider a minimum stop distance / spread multiple guard, but this begins to look like risk-management rule design and must not be hidden as a backtest fix.

Strong recommendation:

First implement **diagnostic/fail-closed reporting**, not a strategy fix.

The next code phase should probably add synthetic tests for one or more of these cases:

1. Backtest stops and reports/raises a clear insolvency error when interval P&L drives equity <= 0.
2. A raw-entry near-zero stop distance does not produce an obscure later `equity_usd must be > 0.0` failure.
3. If adding a custom exception, tests assert the exception includes:
   - decision_time,
   - entry_time,
   - forced_exit_time,
   - start equity,
   - interval P&L,
   - ending equity,
   - symbol/fill information if feasible.

Do not run another full real-data strict validation until the failure semantics are improved and committed.

## Potential Documentation Needed After Code Decision

After fail-closed semantics are implemented and committed, run the strict expanded runner again.

Then document the outcome in `docs/operations`, likely with a new file such as:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md
    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt

But do not create those docs until the failure semantics are clear enough to produce reproducible output.

## Absolute Do-Not Rules At HANDOFF_32

Do not:

1. Do not tune H017.
2. Do not change H017 parameters.
3. Do not change the cost model casually.
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
28. Do not ignore the newly found -119.88 percent strict expanded ruin event.
29. Do not silently “fix” the 518.77-lot event by tuning.
30. Do not silently change raw versus executable entry sizing without tests and docs.
31. Do not continue development while local commits are unpushed.
32. Do not let git status go unread.
33. Do not skip full pytest.
34. Do not allow test count to drop below 532 without explicit test-removal phase.

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

Understood. I am continuing after HANDOFF_32.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is 532 passed.
3. Latest expected commit is `Add handoff document #32 after strict expanded H017 crash localization`.
4. Previous code commit is `47f80a8 Add strict expanded H017 validation runner`.
5. Expanded broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
6. The strict bridge-window preflight confirmed exactly 5476 accepted windows from `2021-07-02 13:00:00+00:00` through `2026-04-30 01:00:00+00:00`.
7. The strict event wrapper exists and preserves native H4/H017 index semantics.
8. The strict expanded runner exists at `scripts/run_h017_strict_event_real.py`.
9. The first strict expanded real-data run passed preflight but crashed with `ValueError: equity_usd must be > 0.0`.
10. Crash localization found equity became non-positive on `2021-07-06 05:00:00+00:00`.
11. The fatal interval started with about `\$9,847.56` equity and ended around `-\$1,987.71`, drawdown about `-119.88%`.
12. The immediate cause was a USDJPY long with `518.77` lots.
13. The pathological USDJPY sizing came from a near-zero raw stop distance: raw entry `110.770000000`, long stop `110.770240804`.
14. The long stop was slightly above raw entry, but below the cost-adjusted buy entry.
15. Current event-engine sizing uses `abs(raw H4 entry open - stop_price)` before entry spread.
16. This created raw unrounded lots around `518.77`, with entry commission alone around `\$3,631.39`.
17. This is not a missing-M1 problem; the fatal window had exactly 240 M1 bars.
18. Do not tune H017.
19. Do not change the cost model casually.
20. Do not use HistData.
21. Do not live trade or start Phase 4 execution.
22. The next logical sub-phase is Phase 3.26-ax: decide and implement fail-closed handling for pathological event-engine sizing/insolvency semantics.
23. First task is hygiene verification only. No new code yet.

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
