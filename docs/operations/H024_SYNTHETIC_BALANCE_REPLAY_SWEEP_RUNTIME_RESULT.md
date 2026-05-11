# H024 Synthetic Balance Replay Sweep Runtime Result

## Status

Research-only. Not demo-approved. Not live-approved. Not Phase 4-approved. No execution approval.

This result preserves a synthetic-balance replay-sweep runtime diagnostic for H024 on Exness Standard Cent symbols.

## Boundary

This is synthetic evidence only.

It does not prove real-account executable sizing because the real account balance and equity in the captured runtime rows were both 0.00 USC.

It must not be treated as:

- demo approval
- live approval
- Phase 4 approval
- execution-adapter approval
- real-balance executable evidence

## Runtime Collection

Runtime CSV:

- `reports\h024_ea_log_only_preflight.csv`

Collection result:

- Rows: 182
- Violations: 0
- Verdict: PASS

Intended-action summary:

- Total rows: 182
- Intended-action header rows: 2
- Intended-action data rows: 6
- Verdict: PASS

USDJPYc:

- headers: 1
- rows: 3
- normalized: USDJPY
- WOULD_OPEN: 0
- BLOCKED: 0
- NO_ACTION: 3

XAUUSDc:

- headers: 1
- rows: 3
- normalized: XAUUSD
- WOULD_OPEN: 1
- BLOCKED: 0
- NO_ACTION: 2

## Manual Replay Sweep Inputs

XAUUSDc H4:

- `InpH024ReplaySweepEnabled = true`
- `InpH024ReplaySweepStartShift = 227`
- `InpH024ReplaySweepEndShift = 229`
- `InpH024ReplaySweepMaxRows = 10`
- `InpH024SyntheticBalanceEnabled = true`
- `InpH024SyntheticBalance = 10000.0`

USDJPYc H4:

- `InpH024ReplaySweepEnabled = true`
- `InpH024ReplaySweepStartShift = 226`
- `InpH024ReplaySweepEndShift = 228`
- `InpH024ReplaySweepMaxRows = 10`
- `InpH024SyntheticBalanceEnabled = true`
- `InpH024SyntheticBalance = 10000.0`

## Synthetic WOULD_OPEN Row

The unique synthetic WOULD_OPEN row was:

- runtime timestamp: `2026.05.11 07:25:44`
- symbol: `XAUUSDc`
- normalized symbol: `XAUUSD`
- timeframe: `H4`
- action: `WOULD_OPEN`
- side: `short`
- closed H4 time: `2026.03.18 08:00:00`
- entry: `4930.0480000000`
- stop: `5019.1630000000`
- stop distance: `89.1150000000`
- synthetic sizing balance: `10000.00`
- risk fraction: `0.01000000`
- risk amount: `100.00`
- raw lots: `0.0112214554`
- final lots: `0.0100000000`
- real account balance: `0.00`
- real account equity: `0.00`

Reason field:

`WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution;balance_source=synthetic_research_only;synthetic_balance=10000.00;real_account_balance=0.00`

## Interpretation

This result shows that the EA can produce a log-only H024 intended-action WOULD_OPEN row under a research-only synthetic 10000 USC balance diagnostic.

It does not remove the real-runtime evidence blocker.

The remaining blocker is still:

- no executable real-runtime WOULD_OPEN row with nonzero final lots has been observed using actual account balance

