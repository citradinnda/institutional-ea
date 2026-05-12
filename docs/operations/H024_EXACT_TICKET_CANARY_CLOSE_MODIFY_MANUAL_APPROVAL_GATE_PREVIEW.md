# H024 Exact-Ticket Canary Close/Modify Manual Approval Gate Preview

## Purpose

This document describes the H024 exact-ticket canary close/modify manual approval gate preview packet.

The packet is read-only. It is a preview/coherence layer only. It does not authorize trading, broker mutation, `order_check`, `order_send`, entry, close, modify, XAUUSD orders, USDJPY orders, automatic execution, or a trading loop.

## Exact Canary Identity

The packet is hard-locked to the known H024 XAUUSDm standard-demo canary:

- server: `Exness-MT5Trial6`
- account currency: `USD`
- runtime symbol: `XAUUSDm`
- model symbol: `XAUUSD`
- ticket: `4413054432`
- identifier: `4413054432`
- magic: `240024`
- volume: `0.01`
- MT5 position type: `1`

Any mismatch fails closed.

## Consumed Upstream Evidence

The preview packet consumes the latest JSONL report for each required upstream:

1. runtime no-mutation safety gate
2. unified read-only post-canary runtime supervision
3. exact-ticket close/modify governance packet
4. exact-ticket close/modify decision artifact validator
5. exact-ticket close/modify pre-action evidence aggregate
6. exact-ticket close/modify bar-age and exit-condition evidence packet
7. runtime exposure/inventory safety supervisor
8. runtime account risk/margin safety supervisor
9. runtime tick/spread safety supervisor

Every upstream must be present, fresh, `PASS`, and have no embedded violations.

## Preview Schema

The packet includes `approval_preview_schema`, a strict explicit operator approval preview schema.

The default status is:

```text
NO_MANUAL_APPROVAL_REQUESTED_PREVIEW_ONLY

The default requested action is:

NO_CLOSE_MODIFY_REQUESTED_PREVIEW_ONLY

Allowed requested-action preview values are intentionally non-executing:

NO_CLOSE_MODIFY_REQUESTED_PREVIEW_ONLY
PREVIEW_CLOSE_ONLY
PREVIEW_MODIFY_STOP_LOSS_ONLY
PREVIEW_MODIFY_TAKE_PROFIT_ONLY
PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT

These values describe review intent only. They do not authorize a broker request.

Required Blocking Fields

The following must remain blocked:

effective_new_entries_blocked = true
broker_mutation_authorized = false
order_check_authorized = false
order_send_authorized = false
entry_authorized = false
close_modify_authorized = false
xauusd_order_authorized = false
usdjpy_order_authorized = false
trading_loop_authorized = false
automatic_execution_authorized = false
symbol_select_authorized = false
manual_approval_gate_preview_authorizes_action = false
live_broker_request_constructed = false
dry_run_request_shape_preview_constructed = false
Passing Operator State

A passing packet uses:

EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED

Operator next action:

KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_MANUAL_APPROVAL_GATE_PREVIEW

A PASS means only that the read-only manual approval gate preview is coherent for operator review. It does not authorize close/modify.

Fail-Closed Operator State

A fail-closed packet uses:

FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_BLOCKED

Operator next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED
Build
python scripts\build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars

Report path:

reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl
Verify
python scripts\verify_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py reports\h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl --require-pass
Safety Boundary

This milestone does not create, close, modify, or check any order. It does not call broker mutation functions. It does not call symbol selection. It does not construct a live broker request.

The only permitted output is read-only JSONL evidence for operator review.
