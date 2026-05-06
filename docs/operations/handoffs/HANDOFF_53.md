# HANDOFF 53 - After H020 Sizing Intent Contract Seed

If any older handoff conflicts with this file, this HANDOFF_53 wins.

This handoff is intentionally self-contained enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

The user is intelligent but not a professional developer. They are building infrastructure-first because previous strategy attempts failed due to weak validation, fictional backtesting, poor cost modeling, and poor risk control.

Current project stage:

- Research/backtest infrastructure.
- Strategy hypothesis work.
- No execution approval.
- No live trading approval.
- No Phase 4 approval.

Target environment:

- Research: Python package `quantcore`
- Execution target later: MetaTrader 5 expert advisor
- Production target later: Oracle Cloud Always Free VPS
- Monitoring later: self-hosted free-tier stack

Current machine:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 inside `.venv`
- No WSL

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

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_53.md`

## Important Human Preference

The user is tired of excessive documentation and slow ceremony.

Going forward:

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do not create governance docs unless they preserve a real decision, preserve a handoff, prevent real ambiguity, or protect against future confusion.
- Do not create subphases inside subphases.
- Do one real action at a time.
- Prefer direct engineering actions over process theater.
- For docs-only changes, do not run full pytest unless there is a clear reason.
- For docs-only changes, basic checks are enough:
  - `git status`
  - `git diff --check`
  - `git diff --stat`
  - optional preview
  - commit
  - push
  - `git status`
  - `git ls-files` for touched docs
- For code changes, tests are mandatory.
- For code changes touching strategy, event engine, sizing, accounting, data loading, validation, or diagnostics:
  - run focused tests if applicable
  - run full `python -m pytest -q`
  - compare test count to current anchor
  - commit
  - push

Current full-test anchor after H020 sizing-intent code:

- `600 passed`

If code tests pass but the count drops below `600` without an explicit test-removal phase, treat it as a regression.

Do not continue development while local commits are unpushed.

Always read `git status` before starting a new phase.

## Non-Negotiable Environment Rules

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
- No WSL

PowerShell rule:

Do not use Linux/macOS heredoc syntax like:

- `python - <<'PY'`

PowerShell does not support that.

Use PowerShell here-strings only when useful. For long docs, VS Code manual editing is acceptable.

## Practical Workflow Rules

General rules:

1. Start each phase with `git status`.
2. Do one real action at a time.
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
  - Current full-test anchor: `600 passed`.
- If full tests pass but count drops below `600` without planned test removal, stop and treat as regression.

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

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Expected after this handoff is committed and pushed:

- On branch `main`
- Branch up to date with `origin/main`
- Nothing to commit, working tree clean
- Latest commit should be `Add handoff document #53 after H020 sizing intent`
- Previous important commit should be `Add H020 sizing intent contract`

Do not require pytest for this first check unless code has changed or status is not clean.

## Recent Expected Commits

Recent expected commits should include, newest first:

- `Add handoff document #53 after H020 sizing intent`
- `Add H020 sizing intent contract`
- `Fix H020 sizing contract formatting`
- `Lock H020 sizing contract`
- `Record H019 guard severity diagnostics`
- `Add guard diagnostic severity fields`
- `Record H019 guard diagnostic for H020`
- `Add H019 guard diagnostic scanner`
- `Expand handoff document #52 after H019 failure`
- `Document H019 failure and seed H020`
- `Add H019 strict real-data runner`
- `Add H019 strict event routing`
- `Add H019 portfolio integration`
- `Add H019 stateful chandelier lifecycle`

## Current Test Anchor

Latest full test result after H020 sizing-intent code:

- `600 passed in 13.31s`

Focused H020 tests:

- `8 passed in 1.57s`

Earlier full-test anchors:

- before H020 sizing-intent: `592 passed`
- before H019/H020 diagnostic additions: `588 passed`

Current anchor going forward:

- `600 passed`

If full test count drops below `600` without explicit test-removal intent, stop.

## Important Paths

Code:

- `C:\Users\equin\Documents\institutional-ea\quantcore`
- `C:\Users\equin\Documents\institutional-ea\scripts`
- `C:\Users\equin\Documents\institutional-ea\tests`

Strategy files:

- `quantcore\strategy\h017.py`
- `quantcore\strategy\h019.py`
- `quantcore\strategy\h020.py`
- `quantcore\strategy\signals.py`
- `quantcore\strategy\heat_governor.py`

Indicator file:

- `quantcore\indicators\chandelier.py`

Event engine:

- `quantcore\backtest\h017_event.py`

Strict event bridge layer:

- `quantcore\backtest\h017_strict_event.py`
- `quantcore\backtest\h019_strict_event.py`

Portfolio sizing/accounting:

- `quantcore\backtest\portfolio.py`

Cost model:

- `quantcore\backtest\cost_model.py`

H018 guard scanner:

- `quantcore\backtest\h018_guard_scan.py`
- `scripts\scan_h018_guard_violations_real.py`
- `tests\test_h018_guard_scan.py`

H019/H020 diagnostic scanner:

- `scripts\scan_h019_guard_violations_real.py`
- `tests\test_h019_guard_scan_real_script.py`

H019 files:

- `quantcore\strategy\h019.py`
- `quantcore\backtest\h019_strict_event.py`
- `scripts\run_h019_strict_event_real.py`
- `tests\test_h019.py`
- `tests\test_h019_strict_event.py`
- `tests\test_h019_strict_event_real_script.py`

H020 files:

- `quantcore\strategy\h020.py`
- `tests\test_h020.py`

Important docs:

- `README.md`
- `docs\operations\H019_GRAVEYARD_RECORD.md`
- `docs\operations\H020_HYPOTHESIS_SEED.md`
- `docs\operations\handoffs\HANDOFF_53.md`

## Gitignore And Raw Data Rules

The repo uses root-anchored:

- `/data/`

Do not change it to unanchored:

- `data/`

Reason:

An unanchored `data/` rule previously risked excluding:

- `quantcore/data/`

Raw data under root `/data/` is gitignored and must not be committed.

Do not commit:

- raw MT5 CSV files
- raw HistData files
- large derived datasets
- broker/vendor source files

Do not modify raw broker files.

## Broker And Data State

Broker:

- Exness

Account environment:

- Demo

Server:

- MT5

Broker timezone used by loader:

- `Europe/Athens`

Meaning:

- Winter UTC+2
- Summer UTC+3
- DST-aware

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

Expanded broker-native USDJPY and XAUUSD M1/H4 data is conditionally accepted for strict validation only under strict complete-window restrictions.

Accepted source:

- Exness demo MT5 broker-native exports

Accepted symbols:

- USDJPY
- XAUUSD

Accepted timeframes:

- Broker-native H4
- Broker-native M1

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

HistData remains rejected for H017/H018/H019/H020 validation under current evidence.

Do not use HistData for:

- H017 validation
- H018 validation
- H019 validation
- H020 validation
- tuning
- production dataset creation

Do not combine broker H4 with HistData M1.

## Strategy Graveyard Summary

Immutable strategy graveyard summary:

- H001: Backtests without intrabar SL/TP simulation are fiction. Must use M1 inside H4 bars to resolve fills.
- H002-H003: ATR-based per-symbol stops mandatory; trade frequency must amortize costs.
- H004a: Single-seed models unreliable; use multi-seed ensembles if ML ever returns.
- H005: Stacked multi-symbol models fail on heterogeneous instruments; use per-symbol models if ML ever returns.
- H006-H007: Confidence filters are not risk management. ML chooses entries; deterministic rules manage risk.
- H008-H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals cannot be risk manager.
- H011-H013: Deterministic ATR stops + Chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk ceiling remained.
- H014-H016: USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1 percent per-trade risk was not 1 percent portfolio risk when trades overlapped. Drawdown breach was -19.43 percent.
- H015: Diversification into negative-edge instruments destroys the portfolio.
- H017: H016 plus portfolio heat governor. H017 failed strict expanded broker-native event validation by insolvency before guards, then failed closed under H018-style guards.
- H018: Guard and diagnostic work revealed structural strategy/execution mismatch. H018 was not a validated strategy.
- H019: Stateful Donchian/Chandelier lifecycle fixed stale-stop first blocker but failed closed on H018 per-trade leverage guard. H019 is in the graveyard.
- H020: New sizing-contract hypothesis. Partially implemented as standalone interval sizing intent. Not validated.

Current verdicts:

- H017 failed.
- H018 not validated.
- H019 failed.
- H020 partially implemented but not validated.
- No strategy is currently promotable.
- No live trading is approved.
- Phase 4 execution is not approved.

## Core Strategy Conventions

ATR:

- Wilder RMA, not SMA.
- First true range is high - low.
- Seed at index window - 1 with simple mean of first window true ranges.
- Recurrence:
  - `ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n`

Chandelier Exit:

- Long: `highest_high(lookback) - multiplier * ATR`
- Short: `lowest_low(lookback) + multiplier * ATR`

Current implementation detail:

- `quantcore/indicators/chandelier.py` rolling windows include the current bar.

Defaults:

- Chandelier multiplier = `3.0`
- Chandelier lookback = `22`

Vol Target:

- Realized vol at bar t uses returns through t-1 only.
- No lookahead.
- H4 periods per year = `1512`

Donchian Signals:

- Long: `close[t] > max(high[t-N ... t-1])`
- Short: `close[t] < min(low[t-N ... t-1])`
- Channel uses prior N bars via `shift(1).rolling(N)`.
- Original H017 signal semantics:
  - Signal is desired direction, not a trade list.
  - Between breakouts, most recent direction is held.
  - Opposite breakout flips direction.
  - Initial post-warmup state before first breakout is flat.

H019 changed how held signals are interpreted:

- Donchian held signal is used to detect entry/flip side changes.
- Chandelier stop breach can flatten the active lifecycle state.
- Stale held direction does not re-enter after stop-out.

Heat governor:

- Combined heat:
  - `sqrt(w' (r^2 * C) w)`

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

- Strategy decides at H4 timestamp t.
- Trade opens on next H4 bar open t+1.
- M1 bars inside the next H4 window resolve stops.
- If no stop is hit, exposure closes at following H4 open as `signal_flip`.
- This is a bridge-layer simplification.

Current event engine sizing behavior:

- It sizes from absolute difference between raw H4 entry open and stop price.
- This occurs before entry spread is applied.
- Do not silently change this behavior.

Event stop selection:

- signed risk fraction > 0 maps to side `buy`.
- signed risk fraction < 0 maps to side `sell`.
- Buy uses `stops_long`.
- Sell uses `stops_short`.
- Directional guard requires:
  - buy stop below raw entry open
  - sell stop above raw entry open

## Portfolio API And Sizing Facts

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

USD gross notional convention currently used by event guard:

- XAUUSD: lots * contract_size * price
- USDJPY: lots * contract_size
  - Because a standard USDJPY lot is 100,000 USD base notional.

## Implemented H018 Guards

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

- below threshold fails closed
- equality passes
- above threshold passes

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

- `< 10.0` passes
- `== 10.0` passes
- `> 10.0` fails closed

### H018 Portfolio-Wide USD Gross Leverage Guard

Implemented in:

- `quantcore/backtest/h017_event.py`

Error class:

- `H018MaximumPortfolioGrossLeverageError`

Constant:

- `_MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE = 10.0`

Rule:

- At a single event interval, total USD-converted gross notional exposure opened by all symbols may not exceed 10 times account equity.

Gross exposure is summed using absolute notional exposure.

Long and short exposures are not netted.

Boundary:

- `< 10.0` passes
- `== 10.0` passes
- `> 10.0` fails closed

Violation policy:

- Raise explicit error.
- Do not silently skip any trade.
- Do not clip any position size.
- Do not net long and short notionals.
- Do not warn and continue.
- Do not log-only continue.
- Do not convert the run into a promotable validation result.

## H017 And H018 Diagnostic Status

H017 verdict:

- H017 failed.
- H017 is not promotable.
- H017 is not live-approved.
- Do not tune H017 casually.
- Do not broaden symbols.
- Do not add ML.
- Do not approve live trading.

H018 verdict:

- H018 is not validated.
- H018 is not promotable.
- H018 is not live-approved.
- H018 guard and diagnostic work revealed structural strategy/execution mismatch.
- H018 should not be patched casually.

Strict H018 broker-native validation was explicitly authorized earlier and run.

Command:

- `python .\scripts\run_h017_strict_event_real.py`

Preflight passed with accepted_count `5476`.

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

- Not a data-preflight failure.
- Not an infrastructure failure.
- Strategy/event validation failure.
- H018 not validated.
- H018 not promotable.
- No live trading.
- No Phase 4.

## H018 Guard Violation Diagnostic Scanner

Files:

- `quantcore/backtest/h018_guard_scan.py`
- `scripts/scan_h018_guard_violations_real.py`
- `tests/test_h018_guard_scan.py`

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

- The issue was structural, not isolated.
- The largest category was invalid directional stops.

## H018 Stop-State Diagnostic

Files:

- `quantcore/backtest/h018_stop_state_diagnostic.py`
- `scripts/diagnose_h018_stop_state_real.py`
- `tests/test_h018_stop_state_diagnostic.py`

Real diagnostic command:

- `python .\scripts\diagnose_h018_stop_state_real.py`

Real diagnostic result:

- `accepted_entry_count=5476`
- `skipped_entry_count=1984`
- `event_interval_count=7460`
- `total_nonzero_signal_count=10952`
- `flat_signal_skipped_count=0`
- `nan_signal_skipped_count=0`
- `unavailable_price_or_stop_skipped_count=0`
- `same_side_stop_valid_at_decision_close_count=9408`
- `same_side_stop_breached_at_decision_close_count=1544`
- `fresh_signal_count=233`
- `held_continuation_count=10719`
- `breached_fresh_signal_count=1`
- `breached_held_continuation_count=1543`

Important interpretation:

- `1544` same-side stops were breached/non-protective at decision close.
- `1543` of those were held continuations.
- Only `1` was a fresh signal.
- This strongly supported stale-held-signal / stop-lifecycle mismatch.
- It did not validate H018.
- It did not approve switching panels.
- It did not approve live trading.

## H019 Design And Implementation

H019 was created to address the stale-held-signal / stop-lifecycle mismatch.

H019 identity:

- Donchian entry/flip trigger.
- Same-side Chandelier lifecycle exit.
- Flat state after same-side stop breach.
- No re-entry from stale held Donchian direction.
- No opposite-panel switching.
- H018 guards remain strict.

H019 implemented files:

- `quantcore/strategy/h019.py`
- `quantcore/backtest/h019_strict_event.py`
- `scripts/run_h019_strict_event_real.py`
- `tests/test_h019.py`
- `tests/test_h019_strict_event.py`
- `tests/test_h019_strict_event_real_script.py`

H019 commits included:

- `Add H019 stateful chandelier lifecycle`
- `Add H019 portfolio integration`
- `Add H019 strict event routing`
- `Add H019 strict real-data runner`

### H019 State Machine

Function:

- `apply_h019_chandelier_lifecycle(...)`

Input:

- held Donchian signal in `{-1, 0, +1, NaN}`
- H4 close
- same-symbol long Chandelier stop panel
- same-symbol short Chandelier stop panel

Output:

- lifecycle `signals`
- `selected_stops`
- `entries`
- `exits`

Semantics:

- NaN signal is warm-up/flat for state transitions.
- Entry only when observed Donchian side changes into nonzero:
  - `0 -> +1`
  - `0 -> -1`
  - `-1 -> +1`
  - `+1 -> -1`
- Long exits when:
  - `close <= long_stop`
- Short exits when:
  - `close >= short_stop`
- Exit is same-side only.
- After stop-out, held same-direction signal does not re-enter.
- Re-entry requires a fresh visible Donchian side change.
- No opposite-panel rescue.

### H019 Portfolio Integration

Function:

- `run_h019(...)`

Implementation:

- Calls `run_h017(...)` to reuse:
  - ATR
  - raw same-side Chandelier panels
  - Donchian held signals
  - vol-target multipliers
  - heat config
- Applies H019 lifecycle to each symbol.
- Recomputes heat governor using H019 lifecycle signals, not stale H017 signals.
- Recomputes positions:
  - `h019_signal * per_trade_risk * vol_multiplier * h019_heat_multiplier`
- Returns `H017Result` shape for bridge compatibility.

Reason for returning `H017Result` shape:

- Existing strict event bridge and guards already consume `positions`, `stops_long`, `stops_short`, and related panels.
- H019 routing must not weaken or bypass H018 guards.

### H019 Strict Event Routing

File:

- `quantcore/backtest/h019_strict_event.py`

Functions:

- `backtest_h019_strict_event(...)`
- `backtest_h019_strict_event_from_result(...)`

Implementation:

- `backtest_h019_strict_event(...)` calls `run_h019(...)`.
- Then routes the H019 result through `backtest_h017_strict_event_from_result(...)`.
- Existing H018 guards remain in the reused event bridge.
- No guard is weakened.
- No silent clipping.
- No silent skipping.
- No validation approval.

## H019 Strict Broker-Native Validation Attempt

The user explicitly authorized:

- `Authorized: run strict H019 broker-native validation.`

Command run:

- `python .\scripts\run_h019_strict_event_real.py`

Console header:

- `H019 strict expanded broker-native event-driven validation`
- broker timezone: `Europe/Athens`
- symbols: USDJPY, XAUUSD
- source: Exness demo MT5 broker-native H4/M1 exports

Strict bridge-window preflight passed:

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

Validation failed closed during strict event execution.

Exception:

- `quantcore.backtest.h017_event.H018MaximumPerTradeLeverageError`

First H019 failure:

- rule_name: `per_trade_usd_gross_leverage_at_or_below_10x_equity`
- symbol: `USDJPY`
- side: `buy`
- decision_time: `2021-07-05 21:00:00+00:00`
- entry_time: `2021-07-06 01:00:00+00:00`
- entry_raw_price: `110.840000000`
- stop_price: `110.741028558`
- raw_stop_distance: `0.098971442`
- equity_usd: `9872.94`
- lots: `1.20`
- contract_size: `100000.000000000`
- quote_currency: `JPY`
- notional_quote: `13300800.000000000`
- notional_usd: `120000.000000000`
- gross_leverage: `12.154432565`
- maximum_gross_leverage: `10.000000000`
- threshold_basis: `per_trade_usd_gross_notional_divided_by_equity`
- validation_action: `fail_closed`

Interpretation:

- Preflight passed.
- This was not a data-preflight failure.
- This was not a HistData issue.
- This was not an infrastructure failure.
- This was not a normal Python bug.
- H018 leverage guard did exactly what it was designed to do.
- H019 is not validated.
- H019 is not promotable.
- H019 is not live-approved.
- Phase 4 remains not approved.

## H019 Graveyard Record

Docs created earlier:

- `docs/operations/H019_GRAVEYARD_RECORD.md`
- `docs/operations/H020_HYPOTHESIS_SEED.md`

H019 graveyard summary:

- H019 fixed one structural problem but exposed another.
- H017/H018 problem:
  - stale held signal versus stop lifecycle.
- H019 problem:
  - risk sizing can exceed strict USD gross leverage limits when stop distance is tight.
- H019 remains useful as a component reference for lifecycle semantics.
- H019 is not a promotable trading strategy.
- H019 does not approve live trading.

Do not fix H019 by:

- weakening H018 leverage guard,
- raising 10x max casually,
- clipping lots silently in event engine,
- skipping violating trades silently,
- treating failed validation as pass,
- changing costs casually,
- changing broker specs casually,
- switching stop panels,
- broadening symbols,
- adding ML,
- approving live trading.

## H019/H020 Guard Diagnostic Scanner

After H019 failed at the first per-trade leverage violation, an H019/H020 guard diagnostic scanner was added.

Files:

- `scripts/scan_h019_guard_violations_real.py`
- `tests/test_h019_guard_scan_real_script.py`

It reuses:

- `quantcore.backtest.h018_guard_scan.scan_h018_guard_violations`

but calls:

- `run_h019(...)`

Because `run_h019(...)` returns an `H017Result`-shaped object, the existing scanner can inspect H019 positions/stops without weakening event guards.

The scanner is diagnostic-only:

- not validation,
- not promotion,
- not H020 implementation,
- not live-trading approval,
- not a guard weakening.

Real diagnostic command run:

- `python .\scripts\scan_h019_guard_violations_real.py`

Strict bridge-window preflight passed exactly:

- `accepted_entry_count=5476`
- `first_accepted_timestamp=2021-07-02 13:00:00+00:00`
- `last_accepted_timestamp=2026-04-30 01:00:00+00:00`

Diagnostic summary:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=5736`
- `candidate_count=5052`
- `skipped_intent_count=424`
- `violation_count=302`

Violation counts by guard:

- `maximum_per_trade_usd_gross_leverage`: `239`
- `invalid_directional_stop`: `2`
- `minimum_stop_distance`: `19`
- `maximum_portfolio_usd_gross_leverage`: `42`

Violation counts by symbol:

- `USDJPY`: `205`
- `XAUUSD`: `55`

Portfolio-wide leverage violations are symbolless, so symbol totals do not include the `42` portfolio violations.

Violation counts by side:

- `buy`: `155`
- `sell`: `105`

Portfolio-wide leverage violations are symbolless and sideless.

## H019/H020 Guard Severity Diagnostics

The H018 scanner was enriched to preserve severity fields structurally.

Files touched:

- `quantcore/backtest/h018_guard_scan.py`
- `scripts/scan_h019_guard_violations_real.py`
- `tests/test_h018_guard_scan.py`

Added diagnostic fields on violations include:

- raw_stop_distance
- minimum_stop_distance
- lots
- notional_usd
- gross_leverage
- maximum_gross_leverage
- portfolio_notional_usd
- portfolio_gross_leverage
- maximum_portfolio_gross_leverage

Added result property:

- `violation_counts_by_side`

Enriched real H019/H020 diagnostic result:

Per-trade gross leverage violations:

- `count`: `239`
- `min`: `10.090896`
- `median`: `15.700000`
- `p95`: `79.820000`
- `max`: `429.700000`

Portfolio gross leverage violations:

- `count`: `42`
- `min`: `10.062785`
- `median`: `11.205005`
- `p95`: `15.568125`
- `max`: `16.938916`

Minimum stop-distance ratio violations, measured as raw stop distance divided by minimum modeled spread:

- `count`: `19`
- `min`: `0.114372`
- `median`: `0.571525`
- `p95`: `0.951577`
- `max`: `0.960424`

Interpretation:

- H019 materially fixed the stale-held-signal versus stop-lifecycle mismatch.
- H019 reduced total H018-style guard violations from `2271` to `302`.
- H019 reduced invalid directional stops from `1545` to `2`.
- Remaining dominant blocker is notional/leverage sizing.
- Per-trade leverage violations are severe, not cosmetic:
  - median `15.70x`,
  - p95 `79.82x`,
  - max `429.70x`.
- Portfolio leverage violations are milder but real:
  - median `11.205x`,
  - max `16.939x`.
- A simple per-trade cap alone is insufficient because portfolio overlap can still breach the hard guard.
- H020 must include both per-trade notional caps and portfolio gross exposure caps.
- H020 must explicitly handle below-spread stops and residual invalid stop geometry.

## H020 Hypothesis Seed And Design Lock

H020 is a sizing-contract hypothesis, not a lifecycle-repair hypothesis.

H020 keeps:

- H019 Donchian entry/flip plus stateful same-side Chandelier lifecycle semantics.
- Same-side Chandelier stops.
- H018 hard validation guards.
- Strict broker-native complete-window validation requirements.

H020 must not weaken event-engine guards.

### H020 Pre-Trade Suppression Rules

Before sizing a candidate trade, H020 checks intended raw-entry stop geometry.

If same-side stop is non-protective at intended raw entry:

- long/buy stop is not below raw entry, or
- short/sell stop is not above raw entry,

then H020 emits flat/no lot intent for that symbol.

If raw stop distance is below one modeled spread for the symbol, H020 emits flat/no lot intent.

This is approved strategy-level intent suppression.

It is not:

- event-engine silent skipping,
- event-engine lot clipping,
- validation pass-through,
- guard weakening.

The event engine must still fail closed if an invalid stop, sub-minimum stop distance, per-trade leverage violation, or portfolio leverage violation reaches validation.

### H020 Risk-Based Lots

For each valid candidate trade, H020 first computes risk-based lots from:

- equity,
- signed risk fraction,
- raw entry price,
- same-side stop distance,
- contract size,
- quote currency conversion,
- lot step,
- minimum lot.

The existing portfolio sizing conventions remain the starting reference.

### H020 Per-Trade Notional Cap

H020 computes maximum per-trade lots from a strategy-level USD gross notional cap.

Decision:

- H020 strategy per-trade cap: below the H018 hard guard.
- Initial implementation cap: `9.0x` equity.
- H018 hard guard remains `10.0x` equity.

For each candidate:

- `candidate_lots = min(risk_based_lots, per_trade_notional_cap_lots)`

Lots must be rounded down to broker lot step.

If rounded lots fall below broker minimum lot, H020 emits flat/no lot intent for that symbol.

### H020 Portfolio Gross Notional Cap

H020 enforces a portfolio-wide strategy-level USD gross notional cap before event validation.

Decision:

- H020 strategy portfolio cap: below the H018 hard guard.
- Initial implementation cap: `9.0x` equity.
- H018 hard portfolio guard remains `10.0x` equity.

If combined candidate USD gross notional exceeds the H020 portfolio cap:

- scale all active candidate lots down proportionally,
- round down to broker lot step,
- recompute notionals after rounding,
- emit flat/no lot intent for any symbol whose rounded lots fall below minimum lot.

Long and short notionals are summed gross.

They are not netted.

### H020 Representation Decision

H020 should not pretend that signed risk fraction alone is enough to express the strategy contract.

Implementation should introduce explicit sizing diagnostics or explicit lot-intent objects.

At minimum, H020 outputs must make visible:

- raw risk-based lots,
- per-trade-cap lots,
- portfolio-scaled lots,
- final emitted lots,
- whether the symbol was suppressed,
- suppression reason if flat,
- raw stop distance,
- per-trade gross leverage estimate,
- portfolio gross leverage estimate.

The strict event bridge may need to be extended to consume explicit lots safely.

If a temporary implementation converts final lots back into a risk-fraction-shaped result for compatibility, that conversion must be tested and documented as a bridge shim, not as the H020 strategy truth.

### H020 Validation Expectations

Before any strict H020 broker-native validation attempt, run an H020 guard diagnostic scan across the accepted complete windows.

Expected diagnostic goal before validation:

- zero invalid directional-stop violations,
- zero minimum stop-distance violations,
- zero per-trade leverage violations,
- zero portfolio leverage violations.

Any nonzero hard-guard violation in H020 diagnostic means the H020 sizing contract or implementation is not ready for strict validation.

## H020 Code Implemented In This Session

New file:

- `quantcore/strategy/h020.py`

New test file:

- `tests/test_h020.py`

Commit message expected before this handoff:

- `Add H020 sizing intent contract`

Focused test result:

- `8 passed in 1.57s`

Full test result:

- `600 passed in 13.31s`

### H020 Module Purpose

`quantcore.strategy.h020` implements standalone interval-level sizing intent.

It does not:

- run H019 lifecycle end-to-end,
- produce a full time panel,
- integrate with strict event bridge,
- execute fills,
- perform real-data validation,
- validate H020,
- promote H020,
- approve live trading.

It exists to lock and test the explicit sizing contract before any event-engine integration.

### H020 Public Types

Implemented in `quantcore.strategy.h020`:

- `H020SizingConfig`
- `H020SymbolSizingIntent`
- `H020IntervalSizingResult`
- `size_h020_interval_intents(...)`

### H020SizingConfig

Fields:

- `per_trade_max_gross_leverage: float = 9.0`
- `portfolio_max_gross_leverage: float = 9.0`

Class method:

- `H020SizingConfig.default()`

Validation:

- per-trade cap must be positive.
- portfolio cap must be positive.

### H020SymbolSizingIntent

Fields:

- `symbol: str`
- `side: str | None`
- `signed_risk_fraction: float`
- `entry_raw_price: float | None`
- `stop_price: float | None`
- `raw_stop_distance: float | None`
- `risk_based_lots: float`
- `per_trade_cap_lots: float`
- `pre_portfolio_lots: float`
- `final_lots: float`
- `final_signed_risk_fraction: float`
- `notional_usd: float`
- `gross_leverage: float`
- `suppressed: bool`
- `suppression_reason: str | None`

Suppression reasons currently implemented:

- `flat_signal`
- `invalid_stop_geometry`
- `minimum_stop_distance`
- `below_min_lot_after_per_trade_cap`
- `below_min_lot_after_portfolio_scale`

### H020IntervalSizingResult

Fields:

- `decision_time: pd.Timestamp`
- `entry_time: pd.Timestamp`
- `equity_usd: float`
- `intents: Mapping[str, H020SymbolSizingIntent]`
- `portfolio_notional_usd: float`
- `portfolio_gross_leverage: float`
- `portfolio_scaled: bool`

### size_h020_interval_intents Signature

Function:

- `size_h020_interval_intents(...)`

Inputs:

- `decision_time`
- `entry_time`
- `equity_usd`
- `signed_risk_by_symbol`
- `entry_raw_price_by_symbol`
- `stops_long_by_symbol`
- `stops_short_by_symbol`
- optional `config`
- optional `instrument_specs`

Current supported internal symbol order:

- `USDJPY`
- `XAUUSD`

### Implemented H020 Behavior

For each symbol:

1. If signed risk is zero:
   - emit suppressed flat intent with reason `flat_signal`.

2. Determine side:
   - signed risk > 0 => `buy`
   - signed risk < 0 => `sell`

3. Select same-side stop:
   - buy uses long stop.
   - sell uses short stop.

4. Check raw-entry protective geometry:
   - buy requires stop < raw entry.
   - sell requires stop > raw entry.
   - otherwise suppress with `invalid_stop_geometry`.

5. Check minimum stop distance:
   - threshold is one modeled spread from `get_default_cost_spec(symbol).spread_price`.
   - USDJPY spread threshold: `0.01`.
   - XAUUSD spread threshold: `0.30`.
   - if below threshold, suppress with `minimum_stop_distance`.

6. Compute risk-based lots:
   - uses existing `size_position_from_risk(...)`.

7. Compute per-trade notional cap lots:
   - uses strategy cap default `9.0x` equity.
   - USDJPY notional per lot in USD is `contract_size`.
   - XAUUSD notional per lot in USD is `contract_size * entry_raw_price`.
   - rounds down to broker lot step/min lot.

8. Compute pre-portfolio lots:
   - `min(risk_based_lots, per_trade_cap_lots)`.

9. If pre-portfolio lots are zero:
   - suppress with `below_min_lot_after_per_trade_cap`.

10. After all symbols, compute combined gross notional:
    - sum symbol `notional_usd`.
    - long and short gross notional are not netted.

11. If portfolio gross notional exceeds strategy cap:
    - scale active lots proportionally by `cap_notional / active_notional`.
    - round down to broker lot step.
    - if rounded lots are zero, suppress with `below_min_lot_after_portfolio_scale`.
    - recompute final notionals and final signed risk fractions.

12. Final signed risk fraction:
    - computed from actual risk implied by final lots and raw stop distance.
    - positive for buy.
    - negative for sell.

### H020 Tests Implemented

Test file:

- `tests/test_h020.py`

Tests:

1. `test_h020_suppresses_flat_signal`
   - flat signal becomes suppressed/no lots.

2. `test_h020_suppresses_invalid_stop_geometry`
   - buy stop equal to entry is invalid and suppressed.

3. `test_h020_suppresses_stop_distance_below_one_spread`
   - USDJPY sell stop distance below `0.01` is suppressed.

4. `test_h020_caps_per_trade_lots_below_hard_guard`
   - tight but valid USDJPY stop creates risk-based lots above cap.
   - final lots capped at 9x strategy gross leverage.
   - expected final lots approx `0.9`.

5. `test_h020_scales_portfolio_gross_notional_after_per_trade_caps`
   - both symbols active.
   - combined notional exceeds 9x portfolio cap.
   - both lots scaled down.
   - final portfolio gross leverage <= 9x.

6. `test_h020_preserves_final_signed_risk_fraction_from_final_lots`
   - XAUUSD sell with 0.1 lot and 10 USD stop produces approx -1% risk.

7. `test_h020_rejects_non_positive_equity`
   - equity <= 0 rejected.

8. `test_h020_rejects_non_positive_caps`
   - non-positive per-trade cap rejected.

## Important H020 Caveats

H020 currently only implements standalone interval sizing intent.

H020 does not yet:

- run H019 lifecycle end-to-end,
- build a full panel of H020 intents over all bars,
- integrate with the strict event bridge,
- run an H020 guard diagnostic on real data,
- run strict H020 broker-native validation,
- produce a validated equity curve,
- approve live trading.

H020 is not validated.

H020 is not promotable.

H020 is not live-approved.

## Recommended Next Engineering Action

Do not run real H020 validation yet.

Recommended next code step:

Build H020 panel-level sizing diagnostics with synthetic tests.

Specifically:

1. Create a panel-level function that:
   - takes an H019/H017Result-shaped result,
   - takes H4 bars by symbol,
   - iterates decision/entry intervals,
   - uses H019 positions as starting signed risk budget,
   - uses next H4 raw open as intended entry price,
   - uses same-side stop panels,
   - calls `size_h020_interval_intents(...)`,
   - outputs explicit H020 interval results or panels.

2. Add synthetic tests that prove:
   - invalid stops become H020 suppression, not event-engine skipping,
   - below-spread stops become H020 suppression,
   - per-trade cap prevents >9x intent,
   - portfolio cap prevents >9x combined intent,
   - final signed risk fractions are visible and deterministic,
   - no H018 guard is weakened.

3. Then build an H020 guard diagnostic scanner using explicit intents.

4. Only after diagnostic shows zero hard-guard violations should strict H020 validation be considered.

5. Do not run strict H020 broker-native validation without explicit user authorization.

## Possible Next Files

Likely next implementation options:

Option A, recommended first:

- Add panel-level sizing to `quantcore/strategy/h020.py`
- Extend `tests/test_h020.py`

Possible new types:

- `H020PanelSizingResult`
- maybe `build_h020_sizing_panel(...)`

Possible output panels:

- `final_signed_risk_fractions`
- `final_lots`
- `suppressed`
- `suppression_reasons`
- `risk_based_lots`
- `per_trade_cap_lots`
- `pre_portfolio_lots`
- `notional_usd`
- `gross_leverage`

Option B, later:

- Add H020 strict bridge that consumes explicit lots.
- This must be carefully tested because current event engine consumes signed risk fraction and sizes internally.
- Do not silently convert lots into risk fractions without tests and documentation.

## Absolute Do-Not Rules

Do not:

- Do not tune H017/H018/H019 casually.
- Do not change H017/H019/H020 parameters as a quick fix.
- Do not switch selected stop panels as a quick fix.
- Do not change cost model casually.
- Do not add ML.
- Do not broaden to more symbols.
- Do not start Phase 4 execution.
- Do not live trade.
- Do not use HistData for H017/H018/H019/H020 validation.
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
- Do not treat source acceptance as strategy promotion.
- Do not treat future validation as live-trading approval.
- Do not silently fix leverage events by tuning.
- Do not silently change raw versus executable entry sizing.
- Do not continue development while local commits are unpushed.
- Do not let `git status` go unread.
- Do not allow code-test count to drop below `600` without explicit test-removal phase.
- Do not call implemented guards validation.
- Do not call diagnostic scanner results validation.
- Do not choose broker margin or friction-burden thresholds casually.
- Do not implement anything from templates only.
- Do not run real H020 validation before H020 diagnostic work and explicit user authorization.

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

Understood. Continuing after HANDOFF_53.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Current branch should be `main`.
- Latest expected commit should be `Add handoff document #53 after H020 sizing intent`.
- Current full-test anchor is `600 passed`.
- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 failed and is in the graveyard.
- H019 strict broker-native validation passed strict complete-window preflight but failed closed on `H018MaximumPerTradeLeverageError`.
- First H019 failure was USDJPY buy at decision time `2021-07-05 21:00:00+00:00`, entry time `2021-07-06 01:00:00+00:00`, with `12.154432565x` per-trade gross leverage versus `10.0x` max.
- H019/H020 diagnostic showed `302` remaining H019 guard violations:
  - `239` per-trade leverage,
  - `42` portfolio leverage,
  - `19` minimum stop-distance,
  - `2` invalid directional stop.
- Per-trade leverage severity was large: median `15.70x`, p95 `79.82x`, max `429.70x`.
- H020 sizing contract is locked:
  - 9x strategy per-trade cap,
  - 9x strategy portfolio cap,
  - flat/no intent for invalid stop geometry,
  - flat/no intent for below-spread raw stop distance.
- H020 standalone interval sizing intent code exists in `quantcore/strategy/h020.py`.
- H020 tests exist in `tests/test_h020.py`.
- H020 is not validated, not promotable, and live trading is not approved.
- Next likely step is H020 panel-level sizing diagnostics with synthetic tests, not real validation.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Then paste the full output.

After hygiene passes, I will help continue H020 panel-level sizing diagnostics before any strict real-data validation.
