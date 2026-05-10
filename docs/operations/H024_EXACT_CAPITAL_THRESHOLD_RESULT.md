# H024 Exact Capital Threshold Result

Status: research / pre-deployment only.

No demo approval.  
No live approval.  
No Phase 4 approval.  
No order-send path approved.  
No execution adapter approved.

## Purpose

This result preserves the exact minimum account-balance thresholds where H024 first becomes mechanically executable at a fixed 1 percent risk fraction.

This was pure Python and broker-native H4 CSV-read-only.

No MT5 access.  
No M1 accepted-window validation.  
No order execution.  
No execution approval.

## Observed Thresholds

```text
ANY executable H024 candidate: 245 USD at 1 percent risk
USDJPY first executable:       245 USD at 1 percent risk
XAUUSD first executable:       935 USD at 1 percent risk
Boundary Checks
balance=244: total=0 USDJPY=0 XAUUSD=0
balance=245: total=1 USDJPY=1 XAUUSD=0

balance=934: total=568 USDJPY=568 XAUUSD=0
balance=935: total=569 USDJPY=568 XAUUSD=1
First USDJPY / Any Candidate
symbol: USDJPY
side: sell
decision_time: 2021-07-17T21:00:00+00:00
entry_time: 2021-07-18T17:00:00+00:00
ea_closed_shift_from_latest_common_h4: 7697
final_signed_risk_fraction: -0.009982289447
entry_price: 110.0150000000
stop_price: 110.2840593855
stop_distance: 0.2690593855
First XAUUSD Candidate
symbol: XAUUSD
side: sell
decision_time: 2023-09-25T21:00:00+00:00
entry_time: 2023-09-26T01:00:00+00:00
ea_closed_shift_from_latest_common_h4: 4184
final_signed_risk_fraction: -0.009997846715
entry_price: 1913.5900000000
stop_price: 1922.9379866787
stop_distance: 9.3479866787
Interpretation

At the current 100 USD / 1 percent risk setting, H024 is not mechanically executable under broker minimum-volume constraints.

USDJPY first becomes mechanically executable at 245 USD.

XAUUSD first becomes mechanically executable at 935 USD.

This does not recommend increasing balance or risk. It only quantifies the feasibility boundary.

This result reinforces the current diagnosis:

H024 signal logic can produce valid signal rows.
Runtime replay has already observed signal rows.
Current 100 USD / 1 percent risk sizing blocks those rows below broker minimum volume.
The blocker is economic / microstructure feasibility, not a code malfunction.
No executable dry-run request exists at the current 100 USD / 1 percent risk setting.
Current Test Anchor
932 passed

If tests drop below 932 without intentional test removal, treat it as a regression.

Current Conclusion

H024 remains promising but not demo deployable.

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
