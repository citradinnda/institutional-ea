HANDOFF 39 - After H018 Decision-Record Template References And Decision-Record Index

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_39 wins.

Project Identity
You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

Research: Python quantcore.
Execution: MetaTrader 5 later.
Production target: Oracle Cloud Always Free VPS later.
Monitoring: self-hosted free-tier stack later.
Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in .venv.
Do not rush into strategy validation or live trading. The project is still in research-validation infrastructure and hypothesis-governance work.

Non-Negotiable Workflow Rules
Use:

Windows.
PowerShell.
VS Code.
Python 3.12.10.
.venv.
No WSL.
No Linux/macOS shell assumptions.

Important PowerShell rule:

Do not use Linux/macOS heredoc syntax like python - <<'PY'

PowerShell does not support that.

Use PowerShell here-strings instead:

@'
python code here
'@ | python -

Tone and workflow:

Step-by-step.
Numbered steps.
Explicit Windows paths.
Plain English.
Define technical terms inline when needed.
Never write code without saying exactly where the file goes and how to run it.
One sub-phase per response.
Never skip git commits.
Never continue while local commits are unpushed.
Always read git status.
If tests pass but the count drops, treat it as a regression.
Do not propose switching to another AI chat unless the user asks.
For documentation-only phases, short copy-safe PowerShell blocks are preferred.
Avoid giant command blocks when possible; VS Code manual file editing is acceptable for long handoff text.
Avoid nested Markdown code fences inside PowerShell here-strings because copy/paste previously failed.
For code or diagnostics, inspect APIs first and split cautiously.
Before writing code that calls internal functions, inspect actual APIs with inspect.signature(...) and dataclasses.fields(...).
After each sub-phase, run focused tests if applicable, run full pytest -q, check status, commit, push, check status, run git ls-files on touched files/directories, and read the output.
After each response, offer exactly:
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

Latest expected commit before this HANDOFF_39 document is committed:

db54550 Add H018 decision record index

Expected latest commit after this handoff is committed:

Add handoff document #39 after H018 decision record index

Recent commits at the time this handoff was written:

db54550 Add H018 decision record index
fb2bbb0 Reference H018 decision record template
89a44cd Add handoff document #38 after H018 governance skeletons
76a36d9 Add H018 decision record template
7c3d67c Reference H018 claim skeleton
d1ea6ae Add H018 claim skeleton
0fc3fdf Add H018 consolidated decision matrix
679491d Add handoff document #37 after H018 execution governance plans
c94b9ed Reference H018 executable entry sizing plan
95d94d1 Add H018 executable entry sizing decision plan

Known note:

There are duplicate consecutive HANDOFF_31 commits earlier in history. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

537 passed

Important test-count rule:

Current correct full-test anchor is 537 passed.
If tests pass but the count drops below 537 without a deliberate test-removal phase, treat it as a regression.

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

On branch main.
Your branch is up to date with origin/main.
Nothing to commit, working tree clean.

Expected latest commit:

Add handoff document #39 after H018 decision record index

Expected previous commit:

db54550 Add H018 decision record index

Expected tests:

537 passed

Read the output before continuing.

Current Important Paths
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
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_BOUNDARY_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md
C:\Users\equin\Documents\institutional-ea\docs\operations\H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md
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

Existing real-data scripts:

C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
C:\Users\equin\Documents\institutional-ea\scripts\run_h017_real.py
C:\Users\equin\Documents\institutional-ea\scripts\run_h017_strict_event_real.py

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

Do not commit raw data.
Do not commit large derived data.
Do not write derived data before explicit authorization.
Do not modify raw vendor/broker files.

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

Winter UTC+2.
Summer UTC+3.
DST-aware.

MT5 loader:

load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

MT5LoadResult fields verified:

bars
n_bars
n_input_rows
earliest_utc
latest_utc
broker_tz

Loaded bars shape verified:

pandas DataFrame.
DatetimeIndex.
index name: dt.
timezone: UTC.
columns: open, high, low, close, volume.

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

Current Source Acceptance Status
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

USDJPY has a broker-native H4 bar at the H4 timestamp.
XAUUSD has a broker-native H4 bar at the same H4 timestamp.
For each symbol, the next H4 timestamp is exactly four hours later.
For each symbol, the M1 window has exactly 240 M1 bars.
No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

HistData State
HistData remains rejected for H017 validation under current evidence.

Current statuses:

HistData as H017 validation source: rejected under current evidence.
HistData as accepted research source: not accepted.
HistData-built H4: not accepted.
Broker H4 plus HistData M1 hybrid: not accepted.
Derived HistData files: not authorized.
H017 validation on HistData: not authorized.
Broker-native expanded source is conditionally accepted for strict validation only.
H017 status is failed/not promotable after strict expanded broker-native insolvency result.

Allowed HistData uses:

Explicitly planned diagnostics only.
Documentation.
Source-quality comparison.
Raw inventory metadata preservation.

Not allowed:

H017 validation.
Strategy tuning.
Derived production datasets.
Derived H4 files for H017 validation.
Broker-H4 plus HistData-M1 hybrid validation.
Silent deduplication.
Raw file modification.
Raw file commits.

Strategy / Validation Background
The project uses strict hypothesis discipline because many prior strategies failed.

Immutable strategy graveyard summary:

H001: Backtest without intrabar SL/TP simulation is fiction. Must use M1 inside H4 bars to resolve fills.
H002-H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
H004a: Single-seed models unreliable; use multi-seed ensembles.
H005: Stacked multi-symbol models fail on heterogeneous instruments; use per-symbol models.
H006-H007: Confidence filters are not risk management. ML chooses entries; deterministic rules manage risk.
H008-H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals cannot be risk manager.
H011-H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk ceiling remained.
H014-H016: Two-asset USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1 percent per-trade risk was not 1 percent portfolio risk when trades overlapped. Drawdown breach was -19.43 percent.
H015: Diversification into negative-edge instruments destroys the portfolio.
H017: H016 plus portfolio heat governor. H017 has failed strict expanded broker-native event validation by insolvency and is not promotable.

Current H017 interpretation:

H017 is not promotable.

The strict expanded broker-native source preflight passed, but the strategy failed event-driven validation by account insolvency on a complete strict bridge window.

Do not broaden to more symbols yet.

Do not add machine learning yet.

Do not tune H017.

Do not approve live trading.

Core Strategy Conventions
ATR:

Wilder RMA, not SMA.

First true range is high - low.

Seed at index window - 1 with simple mean of first window true ranges.

Recurrence:

ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n

Chandelier Exit:

Long: highest_high(lookback) - multiplier * ATR.
Short: lowest_low(lookback) + multiplier * ATR.

Defaults:

multiplier = 3.0
lookback = 22

Vol Target:

Realized vol at bar t uses returns through t-1 only.

No lookahead.

For H4 bars:

periods_per_year = 1512

Signals:

Donchian breakout.
Long: close[t] > max(high[t-N ... t-1]).
Short: close[t] < min(low[t-N ... t-1]).
Channel uses prior N bars via shift(1).rolling(N).

H017:

Inner-joins USDJPY and XAUUSD timestamps.

Computes close-to-close returns.

Uses same returns for vol targeting and heat governor.

Position is signed risk exposure:

signal * per_trade_risk * vol_mult * heat_mult

Heat governor:

Combined heat:

sqrt(w' (r^2 * C) w)

Defaults:

cap = 0.015
per_trade_risk = 0.01
correlation_window = 120
correlation_floor = 0.0

Event-Driven Backtest Conventions
Fill rule:

If stop and take-profit are both touched in the same M1 bar, stop wins.

Reason:

M1 OHLC does not reveal tick order inside the minute, so stop-first is conservative.

Cost model defaults:

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

XAUUSD P&L is already USD.
USDJPY P&L is JPY and must be divided by USDJPY conversion price to become USD.

Event bridge timing:

H017 decides at H4 timestamp t.
Trade opens on next H4 bar open t+1.
M1 bars inside the next H4 window resolve stops.
If no stop is hit, exposure closes at following H4 open as signal_flip.
This is a bridge-layer simplification.

Current event engine sizing behavior:

It sizes from absolute difference between raw H4 entry open and stop price.
This occurs before entry spread is applied.
Do not silently change this behavior.

Any future raw-entry versus executable-entry sizing decision must be explicit, tested, documented, and treated as execution-model semantics, not tuning.

Raw-Entry Invalid-Stop Execution Guard
Implemented in:

quantcore/backtest/h017_event.py

Error class:

H017EventInvalidStopError

Under current raw-entry sizing semantics:

Long/buy stop must be below raw H4 entry open.
Short/sell stop must be above raw H4 entry open.
Equality is invalid:
long/buy stop equal to raw H4 entry open fails closed.
short/sell stop equal to raw H4 entry open fails closed.

Invalid directional stop geometry fails closed.

Invalid directional stops are not skipped silently.

Invalid directional stops are not clipped.

This guard does not promote H017.

This guard does not authorize a real-data rerun.

Current focused synthetic tests are in:

tests/test_h017_event.py

Focused H017 event test anchor:

15 passed

Full test anchor after equality invalid-stop tests and H018 governance docs:

537 passed

Strict Expanded Broker-Native Validation Result
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

Interpretation Of The Insolvency Result
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

Near-Zero Stop-Distance Diagnostic Summary
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

stop_distance_price must be greater than zero.
There is no minimum stop-distance threshold beyond positive.
There is no maximum notional guard.
There is no maximum leverage guard.
Lot size is rounded down to the broker lot step.
If rounded size is below minimum lot, zero lots are returned.

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

Work Completed Since HANDOFF_38
Commit fb2bbb0 - Reference H018 decision record template
Files changed:

README.md
docs/operations/HYPOTHESIS_LEDGER.md
docs/operations/H018_DECISION_MATRIX.md
docs/operations/H018_CLAIM_SKELETON.md

Documented references to:

docs/operations/H018_DECISION_RECORD_TEMPLATE.md

Full tests:

537 passed

Commit was pushed.

Commit db54550 - Add H018 decision record index
File added:

docs/operations/H018_DECISION_RECORD_INDEX.md

Files changed:

README.md
docs/operations/HYPOTHESIS_LEDGER.md
docs/operations/H018_DECISION_MATRIX.md
docs/operations/H018_CLAIM_SKELETON.md
docs/operations/H018_DECISION_RECORD_INDEX.md

Documented:

Pending H018 decision inventory.
H018 hypothesis boundary pending.
Sizing reference pending.
Directional stop validity reference pending.
Minimum stop-distance rule pending.
Maximum notional/leverage rule pending.
Trade violation policy pending.
Real-data rerun classification pending.
H018 claim gate pending.
No policy chosen.
No implementation.
No validation.
No promotion.
No live approval.
No Phase 4 approval.

Full tests:

537 passed

Commit was pushed.

Current H017 Status
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

Current H018 Governance Status
H018 is not yet an implemented strategy.

H018 is not validated.

H018 is not promotable.

H018 does not approve live trading.

H018 does not approve Phase 4 execution.

Current H018 governance documents:

docs/operations/H018_BOUNDARY_DECISION_PLAN.md
docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md
docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md
docs/operations/H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md
docs/operations/H018_DECISION_MATRIX.md
docs/operations/H018_CLAIM_SKELETON.md
docs/operations/H018_DECISION_RECORD_TEMPLATE.md
docs/operations/H018_DECISION_RECORD_INDEX.md

No H018 threshold has been chosen.

No H018 guard has been implemented.

No H018 sizing reference has been chosen.

No H018 real-data validation has been authorized.

Remaining Open Execution-Semantics Questions
Should future sizing use raw H4 entry open or executable entry price after spread?
Should the selected sizing reference be raw, executable, both, conservative worst-case, or a named separate reference?
Should a long stop be required below raw entry, executable entry, or both?
Should a short stop be required above raw entry, executable entry, or both?
Should near-zero but directionally valid stop distances fail closed?
Should minimum stop distance be a multiple of spread, ATR, tick size, broker point, all-in friction, or a combined maximum of several references?
Should maximum leverage/notional be applied in event-engine research validation?
Should maximum exposure be measured by lots, notional, notional/equity, per-trade leverage, portfolio leverage, margin usage, or friction burden?
If a guard skips or clips trades, is that a strategy change and therefore H018?
Should any future real-data run after semantics changes be diagnostic-only?
How should the original H017 insolvency remain visible after fail-closed invalid-stop behavior changes the failure mode?
Should H018 inherit H017 alpha logic but change execution semantics?
Should H018 be defined as a new hypothesis before any code changes?
Should an H018 claim require strict bridge-window preflight plus event validation plus explicit account-exposure guards?
Should H018 decision records be created one policy at a time before any code changes?
Treat these as epistemic design decisions, not quick patches.

Recommended Next Path
Next logical sub-phase after HANDOFF_39 hygiene:

Phase 3.26-bv - H018 boundary decision-record draft

Recommended priority:

Create a documentation-only draft decision record for the H018 hypothesis boundary.

Suggested file:

docs/operations/H018_BOUNDARY_DECISION_RECORD.md

Recommended content:

Use docs/operations/H018_DECISION_RECORD_TEMPLATE.md as the structure.
Classify status as draft or proposed, not accepted, unless the user explicitly chooses to accept after reviewing.
State that H017 remains failed and visible.
State that H018, if pursued, is a new hypothesis/successor due to execution/account-risk semantics changes.
State that no code implementation is authorized by the draft.
State that no validation rerun is authorized by the draft.
State that no live trading or Phase 4 execution is approved.
Do not choose minimum stop-distance threshold.
Do not choose maximum leverage/notional threshold.
Do not choose sizing reference.
Do not choose skip/clipping behavior.

Do not implement code yet.

Do not choose thresholds yet.

Do not rerun strict real-data validation yet.

Do not tune H017.

Absolute Do-Not Rules At HANDOFF_39
Do not:

Do not tune H017.
Do not change H017 parameters.
Do not change the cost model casually.
Do not add ML.
Do not broaden to more symbols.
Do not start Phase 4 execution.
Do not live trade.
Do not use HistData for H017 validation.
Do not accept HistData as a research source.
Do not build HistData H4 for H017 validation.
Do not combine broker H4 with HistData M1.
Do not use sparse 2018 through 2021-06 broker-native prefix as dense M1.
Do not include incomplete H4/M1 windows.
Do not use any bridge window where either symbol has fewer or more than exactly 240 M1 bars.
Do not impute missing M1 bars.
Do not forward-fill or backfill M1 bars.
Do not synthesize bars.
Do not modify raw broker files.
Do not commit raw MT5 CSV files.
Do not commit raw HistData files.
Do not change .gitignore from /data/ to data/.
Do not run old scripts/run_h017_event_real.py as expanded validation.
Do not filter H4 to accepted timestamps only.
Do not ignore the accepted timestamp gaps found in the contiguity diagnostic.
Do not treat source acceptance as H017 promotion.
Do not treat future validation as live-trading approval.
Do not ignore the previous -33.65 percent drawdown.
Do not ignore the strict expanded insolvency event.
Do not silently fix the 518.77-lot event by tuning.
Do not silently change raw versus executable entry sizing without tests and docs.
Do not continue development while local commits are unpushed.
Do not let git status go unread.
Do not skip full pytest.
Do not allow test count to drop below 537 without explicit test-removal phase.
Do not call the raw-entry invalid-stop guard H017 promotion.
Do not call equality invalid-stop tests H017 promotion.
Do not call near-zero stop-distance documentation H017 promotion.
Do not call H018 governance plans H017 or H018 promotion.
Do not rerun broad strict validation after the invalid-stop guard unless explicitly authorized as diagnostics only.
Do not introduce trade skipping or clipping without explicit H018 policy.
Do not implement minimum stop-distance guard before a decision record chooses the rule.
Do not implement maximum notional/leverage guard before a decision record chooses the rule.
Do not implement executable-entry sizing before a decision record chooses the rule.
Do not treat positive near-zero stop-distance behavior as solved.
Do not treat H018 as live-approved.
Do not treat H018 as validated.
Do not choose thresholds casually.
Do not use real-data reruns as a tuning loop.
Do not create H018 decision records that choose policies without first keeping H017 failure visible.
Do not implement anything from H018_DECISION_RECORD_TEMPLATE.md; it is a template only.
Do not treat H018_DECISION_RECORD_INDEX.md as a policy decision; it is an index only.

Known Repo Hygiene Lessons
Do not repeat these mistakes:

.gitignore once had unrooted data/, which risked excluding quantcore/data/.
Some older commits missed files because git add was incomplete.
An empty HANDOFF_16.md was accidentally committed once; verify handoff file size and preview before committing.
Markdown code fences have been damaged by paste before; avoid nested markdown fences in command blocks.
PowerShell does not support Linux heredocs.
VS Code can keep unsaved buffers that overwrite edits.
If terminal output shows command echo ambiguity, verify with Select-String or file previews before proceeding.
Always run tests.
Always inspect git status.
Always push commits.
Always verify git ls-files after commits.
Treat test-count drops as regressions.
If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.
If git commit says nothing to commit, immediately run recovery status/log/ls-files checks before continuing.
When two identical code blocks exist in one file, use function-boundary replacement, not first global text match.
Long pasted PowerShell blocks can be corrupted by chat formatting; prefer shorter blocks or VS Code manual edits for long documents.
tests/test_h017_event.py has a UTF-8 BOM; when programmatically editing it, use utf-8-sig.
A previous documentation sync appeared to fail in terminal output but had actually committed; when output is inconsistent, immediately perform read-only verification before proceeding.
Network/DNS push failures can happen; stop development until git push succeeds.
git diff -- new_untracked_file.md shows nothing for an untracked file before it is added. Use Get-Content, git status, and git ls-files after commit.
Handoff documents should be self-contained enough for a new AI to continue safely.
For very long handoffs, use VS Code manual editing instead of a huge PowerShell here-string.

Exact First Response The Next AI Should Give
The next AI should respond briefly:

Understood. I am continuing after HANDOFF_39.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Current full-test anchor is 537 passed.
Latest expected commit is Add handoff document #39 after H018 decision record index.
Previous commit is db54550 Add H018 decision record index.
H017 remains failed / not promotable / not live-approved.
H018 remains governance-only / unimplemented / unvalidated / not promotable / not live-approved.
Live trading is not approved.
Phase 4 execution work is not approved.
Broker-native USDJPY + XAUUSD M1/H4 data is conditionally accepted only under strict complete-window rules.
The strict expanded broker-native validation originally failed by insolvency after a pathological 518.77-lot USDJPY trade.
H017EventInvalidStopError is implemented.
Under current raw-entry sizing semantics, long/buy stops must be below raw H4 entry open and short/sell stops must be above raw H4 entry open.
Equality is invalid and directly tested.
Invalid directional stop geometry fails closed.
Invalid stops are not skipped silently and are not clipped.
This guard does not promote H017.
This guard does not authorize a real-data rerun.
Near-zero positive stop-distance behavior is documented as an open execution-semantics/account-risk issue.
H018 boundary planning is opened as governance only.
H018 minimum stop-distance planning is opened, but no threshold is chosen.
H018 maximum notional/leverage planning is opened, but no threshold is chosen.
H018 executable-entry sizing planning is opened, but no sizing reference is chosen.
H018 decision matrix exists.
H018 claim skeleton exists.
H018 decision-record template exists.
H018 decision-record index exists.
The decision-record index is not a policy decision.
Do not tune H017.
Do not use HistData.
Do not broaden symbols or add ML.
Do not start Phase 4.
Recommended next logical sub-phase is documentation-only H018 boundary decision-record draft.
First task is hygiene verification only. No new code yet.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10
pytest -q

Then paste the full output.