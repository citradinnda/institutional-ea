# H024 Observed Broker Cost Diagnostic Result

Research only. No demo trading is approved. No live trading is approved. Phase 4 is not approved.

## Purpose

Rerun frozen H024 hold=3 using observed Exness MT5 broker cost facts from the broker symbol-spec audit.

This diagnostic does not:

- tune parameters
- exclude 2023
- add time/session filters
- alter H024 signal logic
- approve deployment

## Command

```powershell
python .\scripts\diagnose_h024_observed_broker_costs_real.py
Setup
Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
broker-native H4 and M1
strict complete H4/M1 bridge windows
accepted bridge-window count: 5476
frozen H024 hold=3 H4
no parameter optimization
no 2023 exclusion
no time/session filters
Observed MT5 Cost Facts Tested

USDJPY:

spread_price: 0.018
commission_usd_per_lot_per_fill: 0.0
stop_slippage_atr_fraction: 0.05

XAUUSD:

spread_price: 0.36
commission_usd_per_lot_per_fill: 0.0
stop_slippage_atr_fraction: 0.05
Baseline Modeled Costs vs Observed Broker Costs
Cost case    Hold H4    Accepted    Executed    Skipped    Fills    Stops    Stop rate    Ending equity USD    PnL USD    Return    Max DD    Win rate    Gross profit USD    Gross loss USD    PF    Fill return Sharpe
baseline modeled costs    3    5476    424    5052    459    56    12.2004%    14093.92    4093.92    40.9392%    -6.7346%    52.2876%    15587.76    -11493.84    1.356184    0.118427
observed broker costs    3    5476    424    5052    459    56    12.2004%    14693.82    4693.82    46.9382%    -6.3694%    52.2876%    16224.83    -11531.01    1.407061    0.131688

Delta observed minus baseline:

total_pnl_usd: +599.90
profit_factor: +0.050877
Observed Broker Cost Splits
By Symbol
Symbol    Fills    Stops    Stop rate    PnL USD    Gross profit USD    Gross loss USD    PF    Win rate
USDJPY    240    25    10.4167%    3266.73    9415.07    -6148.34    1.531319    55.4167%
XAUUSD    219    31    14.1553%    1427.09    6809.76    -5382.67    1.265127    48.8584%
By Side
Side    Fills    Stops    Stop rate    PnL USD    Gross profit USD    Gross loss USD    PF    Win rate
buy    252    32    12.6984%    2489.97    8841.39    -6351.42    1.392033    53.9683%
sell    207    24    11.5942%    2203.85    7383.44    -5179.59    1.425488    50.2415%
Chronological Halves
Half    Fills    Stops    Stop rate    PnL USD    Gross profit USD    Gross loss USD    PF    Win rate
first_half    229    33    14.4105%    2128.82    8250.64    -6121.82    1.347743    53.2751%
second_half    230    23    10.0000%    2565.00    7974.19    -5409.19    1.474193    51.3043%
Chronological Thirds
Third    Fills    Stops    Stop rate    PnL USD    Gross profit USD    Gross loss USD    PF    Win rate
third_1    153    24    15.6863%    1362.59    5573.92    -4211.32    1.323555    51.6340%
third_2    153    21    13.7255%    909.02    5060.93    -4151.90    1.218942    52.2876%
third_3    153    11    7.1895%    2422.20    5589.99    -3167.78    1.764637    52.9412%
By Calendar Year
Year    Fills    Stops    Stop rate    PnL USD    Gross profit USD    Gross loss USD    PF    Win rate
2021    16    1    6.2500%    554.81    859.73    -304.91    2.819570    56.2500%
2022    84    10    11.9048%    1529.00    3292.34    -1763.35    1.867099    57.1429%
2023    90    17    18.8889%    -622.90    2386.38    -3009.28    0.793006    46.6667%
2024    122    17    13.9344%    915.65    4275.87    -3360.22    1.272498    52.4590%
2025    120    11    9.1667%    1856.16    4430.15    -2573.98    1.721126    55.0000%
2026    27    0    0.0000%    461.10    980.37    -519.27    1.887976    40.7407%
Interpretation

H024 remains positive and above PF 1.15 under observed Exness MT5 broker cost facts.

Broker-cost reconciliation is materially improved. The observed zero commission more than offsets the wider observed spread in this diagnostic.

This does not prove future survivability.

2023 remains weak:

2023 PnL: -622.90
2023 PF: 0.793006
2023 stop rate: 18.8889%

Do not add a 2023 exclusion. Do not add time/session filters. Do not tune H024 parameters.

Deployment Boundary

This result does not approve:

demo trading
live trading
Phase 4
EA execution
dry-run/log-only deployment

Next required work remains execution-readiness work such as MT5 order behavior reconciliation, dry-run/log-only EA path, hard kill switch, execution adapter safety checks, and explicit authorization before any Phase 4 work.
