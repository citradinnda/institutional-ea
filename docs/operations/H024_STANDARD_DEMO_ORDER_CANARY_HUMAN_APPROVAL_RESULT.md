# H024 Standard Demo-Order Canary Human Approval Result

Status: PASS

This artifact approves exactly one later demo-order canary under hard controls.

It still does not construct an actual broker request. It does not construct an actual MT5 request. It does not construct an order payload. It does not dispatch. It does not mutate terminal or broker state. It does not approve live order placement. It does not approve execution.

Output artifact:

- `reports/h024_standard_demo_demo_order_canary_human_approval.jsonl`

Decision:

- `APPROVE_SINGLE_DEMO_ORDER_CANARY_UNDER_HARD_CONTROLS_NO_DISPATCH`

Approved controls:

- allowed demo server lock: `Exness-MT5Trial6`
- account currency lock: USD
- account context lock: standard demo only
- runtime symbol lock: `XAUUSDm`
- max lot cap: `0.01`
- single canary order limit: 1
- kill-switch allow-state required
- idempotency ledger required
- final pre-dispatch audit required
- post-order audit required if later approved
- live order forbidden

Next allowed artifact:

- `h024_final_pre_dispatch_audit_packet_v1`