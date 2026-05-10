# HANDOFF_83 — H024 Risk-Fraction Comparison Mode, Optimized Threshold Scans, and Current Research Boundary

If any older handoff conflicts with this one, this handoff wins.

This continues from HANDOFF_82 but is intended to be fully self-contained. A new AI should be able to continue safely from this document without opening older handoffs first.

---

## 0. One-Sentence State

H024 remains a promising USDJPY + XAUUSD MT5 log-only EA candidate, but it is still research-only because at the actual intended 100 USD / 1% risk setting it has no executable broker-minimum-volume candidate, no executable runtime dry-run request exists, and no order-execution path is approved.

---

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current stage:

Execution-safety preparation after H024 research evidence.

Current status:

H024 is promising, but still:

- Not demo-approved
- Not live-approved
- Not Phase 4-approved
- Not approved for any order execution
- Not approved for any execution adapter
- Not approved for `OrderSend`, `OrderCheck`, `CTrade`, or `MqlTradeRequest`

The user is eager to deploy but accepts evidence gates. Be direct and do not soften deployment boundaries.

---

## 2. Human Preference

The user is tired of excessive ceremony.

Going forward:

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do one real action at a time.
- Do not create governance docs unless they preserve a real result, preserve a handoff, prevent ambiguity, or protect against future confusion.
- For docs-only edits, do not run full pytest unless there is a clear reason.
- For code edits, tests are mandatory.
- Avoid long real-data diagnostics casually.
- For real-data diagnostics, get explicit authorization or make a clear safety-bound decision.
- Never soften deployment boundaries because H024 is promising.

The user’s stated goal:

```text
make the EA survive the future, not fit the past

Important sentiment:

The user is eager to deploy. The correct direct answer is that H024 is serious, but still not demo deployable.

3. Environment

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

Terminal / MetaTrader environment:

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

Repo report CSVs are local and intentionally untracked:

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

4. Expected Repo State After This Handoff Is Committed

Expected:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        reports/

nothing added to commit but untracked files present

Expected latest commit after this handoff is committed:

Add handoff document #83

Current full-test anchor after post-HANDOFF_82 code changes:

944 passed in 19.53s

Focused scanner anchor after post-HANDOFF_82 code changes:

15 passed in 1.96s

If full tests drop below 944 without intentional test removal, treat as regression.

Docs-only commits after the 944 anchor do not require pytest.

5. Recent Commit History

Expected recent history before HANDOFF_83 commit:

6b4bb40 Document H024 risk fraction comparison mode result
f0413f2 Optimize H024 threshold comparison scans
b3cd189 Clean H024 threshold comparison whitespace
782eb16 Add H024 risk fraction threshold comparison mode
c225842 Expand handoff document #82
08c37a5 Add handoff document #82
0aafc4e Document H024 risk fraction threshold comparison
63d0573 Expand H024 capital threshold scan brackets
696f4c9 Document H024 100 USD feasibility boundary
6fccf96 Add handoff document #81
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

Important commits created after HANDOFF_82:

782eb16 Add H024 risk fraction threshold comparison mode
b3cd189 Clean H024 threshold comparison whitespace
f0413f2 Optimize H024 threshold comparison scans
6b4bb40 Document H024 risk fraction comparison mode result
6. Non-Negotiable Safety Boundary

H024 remains:

Research / pre-deployment only
No demo deployment approval
No live trading approval
No Phase 4 execution approval
No order-send capability approved
No execution adapter approved

Forbidden in the log-only EA and current project stage:

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

Also not approved:

EA chart attach/detach automation
GUI automation
MT5 launcher/profile mutation affecting live terminals
Order-send automation
Demo/live execution adapter
Raising risk to force executable candidates
Treating capital threshold scans as deployment approval

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
Pure Python risk-fraction threshold comparison
Optimized pure Python risk-fraction threshold comparison mode
Research-only documentation of threshold results
7. Current Deployment Verdict

H024 is not ready for demo or live.

Reason:

At the actual intended current setting:

Balance: 100 USD
Risk fraction: 1%

H024 has no executable historical candidate shifts.

The chain required for deployment is not complete:

runtime CSV -> executable dry-run request -> execution safety review -> demo adapter -> demo order-behavior evidence

At 100 USD / 1%, the chain stops at feasibility:

runtime CSV / historical signal rows -> BLOCKED below broker minimum volume -> no executable dry-run request

The blocker is economic / broker microstructure feasibility, not a known H024 signal-code malfunction.

8. H024 Mechanics Summary

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
9. H020 / H024 Sizing Boundary

H024 uses H020 sizing.

Important H020 behaviors:

Computes explicit pre-trade lot intents.
Suppresses flat signals.
Suppresses invalid stop geometry.
Suppresses stop distances below one spread.
Computes risk-based lots.
Applies per-trade gross notional caps.
Applies portfolio gross notional scaling.
Rounds lots down to broker lot step.
Suppresses lots below broker minimum lot.
Preserves final signed risk fraction from final executable lots.

Therefore, threshold scans must not bypass H020 sizing.

The optimized scanner introduced after HANDOFF_82 reuses H024 signal/stop geometry, but still routes each balance through H020 sizing. This is important: the optimization is a performance/tooling change, not a simplification of the execution feasibility logic.

10. Current EA Facts

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
BLOCKED signal rows preserve positive entry, stop, stop_distance, and raw_lots.
BLOCKED signal rows force final executable lots to 0.
Dry-run reconciler does not emit requests from BLOCKED rows.
11. Data Rules

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

DST-aware.

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
12. Core Files

H024 core:

quantcore\strategy\h024.py
quantcore\strategy\h024_runner.py

H020 sizing contract:

quantcore\strategy\h020.py
tests\test_h020.py

Position sizing reference:

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

Feasibility / threshold tests:

tests\test_h024_min_volume_feasibility.py
tests\test_h024_executable_candidate_shift_scan.py
tests\test_h024_capital_threshold_scan.py

Important operation docs:

docs\operations\H024_100USD_1PCT_FEASIBILITY_BOUNDARY.md
docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_MODE_RESULT.md
docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_RESULT.md
docs\operations\H024_EXACT_CAPITAL_THRESHOLD_RESULT.md
docs\operations\H024_CAPITAL_FEASIBILITY_FRONTIER_RESULT.md
docs\operations\H024_EXECUTABLE_CANDIDATE_SHIFT_SCAN_RESULT.md
docs\operations\H024_MIN_VOLUME_FEASIBILITY_RESULT.md
docs\operations\H024_BLOCKED_SIZING_DIAGNOSTICS_RUNTIME_RESULT.md
docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
docs\operations\H024_EA_WOULD_OPEN_SYNTHETIC_VALIDATION_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\handoffs\HANDOFF_82.md
docs\operations\handoffs\HANDOFF_83.md
13. Evidence Reality Before HANDOFF_83

Already true before this handoff:

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
EA derives entry/stop for signal rows.
EA converts under-min-volume signal rows into BLOCKED, not fake WOULD_OPEN.
BLOCKED signal rows preserve sizing diagnostics.
Runtime replay proved positive entry/stop/stop-distance/raw-lots are preserved on BLOCKED rows.
A reusable verifier exists for BLOCKED sizing diagnostics.
A regression test ensures positive BLOCKED diagnostics cannot become dry-run requests.
Minimum-volume feasibility is quantified.
A reusable executable candidate shift scanner exists.
At 100 USD / 1% risk, no historical H024 candidate survives sizing into an executable candidate.
A reusable exact capital threshold scanner exists.
At 1% risk, ANY / USDJPY first executable historical candidate appears at 245 USD.
At 1% risk, XAUUSD first executable historical candidate appears at 935 USD.
Risk-fraction comparison was manually measured across 0.50%, 0.75%, 1.00%, 1.50%, and 2.00%.
HANDOFF_82 was expanded and committed.
Previous full test anchor was 939 passed before post-HANDOFF_82 scanner changes.
14. What Changed Since HANDOFF_82
14.1 Added Risk-Fraction Threshold Comparison Mode

Commit:

782eb16 Add H024 risk fraction threshold comparison mode

Changed files:

scripts\scan_h024_capital_thresholds.py
tests\test_h024_capital_threshold_scan.py

Purpose:

Replace manual repeated risk-fraction threshold scan commands with one comparison-table command.

New command:

python scripts\scan_h024_capital_thresholds.py --risk-fractions 0.005,0.0075,0.01,0.015,0.02

New behavior:

Parses comma-separated risk fractions.
Builds a comparison table for ANY, USDJPY, and XAUUSD thresholds.
Preserves research-only disclaimer.
Does not approve higher risk, higher balance, demo/live, or execution.

Test result after feature implementation and cleanup:

11 passed

Full suite after feature implementation:

943 passed
14.2 Cleaned Threshold Comparison Whitespace

Commit:

b3cd189 Clean H024 threshold comparison whitespace

Purpose:

Remove EOF whitespace found by git diff --check.

Focused scanner tests after cleanup:

11 passed in 1.14s
14.3 Optimized H024 Threshold Comparison Scans

Commit:

f0413f2 Optimize H024 threshold comparison scans

Changed files:

scripts\scan_h024_capital_thresholds.py
scripts\scan_h024_executable_candidate_shifts.py
tests\test_h024_executable_candidate_shift_scan.py

Problem:

The initial comparison mode was correct but expensive. It could call scan_real_h4_exports() repeatedly for each balance probe, which reloaded broker-native H4 exports and reran the full H024 bridge.

Observed issue:

A first real comparison run was slow enough that it was manually interrupted during the real H4 scan.

Optimization added:

H024ExecutableCandidateScanInputs
build_h024_executable_candidate_scan_inputs(...)
scan_h024_candidate_inputs_for_executable_shifts(...)
build_real_h4_executable_candidate_provider(...)

Important safety detail:

The optimization does not bypass H020.

It reuses:

Broker-native H4 loads
Common H4 index
H024 signal panel
H024 stop geometry

But each balance still routes through:

generate_h020_intent_panel(...)
H020 risk-based lots
H020 per-trade notional caps
H020 portfolio scaling
Broker minimum-lot suppression semantics

Focused tests after optimization:

15 passed in 1.96s

Full suite after optimization:

944 passed in 19.53s
14.4 Verified One-Command Comparison Output

Command:

python scripts\scan_h024_capital_thresholds.py --risk-fractions 0.005,0.0075,0.01,0.015,0.02

Observed output:

H024 risk-fraction capital threshold comparison
========================================================================
Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.

Risk fraction    ANY threshold    USDJPY threshold    XAUUSD threshold
0.50%    490 USD    490 USD    1,870 USD
0.75%    327 USD    327 USD    1,247 USD
1.00%    245 USD    245 USD    935 USD
1.50%    164 USD    164 USD    624 USD
2.00%    123 USD    123 USD    468 USD

Verdict: PASS
Thresholds quantified only; no higher-risk, no higher-balance, no demo/live, and no execution approval implied.

Interpretation:

The optimized command produced the same known threshold table as prior manual repeated scans.

14.5 Documented Risk-Fraction Comparison Mode Result

Commit:

6b4bb40 Document H024 risk fraction comparison mode result

New doc:

docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_MODE_RESULT.md

Purpose:

Preserve the optimized scanner result, the new command, the observed threshold table, and the 944 full-test anchor.

Docs-only edit. No pytest run required after this doc commit.

15. Current Risk-Fraction Threshold Table

The current preserved threshold table is:

Risk fraction    ANY threshold    USDJPY threshold    XAUUSD threshold
0.50%            490 USD          490 USD             1,870 USD
0.75%            327 USD          327 USD             1,247 USD
1.00%            245 USD          245 USD             935 USD
1.50%            164 USD          164 USD             624 USD
2.00%            123 USD          123 USD             468 USD

Key interpretation:

At 100 USD, even 2% risk still does not make H024 mechanically executable.

The first ANY / USDJPY executable threshold at 2% risk is 123 USD.

Approximate implied minimum risk at 100 USD:

ANY / USDJPY: about 2.45%
XAUUSD:       about 9.35%

These are feasibility measurements only.

They do not approve raising risk.

16. Minimum-Volume Feasibility Result

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

Interpretation:

At 100 USD balance and 1% risk:

USDJPY is below broker minimum volume but close for that replay case.
XAUUSD is far below broker minimum volume for that replay case.
The observed blocker is economic / microstructure feasibility, not a code malfunction.
Raising risk to force execution is not approved.
17. Executable Candidate Shift Scan at Current Settings

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

Interpretation:

At the current 100 USD / 1% risk settings, no historical H024 H4 candidate survives sizing into an executable candidate.

18. Coarse Capital Feasibility Frontier

Balance sweep at fixed 1% risk:

100
120
250
550
1000
10000

Observed executable candidate counts:

Balance    Risk    Executable Candidates
100        1%      0
120        1%      0
250        1%      1
550        1%      215
1000       1%      595
10000      1%      1364

Symbol breakdown:

Balance    USDJPY    XAUUSD
100        0         0
120        0         0
250        1         0
550        215       0
1000       591       4
10000      669       695

Interpretation:

USDJPY becomes mechanically executable somewhere between 120 USD and 250 USD at 1% risk.
XAUUSD becomes mechanically executable somewhere between 550 USD and 1000 USD at 1% risk.
Current 100 USD / 1% risk has no executable path.
This is not approval to increase balance, increase risk, demo trade, or execute.
19. Exact Capital Threshold Result at 1% Risk

Exact thresholds at 1% risk:

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
20. Current Important Commands

Verify full suite:

python -m pytest -q

Expected current anchor:

944 passed

Run focused scanner tests:

python -m pytest tests\test_h024_executable_candidate_shift_scan.py tests\test_h024_capital_threshold_scan.py -q

Expected current anchor:

15 passed

Run exact capital threshold scan at 1% risk:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01

Expected thresholds:

ANY:    245 USD
USDJPY: 245 USD
XAUUSD: 935 USD

Run optimized risk-fraction comparison:

python scripts\scan_h024_capital_thresholds.py --risk-fractions 0.005,0.0075,0.01,0.015,0.02

Expected threshold table:

Risk fraction    ANY threshold    USDJPY threshold    XAUUSD threshold
0.50%            490 USD          490 USD             1,870 USD
0.75%            327 USD          327 USD             1,247 USD
1.00%            245 USD          245 USD             935 USD
1.50%            164 USD          164 USD             624 USD
2.00%            123 USD          123 USD             468 USD

Run executable candidate scan at current settings:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 20

Expected:

executable_candidate_rows: 0

Verify blocked sizing diagnostics runtime CSV:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

python scripts\summarize_h024_blocked_sizing_diagnostics.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

Verify blocked rows do not create dry-run requests:

python scripts\reconcile_h024_runtime_dry_run_requests.py `
  reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv `
  --require-request `
  --output-jsonl reports\h024_ea_log_only_replay_blocked_sizing_diagnostics_dry_run_requests.jsonl

Expected safe failure:

Verdict: FAIL
Dry-run requests: 0
Skipped non-request rows: 25
missing required dry-run execution request

This FAIL is expected and safe under --require-request.

21. Current Answer Key

If asked “are we ready to demo/live?”:

No.

If asked “are we officially Phase 4?”:

No.

If asked “did H024 signal path work?”:

Yes, in historical log-only replay.

If asked “did executable dry-run request reconstruction pass at current settings?”:

No. At the actual 100 USD / 1% risk setting, no executable candidate exists. Runtime signal rows are correctly BLOCKED below broker minimum volume.

If asked “did blocked sizing diagnostics pass?”:

Yes. Runtime replay proved BLOCKED signal rows preserve positive entry/stop/stop-distance/raw-lots while keeping executable lots at 0.

If asked “can BLOCKED rows become dry-run requests?”:

No. A regression test guards that BLOCKED rows with positive diagnostics still emit no dry-run requests.

If asked “what is the exact capital threshold at 1% risk?”:

ANY / USDJPY first executable: 245 USD
XAUUSD first executable:      935 USD

If asked “what changed in the scanner?”:

Two things:

It now auto-expands high thresholds instead of assuming the 1% bracket works for every risk fraction.
It now supports optimized one-command risk-fraction comparison mode that reuses H024 geometry while still routing balances through H020 sizing.

If asked “does higher risk fix 100 USD?”:

Not within approved boundaries. Even 2% risk still requires 123 USD for first ANY / USDJPY executable threshold. Approximate implied risk for ANY/USDJPY at 100 USD is about 2.45%, and XAUUSD about 9.35%. These are measurements only, not recommendations.

If asked “should we raise risk to force execution?”:

No.

If asked “does this approve execution adapter work?”:

No.

If asked “is the blocker code or microstructure?”:

The current blocker is economic / broker minimum-volume feasibility, not a known H024 strategy-code malfunction.

If asked “why optimize scanner instead of execution?”:

Because the next safe step was improving research tooling. Execution remains blocked until an executable runtime dry-run request exists and safety layers are separately implemented.

22. What Remains Missing

Critical missing evidence:

No real-current-market WOULD_OPEN runtime row has been observed.
No executable dry-run request has been reconstructed from runtime CSV at the actual current 100 USD / 1% risk setting.
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
23. Recommended Next Work

Best next technical step:

Do not add execution code.

Recommended safe next options:

Add a research-only feasibility table over balances at fixed risk using the optimized reusable H024 scan inputs.
Add a research-only symbol eligibility / stop-model feasibility diagnostic, but avoid overfitting.
Continue only with log-only runtime replay and CSV reconciliation.
Investigate whether alternative broker constraints, symbol eligibility, or stop model changes preserve 100 USD feasibility without raising risk.
If using larger demo balance for future research, keep execution gates blocked until runtime CSV produces an executable dry-run request and safety layers are separately implemented.
Keep HANDOFF documents self-contained when meaningful state changes occur.

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
Raising risk to force executable candidates
24. Immediate First Action For Next AI

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected after this handoff is committed:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Expected latest commit:

Add handoff document #83

Then continue from the actual repo state, not from assumptions.

25. Exact First Response The Next AI Should Give
Understood. Continuing from HANDOFF_83.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, pushed, tracked tree clean except local reports/.
Current full-test anchor is 944 passed.
Current focused scanner anchor is 15 passed.
H024 is promising but remains not demo-approved, not live-approved, and not Phase 4-approved.
No order-send, no OrderCheck, no CTrade, no MqlTradeRequest, no execution adapter.
Runtime replay proved BLOCKED signal rows preserve positive sizing diagnostics while executable lots remain 0.
Dry-run reconciler emits 0 requests from BLOCKED rows.
At current 100 USD / 1% risk, H024 has no executable historical candidate shifts.
At 1% risk, ANY/USDJPY first executable threshold is 245 USD.
At 1% risk, XAUUSD first executable threshold is 935 USD.
At 2% risk, ANY/USDJPY threshold is still 123 USD, so 100 USD remains mechanically non-executable even there.
The optimized --risk-fractions scanner mode exists and preserves H020 sizing semantics.
The blocker is economic / microstructure feasibility, not a code malfunction.
reports/ stays untracked.
H024 is still not demo deployable.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.

