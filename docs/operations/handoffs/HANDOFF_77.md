# HANDOFF_77 - After H024 Runtime Intended-Action Observation, Verifier Recovery, And Summary Checker

If any older handoff conflicts with this file, this HANDOFF_77 wins.

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

HANDOFF_76 - After H024 Runtime Intended-Action Emission And MT5 Compile Recovery

This handoff:

HANDOFF_77 - After H024 Runtime Intended-Action Observation, Verifier Recovery, And Summary Checker
Human Preference

The user is tired of excessive ceremony.

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

The user's stated goal is:

make the EA survive the future, not fit the past

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

PowerShell does not support that.

Use PowerShell here-strings, line arrays, or temporary .py files.

Important PowerShell lessons:

Windows PowerShell may not support -Encoding UTF8NoBOM.
Use [System.IO.File]::WriteAllText(..., [System.Text.UTF8Encoding]::new($false)) when no-BOM UTF-8 matters.
Avoid escaping Python triple quotes inside single-quoted PowerShell string arrays.
Literal \"\"\" caused Python syntax errors before.
Resolve-Path fails for files that do not exist yet; use [System.IO.Path]::GetFullPath(...).
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
Current full-test anchor after latest code work: 892 passed.
If full test count drops below 892 without planned test removal, treat as a regression.
Check for untracked experimental test files polluting the suite.

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
git log --oneline -10

Expected state after this handoff is committed:

Branch main
Up to date with origin/main
No tracked-file changes
Likely one untracked local reports/ directory remains
Latest pushed commit should be the HANDOFF_77 commit, after:
fbefe0e Add H024 intended action runtime summary checker
3802077 Document H024 intended action runtime result
2ea2995 Accept H024 intended action runtime preflight rows
e407aa8 Add handoff document #76
af466d7 Fix H024 intended action runtime compile ordering
0b6eba0 Fix H024 EA intended action compile ordering
7f75685 Wire H024 intended action runtime emission
5214975 Add handoff document #75
a246c0a Add H024 EA intended action log helpers
d81b888 Add H024 intended action log contract

Known latest commits before this handoff doc commit:

fbefe0e Add H024 intended action runtime summary checker
3802077 Document H024 intended action runtime result
2ea2995 Accept H024 intended action runtime preflight rows
e407aa8 Add handoff document #76
af466d7 Fix H024 intended action runtime compile ordering
0b6eba0 Fix H024 EA intended action compile ordering
7f75685 Wire H024 intended action runtime emission
5214975 Add handoff document #75
a246c0a Add H024 EA intended action log helpers
d81b888 Add H024 intended action log contract
Current Test Anchor

Current full-test anchor:

892 passed

Latest full suite:

892 passed in 19.76s

Latest focused runtime summary checker test:

2 passed in 0.71s

Previous anchors:

890 passed after verifier accepted/validated intended-action runtime rows.
888 passed after runtime intended-action emission static tests.
886 passed after H024 EA intended-action static helper tests.
883 passed after Python intended-action log contract.
880 passed after pure-math position sizing.

If full tests pass but count drops below 892 without explicit test-removal intent, stop and treat it as a regression.

Work Since HANDOFF_76
Runtime Collection Attempt

The user explicitly authorized log-only runtime intended-action collection.

Boundary used:

Manual EA attach/remove only.
No chart attach/detach automation.
No GUI automation.
No orders.
No execution adapter.
No demo/live trading.

The first command failed because the helper requires --terminal-data-dir.

Correct terminal paths used:

MetaEditor:

C:\Program Files\MetaTrader 5\MetaEditor64.exe

Terminal data dir:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075

Correct helper form:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --reset-runtime-log

Then after manual attach/remove:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --collect
Runtime Collection Result Before Verifier Fix

The EA compiled/copied and runtime CSV was collected:

Collected runtime CSV to: reports\h024_ea_log_only_preflight.csv
Rows: 144
Violations: 25
Verdict: FAIL

The failure was not because intended-action rows were missing.

The failure was because the existing preflight verifier treated the newly emitted intended-action runtime events as unexpected:

unexpected event 'H024_INTENDED_ACTION_HEADER'
unexpected event 'H024_INTENDED_ACTION_ROW'

This was a good failure.

It proved:

Runtime intended-action rows were now being emitted.
The verifier was stale.
The next correct action was verifier/test recovery, not another MT5 run.
Observed Runtime Intended-Action Rows

Runtime CSV contained intended-action rows for both symbols.

Observed event types:

H024_INTENDED_ACTION_HEADER
H024_INTENDED_ACTION_ROW

Observed intended-action schema:

h024_intended_action_log_v1

Observed normalized symbols:

XAUUSDm -> XAUUSD
USDJPYm -> USDJPY

Observed decisions in this collection:

NO_ACTION only

Important:

This runtime collection did not observe real-current-market WOULD_OPEN.

It only proved that intended-action header/row emission exists at runtime, is parseable, and currently produced NO_ACTION rows.

Commit 2ea2995
2ea2995 Accept H024 intended action runtime preflight rows

Files changed:

scripts\verify_h024_ea_preflight_log.py
tests\test_h024_ea_preflight_log_verifier.py

What changed:

Added H024_INTENDED_ACTION_HEADER and H024_INTENDED_ACTION_ROW to allowed runtime events.
Added validation for intended-action payload shape.
Validates frozen intended-action schema version.
Validates H4 timeframe.
Validates payload symbol matches preflight symbol.
Validates normalized symbols are expected model symbols.
Validates decisions are only:
WOULD_OPEN
BLOCKED
NO_ACTION
Validates WOULD_OPEN has long or short direction.
Validates numeric payload fields are parseable.
Validates volume_digits is an integer.
Validates reason is non-empty.
Added tests proving valid intended-action runtime rows pass.
Added tests proving bad intended-action schema fails.

Focused tests:

48 passed in 1.12s

Collected runtime CSV verification after patch:

H024 log-only EA runtime preflight verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Rows: 144
Violations: 0

Verdict: PASS

Full suite:

890 passed in 30.59s

Commit pushed to origin/main.

Commit 3802077
3802077 Document H024 intended action runtime result

File added:

docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md

Purpose:

Preserve the runtime intended-action observation result because reports/ is local/untracked.
Record that runtime verifier passed with 144 rows and 0 violations.
Record that observed decisions were NO_ACTION only.
Preserve deployment boundary.

This was docs-only.

No full pytest was run, appropriately.

Commit pushed to origin/main.

Commit fbefe0e
fbefe0e Add H024 intended action runtime summary checker

Files added:

scripts\summarize_h024_ea_intended_action_runtime.py
tests\test_h024_ea_intended_action_runtime_summary.py

Purpose:

Add a small CSV-only runtime intended-action summary checker.
It does not touch MT5.
It does not attach charts.
It does not perform GUI automation.
It does not send/check/modify orders.
It summarizes counts by symbol and decision from collected log-only CSVs.

Focused tests:

2 passed in 0.71s

Runtime summary command:

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_preflight.csv

Observed runtime summary:

H024 intended-action runtime summary
========================================================================
Research only. No demo/live/Phase 4 approval.

CSV: reports\h024_ea_log_only_preflight.csv
Total rows: 144
Intended-action header rows: 2
Intended-action data rows: 23

USDJPYm:
  headers: 1
  rows: 11
  normalized: USDJPY
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 11

XAUUSDm:
  headers: 1
  rows: 12
  normalized: XAUUSD
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 12

Verdict: PASS

Full suite:

892 passed in 19.76s

Commit pushed to origin/main.

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
EA strategy-intent rows are deduplicated at runtime.
Synthetic WOULD_OPEN validation passed.
WOULD_OPEN semantic is isolated from actual order execution.
Conflict blocks and warmup gates are proven.
Pure-math position sizing exists in Python and MQL5.
Position sizing has TDD coverage.
Python intended-action log contract exists.
MQL5 intended-action log helper/header/row-builder exists.
Runtime intended-action emission is wired into the log-only EA source.
EA source compiled into refreshed .ex5 after af466d7.
Runtime intended-action rows were observed from actual EA runtime CSV.
Runtime intended-action rows passed updated verifier.
Runtime intended-action summary checker exists and passed against collected CSV.
Full test anchor is now 892 passed.

What is still missing before first demo deployment:

Runtime WOULD_OPEN intended-action rows have not yet been observed under real current market/runtime conditions after the new intended-action wiring.
No demo execution adapter exists.
No order placement behavior has been tested.
No order rejection behavior has been tested.
No requote/slippage behavior has been tested.
No position reconciliation behavior exists.
No kill-switch-to-execution boundary has been implemented.
2023 weakness remains real and visible.
No demo execution approval.
No live execution approval.
No Phase 4 approval.
Current Safe Automation State

Already automated:

Copy EA source to terminal MQL5\Experts
Compile EA with MetaEditor
Reset/collect/verify runtime CSV
Terminal preflight
Profile/template validation
Runtime intended-action CSV summary checker

Not approved:

EA chart attachment/detachment automation
GUI automation
MT5 launcher/profile mutation affecting live terminals
Order-send automation
Demo/live execution adapter
Detected Local MT5 Paths

MetaEditor:

C:\Program Files\MetaTrader 5\MetaEditor64.exe

Terminal data directory:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075

EA source copied to terminal:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5

Compiled EX5:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5
Data And Source Rules

Accepted source for strict validation/diagnostics:

Exness demo MT5 broker-native exports only

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
Local compile logs

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

Pure-math sizing reference:

quantcore\strategy\h024_position_sizer.py
tests\test_h024_position_sizing.py

Intended-action log contract and runtime verification:

quantcore\execution\h024_intended_action_log.py
tests\test_h024_intended_action_log_contract.py
tests\test_h024_ea_intended_action_log_contract_static.py
tests\test_h024_ea_intended_action_runtime_emission_static.py
scripts\summarize_h024_ea_intended_action_runtime.py
tests\test_h024_ea_intended_action_runtime_summary.py

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
docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
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

Python signal definition in:

quantcore\strategy\h024.py

Signal mechanics:

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
Entry uses next H4 bar open t+1.
Last bar signal is suppressed by bridge because there is no next entry bar.
H024 Prior Evidence Summary

Preliminary fixed lifecycle on strict Exness broker-native H4/M1 complete windows:

Hold    Accepted    Executed    Skipped    Fills    Stops    Stop rate    Ending equity    PnL    Return    Max DD    Win rate    PF
1 H4    5476        861         4615       931      21       2.2556%      8450.96          -1549.04 -15.4904% -22.5043% 45.4350% 0.849209
2 H4    5476        559         4917       604      45       7.4503%      10925.34          925.34   9.2534% -14.0533% 50.8278% 1.076884
3 H4    5476        424         5052       459      56       12.2004%     14093.92         4093.92  40.9392%  -6.7346% 52.2876% 1.356184
4 H4    5476        285         5191       307      54       17.5896%     11236.27         1236.27  12.3627%  -6.8030% 49.5114% 1.151364

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

anchored_train_25%_test_rest:
test 2023-01-05T22:00:00+00:00 through 2026-04-30T01:00:00+00:00
fills 359
return 17.8797%
max DD -6.6593%
PF 1.225915
headline pass yes

anchored_train_50%_test_rest:
test 2024-03-05T22:00:00+00:00 through 2026-04-30T01:00:00+00:00
fills 244
return 19.2253%
max DD -4.4683%
PF 1.384976
headline pass yes

anchored_train_75%_test_rest:
test 2025-04-02T21:00:00+00:00 through 2026-04-30T01:00:00+00:00
fills 114
return 13.9192%
max DD -2.6061%
PF 1.653426
headline pass yes

Direction-flip negative control:

frozen H024 PF: 1.356184
direction flip PF: 0.620728
baseline minus direction-flip PnL: 7990.81 USD

Ledger-level permutation diagnostic:

permutation runs: 10000
seed: 240240
max-drawdown worse/equal rate: 57.4400%
min-equity worse/equal rate: 64.3000%
permutation ruin count: 0

This does not replace full execution timestamp shuffle.

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

Previously observed account/terminal facts:

Account currency: USD
Account leverage: 2000
Terminal connected: true
Terminal trade_allowed: false

Important:

terminal_trade_allowed=false was previously observed and must be understood before later execution gates.
Current runtime CSV also showed terminal_trade_allowed=false and mql_trade_allowed=false.
This does not block read-only/log-only preflight.
This does not approve demo trading.

Latest runtime CSV showed account fields including:

account_balance: 1246.45
account_equity: 1246.45
account_leverage: 2000
account_trade_allowed: true
account_trade_expert: true
terminal_connected: true
terminal_trade_allowed: false
mql_trade_allowed: false
EA Runtime State

Current EA source:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5

Current runtime schema:

schema_version = h024_ea_log_only_preflight_v2

Current intended-action schema:

H024_INTENDED_ACTION_LOG_SCHEMA_VERSION = h024_intended_action_log_v1

Current EA runtime input version:

InpEaVersion = 0.6

Current MQL5 property version:

#property version "0.600"

Important:

The EA contains pure-math lot sizing: ComputeH024LotSize(...).
The EA contains intended-action log helper functions:
BuildH024IntendedActionLogHeader()
BuildH024IntendedActionLogRow(...)
The EA now wires intended-action output into runtime log-only CSV rows:
H024_INTENDED_ACTION_HEADER
H024_INTENDED_ACTION_ROW
Runtime intended-action row creation uses BuildH024IntendedActionLogRow(...).
Runtime intended-action volume digits use H024RuntimeVolumeDigits(...) to avoid MQL5 function ordering issues.
These helpers are isolated log/string/math only.
They do not send, check, modify, close, or prepare orders.
MT5 Compile Debug History

Before af466d7, compile artifact recovery exposed several useful facts:

Helper/direct MetaEditor returned exit code 0 while no .ex5 was produced.
Explicit direct compile log was necessary to reveal actual compiler errors.
Stale source-level .log files can mislead.
MQL5 rejected helper usage before declaration:
undeclared identifier 'H024VolumeDigits'
MQL5 also rejected the naive forward declaration:
function 'H024VolumeDigits' must have a body
Final accepted path:
Define runtime-local H024RuntimeVolumeDigits(...) before the runtime writer.
Compile then produced/refreshed .ex5.

Do not assume MetaEditor exit code alone is reliable.

Accepted compile evidence must include:

.ex5 exists or refreshed, and
source/log errors are understood when .ex5 is missing.
Recommended Next Work

Best next gate:

Controlled log-only WOULD_OPEN observation.

This means:

Do not build an execution adapter yet.
Do not place orders.
Do not call OrderSend, OrderCheck, or CTrade.
Do not automate chart attach/detach.
Do not use GUI automation.
Keep all runtime observation log-only.
Try to observe WOULD_OPEN intended-action rows under controlled log-only conditions.
Preserve result in an ops doc only if it records a real result.

A safe next technical enhancement before another MT5 run:

Add a runtime intended-action summary/result doc update that explicitly records current NO_ACTION-only observation and defines the exact criteria for a future log-only WOULD_OPEN pass.

Another safe next technical gate:

Add a checker/test that fails if a collected runtime CSV lacks at least one intended-action header and row per expected symbol.

This is already mostly covered by:

scripts\summarize_h024_ea_intended_action_runtime.py

Do not jump to:

order sending
execution adapter
chart attach/detach automation
GUI automation
demo trading
live trading
Absolute Do-Not Rules

Do not demo trade, live trade, or approve Phase 4.

Do not treat H024 as deployment-ready.

Do not hide 2023 weakness with filters or time/session buckets.

Do not use HistData or synthesize bars.

Do not combine broker H4 with HistData M1.

Do not modify raw broker files.

Do not change .gitignore from /data/ to data/.

Do not continue development while local commits are unpushed.

Do not allow full-test count to drop below 892 without explicit test-removal intent.

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
MetaEditor CLI may return zero while no .ex5 is produced; verify .ex5 exists/refreshed.
Treat missing .ex5 as compile failure.
Explicit MetaEditor compile logs are useful:
MetaEditor64.exe /compile:"<mq5>" /log:"<log>"
Stale H024_LogOnly_Preflight.log can mislead. Remove stale logs before direct compile diagnostics.
Python indentation inside PowerShell here-strings caused repeated IndentationError; use simpler PowerShell-native file append or [System.IO.File]::WriteAllText.
Do not escape Python triple-quote docstrings as \"\"\"; that creates literal backslashes and Python syntax errors.
Resolve-Path fails for files that do not exist yet; use [System.IO.Path]::GetFullPath(...).
MQL5 may reject ordinary forward declarations with “function must have a body.” Prefer ordering functions before use or add small local helpers defined before use.
Exact First Response The Next AI Should Give
Understood. Continuing from HANDOFF_77.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, clean except possibly local reports/, and pushed.
Current full-test anchor is 892 passed.
Latest code commit should include fbefe0e Add H024 intended action runtime summary checker.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
Runtime intended-action rows have now been observed from actual MT5 log-only EA runtime CSV.
The verifier now accepts and validates H024_INTENDED_ACTION_HEADER and H024_INTENDED_ACTION_ROW.
Collected runtime CSV verification passed with 144 rows and 0 violations.
Runtime summary checker passed with 2 headers and 23 intended-action data rows.
USDJPYm had 11 NO_ACTION rows and normalized to USDJPY.
XAUUSDm had 12 NO_ACTION rows and normalized to XAUUSD.
No runtime WOULD_OPEN row was observed in this collection.
No order-send, no CTrade, no MqlTradeRequest, no execution adapter.
Attach/detach automation is not approved. GUI automation is not approved.
Local reports must not be committed.
2023 weakness remains real and must not be hidden with filters.
Best next gate is controlled log-only WOULD_OPEN observation, not execution.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
