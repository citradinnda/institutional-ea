# H021 Hypothesis Seed

H021 starts after H020 failed performance evaluation.

## Current State

H020 proved that the strategy can be represented safely under strict event constraints:

- invalid stop geometry suppressed,
- below-spread stop distances suppressed,
- per-trade gross leverage capped,
- portfolio gross leverage capped,
- H018 hard guards unchanged.

But H020 failed performance:

- starting_equity_usd: `\$10000.00`
- ending_equity_usd: `\$819.07`
- total_return: `-91.8093%`
- max_drawdown: `-91.8860%`
- profit_factor: `0.757663`
- fill_return_sharpe: `-0.086278`

Therefore H020 is in the graveyard.

## H021 Purpose

H021 is not another sizing patch.

H021 must search for positive expectancy before adding more execution machinery.

Core question:

> Can USDJPY + XAUUSD produce a cost-amortized, event-safe edge under strict broker-native H4/M1 simulation?

## H021 Design Direction

H021 should keep the useful infrastructure lessons:

- strict broker-native Exness complete-window validation only,
- M1 intrabar stop resolution inside H4 decisions,
- conservative stop-first fill rule when SL and TP are both touched in one M1 bar,
- modeled spread, commission, and slippage,
- H018 hard guards unchanged,
- no raw-data mutation,
- no HistData,
- no live trading.

H021 should not begin by increasing risk or leverage.

H021 should begin by reducing bad trades.

Likely research directions:

1. Cost-amortization filters
   - avoid trades where expected move is too small versus spread/commission/slippage,
   - require stop distance and target opportunity to be large enough relative to modeled costs.

2. Regime gating
   - avoid low-volatility chop,
   - avoid structurally unfavorable sessions or volatility states if supported by evidence.

3. Entry selectivity
   - Donchian breakout alone may be too weak after costs,
   - require additional confirmation that does not introduce lookahead.

4. Exit asymmetry
   - H019/H020 same-side Chandelier lifecycle survived structurally but may cut winners/hold losers poorly,
   - test whether explicit profit-taking or trailing logic improves expectancy under M1 event simulation.

5. Symbol-specific behavior
   - USDJPY and XAUUSD should be diagnosed separately before assuming the combined portfolio is useful.

## H021 Non-Negotiables

Do not:

- weaken H018 guards,
- raise hard leverage caps casually,
- lower costs casually,
- approve live trading,
- approve Phase 4,
- add ML,
- broaden symbols,
- use HistData,
- tune on sparse or incomplete windows,
- treat a prettier backtest without strict M1 event simulation as evidence.

## First Engineering Step

Build an H021 baseline diagnostic, not a full strategy.

The first useful diagnostic should decompose H020/H019-style trades by:

- symbol,
- side,
- exit reason,
- stop distance bucket,
- gross leverage bucket,
- time/session bucket if available,
- realized P&L after costs.

Goal:

- identify whether losses are broad-based or concentrated in identifiable regimes.

H021 should only become a new strategy after diagnostics show a plausible, non-fictional source of positive expectancy.
