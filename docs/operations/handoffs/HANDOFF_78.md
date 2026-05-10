HANDOFF_78 — After H024 Historical Log-Only Replay WOULD_OPEN Runtime Pass

If any older handoff conflicts with this one, this handoff wins. It continues from HANDOFF_77.

This handoff is standalone enough for a new AI to continue safely without reading older handoffs first.

Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current stage:

Execution-safety preparation after H024 research evidence.

Current status:

H024 is promising, but still not demo-approved, not live-approved, and not Phase 4-approved.

No order execution is approved.

Environment

Use:

Windows
PowerShell
VS Code
Python 3.12.10 inside .venv
No WSL

Repository root:

C:\Users\equin\Documents\institutional-ea

Virtual environment:

C:\Users\equin\Documents\institutional-ea\.venv

Branch:

main

GitHub remote:

https://github.com/citradinnda/institutional-ea.git

Current expected repo state:

On branch main
Up to date with origin/main
Tracked tree clean
Untracked: reports/

Current latest commit:

6d40e6a Document H024 replay WOULD_OPEN runtime result

Recent commits:

6d40e6a Document H024 replay WOULD_OPEN runtime result
7771a0d Add H024 log-only closed shift replay input
a055e2a Add H024 runtime WOULD_OPEN gate
a077463 Update H024 intended action runtime result
3f011ca Add handoff document #77
fbefe0e Add H024 intended action runtime summary checker
3802077 Document H024 intended action runtime result
2ea2995 Accept H024 intended action runtime preflight rows
e407aa8 Add handoff document #76
af466d7 Fix H024 intended action runtime compile ordering
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
Current Test Anchor

Current full-test anchor:

898 passed

Latest full suite:

898 passed in 35.22s

Previous anchor before closed-shift replay input:

895 passed

Before runtime WOULD_OPEN gate:

892 passed

If full tests drop below 898 without intentional test removal, treat as a regression.

Latest Completed Work Since HANDOFF_77
1. Re-verified current real runtime CSV

Existing real-current log-only runtime CSV:

reports\h024_ea_log_only_preflight.csv

Verifier:

Rows: 198
Violations: 0
Verdict: PASS

Summary:

Total rows: 198
Intended-action header rows: 2
Intended-action data rows: 32

USDJPYm:
  headers: 1
  rows: 16
  normalized: USDJPY
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 16

XAUUSDm:
  headers: 1
  rows: 16
  normalized: XAUUSD
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 16

Verdict: PASS

Interpretation:

Runtime intended-action logging works.
Current real-market latest closed bars were NO_ACTION only.
No real-current-market WOULD_OPEN row observed yet.

Commit preserving this:

a077463 Update H024 intended action runtime result
2. Added strict runtime WOULD_OPEN gate

Commit:

a055e2a Add H024 runtime WOULD_OPEN gate

Files changed:

scripts\summarize_h024_ea_intended_action_runtime.py
tests\test_h024_ea_intended_action_runtime_summary.py

What changed:

The intended-action summary script now supports:

python scripts\summarize_h024_ea_intended_action_runtime.py <csv> --require-would-open

Normal mode:

Passes valid NO_ACTION-only runtime CSVs.

Strict mode:

Fails unless at least one valid H024_INTENDED_ACTION_ROW has decision WOULD_OPEN.

Focused tests:

5 passed

Full suite after this:

895 passed

Current real runtime CSV correctly fails strict mode:

Observed WOULD_OPEN rows: 0
Verdict: FAIL
Violations:
- missing required runtime WOULD_OPEN intended-action row

This is intended and protects against overclaiming.

3. Investigated old local reports

Old local reports included files like:

reports\h024_runtime_would_open_test.csv
reports\h024_full_h4_runtime_final.csv
reports\h024_full_h4_runtime_simulated.csv

These contained old-format WOULD_OPEN text in event/detail fields, but not the current runtime intended-action schema.

They failed current verifier/strict gate because they lacked required columns and lacked:

H024_INTENDED_ACTION_HEADER
H024_INTENDED_ACTION_ROW

Conclusion:

Do not use old simulated/final CSVs as proof of current runtime intended-action WOULD_OPEN.

This was the correct rejection behavior.

4. Scanned recent broker-native H4 data for H024 signal bars

A local untracked probe was created in reports:

reports\probe_recent_h024_signals.py
reports\h024_recent_h4_signal_probe.csv

These are local/untracked and must not be committed.

The first probe attempts failed because:

MT5 H4 files are tab-delimited.
Columns are MT5-style:
<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>

After fixing pd.read_csv(path, sep="\t"), the scan parsed successfully.

Data parsed:

USDJPY H4:
  raw rows: 8753
  parsed rows: 8753
  first: 2018-07-03 00:00 UTC
  last: 2026-05-08 20:00 UTC

XAUUSD H4:
  raw rows: 8698
  parsed rows: 8698
  first: 2018-06-28 00:00 UTC
  last: 2026-05-08 20:00 UTC

Recent H024 signals found:

USDJPY recent H4 signals: 6

2026-04-23 16:00 UTC  WOULD_OPEN_LONG
2026-04-27 00:00 UTC  WOULD_OPEN_SHORT
2026-05-01 04:00 UTC  WOULD_OPEN_SHORT
2026-05-05 08:00 UTC  WOULD_OPEN_LONG
2026-05-05 16:00 UTC  WOULD_OPEN_LONG
2026-05-06 04:00 UTC  WOULD_OPEN_SHORT

XAUUSD recent H4 signals: 7

2026-04-14 12:00 UTC  WOULD_OPEN_LONG
2026-04-21 12:00 UTC  WOULD_OPEN_SHORT
2026-04-28 00:00 UTC  WOULD_OPEN_SHORT
2026-04-30 04:00 UTC  WOULD_OPEN_LONG
2026-05-01 04:00 UTC  WOULD_OPEN_SHORT
2026-05-04 04:00 UTC  WOULD_OPEN_SHORT
2026-05-05 20:00 UTC  WOULD_OPEN_LONG

Latest closed bars at 2026-05-08 20:00 UTC were still NO_ACTION for both symbols.

Conclusion:

EA not broken.
Current latest bars are simply no-signal.
Historical replay is the safe shortcut to observe WOULD_OPEN without waiting for a new market signal.
5. Added closed-shift replay input to log-only EA

Commit:

7771a0d Add H024 log-only closed shift replay input

Files changed:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
tests\test_h024_ea_closed_shift_replay_static.py
tests\test_h024_ea_strategy_intent_detail_static.py

New EA input:

input int InpH024ClosedShift = 1;

New helper:

int H024EffectiveClosedShift()
{
   if(InpH024ClosedShift < 1)
   {
      return 1;
   }
   if(InpH024ClosedShift > 240)
   {
      return 240;
   }
   return InpH024ClosedShift;
}

Runtime state/intent evaluation now uses:

const int closed_shift = H024EffectiveClosedShift();

Default behavior remains unchanged:

InpH024ClosedShift = 1 means latest closed H4 bar.

Replay behavior:

Set InpH024ClosedShift to a larger value to evaluate a historical closed H4 bar.

Safety:

No trade API added.
No OrderSend.
No CTrade.
No MqlTradeRequest.
No execution adapter.
Log-only behavior preserved.

Focused tests after patch:

16 passed

EA static verifier:

Violations: 0
Verdict: PASS

Compile helper:

MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Full suite:

898 passed

Important detail:

A stale static test expected:

const int closed_shift = 1;

It was correctly updated to expect:

const int closed_shift = H024EffectiveClosedShift();
6. Historical log-only replay WOULD_OPEN runtime pass

First replay attempt used wrong shifts:

USDJPYm InpH024ClosedShift = 17
XAUUSDm InpH024ClosedShift = 19

Result:

Verifier: PASS
Strict WOULD_OPEN gate: FAIL
Observed WOULD_OPEN rows: 0

Inspector showed actual evaluated bars:

USDJPYm evaluated 2026.05.06 00:00:00
XAUUSDm evaluated 2026.05.06 00:00:00 and 2026.05.05 16:00:00

Conclusion:

Replay input worked.
Shift numbers were off by one for actual MT5 chart history.

Corrected replay shifts:

USDJPYm:
  InpH024ClosedShift = 16
  Target bar: 2026.05.06 04:00:00 UTC
  Expected direction: short

XAUUSDm:
  InpH024ClosedShift = 18
  Target bar: 2026.05.05 20:00:00 UTC
  Expected direction: long

Corrected replay result:

Replay CSV: reports\h024_ea_log_only_replay_would_open.csv
Rows: 228
Violations: 0
Verifier: PASS

Strict intended-action summary:

Total rows: 228
Intended-action header rows: 2
Intended-action data rows: 37
Required WOULD_OPEN rows: at least 1
Observed WOULD_OPEN rows: 37

USDJPYm:
  headers: 1
  rows: 18
  normalized: USDJPY
  WOULD_OPEN: 18
  BLOCKED: 0
  NO_ACTION: 0

XAUUSDm:
  headers: 1
  rows: 19
  normalized: XAUUSD
  WOULD_OPEN: 19
  BLOCKED: 0
  NO_ACTION: 0

Verdict: PASS

Interpretation:

The EA runtime intended-action WOULD_OPEN path is now observed and parseable in MT5 log-only runtime output.
This is historical replay evidence, not real-current-market signal evidence.
Repeated rows are expected because the timer emits repeatedly while the EA is attached.

Commit documenting this:

6d40e6a Document H024 replay WOULD_OPEN runtime result

Doc updated:

docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
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
Runtime intended-action WOULD_OPEN rows were observed in controlled historical log-only replay.
Runtime verifier passes on current runtime CSVs.
Strict WOULD_OPEN gate exists and passed on historical replay CSV.
Full test anchor is now 898 passed.

What remains missing:

No real-current-market WOULD_OPEN runtime row has been observed yet.
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
H024 is more execution-prepared than before, but still not demo deployable.
Current Important Commands

Verify current real-runtime CSV normal summary:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_preflight.csv
python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_preflight.csv

Strict gate on current real-runtime CSV:

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_preflight.csv --require-would-open

Expected currently:

FAIL, because current real-runtime CSV has 0 WOULD_OPEN rows.

Verify replay CSV strict gate:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_would_open.csv
python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_would_open.csv --require-would-open

Expected:

PASS, if local replay CSV remains available.

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
  --report-path reports\h024_ea_log_only_replay_would_open.csv
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
tests\test_h024_intended_action_log_contract.py

EA/runtime:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
scripts\run_h024_mt5_log_only_preflight_local.py
scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\verify_h024_ea_source_static.py

Important tests:

tests\test_h024_ea_closed_shift_replay_static.py
tests\test_h024_ea_strategy_intent_detail_static.py
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

Decide whether controlled historical log-only replay WOULD_OPEN is sufficient for the pre-execution logging gate,
or require a future real-current-market log-only WOULD_OPEN observation.

My recommendation:

Historical replay SHOULD count as sufficient for proving the runtime WOULD_OPEN log path.
Real-current-market WOULD_OPEN observation can remain a monitoring/evidence item, but should not block all further non-execution safety prep.

Safe next technical work:

Add a small ops decision doc section explicitly saying:
- Historical log-only replay passes the WOULD_OPEN logging gate.
- It does not approve demo/live/Phase 4.
- It authorizes only the next non-execution prep step.

Possible next non-execution prep steps:

1. Formalize execution boundary checklist before any adapter.
2. Add static test guaranteeing InpH024ClosedShift cannot be used in future execution mode.
3. Add an execution adapter design doc only — no code that sends orders.
4. Add pre-execution kill-switch contract/spec tests, still no MT5 order APIs.
5. Add dry-run reconciliation between intended-action rows and hypothetical order request shape, without MqlTradeRequest and without OrderCheck.

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

Expected:

On branch main
Your branch is up to date with origin/main
No tracked-file changes
Untracked reports/
Latest commit: 6d40e6a Document H024 replay WOULD_OPEN runtime result

Then continue from there.

Exact First Response The Next AI Should Give
Understood. Continuing from HANDOFF_78.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
- Branch should be main, pushed, tracked tree clean except local reports/.
- Latest commit should be 6d40e6a Document H024 replay WOULD_OPEN runtime result.
- Current full-test anchor is 898 passed.
- H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
- Runtime intended-action NO_ACTION rows were observed in real current log-only runtime.
- A strict --require-would-open gate now exists.
- The EA now has InpH024ClosedShift for log-only historical replay, defaulting to 1.
- Controlled historical replay passed the strict WOULD_OPEN gate with 37 WOULD_OPEN rows:
  - USDJPYm: 18 WOULD_OPEN
  - XAUUSDm: 19 WOULD_OPEN
- This proves the runtime WOULD_OPEN log path in historical log-only replay, not real-current-market signal occurrence.
- No order-send, no OrderCheck, no CTrade, no MqlTradeRequest, no execution adapter.
- reports/ stays untracked.
- H024 is still not demo deployable.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.