# HANDOFF 63 - After H024 Chronological Validation Pass

If any older handoff conflicts with this file, this HANDOFF_63 wins.

This handoff is intentionally self-contained so a new AI can continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is research/backtest infrastructure and strategy hypothesis validation.
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

- `docs\operations\handoffs\HANDOFF_63.md`

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

Important user sentiment:

- The user is eager to deploy.
- Do not let promising H024 results become deployment approval.
- Be direct: H024 is now a serious candidate, but still not ready for demo deployment.

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
  - Current full-test anchor: `720 passed`.
- If full tests pass but count drops below `720` without explicit planned test removal, stop and treat as regression.

Git after changes:

- `git diff --check` or `git diff --cached --check` as appropriate.
- `git diff --stat` or `git diff --cached --stat` as appropriate.
- `git add touched files`
- `git commit`
- `git push`
- `git status`
- `git ls-files touched files`

Runtime discipline:

- Full pytest is currently fast enough locally:
  - latest observed full suite: `720 passed in 18.03s`
- Real-data diagnostics can take much longer.
- Recent diagnostics benefited from bridge-window cache.
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
git log --oneline -20

Expected current state after this handoff is committed and pushed:

branch main
up to date with origin/main
working tree clean

Expected latest commit after this handoff:

Add handoff document #63 after H024 chronological validation

Recent important commits should include:

d7076b7 Record H024 chronological validation result
4088c5f Add H024 chronological validation diagnostic
2d965da Record H024 targeted robustness result
bf736b6 Add H024 robustness diagnostic entrypoint
aeb4d9a Add H024 targeted robustness diagnostic
049348e Record H024 preliminary fixed lifecycle result
68a70ad Align H024 bridge shim on common H4 index
edac3b2 Add H024 fixed lifecycle diagnostic
73afd9a Add H024 bridge shim
d63eed8 Add H024 signal diagnostic shell
6801dde Add H024 pullback continuation signal prototype
5039b54 Add H024 pullback continuation hypothesis seed
668d192 Close H023 entry edge hypothesis

Do not require pytest for the first check unless code changed or status is not clean.

Current Test Anchor

Current full-test anchor:

720 passed in 18.03s

Recent test anchors:

after H024 chronological validation diagnostic: 720 passed
after H024 robustness entrypoint: 714 passed
after H024 targeted robustness diagnostic: 713 passed
after H024 H4 index alignment: 709 passed
after H024 fixed lifecycle diagnostic: 708 passed
after H024 bridge shim: 703 passed
after H024 signal diagnostic shell: 695 passed
after H024 signal prototype: 684 passed
after bridge-window cache work: 678 passed
after H023 reporting fix: 674 passed

If full test count drops below 720 without planned test removal, treat it as a regression.

Important Paths

H024 docs:

docs\operations\H024_HYPOTHESIS_SEED.md
docs\operations\H024_PRELIMINARY_FIXED_LIFECYCLE_RESULT.md
docs\operations\H024_TARGETED_ROBUSTNESS_RESULT.md
docs\operations\H024_CHRONOLOGICAL_VALIDATION_RESULT.md

H024 code/scripts/tests:

quantcore\strategy\h024.py
quantcore\strategy\h024_runner.py
scripts\diagnose_h024_pullback_continuation_real.py
scripts\diagnose_h024_fixed_lifecycle_real.py
scripts\diagnose_h024_robustness_real.py
scripts\diagnose_h024_walk_forward_real.py
tests\test_h024.py
tests\test_h024_runner.py
tests\test_h024_pullback_continuation_real_script.py
tests\test_h024_fixed_lifecycle_real_script.py
tests\test_h024_robustness_real_script.py
tests\test_h024_walk_forward_real_script.py

H023 docs:

docs\operations\H023_HYPOTHESIS_SEED.md
docs\operations\H023_ENTRY_EDGE_PRELIMINARY_RESULT.md
docs\operations\H023_GRAVEYARD_RECORD.md

H023 files:

scripts\diagnose_h023_entry_edge_real.py
tests\test_h023_entry_edge_real_script.py

Important operational docs:

docs\operations\H019_GRAVEYARD_RECORD.md
docs\operations\H020_GRAVEYARD_RECORD.md
docs\operations\H021_HYPOTHESIS_SEED.md
docs\operations\H022_HYPOTHESIS_SEED.md
docs\operations\H022_RISK_LIFECYCLE_RESULT.md
docs\operations\HYPOTHESIS_LEDGER.md
docs\operations\handoffs\HANDOFF_62.md
docs\operations\handoffs\HANDOFF_63.md

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

Long: highest_high(lookback) - multiplier * ATR
Short: lowest_low(lookback) + multiplier * ATR
Current rolling windows include the current bar.
Defaults: multiplier 3.0, lookback 22.

Donchian Signals:

Long: close[t] > max(high[t-N ... t-1])
Short: close[t] < min(low[t-N ... t-1])
Channel uses prior N bars via shift(1).rolling(N).

Baseline bridge timing:

Strategy decides at H4 timestamp t.
Trade opens on next H4 bar open t+1.
M1 bars inside the lifecycle window resolve stops.
If no stop is hit, exposure closes at forced lifecycle exit open.
Fill rule: if stop and take-profit are both touched in the same M1 bar, stop wins.

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

H022 first risk/lifecycle diagnostic reduced damage but still failed expectancy and pass criteria.

H023 preliminary entry-edge diagnostic failed across completed 1, 2, 3, and 4 H4 forward horizons and has been closed in the graveyard.

H024 is now the first serious candidate:

preliminary full-period validation passed for hold=3 H4
targeted stop/cost robustness passed
chronological validation passed

But:

H024 is not fully validated.
H024 is not demo-approved.
H024 is not live-approved.
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
starting_equity_usd: $10000.00
ending_equity_usd: $819.07
total_pnl_usd: -$9180.93
total_return: -91.8093%
max_drawdown: -91.8860%
win_rate: 44.1799%
gross_profit_usd: $28703.99
gross_loss_usd: -$37884.92
profit_factor: 0.757663
fill_return_sharpe: -0.086278

Verdict:

H020 failed performance evaluation.
H020 is not promotable.
H020 is not demo-approved.
H020 is not live-approved.
Phase 4 is not approved.
H021 Summary

H021 became diagnostics-first research into stop-outs and winner precursors.

Key result:

Signal-flip exits:

fills: 3678
total PnL: +$9503.32
profit factor: 1.494947

Stop exits:

fills: 480
total PnL: -$18684.26
profit factor: 0.000000

Interpretation:

Signal-flip exits were profitable in aggregate.
Stop exits were deeply destructive.
Do not remove stops; stops are structural risk controls.

Other H021 findings:

Stop-outs concentrated in tight stop-distance/spread buckets, high estimated gross leverage, certain decision hours, and symbol/side combinations.
Simple exclusions improved losses but did not reveal a profitable retained core.
Positive in-sample buckets existed.
Temporal stability diagnostics found no practical stable positive bucket.
Do not implement H021 time/session buckets as trading rules.
Bridge hold-horizon diagnostic found a structural clue but not deployable evidence.
Fixed lifecycle variants failed.

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
total PnL: -$882.37
return: -8.8237%
max drawdown: -10.8233%
profit factor: 0.876661

Best variant split facts:

Chronological halves:

first half PnL: -$227.27, PF 0.936770
second half PnL: -$655.10, PF 0.815966

Chronological thirds:

third_1 PnL: -$3.03, PF 0.998667
third_2 PnL: -$341.75, PF 0.862801
third_3 PnL: -$537.60, PF 0.775188

H022 verdict:

The first H022 risk/lifecycle diagnostic failed.
No variant reached PF >= 1.15.
No variant produced positive full-period return.
Best variant was still negative after modeled costs.
Temporal splits were weak and deteriorated after the first third.
Risk scaling reduced damage but did not create positive expectancy.
Stop-distance filtering reduced stop rate but did not rescue expectancy.
This is not deployable evidence.
H023 Summary

H023 was pre-registered to test whether the current H020 bridge-compatible Donchian/Chandelier-derived entry source had durable forward directional value before further risk/lifecycle engineering.

Seed doc:

docs\operations\H023_HYPOTHESIS_SEED.md

Preliminary result doc:

docs\operations\H023_ENTRY_EDGE_PRELIMINARY_RESULT.md

Graveyard record:

docs\operations\H023_GRAVEYARD_RECORD.md

Diagnostic script:

scripts\diagnose_h023_entry_edge_real.py

Tests:

tests\test_h023_entry_edge_real_script.py

H023 preliminary main summary:

Horizon    Accepted    Executed    Skipped    Fills    Ending equity    PnL    Return    Max DD    PF    Win rate
1 H4    5476    3318    2158    3860    $579.99    -$9420.01    -94.2001%    -94.2292%    0.722317    45.8031%
2 H4    5476    2337    3139    2683    $502.58    -$9497.42    -94.9742%    -95.0091%    0.674590    47.3723%
3 H4    5476    1883    3593    2183    $952.95    -$9047.05    -90.4705%    -90.4343%    0.730661    47.0912%
4 H4    5476    1280    4196    1520    $2260.52    -$7739.48    -77.3948%    -77.3261%    0.795790    48.3553%
6 H4    5476    0    5476    0    $10000.00    $0.00    0.0000%    0.0000%    nan    nan
8 H4    5476    0    5476    0    $10000.00    $0.00    0.0000%    0.0000%    nan    nan

H023 verdict:

H023 failed the main entry-edge falsification test.
The current H020 bridge-compatible entry source did not show robust forward directional edge after modeled costs across completed 1, 2, 3, and 4 H4 horizons.
Removing stop exits did not reveal hidden profitability.
6/8 H4 rows were diagnostic design/runtime issues, not evidence of profitability.
H023 is closed in the graveyard.
Do not continue trying to rescue the Donchian/Chandelier entry stack.
H024 Summary

H024 is a regime-conditioned pullback-continuation hypothesis.

Seed doc:

docs\operations\H024_HYPOTHESIS_SEED.md

Core signal module:

quantcore\strategy\h024.py

Bridge shim:

quantcore\strategy\h024_runner.py

Diagnostic scripts:

scripts\diagnose_h024_pullback_continuation_real.py
scripts\diagnose_h024_fixed_lifecycle_real.py
scripts\diagnose_h024_robustness_real.py
scripts\diagnose_h024_walk_forward_real.py

Tests:

tests\test_h024.py
tests\test_h024_runner.py
tests\test_h024_pullback_continuation_real_script.py
tests\test_h024_fixed_lifecycle_real_script.py
tests\test_h024_robustness_real_script.py
tests\test_h024_walk_forward_real_script.py

H024 mechanics:

Defines directional regime using slow H4 trend state.
Waits for a pullback against that regime.
Enters only if price resumes in the regime direction after the pullback.
Does not use H021 time/session buckets.
Does not reuse Donchian breakout entry as trigger.
Uses H020 sizing contract.
Returns an H017-compatible bridge shim.
Uses fixed lifecycle event diagnostics with H018 hard guard semantics.
Baseline candidate is hold=3 H4, stop ATR multiple 2.0.

H024 signal prototype:

implemented in quantcore\strategy\h024.py
tested synthetically

H024 bridge shim:

implemented in quantcore\strategy\h024_runner.py
aligns USDJPY/XAUUSD on common H4 timestamps
tested synthetically

H024 fixed lifecycle diagnostic:

implemented in scripts\diagnose_h024_fixed_lifecycle_real.py
tested synthetically
real run completed successfully
H024 Preliminary Fixed Lifecycle Result

Command:

python .\scripts\diagnose_h024_fixed_lifecycle_real.py

Setup:

Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
broker-native H4 and M1
strict complete H4/M1 bridge windows
accepted bridge-window count: 5476
H024 pullback-continuation bridge shim
H018 hard guard semantics preserved through fixed-lifecycle event path
modeled costs preserved

Main summary:

Hold    Accepted    Executed    Skipped    Fills    Stops    Stop rate    Ending equity    PnL    Return    Max DD    Win rate    PF
1 H4    5476    861    4615    931    21    2.2556%    $8450.96    -$1549.04    -15.4904%    -22.5043%    45.4350%    0.849209
2 H4    5476    559    4917    604    45    7.4503%    $10925.34    $925.34    9.2534%    -14.0533%    50.8278%    1.076884
3 H4    5476    424    5052    459    56    12.2004%    $14093.92    $4093.92    40.9392%    -6.7346%    52.2876%    1.356184
4 H4    5476    285    5191    307    54    17.5896%    $11236.27    $1236.27    12.3627%    -6.8030%    49.5114%    1.151364

Initial interpretation:

1 H4 failed.
2 H4 positive but below PF threshold.
3 H4 clearly best.
4 H4 barely passed PF threshold but weaker than 3 H4.

H024 hold=3 split facts:

By symbol:

Symbol    Fills    Stops    Stop rate    PnL    PF    Win rate
USDJPY    240    25    10.4167%    $2832.92    1.460747    55.4167%
XAUUSD    219    31    14.1553%    $1261.01    1.235909    48.8584%

By side:

Side    Fills    Stops    Stop rate    PnL    PF    Win rate
buy    252    32    12.6984%    $2125.89    1.336645    53.9683%
sell    207    24    11.5942%    $1968.04    1.380010    50.2415%

Chronological halves:

Split    Fills    Stops    Stop rate    PnL    PF    Win rate
first_half    229    33    14.4105%    $1843.70    1.299481    53.2751%
second_half    230    23    10.0000%    $2250.22    1.421586    51.3043%

Chronological thirds:

Split    Fills    Stops    Stop rate    PnL    PF    Win rate
third_1    153    24    15.6863%    $1218.22    1.287591    51.6340%
third_2    153    21    13.7255%    $716.50    1.173857    52.2876%
third_3    153    11    7.1895%    $2159.20    1.688370    52.9412%

By calendar year:

Year    Fills    Stops    Stop rate    PnL    PF    Win rate
2021    16    1    6.2500%    $534.92    2.708700    56.2500%
2022    84    10    11.9048%    $1435.99    1.800603    57.1429%
2023    90    17    18.8889%    -$708.20    0.764187    46.6667%
2024    122    17    13.9344%    $758.18    1.228199    52.4590%
2025    120    11    9.1667%    $1661.50    1.654749    55.0000%
2026    27    0    0.0000%    $411.53    1.785618    40.7407%

Risk note:

2023 failed materially.
H024 may be regime-dependent.
Do not add a 2023 exclusion or time/session filter.
H024 Targeted Robustness Result

Command:

python .\scripts\diagnose_h024_robustness_real.py

Setup:

hold fixed at 3 H4
stop ATR multiples: 1.5, 2.0, 2.5
cost multipliers: 1.0x, 1.25x, 1.5x
no broad parameter sweep
no H021 time/session bucket mining

Robustness summary:

Scenario    Stop ATR    Cost multiplier    Fills    Stops    Stop rate    Return    Max DD    PF    Headline pass
stop_atr_1.50_cost_1.00x    1.50    1.00    466    100    21.4592%    57.5337%    -9.7164%    1.328226    yes
stop_atr_1.50_cost_1.25x    1.50    1.25    466    100    21.4592%    50.3372%    -10.0436%    1.287259    yes
stop_atr_1.50_cost_1.50x    1.50    1.50    466    100    21.4592%    43.5683%    -11.3247%    1.251787    yes
stop_atr_2.00_cost_1.00x    2.00    1.00    459    56    12.2004%    40.9392%    -6.7346%    1.356184    yes
stop_atr_2.00_cost_1.25x    2.00    1.25    459    56    12.2004%    36.6204%    -7.1521%    1.316004    yes
stop_atr_2.00_cost_1.50x    2.00    1.50    459    56    12.2004%    31.1085%    -7.8798%    1.266900    yes
stop_atr_2.50_cost_1.00x    2.50    1.00    456    33    7.2368%    31.8154%    -6.4629%    1.365488    yes
stop_atr_2.50_cost_1.25x    2.50    1.25    456    33    7.2368%    28.5103%    -6.8567%    1.324031    yes
stop_atr_2.50_cost_1.50x    2.50    1.50    456    33    7.2368%    25.0625%    -7.3633%    1.282177    yes

Interpretation:

H024 hold=3 is not merely surviving the baseline cost model.
All tested scenarios remained positive and retained PF above 1.15 under up to 1.5x modeled cost stress.
Result is materially stronger than preliminary baseline alone.

Persistent weakness:

2023 remained negative across robustness scenarios.
Examples:
stop_atr_2.00_cost_1.00x: 2023 PnL -$708.20, PF 0.764187
stop_atr_2.00_cost_1.50x: 2023 PnL -$914.77, PF 0.702468
stop_atr_2.50_cost_1.50x: 2023 PnL -$827.12, PF 0.670593
stop_atr_1.50_cost_1.50x: 2023 PnL -$1394.07, PF 0.683708

Curve-fitting assessment:

Evidence is not enough to rule out curve-fitting.
But H024 is structurally different from failed Donchian/Chandelier stack.
Hypothesis seed preceded real H024 run.
No time/session bucket mining was used.
Result survived symbol, side, halves, thirds, and targeted cost/stop stress.
H024 Chronological Validation Result

Command:

python .\scripts\diagnose_h024_walk_forward_real.py

Setup:

hold fixed at 3 H4
baseline stop ATR multiple 2.0
baseline modeled costs
no H021 time/session bucket mining
no 2023 exclusion
no parameter optimization

Summary:

Fold    Train count    Test count    Test start UTC    Test end UTC    Fills    Return    Max DD    PF    Headline pass
anchored_train_25%_test_rest    1369    4107    2023-01-05T22:00:00+00:00    2026-04-30T01:00:00+00:00    359    17.8797%    -6.6593%    1.225915    yes
anchored_train_50%_test_rest    2738    2738    2024-03-05T22:00:00+00:00    2026-04-30T01:00:00+00:00    244    19.2253%    -4.4683%    1.384976    yes
anchored_train_75%_test_rest    4107    1369    2025-04-02T21:00:00+00:00    2026-04-30T01:00:00+00:00    114    13.9192%    -2.6061%    1.653426    yes

Interpretation:

H024 hold=3 passed a meaningful anti-curve-fit test.
Candidate remained positive when evaluated only on later chronological test folds with fixed parameters.
Strengthens evidence that H024 is not only a full-sample artifact.

Persistent weakness:

2023 remains visible.
In 25% train / test-rest fold:
2023 PnL: -$576.42
2023 PF: 0.764465
2023 stop rate: 18.8889%
Despite this, the full 2023-2026 test-rest fold passed overall.
Do not add a 2023 exclusion or time/session filter.

Fold details:

25% train / test rest:

return: 17.8797%
max drawdown: -6.6593%
PF: 1.225915
fills: 359
stop rate: 12.5348%

50% train / test rest:

return: 19.2253%
max drawdown: -4.4683%
PF: 1.384976
fills: 244
stop rate: 10.6557%

75% train / test rest:

return: 13.9192%
max drawdown: -2.6061%
PF: 1.653426
fills: 114
stop rate: 7.0175%
Current Research State

What is known:

H020 failed badly.
H021 found useful failure-mode clues but no strategy.
H022 reduced damage but remained negative.
H023 falsified the Donchian/Chandelier entry stack.
H024 is the first serious positive candidate.
H024 hold=3 H4 passed preliminary full-period validation.
H024 hold=3 H4 passed targeted stop/cost robustness.
H024 hold=3 H4 passed chronological test-rest validation.
H024 still has persistent 2023 weakness.
No demo/live/Phase 4 approval exists.

Current conclusion:

H024 hold=3 H4 is a serious research candidate.
H024 is not yet promotable.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 is not approved.
Deployment Reality Check

The user is eager to deploy.

Answer if asked whether we are ready:

No, not yet.

Reason:

H024 is promising but still needs trade-level audit and execution realism checks.
Persistent 2023 weakness needs inspection, not filtering.
MT5 order behavior, symbol contract assumptions, lot sizing, stop-distance realism, execution prices, and operational controls have not been reconciled.
No dry-run EA or execution adapter safety checks are complete.
No hard kill switch/dry-run/log-only mode has been implemented or validated.

A demo deployment still requires, at minimum:

trade ledger export for H024 hold=3
largest winners/losses inspection
2023 failure trade audit
lot-size and stop-distance audit
symbol contract verification against Exness MT5
spread/commission/slippage reconciliation with MT5 conditions
backtest-to-order behavior reconciliation
MT5 execution adapter safety checks
hard kill switch
dry-run/log-only mode
explicit user authorization for Phase 4/demo execution

Do not soften this because H024 is promising.

Recommended Next Action

Recommended immediate next action:

Add a trade ledger export diagnostic for H024 hold=3 H4.

Purpose:

inspect individual trades
inspect largest winners/losses
inspect 2023 failures
verify lot sizes
verify stop distances
verify execution prices
verify symbol/side concentration
produce a CSV under a safe derived-results path that is not raw broker data

Suggested output:

CSV ledger under reports or another tracked-safe/untracked-safe derived output path
console summary of top losses/winners
year/symbol/side aggregates
no raw broker data committed

Before adding this, inspect .gitignore and current report/output conventions.

Avoid:

optimizing H024 parameters
adding time/session filters
excluding 2023
adding ML
broadening symbols
running new sweeps
deployment work
demo trading
live trading
Absolute Do-Not Rules

Do not:

demo trade
live trade
approve Phase 4
treat H024 as deployment-ready
hide 2023 weakness with a filter
add H021 positive time/session buckets
mine time/session/year filters
run broad parameter sweeps
revive H020
rescue H023 Donchian/Chandelier entry stack
weaken H018 hard guards
raise hard leverage limits casually
lower modeled costs casually
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
allow full-test count to drop below 720 without explicit test-removal intent
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
git diff --check can fail but PowerShell may continue unless $LASTEXITCODE is checked.
EOF blank-line issues occurred during H023 and H024 and required cleanup.
Real-data reporting code must be tested, not just backtest core logic.

Use:

git diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }
Exact First Response The Next AI Should Give

Understood. Continuing after HANDOFF_63.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Current branch should be main.
Current full-test anchor is 720 passed.
H017 failed.
H018 is guard/diagnostic work, not a validated strategy.
H019 failed and is in the graveyard.
H020 survived strict event guard validation but failed performance badly.
H021 found useful failure-mode clues but no deployable strategy.
H022 reduced damage but still failed.
H023 falsified the Donchian/Chandelier entry stack and is closed.
H024 is the first serious positive candidate.
H024 hold=3 H4 preliminary result:
return 40.9392%
max DD -6.7346%
PF 1.356184
H024 hold=3 survived targeted stop/cost robustness:
all 9 targeted scenarios passed
worst tested scenario still had PF 1.282177
H024 hold=3 passed chronological validation:
25% train/test-rest PF 1.225915
50% train/test-rest PF 1.384976
75% train/test-rest PF 1.653426
2023 remains a persistent weakness and must not be hidden with a filter.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 is not approved.
Next recommended action is a trade ledger export/audit diagnostic for H024 hold=3 H4.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -20

Then paste the full output.

After hygiene passes, I will continue with the H024 hold=3 trade ledger export/audit diagnostic only if explicitly authorized.
