# H024 Post-Close Dashboard/Readiness Adapter Runbook

## Purpose

This operational artifact consumes the passing H024 post-close no-open-canary packet and emits a dashboard/readiness-compatible packet for H024.

The old H024 canary was intentionally closed by H025. H024 dashboard/readiness should no longer treat zero H024 positions/orders as an automatic failure when the post-close packet confirms the intentional state.

## Expected operator-facing state

NO OPEN CANARY - INTENTIONALLY CLOSED BY H025

## Inputs

Default input:

reports/h024_post_close_no_open_canary_state.jsonl

The input must confirm:

- verdict PASS
- canary_absence_classification INTENTIONALLY_CLOSED_BY_H025
- exact_ticket_open false
- h024_position_count 0
- h024_order_count 0
- trading_authorized false
- broker_mutation_authorized false
- dashboard_wording NO OPEN CANARY - INTENTIONALLY CLOSED BY H025
- readiness_wording NO OPEN CANARY - INTENTIONALLY CLOSED BY H025

## Outputs

Default outputs:

reports/h024_post_close_dashboard_readiness_adapter.jsonl
reports/h024_post_close_dashboard_readiness_adapter.txt

## PASS meaning

A PASS means H024 dashboard/readiness can display the closed-canary state as an accepted read-only state:

NO OPEN CANARY - INTENTIONALLY CLOSED BY H025

It also means:

- h024_dashboard_compatible true
- h024_readiness_compatible true
- legacy_open_canary_required false
- post_close_no_open_canary_accepted true
- trading_authorized false
- broker_mutation_authorized false

## Safety boundary

This adapter is local evidence adaptation only. It does not reopen the canary and does not perform broker mutation.

Do not add execution modules, new entries, close-all, loops, live-money support, scaling, martingale, or grid behavior.
