# HANDOFF 60 - After H021 Fixed Lifecycle Variant Diagnostic

If any older handoff conflicts with this file, this HANDOFF_60 wins.

This handoff is intentionally self-contained so a new AI can continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is research/backtest infrastructure and strategy hypothesis work.
- No execution approval.
- No live trading approval.
- No demo deployment approval.
- No Phase 4 approval.

Environment:

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

Handoff path:

- `docs\operations\handoffs\HANDOFF_60.md`

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

Current user sentiment:

- The user is eager to deploy.
- Important response discipline: do not let urgency become deployment approval.
- Be direct: the project is closer to understanding failure modes, but is not yet close to a safe demo EA deployment.

## Non-Negotiable Environment Rules

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
- No WSL

Do not use Linux/macOS heredoc syntax such as:

- `python - <<'PY'`

PowerShell does not support that.

Use PowerShell here-strings or normal files only.

## Practical Workflow Rules

General:

1. Start each phase with `git status`.
2. Do one real action at a time.
3. Use explicit Windows paths.
4. Never continue while local commits are unpushed.
5. Always commit and push completed work.
6. Always verify touched files are tracked with `git ls-files` after commit.
7. Do not run real-data validation unless explicitly authorized.
8. Do not start Phase 4 execution unless explicitly authorized.
9. Do not demo trade or live trade.

Testing:

- Docs-only edit:
  - No full pytest required by default.
  - Use `git diff --check` / cached diff checks and `git diff --stat`.
- Code edit:
  - Run focused tests.
  - Run full `python -m pytest -q`.
  - Current full-test anchor: `661 passed`.
- If full tests pass but count drops below `661` without explicit planned test removal, stop and treat as regression.

Git after changes:

- `git diff --check` or `git diff --cached --check` as appropriate.
- `git diff --stat` or `git diff --cached --stat` as appropriate.
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
git log --oneline -12
Expected after this handoff is committed and pushed:

branch main
up to date with origin/main
working tree clean
Expected latest commit after this handoff:

Add handoff document #60 after H021 fixed lifecycle diagnostic
Recent important commits should include:

85ddf29 Add H021 fixed lifecycle variant diagnostic
c20a9cd Add handoff document #59 after H021 bridge horizon diagnostic
f033c08 Add H021 bridge hold-horizon diagnostic
ad0d3e3 Add H021 signal-flip precursor diagnostic
3042ae1 Add handoff document #58 after H021 stability diagnostic
4156c34 Add H021 positive bucket stability diagnostic
3cc49e2 Add handoff document #57 after H021 positive bucket search
1b7b55b Add H021 positive bucket search diagnostic
b446f31 Add handoff document #56 after H021 exclusion diagnostics
3c69015 Add H021 candidate exclusion diagnostic
9080eb1 Add H021 stop precursor diagnostic
705ddd3 Add handoff document #55 after H021 decomposition diagnostic
Do not require pytest for the first check unless code has changed or status is not clean.

Current Test Anchor
Current full-test anchor after H021 fixed lifecycle variant diagnostic code:

661 passed in 22.68s
Recent anchors:

after H021 fixed lifecycle variant diagnostic: 661 passed
after H021 bridge hold-horizon diagnostic: 655 passed
after H021 signal-flip precursor diagnostic: 647 passed
after H021 positive bucket temporal stability diagnostic: 639 passed
after H021 positive bucket search diagnostic: 633 passed
after H021 candidate exclusion diagnostic: 623 passed
after H021 stop precursor diagnostic: 616 passed
after H021 trade decomposition diagnostic: 611 passed
after H020 performance diagnostic script: 607 passed
after H020 strict validation work: 605 passed
after H020 sizing-intent seed: 600 passed
If full test count drops below 661 without planned test removal, treat it as a regression.

Important Paths
H020 scripts:

scripts\scan_h020_sizing_diagnostics_real.py
scripts\run_h020_strict_event_real.py
scripts\diagnose_h020_performance_real.py
H021 scripts:

scripts\diagnose_h021_trade_decomposition_real.py
scripts\diagnose_h021_stop_precursors_real.py
scripts\diagnose_h021_candidate_exclusions_real.py
scripts\diagnose_h021_positive_bucket_search_real.py
scripts\diagnose_h021_positive_bucket_stability_real.py
scripts\diagnose_h021_signal_flip_precursors_real.py
scripts\diagnose_h021_bridge_hold_horizon_real.py
scripts\diagnose_h021_fixed_lifecycle_variants_real.py
Latest H021 tests:

tests\test_h021_signal_flip_precursors_real_script.py
tests\test_h021_bridge_hold_horizon_real_script.py
tests\test_h021_fixed_lifecycle_variants_real_script.py
Important docs:

docs\operations\H019_GRAVEYARD_RECORD.md
docs\operations\H020_HYPOTHESIS_SEED.md
docs\operations\H020_GRAVEYARD_RECORD.md
docs\operations\H021_HYPOTHESIS_SEED.md
docs\operations\HYPOTHESIS_LEDGER.md
docs\operations\handoffs\HANDOFF_59.md
docs\operations\handoffs\HANDOFF_60.md
Important docs note:

Do not assume H021_GRAVEYARD_RECORD.md exists.
The user previously decided not to update HYPOTHESIS_LEDGER.md, H021_HYPOTHESIS_SEED.md, or create H021_GRAVEYARD_RECORD.md.
Preserve H021 temporal stability, bridge horizon, and fixed lifecycle results in handoffs for now unless explicitly asked otherwise.
Data And Source Rules
Accepted source for strict validation/diagnostics:

Exness demo MT5 broker-native exports only.
Accepted symbols:

USDJPY
XAUUSD
Accepted timeframes:

Broker-native H4
Broker-native M1
Broker timezone used by loader:

Europe/Athens
DST-aware
Accepted strict bridge-window range:

first common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
last common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00
accepted bridge-window count: 5476
A common complete H4/M1 bridge window means:

USDJPY has a broker-native H4 bar at the H4 timestamp.
XAUUSD has a broker-native H4 bar at the same H4 timestamp.
For each symbol, the next H4 timestamp is exactly four hours later.
For each symbol, the M1 window has exactly 240 M1 bars.
No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.
Do not use:

HistData for validation/tuning/production dataset creation.
Broker H4 plus HistData M1 combinations.
Sparse 2018 through 2021-06 broker-native prefix as dense M1.
Incomplete H4/M1 windows.
Do not commit:

raw MT5 CSV files
raw HistData files
large derived datasets
broker/vendor source files
The repo uses root-anchored /data/ in .gitignore.

Do not change it to unanchored data/, because that previously risked excluding quantcore/data/.

Core Backtest Conventions
ATR:

Wilder RMA, not SMA.
First true range is high - low.
Seed at index window - 1 with simple mean of first window true ranges.
Recurrence: ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n.
Chandelier Exit:

Long: highest_high(lookback) - multiplier * ATR.
Short: lowest_low(lookback) + multiplier * ATR.
Current rolling windows include the current bar.
Defaults: multiplier 3.0, lookback 22.
Donchian Signals:

Long: close[t] > max(high[t-N ... t-1]).
Short: close[t] < min(low[t-N ... t-1]).
Channel uses prior N bars via shift(1).rolling(N).
Baseline event bridge timing:

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

spread_price 0.01
commission_usd_per_lot_per_fill 7.0
stop_slippage_atr_fraction 0.05
XAUUSD:

spread_price 0.30
commission_usd_per_lot_per_fill 10.0
stop_slippage_atr_fraction 0.05
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
USDJPY: 0.01
XAUUSD: 0.30
Below threshold fails closed.
Equality passes.
Maximum per-trade USD gross leverage:

Hard max 10.0x
< 10.0 passes
== 10.0 passes
> 10.0 fails closed
Maximum portfolio-wide USD gross leverage:

Hard max 10.0x
Long and short exposures are summed gross, not netted.
< 10.0 passes
== 10.0 passes
> 10.0 fails closed
Violation policy:

Raise explicit error.
Do not silently skip trades.
Do not clip position size.
Do not net long and short notionals.
Do not warn/log-only and continue.
Hypothesis Status Summary
H017 failed.
H018 is guard/diagnostic work only; not a validated strategy.
H019 failed and is in the graveyard.
H020 survived strict guard validation but failed performance badly.
H021 is diagnostics-first research.
H021 positive bucket leads failed temporal stability.
H021 signal-flip and bridge-horizon diagnostics found useful structural clues but no validated strategy.
H021 fixed lifecycle variants failed.
No strategy is currently promotable.
No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.
H020 Summary
H020 was a sizing-contract hypothesis on top of H019 lifecycle semantics.

H020 mechanics:

invalid stop geometry becomes flat/no intent at strategy-intent level
below-spread raw stop distance becomes flat/no intent
per-trade strategy cap = 9.0x gross notional
portfolio strategy cap = 9.0x gross notional
H018 hard guards remain 10.0x and unchanged
explicit intent objects preserve diagnostics
bridge shim converts H020 intent back into H017Result-shaped positions for strict event bridge compatibility
H020 strict guard validation:

command: python .\scripts\run_h020_strict_event_real.py
accepted bridge-windows: 5476
completed without guard violations
H020 performance diagnostic:

command: python .\scripts\diagnose_h020_performance_real.py
accepted_entry_count: 5476
executed_entry_count: 5476
skipped_entry_count: 3176
fill_count: 4158
starting_equity_usd: \$10000.00
ending_equity_usd: \$819.07
total_pnl_usd: -\$9180.93
total_return: -91.8093%
max_drawdown: -91.8860%
win_rate: 44.1799%
gross_profit_usd: \$28703.99
gross_loss_usd: -\$37884.92
profit_factor: 0.757663
fill_return_sharpe: -0.086278
Verdict:

H020 failed performance evaluation.
H020 is not promotable.
H020 is not demo-approved.
H020 is not live-approved.
Phase 4 is not approved.
H021 Diagnostic 1 - Trade Decomposition
Script:

scripts\diagnose_h021_trade_decomposition_real.py
Commit:

0282cf9 Add H021 trade decomposition diagnostic
Real result summary:

By symbol:

USDJPY:

fills: 2827
total_pnl_usd: -7259.73
profit_factor: 0.722826
XAUUSD:

fills: 1331
total_pnl_usd: -1921.21
profit_factor: 0.835695
By side:

Buy:

fills: 2497
total_pnl_usd: -5224.34
profit_factor: 0.766060
Sell:

fills: 1661
total_pnl_usd: -3956.60
profit_factor: 0.745606
By exit reason:

Signal flip:

fills: 3678
win_rate: 49.9456%
total_pnl_usd: +9503.32
profit_factor: 1.494947
Stop:

fills: 480
win_rate: 0.0000%
total_pnl_usd: -18684.26
profit_factor: 0.000000
Interpretation:

Signal-flip exits are profitable in aggregate.
Stop exits are deeply destructive.
Do not remove stops; stops are structural risk controls.
H021 became a diagnostics-first investigation into whether stop-outs or winners have decision-time precursors.
H021 Diagnostic 2 - Stop-Loss Precursors
Script:

scripts\diagnose_h021_stop_precursors_real.py
Commit:

9080eb1 Add H021 stop precursor diagnostic
Real result summary:

accepted bridge-windows: 5476
context rows reconstructed: 5282
fill rows enriched: 4158
Important decision-hour damage:

decision_hour_utc 05: fills 585, stops 117, stop_rate 20.0000%, PnL -2621.09, PF 0.715453
decision_hour_utc 10: fills 303, stops 33, stop_rate 10.8911%, PnL -1092.41, PF 0.601259
decision_hour_utc 22: fills 297, stops 31, stop_rate 10.4377%, PnL -1025.01, PF 0.463573
Stop-distance/spread bucket result:

<2x: stop_rate 94.1176%, PnL -217.79, PF 0.004211
2-5x: stop_rate 75.0000%, PnL -208.99, PF 0.663358
5-10x: stop_rate 64.1975%, PnL -79.02, PF 0.952525
10-20x: stop_rate 47.5248%, PnL -1664.75, PF 0.621684
20-50x: stop_rate 17.2932%, PnL -4018.88, PF 0.738456
>=50x: stop_rate 3.7037%, PnL -2991.50, PF 0.808415
Estimated gross leverage bucket result:

<1x: fills 2934, stop_rate 7.0893%, PnL -3208.78, PF 0.768747
1-3x: fills 942, stop_rate 19.8514%, PnL -1771.23, PF 0.866350
3-6x: fills 227, stop_rate 25.9912%, PnL -1675.21, PF 0.752770
6-9x: fills 55, stop_rate 47.2727%, PnL -2525.70, PF 0.365494
Interpretation:

Stop-outs concentrate.
Tight stops and high estimated gross leverage are dangerous.
Wide stops alone do not create profitability.
H021 Diagnostic 3 - Candidate Exclusions
Script:

scripts\diagnose_h021_candidate_exclusions_real.py
Commit:

3c69015 Add H021 candidate exclusion diagnostic
Baseline:

fills: 4158
stops: 480
stop_rate: 11.5440%
total_pnl_usd: -9180.93
profit_factor: 0.757663
Best/simple exclusion results:

Exclude USDJPY all:

retained_fills: 1331
retained_pnl_usd: -1921.21
retained_profit_factor: 0.835695
Keep only stop_distance_spread_bucket >=50x:

retained_fills: 2754
retained_pnl_usd: -2991.50
retained_profit_factor: 0.808415
Exclude decision hours 05, 10, 22:

retained_fills: 2973
retained_pnl_usd: -4442.42
retained_profit_factor: 0.815076
Exclude estimated gross leverage >=3x:

retained_fills: 3876
retained_pnl_usd: -4980.02
retained_profit_factor: 0.816428
Exclude USDJPY sell:

retained_fills: 3092
retained_pnl_usd: -5543.25
retained_profit_factor: 0.796264
Interpretation:

Simple exclusions improve losses but do not reveal a profitable retained core.
Do not implement a strategy from these exclusion candidates.
H021 Diagnostic 4 - Positive Bucket Search
Script:

scripts\diagnose_h021_positive_bucket_search_real.py
Commit:

1b7b55b Add H021 positive bucket search diagnostic
Real result summary:

accepted bridge-windows: 5476
context rows reconstructed: 5282
fill rows enriched: 4158
Important in-sample positive bucket leads:

XAUUSD, stop_distance_spread_bucket 5-10x:

fills: 44
stops: 20
total_pnl_usd: +639.699759
median_pnl_usd: -7.652802
profit_factor: 1.784845
XAUUSD sell, decision_hour_utc 01:

fills: 94
stops: 9
total_pnl_usd: +386.014161
median_pnl_usd: -0.922500
profit_factor: 1.732129
XAUUSD buy, decision_hour_utc 18:

fills: 67
stops: 6
total_pnl_usd: +135.666425
median_pnl_usd: +0.948000
profit_factor: 1.363435
USDJPY sell, decision_hour_utc 06:

fills: 100
stops: 18
total_pnl_usd: +331.990603
median_pnl_usd: +0.018233
profit_factor: 1.281885
XAUUSD, decision_hour_utc 17:

fills: 146
stops: 16
total_pnl_usd: +133.556329
median_pnl_usd: +0.493500
profit_factor: 1.151079
XAUUSD sell, decision_hour_utc 05:

fills: 103
stops: 24
total_pnl_usd: +157.742462
median_pnl_usd: -2.620000
profit_factor: 1.121236
USDJPY buy, decision_hour_utc 01:

fills: 253
stops: 14
total_pnl_usd: +80.258698
median_pnl_usd: -0.371867
profit_factor: 1.040025
USDJPY, stop_distance_spread_bucket >=50x, estimated_gross_leverage_bucket 1-3x:

fills: 434
stops: 20
total_pnl_usd: +39.241651
median_pnl_usd: -0.818062
profit_factor: 1.008218
Interpretation:

Positive decision-time observable buckets exist in-sample.
These are leads only, not a strategy.
Temporal stability testing was required before strategy implementation.
H021 Diagnostic 5 - Positive Bucket Temporal Stability
Script:

scripts\diagnose_h021_positive_bucket_stability_real.py
Commit:

4156c34 Add H021 positive bucket stability diagnostic
Real result summary:

accepted bridge-windows: 5476
context rows reconstructed: 5282
fill rows enriched: 4158
Overall temporal stability verdict:

No tested positive bucket passed a practical temporal-stability smell test.
Positive buckets look like in-sample/session/regime artifacts, not stable positive expectancy.
A bucket with one or two good periods and several losing periods is not stable.
PF near 1.0 with unstable splits is likely noise.
Do not implement trading rules from these buckets.
Do not promote H020 or H021.
No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.
H021 Diagnostic 6 - Signal-Flip Winner Precursors
Script:

scripts\diagnose_h021_signal_flip_precursors_real.py
Tests:

tests\test_h021_signal_flip_precursors_real_script.py
Commit:

ad0d3e3 Add H021 signal-flip precursor diagnostic
Tests before commit:

focused tests: 8 passed in 2.97s
full suite: 647 passed in 16.24s
Real command run with explicit user authorization:

powershell
python .\scripts\diagnose_h021_signal_flip_precursors_real.py
Real diagnostic setup/result:

accepted bridge-windows: 5476
context rows reconstructed: 5282
fill rows enriched: 4158
Top signal-flip precursor contrast rows:

symbol=XAUUSD, side=sell, decision_hour_utc=01

fills: 94
signal-flip winners: 42
signal-flip winner rate: 44.6809%
stops: 9
stop rate: 9.5745%
losers: 52
total_pnl_usd: +386.014161
median_pnl_usd: -0.922500
signal_flip_winner_pnl_usd: +913.263000
adverse_pnl_usd: -527.248839
profit_factor: 1.732129
symbol=XAUUSD, side=buy, decision_hour_utc=18

fills: 67
signal-flip winners: 34
signal-flip winner rate: 50.7463%
stops: 6
stop rate: 8.9552%
losers: 33
total_pnl_usd: +135.666425
median_pnl_usd: +0.948000
signal_flip_winner_pnl_usd: +508.956000
adverse_pnl_usd: -373.289575
profit_factor: 1.363435
symbol=USDJPY, side=sell, decision_hour_utc=06

fills: 100
signal-flip winners: 50
signal-flip winner rate: 50.0000%
stops: 18
stop rate: 18.0000%
losers: 50
total_pnl_usd: +331.990603
median_pnl_usd: +0.018233
signal_flip_winner_pnl_usd: +1509.741858
adverse_pnl_usd: -1177.751255
profit_factor: 1.281885
Interpretation:

This mostly confirmed the prior H021 story.
Profitable signal_flip winners exist.
Adverse outcomes consume most of the edge.
Many positive rows are the same time/session buckets that already failed temporal stability.
Negative median PnL in many positive-total groups shows fragility.
This does not rescue H021.
Do not implement strategy rules from this table.
H021 Diagnostic 7 - Bridge Hold-Horizon Structural Diagnostic
Script:

scripts\diagnose_h021_bridge_hold_horizon_real.py
Tests:

tests\test_h021_bridge_hold_horizon_real_script.py
Commit:

f033c08 Add H021 bridge hold-horizon diagnostic
Tests before commit:

focused tests: 8 passed in 1.34s
full suite: 655 passed in 16.36s
Real command run with explicit user authorization:

powershell
python .\scripts\diagnose_h021_bridge_hold_horizon_real.py
Real diagnostic setup/result:

accepted bridge-windows: 5476
context rows reconstructed: 5282
fill rows enriched: 4158
baseline signal_flip observations replayed: 11029
Result table:

Hold 2 H4 bars:

observations: 3677
alternate stops: 267
alternate stop rate: 7.2614%
baseline_total_pnl_usd: +9507.299118
alternate_total_pnl_usd: +8040.556686
total_delta_usd: -1466.742432
median_delta_usd: -0.058239
baseline_winners: 1837
winners_retained_profit: 1399
winners_to_loss: 438
winners_stopped: 73
winners_improved: 928
loser_to_profit: 426
alternate_profit_factor: 1.250697
Hold 3 H4 bars:

observations: 3676
alternate stops: 484
alternate stop rate: 13.1665%
baseline_total_pnl_usd: +9502.522959
alternate_total_pnl_usd: +8907.067217
total_delta_usd: -595.455741
median_delta_usd: -0.251977
baseline_winners: 1836
winners_retained_profit: 1282
winners_to_loss: 554
winners_stopped: 161
winners_improved: 919
loser_to_profit: 533
alternate_profit_factor: 1.225454
Hold 4 H4 bars:

observations: 3676
alternate stops: 672
alternate stop rate: 18.2807%
baseline_total_pnl_usd: +9502.522959
alternate_total_pnl_usd: +7682.881191
total_delta_usd: -1819.641768
median_delta_usd: -0.574893
baseline_winners: 1836
winners_retained_profit: 1232
winners_to_loss: 604
winners_stopped: 237
winners_improved: 916
loser_to_profit: 589
alternate_profit_factor: 1.166756
Interpretation:

The signal-flip edge is not purely a one-H4-bar accounting artifact.
Mechanical 2, 3, and 4 H4-bar holds remained profitable in aggregate when replaying only baseline signal_flip fills.
However, longer holds increased stop exposure sharply:
2 bars: 7.2614%
3 bars: 13.1665%
4 bars: 18.2807%
Longer holds converted many baseline winners into losses.
Median delta worsened as horizon extended.
This suggested the current strategy may have some directional/entry value.
It also showed lifecycle, stop, and risk shaping were fragile and unresolved.
This was not deployable evidence.
This led to a complete fixed lifecycle portfolio diagnostic.
H021 Diagnostic 8 - Fixed Lifecycle Variant Diagnostic
Script:

scripts\diagnose_h021_fixed_lifecycle_variants_real.py
Tests:

tests\test_h021_fixed_lifecycle_variants_real_script.py
Commit:

85ddf29 Add H021 fixed lifecycle variant diagnostic
Tests before commit:

focused tests: 6 passed in 4.35s
full suite: 661 passed in 22.68s
Files added:

scripts\diagnose_h021_fixed_lifecycle_variants_real.py
tests\test_h021_fixed_lifecycle_variants_real_script.py
Files were committed, pushed, and verified tracked.

Real command run with explicit user authorization:

powershell
python .\scripts\diagnose_h021_fixed_lifecycle_variants_real.py
Diagnostic design:

Complete portfolio backtests, not replay-only.
H020 bridge shim as signal source.
H018 hard guards preserved.
Exness broker-native USDJPY/XAUUSD H4/M1 data only.
Strict accepted bridge windows only.
Accepted bridge-window count: 5476.
Non-overlapping fixed lifecycle portfolio backtests.
Hold horizons tested:
1 H4 bar
2 H4 bars
3 H4 bars
4 H4 bars
Pre-registered pass/fail criteria:

A lifecycle variant was not promotable unless all were true:

Full-period profit factor >= 1.15.
Full-period total return positive after modeled costs.
Max drawdown better than -25%.
No single symbol contributes more than 75% of total net profit.
No chronological third has profit factor below 0.95.
At least two of three chronological thirds have profit factor >= 1.05.
First half and second half are both positive or near-flat, with neither below -5%.
Stop rate does not rise into structurally dangerous territory versus baseline without compensating PF improvement.
Full test suite remains at least 661 passed.
Real result summary:

Hold	Accepted	Executed	Skipped	Fills	Stops	Stop rate	Ending equity	Total PnL	Return	Max DD	PF
1 H4	5476	3541	1935	4158	480	11.5440%	$819.07	-$9180.93	-91.8093%	-91.8860%	0.757663
2 H4	5476	1572	3904	1918	345	17.9875%	$2948.75	-$7051.25	-70.5125%	-70.4236%	0.800784
3 H4	5476	805	4671	993	196	19.7382%	$5019.44	-$4980.56	-49.8056%	-49.6150%	0.795951
4 H4	5476	721	4755	887	264	29.7632%	$4706.25	-$5293.75	-52.9375%	-52.7944%	0.792450
Hold 1 by symbol:

USDJPY:

fills: 2827
stops: 289
stop_rate: 10.2229%
total_pnl_usd: -7259.73
profit_factor: 0.722826
win_rate: 44.2872%
XAUUSD:

fills: 1331
stops: 191
stop_rate: 14.3501%
total_pnl_usd: -1921.21
profit_factor: 0.835695
win_rate: 43.9519%
Hold 2 by symbol:

USDJPY:

fills: 1180
stops: 198
stop_rate: 16.7797%
total_pnl_usd: -5494.74
profit_factor: 0.779085
win_rate: 43.3898%
XAUUSD:

fills: 738
stops: 147
stop_rate: 19.9187%
total_pnl_usd: -1556.52
profit_factor: 0.852077
win_rate: 46.6125%
Hold 3 by symbol:

USDJPY:

fills: 590
stops: 115
stop_rate: 19.4915%
total_pnl_usd: -4393.59
profit_factor: 0.750881
win_rate: 41.6949%
XAUUSD:

fills: 403
stops: 81
stop_rate: 20.0993%
total_pnl_usd: -586.97
profit_factor: 0.913326
win_rate: 46.4020%
Hold 4 by symbol:

USDJPY:

fills: 533
stops: 149
stop_rate: 27.9550%
total_pnl_usd: -4485.07
profit_factor: 0.752781
win_rate: 41.4634%
XAUUSD:

fills: 354
stops: 115
stop_rate: 32.4859%
total_pnl_usd: -808.68
profit_factor: 0.890182
win_rate: 42.6554%
Important temporal split facts:

Hold 1 chronological thirds:

third_1 PF: 0.754599, PnL -5266.12
third_2 PF: 0.790021, PnL -2389.96
third_3 PF: 0.697678, PnL -1524.85
Hold 2 chronological thirds:

third_1 PF: 0.765774, PnL -3489.33
third_2 PF: 0.822253, PnL -2228.31
third_3 PF: 0.832490, PnL -1333.62
Hold 3 chronological thirds:

third_1 PF: 0.768098, PnL -2261.91
third_2 PF: 0.811905, PnL -1501.06
third_3 PF: 0.817577, PnL -1217.59
Hold 4 chronological thirds:

third_1 PF: 0.616728, PnL -3859.42
third_2 PF: 0.980895, PnL -153.50
third_3 PF: 0.826961, PnL -1280.83
Hold 4 calendar-year note:

2024 was slightly positive:
PnL +75.40
PF 1.011967
This does not rescue the variant because full-period and temporal criteria failed badly.
Fixed lifecycle verdict:

The fixed lifecycle diagnostic failed.
No variant passed pre-registered criteria.
No full-period profit factor reached >= 1.15.
No variant produced positive total return.
No variant had max drawdown better than -25%.
Chronological thirds remained weak/negative.
Longer holds increased stop exposure.
4-H4 had one positive calendar year, 2024, but still failed full-period and temporal-stability requirements.
Interpretation:

The prior bridge hold-horizon clue was real but not sufficient.
Simple fixed lifecycle extension does not rescue H021.
Longer holds reduce total losses partly by skipping many entries, not by creating robust expectancy.
Stop/lifecycle/risk structure remains unresolved.
H021 is still diagnostics-first research, not a strategy.
Current H021 Research State
What is known:

H020 survived strict event guard validation but failed catastrophically on performance.
H021 decomposition found that signal-flip exits are profitable in aggregate and stop exits are destructive.
Stop-outs concentrate by tight stop distance, high estimated gross leverage, decision hour, and symbol.
Simple exclusions improve losses but retain negative expectancy.
Positive in-sample decision-time buckets exist.
Tested positive buckets failed temporal stability checks.
Signal-flip winner precursors mostly overlap unstable in-sample session/time buckets.
Bridge hold-horizon diagnostic suggests the signal-flip edge is not purely a one-bar bridge artifact, but longer holds worsen stop risk and median deltas.
Complete fixed lifecycle portfolio variants failed.
The strategy may contain some weak directional/entry value, but current lifecycle/risk/stop structure destroys it.
Current conclusion:

H021 has useful structural/failure-mode clues.
H021 is not a validated strategy.
H021 is not demo-approved.
H021 is not live-approved.
H021 is not Phase 4-approved.
We are not yet nearing a safe demo EA deployment.
We may be nearing a cleaner graveyard decision or a genuinely new pre-registered H022 risk/lifecycle hypothesis, but not deployment.
Deployment Reality Check
The user has asked whether we are nearing first demo deployment and is eager to deploy.

Answer:

No, not yet.

Reason:

No variant has validated positive expectancy.
H020/H021 fail performance and stability.
Fixed lifecycle variants failed.
There is no validated strategy to execute.
A demo deployment still requires, at minimum:

a pre-registered strategy variant
strict guard validation
full performance validation
temporal stability / walk-forward evidence
MT5 execution adapter safety checks
lot sizing and symbol contract verification
hard kill switch
dry-run/log-only mode
reconciliation between Python backtest assumptions and MT5 order behavior
explicit user authorization for Phase 4/demo execution
Do not soften this because the user is eager.

Recommended Next Action
Pause before adding another diagnostic.

If continuing research, avoid more bucket-mining and avoid treating lifecycle extension as a rescue path.

Reasonable next choices:

Formally graveyard H021.
Pre-register a genuinely new H022 hypothesis focused on risk/lifecycle structure, with strict pass/fail criteria before coding.
If H022 is pursued, it should not be casual tuning. It should be a structurally different hypothesis with:

ex-ante rule definition
no in-sample bucket-mining implementation
H018 hard guards preserved
strict real-data validation
temporal splits/walk-forward
failure criteria before coding
Do not implement a deployable EA from current H021 evidence.

Absolute Do-Not Rules
Do not:

demo trade
live trade
approve Phase 4
treat H020 guard-validation success as profitability
treat H021 positive buckets as a validated strategy
treat H021 signal-flip or bridge-horizon diagnostics as deployment approval
treat fixed lifecycle variants as a rescue
implement a strategy directly from in-sample positive buckets
revive H020 by casually tuning caps
weaken H018 hard guards
raise hard leverage limits casually
lower modeled costs casually
switch stop panels casually
remove stops casually
broaden symbols
add ML
use HistData
combine broker H4 with HistData M1
use sparse 2018 through 2021-06 broker-native prefix as dense M1
include incomplete H4/M1 windows
impute M1 bars
forward-fill or backfill M1 bars
synthesize bars
modify raw broker files
commit raw MT5 CSV files
change .gitignore from /data/ to data/
continue development while local commits are unpushed
allow full-test count to drop below 661 without explicit test-removal intent
Known Repo Hygiene Lessons
Do not repeat these mistakes:

.gitignore once had unrooted data/, which risked excluding quantcore/data.
Some older commits missed files because git add was incomplete.
An empty handoff file was accidentally committed once.
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
Exact First Response The Next AI Should Give
Understood. Continuing after HANDOFF_60.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Current branch should be main.
Current full-test anchor is 661 passed.
H017 failed.
H018 is guard/diagnostic work, not a validated strategy.
H019 failed and is in the graveyard.
H020 survived strict event guard validation but failed performance badly:
ending equity \$819.07
total return -91.8093%
max drawdown -91.8860%
profit factor 0.757663
H020 is not promotable.
H021 is diagnostics-first research, not a strategy.
H021 decomposition showed:
signal_flip exits made about +\$9503
stop exits lost about -\$18684
H021 stop precursor diagnostics showed stop-outs concentrate by tight stop distance, high estimated gross leverage, and certain decision hours.
H021 candidate exclusion diagnostics showed simple exclusions improve losses but do not reveal a profitable core.
H021 positive bucket search found in-sample positive decision-time buckets.
H021 temporal stability diagnostic showed those positive bucket leads are not stable enough across time.
H021 signal-flip precursor diagnostic showed winners exist but adverse outcomes consume much of the edge.
H021 bridge hold-horizon diagnostic showed signal-flip edge is not purely a one-bar artifact, but longer holds increase stop risk and remain fragile.
H021 fixed lifecycle variant diagnostic failed:
1-H4 PF 0.757663, return -91.8093%
2-H4 PF 0.800784, return -70.5125%
3-H4 PF 0.795951, return -49.8056%
4-H4 PF 0.792450, return -52.9375%
No H021 strategy is validated.
No demo deployment is approved.
No live trading is approved.
Phase 4 is not approved.
Please run:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -12
Then paste the full output.

After hygiene passes, I will continue only with an explicitly authorized next research action.