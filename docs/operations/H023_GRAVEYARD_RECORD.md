# H023 Graveyard Record - Entry Edge Falsification

## Status

H023 is closed and moved to the graveyard.

H023 is not promotable.
H023 is not demo-approved.
H023 is not live-approved.
Phase 4 is not approved.

## Hypothesis

H023 tested whether the current H020 bridge-compatible Donchian/Chandelier-derived entry source had durable forward directional value before further risk/lifecycle engineering.

The intended falsification rule was direct:

- if neutral fixed-horizon forward outcomes were negative or unstable after modeled costs,
- then further attempts to rescue this entry stack with stop, lifecycle, or risk tuning should stop.

## Evidence

The preliminary real-data diagnostic used:

- Exness demo MT5 broker-native exports only
- USDJPY and XAUUSD
- broker-native H4 and M1 data
- strict complete H4/M1 bridge windows
- 5476 accepted bridge windows
- modeled spread, commission, and stop slippage costs
- H020 bridge-compatible signal source
- H018 hard guard semantics preserved

Completed forward horizons failed:

| Horizon | Return | Max drawdown | Profit factor |
|---|---:|---:|---:|
| 1 H4 | -94.2001% | -94.2292% | 0.722317 |
| 2 H4 | -94.9742% | -95.0091% | 0.674590 |
| 3 H4 | -90.4705% | -90.4343% | 0.730661 |
| 4 H4 | -77.3948% | -77.3261% | 0.795790 |

The 6 H4 and 8 H4 rows produced no executions and are treated as a diagnostic design/runtime issue, not as evidence of profitability.

## Verdict

H023 failed.

The current H020 bridge-compatible entry source did not show robust forward directional edge after modeled costs across the completed 1, 2, 3, and 4 H4 forward horizons.

Removing stop exits did not reveal hidden profitability. All completed horizons had negative full-period return, severe drawdown, and profit factor materially below the required 1.15 threshold.

## Research Consequence

Do not continue trying to rescue the current Donchian/Chandelier entry stack through:

- risk scaling
- lifecycle tuning
- stop-distance filtering
- time/session buckets
- parameter sweeps
- H021 positive-bucket mining

Future work should use either:

1. a genuinely new H024 entry hypothesis, or
2. infrastructure work that reduces diagnostic runtime and failure risk.

## Deployment Consequence

There is still no validated strategy.

No demo trading is approved.
No live trading is approved.
Phase 4 is not approved.
