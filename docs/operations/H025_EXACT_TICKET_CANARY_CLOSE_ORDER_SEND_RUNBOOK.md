# H025 Exact-Ticket Canary Close `order_send` Runbook

## Scope

This is H025 Stage 4 only.

It is authorized only for one-shot demo-account closing of the already-open exact canary position:

- Server: Exness-MT5Trial6
- Symbol: XAUUSDm
- Position side to close: sell
- Close side sent: buy
- Volume: 0.01
- Ticket: 4413054432
- Identifier: 4413054432
- Magic: 240024

## Required preconditions

- H025 Stage 3 `order_check` must have passed for the same exact ticket.
- A fresh Stage 4 approval artifact must explicitly authorize `order_send`.
- The account server must be Exness-MT5Trial6.
- The exact position ticket/identifier/magic/symbol/volume/side must match.
- There must be exactly one H024 position for XAUUSDm magic 240024.
- There must be zero H024 pending orders for XAUUSDm magic 240024.
- A pre-send `mt5.order_check` must pass immediately before `mt5.order_send`.

## Hard prohibitions

This stage must not add:

- new entries
- open-trade module
- unattended loop
- close-all
- `symbol_select`
- live-money account support
- scaling
- martingale
- grid
- automatic position creation

## Runtime reports

The approval artifact and execution evidence are written under `reports/` and must remain untracked.

Main report:

`reports/h025_exact_ticket_canary_close_order_send.jsonl`

## Post-send verification

The script verifies after `order_send` that:

- exact ticket `4413054432` is no longer open
- no H024 pending orders exist for XAUUSDm magic 240024
- no extra H024 positions exist for XAUUSDm magic 240024

If verification fails, the report fails closed for operator review.
