# HANDOFF_87 — H024 Cent Account Runtime Signal Path + Log-Only Replay Sweep Automation

If any older handoff conflicts with this one, this handoff wins.

This is intended to be fully self-contained. A new AI should be able to continue safely from this document without opening older handoffs first.

---

## 0. One-Sentence State

H024 remains research-only and is not demo/live/Phase 4 approved; however, the Exness Standard Cent route using `USDJPYc` / `XAUUSDc` has now produced a verified log-only historical replay signal path on `XAUUSDc`, that signal correctly became `BLOCKED` because the account balance was `0.00 USC`, and a new log-only replay sweep mode has been implemented, compiled, statically verified, committed, pushed, and tested with `958 passed`.

---

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current strategy family:

```text
H024

Current stage:

Execution-safety preparation / cent-account log-only runtime validation

The user is eager to deploy and intends to start with:

10000 USC

on an Exness Standard Cent account.

Do not soften deployment boundaries.

The correct direct answer about deployment is:

H024 is meaningfully closer under the 10000 USC cent-account route, but it is still not demo/live/Phase 4 deployable.
2. Human Preference

The user is tired of ceremony and wants practical progress.

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

Important recent frustration:

A replay-sweep patch attempt initially went wrong because tests were committed without implementation. The user noticed repeated failures and explicitly challenged whether the errors were being read. Be careful. Inspect actual source before patching. Do not blindly repeat failing patch scripts.

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

MetaEditor:

C:\Program Files\MetaTrader 5\MetaEditor64.exe

Terminal data dir:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075

Terminal EA source:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5

Compiled EX5:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5

Terminal runtime CSV:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\h024_ea_log_only_preflight.csv

Repo runtime CSV:

reports\h024_ea_log_only_preflight.csv

reports/ is local and intentionally untracked.

Do not commit reports/.

4. Expected Repo State After This Handoff Is Committed

Expected:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Expected latest commit after this handoff is committed:

Add handoff document #87

Expected latest code commit before handoff:

7bf1728 Add H024 log-only replay sweep mode

Latest full-test anchor after replay-sweep implementation:

958 passed in 16.44s

Focused replay/static anchor:

19 passed in 0.68s

Static EA source verifier:

Violations: 0
Verdict: PASS

MetaEditor compile/copy helper result after replay sweep:

MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.
5. Recent Commit History

Important recent commits:

7bf1728 Add H024 log-only replay sweep mode
d67eff3 Revert "Add H024 log-only replay sweep mode"
7c1b69a Add H024 log-only replay sweep mode
993b274 Document H024 cent-symbol blocked replay result
d42d25e Add handoff document #86
ff18be2 Fix H024 cent collect verifier symbols
2ddaf90 Add handoff document #85
6a8e017 Fix H024 cent preflight helper CLI path
26d6393 Add H024 cent symbol runtime validation support
eb4aa84 Add handoff document #84
b446ed9 Add H024 cent account executable scan specs
cd3c153 Document H024 cent account feasibility probe

Important note:

7c1b69a was a bad commit. It accidentally added only failing replay-sweep static tests without the EA implementation. It made main red. It was immediately reverted by d67eff3. The correct implementation landed later in 7bf1728.

Do not use 7c1b69a as evidence that replay sweep is implemented. Use 7bf1728.

6. Non-Negotiable Safety Boundary

H024 remains:

Research-only
Pre-deployment only
Not demo-approved
Not live-approved
Not Phase 4-approved
Not approved for order execution
Not approved for any execution adapter

Forbidden in current stage:

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
Treating BLOCKED rows as executable
Reconstructing dry-run execution requests from BLOCKED rows

Allowed so far:

Manual EA attach/remove
Copy EA source to terminal Experts
Compile EA with MetaEditor
Reset/collect runtime CSV
Verify runtime CSV
Summarize intended-action rows
Historical log-only replay using InpH024ClosedShift
Log-only replay sweep using InpH024ReplaySweepEnabled
CSV-read-only dry-run request reconciliation
Pure Python dry-run execution request contracts
Runtime BLOCKED sizing diagnostics verification
Pure Python minimum-volume feasibility summary
Pure Python executable candidate shift scanning
Pure Python exact capital threshold scanning
Pure Python risk-fraction threshold comparison
Read-only MT5 account/symbol-info probes
Read-only MT5 order_calc_profit probes
Pure Python cent-account USC feasibility scanner support
Cent-symbol runtime CSV verifier/summarizer support
Cent-symbol local runtime target preflight
Clean cent-symbol log-only runtime collection and verification
7. H024 Strategy Mechanics Summary

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
8. H020 / H024 Sizing Boundary

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

Therefore:

Cent-account scans must not bypass H020 sizing.

The cent scanner routes balances through cent-account USC instrument specs, not by pretending 10000 USC equals 10000 USD.

9. Data Rules

Accepted validation source:

Exness demo/terminal broker-native exports only

Accepted model symbols:

USDJPY
XAUUSD

Current cent account runtime symbols:

USDJPYc
XAUUSDc

Previously observed standard-like symbols:

USDJPYm
XAUUSDm

Symbol normalization:

USDJPYc -> USDJPY
XAUUSDc -> XAUUSD
USDJPYm -> USDJPY
XAUUSDm -> XAUUSD

Accepted timeframes:

Broker-native H4
Broker-native M1

Broker timezone used by loader:

Europe/Athens

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
reports/*.csv
reports/*.json
Local runtime CSVs
Local compile logs
10. Core Files

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

Cent account support:

scripts\scan_h024_executable_candidate_shifts.py
tests\test_h024_cent_account_specs.py

Cent-symbol runtime validation support:

scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\run_h024_mt5_log_only_preflight_local.py
tests\test_h024_cent_symbol_runtime_validation.py
tests\test_h024_mt5_log_only_preflight_local_helper.py

Replay sweep support:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
tests\test_h024_ea_replay_sweep_static.py

Important docs:

docs\operations\H024_CENT_ACCOUNT_SYMBOL_FEASIBILITY_PROBE_RESULT.md
docs\operations\H024_CENT_SYMBOL_REPLAY_BLOCKED_RUNTIME_RESULT.md
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
docs\operations\handoffs\HANDOFF_83.md
docs\operations\handoffs\HANDOFF_84.md
docs\operations\handoffs\HANDOFF_85.md
docs\operations\handoffs\HANDOFF_86.md
docs\operations\handoffs\HANDOFF_87.md
11. EA Current Facts

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

Core replay input:

InpH024ClosedShift = 1

Replay cap:

1 <= effective closed shift <= 240

Normal mode:

Uses InpH024ClosedShift.
Clamps below 1 to 1.
Clamps above 240 to 240.
Preserves old literal static-test strings:
if(InpH024ClosedShift < 1)
if(InpH024ClosedShift > 240)

Sweep mode:

InpH024ReplaySweepEnabled = true
InpH024ReplaySweepStartShift = ...
InpH024ReplaySweepEndShift = ...
InpH024ReplaySweepMaxRows = ...

Sweep mode temporarily sets:

g_h024_replay_sweep_override_shift = shift

then calls:

WriteH024StateObservationRow()
WriteH024IntendedActionRuntimeRow()

for each shift.

Sweep markers:

H024_REPLAY_SWEEP
H024_REPLAY_SWEEP_SHIFT
H024_REPLAY_SWEEP_DONE
12. Runtime Intended-Action Behavior

Runtime intended-action behavior:

NO_ACTION rows can carry zero entry/stop/lots.
Signal rows derive entry/stop from closed H4 bar and ATR stop.
If signal sizing is executable, row may remain WOULD_OPEN.
If signal sizing is below broker minimum volume, row becomes BLOCKED:volume_below_min_for_would_open.
BLOCKED signal rows preserve positive entry/stop/stop-distance when available.
BLOCKED signal rows force final executable lots to 0.
Dry-run reconciler must not emit requests from BLOCKED rows.

Important current reality:

The cent-symbol replay signal path observed so far became BLOCKED because account balance was 0.00 USC.

13. Evidence Before HANDOFF_87

Already true before this handoff:

H024 backtest was promising.
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
Historical log-only replay previously observed WOULD_OPEN path on non-cent/default route.
Dry-run request contract exists in pure Python.
Runtime CSV to dry-run request reconciler exists and is CSV-read-only.
Reconciler correctly rejects non-executable rows.
EA derives entry/stop for signal rows.
EA converts under-min-volume signal rows into BLOCKED, not fake WOULD_OPEN.
BLOCKED signal rows preserve sizing diagnostics.
Runtime replay proved positive entry/stop/stop-distance/raw-lots are preserved on BLOCKED rows.
A reusable verifier exists for BLOCKED sizing diagnostics.
Regression tests ensure positive BLOCKED diagnostics cannot become dry-run requests.
Minimum-volume feasibility is quantified.
Executable candidate shift scanner exists.
Exact capital threshold scanner exists.
Optimized risk-fraction threshold comparison exists.
Read-only MT5 account/symbol probes showed real account is USC cent and exposes USDJPYc / XAUUSDc.
Read-only MT5 order_calc_profit probes showed representative USDJPYc and XAUUSDc candidates executable by size at 10000 USC / 1%.
Pure-Python cent-account scanner support exists.
At 10000 USC / 1% with cent-account USC specs, scanner found 1364 executable historical candidates.
Runtime verifier/summarizer/helper support explicit --cent-account-symbols.
Clean cent-symbol runtime current run passed, but only NO_ACTION rows were observed.
Helper collect bug was fixed so --collect --cent-account-symbols verifies against USDJPYc / XAUUSDc.
14. Clean Cent Runtime Result From HANDOFF_86

Clean cent runtime collection facts:

Rows: 78
Violations: 0
Verdict: PASS

Intended-action summary:

CSV: reports\h024_ea_log_only_preflight.csv
Total rows: 78
Intended-action header rows: 2
Intended-action data rows: 12

USDJPYc:
  headers: 1
  rows: 6
  normalized: USDJPY
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

XAUUSDc:
  headers: 1
  rows: 6
  normalized: XAUUSD
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

Verdict: PASS

Interpretation:

Clean cent-symbol runtime path passed, but no signal was observed.
15. Cent Candidate Scan Evidence

Command used:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 10000 `
  --risk-fraction 0.01 `
  --cent-account-usc-specs `
  --output-csv reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv `
  --max-rows 20

Result:

H024 executable candidate shift scan
========================================================================
Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.

balance: 10000.00
risk_fraction: 0.010000
instrument_specs: Exness Standard Cent USC specs
executable_candidate_rows: 1364
wrote: reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv
Verdict: PASS
Candidates found only for replay planning; no execution approval implied.

Inside the EA cap:

total_candidates=1364
candidates_within_current_ea_replay_cap_240=25

Important rows inside cap:

XAUUSD sell | decision=2026-03-17T22:00:00+00:00 | entry=2026-03-18T02:00:00+00:00 | shift=229 | final_risk=-0.008352
USDJPY sell | decision=2026-03-18T02:00:00+00:00 | entry=2026-03-18T06:00:00+00:00 | shift=228 | final_risk=-0.009907
XAUUSD sell | decision=2026-03-18T06:00:00+00:00 | entry=2026-03-18T10:00:00+00:00 | shift=227 | final_risk=-0.008657

Important insight:

The scanner uses broker CSV-derived shift alignment. Runtime MT5 H4 indexing can differ slightly. A tight sweep around candidate shifts is safer than replaying one exact shift.

16. Manual Replay Attempts And What They Proved
16.1 Far-history replay failed due to 240 cap

Initial candidate shifts were around 8600+ from 2018.

Example:

XAUUSD shift 8665
USDJPY shift 8632

The EA source had:

if(InpH024ClosedShift > 240)
{
   return 240;
}

Therefore, far-history replay cannot be performed with current EA without a tested research-only replay-cap change.

No such cap extension was implemented. Instead, the team found candidates within <=240.

16.2 One-symbol and two-symbol manual replay showed shift/time alignment complexity

Manual replay around 229 / 228 initially produced NO_ACTION rows, while state rows showed the strategy was near a signal but missing resumption.

Example XAUUSD state row near candidate:

closed_h4_time=2026.03.17 20:00:00
trend_down=true
previous_bullish=true
short_pullback_ok=true
short_resumption=false
short_signal_observed=false

This implied a shift/time alignment issue, not an execution issue.

16.3 Tight manual sweep found signal path

A tight manual sweep was run:

XAUUSDc H4:
  InpH024ClosedShift = 229
  InpH024ClosedShift = 228
  InpH024ClosedShift = 227

USDJPYc H4:
  InpH024ClosedShift = 228
  InpH024ClosedShift = 227
  InpH024ClosedShift = 226

Result:

Rows: 264
Violations: 0
Verdict: PASS

Unique intended-action outcomes included:

ROW 66: symbol=XAUUSDc action=BLOCKED side=short closed=2026.03.18 00:00:00
  entry=4991.4050000000 stop=5049.4490000000 raw_lots=0.0000000000 final_lots=0.0000000000
  reason=BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short;closed_h4_time=2026.03.18 00:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

Summary:

USDJPYc:
  headers: 3
  rows: 19
  normalized: USDJPY
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 19

XAUUSDc:
  headers: 3
  rows: 22
  normalized: XAUUSD
  WOULD_OPEN: 0
  BLOCKED: 6
  NO_ACTION: 16

Verdict: PASS

Interpretation:

The cent-symbol H024 signal path exists in runtime.
It was not executable because runtime balance was 0.00 USC.

This result was documented in:

docs\operations\H024_CENT_SYMBOL_REPLAY_BLOCKED_RUNTIME_RESULT.md

Commit:

993b274 Document H024 cent-symbol blocked replay result
17. Why The Signal Was BLOCKED, Not WOULD_OPEN

The runtime account balance was:

0.00 USC

Therefore:

risk budget = 0
raw_lots = 0
final_lots = 0

The EA correctly converted the would-open signal path into:

BLOCKED:volume_below_min_for_would_open

This is not a strategy failure. It is not an execution success. It is correct safety behavior.

Current missing evidence:

A real-runtime executable WOULD_OPEN row with nonzero final lots.

To observe that, either:

Fund the cent account and rerun log-only replay/sweep, or
Add a clearly labeled research-only synthetic balance override diagnostic.

Option 1 is cleaner. Option 2 must be heavily guarded and documented.

18. Replay Sweep Automation Added In 7bf1728

Why added:

Manual attach/remove for every candidate shift is too slow and error-prone.

New safe automation target:

One manual attach per symbol, sweep multiple closed H4 shifts inside the EA.

This avoids:

Chart automation
GUI automation
Order automation
Execution adapter work

It is still log-only.

Commit:

7bf1728 Add H024 log-only replay sweep mode

Files:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
tests\test_h024_ea_replay_sweep_static.py

New inputs:

input bool   InpH024ReplaySweepEnabled = false;
input int    InpH024ReplaySweepStartShift = 1;
input int    InpH024ReplaySweepEndShift = 1;
input int    InpH024ReplaySweepMaxRows = 20;

New globals:

int g_h024_replay_sweep_override_shift = 0;
bool g_h024_replay_sweep_written = false;

New helper functions:

H024ReplaySweepStartShift()
H024ReplaySweepEndShift()
H024ReplaySweepMaxRows()
WriteH024ReplaySweepRows()

New runtime events:

H024_REPLAY_SWEEP
H024_REPLAY_SWEEP_SHIFT
H024_REPLAY_SWEEP_DONE

OnInit behavior:

Writes normal init/context rows.
If sweep disabled:
Writes normal single state/intended-action rows.
If sweep enabled:
Writes intended-action header once.
Sweeps configured shifts.
Writes state and intended-action rows per shift.
Does not repeat sweep on tick/timer.

OnTick / OnTimer behavior:

if(!InpH024ReplaySweepEnabled)
{
   WriteH024StateObservationRow();
   WriteH024StrategyIntentRow();
   WriteH024IntendedActionRuntimeRow();
}

This prevents repeating sweep rows on timer/tick.

Important implementation detail:

H024EffectiveClosedShift() preserves old static clamp strings for compatibility:

if(InpH024ClosedShift < 1)
if(InpH024ClosedShift > 240)

and then supports override mode via:

g_h024_replay_sweep_override_shift
19. Replay Sweep Validation

Focused tests:

19 passed in 0.68s

Static source verifier:

H024 MQL5 EA source static verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Source: ea_mt5\Experts\H024_LogOnly_Preflight.mq5
Violations: 0

Verdict: PASS

Compile/copy helper:

H024 MT5 log-only EA local preflight helper
========================================================================
Research only. No demo/live/Phase 4 approval.
No EA attachment automation. No order-send capability.

Copied EA source to: C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\...\MQL5\Experts\H024_LogOnly_Preflight.mq5
MetaEditor compile return code: 1
EX5 path: ...\H024_LogOnly_Preflight.ex5
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Skipped runtime CSV collection. Attach/remove the EA manually, then rerun with --collect.

Full test suite:

958 passed in 16.44s

Commit:

7bf1728 Add H024 log-only replay sweep mode
20. Known Pitfalls
20.1 MetaEditor returns code 1 even when compile succeeds

The helper accepts compile if EX5 was refreshed.

Expected:

MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Do not treat return code 1 alone as failure if EX5 refreshed.

20.2 One-symbol verifier may fail missing the other symbol

If collecting only XAUUSDc, cent verifier may complain:

log missing required symbols: ['USDJPYc']

That is expected if only one symbol was attached.

For full cent-symbol verifier pass, attach both:

USDJPYc
XAUUSDc
20.3 BLOCKED is not executable

A row with:

BLOCKED:volume_below_min_for_would_open

must not be treated as a dry-run request or execution candidate.

20.4 Runtime account balance is currently 0.00 USC

This is the main reason no executable WOULD_OPEN row exists.

20.5 Scanner shift and MT5 runtime shift can be offset

Use sweeps around candidates rather than only one exact shift.

21. Recommended Next Runtime Validation

Use the new replay sweep mode to validate in MT5.

Step A: Reset old CSVs
$TerminalDataDir = "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
$TerminalCsv = Join-Path $TerminalDataDir "MQL5\Files\h024_ea_log_only_preflight.csv"
$RepoCsv = "reports\h024_ea_log_only_preflight.csv"
Remove-Item $TerminalCsv -ErrorAction SilentlyContinue
Remove-Item $RepoCsv -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force reports | Out-Null
Step B: Attach XAUUSDc H4 once

Open:

XAUUSDc H4

Attach:

H024_LogOnly_Preflight

Set inputs:

InpH024ReplaySweepEnabled = true
InpH024ReplaySweepStartShift = 227
InpH024ReplaySweepEndShift = 229
InpH024ReplaySweepMaxRows = 10

Click OK. Wait 5-10 seconds. Remove EA.

Expected:

H024_REPLAY_SWEEP
H024_REPLAY_SWEEP_SHIFT
H024_REPLAY_SWEEP_DONE
At least one BLOCKED short around 2026.03.18 00:00:00 if terminal history alignment has not shifted.
Step C: Attach USDJPYc H4 once

Open:

USDJPYc H4

Attach:

H024_LogOnly_Preflight

Set inputs:

InpH024ReplaySweepEnabled = true
InpH024ReplaySweepStartShift = 226
InpH024ReplaySweepEndShift = 228
InpH024ReplaySweepMaxRows = 10

Click OK. Wait 5-10 seconds. Remove EA.

Expected:

H024_REPLAY_SWEEP
H024_REPLAY_SWEEP_SHIFT
H024_REPLAY_SWEEP_DONE
Likely NO_ACTION rows based on prior manual sweep.
Step D: Collect
python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --cent-account-symbols `
  --collect
Step E: Summarize
python scripts\summarize_h024_ea_intended_action_runtime.py `
  reports\h024_ea_log_only_preflight.csv `
  --cent-account-symbols

Useful compact extraction:

@'
import csv, re
from pathlib import Path

p = Path("reports/h024_ea_log_only_preflight.csv")
rows = list(csv.reader(p.open(newline="", encoding="utf-8-sig")))

print(f"rows={len(rows)}")

print("\n=== Replay sweep markers ===")
for i, row in enumerate(rows, start=1):
    if len(row) > 31 and row[7] in {"H024_REPLAY_SWEEP", "H024_REPLAY_SWEEP_SHIFT", "H024_REPLAY_SWEEP_DONE"}:
        print(f"ROW {i}: symbol={row[9]} event={row[7]} detail={row[31]}")

print("\n=== Unique intended-action outcomes ===")
seen = set()
for i, row in enumerate(rows, start=1):
    if len(row) > 53 and row[7] == "H024_INTENDED_ACTION_ROW":
        reason = row[53]
        m = re.search(r"closed_h4_time=([^;]+)", reason)
        closed = m.group(1) if m else ""
        key = (row[34], row[37], row[38], closed, row[39], row[40], row[47], row[48], reason)
        if key in seen:
            continue
        seen.add(key)
        print(f"ROW {i}: symbol={row[34]} action={row[37]} side={row[38]} closed={closed}")
        print(f"  entry={row[39]} stop={row[40]} raw_lots={row[47]} final_lots={row[48]}")
        print(f"  reason={reason}")
'@ | python -
22. Recommended Next Engineering Options
Option A — Real-balance evidence

Fund the cent account and rerun log-only replay sweep.

This is the cleanest way to observe real runtime sizing with nonzero risk budget.

Expected if funded and signal repeats:

XAUUSDc replay signal may become WOULD_OPEN if final lots >= minimum volume.

Still not deployment approval. It would only satisfy the executable runtime intended-action evidence gate.

Option B — Synthetic research diagnostic balance override

Add a diagnostic-only balance override.

This must be:

Default off
Clearly labeled as synthetic in CSV rows
Tested
Documented
Verifier/summarizer aware
Never execution-enabled
Never confused with live account evidence

This option may be useful if the user does not want to fund the account yet.

Option C — Runtime terminal H4 shift scanner

Build a read-only terminal-side scanner that computes exact MT5 runtime candidate shifts directly from terminal H4 bars, avoiding broker CSV shift-alignment drift.

Must remain:

Read-only
Log-only
No execution APIs
No chart automation
23. Current Deployment Verdict

H024 is closer, but still:

not demo-approved
not live-approved
not Phase 4-approved
not execution-approved

The blocker has changed from:

No cent-symbol runtime signal path observed.

to:

No executable real-runtime WOULD_OPEN row with nonzero final lots has been observed.

Reason:

Real cent account balance is 0.00 USC.
24. What Not To Do Next

Do not add:

OrderSend
OrderCheck
CTrade
MqlTradeRequest
MqlTradeResult
Execution adapter
Demo trading
Live trading
Phase 4 approval
Chart attach automation
GUI automation

Do not treat the blocked runtime signal as executable.

Do not reconstruct dry-run execution requests from blocked rows.

Do not imply that replay sweep mode is execution automation. It is not.

25. Exact Commands For Current Verification

Repo state:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Focused replay/static tests:

python -m pytest `
  tests\test_h024_ea_replay_sweep_static.py `
  tests\test_h024_ea_closed_shift_execution_boundary_static.py `
  tests\test_h024_ea_source_static_verifier.py `
  tests\test_h024_ea_log_only_preflight_static.py `
  tests\test_h024_ea_closed_shift_replay_static.py `
  -q

Expected:

19 passed

Full test suite:

python -m pytest -q

Expected:

958 passed

Static EA verifier:

python scripts\verify_h024_ea_source_static.py

Expected:

Violations: 0
Verdict: PASS

Automation target preflight:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --automation-target-preflight `
  --cent-account-symbols

Compile/copy EA:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --cent-account-symbols

Collect runtime CSV after manual attach/remove:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --cent-account-symbols `
  --collect

Summarize intended-action runtime:

python scripts\summarize_h024_ea_intended_action_runtime.py `
  reports\h024_ea_log_only_preflight.csv `
  --cent-account-symbols
26. Immediate First Action For Next AI

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

Add handoff document #87

Expected latest code commit before handoff:

7bf1728 Add H024 log-only replay sweep mode
27. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_87.

I understand:

H024 remains research-only and is not demo/live/Phase 4 approved.
No execution adapter, no OrderSend, no OrderCheck, no CTrade, no MqlTradeRequest.
The Exness Standard Cent route uses USDJPYc and XAUUSDc, normalized to USDJPY and XAUUSD.
The real account balance observed so far is 0.00 USC.
Clean cent-symbol runtime verification passed.
A cent-symbol historical replay signal path was observed on XAUUSDc.
That signal became BLOCKED, not WOULD_OPEN, because account balance was zero.
The blocked replay result was documented in docs\operations\H024_CENT_SYMBOL_REPLAY_BLOCKED_RUNTIME_RESULT.md.
A failed replay-sweep test-only commit was reverted.
The correct replay-sweep implementation landed in 7bf1728 Add H024 log-only replay sweep mode.
Latest full test anchor is 958 passed in 16.44s.
The next safe step is to manually validate replay sweep mode in MT5, one attach per symbol, not to add execution code.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
