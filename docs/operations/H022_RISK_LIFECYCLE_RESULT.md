# H022 Risk/Lifecycle Variant Diagnostic Result

## Status

Research diagnostic only.

No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.

## Command

```powershell
python .\scripts\diagnose_h022_risk_lifecycle_variants_real.py
Data
Exness broker-native USDJPY/XAUUSD exports only.
Broker-native H4/M1 strict bridge windows only.
Accepted bridge-window count: 5476.
H020 bridge shim used as signal source.
H018 hard guards preserved.
Summary Results
Variant    Hold    Scale    Min stop/spread    Fills    Stops    Stop rate    Ending equity    PnL    Return    Max DD    PF
scale_0_50_hold_1    1    0.50    none    4159    482    11.5893%    2910.50    -7089.50    -70.8950%    -70.9981%    0.759438
scale_0_50_hold_2    2    0.50    none    1835    345    18.8011%    5865.42    -4134.58    -41.3458%    -41.2643%    0.821041
scale_0_25_hold_1    1    0.25    none    3711    459    12.3686%    5595.52    -4404.48    -44.0448%    -44.1424%    0.753983
scale_0_25_hold_2    2    0.25    none    1603    322    20.0873%    7600.73    -2399.27    -23.9927%    -23.9585%    0.799195
scale_0_50_min_stop_20x_hold_1    1    0.50    20x    3933    294    7.4752%    3734.76    -6265.24    -62.6524%    -62.8015%    0.774444
scale_0_50_min_stop_20x_hold_2    2    0.50    20x    1735    262    15.1009%    6434.48    -3565.52    -35.6552%    -35.8728%    0.832027
scale_0_25_min_stop_50x_hold_1    1    0.25    50x    2486    90    3.6203%    8084.10    -1915.90    -19.1590%    -19.3255%    0.809423
scale_0_25_min_stop_50x_hold_2    2    0.25    50x    1117    109    9.7583%    9117.63    -882.37    -8.8237%    -10.8233%    0.876661
Best Variant
Best by loss reduction:

scale_0_25_min_stop_50x_hold_2
total PnL: -882.37
return: -8.8237%
max drawdown: -10.8233%
profit factor: 0.876661
This was a meaningful risk reduction versus H020/H021, but it still had negative expectancy.

Important split facts for best variant:

first half PnL: -227.27, PF 0.936770
second half PnL: -655.10, PF 0.815966
third_1 PnL: -3.03, PF 0.998667
third_2 PnL: -341.75, PF 0.862801
third_3 PnL: -537.60, PF 0.775188
Verdict
The first H022 risk/lifecycle diagnostic failed.

Reasons:

No variant reached PF >= 1.15.
No variant produced positive full-period return.
Best variant was still negative after modeled costs.
Temporal splits were weak and deteriorated after the first third.
Risk scaling reduced damage but did not create positive expectancy.
Stop-distance filtering reduced stop rate but did not rescue expectancy.
Interpretation
H022 confirms that risk/lifecycle shaping can reduce ruin severity, but the current entry/lifecycle stack still does not show validated positive expectancy.

This is not deployable evidence.

No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.
