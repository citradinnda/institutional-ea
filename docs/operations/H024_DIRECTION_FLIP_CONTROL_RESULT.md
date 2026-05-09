# H024 Direction-Flip Negative-Control Result

Research diagnostic only.

This is not:
- demo approval
- live approval
- Phase 4 approval
- execution approval

## Diagnostic

Command:

```powershell
python .\scripts\diagnose_h024_direction_flip_real.py
Setup
Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
broker-native H4 and M1
strict complete H4/M1 bridge windows
accepted bridge-window count: 5476
frozen H024 hold=3 H4
baseline stop ATR multiple 2.0
baseline modeled costs
no parameter optimization
no 2023 exclusion
no time/session filters
Method

The diagnostic compared frozen H024 against a direction-flip negative control.

The control inverted H024 direction while preserving:

accepted bridge windows
fixed lifecycle semantics
hold=3 H4
modeled costs
H018 hard guard path

Stops were mirrored around the raw H4 entry open so the inverted trade preserved the original raw stop distance while maintaining valid directional stop geometry.

Result
Variant    Accepted    Executed    Fills    Stops    Stop rate    Ending equity USD    PnL USD    Return    Max DD    Win rate    Gross profit USD    Gross loss USD    Profit factor    Fill return Sharpe
frozen H024    5476    424    459    56    12.2004%    14093.92    4093.92    40.9392%    -6.7346%    52.2876%    15587.76    -11493.84    1.356184    0.118427
direction flip    5476    402    433    89    20.5543%    6103.11    -3896.89    -38.9689%    -40.2652%    43.8799%    6377.77    -10274.66    0.620728    -0.188633

Baseline minus direction-flip PnL:

7990.81 USD
Interpretation

The direction-flip negative control materially failed.

The inverted strategy degraded sharply:

total return changed from +40.9392% to -38.9689%
profit factor collapsed from 1.356184 to 0.620728
max drawdown worsened from -6.7346% to -40.2652%
stop rate rose from 12.2004% to 20.5543%

This reduces the concern that H024 is merely benefiting from generic lifecycle mechanics, sizing, or volatility exposure. The result supports the presence of directional information in the frozen H024 signal.

This does not prove H024 will survive the future. It only passes one anti-curve-fit negative control.

Current Status

H024 remains:

not demo-approved
not live-approved
not Phase 4-approved

Next anti-curve-fit diagnostic should be a timestamp-shuffle control or direct 2023 stop-exit market-context audit.
