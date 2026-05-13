# H025 Controlled Exact-Ticket Canary Close Enablement Audit

## Scope

H025 is separate from H024.

H024 remains read-only. H024 must not gain broker mutation, close/modify execution, entries, order-capable loops, `mt5.order_check`, `mt5.order_send`, or `mt5.symbol_select`.

H025 is the controlled path toward closing the already-open exact canary trade only:

- Server: Exness-MT5Trial6
- Symbol: XAUUSDm
- Current position side: sell
- Required close side preview: buy
- Volume: 0.01
- Ticket: 4413054432
- Identifier: 4413054432
- Magic: 240024
- Demo account only

## Existing H024 exact-ticket artifacts reused

- `scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py`

## Stage status

### Stage 1 - Audit existing exact-ticket artifacts

Implemented here.

### Stage 2 - Exact-ticket close request preview

Implemented by `scripts/build_h025_exact_ticket_canary_close_request_preview_jsonl.py`.

This creates an inert, non-submittable close-request preview for ticket/identifier `4413054432` only.

### Stage 3 - Demo-account-only `mt5.order_check`

Not implemented.

### Stage 4 - One-shot demo-account-only `mt5.order_send`

Not implemented.

### Stage 5 - Verify exact ticket closed and no extra H024 positions/orders exist

Not implemented.

## Hard prohibitions still active

- No new entries.
- No open-trade module.
- No unattended loop.
- No close-all.
- No `symbol_select`.
- No live-money account.
- No scaling.
- No martingale.
- No grid.
- No automatic position creation.
- No H024 broker mutation.
- No H025 `order_check` until separate Stage 3 authorization.
- No H025 `order_send` until separate explicit Stage 4 confirmation.
