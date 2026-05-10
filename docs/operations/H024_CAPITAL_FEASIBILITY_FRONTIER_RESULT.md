# H024 Capital Feasibility Frontier Result

Status: research / pre-deployment only.

No demo approval.  
No live approval.  
No Phase 4 approval.  
No order-send path approved.  
No execution adapter approved.

## Purpose

This result preserves a pure-Python H024 executable candidate shift scan across several account balances at a fixed 1 percent risk fraction.

The goal was to characterize when H024 becomes mechanically executable under broker minimum-volume constraints.

This was broker-native H4 CSV-read-only and pure Python.

No MT5 access.  
No M1 accepted-window validation.  
No order execution.  
No execution approval.

## Command Shape

```powershell
$RiskFraction = 0.01

foreach ($BalanceUsd in @(100, 120, 250, 550, 1000, 10000)) {
  python scripts\scan_h024_executable_candidate_shifts.py `
    --balance $BalanceUsd `
    --risk-fraction $RiskFraction `
    --output-csv "reports\h024_executable_candidate_shifts_${BalanceUsd}usd_1pct.csv" `
    --max-rows 5
}

Generated reports remain local and untracked under reports/.

Observed Frontier
Balance  Risk  Executable Candidates
100      1%    0
120      1%    0
250      1%    1
550      1%    215
1000     1%    595
10000    1%    1364
Symbol Breakdown
Balance  USDJPY  XAUUSD
100      0       0
120      0       0
250      1       0
550      215     0
1000     591     4
10000    669     695
First Candidate Examples

At 250 USD / 1 percent risk:

symbol: USDJPY
side: sell
decision_time: 2021-07-17T21:00:00+00:00
entry_time: 2021-07-18T17:00:00+00:00
ea_closed_shift_from_latest_common_h4: 7697
final_signed_risk_fraction: -0.009782643658
entry_price: 110.0150000000
stop_price: 110.2840593855
stop_distance: 0.2690593855

At 1000 USD / 1 percent risk:

symbol: USDJPY
side: buy
decision_time: 2018-09-12T21:00:00+00:00
entry_time: 2018-09-13T21:00:00+00:00
ea_closed_shift_from_latest_common_h4: 8632
final_signed_risk_fraction: 0.009968071067
entry_price: 112.0220000000
stop_price: 110.9053567430
stop_distance: 1.1166432570

At 10000 USD / 1 percent risk:

symbol: XAUUSD
side: sell
decision_time: 2018-07-22T21:00:00+00:00
entry_time: 2018-07-23T21:00:00+00:00
ea_closed_shift_from_latest_common_h4: 8677
final_signed_risk_fraction: -0.008008183852
entry_price: 1224.2110000000
stop_price: 1244.2314596288
stop_distance: 20.0204596288
Interpretation

At the current 100 USD / 1 percent risk setting, H024 has no executable historical candidate shifts.

USDJPY becomes mechanically executable somewhere between 120 USD and 250 USD at 1 percent risk.

XAUUSD becomes mechanically executable somewhere between 550 USD and 1000 USD at 1 percent risk.

This supports the current diagnosis:

The latest runtime replay observed valid signal rows.
Those rows were BLOCKED by broker minimum volume.
The blocker is economic / microstructure feasibility, not a code malfunction.
Raising risk to force execution is not approved.
Higher balance feasibility is not demo or live approval.
Current Test Anchor

After adding the executable candidate scanner:

932 passed

If tests drop below 932 without intentional test removal, treat it as a regression.

Current Conclusion

H024 remains promising but not demo deployable.

At the current 100 USD / 1 percent risk setting, the system has no executable dry-run candidate path to reconcile.

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
