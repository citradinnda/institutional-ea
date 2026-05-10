# H024 Cent-Symbol Historical Replay Blocked Runtime Result

Research only. No demo/live/Phase 4 approval.

## Verdict

PASS for cent-symbol runtime replay validation.

The log-only EA produced a real H024 cent-symbol historical replay signal path on `XAUUSDc`, but the signal was converted to `BLOCKED` because the real Exness Standard Cent account balance was `0.00 USC`.

This does not approve demo or live deployment.

## Safety Boundary

This result does not approve:

- `OrderSend`
- `OrderSendAsync`
- `OrderCheck`
- `CTrade`
- `MqlTradeRequest`
- `MqlTradeResult`
- Execution adapter work
- Demo trading
- Live trading
- Phase 4 approval
- Chart attach/detach automation
- GUI automation

The EA remains log-only and research-only.

## Context

The cent-account route uses:

- Account currency: `USC`
- Runtime symbols: `USDJPYc`, `XAUUSDc`
- Intended normalized symbols: `USDJPY`, `XAUUSD`
- Runtime verifier mode: `--cent-account-symbols`

The account was still unfunded at runtime:

```text
account_balance = 0.00 USC

Therefore, any runtime risk budget based on actual account balance was also zero.

Replay Setup

A pure-Python cent-account executable candidate scan found executable candidates under the modeled 10000 USC / 1% account route.

Within the EA's current replay cap of InpH024ClosedShift <= 240, nearby candidate shifts included:

XAUUSD sell | decision=2026-03-17T22:00:00+00:00 | ea_closed_shift=229
USDJPY sell | decision=2026-03-18T02:00:00+00:00 | ea_closed_shift=228
XAUUSD sell | decision=2026-03-18T06:00:00+00:00 | ea_closed_shift=227

A tight manual replay sweep was then performed:

XAUUSDc H4:
  InpH024ClosedShift = 229
  InpH024ClosedShift = 228
  InpH024ClosedShift = 227

USDJPYc H4:
  InpH024ClosedShift = 228
  InpH024ClosedShift = 227
  InpH024ClosedShift = 226

The runtime CSV was collected to:

reports\h024_ea_log_only_preflight.csv

reports/ remains local and untracked.

Runtime Verification

Collection and verification result:

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
Key Runtime Signal Evidence

The unique intended-action extraction found this runtime signal path:

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

The EA observed an H024 short signal on XAUUSDc.
The signal path reached the would-open decision layer.
The row was correctly converted to BLOCKED because runtime sizing had zero risk budget from a 0.00 USC account balance.
No executable WOULD_OPEN row was produced.
No dry-run execution request should be reconstructed from this row.
Why This Matters

Before this result, the missing cent-account evidence was:

cent-symbol historical log-only replay that produces a signal path

This result satisfies the narrower signal-path evidence:

cent-symbol historical log-only replay can reach WOULD_OPEN logic

But it does not satisfy executable runtime evidence:

valid executable WOULD_OPEN row with nonzero final lots

The blocker has therefore changed to:

real runtime account balance is 0.00 USC, so executable lot sizing cannot be observed without funding or a separately tested research-only balance override diagnostic
Automation Lesson

The manual replay workflow is too slow and error-prone.

A safe next engineering target is a research-only replay sweep mode that can evaluate multiple closed H4 shifts in one manual attach, without:

chart attach/detach automation
GUI automation
order-send capability
execution adapter code
account mutation

Acceptable direction:

Add a log-only replay-sweep diagnostic path to the EA or helper that writes intended-action/state rows for a configured shift range.

Required constraints:

Must remain log-only.
Must preserve the kill switch.
Must be source-statically verified against forbidden execution APIs.
Must not add OrderSend, OrderCheck, CTrade, or MqlTradeRequest.
Must include tests before commit.
Must not pretend 0.00 USC runtime sizing is executable.
Must not use a balance override unless clearly labeled as research-only and tested as synthetic.
Current Deployment Verdict

H024 is closer under the 10000 USC cent-account route, but it remains:

not demo-approved
not live-approved
not Phase 4-approved
not execution-approved

Next safe gates:

Preserve this blocked replay result.
Build a research-only replay-sweep automation path to avoid repeated manual attach/remove cycles.
Either fund the cent account for real-balance log-only runtime sizing evidence or add a separately tested synthetic balance diagnostic.
Only after a valid executable cent-symbol runtime WOULD_OPEN row exists, run CSV-read-only dry-run request reconstruction.
Perform execution-safety review before any execution adapter work.
