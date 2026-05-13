# H024 Standard Demo Existing Path Map Runbook

## Purpose

This artifact stops the project from building parallel standalone scaffolding.

It inspects the existing H024 standard-demo trade path already present in the repo and maps the shortest route toward controlled demo order_check/order_send.

## This artifact is read-only

It does not import MetaTrader5.
It does not call order_check.
It does not call order_send.
It does not call symbol_select.
It does not construct executable trade requests.
It does not authorize trading.

## Existing H024 standard-demo chain

The mapped path is:

1. quantcore/execution/h024_order_intent_simulation.py
2. quantcore/execution/h024_dry_run.py
3. quantcore/execution/h024_dry_run_log.py
4. quantcore/execution/h024_runtime_*_safety_supervisor.py
5. quantcore/execution/h024_manual_approval_checkpoint.py
6. quantcore/execution/h024_broker_request_draft_envelope.py
7. docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md
8. future demo order_check gate, requiring fresh explicit operator approval
9. future one-shot demo order_send gate, requiring separate future operator approval

## PASS meaning

A PASS means the real existing H024 standard-demo path has been identified and the next useful target is:

H024_STANDARD_DEMO_EXISTING_PATH_REPLAY

A PASS does not mean order_check or order_send is authorized.

## Safety boundary

Any future order_check or order_send step must be separate, explicit, demo-only, and manually authorized.

Do not use this path map as approval for broker mutation.
