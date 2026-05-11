# H024 Demo-Only Execution Adapter Design Spec

## Status

Review-only design spec.

This is not an execution adapter. It does not approve an execution adapter. It does not approve demo order placement. It does not approve live order placement. It does not approve Phase 4.

## Current Input Chain

The design may only be considered after the following artifacts have passed:

1. H024 runtime CSV verification.
2. H024 dry-run request JSONL verification.
3. H024 review-only demo-order plan verification.
4. H024 broker metadata preflight verification.
5. H024 order-intent simulation verification.
6. H024 manual approval checkpoint verification.

## Non-Negotiable Boundary

Forbidden in this design stage:

- `OrderSend`
- `OrderSendAsync`
- `OrderCheck`
- `CTrade`
- `MqlTradeRequest`
- `MqlTradeResult`
- MT5 Python imports
- broker API calls
- broker request construction
- chart automation
- terminal mutation
- demo order placement
- live order placement

## Required Future Adapter Inputs

A future adapter, if separately approved, must accept only a verified manual approval checkpoint artifact and must re-check:

- allowed demo server
- account currency
- symbol normalization
- side/action consistency
- stop geometry
- tick alignment
- volume min/max/step/digits
- estimated loss not above risk budget
- explicit human approval reference
- no live-like server
- no execution-like payload inherited from review artifacts

## Required Future Controls

A future adapter design review must require:

- kill switch design
- idempotency key design
- maximum one-action-per-reviewed-intent design
- immutable audit logging design
- failure-mode table
- rejection-first behavior
- no fallback from demo to live
- full static source verification
- full test suite
- explicit human approval artifact

## Interpretation

This spec is a gate. It makes the next unsafe step visible. It is not permission to take that step.