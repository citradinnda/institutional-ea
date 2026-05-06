# HANDOFF 57 - After H021 Positive Bucket Search Diagnostic

If any older handoff conflicts with this file, this HANDOFF_57 wins.

This handoff is intentionally self-contained so a new AI can continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is research/backtest infrastructure and strategy hypothesis work.
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

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_57.md`

## Human Preference

The user is tired of excessive documentation and slow ceremony.

Going forward:

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do not create governance docs unless they preserve a real decision, preserve a handoff, prevent ambiguity, or protect against future confusion.
- Do not create subphases inside subphases.
- Do one real action at a time.
- Prefer direct engineering actions over process theater.
- For docs-only changes, do not run full pytest unless there is a clear reason.
- For code changes, tests are mandatory.

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

Use PowerShell here-strings or normal files only.

## Practical Workflow Rules

General:

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

Testing:

- Docs-only edit:
  - No full pytest required by default.
  - Use `git diff --check` and `git diff --stat`.
- Code edit:
  - Run focused tests.
  - Run full `python -m pytest -q`.
  - Current full-test anchor: `633 passed`.
- If full tests pass but count drops below `633` without explicit planned test removal, stop and treat as regression.
- Previous anchor before the H021 positive bucket search was `623 passed`.

Git after changes:

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

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10
Expected after this handoff is committed and pushed:

text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
Latest commit should be:

text
Add handoff document #57 after H021 positive bucket search
Recent previous commits should include:

text
1b7b55b Add H021 positive bucket search diagnostic
b446f31 Add handoff document #56 after H021 exclusion diagnostics
3c69015 Add H021 candidate exclusion diagnostic
9080eb1 Add H021 stop precursor diagnostic
705ddd3 Add handoff document #55 after H021 decomposition diagnostic
0282cf9 Add H021 trade decomposition diagnostic
2f7e32a Add H021 hypothesis seed
57812f7 Record H020 performance failure
4d0bb73 Add H020 performance diagnostic script
Do not require pytest for this first check unless code has changed or status is not clean.

Current Test Anchor
Current full-test anchor after H021 positive bucket search diagnostic code:

text
633 passed in 20.30s
Recent anchors:

after H021 positive bucket search diagnostic: 633 passed
after H021 candidate exclusion diagnostic: 623 passed
after H021 stop precursor diagnostic: 616 passed
after H021 trade decomposition diagnostic: 611 passed
after H020 performance diagnostic script: 607 passed
after H020 strict validation work: 605 passed
after H020 sizing-intent seed: 600 passed
If full test count drops below 633 without planned test removal, treat it as a regression.

Important Current Commits
Recent important commits, newest first before this handoff:

text
1b7b55b Add H021 positive bucket search diagnostic
b446f31 Add handoff document #56 after H021 exclusion diagnostics
3c69015 Add H021 candidate exclusion diagnostic
9080eb1 Add H021 stop precursor diagnostic
705ddd3 Add handoff document #55 after H021 decomposition diagnostic
0282cf9 Add H021 trade decomposition diagnostic
2f7e32a Add H021 hypothesis seed
57812f7 Record H020 performance failure
4d0bb73 Add H020 performance diagnostic script
71eeb41 Add handoff document #53 after H020 sizing intent
52e0d39 Add comprehensive handoff document #54 after H020 validation success
Important note:

There was a confusing sequence where a stale H53 handoff commit appeared after H54 work.
HANDOFF_57 is now authoritative and supersedes H53, H54, H55, and H56 where conflicts exist.

Important Paths
Code:

quantcore
scripts
tests
Strategy files:

quantcore\strategy\h017.py
quantcore\strategy\h019.py
quantcore\strategy\h020.py
quantcore\strategy\h020_runner.py
quantcore\strategy\signals.py
quantcore\strategy\heat_governor.py
Event/strict bridge files:

quantcore\backtest\h017_event.py
quantcore\backtest\h017_strict_event.py
quantcore\backtest\h019_strict_event.py
quantcore\backtest\h020_strict_event.py
Portfolio/accounting:

quantcore\backtest\portfolio.py
quantcore\backtest\cost_model.py
quantcore\backtest\fill_engine.py
H020 scripts:

scripts\scan_h020_sizing_diagnostics_real.py
scripts\run_h020_strict_event_real.py
scripts\diagnose_h020_performance_real.py
H021 scripts:

scripts\diagnose_h021_trade_decomposition_real.py
scripts\diagnose_h021_stop_precursors_real.py
scripts\diagnose_h021_candidate_exclusions_real.py
scripts\diagnose_h021_positive_bucket_search_real.py
H020/H021 tests:

tests\test_h020.py
tests\test_h020_runner.py
tests\test_h020_sizing_diagnostics_real_script.py
tests\test_h020_strict_event.py
tests\test_h020_strict_event_real_script.py
tests\test_h020_performance_real_script.py
tests\test_h021_trade_decomposition_real_script.py
tests\test_h021_stop_precursors_real_script.py
tests\test_h021_candidate_exclusions_real_script.py
tests\test_h021_positive_bucket_search_real_script.py
Important docs:

docs\operations\H019_GRAVEYARD_RECORD.md
docs\operations\H020_HYPOTHESIS_SEED.md
docs\operations\H020_GRAVEYARD_RECORD.md
docs\operations\H021_HYPOTHESIS_SEED.md
docs\operations\handoffs\HANDOFF_57.md
Gitignore And Raw Data Rules
The repo uses root-anchored:

text
/data/
Do not change it to unanchored:

text
data/
Reason:

An unanchored data/ rule previously risked excluding quantcore/data/.

Do not commit:

raw MT5 CSV files,
raw HistData files,
large derived datasets,
broker/vendor source files.
Do not modify raw broker files.

Broker And Data State
Broker:

Exness
Account environment:

Demo
Server:

MT5
Broker timezone used by loader:

Europe/Athens
Winter UTC+2
Summer UTC+3
DST-aware
MT5 loader signature:

python
load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult
Expanded broker-native raw exports exist locally and are gitignored:

data\raw\USDJPY\H4.csv
data\raw\USDJPY\M1.csv
data\raw\XAUUSD\H4.csv
data\raw\XAUUSD\M1.csv
Reported exact MT5 symbols:

USDJPYm
XAUUSDm
Do not commit these raw files.

Source Acceptance Status
Accepted source for strict validation/diagnostics:

Exness demo MT5 broker-native exports only.
Accepted symbols:

USDJPY
XAUUSD
Accepted timeframes:

Broker-native H4
Broker-native M1
Accepted strict bridge-window range:

First common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
Last common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00
Accepted bridge-window count:

text
5476
A common complete H4/M1 bridge window means:

USDJPY has a broker-native H4 bar at the H4 timestamp.
XAUUSD has a broker-native H4 bar at the same H4 timestamp.
For each symbol, the next H4 timestamp is exactly four hours later.
For each symbol, the M1 window has exactly 240 M1 bars.
No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.
Do not treat 2018 through 2021-06 as dense M1 history.
The expanded files have a sparse daily-like prefix before the dense M1 candidate region, which starts at 2021-07 for both symbols.

HistData remains rejected for H017/H018/H019/H020/H021 validation or tuning under current evidence.

Do not use HistData for:

validation,
tuning,
production dataset creation,
broker H4 + HistData M1 combinations.
Core Strategy And Backtest Conventions
ATR:

Wilder RMA, not SMA.
First true range is high - low.
Seed at index window - 1 with simple mean of first window true ranges.
Recurrence:
ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n
Chandelier Exit:

Long: highest_high(lookback) - multiplier * ATR
Short: lowest_low(lookback) + multiplier * ATR
Current rolling windows include the current bar.
Defaults:
multiplier 3.0
lookback 22
Donchian Signals:

Long: close[t] > max(high[t-N ... t-1])
Short: close[t] < min(low[t-N ... t-1])
Channel uses prior N bars via shift(1).rolling(N).
Event bridge timing:

Strategy decides at H4 timestamp t.
Trade opens on next H4 bar open t+1.
M1 bars inside next H4 window resolve stops.
If no stop is hit, exposure closes at following H4 open as signal_flip.
This is a bridge-layer simplification.
Fill rule:

If stop and take-profit are both touched in the same M1 bar, stop wins.
Reason: M1 OHLC does not reveal tick order inside the minute.
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
H018 Hard Guards
H018 guards remain hard validation guards. Do not weaken them.

Implemented in:

quantcore\backtest\h017_event.py
Invalid stop geometry:

Long/buy stop must be below raw H4 entry open.
Short/sell stop must be above raw H4 entry open.
Equality is invalid.
Invalid directional stop geometry fails closed.
Minimum stop distance:

raw_stop_distance = abs(raw_h4_entry_open - stop_price)
Minimum is one modeled spread:
USDJPY 0.01
XAUUSD 0.30
Below threshold fails closed.
Equality passes.
Maximum per-trade USD gross leverage:

Hard max = 10.0x
A single trade may not create more than 10x account equity in USD-converted gross notional exposure.
Boundary:
< 10.0 passes
== 10.0 passes
> 10.0 fails closed
Maximum portfolio-wide USD gross leverage:

Hard max = 10.0x
Total USD-converted gross notional exposure opened by all symbols in one event interval may not exceed 10x account equity.
Long and short exposures are summed gross, not netted.
Boundary:
< 10.0 passes
== 10.0 passes
> 10.0 fails closed
Violation policy:

Raise explicit error.
Do not silently skip any trade in the event engine.
Do not clip any position size in the event engine.
Do not net long and short notionals.
Do not warn and continue.
Do not log-only continue.
Strategy Graveyard Summary
Immutable summary:

H001: Backtests without intrabar SL/TP simulation are fiction. Must use M1 inside H4 bars to resolve fills.
H002-H003: ATR-based per-symbol stops mandatory; trade frequency must amortize costs.
H004a-H005: Single-seed ML and stacked multi-symbol ML were unreliable. If ML ever returns, use multi-seed and per-symbol modeling.
H006-H010: Confidence filters are not risk management. ML on basic technicals cannot be a risk manager.
H011-H013: Deterministic ATR stops + Chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk remained.
H014-H016: USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1% per-trade risk was not 1% portfolio risk when trades overlapped. Drawdown breached -19.43%.
H017: H016 plus portfolio heat governor. Failed strict expanded broker-native event validation by insolvency before guards, then failed closed under H018-style guards.
H018: Guard and diagnostic work revealed structural strategy/execution mismatch. H018 was not a validated strategy.
H019: Stateful Donchian/Chandelier lifecycle fixed stale-stop first blocker but failed closed on H018 per-trade leverage guard. H019 is in the graveyard.
H020: Explicit sizing contract fixed guard-survivability but failed performance. H020 is in the graveyard.
H021: Active diagnostics-first research phase. No strategy is validated.
Current verdicts:

H017 failed.
H018 is guard/diagnostic work only; not validated.
H019 failed.
H020 failed performance.
H021 is not a strategy yet.
No strategy is currently promotable.
No live trading is approved.
Phase 4 execution is not approved.
H019 Summary
H019 introduced:

Donchian entry/flip trigger.
Same-side Chandelier lifecycle exit.
Flat state after same-side stop breach.
No re-entry from stale held Donchian direction.
No opposite-panel switching.
H018 guards remain strict.
Strict broker-native H019 validation:

Preflight passed over 5476 accepted complete windows.
Failed closed on H018MaximumPerTradeLeverageError.
First H019 failure:

text
symbol: USDJPY
side: buy
decision_time: 2021-07-05 21:00:00+00:00
entry_time: 2021-07-06 01:00:00+00:00
entry_raw_price: 110.840000000
stop_price: 110.741028558
raw_stop_distance: 0.098971442
equity_usd: 9872.94
lots: 1.20
notional_usd: 120000.000000000
gross_leverage: 12.154432565
maximum_gross_leverage: 10.000000000
H019/H020 diagnostic after H019:

total remaining H019 guard violations: 302
per-trade leverage: 239
portfolio leverage: 42
minimum stop-distance: 19
invalid directional stop: 2
Per-trade leverage severity:

median 15.70x
p95 79.82x
max 429.70x
H020 Implementation Summary
H020 was a sizing-contract hypothesis on top of H019 lifecycle semantics.

Implemented files include:

quantcore\strategy\h020.py
quantcore\strategy\h020_runner.py
quantcore\backtest\h020_strict_event.py
scripts\scan_h020_sizing_diagnostics_real.py
scripts\run_h020_strict_event_real.py
scripts\diagnose_h020_performance_real.py
corresponding H020 tests.
H020 mechanics:

invalid stop geometry becomes flat/no intent at strategy-intent level,
below-spread raw stop distance becomes flat/no intent,
per-trade strategy cap = 9.0x gross notional,
portfolio strategy cap = 9.0x gross notional,
H018 hard guards remain 10.0x and unchanged,
explicit intent objects preserve diagnostics,
bridge shim converts H020 intent back into H017Result-shaped positions for strict event bridge compatibility.
Important caveat:

The bridge shim evaluates intents at nominal \$10,000 equity and reverse-engineers final safe signed risk fractions.
This was a routing shim, not the strategy truth.
It was tested and used to pass through the strict H018 event layer.

H020 Strict Guard Validation Result
Command:

powershell
python .\scripts\run_h020_strict_event_real.py
Result:

strict accepted bridge-windows: 5476
completed successfully without guard violations.
Interpretation:

H020 survived strict event/guard validation.
This proved safe representation under current bridge constraints.
It did not prove profitability.

H020 Performance Failure
Performance diagnostic script:

scripts\diagnose_h020_performance_real.py
Command:

powershell
python .\scripts\diagnose_h020_performance_real.py
Real result:

text
accepted_entry_count: 5476
executed_entry_count: 5476
skipped_entry_count: 3176
fill_count: 4158
starting_equity_usd: \$10000.00
ending_equity_usd: \$819.07
total_pnl_usd: -\$9180.93
total_return: -91.8093%
max_drawdown: -91.8860%
winning_fill_count: 1837
losing_fill_count: 2321
flat_fill_count: 0
win_rate: 44.1799%
gross_profit_usd: \$28703.99
gross_loss_usd: -\$37884.92
profit_factor: 0.757663
mean_fill_return: -0.0579%
median_fill_return: -0.0375%
fill_return_sharpe: -0.086278
Verdict:

H020 failed performance evaluation.
H020 is not promotable.
H020 is not live-approved.
Phase 4 is not approved.
H020 graveyard record:

docs\operations\H020_GRAVEYARD_RECORD.md
Key lesson:

H020 separated execution survivability from profitability.
It achieved the first and failed the second.

H021 Start
H021 was started in:

docs\operations\H021_HYPOTHESIS_SEED.md
H021 purpose:

H021 is not another sizing patch.
H021 must search for positive expectancy before adding more execution machinery.

Core question:

Can USDJPY + XAUUSD produce a cost-amortized, event-safe edge under strict broker-native H4/M1 simulation?

H021 should preserve:

strict broker-native Exness complete-window validation only,
M1 intrabar stop resolution inside H4 decisions,
conservative stop-first fill rule,
modeled spread, commission, and slippage,
H018 hard guards unchanged,
no raw-data mutation,
no HistData,
no live trading.
H021 should not begin by increasing risk or leverage.

H021 should begin by reducing bad trades.

Likely research directions:

Cost-amortization filters.
Regime gating.
Entry selectivity.
Exit asymmetry.
Symbol-specific behavior.
H021 Diagnostic 1: Trade Decomposition
Implemented files:

scripts\diagnose_h021_trade_decomposition_real.py
tests\test_h021_trade_decomposition_real_script.py
Commit:

0282cf9 Add H021 trade decomposition diagnostic
Tests after implementation:

focused H021 test: 4 passed
H020 performance + H021 diagnostic focused tests: 6 passed
full test suite: 611 passed in 27.66s
Real command run:

powershell
python .\scripts\diagnose_h021_trade_decomposition_real.py
Real diagnostic result summary:

By symbol:

USDJPY:

fills: 2827
win_rate: 44.2872%
total_pnl_usd: -7259.73
mean_pnl_usd: -2.57
median_pnl_usd: -0.94
profit_factor: 0.722826
XAUUSD:

fills: 1331
win_rate: 43.9519%
total_pnl_usd: -1921.21
mean_pnl_usd: -1.44
median_pnl_usd: -1.47
profit_factor: 0.835695
By side:

Buy:

fills: 2497
win_rate: 45.8550%
total_pnl_usd: -5224.34
mean_pnl_usd: -2.09
median_pnl_usd: -0.75
profit_factor: 0.766060
Sell:

fills: 1661
win_rate: 41.6616%
total_pnl_usd: -3956.60
mean_pnl_usd: -2.38
median_pnl_usd: -1.47
profit_factor: 0.745606
By exit reason:

Signal flip:

fills: 3678
win_rate: 49.9456%
total_pnl_usd: +9503.32
mean_pnl_usd: +2.58
median_pnl_usd: -0.00
profit_factor: 1.494947
Stop:

fills: 480
win_rate: 0.0000%
total_pnl_usd: -18684.26
mean_pnl_usd: -38.93
median_pnl_usd: -27.45
profit_factor: 0.000000
Key interpretation:

H020 losses are not because all trades are bad.
Every signal_flip bucket is profitable.
Every stop bucket is deeply negative.

Stop exits are the destructive component:

480 stop fills caused -18684.26.
3678 signal-flip fills made +9503.32.
USDJPY stop losses are the largest damage:
USDJPY buy stops -7280.03
USDJPY sell stops -4985.46
Resulting H021 research question:

Can likely future stop-outs be identified before entry using only information available at decision time?

Do not jump to removing stops. Stops are structural risk controls.
The evidence says entries that later hit stops are the problem.

H021 Diagnostic 2: Stop-Loss Precursor Diagnostic
Implemented files:

scripts\diagnose_h021_stop_precursors_real.py
tests\test_h021_stop_precursors_real_script.py
Commit:

9080eb1 Add H021 stop precursor diagnostic
Tests:

focused tests: 5 passed
full test suite: 616 passed in 19.61s
Real command run:

powershell
python .\scripts\diagnose_h021_stop_precursors_real.py
Real diagnostic result:

Strict accepted bridge-windows: 5476
Context rows reconstructed: 5282
Fill rows enriched: 4158
Important results by decision hour UTC:

Decision hour UTC 05:

fills: 585
stops: 117
stop_rate: 20.0000%
total_pnl_usd: -2621.09
profit_factor: 0.715453
Decision hour UTC 10:

fills: 303
stops: 33
stop_rate: 10.8911%
total_pnl_usd: -1092.41
profit_factor: 0.601259
Decision hour UTC 22:

fills: 297
stops: 31
stop_rate: 10.4377%
total_pnl_usd: -1025.01
profit_factor: 0.463573
Important results by stop distance / spread bucket:

<2x:

fills: 17
stops: 16
stop_rate: 94.1176%
total_pnl_usd: -217.79
profit_factor: 0.004211
2-5x:

fills: 40
stops: 30
stop_rate: 75.0000%
total_pnl_usd: -208.99
profit_factor: 0.663358
5-10x:

fills: 81
stops: 52
stop_rate: 64.1975%
total_pnl_usd: -79.02
profit_factor: 0.952525
10-20x:

fills: 202
stops: 96
stop_rate: 47.5248%
total_pnl_usd: -1664.75
profit_factor: 0.621684
20-50x:

fills: 1064
stops: 184
stop_rate: 17.2932%
total_pnl_usd: -4018.88
profit_factor: 0.738456
>=50x:

fills: 2754
stops: 102
stop_rate: 3.7037%
total_pnl_usd: -2991.50
profit_factor: 0.808415
Important results by estimated gross leverage bucket:

<1x:

fills: 2934
stops: 208
stop_rate: 7.0893%
total_pnl_usd: -3208.78
profit_factor: 0.768747
1-3x:

fills: 942
stops: 187
stop_rate: 19.8514%
total_pnl_usd: -1771.23
profit_factor: 0.866350
3-6x:

fills: 227
stops: 59
stop_rate: 25.9912%
total_pnl_usd: -1675.21
profit_factor: 0.752770
6-9x:

fills: 55
stops: 26
stop_rate: 47.2727%
total_pnl_usd: -2525.70
profit_factor: 0.365494
Interpretation:

Stop-outs are meaningfully concentrated.

Strongest obvious damage bucket:

estimated_gross_leverage_bucket=6-9x
only 55 fills
26 stops
47.27% stop rate
-2525.70 PnL
profit factor 0.365494
Worst time bucket:

decision_hour_utc=05
entry_hour_utc=09
585 fills
117 stops
20.00% stop rate
-2621.09 PnL
Tight stop-distance buckets are dangerous:

<2x: 94.12% stop rate
2-5x: 75.00% stop rate
5-10x: 64.20% stop rate
10-20x: 47.52% stop rate
But wide stops alone do not create profitability:

>=50x has only 3.70% stop rate but still -2991.50
So “avoid tight stops” is useful but not enough.

H021 Diagnostic 3: Candidate Exclusion Diagnostic
Implemented files:

scripts\diagnose_h021_candidate_exclusions_real.py
tests\test_h021_candidate_exclusions_real_script.py
Commit:

3c69015 Add H021 candidate exclusion diagnostic
Tests:

focused tests: 7 passed
full test suite: 623 passed in 27.45s
Real command run:

powershell
python .\scripts\diagnose_h021_candidate_exclusions_real.py
Real baseline:

Fill rows enriched: 4158
Baseline fills: 4158
Baseline stops: 480
Baseline stop_rate: 11.5440%
Baseline total_pnl_usd: -9180.93
Baseline profit_factor: 0.757663
Candidate exclusion results:

exclude_usdjpy_all:

excluded_fills: 2827
excluded_stops: 289
excluded_pnl_usd: -7259.73
retained_fills: 1331
retained_stops: 191
retained_stop_rate: 14.3501%
retained_pnl_usd: -1921.21
pnl_improvement_usd: 7259.73
retained_profit_factor: 0.835695
exclude_stop_distance_lt_50x_spread:

excluded_fills: 1404
excluded_stops: 378
excluded_pnl_usd: -6189.43
retained_fills: 2754
retained_stops: 102
retained_stop_rate: 3.7037%
retained_pnl_usd: -2991.50
pnl_improvement_usd: 6189.43
retained_profit_factor: 0.808415
exclude_decision_hours_05_10_22:

excluded_fills: 1185
excluded_stops: 181
excluded_pnl_usd: -4738.52
retained_fills: 2973
retained_stops: 299
retained_stop_rate: 10.0572%
retained_pnl_usd: -4442.42
pnl_improvement_usd: 4738.52
retained_profit_factor: 0.815076
exclude_estimated_gross_leverage_ge_3x:

excluded_fills: 282
excluded_stops: 85
excluded_pnl_usd: -4200.92
retained_fills: 3876
retained_stops: 395
retained_stop_rate: 10.1909%
retained_pnl_usd: -4980.02
pnl_improvement_usd: 4200.92
retained_profit_factor: 0.816428
exclude_usdjpy_sell:

excluded_fills: 1066
excluded_stops: 134
excluded_pnl_usd: -3637.69
retained_fills: 3092
retained_stops: 346
retained_stop_rate: 11.1902%
retained_pnl_usd: -5543.25
pnl_improvement_usd: 3637.69
retained_profit_factor: 0.796264
exclude_decision_hour_05:

excluded_fills: 585
excluded_stops: 117
excluded_pnl_usd: -2621.09
retained_fills: 3573
retained_stops: 363
retained_stop_rate: 10.1595%
retained_pnl_usd: -6559.84
retained_profit_factor: 0.771223
exclude_entry_hour_09:

same as exclude_decision_hour_05
exclude_estimated_gross_leverage_6_9x:

excluded_fills: 55
excluded_stops: 26
excluded_pnl_usd: -2525.70
retained_fills: 4103
retained_stops: 454
retained_stop_rate: 11.0651%
retained_pnl_usd: -6655.23
retained_profit_factor: 0.803706
exclude_usdjpy_buy_stop_distance_20_50x:

excluded_fills: 295
excluded_stops: 64
excluded_pnl_usd: -2417.06
retained_fills: 3863
retained_stops: 416
retained_stop_rate: 10.7688%
retained_pnl_usd: -6763.88
retained_profit_factor: 0.788743
exclude_stop_distance_lt_20x_spread:

excluded_fills: 340
excluded_stops: 194
excluded_pnl_usd: -2170.55
retained_fills: 3818
retained_stops: 286
retained_stop_rate: 7.4908%
retained_pnl_usd: -7010.38
retained_profit_factor: 0.773716
exclude_usdjpy_decision_hour_05:

excluded_fills: 401
excluded_stops: 68
excluded_pnl_usd: -2003.00
retained_fills: 3757
retained_stops: 412
retained_stop_rate: 10.9662%
retained_pnl_usd: -7177.93
retained_profit_factor: 0.770473
exclude_xauusd_decision_hour_05:

excluded_fills: 184
excluded_stops: 49
excluded_pnl_usd: -618.09
retained_fills: 3974
retained_stops: 431
retained_stop_rate: 10.8455%
retained_pnl_usd: -8562.84
retained_profit_factor: 0.757328
exclude_stop_distance_lt_10x_spread:

excluded_fills: 138
excluded_stops: 98
excluded_pnl_usd: -505.80
retained_fills: 4020
retained_stops: 382
retained_stop_rate: 9.5025%
retained_pnl_usd: -8675.13
retained_profit_factor: 0.754807
Interpretation:

None of these simple exclusions gets close to profitability.
The best retained set is XAUUSD only:
retained PnL -1921.21
PF 0.835695
still negative.
Removing tight/medium stops helps but is still negative:
keep only >=50x stop-distance: -2991.50, PF 0.808415.
Removing higher leverage helps:
exclude >=3x: retained -4980.02, PF 0.816428.
Time exclusions help but do not solve expectancy:
exclude decision hours 05/10/22: retained -4442.42, PF 0.815076.
Bottom line:

H021 evidence says bad stop-outs are concentrated, but concentration filters alone do not reveal a profitable core.
Do not implement a strategy from these exclusion candidates.
Do not promote H020/H021.
No live trading.
No Phase 4.

H021 Diagnostic 4: Positive Bucket Search Diagnostic
Implemented files:

scripts\diagnose_h021_positive_bucket_search_real.py
tests\test_h021_positive_bucket_search_real_script.py
Commit:

1b7b55b Add H021 positive bucket search diagnostic
Tests:

new focused tests: 10 passed in 2.70s
broader H021 focused tests: 26 passed in 2.44s
full suite: 633 passed in 20.30s
Real command run:

powershell
python .\scripts\diagnose_h021_positive_bucket_search_real.py
Real diagnostic result:

Strict accepted bridge-windows: 5476
Context rows reconstructed: 5282
Fill rows enriched: 4158
The diagnostic scanned decision-time observable groups with minimum fill thresholds:

>=30
>=50
>=100
Fields searched:

1-way:

symbol
side
decision_hour_utc
entry_hour_utc
stop_distance_spread_bucket
estimated_gross_leverage_bucket
2-way:

symbol + side
symbol + decision_hour_utc
symbol + stop_distance_spread_bucket
symbol + estimated_gross_leverage_bucket
side + decision_hour_utc
stop_distance_spread_bucket + estimated_gross_leverage_bucket
3-way:

symbol + side + decision_hour_utc
symbol + side + stop_distance_spread_bucket
symbol + side + estimated_gross_leverage_bucket
symbol + stop_distance_spread_bucket + estimated_gross_leverage_bucket
Positive buckets with at least 30 fills:

Top rows:

symbol=XAUUSD | stop_distance_spread_bucket=5-10x

fills: 44
stops: 20
stop_rate: 45.4545%
total_pnl_usd: +639.699759
mean_pnl_usd: +14.538631
median_pnl_usd: -7.652802
gross_profit_usd: 1454.765000
gross_loss_usd: -815.065241
profit_factor: 1.784845
symbol=XAUUSD | side=sell | decision_hour_utc=01

fills: 94
stops: 9
stop_rate: 9.5745%
total_pnl_usd: +386.014161
mean_pnl_usd: +4.106534
median_pnl_usd: -0.922500
gross_profit_usd: 913.263000
gross_loss_usd: -527.248839
profit_factor: 1.732129
symbol=XAUUSD | side=buy | decision_hour_utc=18

fills: 67
stops: 6
stop_rate: 8.9552%
total_pnl_usd: +135.666425
mean_pnl_usd: +2.024872
median_pnl_usd: +0.948000
gross_profit_usd: 508.956000
gross_loss_usd: -373.289575
profit_factor: 1.363435
Positive buckets with at least 50 fills:

Top rows:

symbol=XAUUSD | side=sell | decision_hour_utc=01

fills: 94
stops: 9
stop_rate: 9.5745%
total_pnl_usd: +386.014161
mean_pnl_usd: +4.106534
median_pnl_usd: -0.922500
gross_profit_usd: 913.263000
gross_loss_usd: -527.248839
profit_factor: 1.732129
symbol=XAUUSD | side=buy | decision_hour_utc=18

fills: 67
stops: 6
stop_rate: 8.9552%
total_pnl_usd: +135.666425
mean_pnl_usd: +2.024872
median_pnl_usd: +0.948000
gross_profit_usd: 508.956000
gross_loss_usd: -373.289575
profit_factor: 1.363435
symbol=USDJPY | side=sell | decision_hour_utc=06

fills: 100
stops: 18
stop_rate: 18.0000%
total_pnl_usd: +331.990603
mean_pnl_usd: +3.319906
median_pnl_usd: +0.018233
gross_profit_usd: 1509.741858
gross_loss_usd: -1177.751255
profit_factor: 1.281885
Positive buckets with at least 100 fills:

symbol=USDJPY | side=sell | decision_hour_utc=06

fills: 100
stops: 18
stop_rate: 18.0000%
total_pnl_usd: +331.990603
mean_pnl_usd: +3.319906
median_pnl_usd: +0.018233
gross_profit_usd: 1509.741858
gross_loss_usd: -1177.751255
profit_factor: 1.281885
symbol=XAUUSD | decision_hour_utc=17

fills: 146
stops: 16
stop_rate: 10.9589%
total_pnl_usd: +133.556329
mean_pnl_usd: +0.914769
median_pnl_usd: +0.493500
gross_profit_usd: 1017.570000
gross_loss_usd: -884.013671
profit_factor: 1.151079
side=sell | decision_hour_utc=06

fills: 149
stops: 29
stop_rate: 19.4631%
total_pnl_usd: +253.967530
mean_pnl_usd: +1.704480
median_pnl_usd: +0.146423
gross_profit_usd: 1950.666858
gross_loss_usd: -1696.699328
profit_factor: 1.149683
symbol=XAUUSD | decision_hour_utc=06

fills: 143
stops: 29
stop_rate: 20.2797%
total_pnl_usd: +197.086724
mean_pnl_usd: +1.378229
median_pnl_usd: -0.894000
gross_profit_usd: 1778.521000
gross_loss_usd: -1581.434276
profit_factor: 1.124625
symbol=XAUUSD | side=sell | decision_hour_utc=05

fills: 103
stops: 24
stop_rate: 23.3010%
total_pnl_usd: +157.742462
mean_pnl_usd: +1.531480
median_pnl_usd: -2.620000
gross_profit_usd: 1458.861000
gross_loss_usd: -1301.118538
profit_factor: 1.121236
symbol=USDJPY | side=buy | decision_hour_utc=01

fills: 253
stops: 14
stop_rate: 5.5336%
total_pnl_usd: +80.258698
mean_pnl_usd: +0.317228
median_pnl_usd: -0.371867
gross_profit_usd: 2085.482421
gross_loss_usd: -2005.223723
profit_factor: 1.040025
symbol=XAUUSD | decision_hour_utc=18

fills: 100
stops: 8
stop_rate: 8.0000%
total_pnl_usd: +19.205881
mean_pnl_usd: +0.192059
median_pnl_usd: -0.742000
gross_profit_usd: 595.908000
gross_loss_usd: -576.702119
profit_factor: 1.033303
symbol=XAUUSD | decision_hour_utc=01

fills: 179
stops: 24
stop_rate: 13.4078%
total_pnl_usd: +11.291354
mean_pnl_usd: +0.063080
median_pnl_usd: -1.028000
gross_profit_usd: 1314.119000
gross_loss_usd: -1302.827646
profit_factor: 1.008667
symbol=USDJPY | stop_distance_spread_bucket=>=50x | estimated_gross_leverage_bucket=1-3x

fills: 434
stops: 20
stop_rate: 4.6083%
total_pnl_usd: +39.241651
mean_pnl_usd: +0.090419
median_pnl_usd: -0.818062
gross_profit_usd: 4814.201325
gross_loss_usd: -4774.959674
profit_factor: 1.008218
side=sell | decision_hour_utc=18

fills: 132
stops: 11
stop_rate: 8.3333%
total_pnl_usd: +6.031575
mean_pnl_usd: +0.045694
median_pnl_usd: -1.676802
gross_profit_usd: 851.782489
gross_loss_usd: -845.750913
profit_factor: 1.007132
Interpretation:

Positive decision-time observable buckets do exist, but this is not a strategy.

Important caution:

These are in-sample bucket leads.
Many are time-of-day buckets and may be regime/session artifacts.
Several 100+ fill buckets are barely above PF 1.0 and likely fragile.
The best 30-fill lead has only 44 fills and a negative median despite high total PnL.
A profitable bucket does not prove deployable edge.
Any positive-core lead needs temporal stability checks before any strategy hypothesis.
No H021 strategy has been implemented.
No H021 strategy is validated.
No live trading is approved.
Phase 4 is not approved.

Current H021 Research State
What we know:

H020 survived strict guard validation but failed catastrophically on performance.
H020/H021 fills show:
signal-flip exits are profitable in aggregate,
stop exits are highly destructive.
Stop-outs concentrate by:
tight stop-distance/spread buckets,
higher estimated gross leverage buckets,
certain decision hours,
USDJPY more than XAUUSD.
Simple exclusion rules improve losses but retain negative expectancy.
Positive bucket search found in-sample positive decision-time buckets.
There is not yet evidence of a promotable strategy.
No positive bucket has been tested for temporal stability.
Current H021 question:

Can any sizeable decision-time observable positive bucket remain positive across time splits or rolling periods after modeled costs under strict broker-native H4/M1 simulation?

Important:

“Decision-time observable” means the feature must be known at or before the H4 decision timestamp, before entry.
Realized exit reason and realized PnL are labels/outcomes, not features.
Do not use future information to filter entries.
Do not remove stops.

Recommended Next Engineering Action
Next action should be a diagnostic, not a strategy.

Recommended diagnostic:

H021 positive bucket temporal stability diagnostic.

Candidate new files:

scripts\diagnose_h021_positive_bucket_stability_real.py
tests\test_h021_positive_bucket_stability_real_script.py
Reuse:

scripts\diagnose_h021_stop_precursors_real.py
build_decision_contexts
enrich_fills_with_decision_context
H021StopPrecursorRecord
scripts\diagnose_h021_positive_bucket_search_real.py
bucket field definitions and bucket summarization logic if useful
Goal:

For promising positive bucket leads, split their fills over time and report whether expectancy persists.

Suggested lead buckets to test first:

symbol=USDJPY, side=sell, decision_hour_utc=06
symbol=XAUUSD, side=sell, decision_hour_utc=01
symbol=XAUUSD, side=buy, decision_hour_utc=18
symbol=XAUUSD, decision_hour_utc=17
symbol=XAUUSD, side=sell, decision_hour_utc=05
symbol=XAUUSD, decision_hour_utc=06
symbol=USDJPY, side=buy, decision_hour_utc=01
symbol=USDJPY, stop_distance_spread_bucket=>=50x, estimated_gross_leverage_bucket=1-3x
Suggested time splits:

calendar year by decision_time
first half vs second half by chronological fill order
optional rolling or expanding periods later, but do not overcomplicate first pass
Output metrics per bucket and time split:

bucket label
period label
fill count
stop count
stop rate
total PnL USD
mean PnL USD
median PnL USD
gross profit USD
gross loss USD
profit factor
Interpretation rules:

A bucket with one profitable year and several losing years is not stable.
A bucket with only one large winner cluster is not stable.
A 100+ fill bucket with PF > 1 overall but PF < 1 in most yearly splits is probably noise.
A stable lead still is not a strategy; it would only justify a later pre-registered strategy hypothesis.
Do not implement a trading rule directly from in-sample positive buckets.
Do not:

add ML,
tune leverage,
alter costs,
weaken guards,
remove stops,
broaden symbols,
approve live trading.
Absolute Do-Not Rules
Do not:

live trade,
approve Phase 4,
treat H020 guard-validation success as profitability,
treat H021 positive buckets as a validated strategy,
implement a strategy directly from in-sample positive buckets,
revive H020 by casually tuning caps,
weaken H018 hard guards,
raise hard leverage limits casually,
lower modeled costs casually,
switch stop panels casually,
remove stops casually,
broaden symbols,
add ML,
use HistData,
combine broker H4 with HistData M1,
use sparse 2018 through 2021-06 broker-native prefix as dense M1,
include incomplete H4/M1 windows,
impute M1 bars,
forward-fill or backfill M1 bars,
synthesize bars,
modify raw broker files,
commit raw MT5 CSV files,
change .gitignore from /data/ to data/,
continue development while local commits are unpushed,
allow full-test count to drop below 633 without explicit test-removal intent.
Known Repo Hygiene Lessons
Do not repeat these mistakes:

.gitignore once had unrooted data/, which risked excluding quantcore/data.
Some older commits missed files because git add was incomplete.
An empty HANDOFF_16.md was accidentally committed once.
A mistaken empty root-level HANDOFF_43.md was created once and was not to be committed.
Markdown code fences have been damaged by paste before.
PowerShell does not support Linux heredocs.
VS Code can keep unsaved buffers that overwrite edits.
If terminal output shows command echo ambiguity, verify with Select-String or file previews before proceeding.
Always inspect git status.
Always push commits.
Always verify git ls-files after commits.
Treat code test-count drops as regressions.
If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.
Network/DNS push failures can happen; stop development until git push succeeds.
For long handoffs, use VS Code manual editing or a PowerShell here-string.
A broad text replacement once accidentally inserted H018MaximumPortfolioGrossLeverageError into existing per-trade pytest.raises calls. Focused tests caught it.
PowerShell line-ending warnings like LF will be replaced by CRLF can be harmless, but verify with git diff --ignore-space-at-eol before restoring.
Exact First Response The Next AI Should Give
The next AI should respond briefly:

text
Understood. Continuing after HANDOFF_57.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
- Current branch should be main.
- Current full-test anchor is 633 passed.
- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 failed and is in the graveyard.
- H020 survived strict event guard validation but failed performance badly:
  ending equity \$819.07,
  total return -91.8093%,
  max drawdown -91.8860%,
  profit factor 0.757663.
- H020 is in the graveyard.
- H021 has started as diagnostics-first research, not a new strategy.
- H021 decomposition showed:
  signal_flip exits made +9503.32,
  stop exits lost -18684.26.
- H021 stop precursor diagnostics showed stop-outs concentrate by tight stop distance, high estimated gross leverage, and certain decision hours.
- H021 candidate exclusion diagnostics showed simple exclusions improve losses but do not reveal a profitable core.
- H021 positive bucket search found in-sample positive decision-time buckets, including:
  USDJPY sell at decision_hour_utc=06 with 100 fills, PF 1.281885, PnL +\$331.99,
  XAUUSD sell at decision_hour_utc=01 with 94 fills, PF 1.732129, PnL +\$386.01,
  XAUUSD buy at decision_hour_utc=18 with 67 fills, PF 1.363435, PnL +\$135.67.
- These are leads only, not a strategy.
- Current H021 question is whether any positive bucket lead is temporally stable.
- No live trading is approved. Phase 4 is not approved.

Please run:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.

After hygiene passes, I will continue with H021 positive bucket temporal stability diagnostics, not strategy implementation.