# HANDOFF_93 — H024 Phase 4 Approval Through Fail-Closed Demo Adapter Skeleton

If any older handoff conflicts with this one, this handoff wins.

This document is self-contained. A new AI should be able to continue safely from this handoff without opening older handoffs first.

## 0. One-Sentence State

H024 has officially left Phase 3 in governance terms: it is now Phase 4-approved via a human decision artifact, demo-only adapter implementation work is approved, and a pure-Python fail-closed demo execution adapter skeleton has been implemented and verified; however H024 is still not execution-approved, not demo-order approved, not live-approved, not adapter-use approved, and no MT5/broker request/order placement is approved.

Latest pushed commit:

- `03a2dd3 Add H024 fail-closed demo execution adapter skeleton`

## 1. Current Status — Say This Directly If Asked

H024 is now Phase 4-approved.

H024 is not approved to trade.

H024 is not approved to place demo orders.

H024 is not approved to place live orders.

H024 is not approved to construct broker requests.

H024 is not approved to call MT5 execution APIs.

H024 has approval to implement a demo-only fail-closed adapter skeleton/contract.

That skeleton now exists and correctly refuses dispatch.

Correct short answer if asked “are we officially leaving Phase 3?”:

- Yes, H024 has officially left Phase 3 and entered Phase 4 governance.
- No, that does not mean execution is approved.
- Phase 4 currently means post-review implementation preparation with hard fail-closed boundaries.
- The system still may not place demo/live orders or mutate broker/terminal state.

## 2. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current strategy family:

- H024

Current stage:

- Phase 4 governance approved
- Demo-only adapter implementation preparation
- Pure-Python fail-closed adapter skeleton implemented
- Adapter-use/order-placement/execution still blocked

The project must preserve a hard boundary between:

1. Evidence/readiness/approval artifacts.
2. Implementation of pure-Python contracts/skeletons.
3. Any real broker/terminal mutation.

We have crossed from 1 into tightly bounded 2.

We have not crossed into 3.

## 3. Human Preference And Morale Context

The user is tired of ceremony and wants practical progress.

Important preference:

- Do not make tiny incremental changes when a fuller, higher-leverage implementation is appropriate.
- Prefer work that materially advances the gate.
- Avoid wasting time/tokens on trivial edits.
- Prefer one copy/paste PowerShell block when commands are needed.
- For docs-only edits, do not run full pytest unless there is a clear reason.
- For code edits, tests are mandatory.
- Avoid long real-data diagnostics casually.
- For real-data diagnostics, get explicit authorization or make a clear safety-bound decision.
- Never soften deployment boundaries because H024 is promising.
- If there is a safe, practical pure-Python gate that materially advances Phase 4 readiness, proceed with a full patch rather than asking excessive clarifying questions.

Important git workflow preference:

- Bundle stage → diff/check → status → commit → push → verify in one PowerShell block unless there is a real reason not to.
- Use boring single-line `git add -- "file1" "file2" ...`.
- Avoid fragile multiline `git add` with backticks.
- Do not commit `reports/`.

Important morale framing:

- The strategy edge is still unproven in deployment.
- The runtime plumbing is meaningfully proven.
- The safety discipline is strong.
- If H024 fails, the pipeline and infrastructure remain valuable and reusable for H025/H026.
- Useful phrase:
  - “A normal trader is trying to be right. You are building a system that can survive being wrong.”

## 4. Environment

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

`reports/` is local and intentionally untracked.

Do not commit `reports/`.

## 5. Expected Repo State At Start Of Next Session

Expected after this handoff is committed and pushed:

- On branch `main`
- Branch up to date with `origin/main`
- Untracked files: `reports/`
- No other uncommitted changes
- Latest commit should be `Add handoff document #93`
- Previous commit should be:
  - `03a2dd3 Add H024 fail-closed demo execution adapter skeleton`

Recent pushed log before this handoff commit:

- `03a2dd3 Add H024 fail-closed demo execution adapter skeleton`
- `94d0fb2 Add H024 demo adapter implementation approval gate`
- `a550ff9 Add H024 Phase 4 human decision gate`
- `fde4cb1 Add H024 Phase 4 review packet gate`
- `b81e1a5 Add handoff document #92`
- `1ee822b Add H024 operator control state snapshot gate`
- `f95fe54 Add H024 execution safety controls preflight gate`
- `81dec3d Add H024 execution safety controls design gate`
- `73c389a Add H024 Phase 4 readiness review gate`

## 6. Non-Negotiable Safety Boundary

H024 is now:

- Phase 4-approved
- Demo-only adapter implementation-approved
- Still not execution-approved
- Still not demo-order approved
- Still not live-approved
- Still not adapter-use approved
- Still not broker-request approved
- Still not terminal-mutation approved

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
- broker API calls
- broker request construction
- MT5 execution adapter that can place an order
- importing the Python `MetaTrader5` package for execution
- any code path that could mutate terminal or broker state

Allowed now:

- Pure-Python Phase 4 governance code
- Pure-Python demo adapter implementation work
- Fail-closed adapter skeletons/contracts
- No-op transports
- Refusal reason evaluation
- Adapter-intent ingestion contracts that still do not construct broker requests
- Read-only JSON/JSONL artifact verification
- Read-only report-based audits
- Tests proving dispatch/mutation/order-placement stay false
- Docs that make the boundary clearer

## 7. H024 Strategy Mechanics Summary

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

## 9. Key Evidence Chain

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

Evidence chain before Phase 4 approval:

- Dry-run reconciliation: PASS
- Dry-run request JSONL audit: PASS
- Demo-order plan proof: PASS
- Broker metadata preflight proof: PASS
- Order-intent simulation proof: PASS
- Manual approval checkpoint proof: PASS, but manual approval false
- Demo execution adapter design proof: PASS, design only
- Phase 4 readiness review proof: PASS
- Execution safety-controls design proof: PASS
- Execution safety-controls preflight proof: PASS and blocks by default
- Operator control-state snapshot proof: PASS
- Explicit allow-state safety preflight proof: PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL
- Phase 4 review packet proof: PASS

## 10. Work Completed After HANDOFF_92

### 10.1 Phase 4 review packet gate

Commit:

- `fde4cb1 Add H024 Phase 4 review packet gate`

Added:

- `quantcore\execution\h024_phase4_review_packet.py`
- `scripts\build_h024_phase4_review_packet_jsonl.py`
- `scripts\verify_h024_phase4_review_packet_jsonl.py`
- `tests\test_h024_phase4_review_packet.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_REVIEW_PACKET_RESULT.md`

Purpose:

- Aggregates current verified review-only artifacts into one human-review packet.
- Emits:
  - schema `h024_phase4_review_packet_v1`
  - kind `PHASE4_REVIEW_PACKET_REVIEW_ONLY`
  - status `READY_FOR_HUMAN_PHASE4_REVIEW`
- Explicitly does not approve Phase 4 by itself.
- Explicitly does not approve execution.

Validation:

- Focused tests: 7 passed
- Real builder: PASS
- Real verifier: PASS
- Full suite after commit: 1080 passed
- Static EA verifier: PASS

### 10.2 Phase 4 human decision gate

Commit:

- `a550ff9 Add H024 Phase 4 human decision gate`

Added:

- `quantcore\execution\h024_phase4_human_decision.py`
- `scripts\build_h024_phase4_human_decision_jsonl.py`
- `scripts\verify_h024_phase4_human_decision_jsonl.py`
- `tests\test_h024_phase4_human_decision.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_HUMAN_DECISION_RESULT.md`

Purpose:

- Records explicit human decision to approve or reject Phase 4.
- User approved Phase 4 only.
- Output decision:
  - `APPROVE_PHASE4_NO_EXECUTION`
- Output status:
  - `PHASE4_APPROVED_NO_EXECUTION_AUTHORITY`
- Sets:
  - `phase4_approved=true`
- Preserves:
  - `demo_order_placement_approved=false`
  - `live_order_placement_approved=false`
  - `execution_adapter_implementation_approved=false`
  - `execution_adapter_approved=false`
  - `execution_approved=false`

Validation:

- Focused tests: 7 passed
- Real builder: PASS
- Real verifier: PASS
- Full suite: 1087 passed
- Static EA verifier: PASS

### 10.3 Demo adapter implementation approval gate

Commit:

- `94d0fb2 Add H024 demo adapter implementation approval gate`

Added:

- `quantcore\execution\h024_demo_adapter_implementation_approval.py`
- `scripts\build_h024_demo_adapter_implementation_approval_jsonl.py`
- `scripts\verify_h024_demo_adapter_implementation_approval_jsonl.py`
- `tests\test_h024_demo_adapter_implementation_approval.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_IMPLEMENTATION_APPROVAL_RESULT.md`

Purpose:

- Records explicit human approval for demo-only adapter implementation work.
- User approved implementation only.
- Output decision:
  - `APPROVE_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT`
- Output status:
  - `DEMO_ADAPTER_IMPLEMENTATION_APPROVED_NO_ORDER_AUTHORITY`
- Sets:
  - `phase4_approved=true`
  - `demo_execution_adapter_implementation_approved=true`
  - `execution_adapter_implementation_approved=true`
- Preserves:
  - `execution_adapter_approved=false`
  - `demo_order_placement_approved=false`
  - `live_order_placement_approved=false`
  - `execution_approved=false`
  - no MT5 imports
  - no broker requests
  - no order placement

Validation:

- Focused tests: 7 passed
- Real builder: PASS
- Real verifier: PASS
- Full suite: 1094 passed
- Static EA verifier: PASS

### 10.4 Fail-closed demo execution adapter skeleton

Commit:

- `03a2dd3 Add H024 fail-closed demo execution adapter skeleton`

Added:

- `quantcore\execution\h024_demo_execution_adapter_skeleton.py`
- `scripts\build_h024_demo_execution_adapter_skeleton_jsonl.py`
- `scripts\verify_h024_demo_execution_adapter_skeleton_jsonl.py`
- `tests\test_h024_demo_execution_adapter_skeleton.py`
- `docs\operations\H024_STANDARD_DEMO_EXECUTION_ADAPTER_SKELETON_RESULT.md`

Purpose:

- Implements pure-Python fail-closed demo adapter skeleton/contract.
- No MT5 import.
- No broker request construction.
- No order payload.
- No terminal mutation.
- No broker mutation.
- No dispatch.
- Refuses because:
  - `execution_adapter_use_not_approved`
  - `demo_order_placement_not_approved`
  - `execution_not_approved`

Output schema:

- `h024_demo_execution_adapter_skeleton_v1`

Output kind:

- `DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED`

Output status:

- `DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED`

Output decision:

- `REFUSE_DISPATCH_NO_ORDER_AUTHORITY`

Real proof:

- `reports\h024_standard_demo_demo_execution_adapter_skeleton.jsonl`
- Skeleton records: 1
- Violations: 0
- Dispatch attempted: false
- Terminal mutated: false
- Broker state mutated: false
- Verdict: PASS

Validation:

- Focused tests: 7 passed
- Real builder: PASS
- Real verifier: PASS
- Full suite: 1101 passed
- Static EA verifier: PASS

## 11. Current Validation Anchors

Latest validation after commit `03a2dd3`:

- Focused demo execution adapter skeleton tests: 7 passed
- Real standard-demo skeleton builder: PASS
- Real standard-demo skeleton verifier: PASS
- Full suite: 1101 passed in 21.32s
- Static EA verifier: PASS
- Git push: PASS

Current latest pushed commit:

- `03a2dd3 Add H024 fail-closed demo execution adapter skeleton`

## 12. Current Approval Matrix

Approved:

- Phase 4 governance: YES
- Demo-only adapter implementation work: YES
- Pure-Python fail-closed adapter skeleton implementation: YES

Not approved:

- Execution adapter use: NO
- MT5 import/access for execution: NO
- Terminal mutation: NO
- Broker request construction: NO
- Broker metadata terminal collection: NO unless separately authorized
- Demo order placement: NO
- Live order placement: NO
- `OrderSend`: NO
- `OrderCheck`: NO
- `CTrade`: NO
- Execution: NO

## 13. Core Files To Know

Recent Phase 4 / adapter files:

- `quantcore\execution\h024_phase4_review_packet.py`
- `scripts\build_h024_phase4_review_packet_jsonl.py`
- `scripts\verify_h024_phase4_review_packet_jsonl.py`
- `tests\test_h024_phase4_review_packet.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_REVIEW_PACKET_RESULT.md`

- `quantcore\execution\h024_phase4_human_decision.py`
- `scripts\build_h024_phase4_human_decision_jsonl.py`
- `scripts\verify_h024_phase4_human_decision_jsonl.py`
- `tests\test_h024_phase4_human_decision.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_HUMAN_DECISION_RESULT.md`

- `quantcore\execution\h024_demo_adapter_implementation_approval.py`
- `scripts\build_h024_demo_adapter_implementation_approval_jsonl.py`
- `scripts\verify_h024_demo_adapter_implementation_approval_jsonl.py`
- `tests\test_h024_demo_adapter_implementation_approval.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_IMPLEMENTATION_APPROVAL_RESULT.md`

- `quantcore\execution\h024_demo_execution_adapter_skeleton.py`
- `scripts\build_h024_demo_execution_adapter_skeleton_jsonl.py`
- `scripts\verify_h024_demo_execution_adapter_skeleton_jsonl.py`
- `tests\test_h024_demo_execution_adapter_skeleton.py`
- `docs\operations\H024_STANDARD_DEMO_EXECUTION_ADAPTER_SKELETON_RESULT.md`

Earlier evidence-chain files still important:

- `quantcore\execution\h024_phase4_readiness_review.py`
- `quantcore\execution\h024_execution_safety_controls_design.py`
- `quantcore\execution\h024_execution_safety_controls.py`
- `quantcore\execution\h024_operator_control_state.py`
- `quantcore\execution\h024_demo_execution_adapter_design.py`
- `quantcore\execution\h024_manual_approval_checkpoint.py`
- `quantcore\execution\h024_order_intent_simulation.py`
- `quantcore\execution\h024_broker_metadata_preflight.py`
- `quantcore\execution\h024_demo_order_plan.py`
- `quantcore\execution\h024_dry_run.py`

EA/runtime:

- `ea_mt5\Experts\H024_LogOnly_Preflight.mq5`
- `scripts\verify_h024_ea_source_static.py`

## 14. Known Pitfalls

PowerShell pitfalls observed:

- Fragile Python meta-writer scripts failed twice due indentation issues.
- Prefer direct PowerShell here-strings with a `Write-Utf8NoBom` helper.
- Avoid complex nested code generation when direct file writes are possible.
- Avoid multiline `git add` with backticks.
- Use single-line `git add -- "file1" "file2" ...`.
- Do not run `exit 1` in helper blocks; use `$ok = $true/$false`.

MetaEditor pitfall:

- MetaEditor may return code 1 even when compile succeeds.
- Acceptable compile result:
  - MetaEditor compile return code: 1
  - EX5 refreshed: True
  - Compile accepted because EX5 refreshed despite nonzero return code.

Encoding pitfall:

- Windows PowerShell `Set-Content -Encoding UTF8` may create BOMs.
- Use explicit UTF-8 no BOM helper for generated code/docs.
- JSON/JSONL readers should use `utf-8-sig`.

Git/report pitfall:

- Never commit `reports/`.
- `reports/` remains intentionally untracked.

Semantic pitfalls:

- Do not treat Phase 4 approval as execution approval.
- Do not treat adapter implementation approval as adapter-use approval.
- Do not treat adapter skeleton existence as order placement approval.
- Do not treat explicit allow-state safety preflight PASS as order approval.
- Do not treat WOULD_OPEN as permission to trade.
- Do not treat any JSONL artifact as an MT5 request.

## 15. Recommended Next Engineering Step

Next safe, practical, high-leverage work:

Build a pure-Python demo adapter intent-ingestion/refusal audit gate.

Purpose:

- Feed the existing real standard-demo order-intent simulation / dry-run evidence into the fail-closed adapter skeleton as a non-executing intent envelope.
- Produce an adapter refusal audit proving the adapter can ingest the real H024 intent context while still refusing dispatch because:
  - adapter use is not approved
  - demo order placement is not approved
  - execution is not approved

Suggested files:

- `quantcore\execution\h024_demo_adapter_intent_refusal_audit.py`
- `scripts\build_h024_demo_adapter_intent_refusal_audit_jsonl.py`
- `scripts\verify_h024_demo_adapter_intent_refusal_audit_jsonl.py`
- `tests\test_h024_demo_adapter_intent_refusal_audit.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_INTENT_REFUSAL_AUDIT_RESULT.md`

Inputs:

- `reports\h024_standard_demo_demo_execution_adapter_skeleton.jsonl`
- `reports\h024_standard_demo_order_intent_simulation.jsonl`
- possibly `reports\h024_standard_demo_execution_safety_controls_allow_state_preflight.jsonl`

Expected behavior:

- Verify upstream skeleton artifact.
- Verify upstream order-intent simulation artifact.
- Build an adapter intent envelope from the real intent context.
- Do not construct a broker request.
- Do not construct an MT5 request.
- Do not import MT5.
- Do not dispatch.
- Do not mutate terminal state.
- Do not mutate broker state.
- Emit refusal audit JSONL:
  - schema suggestion: `h024_demo_adapter_intent_refusal_audit_v1`
  - kind suggestion: `DEMO_ADAPTER_INTENT_REFUSAL_AUDIT`
  - status suggestion: `ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY`
  - decision suggestion: `REFUSE_DISPATCH_NO_ORDER_AUTHORITY`
- Require:
  - `phase4_approved=true`
  - `demo_execution_adapter_implementation_approved=true`
  - `execution_adapter_approved=false`
  - `demo_order_placement_approved=false`
  - `live_order_placement_approved=false`
  - `execution_approved=false`
  - dispatch attempted false
  - terminal mutated false
  - broker state mutated false

This is implementation work, not a new approval gate.

It is allowed by the current adapter implementation approval.

Full test suite required because this is code.

## 16. Exact Commands For Current Verification

Start with:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

Expected before this handoff commit:

Branch main
Up to date with origin/main
Untracked reports/
Latest commit:
03a2dd3 Add H024 fail-closed demo execution adapter skeleton

Expected after this handoff commit:

Latest commit:
Add handoff document #93
Previous commit:
03a2dd3 Add H024 fail-closed demo execution adapter skeleton

Current focused verification:

python scripts\verify_h024_phase4_human_decision_jsonl.py reports\h024_standard_demo_phase4_human_decision.jsonl --allowed-demo-server Exness-MT5Trial6 --require-approved

python scripts\verify_h024_demo_adapter_implementation_approval_jsonl.py reports\h024_standard_demo_demo_adapter_implementation_approval.jsonl --allowed-demo-server Exness-MT5Trial6 --require-approved

python scripts\verify_h024_demo_execution_adapter_skeleton_jsonl.py reports\h024_standard_demo_demo_execution_adapter_skeleton.jsonl --allowed-demo-server Exness-MT5Trial6 --require-refusal

python scripts\verify_h024_ea_source_static.py

Expected:

Violations: 0
Verdict: PASS

Full suite anchor:

python -m pytest -q

Latest known result:

1101 passed
17. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_93.

I understand:

H024 has officially left Phase 3 and is now Phase 4-approved in governance terms.
H024 is still not execution-approved, not demo-order approved, not live-order approved, not adapter-use approved, and not broker-request approved.
Phase 4 approval was recorded by h024_phase4_human_decision_v1 with decision APPROVE_PHASE4_NO_EXECUTION.
Demo-only adapter implementation approval was recorded by h024_demo_adapter_implementation_approval_v1 with decision APPROVE_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT.
A pure-Python fail-closed demo execution adapter skeleton now exists under h024_demo_execution_adapter_skeleton_v1.
The skeleton refuses dispatch with REFUSE_DISPATCH_NO_ORDER_AUTHORITY.
Latest validation anchor is 1101 tests passed plus static EA verifier PASS.
Latest pushed code commit before this handoff is 03a2dd3 Add H024 fail-closed demo execution adapter skeleton.
The next safe engineering step is a pure-Python demo adapter intent-ingestion/refusal audit gate using existing standard-demo artifacts, with no MT5 import, no broker request construction, no terminal mutation, no order placement, and no execution.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

Then paste the full output.

---

# HANDOFF_93 Supplemental Appendix — Missing Context Filled In

This appendix expands HANDOFF_93 so it is not merely safe-continuation self-contained, but also operationally self-contained.

## A. H020 / H024 Sizing Boundary

H024 uses H020 sizing.

Important H020 behaviors that must not be bypassed:

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

Do not reconstruct lots manually inside an execution adapter.

Do not allow adapter code to reinterpret signal sizing, stop geometry, volume step, minimum lot, maximum lot, or risk fraction.

The adapter layer should consume already-verified intent artifacts and refuse/transport according to authority gates. It should not become a second sizing engine.

## B. EA Current Facts

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

## C. Full Review/Approval Artifact Chain And Local Report Outputs

Reports are local and intentionally untracked.

Do not commit `reports/`.

Current standard-demo report lineage:

1. Runtime CSV

- `reports\h024_ea_log_only_preflight.csv`
- Rows: 229
- Violations: 0
- Runtime verifier: PASS

2. Dry-run reconciliation

- Input: `reports\h024_ea_log_only_preflight.csv`
- Output: `reports\h024_standard_demo_dry_run_requests.jsonl`
- Rows: 229
- Intended-action rows: 6
- WOULD_OPEN rows: 1
- Dry-run requests: 1
- Skipped non-request rows: 5
- Verdict: PASS

3. Demo-order plan

- Input: `reports\h024_standard_demo_dry_run_requests.jsonl`
- Output: `reports\h024_standard_demo_demo_order_plans.jsonl`
- Plans: 1
- Violations: 0
- Verdict: PASS

4. Broker metadata preflight

- Input: `reports\h024_standard_demo_demo_order_plans.jsonl`
- Metadata: `reports\h024_standard_demo_broker_metadata_snapshot.json`
- Output: `reports\h024_standard_demo_broker_metadata_preflight.jsonl`
- Preflight records: 1
- Violations: 0
- Verdict: PASS

5. Order-intent simulation

- Input: `reports\h024_standard_demo_broker_metadata_preflight.jsonl`
- Output: `reports\h024_standard_demo_order_intent_simulation.jsonl`
- Order-intent simulation records: 1
- Violations: 0
- Builder verdict: PASS
- Independent verifier verdict: PASS

6. Manual approval checkpoint

- Input: `reports\h024_standard_demo_order_intent_simulation.jsonl`
- Output: `reports\h024_standard_demo_manual_approval_checkpoint.jsonl`
- Manual approval checkpoint records: 1
- Violations: 0
- Approval status: `PENDING_MANUAL_APPROVAL`
- Manual approval granted: false
- Execution approved: false
- Verdict: PASS

7. Demo execution adapter design

- Input: `reports\h024_standard_demo_manual_approval_checkpoint.jsonl`
- Output: `reports\h024_standard_demo_demo_execution_adapter_design.jsonl`
- Design status: `DESIGN_SPEC_ONLY_NOT_IMPLEMENTED`
- Adapter implementation approved: false at that stage
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

8. Phase 4 readiness review

- Output: `reports\h024_standard_demo_phase4_readiness_review.jsonl`
- Review request status: `READY_FOR_PHASE4_REVIEW_REQUEST`
- Phase 4 approved: false at that stage
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

9. Execution safety-controls design

- Output: `reports\h024_standard_demo_execution_safety_controls_design.jsonl`
- Design status: `SAFETY_CONTROLS_DESIGN_SPEC_ONLY_NOT_IMPLEMENTED`
- Phase 4 approved: false at that stage
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

10. Default blocked safety preflight

- Output:
  - `reports\h024_standard_demo_execution_safety_controls_default_blocked_preflight.jsonl`
  - `reports\h024_standard_demo_execution_safety_controls_default_blocked_audit.jsonl`
- Control decision: `BLOCK`
- Blocked reason: `missing_kill_switch_state`
- Execution approved: false
- Verdict: PASS

11. Operator control-state snapshot

- Outputs:
  - `reports\h024_standard_demo_operator_control_state_snapshot.json`
  - `reports\h024_standard_demo_kill_switch_state_snapshot.json`
  - `reports\h024_standard_demo_idempotency_ledger_snapshot.json`
- Snapshot status: `ALLOW_STATE_REVIEW_ONLY_NOT_EXECUTION_APPROVAL`
- Stable intent id:
  - `af20bcb4a54f6b51aafadeb15a65320bf9c448dbae20cf33066da3cd5adb4363`
- Phase 4 approved: false at that stage
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

12. Explicit allow-state safety preflight

- Inputs:
  - `reports\h024_standard_demo_kill_switch_state_snapshot.json`
  - `reports\h024_standard_demo_idempotency_ledger_snapshot.json`
- Outputs:
  - `reports\h024_standard_demo_execution_safety_controls_allow_state_preflight.jsonl`
  - `reports\h024_standard_demo_execution_safety_controls_allow_state_audit.jsonl`
- Control decision: `PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL`
- Blocked reasons: 0
- Execution approved: false
- Verdict: PASS

13. Phase 4 review packet

- Output:
  - `reports\h024_standard_demo_phase4_review_packet.jsonl`
- Schema:
  - `h024_phase4_review_packet_v1`
- Kind:
  - `PHASE4_REVIEW_PACKET_REVIEW_ONLY`
- Status:
  - `READY_FOR_HUMAN_PHASE4_REVIEW`
- Phase 4 approved: false at that stage
- Demo order placement approved: false
- Live order placement approved: false
- Execution adapter approved: false
- Execution approved: false
- Verdict: PASS

14. Phase 4 human decision

- Output:
  - `reports\h024_standard_demo_phase4_human_decision.jsonl`
- Schema:
  - `h024_phase4_human_decision_v1`
- Decision:
  - `APPROVE_PHASE4_NO_EXECUTION`
- Status:
  - `PHASE4_APPROVED_NO_EXECUTION_AUTHORITY`
- Phase 4 approved: true
- Demo order placement approved: false
- Live order placement approved: false
- Execution adapter implementation approved: false
- Execution adapter approved: false
- Execution approved: false
- Verdict: PASS

15. Demo adapter implementation approval

- Output:
  - `reports\h024_standard_demo_demo_adapter_implementation_approval.jsonl`
- Schema:
  - `h024_demo_adapter_implementation_approval_v1`
- Decision:
  - `APPROVE_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT`
- Status:
  - `DEMO_ADAPTER_IMPLEMENTATION_APPROVED_NO_ORDER_AUTHORITY`
- Phase 4 approved: true
- Demo execution adapter implementation approved: true
- Execution adapter implementation approved: true
- Execution adapter approved: false
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

16. Fail-closed demo execution adapter skeleton

- Output:
  - `reports\h024_standard_demo_demo_execution_adapter_skeleton.jsonl`
- Schema:
  - `h024_demo_execution_adapter_skeleton_v1`
- Kind:
  - `DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED`
- Status:
  - `DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED`
- Decision:
  - `REFUSE_DISPATCH_NO_ORDER_AUTHORITY`
- Refusal reasons:
  - `execution_adapter_use_not_approved`
  - `demo_order_placement_not_approved`
  - `execution_not_approved`
- Dispatch attempted: false
- Terminal mutated: false
- Broker state mutated: false
- Verdict: PASS

## D. Exact Current Truth Table

As of commit `03a2dd3` and handoff commit `8a9a881`:

- Phase 4 approved: true
- Demo adapter implementation approved: true
- Demo execution adapter skeleton implemented: true
- Execution adapter use approved: false
- MT5 import/use for execution approved: false
- Broker request construction approved: false
- Terminal mutation approved: false
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false

Do not collapse these states.

The project is in Phase 4, but still in fail-closed non-execution implementation.

## E. What The Next AI Should Not Do Next

Do not immediately implement:

- `MetaTrader5` import
- `OrderSend`
- `OrderCheck`
- `MqlTradeRequest`
- broker request construction
- terminal mutation
- order placement
- demo-order approval
- live-order approval

Do not ask to “just try one demo order” yet.

The next correct step is still pure Python:

- demo adapter intent-ingestion/refusal audit
- real intent context ingestion
- no broker request
- no dispatch
- no mutation

## F. Best Next Artifact

Recommended next schema:

- `h024_demo_adapter_intent_refusal_audit_v1`

Recommended kind:

- `DEMO_ADAPTER_INTENT_REFUSAL_AUDIT`

Recommended status:

- `ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY`

Recommended decision:

- `REFUSE_DISPATCH_NO_ORDER_AUTHORITY`

Purpose:

Prove the adapter skeleton can ingest the real standard-demo H024 order-intent context and still refuse dispatch.

This closes the gap between a generic fail-closed skeleton and a skeleton evaluated against the actual H024 demo intent evidence.
