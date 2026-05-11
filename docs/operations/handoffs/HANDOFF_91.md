# HANDOFF_91 — H024 Phase 4 Readiness Design Chain Through Demo Adapter Design Gate

If any older handoff conflicts with this one, this handoff wins.

This document is self-contained. A new AI should be able to continue safely from this handoff without opening older handoffs first.

## 0. One-Sentence State

H024 remains research-only/log-only and is still not Phase 4-approved, not demo-order approved, not live-approved, and not execution-approved; since HANDOFF_90, we added and verified the pure Python order-intent simulation gate, manual approval checkpoint gate, and demo-only execution adapter design gate, with latest pushed commit `f9c3623 Add H024 demo execution adapter design gate`.

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
- Review-only order-intent simulation
- Manual approval checkpoint design
- Demo-only execution adapter design specification
- Phase 4 readiness design chain

Current deployment verdict:

- H024 is meaningfully closer to Phase 4 review.
- H024 is still not Phase 4-approved.
- H024 is still not demo-order approved.
- H024 is still not live-approved.
- H024 is still not execution-approved.
- No execution adapter is approved.
- No demo order placement is approved.
- No live order placement is approved.

Correct direct answer if asked whether we are near Phase 4:

- Yes, we are meaningfully nearing a Phase 4 review.
- No, H024 is not Phase 4-approved yet.
- The next approved work remains pure Python design/contract/simulation/review code only, unless the user explicitly authorizes a tightly bounded next design gate.
- Do not add MT5 execution code without a separate explicit approval gate.

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

- Bundle stage → diff/check → status → commit → push → verify in one PowerShell block unless there is a real reason not to.
- Use boring single-line `git add -- "file1" "file2" ...` or explicit PowerShell arrays.
- Avoid fragile multiline `git add` commands with backticks.
- Do not commit `reports/`.

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

Order-intent simulation JSONL:

- `reports\h024_standard_demo_order_intent_simulation.jsonl`

Manual approval checkpoint JSONL:

- `reports\h024_standard_demo_manual_approval_checkpoint.jsonl`

Demo execution adapter design JSONL:

- `reports\h024_standard_demo_demo_execution_adapter_design.jsonl`

`reports/` is local and intentionally untracked.

Do not commit `reports/`.

## 4. Expected Repo State At Start Of Next Session

Expected after HANDOFF_91 is committed and pushed:

- On branch `main`
- Branch up to date with `origin/main`
- Untracked files: `reports/`
- No other uncommitted changes
- Latest commit: `Add handoff document #91`
- Previous commit: `f9c3623 Add H024 demo execution adapter design gate`

Observed latest pushed log before this handoff commit:

- `f9c3623 Add H024 demo execution adapter design gate`
- `c9ce886 Add H024 demo execution adapter design gate`
- `3ffb9c1 Add H024 demo execution adapter design gate`
- `fbd5210 Add H024 manual approval checkpoint gate`
- `5a0cf05 Add H024 order intent simulation gate`
- `2921ff0 Add handoff document #90`
- `a9d3156 Add H024 broker metadata preflight gate`
- `f422048 Add H024 demo order plan JSONL tools`

Note:

There are multiple commits named `Add H024 demo execution adapter design gate`. This is not currently a blocker. Treat `f9c3623` as latest source of truth.

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

Forbidden unless a later explicit approval gate changes this:

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
- MT5 execution adapter implementation
- any broker API call
- broker request construction

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
- Review-only order-intent simulation
- Manual approval checkpoint artifact generation
- Demo-only execution adapter design artifact generation
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

Demo-order plan:

- `quantcore\execution\h024_demo_order_plan.py`
- `scripts\build_h024_demo_order_plan_jsonl.py`
- `scripts\verify_h024_demo_order_plan_jsonl.py`
- `tests\test_h024_demo_order_plan.py`
- `tests\test_h024_demo_order_plan_jsonl_tools.py`
- `docs\operations\H024_STANDARD_DEMO_DEMO_ORDER_PLAN_JSONL_RESULT.md`

Broker metadata preflight:

- `quantcore\execution\h024_broker_metadata_preflight.py`
- `scripts\build_h024_broker_metadata_preflight_jsonl.py`
- `scripts\verify_h024_broker_metadata_preflight_jsonl.py`
- `tests\test_h024_broker_metadata_preflight.py`
- `docs\operations\H024_STANDARD_DEMO_BROKER_METADATA_PREFLIGHT_RESULT.md`

Order-intent simulation added since HANDOFF_90:

- `quantcore\execution\h024_order_intent_simulation.py`
- `scripts\build_h024_order_intent_simulation_jsonl.py`
- `scripts\verify_h024_order_intent_simulation_jsonl.py`
- `tests\test_h024_order_intent_simulation.py`
- `docs\operations\H024_STANDARD_DEMO_ORDER_INTENT_SIMULATION_RESULT.md`

Manual approval checkpoint added since HANDOFF_90:

- `quantcore\execution\h024_manual_approval_checkpoint.py`
- `scripts\build_h024_manual_approval_checkpoint_jsonl.py`
- `scripts\verify_h024_manual_approval_checkpoint_jsonl.py`
- `tests\test_h024_manual_approval_checkpoint.py`
- `docs\operations\H024_STANDARD_DEMO_MANUAL_APPROVAL_CHECKPOINT_RESULT.md`

Demo execution adapter design gate added since HANDOFF_90:

- `quantcore\execution\h024_demo_execution_adapter_design.py`
- `scripts\build_h024_demo_execution_adapter_design_jsonl.py`
- `scripts\verify_h024_demo_execution_adapter_design_jsonl.py`
- `tests\test_h024_demo_execution_adapter_design.py`
- `docs\operations\H024_DEMO_EXECUTION_ADAPTER_DESIGN_SPEC.md`
- `docs\operations\H024_STANDARD_DEMO_EXECUTION_ADAPTER_DESIGN_RESULT.md`

Recent important docs:

- `docs\operations\H024_PHASE4_READINESS_GATE.md`
- `docs\operations\H024_DEMO_EXECUTION_ADAPTER_DESIGN_SPEC.md`
- `docs\operations\H024_STANDARD_DEMO_EXECUTION_ADAPTER_DESIGN_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_MANUAL_APPROVAL_CHECKPOINT_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_ORDER_INTENT_SIMULATION_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_BROKER_METADATA_PREFLIGHT_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_DEMO_ORDER_PLAN_JSONL_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_REQUEST_JSONL_AUDIT_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_RECONCILIATION_RESULT.md`
- `docs\operations\handoffs\HANDOFF_90.md`
- `docs\operations\handoffs\HANDOFF_91.md`

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

## 11. Evidence Chain Before HANDOFF_91

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

Demo-order plan proof:

- Input: `reports\h024_standard_demo_dry_run_requests.jsonl`
- Output: `reports\h024_standard_demo_demo_order_plans.jsonl`
- Plans: 1
- Violations: 0
- Verdict: PASS

Broker metadata preflight proof:

- Input: `reports\h024_standard_demo_demo_order_plans.jsonl`
- Metadata: `reports\h024_standard_demo_broker_metadata_snapshot.json`
- Output: `reports\h024_standard_demo_broker_metadata_preflight.jsonl`
- Preflight records: 1
- Violations: 0
- Verdict: PASS

Order-intent simulation proof:

- Input: `reports\h024_standard_demo_broker_metadata_preflight.jsonl`
- Output: `reports\h024_standard_demo_order_intent_simulation.jsonl`
- Order-intent simulation records: 1
- Violations: 0
- Builder verdict: PASS
- Independent verifier verdict: PASS

Manual approval checkpoint proof:

- Input: `reports\h024_standard_demo_order_intent_simulation.jsonl`
- Output: `reports\h024_standard_demo_manual_approval_checkpoint.jsonl`
- Manual approval checkpoint records: 1
- Violations: 0
- Builder verdict: PASS
- Independent verifier verdict: PASS
- Approval status: `PENDING_MANUAL_APPROVAL`
- Manual approval granted: false
- Execution approved: false

Demo execution adapter design proof:

- Input: `reports\h024_standard_demo_manual_approval_checkpoint.jsonl`
- Output: `reports\h024_standard_demo_demo_execution_adapter_design.jsonl`
- Design records: 1
- Violations: 0
- Builder verdict: PASS
- Independent verifier verdict: PASS
- Design status: `DESIGN_SPEC_ONLY_NOT_IMPLEMENTED`
- Adapter implementation approved: false
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false

## 12. New Work Completed Since HANDOFF_90

### 12.1 Order-intent simulation gate

Commit:

- `5a0cf05 Add H024 order intent simulation gate`

Added:

- `quantcore\execution\h024_order_intent_simulation.py`
- `scripts\build_h024_order_intent_simulation_jsonl.py`
- `scripts\verify_h024_order_intent_simulation_jsonl.py`
- `tests\test_h024_order_intent_simulation.py`
- `docs\operations\H024_STANDARD_DEMO_ORDER_INTENT_SIMULATION_RESULT.md`

Purpose:

- Convert verified broker metadata preflight JSONL into final internal review-only order-intent simulation JSONL.
- Preserve symbol, side, entry, stop, volume, risk, source reason, and source timestamp.
- Re-check demo server allowlist, account currency, symbol normalization, tick alignment, volume constraints, stop geometry, estimated loss, and max risk fraction.
- Canonicalize broker-style `BUY`/`SELL` side labels into review-only `long`/`short`.
- Assert output is not a broker request.
- Keep all output review-only and non-executing.

Important real-proof result:

- Focused tests: 18 passed
- Full suite: 1034 passed
- Static EA verifier: PASS
- Real builder: PASS
- Real verifier: PASS

### 12.2 Manual approval checkpoint gate

Commit:

- `fbd5210 Add H024 manual approval checkpoint gate`

Added:

- `quantcore\execution\h024_manual_approval_checkpoint.py`
- `scripts\build_h024_manual_approval_checkpoint_jsonl.py`
- `scripts\verify_h024_manual_approval_checkpoint_jsonl.py`
- `tests\test_h024_manual_approval_checkpoint.py`
- `docs\operations\H024_STANDARD_DEMO_MANUAL_APPROVAL_CHECKPOINT_RESULT.md`

Purpose:

- Build a review-only manual approval checkpoint from verified order-intent simulation.
- Explicitly record that manual approval is still required.
- Explicitly record that manual approval is not granted.
- Explicitly record that execution is not approved.
- Preserve order-intent fields and broker metadata summary.
- Reject execution-like fields.
- Reject source intent failures.

Important real-proof result:

- Manual approval checkpoint tests: 6 passed
- Order-intent simulation tests: 18 passed
- Full suite: 1040 passed
- Static EA verifier: PASS
- Existing real order-intent verifier: PASS
- Real manual checkpoint builder: PASS
- Real manual checkpoint verifier: PASS

### 12.3 Demo execution adapter design gate

Latest commit:

- `f9c3623 Add H024 demo execution adapter design gate`

Also observed two earlier commits with same message:

- `c9ce886 Add H024 demo execution adapter design gate`
- `3ffb9c1 Add H024 demo execution adapter design gate`

Added:

- `quantcore\execution\h024_demo_execution_adapter_design.py`
- `scripts\build_h024_demo_execution_adapter_design_jsonl.py`
- `scripts\verify_h024_demo_execution_adapter_design_jsonl.py`
- `tests\test_h024_demo_execution_adapter_design.py`
- `docs\operations\H024_DEMO_EXECUTION_ADAPTER_DESIGN_SPEC.md`
- `docs\operations\H024_STANDARD_DEMO_EXECUTION_ADAPTER_DESIGN_RESULT.md`

Purpose:

- Build a review-only, design-only artifact for a future demo-only execution adapter.
- Verify the design boundary from a verified manual approval checkpoint.
- Explicitly state the adapter is not implemented.
- Explicitly state adapter implementation is not approved.
- Explicitly state demo order placement is not approved.
- Explicitly state live order placement is not approved.
- Explicitly state execution is not approved.
- Require future separate approval before any adapter implementation.
- Require future separate approval before any demo order.
- Require future separate approval before any live order.
- Keep pure Python and avoid MT5/broker request construction.

Important real-proof result:

- Demo execution adapter design tests: 6 passed
- Manual approval checkpoint tests: 6 passed
- Full suite: 1046 passed
- Static EA verifier: PASS
- Existing real manual checkpoint verifier: PASS
- Real demo execution adapter design builder: PASS
- Real demo execution adapter design verifier: PASS

## 13. Current Validation Anchors

Latest validation after commit `f9c3623`:

- Focused demo execution adapter design tests: 6 passed
- Manual approval checkpoint tests: 6 passed
- Full suite: 1046 passed in 21.55s
- Static EA verifier: PASS
- Existing real manual approval checkpoint verifier: PASS
- Real standard-demo execution adapter design builder: PASS
- Real standard-demo execution adapter design independent verifier: PASS

Latest pushed commit:

- `f9c3623 Add H024 demo execution adapter design gate`

Expected current working tree:

- Clean except untracked `reports/`

## 14. Phase 4 Distance Calibration

Do not present these as formal metrics. They are practical calibration only.

Current practical calibration:

- Phase 4 readiness review: roughly 85–90% there
- Demo-only execution adapter design: roughly 80–85% there
- Actual demo order placement approval: roughly 35–40% there
- Live trading approval: 0%

Why we are closer:

- Real 10000 USD standard demo account produced runtime WOULD_OPEN.
- Runtime verifier passed.
- Dry-run reconciliation passed.
- Dry-run request JSONL audit passed.
- Reusable dry-run request JSONL verifier exists.
- Review-only proposed demo-order plan contract exists.
- Demo-order plan JSONL builder/verifier exist.
- Broker metadata preflight contract exists.
- Broker metadata preflight JSONL builder/verifier exist.
- Order-intent simulation contract exists.
- Order-intent simulation JSONL builder/verifier exist.
- Manual approval checkpoint contract exists.
- Manual approval checkpoint JSONL builder/verifier exist.
- Demo-only execution adapter design artifact exists.
- Demo-only execution adapter design JSONL builder/verifier exist.
- Phase 4 readiness gate exists.

Why we are not done:

- No actual execution adapter implementation exists or is approved.
- No MT5 order request construction exists or is approved.
- No demo order placement is approved.
- No live order placement is approved.
- No final human approval artifact granting demo-order placement exists.
- No kill switch implementation exists.
- No idempotency implementation exists.
- No immutable execution audit log implementation exists.
- No Phase 4 signoff exists.

## 15. Current Phase 4 Readiness Gate Status

Gate A — Evidence Chain:

- PASS

Gate B — Runtime Safety Boundary:

- PASS

Gate C — Demo-Only Execution Adapter Design Spec:

- PASS for review-only design artifact.
- Not implementation.
- Not approval to implement.

Gate D — Order Construction Contract:

- PARTIAL / IN PROGRESS
- Review-only proposed demo-order plan exists.
- Broker metadata preflight exists.
- Order-intent simulation exists.
- Still no broker request construction approved.
- Still no MT5 request construction approved.

Gate E — Broker Metadata Preflight Design:

- PASS for offline explicit metadata preflight.
- Not terminal-collected metadata.
- Still no MT5 access approved.

Gate F — Demo-Only Dry-Run-to-Order Simulation:

- PASS for order-intent simulation.
- No broker request.
- No execution code.

Gate G — Manual Approval Checkpoint:

- PASS for pending manual approval checkpoint artifact.
- Does not grant approval.
- Future explicit approval still required.

Remaining major gap:

- A final Phase 4 readiness review document/checklist that reads all current PASS artifacts and explicitly decides whether Phase 4 review can be requested.
- This should still not approve execution.

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
- Some Markdown docs showed as binary diffs due encoding. Prefer writing docs with explicit UTF-8 no BOM helper.

Do not treat WOULD_OPEN as permission to trade.

Do not treat dry-run request JSONL as an MT5 order request.

Do not treat proposed demo-order plan JSONL as an MT5 order request.

Do not treat broker metadata preflight JSONL as an MT5 order request.

Do not treat order-intent simulation JSONL as an MT5 order request.

Do not treat manual approval checkpoint JSONL as approval.

Do not treat demo execution adapter design JSONL as an adapter or approval.

Do not reconstruct dry-run requests from BLOCKED or NO_ACTION.

Do not commit reports/.

Do not add execution code yet.

Do not add a demo execution adapter implementation before an explicit later approval step.

## 17. Recommended Next Engineering Step

Next approved work:

Build a pure Python Phase 4 readiness review aggregator/checklist gate that reads the current verified review-only artifacts and emits a single `PHASE4_REVIEW_REQUEST_READY` or `NOT_READY` artifact.

This must not approve execution.

It should not:

- import MT5
- call MT5
- use OrderSend
- use OrderCheck
- use CTrade
- create MqlTradeRequest
- construct broker requests
- place demo orders
- place live orders
- mutate terminal state
- approve demo order placement
- approve live order placement

Suggested files:

- `quantcore\execution\h024_phase4_readiness_review.py`
- `scripts\build_h024_phase4_readiness_review_jsonl.py`
- `scripts\verify_h024_phase4_readiness_review_jsonl.py`
- `tests\test_h024_phase4_readiness_review.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_READINESS_REVIEW_RESULT.md`

Expected behavior:

- Accepts verified artifacts or a manifest of paths for:
  - dry-run request JSONL
  - demo-order plan JSONL
  - broker metadata preflight JSONL
  - order-intent simulation JSONL
  - manual approval checkpoint JSONL
  - demo execution adapter design JSONL
- Verifies each artifact with its independent verifier.
- Requires exactly one real standard-demo record in each downstream gate where expected.
- Requires all verdicts PASS.
- Requires manual approval checkpoint status remains `PENDING_MANUAL_APPROVAL`.
- Requires manual approval granted remains false.
- Requires execution approved remains false.
- Requires demo adapter design status remains `DESIGN_SPEC_ONLY_NOT_IMPLEMENTED`.
- Requires no execution-like fields.
- Emits a review request readiness artifact, not approval.
- Suggested schema:
  - `h024_phase4_readiness_review_v1`
- Suggested kind:
  - `PHASE4_READINESS_REVIEW_REQUEST_REVIEW_ONLY`
- Suggested status:
  - `READY_FOR_PHASE4_REVIEW_REQUEST`
- Must explicitly state:
  - Phase 4 not approved
  - Demo order placement not approved
  - Live order placement not approved
  - Execution adapter not approved
  - Human review still required

This is a meaningful gate, not a tiny script.

Full test suite required because this is code.

## 18. Exact Commands For Current Verification

Repo state:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

Expected after HANDOFF_91 is committed and pushed:

On branch main
Branch up to date with origin/main
Untracked files: reports/
Latest commit: Add handoff document #91
Previous commit: f9c3623 Add H024 demo execution adapter design gate

Static EA verifier:

python scripts\verify_h024_ea_source_static.py

Expected:

Violations: 0
Verdict: PASS

Order-intent verifier:

python scripts\verify_h024_order_intent_simulation_jsonl.py reports\h024_standard_demo_order_intent_simulation.jsonl --allowed-demo-server Exness-MT5Trial6 --require-intent

Expected:

Order-intent simulation records: 1
Violations: 0
Verdict: PASS

Manual approval checkpoint verifier:

python scripts\verify_h024_manual_approval_checkpoint_jsonl.py reports\h024_standard_demo_manual_approval_checkpoint.jsonl --allowed-demo-server Exness-MT5Trial6 --require-checkpoint

Expected:

Manual approval checkpoint records: 1
Violations: 0
Verdict: PASS

Demo execution adapter design verifier:

python scripts\verify_h024_demo_execution_adapter_design_jsonl.py reports\h024_standard_demo_demo_execution_adapter_design.jsonl --allowed-demo-server Exness-MT5Trial6 --require-design

Expected:

Design records: 1
Violations: 0
Verdict: PASS

Full suite if code changes are made:

python -m pytest -q

Latest anchor:

1046 passed
19. Immediate First Action For Next AI

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

Expected after this handoff is committed and pushed:

On branch main
Branch up to date with origin/main
Untracked files: reports/
Latest commit: Add handoff document #91
Previous commit: f9c3623 Add H024 demo execution adapter design gate

Then proceed with the pure Python Phase 4 readiness review aggregator/checklist gate only.

20. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_91.

I understand:

H024 remains research-only/log-only and is not Phase 4-approved.
No OrderSend, OrderCheck, CTrade, MqlTradeRequest, broker request construction, demo orders, or live orders are approved.
We have a real 10000.00 USD standard demo replay-sweep WOULD_OPEN on XAUUSDm.
Runtime CSV verification passed with 229 rows and 0 violations.
Dry-run reconciliation produced exactly one dry-run request and skipped five non-request rows.
The dry-run request JSONL audit passed.
A reusable dry-run request JSONL verifier exists.
A review-only demo-order plan contract and JSONL bridge exist.
The real standard-demo dry-run request produced exactly one review-only proposed demo-order plan and verifier PASS.
A broker metadata preflight contract and JSONL bridge exist.
The real standard-demo proposed plan produced exactly one broker metadata preflight record and verifier PASS.
An order-intent simulation contract and JSONL bridge exist.
The real standard-demo preflight produced exactly one order-intent simulation record and verifier PASS.
A manual approval checkpoint contract and JSONL bridge exist.
The real standard-demo order-intent produced exactly one pending manual approval checkpoint record and verifier PASS.
A demo-only execution adapter design contract and JSONL bridge exist.
The real standard-demo manual checkpoint produced exactly one demo execution adapter design record and verifier PASS.
Latest full validation anchor is 1046 tests passed plus static EA verifier PASS.
Latest pushed code commit before this handoff is f9c3623 Add H024 demo execution adapter design gate.
The next approved work is a pure Python Phase 4 readiness review aggregator/checklist gate, with no MT5 access, no broker request construction, no execution code, and no approval-granting semantics.

Please run:

cd C:\Users\equin\Documents\institutional-ea
..venv\Scripts\Activate.ps1
git status
git log --oneline -8

Then paste the full output.