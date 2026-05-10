# H024 Minimum-Volume Feasibility Result

Status: research / pre-deployment only.

No demo approval.  
No live approval.  
No Phase 4 approval.  
No order-send path approved.  
No execution adapter approved.

## Purpose

This result preserves the first pure-Python H024 minimum-volume feasibility check against the runtime BLOCKED sizing diagnostics replay.

The goal was to quantify whether the observed H024 blocked signal rows could reach broker minimum volume under the current account/risk assumptions.

This was CSV-read-only and pure Python.

No MT5 access.  
No order execution.  
No risk increase recommendation.

## Source Runtime CSV

Local untracked report:

```text
reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv

This report remains intentionally untracked.

Command
python scripts\summarize_h024_min_volume_feasibility.py `
  --csv reports\h024_ea_log_only_replay_blocked_sizing_diagnostics.csv `
  --balance 100 `
  --risk-fraction 0.01
Observed Result
H024 minimum-volume feasibility summary
========================================================================
Research only. No demo/live/Phase 4 approval.
Pure Python. No MT5 access. No order execution.

USDJPY | BLOCKED | BELOW_MIN_VOLUME | observations=12 raw_lots=0.0083395062 min_volume=0.0100000000
  balance: 100.00
  risk_fraction: 0.010000
  current_risk_usd: 1.000000
  implied_loss_per_1_lot_usd: 119.911177
  minimum_risk_usd_for_min_volume: 1.199112
  minimum_balance_at_same_risk_fraction: 119.91
  minimum_risk_fraction_at_same_balance: 0.011991

XAUUSD | BLOCKED | BELOW_MIN_VOLUME | observations=13 raw_lots=0.0018247230 min_volume=0.0100000000
  balance: 100.00
  risk_fraction: 0.010000
  current_risk_usd: 1.000000
  implied_loss_per_1_lot_usd: 548.028386
  minimum_risk_usd_for_min_volume: 5.480284
  minimum_balance_at_same_risk_fraction: 548.03
  minimum_risk_fraction_at_same_balance: 0.054803

Verdict: PASS
Feasibility quantified only; no risk increase or execution approval implied.
Interpretation

At 100 USD balance and 1 percent risk:

USDJPY is below broker minimum volume but close.
XAUUSD is far below broker minimum volume.
The observed blocker is economic / microstructure feasibility, not a code malfunction.
The dry-run reconciler should still emit zero execution requests from these BLOCKED rows.
Raising risk to force execution is not approved by this result.
Test Anchor

After adding the feasibility script and tests:

Focused feasibility tests: 4 passed
Full suite: 929 passed in 16.30s

Current full-test anchor is now:

929 passed

If tests drop below 929 without intentional test removal, treat it as a regression.

Current Conclusion

H024 remains promising but not demo deployable.

The next valid gate is still to reconstruct an actual executable dry-run request from runtime CSV safely, without changing execution risk just to force a trade.

Do not proceed to:

OrderSend
OrderSendAsync
OrderCheck
CTrade
MqlTradeRequest
Execution adapter
Demo trading
Live trading
Phase 4
Chart automation
