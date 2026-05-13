# H025 Exact-Ticket Canary Post-Close Verification Runbook

## Scope

This is H025 Stage 5.

It verifies that the already-executed H025 Stage 4 one-shot demo close succeeded and remains true:

- Exact ticket `4413054432` is no longer open.
- H024 `XAUUSDm` magic `240024` position count is `0`.
- H024 `XAUUSDm` magic `240024` pending order count is `0`.
- The project has no open H024 canary trade.

## Boundary

This stage is read-only verification only.

It must not call:

- `mt5.order_check`
- `mt5.order_send`
- `mt5.symbol_select`

It must not add:

- new entries
- open-trade module
- unattended loop
- close-all
- live-money support
- scaling
- martingale
- grid
- automatic position creation

## Command

```powershell
python scripts\build_h025_exact_ticket_canary_post_close_verification_jsonl.py
Output

Runtime reports are generated under reports/ and must remain untracked:

reports/h025_exact_ticket_canary_post_close_verification.jsonl
reports/h025_exact_ticket_canary_post_close_verification.txt
Expected PASS result
post_close_verified: true
exact_ticket_open: false
h024_position_count: 0
h024_order_count: 0
open_canary_trade_exists: false
