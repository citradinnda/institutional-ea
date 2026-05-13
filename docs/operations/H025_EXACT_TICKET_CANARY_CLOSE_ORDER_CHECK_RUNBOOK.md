# H025 Exact-Ticket Canary Close `order_check` Runbook

## Scope

This is H025 Stage 3 only.

It adds a demo-account-only `mt5.order_check` preflight for closing the already-open exact canary position:

- Server: Exness-MT5Trial6
- Symbol: XAUUSDm
- Current position side: sell
- Close side checked: buy
- Volume: 0.01
- Ticket: 4413054432
- Identifier: 4413054432
- Magic: 240024

## Non-negotiable boundary

This stage does not close the trade.

This stage must not call:

- `mt5.order_send`
- `mt5.symbol_select`

This stage must not add:

- new entries
- open-trade module
- unattended loop
- close-all
- live-money account support
- scaling
- martingale
- grid
- automatic position creation

## Manual approval

The `order_check` script fails closed unless an explicit operator approval artifact is provided.

Default approval path:

`reports/h025_exact_ticket_canary_close_order_check_operator_approval.json`

The approval artifact is runtime evidence and must remain untracked.

## Commands

Write a disabled approval template:

```powershell
python scripts\build_h025_exact_ticket_canary_close_order_check_jsonl.py --write-approval-template reports\h025_exact_ticket_canary_close_order_check_operator_approval.json

After manual review, edit the artifact so:

operator_approved is true
order_check_authorized is true
exact ticket, identifier, symbol, server, magic, volume, side, and intent are unchanged

Run the broker preflight:

python scripts\build_h025_exact_ticket_canary_close_order_check_jsonl.py --approval-json reports\h025_exact_ticket_canary_close_order_check_operator_approval.json

Output report:

reports/h025_exact_ticket_canary_close_order_check.jsonl

Stage 4 remains forbidden

Do not add mt5.order_send until the operator explicitly approves H025 Stage 4.
