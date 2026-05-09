# HANDOFF_67 - After H024 Log-Only EA Runtime Preflight

If any older handoff conflicts with this file, this HANDOFF_67 wins.

This handoff is self-contained enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is execution-safety preparation after H024 research evidence.
- No demo deployment approval.
- No live trading approval.
- No Phase 4 execution approval.

Environment:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 inside `.venv`
- No WSL

Repository root:

```text
C:\Users\equin\Documents\institutional-ea

Virtual environment:

C:\Users\equin\Documents\institutional-ea\.venv

Branch:

main

GitHub remote:

https://github.com/citradinnda/institutional-ea.git

Previous handoff:

HANDOFF_66 - After H024 MT5 Terminal Preflight Logger And Verifier

This handoff:

HANDOFF_67 - After H024 Log-Only EA Runtime Preflight
Human Preference

The user is tired of excessive documentation and slow ceremony.

Going forward:

Keep responses practical and concise.
Prefer one copy/paste PowerShell block when commands are needed.
Do one real action at a time.
Do not create governance docs unless they preserve a real decision, preserve a handoff, prevent ambiguity, or protect against future confusion.
For docs-only edits, do not run full pytest unless there is a clear reason.
For code edits, tests are mandatory.
Avoid long real-data diagnostics casually.
For real-data diagnostics, get explicit user authorization and run one at a time.
Never soften deployment boundaries because H024 is promising.
The user?s stated goal is: make the EA survive the future, not fit the past.

Important sentiment:

The user is eager to deploy.
The user accepts evidence gates.
Be direct: H024 is serious, but still not demo deployable.
Non-Negotiable Environment Rules

Use:

Windows
PowerShell
VS Code
Python 3.12.10
.venv
No WSL

Do not use Linux/macOS heredoc syntax such as:

python - <<'PY'

PowerShell does not support that. Use PowerShell here-strings or temporary .py files.

Practical Workflow Rules

General:

Start with git status.
Do one real action at a time.
Use explicit Windows paths.
Never continue while local commits are unpushed.
Always commit and push completed work.
Always verify touched files are tracked with git ls-files after commit.
Do not run real-data validation unless explicitly authorized.
Do not start Phase 4 execution unless explicitly authorized.
Do not demo trade or live trade.

Testing:

Docs-only edit:

No full pytest required by default.
Use git diff --check, git diff --cached --check, and git diff --stat.

Code edit:

Run focused tests.
Run full python -m pytest -q before commit.
Current full-test anchor after latest code work: 801 passed.
If full test count drops below 801 without planned test removal, treat as a regression.

Git after changes:

git diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }

git diff --stat
git add <touched files>

git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "git diff --cached --check failed" }

git commit -m "<message>"
git push
git status
git ls-files <touched files>
Immediate First Action For The Next AI

Do not write code first.

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -20

Expected state after this handoff commit:

branch main
up to date with origin/main
no tracked-file changes
likely one untracked local reports/ directory remains

Known latest commits before this handoff commit:

dc9c0c5 Record H024 EA log-only preflight result
92a4433 Require both H024 EA preflight symbols
c3aad45 Add H024 log-only EA preflight verifier
7f04588 Add H024 log-only EA preflight skeleton
2afe24a Add handoff document #66
4557a60 Add H024 MT5 terminal preflight verifier
e83ee15 Record H024 MT5 terminal preflight result
637555f Add H024 MT5 terminal preflight logger
3714203 Add handoff document #65
4808742 Add H024 dry-run action log verifier
c292fb4 Record H024 dry-run action export result
ffbd918 Add H024 dry-run action log export
d5eca9c Add H024 dry-run execution primitives
Current Test Anchor

Current full-test anchor:

801 passed

Latest observed full suite:

801 passed in 16.52s

If full tests pass but count drops below 801 without explicit test-removal intent, stop and treat it as a regression.

Data And Source Rules

Accepted source for strict validation/diagnostics:

Exness demo MT5 broker-native exports only.

Accepted model symbols:

USDJPY
XAUUSD

Observed Exness MT5 account symbol names:

USDJPYm
XAUUSDm

For model/audit comparison, normalize:

USDJPYm -> USDJPY
XAUUSDm -> XAUUSD

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
local reports/*.csv
local reports/*.json

The repo uses root-anchored /data/ in .gitignore.

Do not change it to unanchored data/.

Core Backtest Conventions

ATR:

Wilder RMA, not SMA.
First true range is high - low.
Seed at index window - 1 with simple mean of first window true ranges.
Recurrence:
ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n

Chandelier Exit:

Long: highest_high(lookback) - multiplier * ATR
Short: lowest_low(lookback) + multiplier * ATR

Current rolling windows include current bar.

Defaults:

multiplier 3.0
lookback 22

Donchian Signals:

Long: close[t] > max(high[t-N ... t-1])
Short: close[t] < min(low[t-N ... t-1])

Channel uses prior N bars via shift(1).rolling(N).

Baseline bridge timing:

Strategy decides at H4 timestamp t.
Trade opens on next H4 bar open t+1.
M1 bars inside lifecycle window resolve stops.
If no stop is hit, exposure closes at forced lifecycle exit open.
If stop and take-profit are both touched in same M1 bar, stop wins.

Original/default modeled cost assumptions:

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

Raw stop distance must be at least one modeled/current cost-spec spread.
Equality passes.
Below threshold fails closed.

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
H021 found useful failure-mode clues but no validated strategy.
H022 reduced damage but still failed.
H023 falsified the Donchian/Chandelier entry stack and is closed.
H024 is the first serious positive candidate, but:
H024 is not fully execution-validated.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 execution is not approved.
Important H024 Files

Core H024:

quantcore\strategy\h024.py
quantcore\strategy\h024_runner.py

Backtest/cost execution support:

quantcore\backtest\cost_model.py
quantcore\backtest\h017_event.py
quantcore\backtest\portfolio.py

Dry-run execution-prep:

quantcore\execution\__init__.py
quantcore\execution\h024_dry_run.py
quantcore\execution\h024_dry_run_log.py

EA/log-only runtime prep:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
scripts\verify_h024_ea_preflight_log.py
tests\test_h024_ea_log_only_preflight_static.py
tests\test_h024_ea_preflight_log_verifier.py
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md

Recent scripts:

scripts\audit_h024_broker_symbol_specs.py
scripts\diagnose_h024_observed_broker_costs_real.py
scripts\audit_h024_mt5_order_behavior.py
scripts\dry_run_h024_actions_real.py
scripts\verify_h024_dry_run_actions.py
scripts\log_h024_mt5_terminal_preflight.py
scripts\verify_h024_mt5_terminal_preflight.py
scripts\verify_h024_ea_preflight_log.py

Recent tests:

tests\test_h024_broker_symbol_specs_audit.py
tests\test_h024_observed_broker_costs_real_script.py
tests\test_h024_mt5_order_behavior_audit.py
tests\test_h024_dry_run_execution.py
tests\test_h024_dry_run_log.py
tests\test_h024_dry_run_action_verifier.py
tests\test_h024_mt5_terminal_preflight_logger.py
tests\test_h024_mt5_terminal_preflight_verifier.py
tests\test_h024_ea_log_only_preflight_static.py
tests\test_h024_ea_preflight_log_verifier.py

Recent result/safety docs:

docs\operations\H024_BROKER_SYMBOL_SPEC_AUDIT_RESULT.md
docs\operations\H024_OBSERVED_BROKER_COST_RESULT.md
docs\operations\H024_MT5_ORDER_BEHAVIOR_AUDIT_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\H024_MT5_TERMINAL_PREFLIGHT_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
H024 Mechanics

H024 is a regime-conditioned pullback-continuation hypothesis.

Mechanics:

Defines directional regime using slow H4 trend state.
Waits for a pullback against that regime.
Enters only if price resumes in the regime direction after the pullback.
Does not use H021 time/session buckets.
Does not reuse Donchian breakout entry as trigger.
Uses H020 sizing contract.
Returns an H017-compatible bridge shim.
Uses fixed lifecycle event diagnostics with H018 hard guard semantics.
Baseline candidate is hold=3 H4, stop ATR multiple 2.0.
H024 Prior Evidence Summary
Preliminary Fixed Lifecycle

Command:

python .\scripts\diagnose_h024_fixed_lifecycle_real.py

Setup:

Exness demo MT5 broker-native exports only.
USDJPY and XAUUSD.
Broker-native H4 and M1.
Strict complete H4/M1 bridge windows.
Accepted bridge-window count: 5476.
H024 pullback-continuation bridge shim.
H018 hard guard semantics preserved.
Modeled costs preserved.

Main result:

Hold    Accepted    Executed    Skipped    Fills    Stops    Stop rate    Ending equity    PnL    Return    Max DD    Win rate    PF
1 H4    5476    861    4615    931    21    2.2556%    8450.96    -1549.04    -15.4904%    -22.5043%    45.4350%    0.849209
2 H4    5476    559    4917    604    45    7.4503%    10925.34    925.34    9.2534%    -14.0533%    50.8278%    1.076884
3 H4    5476    424    5052    459    56    12.2004%    14093.92    4093.92    40.9392%    -6.7346%    52.2876%    1.356184
4 H4    5476    285    5191    307    54    17.5896%    11236.27    1236.27    12.3627%    -6.8030%    49.5114%    1.151364

H024 hold=3 was best.

Persistent weakness:

2023 PnL: -708.20
2023 PF: 0.764187

Do not add 2023 exclusion. Do not add time/session filter.

Targeted Robustness

Command:

python .\scripts\diagnose_h024_robustness_real.py

Setup:

hold fixed at 3 H4
stop ATR multiples: 1.5, 2.0, 2.5
cost multipliers: 1.0x, 1.25x, 1.5x
no broad parameter sweep
no H021 time/session bucket mining

All 9 targeted stop/cost scenarios passed.

Worst tested PF:

1.282177
Chronological Validation

Command:

python .\scripts\diagnose_h024_walk_forward_real.py

Summary:

Fold    Train count    Test count    Test start UTC    Test end UTC    Fills    Return    Max DD    PF    Headline pass
anchored_train_25%_test_rest    1369    4107    2023-01-05T22:00:00+00:00    2026-04-30T01:00:00+00:00    359    17.8797%    -6.6593%    1.225915    yes
anchored_train_50%_test_rest    2738    2738    2024-03-05T22:00:00+00:00    2026-04-30T01:00:00+00:00    244    19.2253%    -4.4683%    1.384976    yes
anchored_train_75%_test_rest    4107    1369    2025-04-02T21:00:00+00:00    2026-04-30T01:00:00+00:00    114    13.9192%    -2.6061%    1.653426    yes

Interpretation:

H024 passed a meaningful anti-curve-fit chronological test.
2023 weakness remains visible.
No 2023 exclusion or filter is approved.
Trade Ledger Audit

Command:

python .\scripts\diagnose_h024_trade_ledger_real.py

Output CSV:

reports\h024_hold3_trade_ledger.csv

Do not commit this CSV.

Ledger summary:

Ledger rows: 459
Lifecycle fills: 459
Net PnL USD: 4093.92

By symbol:

Symbol    Fills    Stops    Stop rate    PnL USD    PF    Win rate
USDJPY    240    25    10.4167%    2832.92    1.460747    55.4167%
XAUUSD    219    31    14.1553%    1261.01    1.235909    48.8584%

By year:

Year    Fills    Stops    Stop rate    PnL USD    PF    Win rate
2021    16    1    6.2500%    534.92    2.708700    56.2500%
2022    84    10    11.9048%    1435.99    1.800603    57.1429%
2023    90    17    18.8889%    -708.20    0.764187    46.6667%
2024    122    17    13.9344%    758.18    1.228199    52.4590%
2025    120    11    9.1667%    1661.50    1.654749    55.0000%
2026    27    0    0.0000%    411.53    1.785618    40.7407%
Actual Gross Leverage Audit

Actual gross leverage distribution:

Slice    Fills    Min    Median    Mean    P90    Max
all_fills    459    0.238174    1.055387    1.156458    1.975010    3.285420
stop_fills    56    0.242458    0.946250    1.119561    1.824440    2.499557
2023_stop_fills    17    0.523237    1.027594    1.121347    1.693794    2.446090

Interpretation:

2023 weakness is not leverage pathology.
Largest losses are ordinary stopped-risk losses, not lot-sizing blowups.
Actual gross leverage is moderate and far below H018 10x hard guard.
Direction-Flip Negative Control

Command:

python .\scripts\diagnose_h024_direction_flip_real.py

Result:

Variant    Accepted    Executed    Fills    Stops    Stop rate    Ending equity USD    PnL USD    Return    Max DD    Win rate    Gross profit USD    Gross loss USD    PF    Fill return Sharpe
frozen H024    5476    424    459    56    12.2004%    14093.92    4093.92    40.9392%    -6.7346%    52.2876%    15587.76    -11493.84    1.356184    0.118427
direction flip    5476    402    433    89    20.5543%    6103.11    -3896.89    -38.9689%    -40.2652%    43.8799%    6377.77    -10274.66    0.620728    -0.188633

Baseline minus direction-flip PnL:

7990.81 USD

Interpretation:

Direction-flip control materially failed.
This reduces concern that H024 is generic lifecycle/sizing/volatility exposure.
It supports directional information in frozen H024.
It does not prove future survivability.
Timestamp Shuffle Control

Code exists:

scripts\diagnose_h024_timestamp_shuffle_real.py
tests\test_h024_timestamp_shuffle_real_script.py

But the real diagnostic was too slow. Even after reducing default run count from 100 to 10, it still took too long.

Current instruction:

Do not run brute-force timestamp shuffle again.
It needs cheaper implementation, batching, checkpointing, or replacement.
Do not treat it as completed evidence.
Ledger-Level Permutation Diagnostic

Command:

python .\scripts\diagnose_h024_ledger_permutation.py

Cheap proxy. It randomly reorders realized trade PnLs from the existing ledger 10,000 times.

It does not:

test signal direction
replace full execution timestamp shuffle
rerun M1 lifecycle execution
approve deployment

Observed path:

Metric    Value
total_pnl_usd    4093.92
ending_equity_usd    14093.92
max_drawdown    -6.7346%
min_equity_usd    9901.07
ruin    false

Permutation summary:

permutation runs: 10000
seed: 240240
max-drawdown worse/equal rate: 57.4400%
min-equity worse/equal rate: 64.3000%
permutation ruin count: 0

Interpretation:

Realized H024 trade order was not unusually lucky.
Observed drawdown was slightly better than median/mean permutation, but not suspiciously favorable.
Reduces path-order luck concern.
Does not prove future survivability.
Broker Symbol Spec Audit

Script:

scripts\audit_h024_broker_symbol_specs.py

Test:

tests\test_h024_broker_symbol_specs_audit.py

Result doc:

docs\operations\H024_BROKER_SYMBOL_SPEC_AUDIT_RESULT.md

Observed Exness MT5 CSV used:

symbol,contract_size,quote_currency,lot_step,min_lot,spread_price,commission_usd_per_lot_per_fill,stop_slippage_atr_fraction,max_lot,stops_level_points,freeze_level_points,point,digits
USDJPY,100000.00000000,JPY,0.01000000,0.01000000,0.01800000,0.00000000,0.05000000,300.00000000,0,0,0.0010000000,3
XAUUSD,100.00000000,USD,0.01000000,0.01000000,0.36000000,0.00000000,0.05000000,200.00000000,0,0,0.0010000000,3

Initial static result failed because cost assumptions differed:

USDJPY spread: model 0.010 vs MT5 0.018
XAUUSD spread: model 0.300 vs MT5 0.360
USDJPY commission: model 7.0 vs MT5 0.0
XAUUSD commission: model 10.0 vs MT5 0.0

Instrument assumptions matched:

contract size
quote currency
lot step
minimum lot

This caused broker-cost reconciliation work.

Observed Broker Cost Diagnostic

Code added:

scripts\diagnose_h024_observed_broker_costs_real.py
tests\test_h024_observed_broker_costs_real_script.py

Result doc:

docs\operations\H024_OBSERVED_BROKER_COST_RESULT.md

Core code changed to allow cost override:

quantcore\backtest\h017_event.py
scripts\diagnose_h021_fixed_lifecycle_variants_real.py
scripts\diagnose_h024_fixed_lifecycle_real.py

Observed MT5 cost facts tested:

USDJPY:

spread_price 0.018
commission_usd_per_lot_per_fill 0.0
stop_slippage_atr_fraction 0.05

XAUUSD:

spread_price 0.36
commission_usd_per_lot_per_fill 0.0
stop_slippage_atr_fraction 0.05

Command:

python .\scripts\diagnose_h024_observed_broker_costs_real.py

Result:

Cost case    Hold H4    Accepted    Executed    Skipped    Fills    Stops    Stop rate    Ending equity USD    PnL USD    Return    Max DD    Win rate    Gross profit USD    Gross loss USD    PF    Fill return Sharpe
baseline modeled costs    3    5476    424    5052    459    56    12.2004%    14093.92    4093.92    40.9392%    -6.7346%    52.2876%    15587.76    -11493.84    1.356184    0.118427
observed broker costs    3    5476    424    5052    459    56    12.2004%    14693.82    4693.82    46.9382%    -6.3694%    52.2876%    16224.83    -11531.01    1.407061    0.131688

Delta observed minus baseline:

total_pnl_usd: +599.90
profit_factor: +0.050877

Interpretation:

H024 remains positive and above PF 1.15 under observed Exness MT5 broker cost facts.
Broker-cost reconciliation is materially improved.
The observed zero commission more than offsets wider observed spread in this diagnostic.
This does not prove future survivability.

2023 remains weak under observed broker costs:

PnL: -622.90
PF: 0.793006
stop rate: 18.8889%

Do not add 2023 exclusion. Do not tune H024.

MT5 Static Order Behavior Audit

Code added:

scripts\audit_h024_mt5_order_behavior.py
tests\test_h024_mt5_order_behavior_audit.py

Result doc:

docs\operations\H024_MT5_ORDER_BEHAVIOR_AUDIT_RESULT.md

Local CSV used, not committed:

reports\h024_mt5_order_behavior.csv

Exported from Exness MT5 terminal using Python MetaTrader5 API.

Observed rows:

{'symbol': 'USDJPYm', 'trade_mode': 4, 'execution_mode': 2, 'order_filling_modes': 3, 'order_modes': 127, 'volume_min': 0.01, 'volume_max': 300.0, 'volume_step': 0.01, 'stops_level_points': 0, 'freeze_level_points': 0, 'point': 0.001, 'digits': 3, 'spread_float': True}
{'symbol': 'XAUUSDm', 'trade_mode': 4, 'execution_mode': 2, 'order_filling_modes': 3, 'order_modes': 127, 'volume_min': 0.01, 'volume_max': 200.0, 'volume_step': 0.01, 'stops_level_points': 0, 'freeze_level_points': 0, 'point': 0.001, 'digits': 3, 'spread_float': True}

Audit command:

python .\scripts\audit_h024_mt5_order_behavior.py

Result:

Mismatch count: 0
Verdict: PASS

Interpretation:

Static MT5 order-behavior facts are reconciled for USDJPYm and XAUUSDm.
This does not test actual order placement, rejection behavior, requotes, slippage, market-hours behavior, or modification behavior.
Dry-Run EA Safety Plan

Doc added:

docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md

Key decision:

H024 is promising enough for dry-run/log-only EA preparation.
H024 is not approved for demo deployment.
H024 is not approved for live deployment.
Phase 4 execution is not approved.

Core non-negotiable dry-run rule:

Dry-run/log-only mode must not place, modify, close, or delete orders.
In dry-run/log-only mode, code must not call any live MT5 order-sending function.
The dry-run path may calculate intended actions and write logs only.
Any accidental call path capable of placing an order is a fail-closed defect.
Dry-Run Execution Primitives

Code added:

quantcore\execution\__init__.py
quantcore\execution\h024_dry_run.py
tests\test_h024_dry_run_execution.py

Commit:

d5eca9c Add H024 dry-run execution primitives

What exists:

Pure dry-run/log-only execution-prep layer.
No MT5 import.
No mt5.order_send.
No order tickets.
No execution adapter.

Tests prove:

kill switch defaults to blocked
dry-run emits WOULD_OPEN only, not an order ticket
no MetaTrader5 / mt5 / order-send dependency exists
unknown symbols fail closed
bad broker symbol mapping fails closed
invalid stop geometry fails closed
volume normalization rounds down or blocks
per-trade leverage violation blocks
demo_execution mode is rejected

Primary outputs:

WOULD_OPEN
NO_ACTION
BLOCKED

Forbidden in dry-run:

order ticket
position ticket
order send result
MT5 runtime import/call
Dry-Run Action Log Export

Code added:

quantcore\execution\h024_dry_run_log.py
scripts\dry_run_h024_actions_real.py
tests\test_h024_dry_run_log.py

Commit:

ffbd918 Add H024 dry-run action log export

Command run:

python .\scripts\dry_run_h024_actions_real.py

Output CSV:

reports\h024_dry_run_actions.csv

Do not commit this CSV.

Result:

H024 dry-run/log-only action export
========================================================================
Research only. No demo/live/Phase 4 approval.
No MT5 order-send capability is present in this script.

Strict accepted bridge-windows: 5476
Wrote: C:\Users\equin\Documents\institutional-ea\reports\h024_dry_run_actions.csv
WOULD_OPEN: 459
NO_ACTION: 4707
BLOCKED: 0

Dry-run output only. No demo/live/Phase 4 approval.

Result doc:

docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md

Interpretation:

Dry-run export produced 459 WOULD_OPEN records.
This matches known H024 hold=3 lifecycle fill count.
Dry-run conversion layer can reproduce intended H024 action count from frozen research path.
Still no demo/live/Phase 4 approval.
Dry-Run Action Log Verifier

Code added:

scripts\verify_h024_dry_run_actions.py
tests\test_h024_dry_run_action_verifier.py

Commit:

4808742 Add H024 dry-run action log verifier

Command run:

python .\scripts\verify_h024_dry_run_actions.py

Result:

H024 dry-run action log verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Rows: 5166
WOULD_OPEN: 459
NO_ACTION: 4707
BLOCKED: 0
Violations: 0

Verdict: PASS

Interpretation:

Local dry-run action log shape passed.
No forbidden execution fields were present.
All WOULD_OPEN rows had required audit fields populated.
Still no demo/live/Phase 4 approval.
MT5 Terminal/Account Preflight Logger

Code added:

scripts\log_h024_mt5_terminal_preflight.py
tests\test_h024_mt5_terminal_preflight_logger.py

Commit:

637555f Add H024 MT5 terminal preflight logger

Focused test result:

7 passed

Full suite after commit:

784 passed in 16.09s

Purpose:

Query the local MT5 terminal/account/symbol metadata path.
Verify terminal connection, account facts, symbol selection, current tick, volume constraints, stop/freeze levels, spread, point/digits, and static order metadata.
Write a local JSON report.
Preserve strict no-order-send boundary.

Local output:

reports\h024_mt5_terminal_preflight.json

Do not commit this JSON.

Safety properties:

The logger imports MetaTrader5.
It reads terminal/account/symbol/tick metadata.
It does not place, modify, close, or delete orders.
It wraps MT5 with a guarded reader that blocks forbidden call attempts.
It reports forbidden call attempts.

Forbidden calls guarded:

order_send
order_check
order_calc_margin
order_calc_profit
positions_get
orders_get
history_orders_get
history_deals_get
MT5 Terminal/Account Preflight Result

Result doc:

docs\operations\H024_MT5_TERMINAL_PREFLIGHT_RESULT.md

Commit:

e83ee15 Record H024 MT5 terminal preflight result

Command run with explicit user authorization:

python .\scripts\log_h024_mt5_terminal_preflight.py

Output:

H024 MT5 terminal/account preflight
========================================================================
Research only. No demo/live/Phase 4 approval.

MT5 initialized: True
Forbidden MT5 call attempts: 0
Symbols checked: 2
- USDJPY / USDJPYm: ok (selected and tick available) bid=156.676 ask=156.694 spread=18
- XAUUSD / XAUUSDm: ok (selected and tick available) bid=4715.309 ask=4715.669 spread=360

Wrote: C:\Users\equin\Documents\institutional-ea\reports\h024_mt5_terminal_preflight.json
Verdict: PASS

JSON details:

Generated at UTC: 2026-05-09T13:23:49.195429+00:00
MT5 initialized: true
Forbidden MT5 call attempts: 0
Account company: Exness Technologies Ltd
Account name: Vasa Standard Demo
Account server: Exness-MT5Trial6
Account currency: USD
Account balance: 1246.45
Account equity: 1246.45
Account leverage: 2000
Account trade_allowed: true
Account trade_expert: true
Terminal connected: true
Terminal trade_allowed: false
Terminal tradeapi_disabled: false

Symbols:

Model symbol    Broker symbol    Status    Bid    Ask    Spread points    Trade mode    Execution mode    Filling modes    Order modes    Volume min    Volume max    Volume step    Stops level    Freeze level    Point    Digits
USDJPY    USDJPYm    ok    156.676    156.694    18    4    2    3    127    0.01    300.0    0.01    0    0    0.001    3
XAUUSD    XAUUSDm    ok    4715.309    4715.669    360    4    2    3    127    0.01    200.0    0.01    0    0    0.001    3

Important interpretation:

The read-only MT5 terminal/account preflight passed.
Zero forbidden MT5 call attempts were recorded.
The terminal-level trade_allowed value was false while account-level trade_allowed and trade_expert were true.
This does not block the read-only preflight result, but it must be understood before any later EA-runtime or demo-order gate.
This result does not approve demo trading, live trading, Phase 4, EA execution, order placement, order modification, or order closing.
MT5 Terminal/Account Preflight Verifier

Code added:

scripts\verify_h024_mt5_terminal_preflight.py
tests\test_h024_mt5_terminal_preflight_verifier.py

Commit:

4557a60 Add H024 MT5 terminal preflight verifier

Focused test result:

7 passed in 0.60s

Verifier run against local JSON:

python .\scripts\verify_h024_mt5_terminal_preflight.py

Result:

H024 MT5 terminal/account preflight verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Violations: 0

Verdict: PASS

Safety boundary:

This verifier does not approve demo trading, live trading, or Phase 4.
This verifier only checks the local terminal preflight report shape and safety fields.

Full suite after commit:

791 passed in 17.95s

Purpose:

Verify local terminal preflight JSON shape and required safety fields.
Confirm no forbidden call attempts.
Confirm MT5 initialized and terminal/account/symbol fields are compatible with the expected H024 dry-run readiness facts.
Does not import MT5.
Does not touch the terminal.
Does not approve execution.

Local JSON remains uncommitted:

reports\h024_mt5_terminal_preflight.json
H024 Log-Only EA Runtime Preflight Skeleton

Code added:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
tests\test_h024_ea_log_only_preflight_static.py

Commit:

7f04588 Add H024 log-only EA preflight skeleton

Focused test result:

3 passed in 0.64s

Full suite after commit:

794 passed in 18.32s

Purpose:

Add first MQL5 log-only EA skeleton.
Verify it has runtime hooks and logging.
Verify it has no obvious execution-surface tokens.

Safety boundary:

No OrderSend.
No OrderCheck.
No CTrade.
No #include <Trade...>.
No PositionOpen.
No PositionClose.
No buy/sell order helper calls.
No execution adapter.
No demo/live/Phase 4 approval.

EA runtime hooks:

OnInit
OnTick
OnDeinit

EA output file:

h024_ea_log_only_preflight.csv

Runtime output location in MT5 terminal data folder:

...\MetaQuotes\Terminal\<terminal-id>\MQL5\Files\h024_ea_log_only_preflight.csv
H024 Log-Only EA Runtime Preflight Verifier

Code added:

scripts\verify_h024_ea_preflight_log.py
tests\test_h024_ea_preflight_log_verifier.py

Commit:

c3aad45 Add H024 log-only EA preflight verifier

Focused test result:

6 passed in 0.52s

Full suite after commit:

800 passed in 16.53s

Purpose:

Verify runtime CSV shape.
Verify allowed events only.
Verify kill switch stayed blocked.
Verify symbols are expected.
Verify numeric/boolean fields parse.
Verify at least one INIT row exists.
Does not touch MT5.
Required Both H024 EA Runtime Symbols

Verifier tightened:

scripts\verify_h024_ea_preflight_log.py
tests\test_h024_ea_preflight_log_verifier.py

Commit:

92a4433 Require both H024 EA preflight symbols

Focused test result:

7 passed in 0.52s

Local runtime CSV verifier result after tightening:

H024 log-only EA runtime preflight verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Rows: 4
Violations: 0

Verdict: PASS

Full suite after commit:

801 passed in 16.52s

New required symbol coverage:

USDJPYm
XAUUSDm
H024 EA Log-Only Runtime Preflight Result

Result doc:

docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md

Commit:

dc9c0c5 Record H024 EA log-only preflight result

Local runtime CSV:

reports\h024_ea_log_only_preflight.csv

Do not commit this CSV.

Runtime symbols covered:

Model symbol    Broker symbol    Runtime rows
USDJPY    USDJPYm    INIT + DEINIT
XAUUSD    XAUUSDm    INIT + DEINIT

Observed runtime facts:

Field    USDJPYm    XAUUSDm
account_company    Exness Technologies Ltd    Exness Technologies Ltd
account_server    Exness-MT5Trial6    Exness-MT5Trial6
account_currency    USD    USD
account_balance    1246.45    1246.45
account_equity    1246.45    1246.45
account_leverage    2000    2000
account_trade_allowed    true    true
account_trade_expert    true    true
terminal_connected    true    true
terminal_trade_allowed    false    false
mql_trade_allowed    true    true
bid    156.676    4715.309
ask    156.694    4715.669
spread_points    18    360
volume_min    0.01    0.01
volume_max    300.00    200.00
volume_step    0.01    0.01
stops_level    0    0
freeze_level    0    0
point    0.0010000000    0.0010000000
digits    3    3

Verifier command:

python .\scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_preflight.csv

Verifier result:

H024 log-only EA runtime preflight verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Rows: 4
Violations: 0

Verdict: PASS

Interpretation:

The terminal-attached log-only EA runtime preflight passed for both required H024 broker symbols.
EA can attach to MT5 charts.
EA can write runtime preflight logs from the MT5 terminal context.
Runtime account, terminal, and symbol metadata are available to the EA.
Kill switch default remained blocked.
Python verifier accepted the runtime CSV shape and required both symbols.
The log-only runtime path did not require any order-send capability.

Important limitation:

This does not approve demo trading, live trading, Phase 4 execution, order placement, order modification, or order closing.
The observed terminal_trade_allowed=false condition remains important. It did not block this read-only runtime preflight, but it must be understood before any later execution gate.
Current Deployment Reality Check

Answer if asked whether ready to demo/live:

No.

H024 is not demo deployable yet.

Reasons:

No actual trading EA exists.
No H024 real-time strategy state machine exists inside EA runtime.
No runtime intended-action logs exist inside EA.
No demo execution adapter has been designed or authorized.
No order placement/modification/rejection behavior has been tested.
No actual order-send path is allowed.
No explicit user authorization for Phase 4/demo execution exists.
2023 weakness remains real and visible.
Terminal-level trade_allowed was false in both Python terminal preflight and EA runtime preflight and must be understood before later execution gates.

What is currently justified:

Continue dry-run/log-only preparation.
Add no-order intended-action runtime logging.
Add verifiers for intended-action runtime logs.
Add stricter static source verifier for MQL5 execution-surface exclusions.
Add more robust log format/versioning if needed.

What is not justified:

Demo order placement.
Live order placement.
Phase 4 execution.
Execution adapter with order-send enabled.
Any automatic trading.
Enabling OrderSend.
Adding CTrade.
Adding trade-modification code.
Recommended Next Work

Next best gate:

Add a stricter static verifier script for the MQL5 EA source.

Purpose:

enforce no execution-surface tokens from a standalone script
verify the log-only EA source remains incapable of order placement
make the safety invariant explicit outside pytest only

Possible files:

scripts\verify_h024_ea_source_static.py
tests\test_h024_ea_source_static_verifier.py

Alternative next gate:

Add no-order intended-action logging inside EA runtime.

Purpose:

represent H024 dry-run intent in EA logs only
keep kill switch default blocked
still no OrderSend
still no CTrade
still no order placement/modification/closing/deletion

Possible files:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
scripts\verify_h024_ea_intent_log.py
tests\test_h024_ea_intent_log_verifier.py

Before any EA runtime action touching MT5:

Get explicit user authorization.
Run one terminal-attached action at a time.
Preserve local CSVs in reports/ only.
Do not commit local report CSVs.
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
commit local report CSVs
commit local report JSONs
change .gitignore from /data/ to data/
continue development while local commits are unpushed
allow full-test count to drop below 801 without explicit test-removal intent
run brute-force timestamp shuffle again until redesigned
add OrderSend
add OrderCheck
add CTrade
add #include <Trade...>
add position open/close code
add order modification/deletion code
Known Repo Hygiene Lessons

Do not repeat these mistakes:

.gitignore once had unrooted data/, which risked excluding quantcore/data.
Some older commits missed files because git add was incomplete.
An empty handoff file was accidentally committed once.
Markdown code fences have been damaged by paste before.
PowerShell does not support Linux heredocs.
VS Code can keep unsaved buffers that overwrite edits.
If terminal output shows command echo ambiguity, verify with Select-String or file previews.
Always inspect git status.
Always push commits.
Always verify git ls-files after commits.
Treat code test-count drops as regressions.
If terminal output is too large to paste, rerun a compact read-only diagnostic.
Network/DNS push failures can happen; stop development until git push succeeds.
git diff --check can fail but PowerShell may continue unless $LASTEXITCODE is checked.
Real-data reporting code must be tested, not just backtest core logic.
Brute-force real-data timestamp shuffle was too slow; do not rerun until redesigned with batching/checkpointing or a cheaper path.
Local reports\h024_mt5_terminal_preflight.json should remain uncommitted.
Local reports\h024_ea_log_only_preflight.csv should remain uncommitted.
Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_67.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, clean except possibly local reports/, and pushed.
Current full-test anchor is 801 passed.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
Broker-cost reconciliation passed under observed Exness MT5 costs.
Static MT5 order behavior audit passed.
Dry-run/log-only execution primitives exist and have no MT5 order-send capability.
Dry-run action export produced 459 WOULD_OPEN, 4707 NO_ACTION, 0 BLOCKED.
Dry-run action log verifier passed: 5166 rows, 0 violations.
MT5 terminal/account preflight logger passed against local Exness demo terminal/account.
MT5 terminal/account preflight verifier passed against local JSON: 0 violations.
Log-only MQL5 EA skeleton exists.
Static tests verify the EA skeleton has no obvious execution-surface tokens.
Terminal-attached log-only EA runtime preflight passed for both USDJPYm and XAUUSDm.
EA runtime verifier now requires both symbols and passed against the local 4-row CSV.
Local reports\h024_mt5_terminal_preflight.json and reports\h024_ea_log_only_preflight.csv must not be committed.
2023 weakness remains real and must not be hidden with filters.
The next recommended gate is either a stricter MQL5 source static verifier or no-order intended-action runtime logging.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -20

Then paste the full output.
