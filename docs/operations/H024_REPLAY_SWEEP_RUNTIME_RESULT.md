# H024 Replay Sweep Runtime Result

Research only. No demo/live/Phase 4 approval.

## Summary

The H024 log-only replay sweep mode was manually validated in MT5 on the Exness Standard Cent symbols:

- `USDJPYc`
- `XAUUSDc`

The replay sweep emitted the expected marker events, produced intended-action runtime rows, and the verifier was updated to allow the replay-sweep marker events.

This remains log-only evidence only. It is not demo approval, live approval, Phase 4 approval, or execution approval.

## Runtime Collection

Runtime CSV:

- `reports\h024_ea_log_only_preflight.csv`

Collection result after verifier fix:

- Rows: 419
- Violations: 0
- Verdict: PASS

Intended-action summary:

- Total rows: 419
- Intended-action header rows: 4
- Intended-action data rows: 38

`USDJPYc`:

- headers: 2
- rows: 14
- normalized: USDJPY
- WOULD_OPEN: 0
- BLOCKED: 0
- NO_ACTION: 14

`XAUUSDc`:

- headers: 2
- rows: 24
- normalized: XAUUSD
- WOULD_OPEN: 0
- BLOCKED: 1
- NO_ACTION: 23

Summary verdict: PASS

## Replay Sweep Markers

Observed marker rows for `USDJPYc`:

- H024_REPLAY_SWEEP start_shift=226;end_shift=228;max_rows=10
- H024_REPLAY_SWEEP_SHIFT closed_shift=226
- H024_REPLAY_SWEEP_SHIFT closed_shift=227
- H024_REPLAY_SWEEP_SHIFT closed_shift=228
- H024_REPLAY_SWEEP_DONE rows_written=3

Observed marker rows for `XAUUSDc`:

- H024_REPLAY_SWEEP start_shift=227;end_shift=229;max_rows=10
- H024_REPLAY_SWEEP_SHIFT closed_shift=227
- H024_REPLAY_SWEEP_SHIFT closed_shift=228
- H024_REPLAY_SWEEP_SHIFT closed_shift=229
- H024_REPLAY_SWEEP_DONE rows_written=3

## Runtime Signal Evidence

The replay sweep observed a cent-symbol H024 signal path on `XAUUSDc`.

Unique blocked signal row:

- symbol: XAUUSDc
- action: BLOCKED
- side: short
- closed_h4_time: 2026.03.18 08:00:00
- entry: 4930.0480000000
- stop: 5019.1630000000
- raw_lots: 0.0000000000
- final_lots: 0.0000000000
- reason: BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

Interpretation:

- The log-only replay sweep signal path works on `XAUUSDc`.
- The signal was correctly converted to `BLOCKED`, not `WOULD_OPEN`.
- Entry, stop, side, and closed H4 time were preserved.
- Final executable lots remained zero.
- This row must not be converted into a dry-run request or execution request.

## Verifier Fix

Initial collection failed because the verifier did not yet allow replay-sweep marker events:

- H024_REPLAY_SWEEP
- H024_REPLAY_SWEEP_SHIFT
- H024_REPLAY_SWEEP_DONE

The verifier allowlist was updated in:

- `scripts\verify_h024_ea_preflight_log.py`

Commit:

- `ff9f500 Allow H024 replay sweep runtime markers`

Focused verification after the fix:

- 31 passed in 2.56s

Full test suite:

- 958 passed in 38.98s

## Current Deployment Verdict

H024 remains:

- research-only
- not demo-approved
- not live-approved
- not Phase 4-approved
- not execution-approved

The current remaining blocker is unchanged:

- No executable real-runtime `WOULD_OPEN` row with nonzero final lots has been observed.

The observed real runtime balance remains effectively unsuitable for executable evidence because prior runtime evidence showed the cent account balance was `0.00 USC`.
