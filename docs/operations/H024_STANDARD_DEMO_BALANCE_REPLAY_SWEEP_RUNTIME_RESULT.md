# H024 Standard Demo Balance Replay Sweep Runtime Result

## Status

Research-only. Log-only. Not live-approved. Not Phase 4-approved. No execution approval.

This document preserves a real demo-account-balance replay-sweep runtime result for H024 on Exness standard demo symbols.

## Boundary

This is stronger than synthetic-balance evidence because the intended-action sizing used the actual demo account balance reported by MT5.

It is still not:

- live approval
- Phase 4 approval
- execution-adapter approval
- permission to add `OrderSend`, `OrderCheck`, `CTrade`, or trade request objects
- permission to place demo or live orders

## Runtime Collection

Runtime CSV:

- `reports\h024_ea_log_only_preflight.csv`

Collection result:

- Rows: 229
- Violations: 0
- Verdict: PASS

Account context observed in runtime rows:

- broker/company: `Exness Technologies Ltd`
- server: `Exness-MT5Trial6`
- account currency: `USD`
- account balance: `10000.00`
- account equity: `10000.00`
- account leverage: `2000`

Intended-action summary:

- Total rows: 229
- Intended-action header rows: 2
- Intended-action data rows: 6
- Verdict: PASS

USDJPYm:

- headers: 1
- rows: 3
- normalized: USDJPY
- WOULD_OPEN: 0
- BLOCKED: 0
- NO_ACTION: 3

XAUUSDm:

- headers: 1
- rows: 3
- normalized: XAUUSD
- WOULD_OPEN: 1
- BLOCKED: 0
- NO_ACTION: 2

## Manual Replay Sweep Inputs

XAUUSDm H4:

- `InpH024ReplaySweepEnabled = true`
- `InpH024ReplaySweepStartShift = 227`
- `InpH024ReplaySweepEndShift = 229`
- `InpH024ReplaySweepMaxRows = 10`
- `InpH024SyntheticBalanceEnabled = false`
- `InpH024SyntheticBalance = 0.0`

USDJPYm H4:

- `InpH024ReplaySweepEnabled = true`
- `InpH024ReplaySweepStartShift = 226`
- `InpH024ReplaySweepEndShift = 228`
- `InpH024ReplaySweepMaxRows = 10`
- `InpH024SyntheticBalanceEnabled = false`
- `InpH024SyntheticBalance = 0.0`

## Real Demo-Balance WOULD_OPEN Row

The unique real demo-balance WOULD_OPEN row was:

- runtime timestamp: `2026.05.11 07:45:49`
- symbol: `XAUUSDm`
- normalized symbol: `XAUUSD`
- timeframe: `H4`
- action: `WOULD_OPEN`
- side: `short`
- closed H4 time: `2026.03.18 08:00:00`
- entry: `4930.0410000000`
- stop: `5019.0680000000`
- stop distance: `89.0270000000`
- tick size: `0.0010000000`
- tick value USD per lot: `0.1000000000`
- account balance USD: `10000.00`
- risk fraction: `0.01000000`
- risk USD: `100.00`
- raw lots: `0.0112325474`
- final lots: `0.0100000000`
- min volume: `0.0100000000`
- max volume: `200.0000000000`
- volume step: `0.0100000000`
- volume digits: `2`

Reason field:

`WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution`

## Interpretation

This result shows that the H024 log-only EA can produce an executable intended-action WOULD_OPEN row using an actual 10000.00 USD Exness standard demo account balance.

This removes the specific prior evidence gap of only having synthetic or zero-balance BLOCKED signal evidence for this replay window.

It does not approve live trading, Phase 4, or order execution.

## Next Safe Follow-Up

The next safe engineering step is to preserve this result and then decide whether to:

- finish the verifier-awareness patch for synthetic reason markers, or
- add a standard-demo runtime result summary/check path if repeated standard demo validation is expected.

Do not add execution code.
