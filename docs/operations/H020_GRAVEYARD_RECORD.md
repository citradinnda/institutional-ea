# H020 Graveyard Record

H020 was a sizing-contract hypothesis built on H019 lifecycle semantics.

## Purpose

H020 attempted to fix H019's remaining strict-validation blocker:

- excessive per-trade USD gross leverage when stop distance was tight,
- portfolio-wide gross leverage overlap,
- invalid/non-protective stop geometry,
- below-spread raw stop distances.

H020 used:

- H019 Donchian entry/flip plus stateful same-side Chandelier lifecycle,
- same-side Chandelier stops,
- strategy-level `9.0x` per-trade gross notional cap,
- strategy-level `9.0x` portfolio gross notional cap,
- flat/no-intent suppression for invalid stop geometry,
- flat/no-intent suppression for raw stop distances below one modeled spread,
- strict H018 hard guards unchanged.

## Validation Status

H020 successfully passed strict broker-native event validation across the accepted Exness complete-window dataset without guard violations.

Accepted strict bridge windows:

- `5476`

Accepted range:

- first UTC: `2021-07-02 13:00:00+00:00`
- last UTC: `2026-04-30 01:00:00+00:00`

This proved that the H020 sizing contract could survive the strict event/guard layer.

It did not prove profitability.

## Performance Diagnostic

Real diagnostic command:

- `python .\scripts\diagnose_h020_performance_real.py`

Result:

- accepted_entry_count: `5476`
- executed_entry_count: `5476`
- skipped_entry_count: `3176`
- fill_count: `4158`
- starting_equity_usd: `\$10000.00`
- ending_equity_usd: `\$819.07`
- total_pnl_usd: `-\$9180.93`
- total_return: `-91.8093%`
- max_drawdown: `-91.8860%`
- winning_fill_count: `1837`
- losing_fill_count: `2321`
- flat_fill_count: `0`
- win_rate: `44.1799%`
- gross_profit_usd: `\$28703.99`
- gross_loss_usd: `-\$37884.92`
- profit_factor: `0.757663`
- mean_fill_return: `-0.0579%`
- median_fill_return: `-0.0375%`
- fill_return_sharpe: `-0.086278`

## Verdict

H020 failed performance evaluation.

H020 is:

- not promotable,
- not live-approved,
- not Phase-4-approved.

The result is not a small parameter miss. H020 survived the guard layer but lost most account equity under strict broker-native event simulation and modeled costs.

## Do Not Patch H020 By

Do not:

- weaken H018 hard guards,
- raise the `10.0x` hard leverage guard casually,
- raise H020 `9.0x` strategy caps casually,
- reduce costs casually,
- switch stop panels casually,
- broaden symbols,
- add ML,
- treat guard-validation success as strategy validation,
- approve live trading,
- approve Phase 4.

## Lesson

H020 separated execution survivability from profitability.

That was useful: the project now has a cleaner distinction between:

- a strategy that can be represented safely under strict event constraints, and
- a strategy that actually has positive expectancy.

H020 achieved the first and failed the second.
