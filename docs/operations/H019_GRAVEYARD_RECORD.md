# H019 Graveyard Record

## Verdict

H019 is failed in its current form.

H019 is not validated.

H019 is not promotable.

H019 is not live-approved.

H019 does not authorize Phase 4 execution.

H019 does not authorize live trading.

## Hypothesis Identity

H019 was created after H018 diagnostics showed that H017/H018 had a stale-held-signal / stop-lifecycle mismatch.

H019 changed the strategy semantics from:

- continuous held Donchian exposure using raw Chandelier panels,

to:

- Donchian entry or flip trigger,
- same-side Chandelier close-based lifecycle exit,
- flat state after stop breach,
- no re-entry from stale held Donchian direction,
- no opposite stop-panel switching.

## Implemented H019 Components

Code:

- `quantcore/strategy/h019.py`
- `quantcore/backtest/h019_strict_event.py`
- `scripts/run_h019_strict_event_real.py`

Tests:

- `tests/test_h019.py`
- `tests/test_h019_strict_event.py`
- `tests/test_h019_strict_event_real_script.py`

Latest full-test count after H019 runner:

- `588 passed`

Relevant commits:

- `d0bc62d Add H019 stateful chandelier lifecycle`
- `5b4097d Add H019 portfolio integration`
- `41538c4 Add H019 strict event routing`
- `ea95f1a Add H019 strict real-data runner`

## Strict Broker-Native Validation Attempt

The user explicitly authorized:

- `Authorized: run strict H019 broker-native validation.`

Command run:

- `python .\scripts\run_h019_strict_event_real.py`

Data source:

- Exness demo MT5 broker-native exports
- USDJPY H4/M1
- XAUUSD H4/M1
- broker timezone: `Europe/Athens`

Strict bridge-window preflight passed.

Accepted window contract:

- `expected_m1_bars_per_h4=240`
- `expected_h4_delta=0 days 04:00:00`
- `candidate_common_h4_count=8654`
- `usdjpy_complete_count=5685`
- `xauusd_complete_count=6149`
- `common_complete_count=5476`
- `accepted_count=5476`
- `first_accepted_timestamp=2021-07-02 13:00:00+00:00`
- `last_accepted_timestamp=2026-04-30 01:00:00+00:00`
- `usdjpy_only_complete_count=209`
- `xauusd_only_complete_count=673`
- `rejected_count=3178`

The validation failed closed during strict event execution.

Failure exception:

- `H018MaximumPerTradeLeverageError`

First failure:

- symbol: `USDJPY`
- side: `buy`
- decision_time: `2021-07-05 21:00:00+00:00`
- entry_time: `2021-07-06 01:00:00+00:00`
- entry_raw_price: `110.840000000`
- stop_price: `110.741028558`
- raw_stop_distance: `0.098971442`
- equity_usd: `9872.94`
- lots: `1.20`
- contract_size: `100000.000000000`
- quote_currency: `JPY`
- notional_quote: `13300800.000000000`
- notional_usd: `120000.000000000`
- gross_leverage: `12.154432565`
- maximum_gross_leverage: `10.000000000`
- validation_action: `fail_closed`

## Interpretation

This was not a data-preflight failure.

This was not a HistData issue.

This was not an infrastructure failure.

This was not a normal Python bug.

The H018 leverage guard did exactly what it was designed to do: fail closed when a single trade exceeded the maximum allowed USD gross notional leverage.

H019 appears to have moved the first blocker from invalid stop lifecycle geometry to notional leverage sizing. That is useful evidence, but it is not validation.

## Why H019 Failed

H019 addressed the stop-lifecycle mismatch but preserved the H017-style risk sizing structure.

The event engine sizes lots from:

- equity,
- signed risk fraction,
- raw entry price,
- raw stop distance,
- contract spec,
- broker lot step.

When the stop distance is relatively tight, the same target risk can imply too much gross notional exposure.

In the first H019 failure, USDJPY produced:

- target trade that rounded to `1.20` lots,
- `120000` USD notional,
- equity only `9872.94`,
- per-trade gross leverage `12.1544x`.

The H018 per-trade leverage limit is `10.0x`, so the run failed closed.

## What Not To Do

Do not fix H019 by:

- weakening the H018 leverage guard,
- raising the 10x maximum casually,
- clipping lots silently,
- skipping the trade silently,
- treating the failed validation as a pass,
- changing costs,
- changing raw versus executable entry sizing silently,
- switching stop panels,
- broadening symbols,
- adding ML,
- approving live trading.

## Research Lesson

H019 fixed one structural problem but exposed another:

- H017/H018 problem: stale held signal versus stop lifecycle.
- H019 problem: sizing can exceed strict USD gross leverage limits when stop distance is tight.

Therefore, the next hypothesis should explicitly define the sizing and leverage contract as part of the strategy, not as an after-the-fact guard failure.

## Final H019 Status

H019 is in the strategy graveyard.

H019 may remain useful as a component reference for lifecycle semantics.

H019 is not a promotable trading strategy.

H019 does not approve live trading.
