# H024 USDJPY Broker-Readiness Packet

## Purpose

This packet is the first USDJPY-specific broker-readiness layer for H024.

It is read-only. It does not place an order, does not run `order_check`, does not run `order_send`, does not close or modify anything, and does not authorize a trading loop.

## Boundary

The existing H024 canary is XAUUSDm only. It does not authorize USDJPY trading.

USDJPY must remain separate from the XAUUSDm canary stack:

- Model symbol: `USDJPY`
- Runtime symbol: `USDJPYm`
- Strategy: `H024`
- Magic: `240024`
- Required server: `Exness-MT5Trial6`
- Required account currency: `USD`

## Read-Only Checks

The packet verifies:

1. MT5 initializes.
2. Account server is `Exness-MT5Trial6`.
3. Account currency is `USD`.
4. Runtime symbol `USDJPYm` is available.
5. Symbol properties are sane:
   - point
   - tick size
   - contract size
   - volume minimum
   - volume step
   - volume maximum
   - visible/trade status
6. Tick state is sane:
   - bid and ask are positive
   - ask is not below bid
   - spread does not exceed the configured sanity limit
7. Broker-native H4 and M1 data are available.
8. H020 sizing feasibility is plausible for a future 0.01-lot governed canary.
9. There are no existing H024 USDJPY positions.
10. There are no existing H024 USDJPY pending orders.
11. Any future USDJPY request must be separately governed.

## Explicit Non-Authorization

The generated record must keep all of these false:

- `broker_mutation_authorized`
- `order_check_authorized`
- `order_send_authorized`
- `usd_jpy_order_authorized`
- `trading_loop_authorized`

The packet also records:

- `requires_separate_canary_governance: true`

## Commands

Build the packet:

```powershell
python scripts\build_h024_usdjpy_broker_readiness_jsonl.py

Verify the packet:

python scripts\verify_h024_usdjpy_broker_readiness_jsonl.py reports\h024_usdjpy_broker_readiness.jsonl --require-pass

Focused tests:

python -m pytest -q tests\test_h024_usdjpy_broker_readiness.py
Runtime Artifact

The runtime JSONL output is local only:

reports\h024_usdjpy_broker_readiness.jsonl

Do not commit reports/.