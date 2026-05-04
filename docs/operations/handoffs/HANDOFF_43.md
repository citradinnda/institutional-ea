HANDOFF 43 - After H018 Maximum Per-Trade Leverage Policy Acceptance And Handoff Folder Repair

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_43 wins.

Project Identity

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
- No Linux/macOS shell assumptions.

Non-Negotiable Workflow Rules

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

Tone and workflow:

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

Repository State At This Handoff

Repository root:

C:\Users\equin\Documents\institutional-ea

Virtual environment:

C:\Users\equin\Documents\institutional-ea\.venv

Branch:

main

GitHub remote:

https://github.com/citradinnda/institutional-ea.git

Latest expected commit before this HANDOFF_43 document is committed:

3c5c46a Accept H018 maximum per-trade leverage policy

Expected latest commit after this handoff is committed:

Add handoff folder and document #43 after H018 leverage policy acceptance

Important repository organization change in this handoff commit:

- Existing tracked handoff files are moved from docs/operations/HANDOFF_*.md into docs/operations/handoffs/HANDOFF_*.md.
- The correct path for this handoff is docs/operations/handoffs/HANDOFF_43.md.
- A mistaken empty root-level HANDOFF_43.md was created during the prior attempt and must not be committed. It should be deleted before committing this handoff.

Recent commits at the time this handoff was written:

3c5c46a Accept H018 maximum per-trade leverage policy
de96b7a Add handoff document #42 after H018 minimum stop-distance guard
3ae9e18 Implement H018 minimum stop-distance guard
2c379fb Accept H018 minimum stop-distance policy
960f1be Add handoff document #41 after H018 fail closed policy acceptance
79799ec Accept H018 fail closed trade violation policy
2af283f Add H018 trade violation policy decision record draft
9dedd4f Add H018 maximum notional leverage decision record draft
876ccb9 Add handoff document #40 after H018 minimum stop-distance draft
dbc569e Add H018 minimum stop-distance decision record draft

Known note:

There are duplicate consecutive HANDOFF_31 commits earlier in history. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

545 passed

Previous full-test anchor before H018 minimum stop-distance guard implementation was:

537 passed

The increase to 545 is expected because new focused synthetic tests were added.

Focused H017 event test anchor after H018 minimum stop-distance guard:

23 passed

Important test-count rule:

Current correct full-test anchor is 545 passed.

If tests pass but the count drops below 545 without a deliberate test-removal phase, treat it as a regression.

Immediate First Action For The Next AI

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

Add handoff folder and document #43 after H018 leverage policy acceptance

Expected previous commit:

3c5c46a Accept H018 maximum per-trade leverage policy

Expected tests:

545 passed

Read the output before continuing.

Current Important Paths

Code:

C:\Users\equin\Documents\institutional-ea\quantcore
C:\Users\equin\Documents\institutional-ea\scripts
C:\Users\equin\Documents\institutional-ea\tests

Handoff folder after this commit:

C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs

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

Gitignore / Raw Data Rules

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

MT5 / Broker Data State

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

Expanded Broker-Native Source Diagnostics Summary

Loader timestamp-shape diagnostic:

USDJPY M1:

- n_input_rows: 1785312
- n_bars: 1785312
- earliest_utc: 2018-07-02 21:00:00+00:00
- latest_utc: 2026-04-30 07:00:00+00:00
- duplicate_timestamps_after_load: 0

USDJPY H4:

- n_input_rows: 8713
- n_bars: 8713
- earliest_utc: 2018-07-02 21:00:00+00:00
- latest_utc: 2026-04-30 05:00:00+00:00
- duplicate_timestamps_after_load: 0

XAUUSD M1:

- n_input_rows: 1704907
- n_bars: 1704907
- earliest_utc: 2018-06-27 21:00:00+00:00
- latest_utc: 2026-04-30 07:00:00+00:00
- duplicate_timestamps_after_load: 0

XAUUSD H4:

- n_input_rows: 8658
- n_bars: 8658
- earliest_utc: 2018-06-27 21:00:00+00:00
- latest_utc: 2026-04-30 05:00:00+00:00
- duplicate_timestamps_after_load: 0

Coverage-density diagnostic:

The expanded files have a sparse daily-like prefix from 2018 through 2021-06.

The dense M1 candidate region starts at 2021-07 for both symbols.

Do not treat 2018 through 2021-06 as dense M1 history.

H4/M1 aggregation compatibility diagnostic:

On every fully covered comparable H4 window, broker-native M1 aggregation exactly reproduced broker-native H4 OHLCV.

USDJPY:

- compared_full_m1_windows: 5701
- matched_bars: 5701
- mismatched_bars: 0
- first_full_m1_window_utc: 2021-07-02 13:00:00+00:00
- last_full_m1_window_utc: 2026-04-30 01:00:00+00:00

XAUUSD:

- compared_full_m1_windows: 6149
- matched_bars: 6149
- mismatched_bars: 0
- first_full_m1_window_utc: 2021-07-02 13:00:00+00:00
- last_full_m1_window_utc: 2026-04-30 01:00:00+00:00

Cross-symbol common-window diagnostic:

Common M1 span:

2021-07-01 21:00:00+00:00 through 2026-04-30 07:00:00+00:00

Common complete H4/M1 windows:

- common_complete_h4_m1_windows: 5476
- first_common_complete_h4_window_utc: 2021-07-02 13:00:00+00:00
- last_common_complete_h4_window_utc: 2026-04-30 01:00:00+00:00

Current Source Acceptance Status

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

HistData State

HistData remains rejected for H017 validation under current evidence.

Current statuses:

- HistData as H017 validation source: rejected under current evidence.
- HistData as accepted research source: not accepted.
- HistData-built H4: not accepted.
- Broker H4 plus HistData M1 hybrid: not accepted.
- Derived HistData files: not authorized.
- H017 validation on HistData: not authorized.
- Broker-native expanded source is conditionally accepted for strict validation only.
- H017 status is failed/not promotable after strict expanded broker-native insolvency result.

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

Strategy / Validation Background

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

Core Strategy Conventions

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

Event-Driven Backtest Conventions

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

Current Portfolio API From Inspection

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

Default instrument specs inspected:

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

Representative current sizing examples from read-only inspection:

USDJPY with 10000 USD equity, entry 150.0, stop distance 1.0:

- lots = 0.15
- notional_quote = 2250000.0 JPY
- notional_usd_estimate = 15000.0
- gross_leverage_estimate = 1.5

USDJPY with 10000 USD equity, entry 150.0, stop distance 0.01:

- lots = 15.0
- notional_quote = 225000000.0 JPY
- notional_usd_estimate = 1500000.0
- gross_leverage_estimate = 150.0

XAUUSD with 10000 USD equity, entry 2000.0, stop distance 10.0:

- lots = 0.10
- notional_quote = 20000.0 USD
- notional_usd_estimate = 20000.0
- gross_leverage_estimate = 2.0

XAUUSD with 10000 USD equity, entry 2000.0, stop distance 0.30:

- lots = 3.33
- notional_quote = 666000.0 USD
- notional_usd_estimate = 666000.0
- gross_leverage_estimate = 66.6

Important interpretation:

The H018 minimum stop-distance guard blocks sub-spread denominators, but a trade exactly one spread away can still create extreme gross leverage. Therefore maximum per-trade leverage protection is still required before any future H018 real-data validation attempt.

Raw-Entry Invalid-Stop Execution Guard

Implemented in:

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

H018 Minimum Stop-Distance Policy

Accepted in commit:

2c379fb Accept H018 minimum stop-distance policy

Implemented in commit:

3ae9e18 Implement H018 minimum stop-distance guard

Files changed by implementation:

- quantcore/backtest/h017_event.py
- tests/test_h017_event.py

Error class:

H018MinimumStopDistanceError

Implemented in:

quantcore/backtest/h017_event.py

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

Validation-mode policy:

- Fail closed.
- Do not skip.
- Do not clip.
- Do not warn-and-continue.
- Do not log-only continue.

Focused tests added in tests/test_h017_event.py:

- test_h018_minimum_stop_distance_long_below_one_spread_fails_closed
- test_h018_minimum_stop_distance_short_below_one_spread_fails_closed
- test_h018_minimum_stop_distance_at_or_above_one_spread_passes_guard

Focused test result after implementation:

23 passed

Full test result after implementation:

545 passed

Important interpretation:

This implementation does not promote H017.

This implementation does not validate H018.

This implementation does not authorize a real-data rerun.

This implementation does not approve live trading.

This implementation does not approve Phase 4 execution.

H018 Maximum Per-Trade USD Gross Leverage Policy

Accepted in commit:

3c5c46a Accept H018 maximum per-trade leverage policy

Decision record:

docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md

Index:

docs/operations/H018_DECISION_RECORD_INDEX.md

Status:

Accepted for implementation.

Not yet implemented at the time this handoff was written.

Accepted rule name:

per_trade_usd_gross_leverage_at_or_below_10x_equity

Accepted rule:

A single trade may not create more than 10 times account equity in USD-converted gross notional exposure.

Measurement:

gross_leverage = notional_usd / equity_usd

Threshold:

10.0

Boundary behavior:

1. gross_leverage < 10.0 passes.
2. gross_leverage == 10.0 passes.
3. gross_leverage > 10.0 fails closed.

Violation policy:

- Raise an explicit H018 maximum leverage violation error.
- Do not silently skip the trade.
- Do not clip the position size.
- Do not warn and continue.
- Do not log-only continue.
- Do not convert the run into a promotable validation result.

Instrument handling:

XAUUSD:

- Current PositionSize.notional_quote is already USD-denominated because quote currency is USD.
- notional_usd = position_size.notional_quote

USDJPY:

- Current PositionSize.notional_quote is JPY-denominated because quote currency is JPY.
- USDJPY price is JPY per 1 USD.
- notional_usd = position_size.notional_quote / entry_raw_price
- This follows the existing project convention used by quote_pnl_to_usd for JPY quote-currency conversion.

Accepted implementation placement:

The guard must run after preliminary position sizing because it requires computed lot size and notional.

In the event engine, intended placement is:

1. Validate raw-entry directional stop geometry.
2. Validate minimum raw stop distance.
3. Compute preliminary PositionSize with size_position_from_risk.
4. Validate maximum per-trade USD gross leverage.
5. Only then build the execution-cost-adjusted entry fill.

The guard must run before any fill is created for the violating trade.

Required audit fields:

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

Required synthetic tests before or with implementation:

1. USDJPY below 10.0x passes.
2. USDJPY exactly 10.0x passes.
3. USDJPY above 10.0x fails closed.
4. XAUUSD below 10.0x passes.
5. XAUUSD exactly 10.0x passes.
6. XAUUSD above 10.0x fails closed.
7. Fail-closed error audit fields are preserved.
8. Existing raw-entry invalid-stop behavior remains unchanged.
9. Existing H018 minimum stop-distance behavior remains unchanged.
10. Full pytest count must not drop below current 545-test anchor unless an explicit test-removal phase exists.

Rejected alternatives for first implementation:

- No maximum exposure guard.
- Broker-lot cap only.
- Quote-currency notional cap without USD conversion.
- Position clipping.
- Trade skipping.
- Warn-and-continue.
- Log-only continuation.
- Diagnostic-only continuation for validation mode.

Diagnostic-only continuation is deferred to a separately labeled diagnostic mode.

Real-data run classification:

This decision does not authorize a real-data rerun.

After implementation, any real-data run must be classified as one of:

1. Diagnostic-only run.
2. H018 validation run after a formal H018 claim exists.

A run after this implementation must not be described as H017 promotion.

A passing run after this implementation would not automatically validate H018.

A passing run after this implementation would not approve live trading.

A passing run after this implementation would not approve Phase 4 execution.

H018 Current Governance Status

H018 is not yet a fully implemented strategy.

H018 is not validated.

H018 is not promotable.

H018 does not approve live trading.

H018 does not approve Phase 4 execution.

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

Implemented H018-related code so far:

1. H018MinimumStopDistanceError.
2. _validate_minimum_stop_distance.
3. Integration in _build_symbol_interval_fill after directional stop validation and before sizing.
4. Focused synthetic tests for below, equal, and above threshold behavior.

Not yet implemented:

1. H018 maximum per-trade USD gross leverage error class.
2. H018 maximum per-trade USD gross leverage validator.
3. H018 maximum per-trade USD gross leverage integration after size_position_from_risk.
4. H018 maximum per-trade USD gross leverage focused synthetic tests.

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

Strict Expanded Broker-Native Validation Result

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

Research verdict printed by the runner before invalid-stop and H018 guards:

- STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True
- H017 STRICT EVENT BACKTEST COMPLETED: False
- H017 VALIDATION FAILED BY INSOLVENCY: True
- H017 PROMOTABLE BY CLAIM: False
- EXPANDED VALIDATION IS RESEARCH EVIDENCE ONLY: True
- LIVE TRADING APPROVED: False

Important:

Do not rerun broad strict real-data validation as a promotion attempt after the invalid-stop guard, minimum-distance guard, or future maximum-leverage guard.

Any rerun must be explicitly authorized as diagnostics only or as a later H018 validation attempt after all required gates are satisfied.

H017 remains failed unless a separate governance phase says otherwise.

Interpretation Of The Insolvency Result

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

The invalid-stop guard now fails closed on this class of raw-entry directional stop geometry.

The H018 minimum stop-distance guard now also fails closed on directionally valid raw stop distances smaller than one modeled spread.

The accepted H018 maximum per-trade USD gross leverage policy is designed to block remaining directionally valid but over-leveraged trades after preliminary sizing.

These changes do not erase the original H017 validation failure.

Do not silently fix this by tuning H017 or changing costs.

Work Completed Since HANDOFF_42

Commit 3c5c46a - Accept H018 maximum per-trade leverage policy

Files changed:

- docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_RECORD.md
- docs/operations/H018_DECISION_RECORD_INDEX.md

Accepted:

- maximum per-trade USD gross leverage is 10.0x equity.
- exposure basis is notional_usd / equity_usd.
- XAUUSD notional_quote is treated as USD.
- USDJPY notional_quote is converted to USD by dividing by entry_raw_price.
- gross_leverage < 10.0 passes.
- gross_leverage == 10.0 passes.
- gross_leverage > 10.0 fails closed.
- no skip.
- no clipping.
- no warn-and-continue.
- no log-only continuation.
- diagnostic-only continuation deferred.
- no real-data rerun authorization.
- no H017 promotion.
- no H018 validation.
- no live approval.
- no Phase 4 approval.

Full tests:

545 passed

Commit was pushed.

Current handoff commit should also:

- move tracked prior handoff files into docs/operations/handoffs.
- delete mistaken empty root HANDOFF_43.md if present.
- add docs/operations/handoffs/HANDOFF_43.md.
- repair stale H018_DECISION_RECORD_INDEX.md rows that still said maximum notional/leverage was Draft.

Recommended Next Path

After HANDOFF_43 hygiene verification, the next AI should implement the accepted H018 maximum per-trade USD gross leverage guard.

Do not create another broad draft-only document by default.

Recommended next sub-phase:

Phase 3.26-cg - Implement H018 maximum per-trade USD gross leverage guard

Safe implementation outline:

1. Read git status.
2. Inspect quantcore/backtest/h017_event.py around:
   - imports
   - H017EventInvalidStopError
   - H018MinimumStopDistanceError
   - _build_symbol_interval_fill
   - _validate_directional_stop
   - _validate_minimum_stop_distance
3. Inspect quantcore/backtest/portfolio.py:
   - InstrumentSpec
   - PositionSize
   - get_default_instrument_spec
   - quote_pnl_to_usd
   - size_position_from_risk
4. Inspect tests/test_h017_event.py.
5. Preserve UTF-8 BOM behavior if programmatically editing tests/test_h017_event.py or quantcore/backtest/h017_event.py. Use utf-8-sig if needed.
6. Add H018MaximumPerTradeLeverageError in quantcore/backtest/h017_event.py.
7. Add helper to compute notional_usd from PositionSize.notional_quote:
   - if quote_currency == USD, use notional_quote.
   - if quote_currency == JPY, divide by entry_raw_price.
   - unknown quote currency should fail loudly.
8. Add _validate_maximum_per_trade_usd_gross_leverage.
9. Call it after size_position_from_risk and after zero-lot check, before cost-adjusted entry fill construction.
10. Add focused synthetic tests:
    - USDJPY below 10.0x passes.
    - USDJPY exactly 10.0x passes.
    - USDJPY above 10.0x fails closed.
    - XAUUSD below 10.0x passes.
    - XAUUSD exactly 10.0x passes.
    - XAUUSD above 10.0x fails closed.
    - Audit fields are preserved.
11. Run focused H017 event tests.
12. Run full pytest -q.
13. Verify test count is at least 545 and likely higher.
14. Commit.
15. Push.
16. Verify git status, git log, and git ls-files.

Potential test construction notes:

For XAUUSD with equity 10000 and entry 2000:

- 10.0x means notional_usd <= 100000.
- XAUUSD notional = lots * 100 * 2000.
- lots 0.50 gives 100000 notional and exactly 10.0x.
- With target risk 100 USD and stop distance 2.0:
  risk_per_lot = 2.0 * 100 = 200 USD.
  raw lots = 100 / 200 = 0.50.
  This creates exactly 10.0x.

For XAUUSD above 10.0x:

- stop distance smaller than 2.0 but still above minimum 0.30 can create more than 0.50 lots.
- Example stop distance 1.0 gives 1.00 lot, 200000 USD notional, 20.0x.

For USDJPY with equity 10000 and entry 150:

- 10.0x means notional_usd <= 100000.
- USDJPY notional_usd = lots * 100000 because notional_quote / entry_price = lots * contract_size.
- lots 1.00 gives 100000 USD notional and exactly 10.0x.
- With target risk 100 USD and entry 150, risk_per_lot_usd = stop_distance * 100000 / 150.
- To get 1.00 lot at 100 USD target, stop_distance = 0.15.
- USDJPY stop distance 0.15 is above minimum 0.01.
- For above 10.0x, stop distance 0.10 gives 1.50 lots and 15.0x.

These are examples for focused synthetic tests only; inspect actual existing test helpers before coding.

Absolute Do-Not Rules At HANDOFF_43

Do not:

- Do not tune H017.
- Do not change H017 parameters.
- Do not change the cost model casually.
- Do not add ML.
- Do not broaden to more symbols.
- Do not start Phase 4 execution.
- Do not live trade.
- Do not use HistData for H017 validation.
- Do not accept HistData as a research source.
- Do not build HistData H4 for H017 validation.
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
- Do not allow test count to drop below 545 without explicit test-removal phase.
- Do not call the raw-entry invalid-stop guard H017 promotion.
- Do not call the H018 minimum stop-distance guard H017 promotion.
- Do not call the H018 maximum leverage policy H018 validation.
- Do not call H018 governance plans H017 or H018 promotion.
- Do not rerun broad strict validation after guards unless explicitly authorized as diagnostics or later H018 validation.
- Do not introduce trade skipping or clipping; accepted validation-mode policy rejects both for first implementation.
- Do not implement executable-entry sizing before a decision record chooses the rule.
- Do not treat positive near-zero stop-distance behavior as fully solved until maximum leverage guard is implemented and tested.
- Do not treat H018 as live-approved.
- Do not treat H018 as validated.
- Do not choose thresholds casually.
- Do not use real-data reruns as a tuning loop.
- Do not create more broad draft-only decision records unless there is a concrete missing gate.
- Do not implement anything from H018_DECISION_RECORD_TEMPLATE.md; it is a template only.
- Do not treat H018_DECISION_RECORD_INDEX.md as a full policy decision by itself.
- Do not treat H018_BOUNDARY_DECISION_RECORD.md as accepted; it is Draft.
- Do not treat H018_SIZING_REFERENCE_DECISION_RECORD.md as accepted; it is Draft.
- Do not treat accepted maximum leverage policy as authorizing real-data validation.
- Do not commit an empty HANDOFF_43.md.
- Do not leave a root-level HANDOFF_43.md in the repository.
- Do not forget that handoff files now live in docs/operations/handoffs.

Known Repo Hygiene Lessons

Do not repeat these mistakes:

- .gitignore once had unrooted data/, which risked excluding quantcore/data.
- Some older commits missed files because git add was incomplete.
- An empty HANDOFF_16.md was accidentally committed once; verify handoff file size and preview before committing.
- A mistaken empty root-level HANDOFF_43.md was created during this handoff attempt. Delete it and do not commit it.
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

Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after HANDOFF_43.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
- Current full-test anchor is 545 passed.
- Latest expected commit after handoff commit is Add handoff folder and document #43 after H018 leverage policy acceptance.
- Previous commit before the handoff should be 3c5c46a Accept H018 maximum per-trade leverage policy.
- Handoff files now live in docs/operations/handoffs.
- H017 remains failed / not promotable / not live-approved.
- H018 remains not validated / not promotable / not live-approved.
- Live trading is not approved.
- Phase 4 execution work is not approved.
- Broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
- The strict expanded broker-native validation originally failed by insolvency after a pathological 518.77-lot USDJPY trade.
- H017EventInvalidStopError is implemented.
- Under current raw-entry sizing semantics, long/buy stops must be below raw H4 entry open and short/sell stops must be above raw H4 entry open.
- Equality is invalid for directional stop geometry.
- Invalid directional stop geometry fails closed.
- H018MinimumStopDistanceError is implemented.
- H018 minimum stop-distance guard is implemented.
- The H018 minimum stop-distance rule is raw_stop_distance >= one modeled spread for the symbol.
- USDJPY minimum raw-entry stop distance is 0.01.
- XAUUSD minimum raw-entry stop distance is 0.30.
- Below threshold fails closed.
- Equality passes the minimum-distance guard.
- Above threshold passes the minimum-distance guard.
- H018 maximum per-trade USD gross leverage policy is accepted but not yet implemented.
- The accepted max leverage rule is notional_usd / equity_usd <= 10.0.
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
- Recommended next logical sub-phase is implementation of the accepted maximum per-trade USD gross leverage guard, with API inspection first.
- First task is hygiene verification only. No new code yet.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10
pytest -q

Then paste the full output.