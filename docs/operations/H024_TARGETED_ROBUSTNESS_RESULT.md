# H024 Targeted Robustness Result

## Status

H024 hold=3 H4 survived the first targeted robustness diagnostic.

H024 is still not fully validated.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 is not approved.

## Diagnostic

Command:

```powershell
python .\scripts\diagnose_h024_robustness_real.py

Setup:

Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
broker-native H4 and M1
strict complete H4/M1 bridge windows
accepted bridge-window count: 5476
H024 pullback-continuation bridge shim
fixed lifecycle hold: 3 H4 only
targeted stop ATR multiples: 1.5, 2.0, 2.5
targeted cost multipliers: 1.0x, 1.25x, 1.5x
H018 hard guard semantics preserved through fixed-lifecycle event path
no H021 time/session bucket mining
no broad parameter sweep
Robustness Summary
Scenario    Stop ATR    Cost multiplier    Fills    Stops    Stop rate    Return    Max DD    PF    Headline pass
stop_atr_1.50_cost_1.00x    1.50    1.00    466    100    21.4592%    57.5337%    -9.7164%    1.328226    yes
stop_atr_1.50_cost_1.25x    1.50    1.25    466    100    21.4592%    50.3372%    -10.0436%    1.287259    yes
stop_atr_1.50_cost_1.50x    1.50    1.50    466    100    21.4592%    43.5683%    -11.3247%    1.251787    yes
stop_atr_2.00_cost_1.00x    2.00    1.00    459    56    12.2004%    40.9392%    -6.7346%    1.356184    yes
stop_atr_2.00_cost_1.25x    2.00    1.25    459    56    12.2004%    36.6204%    -7.1521%    1.316004    yes
stop_atr_2.00_cost_1.50x    2.00    1.50    459    56    12.2004%    31.1085%    -7.8798%    1.266900    yes
stop_atr_2.50_cost_1.00x    2.50    1.00    456    33    7.2368%    31.8154%    -6.4629%    1.365488    yes
stop_atr_2.50_cost_1.25x    2.50    1.25    456    33    7.2368%    28.5103%    -6.8567%    1.324031    yes
stop_atr_2.50_cost_1.50x    2.50    1.50    456    33    7.2368%    25.0625%    -7.3633%    1.282177    yes
Interpretation

H024 hold=3 H4 is not merely surviving the baseline cost model.

All tested scenarios remained positive and retained PF above 1.15 even under 1.5x modeled cost stress.

The result is materially stronger than the preliminary baseline alone.

Persistent Weakness

The 2023 calendar-year split remains the main concern.

Across robustness scenarios, 2023 remained negative with PF materially below 1.0.

Examples:

stop_atr_2.00_cost_1.00x: 2023 PnL -$708.20, PF 0.764187
stop_atr_2.00_cost_1.50x: 2023 PnL -$914.77, PF 0.702468
stop_atr_2.50_cost_1.50x: 2023 PnL -$827.12, PF 0.670593
stop_atr_1.50_cost_1.50x: 2023 PnL -$1394.07, PF 0.683708

This means the strategy may be regime-dependent.

Curve-Fitting Assessment

The current evidence is not yet enough to rule out curve fitting.

Reasons curve-fitting risk remains:

H024 was designed after observing H020-H023 failures.
The preferred 3 H4 hold was selected after observing 1, 2, 3, and 4 H4 results.
Validation is still on one broker-native dataset and two symbols.
2023 is a persistent failure year.

Reasons the result is still worth further validation:

H024 is structurally different from the failed Donchian/Chandelier stack.
The hypothesis seed preceded the real H024 run.
No time/session bucket mining was used.
The result survived symbol, side, halves, thirds, and targeted cost/stop stress.
All targeted robustness scenarios passed the headline threshold.
Verdict

H024 hold=3 H4 remains a serious research candidate.

It is not yet promotable.
No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.

Next Required Work

The next validation step should test temporal generalization, not optimize parameters.

Recommended next action:

add a walk-forward or anchored chronological validation diagnostic for H024 hold=3 H4
keep hold fixed at 3 H4
keep the baseline stop ATR multiple fixed at 2.0 first
report train/test chronological folds
do not tune on test folds
do not add time/session filters to remove 2023
do not deploy
