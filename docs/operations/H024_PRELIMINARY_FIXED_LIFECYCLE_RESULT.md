# H024 Preliminary Fixed Lifecycle Result

## Status

Preliminary real-data diagnostic result.

H024 is not yet validated.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 is not approved.

## Diagnostic

Command:

```powershell
python .\scripts\diagnose_h024_fixed_lifecycle_real.py

Setup:

Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
broker-native H4 and M1
strict complete H4/M1 bridge windows
accepted bridge-window count: 5476
H024 pullback-continuation bridge shim
H018 hard guard semantics preserved through fixed-lifecycle event path
modeled costs preserved
Main Summary
Hold    Accepted    Executed    Skipped    Fills    Stops    Stop rate    Ending equity    PnL    Return    Max DD    Win rate    Profit factor
1 H4    5476    861    4615    931    21    2.2556%    $8450.96    -$1549.04    -15.4904%    -22.5043%    45.4350%    0.849209
2 H4    5476    559    4917    604    45    7.4503%    $10925.34    $925.34    9.2534%    -14.0533%    50.8278%    1.076884
3 H4    5476    424    5052    459    56    12.2004%    $14093.92    $4093.92    40.9392%    -6.7346%    52.2876%    1.356184
4 H4    5476    285    5191    307    54    17.5896%    $11236.27    $1236.27    12.3627%    -6.8030%    49.5114%    1.151364
Initial Interpretation

H024 hold=3 H4 is the first variant in this project to pass the headline full-period criteria:

positive full-period return after modeled costs
profit factor above 1.15
no catastrophic drawdown
both symbols positive
both sides positive
both chronological halves positive
all chronological thirds positive

This is promising research evidence, not deployment evidence.

H024 Hold=3 Split Facts

By symbol:

Symbol    Fills    Stops    Stop rate    PnL    Profit factor    Win rate
USDJPY    240    25    10.4167%    $2832.92    1.460747    55.4167%
XAUUSD    219    31    14.1553%    $1261.01    1.235909    48.8584%

By side:

Side    Fills    Stops    Stop rate    PnL    Profit factor    Win rate
buy    252    32    12.6984%    $2125.89    1.336645    53.9683%
sell    207    24    11.5942%    $1968.04    1.380010    50.2415%

Chronological halves:

Split    Fills    Stops    Stop rate    PnL    Profit factor    Win rate
first_half    229    33    14.4105%    $1843.70    1.299481    53.2751%
second_half    230    23    10.0000%    $2250.22    1.421586    51.3043%

Chronological thirds:

Split    Fills    Stops    Stop rate    PnL    Profit factor    Win rate
third_1    153    24    15.6863%    $1218.22    1.287591    51.6340%
third_2    153    21    13.7255%    $716.50    1.173857    52.2876%
third_3    153    11    7.1895%    $2159.20    1.688370    52.9412%

By calendar year:

Year    Fills    Stops    Stop rate    PnL    Profit factor    Win rate
2021    16    1    6.2500%    $534.92    2.708700    56.2500%
2022    84    10    11.9048%    $1435.99    1.800603    57.1429%
2023    90    17    18.8889%    -$708.20    0.764187    46.6667%
2024    122    17    13.9344%    $758.18    1.228199    52.4590%
2025    120    11    9.1667%    $1661.50    1.654749    55.0000%
2026    27    0    0.0000%    $411.53    1.785618    40.7407%
Risk Notes

The 2023 calendar-year split failed materially:

PnL: -$708.20
PF: 0.764187
stop rate: 18.8889%

This means H024 is not yet validated. The result may be regime-dependent.

The 4 H4 hold barely clears the PF threshold at 1.151364 and is less attractive than 3 H4.

The 2 H4 hold is positive but below the PF threshold.

The 1 H4 hold fails.

Verdict

H024 hold=3 H4 is a promising candidate for further robustness testing.

It is not yet promotable.
No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.

Next Required Work

Run a targeted robustness diagnostic for H024 hold=3 H4 only.

The robustness diagnostic should check:

modest cost stress
nearby stop ATR multiples
chronological stability under the same pre-registered split reporting
whether 2023 failure is isolated or structurally explained

Do not run broad parameter sweeps.
Do not mine H021 time/session buckets.
Do not deploy.
