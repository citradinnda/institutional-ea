# H024 One-Shot Standard-Demo Canary Supervisory State

## Purpose

This packet is the top-level read-only supervisor for the H024 XAUUSDm one-shot standard-demo canary.

It consumes the current monitor, lifecycle-decision, and observation-analysis packets and emits a single operational state:

- continue observing the open canary
- recommend human review without code mutation
- accept a closed-explained state without re-entry
- stop and investigate local evidence inconsistency

## Inputs

Local runtime inputs under `reports/`:

- `reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl`
- `reports/h024_standard_demo_one_shot_demo_canary_lifecycle_decision.jsonl`
- `reports/h024_standard_demo_one_shot_demo_canary_observation_analysis.jsonl`

These files are local runtime evidence and must not be committed.

## Output

Local runtime output:

- `reports/h024_standard_demo_one_shot_demo_canary_supervisory_state.jsonl`

This file must not be committed.

## Automation boundary

The supervisor is part of observation automation.

It treats any mutation authorization in any consumed packet as a fail-closed violation, even if another packet says false.

It authorizes no broker mutation:

- no second H024 entry
- no live order
- no trading loop
- no scale-up
- no extra symbols
- no close
- no modify

Manual MT5 risk management remains available to the human operator, but code-level close/modify requires separately governed close automation.

## USDJPY boundary

USDJPY matters for the H024 universe.

It is not authorized by the XAUUSDm canary supervisor. USDJPY requires separate broker-symbol readiness and governance:

- model symbol `USDJPY`
- runtime symbol expected on Exness standard demo: `USDJPYm`
- broker data readiness
- H020 sizing verification
- request-shape preview
- separate one-shot demo canary decision if later approved

USDJPY must not piggyback on the XAUUSDm canary ticket, ledger, or lifecycle state.

## Review thresholds

The supervisor can recommend human review when observation thresholds are crossed.

A human-review recommendation is not a close authorization. It is an operator attention flag only.

Default thresholds:

- floating loss at or beyond 40 USD
- adverse price move from fill at or beyond 45 price units

## Current intended state

For the current HANDOFF_98 canary, the expected state is:

- monitor verdict: PASS
- lifecycle decision verdict: PASS
- observation analysis verdict: PASS
- monitor lifecycle state: open
- lifecycle decision: continue_hold
- supervisory state: continue_observe_open
- broker mutation authorized: false
- trading loop authorized: false
- edge inference authorized: false
