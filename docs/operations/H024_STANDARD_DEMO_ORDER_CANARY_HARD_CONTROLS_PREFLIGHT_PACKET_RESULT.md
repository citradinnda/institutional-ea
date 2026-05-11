# H024 Standard Demo-Order Canary Hard-Controls Preflight Packet Result

Status: PASS

This artifact is review-only and requests separate human review for a possible later tightly controlled demo-order canary.

It requires:

- allowed demo server lock: `Exness-MT5Trial6`
- account currency lock: USD
- standard demo context only
- runtime symbol lock: `XAUUSDm`
- kill-switch allow-state
- idempotency ledger
- max-lot cap
- single-canary-order limit
- post-order audit if later approved
- final pre-dispatch audit if later approved
- live order remains forbidden

It does not approve a demo-order canary. It does not approve demo order placement. It does not construct an actual broker request. It does not construct an actual MT5 request. It does not construct an order payload. It does not dispatch. It does not mutate terminal or broker state. It does not approve execution.

Output artifact:

- `reports/h024_standard_demo_demo_order_canary_hard_controls_preflight_packet.jsonl`

Decision:

- `REQUEST_HUMAN_DEMO_ORDER_CANARY_APPROVAL_WITH_HARD_CONTROLS_NO_ORDER_PLACEMENT`

Next required gate:

- a separate explicit human demo-order canary approval artifact