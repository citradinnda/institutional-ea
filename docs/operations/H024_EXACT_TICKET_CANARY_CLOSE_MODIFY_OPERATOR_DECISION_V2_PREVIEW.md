# H024 Exact-Ticket Canary Close/Modify Operator Decision V2 Preview

This packet is a read-only operator-decision preview for the known H024 XAUUSDm canary.

It does not authorize trading, broker mutation, order checking, order sending, entry, close, modify, SL/TP modification, XAUUSD orders, USDJPY orders, automatic execution, or a trading loop.

## Purpose

The packet upgrades the prior static exact-ticket decision artifact into a stricter operator-intent preview schema.

It exists to make a future human/operator close-or-modify intent unambiguous while preserving the current no-mutation boundary.

## Exact Identity Lock

The only canary identity accepted by this packet is:

- runtime symbol: `XAUUSDm`
- model symbol: `XAUUSD`
- ticket: `4413054432`
- identifier: `4413054432`
- magic: `240024`
- volume: `0.01`
- MT5 position type: `1`

Any mismatch fails closed.

## Upstream Evidence

The builder consumes the latest JSONL records from:

- `h024_runtime_no_mutation_safety_gate.jsonl`
- `h024_unified_read_only_post_canary_runtime_supervision.jsonl`
- `h024_exact_ticket_canary_close_modify_governance.jsonl`
- `h024_exact_ticket_canary_close_modify_decision_artifact.jsonl`
- `h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl`
- `h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl`
- `h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl`
- `h024_runtime_exposure_inventory_safety_supervisor.jsonl`
- `h024_runtime_account_risk_margin_safety_supervisor.jsonl`
- `h024_runtime_tick_spread_safety_supervisor.jsonl`

Every upstream packet must be present, parseable, fresh, PASS, and non-authorizing.

## Operator Decision Preview Schema

Allowed `decision_preview_status` values:

- `NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY`
- `OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY`

Allowed `requested_action` values:

- `NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY`
- `PREVIEW_CLOSE_ONLY`
- `PREVIEW_MODIFY_STOP_LOSS_ONLY`
- `PREVIEW_MODIFY_TAKE_PROFIT_ONLY`
- `PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT`

These are preview values only. They do not authorize close or modify.

## Report

Default output:

```text
reports/h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl

reports/ is generated output and must remain untracked.

Passing Meaning

PASS means:

all upstream read-only evidence is coherent
exact canary identity is locked
operator decision preview is non-ambiguous
action paths remain blocked
no live broker request exists
no dry-run broker request shape exists
broker mutation remains unauthorized

PASS does not mean close, modify, broker mutation, order checking, order sending, or execution is authorized.
