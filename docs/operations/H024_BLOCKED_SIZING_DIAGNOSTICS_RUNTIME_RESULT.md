# H024 Blocked Sizing Diagnostics Runtime Result

Research only. No demo/live/Phase 4 approval.

## Summary

This result preserves the post-bf5f420 runtime replay gate proving that H024 BLOCKED signal rows now preserve sizing diagnostics while remaining non-executable.

Runtime CSV:

`reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv`

This local report is intentionally not committed.

## Runtime Preflight Verification

Command:

```powershell
python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

Observed:

Rows: 156
Violations: 0
Verdict: PASS
Intended-Action Runtime Summary

Command:

python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

Observed:

Total rows: 156
Intended-action header rows: 2
Intended-action data rows: 25

USDJPYm:
  rows: 12
  normalized: USDJPY
  WOULD_OPEN: 0
  BLOCKED: 12
  NO_ACTION: 0

XAUUSDm:
  rows: 13
  normalized: XAUUSD
  WOULD_OPEN: 0
  BLOCKED: 13
  NO_ACTION: 0

Verdict: PASS
Blocked Sizing Diagnostics Check

Observed:

BLOCKED rows checked: 25

USDJPYm USDJPY | BLOCKED | entry=155.821 stop=158.163 dist=2.342 raw_lots=0.0083395062 lots=0.0 min_volume=0.01 | BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short;closed_h4_time=2026.05.06 04:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

XAUUSDm XAUUSD | BLOCKED | entry=4593.801 stop=4525.492 dist=68.309 raw_lots=0.001824723 lots=0.0 min_volume=0.01 | BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=long;closed_h4_time=2026.05.05 20:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

Verdict: PASS

Interpretation:

Signal rows were observed.
Runtime entry/stop derivation worked.
Stop distance was positive.
Raw lots were positive.
Raw lots were below broker minimum volume.
Final executable lots remained 0.
Rows correctly remained BLOCKED.
Dry-Run Request Reconciliation

Command:

python scripts\reconcile_h024_runtime_dry_run_requests.py `
  reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv `
  --require-request `
  --output-jsonl reports\h024_ea_log_only_replay_blocked_sizing_diagnostics_dry_run_requests.jsonl

Observed:

Rows: 156
Intended-action rows: 25
WOULD_OPEN rows: 0
Dry-run requests: 0
Skipped non-request rows: 25

Violations:
- missing required dry-run execution request

Verdict: FAIL

Interpretation:

This FAIL is the correct safety behavior under --require-request.

The replayed signal rows are not executable because they are below broker minimum volume. Therefore the dry-run reconciler must not emit execution requests.

Safety Boundary

This result does not approve:

demo trading
live trading
Phase 4 execution
OrderSend
OrderCheck
CTrade
MqlTradeRequest
execution adapter work
chart attach automation
GUI automation

H024 remains research / pre-deployment only.
