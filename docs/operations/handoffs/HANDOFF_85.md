# HANDOFF_85 — H024 Cent-Symbol Runtime Validation Gate Unblocked

If any older handoff conflicts with this one, this handoff wins.

This continues from HANDOFF_84 and is intended to be fully self-contained. A new AI should be able to continue safely from this document without opening older handoffs first.

---

## 0. One-Sentence State

H024 remains research-only and not deployment-approved, but the Exness Standard Cent path is now one gate further: cent-account symbol validation support for `USDJPYc` / `XAUUSDc` has been added, committed, pushed, and tested with `952 passed`; the next safe gate is manual cent-symbol log-only runtime/replay and CSV verification, still with no execution code.

---

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current stage:

Execution-safety preparation after H024 research evidence, now focused on the user's Exness Standard Cent account route.

Current status:

H024 is promising, but still:

- Not demo-approved
- Not live-approved
- Not Phase 4-approved
- Not approved for any order execution
- Not approved for any execution adapter
- Not approved for `OrderSend`, `OrderCheck`, `CTrade`, or `MqlTradeRequest`

The user is eager to deploy and plans to start with `10k USC` on an Exness Standard Cent account.

Do not soften deployment boundaries.

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

Important sentiment:

The user wants to make the EA survive the future, not fit the past.

The user is eager to deploy. The correct direct answer is:

H024 is meaningfully closer under the 10k USC cent-account route, but it is still not demo/live/Phase 4 deployable.

---

## 3. Environment

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

Repo report CSVs are local and intentionally untracked.

Do not commit reports/.

4. Expected Repo State After This Handoff Is Committed

Expected:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Expected latest commit after this handoff is committed:

Add handoff document #85

Expected latest commit before HANDOFF_85 commit:

6a8e017 Fix H024 cent preflight helper CLI path

Current full-test anchor after cent-symbol runtime validation and helper CLI repair:

952 passed in 16.78s

Focused cent/local-helper anchor:

20 passed in 0.67s

Diff check anchor:

git diff --check
# clean / no output
5. Recent Commit History

Expected recent history before HANDOFF_85 commit:

6a8e017 Fix H024 cent preflight helper CLI path
26d6393 Add H024 cent symbol runtime validation support
eb4aa84 Add handoff document #84
b446ed9 Add H024 cent account executable scan specs
cd3c153 Document H024 cent account feasibility probe
a2665ea Document H024 executable density thresholds
dbfca1f Expand H024 balance density symbol breakdown
011d3fc Document H024 balance executable candidate density
d1c0a63 Add handoff document #83
6b4bb40 Document H024 risk fraction comparison mode result
f0413f2 Optimize H024 threshold comparison scans

Important commits created after HANDOFF_84:

26d6393 Add H024 cent symbol runtime validation support
6a8e017 Fix H024 cent preflight helper CLI path
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
Treating feasibility scans as deployment approval

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
Read-only MT5 account/symbol-info probes
Read-only MT5 order_calc_profit probes
Pure Python cent-account USC feasibility scanner support
Cent-symbol runtime CSV verifier/summarizer support
Cent-symbol local runtime target preflight
7. Current Deployment Verdict

H024 is still not approved for demo or live.

However, the deployment-relevant feasibility universe changed.

Before HANDOFF_84, the important result was:

At 100 USD / 1% risk on standard-like USDJPYm / XAUUSDm symbols, H024 had no executable historical candidate.

After HANDOFF_84, the user clarified they plan to start with:

10,000 USC

on an Exness Standard Cent account.

The real terminal account probe showed:

Account currency: USC
Available symbols: USDJPYc, XAUUSDc
Unavailable symbols: USDJPYm, XAUUSDm, USDJPY, XAUUSD
Balance at probe time: 0.0 USC

This means prior standard-symbol scans are not the final deployment authority for the cent account.

Current best answer:

The 10k USC cent-account path is mechanically plausible by size, and cent-symbol validation tooling is now in place, but this does not approve deployment.

The blocker has changed from:

minimum volume impossible at 100 USD standard-symbol sizing

to:

need cent-symbol log-only runtime/replay, executable runtime dry-run request reconstruction, and execution-safety review
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

Therefore, cent-account scans must not bypass H020 sizing.

The cent scanner support reuses H024 signal/stop geometry, but routes balances through H020 sizing using alternate InstrumentSpec values.

This is important:

The cent support is a performance/research-accounting change, not execution approval.

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

Cent-account runtime has not yet been fully replayed/log-validated.

11. Data Rules

Accepted validation source:

Exness demo/terminal broker-native exports only

Accepted model symbols:

USDJPY
XAUUSD

Previously observed standard symbols:

USDJPYm
XAUUSDm

Current cent account symbols:

USDJPYc
XAUUSDc

Normalize for model logic:

USDJPYc -> USDJPY
XAUUSDc -> XAUUSD
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

Cent-account scanner support:

scripts\scan_h024_executable_candidate_shifts.py
tests\test_h024_cent_account_specs.py

Cent-symbol runtime validation support:

scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\run_h024_mt5_log_only_preflight_local.py
tests\test_h024_cent_symbol_runtime_validation.py
tests\test_h024_mt5_log_only_preflight_local_helper.py

Important operation docs:

docs\operations\H024_CENT_ACCOUNT_SYMBOL_FEASIBILITY_PROBE_RESULT.md
docs\operations\H024_BALANCE_EXECUTABLE_CANDIDATE_DENSITY_RESULT.md
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
docs\operations\handoffs\HANDOFF_83.md
docs\operations\handoffs\HANDOFF_84.md
docs\operations\handoffs\HANDOFF_85.md
13. Evidence Reality Before HANDOFF_85

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
At 100 USD / 1% risk on standard-like m specs, no historical H024 candidate survives sizing into an executable candidate.
A reusable exact capital threshold scanner exists.
At 1% risk on standard-like specs, ANY / USDJPY first executable historical candidate appears at 245 USD.
At 1% risk on standard-like specs, XAUUSD first executable historical candidate appears at 935 USD.
Optimized risk-fraction threshold comparison exists.
HANDOFF_84 was committed.
Read-only MT5 account/symbol probes showed the real account is USC cent and exposes USDJPYc / XAUUSDc.
Read-only MT5 order_calc_profit probes showed representative USDJPYc and XAUUSDc candidates executable by size at 10000 USC / 1%.
Pure-Python cent-account scanner support exists.
At 10000 USC / 1% with cent-account USC specs, scanner found 1364 executable historical candidates.
14. What Changed Since HANDOFF_84
14.1 Added Cent-Symbol Runtime Validation Support

Commit:

26d6393 Add H024 cent symbol runtime validation support

Changed files:

scripts\run_h024_mt5_log_only_preflight_local.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\verify_h024_ea_preflight_log.py
tests\test_h024_cent_symbol_runtime_validation.py

Purpose:

Allow runtime verifier/summarizer/local helper to validate Exness Standard Cent broker symbols:

USDJPYc
XAUUSDc

while preserving default existing symbol expectations:

USDJPYm
XAUUSDm

Important behavior:

Default mode remains USDJPYm / XAUUSDm.
Explicit cent mode expects USDJPYc / XAUUSDc.
Normalization remains prefix-based:
USDJPYc -> USDJPY
XAUUSDc -> XAUUSD
USDJPYm -> USDJPY
XAUUSDm -> XAUUSD

New explicit flag added to runtime tooling:

--cent-account-symbols

Verifier support:

python scripts\verify_h024_ea_preflight_log.py <csv> --cent-account-symbols

Summarizer support:

python scripts\summarize_h024_ea_intended_action_runtime.py <csv> --cent-account-symbols

Local helper support:

python scripts\run_h024_mt5_log_only_preflight_local.py ... --cent-account-symbols

Focused tests after first cent-symbol validation support:

48 passed in 1.02s

Full test anchor after first cent-symbol validation support:

950 passed in 21.46s

Commit was pushed.

14.2 Found and Fixed Local Helper CLI Regression

After commit 26d6393, running the cent-symbol local runtime target preflight exposed a real CLI-path bug:

NameError: name 'expected_symbols' is not defined

This happened in:

scripts\run_h024_mt5_log_only_preflight_local.py

inside the --automation-target-preflight path.

A repair was made.

Commit:

6a8e017 Fix H024 cent preflight helper CLI path

Changed files:

scripts\run_h024_mt5_log_only_preflight_local.py
tests\test_h024_mt5_log_only_preflight_local_helper.py

Important test/behavior fixes:

main(argv=None) is now testable.
CLI argument parsing now uses parse_args(argv).
expected_symbols is selected before the automation-target branch.
--automation-target-preflight now stops after preflight verdict and does not continue into copy/compile.
Regression coverage added for cent-symbol validation in the local helper.
Regression coverage added to prevent preflight-only mode from copying or compiling.
--repo-ea-source parser support was added for testability.

Important safety semantics:

--automation-target-preflight now does what it says: validates local paths/source invariants without copying, compiling, or collecting.

Focused test anchor after repair:

20 passed in 0.67s

Full test anchor after repair:

952 passed in 16.78s

Diff check:

git diff --check
# clean

Commit was pushed.

14.3 Cent-Symbol Local Runtime Target Preflight Passed

Command run:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --automation-target-preflight `
  --cent-account-symbols

Observed output after repair:

H024 MT5 log-only EA local preflight helper
========================================================================
Research only. No demo/live/Phase 4 approval.
No EA attachment automation. No order-send capability.

Automation target preflight:
- terminal_data_dir: C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075
- terminal_experts_dir: C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts
- terminal_files_dir: C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files
- repo_ea_source: ea_mt5\Experts\H024_LogOnly_Preflight.mq5
- expected_schema_version: h024_ea_log_only_preflight_v2
- expected_ea_version: 0.6
- expected_symbols: USDJPYc, XAUUSDc
Violations: 0

Verdict: PASS

Interpretation:

The local runtime target is ready for the next manual cent-symbol log-only runtime/replay step.

This does not approve demo/live deployment.

15. Current Answer Key

If asked "are we ready to demo/live?":

No.

If asked "are we officially Phase 4?":

No.

If asked "did the 10k USC cent account solve the old minimum-volume blocker?":

It appears to solve the sizing/min-volume feasibility blocker in pure-Python scanner and read-only MT5 profit probes, but it does not approve deployment.

If asked "what is the latest full-test anchor?":

952 passed in 16.78s

If asked "what is the latest commit before HANDOFF_85?":

6a8e017 Fix H024 cent preflight helper CLI path

If asked "what changed from HANDOFF_84?":

Cent-symbol runtime validation and helper CLI support were added. The verifier/summarizer/local helper can now explicitly validate Exness Standard Cent runtime symbols USDJPYc and XAUUSDc, while default behavior remains USDJPYm / XAUUSDm. The cent-symbol local runtime target preflight passed with Violations: 0.

If asked "does 10k USC equal 10k USD?":

No. It is a cent-account balance denomination. The scanner models USC accounting through cent-contract specs, not by pretending the account is a standard USD account.

If asked "does this approve OrderSend?":

No.

If asked "what is the next gate?":

Manual cent-symbol log-only runtime/replay, then runtime CSV verification/summarization with --cent-account-symbols, then executable runtime dry-run request reconstruction if a valid WOULD_OPEN row is observed.

If asked "what should we not do next?":

Do not add execution adapter, OrderSend, OrderCheck, CTrade, or MqlTradeRequest.

16. Current Important Commands

Verify full suite:

python -m pytest -q

Expected current anchor:

952 passed

Run focused cent/local-helper tests:

python -m pytest `
  tests\test_h024_mt5_log_only_preflight_local_helper.py `
  tests\test_h024_cent_symbol_runtime_validation.py `
  -q

Expected focused anchor:

20 passed

Run cent-symbol local runtime target preflight:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --automation-target-preflight `
  --cent-account-symbols

Expected:

expected_symbols: USDJPYc, XAUUSDc
Violations: 0
Verdict: PASS

Run cent-account 10k USC executable candidate scan:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 10000 `
  --risk-fraction 0.01 `
  --cent-account-usc-specs `
  --output-csv reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv `
  --max-rows 10

Expected:

instrument_specs: Exness Standard Cent USC specs
executable_candidate_rows: 1364
Verdict: PASS

Run standard default scan for contrast:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 5

Expected:

executable_candidate_rows: 0
Verdict: PASS
Scan completed; no executable candidate shifts found at these settings.
17. What Remains Missing

Critical missing evidence:

Account was unfunded during the probe: balance=0.0 USC.
No cent-symbol H024 log-only runtime replay has been completed.
No cent-symbol runtime CSV has been verified after manual attach/remove.
No executable runtime dry-run request has been reconstructed from cent-symbol runtime CSV.
No execution safety review after cent feasibility.
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
18. Recommended Next Work

Best next technical step:

Do not add execution code.

Recommended next safe work:

Run cent-symbol helper compile/copy only if needed, still without attach/detach automation.
Manually attach the log-only EA to USDJPYc and XAUUSDc.
Let it emit runtime CSV rows.
Remove the EA manually.
Collect/verify runtime CSV using --cent-account-symbols.
Summarize intended-action runtime rows using --cent-account-symbols.
Only if valid executable WOULD_OPEN rows are observed, reconcile runtime CSV into dry-run requests.
Only after an executable cent-symbol runtime dry-run request exists, perform a separate execution-safety review.

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
19. Immediate First Action For Next AI

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

Add handoff document #85

Then continue from the actual repo state, not from assumptions.

20. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_85.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, pushed, tracked tree clean except local reports/.
Current full-test anchor is 952 passed in 16.78s.
Latest pre-handoff commit is 6a8e017 Fix H024 cent preflight helper CLI path.
H024 is still not demo-approved, not live-approved, and not Phase 4-approved.
No OrderSend, no OrderCheck, no CTrade, no MqlTradeRequest, no execution adapter.
User intends to start with 10k USC.
Real terminal account is USC cent account on Exness-MT5Real25; probe balance was 0.0 USC.
Available account symbols are USDJPYc and XAUUSDc; USDJPYm, XAUUSDm, USDJPY, and XAUUSD were not found.
Read-only MT5 order_calc_profit showed representative USDJPYc and XAUUSDc candidates executable by size at 10000 USC / 1%.
The scanner supports --cent-account-usc-specs.
At 10000 USC / 1% with cent-account USC specs, the scanner found 1364 executable historical candidates.
Runtime verifier/summarizer/helper now support explicit --cent-account-symbols.
Cent-symbol local runtime target preflight passed with expected symbols USDJPYc, XAUUSDc, Violations: 0, Verdict: PASS.
This solves the prior sizing/min-volume feasibility blocker for the intended cent-account path and unblocks cent-symbol log-only runtime/replay, but does not approve deployment.
Next safe gate is manual cent-symbol log-only runtime/replay and executable runtime dry-run request reconstruction.
reports/ stays untracked.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
