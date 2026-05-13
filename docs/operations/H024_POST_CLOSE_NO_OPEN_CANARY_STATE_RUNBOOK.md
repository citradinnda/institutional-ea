# H024 Post-Close No-Open-Canary State Runbook

## Current source of truth

HANDOFF_120 is the active handoff and supersedes older handoffs.

The original H024 canary trade is already closed:

- Server: Exness-MT5Trial6
- Symbol: XAUUSDm
- Model symbol: XAUUSD
- Side: sell
- Volume: 0.01
- Ticket: 4413054432
- Identifier: 4413054432
- Magic: 240024

H025 Stage 4 closed the exact ticket. H025 Stage 5 verified the exact ticket is closed and that H024 has zero positions and zero orders.

## Purpose

This operational artifact teaches the H024 observer path that the old canary being absent is no longer automatically a failure when H025 Stage 5 has verified the post-close state.

Expected operator-facing wording:

NO OPEN CANARY - INTENTIONALLY CLOSED BY H025

## Safety boundary

This artifact is read-only only.

Do not add broker mutation. Do not reopen the canary. Do not rerun H025 Stage 4. Do not add new entries, close-all, unattended loops, live-money support, scaling, martingale, or grid behavior.

## Packet

Script:

scripts/build_h024_post_close_no_open_canary_state_jsonl.py

Default input:

reports/h025_exact_ticket_canary_post_close_verification.jsonl

Default outputs:

reports/h024_post_close_no_open_canary_state.jsonl
reports/h024_post_close_no_open_canary_state.txt

## PASS criteria

The packet returns PASS only when the Stage 5 packet confirms:

- verdict is PASS
- post_close_verified is true
- open_canary_trade_exists is false
- exact_ticket_open is false
- h024_position_count is 0
- h024_order_count is 0

The packet always reports:

- trading_authorized false
- broker_mutation_authorized false
- entry_authorized false
- close_all_authorized false
- live_money_authorized false
