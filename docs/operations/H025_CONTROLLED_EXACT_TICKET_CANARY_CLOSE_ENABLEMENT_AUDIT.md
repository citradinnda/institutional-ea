# H025 Controlled Exact-Ticket Canary Close Enablement Audit

## Scope

H025 is separate from H024.

H024 remains read-only. H024 must not gain broker mutation, close/modify execution, entries, order-capable loops, `mt5.order_check`, `mt5.order_send`, or `mt5.symbol_select`.

H025 is the controlled path toward closing the already-open exact canary trade only:

- Server: Exness-MT5Trial6
- Symbol: XAUUSDm
- Side currently open: sell
- Volume: 0.01
- Ticket: 4413054432
- Identifier: 4413054432
- Magic: 240024
- Demo account only

## Existing H024 exact-ticket artifacts being reused

The following H024 read-only artifacts already exist and are reused as upstream governance/evidence concepts:

- `scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py`
- `scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py`

## H025 staged progression

### Stage 1 - Audit existing exact-ticket artifacts

Status: implemented by this document.

Purpose: identify and preserve the existing governance/evidence artifacts instead of restarting from generic `would_open` or generic `INTENT`.

### Stage 2 - Exact-ticket close request preview

Status: implemented by `scripts/build_h025_exact_ticket_canary_close_request_preview_jsonl.py`.

Purpose: produce an inert, non-submittable close-request shape for the exact known canary only.

The preview may describe the close shape, but it must not submit anything to MetaTrader 5.

### Stage 3 - Demo-account-only `mt5.order_check`

Status: not implemented in this milestone.

Must be behind manual operator approval and exact-ticket constraints.

### Stage 4 - One-shot demo-account-only `mt5.order_send`

Status: not implemented in this milestone.

Must require explicit confirmation after Stage 3.

### Stage 5 - Verify closure and no extra H024 exposure

Status: not implemented in this milestone.

## Hard prohibitions still active after this milestone

- No new entries.
- No open-trade module.
- No unattended loop.
- No close-all.
- No symbol selection unless separately gated and explicitly required.
- No live-money account.
- No scaling.
- No martingale.
- No grid.
- No automatic position creation.
- No H024 broker mutation.
- No H025 `order_check` until a separate approved Stage 3 commit.
- No H025 `order_send` until a separate explicit Stage 4 confirmation.
