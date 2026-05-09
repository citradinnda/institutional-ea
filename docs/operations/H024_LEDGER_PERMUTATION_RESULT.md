# H024 Ledger-Level Permutation Result

Research diagnostic only.

This is not:
- demo approval
- live approval
- Phase 4 approval
- execution approval

## Diagnostic

Command:

```powershell
python .\scripts\diagnose_h024_ledger_permutation.py
Method

This is a cheap ledger-level negative-control proxy.

It uses the existing H024 hold=3 trade ledger and randomly reorders the realized trade PnLs 10,000 times.

This tests whether the observed trade-order equity path was unusually lucky.

It does not:

test signal direction
replace full execution timestamp-shuffle validation
rerun M1 lifecycle execution
approve deployment
Result

Observed ledger path:

Metric    Value
total_pnl_usd    4093.92
ending_equity_usd    14093.92
max_drawdown    -6.7346%
min_equity_usd    9901.07
ruin    false

Permutation distribution:

Metric    Min    P10    Median    Mean    P90    Max
ending_equity_usd    14093.922816    14093.922816    14093.922816    14093.922816    14093.922816    14093.922816
total_pnl_usd    4093.922816    4093.922816    4093.922816    4093.922816    4093.922816    4093.922816
max_drawdown    -0.234424    -0.101874    -0.070896    -0.074721    -0.052177    -0.034531
min_equity_usd    8125.074718    9409.475200    9830.724716    9757.552260    10000.000000    10000.000000

Summary:

Metric    Value
permutation runs    10000
seed    240240
permutations with max_drawdown <= observed max_drawdown    5744
max-drawdown worse/equal rate    57.4400%
permutations with min_equity <= observed min_equity    6430
min-equity worse/equal rate    64.3000%
permutation ruin count    0
Interpretation

The realized H024 trade order was not unusually lucky.

The observed max drawdown was slightly better than the shuffled median and mean, but not suspiciously favorable. A majority of random PnL reorderings had drawdown or minimum-equity outcomes worse than or equal to the observed path.

This reduces concern that H024's equity curve depends on an unusually lucky ordering of realized winners and losers.

This does not prove future survivability and does not replace a full execution timestamp-shuffle diagnostic.

Status

H024 remains:

not demo-approved
not live-approved
not Phase 4-approved

Current anti-curve-fit posture:

direction-flip negative control passed
ledger-level path permutation control passed
expensive full timestamp-shuffle control was abandoned pending cheaper implementation or batching
2023 stop-exit weakness remains unresolved but appears stop-regime driven, not leverage-driven
