# HANDOFF_64 - After H024 Anti-Curve-Fit Work And Broker Symbol Spec Audit Failure

If any older handoff conflicts with this file, this HANDOFF_64 wins.

This handoff is intentionally self-contained so a new AI can continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is research/backtest infrastructure, anti-curve-fit validation, and broker/execution realism.
- No execution approval.
- No demo deployment approval.
- No live trading approval.
- No Phase 4 approval.

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

HANDOFF_63 - After H024 Chronological Validation Pass

This handoff:

HANDOFF_64 - After H024 Anti-Curve-Fit Work And Broker Symbol Spec Audit Failure
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
The user’s stated goal is: make the EA survive the future, not fit the past.

Important sentiment:

The user is eager to deploy.
The user accepts evidence gates.
Be direct: H024 is serious, but still not deployable.
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
Current full-test anchor after recent work: 724 passed.
If full test count drops below 724 without planned test removal, treat as a regression.

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
git log --oneline -15

Expected clean state:

branch main
up to date with origin/main
working tree clean

Known recent confirmed commits include:

a439425 Record H024 ledger permutation result
13198e3 Add H024 ledger permutation diagnostic
f7f3298 Record H024 2023 stop ledger audit
968295b Reduce H024 timestamp shuffle default run count
a44adb1 Add H024 timestamp shuffle control
04a7c3d Record H024 direction flip control result
d08b0a1 Add H024 direction flip control
4f7459d Add H024 anti-curve-fit protocol
8785102 Record H024 leverage audit addendum
1919dce Report H024 ledger leverage audit
68fcfbf Add H024 ledger actual leverage audit fields
ef98b68 Record H024 trade ledger audit result
44e3829 Add H024 trade ledger diagnostic
51a003f Add handoff document #63 after H024 chronological validation

There may also be a later commit like:

Add H024 broker symbol spec audit

because a broker symbol audit script was added and used. Verify from git log.

The broker symbol audit result doc may not yet be committed. Verify whether this file exists and is tracked:

docs\operations\H024_BROKER_SYMBOL_SPEC_AUDIT_RESULT.md

Check with:

git ls-files docs\operations\H024_BROKER_SYMBOL_SPEC_AUDIT_RESULT.md
Current Test Anchor

Current full-test anchor:

724 passed

Recent observed full suite examples:

724 passed in 15.30s
724 passed in 15.66s

If full tests pass but count drops below 724 without explicit test-removal intent, stop and treat it as a regression.

Data And Source Rules

Accepted source for strict validation/diagnostics:

Exness demo MT5 broker-native exports only.

Accepted model symbols:

USDJPY
XAUUSD

Observed Exness MT5 account symbol names from user:

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
local reports/*.csv

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

Original/default modeled cost assumptions before broker audit:

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

Raw stop distance must be at least one modeled spread.
USDJPY default model spread: 0.01
XAUUSD default model spread: 0.30
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

H021 found useful failure-mode clues but no validated strategy.

H022 reduced damage but still failed.

H023 falsified the Donchian/Chandelier entry stack and is closed.

H024 is the first serious positive candidate, but:

H024 is not fully validated.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 is not approved.
Important H024 Files

Core H024:

quantcore\strategy\h024.py
quantcore\strategy\h024_runner.py

Diagnostics/scripts:

scripts\diagnose_h024_pullback_continuation_real.py
scripts\diagnose_h024_fixed_lifecycle_real.py
scripts\diagnose_h024_robustness_real.py
scripts\diagnose_h024_walk_forward_real.py
scripts\diagnose_h024_trade_ledger_real.py
scripts\diagnose_h024_direction_flip_real.py
scripts\diagnose_h024_timestamp_shuffle_real.py
scripts\diagnose_h024_ledger_permutation.py
scripts\audit_h024_broker_symbol_specs.py

Tests:

tests\test_h024.py
tests\test_h024_runner.py
tests\test_h024_pullback_continuation_real_script.py
tests\test_h024_fixed_lifecycle_real_script.py
tests\test_h024_robustness_real_script.py
tests\test_h024_walk_forward_real_script.py
tests\test_h024_trade_ledger_real_script.py
tests\test_h024_direction_flip_real_script.py
tests\test_h024_timestamp_shuffle_real_script.py
tests\test_h024_ledger_permutation_script.py
tests\test_h024_broker_symbol_specs_audit.py

Result/protocol docs:

docs\operations\H024_HYPOTHESIS_SEED.md
docs\operations\H024_PRELIMINARY_FIXED_LIFECYCLE_RESULT.md
docs\operations\H024_TARGETED_ROBUSTNESS_RESULT.md
docs\operations\H024_CHRONOLOGICAL_VALIDATION_RESULT.md
docs\operations\H024_TRADE_LEDGER_AUDIT_RESULT.md
docs\operations\H024_ANTI_CURVE_FIT_PROTOCOL.md
docs\operations\H024_DIRECTION_FLIP_CONTROL_RESULT.md
docs\operations\H024_LEDGER_PERMUTATION_RESULT.md
docs\operations\H024_BROKER_SYMBOL_SPEC_AUDIT_RESULT.md

The broker result doc may still need to be created/committed. Verify.

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
H018 hard guard semantics preserved
modeled costs preserved

Main summary:

Hold	Accepted	Executed	Skipped	Fills	Stops	Stop rate	Ending equity	PnL	Return	Max DD	Win rate	PF
1 H4	5476	861	4615	931	21	2.2556%	8450.96	-1549.04	-15.4904%	-22.5043%	45.4350%	0.849209
2 H4	5476	559	4917	604	45	7.4503%	10925.34	925.34	9.2534%	-14.0533%	50.8278%	1.076884
3 H4	5476	424	5052	459	56	12.2004%	14093.92	4093.92	40.9392%	-6.7346%	52.2876%	1.356184
4 H4	5476	285	5191	307	54	17.5896%	11236.27	1236.27	12.3627%	-6.8030%	49.5114%	1.151364

H024 hold=3 was best.

Persistent weakness:

2023 failed materially:
PnL: -708.20
PF: 0.764187
Do not add 2023 exclusion.
Do not add time/session filter.
H024 Targeted Robustness Result

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

Interpretation:

H024 hold=3 is not merely surviving baseline cost model.
It survived up to 1.5x modeled cost stress.
2023 remained weak across scenarios.
This did not prove no curve fitting.
H024 Chronological Validation Result

Command:

python .\scripts\diagnose_h024_walk_forward_real.py

Summary:

Fold	Train count	Test count	Test start UTC	Test end UTC	Fills	Return	Max DD	PF	Headline pass
anchored_train_25%_test_rest	1369	4107	2023-01-05T22:00:00+00:00	2026-04-30T01:00:00+00:00	359	17.8797%	-6.6593%	1.225915	yes
anchored_train_50%_test_rest	2738	2738	2024-03-05T22:00:00+00:00	2026-04-30T01:00:00+00:00	244	19.2253%	-4.4683%	1.384976	yes
anchored_train_75%_test_rest	4107	1369	2025-04-02T21:00:00+00:00	2026-04-30T01:00:00+00:00	114	13.9192%	-2.6061%	1.653426	yes

Interpretation:

H024 passed a meaningful anti-curve-fit chronological test.
2023 weakness remains visible.
No 2023 exclusion or filter is approved.
H024 Trade Ledger Audit Result

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

Symbol	Fills	Stops	Stop rate	PnL USD	PF	Win rate
USDJPY	240	25	10.4167%	2832.92	1.460747	55.4167%
XAUUSD	219	31	14.1553%	1261.01	1.235909	48.8584%

By side:

Side	Fills	Stops	Stop rate	PnL USD	PF	Win rate
buy	252	32	12.6984%	2125.89	1.336645	53.9683%
sell	207	24	11.5942%	1968.04	1.380010	50.2415%

By year:

Year	Fills	Stops	Stop rate	PnL USD	PF	Win rate
2021	16	1	6.2500%	534.92	2.708700	56.2500%
2022	84	10	11.9048%	1435.99	1.800603	57.1429%
2023	90	17	18.8889%	-708.20	0.764187	46.6667%
2024	122	17	13.9344%	758.18	1.228199	52.4590%
2025	120	11	9.1667%	1661.50	1.654749	55.0000%
2026	27	0	0.0000%	411.53	1.785618	40.7407%
H024 Actual Gross Leverage Audit

After adding interval-start equity and actual gross leverage fields to the ledger:

Actual gross leverage distribution:

Slice	Fills	Min	Median	Mean	P90	Max
all_fills	459	0.238174	1.055387	1.156458	1.975010	3.285420
stop_fills	56	0.242458	0.946250	1.119561	1.824440	2.499557
2023_stop_fills	17	0.523237	1.027594	1.121347	1.693794	2.446090

Interpretation:

2023 weakness is not leverage pathology.
Largest losses are ordinary stopped-risk losses, not lot-sizing blowups.
Actual gross leverage is moderate and far below H018 10x hard guard.
2023 Stop-Exit Ledger Audit

The 17 2023 stop exits were inspected directly.

Actual gross leverage range:

min: 0.523237x
max: 2.446090x

Largest 2023 stop loss:

USDJPY sell
entry: 2023-09-29T05:00:00+00:00
exit: 2023-09-29T11:12:00+00:00
lots: 0.28
raw stop distance: 0.591751
actual gross leverage: 2.446090x
PnL: -122.250019 USD

PnL decile audit:

Worst PnL decile:

46 fills
PnL: -5113.274204 USD
average actual gross leverage: 1.268542x
average raw stop distance: 8.853993
stop exits: 43 of 46

Best PnL decile:

46 fills
PnL: +7366.081209 USD
average actual gross leverage: 1.435053x
average raw stop distance: 7.632218
stop exits: 0 of 46

Interpretation:

Loss concentration is stop-exit driven, not leverage-driven.
Best decile had higher average leverage than worst decile.
Main unresolved issue is stop-hit clustering under adverse regimes.
H024 Anti-Curve-Fit Protocol

Doc:

docs\operations\H024_ANTI_CURVE_FIT_PROTOCOL.md

Key rule:

H024 is frozen.
No parameter tuning during anti-curve-fit evaluation.
No 2023 exclusion.
No time/session filters.
Any parameter change becomes H025, not H024 adjustment.
H024 Direction-Flip Negative Control

Command:

python .\scripts\diagnose_h024_direction_flip_real.py

Result:

Variant	Accepted	Executed	Fills	Stops	Stop rate	Ending equity USD	PnL USD	Return	Max DD	Win rate	Gross profit USD	Gross loss USD	PF	Fill return Sharpe
frozen H024	5476	424	459	56	12.2004%	14093.92	4093.92	40.9392%	-6.7346%	52.2876%	15587.76	-11493.84	1.356184	0.118427
direction flip	5476	402	433	89	20.5543%	6103.11	-3896.89	-38.9689%	-40.2652%	43.8799%	6377.77	-10274.66	0.620728	-0.188633

Baseline minus direction-flip PnL:

7990.81 USD

Interpretation:

Direction-flip control materially failed.
This reduces concern that H024 is generic lifecycle/sizing/volatility exposure.
It supports directional information in frozen H024.
It does not prove future survivability.
H024 Timestamp Shuffle Control

Code was added:

scripts\diagnose_h024_timestamp_shuffle_real.py
tests\test_h024_timestamp_shuffle_real_script.py

But the real diagnostic was too slow. Even after reducing default run count from 100 to 10, it still took too long.

Current instruction:

Do not run brute-force timestamp shuffle again.
It needs cheaper implementation, batching, checkpointing, or replacement.
Do not treat it as completed evidence.

Relevant commits:

a44adb1 Add H024 timestamp shuffle control
968295b Reduce H024 timestamp shuffle default run count
H024 Ledger-Level Permutation Diagnostic

Command:

python .\scripts\diagnose_h024_ledger_permutation.py

This is a cheap proxy. It randomly reorders realized trade PnLs from the existing ledger 10,000 times.

It does not:

test signal direction
replace full execution timestamp shuffle
rerun M1 lifecycle execution
approve deployment

Observed path:

Metric	Value
total_pnl_usd	4093.92
ending_equity_usd	14093.92
max_drawdown	-6.7346%
min_equity_usd	9901.07
ruin	false

Permutation distribution:

Metric	Min	P10	Median	Mean	P90	Max
ending_equity_usd	14093.922816	14093.922816	14093.922816	14093.922816	14093.922816	14093.922816
total_pnl_usd	4093.922816	4093.922816	4093.922816	4093.922816	4093.922816	4093.922816
max_drawdown	-0.234424	-0.101874	-0.070896	-0.074721	-0.052177	-0.034531
min_equity_usd	8125.074718	9409.475200	9830.724716	9757.552260	10000.000000	10000.000000

Summary:

permutation runs: 10000
seed: 240240
permutations with max_drawdown <= observed max_drawdown: 5744
max-drawdown worse/equal rate: 57.4400%
permutations with min_equity <= observed min_equity: 6430
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

Expected input CSV path:

reports\h024_mt5_symbol_specs.csv

Do not commit this CSV.

The user exported MT5 symbol facts from Exness.

Initial MT5 symbols:

USDJPYm
XAUUSDm

For audit comparison, these were normalized to model symbols:

USDJPY
XAUUSD

CSV used:

symbol,contract_size,quote_currency,lot_step,min_lot,spread_price,commission_usd_per_lot_per_fill,stop_slippage_atr_fraction,max_lot,stops_level_points,freeze_level_points,point,digits
USDJPY,100000.00000000,JPY,0.01000000,0.01000000,0.01800000,0.00000000,0.05000000,300.00000000,0,0,0.0010000000,3
XAUUSD,100.00000000,USD,0.01000000,0.01000000,0.36000000,0.00000000,0.05000000,200.00000000,0,0,0.0010000000,3

Audit command:

python .\scripts\audit_h024_broker_symbol_specs.py

Audit result:

H024 broker symbol/spec audit
========================================================================
Research only. No demo/live/Phase 4 approval.

symbol                           field expected observed   status
USDJPY                   contract_size   100000   100000       ok
USDJPY                  quote_currency      JPY      JPY       ok
USDJPY                        lot_step     0.01     0.01       ok
USDJPY                         min_lot     0.01     0.01       ok
USDJPY                    spread_price     0.01    0.018 mismatch
USDJPY commission_usd_per_lot_per_fill        7        0 mismatch
USDJPY      stop_slippage_atr_fraction     0.05     0.05       ok
XAUUSD                   contract_size      100      100       ok
XAUUSD                  quote_currency      USD      USD       ok
XAUUSD                        lot_step     0.01     0.01       ok
XAUUSD                         min_lot     0.01     0.01       ok
XAUUSD                    spread_price      0.3     0.36 mismatch
XAUUSD commission_usd_per_lot_per_fill       10        0 mismatch
XAUUSD      stop_slippage_atr_fraction     0.05     0.05       ok

Mismatch count: 4

Verdict: FAIL

Interpretation:

Static instrument assumptions match:

contract size
quote currency
lot step
minimum lot

Static cost assumptions do not match:

USDJPY spread:      model 0.010 vs MT5 0.018
XAUUSD spread:      model 0.300 vs MT5 0.360
USDJPY commission:  model 7.0   vs MT5 0.0
XAUUSD commission:  model 10.0  vs MT5 0.0

The commission mismatch may reflect Exness account type. A zero-commission account can still be more expensive through wider spreads.

This blocks demo-readiness review until broker-cost reconciliation is completed.

Immediate Next Work After Hygiene

After the user provides git status and git log --oneline -15, do this:

Case A: Broker audit result doc is not committed

If this file does not exist or is untracked:

docs\operations\H024_BROKER_SYMBOL_SPEC_AUDIT_RESULT.md

Create it using the broker audit result above.

Commit message:

Record H024 broker symbol spec audit result

No full pytest required because it is docs-only. Use git diff --check, cached check, commit, push, status, and git ls-files.

Case B: Broker audit result doc is already committed

Proceed to implement frozen H024 observed-broker-cost rerun diagnostic.

Purpose:

rerun frozen H024 hold=3 using observed MT5 cost facts
compare against baseline H024 hold=3
no parameter optimization
no 2023 exclusion
no deployment approval

Observed MT5 cost facts to test:

USDJPY:
  spread_price = 0.018
  commission_usd_per_lot_per_fill = 0.0
  stop_slippage_atr_fraction = 0.05

XAUUSD:
  spread_price = 0.36
  commission_usd_per_lot_per_fill = 0.0
  stop_slippage_atr_fraction = 0.05

Expected implementation approach:

Inspect current cost injection path:
quantcore\backtest\cost_model.py
quantcore\backtest\h017_event.py
scripts\diagnose_h021_fixed_lifecycle_variants_real.py
scripts\diagnose_h024_fixed_lifecycle_real.py
Add a minimally invasive way to pass cost_specs_by_symbol into fixed-lifecycle execution.
Preserve default behavior exactly when no override is supplied.
Add focused synthetic tests proving:
default cost path is unchanged
custom observed broker cost specs alter commission/spread as expected
H024 observed-cost script runs on synthetic data
report clearly says research-only and no demo/live/Phase 4 approval
Run focused tests and full test suite.

Suggested new files:

scripts\diagnose_h024_observed_broker_costs_real.py
tests\test_h024_observed_broker_costs_real_script.py

Potential core files if needed:

quantcore\backtest\h017_event.py
scripts\diagnose_h021_fixed_lifecycle_variants_real.py

Commit message if code is added:

Add H024 observed broker cost diagnostic

After code commit, ask user before running real-data diagnostic because it is a real-data backtest.

Command to run only after explicit user authorization:

python .\scripts\diagnose_h024_observed_broker_costs_real.py
Interpretation Standard For Observed Broker Cost Rerun

If H024 remains positive with PF >= 1.15 under observed MT5 cost facts, broker-cost reconciliation improves.

If H024 fails or materially degrades below acceptance thresholds, H024 remains research-only and broker-cost mismatch blocks deployment.

Even if it passes:

no demo approval
no live approval
no Phase 4 approval

Next required checks would still include:

MT5 order behavior reconciliation
dry-run/log-only EA path
hard kill switch
execution adapter safety checks
explicit user authorization for any demo/Phase 4 work
Deployment Reality Check

Answer if asked whether ready to demo/live:

No.

Reasons:

H024 is promising but not deployment-ready.
Broker cost assumptions currently fail static reconciliation.
Observed MT5 spread/commission scenario has not been rerun.
MT5 order behavior has not been reconciled.
Symbol contract assumptions matched, but live execution constraints still need checks.
Stop level/freeze level were exported as 0, but this should still be documented.
No dry-run EA exists.
No execution adapter safety checks complete.
No hard kill switch validated.
No log-only mode validated.
No Phase 4 authorization.
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
change .gitignore from /data/ to data/
continue development while local commits are unpushed
allow full-test count to drop below 724 without explicit test-removal intent
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
Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_64.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, clean, and pushed.
Current full-test anchor is 724 passed.
H024 is the first serious candidate but remains not demo-approved, not live-approved, and not Phase 4-approved.
H024 hold=3 passed preliminary fixed lifecycle, targeted robustness, chronological validation, trade-ledger audit, direction-flip negative control, and ledger-level permutation control.
The brute-force timestamp shuffle was too slow and should not be rerun without redesign.
2023 weakness remains real and must not be hidden with a filter.
Static MT5 broker symbol audit matched instrument specs but failed cost assumptions:
USDJPY spread 0.018 observed vs 0.010 modeled
XAUUSD spread 0.36 observed vs 0.30 modeled
USDJPY commission 0 observed vs 7 modeled
XAUUSD commission 0 observed vs 10 modeled
This blocks demo-readiness until broker-cost reconciliation is completed.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -15

Then paste the full output.

After hygiene passes, I will either:

record the broker symbol spec audit result if it is not already committed, or
implement the frozen H024 observed-broker-cost rerun diagnostic if it is already recorded.