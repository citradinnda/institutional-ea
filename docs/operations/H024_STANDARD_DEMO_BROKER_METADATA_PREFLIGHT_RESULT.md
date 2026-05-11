# H024 Standard Demo Broker Metadata Preflight Result

## Verdict

PASS.

This is a pure Python, offline metadata preflight result. It is not an MT5 order request, not a demo order, not a live order, and not Phase 4 approval.

## Inputs

Review-only proposed plan JSONL:

- `reports\h024_standard_demo_demo_order_plans.jsonl`

Offline broker metadata snapshot:

- `reports\h024_standard_demo_broker_metadata_snapshot.json`

Explicit demo server allowlist:

- `Exness-MT5Trial6`

## Offline Metadata Snapshot

The XAUUSDm metadata snapshot used for this preflight was derived from the preserved standard-demo runtime evidence:

- symbol: `XAUUSDm`
- normalized symbol: `XAUUSD`
- server: `Exness-MT5Trial6`
- account currency: `USD`
- tick size: `0.001`
- tick value: `0.1`
- minimum volume: `0.01`
- maximum volume: `200.0`
- volume step: `0.01`
- volume digits: `2`
- price digits: `3`
- spread points: `16.0`

## Commands

```powershell
python scripts\build_h024_broker_metadata_preflight_jsonl.py `
  reports\h024_standard_demo_demo_order_plans.jsonl `
  --metadata-json reports\h024_standard_demo_broker_metadata_snapshot.json `
  --output-jsonl reports\h024_standard_demo_broker_metadata_preflight.jsonl `
  --allowed-demo-server Exness-MT5Trial6 `
  --require-preflight

python scripts\verify_h024_broker_metadata_preflight_jsonl.py `
  reports\h024_standard_demo_broker_metadata_preflight.jsonl `
  --allowed-demo-server Exness-MT5Trial6 `
  --require-preflight
Observed Result

Builder:

Plans read: 1
Preflight records produced: 1
Violations: 0
Verdict: PASS

Verifier:

Preflight records: 1
Violations: 0
Verdict: PASS
Safety Interpretation

The generated preflight artifact has schema:

h024_broker_metadata_preflight_v1

and kind:

BROKER_METADATA_PREFLIGHT_REVIEW_ONLY

It validates, offline only:

proposed plan schema and plan kind
demo server allowlist
symbol normalization
account currency
broker tick size and tick value
broker min/max/step/digit volume constraints
entry and stop tick alignment
stop geometry
estimated metadata loss within intended risk_usd
risk fraction cap
preservation of mode=log_only_no_execution

This advances the Phase 4 readiness design chain but does not approve execution code or order placement.
