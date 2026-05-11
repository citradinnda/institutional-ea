# HANDOFF_89 — H024 Standard Demo WOULD_OPEN + Dry-Run Bridge + Phase 4 Readiness Gate

If any older handoff conflicts with this one, this handoff wins.

This document is intended to be fully self-contained. A new AI should be able to continue safely from this document without opening older handoffs first.

## 0. One-Sentence State

H024 remains research-only/log-only and is not demo-order/live/Phase 4/execution approved, but it now has a clean Exness standard demo 10000 USD runtime replay-sweep WOULD_OPEN on XAUUSDm, verified dry-run request reconciliation, verified dry-run request JSONL audit, a reusable JSONL verifier, and a documented Phase 4 readiness gate.

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current strategy family:

- H024

Current stage:

- Execution-safety preparation
- Log-only runtime validation
- Dry-run request contract validation
- Phase 4 readiness planning

Current deployment verdict:

- H024 is meaningfully closer to a Phase 4 review.
- H024 is still not Phase 4-approved.
- H024 is still not demo-order approved.
- H024 is still not live-approved.
- H024 is still not execution-approved.

Do not soften this.

Correct direct answer if asked whether we are near Phase 4:

- Yes, we are meaningfully nearing a Phase 4 review.
- No, H024 is not Phase 4-approved yet.
- The next approved work is pure design-contract code only, not execution code.

## 2. Human Preference And Morale Context

The user is tired of ceremony and wants practical progress.

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

Important git workflow preference:

- The user explicitly asked why we were not doing git operations in one block.
- Going forward, bundle stage → diff → status → commit → push → verify in one PowerShell block unless there is a real reason not to.

Important frustration:

- A previous replay-sweep patch attempt went wrong because tests were committed without implementation.
- The user noticed repeated failures and explicitly challenged whether errors were being read.
- Be careful. Inspect actual source before patching. Do not blindly repeat failing patch scripts.

Important morale context:

- The user is excited by progress but emotionally worried that after a lot of work the EA may still fail.
- Reassure honestly, not by promising profitability.
- The correct motivational framing is:
  - The strategy edge is still unproven in deployment.
  - The runtime plumbing is now meaningfully proven.
  - The safety discipline is strong.
  - If H024 fails, the pipeline and infrastructure remain valuable and reusable for H025/H026.
- A useful phrase:
  - “A normal trader is trying to be right. You are building a system that can survive being wrong.”

## 3. Environment

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 inside `.venv`
- No WSL

Repository root:

- `C:\Users\equin\Documents\institutional-ea`

Virtual environment:

- `C:\Users\equin\Documents\institutional-ea\.venv`

Branch:

- `main`

GitHub remote:

- `https://github.com/citradinnda/institutional-ea.git`

MetaEditor:

- `C:\Program Files\MetaTrader 5\MetaEditor64.exe`

Terminal data dir used in recent runtime work:

- `C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075`

Terminal EA source:

- `C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5`

Compiled EX5:

- `C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5`

Terminal runtime CSV:

- `C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\h024_ea_log_only_preflight.csv`

Repo runtime CSV:

- `reports\h024_ea_log_only_preflight.csv`

Dry-run request JSONL:

- `reports\h024_standard_demo_dry_run_requests.jsonl`

`reports/` is local and intentionally untracked.

Do not commit `reports/`.

## 4. Expected Repo State After This Handoff Is Committed

Expected:

- On branch `main`
- Branch up to date with `origin/main`
- Untracked files: `reports/`
- No other uncommitted changes

Expected latest commit after this handoff is committed:

- `Add handoff document #89`

Expected latest commit before this handoff:

- `e181513 Document H024 Phase 4 readiness gate`

Recent important commits:

- `e181513 Document H024 Phase 4 readiness gate`
- `b7ce340 Add H024 dry-run request JSONL verifier`
- `17a7907 Document H024 standard demo dry-run request audit`
- `aa7ce8c Document H024 standard demo dry-run reconciliation result`
- `c150a27 Validate H024 synthetic balance runtime reasons`
- `1c5ebcc Document H024 standard demo balance replay sweep result`
- `e67ef47 Document H024 synthetic balance replay sweep result`
- `f622eb9 Add handoff document #88`
- `fb95bd9 Add H024 synthetic balance diagnostic`
- `fc5918c Document H024 replay sweep runtime result`
- `ff9f500 Allow H024 replay sweep runtime markers`

## 5. Non-Negotiable Safety Boundary

H024 remains:

- Research-only
- Log-only
- Pre-deployment only
- Not demo-order approved
- Not live-approved
- Not Phase 4-approved
- Not execution-approved
- Not approved for any execution adapter

Forbidden in current stage:

- `OrderSend`
- `OrderSendAsync`
- `OrderCheck`
- `CTrade`
- `#include <Trade...>`
- `MqlTradeRequest`
- `MqlTradeResult`
- `PositionOpen`
- `PositionClose`
- `PositionModify`
- pending-order helpers
- chart attach/detach automation
- GUI automation
- live-terminal mutation
- demo order placement
- live order placement

Allowed:

- Manual EA attach/remove
- Copy EA source to terminal Experts
- Compile EA with MetaEditor
- Reset/collect runtime CSV
- Verify runtime CSV
- Summarize intended-action rows
- Historical log-only replay with `InpH024ClosedShift`
- Log-only replay sweep with `InpH024ReplaySweepEnabled`
- CSV-read-only dry-run request reconciliation
- JSONL-read-only dry-run request verification
- Pure Python contract/design work with no MT5 access and no execution code

## 6. H024 Strategy Mechanics Summary

H024 is a regime-conditioned pullback-continuation hypothesis.

Mechanics:

- Defines directional regime using slow H4 trend state.
- Waits for pullback against that regime.
- Enters only if price resumes in regime direction after pullback.
- Does not use H021 time/session buckets.
- Does not reuse Donchian breakout trigger.
- Uses H020 sizing contract.
- Returns H017-compatible bridge shim.
- Uses H018 hard guard semantics.
- Baseline candidate: hold = 3 H4, stop ATR multiple = 2.0.

Frozen signal defaults:

- `slow_window = 5`
- `slope_lag = 2`
- `atr_window = 3`
- `pullback_window = 3`
- `min_pullback_atr = 0.25`
- `max_pullback_atr = 3.0`
- `min_slope_atr = 0.05`

Signal logic summary:

- `slow_ma = close rolling 5 mean`
- `atr = Wilder ATR(3)`
- `slope = slow_ma - slow_ma.shift(2)`
- `slope_threshold = atr * 0.05`
- `trend_up = close > slow_ma and slope > slope_threshold`
- `trend_down = close < slow_ma and slope < -slope_threshold`
- `previous_bearish = close.shift(1) < open.shift(1)`
- `previous_bullish = close.shift(1) > open.shift(1)`
- `long_signal = trend_up plus bearish pullback plus long resumption`
- `short_signal = trend_down plus bullish pullback plus short resumption`

## 7. H020 / H024 Sizing Boundary

H024 uses H020 sizing.

Important H020 behaviors:

- Computes explicit pre-trade lot intents.
- Suppresses flat signals.
- Suppresses invalid stop geometry.
- Suppresses stop distances below one spread.
- Computes risk-based lots.
- Applies per-trade gross notional caps.
- Applies portfolio gross notional scaling.
- Rounds lots down to broker lot step.
- Suppresses lots below broker minimum lot.
- Preserves final signed risk fraction from final executable lots.

Do not bypass H020 sizing.

## 8. Data Rules

Accepted validation source:

- Exness demo/terminal broker-native exports/runtime only

Accepted model symbols:

- `USDJPY`
- `XAUUSD`

Observed standard demo runtime symbols:

- `USDJPYm`
- `XAUUSDm`

Observed cent account runtime symbols:

- `USDJPYc`
- `XAUUSDc`

Symbol normalization:

- `USDJPYm -> USDJPY`
- `XAUUSDm -> XAUUSD`
- `USDJPYc -> USDJPY`
- `XAUUSDc -> XAUUSD`

Accepted timeframes:

- Broker-native H4
- Broker-native M1

Broker timezone used by loader:

- `Europe/Athens`

Do not use:

- HistData for validation/tuning/production dataset creation
- Broker H4 plus HistData M1 combinations
- Sparse 2018 through 2021-06 broker-native prefix as dense M1
- Incomplete H4/M1 windows

Do not commit:

- Raw MT5 CSV files
- Raw HistData files
- Large derived datasets
- Broker/vendor source files
- `reports/*.csv`
- `reports/*.json`
- `reports/*.jsonl`
- local runtime CSVs
- local compile logs

## 9. Core Files

H024 core:

- `quantcore\strategy\h024.py`
- `quantcore\strategy\h024_runner.py`

H020 sizing contract:

- `quantcore\strategy\h020.py`
- `tests\test_h020.py`

EA/runtime:

- `ea_mt5\Experts\H024_LogOnly_Preflight.mq5`
- `scripts\run_h024_mt5_log_only_preflight_local.py`
- `scripts\verify_h024_ea_preflight_log.py`
- `scripts\summarize_h024_ea_intended_action_runtime.py`
- `scripts\verify_h024_ea_source_static.py`
- `scripts\reconcile_h024_runtime_dry_run_requests.py`
- `scripts\verify_h024_dry_run_request_jsonl.py`
- `scripts\summarize_h024_blocked_sizing_diagnostics.py`

Dry-run contracts:

- `quantcore\execution\h024_intended_action_log.py`
- `quantcore\execution\h024_dry_run_execution_request.py`
- `quantcore\execution\h024_dry_run.py`
- `tests\test_h024_intended_action_log_contract.py`
- `tests\test_h024_dry_run_execution_request_contract.py`
- `tests\test_h024_dry_run_request_jsonl_verifier.py`

Recent important docs:

- `docs\operations\H024_PHASE4_READINESS_GATE.md`
- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_REQUEST_JSONL_AUDIT_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_RECONCILIATION_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_BALANCE_REPLAY_SWEEP_RUNTIME_RESULT.md`
- `docs\operations\H024_SYNTHETIC_BALANCE_REPLAY_SWEEP_RUNTIME_RESULT.md`
- `docs\operations\H024_REPLAY_SWEEP_RUNTIME_RESULT.md`
- `docs\operations\handoffs\HANDOFF_88.md`
- `docs\operations\handoffs\HANDOFF_89.md`

## 10. EA Current Facts

EA source:

- `ea_mt5\Experts\H024_LogOnly_Preflight.mq5`

Runtime schema:

- `h024_ea_log_only_preflight_v2`

EA input version:

- `InpEaVersion = "0.6"`

Intended-action schema:

- `h024_intended_action_log_v1`

Core replay input:

- `InpH024ClosedShift = 1`

Replay cap:

- `1 <= effective closed shift <= 240`

Sweep mode inputs:

- `InpH024ReplaySweepEnabled = false`
- `InpH024ReplaySweepStartShift = 1`
- `InpH024ReplaySweepEndShift = 1`
- `InpH024ReplaySweepMaxRows = 20`

Sweep markers:

- `H024_REPLAY_SWEEP`
- `H024_REPLAY_SWEEP_SHIFT`
- `H024_REPLAY_SWEEP_DONE`

Synthetic balance diagnostic inputs:

- `InpH024SyntheticBalanceEnabled = false`
- `InpH024SyntheticBalance = 0.0`

Synthetic diagnostic behavior:

- Default off.
- Only affects intended-action sizing balance.
- Does not alter account_balance/equity fields in normal preflight columns.
- Appends explicit reason suffix when enabled:
  - `balance_source=synthetic_research_only`
  - `synthetic_balance=...`
  - `real_account_balance=...`
- It is log-only and research-only.
- It is not real account evidence.
- It is not demo/live/Phase 4 approval.

## 11. Major Evidence Achieved Since HANDOFF_88

### 11.1 Synthetic balance replay-sweep evidence

A synthetic 10000 USC/units balance replay sweep produced:

- Runtime verifier PASS
- Intended-action summary PASS
- `XAUUSDc`: 1 synthetic `WOULD_OPEN`
- `USDJPYc`: 3 `NO_ACTION`

Synthetic WOULD_OPEN row:

- symbol: `XAUUSDc`
- normalized: `XAUUSD`
- action: `WOULD_OPEN`
- side: `short`
- closed H4 time: `2026.03.18 08:00:00`
- entry: `4930.0480000000`
- stop: `5019.1630000000`
- raw lots: `0.0112214554`
- final lots: `0.0100000000`
- reason included:
  - `balance_source=synthetic_research_only`
  - `synthetic_balance=10000.00`
  - `real_account_balance=0.00`

Preserved in:

- `docs\operations\H024_SYNTHETIC_BALANCE_REPLAY_SWEEP_RUNTIME_RESULT.md`

Commit:

- `e67ef47 Document H024 synthetic balance replay sweep result`

### 11.2 Synthetic reason verifier guard

The runtime verifier now validates that if an intended-action reason contains:

- `balance_source=synthetic_research_only`

then it must also contain:

- `synthetic_balance=`
- `real_account_balance=`

Files:

- `scripts\verify_h024_ea_preflight_log.py`
- `tests\test_h024_ea_preflight_log_synthetic_reason.py`

Focused verifier tests passed:

- 30 passed

Full suite anchor after this work:

- 964 passed

Static EA verifier:

- PASS

Commit:

- `c150a27 Validate H024 synthetic balance runtime reasons`

### 11.3 Standard demo 10000 USD replay-sweep evidence

The user set a standard demo account balance to 10000 USD and ran standard symbols.

Runtime collection:

- CSV: `reports\h024_ea_log_only_preflight.csv`
- Rows: 229
- Violations: 0
- Verdict: PASS

Account context:

- broker/company: `Exness Technologies Ltd`
- server: `Exness-MT5Trial6`
- account currency: `USD`
- account balance: `10000.00`
- account equity: `10000.00`
- account leverage: `2000`

Intended-action summary:

- Total rows: 229
- Intended-action header rows: 2
- Intended-action data rows: 6
- Verdict: PASS

USDJPYm:

- headers: 1
- rows: 3
- normalized: `USDJPY`
- `WOULD_OPEN`: 0
- `BLOCKED`: 0
- `NO_ACTION`: 3

XAUUSDm:

- headers: 1
- rows: 3
- normalized: `XAUUSD`
- `WOULD_OPEN`: 1
- `BLOCKED`: 0
- `NO_ACTION`: 2

Manual replay sweep inputs for XAUUSDm H4:

- `InpH024ReplaySweepEnabled = true`
- `InpH024ReplaySweepStartShift = 227`
- `InpH024ReplaySweepEndShift = 229`
- `InpH024ReplaySweepMaxRows = 10`
- `InpH024SyntheticBalanceEnabled = false`
- `InpH024SyntheticBalance = 0.0`

Manual replay sweep inputs for USDJPYm H4:

- `InpH024ReplaySweepEnabled = true`
- `InpH024ReplaySweepStartShift = 226`
- `InpH024ReplaySweepEndShift = 228`
- `InpH024ReplaySweepMaxRows = 10`
- `InpH024SyntheticBalanceEnabled = false`
- `InpH024SyntheticBalance = 0.0`

Unique real demo-balance WOULD_OPEN row:

- runtime timestamp: `2026.05.11 07:45:49`
- symbol: `XAUUSDm`
- normalized symbol: `XAUUSD`
- timeframe: `H4`
- action: `WOULD_OPEN`
- side: `short`
- closed H4 time: `2026.03.18 08:00:00`
- entry: `4930.0410000000`
- stop: `5019.0680000000`
- stop distance: `89.0270000000`
- tick size: `0.0010000000`
- tick value USD per lot: `0.1000000000`
- account balance USD: `10000.00`
- risk fraction: `0.01000000`
- risk USD: `100.00`
- raw lots: `0.0112325474`
- final lots: `0.0100000000`
- min volume: `0.0100000000`
- max volume: `200.0000000000`
- volume step: `0.0100000000`
- volume digits: `2`

Reason field:

`WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution`

Preserved in:

- `docs\operations\H024_STANDARD_DEMO_BALANCE_REPLAY_SWEEP_RUNTIME_RESULT.md`

Commit:

- `1c5ebcc Document H024 standard demo balance replay sweep result`

Interpretation:

- This is stronger than synthetic evidence.
- It is actual demo account balance evidence.
- It is still not live evidence, not Phase 4 approval, and not execution approval.

### 11.4 Dry-run request reconciliation from standard demo CSV

Command used:

```powershell
python scripts\reconcile_h024_runtime_dry_run_requests.py `
  reports\h024_ea_log_only_preflight.csv `
  --require-request `
  --output-jsonl reports\h024_standard_demo_dry_run_requests.jsonl

Output:

Rows: 229
Intended-action rows: 6
WOULD_OPEN rows: 1
Dry-run requests: 1
Skipped non-request rows: 5
Verdict: PASS

JSONL output:

reports\h024_standard_demo_dry_run_requests.jsonl

Preserved in:

docs\operations\H024_STANDARD_DEMO_DRY_RUN_RECONCILIATION_RESULT.md

Commit:

aa7ce8c Document H024 standard demo dry-run reconciliation result

Interpretation:

Exactly one dry-run request was reconstructed from the one WOULD_OPEN row.
The five non-request intended-action rows did not become dry-run requests.
This is CSV-read-only. No MT5 access. No order execution.
11.5 Dry-run request JSONL audit

The reconstructed request was:

{"entry_price": 4930.041, "normalized_symbol": "XAUUSD", "request_kind": "DRY_RUN_MARKET_OPEN", "risk_usd": 100.0, "schema_version": "h024_dry_run_execution_request_v1", "side": "SELL", "source_reason": "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution", "source_schema_version": "h024_intended_action_log_v1", "stop_loss": 5019.068, "symbol": "XAUUSDm", "timeframe": "H4", "timestamp": "2026.05.11 07:45:49", "volume_lots": 0.01}

Audit result:

Requests: 1
Violations: 0
Verdict: PASS

Preserved in:

docs\operations\H024_STANDARD_DEMO_DRY_RUN_REQUEST_JSONL_AUDIT_RESULT.md

Commit:

17a7907 Document H024 standard demo dry-run request audit
11.6 Reusable dry-run request JSONL verifier

Added reusable verifier:

scripts\verify_h024_dry_run_request_jsonl.py

Added tests:

tests\test_h024_dry_run_request_jsonl_verifier.py

Verifier checks include:

request schema is h024_dry_run_execution_request_v1
request kind is DRY_RUN_MARKET_OPEN
source schema is h024_intended_action_log_v1
symbol is allowed
normalized symbol is allowed
symbol normalization is consistent
timeframe is H4
side is BUY/SELL
entry, stop, risk, and volume are positive numbers
BUY stop is below entry
SELL stop is above entry
source reason is non-empty
source reason contains WOULD_OPEN:
source reason contains mode=log_only_no_execution
request does not contain execution-like keys such as order, ticket, position, or deal

Validation at commit:

focused JSONL verifier tests: 6 passed
current JSONL verifier on reports\h024_standard_demo_dry_run_requests.jsonl: PASS
full suite: 970 passed
static EA verifier: PASS

Commit:

b7ce340 Add H024 dry-run request JSONL verifier
11.7 Phase 4 readiness gate

Added:

docs\operations\H024_PHASE4_READINESS_GATE.md

Commit:

e181513 Document H024 Phase 4 readiness gate

Key conclusion:

H024 is close enough to begin Phase 4 readiness planning.
H024 is not Phase 4-approved.
Do not add execution code yet.

Gate status:

Gate A — Evidence Chain:

PASS

Gate B — Runtime Safety Boundary:

PASS

Gate C — Demo-Only Execution Adapter Design Spec:

NOT STARTED

Gate D — Order Construction Contract:

NOT STARTED

Gate E — Broker Metadata Preflight Design:

NOT STARTED

Gate F — Demo-Only Dry-Run-to-Order Simulation:

NOT STARTED

Gate G — Manual Approval Checkpoint:

NOT STARTED
12. Current Validation Anchors

Latest full validation anchor from code change b7ce340:

focused JSONL verifier tests: 6 passed
current JSONL verifier: PASS
full suite: 970 passed in 17.77s
static EA verifier: PASS

Latest docs-only commit after that:

e181513 Document H024 Phase 4 readiness gate

No full suite was needed for the docs-only Phase 4 readiness gate commit.

13. Phase 4 Distance Calibration

If the user asks how close we are:

Phase 4 readiness review: around 70% there
Demo-only execution adapter design: around 40% there
Actual demo order placement approval: around 20–25% there
Live trading approval: 0%

Do not present these as formal metrics. They are a practical calibration.

Why we are closer:

Real 10000 USD standard demo account produced a runtime WOULD_OPEN.
Runtime verifier passed.
Dry-run reconciliation passed.
JSONL request audit passed.
Reusable JSONL verifier exists.
Phase 4 readiness gate exists.

Why we are not done:

No demo-only execution adapter design spec yet.
No pure Python demo-order-plan contract yet.
No broker metadata preflight design yet.
No dry-run-to-order simulation yet.
No manual approval checkpoint yet.
No execution code is approved.
14. Known Pitfalls

MetaEditor may return code 1 even when compile succeeds.

Acceptable compile result:

MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Do not treat WOULD_OPEN as permission to trade.

Do not treat dry-run request JSONL as an MT5 order request.

Do not reconstruct dry-run requests from BLOCKED or NO_ACTION.

Do not commit reports/.

Do not add execution code yet.

Do not add a demo execution adapter before the Phase 4 readiness gate design steps are completed.

15. Recommended Next Engineering Step

Next approved work:

Build a pure Python demo-only order construction contract from the audited dry-run request JSONL.

This must not:

import MT5
call MT5
use OrderSend
use OrderCheck
use CTrade
create MqlTradeRequest
place demo orders
place live orders

It should only produce an internal proposed-order object suitable for review.

Suggested files:

quantcore\execution\h024_demo_order_plan.py
tests\test_h024_demo_order_plan.py

The word demo in this contract names the future target environment. It does not approve demo order placement.

Expected contract behavior:

accepts a verified dry-run request dict/object
accepts explicit account/server context
requires demo-only server allowlist
rejects live-like or unknown servers
rejects schema mismatch
rejects unsupported request kind
rejects invalid side
rejects invalid stop geometry
rejects zero/negative volume
rejects unknown symbols
preserves source reason
preserves source timestamp
emits an internal proposed demo-order plan
contains no MT5 side effects
16. Exact Commands For Current Verification

Repo state:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected after this handoff is committed and pushed:

On branch main
Branch up to date with origin/main
Untracked files: reports/
Latest commit: Add handoff document #89
Previous commit: e181513 Document H024 Phase 4 readiness gate

Runtime CSV verifier:

python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_preflight.csv

Expected:

Rows: 229
Violations: 0
Verdict: PASS

Dry-run request JSONL verifier:

python scripts\verify_h024_dry_run_request_jsonl.py reports\h024_standard_demo_dry_run_requests.jsonl --require-request

Expected:

Requests: 1
Violations: 0
Verdict: PASS

Static EA verifier:

python scripts\verify_h024_ea_source_static.py

Expected:

Violations: 0
Verdict: PASS

Full suite, if code changes are made:

python -m pytest -q

Latest anchor:

970 passed in 17.77s
17. Immediate First Action For Next AI

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected:

On branch main
Branch up to date with origin/main
Untracked files: reports/
Latest commit: Add handoff document #89

Then proceed with the pure Python demo-order-plan contract only.

18. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_89.

I understand:

H024 remains research-only/log-only and is not Phase 4-approved.
No OrderSend, OrderCheck, CTrade, MqlTradeRequest, demo orders, or live orders are approved.
We now have a real 10000.00 USD standard demo replay-sweep WOULD_OPEN on XAUUSDm.
Runtime CSV verification passed with 229 rows and 0 violations.
Dry-run reconciliation produced exactly one dry-run request and skipped five non-request rows.
The dry-run request JSONL audit passed.
A reusable dry-run request JSONL verifier was added and tested.
The Phase 4 readiness gate is documented.
Latest code validation anchor is 970 tests passed plus static EA verifier PASS.
The next approved work is a pure Python demo-order-plan contract, with no MT5 access and no execution code.

Please run:

cd C:\Users\equin\Documents\institutional-ea
..venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
