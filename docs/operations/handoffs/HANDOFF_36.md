# HANDOFF 36 - After H017 Equality Invalid-Stop Tests And Near-Zero Stop Diagnostic

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_36 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research: Python quantcore.
- Execution: MetaTrader 5 later.
- Production target: Oracle Cloud Always Free VPS later.
- Monitoring: self-hosted free-tier stack later.
- Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in `.venv`.

Do not rush into strategy validation or live trading. The project is still in research-validation infrastructure and hypothesis-governance work.

## Non-Negotiable Workflow Rules

Use:

- Windows.
- PowerShell.
- VS Code.
- Python 3.12.10.
- `.venv`.
- No WSL.
- No Linux/macOS shell assumptions.

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
17. After each response, offer exactly:

    ? done
    ?? error ? paste it
    ?? question

## Repository State At This Handoff

Repository root:

    C:\Users\equin\Documents\institutional-ea

Virtual environment:

    C:\Users\equin\Documents\institutional-ea\.venv

Branch:

    main

GitHub remote:

    https://github.com/citradinnda/institutional-ea.git

Latest expected commit before this HANDOFF_36 document is committed:

    90ad396 Document near-zero H017 stop-distance diagnostic

Expected latest commit after this handoff is committed:

    Add handoff document #36 after near-zero stop diagnostic

Recent commits at the time this handoff was written:

    90ad396 Document near-zero H017 stop-distance diagnostic
    7919e1b Document equality invalid H017 stop tests
    30fc482 Test equality invalid H017 stop geometry
    28efb04 Sync H017 docs after invalid stop guard
    d838057 Add handoff document #35 after H017 invalid stop guard
    5a53f18 Document H017 invalid stop guard implementation
    ef7f717 Fail closed on invalid H017 event stop geometry
    e854b4a Add H017 execution semantics decision record
    9bc8130 Add H017 execution semantics decision plan
    25dc5fd Add handoff document #34 after H017 failure ledger and README status

Known note:

There are duplicate consecutive HANDOFF_31 commits earlier in history. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    537 passed

Important test-count rule:

- Current correct full-test anchor is 537 passed.
- If tests pass but the count drops below 537 without a deliberate test-removal phase, treat it as a regression.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification only.

Ask the user to run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10
    pytest -q

Expected status after this handoff is committed and pushed:

- On branch main.
- Your branch is up to date with origin/main.
- Nothing to commit, working tree clean.

Expected latest commit:

    Add handoff document #36 after near-zero stop diagnostic

Expected previous commit:

    90ad396 Document near-zero H017 stop-distance diagnostic

Expected tests:

    537 passed

Read the output before continuing.

## Current Important Paths

Code:

    C:\Users\equin\Documents\institutional-ea\quantcore
    C:\Users\equin\Documents\institutional-ea\scripts
    C:\Users\equin\Documents\institutional-ea\tests

Important docs:

    C:\Users\equin\Documents\institutional-ea\README.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HYPOTHESIS_LEDGER.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EXECUTION_SEMANTICS_DECISION_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EXECUTION_SEMANTICS_DECISION_RECORD.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H017_NEAR_ZERO_STOP_DISTANCE_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_SOURCE_ACCEPTANCE_CHECKPOINT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT_OUTPUT.txt

Strict expanded runner:

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

    C:\Users\equin\Documents\institutional-ea\tests\test_h017_event.py
    C:\Users\equin\Documents\institutional-ea\tests\test_h017_strict_event.py
    C:\Users\equin\Documents\institutional-ea\tests\test_bridge_windows.py
    C:\Users\equin\Documents\institutional-ea\tests\test_fill_engine.py
    C:\Users\equin\Documents\institutional-ea\tests\test_portfolio.py
    C:\Users\equin\Documents\institutional-ea\tests\test_cost_model.py

Existing real-data scripts:

    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_real.py
    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_strict_event_real.py

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

- Do not commit raw data.
- Do not commit large derived data.
- Do not write derived data before explicit authorization.
- Do not modify raw vendor/broker files.

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

- Winter UTC+2.
- Summer UTC+3.
- DST-aware.

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

- pandas DataFrame.
- DatetimeIndex.
- index name: `dt`.
- timezone: UTC.
- columns: `open`, `high`, `low`, `close`, `volume`.

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
    first_common_complete_h4_window_utc: 2021-07-02 13:00:00+00:00
    last_common_complete_h4_window_utc: 2026-04-30 01:00:00+00:00

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

Accepted validation bridge-window range:

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
8. H017 status is failed/not promotable after strict expanded broker-native insolvency result.

Allowed HistData uses:

- Explicitly planned diagnostics only.
- Documentation.
- Source-quality comparison.
- Raw inventory metadata preservation.

Not allowed:

- H017 validation.
- Strategy tuning.
- Derived production datasets.
- Derived H4 files for H017 validation.
- Broker-H4 plus HistData-M1 hybrid validation.
- Silent deduplication.
- Raw file modification.
- Raw file commits.

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
- H017: H016 plus portfolio heat governor. H017 has failed strict expanded broker-native event validation by insolvency and is not promotable.

Current H017 interpretation:

H017 is not promotable.

The strict expanded broker-native source preflight passed, but the strategy failed event-driven validation by account insolvency on a complete strict bridge window.

Do not broaden to more symbols yet.

Do not add machine learning yet.

Do not tune H017.

Do not approve live trading.

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

Current event engine sizing behavior:

- It sizes from:

    abs(raw H4 entry open - stop_price)

- This occurs before entry spread is applied.
- Do not silently change this behavior.
- Any future raw-entry versus executable-entry sizing decision must be explicit, tested, documented, and treated as an execution-model semantics decision, not tuning.

## Raw-Entry Invalid-Stop Execution Guard

Implemented in:

    quantcore/backtest/h017_event.py

Error class:

    H017EventInvalidStopError

Under current raw-entry sizing semantics:

- Long/buy stop must be below raw H4 entry open.
- Short/sell stop must be above raw H4 entry open.
- Equality is invalid:
  - long/buy stop equal to raw H4 entry open fails closed,
  - short/sell stop equal to raw H4 entry open fails closed.

Invalid directional stop geometry fails closed.

Invalid directional stops are not skipped silently.

Invalid directional stops are not clipped.

This guard does not promote H017.

This guard does not authorize a real-data rerun.

Current focused synthetic tests are in:

    tests/test_h017_event.py

Focused H017 event test anchor:

    15 passed

Full test anchor after equality invalid-stop tests:

    537 passed

## Strict Expanded Broker-Native Validation Result

Script:

    scripts/run_h017_strict_event_real.py

The strict bridge-window preflight passed.

Strict bridge-window preflight:

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

Strict event-driven backtest result before invalid-stop guard:

    completed=False
    failure_reason=insolvency
    decision_time=2021-07-06 01:00:00+00:00
    entry_time=2021-07-06 05:00:00+00:00
    forced_exit_time=2021-07-06 09:00:00+00:00
    interval_start_equity_usd=9847.56
    interval_pnl_usd=-11835.26
    ending_equity_usd=-1987.71
    interval_return_pct=-120.18
    interval_fills=2

Fatal USDJPY fill before invalid-stop guard:

    symbol=USDJPY
    side=buy
    entry_time=2021-07-06 05:00:00+00:00
    exit_time=2021-07-06 05:00:00+00:00
    entry_price=110.775000000
    exit_price=110.765228764
    lots=518.77
    pnl_quote=-506902.42
    commission=7262.78
    slippage=0.000012040
    exit_reason=stop

Fatal XAUUSD fill before invalid-stop guard:

    symbol=XAUUSD
    side=buy
    entry_time=2021-07-06 05:00:00+00:00
    exit_time=2021-07-06 09:00:00+00:00
    entry_price=1807.480000000
    exit_price=1809.622000000
    lots=0.02
    pnl_quote=4.28
    commission=0.40
    slippage=0.000000000
    exit_reason=signal_flip

Research verdict printed by the runner before invalid-stop guard:

    STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True
    H017 STRICT EVENT BACKTEST COMPLETED: False
    H017 VALIDATION FAILED BY INSOLVENCY: True
    H017 PROMOTABLE BY CLAIM: False
    EXPANDED VALIDATION IS RESEARCH EVIDENCE ONLY: True
    LIVE TRADING APPROVED: False

Important:

Do not rerun broad strict real-data validation as a promotion attempt after the invalid-stop guard.

Any rerun must be explicitly authorized as diagnostics only.

H017 remains failed unless a separate governance phase says otherwise.

## Interpretation Of The Insolvency Result

This is not a data preflight failure.

This is not a missing-M1 problem.

The fatal interval was a complete strict bridge window.

The fatal event was caused by event-engine execution reaching account ruin after a pathological USDJPY size:

    518.77 lots

Prior diagnostics localized the sizing pathology to a near-zero raw stop distance:

    raw H4 entry open=110.770000000
    H017 long stop=110.770240804

For a long trade, that stop was slightly above the raw H4 entry open but below the cost-adjusted buy entry.

Before the invalid-stop guard, the event-engine sizing used:

    abs(raw H4 entry open - stop_price)

before entry spread was applied and without directional validation.

This collapsed the sizing denominator and caused huge lots and huge commission.

The invalid-stop guard now fails closed on this class of raw-entry directional stop geometry, but this does not erase the original H017 validation failure.

Do not silently fix this by tuning H017 or changing costs.

Any future change to raw-entry versus executable-entry sizing must be explicit, tested, and documented as an execution-model semantics decision.

## Work Completed Since HANDOFF_35

### Commit 28efb04 - Sync H017 docs after invalid stop guard

Files changed:

    docs/operations/H017_EXECUTION_SEMANTICS_DECISION_PLAN.md
    docs/operations/HYPOTHESIS_LEDGER.md

Updated:

- Synchronized older 533/535 test-anchor drift.
- Added post-plan implementation note for `H017EventInvalidStopError`.
- Added ledger note that raw-entry directional invalid stops fail closed.
- Preserved H017 failed/not-promotable status.

Full tests:

    535 passed

Commit was pushed.

### Commit 30fc482 - Test equality invalid H017 stop geometry

File changed:

    tests/test_h017_event.py

Added synthetic tests:

- `test_long_stop_equal_to_raw_entry_fails_closed`
- `test_short_stop_equal_to_raw_entry_fails_closed`

Confirmed equality semantics:

- Long/buy stop equal to raw H4 entry open fails closed.
- Short/sell stop equal to raw H4 entry open fails closed.

Focused tests:

    15 passed

Full tests:

    537 passed

Commit was pushed.

### Commit 7919e1b - Document equality invalid H017 stop tests

Files changed:

    README.md
    docs/operations/H017_EXECUTION_SEMANTICS_DECISION_PLAN.md
    docs/operations/H017_EXECUTION_SEMANTICS_DECISION_RECORD.md
    docs/operations/HYPOTHESIS_LEDGER.md

Updated:

- README full-test anchor to 537 passed.
- Decision plan full-test anchor to 537 passed.
- Decision record implemented-tests list to include equality invalid-stop tests.
- Hypothesis ledger to state equality is invalid under current raw-entry semantics.

Full tests:

    537 passed

Commit was pushed.

### Commit 90ad396 - Document near-zero H017 stop-distance diagnostic

Files added:

    docs/operations/H017_NEAR_ZERO_STOP_DISTANCE_DIAGNOSTIC.md

Files changed:

    docs/operations/H017_EXECUTION_SEMANTICS_DECISION_RECORD.md

Documented:

- Zero and negative stop distances are rejected.
- Any positive stop distance is currently accepted.
- Positive near-zero stop distances can still create extreme lots and extreme notional exposure.
- No minimum stop-distance guard has been chosen.
- No maximum notional/leverage guard has been chosen.
- No H017 promotion is implied.
- No real-data rerun is authorized.

Full tests:

    537 passed

Commit was pushed.

## Near-Zero Stop-Distance Diagnostic Summary

Read-only diagnostic used:

    quantcore.backtest.portfolio.size_position_from_risk

Current sizing API:

    size_position_from_risk(
        *,
        symbol: str,
        signed_risk_fraction: float,
        equity_usd: float,
        entry_price: float,
        stop_distance_price: float,
        instrument_spec: InstrumentSpec | None = None,
    ) -> PositionSize

Current behavior:

1. `stop_distance_price` must be greater than zero.
2. There is no minimum stop-distance threshold beyond positive.
3. There is no maximum notional guard.
4. There is no maximum leverage guard.
5. Lot size is rounded down to the broker lot step.
6. If rounded size is below minimum lot, zero lots are returned.

Diagnostic examples:

XAUUSD normal 10.0 USD stop:

    lots=0.100000
    notional_quote_div_equity_usd=2.000000

XAUUSD small 0.01 USD stop:

    lots=100.000000
    notional_quote_div_equity_usd=2000.000000

XAUUSD near-zero 0.0001 USD stop:

    lots=10000.000000
    notional_quote_div_equity_usd=200000.000000

USDJPY normal 1.0 JPY stop:

    lots=0.150000
    notional_quote_div_equity_usd=225.000000

USDJPY fatal-geometry-sized raw distance from H017 insolvency diagnostic:

    stop_distance_price=0.000240804
    lots=452.980000
    notional_quote=5017659460.000000
    notional_quote_div_equity_usd=509533.271186

Zero and negative checks:

    stop_distance_price=0.0 -> ValueError: stop_distance_price must be > 0.0
    stop_distance_price=-0.01 -> ValueError: stop_distance_price must be > 0.0

Interpretation:

The current sizing API correctly rejects zero and negative stop distances, but positive near-zero stop distances can still create extreme exposure.

This is an execution-semantics and account-risk governance issue.

Do not patch it silently.

## Current H017 Status

H017 is:

    failed / not promotable

Live trading is:

    not approved

Phase 4 execution is:

    not approved

Source acceptance is:

    broker-native data conditionally accepted under strict complete-window rules

Strategy validation status is:

    failed by strict expanded broker-native event-driven insolvency

Execution semantics status:

    raw-entry directional invalid-stop guard implemented and tested

Equality invalid-stop status:

    implemented and tested

Near-zero positive stop-distance status:

    documented as open execution-semantics/account-risk issue

Remaining open execution-semantics questions:

1. Should future sizing use raw H4 entry open or executable entry price after spread?
2. Should a long stop be required below raw entry, executable entry, or both?
3. Should a short stop be required above raw entry, executable entry, or both?
4. Should there be a minimum stop distance relative to spread, ATR, tick size, broker point, or all-in friction?
5. Should there be a maximum leverage/notional guard?
6. Are such guards execution-realism constraints, account-risk constraints, strategy rules, or broker-margin approximations?
7. If a guard skips or clips trades, does that require H018?
8. Should any semantics change retire H017 and open H018?

## Recommended Next Path

Next logical sub-phase after HANDOFF_36 hygiene:

    Phase 3.26-bt - H018 boundary decision plan

Recommended priority:

Open an H018 boundary decision plan before implementing any more execution-semantics changes.

Reason:

The remaining issues are linked:

1. Minimum stop-distance guard.
2. Maximum notional/leverage guard.
3. Executable-entry sizing.
4. Trade skip/clip/fail-closed policy.

All of them can materially change trade eligibility, realized exposure, or validation outcome.

Therefore, the safest next work package is a documentation-only H018 boundary plan that states:

- H017 remains failed.
- H017 is not repaired by execution-semantics changes.
- Any trade-skipping or clipping likely requires H018.
- Any executable-entry sizing adoption likely requires H018.
- Any minimum stop-distance filter likely requires H018.
- Any maximum notional/leverage clipping likely requires H018.
- Synthetic tests must precede any real-data run.
- Any future real-data run under altered semantics is diagnostic or H018 validation, not H017 promotion.

After that, decide and document these as subordinate plans:

1. Minimum stop-distance decision plan.
2. Maximum notional/leverage decision plan.
3. Executable-entry sizing decision plan.

Do not start by changing H017 parameters.

Do not start by changing event-engine code.

Do not start by rerunning broad real-data validation.

## Potential Future Technical Questions

Future work may need to decide explicitly:

1. Should event-engine sizing use raw H4 entry open or executable entry price after spread?
2. Should the selected sizing reference be raw, executable, or a named separate reference?
3. Should invalid directional stops fail closed, skip, or become new strategy rules?
4. Should same-price stops remain invalid? Current guard treats equality as invalid:
   - long invalid if stop >= raw entry,
   - short invalid if stop <= raw entry.
5. Should near-zero but directionally valid stop distances fail closed?
6. Should minimum stop distance be a multiple of spread, ATR, tick size, broker point, or all-in friction?
7. Should maximum leverage/notional be applied in event-engine research validation?
8. If a guard skips or clips trades, is that a strategy change and therefore H018?
9. Should any future real-data run after semantics changes be diagnostic-only?
10. How should the original H017 insolvency remain visible after fail-closed invalid-stop behavior changes the failure mode?
11. Should H018 inherit H017 alpha logic but change execution semantics?
12. Should H018 be defined as a new hypothesis before any code changes?
13. Should an H018 claim require strict bridge-window preflight plus event validation plus explicit account-exposure guards?

Treat these as epistemic design decisions, not quick patches.

## Absolute Do-Not Rules At HANDOFF_36

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
24. Do not ignore the accepted timestamp gaps found in the contiguity diagnostic.
25. Do not treat source acceptance as H017 promotion.
26. Do not treat future validation as live-trading approval.
27. Do not ignore the previous -33.65 percent drawdown.
28. Do not ignore the strict expanded insolvency event.
29. Do not silently fix the 518.77-lot event by tuning.
30. Do not silently change raw versus executable entry sizing without tests and docs.
31. Do not continue development while local commits are unpushed.
32. Do not let git status go unread.
33. Do not skip full pytest.
34. Do not allow test count to drop below 537 without explicit test-removal phase.
35. Do not call the raw-entry invalid-stop guard H017 promotion.
36. Do not call equality invalid-stop tests H017 promotion.
37. Do not call near-zero stop-distance documentation H017 promotion.
38. Do not rerun broad strict validation after the invalid-stop guard unless explicitly authorized as diagnostics only.
39. Do not introduce trade skipping or clipping without opening the H018 boundary question.
40. Do not implement minimum stop-distance guard before a decision plan.
41. Do not implement maximum notional/leverage guard before a decision plan.
42. Do not implement executable-entry sizing before a decision plan.
43. Do not treat positive near-zero stop-distance behavior as solved.

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
15. When two identical code blocks exist in one file, use function-boundary replacement, not first global text match.
16. Long pasted PowerShell blocks can be corrupted by chat formatting; prefer shorter here-string writes and verify with previews.
17. `tests/test_h017_event.py` has a UTF-8 BOM; when programmatically editing it, use `utf-8-sig`.
18. A previous documentation sync appeared to fail in terminal output but had actually committed; when output is inconsistent, immediately perform read-only verification before proceeding.
19. Network/DNS push failures can happen; stop development until `git push` succeeds.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after HANDOFF_36.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is 537 passed.
3. Latest expected commit is `Add handoff document #36 after near-zero stop diagnostic`.
4. Previous commit is `90ad396 Document near-zero H017 stop-distance diagnostic`.
5. H017 remains failed / not promotable / not live-approved.
6. Live trading is not approved.
7. Phase 4 execution work is not approved.
8. Broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
9. The strict expanded broker-native validation originally failed by insolvency after a pathological 518.77-lot USDJPY trade.
10. `H017EventInvalidStopError` is implemented.
11. Under current raw-entry sizing semantics, long/buy stops must be below raw H4 entry open and short/sell stops must be above raw H4 entry open.
12. Equality is invalid and directly tested.
13. Invalid directional stop geometry fails closed.
14. Invalid stops are not skipped silently and are not clipped.
15. This guard does not promote H017.
16. This guard does not authorize a real-data rerun.
17. Near-zero positive stop-distance behavior is documented as an open execution-semantics/account-risk issue.
18. Minimum stop-distance guard remains undecided.
19. Maximum notional/leverage guard remains undecided.
20. Executable-entry sizing remains undecided.
21. Do not tune H017.
22. Do not use HistData.
23. Do not broaden symbols or add ML.
24. Do not start Phase 4.
25. Recommended next logical sub-phase is Phase 3.26-bt: H018 boundary decision plan.
26. First task is hygiene verification only. No new code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10
    pytest -q

Then paste the full output.
