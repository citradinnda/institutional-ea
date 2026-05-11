# HANDOFF_95 — H024 Broker-Request Preview Envelope Complete

If this handoff conflicts with any older handoff, this handoff wins.

This document is self-contained. A new AI should be able to continue safely from this handoff without opening older handoffs first.

## 0. One-Sentence State

H024 is Phase 4-approved and now has a fully verified pure-Python, non-mutating broker-request preview envelope path from real intent context, with preview-only construction approval, no MT5 import/call, no broker request construction, no order payload construction, no dispatch, no terminal/broker mutation, no demo/live order approval, and no execution approval.

Latest pushed commit before this handoff:

- `56f609a Add H024 broker-request preview envelope`

## 1. Current Status — Say This Directly If Asked

H024 has left Phase 3 and is in Phase 4 governance.

H024 is not approved to trade.

H024 is not approved to place demo orders.

H024 is not approved to place live orders.

H024 is not approved to call MT5 execution APIs.

H024 is not approved to mutate terminal or broker state.

H024 is not approved to construct an actual broker request.

H024 is not approved to construct an MT5 request.

H024 is not approved to construct an order payload.

H024 is approved for pure-Python, review-only, non-mutating readiness/preview work.

Latest meaningful progress:

- Pure-Python no-op adapter use was approved only for the no-op path.
- The approved no-op adapter-use path was actually invoked and audited.
- Broker-request construction readiness packet was built and verified.
- Preview-only broker-request construction approval was built and verified.
- An inert broker-request preview envelope was built from the real standard-demo H024 intent and allow-state preflight.
- The preview envelope is explicitly not a broker request, not an MT5 request, and not an order payload.
- Boundary static verifier now scans 23 adapter-boundary files with zero prohibited findings.
- Static EA verifier passes.
- Full test suite passed: `1329 passed`.

Correct short answer if asked “what changed since HANDOFF_94?”:

- We moved from fail-closed adapter readiness into no-op adapter use.
- We approved only pure-Python no-op adapter use.
- We invoked that no-op path and proved broker-facing transport still refused.
- We created broker-request construction readiness.
- We approved preview-only broker-request envelope construction.
- We built a stable, inert preview envelope from real H024 intent.
- Execution remains fully blocked.

## 2. Environment

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

Reports are local and intentionally untracked:

- `reports/`

Do not commit `reports/`.

Expected repo state at handoff:

- Branch `main`
- Up to date with `origin/main`
- Latest code commit: `56f609a Add H024 broker-request preview envelope`
- Working tree clean except untracked `reports/`

## 3. Human Preference And Operating Style

The user is tired of ceremony and wants practical progress toward deployment.

Important preference:

- Do not make tiny incremental changes when a fuller, higher-leverage implementation is appropriate.
- Prefer meaningful gate advancement over tiny docs-only changes.
- Use one copy/paste PowerShell block when commands are needed.
- For code edits, tests are mandatory.
- Do not run long real-data diagnostics casually unless explicitly authorized or clearly safety-bound.
- Do not soften deployment boundaries because H024 is promising.
- Never ask the user to “try one demo order” unless the explicit approval gate exists.

Git workflow preference:

- Bundle stage → diff/check → status → commit → push → verify in one PowerShell block.
- Use boring single-line `git add -- "file1" "file2" ...`.
- Do not commit `reports/`.

Morale framing:

- The strategy edge is still unproven in deployment.
- Runtime plumbing is increasingly proven.
- Safety discipline is strong.
- A useful phrase:
  - “A normal trader is trying to be right. You are building a system that can survive being wrong.”

## 4. Non-Negotiable Safety Boundary

Still forbidden unless a later explicit approval gate changes this:

Python / execution:

- `import MetaTrader5`
- `from MetaTrader5 import ...`
- `mt5.initialize`
- `mt5.login`
- `mt5.shutdown`
- `mt5.order_send`
- `mt5.order_check`
- Any broker API call
- Any terminal mutation path

MQL / EA:

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
- Pending order helpers

Operationally forbidden:

- Chart attach/detach automation
- GUI automation
- Live-terminal mutation
- Demo order placement
- Live order placement
- Broker request construction
- MT5 execution adapter that can place an order
- Anything that mutates broker or terminal state

Allowed now:

- Pure-Python governance/readiness code
- Pure-Python fail-closed/no-op/preview artifacts
- Static source boundary verification
- Read-only JSON/JSONL artifact verification
- Inert preview envelope construction
- Tests proving request construction, dispatch, mutation, and execution stay false

## 5. Current Approval Truth Table

Approved / true:

- Phase 4 approved: true
- Demo adapter implementation approved: true
- Execution adapter implementation approved: true
- Adapter-readiness review approved: true
- Adapter-use readiness review approved: true
- No-op adapter use approved: true
- No-op adapter use invoked: true
- Broker-request construction readiness packet passed: true
- Broker-request preview construction approved: true
- Broker-request preview envelope constructed: true
- Preview envelope only: true

Still not approved / false:

- Broker request construction approved: false
- Actual broker request constructed: false
- MT5 request constructed: false
- Order payload constructed: false
- Execution-capable adapter use approved: false
- Execution adapter approved as transport: false
- Broker request approved: false
- MT5 execution approved: false
- Terminal mutation approved: false
- Broker mutation approved: false
- Demo order placement approved: false
- Live order placement approved: false
- Execution approved: false

Do not collapse “preview envelope construction approved” into “broker request construction approved.”

## 6. Latest Code/Artifact Chain

Latest commits:

- `56f609a Add H024 broker-request preview envelope`
- `9e8ebdb Add H024 broker-request construction readiness packet`
- `1cd9885 Add H024 demo adapter no-op use invocation audit`
- `d03403e Add H024 demo adapter no-op use approval`
- `db58b20 Add H024 demo adapter no-op use approval`
- `3ff85c2 Add H024 Phase 4 demo adapter-use readiness human decision`
- `507674e Add H024 Phase 4 demo adapter-use readiness packet`
- `fc14036 Add H024 demo adapter no-op transport contract`

Note:

- There are two no-op use approval commits: `db58b20` and `d03403e`.
- Do not rewrite history. Latest state is validated and pushed.

## 7. Latest Validation Anchors

After `56f609a`:

- Focused broker-request preview tests: `43 passed`
- Broker-request construction readiness verifier: PASS
- Broker-request preview construction approval builder/verifier: PASS
- Broker-request preview envelope builder/verifier: PASS
- Adapter boundary static verifier: PASS
- Adapter-boundary files scanned: 23
- Prohibited findings: 0
- Violations: 0
- Static EA verifier: PASS
- Full suite: `1329 passed in 23.20s`
- Git push: PASS
- Final repo status: clean except untracked `reports/`

## 8. Latest New Files To Know

Broker-request preview envelope:

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
- `docs\operations\H024_STANDARD_DEMO_BROKER_REQUEST_CONSTRUCTION_READINESS_PACKET_RESULT.md`

No-op adapter-use invocation:

- `quantcore\execution\h024_demo_adapter_noop_use_invocation_audit.py`
- `scripts\build_h024_demo_adapter_noop_use_invocation_audit_jsonl.py`
- `scripts\verify_h024_demo_adapter_noop_use_invocation_audit_jsonl.py`
- `tests\test_h024_demo_adapter_noop_use_invocation_audit.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_NOOP_USE_INVOCATION_AUDIT_RESULT.md`

No-op adapter-use approval:

- `quantcore\execution\h024_demo_adapter_noop_use_approval.py`
- `scripts\build_h024_demo_adapter_noop_use_approval_jsonl.py`
- `scripts\verify_h024_demo_adapter_noop_use_approval_jsonl.py`
- `tests\test_h024_demo_adapter_noop_use_approval.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_NOOP_USE_APPROVAL_RESULT.md`

Boundary static verifier:

- `quantcore\execution\h024_demo_adapter_boundary_static_verifier.py`
- `scripts\build_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `scripts\verify_h024_demo_adapter_boundary_static_verifier_jsonl.py`
- `docs\operations\H024_STANDARD_DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER_RESULT.md`

## 9. Local Reports / Artifacts

These are under `reports/` and intentionally untracked.

Latest important artifacts:

- `reports\h024_standard_demo_broker_request_preview_construction_approval.jsonl`
- `reports\h024_standard_demo_broker_request_preview_envelope.jsonl`
- `reports\h024_standard_demo_broker_request_construction_readiness_packet.jsonl`
- `reports\h024_standard_demo_demo_adapter_noop_use_invocation_audit.jsonl`
- `reports\h024_standard_demo_demo_adapter_noop_use_approval.jsonl`
- `reports\h024_standard_demo_demo_adapter_noop_transport_contract.jsonl`
- `reports\h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl`
- `reports\h024_standard_demo_order_intent_simulation.jsonl`
- `reports\h024_standard_demo_execution_safety_controls_allow_state_preflight.jsonl`

Latest preview-envelope state:

- Schema: `h024_broker_request_preview_envelope_v1`
- Kind: `BROKER_REQUEST_PREVIEW_ENVELOPE`
- Status: `PREVIEW_ENVELOPE_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH`
- Decision: `CONSTRUCT_PREVIEW_ENVELOPE_ONLY_REFUSE_DISPATCH`
- Verdict: PASS
- Violations: 0
- Preview envelope constructed: true
- Verified intent consumed: true
- H020 sizing consumed, not reinterpreted: true
- Idempotency key attached: true
- Kill-switch allow-state required: true
- Request construction refused beyond preview: true
- Not MT5 request: true
- Not broker request: true
- Not order payload: true
- Dispatch attempted: false
- Terminal mutated: false
- Broker state mutated: false

## 10. Strategy Context

H024 is a regime-conditioned pullback-continuation hypothesis.

Mechanics:

- Uses slow H4 trend regime.
- Waits for pullback against that regime.
- Enters only after resumption in regime direction.
- Does not use H021 time/session buckets.
- Does not reuse Donchian breakout trigger.
- Uses H020 sizing contract.
- Returns H017-compatible bridge shim.
- Uses H018 hard guard semantics.
- Baseline candidate: hold = 3 H4, stop ATR multiple = 2.0.

Frozen defaults:

- `slow_window = 5`
- `slope_lag = 2`
- `atr_window = 3`
- `pullback_window = 3`
- `min_pullback_atr = 0.25`
- `max_pullback_atr = 3.0`
- `min_slope_atr = 0.05`

H020 sizing must not be bypassed. Adapter/request layers must consume verified intent/sizing artifacts and must not reinterpret sizing, stop geometry, volume step, min/max lot, or risk fraction.

## 11. Real Standard-Demo Intent Context

Observed account/server evidence:

- Broker/company: `Exness Technologies Ltd`
- Server: `Exness-MT5Trial6`
- Currency: USD
- Balance: 10000
- Equity: 10000
- Leverage: 2000

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

This row is evidence only. It is not permission to trade.

## 12. Known Pitfalls

PowerShell:

- Do not use Bash heredocs like `python - <<'PY'`.
- Use PowerShell here-strings and `Write-Utf8NoBom`.
- Avoid fragile multiline `git add` with backticks.
- Use one-line `git add -- "file1" "file2"`.

Static verifier:

- Python files must be scanned via AST, not raw text.
- Comments/docstrings/refusal strings may mention prohibited terms.
- MQL files can be scanned as text.

Governance:

- Do not treat preview envelope approval as broker-request approval.
- Do not treat no-op adapter use approval as execution-capable adapter approval.
- Do not treat allow-state safety preflight as order approval.
- Do not treat WOULD_OPEN as permission to trade.
- Do not treat a JSONL preview envelope as an MT5 request.

Reports:

- Never commit `reports/`.

## 13. Recommended Next Engineering Step

Next safe, practical, high-leverage step:

Build **broker-request construction human decision / approval for inert canonical broker-request draft construction only**, then build the inert canonical draft.

But be precise:

- This still must not import `MetaTrader5`.
- This still must not call MT5.
- This still must not dispatch.
- This still must not place a demo order.
- This still must not place a live order.
- This should only authorize and build an inert canonical broker-request draft object, likely still named carefully as a draft/review artifact.
- The artifact should be serializable JSONL.
- It should consume the preview envelope and verified intent.
- It should preserve:
  - `mt5_request_constructed=false`
  - `order_payload_constructed=false`
  - `transport_dispatch_attempted=false`
  - `terminal_mutated=false`
  - `broker_state_mutated=false`
  - `demo_order_placement_approved=false`
  - `live_order_placement_approved=false`
  - `execution_approved=false`

Suggested next files:

- `quantcore\execution\h024_broker_request_draft_construction_approval.py`
- `scripts\build_h024_broker_request_draft_construction_approval_jsonl.py`
- `scripts\verify_h024_broker_request_draft_construction_approval_jsonl.py`
- `quantcore\execution\h024_broker_request_draft_envelope.py`
- `scripts\build_h024_broker_request_draft_envelope_jsonl.py`
- `scripts\verify_h024_broker_request_draft_envelope_jsonl.py`
- tests for both
- docs for both
- update boundary static verifier target list

Expected schema ideas:

- `h024_broker_request_draft_construction_approval_v1`
- `h024_broker_request_draft_envelope_v1`

Important naming:

- Avoid pretending the draft is an executable MT5 request.
- It is a broker-request draft/review envelope only.
- It should not contain a dict shaped exactly like `MqlTradeRequest`.
- It should not be passed to any transport.
- It should be explicitly not dispatchable.

## 14. Exact Commands To Verify Current State

Run:

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
Latest commit before handoff: 56f609a Add H024 broker-request preview envelope
Preview construction approval: PASS
Preview envelope: PASS
Boundary verifier: 23 files, PASS
Static EA verifier: PASS
15. Exact First Response The Next AI Should Give

Use this exact style:

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
16. Do Not Let The Next AI Do These Things

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

The next step is still pure Python, inert, review-only, and non-mutating.