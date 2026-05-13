# DEMO_AUTOMATION_READINESS_BRIDGE Runbook

## Purpose

This is an operational bridge toward controlled demo automation.

It is not a new strategy hypothesis and does not allocate a new H0** ID.

The bridge consumes:

reports/h024_post_close_operational_completion.jsonl

and opens the next practical target:

INERT_DEMO_ENTRY_REQUEST_PREVIEW

## Why this exists

The old H024 canary is closed and post-close observer work is complete enough to stop looping on the missing canary.

The project should now move toward controlled demo automation by defining an inert demo entry preview before any order-capable action is introduced.

## Symbol policy

Allowed demo symbols:

- USDJPYm
- XAUUSDm

Banned symbols:

- EURUSDm
- GBPUSDm
- US500m

This carries forward the Strategy Graveyard findings: only USDJPYm and XAUUSDm remain in the active research universe; EURUSDm, GBPUSDm, and US500m are banned unless a future pre-registered hypothesis gives a new evidence-based reason to re-test them.

## Risk policy carried forward

- max_risk_per_trade_pct: 0.5
- max_portfolio_heat_pct: 1.0

## PASS meaning

A PASS means the project is ready to implement an inert demo entry request preview.

It does not authorize trading.

It does not authorize:

- broker mutation
- order checks
- order sends
- symbol selection
- new entries
- close-all behavior
- unattended loops
- live-money support

## Next implementation target

INERT_DEMO_ENTRY_REQUEST_PREVIEW

The preview should define these fields without broker mutation:

- account_server
- symbol
- model_symbol
- strategy_signal_source
- model_artifact_manifest
- live_candle_parity_snapshot
- entry_side_preview
- volume_preview
- risk_per_trade_pct_preview
- portfolio_heat_pct_preview
- atr_stop_distance_preview
- spread_snapshot
- slippage_assumption
- kill_switch_state
- operator_approval_required_for_any_future_order_check

## Safety boundary

This bridge is read-only local evidence validation only.

Do not add broker mutation here.
