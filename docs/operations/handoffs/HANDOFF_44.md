# HANDOFF 44 - After H018 Maximum Per-Trade Leverage Guard Implementation

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_44 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research: Python quantcore.
- Execution: MetaTrader 5 later.
- Production target: Oracle Cloud Always Free VPS later.
- Monitoring: self-hosted free-tier stack later.
- Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in .venv.
- No WSL.

## Non-Negotiable Workflow Rules

Use:

- Windows.
- PowerShell.
- VS Code.
- Python 3.12.10.
- .venv.
- No WSL.

Important PowerShell rule:

Do not use Linux/macOS heredoc syntax like python - <<'PY'. PowerShell does not support that.

Use PowerShell here-strings instead.

Workflow:

- Step-by-step.
- Numbered steps.
- Explicit Windows paths.
- Plain English.
- Define technical terms inline when needed.
- Never write code without saying exactly where the file goes and how to run it.
- One sub-phase per response.
- Never skip git commits.
- Never continue while local commits are unpushed.
- Always read git status.
- If tests pass but the count drops, treat it as a regression.
- Do not propose switching to another AI chat unless the user asks.
- For documentation-only phases, short copy-safe PowerShell blocks are preferred.
- Avoid giant command blocks when possible; VS Code manual file editing is acceptable for long handoff text.
- Avoid nested Markdown code fences inside PowerShell here-strings because copy/paste previously failed.
- For code or diagnostics, inspect APIs first and split cautiously.
- Before writing code that calls internal functions, inspect actual APIs with inspect.signature and dataclasses.fields.
- After each sub-phase, run focused tests if applicable, run full pytest -q, check status, commit, push, check status, run git ls-files on touched files/directories, and read the output.
- After each response, offer exactly:
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

Handoff folder:

C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs

Correct path for this handoff:

C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_44.md

Latest implementation commit before this handoff is committed:

9d062d8 Implement H018 maximum per-trade leverage guard

Expected handoff commit message after this file is committed:

Add handoff document #44 after H018 max leverage guard

Recent commits at the time this handoff was written:

9d062d8 Implement H018 maximum per-trade leverage guard
fffe81c Move all handoff documents into handoff folder
4b35a76 Add handoff folder and document #43 after H018 leverage policy acceptance
3c5c46a Accept H018 maximum per-trade leverage policy
de96b7a Add handoff document #42 after H018 minimum stop-distance guard
3ae9e18 Implement H018 minimum stop-distance guard
2c379fb Accept H018 minimum stop-distance policy
960f1be Add handoff document #41 after H018 fail closed policy acceptance
79799ec Accept H018 fail closed trade violation policy
2af283f Add H018 trade violation policy decision record draft

Known note:

There are duplicate consecutive HANDOFF_31 commits earlier in history. This is known and not blocking. Do not rewrite history.

## Test Anchors

Previous full-test anchor before H018 maximum leverage guard implementation:

545 passed

Focused H017 event test result after H018 maximum leverage guard implementation:

30 passed

Expected full-test anchor after H018 maximum leverage guard implementation:

552 passed

Reason:

- Previous full suite was 545 passed.
- Seven focused synthetic test cases were added.
- Therefore the expected full count is 552 passed.

Important:

The user pasted the successful focused result:

30 passed

The implementation commit was pushed cleanly.

If the next AI has any doubt about the full-suite result, the immediate first action must include pytest -q and the expected result is 552 passed.

Test-count rule:

If tests pass but the count drops below 552 without an explicit test-removal phase, treat it as a regression.

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
- Branch up to date with origin/main.
- Nothing to commit, working tree clean.

Expected latest commit after handoff commit:

Add handoff document #44 after H018 max leverage guard

Expected previous implementation commit:

9d062d8 Implement H018 maximum per-trade leverage guard

Expected tests:

552 passed

Read the output before continuing.

## Current Important Paths

Code:

C:\Users\equin\Documents\institutional-ea\quantcore
C:\Users\equin\Documents\institutional-ea\scripts
C:\Users\equin\Documents\institutional-ea\tests

Handoffs:

C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs

Important implementation files changed in latest implementation commit:

C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_event.py
C:\Users\equin\Documents\institutional-ea\tests\test_h017_event.py

Important docs:

C:\Users\equin\Documents\institutional-ea\README.md
C:\Users\equin\Documents\institutional-ea\docs\operations\HYPOTHESIS_LEDGER.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EXECUTION_SEMANTICS_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EXECUTION_SEMANTICS_DECISION_RECORD.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H017_NEAR_ZERO_STOP_DISTANCE_DIAGNOSTIC.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_BOUNDARY_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_BOUNDARY_DECISION_RECORD.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_SIZING_REFERENCE_DECISION_RECORD.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_MINIMUM_STOP_DISTANCE_DECISION_RECORD.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_TRADE_VIOLATION_POLICY_DECISION_RECORD.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_DECISION_MATRIX.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_CLAIM_SKELETON.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_DECISION_RECORD_TEMPLATE.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_DECISION_RECORD_INDEX.md

## Gitignore / Raw Data Rules

Important .gitignore rule:

The repo uses root-anchored:

/data/

Do not change it to unanchored:

data/

Reason:

An unanchored data/ rule previously risked excluding:

quantcore/data/

Raw data files under /data/ are gitignored and must not be committed.

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

- bars
- n_bars
- n_input_rows
- earliest_utc
- latest_utc
- broker_tz

Loaded bars shape verified:

- pandas DataFrame.
- DatetimeIndex.
- index name: dt.
- timezone: UTC.
- columns: open, high, low, close, volume.

Expanded broker-native raw exports are local and gitignored:

C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Reported exact MT5 symbols:

USDJPYm
XAUUSDm

Do not commit these raw files.

## Current Source Acceptance Status

Expanded broker-native USDJPY and XAUUSD M1/H4 data is conditionally accepted for H017/H018-style strict validation only under strict restrictions.

Accepted source:

Exness demo MT5 broker-native exports

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

Required bridge-window rule:

A common complete H4/M1 bridge window means:

1. USDJPY has a broker-native H4 bar at the H4 timestamp.
2. XAUUSD has a broker-native H4 bar at the same H4 timestamp.
3. For each symbol, the next H4 timestamp is exactly four hours later.
4. For each symbol, the M1 window has exactly 240 M1 bars.
5. No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

Do not treat 2018 through 2021-06 as dense M1 history. The expanded files have a sparse daily-like prefix before the dense M1 candidate region, which starts at 2021-07 for both symbols.

HistData remains rejected for H017 validation under current evidence.

Do not use HistData for H017 validation, H018 validation, tuning, or production dataset creation.

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
- For H4 bars: periods_per_year = 1512

Signals:

- Donchian breakout.
- Long: close[t] > max(high[t-N ... t-1])
- Short: close[t] < min(low[t-N ... t-1])
- Channel uses prior N bars via shift(1).rolling(N).

H017:

- Inner-joins USDJPY and XAUUSD timestamps.
- Computes close-to-close returns.
- Uses same returns for vol targeting and heat governor.
- Position is signed risk exposure: signal * per_trade_risk * vol_mult * heat_mult

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

Any future raw-entry versus executable-entry sizing decision must be explicit, tested, documented, and treated as execution-model semantics, not tuning.

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
- risk_per_lot_usd is converted through quote_pnl_to_usd.
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

- XAUUSD quote currency is USD, so pnl_quote is already USD.
- USDJPY quote currency is JPY, so pnl_jpy / usdjpy_price converts to USD.

## Implemented Guards At This Handoff

### Raw-Entry Invalid-Stop Execution Guard

Implemented before this handoff in:

quantcore/backtest/h017_event.py

Error class:

H017EventInvalidStopError

Under current raw-entry sizing semantics:

- Long/buy stop must be below raw H4 entry open.
- Short/sell stop must be above raw H4 entry open.
- Equality is invalid.
- Long/buy stop equal to raw H4 entry open fails closed.
- Short/sell stop equal to raw H4 entry open fails closed.
- Invalid directional stop geometry fails closed.
- Invalid directional stops are not skipped silently.
- Invalid directional stops are not clipped.

This guard does not promote H017.

This guard does not authorize a real-data rerun.

### H018 Minimum Stop-Distance Guard

Accepted in commit:

2c379fb Accept H018 minimum stop-distance policy

Implemented in commit:

3ae9e18 Implement H018 minimum stop-distance guard

Implemented in:

quantcore/backtest/h017_event.py

Error class:

H018MinimumStopDistanceError

Accepted H018 minimum stop-distance rule:

raw_stop_distance = abs(raw_h4_entry_open - stop_price)

minimum_stop_distance = one modeled spread for the symbol

The modeled spread is read from:

quantcore.backtest.cost_model.get_default_cost_spec(symbol).spread_price

Current thresholds:

- USDJPY: 0.01
- XAUUSD: 0.30

Boundary behavior:

- raw_stop_distance < minimum_stop_distance -> fail closed.
- raw_stop_distance == minimum_stop_distance -> pass this guard.
- raw_stop_distance > minimum_stop_distance -> pass this guard.

Implementation placement:

- The guard runs after _validate_directional_stop.
- The guard runs after stop_distance_price is computed from raw H4 entry open and stop price.
- The guard runs before size_position_from_risk.

Important implementation detail:

The implementation uses math.isclose with rel_tol=1e-12 and abs_tol=1e-12 so floating-point representation of exact boundary cases does not accidentally fail when it is effectively equal to the threshold.

Audit fields on H018MinimumStopDistanceError:

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

Policy accepted in commit:

3c5c46a Accept H018 maximum per-trade leverage policy

Implemented in commit:

9d062d8 Implement H018 maximum per-trade leverage guard

Files changed:

- quantcore/backtest/h017_event.py
- tests/test_h017_event.py

Implemented error class:

H018MaximumPerTradeLeverageError

Implemented constant:

_MAXIMUM_PER_TRADE_USD_GROSS_LEVERAGE = 10.0

Implemented helper:

_position_notional_usd(...)

Implemented validator:

_validate_maximum_per_trade_usd_gross_leverage(...)

Accepted and implemented rule name:

per_trade_usd_gross_leverage_at_or_below_10x_equity

Accepted and implemented rule:

A single trade may not create more than 10 times account equity in USD-converted gross notional exposure.

Measurement:

gross_leverage = notional_usd / equity_usd

Threshold:

10.0

Boundary behavior:

- gross_leverage < 10.0 passes.
- gross_leverage == 10.0 passes.
- gross_leverage > 10.0 fails closed.

Violation policy:

- Raise explicit H018MaximumPerTradeLeverageError.
- Do not silently skip the trade.
- Do not clip the position size.
- Do not warn and continue.
- Do not log-only continue.
- Do not convert the run into a promotable validation result.

Instrument handling:

XAUUSD:

- PositionSize.notional_quote is already USD-denominated because quote currency is USD.
- notional_usd = position_size.notional_quote

USDJPY:

- PositionSize.notional_quote is JPY-denominated because quote currency is JPY.
- USDJPY price is JPY per 1 USD.
- notional_usd = position_size.notional_quote / entry_raw_price
- This follows the existing project convention used by quote_pnl_to_usd for JPY quote-currency conversion.

Implemented placement in _build_symbol_interval_fill:

1. Validate raw-entry directional stop geometry.
2. Validate minimum raw stop distance.
3. Compute preliminary PositionSize with size_position_from_risk.
4. If lots are zero, return None as before.
5. Validate maximum per-trade USD gross leverage.
6. Only then build the execution-cost-adjusted entry fill.

The guard runs before any fill is created for the violating trade.

Audit fields on H018MaximumPerTradeLeverageError:

- rule_name = per_trade_usd_gross_leverage_at_or_below_10x_equity
- symbol
- side
- decision_time
- entry_time
- entry_raw_price
- stop_price
- raw_stop_distance
- equity_usd
- lots
- contract_size
- quote_currency
- notional_quote
- notional_usd
- gross_leverage
- maximum_gross_leverage = 10.0
- threshold_basis = per_trade_usd_gross_notional_divided_by_equity
- validation_action = fail_closed

Implementation uses math.isclose with rel_tol=1e-12 and abs_tol=1e-12 so floating-point representation of exact boundary cases does not accidentally fail when effectively equal to 10.0.

## Tests Added Or Repaired In Commit 9d062d8

New focused synthetic tests added in tests/test_h017_event.py:

1. USDJPY below 10.0x passes.
2. USDJPY exactly 10.0x passes.
3. XAUUSD below 10.0x passes.
4. XAUUSD exactly 10.0x passes.
5. USDJPY above 10.0x fails closed.
6. XAUUSD above 10.0x fails closed.
7. Fail-closed error audit fields are preserved.

Focused test result after repair:

30 passed

Existing tests repaired because the new max-leverage guard correctly invalidated old over-leveraged synthetic fixtures:

1. test_interval_ruin_raises_clear_insolvency_error
   - Changed from extreme XAUUSD buy to synthetic XAUUSD sell.
   - New short stop is 4000.0 from entry 2000.0.
   - This keeps initial gross notional under 10x while still producing insolvency by a large adverse stop move.
   - Expected fill side changed from buy to sell.
   - Expected lots changed from 20.0 to 0.1.

2. test_h018_minimum_stop_distance_at_or_above_one_spread_passes_guard
   - Synthetic risk fractions for boundary pass cases were reduced so the test remains about minimum-distance behavior and does not accidentally violate the new maximum-leverage guard.

Important interpretation:

These test repairs do not weaken the guard.

They isolate old test intent from the newly implemented leverage policy.

## H018 Current Governance Status

H018 is not yet a fully validated strategy.

H018 is not promotable.

H018 does not approve live trading.

H018 does not approve Phase 4 execution.

Accepted and implemented H018-related code so far:

1. H017EventInvalidStopError.
2. Raw-entry directional stop validation.
3. H018MinimumStopDistanceError.
4. _validate_minimum_stop_distance.
5. H018MaximumPerTradeLeverageError.
6. _position_notional_usd.
7. _validate_maximum_per_trade_usd_gross_leverage.
8. Event-engine integration of max leverage guard after preliminary sizing and before fill creation.

Accepted H018 policy decisions so far:

1. H018 validation-mode guard violations fail closed.
2. H018 minimum stop-distance rule:
   - raw_stop_distance must be greater than or equal to one modeled spread for the symbol.
   - USDJPY threshold is 0.01.
   - XAUUSD threshold is 0.30.
   - below threshold fails closed.
   - equality passes this guard.
   - above threshold passes this guard.
3. H018 maximum per-trade USD gross leverage rule:
   - gross_leverage = notional_usd / equity_usd.
   - maximum gross leverage is 10.0.
   - below 10.0 passes.
   - equality at 10.0 passes.
   - above 10.0 fails closed.
   - XAUUSD notional_quote is USD.
   - USDJPY notional_quote is converted to USD by dividing by entry_raw_price.
4. Skip trade is rejected for first H018 validation-mode implementation.
5. Position clipping is rejected for first H018 validation-mode implementation.
6. Warn-and-continue is rejected.
7. Log-only continuation is rejected for validation mode.
8. Diagnostic-only continuation is deferred to a separately labeled diagnostic mode.

Still not chosen:

- No executable-entry sizing rule.
- No stop-validity reference final decision beyond current raw-entry guard behavior.
- No real-data rerun classification beyond not authorized by current policies.
- No formal H018 claim.
- No portfolio-wide leverage cap.
- No broker margin model.
- No friction-burden cap.

Still not authorized:

- No real-data validation rerun.
- No H018 claim.
- No live trading.
- No Phase 4 execution.

## Strict Expanded Broker-Native Validation Result

Script:

scripts/run_h017_strict_event_real.py

The strict bridge-window preflight passed.

Strict bridge-window preflight:

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

Fatal USDJPY fill before invalid-stop and H018 guards:

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

Fatal XAUUSD fill before invalid-stop and H018 guards:

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

Important:

Do not rerun broad strict real-data validation as a promotion attempt after the invalid-stop guard, minimum-distance guard, or maximum-leverage guard.

Any rerun must be explicitly authorized as diagnostics only or as a later H018 validation attempt after all required gates are satisfied.

H017 remains failed unless a separate governance phase says otherwise.

## Interpretation Of The Insolvency Result

This is not a data preflight failure.

This is not a missing-M1 problem.

The fatal interval was a complete strict bridge window.

The fatal event was caused by event-engine execution reaching account ruin after a pathological USDJPY size:

518.77 lots

Prior diagnostics localized the sizing pathology to a near-zero raw stop distance:

- raw H4 entry open = 110.770000000
- H017 long stop = 110.770240804

For a long trade, that stop was slightly above the raw H4 entry open but below the cost-adjusted buy entry.

Before the invalid-stop guard, event-engine sizing used:

abs(raw H4 entry open - stop_price)

before entry spread was applied and without directional validation.

This collapsed the sizing denominator and caused huge lots and huge commission.

Now:

1. The invalid-stop guard fails closed on invalid raw-entry directional stop geometry.
2. The H018 minimum stop-distance guard fails closed on directionally valid raw stop distances smaller than one modeled spread.
3. The H018 maximum per-trade USD gross leverage guard fails closed on remaining directionally valid but over-leveraged trades after preliminary sizing.

These changes do not erase the original H017 validation failure.

Do not silently fix this by tuning H017 or changing costs.

## Recommended Next Path

After HANDOFF_44 hygiene verification, the next AI should not immediately run real-data validation.

Recommended next sub-phase:

Phase 3.26-ch - Post-implementation documentation and governance sync for H018 max leverage guard

Safe outline:

1. Read git status.
2. Run git log --oneline -10.
3. Run pytest -q and confirm 552 passed.
4. Inspect docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md.
5. Inspect docs/operations/H018_DECISION_RECORD_INDEX.md.
6. Decide whether the implementation commit already satisfies the accepted policy documentation or whether a short documentation sync is needed.
7. If docs are changed, run tests, commit, push, verify status and git ls-files.
8. Do not run broad real-data validation yet.
9. Do not call H018 validated or promotable.

Possible later path after docs sync:

- Decide next missing H018 gate explicitly.
- Candidate gates still include:
  - executable-entry sizing semantics,
  - stop-validity reference final decision,
  - formal H018 claim definition,
  - diagnostic-only versus validation-mode run classification,
  - portfolio-wide leverage cap,
  - broker margin model,
  - friction-burden cap.

Do not create more broad draft-only decision records unless there is a concrete missing gate.

## Absolute Do-Not Rules At HANDOFF_44

Do not:

- Do not tune H017.
- Do not change H017 parameters.
- Do not change the cost model casually.
- Do not add ML.
- Do not broaden to more symbols.
- Do not start Phase 4 execution.
- Do not live trade.
- Do not use HistData for H017 validation.
- Do not use HistData for H018 validation.
- Do not accept HistData as a research source.
- Do not build HistData H4 for H017/H018 validation.
- Do not combine broker H4 with HistData M1.
- Do not use sparse 2018 through 2021-06 broker-native prefix as dense M1.
- Do not include incomplete H4/M1 windows.
- Do not use any bridge window where either symbol has fewer or more than exactly 240 M1 bars.
- Do not impute missing M1 bars.
- Do not forward-fill or backfill M1 bars.
- Do not synthesize bars.
- Do not modify raw broker files.
- Do not commit raw MT5 CSV files.
- Do not commit raw HistData files.
- Do not change .gitignore from /data/ to data/.
- Do not run old scripts/run_h017_event_real.py as expanded validation.
- Do not filter H4 to accepted timestamps only.
- Do not ignore the accepted timestamp gaps found in the contiguity diagnostic.
- Do not treat source acceptance as H017 promotion.
- Do not treat future validation as live-trading approval.
- Do not ignore the previous -33.65 percent drawdown.
- Do not ignore the strict expanded insolvency event.
- Do not silently fix the 518.77-lot event by tuning.
- Do not silently change raw versus executable entry sizing without tests and docs.
- Do not continue development while local commits are unpushed.
- Do not let git status go unread.
- Do not skip full pytest.
- Do not allow test count to drop below 552 without explicit test-removal phase.
- Do not call the raw-entry invalid-stop guard H017 promotion.
- Do not call the H018 minimum stop-distance guard H017 promotion.
- Do not call the H018 maximum leverage guard H018 validation.
- Do not call H018 governance plans H017 or H018 promotion.
- Do not rerun broad strict validation after guards unless explicitly authorized as diagnostics or later H018 validation.
- Do not introduce trade skipping or clipping; accepted validation-mode policy rejects both for first implementation.
- Do not implement executable-entry sizing before a decision record chooses the rule.
- Do not treat near-zero stop-distance behavior as fully solved for production; H018 is still not validated.
- Do not treat H018 as live-approved.
- Do not treat H018 as validated.
- Do not choose thresholds casually.
- Do not use real-data reruns as a tuning loop.
- Do not create more broad draft-only decision records unless there is a concrete missing gate.
- Do not implement anything from H018_DECISION_RECORD_TEMPLATE.md; it is a template only.
- Do not treat H018_DECISION_RECORD_INDEX.md as a full policy decision by itself.
- Do not treat H018_BOUNDARY_DECISION_RECORD.md as accepted; it is Draft.
- Do not treat H018_SIZING_REFERENCE_DECISION_RECORD.md as accepted; it is Draft.
- Do not treat accepted/implemented maximum leverage policy as authorizing real-data validation.

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
- Always run tests.
- Always inspect git status.
- Always push commits.
- Always verify git ls-files after commits.
- Treat test-count drops as regressions.
- If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.
- If git commit says nothing to commit, immediately run recovery status/log/ls-files checks before continuing.
- When two identical code blocks exist in one file, use function-boundary replacement, not first global text match.
- Long pasted PowerShell blocks can be corrupted by chat formatting; prefer shorter blocks or VS Code manual edits for long documents.
- tests/test_h017_event.py has a UTF-8 BOM; when programmatically editing it, use utf-8-sig.
- quantcore/backtest/h017_event.py also has a UTF-8 BOM; when programmatically reading it for ast or edits, use utf-8-sig.
- A previous documentation sync appeared to fail in terminal output but had actually committed; when output is inconsistent, immediately perform read-only verification before proceeding.
- Network/DNS push failures can happen; stop development until git push succeeds.
- git diff -- new_untracked_file.md shows nothing for an untracked file before it is added. Use Get-Content, git status, and git ls-files after commit.
- Handoff documents should be self-contained enough for a new AI to continue safely.
- For very long handoffs, use VS Code manual editing instead of a huge PowerShell here-string.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after HANDOFF_44.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
- Current expected full-test anchor is 552 passed.
- Latest expected implementation commit before handoff is 9d062d8 Implement H018 maximum per-trade leverage guard.
- Expected handoff commit after this file is Add handoff document #44 after H018 max leverage guard.
- Handoff files live in docs/operations/handoffs.
- H017 remains failed / not promotable / not live-approved.
- H018 remains not validated / not promotable / not live-approved.
- Live trading is not approved.
- Phase 4 execution work is not approved.
- Broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
- The strict expanded broker-native validation originally failed by insolvency after a pathological 518.77-lot USDJPY trade.
- H017EventInvalidStopError is implemented.
- H018MinimumStopDistanceError is implemented.
- H018MaximumPerTradeLeverageError is implemented.
- Under current raw-entry sizing semantics, long/buy stops must be below raw H4 entry open and short/sell stops must be above raw H4 entry open.
- Equality is invalid for directional stop geometry.
- Invalid directional stop geometry fails closed.
- The H018 minimum stop-distance rule is raw_stop_distance >= one modeled spread for the symbol.
- USDJPY minimum raw-entry stop distance is 0.01.
- XAUUSD minimum raw-entry stop distance is 0.30.
- Below threshold fails closed.
- Equality passes the minimum-distance guard.
- Above threshold passes the minimum-distance guard.
- The H018 maximum per-trade USD gross leverage rule is implemented.
- The max leverage rule is notional_usd / equity_usd <= 10.0.
- XAUUSD PositionSize.notional_quote is already USD.
- USDJPY PositionSize.notional_quote is converted to USD by dividing by entry_raw_price.
- gross_leverage < 10.0 passes.
- gross_leverage == 10.0 passes.
- gross_leverage > 10.0 fails closed.
- Skip trade is rejected for first H018 validation-mode implementation.
- Position clipping is rejected for first H018 validation-mode implementation.
- Warn-and-continue is rejected.
- Log-only continuation is rejected for validation mode.
- Diagnostic-only continuation is deferred to a separately labeled diagnostic mode.
- No executable-entry sizing rule has been chosen.
- No real-data rerun is authorized.
- No H018 claim has been accepted.
- Do not tune H017.
- Do not use HistData.
- Do not broaden symbols or add ML.
- Do not start Phase 4.
- Recommended next logical sub-phase is hygiene verification, then possible post-implementation documentation/governance sync.
- First task is hygiene verification only. No new code yet.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10
pytest -q

Then paste the full output.
