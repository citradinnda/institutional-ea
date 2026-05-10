# HANDOFF_81 — H024 Capital Feasibility Boundary Quantified and Reproducible

If any older handoff conflicts with this one, this handoff wins. It continues from HANDOFF_80.

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
Your branch is up to date with 'origin/main'.
Tracked tree clean
Untracked: reports/
Latest commit: c3a85a8 Add H024 capital threshold scanner

Expected repo state after this handoff is committed:

On branch main
Your branch is up to date with 'origin/main'.
Tracked tree clean
Untracked: reports/
Latest commit: Add handoff document #81

Current full-test anchor:

937 passed in 17.90s

If tests drop below 937 without intentional test removal, treat as a regression.

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

The user is eager to deploy. The user accepts evidence gates. Be direct: H024 is serious, but still not demo deployable.

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
Pure Python minimum-volume feasibility summary
Pure Python executable candidate shift scanning
Pure Python exact capital threshold scanning
Current Latest Commits

Expected recent history before this handoff is committed:

c3a85a8 Add H024 capital threshold scanner
fb672f7 Document H024 exact capital threshold result
637d35a Document H024 capital feasibility frontier
e5c7b54 Document H024 executable candidate shift scan result
beabfb1 Add H024 executable candidate shift scanner
f2f7381 Document H024 minimum volume feasibility result
161904d Add H024 minimum volume feasibility summary
0365f0a Add handoff document #80
9d4e410 Guard H024 dry-run reconciliation against blocked requests
96ecf0f Add H024 blocked sizing diagnostics verifier

After this handoff is committed, latest commit should be:

Add handoff document #81
What Changed Since HANDOFF_80
1. Added minimum-volume feasibility summary

Commit:

161904d Add H024 minimum volume feasibility summary

New files:

scripts\summarize_h024_min_volume_feasibility.py
tests\test_h024_min_volume_feasibility.py

Purpose:

Quantify whether observed H024 runtime signal rows can reach broker minimum volume under a given balance and risk fraction.

This is pure Python and CSV-read-only.

No MT5 access.
No order execution.
No risk increase recommendation.

Focused tests:

4 passed

Full suite after this work:

929 passed
2. Ran feasibility summary against real runtime BLOCKED sizing replay

Input report:

reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

This report is local and intentionally untracked.

Command shape:

python scripts\summarize_h024_min_volume_feasibility.py `
  --csv reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv `
  --balance 100 `
  --risk-fraction 0.01

Observed deduped result:

USDJPY | BLOCKED | BELOW_MIN_VOLUME | observations=12 raw_lots=0.0083395062 min_volume=0.0100000000
  balance: 100.00
  risk_fraction: 0.010000
  current_risk_usd: 1.000000
  implied_loss_per_1_lot_usd: 119.911177
  minimum_risk_usd_for_min_volume: 1.199112
  minimum_balance_at_same_risk_fraction: 119.91
  minimum_risk_fraction_at_same_balance: 0.011991

XAUUSD | BLOCKED | BELOW_MIN_VOLUME | observations=13 raw_lots=0.0018247230 min_volume=0.0100000000
  balance: 100.00
  risk_fraction: 0.010000
  current_risk_usd: 1.000000
  implied_loss_per_1_lot_usd: 548.028386
  minimum_risk_usd_for_min_volume: 5.480284
  minimum_balance_at_same_risk_fraction: 548.03
  minimum_risk_fraction_at_same_balance: 0.054803

Verdict: PASS
Feasibility quantified only; no risk increase or execution approval implied.

Interpretation:

At 100 USD balance and 1 percent risk:

USDJPY is below broker minimum volume but close.
XAUUSD is far below broker minimum volume.
The observed blocker is economic / microstructure feasibility, not a code malfunction.
Raising risk to force execution is not approved.
3. Documented minimum-volume feasibility result

Commit:

f2f7381 Document H024 minimum volume feasibility result

New doc:

docs\operations\H024_MIN_VOLUME_FEASIBILITY_RESULT.md

Purpose:

Preserve the feasibility result from the BLOCKED runtime replay.

4. Added executable candidate shift scanner

Commit:

beabfb1 Add H024 executable candidate shift scanner

New files:

scripts\scan_h024_executable_candidate_shifts.py
tests\test_h024_executable_candidate_shift_scan.py

Purpose:

Find whether any historical H024 H4 decision row survives H024 signal logic plus H020 sizing into an executable candidate at a given balance and risk fraction.

Important scope:

Pure Python
Broker-native H4 CSV-read-only
No MT5 access
No M1 accepted-window validation
No order execution
Intended only to locate replay-planning shifts

Focused tests:

3 passed

Full suite after this work:

932 passed
5. Scanned executable candidates at 100 USD / 1 percent risk

Command shape:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 20

Observed:

balance: 100.00
risk_fraction: 0.010000
executable_candidate_rows: 0
wrote: reports\h024_executable_candidate_shifts_100usd_1pct.csv

Verdict: PASS
Scan completed; no executable candidate shifts found at these settings.

Interpretation:

At the current 100 USD / 1 percent risk settings, no historical H024 H4 candidate survives sizing into an executable candidate.

6. Documented executable candidate shift scan result

Commit:

e5c7b54 Document H024 executable candidate shift scan result

New doc:

docs\operations\H024_EXECUTABLE_CANDIDATE_SHIFT_SCAN_RESULT.md

Purpose:

Preserve the result that no executable candidate exists at 100 USD / 1 percent risk.

7. Scanned capital feasibility frontier

A balance sweep was run at fixed 1 percent risk:

100
120
250
550
1000
10000

Observed executable candidate counts:

Balance  Risk  Executable Candidates
100      1%    0
120      1%    0
250      1%    1
550      1%    215
1000     1%    595
10000    1%    1364

Symbol breakdown:

Balance  USDJPY  XAUUSD
100      0       0
120      0       0
250      1       0
550      215     0
1000     591     4
10000    669     695

Interpretation:

USDJPY becomes mechanically executable somewhere between 120 USD and 250 USD at 1 percent risk.
XAUUSD becomes mechanically executable somewhere between 550 USD and 1000 USD at 1 percent risk.
Current 100 USD / 1 percent risk has no executable path.
This is not approval to increase balance, increase risk, demo trade, or execute.
8. Documented capital feasibility frontier

Commit:

637d35a Document H024 capital feasibility frontier

New doc:

docs\operations\H024_CAPITAL_FEASIBILITY_FRONTIER_RESULT.md

Purpose:

Preserve the coarse balance frontier.

9. Ran exact capital threshold scan

An ad-hoc exact-threshold scan was run using the existing executable candidate scanner logic.

Observed exact thresholds at 1 percent risk:

ANY executable H024 candidate: 245 USD
USDJPY first executable:       245 USD
XAUUSD first executable:       935 USD

Boundary checks:

balance=244: total=0 USDJPY=0 XAUUSD=0
balance=245: total=1 USDJPY=1 XAUUSD=0

balance=934: total=568 USDJPY=568 XAUUSD=0
balance=935: total=569 USDJPY=568 XAUUSD=1

First USDJPY / ANY candidate:

symbol: USDJPY
side: sell
decision_time: 2021-07-17T21:00:00+00:00
entry_time: 2021-07-18T17:00:00+00:00
ea_closed_shift_from_latest_common_h4: 7697
final_signed_risk_fraction: -0.009982289447
entry_price: 110.0150000000
stop_price: 110.2840593855
stop_distance: 0.2690593855

First XAUUSD candidate:

symbol: XAUUSD
side: sell
decision_time: 2023-09-25T21:00:00+00:00
entry_time: 2023-09-26T01:00:00+00:00
ea_closed_shift_from_latest_common_h4: 4184
final_signed_risk_fraction: -0.009997846715
entry_price: 1913.5900000000
stop_price: 1922.9379866787
stop_distance: 9.3479866787
10. Documented exact capital threshold result

Commit:

fb672f7 Document H024 exact capital threshold result

New doc:

docs\operations\H024_EXACT_CAPITAL_THRESHOLD_RESULT.md

Purpose:

Preserve exact balance thresholds.

11. Added reusable capital threshold scanner

Commit:

c3a85a8 Add H024 capital threshold scanner

New files:

scripts\scan_h024_capital_thresholds.py
tests\test_h024_capital_threshold_scan.py

Purpose:

Turn the ad-hoc exact threshold scan into a reusable script with tests.

Command:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01

Observed:

H024 exact capital threshold scan
========================================================================
Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.

ANY threshold balance: 245 USD at 1.00% risk
  total_candidates: 1
  USDJPY: 1
  XAUUSD: 0
  first_matching_candidate: USDJPY sell decision=2021-07-17T21:00:00+00:00 entry=2021-07-18T17:00:00+00:00 shift=7697 final_risk=-0.009982289447 entry_price=110.0150000000 stop_price=110.2840593855 stop_distance=0.2690593855

USDJPY threshold balance: 245 USD at 1.00% risk
  total_candidates: 1
  USDJPY: 1
  XAUUSD: 0
  first_matching_candidate: USDJPY sell decision=2021-07-17T21:00:00+00:00 entry=2021-07-18T17:00:00+00:00 shift=7697 final_risk=-0.009982289447 entry_price=110.0150000000 stop_price=110.2840593855 stop_distance=0.2690593855

XAUUSD threshold balance: 935 USD at 1.00% risk
  total_candidates: 569
  USDJPY: 568
  XAUUSD: 1
  first_matching_candidate: XAUUSD sell decision=2023-09-25T21:00:00+00:00 entry=2023-09-26T01:00:00+00:00 shift=4184 final_risk=-0.009997846715 entry_price=1913.5900000000 stop_price=1922.9379866787 stop_distance=9.3479866787

Boundary checks:
  ANY balance=244: matching=0 total=0 USDJPY=0 XAUUSD=0
  ANY balance=245: matching=1 total=1 USDJPY=1 XAUUSD=0
  USDJPY balance=244: matching=0 total=0 USDJPY=0 XAUUSD=0
  USDJPY balance=245: matching=1 total=1 USDJPY=1 XAUUSD=0
  XAUUSD balance=934: matching=0 total=568 USDJPY=568 XAUUSD=0
  XAUUSD balance=935: matching=1 total=569 USDJPY=568 XAUUSD=1

Verdict: PASS
Thresholds quantified only; no higher-balance approval or execution approval implied.

Focused tests:

5 passed

Full suite after this work:

937 passed in 17.90s
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
Runtime CSV to dry-run request reconciler exists and is CSV-read-only.
Reconciler correctly rejects non-executable rows.
EA now derives entry/stop for signal rows.
EA now converts under-min-volume signal rows into BLOCKED, not fake WOULD_OPEN.
BLOCKED signal rows now preserve sizing diagnostics.
A runtime replay proved positive entry/stop/stop-distance/raw-lots are preserved on BLOCKED rows.
A reusable verifier exists for BLOCKED sizing diagnostics.
A regression test ensures positive BLOCKED diagnostics cannot become dry-run requests.
Minimum-volume feasibility is quantified.
At 100 USD / 1 percent risk, USDJPY blocked replay rows require about 119.91 USD balance for that specific replay case.
At 100 USD / 1 percent risk, XAUUSD blocked replay rows require about 548.03 USD balance for that specific replay case.
A reusable executable candidate shift scanner exists.
At 100 USD / 1 percent risk, no historical H024 candidate survives sizing into an executable candidate.
A reusable exact capital threshold scanner exists.
At 1 percent risk, ANY / USDJPY first executable historical candidate appears at 245 USD.
At 1 percent risk, XAUUSD first executable historical candidate appears at 935 USD.
Current full test anchor is 937 passed.

What remains missing:

No real-current-market WOULD_OPEN runtime row has been observed.
No executable dry-run request has been reconstructed from runtime CSV at the actual current 100 USD / 1 percent risk setting.
Current replay signal rows are blocked by broker minimum volume.
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
Answer Key for Common Questions

If asked “are we ready to demo/live?”:

No.

If asked “did H024 signal path work?”:

Yes, in historical log-only replay.

If asked “did executable dry-run request reconstruction pass at current settings?”:

No. At the actual 100 USD / 1 percent risk setting, no executable candidate exists. Runtime signal rows are correctly BLOCKED below broker minimum volume.

If asked “did blocked sizing diagnostics pass?”:

Yes. Runtime replay proved BLOCKED signal rows preserve positive entry/stop/stop-distance/raw-lots while keeping executable lots at 0.

If asked “can BLOCKED rows become dry-run requests?”:

No. A regression test guards that BLOCKED rows with positive diagnostics still emit no dry-run requests.

If asked “what is the exact capital threshold at 1 percent risk?”:

ANY / USDJPY first executable: 245 USD.
XAUUSD first executable: 935 USD.

If asked “does that mean we should raise the account balance or risk?”:

No. The threshold scan quantifies feasibility only. It does not recommend increasing balance or risk and does not approve demo/live/Phase 4.
Current Important Commands

Verify full suite:

python -m pytest -q

Expected current anchor:

937 passed

Run minimum-volume feasibility summary against blocked runtime CSV:

python scripts\summarize_h024_min_volume_feasibility.py `
  --csv reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv `
  --balance 100 `
  --risk-fraction 0.01

Run executable candidate scan at current settings:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 20

Expected at current settings:

executable_candidate_rows: 0

Run exact capital threshold scan:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01

Expected thresholds:

ANY: 245 USD
USDJPY: 245 USD
XAUUSD: 935 USD

Verify blocked sizing diagnostics runtime CSV:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

python scripts\summarize_h024_blocked_sizing_diagnostics.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

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

This FAIL is expected and safe under --require-request.

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

Repo report CSVs are local and untracked:

reports\h024_ea_log_only_preflight.csv
reports\h024_ea_log_only_replay_would_open.csv
reports\h024_ea_log_only_replay_would_open_prices.csv
reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv
reports\h024_ea_log_only_replay_blocked_sizing_diagnostics_dry_run_requests.jsonl
reports\h024_executable_candidate_shifts_100usd_1pct.csv
reports\h024_executable_candidate_shifts_120usd_1pct.csv
reports\h024_executable_candidate_shifts_250usd_1pct.csv
reports\h024_executable_candidate_shifts_550usd_1pct.csv
reports\h024_executable_candidate_shifts_1000usd_1pct.csv
reports\h024_executable_candidate_shifts_10000usd_1pct.csv

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

Important current input:

InpH024ClosedShift = 1

Meaning:

Defaults to latest closed H4 bar.
Set manually for historical replay only.
Do not automate chart attach/detach.

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
quantcore\execution\h024_dry_run.py
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

Feasibility / capital threshold tools:

scripts\summarize_h024_min_volume_feasibility.py
scripts\scan_h024_executable_candidate_shifts.py
scripts\scan_h024_capital_thresholds.py

tests\test_h024_min_volume_feasibility.py
tests\test_h024_executable_candidate_shift_scan.py
tests\test_h024_capital_threshold_scan.py

Important docs:

docs\operations\H024_MIN_VOLUME_FEASIBILITY_RESULT.md
docs\operations\H024_EXECUTABLE_CANDIDATE_SHIFT_SCAN_RESULT.md
docs\operations\H024_CAPITAL_FEASIBILITY_FRONTIER_RESULT.md
docs\operations\H024_EXACT_CAPITAL_THRESHOLD_RESULT.md
docs\operations\H024_BLOCKED_SIZING_DIAGNOSTICS_RUNTIME_RESULT.md
docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
docs\operations\H024_EA_WOULD_OPEN_SYNTHETIC_VALIDATION_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\handoffs\HANDOFF_80.md
docs\operations\handoffs\HANDOFF_81.md
Recommended Next Work

Best next technical step:

Decide whether to keep H024 as:

A strategy that requires a larger account-size feasibility threshold before demo consideration.
A research candidate needing sizing/stop/symbol policy revision.
A strategy that remains pre-deployment because current 100 USD / 1 percent risk cannot produce executable dry-run requests.

Safe next work options:

Add a short policy note that H024 is infeasible at 100 USD / 1 percent risk under current broker min volume.
Add a parameterized report comparing thresholds at fixed risk fractions without recommending higher risk.
Investigate whether stop model or symbol eligibility should be revised at research level.
Continue only with log-only runtime replay and CSV reconciliation.
If using a larger demo balance for future research, still keep all execution gates blocked until runtime CSV produces an executable dry-run request and safety layers are separately implemented.

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
Raising risk to force an executable candidate
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
Latest commit: Add handoff document #81

Then continue from the actual repo state.

Exact First Response The Next AI Should Give
Understood. Continuing from HANDOFF_81.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, pushed, tracked tree clean except local reports/.
Current full-test anchor is 937 passed.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
No order-send, no OrderCheck, no CTrade, no MqlTradeRequest, no execution adapter.
Runtime replay proved BLOCKED signal rows preserve positive sizing diagnostics while executable lots remain 0.
Dry-run reconciler emits 0 requests from BLOCKED rows.
At current 100 USD / 1 percent risk, H024 has no executable historical candidate shifts.
At 1 percent risk, ANY/USDJPY first executable threshold is 245 USD.
At 1 percent risk, XAUUSD first executable threshold is 935 USD.
The blocker is economic / microstructure feasibility, not a code malfunction.
reports/ stays untracked.
H024 is still not demo deployable.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.

