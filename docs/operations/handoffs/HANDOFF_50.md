# HANDOFF 50 - After H018 Invalid Stop Panel Diagnostic

If any older handoff conflicts with this file, this HANDOFF_50 wins.

This handoff is intentionally self-contained enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

The user is intelligent but not a professional developer. They are building infrastructure-first because previous strategy attempts failed due to weak validation, fictional backtesting, poor cost modeling, and poor risk control.

Target environment:

- Research: Python package `quantcore`.
- Execution target later: MetaTrader 5 expert advisor.
- Production target later: Oracle Cloud Always Free VPS.
- Monitoring later: self-hosted free-tier stack.
- Current machine: Windows.
- Shell: PowerShell.
- Editor: VS Code.
- Python: 3.12.10 inside `.venv`.
- No WSL.

Repository root:

- `C:\Users\equin\Documents\institutional-ea`

Virtual environment:

- `C:\Users\equin\Documents\institutional-ea\.venv`

Branch:

- `main`

GitHub remote:

- `https://github.com/citradinnda/institutional-ea.git`

Handoff folder:

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs`

This handoff path:

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_50.md`

## Important Human Preference

The user is tired of excessive documentation and slow ceremony.

Going forward:

- Do not document every tiny change.
- Do not create governance docs unless they prevent real confusion, record a real decision, preserve a handoff, or protect against future ambiguity.
- Do not create subphases inside subphases.
- Do one real action at a time.
- Keep responses practical and concise.
- Prefer direct engineering actions over process theater.
- For docs-only changes, do not run full pytest unless there is a clear reason.
- For docs-only changes, basic checks are enough:
  - `git status`
  - `git diff --check`
  - `git diff --stat`
  - optional preview with `Get-Content` or `Select-String`
  - commit
  - push
  - `git status`
  - `git ls-files` for touched docs
- For code changes, tests are mandatory.
- For code changes touching strategy, event engine, sizing, accounting, data loading, or validation logic:
  - run focused tests if applicable,
  - run full `python -m pytest -q`,
  - compare test count to current anchor,
  - commit,
  - push.

Current full-test anchor after latest code commit:

- `575 passed`

If code tests pass but the count drops below `575` without an explicit test-removal phase, treat it as a regression.

Do not continue development while local commits are unpushed.

Always read `git status` before starting a new phase.

## Non-Negotiable Environment Rules

Use:

- Windows.
- PowerShell.
- VS Code.
- Python 3.12.10.
- `.venv`.
- No WSL.

PowerShell rule:

Do not use Linux/macOS heredoc syntax like:

- `python - <<'PY'`

PowerShell does not support that.

Use PowerShell here-strings only when truly necessary. For long docs, prefer VS Code manual editing.

## Practical Workflow Rules

General rules:

1. Start each phase with `git status`.
2. Do one sub-phase at a time.
3. Use explicit Windows paths.
4. Use plain English.
5. Define technical terms inline when needed.
6. Never write code without saying exactly where the file goes and how to run it.
7. Never continue while local commits are unpushed.
8. Always commit and push completed work.
9. Always verify touched files are tracked with `git ls-files` after commit.
10. Do not run real-data validation unless explicitly authorized.
11. Do not start Phase 4 execution unless explicitly authorized.
12. Do not live trade.

Testing rules:

- Docs-only edit:
  - No full pytest required by default.
  - Use `git diff --check` and `git diff --stat`.
- Code edit:
  - Run focused tests when applicable.
  - Run full `python -m pytest -q`.
  - Current full-test anchor: `575 passed`.
- If full tests pass but count drops below `575` without planned test removal, stop and treat as regression.

Git rules:

Before changes:

- `git status`

After changes:

- `git diff --check`
- `git diff --stat`
- `git add touched files`
- `git commit`
- `git push`
- `git status`
- `git ls-files touched files`

## Repository State At This Handoff

Latest pushed code commit before this handoff document:

- `6a52328 Extend H018 invalid stop panel diagnostics`

Expected handoff commit message after this file is committed:

- `Add handoff document #50 after invalid stop panel diagnostics`

Recent commits expected before this handoff commit:

- `6a52328 Extend H018 invalid stop panel diagnostics`
- `966812c Add handoff document #49 after invalid stop diagnostics`
- `4486205 Add handoff document #49 after invalid stop diagnostics`
- `11b27df Add H018 invalid stop cause diagnostic`
- `51d6042 Add H018 guard violation diagnostic scanner`
- `33e4fff Add handoff document #48 after friction diagnostic calculator`
- `adb5fab Add diagnostic projected friction calculator`
- `cbaa70e Add handoff document #47 after H018 governance sync`
- `daaa2b6 Sync H018 portfolio leverage guard governance docs`
- `7be5a45 Add handoff document #46 after H018 portfolio leverage guard`

Note:

- There are two consecutive handoff #49 commits: `966812c` and `4486205`.
- This is not blocking because the tree is clean and pushed.

Current full-test anchor:

- `575 passed`

Last full pytest result before this handoff:

- `575 passed in 17.23s`

Focused test result before this handoff:

- `tests/test_h018_invalid_stop_cause.py`: `4 passed in 1.89s`

No code changed after those tests except this docs-only handoff file if it is being created.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Expected after this handoff is committed and pushed:

- On branch `main`.
- Branch up to date with `origin/main`.
- Nothing to commit, working tree clean.
- Latest commit should be `Add handoff document #50 after invalid stop panel diagnostics`.
- Previous commit should be `6a52328 Extend H018 invalid stop panel diagnostics`.

Do not require pytest for this first check unless code has changed or status is not clean.

## Important Paths

Code:

- `C:\Users\equin\Documents\institutional-ea\quantcore`
- `C:\Users\equin\Documents\institutional-ea\scripts`
- `C:\Users\equin\Documents\institutional-ea\tests`

Strategy files likely relevant next:

- `C:\Users\equin\Documents\institutional-ea\quantcore\strategy\h017.py`
- `C:\Users\equin\Documents\institutional-ea\quantcore\strategy\signals.py`
- `C:\Users\equin\Documents\institutional-ea\quantcore\strategy\heat_governor.py`

Indicator file relevant to the current issue:

- `C:\Users\equin\Documents\institutional-ea\quantcore\indicators\chandelier.py`

Event engine:

- `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_event.py`

Strict event bridge layer:

- `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_strict_event.py`

Portfolio sizing/accounting:

- `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\portfolio.py`

Cost model:

- `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\cost_model.py`

Diagnostic friction calculator:

- `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\friction.py`

H018 guard scanner:

- `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h018_guard_scan.py`
- `C:\Users\equin\Documents\institutional-ea\scripts\scan_h018_guard_violations_real.py`
- `C:\Users\equin\Documents\institutional-ea\tests\test_h018_guard_scan.py`

H018 invalid-stop cause/panel diagnostic:

- `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h018_invalid_stop_cause.py`
- `C:\Users\equin\Documents\institutional-ea\scripts\diagnose_h018_invalid_stop_causes_real.py`
- `C:\Users\equin\Documents\institutional-ea\tests\test_h018_invalid_stop_cause.py`

Strict real-data script:

- `C:\Users\equin\Documents\institutional-ea\scripts\run_h017_strict_event_real.py`

Important docs:

- `README.md`
- `docs/operations/H018_DECISION_RECORD_INDEX.md`
- `docs/operations/H018_DECISION_MATRIX.md`
- `docs/operations/H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md`
- `docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md`
- `docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md`
- `docs/operations/H018_SIZING_REFERENCE_DECISION_RECORD.md`
- `docs/operations/H018_PORTFOLIO_GROSS_LEVERAGE_DECISION_RECORD.md`
- `docs/operations/handoffs/HANDOFF_50.md`

## Gitignore / Raw Data Rules

The repo uses root-anchored:

- `/data/`

Do not change it to unanchored:

- `data/`

Reason:

An unanchored `data/` rule previously risked excluding:

- `quantcore/data/`

Raw data under root `/data/` is gitignored and must not be committed.

Do not commit:

- raw MT5 CSV files,
- raw HistData files,
- large derived datasets,
- broker/vendor source files.

Do not modify raw broker files.

## Broker / Data State

Broker:

- Exness

Account environment:

- Demo

Server:

- MT5

Broker timezone used by loader:

- `Europe/Athens`

Meaning:

- Winter UTC+2.
- Summer UTC+3.
- DST-aware.

MT5 loader signature:

- `load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult`

Expanded broker-native raw exports exist locally and are gitignored:

- `data\raw\USDJPY\H4.csv`
- `data\raw\USDJPY\M1.csv`
- `data\raw\XAUUSD\H4.csv`
- `data\raw\XAUUSD\M1.csv`

Reported exact MT5 symbols:

- `USDJPYm`
- `XAUUSDm`

Do not commit these raw files.

## Source Acceptance Status

Expanded broker-native USDJPY and XAUUSD M1/H4 data is conditionally accepted for H017/H018-style strict validation only under strict complete-window restrictions.

Accepted source:

- Exness demo MT5 broker-native exports.

Accepted symbols:

- USDJPY
- XAUUSD

Accepted timeframes:

- Broker-native H4.
- Broker-native M1.

Accepted validation bridge-window range:

- First possible common complete H4/M1 bridge window UTC: `2021-07-02 13:00:00+00:00`
- Last possible common complete H4/M1 bridge window UTC: `2026-04-30 01:00:00+00:00`

Accepted bridge-window count:

- `5476` common complete H4/M1 windows

A common complete H4/M1 bridge window means:

- USDJPY has a broker-native H4 bar at the H4 timestamp.
- XAUUSD has a broker-native H4 bar at the same H4 timestamp.
- For each symbol, the next H4 timestamp is exactly four hours later.
- For each symbol, the M1 window has exactly 240 M1 bars.
- No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

Do not treat 2018 through 2021-06 as dense M1 history. The expanded files have a sparse daily-like prefix before the dense M1 candidate region, which starts at 2021-07 for both symbols.

HistData remains rejected for H017/H018 validation under current evidence.

Do not use HistData for:

- H017 validation,
- H018 validation,
- tuning,
- production dataset creation.

## Strategy / Validation Background

The project uses strict hypothesis discipline because prior strategies failed.

Immutable strategy graveyard summary:

- H001: Backtests without intrabar SL/TP simulation are fiction. Must use M1 inside H4 bars to resolve fills.
- H002-H003: ATR-based per-symbol stops mandatory; trade frequency must amortize costs.
- H004a: Single-seed models unreliable; use multi-seed ensembles if ML ever returns.
- H005: Stacked multi-symbol models fail on heterogeneous instruments; use per-symbol models if ML ever returns.
- H006-H007: Confidence filters are not risk management. ML chooses entries; deterministic rules manage risk.
- H008-H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals cannot be risk manager.
- H011-H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk ceiling remained.
- H014-H016: USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1 percent per-trade risk was not 1 percent portfolio risk when trades overlapped. Drawdown breach was -19.43 percent.
- H015: Diversification into negative-edge instruments destroys the portfolio.
- H017: H016 plus portfolio heat governor. H017 failed strict expanded broker-native event validation by insolvency before guards and now fails closed under H018-style guards.

Current H017 verdict:

- H017 is failed.
- H017 is not promotable.
- H017 is not live-approved.
- Do not tune H017 casually.
- Do not broaden symbols.
- Do not add ML.
- Do not approve live trading.

## Core Strategy Conventions

ATR:

- Wilder RMA, not SMA.
- First true range is high - low.
- Seed at index window - 1 with simple mean of first window true ranges.
- Recurrence: `ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n`

Chandelier Exit:

- Long: `highest_high(lookback) - multiplier * ATR`
- Short: `lowest_low(lookback) + multiplier * ATR`

Current implementation detail:

- `quantcore/indicators/chandelier.py` rolling windows include the current bar.
- H017 computes raw long and short Chandelier panels independently.
- These raw panels are not currently stateful protective trailing stops bound to an active trade lifecycle.

Defaults:

- multiplier = `3.0`
- lookback = `22`

Vol Target:

- Realized vol at bar t uses returns through t-1 only.
- No lookahead.
- H4 periods per year = `1512`

Signals:

- Donchian breakout.
- Long: `close[t] > max(high[t-N ... t-1])`
- Short: `close[t] < min(low[t-N ... t-1])`
- Channel uses prior N bars via `shift(1).rolling(N)`.

Signal semantics:

- Signal is desired direction, not a trade list.
- Between breakouts, the most recent direction is held.
- Opposite breakout flips direction.
- Initial post-warmup state before first breakout is flat.

H017:

- Inner-joins USDJPY and XAUUSD timestamps.
- Computes close-to-close returns.
- Uses same returns for vol targeting and heat governor.
- Position is signed risk exposure:
  - `signal * per_trade_risk * vol_mult * heat_mult`
- Therefore H017 position side is currently exactly the held signal sign unless vol/heat zero it.

Heat governor:

- Combined heat: `sqrt(w' (r^2 * C) w)`

Defaults:

- cap = `0.015`
- per_trade_risk = `0.01`
- correlation_window = `120`
- correlation_floor = `0.0`

## Event-Driven Backtest Conventions

Fill rule:

- If stop and take-profit are both touched in the same M1 bar, stop wins.

Reason:

- M1 OHLC does not reveal tick order inside the minute, so stop-first is conservative.

Cost model defaults:

USDJPY:

- spread_price = `0.01`
- commission_usd_per_lot_per_fill = `7.0`
- stop_slippage_atr_fraction = `0.05`

XAUUSD:

- spread_price = `0.30`
- commission_usd_per_lot_per_fill = `10.0`
- stop_slippage_atr_fraction = `0.05`

Commission is per fill. A round trip charges entry and exit.

Portfolio P&L:

- XAUUSD P&L is already USD.
- USDJPY P&L is JPY and must be divided by USDJPY conversion price to become USD.

Event bridge timing:

- H017 decides at H4 timestamp t.
- Trade opens on next H4 bar open t+1.
- M1 bars inside the next H4 window resolve stops.
- If no stop is hit, exposure closes at following H4 open as `signal_flip`.
- This is a bridge-layer simplification.

Current event engine sizing behavior:

- It sizes from absolute difference between raw H4 entry open and stop price.
- This occurs before entry spread is applied.
- Do not silently change this behavior.

Event stop selection:

- `signed_risk_fraction > 0` maps to side `buy`.
- `signed_risk_fraction < 0` maps to side `sell`.
- Buy uses `h017_result.stops_long`.
- Sell uses `h017_result.stops_short`.
- Directional guard requires:
  - buy stop below raw entry open.
  - sell stop above raw entry open.

## Portfolio API

`InstrumentSpec` dataclass fields:

- symbol
- contract_size
- quote_currency
- lot_step
- min_lot

`PositionSize` dataclass fields:

- symbol
- side
- signed_risk_fraction
- lots
- target_risk_usd
- actual_risk_usd
- notional_quote

`size_position_from_risk` signature:

- `size_position_from_risk(*, symbol: str, signed_risk_fraction: float, equity_usd: float, entry_price: float, stop_distance_price: float, instrument_spec: InstrumentSpec | None = None) -> PositionSize`

Current behavior:

- `equity_usd` must be positive.
- `entry_price` must be positive.
- `stop_distance_price` must be positive.
- `target_risk_usd = abs(signed_risk_fraction) * equity_usd`.
- `risk_per_lot_quote = stop_distance_price * contract_size`.
- risk per lot is converted through `quote_pnl_to_usd`.
- raw lots are rounded down to broker `lot_step`.
- if rounded lots are below `min_lot`, zero lots are returned.
- `actual_risk_usd = lots * risk_per_lot_usd`.
- `notional_quote = lots * contract_size * entry_price`.

Default instrument specs:

USDJPY:

- contract_size = `100000.0`
- quote_currency = `JPY`
- lot_step = `0.01`
- min_lot = `0.01`

XAUUSD:

- contract_size = `100.0`
- quote_currency = `USD`
- lot_step = `0.01`
- min_lot = `0.01`

`quote_pnl_to_usd` convention:

- XAUUSD quote currency is USD, so quote P&L is already USD.
- USDJPY quote currency is JPY, so JPY P&L divided by USDJPY price converts to USD.

## Implemented Guards

### Raw-Entry Invalid-Stop Guard

Implemented in:

- `quantcore/backtest/h017_event.py`

Error class:

- `H017EventInvalidStopError`

Rule:

- Long/buy stop must be below raw H4 entry open.
- Short/sell stop must be above raw H4 entry open.
- Equality is invalid.
- Invalid directional stop geometry fails closed.
- Invalid stops are not skipped or clipped.

This does not promote H017 or validate H018.

### H018 Minimum Stop-Distance Guard

Implemented in:

- `quantcore/backtest/h017_event.py`

Error class:

- `H018MinimumStopDistanceError`

Rule:

- `raw_stop_distance = abs(raw_h4_entry_open - stop_price)`

Minimum stop distance is one modeled spread for the symbol.

Thresholds:

- USDJPY: `0.01`
- XAUUSD: `0.30`

Boundary:

- below threshold fails closed.
- equality passes.
- above threshold passes.

### H018 Maximum Per-Trade USD Gross Leverage Guard

Implemented in:

- `quantcore/backtest/h017_event.py`

Error class:

- `H018MaximumPerTradeLeverageError`

Constant:

- `_MAXIMUM_PER_TRADE_USD_GROSS_LEVERAGE = 10.0`

Rule:

- A single trade may not create more than 10 times account equity in USD-converted gross notional exposure.

Measurement:

- `gross_leverage = notional_usd / equity_usd`

Boundary:

- `< 10.0` passes.
- `== 10.0` passes.
- `> 10.0` fails closed.

### H018 Portfolio-Wide USD Gross Leverage Guard

Implemented in:

- `quantcore/backtest/h017_event.py`

Error class:

- `H018MaximumPortfolioGrossLeverageError`

Constant:

- `_MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE = 10.0`

Rule:

- At a single event interval, the total USD-converted gross notional exposure opened by all symbols may not exceed 10 times account equity.

Gross exposure is summed using absolute notional exposure.

Long and short exposures are not netted.

Boundary:

- `< 10.0` passes.
- `== 10.0` passes.
- `> 10.0` fails closed.

Violation policy:

- Raise explicit error.
- Do not silently skip any trade.
- Do not clip any position size.
- Do not net long and short notionals.
- Do not warn and continue.
- Do not log-only continue.
- Do not convert the run into a promotable validation result.

## Current H018 Governance Status

H018 is not validated.

H018 is not promotable.

H018 does not approve live trading.

H018 does not approve Phase 4 execution.

Accepted and implemented H018-related code so far:

- `H017EventInvalidStopError`
- raw-entry directional stop validation
- `H018MinimumStopDistanceError`
- `_validate_minimum_stop_distance`
- `H018MaximumPerTradeLeverageError`
- `_position_notional_usd`
- `_validate_maximum_per_trade_usd_gross_leverage`
- `H018MaximumPortfolioGrossLeverageError`
- `_SymbolIntervalCandidate`
- `_validate_maximum_portfolio_usd_gross_leverage`
- diagnostic projected friction calculator
- H018 guard violation diagnostic scanner
- H018 invalid-stop cause diagnostic
- H018 invalid-stop panel diagnostic extension

Still not chosen:

- No formal H018 claim.
- No broker margin model.
- No friction-burden cap threshold.
- No diagnostic-only continuation mode integrated into event backtest.
- No approved fix for invalid stop/position mismatch.
- No approved strategy semantic change.

Still not authorized:

- No live trading.
- No Phase 4 execution.

## Latest Real Validation And Diagnostic Results

### 1. Strict H018 Broker-Native Validation Was Explicitly Authorized And Run

The user explicitly authorized:

- `Authorized: run strict H018 broker-native validation.`

Command used:

- `python .\scripts\run_h017_strict_event_real.py`

Preflight passed exactly:

- `expected_m1_bars_per_h4=240`
- `expected_h4_delta=0 days 04:00:00`
- `candidate_common_h4_count=8654`
- `usdjpy_complete_count=5685`
- `xauusd_complete_count=6149`
- `common_complete_count=5476`
- `accepted_count=5476`
- `first_accepted_timestamp=2021-07-02 13:00:00+00:00`
- `last_accepted_timestamp=2026-04-30 01:00:00+00:00`
- `usdjpy_only_complete_count=209`
- `xauusd_only_complete_count=673`
- `rejected_count=3178`

Validation failed closed with:

- `H017EventInvalidStopError`

First failure:

- symbol: `XAUUSD`
- side: `sell`
- decision_time: `2021-07-05 17:00:00+00:00`
- entry_time: `2021-07-05 21:00:00+00:00`
- entry_raw_price: `1791.212000000`
- stop_price: `1786.180536020`

For a sell trade, stop must be above entry. It was below entry.

Classification:

- This is not a data-preflight failure.
- This is not an infrastructure failure.
- This is a strategy/event validation failure.
- H018 is not validated.
- H018 is not promotable.
- No live trading.
- No Phase 4.

### 2. H018 Guard Violation Diagnostic Scanner

Commit:

- `51d6042 Add H018 guard violation diagnostic scanner`

Files:

- `quantcore/backtest/h018_guard_scan.py`
- `scripts/scan_h018_guard_violations_real.py`
- `tests/test_h018_guard_scan.py`

Purpose:

- diagnostic-only scan across accepted strict windows
- counts guard failures without pretending validation passed
- does not execute fills for promotion
- does not tune, skip, clip, resize, or approve anything

Focused test result:

- `5 passed in 1.80s`

Full test result after this code:

- `571 passed in 13.13s`

Real diagnostic command:

- `python .\scripts\scan_h018_guard_violations_real.py`

Real diagnostic result:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=10952`
- `candidate_count=8275`
- `skipped_intent_count=560`
- `violation_count=2271`

Violation breakdown:

- `invalid_directional_stop`: `1545`
- `maximum_per_trade_usd_gross_leverage`: `527`
- `minimum_stop_distance`: `45`
- `maximum_portfolio_usd_gross_leverage`: `154`

By symbol:

- `XAUUSD`: `874`
- `USDJPY`: `1243`

Interpretation:

- The issue is structural, not isolated.
- H017/H018 current form is invalid under strict event execution.
- The largest category is invalid directional stops.

### 3. H018 Invalid-Stop Cause Diagnostic

Commit:

- `11b27df Add H018 invalid stop cause diagnostic`

Files:

- `quantcore/backtest/h018_invalid_stop_cause.py`
- `scripts/diagnose_h018_invalid_stop_causes_real.py`
- `tests/test_h018_invalid_stop_cause.py`

Purpose:

Determine whether invalid stops are caused by:

1. stop valid at decision close but crossed by next executable entry open, or
2. stop already invalid at decision close.

Focused test result:

- `4 passed in 2.14s`

Full test result after this code:

- `575 passed in 12.94s`

Real diagnostic command:

- `python .\scripts\diagnose_h018_invalid_stop_causes_real.py`

Real diagnostic result before panel extension:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=10952`
- `invalid_at_entry_count=1545`

Cause breakdown:

- `already_invalid_at_decision_close`: `1544`
- `crossed_between_decision_close_and_entry_open`: `1`

By symbol:

- `XAUUSD`: `726`
- `USDJPY`: `819`

By side:

- `sell`: `788`
- `buy`: `757`

Interpretation:

- The invalid-stop problem is not mainly next-open gap/crossing.
- Almost all invalid stops were already on the wrong side at decision close itself.

### 4. H018 Invalid-Stop Panel Diagnostic Extension

Commit:

- `6a52328 Extend H018 invalid stop panel diagnostics`

Files:

- `quantcore/backtest/h018_invalid_stop_cause.py`
- `scripts/diagnose_h018_invalid_stop_causes_real.py`
- `tests/test_h018_invalid_stop_cause.py`

Purpose:

Extend invalid-stop observations with:

- `signed_risk_fraction`
- optional `signal_value`
- `selected_stop_panel`
- `long_stop_price`
- `short_stop_price`
- `long_stop_valid_at_decision_close`
- `short_stop_valid_at_decision_close`
- `stop_panel_diagnostic`

Focused test result:

- `4 passed in 1.89s`

Full test result:

- `575 passed in 17.23s`

Real diagnostic command:

- `python .\scripts\diagnose_h018_invalid_stop_causes_real.py`

Real diagnostic result after panel extension:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=10952`
- `invalid_at_entry_count=1545`

Cause counts:

- `already_invalid_at_decision_close`: `1544`
- `crossed_between_decision_close_and_entry_open`: `1`

By symbol:

- `XAUUSD`: `726`
- `USDJPY`: `819`

By side:

- `sell`: `788`
- `buy`: `757`

Stop-panel diagnostic counts:

- `selected_panel_nonprotective_opposite_panel_protective`: `1425`
- `selected_panel_protective_at_decision_close`: `1`
- `selected_panel_nonprotective_both_panels_nonprotective`: `119`

Important interpretation:

- The key line is the panel diagnostic count.
- 1425 out of 1545 invalid stops are cases where the selected same-side raw Chandelier panel was non-protective at decision close, while the opposite panel was protective under its own side-specific definition.
- This does not mean switching stop panels is approved.
- For a buy, “opposite panel protective” means the short panel is valid for a short, not for the current buy.
- Switching panels would likely invert trade semantics, not fix them.
- The evidence supports a stale-held-signal / state mismatch hypothesis:
  - Donchian signal holds a side until opposite breakout.
  - Raw same-side Chandelier stop can be breached before opposite breakout.
  - H017 still emits the held side as desired exposure.
  - The event engine then tries to open a new bracket trade for that side using a stop already on the wrong side.
  - The guard correctly fails closed.

First invalid observation after panel extension:

- `cause=already_invalid_at_decision_close`
- `symbol=XAUUSD`
- `side=sell`
- `decision_time=2021-07-05 17:00:00+00:00`
- `entry_time=2021-07-05 21:00:00+00:00`
- `decision_close=1791.224`
- `entry_open=1791.212`
- `stop_price=1786.1805360200765`
- `selected_stop_panel=stops_short`
- `long_stop_price=1759.4234639799236`
- `short_stop_price=1786.1805360200765`
- `long_stop_valid_at_decision_close=True`
- `short_stop_valid_at_decision_close=False`
- `stop_panel_diagnostic=selected_panel_nonprotective_opposite_panel_protective`
- `decision_margin=-5.043463979923445`
- `entry_margin=-5.031463979923501`

## Current Diagnostic Scripts

Guard scanner:

- `python .\scripts\scan_h018_guard_violations_real.py`

Invalid-stop cause and panel diagnostic:

- `python .\scripts\diagnose_h018_invalid_stop_causes_real.py`

Strict validation script:

- `python .\scripts\run_h017_strict_event_real.py`

Do not rerun strict validation as a promotion attempt. It is known to fail closed under current code and strategy state.

## Current Diagnosis Of The Strategy/Stop Problem

Confirmed from read-only inspection:

`quantcore/strategy/h017.py`:

- `positions = signals * per_trade_risk * vol_mult * heat_mult`
- Position side is exactly signal sign unless vol/heat zero it.
- `stops_long` and `stops_short` are raw Chandelier panels computed independently.

`quantcore/strategy/signals.py`:

- Donchian signal is held between breakouts.
- It is desired direction, not a trade list.
- It does not flatten when a Chandelier stop would be hit.

`quantcore/indicators/chandelier.py`:

- Long stop panel:
  - rolling highest high including current bar minus multiplier times ATR.
- Short stop panel:
  - rolling lowest low including current bar plus multiplier times ATR.
- These are raw indicator bands, not active-position stateful trailing stop lifecycle objects.

`quantcore/backtest/h017_event.py`:

- Event engine selects stop panel from signed position side:
  - buy uses `stops_long`
  - sell uses `stops_short`
- It then requires valid protective geometry at next H4 raw entry open.

Current best diagnosis:

- H017 emits persistent desired exposure from held Donchian signal.
- Same-side raw Chandelier stop can become non-protective before opposite Donchian breakout.
- Event engine requires every nonzero interval exposure to be representable as a valid bracket trade.
- Therefore the strategy output and strict event semantics are mismatched.
- The guard is correct.
- The strategy/stop lifecycle semantics are underdefined or inconsistent.

## Recommended Next Action

Do not fix yet.

Do not tune parameters.

Do not switch stop panels.

Next useful diagnostic:

Build a small diagnostic/state check that counts how often H017 is holding a signal after its same-side Chandelier stop is breached at decision close.

Suggested purpose:

- Directly prove how often the held signal is stale relative to same-side protective stop semantics.
- Count by symbol and side:
  - total nonzero held-signal observations
  - same-side stop valid at decision close
  - same-side stop breached/non-protective at decision close
  - flat/warmup/NaN skipped
- Optionally split:
  - at fresh signal-change bar
  - held continuation after prior same-side signal
  - bars after first breach until opposite breakout
- This should remain diagnostic-only.

Suggested files if implemented:

- `quantcore/backtest/h018_stop_state_diagnostic.py`
- `scripts/diagnose_h018_stop_state_real.py`
- `tests/test_h018_stop_state_diagnostic.py`

Do not name this validation.

Do not promote H018 based on it.

Potential strategic decisions after diagnostic evidence:

1. Treat Chandelier as a true stateful exit:
   - If long and close/low breaches long stop, strategy becomes flat until fresh Donchian long/short trigger.
   - If short and close/high breaches short stop, strategy becomes flat until fresh Donchian trigger.
   - Requires explicit design, tests, and new hypothesis identity. It may no longer be H017 as originally tested.

2. Treat Donchian held exposure as continuous trend exposure and define a separate always-valid protective stop:
   - Requires new protective-stop construction and new sizing semantics.
   - Must not be silently patched into H017.

3. Reject H017/H018 current line:
   - Current evidence is already enough to say the present strategy/execution contract is invalid.

## Important Interpretation Guardrail

The new evidence does not mean “fix the guard.”

The guard is doing its job.

The current evidence says the strategy state/stop state is inconsistent with event-valid protective-stop semantics.

Do not solve this by:

- removing the guard,
- skipping invalid trades,
- clipping invalid trades,
- changing raw-entry sizing silently,
- switching to the opposite stop panel,
- changing costs,
- tuning parameters,
- broadening symbols,
- adding ML,
- treating diagnostics as validation.

First understand and decide the stop/position lifecycle.

## Absolute Do-Not Rules

Do not:

- Do not tune H017 casually.
- Do not change H017 parameters as a quick fix.
- Do not switch selected stop panels as a quick fix.
- Do not change cost model casually.
- Do not add ML.
- Do not broaden to more symbols.
- Do not start Phase 4 execution.
- Do not live trade.
- Do not use HistData for H017 or H018 validation.
- Do not combine broker H4 with HistData M1.
- Do not use sparse 2018 through 2021-06 broker-native prefix as dense M1.
- Do not include incomplete H4/M1 windows.
- Do not impute M1 bars.
- Do not forward-fill or backfill M1 bars.
- Do not synthesize bars.
- Do not modify raw broker files.
- Do not commit raw MT5 CSV files.
- Do not change `.gitignore` from `/data/` to `data/`.
- Do not run old `scripts/run_h017_event_real.py` as expanded validation.
- Do not treat source acceptance as H017 promotion.
- Do not treat future validation as live-trading approval.
- Do not silently fix the 518.77-lot event by tuning.
- Do not silently change raw versus executable entry sizing.
- Do not continue development while local commits are unpushed.
- Do not let `git status` go unread.
- Do not allow code-test count to drop below `575` without explicit test-removal phase.
- Do not call implemented guards H018 validation.
- Do not call diagnostic scanner results H018 validation.
- Do not choose broker margin or friction-burden thresholds casually.
- Do not implement anything from `H018_DECISION_RECORD_TEMPLATE.md`; it is a template only.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

- `.gitignore` once had unrooted `data/`, which risked excluding `quantcore/data`.
- Some older commits missed files because `git add` was incomplete.
- An empty `HANDOFF_16.md` was accidentally committed once; verify handoff file size and preview before committing.
- A mistaken empty root-level `HANDOFF_43.md` was created during HANDOFF_43 and was not to be committed.
- Markdown code fences have been damaged by paste before; avoid nested markdown fences in command blocks.
- PowerShell does not support Linux heredocs.
- VS Code can keep unsaved buffers that overwrite edits.
- If terminal output shows command echo ambiguity, verify with `Select-String` or file previews before proceeding.
- Always inspect `git status`.
- Always push commits.
- Always verify `git ls-files` after commits.
- Treat code test-count drops as regressions.
- If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.
- If `git commit` says nothing to commit, immediately run recovery status/log/ls-files checks before continuing.
- Network/DNS push failures can happen; stop development until `git push` succeeds.
- For very long handoffs, use VS Code manual editing instead of a huge PowerShell here-string.
- A broad text replacement once accidentally inserted `H018MaximumPortfolioGrossLeverageError` into existing per-trade `pytest.raises` calls. Focused tests caught it.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. Continuing after HANDOFF_50.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Current branch should be `main`.
- Latest expected commit should be `Add handoff document #50 after invalid stop panel diagnostics`.
- Previous expected commit should be `6a52328 Extend H018 invalid stop panel diagnostics`.
- Current full-test anchor is `575 passed`.
- H017 remains failed / not promotable / not live-approved.
- H018 remains not validated / not promotable / not live-approved.
- Live trading is not approved.
- Phase 4 execution work is not approved.
- Broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
- HistData is rejected for H017/H018 validation.
- Implemented guards are working; the strategy is failing them.
- Invalid-stop cause diagnostic found 1544 of 1545 invalid stops were already invalid at decision close.
- Invalid-stop panel diagnostic found 1425 of 1545 invalid stops had selected same-side panel non-protective while the opposite panel was protective under its own side definition.
- This does not approve switching panels.
- Current best diagnosis is a stale-held-signal / stop lifecycle mismatch.
- Next recommended task is a diagnostic-only stop-state check counting how often H017 holds a signal after same-side Chandelier stop is breached.
- No code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Then paste the full output.

After hygiene passes, I will proceed with the smallest diagnostic-only next step.