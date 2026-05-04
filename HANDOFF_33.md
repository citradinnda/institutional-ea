# HANDOFF 33 - Self-Contained Continuation After Strict Expanded H017 Insolvency Result

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_33 wins.

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

Latest expected commit before this HANDOFF_33 document is committed:

    83269f5 Document strict expanded H017 insolvency result

Expected latest commit after this handoff is committed:

    Add handoff document #33 after strict expanded H017 insolvency result

Recent commits at the time this handoff was written:

    83269f5 Document strict expanded H017 insolvency result
    e2c9283 Catch strict H017 insolvency in console main
    9853c6a Report strict H017 insolvency validation failure
    247af24 Fail closed on H017 event backtest insolvency
    a5c3e93 Add handoff document #32 after strict expanded H017 crash localization
    47f80a8 Add strict expanded H017 validation runner
    756c014 Add handoff document #31 after strict H017 event wrapper
    737ec19 Add handoff document #31 after strict H017 event wrapper
    06de306 Add strict H017 event wrapper

Known note:

There are duplicate consecutive HANDOFF_31 commits. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    533 passed

Important test-count rule:

- Current correct full-test anchor is 533 passed.
- If tests pass but the count drops below 533 without a deliberate test-removal phase, treat it as a regression.

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

    Add handoff document #33 after strict expanded H017 insolvency result

Expected previous commit:

    83269f5 Document strict expanded H017 insolvency result

Expected tests:

    533 passed

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

Strict expanded runner:

    C:\Users\equin\Documents\institutional-ea\scripts\run_h017_strict_event_real.py

New strict insolvency result docs:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt

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
- H017: H016 plus portfolio heat governor. It has now failed strict expanded broker-native event validation by insolvency and is not promotable.

Current H017 interpretation after this handoff:

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

## Work Completed Since HANDOFF_32

### Phase 3.26-ax - Fail-closed handling for pathological event-engine insolvency semantics

Initial hygiene after HANDOFF_32:

- Branch `main`.
- Up to date with origin.
- Working tree clean.
- Full tests: 532 passed.
- Latest handoff commit verified:
    a5c3e93 Add handoff document #32 after strict expanded H017 crash localization

Read-only inspections confirmed:

- `H017EventBacktestResult` had no insolvency fields.
- `backtest_h017_event_from_result(...)` updated `current_equity` interval by interval.
- It only failed later when the next nonzero trade tried to size using `equity_usd <= 0`.
- The previous real-data crash was therefore an unclear later failure rather than a clear ruin report.

#### Commit 247af24 - Fail closed on H017 event backtest insolvency

Files changed:

    quantcore/backtest/h017_event.py
    tests/test_h017_event.py

Added:

    H017EventInsolvencyError

The exception is raised immediately when an H017 event interval drives account equity non-positive.

It stores:

    decision_time
    entry_time
    forced_exit_time
    interval_start_equity_usd
    interval_pnl_usd
    ending_equity_usd
    interval_fills

Synthetic test added:

    test_interval_ruin_raises_clear_insolvency_error

Focused event tests:

    11 passed

Full tests after this commit:

    533 passed

Important interpretation:

This did not change H017, costs, sizing, or strategy behavior. It only changed failure semantics from a later generic positive-equity error to an immediate fail-closed insolvency error.

#### Commit 9853c6a - Report strict H017 insolvency validation failure

File changed:

    scripts/run_h017_strict_event_real.py

Added a console reporting helper for `H017EventInsolvencyError`:

    _print_insolvency_failure(...)

The helper prints:

- completed=False
- failure_reason=insolvency
- decision_time
- entry_time
- forced_exit_time
- interval_start_equity_usd
- interval_pnl_usd
- ending_equity_usd
- interval_return_pct
- interval fill details
- fail-closed research verdict

Full tests:

    533 passed

#### Commit e2c9283 - Catch strict H017 insolvency in console main

File changed:

    scripts/run_h017_strict_event_real.py

A first patch inserted the catch in `run_validation()` but not `main()`. Running the real-data script still produced a traceback.

Then a targeted function-boundary patch moved the console `try/except` to `main()` and restored `run_validation()` as a programmatic API that raises normally.

Full tests:

    533 passed

#### Strict expanded real-data rerun after console catch

Command:

    python scripts\run_h017_strict_event_real.py

Result:

- No Python traceback.
- Strict bridge-window preflight passed.
- Backtest reported completed=False.
- Failure reason was insolvency.
- Script exit code was 1.
- Git status remained clean.

Exact output was saved to:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt

#### Commit 83269f5 - Document strict expanded H017 insolvency result

Files added:

    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md
    docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt

Full tests:

    533 passed

Final status after commit:

- Branch `main`.
- Up to date with origin.
- Working tree clean.

## Strict Expanded Broker-Native Validation Result

Script:

    scripts/run_h017_strict_event_real.py

The strict bridge-window preflight passed.

Raw MT5 export summaries:

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

Rejection counts:

    usdjpy_m1_count_not_expected: 2969
    usdjpy_missing_next_h4_timestamp: 1
    usdjpy_non_4h_next_h4_delta: 1179
    xauusd_m1_count_not_expected: 2505
    xauusd_missing_next_h4_timestamp: 1
    xauusd_non_4h_next_h4_delta: 1193

Strict event-driven backtest result:

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

Fatal USDJPY fill:

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

Fatal XAUUSD fill:

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

Research verdict printed by the runner:

    STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True
    H017 STRICT EVENT BACKTEST COMPLETED: False
    H017 VALIDATION FAILED BY INSOLVENCY: True
    H017 PROMOTABLE BY CLAIM: False
    EXPANDED VALIDATION IS RESEARCH EVIDENCE ONLY: True
    LIVE TRADING APPROVED: False

Script exit code:

    1

## Interpretation Of The Insolvency Result

This is not a data preflight failure.

This is not a missing-M1 problem.

The fatal interval was a complete strict bridge window.

The fatal event is caused by event-engine execution reaching account ruin after a pathological USDJPY size:

    518.77 lots

Prior diagnostics localized the sizing pathology to a near-zero raw stop distance:

    raw H4 entry open=110.770000000
    H017 long stop=110.770240804

For a long trade, that stop was slightly above the raw H4 entry open but below the cost-adjusted buy entry.

Current event-engine sizing uses:

    abs(raw H4 entry open - stop_price)

before entry spread is applied.

This collapsed the sizing denominator and caused huge lots and huge commission.

Do not silently "fix" this by tuning H017 or changing costs.

Any future change to raw-entry versus executable-entry sizing must be explicit, tested, and documented as an execution-model semantics decision.

## Current H017 Status

H017 is:

    not promotable

Live trading is:

    not approved

Phase 4 execution is:

    not approved

Source acceptance is:

    broker-native data conditionally accepted under strict complete-window rules

Strategy validation status is:

    failed by strict expanded broker-native event-driven insolvency

## Recommended Next Path

Next logical sub-phase after HANDOFF_33 hygiene:

    Phase 3.26-ba - Decide next epistemic response to strict expanded H017 insolvency

Do not write code first.

Recommended order:

1. Reconfirm hygiene:
   - git status
   - git log --oneline -15
   - pytest -q

2. Read the new docs:
   - docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md
   - docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt

3. Decide whether the next work is:
   - documentation of H017 failure in a hypothesis ledger,
   - event-engine semantics research around raw-entry versus executable-entry sizing,
   - explicit synthetic tests for directionally invalid stops,
   - explicit synthetic tests for cost-adjusted sizing alternatives,
   - or a new H018 hypothesis that treats this as a H017 failure.

Strong recommendation:

Do not start by changing H017 parameters.

Do not call a sizing semantics change "a fix" until it has tests and documentation.

Do not rerun broad real-data validation as if the strategy is alive/promotable.

## Potential Future Technical Questions

Future work may need to decide explicitly:

1. Should event-engine sizing use raw H4 entry open or executable entry price after spread?
2. Should a long stop be required to be below raw entry, executable entry, or both?
3. Should a short stop be required to be above raw entry, executable entry, or both?
4. Should there be a minimum stop distance relative to spread?
5. Should there be an explicit maximum leverage/notional guard?
6. Are those guards execution-realism constraints or strategy risk-management rules?
7. If a guard skips trades, is that a strategy change and therefore a new hypothesis?

Treat these as epistemic design decisions, not quick patches.

## Absolute Do-Not Rules At HANDOFF_33

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
29. Do not silently "fix" the 518.77-lot event by tuning.
30. Do not silently change raw versus executable entry sizing without tests and docs.
31. Do not continue development while local commits are unpushed.
32. Do not let git status go unread.
33. Do not skip full pytest.
34. Do not allow test count to drop below 533 without explicit test-removal phase.

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

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after HANDOFF_33.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is 533 passed.
3. Latest expected commit is `Add handoff document #33 after strict expanded H017 insolvency result`.
4. Previous commit is `83269f5 Document strict expanded H017 insolvency result`.
5. Expanded broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
6. The strict bridge-window preflight confirmed exactly 5476 accepted windows from `2021-07-02 13:00:00+00:00` through `2026-04-30 01:00:00+00:00`.
7. The strict event wrapper exists and preserves native H4/H017 index semantics.
8. The strict expanded runner exists at `scripts/run_h017_strict_event_real.py`.
9. The event engine now has fail-closed `H017EventInsolvencyError` semantics.
10. The strict expanded runner now reports insolvency cleanly from `main()` without a traceback.
11. The strict expanded real-data run failed by insolvency with script exit code 1.
12. Fatal interval: decision `2021-07-06 01:00:00+00:00`, entry `2021-07-06 05:00:00+00:00`, forced exit `2021-07-06 09:00:00+00:00`.
13. Fatal interval started with about `\$9,847.56` and ended around `-\$1,987.71`.
14. Fatal USDJPY fill was `518.77` lots.
15. This was not a missing-M1 issue; the fatal interval was a complete strict bridge window.
16. H017 is not promotable.
17. Live trading is not approved.
18. Do not tune H017.
19. Do not change cost model or sizing semantics casually.
20. Do not use HistData.
21. Next logical sub-phase is Phase 3.26-ba: decide next epistemic response to strict expanded H017 insolvency.
22. First task is hygiene verification only. No new code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -15
    pytest -q

Then paste the full output.
