# HANDOFF_96 — H024 Demo-Order Readiness Packet Complete, Canary Approval Still Blocked

If this handoff conflicts with any older handoff, this handoff wins.

This handoff is intentionally self-contained. A new AI should be able to continue safely without opening HANDOFF_95 or older handoffs first.

## 0. One-Sentence State

H024 is Phase 4-approved and now has a verified pure-Python non-mutating path through no-op adapter use, broker-request preview envelope, inert broker-request draft envelope, MT5 request-shape design review, inert MT5 request-shape preview envelope, MT5 request-shape preview review approval, and a demo-order readiness packet; however H024 is still not approved to construct an actual broker request, not approved to construct an actual MT5 request, not approved to construct an order payload, not approved to dispatch, not approved to place demo/live orders, and not execution-approved.

Latest pushed code commit before this handoff:

- `8132f11 Add H024 demo-order readiness packet`

Recent pushed commits:

- `8132f11 Add H024 demo-order readiness packet`
- `3288883 Add H024 MT5 request-shape preview gate`
- `846fcb2 Add H024 draft review and MT5 shape design review`
- `8747771 Add H024 broker-request draft envelope`
- `fea6cd7 Expand handoff document #95`
- `5263c3c Add handoff document #95`
- `56f609a Add H024 broker-request preview envelope`
- `9e8ebdb Add H024 broker-request construction readiness packet`

Latest validation anchor:

- Demo-order readiness packet: PASS
- MT5 request-shape preview review human decision: PASS
- Boundary static verifier: PASS
- Adapter-boundary files scanned: 47
- Prohibited findings: 0
- Static EA verifier: PASS
- Focused demo-order readiness tests: `6 passed`
- Full test suite: `1356 passed in 22.28s`
- Git push: PASS

## 1. Current Status — Say This Directly If Asked

H024 has officially left Phase 3 and is in Phase 4 governance.

H024 is not approved to trade.

H024 is not approved to place demo orders.

H024 is not approved to place live orders.

H024 is not approved to call MT5 execution APIs.

H024 is not approved to mutate terminal or broker state.

H024 is not approved to construct an actual broker request.

H024 is not approved to construct an actual MT5 request.

H024 is not approved to construct an order payload.

H024 is not approved to dispatch transport.

H024 is not execution-approved.

Current highest deployment-adjacent artifact:

- A demo-order readiness packet exists.
- It is review-only.
- It requests human review for a possible later tightly controlled demo-order canary.
- It does not approve a demo-order canary.
- It does not approve demo order placement.
- It does not approve live order placement.
- It does not construct an actual MT5 request.
- It does not construct an order payload.
- It does not construct an actual broker request.
- It does not dispatch transport.
- It does not mutate terminal or broker state.
- It does not approve execution.

Correct short answer if asked “how close are we to deployment?”:

- For live deployment: still not close.
- For first tightly controlled demo canary: we are now at the demo-order readiness review boundary.
- The next safe work should still be pure Python, review-only, and non-mutating.
- The next major safe block is a separate explicit demo-order canary human approval artifact plus pre-canary hard-controls readiness artifacts.
- No actual MT5 request construction, dispatch, or order placement is approved yet.

## 2. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current strategy family:

- H024

Current stage:

- Phase 4 governance approved.
- Demo adapter implementation/readiness work approved.
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
- Inert canonical broker-request draft construction approval implemented.
- Inert canonical broker-request draft envelope implemented.
- Broker-request draft review human decision implemented.
- MT5 request-shape design review packet implemented.
- MT5 request-shape construction approval implemented.
- Inert MT5 request-shape preview envelope implemented.
- MT5 request-shape preview review human decision implemented.
- Demo-order readiness packet implemented.
- Actual broker request construction still blocked.
- Actual MT5 request construction still blocked.
- Order payload construction still blocked.
- Dispatch still blocked.
- Demo/live order placement still blocked.
- Execution still blocked.

The project must preserve a hard boundary between:

1. Evidence/readiness/approval artifacts.
2. Pure-Python contracts, skeletons, readiness gates, inert preview/draft artifacts, and review-only packets.
3. Any real broker/terminal mutation.

We are still inside 1 and bounded 2.

We have not crossed into 3.

## 3. Human Preference And Morale Context

The user is tired of ceremony and wants practical progress toward deployment.

Important preference:

- Do not make tiny incremental changes when a fuller, higher-leverage implementation is appropriate.
- Prefer work that materially advances the gate.
- The user explicitly clarified that “multiple things” means multiple major things in one command block, not merely many small files.
- When safe, bundle multiple major review-only gates into one coherent PowerShell block.
- Do not break safety boundaries to speed up.
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
  - `Add handoff document #96`
  - or `Expand handoff document #96`
- Previous code commit should be:
  - `8132f11 Add H024 demo-order readiness packet`

## 6. Non-Negotiable Safety Boundary

H024 is now:

- Phase 4-approved.
- Demo adapter implementation-approved.
- Adapter-readiness review-approved.
- Adapter-use readiness review-approved.
- No-op adapter use-approved.
- Preview-only broker-request envelope construction-approved.
- Inert broker-request draft construction-approved.
- Broker-request draft review-approved.
- MT5 request-shape design review packet constructed.
- Inert MT5 request-shape preview construction-approved.
- Inert MT5 request-shape preview envelope constructed.
- MT5 request-shape preview review-approved.
- Demo-order readiness packet constructed.
- Still not actual broker-request construction-approved.
- Still not actual MT5 request construction-approved.
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
- Inert canonical broker-request draft envelope construction
- Inert MT5 request-shape design review
- Inert MT5 request-shape preview envelope construction
- Demo-order readiness packet construction
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
| Inert broker-request draft construction approved | true |
| Inert broker-request draft envelope constructed | true |
| Broker-request draft review approved | true |
| MT5 request-shape design review packet constructed | true |
| MT5 request-shape construction approved for inert preview only | true |
| Inert MT5 request-shape preview envelope constructed | true |
| MT5 request-shape preview review approved | true |
| Demo-order readiness packet constructed | true |
| Demo-order canary review requested | true |
| H020 sizing consumed, not reinterpreted | true |
| Idempotency carried forward through preview/draft/shape-readiness path | true |
| Kill-switch allow-state required by readiness path | true |

Still false / not approved:

| State | Value |
|---|---:|
| Demo-order canary approved | false |
| Actual broker request construction approved | false |
| Actual broker request constructed | false |
| Actual MT5 request construction approved | false |
| Actual MT5 request constructed | false |
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

Do not allow adapter/request/readiness code to reinterpret:

- signal sizing
- stop geometry
- volume step
- minimum lot
- maximum lot
- risk fraction

The adapter/request/readiness layer should consume already-verified intent artifacts and refuse/preview/draft/readiness-check according to authority gates. It must not become a second sizing engine.

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

## 12. Artifact Lineage Since HANDOFF_95

`reports/` is intentionally untracked. Do not commit it.

### 12.1 Broker-request preview construction approval + preview envelope

Commit:

- `56f609a Add H024 broker-request preview envelope`

Outputs:

- `reports\h024_standard_demo_broker_request_preview_construction_approval.jsonl`
- `reports\h024_standard_demo_broker_request_preview_envelope.jsonl`

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

Validation at that time:

- Full suite: `1329 passed`

### 12.2 Broker-request draft envelope

Commit:

- `8747771 Add H024 broker-request draft envelope`

Outputs:

- `reports\h024_standard_demo_broker_request_draft_construction_approval.jsonl`
- `reports\h024_standard_demo_broker_request_draft_envelope.jsonl`

Purpose:

- Adds inert canonical broker-request draft construction approval.
- Adds inert broker-request draft envelope.
- Consumes preview envelope.
- Carries idempotency forward.
- Consumes H020 sizing without reinterpretation.
- Requires kill-switch allow-state.
- Remains non-dispatchable.
- Explicitly not MT5 request, not order payload, not actual broker request.

Validation:

- Draft construction approval: PASS
- Draft envelope: PASS
- Full suite: `1337 passed`

### 12.3 Broker-request draft review + MT5 request-shape design review

Commit:

- `846fcb2 Add H024 draft review and MT5 shape design review`

Outputs:

- `reports\h024_standard_demo_broker_request_draft_review_human_decision.jsonl`
- `reports\h024_standard_demo_mt5_request_shape_design_review_packet.jsonl`

Purpose:

- Human decision approving review of inert broker-request draft only.
- Permits preparation of MT5 request-shape design review only.
- Adds MT5 request-shape design review packet.
- Does not construct MT5 request.
- Does not construct order payload.
- Does not dispatch.
- Does not mutate terminal/broker state.

Validation:

- Draft review human decision: PASS
- MT5 request-shape design review packet: PASS
- Boundary verifier: 35 files, 0 prohibited findings, PASS
- Full suite: `1343 passed`

### 12.4 MT5 request-shape preview gate

Commit:

- `3288883 Add H024 MT5 request-shape preview gate`

Outputs:

- `reports\h024_standard_demo_mt5_request_shape_construction_approval.jsonl`
- `reports\h024_standard_demo_mt5_request_shape_preview_envelope.jsonl`

Purpose:

- Adds construction approval for an inert MT5 request-shape preview only.
- Adds inert MT5 request-shape preview envelope.
- Consumes MT5 request-shape design review packet.
- Consumes reviewed draft summary.
- Carries idempotency forward.
- Consumes H020 sizing without reinterpretation.
- Requires kill-switch allow-state.
- Explicitly not actual MT5 request, not order payload, not actual broker request, not dispatchable.

Validation:

- MT5 request-shape construction approval: PASS
- MT5 request-shape preview envelope: PASS
- Boundary verifier: 41 files, 0 prohibited findings, PASS
- EA static verifier: PASS
- Focused tests: `7 passed`
- Full suite: `1350 passed`

### 12.5 MT5 request-shape preview review + demo-order readiness packet

Commit:

- `8132f11 Add H024 demo-order readiness packet`

Outputs:

- `reports\h024_standard_demo_mt5_request_shape_preview_review_human_decision.jsonl`
- `reports\h024_standard_demo_demo_order_readiness_packet.jsonl`

Purpose:

- Adds human decision approving review of inert MT5 request-shape preview only.
- Permits preparation of a demo-order readiness packet only.
- Adds demo-order readiness packet.
- Requests human review for possible later tightly controlled demo-order canary.
- Does not approve demo-order canary.
- Does not approve demo order placement.
- Does not construct actual MT5 request.
- Does not construct order payload.
- Does not dispatch.
- Does not mutate terminal/broker state.
- Does not approve execution.

Validation:

- MT5 request-shape preview review human decision: PASS
- Demo-order readiness packet: PASS
- Boundary verifier: 47 files, 0 prohibited findings, PASS
- EA static verifier: PASS
- Focused tests: `6 passed`
- Full suite: `1356 passed`

## 13. Core Files To Know

Latest demo-order readiness files:

- `quantcore\execution\h024_mt5_request_shape_preview_review_human_decision.py`
- `quantcore\execution\h024_demo_order_readiness_packet.py`
- `scripts\build_h024_mt5_request_shape_preview_review_human_decision_jsonl.py`
- `scripts\verify_h024_mt5_request_shape_preview_review_human_decision_jsonl.py`
- `scripts\build_h024_demo_order_readiness_packet_jsonl.py`
- `scripts\verify_h024_demo_order_readiness_packet_jsonl.py`
- `tests\test_h024_mt5_request_shape_preview_review_human_decision.py`
- `tests\test_h024_demo_order_readiness_packet.py`
- `tests\test_h024_demo_order_readiness_boundary_targets.py`
- `docs\operations\H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_REVIEW_HUMAN_DECISION_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_ORDER_READINESS_PACKET_RESULT.md`

MT5 request-shape preview files:

- `quantcore\execution\h024_mt5_request_shape_construction_approval.py`
- `quantcore\execution\h024_mt5_request_shape_preview_envelope.py`
- `scripts\build_h024_mt5_request_shape_construction_approval_jsonl.py`
- `scripts\verify_h024_mt5_request_shape_construction_approval_jsonl.py`
- `scripts\build_h024_mt5_request_shape_preview_envelope_jsonl.py`
- `scripts\verify_h024_mt5_request_shape_preview_envelope_jsonl.py`
- `tests\test_h024_mt5_request_shape_construction_approval.py`
- `tests\test_h024_mt5_request_shape_preview_envelope.py`
- `tests\test_h024_mt5_request_shape_preview_boundary_targets.py`
- `docs\operations\H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_CONSTRUCTION_APPROVAL_RESULT.md`
- `docs\operations\H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md`

Draft/design files:

- `quantcore\execution\h024_broker_request_draft_review_human_decision.py`
- `quantcore\execution\h024_mt5_request_shape_design_review_packet.py`
- `quantcore\execution\h024_broker_request_draft_construction_approval.py`
- `quantcore\execution\h024_broker_request_draft_envelope.py`
- related build/verify scripts and tests

Boundary static verifier:

- `quantcore\execution\h024_demo_adapter_boundary_static_verifier.py`
- `scripts\build_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- Latest scans 47 adapter-boundary files.
- Prohibited findings: 0.
- Python scanning must remain AST-based.
- MQL scanning may remain text-based.

EA/runtime:

- `ea_mt5\Experts\H024_LogOnly_Preflight.mq5`
- `scripts\verify_h024_ea_source_static.py`

## 14. Boundary Static Verifier Current Surface

Latest boundary verifier scans 47 files.

It must include all pure-Python adapter/readiness/preview/draft/review implementation surfaces through:

- fail-closed skeleton
- intent refusal audit
- boundary verifier scripts
- no-op transport contract
- no-op adapter-use approval
- no-op adapter-use invocation audit
- broker-request construction readiness packet
- broker-request preview envelope
- broker-request draft construction approval
- broker-request draft envelope
- broker-request draft review human decision
- MT5 request-shape design review packet
- MT5 request-shape construction approval
- MT5 request-shape preview envelope
- MT5 request-shape preview review human decision
- demo-order readiness packet

The verifier must fail on executable prohibited imports/calls, but must not fail on comments/docstrings/refusal strings.

Python scanning must remain AST-based.

MQL scanning may remain text-based.

## 15. Known Pitfalls

PowerShell pitfalls:

- Do not use Bash heredocs like `python - <<'PY'`.
- Use PowerShell here-strings and `Write-Utf8NoBom`.
- Avoid complex nested code generation when direct file writes are possible.
- Avoid multiline `git add` with backticks.
- Use single-line `git add -- "file1" "file2" ...`.

Boundary verifier pitfalls:

- Use correct CLI:
  - `python scripts\build_h024_demo_adapter_boundary_static_verifier_jsonl.py --output reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl`
- Earlier a bad command omitted `--output`.
- Also, when patching target strings, ensure each target string has a comma; missing commas can silently concatenate adjacent Python strings and reduce scan count.
- Expected scan count after `8132f11`: 47 files.
- Do not accept a lower scan count without explanation.

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
- Do not treat broker-request draft envelope as an actual broker request.
- Do not treat MT5 request-shape design review as MT5 request construction approval.
- Do not treat inert MT5 request-shape preview envelope as an actual MT5 request.
- Do not treat demo-order readiness packet as demo-order approval.
- Do not treat explicit allow-state safety preflight as order approval.
- Do not treat WOULD_OPEN as permission to trade.
- Do not treat any JSONL artifact as an MT5 request or order payload.

## 16. Recommended Next Engineering Step

Next safe, practical, high-leverage work:

Build a combined pure-Python, review-only block containing:

1. **Demo-order canary approval readiness human decision**
   - Approves only the readiness review, not the order.
   - Allows construction of a canary hard-controls preflight packet.
   - Does not approve demo-order placement.
   - Does not approve MT5 request construction.
   - Does not approve order payload construction.
   - Does not approve dispatch.

2. **Canary hard-controls preflight packet**
   - Review-only, no order authority.
   - Must explicitly require:
     - allowed demo server lock: `Exness-MT5Trial6`
     - account currency lock: USD
     - standard demo context only
     - symbol lock to the already-observed runtime symbol from the readiness/shape path
     - kill-switch allow-state
     - idempotency ledger
     - max-lot cap
     - single-canary-order limit
     - post-order audit requirement if later approved
     - live order remains forbidden
   - Must preserve false:
     - actual broker request constructed
     - MT5 request constructed
     - order payload constructed
     - dispatch attempted
     - terminal mutated
     - broker state mutated
     - demo order placement approved
     - live order placement approved
     - execution approved

Do this as multiple major things in one command block if safe, but do not skip gates.

Suggested schemas:

- `h024_demo_order_canary_approval_readiness_human_decision_v1`
- `h024_demo_order_canary_hard_controls_preflight_packet_v1`

Suggested decisions:

- `APPROVE_DEMO_ORDER_CANARY_READINESS_REVIEW_ONLY_NO_ORDER_PLACEMENT`
- `REQUEST_HUMAN_DEMO_ORDER_CANARY_APPROVAL_WITH_HARD_CONTROLS_NO_ORDER_PLACEMENT`

Important:

- Do not implement `MetaTrader5`.
- Do not construct an actual MT5 request.
- Do not construct an order payload.
- Do not dispatch.
- Do not place a demo order.
- Do not ask the user to “try one demo order.”
- The next block may request human canary approval, but must not itself place or enable order placement.

Likely remaining gates before one controlled demo canary:

1. Demo-order canary readiness review human decision.
2. Canary hard-controls preflight packet.
3. Human demo-order canary approval artifact.
4. Inert final pre-dispatch audit packet.
5. Only after separate explicit human approval: one tightly controlled demo-order path with kill switch, idempotency ledger, max-lot cap, server lock, symbol lock, and immediate post-order audit.

Do not skip these boundaries.

## 17. Exact Commands To Verify Current State

Start the next session by asking the user to run:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8

python scripts\verify_h024_mt5_request_shape_preview_review_human_decision_jsonl.py reports\h024_standard_demo_mt5_request_shape_preview_review_human_decision.jsonl --allowed-demo-server Exness-MT5Trial6 --require-approved

python scripts\verify_h024_demo_order_readiness_packet_jsonl.py reports\h024_standard_demo_demo_order_readiness_packet.jsonl --allowed-demo-server Exness-MT5Trial6 --require-pass

python scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl --require-pass

python scripts\verify_h024_ea_source_static.py

Expected:

Branch up to date with origin/main
Untracked reports/ only
Latest code commit before handoff: 8132f11 Add H024 demo-order readiness packet
MT5 request-shape preview review human decision: PASS
Demo-order readiness packet: PASS
Boundary verifier: 47 files, PASS, 0 prohibited findings
Static EA verifier: PASS

Full suite anchor:

python -m pytest -q

Latest known result:

1356 passed in 22.28s
18. Exact First Response The Next AI Should Give

The next AI should say:

Understood. Continuing from HANDOFF_96.

I understand:

H024 is Phase 4-approved.
H024 now has a verified pure-Python non-mutating path through no-op adapter use, broker-request preview envelope, inert broker-request draft envelope, MT5 request-shape design review, inert MT5 request-shape preview envelope, MT5 request-shape preview review approval, and a demo-order readiness packet.
The latest pushed code commit before this handoff is 8132f11 Add H024 demo-order readiness packet.
The latest validation anchor is 1356 passed, static EA verifier PASS, and adapter boundary static verifier PASS scanning 47 files with zero prohibited findings.
H024 is still not approved to construct an actual broker request, not approved to construct an actual MT5 request, not approved to construct an order payload, not approved to dispatch, not approved to place demo/live orders, and not execution-approved.
The next safe engineering step is a pure-Python, review-only block for demo-order canary readiness review and hard-controls preflight, still non-dispatchable, still no MT5 import/call, still no terminal/broker mutation, and still no order placement.

Please run:

cd C:\Users\equin\Documents\institutional-ea
..venv\Scripts\Activate.ps1
git status
git log --oneline -8
python scripts\verify_h024_demo_order_readiness_packet_jsonl.py reports\h024_standard_demo_demo_order_readiness_packet.jsonl --allowed-demo-server Exness-MT5Trial6 --require-pass
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

Do not treat demo-order readiness packet as canary approval.

Do not treat MT5 request-shape preview as an actual MT5 request.

Do not treat any shape/draft/preview artifact as an order payload.

The next step is still pure Python, inert, review-only, non-dispatchable, and non-mutating.

20. Compact Continuation Prompt For Another AI

Paste this to another AI if not using the file directly:

You are continuing the Institutional EA project from HANDOFF_96.

You are a senior quant engineer and mentor helping a solo retail trader on Windows build H024, a USDJPY + XAUUSD MT5 expert advisor with institutional-grade safety discipline.

Read and obey docs/operations/handoffs/HANDOFF_96.md. If anything conflicts with older handoffs, HANDOFF_96 wins.

Current state:

Latest code commit before handoff: 8132f11 Add H024 demo-order readiness packet.
H024 is Phase 4-approved.
H024 has no-op adapter use approved and invoked.
H024 has broker-request preview and inert broker-request draft gates completed.
H024 has MT5 request-shape design review and inert MT5 request-shape preview gates completed.
H024 has MT5 request-shape preview review approved.
H024 has a demo-order readiness packet constructed.
Latest validation: 1356 passed, static EA verifier PASS, boundary verifier PASS scanning 47 files with zero prohibited findings.
Working tree should be clean except untracked reports/.

Hard boundaries:

Do not import MetaTrader5.
Do not call MT5.
Do not construct an actual MT5 request.
Do not construct an order payload.
Do not dispatch transport.
Do not mutate terminal or broker state.
Do not place demo or live orders.
Do not treat demo-order readiness as demo-order approval.
Execution remains blocked.

User preference:

Do multiple major things per command block when safe.
Do not waste time on tiny incremental changes.
Bundle safe review-only gates together, but never skip safety boundaries.
Use PowerShell, not Bash.
Use one copy/paste block.
Code changes require tests.
Do not commit reports/.

Next safe step:
Build a pure-Python, review-only block for demo-order canary readiness review and canary hard-controls preflight. It must still not approve demo order placement, must not construct actual MT5 requests or order payloads, must not dispatch, and must not mutate terminal/broker state.