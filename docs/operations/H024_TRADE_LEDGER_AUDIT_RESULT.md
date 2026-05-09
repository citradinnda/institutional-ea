# H024 Trade Ledger Audit Result

Research diagnostic only.

This is not:
- demo approval
- live approval
- Phase 4 approval
- execution approval

## Diagnostic

Command:

```powershell
python .\scripts\diagnose_h024_trade_ledger_real.py

Output ledger:

reports\h024_hold3_trade_ledger.csv

The CSV is a derived local audit artifact and should not be committed.

Setup
Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
broker-native H4 and M1
strict complete H4/M1 bridge windows
accepted bridge-window count: 5476
H024 hold=3 H4
baseline stop ATR multiple 2.0
baseline modeled costs
no H021 time/session bucket mining
no 2023 exclusion
no parameter optimization
Ledger Summary
Metric    Value
Ledger rows    459
Lifecycle fills    459
Net PnL USD    4093.92
By Symbol
Symbol    Fills    Stops    Stop rate    PnL USD    Profit factor    Win rate
USDJPY    240    25    10.4167%    2832.92    1.460747    55.4167%
XAUUSD    219    31    14.1553%    1261.01    1.235909    48.8584%
By Side
Side    Fills    Stops    Stop rate    PnL USD    Profit factor    Win rate
buy    252    32    12.6984%    2125.89    1.336645    53.9683%
sell    207    24    11.5942%    1968.04    1.380010    50.2415%
By Exit Year
Year    Fills    Stops    Stop rate    PnL USD    Profit factor    Win rate
2021    16    1    6.2500%    534.92    2.708700    56.2500%
2022    84    10    11.9048%    1435.99    1.800603    57.1429%
2023    90    17    18.8889%    -708.20    0.764187    46.6667%
2024    122    17    13.9344%    758.18    1.228199    52.4590%
2025    120    11    9.1667%    1661.50    1.654749    55.0000%
2026    27    0    0.0000%    411.53    1.785618    40.7407%
2023 Audit Slice
Symbol    Side    Exit reason    Fills    PnL USD    Avg lots    Avg raw stop distance
USDJPY    buy    signal_flip    22    764.566249    0.169545    1.004200
USDJPY    buy    stop    6    -690.656496    0.141667    1.135589
USDJPY    sell    signal_flip    14    92.420862    0.164286    0.958989
USDJPY    sell    stop    4    -464.535033    0.165000    1.021587
XAUUSD    buy    signal_flip    16    -83.646000    0.064375    15.919235
XAUUSD    buy    stop    5    -483.950024    0.050000    19.560749
XAUUSD    sell    signal_flip    21    344.960000    0.061905    17.171272
XAUUSD    sell    stop    2    -187.361082    0.050000    17.367722
Interpretation

The ledger confirms the prior H024 hold=3 result at the fill level.

H024 remains balanced enough across symbol and side to continue audit work. USDJPY is stronger than XAUUSD, but XAUUSD remains positive. Buy and sell sides are both positive with comparable profit factors.

The persistent 2023 weakness remains real and must not be hidden with a year, time, or session exclusion. The 2023 slice suggests the weakness is concentrated in stop exits rather than all 2023 signal-flip exits. In 2023, signal-flip exits were positive in aggregate, while stop exits were materially negative.

This result supports continuing audit and execution-realism work. It does not support deployment.

Next Research Actions

Recommended next actions:

Inspect the largest losses and largest winners directly from the CSV ledger.
Drill into 2023 stop exits by timestamp, symbol, side, raw stop distance, lot size, and local market context.
Add interval-equity and actual gross-leverage columns to the ledger if needed for lot-size audit.
Reconcile symbol contract assumptions against Exness MT5.
Reconcile modeled spread, commission, and stop slippage assumptions against observed MT5 conditions.

Do not:

optimize H024 parameters
exclude 2023
add time/session filters
approve demo trading
approve live trading
start Phase 4
