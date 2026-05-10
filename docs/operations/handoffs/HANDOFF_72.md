# HANDOFF_72 - After H024 EA Strategy Intent Dedup Runtime Verification

If any older handoff conflicts with this file, this HANDOFF_72 wins.

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

HANDOFF_71 - After H024 EA 0.6 Log-Only Strategy Intent Runtime Preflight

This handoff:

HANDOFF_72 - After H024 EA Strategy Intent Dedup Runtime Verification
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
Current full-test anchor after latest code work: 855 passed.
If full test count drops below 855 without planned test removal, treat as a regression.

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

Expected state after this handoff commit:

branch main
up to date with origin/main
no tracked-file changes
likely one untracked local reports/ directory remains

Known latest commits before this handoff commit:

29b5c67 Record H024 EA strategy intent dedup runtime result
7e45142 Deduplicate H024 EA strategy intent emissions
b091922 Harden H024 EA would-open log verifier tests
b3657a8 Add handoff document #71
bf7d7c5 Record H024 EA log-only strategy intent runtime result
6999a46 Add H024 EA log-only strategy intent rows
2c817a8 Record H024 EA state observation parity result
43bac50 Add H024 EA state observation parity verifier
e8eaedc Add handoff document #70
f824c3c Record H024 EA state observation runtime preflight result
28bc4b5 Fix H024 EA state observation compile compatibility
aa23c79 Add H024 EA state observation rows
adc4b7b Record H024 EA closed-bar runtime preflight result
560d857 Add H024 EA closed-bar observation rows
a415548 Add handoff document #69
Current Test Anchor

Current full-test anchor:

855 passed

Latest full suite after EA strategy-intent dedup code work:

855 passed in 15.65s

Focused tests after evidence doc:

25 passed in 0.74s

If full tests pass but count drops below 855 without explicit test-removal intent, stop and treat it as a regression.

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

raw MT5 CSV files
raw HistData files
large derived datasets
broker/vendor source files
local reports/*.csv
local reports/*.json
local runtime CSVs

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

Recent result/safety docs:

docs\operations\H024_BROKER_SYMBOL_SPEC_AUDIT_RESULT.md
docs\operations\H024_OBSERVED_BROKER_COST_RESULT.md
docs\operations\H024_MT5_ORDER_BEHAVIOR_AUDIT_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\H024_MT5_TERMINAL_PREFLIGHT_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
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

Hold    Accepted    Executed    Skipped    Fills    Stops    Stop rate    Ending equity    PnL    Return    Max DD    Win rate    PF
1 H4    5476        861         4615       931      21       2.2556%      8450.96          -1549.04 -15.4904% -22.5043% 45.4350% 0.849209
2 H4    5476        559         4917       604      45       7.4503%      10925.34         925.34   9.2534%  -14.0533% 50.8278% 1.076884
3 H4    5476        424         5052       459      56       12.2004%     14093.92         4093.92  40.9392% -6.7346%  52.2876% 1.356184
4 H4    5476        285         5191       307      54       17.5896%     11236.27         1236.27  12.3627% -6.8030%  49.5114% 1.151364

H024 hold=3 was best.

Persistent weakness:

2023 PnL: -708.20
2023 PF: 0.764187

Do not add a 2023 exclusion. Do not add time/session filter.

Targeted robustness:

hold fixed at 3 H4
stop ATR multiples: 1.5, 2.0, 2.5
cost multipliers: 1.0x, 1.25x, 1.5x
all 9 targeted stop/cost scenarios passed
worst tested PF: 1.282177

Chronological validation:

Fold                         Train count  Test count  Test start UTC               Test end UTC                 Fills  Return    Max DD    PF        Headline pass
anchored_train_25%_test_rest 1369         4107        2023-01-05T22:00:00+00:00    2026-04-30T01:00:00+00:00   359    17.8797%  -6.6593%  1.225915  yes
anchored_train_50%_test_rest 2738         2738        2024-03-05T22:00:00+00:00    2026-04-30T01:00:00+00:00   244    19.2253%  -4.4683%  1.384976  yes
anchored_train_75%_test_rest 4107         1369        2025-04-02T21:00:00+00:00    2026-04-30T01:00:00+00:00   114    13.9192%  -2.6061%  1.653426  yes

Interpretation:

H024 passed a meaningful anti-curve-fit chronological test.
2023 weakness remains visible.
No 2023 exclusion or filter is approved.

Direction-flip negative control:

frozen H024 PF: 1.356184
direction flip PF: 0.620728
baseline minus direction-flip PnL: 7990.81 USD

Interpretation:

Direction-flip control materially failed.
This supports directional information in frozen H024.
It does not prove future survivability.

Ledger-level permutation diagnostic:

permutation runs: 10000
seed: 240240
max-drawdown worse/equal rate: 57.4400%
min-equity worse/equal rate: 64.3000%
permutation ruin count: 0

Interpretation:

Realized H024 trade order was not unusually lucky.
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

Do not add a 2023 exclusion. Do not tune H024.

Static MT5 order behavior audit passed for:

USDJPYm
XAUUSDm

Observed order facts:

trade_mode: 4
execution_mode: 2
order_filling_modes: 3
order_modes: 127
volume_min: 0.01
volume_step: 0.01
stops_level_points: 0
freeze_level_points: 0
spread_float: true

This does not test actual order placement, rejection behavior, requotes, slippage, market-hours behavior, or modification behavior.

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
order modification/deletion
MqlTradeRequest
MqlTradeResult
execution adapter
order ticket
position ticket
order-send result

Dry-run output only:

WOULD_OPEN
NO_ACTION
BLOCKED

Dry-run action export result:

WOULD_OPEN: 459
NO_ACTION: 4707
BLOCKED: 0

Dry-run action verifier:

Rows: 5166
WOULD_OPEN: 459
NO_ACTION: 4707
BLOCKED: 0
Violations: 0
Verdict: PASS

This does not approve demo/live/Phase 4.

MT5 Terminal/Account Preflight

Python terminal/account preflight passed:

MT5 initialized: True
Forbidden MT5 call attempts: 0
Symbols checked: 2
USDJPY / USDJPYm: ok
XAUUSD / XAUUSDm: ok
Verdict: PASS

Observed account/terminal facts:

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

Important:

terminal_trade_allowed=false was observed and must be understood before later execution gates.
This does not block read-only preflight.
This does not approve demo trading, live trading, Phase 4, EA execution, order placement, order modification, or order closing.
EA Runtime State

Current EA source:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5

Current runtime CSV:

h024_ea_log_only_preflight.csv

Runtime output location in MT5 terminal data folder:

...\MetaQuotes\Terminal\<terminal-id>\MQL5\Files\h024_ea_log_only_preflight.csv

Current terminal data directory:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075

MetaEditor:

C:\Program Files\MetaTrader 5\MetaEditor64.exe

Current runtime schema:

schema_version = h024_ea_log_only_preflight_v2
runtime_mode = log_only_preflight

Current EA runtime input version:

InpEaVersion = 0.6

Current MQL5 property version:

#property version "0.600"

Reason for difference:

Runtime/verifier version uses 0.6.
MQL5 Market-compatible property version requires xxx.yyy style; using 0.600 avoids compile failure.
Work Since HANDOFF_71
Commit b091922 - Harden H024 EA would-open log verifier tests

Added focused verifier tests for constrained WOULD_OPEN runtime-log semantics.

New/covered behavior:

Accept constrained WOULD_OPEN with side=short.
Reject WOULD_OPEN missing side.
Reject WOULD_OPEN with kill_switch_blocked=false.
Reject BLOCKED intent rows in runtime preflight.

Still no execution surface.

Full suite after this code work:

853 passed in 17.30s
Commit 7e45142 - Deduplicate H024 EA strategy intent emissions

Inspection found the EA emitted duplicate strategy-derived intent rows per runtime callback:

OnInit had duplicate WriteH024StrategyIntentRow() calls.
OnTick had triple strategy intent calls.
OnTimer had duplicate strategy intent calls.

Changed:

Removed duplicate calls.
Added tests\test_h024_ea_strategy_intent_emission_static.py.

Static guard now requires:

OnInit emits exactly one strategy-intent row.
OnTick emits exactly one strategy-intent row.
OnTimer emits exactly one strategy-intent row.
OnDeinit emits no strategy-intent row.

Focused static checks:

10 passed in 0.50s

Full suite after this code work:

855 passed in 15.65s
Commit 29b5c67 - Record H024 EA strategy intent dedup runtime result

Recorded runtime evidence doc:

docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md

Runtime confirmation after dedup:

Rows: 114
Runtime verifier: PASS, 0 violations
State parity: PASS, 22 rows checked, 550 comparisons, 0 violations

Runtime events:

INIT: 2
INTENT: 44
MARKET_STATE: 22
BAR_OBSERVATION: 22
H024_STATE_OBSERVATION: 22
DEINIT: 2

Intent shape:

generic intents: 22
strategy intents: 22
intent prefixes:
NO_ACTION: 44

Interpretation:

The deduplicated EA runtime log now shows one generic intent and one strategy-derived intent per observation cycle.
This confirms the duplicate strategy-intent emission issue was removed at runtime.
All observed strategy-derived intent rows remained NO_ACTION.
No runtime WOULD_OPEN row was observed under a real signal condition.
This result does not approve demo trading, live trading, Phase 4 execution, order placement, order modification, sizing, or execution-adapter work.

Focused tests after docs evidence:

25 passed in 0.74s

No full pytest was run for this docs-only evidence commit.

Current Deployment Reality Check

Answer if asked whether ready to demo/live:

No.

H024 is still not demo deployable.

What is now true:

Backtest H024 is promising.
Broker-cost reconciliation passed.
Static MT5 order-behavior facts passed.
Dry-run Python action export exists and passed.
MT5 terminal/account read-only preflight passed.
MQL5 log-only EA shell exists.
EA can attach manually to both USDJPYm and XAUUSDm.
EA can write versioned runtime CSV.
EA can log current H4/M1 market state.
EA can log latest completed H4/M1 bar observations.
EA can compute and log frozen H024 state ingredients from closed H4 bars.
EA state observation runtime preflight passed.
EA state observation parity with Python passed.
EA 0.6 can emit strategy-derived log-only INTENT rows.
EA 0.6 runtime log-only strategy-intent preflight passed.
EA 0.6 strategy-intent rows are now deduplicated at runtime.
EA 0.6 state parity passed after dedup runtime sample with 550 comparisons, 0 violations.
Runtime verifier passed after dedup with 114 rows, 0 violations.

What is still missing before first demo deployment:

Runtime WOULD_OPEN row emission has not been observed under a real signal condition.
Runtime WOULD_OPEN semantics need validation without adding execution surface.
Runtime position sizing in the EA is not implemented.
Executable intended-action logs are not implemented.
No demo execution adapter exists.
No order placement/modification/rejection behavior testing has been done.
No order-send path is allowed.
No explicit user authorization for Phase 4/demo execution exists.
Terminal-level trade_allowed=false was previously observed and must be understood before any execution gate.
2023 weakness remains real and visible.

Practical estimate:

Roughly 80-90% of the way to a log-only shadow EA.
Roughly 40-50% of the way to first demo deployment.
The remaining work is higher-risk because it involves WOULD_OPEN semantics, sizing, intended action logs, and eventually order behavior.
Recommended Next Work

Best next gate:

Validate runtime WOULD_OPEN behavior without adding execution surface.

Safe options:

Controlled historical/synthetic EA logic harness:
Add a pure function/test-style harness for H024 strategy intent semantics if feasible without MT5 execution.
It should prove long, short, no-signal, insufficient-warmup, and conflict outcomes.
It should remain log-only and not touch MT5 order APIs.
Controlled runtime wait:
Keep manually attaching EA in log-only mode and collect rows when a real H024 signal occurs.
Do not add attach/detach automation unless explicitly approved through a separate safety design.
Do not add order-send code.
Strengthen source/static guards:
Ensure H024StrategyIntentDetail() stays free of order-send and execution concepts.
Ensure WOULD_OPEN detail is constrained to side, closed_h4_time, source, and log-only mode.

Do not jump directly to:

sizing
order-send
execution adapter
demo deployment
live deployment
Phase 4
Current Safe Automation State

Already automated:

Copy EA source to terminal MQL5\Experts.
Compile EA with MetaEditor if MetaEditor is supplied and compilation succeeds/refreshed EX5 can be verified.
Reset runtime CSV.
Collect runtime CSV.
Verify runtime CSV.
Verify EA state observation parity.
Automation target preflight.
Inert profile/template plan validation.

Not approved:

EA chart attachment automation.
EA chart detachment automation.
GUI automation.
MT5 launcher/profile mutation that can affect a live terminal.
Order-send automation.
Demo/live execution adapter.

Reason:

Full GUI automation can accidentally interact with the wrong terminal, chart, account, or EA input.
MT5 profile/template manipulation can be brittle and terminal-specific.
Before any launcher/attach automation, the project must prove strict target validation and reject unsafe plans.
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
allow full-test count to drop below 855 without explicit test-removal intent
run brute-force timestamp shuffle again until redesigned
add OrderSend
add OrderCheck
add CTrade
add #include <Trade...>
add position open/close code
add order modification/deletion code
add MqlTradeRequest
add MqlTradeResult
add GUI attach/detach automation without explicit safety design and approval
add MT5 launcher/profile mutation code that can affect a live terminal without strict target validation
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
MetaEditor CLI may return nonzero even when compile succeeds with warnings; verify .ex5 refresh and/or logs\metaeditor.log.
MetaEditor CLI may return zero even when .ex5 is not created. Treat missing .ex5 as compile failure.
If .ex5 disappears, MT5 Navigator will not show the EA.
Manual MetaEditor Errors tab may be needed to identify MQL5 compile errors.
Python indentation inside PowerShell here-strings caused repeated IndentationError; use simpler PowerShell-native file append for docs where possible.
git diff --check caught blank lines at EOF before; fix whitespace before committing.
Resolve-Path fails for files that do not exist yet; use [System.IO.Path]::GetFullPath($path) when creating new files.
Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_72.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, clean except possibly local reports/, and pushed.
Current full-test anchor is 855 passed.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
Latest known commit before this handoff is 29b5c67 Record H024 EA strategy intent dedup runtime result.
EA runtime input version is 0.6.
MQL5 property version is 0.600.
EA 0.6 emits log-only strategy-derived INTENT rows.
EA 0.6 runtime strategy-intent dedup verification passed: 114 rows, 0 violations.
EA 0.6 runtime state parity after dedup passed: 22 rows checked, 550 comparisons, 0 violations.
Runtime intent shape after dedup was 22 generic intents and 22 strategy intents.
All observed strategy-derived intent rows were still NO_ACTION.
No runtime WOULD_OPEN row has been observed yet under a real signal condition.
No order-send, no CTrade, no MqlTradeRequest, no execution adapter.
Attach/detach automation is not approved.
GUI automation is not approved.
Order-send automation is not approved.
Local reports must not be committed.
2023 weakness remains real and must not be hidden with filters.
The next recommended gate is validating runtime WOULD_OPEN behavior without adding execution surface.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -15

Then paste the full output.