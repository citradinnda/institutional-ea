# HANDOFF_79 — After H024 Runtime Price/Sizing Diagnostics and Dry-Run Reconciliation Gate

If any older handoff conflicts with this one, this handoff wins. It continues from HANDOFF_78.

This handoff is standalone enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current stage:

Execution-safety preparation after H024 research evidence.

Current status:

H024 is promising, but still **not demo-approved, not live-approved, and not Phase 4-approved**.

No order execution is approved.

## Environment

Use:

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

Current expected repo state before this handoff is committed:

On branch main
Up to date with origin/main
Tracked tree clean
Untracked: reports/
Latest commit: bf5f420 Preserve H024 blocked sizing diagnostics

Current full-test anchor:

921 passed in 19.22s

If tests drop below 921 without intentional test removal, treat as a regression.

Human Preference

The user is tired of excessive ceremony.

Going forward:

Keep responses practical and concise.
Prefer one copy/paste PowerShell block when commands are needed.
Do one real action at a time.
Do not create governance docs unless they preserve a real result, preserve a handoff, prevent ambiguity, or protect against future confusion.
For docs-only edits, do not run full pytest unless there is a clear reason.
For code edits, tests are mandatory.
Avoid long real-data diagnostics casually.
For real-data diagnostics, get explicit authorization or make a clear safety-bound decision.
Never soften deployment boundaries because H024 is promising.

The user’s stated goal:

make the EA survive the future, not fit the past

Important sentiment:

The user is eager to deploy.
The user accepts evidence gates.
Be direct: H024 is serious, but still not demo deployable.

Non-Negotiable Safety Boundary

H024 remains:

Research / pre-deployment only
No demo deployment approval
No live trading approval
No Phase 4 execution approval
No order-send capability approved
No execution adapter approved

Forbidden for the log-only EA:

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
Pending order helpers

Not approved:

EA chart attach/detach automation
GUI automation
MT5 launcher/profile mutation affecting live terminals
Order-send automation
Demo/live execution adapter

Allowed so far:

Manual EA attach/remove
Copy EA source to terminal Experts
Compile EA with MetaEditor
Reset/collect runtime CSV
Verify runtime CSV
Summarize intended-action rows
Historical log-only replay using InpH024ClosedShift
CSV-read-only dry-run request reconciliation
Pure Python dry-run execution request contracts
Current Latest Commits

Expected recent history before committing this handoff:

bf5f420 Preserve H024 blocked sizing diagnostics
3874c01 Update H024 closed-shift static expectation
fe8abd1 Populate H024 runtime intended-action prices
6f49ff4 Add H024 runtime dry-run reconciliation
d1d0956 Add H024 dry-run execution request contract
43faae3 Guard H024 closed-shift replay boundary
2f1cbdb Clean H024 runtime result formatting
4f4a89e Record H024 replay logging gate decision
278485b Add handoff document #78
6d40e6a Document H024 replay WOULD_OPEN runtime result
What Changed Since HANDOFF_78
1. Preserved HANDOFF_78

Commit:

278485b Add handoff document #78

docs/operations/handoffs/HANDOFF_78.md was committed and pushed.

2. Recorded historical replay logging gate decision

Commit:

4f4a89e Record H024 replay logging gate decision

Then cleaned formatting:

2f1cbdb Clean H024 runtime result formatting

Doc updated:

docs/operations/H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md

Decision recorded:

Historical log-only replay counts as sufficient for the pre-execution runtime intended-action WOULD_OPEN logging gate.

Scope explicitly preserved:

It proves runtime WOULD_OPEN logging path under controlled historical log-only replay.
It does not prove real-current-market signal occurrence.
It does not approve demo trading.
It does not approve live trading.
It does not approve Phase 4.
It does not approve OrderSend, OrderCheck, CTrade, MqlTradeRequest, or any execution adapter.
3. Added static guard for closed-shift replay boundary

Commit:

43faae3 Guard H024 closed-shift replay boundary

New test:

tests/test_h024_ea_closed_shift_execution_boundary_static.py

Purpose:

Ensures InpH024ClosedShift remains bounded.
Ensures raw InpH024ClosedShift is not used outside the bounded helper.
Ensures closed-shift replay did not add any trade API surface.

Focused tests at the time:

17 passed

Full suite after this:

901 passed
4. Added pure dry-run execution request contract

Commit:

d1d0956 Add H024 dry-run execution request contract

New files:

quantcore/execution/h024_dry_run_execution_request.py
tests/test_h024_dry_run_execution_request_contract.py

Purpose:

Convert a validated intended-action row into a deterministic hypothetical dry-run request shape.

Schema:

h024_dry_run_execution_request_v1

Required fields:

schema_version
source_schema_version
timestamp
symbol
normalized_symbol
timeframe
request_kind
side
volume_lots
entry_price
stop_loss
risk_usd
source_reason

Behavior:

WOULD_OPEN long -> dry-run BUY request.
WOULD_OPEN short -> dry-run SELL request.
BLOCKED / NO_ACTION -> no request.
Missing fields reject.
Zero lots reject.
Invalid direction rejects.

Safety:

Pure Python only.
No MT5 access.
No order execution.
No OrderSend / OrderCheck / CTrade / MqlTradeRequest.

Full suite after this:

908 passed
5. Added runtime CSV -> dry-run request reconciler

Commit:

6f49ff4 Add H024 runtime dry-run reconciliation

New files:

scripts/reconcile_h024_runtime_dry_run_requests.py
tests/test_h024_runtime_dry_run_reconciliation.py

Purpose:

Read collected log-only runtime CSVs, validate them through existing preflight verifier, reconstruct intended-action rows, and produce dry-run request JSONL only when rows are genuinely executable.

Safety:

CSV read only.
No MT5 access.
No order execution.
No trade APIs.

Command:

python scripts\reconcile_h024_runtime_dry_run_requests.py <csv> --require-request --output-jsonl <path>

Full suite after this:

914 passed
6. Reconciler rejected old replay CSV correctly

Old replay CSV:

reports\h024_ea_log_only_replay_would_open.csv

Result:

Preflight verifier: PASS
Intended-action summary with --require-would-open: PASS
Dry-run reconciler with --require-request: FAIL

Reason:

The replay emitted WOULD_OPEN rows, but all had:

entry_price=0
stop_price=0
raw_lots=0
lots=0

Interpretation:

This was a good failure. The old replay proved the runtime WOULD_OPEN log path, but did not prove reconstructable dry-run execution intent.

The correct conclusion:

Runtime WOULD_OPEN path: PASS
Executable dry-run request reconstruction: FAIL
7. Patched EA to derive runtime entry/stop prices

Commit:

fe8abd1 Populate H024 runtime intended-action prices

Files changed:

ea_mt5/Experts/H024_LogOnly_Preflight.mq5
tests/test_h024_ea_intended_action_runtime_prices_static.py

New helper:

bool H024RuntimeEntryStopPrices(
   const string direction,
   double &entry_price,
   double &stop_price
)

Behavior:

Uses H024EffectiveClosedShift().
Uses broker-native H4 rates.
Uses ATR window = 3.
Uses stop ATR multiple = 2.0.
Entry = closed H4 bar close.
Long stop = entry - 2 ATR.
Short stop = entry + 2 ATR.
Prices normalized by symbol digits.

Runtime row now:

Computes entry/stop for signal rows.
If entry/stop invalid, converts WOULD_OPEN to BLOCKED:invalid_entry_stop_for_would_open.
If computed volume is below minimum, converts WOULD_OPEN to BLOCKED:volume_below_min_for_would_open.
Still sends no orders and uses no trade APIs.

EA static verifier:

Violations: 0
Verdict: PASS

MetaEditor compile helper:

MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.
8. Updated stale closed-shift static expectation

Commit:

3874c01 Update H024 closed-shift static expectation

Reason:

Adding H024RuntimeEntryStopPrices() introduced a third valid use of:

const int closed_shift = H024EffectiveClosedShift();

Test updated from count 2 to count 3.

Full suite after this:

917 passed
9. Replayed again after runtime price patch

New local replay CSV:

reports\h024_ea_log_only_replay_would_open_prices.csv

Result:

Preflight verifier:

Rows: 312
Violations: 0
Verdict: PASS

Intended-action summary with --require-would-open:

Total rows: 312
Intended-action header rows: 2
Intended-action data rows: 51
Observed WOULD_OPEN rows: 0

USDJPYm:
  rows: 17
  WOULD_OPEN: 0
  BLOCKED: 17
  NO_ACTION: 0

XAUUSDm:
  rows: 34
  WOULD_OPEN: 0
  BLOCKED: 34
  NO_ACTION: 0

Verdict: FAIL
Violation:
- missing required runtime WOULD_OPEN intended-action row

Dry-run reconciler with --require-request:

Rows: 312
Intended-action rows: 51
WOULD_OPEN rows: 0
Dry-run requests: 0
Skipped non-request rows: 51
Verdict: FAIL
Violation:
- missing required dry-run execution request

This is correct behavior.

Interpretation:

Signal path was observed.
Entry/stop derivation worked.
The EA refused to mark the rows as executable because computed lots were below broker minimum volume.
No fake executable request was produced.
10. Quantified broker min-volume sizing infeasibility

From replay diagnostic script on:

reports\h024_ea_log_only_replay_would_open_prices.csv

XAUUSDm long:

entry=4593.801
stop=4525.492
stop_distance=68.309
loss_per_1_lot_usd=6830.90
balance=1246.45
risk_fraction=1.0000%
current_risk_usd=12.46
raw_lots_at_current_risk=0.001825
min_volume=0.01
min_risk_usd_for_min_volume=68.31
min_balance_at_same_risk_fraction=6830.90
min_risk_fraction_at_same_balance=5.4803%
reason=BLOCKED:volume_below_min_for_would_open

USDJPYm short:

entry=155.821
stop=158.163
stop_distance=2.342
loss_per_1_lot_usd=1494.63
balance=1246.45
risk_fraction=1.0000%
current_risk_usd=12.46
raw_lots_at_current_risk=0.008340
min_volume=0.01
min_risk_usd_for_min_volume=14.95
min_balance_at_same_risk_fraction=1494.63
min_risk_fraction_at_same_balance=1.1991%
reason=BLOCKED:volume_below_min_for_would_open

Important interpretation:

At the current balance and 1% risk:

USDJPY is close but still below broker min volume.
XAUUSD is far below broker min volume.
Do not casually raise risk to force execution.
This is exactly why the dry-run gate exists.
11. Preserved blocked sizing diagnostics

Commit:

bf5f420 Preserve H024 blocked sizing diagnostics

Files changed:

quantcore/execution/h024_intended_action_log.py
ea_mt5/Experts/H024_LogOnly_Preflight.mq5
tests/test_h024_intended_action_blocked_sizing_diagnostics.py
tests/test_h024_ea_blocked_sizing_diagnostics_static.py

Before:

Blocked signal rows with positive entry/stop still logged:

stop_distance_price=0
raw_lots=0
lots=0

After:

Blocked signal rows now preserve diagnostics:

decision=BLOCKED
entry_price=positive
stop_price=positive
stop_distance_price=positive
raw_lots=positive but below min_volume
lots=0

This is the correct behavior for:

signal exists, but broker min-volume makes it non-executable under current sizing

Focused tests:

16 passed

EA source static verifier:

Violations: 0
Verdict: PASS

Compile helper:

EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Full suite after this:

921 passed in 19.22s
Current Evidence Reality Check

What is now true:

H024 backtest is promising.
Broker-cost reconciliation passed.
MT5 order-behavior facts were audited statically/read-only.
Python terminal/account preflight passed.
Log-only EA exists.
EA compiles into refreshed EX5.
EA has no order-send path.
EA logs runtime preflight rows.
EA logs intended-action header and row events.
Runtime intended-action NO_ACTION rows were observed in real current log-only runtime.
Strict --require-would-open gate exists.
Historical log-only replay previously observed WOULD_OPEN path.
Dry-run request contract exists in pure Python.
Runtime CSV -> dry-run request reconciler exists and is CSV-read-only.
Reconciler correctly rejects non-executable rows.
EA now derives entry/stop for signal rows.
EA now converts under-min-volume signal rows into BLOCKED, not fake WOULD_OPEN.
Blocked signal rows now preserve sizing diagnostics.
Full test anchor is 921 passed.

What remains missing:

No real-current-market WOULD_OPEN runtime row has been observed.
No executable dry-run request has been reconstructed from runtime CSV yet.
Current replay signal rows are blocked by broker min-volume at current account/risk.
No demo execution adapter exists.
No order placement behavior has been tested.
No order rejection behavior has been tested.
No requote/slippage behavior has been tested.
No position reconciliation exists.
No kill-switch-to-execution boundary has been implemented.
No demo approval.
No live approval.
No Phase 4 approval.
2023 weakness remains real.

Answer if asked “are we ready to demo/live?”:

No.

Answer if asked “did H024 signal path work?”:

Yes, in historical log-only replay.

Answer if asked “did executable dry-run request reconstruction pass?”:

No. It correctly failed because the replayed signals were below broker minimum volume under the current balance/risk settings.

Current Important Commands

Verify full suite:

python -m pytest -q

Expected current anchor:

921 passed

Verify current real-runtime CSV normal summary:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_preflight.csv
python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_preflight.csv

Strict gate on current real-runtime CSV:

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_preflight.csv --require-would-open

Expected currently:

FAIL, because current real-runtime CSV has 0 WOULD_OPEN rows.

Verify old historical replay CSV strict gate:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_would_open.csv
python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_would_open.csv --require-would-open

Expected:

PASS for the old runtime WOULD_OPEN logging gate if local CSV remains available.

But dry-run reconciliation on this old CSV is expected to FAIL because rows had zero entry/stop/lots:

python scripts\reconcile_h024_runtime_dry_run_requests.py reports\h024_ea_log_only_replay_would_open.csv --require-request

Verify latest replay-with-prices CSV:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_would_open_prices.csv
python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_would_open_prices.csv --require-would-open
python scripts\reconcile_h024_runtime_dry_run_requests.py reports\h024_ea_log_only_replay_would_open_prices.csv --require-request

Expected:

Preflight verifier: PASS
Intended-action --require-would-open: FAIL because rows are BLOCKED
Dry-run --require-request: FAIL because rows are below min volume

Compile/copy EA helper:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe"

Reset runtime log before manual attach:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --reset-runtime-log

Collect runtime CSV after manual attach/remove:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --collect

Collect to replay report path:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --collect `
  --report-path reports\h024_ea_log_only_replay_would_open_prices.csv
MT5 Local Paths

MetaEditor:

C:\Program Files\MetaTrader 5\MetaEditor64.exe

Terminal data dir:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075

Terminal EA source:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5

Compiled EX5:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5

Runtime CSV in terminal:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\h024_ea_log_only_preflight.csv

Repo report CSVs:

reports\h024_ea_log_only_preflight.csv
reports\h024_ea_log_only_replay_would_open.csv
reports\h024_ea_log_only_replay_would_open_prices.csv

Do not commit reports/.

Current EA Facts

EA source:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5

MQL5 property version:

#property version "0.600"

Runtime schema:

h024_ea_log_only_preflight_v2

EA input version:

InpEaVersion = "0.6"

Intended-action schema:

h024_intended_action_log_v1

Current key inputs:

input bool   InpKillSwitchBlocked = true;
input string InpRunLabel = "H024_LOG_ONLY_PREFLIGHT";
input string InpSchemaVersion = "h024_ea_log_only_preflight_v2";
input string InpEaVersion = "0.6";
input string InpSourceVersion = "manual";
input string InpRuntimeMode = "log_only_preflight";
input double InpRiskFraction = 0.01;
input string InpOutputFile = "h024_ea_log_only_preflight.csv";
input int    InpTimerSeconds = 1;
input int    InpH024ClosedShift = 1;

Important:

InpH024ClosedShift defaults to 1, preserving latest-closed-bar behavior.
Set it manually for historical replay only.

Current runtime intended-action behavior:

NO_ACTION rows can carry zero entry/stop/lots.
Signal rows first derive entry/stop from closed H4 bar and ATR stop.
If signal sizing is executable, row may remain WOULD_OPEN.
If signal sizing is below broker minimum volume, row becomes BLOCKED:volume_below_min_for_would_open.
BLOCKED signal rows should preserve positive entry/stop/stop_distance/raw_lots but final lots=0.
Data Rules

Accepted validation source:

Exness demo MT5 broker-native exports only

Accepted model symbols:

USDJPY
XAUUSD

Observed Exness MT5 symbols:

USDJPYm
XAUUSDm

Normalize:

USDJPYm -> USDJPY
XAUUSDm -> XAUUSD

Accepted timeframes:

Broker-native H4
Broker-native M1

Broker timezone used by loader:

Europe/Athens
DST-aware

Do not use:

HistData for validation/tuning/production dataset creation
Broker H4 plus HistData M1 combinations
Sparse 2018 through 2021-06 broker-native prefix as dense M1
Incomplete H4/M1 windows

Do not commit:

Raw MT5 CSV files
Raw HistData files
Large derived datasets
Broker/vendor source files
Local reports/*.csv
Local reports/*.json
Local runtime CSVs
Local compile logs
H024 Mechanics Summary

H024 is a regime-conditioned pullback-continuation hypothesis.

Mechanics:

Defines directional regime using slow H4 trend state.
Waits for pullback against that regime.
Enters only if price resumes in regime direction after pullback.
Does not use H021 time/session buckets.
Does not reuse Donchian breakout trigger.
Uses H020 sizing contract.
Returns H017-compatible bridge shim.
Uses H018 hard guard semantics.
Baseline candidate: hold = 3 H4, stop ATR multiple = 2.0.

Frozen signal defaults:

slow_window = 5
slope_lag = 2
atr_window = 3
pullback_window = 3
min_pullback_atr = 0.25
max_pullback_atr = 3.0
min_slope_atr = 0.05

Signal logic:

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
Core Files

H024 core:

quantcore\strategy\h024.py
quantcore\strategy\h024_runner.py

Position sizing:

quantcore\strategy\h024_position_sizer.py
tests\test_h024_position_sizing.py

Execution/log contracts:

quantcore\execution\h024_intended_action_log.py
quantcore\execution\h024_dry_run_execution_request.py
tests\test_h024_intended_action_log_contract.py
tests\test_h024_dry_run_execution_request_contract.py
tests\test_h024_intended_action_blocked_sizing_diagnostics.py

EA/runtime:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
scripts\run_h024_mt5_log_only_preflight_local.py
scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\verify_h024_ea_source_static.py
scripts\reconcile_h024_runtime_dry_run_requests.py

Important tests:

tests\test_h024_ea_closed_shift_execution_boundary_static.py
tests\test_h024_ea_closed_shift_replay_static.py
tests\test_h024_ea_strategy_intent_detail_static.py
tests\test_h024_ea_intended_action_runtime_prices_static.py
tests\test_h024_ea_blocked_sizing_diagnostics_static.py
tests\test_h024_runtime_dry_run_reconciliation.py
tests\test_h024_ea_intended_action_runtime_summary.py
tests\test_h024_ea_preflight_log_verifier.py
tests\test_h024_ea_source_static_verifier.py
tests\test_h024_ea_intended_action_runtime_emission_static.py
tests\test_h024_ea_strategy_intent_decision_harness.py

Important docs:

docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
docs\operations\H024_EA_WOULD_OPEN_SYNTHETIC_VALIDATION_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
Recommended Next Work

Best next gate:

Re-run historical replay after bf5f420 to confirm BLOCKED signal rows now preserve:

positive stop_distance_price
positive raw_lots
lots = 0
reason = BLOCKED:volume_below_min_for_would_open

This is a runtime evidence preservation gate, not an execution gate.

Recommended next command sequence:

Reset runtime log.
Manually attach EA to replay shifts:
USDJPYm InpH024ClosedShift = 16
XAUUSDm InpH024ClosedShift = 18
Let it run briefly.
Remove both EAs.
Collect to:
reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
Verify:
preflight verifier passes
intended-action summary shows BLOCKED rows
diagnostics show positive raw lots below min volume

Do not try to force executable dry-run requests by raising risk casually.

Possible safe next technical steps:

Add a script/test that summarizes BLOCKED sizing diagnostics from runtime CSV.
Add a report/doc preserving the min-volume infeasibility result.
Add a guard that dry-run requests are never created from BLOCKED rows, even if they contain positive entry/stop/raw_lots.
Add non-execution boundary checklist/specification.
Investigate whether strategy stop model or account sizing policy needs a research-level feasibility review.

Do not jump directly to:

OrderSend
OrderCheck
CTrade
MqlTradeRequest
Execution adapter
Demo trading
Live trading
Phase 4
Chart automation
GUI automation
Immediate First Action For Next AI

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected after this handoff is committed:

On branch main
Your branch is up to date with origin/main
No tracked-file changes
Untracked reports/
Latest commit: Add handoff document #79

Then continue from the actual repo state.

Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_79.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, pushed, tracked tree clean except local reports/.
Current full-test anchor is 921 passed.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
No order-send, no OrderCheck, no CTrade, no MqlTradeRequest, no execution adapter.
Historical replay previously proved the runtime WOULD_OPEN log path.
The dry-run request reconciler correctly rejected old replay rows because they had zero entry/stop/lots.
EA runtime intended-action rows now derive entry/stop from closed H4 price and ATR stop.
Latest replay after price patch produced BLOCKED rows, not WOULD_OPEN, because computed volume was below broker min volume.
XAUUSD raw lots were about 0.001825 versus min 0.01.
USDJPY raw lots were about 0.008340 versus min 0.01.
Blocked signal rows now preserve sizing diagnostics after commit bf5f420.
reports/ stays untracked.
H024 is still not demo deployable.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
