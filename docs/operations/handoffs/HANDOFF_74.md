# HANDOFF_74 - After H024 Pure-Math Position Sizing TDD

If any older handoff conflicts with this file, this HANDOFF_74 wins.

This handoff is standalone enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is execution-safety preparation after H024 research evidence.
- H024 remains research/pre-deployment only.
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

HANDOFF_73 - After H024 EA WOULD_OPEN Synthetic Validation

This handoff:

HANDOFF_74 - After H024 Pure-Math Position Sizing TDD
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
The user's stated goal is: make the EA survive the future, not fit the past.

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

PowerShell does not support that. Use PowerShell here-strings, line arrays, or temporary .py files.

Important PowerShell lesson:

Windows PowerShell may not support -Encoding UTF8NoBOM.
Use [System.IO.File]::WriteAllText(..., [System.Text.UTF8Encoding]::new($false)) when no-BOM UTF-8 matters.
Avoid escaping Python triple quotes inside single-quoted PowerShell string arrays. Literal \"\"\" caused Python syntax errors.
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
Current full-test anchor after latest code work: 880 passed.
Previous anchor was 867 passed before position-sizing tests.
If full test count drops below 880 without planned test removal, treat as a regression.

Git after changes:

git diff --check
if ($LASTEXITCODE -ne 0) { throw "git diff --check failed" }

git diff --stat

git add <touched files>

git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "git diff --cached --check failed" }

git diff --cached --stat
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

Expected state after this handoff:

Branch main
Up to date with origin/main
No tracked-file changes
Likely one untracked local reports/ directory remains
Latest pushed commit should be:
4409ba4 Add H024 pure math position sizing

Known latest commits:

4409ba4 Add H024 pure math position sizing
9c73857 Update self-contained handoff document #73 with full context
28efcf8 Record H024 EA WOULD_OPEN synthetic validation result
cb913c2 Add ultimate H024 full H4 log-only runtime CI harness
dfe02b9 Add H024 EA strategy intent decision harness
821af43 Guard H024 EA strategy intent detail semantics
83a9080 Add handoff document #72
29b5c67 Record H024 EA strategy intent dedup runtime result
7e45142 Deduplicate H024 EA strategy intent emissions
b091922 Harden H024 EA would-open log verifier tests
Current Test Anchor

Current full-test anchor:

880 passed

Latest full suite after H024 pure-math position sizing work:

880 passed in 16.42s

Focused position-sizing/static gate after MQL5 sizing patch:

24 passed in 1.29s

Expanded Python position-sizing focused test result:

13 passed in 1.11s

If full tests pass but count drops below 880 without explicit test-removal intent, stop and treat it as a regression. Check for untracked experimental test files polluting the suite.

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

Accepted strict bridge-window range from prior research:

first common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
last common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00
accepted bridge-window count: 5476

Important current-data note:

For EA state parity after runtime logs dated 2026-05-08, the user updated broker-native H4 exports through at least:

2026-05-08 13:00:00+00:00

Do not use:

HistData for validation/tuning/production dataset creation.
Broker H4 plus HistData M1 combinations.
Sparse 2018 through 2021-06 broker-native prefix as dense M1.
Incomplete H4/M1 windows.

Do not commit:

Raw MT5 CSV files
Raw HistData files
Large derived datasets
Broker/vendor source files
Local reports/*.csv
Local reports/*.json
Local runtime CSVs

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

New pure-math sizing reference:

quantcore\strategy\h024_position_sizer.py
tests\test_h024_position_sizing.py

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
scripts\verify_h024_ea_source_static.py
scripts\verify_h024_ea_preflight_log.py
scripts\verify_h024_ea_state_observation_parity_real.py
scripts\run_h024_mt5_log_only_preflight_local.py
scripts\validate_h024_mt5_profile_template_plan.py
tests\test_h024_ea_source_static_verifier.py
tests\test_h024_ea_log_only_preflight_static.py
tests\test_h024_ea_preflight_log_verifier.py
tests\test_h024_ea_state_observation_parity_real_script.py
tests\test_h024_mt5_log_only_preflight_local_helper.py
tests\test_h024_mt5_profile_template_plan_validator.py
tests\test_h024_ea_strategy_intent_emission_static.py
tests\test_h024_ea_strategy_intent_detail_static.py
tests\test_h024_ea_strategy_intent_decision_harness.py
tests\h024_full_h4_runtime_ci_harness.py

Recent result/safety docs:

docs\operations\H024_OBSERVED_BROKER_COST_RESULT.md
docs\operations\H024_MT5_ORDER_BEHAVIOR_AUDIT_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\H024_MT5_TERMINAL_PREFLIGHT_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
docs\operations\H024_EA_WOULD_OPEN_SYNTHETIC_VALIDATION_RESULT.md
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

Frozen H024 signal defaults:

slow_window = 5
slope_lag = 2
atr_window = 3
pullback_window = 3
min_pullback_atr = 0.25
max_pullback_atr = 3.0
min_slope_atr = 0.05

Python signal definition in quantcore\strategy\h024.py:

slow_ma = close.rolling(5).mean()
atr = Wilder ATR(3)
slope = slow_ma - slow_ma.shift(2)
slope_threshold = atr * 0.05

trend_up = close > slow_ma and slope > slope_threshold
trend_down = close < slow_ma and slope < -slope_threshold

previous_bearish = close.shift(1) < open.shift(1)
previous_bullish = close.shift(1) > open.shift(1)

recent_high_before_signal = high.shift(1).rolling(3).max()
recent_low_before_signal = low.shift(1).rolling(3).min()

long_pullback_depth_atr = (recent_high_before_signal - low.shift(1)) / atr.shift(1)
short_pullback_depth_atr = (high.shift(1) - recent_low_before_signal) / atr.shift(1)

long_pullback_ok = long_pullback_depth_atr between 0.25 and 3.0 inclusive
short_pullback_ok = short_pullback_depth_atr between 0.25 and 3.0 inclusive

long_resumption = close > high.shift(1)
short_resumption = close < low.shift(1)

long_signal = trend_up and previous_bearish and long_pullback_ok and long_resumption
short_signal = trend_down and previous_bullish and short_pullback_ok and short_resumption

Bridge timing:

Signal evaluated at H4 close timestamp t.
Entry uses next H4 open t+1.
Last bar signal is suppressed by bridge because there is no next entry bar.
H024 Prior Evidence Summary

Preliminary fixed lifecycle on strict Exness broker-native H4/M1 complete windows:

Hold	Accepted	Executed	Skipped	Fills	Stops	Stop rate	Ending equity	PnL	Return	Max DD	Win rate	PF
1 H4	5476	861	4615	931	21	2.2556%	8450.96	-1549.04	-15.4904%	-22.5043%	45.4350%	0.849209
2 H4	5476	559	4917	604	45	7.4503%	10925.34	925.34	9.2534%	-14.0533%	50.8278%	1.076884
3 H4	5476	424	5052	459	56	12.2004%	14093.92	4093.92	40.9392%	-6.7346%	52.2876%	1.356184
4 H4	5476	285	5191	307	54	17.5896%	11236.27	1236.27	12.3627%	-6.8030%	49.5114%	1.151364

H024 hold=3 was best.

Persistent weakness:

2023 PnL: -708.20
2023 PF: 0.764187

Do not add a 2023 exclusion.
Do not add time/session filter.

Targeted robustness:

hold fixed at 3 H4
stop ATR multiples: 1.5, 2.0, 2.5
cost multipliers: 1.0x, 1.25x, 1.5x
all 9 targeted stop/cost scenarios passed
worst tested PF: 1.282177

Chronological validation:

Fold	Train count	Test count	Test start UTC	Test end UTC	Fills	Return	Max DD	PF	Headline pass
anchored_train_25%_test_rest	1369	4107	2023-01-05T22:00:00+00:00	2026-04-30T01:00:00+00:00	359	17.8797%	-6.6593%	1.225915	yes
anchored_train_50%_test_rest	2738	2738	2024-03-05T22:00:00+00:00	2026-04-30T01:00:00+00:00	244	19.2253%	-4.4683%	1.384976	yes
anchored_train_75%_test_rest	4107	1369	2025-04-02T21:00:00+00:00	2026-04-30T01:00:00+00:00	114	13.9192%	-2.6061%	1.653426	yes

Direction-flip negative control:

frozen H024 PF: 1.356184
direction flip PF: 0.620728
baseline minus direction-flip PnL: 7990.81 USD

Supports directional information in frozen H024, but does not prove future survivability.

Ledger-level permutation diagnostic:

permutation runs: 10000
seed: 240240
max-drawdown worse/equal rate: 57.4400%
min-equity worse/equal rate: 64.3000%
permutation ruin count: 0

Does not replace full execution timestamp shuffle.
Do not run brute-force timestamp shuffle again until redesigned.

Broker And MT5 Evidence

Broker symbol spec audit found observed Exness MT5 cost facts:

USDJPY:
  spread_price 0.018
  commission_usd_per_lot_per_fill 0.0
  stop_slippage_atr_fraction 0.05

XAUUSD:
  spread_price 0.36
  commission_usd_per_lot_per_fill 0.0
  stop_slippage_atr_fraction 0.05

Observed broker costs diagnostic:

baseline modeled costs PnL: 4093.92
baseline modeled costs PF: 1.356184
observed broker costs PnL: 4693.82
observed broker costs PF: 1.407061
delta observed minus baseline PnL: +599.90

2023 remains weak under observed broker costs:

PnL: -622.90
PF: 0.793006
stop rate: 18.8889%

Do not add a 2023 exclusion.
Do not tune H024.

Static MT5 order behavior audit passed for:

USDJPYm
XAUUSDm

Observed order facts:

trade_mode: 4
execution_mode: 2
order_filling_modes: 3
order_modes: 127

This does not test actual order placement, rejection behavior, requotes, or slippage.

Dry-Run And EA Safety Boundary

Dry-run/log-only mode must not place, modify, close, or delete orders.

In dry-run/log-only mode, code must not call any live MT5 order-sending function.

Forbidden in dry-run/log-only:

OrderSend
OrderSendAsync
OrderCheck
CTrade
#include <Trade...>
PositionOpen
PositionClose
PositionModify
pending order helpers
MqlTradeRequest
MqlTradeResult

Dry-run output only:

WOULD_OPEN
NO_ACTION
BLOCKED

Dry-run action export result:

Rows: 5166
WOULD_OPEN: 459
NO_ACTION: 4707
BLOCKED: 0
Violations: 0
Verdict: PASS

This does not approve demo/live/Phase 4.

MT5 Terminal/Account Preflight

Python terminal/account preflight passed.

Observed account/terminal facts:

Account currency: USD
Account leverage: 2000
Terminal connected: true
Terminal trade_allowed: false

Important:

terminal_trade_allowed=false was observed and must be understood before later execution gates.

This does not block read-only preflight.
This does not approve demo trading.

EA Runtime State

Current EA source:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5

Current runtime schema:

schema_version = h024_ea_log_only_preflight_v2

Current EA runtime input version:

InpEaVersion = 0.6

Current MQL5 property version:

#property version "0.600"

Important:

The EA now contains a pure-math lot sizing function:

ComputeH024LotSize(...)

This function is isolated math only.
It does not send, check, modify, close, or prepare orders.

Work Since HANDOFF_73
Commit

Latest completed and pushed commit:

4409ba4 Add H024 pure math position sizing
Files changed
ea_mt5/Experts/H024_LogOnly_Preflight.mq5
quantcore/strategy/h024_position_sizer.py
tests/test_h024_position_sizing.py
What changed
Added quantcore\strategy\h024_position_sizer.py.

This module defines a pure Python fixed-risk position sizing reference:

H024PositionSizeRequest
H024PositionSizeResult
H024PositionSizer

The sizing contract uses:

risk_usd = account_balance_usd * risk_fraction
stop_distance_price = abs(entry_price - stop_price)
stop_distance_ticks = stop_distance_price / tick_size
loss_usd_per_lot = stop_distance_ticks * tick_value_usd_per_lot
raw_lots = risk_usd / loss_usd_per_lot
capped_lots = min(raw_lots, max_volume)
stepped_lots = floor_to_volume_step(capped_lots)
if stepped_lots < min_volume: lots = 0.0
else lots = round(stepped_lots, volume_digits)
Added tests\test_h024_position_sizing.py.

The tests cover:

Fixed-risk sizing from account balance, risk fraction, stop distance, tick size, and tick value.
Rounding down to broker volume step.
Returning zero if minimum volume would exceed risk constraints.
Capping at broker max volume.
XAUUSD-style tick contract.
Invalid input fail-closed behavior.
Static scan confirming the log-only EA remains execution-API-free.
Added pure MQL5 lot sizing function to ea_mt5\Experts\H024_LogOnly_Preflight.mq5.

Current function:

ComputeH024LotSize(
   account_balance_usd,
   risk_fraction,
   entry_price,
   stop_price,
   tick_size,
   tick_value_usd_per_lot,
   volume_step,
   min_volume,
   max_volume,
   volume_digits = 2
)

MQL5 behavior:

Returns 0.0 on invalid inputs.
Uses absolute price stop distance.
Converts price distance to ticks.
Converts ticks to USD loss per lot.
Computes raw lots.
Caps to max_volume.
Floors to volume_step.
Returns 0.0 if below min_volume.
Normalizes final lots to volume_digits.

Important correction made during this work:

An earlier MQL5 draft had malformed condition lines with stray | characters:

if(stop_distance_points <= 0.0 |
| tick_value <= 0.0 |
| tick_size <= 0.0)

This was fixed before commit. Current MQL5 tail is syntactically sane and focused tests passed.

Validation completed

Focused Python position-sizing tests:

13 passed in 1.11s

Focused position-sizing + EA static tests after MQL5 patch:

24 passed in 1.29s

Full test suite:

880 passed in 16.42s

Git hygiene completed:

git diff --check passed
git diff --cached --check passed
commit succeeded
push succeeded
git status clean except untracked reports/
git ls-files confirmed all touched files are tracked

Final post-push status:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
Current Deployment Reality Check

Answer if asked whether ready to demo/live:

No.

H024 is still not demo deployable.

What is now true:

Backtest H024 is promising.
Broker-cost reconciliation passed.
Static MT5 order-behavior facts passed.
MT5 terminal/account read-only preflight passed.
MQL5 log-only EA shell exists.
EA can compute and log frozen H024 state ingredients from closed H4 bars.
EA 0.6 strategy-intent rows are deduplicated at runtime.
Synthetic WOULD_OPEN validation passed.
WOULD_OPEN semantic is isolated from actual order execution.
Conflict blocks and warmup gates are proven.
NEW: Pure-math position sizing now exists in Python and MQL5.
NEW: Position sizing has TDD coverage for fixed-risk, tick conversion, volume step flooring, min/max volume bounds, and fail-closed invalid inputs.
NEW: Full test suite anchor increased to 880 passed.

What is still missing before first demo deployment:

Position sizing is implemented as isolated math, but not yet integrated into executable intended-action logs.
Executable intended-action logs are not implemented.
No demo execution adapter exists.
No order placement/modification/rejection behavior testing has been done.
Runtime WOULD_OPEN row emission has not been observed under a real, live signal condition.
2023 weakness remains real and visible.
No demo execution approval.
No live execution approval.
No Phase 4 approval.
Recommended Next Work

Best next gate:

Executable Intended-Action Log Contract

Do not jump to order sending.

Recommended next TDD path:

Add/extend Python tests defining intended-action row schema for future execution decisions.
The intended-action log should include enough fields to reconstruct what the EA would have done without sending an order.
Required likely fields:
timestamp
schema_version
ea_version
symbol
normalized_symbol
timeframe
decision
direction
entry_price
stop_price
stop_distance_price
tick_size
tick_value_usd_per_lot
account_balance_usd
risk_fraction
raw_lots or computed lots
final lots
min_volume
max_volume
volume_step
volume_digits
reason/detail
Keep it log-only.
Add MQL5 implementation only after tests define the contract.
Run focused tests, then full pytest.
Commit and push.

Alternative safe next gate:

MQL5 static tests specifically asserting ComputeH024LotSize exists and remains execution-surface-free

This is smaller but less valuable than intended-action logs.

Current Safe Automation State

Already automated:

Copy EA source to terminal MQL5\Experts.
Compile EA with MetaEditor.
Reset/Collect/Verify runtime CSV.
Terminal Preflight.
Profile/Template validation.

Not approved:

EA chart attachment/detachment automation.
GUI automation.
MT5 launcher/profile mutation affecting live terminals.
Order-send automation.
Demo/live execution adapter.
Absolute Do-Not Rules

Do not demo trade, live trade, or approve Phase 4.

Do not treat H024 as deployment-ready.

Do not hide 2023 weakness with filters or time/session buckets.

Do not use HistData or synthesize bars.

Do not combine broker H4 with HistData M1.

Do not modify raw broker files.

Do not change .gitignore from /data/ to data/.

Do not continue development while local commits are unpushed.

Do not allow full-test count to drop below 880 without explicit test-removal intent.

Do not use untracked test files to dictate regressions.

Do not add any execution API to the log-only EA:

OrderSend
OrderSendAsync
OrderCheck
CTrade
#include <Trade...>
MqlTradeRequest
MqlTradeResult
PositionOpen
PositionClose
PositionModify

Do not implement execution adapter yet.

Do not automate chart attach/detach yet.

Known Repo Hygiene Lessons
Do not repeat unrooted data/ in .gitignore.
PowerShell does not support Linux heredocs.
Treat code test-count drops as regressions.
Untracked test files can pollute pytest; ensure clean state or explicit tracking.
Network/DNS push failures can happen; stop development until git push succeeds.
MetaEditor CLI may return nonzero even when compile succeeds with warnings; verify .ex5 refresh.
Treat missing .ex5 as compile failure.
Python indentation inside PowerShell here-strings caused repeated IndentationError; use simpler PowerShell-native file append or [System.IO.File]::WriteAllText.
Do not escape Python triple-quote docstrings as \"\"\"; that creates literal backslashes and Python syntax errors.
Resolve-Path fails for files that do not exist yet; use [System.IO.Path]::GetFullPath(...).
Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_74.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, clean except possibly local reports/, and pushed.
Current full-test anchor is 880 passed.
Latest pushed commit should be 4409ba4 Add H024 pure math position sizing.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
Synthetic WOULD_OPEN validation passed without execution APIs.
Pure-math position sizing now exists in Python and MQL5.
No order-send, no CTrade, no MqlTradeRequest, no execution adapter.
Attach/detach automation is not approved. GUI automation is not approved.
Local reports must not be committed.
2023 weakness remains real and must not be hidden with filters.
Best next gate is executable intended-action log TDD, still log-only.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -15

Then paste the full output.