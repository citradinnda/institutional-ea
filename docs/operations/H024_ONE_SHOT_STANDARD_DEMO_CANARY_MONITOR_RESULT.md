# H024 One-Shot Standard-Demo Canary Monitor Result

This document records the read-only monitor packet for the first H024 standard-demo broker-side canary.

## Scope

The monitor is observation-only. It may read MT5 account, position, pending-order, and deal-history state. It must not send, check, close, modify, loop, scale, add symbols, or automate the GUI.

## Expected Canary

- Server: `Exness-MT5Trial6`
- Currency: `USD`
- Symbol: `XAUUSDm`
- Side: sell / MT5 type `1`
- Volume: `0.01`
- Magic: `240024`
- Order/ticket/identifier: `4413054432`
- Entry deal: `3788869526`
- Fill price: `4728.4490000000005`
- Stop loss: `4817.394`
- Comment prefix: `H024_ONE_SHOT_DE`

## Output

Runtime monitor output is written locally to:

`reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl`

Do not commit `reports/`.

## Accepted Lifecycle States

The monitor may pass in either of these states:

1. `open`: exactly one expected H024 canary position is open and no extra H024 pending orders or second entry deals exist.
2. `closed_explained`: no H024 canary position is open, but matching close/deal history explains the closure and no second entry exists.

Any other state is a failure until investigated.