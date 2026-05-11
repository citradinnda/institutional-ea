# H024 One-Shot Standard-Demo Canary Execution Path

Status: implemented, not invoked

This implementation adds an execution-capable one-shot standard-demo canary path.

It is hard-locked to:

- allowed demo server: `Exness-MT5Trial6`
- account currency: USD
- symbol: `XAUUSDm`
- side: sell
- max lot cap: `0.01`
- stop-loss distance: `89.027`
- one canary order only
- idempotency ledger required
- exact manual acknowledgement required for `--send`
- no live order allowance

The implementation is not automatically invoked by tests or by import.

The dry-run command builds the request only and does not call `order_check` or `order_send`:

```powershell
python scripts\run_h024_one_shot_demo_canary.py

The send path is intentionally explicit and requires the exact acknowledgement string:

python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER

Before using the send path, verify that MT5 is logged into the intended standard demo account and that XAUUSDm is visible in Market Watch.