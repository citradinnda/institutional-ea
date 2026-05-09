# H024 Chronological Validation Result

## Status

H024 hold=3 H4 passed the first chronological validation diagnostic.

H024 is still not fully validated.
H024 is not demo-approved.
H024 is not live-approved.
Phase 4 is not approved.

## Diagnostic

Command:

```powershell
python .\scripts\diagnose_h024_walk_forward_real.py

Setup:

Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
broker-native H4 and M1
strict complete H4/M1 bridge windows
accepted bridge-window count: 5476
H024 pullback-continuation bridge shim
fixed lifecycle hold: 3 H4
baseline stop ATR multiple: 2.0
baseline modeled costs
no H021 time/session bucket mining
no 2023 exclusion
no parameter optimization
Summary
Fold    Train count    Test count    Test start UTC    Test end UTC    Fills    Return    Max DD    PF    Headline pass
anchored_train_25%_test_rest    1369    4107    2023-01-05T22:00:00+00:00    2026-04-30T01:00:00+00:00    359    17.8797%    -6.6593%    1.225915    yes
anchored_train_50%_test_rest    2738    2738    2024-03-05T22:00:00+00:00    2026-04-30T01:00:00+00:00    244    19.2253%    -4.4683%    1.384976    yes
anchored_train_75%_test_rest    4107    1369    2025-04-02T21:00:00+00:00    2026-04-30T01:00:00+00:00    114    13.9192%    -2.6061%    1.653426    yes
Interpretation

H024 hold=3 H4 passed a meaningful anti-curve-fit test.

The candidate remained positive when evaluated only on later chronological test folds with fixed parameters.

This strengthens the evidence that the preliminary H024 result is not only a full-sample artifact.

Persistent Weakness

The 2023 weakness remains visible.

In the 25% train / test-rest fold, which includes 2023 onward:

2023 PnL: -$576.42
2023 PF: 0.764465
2023 stop rate: 18.8889%

Despite this, the full 2023-2026 test-rest fold passed overall.

Do not add a 2023 exclusion or time/session filter to hide this weakness.

Fold Details
25% Train / Test Rest

Test period: 2023-01-05T22:00:00+00:00 to 2026-04-30T01:00:00+00:00

Main metrics:

return: 17.8797%
max drawdown: -6.6593%
PF: 1.225915
fills: 359
stop rate: 12.5348%

Split facts:

USDJPY PF: 1.237560, PnL: $1039.70
XAUUSD PF: 1.211510, PnL: $748.27
buy PF: 1.131004, PnL: $601.04
sell PF: 1.356825, PnL: $1186.93
first half PF: 1.020120, PnL: $88.50
second half PF: 1.483369, PnL: $1699.47
third_1 PF: 1.024866, PnL: $73.75
third_2 PF: 1.171736, PnL: $441.41
third_3 PF: 1.535243, PnL: $1272.80
50% Train / Test Rest

Test period: 2024-03-05T22:00:00+00:00 to 2026-04-30T01:00:00+00:00

Main metrics:

return: 19.2253%
max drawdown: -4.4683%
PF: 1.384976
fills: 244
stop rate: 10.6557%

Split facts:

USDJPY PF: 1.302536, PnL: $855.12
XAUUSD PF: 1.492487, PnL: $1067.42
buy PF: 1.091434, PnL: $274.45
sell PF: 1.827214, PnL: $1648.09
first half PF: 1.239265, PnL: $613.41
second half PF: 1.538693, PnL: $1309.12
third_1 PF: 0.992584, PnL: -$14.52
third_2 PF: 1.698943, PnL: $1024.17
third_3 PF: 1.581388, PnL: $912.89
75% Train / Test Rest

Test period: 2025-04-02T21:00:00+00:00 to 2026-04-30T01:00:00+00:00

Main metrics:

return: 13.9192%
max drawdown: -2.6061%
PF: 1.653426
fills: 114
stop rate: 7.0175%

Split facts:

USDJPY PF: 1.906065, PnL: $1064.99
XAUUSD PF: 1.342415, PnL: $326.94
buy PF: 1.246903, PnL: $320.87
sell PF: 2.289479, PnL: $1071.05
first half PF: 1.776973, PnL: $854.06
second half PF: 1.521702, PnL: $537.86
third_1 PF: 1.542343, PnL: $450.04
third_2 PF: 1.366573, PnL: $280.71
third_3 PF: 2.236731, PnL: $661.17
Verdict

H024 hold=3 H4 remains a serious candidate.

It has now passed:

preliminary full-period validation
targeted stop/cost robustness
chronological test-rest validation

It is still not promotable to demo.

Next Required Work

Next validation should focus on execution realism and operational readiness, not alpha optimization.

Recommended next actions:

Add a trade ledger export diagnostic for H024 hold=3 H4.
Inspect largest winners/losses and 2023 failure trades.
Verify lot sizes, stop distances, symbol contract assumptions, and execution prices.
Reconcile backtest assumptions against MT5 execution constraints.
Do not deploy until this audit is complete.
