# HANDOFF_95 — H024 Broker-Request Preview Envelope Complete, Execution Still Blocked

If this handoff conflicts with any older handoff, this handoff wins.

This document is intentionally self-contained. A new AI should be able to continue safely from this document without opening HANDOFF_94 or any older handoff first.

## 0. One-Sentence State

H024 is Phase 4-approved and now has a verified pure-Python non-mutating path through no-op adapter use, no-op invocation, broker-request construction readiness, preview-only broker-request construction approval, and an inert broker-request preview envelope built from real standard-demo intent; however H024 is still not approved to construct an actual broker request, not approved to construct an MT5 request, not approved to construct an order payload, not approved to dispatch, not approved to place demo/live orders, and not execution-approved.

Latest pushed code commit before this handoff:

- `56f609a Add H024 broker-request preview envelope`

Latest validation anchor:

- Focused preview tests: `43 passed`
- Broker-request preview construction approval: PASS
- Broker-request preview envelope: PASS
- Adapter boundary static verifier: PASS
- Adapter-boundary files scanned: 23
- Prohibited findings: 0
- Static EA verifier: PASS
- Full test suite: `1329 passed in 23.20s`
- Git push: PASS

## 1. Current Status — Say This Directly If Asked

H024 has officially left Phase 3 and is in Phase 4 governance.

H024 is not approved to trade.

H024 is not approved to place demo orders.

H024 is not approved to place live orders.

H024 is not approved to call MT5 execution APIs.

H024 is not approved to mutate terminal or broker state.

H024 is not approved to construct an actual broker request.

H024 is not approved to construct an MT5 request.

H024 is not approved to construct an order payload.

H024 is not approved to dispatch transport.

H024 is approved for pure-Python, review-only, non-mutating readiness/preview work.

Current highest deployment-adjacent artifact:

- An inert broker-request preview envelope exists.
- It consumes the real standard-demo H024 order-intent simulation.
- It consumes the safety allow-state preflight.
- It attaches a stable preview idempotency key.
- It records that H020 sizing is consumed, not reinterpreted.
- It is explicitly not an MT5 request.
- It is explicitly not a broker request.
- It is explicitly not an order payload.
- It is not dispatchable.
- It does not mutate terminal or broker state.
- It does not approve execution.

Correct short answer if asked “how close are we to deployment?”:

- For live deployment: not close.
- For first tightly controlled demo canary: we are now in the final pre-execution corridor.
- The next steps are still pure Python and non-mutating, but they directly shape the eventual order path.
- The next safe step is an inert canonical broker-request draft construction approval and draft envelope.
- No actual MT5 request, dispatch, or order placement is approved yet.

## 2. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current strategy family:

- H024

Current stage:

- Phase 4 governance approved.
- Demo-only adapter implementation/readiness work approved.
- Pure-Python fail-closed adapter skeleton implemented.
- Real standard-demo intent ingestion/refusal audit implemented.
- Adapter implementation boundary static verifier implemented and expanded.
- Phase 4 demo adapter readiness packet implemented.
- Human adapter-readiness review decision implemented.
- No-op transport contract implemented.
- Adapter-use readiness packet implemented.
- Human adapter-use readiness decision implemented.
- Pure-Python no-op adapter-use approval implemented.
- No-op adapter-use invocation audit implemented.
- Broker-request construction readiness packet implemented.
- Preview-only broker-request construction approval implemented.
- Inert broker-request preview envelope implemented.
- Actual broker request construction still blocked.
- MT5 request construction still blocked.
- Order payload construction still blocked.
- Dispatch still blocked.
- Demo/live order placement still blocked.
- Execution still blocked.

The project must preserve a hard boundary between:

1. Evidence/readiness/approval artifacts.
2. Pure-Python contracts, skeletons, readiness gates, and inert preview/draft artifacts.
3. Any real broker/terminal mutation.

We are inside 1 and bounded 2.

We have not crossed into 3.

## 3. Human Preference And Morale Context

The user is tired of ceremony and wants practical progress toward deployment.

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

- Bundle stage -> check -> status -> commit -> push -> verify in one PowerShell block unless there is a real reason not to.
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

Repo EA source:

- `ea_mt5\Experts\H024_LogOnly_Preflight.mq5`

`reports/` is local and intentionally untracked.

Do not commit:

- `reports/`
- raw MT5 CSVs
- raw HistData files
- large derived datasets
- local runtime CSVs
- local JSON/JSONL report artifacts
- local compile logs

## 5. Expected Repo State At Start Of Next Session

Expected after this handoff is committed and pushed:

- On branch `main`
- Branch up to date with `origin/main`
- Untracked files: `reports/`
- No other uncommitted changes
- Latest commit should be either:
  - `Add handoff document #95`
  - or `Expand handoff document #95`
- Previous code commit should be:
  - `56f609a Add H024 broker-request preview envelope`

Recent pushed commits before this handoff:

- `56f609a Add H024 broker-request preview envelope`
- `9e8ebdb Add H024 broker-request construction readiness packet`
- `1cd9885 Add H024 demo adapter no-op use invocation audit`
- `d03403e Add H024 demo adapter no-op use approval`
- `db58b20 Add H024 demo adapter no-op use approval`
- `3ff85c2 Add H024 Phase 4 demo adapter-use readiness human decision`
- `507674e Add H024 Phase 4 demo adapter-use readiness packet`
- `fc14036 Add H024 demo adapter no-op transport contract`
- `fa06afd Expand handoff document #94`
- `b2b8d06 Add handoff document #94`
- `1cb692d Add H024 Phase 4 demo adapter readiness human decision`

Note:

- There are two no-op-use-approval commits: `db58b20` and `d03403e`.
- Do not rewrite history. Latest validated state is pushed and good.

## 6. Non-Negotiable Safety Boundary

H024 is now:

- Phase 4-approved.
- Demo adapter implementation-approved.
- Adapter-readiness review-approved.
- Adapter-use readiness review-approved.
- No-op adapter use-approved.
- Preview-only broker-request envelope construction-approved.
- Still not actual broker-request construction-approved.
- Still not MT5 request construction-approved.
- Still not order-payload construction-approved.
- Still not execution-capable adapter-use approved.
- Still not broker-request approved.
- Still not demo-order approved.
- Still not live-order approved.
- Still not execution-approved.

Forbidden unless a later explicit approval gate changes this:

Python:

- `import MetaTrader5`
- `from MetaTrader5 import ...`
- `mt5.initialize`
- `mt5.login`
- `mt5.shutdown`
- `mt5.order_send`
- `mt5.order_check`
- Direct `order_send`
- Direct `order_check`
- Any broker API call
- Any terminal mutation path

MQL:

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
- `BuyStop`
- `SellStop`
- `BuyLimit`
- `SellLimit`
- `BuyStopLimit`
- `SellStopLimit`

Operationally forbidden:

- Chart attach/detach automation
- GUI automation
- Live-terminal mutation
- Demo order placement
- Live order placement
- Broker request dispatch
- MT5 execution adapter that can place an order
- Anything that mutates broker or terminal state

Allowed now:

- Pure-Python Phase 4 governance code
- Pure-Python demo adapter implementation/readiness code
- Fail-closed skeletons/contracts
- No-op transports
- No-op adapter use
- No-op adapter-use invocation audits
- Refusal reason evaluation
- Adapter-intent ingestion contracts that still do not construct broker requests
- Read-only JSON/JSONL artifact verification
- Read-only report-based audits
- Static source boundary verifiers
- Review-only readiness packets
- Human decision artifacts that explicitly preserve no-execution authority
- Preview-only inert broker-request envelope construction
- Tests proving request construction, dispatch, mutation, and order placement stay false

## 7. Current Approval Matrix

Approved / true:

| State | Value |
|---|---:|
| Phase 4 approved | true |
| Demo adapter implementation approved | true |
| Execution adapter implementation approved | true |
| Fail-closed skeleton implemented | true |
| Real-intent refusal audit passed | true |
| Adapter boundary static verifier passed | true |
| Phase 4 demo adapter readiness packet passed | true |
| Adapter-readiness human decision approved | true |
| No-op transport contract passed | true |
| Adapter-use readiness packet passed | true |
| Adapter-use readiness human decision approved | true |
| No-op adapter use approved | true |
| No-op adapter use invoked | true |
| Broker-request construction readiness packet passed | true |
| Broker-request preview construction approved | true |
| Broker-request preview envelope constructed | true |
| Preview envelope only | true |
| H020 sizing consumed, not reinterpreted | true |
| Preview idempotency key attached | true |
| Kill-switch allow-state required by preview | true |

Still false / not approved:

| State | Value |
|---|---:|
| Actual broker request construction approved | false |
| Actual broker request constructed | false |
| MT5 request construction approved | false |
| MT5 request constructed | false |
| Order payload construction approved | false |
| Order payload constructed | false |
| Execution-capable adapter use approved | false |
| Execution adapter approved as transport | false |
| Transport dispatch attempted | false |
| Terminal mutation approved | false |
| Terminal mutated | false |
| Broker mutation approved | false |
| Broker state mutated | false |
| Demo order placement approved | false |
| Live order placement approved | false |
| Execution approved | false |

Never collapse these states.

## 8. Strategy Mechanics Summary

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

## 9. H020 / H024 Sizing Boundary

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

Do not reconstruct lots manually inside an adapter.

Do not allow adapter code to reinterpret:

- signal sizing
- stop geometry
- volume step
- minimum lot
- maximum lot
- risk fraction

The adapter/request layer should consume already-verified intent artifacts and refuse/preview/draft according to authority gates. It must not become a second sizing engine.

## 10. Data Rules

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

## 11. Real Standard-Demo Evidence Context

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

This row is evidence only.

This row is not permission to trade.

## 12. Full Local Artifact Lineage

`reports/` is intentionally untracked. Do not commit it.

### 12.1 Runtime CSV

- `reports\h024_ea_log_only_preflight.csv`
- Rows: 229
- Violations: 0
- Runtime verifier: PASS

### 12.2 Dry-run reconciliation

- Input: `reports\h024_ea_log_only_preflight.csv`
- Output: `reports\h024_standard_demo_dry_run_requests.jsonl`
- Rows: 229
- Intended-action rows: 6
- WOULD_OPEN rows: 1
- Dry-run requests: 1
- Skipped non-request rows: 5
- Verdict: PASS

### 12.3 Demo-order plan

- Output: `reports\h024_standard_demo_demo_order_plans.jsonl`
- Plans: 1
- Violations: 0
- Verdict: PASS

This is not order approval.

### 12.4 Broker metadata preflight

- Metadata: `reports\h024_standard_demo_broker_metadata_snapshot.json`
- Output: `reports\h024_standard_demo_broker_metadata_preflight.jsonl`
- Preflight records: 1
- Violations: 0
- Verdict: PASS

### 12.5 Order-intent simulation

- Output: `reports\h024_standard_demo_order_intent_simulation.jsonl`
- Order-intent simulation records: 1
- Violations: 0
- Builder verdict: PASS
- Independent verifier verdict: PASS

This simulates intent only. It does not construct an MT5 request.

### 12.6 Manual approval checkpoint

- Output: `reports\h024_standard_demo_manual_approval_checkpoint.jsonl`
- Manual approval checkpoint records: 1
- Violations: 0
- Approval status: `PENDING_MANUAL_APPROVAL`
- Manual approval granted: false
- Execution approved: false
- Verdict: PASS

### 12.7 Demo execution adapter design

- Output: `reports\h024_standard_demo_demo_execution_adapter_design.jsonl`
- Design status: `DESIGN_SPEC_ONLY_NOT_IMPLEMENTED`
- Adapter implementation approved: false at that stage
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

### 12.8 Phase 4 readiness review

- Output: `reports\h024_standard_demo_phase4_readiness_review.jsonl`
- Review request status: `READY_FOR_PHASE4_REVIEW_REQUEST`
- Phase 4 approved: false at that stage
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

### 12.9 Execution safety-controls design

- Output: `reports\h024_standard_demo_execution_safety_controls_design.jsonl`
- Design status: `SAFETY_CONTROLS_DESIGN_SPEC_ONLY_NOT_IMPLEMENTED`
- Execution approved: false
- Verdict: PASS

### 12.10 Default blocked safety preflight

- Outputs:
  - `reports\h024_standard_demo_execution_safety_controls_default_blocked_preflight.jsonl`
  - `reports\h024_standard_demo_execution_safety_controls_default_blocked_audit.jsonl`
- Control decision: `BLOCK`
- Blocked reason: `missing_kill_switch_state`
- Execution approved: false
- Verdict: PASS

### 12.11 Operator control-state snapshot

- Outputs:
  - `reports\h024_standard_demo_operator_control_state_snapshot.json`
  - `reports\h024_standard_demo_kill_switch_state_snapshot.json`
  - `reports\h024_standard_demo_idempotency_ledger_snapshot.json`
- Snapshot status: `ALLOW_STATE_REVIEW_ONLY_NOT_EXECUTION_APPROVAL`
- Stable intent id:
  - `af20bcb4a54f6b51aafadeb15a65320bf9c448dbae20cf33066da3cd5adb4363`
- Execution approved: false
- Verdict: PASS

### 12.12 Explicit allow-state safety preflight

- Outputs:
  - `reports\h024_standard_demo_execution_safety_controls_allow_state_preflight.jsonl`
  - `reports\h024_standard_demo_execution_safety_controls_allow_state_audit.jsonl`
- Control decision: `PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL`
- Blocked reasons: 0
- Execution approved: false
- Verdict: PASS

This is review-only. It is not order approval.

### 12.13 Phase 4 review packet

- Output: `reports\h024_standard_demo_phase4_review_packet.jsonl`
- Schema: `h024_phase4_review_packet_v1`
- Kind: `PHASE4_REVIEW_PACKET_REVIEW_ONLY`
- Status: `READY_FOR_HUMAN_PHASE4_REVIEW`
- Execution adapter approved: false
- Execution approved: false
- Verdict: PASS

### 12.14 Phase 4 human decision

- Output: `reports\h024_standard_demo_phase4_human_decision.jsonl`
- Schema: `h024_phase4_human_decision_v1`
- Decision: `APPROVE_PHASE4_NO_EXECUTION`
- Status: `PHASE4_APPROVED_NO_EXECUTION_AUTHORITY`
- Phase 4 approved: true
- Execution adapter implementation approved: false at that stage
- Execution adapter approved: false
- Execution approved: false
- Verdict: PASS

This is when H024 officially left Phase 3. It did not approve execution.

### 12.15 Demo adapter implementation approval

- Output: `reports\h024_standard_demo_demo_adapter_implementation_approval.jsonl`
- Schema: `h024_demo_adapter_implementation_approval_v1`
- Decision: `APPROVE_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT`
- Status: `DEMO_ADAPTER_IMPLEMENTATION_APPROVED_NO_ORDER_AUTHORITY`
- Phase 4 approved: true
- Demo execution adapter implementation approved: true
- Execution adapter implementation approved: true
- Execution adapter approved: false
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false
- Verdict: PASS

### 12.16 Fail-closed demo execution adapter skeleton

- Output: `reports\h024_standard_demo_demo_execution_adapter_skeleton.jsonl`
- Schema: `h024_demo_execution_adapter_skeleton_v1`
- Kind: `DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED`
- Status: `DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED`
- Decision: `REFUSE_DISPATCH_NO_ORDER_AUTHORITY`
- Refusal reasons:
  - `execution_adapter_use_not_approved`
  - `demo_order_placement_not_approved`
  - `execution_not_approved`
- Dispatch attempted: false
- Terminal mutated: false
- Broker state mutated: false
- Verdict: PASS

### 12.17 Demo adapter intent-ingestion/refusal audit

- Output: `reports\h024_standard_demo_demo_adapter_intent_refusal_audit.jsonl`
- Schema: `h024_demo_adapter_intent_refusal_audit_v1`
- Kind: `DEMO_ADAPTER_INTENT_REFUSAL_AUDIT`
- Status: `ADAPTER_INTENT_INGESTED_REFUSED_NO_ORDER_AUTHORITY`
- Decision: `REFUSE_DISPATCH_NO_ORDER_AUTHORITY`
- Purpose:
  - Proves the adapter path can ingest the real standard-demo H024 order-intent context and still refuse dispatch.
- Required false states:
  - broker request constructed false
  - MT5 request constructed false
  - order payload constructed false
  - dispatch attempted false
  - terminal mutated false
  - broker state mutated false
- Verdict: PASS

### 12.18 Demo adapter boundary static verifier

- Output: `reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl`
- Schema: `h024_demo_adapter_boundary_static_verifier_v1`
- Kind: `DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER`
- Status: `ADAPTER_IMPLEMENTATION_BOUNDARY_STATIC_VERIFIED`
- Decision: `ALLOW_IMPLEMENTATION_SURFACE_REVIEW_ONLY_NO_EXECUTION`
- Latest scanned adapter-boundary files: 23
- Prohibited findings: 0
- Violations: 0
- Verdict: PASS

Important:

- Python files are scanned with Python AST parsing.
- MQL files are scanned as text.
- Do not regress to raw text scanning for Python files.

### 12.19 Phase 4 demo adapter readiness packet

- Output: `reports\h024_standard_demo_phase4_demo_adapter_readiness_packet.jsonl`
- Schema: `h024_phase4_demo_adapter_readiness_packet_v1`
- Kind: `PHASE4_DEMO_ADAPTER_READINESS_PACKET_REVIEW_ONLY`
- Status: `READY_FOR_HUMAN_ADAPTER_READINESS_REVIEW_NO_EXECUTION`
- Decision: `REVIEW_ONLY_NO_EXECUTION_AUTHORITY`
- Verdict: PASS

### 12.20 Phase 4 demo adapter readiness human decision

- Output: `reports\h024_standard_demo_phase4_demo_adapter_readiness_human_decision.jsonl`
- Schema: `h024_phase4_demo_adapter_readiness_human_decision_v1`
- Kind: `PHASE4_DEMO_ADAPTER_READINESS_HUMAN_DECISION`
- Status: `ADAPTER_READINESS_REVIEW_APPROVED_NO_EXECUTION_AUTHORITY`
- Decision: `APPROVE_ADAPTER_READINESS_REVIEW_NO_EXECUTION`
- Verdict: PASS

This approves adapter-readiness review only.

### 12.21 Demo adapter no-op transport contract

Commit:

- `fc14036 Add H024 demo adapter no-op transport contract`

Output:

- `reports\h024_standard_demo_demo_adapter_noop_transport_contract.jsonl`

Schema:

- `h024_demo_adapter_noop_transport_contract_v1`

Kind:

- `DEMO_ADAPTER_NOOP_TRANSPORT_CONTRACT`

Status:

- `NOOP_TRANSPORT_CONTRACT_READY_REFUSES_EXECUTION`

Decision:

- `REFUSE_TRANSPORT_NO_ADAPTER_USE_AUTHORITY`

Purpose:

- Defines no-op transport semantics before any real transport exists.
- Proves transport still refuses because adapter use/order/execution authority is absent at that stage.
- Does not construct broker requests.
- Does not construct MT5 requests.
- Does not construct order payloads.
- Does not dispatch.

Validation at commit:

- No-op transport artifact PASS
- Boundary verifier updated to 9 files
- Full suite passed

### 12.22 Adapter-use readiness packet

Commit:

- `507674e Add H024 Phase 4 demo adapter-use readiness packet`

Output:

- `reports\h024_standard_demo_phase4_demo_adapter_use_readiness_packet.jsonl`

Schema:

- `h024_phase4_demo_adapter_use_readiness_packet_v1`

Kind:

- `PHASE4_DEMO_ADAPTER_USE_READINESS_PACKET_REVIEW_ONLY`

Status:

- `READY_FOR_HUMAN_ADAPTER_USE_REVIEW_NO_EXECUTION`

Decision:

- `REQUEST_HUMAN_ADAPTER_USE_REVIEW_NO_EXECUTION_AUTHORITY`

Purpose:

- Aggregates no-op transport and boundary proof.
- Requests human review for adapter-use readiness.
- Does not approve adapter use.
- Does not approve broker request construction or execution.

Validation:

- Adapter-use readiness packet PASS
- Full suite passed: `1189 passed`

### 12.23 Adapter-use readiness human decision

Commit:

- `3ff85c2 Add H024 Phase 4 demo adapter-use readiness human decision`

Output:

- `reports\h024_standard_demo_phase4_demo_adapter_use_readiness_human_decision.jsonl`

Schema:

- `h024_phase4_demo_adapter_use_readiness_human_decision_v1`

Kind:

- `PHASE4_DEMO_ADAPTER_USE_READINESS_HUMAN_DECISION`

Status:

- `ADAPTER_USE_READINESS_REVIEW_APPROVED_NO_EXECUTION_AUTHORITY`

Decision:

- `APPROVE_ADAPTER_USE_READINESS_REVIEW_NO_EXECUTION`

Purpose:

- Human decision approving adapter-use readiness review only.
- Does not approve adapter use.
- Does not approve broker requests/orders/execution.

Validation:

- Human decision PASS
- Full suite passed: `1212 passed`

### 12.24 No-op adapter-use approval

Commits:

- `db58b20 Add H024 demo adapter no-op use approval`
- `d03403e Add H024 demo adapter no-op use approval`

Output:

- `reports\h024_standard_demo_demo_adapter_noop_use_approval.jsonl`

Schema:

- `h024_demo_adapter_noop_use_approval_v1`

Kind:

- `DEMO_ADAPTER_NOOP_USE_APPROVAL`

Status:

- `NOOP_ADAPTER_USE_APPROVED_NO_EXECUTION_AUTHORITY`

Decision:

- `APPROVE_NOOP_ADAPTER_USE_ONLY_NO_BROKER_REQUEST_AUTHORITY`

Purpose:

- Approves only invocation of the pure-Python no-op adapter-use path.
- Does not approve execution-capable adapter use.
- Does not approve broker request construction.
- Does not approve MT5 execution.
- Does not approve demo/live orders.

Important incident:

- Initial negative tests revealed verifier did not check `approved_scope.may_*` forbidden permission flags.
- Verifier was patched.
- Latest passing commit is `d03403e`.
- Do not rewrite history.

Validation:

- Focused tests passed: `45 passed`
- Boundary verifier expanded to 12 files
- Full suite passed: `1244 passed`

### 12.25 No-op adapter-use invocation audit

Commit:

- `1cd9885 Add H024 demo adapter no-op use invocation audit`

Output:

- `reports\h024_standard_demo_demo_adapter_noop_use_invocation_audit.jsonl`

Schema:

- `h024_demo_adapter_noop_use_invocation_audit_v1`

Kind:

- `DEMO_ADAPTER_NOOP_USE_INVOCATION_AUDIT`

Status:

- `NOOP_ADAPTER_USE_INVOKED_REFUSED_BROKER_TRANSPORT`

Decision:

- `INVOKE_NOOP_ADAPTER_USE_ONLY_REFUSE_BROKER_TRANSPORT`

Purpose:

- Exercises the explicitly approved pure-Python no-op adapter-use path.
- Records that no-op adapter use was invoked.
- Records that no-op transport contract was invoked.
- Records broker-facing transport remains refused.
- Does not construct broker requests, MT5 requests, or order payloads.
- Does not dispatch.
- Does not mutate terminal/broker state.

Validation:

- Focused tests passed: `42 passed`
- Boundary verifier expanded to 15 files
- Full suite passed: `1273 passed`

### 12.26 Broker-request construction readiness packet

Commit:

- `9e8ebdb Add H024 broker-request construction readiness packet`

Output:

- `reports\h024_standard_demo_broker_request_construction_readiness_packet.jsonl`

Schema:

- `h024_broker_request_construction_readiness_packet_v1`

Kind:

- `BROKER_REQUEST_CONSTRUCTION_READINESS_PACKET_REVIEW_ONLY`

Status:

- `READY_FOR_HUMAN_BROKER_REQUEST_CONSTRUCTION_REVIEW_NO_EXECUTION`

Decision:

- `REQUEST_HUMAN_BROKER_REQUEST_CONSTRUCTION_REVIEW_NO_EXECUTION_AUTHORITY`

Purpose:

- Requests human review for broker-request construction readiness.
- Aggregates approved no-op invocation and boundary proof.
- Does not approve broker request construction.
- Does not construct a broker request.
- Does not construct an MT5 request or order payload.
- Does not dispatch or mutate.

Required next capability constraints embedded:

- Must consume verified intent.
- Must not reinterpret H020 sizing.
- Must attach idempotency key.
- Must require kill-switch allow-state.
- Must emit preview-only JSON.
- Must not import MetaTrader5.
- Must not call MT5 execution API.
- Must not dispatch transport.

Validation:

- Focused tests passed: `39 passed`
- Boundary verifier expanded to 18 files
- Full suite passed: `1299 passed`

### 12.27 Broker-request preview construction approval + preview envelope

Commit:

- `56f609a Add H024 broker-request preview envelope`

Outputs:

- `reports\h024_standard_demo_broker_request_preview_construction_approval.jsonl`
- `reports\h024_standard_demo_broker_request_preview_envelope.jsonl`

Preview construction approval schema:

- `h024_broker_request_preview_construction_approval_v1`

Preview construction approval kind:

- `BROKER_REQUEST_PREVIEW_CONSTRUCTION_APPROVAL`

Preview construction approval status:

- `BROKER_REQUEST_PREVIEW_CONSTRUCTION_APPROVED_NO_DISPATCH_AUTHORITY`

Preview construction approval decision:

- `APPROVE_PREVIEW_ENVELOPE_CONSTRUCTION_ONLY_NO_MT5_NO_DISPATCH`

Preview envelope schema:

- `h024_broker_request_preview_envelope_v1`

Preview envelope kind:

- `BROKER_REQUEST_PREVIEW_ENVELOPE`

Preview envelope status:

- `PREVIEW_ENVELOPE_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH`

Preview envelope decision:

- `CONSTRUCT_PREVIEW_ENVELOPE_ONLY_REFUSE_DISPATCH`

Purpose:

- Approves only preview-envelope construction.
- Builds an inert preview envelope from:
  - preview construction approval
  - real standard-demo order-intent simulation
  - execution safety controls allow-state preflight
- Attaches stable preview idempotency key.
- Records verified intent consumed.
- Records H020 sizing consumed, not reinterpreted.
- Records kill-switch allow-state required.
- Explicitly records:
  - not MT5 request
  - not broker request
  - not order payload
- Preserves all false mutation/dispatch/order/execution states.

Validation:

- Focused preview tests: `43 passed`
- Preview construction approval builder/verifier: PASS
- Preview envelope builder/verifier: PASS
- Boundary verifier expanded to 23 files
- Static EA verifier: PASS
- Full suite: `1329 passed`

## 13. Core Files To Know

Latest preview/draft-adjacent files:

- `quantcore\execution\h024_broker_request_preview_envelope.py`
- `scripts\build_h024_broker_request_preview_construction_approval_jsonl.py`
- `scripts\verify_h024_broker_request_preview_construction_approval_jsonl.py`
- `scripts\build_h024_broker_request_preview_envelope_jsonl.py`
- `scripts\verify_h024_broker_request_preview_envelope_jsonl.py`
- `tests\test_h024_broker_request_preview_envelope.py`
- `tests\test_h024_broker_request_preview_envelope_boundary_targets.py`
- `docs\operations\H024_STANDARD_DEMO_BROKER_REQUEST_PREVIEW_ENVELOPE_RESULT.md`

Broker-request construction readiness:

- `quantcore\execution\h024_broker_request_construction_readiness_packet.py`
- `scripts\build_h024_broker_request_construction_readiness_packet_jsonl.py`
- `scripts\verify_h024_broker_request_construction_readiness_packet_jsonl.py`
- `tests\test_h024_broker_request_construction_readiness_packet.py`
- `tests\test_h024_broker_request_construction_readiness_packet_boundary_targets.py`
- `docs\operations\H024_STANDARD_DEMO_BROKER_REQUEST_CONSTRUCTION_READINESS_PACKET_RESULT.md`

No-op adapter-use invocation:

- `quantcore\execution\h024_demo_adapter_noop_use_invocation_audit.py`
- `scripts\build_h024_demo_adapter_noop_use_invocation_audit_jsonl.py`
- `scripts\verify_h024_demo_adapter_noop_use_invocation_audit_jsonl.py`
- `tests\test_h024_demo_adapter_noop_use_invocation_audit.py`
- `tests\test_h024_demo_adapter_noop_use_invocation_audit_boundary_targets.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_NOOP_USE_INVOCATION_AUDIT_RESULT.md`

No-op adapter-use approval:

- `quantcore\execution\h024_demo_adapter_noop_use_approval.py`
- `scripts\build_h024_demo_adapter_noop_use_approval_jsonl.py`
- `scripts\verify_h024_demo_adapter_noop_use_approval_jsonl.py`
- `tests\test_h024_demo_adapter_noop_use_approval.py`
- `tests\test_h024_demo_adapter_noop_use_approval_boundary_targets.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_NOOP_USE_APPROVAL_RESULT.md`

Boundary static verifier:

- `quantcore\execution\h024_demo_adapter_boundary_static_verifier.py`
- `scripts\build_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `tests\test_h024_demo_adapter_boundary_static_verifier.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER_RESULT.md`

EA/runtime:

- `ea_mt5\Experts\H024_LogOnly_Preflight.mq5`
- `scripts\verify_h024_ea_source_static.py`

## 14. Boundary Static Verifier Current Surface

Latest boundary verifier scans 23 files.

It must include all pure-Python adapter/readiness/preview implementation surfaces through:

- fail-closed skeleton
- intent refusal audit
- boundary verifier scripts
- no-op transport contract
- no-op adapter-use approval
- no-op adapter-use invocation audit
- broker-request construction readiness packet
- broker-request preview envelope module
- preview construction approval scripts
- preview envelope builder/verifier scripts

The verifier must fail on executable prohibited imports/calls, but must not fail on comments/docstrings/refusal strings.

Python scanning must remain AST-based.

MQL scanning may remain text-based.

## 15. Known Pitfalls

PowerShell pitfalls:

- Do not use Bash heredocs like `python - <<'PY'`.
- That already caused a parse failure in this session.
- Use PowerShell here-strings and `Write-Utf8NoBom`.
- Avoid complex nested code generation when direct file writes are possible.
- Avoid multiline `git add` with backticks.
- Use single-line `git add -- "file1" "file2" ...`.

Static verifier pitfalls:

- Do not scan Python code as raw text for prohibited concepts.
- Comments/docstrings/refusal strings legitimately mention `OrderSend`, `MqlTradeRequest`, `MetaTrader5`, etc.
- Python targets must be scanned via AST for executable imports/calls.
- MQL targets can be scanned as text.

Readiness packet pitfalls:

- Some upstream artifacts may be valid without top-level `verdict`.
- Do not require every upstream artifact to share a `verdict: PASS` convention if schema/kind/status/decision/authority flags/mutation flags/violations prove validity.

MetaEditor pitfall:

- MetaEditor may return code 1 even when compile succeeds.
- Acceptable compile result in prior work:
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
- Do not treat adapter-use readiness approval as execution-capable adapter-use approval.
- Do not treat no-op adapter-use approval as broker-request approval.
- Do not treat preview-envelope construction approval as actual broker-request construction approval.
- Do not treat a preview envelope as a broker request.
- Do not treat explicit allow-state safety preflight as order approval.
- Do not treat WOULD_OPEN as permission to trade.
- Do not treat any JSONL artifact as an MT5 request.

## 16. Recommended Next Engineering Step

Next safe, practical, high-leverage work:

Build **inert canonical broker-request draft construction approval and draft envelope**.

This is the next step because:

- The preview envelope exists and proves the real intent can be safely represented without becoming a broker/MT5/order request.
- The next useful deployment-adjacent artifact is a canonical draft that makes the eventual request fields explicit for human review.
- It must still be non-dispatchable and not shaped as an MT5 request object.

Recommended next artifacts:

- `quantcore\execution\h024_broker_request_draft_construction_approval.py`
- `scripts\build_h024_broker_request_draft_construction_approval_jsonl.py`
- `scripts\verify_h024_broker_request_draft_construction_approval_jsonl.py`
- `quantcore\execution\h024_broker_request_draft_envelope.py`
- `scripts\build_h024_broker_request_draft_envelope_jsonl.py`
- `scripts\verify_h024_broker_request_draft_envelope_jsonl.py`
- `tests\test_h024_broker_request_draft_construction_approval.py`
- `tests\test_h024_broker_request_draft_envelope.py`
- boundary-target tests
- docs result files
- update `h024_demo_adapter_boundary_static_verifier.py`

Suggested schemas:

- `h024_broker_request_draft_construction_approval_v1`
- `h024_broker_request_draft_envelope_v1`

Suggested decisions:

- `APPROVE_INERT_BROKER_REQUEST_DRAFT_ONLY_NO_MT5_NO_DISPATCH`
- `CONSTRUCT_INERT_BROKER_REQUEST_DRAFT_ONLY_REFUSE_DISPATCH`

Must preserve false:

- `actual_broker_request_constructed=false`
- `mt5_request_constructed=false`
- `order_payload_constructed=false`
- `transport_dispatch_attempted=false`
- `dispatch_attempted=false`
- `terminal_mutated=false`
- `broker_state_mutated=false`
- `demo_order_placement_approved=false`
- `live_order_placement_approved=false`
- `execution_approved=false`

Must include true:

- `preview_envelope_consumed=true`
- `verified_intent_consumed=true`
- `h020_sizing_consumed_not_reinterpreted=true`
- `idempotency_key_carried_forward=true`
- `kill_switch_allow_state_required=true`
- `draft_is_non_dispatchable=true`
- `not_mt5_request=true`
- `not_order_payload=true`

Important design constraint:

- The draft should not be a dict shaped exactly like `MqlTradeRequest`.
- It should be a review envelope with normalized conceptual fields, not an executable request object.
- Do not include field names or structures that invite direct `mt5.order_send(draft)` usage.
- Do not import or call `MetaTrader5`.

After that, likely remaining gates before one controlled demo canary:

1. Inert canonical broker-request draft construction approval.
2. Inert canonical broker-request draft envelope.
3. Human decision approving broker-request draft review only.
4. MT5 request-shape design review, still no import/call.
5. Human approval for MT5 request-shape construction only.
6. Inert MT5 request preview, still not sent.
7. Demo-order readiness packet.
8. Human demo-order canary approval.
9. One canary demo order path with kill switch, idempotency ledger, max-lot cap, symbol/server lock, and immediate post-order audit.

Do not skip these boundaries.

## 17. Exact Commands To Verify Current State

Start the next session by asking the user to run:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

python scripts\verify_h024_broker_request_preview_construction_approval_jsonl.py reports\h024_standard_demo_broker_request_preview_construction_approval.jsonl --allowed-demo-server Exness-MT5Trial6 --require-approved

python scripts\verify_h024_broker_request_preview_envelope_jsonl.py reports\h024_standard_demo_broker_request_preview_envelope.jsonl --allowed-demo-server Exness-MT5Trial6 --require-pass

python scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl --require-pass

python scripts\verify_h024_ea_source_static.py

Expected:

Branch up to date with origin/main
Untracked reports/ only
Latest code commit before handoff: 56f609a Add H024 broker-request preview envelope
Preview construction approval: PASS
Preview envelope: PASS
Boundary verifier: 23 files, PASS
Static EA verifier: PASS

Full suite anchor:

python -m pytest -q

Latest known result:

1329 passed in 23.20s
18. Exact First Response The Next AI Should Give

The next AI should say:

Understood. Continuing from HANDOFF_95.

I understand:

H024 is Phase 4-approved.
H024 now has a verified pure-Python no-op adapter-use path, an invoked no-op adapter-use audit, broker-request construction readiness, preview-only broker-request construction approval, and an inert broker-request preview envelope built from the real standard-demo intent.
The latest pushed code commit before this handoff is 56f609a Add H024 broker-request preview envelope.
The latest validation anchor is 1329 tests passed, static EA verifier PASS, and adapter boundary static verifier PASS scanning 23 files with zero prohibited findings.
H024 is still not approved to construct an actual broker request, not approved to construct an MT5 request, not approved to construct an order payload, not approved to dispatch, not approved to place demo/live orders, and not execution-approved.
The next safe engineering step is an inert canonical broker-request draft construction approval and draft envelope, still pure Python, still non-dispatchable, still no MT5 import/call, and still no terminal/broker mutation.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8
python scripts\verify_h024_broker_request_preview_envelope_jsonl.py reports\h024_standard_demo_broker_request_preview_envelope.jsonl --allowed-demo-server Exness-MT5Trial6 --require-pass
python scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl --require-pass
python scripts\verify_h024_ea_source_static.py

Then paste the full output.
19. Do Not Let The Next AI Do These Things

Do not immediately implement:

MetaTrader5 import
MT5 terminal connection
Actual broker request dispatch
Actual MT5 request construction
Actual order payload construction
OrderSend
OrderCheck
MqlTradeRequest
Demo order placement
Live order placement
Terminal mutation
GUI automation
Chart attach automation

Do not ask the user to “try one demo order.”

Do not treat preview envelope as a broker request.

Do not treat preview construction approval as actual broker-request construction approval.

The next step is still pure Python, inert, review-only, non-dispatchable, and non-mutating.

20. Compact Continuation Prompt For Another AI

Paste this to another AI if not using the file directly:

You are continuing the Institutional EA project from HANDOFF_95.

You are a senior quant engineer and mentor helping a solo retail trader on Windows build H024, a USDJPY + XAUUSD MT5 expert advisor with institutional-grade safety discipline.

Read and obey docs/operations/handoffs/HANDOFF_95.md. If anything conflicts with older handoffs, HANDOFF_95 wins.

Current state:
- Latest code commit before handoff: 56f609a Add H024 broker-request preview envelope.
- H024 is Phase 4-approved.
- H024 has no-op adapter use approved and invoked.
- H024 has broker-request construction readiness passed.
- H024 has preview-only broker-request construction approval.
- H024 has an inert broker-request preview envelope built from the real standard-demo H024 intent and safety allow-state preflight.
- Latest validation: 1329 tests passed, static EA verifier PASS, boundary verifier PASS scanning 23 files with zero prohibited findings.
- Working tree should be clean except untracked reports/.

Hard boundaries:
- Do not import MetaTrader5.
- Do not call MT5.
- Do not construct an MT5 request.
- Do not construct an order payload.
- Do not dispatch transport.
- Do not mutate terminal or broker state.
- Do not place demo or live orders.
- Do not treat preview envelope as a broker request.
- Execution remains blocked.

Next safe step:
Build inert canonical broker-request draft construction approval and draft envelope. It must consume the preview envelope, carry idempotency forward, require kill-switch allow-state, consume H020 sizing without reinterpretation, and remain non-dispatchable, not an MT5 request, not an order payload, and non-mutating.

Use PowerShell, not Bash. Use one copy/paste block. Code changes require tests. Do not commit reports/.
