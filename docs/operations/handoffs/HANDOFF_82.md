# HANDOFF_82 — H024 Threshold Scanner Generalized and Risk-Fraction Feasibility Preserved

If any older handoff conflicts with this one, this handoff wins. It continues from HANDOFF_81.

This handoff is standalone enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current stage:

Execution-safety preparation after H024 research evidence.

Current status:

H024 is promising, but still not demo-approved, not live-approved, and not Phase 4-approved.

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
Current Expected Repo State

Expected after this handoff is committed:

On branch main
Your branch is up to date with 'origin/main'.
Tracked tree clean
Untracked: reports/
Latest commit: Add handoff document #82

Current full-test anchor:

939 passed in 19.55s

If tests drop below 939 without intentional test removal, treat as a regression.

Non-Negotiable Safety Boundary

H024 remains:

Research / pre-deployment only
No demo deployment approval
No live trading approval
No Phase 4 execution approval
No order-send capability approved
No execution adapter approved

Forbidden:

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
Pure Python risk-fraction threshold comparison
Current Latest Commits

Expected recent history before this handoff is committed:

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

After this handoff is committed, latest commit should be:

Add handoff document #82
What Changed Since HANDOFF_81
1. Documented the 100 USD / 1 Percent Feasibility Boundary

Commit:

696f4c9 Document H024 100 USD feasibility boundary

New doc:

docs\operations\H024_100USD_1PCT_FEASIBILITY_BOUNDARY.md

Purpose:

Preserve the deployment blocker clearly.

Key result:

At 100 USD balance and 1 percent risk, H024 has no executable historical candidate shifts.

The blocker is economic / broker minimum-volume feasibility, not a known strategy-code malfunction.

This document explicitly says the 245 USD threshold result does not approve:

Higher account balance
Higher risk
Demo trading
Live trading
Phase 4 execution
OrderSend / OrderCheck / CTrade / MqlTradeRequest
Execution adapter work

Docs-only edit. No pytest run required.

2. Found a Scanner Robustness Problem During Risk-Fraction Comparison

Attempted risk comparison using:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.005
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.0075
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.015
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.02

Observed failures before patch:

At lower risk fractions, the scanner crashed because the original high boundary was calibrated to the 1 percent scan and did not contain a candidate.

Example error:

ValueError: high boundary must have at least one candidate for ANY; observed 0

A later run was manually interrupted during repeated real H4 rescans.

Interpretation:

This was a scanner-bracketing robustness problem, not a strategy deployment signal.

3. Generalized the Capital Threshold Scanner

Commit:

63d0573 Expand H024 capital threshold scan brackets

Changed files:

scripts\scan_h024_capital_thresholds.py
tests\test_h024_capital_threshold_scan.py

Purpose:

Make the threshold scanner usable across risk fractions instead of assuming the original 1 percent risk brackets.

Important behavior added:

Auto-expands high boundary until at least one matching candidate is found.
Supports --max-high.
Supports --high-growth-factor.
Supports --no-auto-expand-high.
Defaults low boundaries to 0.
Treats balance <= 0 as an empty candidate set without rescanning real H4 data.
Rejects non-positive risk fraction.
Keeps exact binary threshold search once a valid bracket exists.

Focused test result:

7 passed in 1.21s

Full suite result after patch:

939 passed in 19.55s
4. Revalidated Original 1 Percent Baseline After Patch

Command:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01

Observed result remained unchanged:

ANY threshold balance: 245 USD at 1.00% risk
USDJPY threshold balance: 245 USD at 1.00% risk
XAUUSD threshold balance: 935 USD at 1.00% risk
Verdict: PASS

Boundary checks remained valid:

ANY balance=244: matching=0 total=0 USDJPY=0 XAUUSD=0
ANY balance=245: matching=1 total=1 USDJPY=1 XAUUSD=0
USDJPY balance=244: matching=0 total=0 USDJPY=0 XAUUSD=0
USDJPY balance=245: matching=1 total=1 USDJPY=1 XAUUSD=0
XAUUSD balance=934: matching=0 total=568 USDJPY=568 XAUUSD=0
XAUUSD balance=935: matching=1 total=569 USDJPY=568 XAUUSD=1
5. Ran Risk-Fraction Threshold Comparison

Commands:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.005
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.0075
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.015
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.02

Observed thresholds:

Risk fraction    ANY threshold    USDJPY threshold    XAUUSD threshold
0.50%    490 USD    490 USD    1,870 USD
0.75%    327 USD    327 USD    1,247 USD
1.00%    245 USD    245 USD    935 USD
1.50%    164 USD    164 USD    624 USD
2.00%    123 USD    123 USD    468 USD

Key interpretation:

At 100 USD, even 2 percent risk still does not make H024 mechanically executable.

The first ANY / USDJPY executable threshold at 2 percent risk is 123 USD.

Approximate implied minimum risk at 100 USD:

Scope    Approximate risk needed at 100 USD
ANY / USDJPY    2.45%
XAUUSD    9.35%

These are feasibility measurements only.

They do not approve raising risk.

6. Documented Risk-Fraction Threshold Comparison

Commit:

0aafc4e Document H024 risk fraction threshold comparison

New doc:

docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_RESULT.md

Purpose:

Preserve the threshold comparison and prevent future confusion.

Docs-only edit. No pytest run required.

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
EA converts under-min-volume signal rows into BLOCKED, not fake WOULD_OPEN.
BLOCKED signal rows preserve sizing diagnostics.
A runtime replay proved positive entry/stop/stop-distance/raw-lots are preserved on BLOCKED rows.
A reusable verifier exists for BLOCKED sizing diagnostics.
A regression test ensures positive BLOCKED diagnostics cannot become dry-run requests.
Minimum-volume feasibility is quantified.
At 100 USD / 1 percent risk, H024 has no executable historical candidate shifts.
At 1 percent risk, ANY / USDJPY first executable historical candidate appears at 245 USD.
At 1 percent risk, XAUUSD first executable historical candidate appears at 935 USD.
Threshold scanner now auto-expands high brackets across risk fractions.
At 2 percent risk, ANY / USDJPY threshold is still 123 USD.
Therefore, a 100 USD account remains mechanically non-executable even at 2 percent risk.
Current full test anchor is 939 passed.

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

If asked “what is the exact capital threshold at 1 percent risk?”:

ANY / USDJPY first executable: 245 USD.
XAUUSD first executable: 935 USD.

If asked “what changed in the scanner?”:

It now auto-expands high thresholds instead of assuming the 1 percent bracket works for every risk fraction.

If asked “does higher risk fix 100 USD?”:

Not safely and not within approved boundaries. Even 2 percent risk still requires 123 USD for first ANY / USDJPY executable threshold. Approximate implied risk for ANY/USDJPY at 100 USD is about 2.45 percent, and XAUUSD about 9.35 percent. These are measurements only, not recommendations.

If asked “should we raise risk to force execution?”:

No.

If asked “does this approve execution adapter work?”:

No.

Current Important Commands

Verify full suite:

python -m pytest -q

Expected current anchor:

939 passed

Run exact capital threshold scan at 1 percent risk:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01

Expected thresholds:

ANY: 245 USD
USDJPY: 245 USD
XAUUSD: 935 USD

Run risk-fraction comparison manually:

python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.005
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.0075
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.01
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.015
python scripts\scan_h024_capital_thresholds.py --risk-fraction 0.02

Expected threshold table:

Risk fraction    ANY threshold    USDJPY threshold    XAUUSD threshold
0.50%    490 USD    490 USD    1,870 USD
0.75%    327 USD    327 USD    1,247 USD
1.00%    245 USD    245 USD    935 USD
1.50%    164 USD    164 USD    624 USD
2.00%    123 USD    123 USD    468 USD

Run executable candidate scan at current settings:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 20

Expected at current settings:

executable_candidate_rows: 0
Important Files

Capital feasibility and threshold docs:

docs\operations\H024_100USD_1PCT_FEASIBILITY_BOUNDARY.md
docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_RESULT.md
docs\operations\H024_EXACT_CAPITAL_THRESHOLD_RESULT.md
docs\operations\H024_CAPITAL_FEASIBILITY_FRONTIER_RESULT.md
docs\operations\H024_EXECUTABLE_CANDIDATE_SHIFT_SCAN_RESULT.md
docs\operations\H024_MIN_VOLUME_FEASIBILITY_RESULT.md

Capital threshold tools:

scripts\scan_h024_capital_thresholds.py
scripts\scan_h024_executable_candidate_shifts.py
scripts\summarize_h024_min_volume_feasibility.py

Capital threshold tests:

tests\test_h024_capital_threshold_scan.py
tests\test_h024_executable_candidate_shift_scan.py
tests\test_h024_min_volume_feasibility.py

EA/runtime:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
scripts\run_h024_mt5_log_only_preflight_local.py
scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\verify_h024_ea_source_static.py
scripts\reconcile_h024_runtime_dry_run_requests.py
scripts\summarize_h024_blocked_sizing_diagnostics.py
Data Rules

Accepted validation source:

Exness demo MT5 broker-native exports only.

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
Recommended Next Work

Best next technical step:

Do not add execution code.

Recommended safe next options:

Add a reusable table-output mode to scan_h024_capital_thresholds.py so risk-fraction comparisons can be produced by one command instead of manual repeated scans.
Add tests for that comparison-table mode.
Keep all results research-only.
Continue only with log-only runtime replay and CSV reconciliation.
Investigate stop model / symbol eligibility / sizing policy at research level.

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
Latest commit: Add handoff document #82

Then continue from the actual repo state.
