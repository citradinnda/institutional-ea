# HANDOFF 52 - After H019 Failure And H020 Seed, Before H019/H020 Guard Diagnostic

If any older handoff conflicts with this file, this HANDOFF_52 wins.

This handoff is intentionally self-contained enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

The user is intelligent but not a professional developer. They are building infrastructure-first because previous strategy attempts failed due to weak validation, fictional backtesting, poor cost modeling, and poor risk control.

Target environment:

- Research: Python package `quantcore`
- Execution target later: MetaTrader 5 expert advisor
- Production target later: Oracle Cloud Always Free VPS
- Monitoring later: self-hosted free-tier stack
- Current machine: Windows
- Shell: PowerShell
- Editor: VS Code
- Python: 3.12.10 inside `.venv`
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

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_52.md`

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

Current full-test anchor:

- `588 passed`

If code tests pass but the count drops below `588` without an explicit test-removal phase, treat it as a regression.

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

Use PowerShell here-strings only when useful. For long docs, VS Code manual editing is also acceptable.

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
  - Current full-test anchor: `588 passed`.
- If full tests pass but count drops below `588` without planned test removal, stop and treat as regression.

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

Latest pushed commit before this handoff expansion should be one of:

- `4e020ca Document H019 failure and seed H020`
- or a shorter handoff commit if it was already committed before this expanded version

Expected final handoff commit message after this expanded file is committed:

- `Expand handoff document #52 after H019 failure`

Recent commits expected:

- `4e020ca Document H019 failure and seed H020`
- `ea95f1a Add H019 strict real-data runner`
- `41538c4 Add H019 strict event routing`
- `5b4097d Add H019 portfolio integration`
- `d0bc62d Add H019 stateful chandelier lifecycle`
- `80ab5d2 Add handoff document #51 before H019`
- `79a464f Add H018 stop-state diagnostic`
- `a6b6bf9 Add handoff document #50 after invalid stop panel diagnostics`
- `6a52328 Extend H018 invalid stop panel diagnostics`
- `966812c Add handoff document #49 after invalid stop diagnostics`

Current full-test anchor:

- `588 passed`

Last full pytest result after latest code commit:

- `588 passed in 12.50s`

No code should change after those tests except docs-only handoff/graveyard/seed documents if being edited.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Expected after this expanded handoff is committed and pushed:

- On branch `main`
- Branch up to date with `origin/main`
- Nothing to commit, working tree clean
- Latest commit should be `Expand handoff document #52 after H019 failure`
- Previous important commit should be `4e020ca Document H019 failure and seed H020`

Do not require pytest for this first check unless code has changed or status is not clean.

## Important Paths

Code:

- `C:\Users\equin\Documents\institutional-ea\quantcore`
- `C:\Users\equin\Documents\institutional-ea\scripts`
- `C:\Users\equin\Documents\institutional-ea\tests`

Strategy files:

- `quantcore\strategy\h017.py`
- `quantcore\strategy\h019.py`
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

Friction diagnostic:

- `quantcore\backtest\friction.py`

H018 guard scanner:

- `quantcore\backtest\h018_guard_scan.py`
- `scripts\scan_h018_guard_violations_real.py`
- `tests\test_h018_guard_scan.py`

H018 invalid-stop diagnostics:

- `quantcore\backtest\h018_invalid_stop_cause.py`
- `scripts\diagnose_h018_invalid_stop_causes_real.py`
- `tests\test_h018_invalid_stop_cause.py`

H018 stop-state diagnostic:

- `quantcore\backtest\h018_stop_state_diagnostic.py`
- `scripts\diagnose_h018_stop_state_real.py`
- `tests\test_h018_stop_state_diagnostic.py`

H019 files:

- `quantcore\strategy\h019.py`
- `quantcore\backtest\h019_strict_event.py`
- `scripts\run_h019_strict_event_real.py`
- `tests\test_h019.py`
- `tests\test_h019_strict_event.py`
- `tests\test_h019_strict_event_real_script.py`

Important docs:

- `README.md`
- `docs\operations\H019_GRAVEYARD_RECORD.md`
- `docs\operations\H020_HYPOTHESIS_SEED.md`
- `docs\operations\handoffs\HANDOFF_52.md`

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
- H019: Stateful Donchian/Chandelier lifecycle fixed the stale-stop first blocker but failed closed on H018 per-trade leverage guard. H019 is now in the graveyard.

Current verdicts:

- H017 failed.
- H018 not validated.
- H019 failed.
- H020 not implemented yet.
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

## H017 And H018 Diagnostic Status Before H019

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

### H018 Guard Violation Diagnostic Scanner

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

### H018 Invalid-Stop Cause Diagnostic

Files:

- `quantcore/backtest/h018_invalid_stop_cause.py`
- `scripts/diagnose_h018_invalid_stop_causes_real.py`
- `tests/test_h018_invalid_stop_cause.py`

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

Interpretation:

- The invalid-stop problem was not mainly next-open gap/crossing.
- Almost all invalid stops were already invalid at decision close.
- Switching to opposite panel was not approved because opposite panel is protective for the opposite side under its own semantics.

### H018 Stop-State Diagnostic

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

Bucket counts by symbol and side:

USDJPY buy:

- total nonzero signal count: `3215`
- same-side stop valid at decision close: `2848`
- same-side stop breached at decision close: `367`
- fresh signal count: `67`
- held continuation count: `3148`
- breached fresh signal count: `0`
- breached held continuation count: `367`

USDJPY sell:

- total nonzero signal count: `2261`
- same-side stop valid at decision close: `1810`
- same-side stop breached at decision close: `451`
- fresh signal count: `69`
- held continuation count: `2192`
- breached fresh signal count: `1`
- breached held continuation count: `450`

XAUUSD buy:

- total nonzero signal count: `3214`
- same-side stop valid at decision close: `2825`
- same-side stop breached at decision close: `389`
- fresh signal count: `48`
- held continuation count: `3166`
- breached fresh signal count: `0`
- breached held continuation count: `389`

XAUUSD sell:

- total nonzero signal count: `2262`
- same-side stop valid at decision close: `1925`
- same-side stop breached at decision close: `337`
- fresh signal count: `49`
- held continuation count: `2213`
- breached fresh signal count: `0`
- breached held continuation count: `337`

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

H019 commits:

- `d0bc62d Add H019 stateful chandelier lifecycle`
- `5b4097d Add H019 portfolio integration`
- `41538c4 Add H019 strict event routing`
- `ea95f1a Add H019 strict real-data runner`

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

Focused state-machine tests passed.

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

### H019 Real-Data Runner

File:

- `scripts/run_h019_strict_event_real.py`

Purpose:

- Run strict expanded broker-native H019 validation manually.
- Mirror H017 strict runner but call H019 route.
- Use strict common complete bridge-window preflight.
- Verify exact accepted bridge-window contract.
- Use broker-native MT5 Exness demo H4/M1 data only.
- Do not use HistData.
- Do not write derived datasets.
- Do not approve live trading.

Focused script tests passed.

Full test count after H019 runner:

- `588 passed`

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

Raw MT5 export summary from the run:

USDJPY H4:

- `n_input_rows=8713`
- `n_bars=8713`
- `earliest_utc=2018-07-02 21:00:00+00:00`
- `latest_utc=2026-04-30 05:00:00+00:00`
- `broker_tz=Europe/Athens`

XAUUSD H4:

- `n_input_rows=8658`
- `n_bars=8658`
- `earliest_utc=2018-06-27 21:00:00+00:00`
- `latest_utc=2026-04-30 05:00:00+00:00`
- `broker_tz=Europe/Athens`

USDJPY M1:

- `n_input_rows=1785312`
- `n_bars=1785312`
- `earliest_utc=2018-07-02 21:00:00+00:00`
- `latest_utc=2026-04-30 07:00:00+00:00`
- `broker_tz=Europe/Athens`

XAUUSD M1:

- `n_input_rows=1704907`
- `n_bars=1704907`
- `earliest_utc=2018-06-27 21:00:00+00:00`
- `latest_utc=2026-04-30 07:00:00+00:00`
- `broker_tz=Europe/Athens`

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

Rejection counts:

- `usdjpy_m1_count_not_expected: 2969`
- `usdjpy_missing_next_h4_timestamp: 1`
- `usdjpy_non_4h_next_h4_delta: 1179`
- `xauusd_m1_count_not_expected: 2505`
- `xauusd_missing_next_h4_timestamp: 1`
- `xauusd_non_4h_next_h4_delta: 1193`

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

The user asked to document everything, put H019 in the graveyard if failed, and start a new hypothesis.

Conclusion:

- H019 is failed in current form.

Docs created and pushed in commit:

- `4e020ca Document H019 failure and seed H020`

Docs:

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

## H020 Hypothesis Seed

H020 is a new hypothesis seed.

No H020 code exists yet.

H020 is not validated.

H020 is not promotable.

H020 is not live-approved.

Phase 4 execution is not approved.

Live trading is not approved.

Reason H020 exists:

- H019 failed strict broker-native event validation because the strategy produced a trade whose USD gross notional exposure exceeded the H018 maximum per-trade leverage guard.

H020 core question:

Can a Donchian-entry plus stateful-Chandelier-exit strategy remain viable when position sizing is explicitly constrained by both:

1. target risk from stop distance, and
2. maximum USD gross notional leverage?

Proposed H020 identity:

- H020: stateful Chandelier lifecycle with notional-aware sizing contract

Starting point:

- Keep H019 lifecycle semantics.
- Keep same-side Chandelier stops.
- Keep H018 guards.
- Add explicit pre-trade sizing contract that prevents impossible gross leverage before event validation.

Proposed sizing principle:

For each candidate trade, calculate both:

1. risk-based lots, derived from:
   - equity,
   - risk fraction,
   - stop distance,
   - contract size,
   - quote currency conversion,
   - lot step,
   - min lot;

2. max-notional lots, derived from:
   - equity,
   - maximum allowed gross leverage,
   - entry price,
   - contract size,
   - quote currency conversion,
   - lot step,
   - min lot.

Then:

- `allowed_lots = min(risk_based_lots, max_notional_lots)`

Open design question:

- If `allowed_lots` is below broker minimum lot, should strategy emit zero exposure?
- If yes, this is explicit strategy sizing semantics, not silent event-engine skipping.
- If no, H020 may continue failing guards in small-equity or tight-stop cases.

Important distinction:

- H018 guard behavior must remain fail-closed.
- H020 must not weaken guards.
- H020 should define strategy outputs compatible with the guards under normal conditions.
- A guard failure after H020 would still mean the implementation or assumptions are wrong.

H020 design choices to lock before code:

1. Per-trade notional cap:
   - use existing H018 10x equity cap,
   - or choose lower strategy cap below the hard guard?

2. Portfolio notional cap:
   - use existing H018 10x portfolio gross cap,
   - or choose lower strategy cap below the hard guard?

3. Lot clipping semantics:
   - Is reducing risk-based lots to the notional cap approved strategy behavior?
   - This is not the same as event engine silently clipping a violation.
   - It must be visible in strategy output or diagnostics.

4. Minimum-lot semantics:
   - If capped lots fall below min lot, should H020 emit flat?

5. Risk accounting:
   - Should H020 positions continue as signed risk fraction?
   - Or should strategy/event bridge move toward explicit lot-intent objects?

6. Heat governor interaction:
   - Should heat be applied before notional cap?
   - after notional cap?
   - or through portfolio allocation?

7. Diagnostic requirement:
   - Before strict validation, run H019/H020 guard scan across accepted windows.

## Recommended Next Engineering Action

Do not write H020 sizing code yet.

First build an H019/H020 guard diagnostic scanner.

Reason:

H019 failed at the first per-trade leverage violation. We need the full distribution before choosing H020 sizing semantics.

The diagnostic should answer:

- Are invalid directional stops now near zero?
- How many per-trade leverage violations remain?
- How many portfolio leverage violations remain?
- How many minimum stop-distance violations remain?
- Which symbols and sides dominate failures?
- Are failures mostly tight-stop sizing, overlapping exposure, or both?

Recommended fastest safe implementation:

- Reuse `quantcore.backtest.h018_guard_scan.scan_h018_guard_violations`
- Create an H019 real diagnostic script that calls `run_h019(...)` instead of `run_h017(...)`.
- Because `run_h019(...)` returns `H017Result` shape, the existing scanner should work.
- Add no-real-data test that verifies the script routes through `run_h019(...)`.

Likely new files:

- `scripts/scan_h019_guard_violations_real.py`
- `tests/test_h019_guard_scan_real_script.py`

Probably no new core scanner module is needed yet.

Do not treat the scanner output as validation.

Do not run real diagnostic unless explicitly authorized or the user says to proceed with the diagnostic. If authorized, it is diagnostic-only.

## Existing H018 Guard Scanner Details Useful For H019 Diagnostic

Core scanner:

- `quantcore/backtest/h018_guard_scan.py`

Main function:

- `scan_h018_guard_violations(...)`

Inputs include:

- `h017_result`
- `h4_by_symbol`
- `accepted_entry_times`
- `starting_equity_usd`
- `expected_h4_delta`

Because H019 returns an `H017Result`-shaped object, pass the H019 result as `h017_result`.

Existing H018 real script:

- `scripts/scan_h018_guard_violations_real.py`

Existing H018 real script flow:

1. Load broker-native exports.
2. Assess strict complete bridge windows.
3. Assert accepted bridge-window contract.
4. Run `run_h017(...)`.
5. Call `scan_h018_guard_violations(...)`.
6. Print:
   - accepted_entry_count
   - executed_entry_count
   - skipped_entry_count
   - event_interval_count
   - trade_intent_count
   - candidate_count
   - skipped_intent_count
   - violation_count
   - violation_counts_by_guard
   - violation_counts_by_symbol
   - first violations

H019 diagnostic script should mirror that but:

- title should say H019 diagnostic,
- import `run_h019` from `quantcore.strategy.h019`,
- call `run_h019(...)`,
- print H019/H020 interpretation guardrails.

Suggested script name:

- `scripts\scan_h019_guard_violations_real.py`

Suggested test name:

- `tests\test_h019_guard_scan_real_script.py`

## Absolute Do-Not Rules

Do not:

- Do not tune H017/H018/H019 casually.
- Do not change H017/H019 parameters as a quick fix.
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
- Do not allow code-test count to drop below `588` without explicit test-removal phase.
- Do not call implemented guards validation.
- Do not call diagnostic scanner results validation.
- Do not choose broker margin or friction-burden thresholds casually.
- Do not implement anything from templates only.
- Do not start H020 sizing code before H019/H020 guard diagnostic distribution is known.

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

Understood. Continuing after HANDOFF_52.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Current branch should be `main`.
- Latest expected commit should be `Expand handoff document #52 after H019 failure`.
- Current full-test anchor is `588 passed`.
- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 is failed and in the graveyard.
- H019 strict broker-native validation passed the strict complete-window preflight but failed closed on `H018MaximumPerTradeLeverageError`.
- First H019 failure was USDJPY buy at decision time `2021-07-05 21:00:00+00:00`, entry time `2021-07-06 01:00:00+00:00`, with `12.154432565x` per-trade gross leverage versus `10.0x` max.
- Live trading is not approved.
- Phase 4 is not approved.
- HistData is rejected for H017/H018/H019/H020 validation.
- H020 is only a hypothesis seed; no H020 code exists.
- Next engineering step is an H019/H020 guard diagnostic scan, not H020 sizing code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Then paste the full output.

After hygiene passes, I will help create the H019 guard diagnostic scanner before any H020 sizing code.
