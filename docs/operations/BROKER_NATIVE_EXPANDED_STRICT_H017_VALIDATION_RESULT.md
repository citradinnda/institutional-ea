# Broker-Native Expanded Strict H017 Validation Result

## Status

H017 failed the expanded broker-native strict event-driven validation by account insolvency.

This is a fail-closed validation result, not a data preflight failure.

## Validation Path

Script:

    scripts/run_h017_strict_event_real.py

Data source:

    Exness demo MT5 broker-native exports

Symbols:

    USDJPY
    XAUUSD

Timeframes:

    Broker-native H4
    Broker-native M1

Broker timezone:

    Europe/Athens

Important restrictions:

1. No HistData was used.
2. No derived datasets were written.
3. No M1 imputation was used.
4. No forward-fill or backfill was used.
5. No synthetic bars were inserted.
6. Native H4 index semantics were preserved.
7. Accepted strict bridge-window timestamps were passed into the strict event wrapper.
8. H017 parameters were not tuned.
9. Cost-model assumptions were not changed.
10. The result does not approve live trading.

## Code State

Relevant commits:

    e2c9283 Catch strict H017 insolvency in console main
    9853c6a Report strict H017 insolvency validation failure
    247af24 Fail closed on H017 event backtest insolvency
    a5c3e93 Add handoff document #32 after strict expanded H017 crash localization
    47f80a8 Add strict expanded H017 validation runner

Full-test anchor after the insolvency handling work:

    533 passed

## Raw MT5 Export Summaries

USDJPY H4:

    n_input_rows=8713
    n_bars=8713
    earliest_utc=2018-07-02 21:00:00+00:00
    latest_utc=2026-04-30 05:00:00+00:00
    broker_tz=Europe/Athens

XAUUSD H4:

    n_input_rows=8658
    n_bars=8658
    earliest_utc=2018-06-27 21:00:00+00:00
    latest_utc=2026-04-30 05:00:00+00:00
    broker_tz=Europe/Athens

USDJPY M1:

    n_input_rows=1785312
    n_bars=1785312
    earliest_utc=2018-07-02 21:00:00+00:00
    latest_utc=2026-04-30 07:00:00+00:00
    broker_tz=Europe/Athens

XAUUSD M1:

    n_input_rows=1704907
    n_bars=1704907
    earliest_utc=2018-06-27 21:00:00+00:00
    latest_utc=2026-04-30 07:00:00+00:00
    broker_tz=Europe/Athens

## Strict Bridge-Window Preflight Result

The strict complete H4/M1 bridge-window preflight passed.

Required rule:

1. USDJPY has a broker-native H4 bar at the H4 timestamp.
2. XAUUSD has a broker-native H4 bar at the same H4 timestamp.
3. For each symbol, the next H4 timestamp is exactly four hours later.
4. For each symbol, the M1 window `[H4 timestamp, H4 timestamp + 4 hours)` contains exactly 240 M1 bars.
5. No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

Observed result:

    expected_m1_bars_per_h4=240
    expected_h4_delta=0 days 04:00:00
    candidate_common_h4_count=8654
    usdjpy_complete_count=5685
    xauusd_complete_count=6149
    common_complete_count=5476
    accepted_count=5476
    first_accepted_timestamp=2021-07-02 13:00:00+00:00
    last_accepted_timestamp=2026-04-30 01:00:00+00:00
    usdjpy_only_complete_count=209
    xauusd_only_complete_count=673
    rejected_count=3178

Rejection counts:

    usdjpy_m1_count_not_expected: 2969
    usdjpy_missing_next_h4_timestamp: 1
    usdjpy_non_4h_next_h4_delta: 1179
    xauusd_m1_count_not_expected: 2505
    xauusd_missing_next_h4_timestamp: 1
    xauusd_non_4h_next_h4_delta: 1193

## Strict Event-Driven Backtest Result

The strict event-driven backtest did not complete.

Failure reason:

    insolvency

Fatal interval:

    decision_time=2021-07-06 01:00:00+00:00
    entry_time=2021-07-06 05:00:00+00:00
    forced_exit_time=2021-07-06 09:00:00+00:00
    interval_start_equity_usd=9847.56
    interval_pnl_usd=-11835.26
    ending_equity_usd=-1987.71
    interval_return_pct=-120.18
    interval_fills=2

Fatal interval fills:

USDJPY:

    symbol=USDJPY
    side=buy
    entry_time=2021-07-06 05:00:00+00:00
    exit_time=2021-07-06 05:00:00+00:00
    entry_price=110.775000000
    exit_price=110.765228764
    lots=518.77
    pnl_quote=-506902.42
    commission=7262.78
    slippage=0.000012040
    exit_reason=stop

XAUUSD:

    symbol=XAUUSD
    side=buy
    entry_time=2021-07-06 05:00:00+00:00
    exit_time=2021-07-06 09:00:00+00:00
    entry_price=1807.480000000
    exit_price=1809.622000000
    lots=0.02
    pnl_quote=4.28
    commission=0.40
    slippage=0.000000000
    exit_reason=signal_flip

## Interpretation

The validation failure is caused by event-engine execution reaching account ruin on a complete strict bridge window.

This is not a missing-M1 problem. The fatal window was already identified as having exactly 240 M1 bars.

The immediate pathological event is a USDJPY long sized to 518.77 lots on an account with approximately 9847.56 USD of interval-start equity.

Prior diagnostics localized the sizing pathology to a near-zero raw stop distance:

    raw entry price=110.770000000
    H017 long stop=110.770240804

The long stop was slightly above the raw H4 entry open, while below the cost-adjusted buy entry. The current event engine sizes from:

    abs(raw H4 entry open - stop_price)

before entry spread is applied.

This document records the observed validation result. It does not silently change sizing semantics, cost semantics, or H017 strategy logic.

## Research Verdict

    STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True
    H017 STRICT EVENT BACKTEST COMPLETED: False
    H017 VALIDATION FAILED BY INSOLVENCY: True
    H017 PROMOTABLE BY CLAIM: False
    EXPANDED VALIDATION IS RESEARCH EVIDENCE ONLY: True
    LIVE TRADING APPROVED: False

## Guardrails

1. H017 is not promotable.
2. Live trading is not approved.
3. This result must not be hidden by tuning.
4. This result must not be fixed by silently changing raw-entry versus executable-entry sizing.
5. Any future sizing semantics change must be explicit, tested, and documented.
6. HistData remains rejected for H017 validation under current evidence.
7. Broker-native source acceptance is not strategy promotion.
