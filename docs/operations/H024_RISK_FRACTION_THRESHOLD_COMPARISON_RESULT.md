# H024 Risk Fraction Capital Threshold Comparison

Status: research-only / pre-deployment.

H024 is not demo-approved, not live-approved, and not Phase 4-approved.

No order-send path, execution adapter, OrderCheck, CTrade, MqlTradeRequest, demo trading, or live trading is approved.

## Purpose

Compare H024 executable-candidate capital thresholds across fixed risk fractions.

This result quantifies mechanical broker minimum-volume feasibility only.

It does not recommend increasing risk, increasing account balance, or proceeding to execution.

## Method

Command family:

```powershell
python scripts\scan_h024_capital_thresholds.py --risk-fraction <risk_fraction>

Scanner scope:

Pure Python
Broker-native H4 CSV read-only
No MT5 access
No order execution
Exact threshold scan with boundary checks
Results
Risk fraction    ANY threshold    USDJPY threshold    XAUUSD threshold
0.50%    490 USD    490 USD    1,870 USD
0.75%    327 USD    327 USD    1,247 USD
1.00%    245 USD    245 USD    935 USD
1.50%    164 USD    164 USD    624 USD
2.00%    123 USD    123 USD    468 USD
Interpretation

At the current intended setting:

Balance: 100 USD
Risk fraction: 1%

H024 remains mechanically non-executable.

Even at 2% risk, the first ANY / USDJPY executable threshold is still 123 USD, so a 100 USD account remains below threshold.

Approximate implied minimum risk fractions at 100 USD are:

Scope    Approximate risk needed at 100 USD
ANY / USDJPY    2.45%
XAUUSD    9.35%

These implied risk fractions are feasibility measurements only.

They do not approve raising risk.

Deployment Boundary

This comparison does not change deployment status.

H024 remains:

Research-only
Not demo-approved
Not live-approved
Not Phase 4-approved
Not approved for execution adapter work

The current blocker remains economic / broker minimum-volume feasibility, not a known strategy-code malfunction.
