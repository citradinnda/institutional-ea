# H026 / H024-Post-Close Read-Only No-Open-Canary Observer State Runbook

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

H026 teaches the H024 observer/dashboard/readiness path that the old canary being absent is no longer automatically a failure when H025 Stage 5 has verified the post-close state.

Expected operator-facing wording:

NO OPEN CANARY - INTENTIONALLY CLOSED BY H025

## Safety boundary

This milestone is read-only only.

Do not add broker mutation. Do not reopen the canary. Do not rerun H025 Stage 4. Do not add new entries, close-all, unattended loops, live-money support, scaling, martingale, or grid behavior.

The H026 packet consumes H025 Stage 5 evidence. It does not call broker execution APIs.

## Packet

Script:

scripts/build_h026_h024_post_close_no_open_canary_state_jsonl.py

Default input:

reports/h025_exact_ticket_canary_post_close_verification.jsonl

Default outputs:

reports/h026_h024_post_close_no_open_canary_state.jsonl
reports/h026_h024_post_close_no_open_canary_state.txt

## PASS criteria

H026 returns PASS only when the Stage 5 packet confirms:

- verdict is PASS
- post_close_verified is true
- open_canary_trade_exists is false
- exact_ticket_open is false
- h024_position_count is 0
- h024_order_count is 0

H026 always reports:

- trading_authorized false
- broker_mutation_authorized false
- entry_authorized false
- close_all_authorized false
- live_money_authorized false

## FAIL_CLOSED criteria

H026 fails closed when:

- Stage 5 evidence is missing
- Stage 5 evidence is malformed
- Stage 5 verdict is not PASS
- post-close verification is not true
- the exact ticket is still open
- open canary trade exists
- H024 position count is not zero
- H024 order count is not zero

In those cases, absence is classified as:

UNEXPECTED_MISSING_CANARY_OR_STAGE5_UNVERIFIED

## Validation

Run:

python -m py_compile scripts\build_h026_h024_post_close_no_open_canary_state_jsonl.py
python -m py_compile tests\test_h026_h024_post_close_no_open_canary_state.py
python -m pytest tests\test_h026_h024_post_close_no_open_canary_state.py -q
python scripts\build_h026_h024_post_close_no_open_canary_state_jsonl.py

Expected PASS output includes:

NO OPEN CANARY - INTENTIONALLY CLOSED BY H025

Expected final git state before committing source files:

- tracked changes for the new H026 script, test, and runbook
- reports/ remains untracked
