# H024 Executable Candidate Shift Scan Result

Status: research / pre-deployment only.

No demo approval.  
No live approval.  
No Phase 4 approval.  
No order-send path approved.  
No execution adapter approved.

## Purpose

This result preserves the first pure-Python H024 historical H4 scan for executable candidate replay shifts at the current account/risk assumptions.

The goal was to answer:

Can any historical H024 H4 decision row survive H024 signal logic plus H020 sizing into an executable candidate at 100 USD balance and 1 percent risk?

This was H4 CSV-read-only and pure Python.

No MT5 access.  
No M1 accepted-window validation.  
No order execution.  
No execution approval.

## Command

```powershell
python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 20
Observed Result
H024 executable candidate shift scan
========================================================================
Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.

balance: 100.00
risk_fraction: 0.010000
executable_candidate_rows: 0
wrote: reports\h024_executable_candidate_shifts_100usd_1pct.csv

Verdict: PASS
Scan completed; no executable candidate shifts found at these settings.
Interpretation

At 100 USD balance and 1 percent risk, no historical H024 H4 candidate survived sizing into an executable candidate.

This reinforces the minimum-volume feasibility blocker:

The latest runtime replay produced signal rows.
Those rows were BLOCKED because computed volume was below broker minimum.
The feasibility summary showed USDJPY is close but below minimum volume.
XAUUSD is far below minimum volume.
The scanner found no other historical H4 replay shift that would produce an executable candidate at the same account/risk settings.

This is not a code malfunction. It is an economic / microstructure feasibility constraint.

This result does not recommend raising risk.

Test Anchor

After adding the scanner and tests:

Focused scanner tests: 3 passed
Full suite: 932 passed in 20.70s

Current full-test anchor is now:

932 passed

If tests drop below 932 without intentional test removal, treat it as a regression.

Current Conclusion

H024 remains promising but not demo deployable.

There is still no runtime CSV row that reconstructs into an executable dry-run request at the current 100 USD / 1 percent risk settings.

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
