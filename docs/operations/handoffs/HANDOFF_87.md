# HANDOFF_87 — H024 Cent Replay Signal Path + Log-Only Replay Sweep Automation

If any older handoff conflicts with this one, this handoff wins.

This continues from HANDOFF_86 and the commits after it. It is intended to be fully self-contained.

---

## 0. One-Sentence State

H024 remains research-only and not demo/live/Phase 4 approved; however, the Exness Standard Cent `USDJPYc` / `XAUUSDc` log-only route has now produced a verified cent-symbol historical replay signal path that correctly became `BLOCKED` because the account balance was `0.00 USC`, and a new log-only replay sweep mode has been implemented, committed, pushed, compiled, statically verified, and tested with `958 passed`.

---

## 1. Current Repo State

Repository root:

```text
C:\Users\equin\Documents\institutional-ea

Branch:

main

Expected status after this handoff commit:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Do not commit reports/.

Latest code commit before this handoff:

7bf1728 Add H024 log-only replay sweep mode

Important recent commits:

7bf1728 Add H024 log-only replay sweep mode
d67eff3 Revert "Add H024 log-only replay sweep mode"
7c1b69a Add H024 log-only replay sweep mode
993b274 Document H024 cent-symbol blocked replay result
d42d25e Add handoff document #86
ff18be2 Fix H024 cent collect verifier symbols
2ddaf90 Add handoff document #85

Note on 7c1b69a / d67eff3:

A first attempt accidentally committed only failing replay-sweep tests without the EA implementation. That made main red. It was immediately reverted by d67eff3, restoring green status. The correct implementation then landed in 7bf1728.

Latest full test anchor after the correct replay-sweep implementation:

958 passed in 16.44s

Focused replay/static test anchor:

19 passed in 0.68s

Static EA verifier:

Violations: 0
Verdict: PASS

MetaEditor compile/copy helper:

MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.
2. Non-Negotiable Safety Boundary

H024 remains:

Research-only
Not demo-approved
Not live-approved
Not Phase 4-approved
Not approved for any execution adapter
Not approved for any order placement

Still forbidden:

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
Chart attach/detach automation
GUI automation
MT5 profile/template mutation affecting live terminals
Raising risk to force executable candidates
Treating feasibility or replay evidence as deployment approval

The new replay sweep is log-only. It must not be confused with execution automation.

3. Environment

Windows / PowerShell / VS Code.

Python:

Python 3.12.10 inside .venv

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

Repo runtime report CSV:

reports\h024_ea_log_only_preflight.csv

reports/ is local and intentionally untracked.

4. Cent Account Reality

The user intends to start with:

10000 USC

on an Exness Standard Cent account.

Known runtime/account facts:

Account currency: USC
Available symbols: USDJPYc, XAUUSDc
Unavailable symbols: USDJPYm, XAUUSDm, USDJPY, XAUUSD
Probe/runtime balance: 0.00 USC

Symbol normalization:

USDJPYc -> USDJPY
XAUUSDc -> XAUUSD
USDJPYm -> USDJPY
XAUUSDm -> XAUUSD

Current deployment-relevant interpretation:

The 10000 USC route remains mechanically plausible by size under cent specs, but real runtime executable sizing cannot be observed while the account balance is 0.00 USC.

5. Evidence Preserved Since HANDOFF_86
5.1 Clean cent-symbol runtime path

Before this handoff, clean USDJPYc / XAUUSDc log-only runtime collection passed:

Rows: 78
Violations: 0
Verdict: PASS

Intended-action summary:

USDJPYc:
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

XAUUSDc:
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

This proved the clean cent-symbol runtime path, but no signal.

5.2 Cent candidate scan

The cent-account scanner found:

balance: 10000.00
risk_fraction: 0.010000
instrument_specs: Exness Standard Cent USC specs
executable_candidate_rows: 1364
Verdict: PASS

Inside the EA’s current replay cap InpH024ClosedShift <= 240, there were:

candidates_within_current_ea_replay_cap_240 = 25

Notable nearby candidates:

XAUUSD sell | decision=2026-03-17T22:00:00+00:00 | ea_closed_shift=229
USDJPY sell | decision=2026-03-18T02:00:00+00:00 | ea_closed_shift=228
XAUUSD sell | decision=2026-03-18T06:00:00+00:00 | ea_closed_shift=227
5.3 Manual replay sweep found real cent-symbol signal path

A manual tight replay sweep was run:

XAUUSDc H4:
  InpH024ClosedShift = 229
  InpH024ClosedShift = 228
  InpH024ClosedShift = 227

USDJPYc H4:
  InpH024ClosedShift = 228
  InpH024ClosedShift = 227
  InpH024ClosedShift = 226

Runtime CSV:

reports\h024_ea_log_only_preflight.csv

Verification:

Rows: 264
Violations: 0
Verdict: PASS

Intended-action summary:

Total rows: 264
Intended-action header rows: 6
Intended-action data rows: 41

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

Key unique runtime signal row:

symbol=XAUUSDc
action=BLOCKED
side=short
closed_h4_time=2026.03.18 00:00:00
entry=4991.4050000000
stop=5049.4490000000
raw_lots=0.0000000000
final_lots=0.0000000000
reason=BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short;closed_h4_time=2026.03.18 00:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

Interpretation:

The EA observed a real H024 short signal on XAUUSDc.
The signal path reached the would-open decision layer.
The row was correctly converted to BLOCKED.
It was blocked because runtime account balance was 0.00 USC, so risk budget was zero.
No executable WOULD_OPEN row was produced.
No dry-run execution request should be reconstructed from this blocked row.

This result was documented and committed as:

993b274 Document H024 cent-symbol blocked replay result

Doc:

docs\operations\H024_CENT_SYMBOL_REPLAY_BLOCKED_RUNTIME_RESULT.md
6. New Replay Sweep Automation

Commit:

7bf1728 Add H024 log-only replay sweep mode

Files changed:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
tests\test_h024_ea_replay_sweep_static.py

New EA inputs:

input bool   InpH024ReplaySweepEnabled = false;
input int    InpH024ReplaySweepStartShift = 1;
input int    InpH024ReplaySweepEndShift = 1;
input int    InpH024ReplaySweepMaxRows = 20;

New globals:

int g_h024_replay_sweep_override_shift = 0;
bool g_h024_replay_sweep_written = false;

Effective shift behavior:

Normal mode preserves the legacy InpH024ClosedShift clamp and exact static strings:
if(InpH024ClosedShift < 1)
if(InpH024ClosedShift > 240)
Sweep mode temporarily overrides the effective shift with g_h024_replay_sweep_override_shift.
Sweep start/end/max rows are bounded to 1..240.

New replay-sweep rows:

H024_REPLAY_SWEEP
H024_REPLAY_SWEEP_SHIFT
H024_REPLAY_SWEEP_DONE

Behavior:

In sweep mode, OnInit() writes:
ordinary preflight context rows
one intended-action header
state/intended-action rows for each shift in the configured range
OnTick() and OnTimer() are guarded with if(!InpH024ReplaySweepEnabled) so they do not repeat the sweep rows.
The sweep is written once per attach using g_h024_replay_sweep_written.

Important:

This is not chart automation. It still requires one manual attach per symbol. It reduces repeated attach/remove cycles by sweeping multiple shifts in one attach.

7. Validation For Replay Sweep Commit

Focused tests:

19 passed in 0.68s

Static source verifier:

Violations: 0
Verdict: PASS

Compile/copy helper:

MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Full test suite:

958 passed in 16.44s

Diff summary before commit:

ea_mt5/Experts/H024_LogOnly_Preflight.mq5 | 158 +++++++++++++++++++++++++++---
1 file changed, 145 insertions(+), 13 deletions(-)

Commit:

7bf1728 Add H024 log-only replay sweep mode
8. Important Lesson From The Failed Patch Attempt

A first patch attempt committed tests/test_h024_ea_replay_sweep_static.py without the EA implementation. This made the suite fail with four replay-sweep static-test failures.

Recovery path:

d67eff3 Revert "Add H024 log-only replay sweep mode"

Then the source was inspected exactly, including:

OnInit
OnTick
OnTimer
WriteH024IntendedActionRuntimeRow
WriteH024StateObservationRow

The successful patch used exact source blocks rather than brittle guessed blocks.

For future work: inspect exact source before patching MQL5.

9. Current Deployment Verdict

H024 is meaningfully closer under the 10000 USC cent-account route, but still:

not demo-approved
not live-approved
not Phase 4-approved
not execution-approved

The current blocker is no longer “no cent-symbol runtime signal path.”

The current blocker is:

No executable real-runtime WOULD_OPEN row with nonzero final lots has been observed.

Reason:

The real cent account balance is 0.00 USC, so runtime sizing produces zero risk budget and signal rows become BLOCKED.
10. Recommended Next Step

Use the new replay sweep mode to validate it in MT5 with fewer manual steps.

Recommended first sweep:

XAUUSDc H4 attach

Set inputs:

InpH024ReplaySweepEnabled = true
InpH024ReplaySweepStartShift = 227
InpH024ReplaySweepEndShift = 229
InpH024ReplaySweepMaxRows = 10

Expected:

One manual attach/remove on XAUUSDc H4
Runtime rows include H024_REPLAY_SWEEP
Runtime rows include H024_REPLAY_SWEEP_SHIFT
Runtime rows include H024_REPLAY_SWEEP_DONE
Intended-action rows include at least one BLOCKED short signal around 2026.03.18 00:00:00, unless terminal history shifted since the previous run
USDJPYc H4 attach

Optional second sweep:

InpH024ReplaySweepEnabled = true
InpH024ReplaySweepStartShift = 226
InpH024ReplaySweepEndShift = 228
InpH024ReplaySweepMaxRows = 10

Expected:

One manual attach/remove on USDJPYc H4
Likely NO_ACTION based on prior manual sweep, unless terminal history shifted
11. Suggested Next Runtime Command

After manual attach/remove with sweep mode, collect using:

python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --cent-account-symbols `
  --collect

Then summarize:

python scripts\summarize_h024_ea_intended_action_runtime.py `
  reports\h024_ea_log_only_preflight.csv `
  --cent-account-symbols

If running only one symbol, the standard cent verifier may fail for missing the other symbol. That is expected unless both symbols are attached.

12. What Not To Do Next

Do not add:

OrderSend
OrderCheck
CTrade
MqlTradeRequest
Execution adapter
Demo trading
Live trading
Phase 4 approval
Chart attach automation
GUI automation

Do not treat BLOCKED:volume_below_min_for_would_open as executable.

Do not reconstruct dry-run execution requests from blocked rows.

13. Best Next Engineering Options

Option A — Real-balance evidence:

Fund the cent account and rerun log-only replay sweep. This is the cleanest way to observe real runtime sizing with nonzero risk budget.

Option B — Synthetic research diagnostic:

Add a clearly labeled, tested, research-only balance override for diagnostic sizing only. This must not be confused with live execution readiness.

If adding a synthetic balance diagnostic, it must:

Default off
Be obvious in runtime CSV rows
Be documented as synthetic
Have static tests
Have verifier/summarizer awareness
Never enable order execution
Never imply deployment approval
14. Immediate First Action For Next AI

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
15. Exact First Response The Next AI Should Give

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
