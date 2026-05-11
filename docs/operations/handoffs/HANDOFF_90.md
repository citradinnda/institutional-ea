# HANDOFF_90 — H024 Demo-Order Plan Bridge + Broker Metadata Preflight Gate

If any older handoff conflicts with this one, this handoff wins.

This document is self-contained. A new AI should be able to continue safely from this handoff without opening older handoffs first.

## 0. One-Sentence State

H024 remains research-only/log-only and is not Phase 4-approved, not demo-order approved, not live-approved, and not execution-approved; since HANDOFF_89, we added and verified a pure Python review-only demo-order-plan contract, JSONL bridge, independent plan verifier, broker metadata preflight contract, JSONL bridge, independent preflight verifier, real standard-demo proof artifacts, and pushed everything through commit `a9d3156`.

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
- Review-only demo-order planning
- Offline broker metadata preflight
- Phase 4 readiness design chain

Current deployment verdict:

- H024 is meaningfully closer to a Phase 4 review.
- H024 is still not Phase 4-approved.
- H024 is still not demo-order approved.
- H024 is still not live-approved.
- H024 is still not execution-approved.
- No execution adapter is approved.

Correct direct answer if asked whether we are near Phase 4:

- Yes, we are meaningfully nearing a Phase 4 review.
- No, H024 is not Phase 4-approved yet.
- The next approved work remains pure Python design/contract/simulation code only, not MT5 execution code.

## 2. Human Preference And Morale Context

The user is tired of ceremony and wants practical progress.

Important current preference:

- Do not make tiny incremental changes when a fuller, higher-leverage implementation is appropriate.
- Prefer work that actually advances the gate, even if the patch is larger.
- Avoid wasting time/tokens on trivial edits.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do one real high-leverage action at a time.
- For docs-only edits, do not run full pytest unless there is a clear reason.
- For code edits, tests are mandatory.
- Avoid long real-data diagnostics casually.
- For real-data diagnostics, get explicit authorization or make a clear safety-bound decision.
- Never soften deployment boundaries because H024 is promising.

Important git workflow preference:

- Bundle stage → diff → status → commit → push → verify in one PowerShell block unless there is a real reason not to.
- Use boring single-line `git add -- "file1" "file2" ...` or an explicit PowerShell array invocation.
- Avoid fragile multiline `git add` commands with backticks; a prior command got mangled and failed to stage files.

Important morale framing:

- The strategy edge is still unproven in deployment.
- The runtime plumbing is now meaningfully proven.
- The safety discipline is strong.
- If H024 fails, the pipeline and infrastructure remain valuable and reusable for H025/H026.
- Useful phrase:
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

Review-only proposed demo-order plan JSONL:

- `reports\h024_standard_demo_demo_order_plans.jsonl`

Offline broker metadata snapshot:

- `reports\h024_standard_demo_broker_metadata_snapshot.json`

Broker metadata preflight JSONL:

- `reports\h024_standard_demo_broker_metadata_preflight.jsonl`

`reports/` is local and intentionally untracked.

Do not commit `reports/`.

## 4. Expected Repo State After This Handoff Is Committed

Expected before committing HANDOFF_90:

- On branch `main`
- Branch up to date with `origin/main`
- Untracked files: `reports/`
- No other uncommitted changes
- Latest commit: `a9d3156 Add H024 broker metadata preflight gate`

Expected after committing HANDOFF_90:

- On branch `main`
- Branch up to date with `origin/main`
- Untracked files: `reports/`
- No other uncommitted changes
- Latest commit: `Add handoff document #90`
- Previous commit: `a9d3156 Add H024 broker metadata preflight gate`

Recent important commits:

- `a9d3156 Add H024 broker metadata preflight gate`
- `f422048 Add H024 demo order plan JSONL tools`
- `ba2a0c1 Add H024 demo order plan JSONL bridge`
- `9b1b4f5 Add H024 demo order plan contract`
- `732593c Add handoff document #89`
- `780603a Add handoff document #89`
- `e181513 Document H024 Phase 4 readiness gate`
- `b7ce340 Add H024 dry-run request JSONL verifier`
- `17a7907 Document H024 standard demo dry-run request audit`
- `aa7ce8c Document H024 standard demo dry-run reconciliation result`

Note:

There are two commits named `Add handoff document #89`. This is not currently a blocker.

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
- MT5 execution adapter
- any broker API call

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
- Review-only proposed demo-order plan generation
- Offline broker metadata preflight using explicitly supplied metadata
- Pure Python contract/design/simulation work with no MT5 access and no execution code

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

Review-only proposed demo-order plan work added since HANDOFF_89:

- `quantcore\execution\h024_demo_order_plan.py`
- `tests\test_h024_demo_order_plan.py`
- `scripts\build_h024_demo_order_plan_jsonl.py`
- `scripts\verify_h024_demo_order_plan_jsonl.py`
- `tests\test_h024_demo_order_plan_jsonl_tools.py`
- `docs\operations\H024_STANDARD_DEMO_DEMO_ORDER_PLAN_JSONL_RESULT.md`

Offline broker metadata preflight work added since HANDOFF_89:

- `quantcore\execution\h024_broker_metadata_preflight.py`
- `scripts\build_h024_broker_metadata_preflight_jsonl.py`
- `scripts\verify_h024_broker_metadata_preflight_jsonl.py`
- `tests\test_h024_broker_metadata_preflight.py`
- `docs\operations\H024_STANDARD_DEMO_BROKER_METADATA_PREFLIGHT_RESULT.md`

Recent important docs:

- `docs\operations\H024_PHASE4_READINESS_GATE.md`
- `docs\operations\H024_STANDARD_DEMO_BROKER_METADATA_PREFLIGHT_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_DEMO_ORDER_PLAN_JSONL_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_REQUEST_JSONL_AUDIT_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_RECONCILIATION_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_BALANCE_REPLAY_SWEEP_RUNTIME_RESULT.md`
- `docs\operations\H024_SYNTHETIC_BALANCE_REPLAY_SWEEP_RUNTIME_RESULT.md`
- `docs\operations\H024_REPLAY_SWEEP_RUNTIME_RESULT.md`
- `docs\operations\handoffs\HANDOFF_89.md`
- `docs\operations\handoffs\HANDOFF_90.md`

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

## 11. Evidence Chain Before HANDOFF_90

Standard demo 10000 USD replay-sweep evidence:

- Runtime collection CSV: `reports\h024_ea_log_only_preflight.csv`
- Rows: 229
- Violations: 0
- Runtime verifier: PASS
- Account broker/company: `Exness Technologies Ltd`
- Server: `Exness-MT5Trial6`
- Currency: `USD`
- Balance: `10000.00`
- Equity: `10000.00`
- Leverage: `2000`

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

Dry-run reconciliation:

- Command produced `reports\h024_standard_demo_dry_run_requests.jsonl`
- Rows: 229
- Intended-action rows: 6
- WOULD_OPEN rows: 1
- Dry-run requests: 1
- Skipped non-request rows: 5
- Verdict: PASS

Reusable dry-run request JSONL verifier:

- `scripts\verify_h024_dry_run_request_jsonl.py`
- Current standard demo request JSONL verification: PASS

## 12. New Work Completed Since HANDOFF_89

### 12.1 Pure Python demo-order plan contract

Added:

- `quantcore\execution\h024_demo_order_plan.py`
- `tests\test_h024_demo_order_plan.py`

Commit:

- `9b1b4f5 Add H024 demo order plan contract`

Purpose:

- Convert an already verified H024 dry-run request into an internal review-only proposed demo-order plan.
- Preserve source reason and source timestamp.
- Require explicit account/server context.
- Require demo server allowlist.
- Reject live-like or unknown servers.
- Reject schema mismatch.
- Reject unsupported request kind.
- Reject invalid side.
- Reject invalid stop geometry.
- Reject zero/negative volume.
- Reject unknown symbols.
- Contain no MT5 side effects.

Focused validation at commit:

- 23 passed

Full validation at commit:

- 993 passed

Static EA verifier:

- PASS

### 12.2 Demo-order plan JSONL bridge and verifier

Added:

- `scripts\build_h024_demo_order_plan_jsonl.py`
- `scripts\verify_h024_demo_order_plan_jsonl.py`
- `tests\test_h024_demo_order_plan_jsonl_tools.py`

Documentation:

- `docs\operations\H024_STANDARD_DEMO_DEMO_ORDER_PLAN_JSONL_RESULT.md`

Commits:

- `ba2a0c1 Add H024 demo order plan JSONL bridge`
- `f422048 Add H024 demo order plan JSONL tools`

Real standard-demo result:

Builder:

- Input: `reports\h024_standard_demo_dry_run_requests.jsonl`
- Output: `reports\h024_standard_demo_demo_order_plans.jsonl`
- Requests read: 1
- Plans produced: 1
- Violations: 0
- Verdict: PASS

Verifier:

- Plans: 1
- Violations: 0
- Verdict: PASS

Important fix:

- JSON/JSONL readers were made tolerant of UTF-8 BOMs via `utf-8-sig`.
- Regression test added because Windows PowerShell can emit BOMs.

### 12.3 Broker metadata preflight gate

Added:

- `quantcore\execution\h024_broker_metadata_preflight.py`
- `scripts\build_h024_broker_metadata_preflight_jsonl.py`
- `scripts\verify_h024_broker_metadata_preflight_jsonl.py`
- `tests\test_h024_broker_metadata_preflight.py`
- `docs\operations\H024_STANDARD_DEMO_BROKER_METADATA_PREFLIGHT_RESULT.md`

Commit:

- `a9d3156 Add H024 broker metadata preflight gate`

Purpose:

- Validate a review-only H024 proposed demo-order plan against an explicit offline broker metadata snapshot.
- This is not terminal metadata collection.
- This is not MT5 access.
- This is not an order request.
- This is not execution code.

Preflight validates:

- proposed plan schema and plan kind
- demo server allowlist
- symbol normalization
- account currency
- broker tick size and tick value
- broker min/max/step/digit volume constraints
- entry and stop tick alignment
- stop geometry
- estimated metadata loss within intended `risk_usd`
- risk fraction cap
- preservation of `mode=log_only_no_execution`
- absence of execution-like fields

Offline metadata snapshot used in real proof:

- symbol: `XAUUSDm`
- normalized symbol: `XAUUSD`
- server: `Exness-MT5Trial6`
- account currency: `USD`
- tick size: `0.001`
- tick value: `0.1`
- min volume: `0.01`
- max volume: `200.0`
- volume step: `0.01`
- volume digits: `2`
- price digits: `3`
- spread points: `16.0`

Real standard-demo preflight result:

Builder:

- Input plan JSONL: `reports\h024_standard_demo_demo_order_plans.jsonl`
- Metadata JSON: `reports\h024_standard_demo_broker_metadata_snapshot.json`
- Output: `reports\h024_standard_demo_broker_metadata_preflight.jsonl`
- Plans read: 1
- Preflight records produced: 1
- Violations: 0
- Verdict: PASS

Verifier:

- Input: `reports\h024_standard_demo_broker_metadata_preflight.jsonl`
- Preflight records: 1
- Violations: 0
- Verdict: PASS

Important fixes during this work:

- BOM-tolerant JSON/JSONL readers added with regression coverage.
- A literal backslash-n metadata JSON failure was diagnosed and prevented with a regression test.
- The real metadata snapshot is written with a real newline, not literal `\n`.

## 13. Current Validation Anchors

Latest full validation before commit `a9d3156`:

- Focused tests: 46 passed
- Full suite: 1016 passed in 20.97s
- Static EA verifier: PASS
- Real proposed plan JSONL builder: PASS
- Real proposed plan JSONL verifier: PASS
- Real broker metadata preflight JSONL builder: PASS
- Real broker metadata preflight JSONL verifier: PASS

Post-commit quick validation before push:

- Focused broker metadata/demo-order JSONL tests: 23 passed
- Static EA verifier: PASS
- Demo-order-plan JSONL verifier on real report: PASS
- Broker metadata preflight JSONL verifier on real report: PASS

Latest pushed commit:

- `a9d3156 Add H024 broker metadata preflight gate`

Expected current working tree:

- Clean except untracked `reports/`

## 14. Phase 4 Distance Calibration

Do not present these as formal metrics. They are practical calibration only.

Current practical calibration:

- Phase 4 readiness review: roughly 75–80% there
- Demo-only execution adapter design: roughly 55–60% there
- Actual demo order placement approval: roughly 25–30% there
- Live trading approval: 0%

Why we are closer:

- Real 10000 USD standard demo account produced runtime WOULD_OPEN.
- Runtime verifier passed.
- Dry-run reconciliation passed.
- Dry-run request JSONL audit passed.
- Reusable dry-run request JSONL verifier exists.
- Review-only proposed demo-order plan contract exists.
- Demo-order plan JSONL builder/verifier exist.
- Real plan JSONL proof exists.
- Broker metadata preflight contract exists.
- Broker metadata preflight JSONL builder/verifier exist.
- Real broker metadata preflight proof exists.
- Phase 4 readiness gate exists.

Why we are not done:

- No dry-run-to-order simulation layer yet.
- No final proposed order-intent artifact yet.
- No adapter design spec yet.
- No manual approval checkpoint yet.
- No MT5 execution code is approved.
- No demo order placement is approved.
- No live order placement is approved.

## 15. Current Phase 4 Readiness Gate Status

Gate A — Evidence Chain:

- PASS

Gate B — Runtime Safety Boundary:

- PASS

Gate C — Demo-Only Execution Adapter Design Spec:

- PARTIAL / IN PROGRESS
- We now have proposed demo-order plan contract and JSONL bridge.
- We do not yet have the full adapter design spec.

Gate D — Order Construction Contract:

- PARTIAL / IN PROGRESS
- Review-only proposed demo-order plan exists.
- Broker metadata preflight exists.
- Final dry-run-to-order simulation / final order-intent contract is not started.

Gate E — Broker Metadata Preflight Design:

- PASS for offline explicit metadata preflight.
- Not terminal-collected metadata.
- Still no MT5 access approved.

Gate F — Demo-Only Dry-Run-to-Order Simulation:

- NOT STARTED

Gate G — Manual Approval Checkpoint:

- NOT STARTED

## 16. Known Pitfalls

MetaEditor may return code 1 even when compile succeeds.

Acceptable compile result:

- MetaEditor compile return code: 1
- EX5 refreshed: True
- Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

PowerShell pitfalls observed:

- `exit 1` in helper blocks can terminate the VS Code terminal and hide diagnostics.
- Prefer `$ok = $true/$false` and print STOPPED instead of `exit`.
- Multiline `git add` with backticks got mangled once and failed to stage files.
- Use single-line `git add -- "file1" "file2" ...` for critical commit steps.
- Windows PowerShell `Set-Content -Encoding UTF8` may create BOMs.
- JSON/JSONL readers should use `utf-8-sig` when reading user/report files.
- Be careful not to write literal `\n` after JSON; write a real newline.

Do not treat WOULD_OPEN as permission to trade.

Do not treat dry-run request JSONL as an MT5 order request.

Do not treat proposed demo-order plan JSONL as an MT5 order request.

Do not treat broker metadata preflight JSONL as an MT5 order request.

Do not reconstruct dry-run requests from BLOCKED or NO_ACTION.

Do not commit reports/.

Do not add execution code yet.

Do not add a demo execution adapter before the remaining Phase 4 readiness design steps are completed.

## 17. Recommended Next Engineering Step

Next approved work:

Build a pure Python dry-run-to-order simulation / final proposed order-intent contract from the verified broker metadata preflight JSONL.

This must not:

- import MT5
- call MT5
- use OrderSend
- use OrderCheck
- use CTrade
- create MqlTradeRequest
- place demo orders
- place live orders
- mutate terminal state

It should only produce an internal final review artifact suitable for a later manual approval checkpoint.

Suggested files:

- `quantcore\execution\h024_order_intent_simulation.py`
- `scripts\build_h024_order_intent_simulation_jsonl.py`
- `scripts\verify_h024_order_intent_simulation_jsonl.py`
- `tests\test_h024_order_intent_simulation.py`
- `docs\operations\H024_STANDARD_DEMO_ORDER_INTENT_SIMULATION_RESULT.md`

Expected behavior:

- Accepts a verified broker metadata preflight dict/object.
- Requires preflight schema `h024_broker_metadata_preflight_v1`.
- Requires preflight kind `BROKER_METADATA_PREFLIGHT_REVIEW_ONLY`.
- Preserves symbol, side, entry, stop, volume, risk, source reason, source timestamp.
- Computes final normalized side/order action, but names it as review-only intent, not broker request.
- Re-validates server allowlist.
- Re-validates account currency.
- Re-validates no execution-like keys.
- Re-validates tick alignment.
- Re-validates volume step/min/max/digits.
- Re-validates loss estimate.
- Re-validates max risk fraction.
- Emits schema such as `h024_order_intent_simulation_v1`.
- Emits kind such as `ORDER_INTENT_SIMULATION_REVIEW_ONLY`.
- Includes checks proving it is not an order request and contains no ticket/order/deal/result fields.
- Has CLI builder and independent verifier.
- Has tests for both success and failure paths.
- Runs against `reports\h024_standard_demo_broker_metadata_preflight.jsonl` if present.
- Documents the real standard-demo result.
- Full test suite required because this is code.

Important:

Do this as a meaningful gate, not a tiny script.

## 18. Exact Commands For Current Verification

Repo state:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected before HANDOFF_90 is committed:

On branch main
Branch up to date with origin/main
Untracked files: reports/
Latest commit: a9d3156 Add H024 broker metadata preflight gate

Static EA verifier:

python scripts\verify_h024_ea_source_static.py

Expected:

Violations: 0
Verdict: PASS

Demo-order-plan JSONL verifier:

python scripts\verify_h024_demo_order_plan_jsonl.py reports\h024_standard_demo_demo_order_plans.jsonl --allowed-demo-server Exness-MT5Trial6 --require-plan

Expected:

Plans: 1
Violations: 0
Verdict: PASS

Broker metadata preflight JSONL verifier:

python scripts\verify_h024_broker_metadata_preflight_jsonl.py reports\h024_standard_demo_broker_metadata_preflight.jsonl --allowed-demo-server Exness-MT5Trial6 --require-preflight

Expected:

Preflight records: 1
Violations: 0
Verdict: PASS

Full suite if code changes are made:

python -m pytest -q

Latest anchor:

1016 passed
19. Immediate First Action For Next AI

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected after this handoff is committed and pushed:

On branch main
Branch up to date with origin/main
Untracked files: reports/
Latest commit: Add handoff document #90
Previous commit: a9d3156 Add H024 broker metadata preflight gate

Then proceed with the pure Python order-intent simulation gate only.

20. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_90.

I understand:

H024 remains research-only/log-only and is not Phase 4-approved.
No OrderSend, OrderCheck, CTrade, MqlTradeRequest, demo orders, or live orders are approved.
We have a real 10000.00 USD standard demo replay-sweep WOULD_OPEN on XAUUSDm.
Runtime CSV verification passed with 229 rows and 0 violations.
Dry-run reconciliation produced exactly one dry-run request and skipped five non-request rows.
The dry-run request JSONL audit passed.
A reusable dry-run request JSONL verifier exists.
A review-only demo-order plan contract and JSONL bridge now exist.
The real standard-demo dry-run request produced exactly one review-only proposed demo-order plan and verifier PASS.
A broker metadata preflight contract and JSONL bridge now exist.
The real standard-demo proposed plan produced exactly one broker metadata preflight record and verifier PASS.
Latest full validation anchor is 1016 tests passed plus static EA verifier PASS.
Latest pushed code commit before this handoff is a9d3156 Add H024 broker metadata preflight gate.
The next approved work is a pure Python order-intent simulation gate, with no MT5 access and no execution code.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
