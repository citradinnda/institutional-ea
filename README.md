# Institutional EA

Personal research and production code for a USDJPY + XAUUSD MetaTrader 5 expert advisor.

This repository is infrastructure-first research. It is not a live-trading system.

## Current Status

- Current hypothesis: H017.
- H017 status: failed / not promotable.
- Failure mode: strict expanded broker-native event-driven validation failed by account insolvency.
- H018 boundary planning: opened as governance only; no H018 validation is authorized yet.
- Live trading approved: False.
- Phase 4 execution work: not approved.

The strict expanded broker-native validation used Exness demo MT5 USDJPY and XAUUSD H4/M1 exports under complete bridge-window rules. The data/source preflight passed, but H017 failed during event-driven validation.

The fatal validation result is documented here:

- `docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT.md`
- `docs/operations/BROKER_NATIVE_EXPANDED_STRICT_H017_VALIDATION_RESULT_OUTPUT.txt`

The formal hypothesis status is documented here:

- `docs/operations/HYPOTHESIS_LEDGER.md`

The operational run log is documented here:

- `docs/operations/H017_EVENT_VALIDATION_RUN_LOG.md`

The H018 boundary decision plan is documented here:

- `docs/operations/H018_BOUNDARY_DECISION_PLAN.md`
- `docs/operations/H018_MINIMUM_STOP_DISTANCE_DECISION_PLAN.md`
- `docs/operations/H018_MAX_NOTIONAL_LEVERAGE_DECISION_PLAN.md`
- `docs/operations/H018_EXECUTABLE_ENTRY_SIZING_DECISION_PLAN.md`

## Guardrails

Do not treat source acceptance as strategy promotion.

Do not tune H017 to hide the insolvency result.

Do not silently change sizing semantics, cost assumptions, or H017 parameters.

Do not use HistData for H017 validation under current evidence.

Do not broaden to more symbols or add machine learning until a new explicit hypothesis phase authorizes it.

## Environment

- Operating system: Windows.
- Shell: PowerShell.
- Python: 3.12.x.
- Virtual environment: `.venv`.

Typical setup:

    cd C:\Users\equin\Documents\institutional-ea
    py -3.12 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -e .[dev]
    pytest -q

Current full-test anchor after H017 equality invalid-stop tests:

    537 passed

## H018 decision matrix

H018 execution-semantics and account-risk planning is consolidated in docs/operations/H018_DECISION_MATRIX.md. This matrix is governance-only: it does not choose thresholds, implement guards, validate H018, promote H017, approve live trading, or approve Phase 4 execution work.

## H018 claim skeleton

A governance skeleton for any future H018 claim is documented in docs/operations/H018_CLAIM_SKELETON.md. It defines required claim fields, synthetic-test gates, source gates, event-validation gates, and non-promotion language. It does not implement H018, validate H018, promote H017, approve live trading, or approve Phase 4 execution.
