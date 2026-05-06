# H023 Entry Edge Preliminary Result

## Status

Preliminary real-data result recorded from the first H023 diagnostic run.

Research only.

No strategy is validated.
No demo deployment is approved.
No live trading is approved.
Phase 4 is not approved.

## Context

H023 was designed to test whether the H020 bridge-compatible Donchian/Chandelier-derived entry source has durable forward directional value before further stop/lifecycle/risk engineering.

The diagnostic intentionally avoided H021 positive time/session bucket rules.

## Real Diagnostic Run

Command:

```powershell
python .\scripts\diagnose_h023_entry_edge_real.py
Data:

Exness demo MT5 broker-native exports only
USDJPY and XAUUSD
Broker-native H4 and M1
Strict common complete H4/M1 bridge windows
Accepted bridge-window count: 5476
The run completed the expensive main forward-horizon backtests and printed the main summary table, then crashed during split-report formatting.

The split-report crash was caused by calling summarize_fills_by_field with a positional field argument instead of keyword argument field=....

The reporting bug was fixed afterward in commit:

ce40929 Fix H023 split report formatting
Because the main horizon summary completed before the crash, the preliminary H023 research conclusion can still be recorded.

Main Summary Result
Horizon    Accepted    Executed    Skipped    Fills    Ending equity    PnL    Return    Max DD    PF    Win rate
1 H4    5476    3318    2158    3860    $579.99    -$9420.01    -94.2001%    -94.2292%    0.722317    45.8031%
2 H4    5476    2337    3139    2683    $502.58    -$9497.42    -94.9742%    -95.0091%    0.674590    47.3723%
3 H4    5476    1883    3593    2183    $952.95    -$9047.05    -90.4705%    -90.4343%    0.730661    47.0912%
4 H4    5476    1280    4196    1520    $2260.52    -$7739.48    -77.3948%    -77.3261%    0.795790    48.3553%
6 H4    5476    0    5476    0    $10000.00    $0.00    0.0000%    0.0000%    nan    nan
8 H4    5476    0    5476    0    $10000.00    $0.00    0.0000%    0.0000%    nan    nan
Preliminary Verdict
H023 failed the main entry-edge falsification test.

The current H020 bridge-compatible entry source did not show robust forward directional edge after modeled costs across the completed 1, 2, 3, and 4 H4 horizons.

Removing stop exits did not reveal hidden profitability.

All completed forward horizons had:

negative full-period return
severe drawdown
profit factor materially below the required 1.15 threshold
The 6 H4 and 8 H4 rows produced no executions and should be treated as a diagnostic design/runtime issue, not as evidence of profitability.

Interpretation
The preliminary H023 result points away from further attempts to rescue the current Donchian/Chandelier entry stack with stop/lifecycle/risk tuning.

Combined with H020, H021, and H022:

H020 failed performance badly.
H021 found useful failure-mode clues but no stable strategy.
H022 reduced damage but remained negative.
H023 did not reveal hidden forward entry edge.
No strategy is promotable from this evidence.

Rerun Policy
A rerun of H023 may be useful only if complete split details are needed for archival purposes after the reporting fix.

Do not rerun casually because recent real-data diagnostics have taken roughly 30-60 minutes.

If rerun, treat it as research-only and record the complete split report separately.
