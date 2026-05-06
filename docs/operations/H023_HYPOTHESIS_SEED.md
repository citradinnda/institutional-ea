# H023 Entry Edge Falsification Hypothesis Seed

## Purpose

H023 tests whether the current Donchian/Chandelier-derived entry stack has durable directional value before additional risk/lifecycle engineering is attempted.

H020, H021, and H022 showed that risk scaling, stop-distance filtering, and fixed lifecycle variants can reduce damage but have not produced validated positive expectancy. H023 therefore asks a simpler question:

Does the entry signal itself have robust forward edge after modeled costs, across time, symbols, sides, and holding horizons?

If not, the current entry stack should be deprioritized rather than repeatedly rescued with lifecycle/risk variants.

## Status

Research only.

No strategy is validated.
No demo deployment is approved.
No live trading is approved.
Phase 4 is not approved.

## Data Rules

Use only:

- Exness demo MT5 broker-native exports
- USDJPY and XAUUSD
- Broker-native H4 and M1
- Strict common complete H4/M1 bridge windows
- Broker timezone: Europe/Athens, DST-aware

Do not use:

- HistData
- Broker H4 plus HistData M1 combinations
- Sparse 2018 through 2021-06 broker-native prefix as dense M1
- Incomplete bridge windows
- M1 imputation, forward-fill, backfill, or synthetic bars

## Signal Source

Use the existing H020 bridge-compatible signal/intention source as the entry source.

H018 hard guards remain unchanged.

H023 must not implement H021 positive time/session buckets as trading rules.

## Diagnostic Design

For each accepted entry intent, measure neutral forward outcomes over fixed H4 horizons, for example:

- 1 H4 bar
- 2 H4 bars
- 3 H4 bars
- 4 H4 bars
- 6 H4 bars
- 8 H4 bars

The diagnostic should evaluate whether entry direction has edge independent of the existing stop/lifecycle contract.

Suggested outputs:

- fill/intention count
- mean and median forward PnL
- total forward PnL
- profit factor
- win rate
- return after modeled costs
- max drawdown from sequential replay if applicable
- symbol split
- side split
- chronological halves
- chronological thirds

If M1 path analysis is included, also report:

- maximum favorable excursion
- maximum adverse excursion
- adverse excursion versus initial risk geometry
- stop-equivalent touch rate
- whether favorable excursion exists before adverse excursion

## Pass Criteria

H023 is not promotable unless a tested entry-edge view shows all of the following:

- full-period profit factor >= 1.15 after modeled costs
- positive full-period total return after modeled costs
- no chronological third has profit factor below 0.95
- at least two of three chronological thirds have profit factor >= 1.05
- first half and second half are both positive or near-flat, with neither below -5%
- no single symbol contributes more than 75% of total net profit
- no single side contributes more than 75% of total net profit unless explicitly justified
- evidence is not dependent on H021 time/session positive buckets

## Falsification Criteria

H023 should be considered failed if:

- forward entry returns remain negative after modeled costs
- profit factor remains materially below 1.15
- apparent edge exists only in one chronological split
- apparent edge depends mainly on one symbol or one side
- median outcomes remain negative while totals are rescued by a small number of outliers
- MFE/MAE shows that adverse movement consistently appears before favorable movement
- results merely reproduce H021 in-sample bucket artifacts

## Interpretation Rules

Do not treat H023 as deployment approval.

A positive H023 result would only justify designing a later strategy hypothesis with explicit risk/lifecycle rules.

A negative H023 result means the current entry stack should be deprioritized rather than repeatedly tuned.

## Runtime Discipline

Do not run the real-data diagnostic casually.

The next implementation should prefer reusable/cached intermediate tables where practical, because recent real-data diagnostics took roughly 30-60 minutes.
