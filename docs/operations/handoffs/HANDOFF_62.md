# HANDOFF 62 - After H023 Preliminary Entry Edge Result

If any older handoff conflicts with this file, this HANDOFF_62 wins.

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

- `docs\operations\handoffs\HANDOFF_62.md`

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
- Avoid running real-data diagnostics casually because they can take a long time.
- For real-data diagnostics, use explicit user authorization and run one at a time.

Current user sentiment:

- The user is eager to deploy but frustrated by long diagnostics and errors after waiting.
- Important response discipline: do not let urgency become deployment approval.
- Be direct: the project is closer to understanding failure modes, but is not close to a safe demo EA deployment.

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
  - Run full `python -m pytest -q` before commit.
  - Current full-test anchor: `674 passed`.
- If full tests pass but count drops below `674` without explicit planned test removal, stop and treat as regression.

Git after changes:

- `git diff --check` or `git diff --cached --check` as appropriate.
- `git diff --stat` or `git diff --cached --stat` as appropriate.
- `git add touched files`
- `git commit`
- `git push`
- `git status`
- `git ls-files touched files`

Runtime discipline:

- Full pytest is currently fast enough when run locally:
  - latest observed full suite: `674 passed in 23.54s`
- Real-data diagnostics can take much longer.
- Recent H023 real-data run took roughly an hour and then crashed in reporting after the main summary printed.
- For docs-only changes, do not run pytest.
- For small code changes, run focused tests first, then full tests before commit.
- For real-data diagnostics, ask explicitly and remind that the action is research-only.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -15
Expected after this handoff is committed and pushed:

branch main
up to date with origin/main
working tree clean
Expected latest commit after this handoff:

Add handoff document #62 after H023 preliminary result
Recent important commits should include:

9563379 Record H023 preliminary entry edge result
ce40929 Fix H023 split report formatting
fc9492b Fix H023 H020 signal source handling
d1c017b Fix H023 script EOF whitespace
dca9f37 Fix H023 real data loader path
728c869 Fix H023 test file EOF whitespace
ccfd173 Add H023 entry edge diagnostic
16b2252 Add H023 entry edge hypothesis seed
09fde16 Add handoff document #61 after H022 risk lifecycle diagnostic
6bd17fd Record H022 risk lifecycle diagnostic result
de5c021 Add H022 risk lifecycle variant diagnostic
Do not require pytest for the first check unless code has changed or status is not clean.

Current Test Anchor
Current full-test anchor after H023 reporting fix:

674 passed in 23.54s
Recent anchors:

after H023 split report formatting fix: 674 passed
after H023 H020 signal source fix: 673 passed
after H023 real loader path fix: 672 passed
after H023 initial diagnostic implementation: 671 passed
after H022 risk/lifecycle diagnostic: 666 passed
after H021 fixed lifecycle variant diagnostic: 661 passed
after H021 bridge hold-horizon diagnostic: 655 passed
after H021 signal-flip precursor diagnostic: 647 passed
after H021 positive bucket temporal stability diagnostic: 639 passed
after H021 positive bucket search diagnostic: 633 passed
If full test count drops below 674 without planned test removal, treat it as a regression.

Important Paths
H023 files:

docs\operations\H023_HYPOTHESIS_SEED.md
docs\operations\H023_ENTRY_EDGE_PRELIMINARY_RESULT.md
scripts\diagnose_h023_entry_edge_real.py
tests\test_h023_entry_edge_real_script.py
H022 files:

docs\operations\H022_HYPOTHESIS_SEED.md
docs\operations\H022_RISK_LIFECYCLE_RESULT.md
scripts\diagnose_h022_risk_lifecycle_variants_real.py
tests\test_h022_risk_lifecycle_variants_real_script.py
H021 files:

scripts\diagnose_h021_trade_decomposition_real.py
scripts\diagnose_h021_stop_precursors_real.py
scripts\diagnose_h021_candidate_exclusions_real.py
scripts\diagnose_h021_positive_bucket_search_real.py
scripts\diagnose_h021_positive_bucket_stability_real.py
scripts\diagnose_h021_signal_flip_precursors_real.py
scripts\diagnose_h021_bridge_hold_horizon_real.py
scripts\diagnose_h021_fixed_lifecycle_variants_real.py
Important docs:

docs\operations\H019_GRAVEYARD_RECORD.md
docs\operations\H020_HYPOTHESIS_SEED.md
docs\operations\H020_GRAVEYARD_RECORD.md
docs\operations\H021_HYPOTHESIS_SEED.md
docs\operations\H022_HYPOTHESIS_SEED.md
docs\operations\H022_RISK_LIFECYCLE_RESULT.md
docs\operations\H023_HYPOTHESIS_SEED.md
docs\operations\H023_ENTRY_EDGE_PRELIMINARY_RESULT.md
docs\operations\HYPOTHESIS_LEDGER.md
docs\operations\handoffs\HANDOFF_61.md
docs\operations\handoffs\HANDOFF_62.md
Important docs note:

Do not assume H021_GRAVEYARD_RECORD.md exists.
The user previously decided not to update HYPOTHESIS_LEDGER.md, H021_HYPOTHESIS_SEED.md, or create H021_GRAVEYARD_RECORD.md.
H021 temporal stability, bridge horizon, and fixed lifecycle results are preserved in handoffs for now unless explicitly asked otherwise.
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
H021 is diagnostics-first research and failed to produce a validated strategy.
H021 positive bucket leads failed temporal stability.
H021 signal-flip and bridge-horizon diagnostics found useful structural clues but no validated strategy.
H021 fixed lifecycle variants failed.
H022 first risk/lifecycle diagnostic reduced damage but still failed expectancy and pass criteria.
H023 preliminary entry-edge diagnostic failed across completed 1, 2, 3, and 4 H4 forward horizons.
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
H021 Summary
H021 became a diagnostics-first investigation into whether stop-outs or winners have decision-time precursors.

Key results:

Trade decomposition:

Signal-flip exits:
fills: 3678
total PnL: +\$9503.32
profit factor: 1.494947
Stop exits:
fills: 480
total PnL: -\$18684.26
profit factor: 0.000000
Interpretation:

Signal-flip exits were profitable in aggregate.
Stop exits were deeply destructive.
Do not remove stops; stops are structural risk controls.
Stop precursor diagnostics:

Stop-outs concentrated in tight stop-distance/spread buckets, high estimated gross leverage, certain decision hours, and symbol/side combinations.
Simple exclusions improved losses but did not reveal a profitable retained core.
Positive bucket search:

Found in-sample positive leads.
Temporal stability diagnostic found no practical stable positive bucket.
Do not implement H021 time/session buckets as trading rules.
Bridge hold-horizon diagnostic:

Signal-flip edge was not purely a one-H4-bar accounting artifact.
Replay-only 2, 3, and 4 H4 holds remained profitable in aggregate on baseline signal-flip fills.
Longer holds increased stop exposure and worsened median deltas.
This was a structural clue, not deployable evidence.
Fixed lifecycle variants:

Hold    Return    Max DD    PF
1 H4    -91.8093%    -91.8860%    0.757663
2 H4    -70.5125%    -70.4236%    0.800784
3 H4    -49.8056%    -49.6150%    0.795951
4 H4    -52.9375%    -52.7944%    0.792450
Verdict:

H021 failed to produce a validated strategy.
H021 is not promotable.
No demo/live/Phase 4 approval.
H022 Summary
H022 was pre-registered as a risk/lifecycle reset hypothesis after H021 failed.

Seed doc:

docs\operations\H022_HYPOTHESIS_SEED.md
Result doc:

docs\operations\H022_RISK_LIFECYCLE_RESULT.md
Script:

scripts\diagnose_h022_risk_lifecycle_variants_real.py
Real diagnostic setup:

Research diagnostic only.
Exness broker-native USDJPY/XAUUSD exports only.
Broker-native H4/M1 strict bridge windows only.
Accepted bridge-window count: 5476.
H020 bridge shim used as signal source.
H018 hard guards preserved.
No H021 time/session positive bucket mining.
Best variant by loss reduction:

scale_0_25_min_stop_50x_hold_2
total PnL: -\$882.37
return: -8.8237%
max drawdown: -10.8233%
profit factor: 0.876661
Best variant split facts:

Chronological halves:

first half PnL: -\$227.27, PF 0.936770
second half PnL: -\$655.10, PF 0.815966
Chronological thirds:

third_1 PnL: -\$3.03, PF 0.998667
third_2 PnL: -\$341.75, PF 0.862801
third_3 PnL: -\$537.60, PF 0.775188
H022 verdict:

The first H022 risk/lifecycle diagnostic failed.
No variant reached PF >= 1.15.
No variant produced positive full-period return.
Best variant was still negative after modeled costs.
Temporal splits were weak and deteriorated after the first third.
Risk scaling reduced damage but did not create positive expectancy.
Stop-distance filtering reduced stop rate but did not rescue expectancy.
Interpretation:

H022 confirmed risk/lifecycle shaping can reduce ruin severity.
The current entry/lifecycle stack still did not show validated positive expectancy.
This is not deployable evidence.
H023 Summary
H023 was pre-registered to test whether the current H020 bridge-compatible Donchian/Chandelier-derived entry source has durable forward directional value before further risk/lifecycle engineering.

Seed doc:

docs\operations\H023_HYPOTHESIS_SEED.md
Diagnostic script:

scripts\diagnose_h023_entry_edge_real.py
Tests:

tests\test_h023_entry_edge_real_script.py
Preliminary result doc:

docs\operations\H023_ENTRY_EDGE_PRELIMINARY_RESULT.md
Important implementation commits:

16b2252 Add H023 entry edge hypothesis seed
ccfd173 Add H023 entry edge diagnostic
728c869 Fix H023 test file EOF whitespace
dca9f37 Fix H023 real data loader path
d1c017b Fix H023 script EOF whitespace
fc9492b Fix H023 H020 signal source handling
ce40929 Fix H023 split report formatting
9563379 Record H023 preliminary entry edge result
H023 design:

Uses H020 bridge-compatible signal source.
Uses strict accepted Exness broker-native H4/M1 bridge windows.
Measures neutral forward fixed-horizon outcomes over H4 horizons.
Avoids H021 time/session bucket rules.
Keeps modeled costs.
Preserves H018 hard guards via sizing/geometry checks.
Intended as falsification: if entry edge is negative or unstable, stop trying to rescue this entry stack.
Real diagnostic command run with explicit user authorization:

powershell
python .\scripts\diagnose_h023_entry_edge_real.py
Real diagnostic setup:

accepted bridge-windows: 5476
Exness demo MT5 broker-native exports only
USDJPY/XAUUSD
broker-native H4/M1 strict bridge windows
The first real run completed the expensive main forward-horizon backtests and printed the summary table, then crashed during split-report formatting.

Crash:

TypeError: summarize_fills_by_field() takes 1 positional argument but 2 were given
Cause:

H023 reporting called summarize_fills_by_field(result.fills, "symbol").
Existing H021 helper requires keyword argument: summarize_fills_by_field(result.fills, field="symbol").
Fix:

ce40929 Fix H023 split report formatting
Added format_h023_group_reports.
Added regression test.
Full suite after fix: 674 passed.
H023 preliminary main summary:

Horizon    Accepted    Executed    Skipped    Fills    Ending equity    PnL    Return    Max DD    PF    Win rate
1 H4    5476    3318    2158    3860    $579.99    -$9420.01    -94.2001%    -94.2292%    0.722317    45.8031%
2 H4    5476    2337    3139    2683    $502.58    -$9497.42    -94.9742%    -95.0091%    0.674590    47.3723%
3 H4    5476    1883    3593    2183    $952.95    -$9047.05    -90.4705%    -90.4343%    0.730661    47.0912%
4 H4    5476    1280    4196    1520    $2260.52    -$7739.48    -77.3948%    -77.3261%    0.795790    48.3553%
6 H4    5476    0    5476    0    $10000.00    $0.00    0.0000%    0.0000%    nan    nan
8 H4    5476    0    5476    0    $10000.00    $0.00    0.0000%    0.0000%    nan    nan
H023 preliminary verdict:

H023 failed the main entry-edge falsification test.
The current H020 bridge-compatible entry source did not show robust forward directional edge after modeled costs across the completed 1, 2, 3, and 4 H4 horizons.
Removing stop exits did not reveal hidden profitability.
All completed forward horizons had:
negative full-period return
severe drawdown
profit factor materially below required 1.15
The 6 H4 and 8 H4 rows produced no executions and should be treated as a diagnostic design/runtime issue, not as evidence of profitability.
Interpretation:

H023 points away from further attempts to rescue the current Donchian/Chandelier entry stack with stop/lifecycle/risk tuning.
Combined with H020, H021, and H022, current evidence says no validated strategy exists.
No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.
Rerun policy:

Do not rerun H023 casually; the last real-data run took roughly an hour.
A rerun may be useful only if complete split details are needed for archival after the reporting fix.
The main summary already strongly failed.
Current Research State
What is known:

H020 survived strict event guard validation but failed catastrophically on performance.
H021 decomposition found signal-flip exits profitable in aggregate and stop exits destructive.
Stop-outs concentrate by tight stop distance, high estimated gross leverage, decision hour, and symbol.
Simple exclusions improve losses but retain negative expectancy.
Positive in-sample decision-time buckets exist.
Tested positive buckets failed temporal stability checks.
Signal-flip winner precursors mostly overlap unstable in-sample session/time buckets.
Bridge hold-horizon diagnostic suggests the signal-flip edge is not purely a one-bar bridge artifact, but complete fixed lifecycle variants failed.
H022 first risk/lifecycle variants reduced damage but failed profitability and stability criteria.
H023 preliminary result suggests the current entry stack does not have hidden durable forward edge after modeled costs.
There is no validated strategy.
Current conclusion:

H021 has useful structural/failure-mode clues but is not a strategy.
H022 first diagnostic is useful but failed.
H023 preliminary result is strongly negative.
No current hypothesis is promotable.
No demo deployment is approved.
No live trading is approved.
Phase 4 is not approved.
We are not close to a safe demo EA deployment.
Deployment Reality Check
The user has asked whether we are nearing first demo deployment and is eager to deploy.

Answer:

No, not yet.

Reason:

No variant has validated positive expectancy.
H020/H021 fail performance and stability.
H022 first diagnostic still has negative expectancy.
H023 preliminary result did not reveal entry edge.
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
Recommended immediate next action:

Stop adding diagnostics for the current Donchian/Chandelier entry stack unless there is a genuinely new structural reason.
Do not rerun H023 unless the user explicitly wants complete split details archived.
Consider either:
formally closing/graveyarding H023 after accepting preliminary result,
improving diagnostic runtime/caching before any further real-data diagnostics,
designing a genuinely new H024 entry hypothesis that is not a parameter sweep and not H021 bucket mining.
Best practical next engineering action if continuing research:

Add caching/reuse for expensive H4/M1 accepted windows and enriched intermediate tables before more real-data sweeps.
This directly addresses user frustration with 30-60+ minute diagnostics.
Avoid:

more bucket-mining
direct implementation of H021 positive buckets
treating H022 damage reduction as profitability
treating H023 failed forward horizon result as something to tune around
deployment work
casual reruns of expensive diagnostics
Absolute Do-Not Rules
Do not:

demo trade
live trade
approve Phase 4
treat H020 guard-validation success as profitability
treat H021 positive buckets as a validated strategy
treat H021 signal-flip or bridge-horizon diagnostics as deployment approval
treat H021 fixed lifecycle variants as a rescue
treat H022 loss reduction as a validated strategy
treat H023 preliminary result as deployable
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
allow full-test count to drop below 674 without explicit test-removal intent
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
git diff --check can fail but PowerShell may continue unless $LASTEXITCODE is checked; use:
git diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }
EOF blank-line issues occurred twice during H023 and required follow-up cleanup commits.
Real-data reporting code must be tested, not just backtest core logic. H023 crashed after a long run because split-report formatting was not covered initially.
Exact First Response The Next AI Should Give
Understood. Continuing after HANDOFF_62.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Current branch should be main.
Current full-test anchor is 674 passed.
H017 failed.
H018 is guard/diagnostic work, not a validated strategy.
H019 failed and is in the graveyard.
H020 survived strict event guard validation but failed performance badly:
ending equity \$819.07
total return -91.8093%
max drawdown -91.8860%
profit factor 0.757663
H021 is diagnostics-first research, not a strategy.
H021 decomposition showed:
signal_flip exits made about +\$9503
stop exits lost about -\$18684
H021 positive bucket leads failed temporal stability.
H021 bridge hold-horizon diagnostic found a structural clue but not a deployable strategy.
H021 fixed lifecycle variants failed.
H022 first risk/lifecycle diagnostic failed:
best row was scale_0_25_min_stop_50x_hold_2
PF 0.876661
return -8.8237%
max DD -10.8233%
H023 preliminary entry-edge diagnostic failed:
1 H4 PF 0.722317, return -94.2001%
2 H4 PF 0.674590, return -94.9742%
3 H4 PF 0.730661, return -90.4705%
4 H4 PF 0.795790, return -77.3948%
6/8 H4 produced no executions and are diagnostic design/runtime issues.
H023 split-report crash was fixed in ce40929.
No strategy is validated.
No demo deployment is approved.
No live trading is approved.
Phase 4 is not approved.
Real-data diagnostics can be slow, so avoid running them casually.
Please run:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -15
Then paste the full output.

After hygiene passes, I will continue only with an explicitly authorized next research action.
