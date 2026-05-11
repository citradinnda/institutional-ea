# H024 Phase 4 Readiness Gate

## Status

H024 is meaningfully closer to a Phase 4 review, but it is not Phase 4-approved.

Current status:

- Research-only
- Log-only
- Not live-approved
- Not Phase 4-approved
- Not execution-approved
- No demo order placement approved
- No execution adapter approved

This document defines the gate between the current verified log-only/dry-run evidence and any future demo-only execution adapter design.

## Non-Negotiable Boundary

Do not add or use any of the following until this gate is explicitly passed and documented:

- `OrderSend`
- `OrderSendAsync`
- `OrderCheck`
- `CTrade`
- `MqlTradeRequest`
- `MqlTradeResult`
- `PositionOpen`
- `PositionClose`
- `PositionModify`
- pending-order helpers
- chart attach/detach automation
- GUI automation
- live-terminal mutation
- live trading
- demo trading

A dry-run request is not an order request.

A `WOULD_OPEN` intended-action row is not permission to trade.

## Evidence Now Achieved

### Runtime log-only evidence

Standard demo replay-sweep runtime result:

- server: `Exness-MT5Trial6`
- account currency: `USD`
- account balance: `10000.00`
- account equity: `10000.00`
- symbols: `USDJPYm`, `XAUUSDm`
- runtime verifier: PASS
- rows: 229
- violations: 0
- intended-action summary: PASS

Unique real demo-balance signal:

- symbol: `XAUUSDm`
- normalized symbol: `XAUUSD`
- timeframe: `H4`
- action: `WOULD_OPEN`
- side: `short`
- closed H4 time: `2026.03.18 08:00:00`
- entry: `4930.0410000000`
- stop: `5019.0680000000`
- raw lots: `0.0112325474`
- final lots: `0.0100000000`
- risk USD: `100.00`

Preserved in:

- `docs\operations\H024_STANDARD_DEMO_BALANCE_REPLAY_SWEEP_RUNTIME_RESULT.md`

### Dry-run reconciliation evidence

CSV-read-only reconciliation result:

- input CSV: `reports\h024_ea_log_only_preflight.csv`
- rows: 229
- intended-action rows: 6
- WOULD_OPEN rows: 1
- dry-run requests: 1
- skipped non-request rows: 5
- verdict: PASS

Preserved in:

- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_RECONCILIATION_RESULT.md`

### Dry-run request audit evidence

Reconstructed request audit:

- requests: 1
- violations: 0
- verdict: PASS

Audited request:

- schema version: `h024_dry_run_execution_request_v1`
- request kind: `DRY_RUN_MARKET_OPEN`
- source schema version: `h024_intended_action_log_v1`
- symbol: `XAUUSDm`
- normalized symbol: `XAUUSD`
- timeframe: `H4`
- side: `SELL`
- entry price: `4930.041`
- stop loss: `5019.068`
- risk USD: `100.0`
- volume lots: `0.01`

Preserved in:

- `docs\operations\H024_STANDARD_DEMO_DRY_RUN_REQUEST_JSONL_AUDIT_RESULT.md`

### Repeatable verifier evidence

Reusable dry-run request JSONL verifier added in:

- `scripts\verify_h024_dry_run_request_jsonl.py`
- `tests\test_h024_dry_run_request_jsonl_verifier.py`

Latest validation anchor at creation:

- focused JSONL verifier tests: 6 passed
- current JSONL verifier: PASS
- full suite: 970 passed
- static EA verifier: PASS

Latest supporting commit:

- `b7ce340 Add H024 dry-run request JSONL verifier`

## Why This Is Not Yet Phase 4 Approval

The current system proves:

- the EA can emit a log-only intended action
- runtime logs can be verified
- a real 10000.00 USD standard demo account balance can size a nonzero `WOULD_OPEN`
- the runtime CSV can reconstruct exactly one dry-run request
- the dry-run request can be audited against a contract

The current system does not yet prove:

- safe construction of an MT5 order request
- safe broker-side preflight checking
- safe handling of slippage, filling mode, deviation, magic number, or comments
- safe prevention of duplicate orders
- safe behavior under terminal reconnects
- safe behavior under symbol metadata drift
- safe behavior after partial failure
- safe post-order audit and reconciliation
- safe demo-only containment
- safe kill-switch behavior around actual order submission

## Phase 4 Readiness Gate

H024 may enter Phase 4 design review only after all items below are satisfied.

### Gate A — Evidence Chain

Required:

- standard demo runtime CSV verifier PASS
- intended-action runtime summary PASS
- at least one real demo-balance `WOULD_OPEN` row with nonzero final lots
- dry-run reconciliation PASS with `--require-request`
- dry-run request JSONL verifier PASS with `--require-request`
- no request reconstructed from `NO_ACTION`
- no request reconstructed from `BLOCKED`

Current status:

- PASS

### Gate B — Runtime Safety Boundary

Required:

- EA source static verifier PASS
- no execution primitives in the EA
- no `OrderSend`
- no `OrderSendAsync`
- no `OrderCheck`
- no `CTrade`
- no `MqlTradeRequest`
- no `MqlTradeResult`
- no chart attach automation
- no GUI automation

Current status:

- PASS

### Gate C — Demo-Only Execution Adapter Design Spec

Required before code:

- explicit statement that adapter is demo-only
- explicit allowed account server list
- explicit denied live-server behavior
- explicit symbol allowlist
- explicit volume cap
- explicit risk cap
- explicit one-request-at-a-time behavior
- explicit idempotency / duplicate-prevention rule
- explicit order comment format
- explicit magic number policy
- explicit no-position / existing-position behavior
- explicit failure-mode table
- explicit post-order audit fields
- explicit rollback / disable procedure

Current status:

- NOT STARTED

### Gate D — Order Construction Contract

Required before code:

- pure Python order-construction contract
- no MT5 access
- no order sending
- maps dry-run request to a proposed demo order object
- rejects invalid side
- rejects invalid stop geometry
- rejects zero/negative volume
- rejects unknown symbols
- rejects request schema mismatch
- rejects live account/server context
- preserves source reason and source timestamp
- covered by focused tests

Current status:

- NOT STARTED

### Gate E — Broker Metadata Preflight Design

Required before any actual order check or send:

- read-only symbol metadata probe design
- allowed filling-mode handling
- volume min/max/step validation
- point/digits validation
- stops-level validation
- freeze-level validation
- spread sanity check
- market-open/trading-enabled checks
- deterministic failure behavior

Current status:

- NOT STARTED

### Gate F — Demo-Only Dry-Run-to-Order Simulation

Required before MT5 order code:

- pure simulation consumes verified dry-run JSONL
- emits proposed order plan
- verifies SELL stop is above entry
- verifies BUY stop is below entry
- verifies volume is broker-step aligned
- verifies risk cap is preserved
- verifies no execution-like side effects
- full test coverage

Current status:

- NOT STARTED

### Gate G — Manual Approval Checkpoint

Required before any execution adapter code:

- written approval document naming the exact adapter scope
- explicit statement that approval is demo-only
- explicit statement that live trading remains forbidden
- explicit rollback plan
- latest full test suite PASS
- latest static EA verifier PASS
- clean git status except `reports/`

Current status:

- NOT STARTED

## Recommended Next Engineering Step

Next safe action:

Build a pure Python demo-only order construction contract from the audited dry-run request JSONL.

The contract must not import MT5, must not call MT5, and must not create `MqlTradeRequest`.

It should produce an internal proposed-order object only, suitable for review.

Suggested files:

- `quantcore\execution\h024_demo_order_plan.py`
- `tests\test_h024_demo_order_plan.py`

The word "demo" in this contract does not approve demo order placement. It only names the future target environment.

## Current Verdict

H024 is close enough to begin Phase 4 readiness planning.

H024 is not Phase 4-approved.

Do not add execution code yet.

The next approved work is design-contract code only: dry-run request to proposed demo-order plan, with no MT5 access and no order execution.
