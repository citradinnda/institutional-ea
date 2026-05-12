# H024 Read-Only VPS Deployment Readiness Aggregate

## Purpose

This packet moves H024 from governance-only artifacts toward operational read-only VPS observation.

It verifies that the repo can run the H024 observer workflow on a VPS as read-only packet generation and reporting. It does not authorize trading.

## Hard boundary

This packet and its runner authorize no broker mutation.

It authorizes:

- no order_check
- no order_send
- no entries
- no close/modify
- no XAUUSD order
- no USDJPY order
- no symbol_select
- no executable trade request
- no live broker request
- no MT5 request dictionary
- no order-capable trading loop
- no automatic execution

A PASS means read-only VPS observer readiness is coherent for operator review.

A PASS does not mean trading is authorized.

## Consumed upstream reports

The readiness aggregate consumes latest JSONL records for:

- runtime heartbeat
- runtime lockout reader
- tick/spread supervisor
- exposure/inventory supervisor
- account risk/margin supervisor
- runtime safety aggregate
- unified read-only runtime supervision
- runtime no-mutation safety gate
- exact-ticket close/modify governance
- exact-ticket decision artifact validator
- exact-ticket pre-action evidence aggregate
- exact-ticket bar-age exit-condition evidence
- exact-ticket manual approval gate preview
- exact-ticket operator decision v2 preview
- exact-ticket execution readiness dry-run schema preview
- read-only black-swan guard

The aggregate fails closed if any upstream report is missing, malformed, stale, fail-closed, has embedded violations, has unsafe authorization, has an executable/live request object, or does not preserve the exact known XAUUSDm canary identity where required.

## Exact canary identity

Expected canary:

- server: Exness-MT5Trial6
- account currency: USD
- runtime symbol: XAUUSDm
- model symbol: XAUUSD
- side: sell
- MT5 position type: 1
- volume: 0.01
- magic: 240024
- ticket/identifier: 4413054432

## Environment checks

The packet checks:

- repository base directory exists
- reports/ exists and is writable
- Python venv is active or sys.executable is under .venv
- MetaTrader5 package is importable unless explicitly allowed by CLI override
- operator runbook commands do not contain broker mutation tokens

MT5 runtime/account/server checks are consumed from the existing read-only runtime heartbeat packet.

## Operator commands

From repo root:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1
python scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass

Scheduled task preview for operator review only:

schtasks /Create /SC MINUTE /MO 5 /TN H024ReadOnlyObserver /TR "powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_once.ps1"

The packet does not create the scheduled task. The command is documentation/preview only.

Expected output

Report:

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Passing state:

Verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED
Violations: 0

Fail-closed state:

Verdict: FAIL_CLOSED
Operator state: FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_UNVERIFIED_NO_TRADING_AUTHORIZED
Operator next action: FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED
Runner behavior

scripts/run_h024_read_only_vps_observer_once.ps1 runs the existing read-only upstream builders, verifies black-swan guard, builds the VPS deployment readiness aggregate, and verifies it with --require-pass.

It is an observer runner only. It does not call broker mutation functions and does not invoke historical one-shot canary scripts.

Validation

Focused validation:

python -m pytest tests\test_h024_read_only_vps_deployment_readiness_aggregate.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1
python scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass

Keep reports/ untracked.