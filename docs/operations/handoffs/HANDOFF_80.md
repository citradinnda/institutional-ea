# HANDOFF_80 — H024 Blocked Sizing Diagnostics Gate Preserved and Reconciler Guarded

If any older handoff conflicts with this one, this handoff wins. It continues from HANDOFF_79.

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

Expected repo state after this handoff is committed:

On branch main
Your branch is up to date with 'origin/main'.
Tracked tree clean
Untracked: reports/
Latest commit: Add handoff document #80

Current full-test anchor:

925 passed in 17.83s

If tests drop below 925 without intentional test removal, treat as a regression.

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
Runtime BLOCKED sizing diagnostics verification
Current Latest Commits

Expected recent history after this handoff is committed:

<new> Add handoff document #80
9d4e410 Guard H024 dry-run reconciliation against blocked requests
96ecf0f Add H024 blocked sizing diagnostics verifier
a16dcdf Document H024 blocked sizing diagnostics runtime result
4652abd Add handoff document #79
bf5f420 Preserve H024 blocked sizing diagnostics
3874c01 Update H024 closed-shift static expectation
fe8abd1 Populate H024 runtime intended-action prices
6f49ff4 Add H024 runtime dry-run reconciliation
d1d0956 Add H024 dry-run execution request contract
What Changed Since HANDOFF_79
1. Verified repo state after HANDOFF_79

Observed:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
        reports/

nothing added to commit but untracked files present

Latest commit at the time:

4652abd Add handoff document #79

This matched the expected HANDOFF_79 starting point.

2. Re-ran historical replay after blocked sizing diagnostics patch

The next HANDOFF_79 gate was:

Prove that after commit bf5f420 Preserve H024 blocked sizing diagnostics, runtime BLOCKED signal rows preserve positive sizing diagnostics instead of zeroing them out.

Manual MT5 replay settings:

USDJPYm  InpH024ClosedShift = 16
XAUUSDm  InpH024ClosedShift = 18

The EA was manually attached and removed. No chart automation was used.

Collected report:

reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

This report is local and intentionally untracked.

Compile / collect helper output:

H024 MT5 log-only EA local preflight helper
========================================================================
Research only. No demo/live/Phase 4 approval.
No EA attachment automation. No order-send capability.

Copied EA source to: C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5
MetaEditor compile return code: 1
EX5 path: C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.
Collected runtime CSV to: reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
Rows: 156
Violations: 0

Verdict: PASS

Interpretation:

The nonzero MetaEditor return code is still accepted only because the EX5 was refreshed. This is existing local behavior. It does not imply execution approval.

3. Runtime preflight verification passed

Command:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

Observed:

H024 log-only EA runtime preflight verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Rows: 156
Violations: 0

Verdict: PASS
4. Intended-action runtime summary passed with BLOCKED rows

Command:

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

Observed:

H024 intended-action runtime summary
========================================================================
Research only. No demo/live/Phase 4 approval.

CSV: reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
Total rows: 156
Intended-action header rows: 2
Intended-action data rows: 25

USDJPYm:
  headers: 1
  rows: 12
  normalized: USDJPY
  WOULD_OPEN: 0
  BLOCKED: 12
  NO_ACTION: 0

XAUUSDm:
  headers: 1
  rows: 13
  normalized: XAUUSD
  WOULD_OPEN: 0
  BLOCKED: 13
  NO_ACTION: 0

Verdict: PASS

Interpretation:

Signal rows were observed, but they correctly stayed BLOCKED because computed volume was below broker minimum.

5. Verified BLOCKED rows preserve positive sizing diagnostics

An ad-hoc line-by-line mixed-schema CSV parser was used because the runtime CSV contains mixed row shapes.

Reason Pandas failed:

pandas.errors.ParserError: Error tokenizing data. C error: Expected 32 fields in line 8, saw 54

The mixed runtime CSV contains both base preflight rows and longer intended-action rows.

Correct diagnostic result:

H024 blocked sizing diagnostics check
========================================================================
CSV: reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
Physical CSV rows: 157
Row length histogram: {32: 130, 54: 27}
Intended-action header rows found: 2
Intended-action data rows found: 25
BLOCKED rows checked: 25

USDJPYm USDJPY | BLOCKED | entry=155.821 stop=158.163 dist=2.342 raw_lots=0.0083395062 lots=0.0 min_volume=0.01 | BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short;closed_h4_time=2026.05.06 04:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

XAUUSDm XAUUSD | BLOCKED | entry=4593.801 stop=4525.492 dist=68.309 raw_lots=0.001824723 lots=0.0 min_volume=0.01 | BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=long;closed_h4_time=2026.05.05 20:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

Verdict: PASS
BLOCKED signal rows preserved positive entry/stop/stop-distance/raw-lots diagnostics while keeping executable lots at 0.

Key evidence:

USDJPY raw_lots=0.0083395062 < min_volume=0.01
XAUUSD raw_lots=0.001824723 < min_volume=0.01
lots=0.0

Interpretation:

The gate passed.

The EA observed signal rows, derived entry/stop/stop-distance/raw-lots, preserved those diagnostics, and kept final executable lots at 0 because broker minimum volume blocked execution.

6. Dry-run reconciler correctly produced zero requests from BLOCKED rows

Command:

python scripts\reconcile_h024_runtime_dry_run_requests.py `
  reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv `
  --require-request `
  --output-jsonl reports\h024_ea_log_only_replay_blocked_sizing_diagnostics_dry_run_requests.jsonl

Observed:

H024 dry-run execution request reconciliation
========================================================================
Research only. No demo/live/Phase 4 approval.
CSV read only. No MT5 access. No order execution.

CSV: reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
Rows: 156
Intended-action rows: 25
WOULD_OPEN rows: 0
Dry-run requests: 0
Skipped non-request rows: 25

Violations:
- missing required dry-run execution request

Verdict: FAIL

Interpretation:

This FAIL is the correct safety behavior under --require-request.

It proves:

WOULD_OPEN rows: 0
Dry-run requests: 0
Skipped non-request rows: 25

The reconciler did not create requests from BLOCKED rows, even though the rows contained positive entry/stop/raw-lots diagnostics.

7. Preserved the blocked sizing diagnostics runtime result

Commit:

a16dcdf Document H024 blocked sizing diagnostics runtime result

New doc:

docs\operations\H024_BLOCKED_SIZING_DIAGNOSTICS_RUNTIME_RESULT.md

Purpose:

Preserves the post-bf5f420 runtime replay gate proving that H024 BLOCKED signal rows preserve sizing diagnostics while remaining non-executable.

Important preserved conclusion:

Signal rows were observed.
Runtime entry/stop derivation worked.
Stop distance was positive.
Raw lots were positive.
Raw lots were below broker minimum volume.
Final executable lots remained 0.
Rows correctly remained BLOCKED.
Dry-run reconciler emitted 0 execution requests.
8. Added reusable blocked sizing diagnostics verifier

Commit:

96ecf0f Add H024 blocked sizing diagnostics verifier

New files:

scripts\summarize_h024_blocked_sizing_diagnostics.py
tests\test_h024_blocked_sizing_diagnostics_summary.py

Purpose:

Turn the ad-hoc mixed-schema BLOCKED sizing diagnostics parser into a reusable verifier.

Focused tests:

3 passed in 1.38s

Runtime CSV verification output:

H024 blocked sizing diagnostics verification
========================================================================
Research only. No demo/live/Phase 4 approval.

CSV: reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
Row length histogram: {32: 130, 54: 27}
Intended-action header rows found: 2
Intended-action data rows found: 25
BLOCKED rows checked: 25

USDJPYm USDJPY | BLOCKED | entry=155.8210000000 stop=158.1630000000 dist=2.3420000000 raw_lots=0.0083395062 lots=0.0000000000 min_volume=0.0100000000 | BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short;closed_h4_time=2026.05.06 04:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

XAUUSDm XAUUSD | BLOCKED | entry=4593.8010000000 stop=4525.4920000000 dist=68.3090000000 raw_lots=0.0018247230 lots=0.0000000000 min_volume=0.0100000000 | BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=long;closed_h4_time=2026.05.05 20:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

Verdict: PASS
BLOCKED rows preserve positive entry/stop/stop-distance/raw-lots diagnostics while keeping executable lots at 0.

Full suite after this:

924 passed in 19.95s
9. Added dry-run reconciler regression guard against BLOCKED requests

Commit:

9d4e410 Guard H024 dry-run reconciliation against blocked requests

Modified file:

tests\test_h024_runtime_dry_run_reconciliation.py

Added focused test:

test_blocked_rows_with_positive_sizing_diagnostics_do_not_emit_dry_run_requests

Purpose:

Guarantees that BLOCKED rows with positive entry/stop/raw_lots and lots=0 do not become dry-run execution requests.

Focused test result:

7 passed in 0.55s

Full suite after this:

925 passed in 17.83s

Current repo state after this commit:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
        reports/

nothing added to commit but untracked files present
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
BLOCKED signal rows now preserve sizing diagnostics.
A runtime replay proved positive entry/stop/stop-distance/raw-lots are preserved on BLOCKED rows.
A reusable verifier exists for BLOCKED sizing diagnostics.
A regression test ensures positive BLOCKED diagnostics cannot become dry-run requests.
Full test anchor is now 925 passed.

What remains missing:

No real-current-market WOULD_OPEN runtime row has been observed.
No executable dry-run request has been reconstructed from runtime CSV yet.
Current replay signal rows are blocked by broker min volume at current account/risk.
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

Answer if asked “did blocked sizing diagnostics pass?”:

Yes. The latest replay proved BLOCKED signal rows preserve positive entry/stop/stop-distance/raw-lots while keeping executable lots at 0.

Answer if asked “can BLOCKED rows become dry-run requests?”:

No. A regression test now guards that BLOCKED rows with positive diagnostics still emit no dry-run requests.
Current Important Commands

Verify full suite:

python -m pytest -q

Expected current anchor:

925 passed

Verify current runtime blocked sizing diagnostics CSV:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

python scripts\summarize_h024_blocked_sizing_diagnostics.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

Expected:

Preflight verifier: PASS
Intended-action summary: PASS with BLOCKED rows
Blocked sizing diagnostics verifier: PASS

Verify blocked rows do not create dry-run requests:

python scripts\reconcile_h024_runtime_dry_run_requests.py `
  reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv `
  --require-request `
  --output-jsonl reports\h024_ea_log_only_replay_blocked_sizing_diagnostics_dry_run_requests.jsonl

Expected:

Verdict: FAIL
Dry-run requests: 0
Skipped non-request rows: 25
missing required dry-run execution request

This is expected and safe.

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

Collect to blocked diagnostics report path:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --collect `
  --report-path reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
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
reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
reports\h024_ea_log_only_replay_blocked_sizing_diagnostics_dry_run_requests.jsonl

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
BLOCKED signal rows preserve positive entry/stop/stop_distance/raw_lots but final lots = 0.
Dry-run reconciler does not emit requests from BLOCKED rows.
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
scripts\summarize_h024_blocked_sizing_diagnostics.py

Important tests:

tests\test_h024_blocked_sizing_diagnostics_summary.py
tests\test_h024_runtime_dry_run_reconciliation.py
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

docs\operations\H024_BLOCKED_SIZING_DIAGNOSTICS_RUNTIME_RESULT.md
docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
docs\operations\H024_EA_WOULD_OPEN_SYNTHETIC_VALIDATION_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\handoffs\HANDOFF_79.md
docs\operations\handoffs\HANDOFF_80.md
Recommended Next Work

Best next technical step:

Add a small, explicit feasibility review around H024 sizing versus broker minimum volume, without changing execution risk.

The observed blocker is not code malfunction. It is economic/microstructure feasibility:

At current balance and 1% risk:
USDJPY raw lots are close but below min volume.
XAUUSD raw lots are far below min volume.

Do not casually raise risk to force execution.

Useful safe next steps:

Add a pure Python script/test to compute minimum feasible balance/risk fraction for candidate signals.
Preserve a short doc explaining min-volume feasibility constraints.
Investigate whether the stop model, account sizing policy, or symbol eligibility should be revised at research level.
Keep dry-run/execution gates blocked until an actual executable request is reconstructed safely.

Possible command direction:

Create something like:

scripts\summarize_h024_min_volume_feasibility.py
tests\test_h024_min_volume_feasibility.py

It should be pure Python and should not touch MT5.

Inputs could be a runtime CSV or explicit values:

balance
risk_fraction
raw_lots
min_volume
stop_distance_price
loss_per_1_lot_usd

Outputs:

minimum risk USD for min volume
minimum balance at same risk fraction
minimum risk fraction at same balance
feasibility verdict

The script should not recommend raising risk. It should only quantify feasibility.

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
Latest commit: Add handoff document #80

Then continue from the actual repo state.

Exact First Response The Next AI Should Give
Understood. Continuing from HANDOFF_80.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, pushed, tracked tree clean except local reports/.
Current full-test anchor is 925 passed.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
No order-send, no OrderCheck, no CTrade, no MqlTradeRequest, no execution adapter.
Historical replay proved the runtime WOULD_OPEN log path earlier.
Runtime intended-action rows now derive entry/stop from closed H4 price and ATR stop.
Latest replay produced BLOCKED rows because computed volume was below broker min volume.
Blocked rows preserve positive entry/stop/stop-distance/raw-lots while executable lots remain 0.
Dry-run reconciler emits 0 requests from BLOCKED rows.
A regression test guards that positive BLOCKED diagnostics cannot become dry-run requests.
Full suite anchor is 925 passed.
reports/ stays untracked.
H024 is still not demo deployable.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.

