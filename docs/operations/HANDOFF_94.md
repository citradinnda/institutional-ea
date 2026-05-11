# HANDOFF_94 — H024 Phase 4 Demo Adapter Readiness Human Decision Complete

If any older handoff conflicts with this one, this handoff wins.

This document is self-contained. A new AI should be able to continue safely from this handoff without opening older handoffs first.

## 0. One-Sentence State

H024 is Phase 4-approved and demo-adapter implementation/readiness-review approved, with a fail-closed pure-Python adapter skeleton, real-intent refusal audit, boundary static verifier, readiness packet, and human readiness decision all implemented and verified; however H024 is still not execution-approved, not demo-order approved, not live-order approved, not adapter-use approved, not broker-request approved, and no MT5/broker request/order placement is approved.

Latest pushed commit:

- `1cb692d Add H024 Phase 4 demo adapter readiness human decision`

## 1. Current Status — Say This Directly If Asked

H024 has officially left Phase 3 and is in Phase 4 governance.

H024 is not approved to trade.

H024 is not approved to place demo orders.

H024 is not approved to place live orders.

H024 is not approved to construct broker requests.

H024 is not approved to call MT5 execution APIs.

H024 is not approved for adapter use.

H024 is approved for demo-only pure-Python adapter implementation/readiness work.

A fail-closed adapter skeleton exists.

That skeleton correctly refuses dispatch.

The skeleton has been tested against the real standard-demo order-intent context and still refuses dispatch.

The adapter implementation surface has a static boundary verifier proving no prohibited execution imports/calls are present.

A Phase 4 demo adapter readiness packet aggregates the skeleton, real-intent refusal audit, and boundary static verifier.

A human decision artifact now approves adapter-readiness review only.

That human decision does not approve adapter use, broker requests, demo orders, live orders, or execution.

Correct short answer if asked “what changed since HANDOFF_93?”:

- We implemented and verified the real-intent refusal audit.
- We implemented and fixed the adapter boundary static verifier.
- We implemented and verified the Phase 4 demo adapter readiness packet.
- We implemented and verified the human decision artifact approving adapter-readiness review only.
- Execution remains fully blocked.

## 2. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current strategy family:

- H024

Current stage:

- Phase 4 governance approved
- Demo-only adapter implementation/readiness work approved
- Pure-Python fail-closed adapter skeleton implemented
- Real standard-demo intent ingestion/refusal audit implemented
- Adapter implementation boundary static verifier implemented and fixed
- Phase 4 demo adapter readiness packet implemented
- Human adapter-readiness review decision implemented
- Adapter-use/order-placement/execution still blocked

The project must preserve a hard boundary between:

1. Evidence/readiness/approval artifacts.
2. Implementation of pure-Python contracts/skeletons/readiness gates.
3. Any real broker/terminal mutation.

We are inside 1 and tightly bounded 2.

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
- Latest commit should be `Add handoff document #94`
- Previous commit should be:
  - `1cb692d Add H024 Phase 4 demo adapter readiness human decision`

Recent pushed log before this handoff commit:

- `1cb692d Add H024 Phase 4 demo adapter readiness human decision`
- `9490424 Add H024 Phase 4 demo adapter readiness packet`
- `bd7e55d Fix H024 demo adapter boundary static verifier`
- `5e1c55b Add H024 demo adapter boundary static verifier`
- `11fbdd7 Add H024 demo adapter intent refusal audit gate`
- `509af44 Expand handoff document #93`
- `8a9a881 Add handoff document #93`
- `03a2dd3 Add H024 fail-closed demo execution adapter skeleton`

Note:

- Commit `5e1c55b` introduced the static verifier but its first real artifact failed because Python text scanning falsely matched comments/docstrings.
- Commit `bd7e55d` fixed that by using AST-based scanning for Python files and text scanning for MQL files.
- The fixed static verifier is valid.

## 6. Non-Negotiable Safety Boundary

H024 is now:

- Phase 4-approved
- Demo adapter implementation-approved
- Adapter-readiness review-approved
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
- Pure-Python demo adapter implementation/readiness code
- Fail-closed adapter skeletons/contracts
- No-op transports
- Refusal reason evaluation
- Adapter-intent ingestion contracts that still do not construct broker requests
- Read-only JSON/JSONL artifact verification
- Read-only report-based audits
- Static source boundary verifiers
- Review-only readiness packets
- Human decision artifacts that explicitly preserve no-execution authority
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

## 8. H020 / H024 Sizing Boundary

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

## 9. Data Rules

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

## 10. Key Evidence Chain

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

Evidence chain before latest adapter-readiness work:

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
- Phase 4 human decision proof: PASS
- Demo adapter implementation approval proof: PASS
- Fail-closed demo execution adapter skeleton proof: PASS

## 11. Work Completed After HANDOFF_93

### 11.1 Demo adapter intent-ingestion/refusal audit

Commit:

- `11fbdd7 Add H024 demo adapter intent refusal audit gate`

Added:

- `quantcore\execution\h024_demo_adapter_intent_refusal_audit.py`
- `scripts\build_h024_demo_adapter_intent_refusal_audit_jsonl.py`
- `scripts\verify_h024_demo_adapter_intent_refusal_audit_jsonl.py`
- `tests\test_h024_demo_adapter_intent_refusal_audit.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_INTENT_REFUSAL_AUDIT_RESULT.md`

Purpose:

- Feeds the real standard-demo order-intent simulation context into the fail-closed adapter skeleton audit path.
- Proves the adapter can ingest real H024 intent context while still refusing dispatch.
- Does not construct a broker request.
- Does not construct an MT5 request.
- Does not construct an order payload.
- Does not dispatch.
- Does not mutate terminal state.
- Does not mutate broker state.

Output schema:

- `h024_demo_adapter_intent_refusal_audit_v1`

Output kind:

- `DEMO_ADAPTER_INTENT_REFUSAL_AUDIT`

Output status:

- `ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY`

Output decision:

- `REFUSE_DISPATCH_NO_ORDER_AUTHORITY`

Real artifact:

- `reports\h024_standard_demo_demo_adapter_intent_refusal_audit.jsonl`

Validation:

- Focused tests: 8 passed
- Real builder: PASS
- Real verifier: PASS
- Full suite after commit: 1109 passed
- Static EA verifier: PASS

### 11.2 Demo adapter boundary static verifier

Initial commit:

- `5e1c55b Add H024 demo adapter boundary static verifier`

Fix commit:

- `bd7e55d Fix H024 demo adapter boundary static verifier`

Added:

- `quantcore\execution\h024_demo_adapter_boundary_static_verifier.py`
- `scripts\build_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `tests\test_h024_demo_adapter_boundary_static_verifier.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER_RESULT.md`

Purpose:

- Static verification of the demo adapter implementation surface.
- Fails if executable Python imports/calls or MQL execution symbols are present.
- Python files are scanned using AST parsing so comments/docstrings/refusal strings can mention prohibited concepts without false-failing.
- MQL files are scanned as text.

Default scanned targets:

- `quantcore/execution/h024_demo_execution_adapter_skeleton.py`
- `quantcore/execution/h024_demo_adapter_intent_refusal_audit.py`
- `scripts/build_h024_demo_execution_adapter_skeleton_jsonl.py`
- `scripts/verify_h024_demo_execution_adapter_skeleton_jsonl.py`
- `scripts/build_h024_demo_adapter_intent_refusal_audit_jsonl.py`
- `scripts/verify_h024_demo_adapter_intent_refusal_audit_jsonl.py`

Output schema:

- `h024_demo_adapter_boundary_static_verifier_v1`

Output kind:

- `DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER`

Output status:

- `ADAPTER_IMPLEMENTATION_BOUNDARY_STATIC_VERIFIED`

Output decision:

- `ALLOW_IMPLEMENTATION_SURFACE_REVIEW_ONLY_NO_EXECUTION`

Real artifact:

- `reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl`

Validation after fix:

- Focused tests: 13 passed
- Real builder: PASS
- Real verifier: PASS
- Full suite after fix: 1122 passed
- Static EA verifier: PASS

### 11.3 Phase 4 demo adapter readiness packet

Commit:

- `9490424 Add H024 Phase 4 demo adapter readiness packet`

Added:

- `quantcore\execution\h024_phase4_demo_adapter_readiness_packet.py`
- `scripts\build_h024_phase4_demo_adapter_readiness_packet_jsonl.py`
- `scripts\verify_h024_phase4_demo_adapter_readiness_packet_jsonl.py`
- `tests\test_h024_phase4_demo_adapter_readiness_packet.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_ADAPTER_READINESS_PACKET_RESULT.md`

Purpose:

- Aggregates:
  - fail-closed demo execution adapter skeleton
  - real-intent refusal audit
  - adapter boundary static verifier
- Produces one review-only readiness packet.
- Does not approve adapter use.
- Does not approve broker requests.
- Does not approve demo/live order placement.
- Does not approve execution.

Output schema:

- `h024_phase4_demo_adapter_readiness_packet_v1`

Output kind:

- `PHASE4_DEMO_ADAPTER_READINESS_PACKET_REVIEW_ONLY`

Output status:

- `READY_FOR_HUMAN_ADAPTER_READINESS_REVIEW_NO_EXECUTION`

Output decision:

- `REVIEW_ONLY_NO_EXECUTION_AUTHORITY`

Real artifact:

- `reports\h024_standard_demo_phase4_demo_adapter_readiness_packet.jsonl`

Validation:

- Focused tests: 10 passed
- Upstream skeleton verifier: PASS
- Upstream intent refusal audit verifier: PASS
- Upstream boundary static verifier: PASS
- Real readiness packet builder: PASS
- Real readiness packet verifier: PASS
- Full suite after commit: 1132 passed
- Static EA verifier: PASS

### 11.4 Phase 4 demo adapter readiness human decision

Commit:

- `1cb692d Add H024 Phase 4 demo adapter readiness human decision`

Added:

- `quantcore\execution\h024_phase4_demo_adapter_readiness_human_decision.py`
- `scripts\build_h024_phase4_demo_adapter_readiness_human_decision_jsonl.py`
- `scripts\verify_h024_phase4_demo_adapter_readiness_human_decision_jsonl.py`
- `tests\test_h024_phase4_demo_adapter_readiness_human_decision.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_ADAPTER_READINESS_HUMAN_DECISION_RESULT.md`

Purpose:

- Records human approval of adapter-readiness review only.
- Does not approve adapter use.
- Does not approve broker request construction.
- Does not approve MT5 execution.
- Does not approve terminal mutation.
- Does not approve demo order placement.
- Does not approve live order placement.
- Does not approve execution.

Output schema:

- `h024_phase4_demo_adapter_readiness_human_decision_v1`

Output kind:

- `PHASE4_DEMO_ADAPTER_READINESS_HUMAN_DECISION`

Output status:

- `ADAPTER_READINESS_REVIEW_APPROVED_NO_EXECUTION_AUTHORITY`

Output decision:

- `APPROVE_ADAPTER_READINESS_REVIEW_NO_EXECUTION`

Real artifact:

- `reports\h024_standard_demo_phase4_demo_adapter_readiness_human_decision.jsonl`

Validation:

- Focused tests: 10 passed
- Readiness packet verifier: PASS
- Human decision builder: PASS
- Human decision verifier: PASS
- Full suite: 1142 passed
- Static EA verifier: PASS

## 12. Latest Validation Anchors

Latest validation after commit `1cb692d`:

- Focused adapter readiness human decision tests: 10 passed
- Readiness packet verifier: PASS
- Human decision builder: PASS
- Human decision verifier: PASS
- Full suite: 1142 passed in 21.77s
- Static EA verifier: PASS
- Git push: PASS

Current latest pushed commit:

- `1cb692d Add H024 Phase 4 demo adapter readiness human decision`

## 13. Current Approval Matrix

Approved:

- Phase 4 governance: YES
- Demo-only adapter implementation work: YES
- Pure-Python fail-closed adapter skeleton implementation: YES
- Real-intent refusal audit implementation: YES
- Adapter boundary static verification: YES
- Phase 4 demo adapter readiness packet: YES, review-only
- Human adapter-readiness review decision: YES, review-only

Not approved:

- Execution adapter use: NO
- Execution adapter as a transport: NO
- Broker request construction: NO
- MT5 import/access for execution: NO
- Terminal mutation: NO
- Broker mutation: NO
- Demo order placement: NO
- Live order placement: NO
- Execution: NO

## 14. Core Files To Know

Latest Phase 4 adapter-readiness files:

- `quantcore\execution\h024_demo_execution_adapter_skeleton.py`
- `scripts\build_h024_demo_execution_adapter_skeleton_jsonl.py`
- `scripts\verify_h024_demo_execution_adapter_skeleton_jsonl.py`
- `tests\test_h024_demo_execution_adapter_skeleton.py`
- `docs\operations\H024_STANDARD_DEMO_EXECUTION_ADAPTER_SKELETON_RESULT.md`

- `quantcore\execution\h024_demo_adapter_intent_refusal_audit.py`
- `scripts\build_h024_demo_adapter_intent_refusal_audit_jsonl.py`
- `scripts\verify_h024_demo_adapter_intent_refusal_audit_jsonl.py`
- `tests\test_h024_demo_adapter_intent_refusal_audit.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_INTENT_REFUSAL_AUDIT_RESULT.md`

- `quantcore\execution\h024_demo_adapter_boundary_static_verifier.py`
- `scripts\build_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `tests\test_h024_demo_adapter_boundary_static_verifier.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER_RESULT.md`

- `quantcore\execution\h024_phase4_demo_adapter_readiness_packet.py`
- `scripts\build_h024_phase4_demo_adapter_readiness_packet_jsonl.py`
- `scripts\verify_h024_phase4_demo_adapter_readiness_packet_jsonl.py`
- `tests\test_h024_phase4_demo_adapter_readiness_packet.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_ADAPTER_READINESS_PACKET_RESULT.md`

- `quantcore\execution\h024_phase4_demo_adapter_readiness_human_decision.py`
- `scripts\build_h024_phase4_demo_adapter_readiness_human_decision_jsonl.py`
- `scripts\verify_h024_phase4_demo_adapter_readiness_human_decision_jsonl.py`
- `tests\test_h024_phase4_demo_adapter_readiness_human_decision.py`
- `docs\operations\H024_STANDARD_DEMO_PHASE4_ADAPTER_READINESS_HUMAN_DECISION_RESULT.md`

Earlier evidence-chain files still important:

- `quantcore\execution\h024_phase4_review_packet.py`
- `quantcore\execution\h024_phase4_human_decision.py`
- `quantcore\execution\h024_demo_adapter_implementation_approval.py`
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

## 15. Known Pitfalls

PowerShell pitfalls observed:

- Fragile Python meta-writer scripts failed due indentation and newline escaping.
- Prefer direct PowerShell here-strings with `Write-Utf8NoBom`.
- Avoid complex nested code generation when direct file writes are possible.
- Avoid multiline `git add` with backticks.
- Use single-line `git add -- "file1" "file2" ...`.
- Do not run `exit 1` inside helper blocks; use thrown exceptions or `$ok = $true/$false`.

Static verifier pitfall:

- Do not scan Python code as raw text for prohibited concepts.
- Comments/docstrings/refusal strings legitimately mention `OrderSend`, `MqlTradeRequest`, `MetaTrader5`, etc.
- Python targets must be scanned via AST for executable imports/calls.
- MQL targets can be scanned as text.

Readiness packet pitfall:

- Some upstream artifacts may be valid without top-level `verdict`.
- Do not require every upstream artifact to share a `verdict: PASS` convention if schema/kind/status/decision/authority flags/mutation flags/violations prove validity.

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
- Do not treat adapter-readiness review approval as adapter-use approval.
- Do not treat fail-closed skeleton existence as order placement approval.
- Do not treat real-intent ingestion as order placement approval.
- Do not treat boundary static verifier PASS as execution approval.
- Do not treat explicit allow-state safety preflight PASS as order approval.
- Do not treat WOULD_OPEN as permission to trade.
- Do not treat any JSONL artifact as an MT5 request.

## 16. Recommended Next Engineering Step

Next safe, practical, high-leverage work:

Build a pure-Python demo adapter no-op transport contract gate.

Purpose:

- Define the next layer after the skeleton: a no-op transport contract that accepts a verified intent envelope and produces a transport refusal/no-op result.
- It must not construct broker requests.
- It must not construct MT5 requests.
- It must not import `MetaTrader5`.
- It must not dispatch.
- It must not mutate terminal state.
- It must not mutate broker state.
- It must preserve all current non-authorizations.
- It should require the adapter-readiness human decision artifact to be PASS.
- It should prove that even after human adapter-readiness review approval, adapter use and order placement remain blocked.

Suggested files:

- `quantcore\execution\h024_demo_adapter_noop_transport_contract.py`
- `scripts\build_h024_demo_adapter_noop_transport_contract_jsonl.py`
- `scripts\verify_h024_demo_adapter_noop_transport_contract_jsonl.py`
- `tests\test_h024_demo_adapter_noop_transport_contract.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_NOOP_TRANSPORT_CONTRACT_RESULT.md`

Inputs:

- `reports\h024_standard_demo_phase4_demo_adapter_readiness_human_decision.jsonl`
- `reports\h024_standard_demo_demo_adapter_intent_refusal_audit.jsonl`
- possibly `reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl`

Expected behavior:

- Verify readiness human decision artifact is PASS.
- Verify intent refusal audit is PASS.
- Build a pure-Python no-op transport result.
- Preserve:
  - `adapter_readiness_review_approved=true`
  - `execution_adapter_use_approved=false`
  - `execution_adapter_approved=false`
  - `broker_request_approved=false`
  - `mt5_execution_approved=false`
  - `terminal_mutation_approved=false`
  - `demo_order_placement_approved=false`
  - `live_order_placement_approved=false`
  - `execution_approved=false`
- Emit:
  - schema suggestion: `h024_demo_adapter_noop_transport_contract_v1`
  - kind suggestion: `DEMO_ADAPTER_NOOP_TRANSPORT_CONTRACT`
  - status suggestion: `NOOP_TRANSPORT_CONTRACT_READY_REFUSES_EXECUTION`
  - decision suggestion: `REFUSE_TRANSPORT_NO_ADAPTER_USE_AUTHORITY`
- Require:
  - broker request constructed false
  - MT5 request constructed false
  - order payload constructed false
  - transport dispatch attempted false
  - terminal mutated false
  - broker state mutated false
- Add/update the adapter boundary static verifier targets to include the new no-op transport module and scripts.
- Full test suite required because this is code.

Do not implement:

- `MetaTrader5` import
- `OrderSend`
- `OrderCheck`
- `MqlTradeRequest`
- broker request construction
- terminal mutation
- order placement
- demo-order approval
- live-order approval

## 17. Exact Commands For Current Verification

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
1cb692d Add H024 Phase 4 demo adapter readiness human decision

Expected after this handoff commit:

Latest commit:
Add handoff document #94
Previous commit:
1cb692d Add H024 Phase 4 demo adapter readiness human decision

Current focused verification:

python scripts\verify_h024_phase4_demo_adapter_readiness_packet_jsonl.py reports\h024_standard_demo_phase4_demo_adapter_readiness_packet.jsonl --allowed-demo-server Exness-MT5Trial6 --require-ready

python scripts\verify_h024_phase4_demo_adapter_readiness_human_decision_jsonl.py reports\h024_standard_demo_phase4_demo_adapter_readiness_human_decision.jsonl --allowed-demo-server Exness-MT5Trial6 --require-approved

python scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl --require-pass

python scripts\verify_h024_ea_source_static.py

Expected:

Violations: 0
Verdict: PASS

Full suite anchor:

python -m pytest -q

Latest known result:

1142 passed
18. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_94.

I understand:

H024 is Phase 4-approved and demo-adapter implementation/readiness-review approved.
H024 is still not execution-approved, not demo-order approved, not live-order approved, not adapter-use approved, and not broker-request approved.
A pure-Python fail-closed demo execution adapter skeleton exists.
A real standard-demo adapter intent-ingestion/refusal audit exists and passes.
An adapter boundary static verifier exists, was fixed to use Python AST scanning, and passes with zero prohibited findings.
A Phase 4 demo adapter readiness packet exists and passes.
A human decision artifact approves adapter-readiness review only with APPROVE_ADAPTER_READINESS_REVIEW_NO_EXECUTION.
Latest validation anchor is 1142 tests passed plus static EA verifier PASS.
Latest pushed code commit before this handoff is 1cb692d Add H024 Phase 4 demo adapter readiness human decision.
The next safe engineering step is a pure-Python demo adapter no-op transport contract gate requiring the readiness human decision, while still refusing transport because adapter use, broker requests, demo orders, live orders, and execution are not approved.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

Then paste the full output.