# HANDOFF 47 - After H018 Portfolio Leverage Guard Governance Sync

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_47 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

The user is intelligent but not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

Target environment:

- Research: Python package quantcore.
- Execution target later: MetaTrader 5 expert advisor.
- Production target later: Oracle Cloud Always Free VPS.
- Monitoring later: self-hosted free-tier stack.
- Current machine: Windows.
- Shell: PowerShell.
- Editor: VS Code.
- Python: 3.12.10 inside .venv.
- No WSL.

## Important Human Preference Update

The user is tired of excessive documentation and slow ceremony.

Going forward:

- Do not document every tiny change.
- Do not create governance docs unless they prevent real confusion, record a real decision, preserve a handoff, or protect against future ambiguity.
- For docs-only changes, do not run full pytest unless there is a clear reason.
- For docs-only changes, basic checks are enough:
  - git status
  - git diff --check
  - git diff --stat
  - optional preview with Get-Content or Select-String
  - commit
  - push
  - git status
  - git ls-files for touched docs
- For code changes, tests are still mandatory.
- For code changes touching strategy, event engine, sizing, accounting, data loading, or validation logic:
  - run focused tests if applicable,
  - run full pytest -q,
  - compare test count to the current anchor,
  - commit,
  - push.
- Current full-test anchor is 558 passed.
- If code tests pass but the count drops below 558 without an explicit test-removal phase, treat it as a regression.
- Do not continue development while local commits are unpushed.
- Always read git status before starting a new phase.
- Keep responses step-by-step and short enough to be usable.

## Non-Negotiable Environment Rules

Use:

- Windows.
- PowerShell.
- VS Code.
- Python 3.12.10.
- .venv.
- No WSL.

PowerShell rule:

Do not use Linux/macOS heredoc syntax like:

python - <<'PY'

PowerShell does not support that.

Use PowerShell here-strings only when truly necessary. For long docs, prefer VS Code manual editing.

## Practical Workflow Rules

Use a lighter workflow than older handoffs.

General rules:

1. Start each phase with git status.
2. Do one sub-phase at a time.
3. Use explicit Windows paths.
4. Use plain English.
5. Define technical terms inline when needed.
6. Never write code without saying exactly where the file goes and how to run it.
7. Never continue while local commits are unpushed.
8. Always commit and push completed work.
9. Always verify touched files are tracked with git ls-files after commit.
10. Do not run real-data validation unless explicitly authorized.
11. Do not start Phase 4 execution unless explicitly authorized.
12. Do not live trade.

Testing rules:

- Docs-only edit:
  - No full pytest required by default.
  - Use git diff --check and git diff --stat.
- Code edit:
  - Run focused tests when applicable.
  - Run full pytest -q.
  - Current anchor: 558 passed.
- If full tests pass but count drops below 558 without planned test removal, stop and treat as regression.

Git rules:

- Before changes:
  - git status
- After changes:
  - git diff --check
  - git diff --stat
  - git add touched files
  - git commit
  - git push
  - git status
  - git ls-files touched files

## Repository State At This Handoff

Repository root:

C:\Users\equin\Documents\institutional-ea

Virtual environment:

C:\Users\equin\Documents\institutional-ea\.venv

Branch:

main

GitHub remote:

https://github.com/citradinnda/institutional-ea.git

Handoff folder:

C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs

This handoff path:

C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_47.md

Latest commit before this handoff should be:

daaa2b6 Sync H018 portfolio leverage guard governance docs

Recent commits expected before this handoff:

- daaa2b6 Sync H018 portfolio leverage guard governance docs
- 7be5a45 Add handoff document #46 after H018 portfolio leverage guard
- c7b50ee Implement H018 portfolio gross leverage guard
- 98173b5 Add handoff document #45 after H018 portfolio leverage policy acceptance
- 0bc94a2 Accept H018 portfolio gross leverage policy
- 6907b47 Accept H018 raw-entry sizing reference policy
- bf89ff4 Sync H018 max leverage guard governance docs
- 65e0901 Add handoff document #44 after H018 max leverage guard
- 9d062d8 Implement H018 maximum per-trade leverage guard
- fffe81c Move all handoff documents into handoff folder

Expected handoff commit message after this file is committed:

Add handoff document #47 after H018 governance sync

Current full-test anchor:

558 passed

Last full pytest result before this handoff:

558 passed in 13.62s

No code changed after that test. The last work was docs-only governance sync.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification only.

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea

.\.venv\Scripts\Activate.ps1

git status

git log --oneline -10

Expected after this handoff is committed and pushed:

- On branch main.
- Branch up to date with origin/main.
- Nothing to commit, working tree clean.
- Latest commit: Add handoff document #47 after H018 governance sync.
- Previous commit: daaa2b6 Sync H018 portfolio leverage guard governance docs.

Do not require pytest for this first check unless code has changed or status is not clean.

## Important Paths

Code:

- C:\Users\equin\Documents\institutional-ea\quantcore
- C:\Users\equin\Documents\institutional-ea\scripts
- C:\Users\equin\Documents\institutional-ea\tests

Event engine:

C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_event.py

Portfolio sizing/accounting:

C:\Users\equin\Documents\institutional-ea\quantcore\backtest\portfolio.py

Focused event tests:

C:\Users\equin\Documents\institutional-ea\tests\test_h017_event.py

Important docs:

- README.md
- docs/operations/H018_DECISION_RECORD_INDEX.md
- docs/operations/H018_DECISION_MATRIX.md
- docs/operations/H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md
- docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md
- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md
- docs/operations/H018_SIZING_REFERENCE_DECISION_RECORD.md
- docs/operations/H018_PORTFOLIO_GROSS_LEVERAGE_DECISION_RECORD.md
- docs/operations/handoffs/HANDOFF_47.md

## Current Governance Sync Status

The latest docs sync commit was:

daaa2b6 Sync H018 portfolio leverage guard governance docs

It updated:

- README.md
- docs/operations/H018_DECISION_MATRIX.md
- docs/operations/H018_DECISION_RECORD_INDEX.md
- docs/operations/H018_PORTFOLIO_GROSS_LEVERAGE_DECISION_RECORD.md

Purpose:

- Mark H018 portfolio-wide gross leverage guard as implemented.
- Update README implemented-guard list.
- Update README full-test anchor from 552 passed to 558 passed.
- Replace stale wording that said H018 remained fully unimplemented.
- Preserve that H018 remains not validated, not promotable, and not live-approved.

Important:

This was docs-only. No code changed in that commit.

## Gitignore / Raw Data Rules

The repo uses root-anchored:

/data/

Do not change it to unanchored:

data/

Reason:

An unanchored data/ rule previously risked excluding:

quantcore/data/

Raw data under root /data/ is gitignored and must not be committed.

Do not commit:

- raw MT5 CSV files,
- raw HistData files,
- large derived datasets,
- broker/vendor source files.

Do not modify raw broker files.

## Broker / Data State

Broker:

Exness

Account environment:

Demo

Server:

MT5

Broker timezone used by loader:

Europe/Athens

Meaning:

- Winter UTC+2.
- Summer UTC+3.
- DST-aware.

MT5 loader signature:

load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

Expanded broker-native raw exports exist locally and are gitignored:

- data\raw\USDJPY\H4.csv
- data\raw\USDJPY\M1.csv
- data\raw\XAUUSD\H4.csv
- data\raw\XAUUSD\M1.csv

Reported exact MT5 symbols:

- USDJPYm
- XAUUSDm

Do not commit these raw files.

## Source Acceptance Status

Expanded broker-native USDJPY and XAUUSD M1/H4 data is conditionally accepted for H017/H018-style strict validation only under strict complete-window restrictions.

Accepted source:

Exness demo MT5 broker-native exports.

Accepted symbols:

- USDJPY
- XAUUSD

Accepted timeframes:

- Broker-native H4.
- Broker-native M1.

Accepted validation bridge-window range:

- First possible common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
- Last possible common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00

Accepted bridge-window count:

5476 common complete H4/M1 windows

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
- H017: H016 plus portfolio heat governor. H017 failed strict expanded broker-native event validation by insolvency and is not promotable.

Current H017 verdict:

- H017 is failed.
- H017 is not promotable.
- H017 is not live-approved.
- Do not tune H017.
- Do not broaden symbols.
- Do not add ML.
- Do not approve live trading.

## Core Strategy Conventions

ATR:

- Wilder RMA, not SMA.
- First true range is high - low.
- Seed at index window - 1 with simple mean of first window true ranges.
- Recurrence: ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n

Chandelier Exit:

- Long: highest_high(lookback) - multiplier * ATR
- Short: lowest_low(lookback) + multiplier * ATR

Defaults:

- multiplier = 3.0
- lookback = 22

Vol Target:

- Realized vol at bar t uses returns through t-1 only.
- No lookahead.
- H4 periods per year = 1512

Signals:

- Donchian breakout.
- Long: close[t] > max(high[t-N ... t-1])
- Short: close[t] < min(low[t-N ... t-1])
- Channel uses prior N bars via shift(1).rolling(N).

H017:

- Inner-joins USDJPY and XAUUSD timestamps.
- Computes close-to-close returns.
- Uses same returns for vol targeting and heat governor.
- Position is signed risk exposure:
  signal * per_trade_risk * vol_mult * heat_mult

Heat governor:

Combined heat:

sqrt(w' (r^2 * C) w)

Defaults:

- cap = 0.015
- per_trade_risk = 0.01
- correlation_window = 120
- correlation_floor = 0.0

## Event-Driven Backtest Conventions

Fill rule:

If stop and take-profit are both touched in the same M1 bar, stop wins.

Reason:

M1 OHLC does not reveal tick order inside the minute, so stop-first is conservative.

Cost model defaults:

USDJPY:

- spread_price = 0.01
- commission_usd_per_lot_per_fill = 7.0
- stop_slippage_atr_fraction = 0.05

XAUUSD:

- spread_price = 0.30
- commission_usd_per_lot_per_fill = 10.0
- stop_slippage_atr_fraction = 0.05

Commission is per fill. A round trip charges entry and exit.

Portfolio P&L:

- XAUUSD P&L is already USD.
- USDJPY P&L is JPY and must be divided by USDJPY conversion price to become USD.

Event bridge timing:

- H017 decides at H4 timestamp t.
- Trade opens on next H4 bar open t+1.
- M1 bars inside the next H4 window resolve stops.
- If no stop is hit, exposure closes at following H4 open as signal_flip.
- This is a bridge-layer simplification.

Current event engine sizing behavior:

It sizes from absolute difference between raw H4 entry open and stop price.

This occurs before entry spread is applied.

Do not silently change this behavior.

## Current Portfolio API From Inspection

InstrumentSpec dataclass fields:

- symbol
- contract_size
- quote_currency
- lot_step
- min_lot

PositionSize dataclass fields:

- symbol
- side
- signed_risk_fraction
- lots
- target_risk_usd
- actual_risk_usd
- notional_quote

size_position_from_risk signature:

size_position_from_risk(*, symbol: str, signed_risk_fraction: float, equity_usd: float, entry_price: float, stop_distance_price: float, instrument_spec: InstrumentSpec | None = None) -> PositionSize

Current behavior:

- equity_usd must be positive.
- entry_price must be positive.
- stop_distance_price must be positive.
- target_risk_usd = abs(signed_risk_fraction) * equity_usd.
- risk_per_lot_quote = stop_distance_price * contract_size.
- risk per lot is converted through quote_pnl_to_usd.
- raw lots are rounded down to broker lot_step.
- if rounded lots are below min_lot, zero lots are returned.
- actual_risk_usd = lots * risk_per_lot_usd.
- notional_quote = lots * contract_size * entry_price.

Default instrument specs:

USDJPY:

- contract_size = 100000.0
- quote_currency = JPY
- lot_step = 0.01
- min_lot = 0.01

XAUUSD:

- contract_size = 100.0
- quote_currency = USD
- lot_step = 0.01
- min_lot = 0.01

quote_pnl_to_usd convention:

- XAUUSD quote currency is USD, so quote P&L is already USD.
- USDJPY quote currency is JPY, so JPY P&L divided by USDJPY price converts to USD.

## Implemented Guards

### Raw-Entry Invalid-Stop Guard

Implemented in:

quantcore/backtest/h017_event.py

Error class:

H017EventInvalidStopError

Rule:

- Long/buy stop must be below raw H4 entry open.
- Short/sell stop must be above raw H4 entry open.
- Equality is invalid.
- Invalid directional stop geometry fails closed.
- Invalid stops are not skipped or clipped.

This does not promote H017.

### H018 Minimum Stop-Distance Guard

Implemented in:

quantcore/backtest/h017_event.py

Error class:

H018MinimumStopDistanceError

Rule:

raw_stop_distance = abs(raw_h4_entry_open - stop_price)

Minimum stop distance is one modeled spread for the symbol.

Thresholds:

- USDJPY: 0.01
- XAUUSD: 0.30

Boundary:

- below threshold fails closed.
- equality passes.
- above threshold passes.

Implementation uses math.isclose with rel_tol=1e-12 and abs_tol=1e-12.

Audit fields include:

- rule_name = raw_stop_distance_at_least_one_modeled_spread
- symbol
- side
- decision_time
- entry_time
- entry_raw_price
- stop_price
- raw_stop_distance
- minimum_stop_distance
- threshold_basis = one_modeled_spread
- validation_action = fail_closed

### H018 Maximum Per-Trade USD Gross Leverage Guard

Implemented in commit:

9d062d8 Implement H018 maximum per-trade leverage guard

Implemented in:

quantcore/backtest/h017_event.py

Tests in:

tests/test_h017_event.py

Error class:

H018MaximumPerTradeLeverageError

Constant:

_MAXIMUM_PER_TRADE_USD_GROSS_LEVERAGE = 10.0

Helper:

_position_notional_usd(...)

Validator:

_validate_maximum_per_trade_usd_gross_leverage(...)

Rule name:

per_trade_usd_gross_leverage_at_or_below_10x_equity

Rule:

A single trade may not create more than 10 times account equity in USD-converted gross notional exposure.

Measurement:

gross_leverage = notional_usd / equity_usd

Threshold:

10.0

Boundary:

- < 10.0 passes.
- == 10.0 passes.
- > 10.0 fails closed.

Instrument handling:

XAUUSD:

- PositionSize.notional_quote is already USD.
- notional_usd = position_size.notional_quote

USDJPY:

- PositionSize.notional_quote is JPY.
- USDJPY price is JPY per 1 USD.
- notional_usd = position_size.notional_quote / entry_raw_price

### H018 Portfolio-Wide USD Gross Leverage Guard

Implemented in commit:

c7b50ee Implement H018 portfolio gross leverage guard

Governance docs synced in commit:

daaa2b6 Sync H018 portfolio leverage guard governance docs

Implemented in:

quantcore/backtest/h017_event.py

Tests in:

tests/test_h017_event.py

Error class:

H018MaximumPortfolioGrossLeverageError

Constant:

_MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE = 10.0

Candidate dataclass:

_SymbolIntervalCandidate

Validator:

_validate_maximum_portfolio_usd_gross_leverage(...)

Rule name:

portfolio_usd_gross_leverage_at_or_below_10x_equity

Rule:

At a single event interval, the total USD-converted gross notional exposure opened by all symbols may not exceed 10 times account equity.

Measurement:

portfolio_gross_leverage = portfolio_notional_usd / interval_start_equity_usd

Where:

- portfolio_notional_usd is the sum of USD-converted gross notional for all non-zero-lot candidate trades in the same event interval.
- interval_start_equity_usd is the equity used for sizing at the start of that interval.
- Gross exposure is summed using absolute notional exposure.
- Long and short exposures are not netted.
- USDJPY notional is converted from JPY to USD by dividing notional_quote by entry_raw_price.
- XAUUSD notional_quote is already USD-denominated.

Threshold:

10.0

Boundary:

- < 10.0 passes.
- == 10.0 passes.
- > 10.0 fails closed.

Violation policy:

- Raise explicit H018MaximumPortfolioGrossLeverageError.
- Do not silently skip any trade.
- Do not clip any position size.
- Do not net long and short notionals.
- Do not warn and continue.
- Do not log-only continue.
- Do not convert the run into a promotable validation result.

Implemented placement:

For each interval:

1. For each symbol, build a preliminary candidate before any fill is created.
2. Candidate build validates directional stop geometry.
3. Candidate build validates minimum raw stop distance.
4. Candidate build computes preliminary PositionSize.
5. Zero-lot positions return no candidate.
6. Candidate build validates maximum per-trade USD gross leverage.
7. Non-zero candidates are collected across symbols.
8. Portfolio-wide USD gross leverage is validated across collected candidates.
9. Only after portfolio validation passes are execution-cost-adjusted fills created.

This preserves current raw-entry sizing and raw-entry directional stop semantics.

This preserves existing fill/P&L behavior by moving pre-fill candidate construction out of _build_symbol_interval_fill and keeping fill creation logic equivalent after validation.

Focused tests added by portfolio guard implementation:

- Single-symbol interval at or below 10.0x passes.
- Two-symbol interval with combined exposure below 10.0x passes.
- Two-symbol interval with combined exposure exactly 10.0x passes.
- Two-symbol interval with combined exposure above 10.0x fails closed.
- Fail-closed error audit fields are preserved.
- Long and short notionals are summed gross and not netted.

Focused event tests after implementation:

36 passed

Full suite after implementation:

558 passed

## Accepted H018 Policies

Accepted and implemented:

- Fail-closed validation-mode trade violation policy.
- Minimum raw stop-distance rule.
- Maximum per-trade USD gross leverage rule.
- Raw-entry sizing reference.
- Raw-entry directional stop-validity reference.
- Portfolio-wide USD gross leverage rule.

Important status distinction:

The H018 guard layer is partially implemented, but H018 is still not validated, not promotable, and not live-approved.

## Current H018 Governance Status

H018 is not validated.

H018 is not promotable.

H018 does not approve live trading.

H018 does not approve Phase 4 execution.

Accepted and implemented H018-related code so far:

- H017EventInvalidStopError.
- Raw-entry directional stop validation.
- H018MinimumStopDistanceError.
- _validate_minimum_stop_distance.
- H018MaximumPerTradeLeverageError.
- _position_notional_usd.
- _validate_maximum_per_trade_usd_gross_leverage.
- Event-engine integration of max per-trade leverage guard after preliminary sizing and before fill creation.
- H018MaximumPortfolioGrossLeverageError.
- _SymbolIntervalCandidate.
- _validate_maximum_portfolio_usd_gross_leverage.
- Two-stage candidate-then-fill interval processing for portfolio leverage validation.

Still not chosen:

- No real-data rerun classification.
- No formal H018 claim.
- No broker margin model.
- No friction-burden cap.
- No diagnostic-only continuation mode.

Still not authorized:

- No real-data validation rerun.
- No H018 claim.
- No live trading.
- No Phase 4 execution.

## Strict Expanded Broker-Native Validation Result

Script:

scripts/run_h017_strict_event_real.py

Strict bridge-window preflight passed.

Preflight facts:

- expected_m1_bars_per_h4 = 240
- expected_h4_delta = 0 days 04:00:00
- candidate_common_h4_count = 8654
- usdjpy_complete_count = 5685
- xauusd_complete_count = 6149
- common_complete_count = 5476
- accepted_count = 5476
- first_accepted_timestamp = 2021-07-02 13:00:00+00:00
- last_accepted_timestamp = 2026-04-30 01:00:00+00:00
- usdjpy_only_complete_count = 209
- xauusd_only_complete_count = 673
- rejected_count = 3178

Strict event-driven backtest result before invalid-stop and H018 guards:

- completed = False
- failure_reason = insolvency
- decision_time = 2021-07-06 01:00:00+00:00
- entry_time = 2021-07-06 05:00:00+00:00
- forced_exit_time = 2021-07-06 09:00:00+00:00
- interval_start_equity_usd = 9847.56
- interval_pnl_usd = -11835.26
- ending_equity_usd = -1987.71
- interval_return_pct = -120.18
- interval_fills = 2

Fatal USDJPY fill before guards:

- symbol = USDJPY
- side = buy
- entry_time = 2021-07-06 05:00:00+00:00
- exit_time = 2021-07-06 05:00:00+00:00
- entry_price = 110.775000000
- exit_price = 110.765228764
- lots = 518.77
- pnl_quote = -506902.42
- commission = 7262.78
- slippage = 0.000012040
- exit_reason = stop

Fatal XAUUSD fill before guards:

- symbol = XAUUSD
- side = buy
- entry_time = 2021-07-06 05:00:00+00:00
- exit_time = 2021-07-06 09:00:00+00:00
- entry_price = 1807.480000000
- exit_price = 1809.622000000
- lots = 0.02
- pnl_quote = 4.28
- commission = 0.40
- slippage = 0.000000000
- exit_reason = signal_flip

Root cause interpretation:

The fatal USDJPY event had pathological sizing caused by near-zero raw stop distance:

- raw H4 entry open = 110.770000000
- H017 long stop = 110.770240804

For a long trade, that stop was slightly above raw H4 entry open but below the cost-adjusted buy entry.

Before guards, event-engine sizing used:

abs(raw H4 entry open - stop_price)

before entry spread and without directional validation. That collapsed the sizing denominator and produced huge lots and commission.

This is not a data-preflight failure. It is a strategy/event-engine account-risk failure.

H017 remains failed.

Do not rerun broad strict real-data validation as a promotion attempt after guards.

## Current Code Structure Relevant To Next Work

In quantcore/backtest/h017_event.py, current interval loop now does:

- keeps current_equity;
- for each decision interval:
  - sets interval_start_equity;
  - builds interval_candidates list;
  - loops through _SYMBOLS;
  - calls _build_symbol_interval_candidate(...) for each symbol;
  - candidate build performs stop geometry, minimum stop distance, sizing, zero-lot filtering, and per-trade leverage validation;
  - collects all non-zero candidates;
  - calls _validate_maximum_portfolio_usd_gross_leverage(...);
  - only after portfolio guard passes, calls _build_symbol_interval_fill(...) for each candidate;
  - appends fills and sums interval P&L;
  - raises insolvency error if equity <= 0.

Current _build_symbol_interval_candidate(...) responsibilities:

- Reads signed risk fraction.
- Determines side.
- Reads stop price.
- Reads raw entry price and forced exit raw price.
- Validates directional stop.
- Computes raw stop distance.
- Validates minimum stop distance.
- Builds PositionSize.
- Returns None if lots zero.
- Validates per-trade maximum leverage.
- Computes notional_usd.
- Returns _SymbolIntervalCandidate.

Current _build_symbol_interval_fill(...) responsibilities:

- Accepts _SymbolIntervalCandidate.
- Builds execution-cost-adjusted entry fill.
- Calls simulate_bracket_trade.
- Builds exit cost.
- Computes P&L.
- Returns Fill.

Do not silently change fill rules, cost model, raw-entry sizing, stop validity, or P&L accounting.

## Recommended Next Path

After HANDOFF_47 hygiene verification, do not run real-data validation.

Recommended next sub-phase depends on what the user wants.

Reasonable next options:

1. Continue H018 risk hardening with one carefully chosen missing guard.
2. Decide whether a friction-burden cap is needed.
3. Decide whether broker margin model should be represented.
4. Create a diagnostic-only mode only if explicitly needed.
5. Inspect current code/tests for maintainability before any new guard.
6. If the user wants speed, pause governance and work only on implementation/test tasks.

Do not write a large decision record unless the decision is genuinely important.

Do not create docs just because a small implementation detail changed.

Potential next technical risk area:

Friction burden.

Reason:

The old fatal event included very large commission relative to equity due to huge lots. Current leverage and minimum-distance guards reduce that specific pathology, but there is still no explicit cap on projected spread + commission + slippage burden as a fraction of equity or risk.

However:

- Do not choose a threshold casually.
- Do not implement without inspecting current cost model APIs.
- Do not run real-data validation as a promotion attempt.

Before writing code that calls internal functions, inspect APIs with inspect.signature and dataclasses.fields.

## Absolute Do-Not Rules

Do not:

- Do not tune H017.
- Do not change H017 parameters.
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
- Do not change .gitignore from /data/ to data/.
- Do not run old scripts/run_h017_event_real.py as expanded validation.
- Do not treat source acceptance as H017 promotion.
- Do not treat future validation as live-trading approval.
- Do not silently fix the 518.77-lot event by tuning.
- Do not silently change raw versus executable entry sizing.
- Do not continue development while local commits are unpushed.
- Do not let git status go unread.
- Do not allow code-test count to drop below 558 without explicit test-removal phase.
- Do not call implemented guards H018 validation.
- Do not call accepted portfolio leverage policy H018 validation.
- Do not rerun broad strict validation after guards unless explicitly authorized as diagnostics or later H018 validation.
- Do not introduce trade skipping or clipping.
- Do not net long and short notionals for the portfolio gross leverage guard.
- Do not treat diagnostic-only continuation as implemented.
- Do not choose broker margin or friction-burden thresholds casually.
- Do not implement anything from H018_DECISION_RECORD_TEMPLATE.md; it is a template only.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

- .gitignore once had unrooted data/, which risked excluding quantcore/data.
- Some older commits missed files because git add was incomplete.
- An empty HANDOFF_16.md was accidentally committed once; verify handoff file size and preview before committing.
- A mistaken empty root-level HANDOFF_43.md was created during HANDOFF_43 and was not to be committed.
- Markdown code fences have been damaged by paste before; avoid nested markdown fences in command blocks.
- PowerShell does not support Linux heredocs.
- VS Code can keep unsaved buffers that overwrite edits.
- If terminal output shows command echo ambiguity, verify with Select-String or file previews before proceeding.
- Always inspect git status.
- Always push commits.
- Always verify git ls-files after commits.
- Treat code test-count drops as regressions.
- If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.
- If git commit says nothing to commit, immediately run recovery status/log/ls-files checks before continuing.
- Network/DNS push failures can happen; stop development until git push succeeds.
- git diff -- new_untracked_file.md shows nothing for an untracked file before it is added. Use Get-Content, git status, and git ls-files after commit.
- Handoff documents should be self-contained enough for a new AI to continue safely.
- For very long handoffs, use VS Code manual editing instead of a huge PowerShell here-string.
- A broad text replacement once accidentally inserted H018MaximumPortfolioGrossLeverageError into existing per-trade pytest.raises calls. Focused tests caught it. Verify targeted replacements with line-number previews.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after HANDOFF_47.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
- Current branch should be main.
- Latest expected commit should be Add handoff document #47 after H018 governance sync.
- Previous expected commit is daaa2b6 Sync H018 portfolio leverage guard governance docs.
- Current full-test anchor is 558 passed.
- Docs-only changes do not require full pytest by default under the updated workflow.
- Code changes still require focused tests and full pytest -q.
- H017 remains failed / not promotable / not live-approved.
- H018 remains not validated / not promotable / not live-approved.
- Live trading is not approved.
- Phase 4 execution work is not approved.
- Broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
- HistData is rejected for H017/H018 validation.
- No real-data rerun is authorized.
- Do not tune H017.
- Do not broaden symbols or add ML.
- H017EventInvalidStopError is implemented.
- H018MinimumStopDistanceError is implemented.
- H018MaximumPerTradeLeverageError is implemented.
- H018MaximumPortfolioGrossLeverageError is implemented.
- Raw-entry sizing and raw-entry directional stop validity are accepted and implemented.
- Portfolio-wide USD gross leverage guard is accepted and implemented.
- Portfolio gross leverage sums USD-converted gross notionals across candidate non-zero-lot trades and divides by interval-start equity.
- Long and short notionals must be summed gross and not netted.
- Portfolio-wide cap is 10.0x equity.
- Below 10.0 passes.
- Equality at 10.0 passes.
- Above 10.0 fails closed.
- Do not document every tiny change. Keep governance minimal and useful.
- First task is hygiene verification only. No code yet.

Please run:

cd C:\Users\equin\Documents\institutional-ea

.\.venv\Scripts\Activate.ps1

git status

git log --oneline -10

Then paste the full output.