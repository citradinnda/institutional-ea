# DR-002: External M1 Data Source Evaluation

## Status

Proposed.

## Date

2026-05-03

## Context

H017 requires realistic event-driven validation using M1 data inside H4 bars.

The event-driven pipeline is already able to:

- Load local MT5 H4 and M1 exports.
- Trim known H4 leakage.
- Build a clean common event window.
- Simulate event-driven fills using M1 intrabar data.
- Apply broker-like execution costs.
- Produce a research sufficiency verdict.

The current blocker is not the pipeline.

The current blocker is insufficient broker-native M1 history.

The current broker-native Exness MT5 terminal/server currently exposes only a short M1 window for the required symbols:

    USDJPY M1 earliest timestamp: 2026-01-26 03:09:00+00:00
    USDJPY M1 latest timestamp: 2026-04-30 07:00:00+00:00

    XAUUSD M1 earliest timestamp: 2026-01-20 02:22:00+00:00
    XAUUSD M1 latest timestamp: 2026-04-30 07:00:00+00:00

The resulting clean common event window is:

    start_utc=2026-01-26 03:09:00+00:00
    end_utc=2026-04-29 09:00:00+00:00

The current common H4 sample is:

    n_common_h4_bars=411

The current minimum required H4 sample is:

    minimum_research_h4_bars=1512

Therefore:

    RESEARCH VALIDATION SUFFICIENT: False

Broker-native MT5 acquisition was attempted and documented in:

    C:\Users\equin\Documents\institutional-ea\docs\operations\MT5_M1_ACQUISITION_ATTEMPTS.md

The attempt did not improve effective M1 coverage.

## Decision

External M1 data may be evaluated, but it must not be silently accepted as research evidence.

Before any external M1 source is used for H017 promotion decisions, the project must document:

- Data source name.
- Data vendor or broker origin.
- Instrument mapping for USDJPY and XAUUSD.
- Timezone convention.
- Timestamp semantics.
- Column schema.
- Price type.
- Session coverage.
- Weekend handling.
- Missing bar behavior.
- Spread availability or absence.
- Known limitations.
- License or terms constraints.
- Whether the source is suitable for redistribution or only local research use.

A new external data source must go through loader-validation work before its outputs are trusted.

## Non-negotiable acceptance criteria

An external M1 source must satisfy all of the following before it can support research-grade H017 event validation.

### 1. Provenance is documented

Provenance means where the data came from and how it was produced.

The source must be traceable enough that future runs can identify the same data family again.

Minimum provenance fields:

- Source name.
- Vendor, broker, or platform.
- Download or export method.
- Download date.
- Instrument names as provided by the source.
- Any symbol suffixes or broker-specific aliases.
- Whether data is bid, ask, mid, trade, or unknown.

### 2. Timezone semantics are explicit

Timezone semantics means what timezone the timestamps represent.

The loader must not guess silently.

The source must state or be empirically validated for:

- Raw timestamp timezone.
- Daylight saving time behavior, if applicable.
- Whether timestamps mark bar open time or bar close time.
- Whether timestamps can be converted cleanly to UTC.

### 3. Bar schema is validated

Bar schema means the expected columns and their meanings.

At minimum, M1 data must provide:

- timestamp
- open
- high
- low
- close

Volume is optional for H017, but if present, its meaning must be documented.

Spread is optional because the current backtest cost model applies explicit spread assumptions. If spread is present, it must not silently override the cost model.

### 4. OHLC integrity is checked

OHLC means open, high, low, close.

For each bar:

- high must be greater than or equal to open.
- high must be greater than or equal to close.
- low must be less than or equal to open.
- low must be less than or equal to close.
- prices must be positive.
- timestamps must be monotonic after sorting.
- duplicate timestamps must be rejected or explicitly resolved.

### 5. Coverage is measured, not assumed

The project must compute:

- earliest timestamp by symbol.
- latest timestamp by symbol.
- clean common event window start.
- clean common event window end.
- common H4 bar count.
- minimum required H4 bar count.
- research sufficiency verdict.

A source that does not reach the required M1 window may still be useful for pipeline testing, but not for H017 promotion.

### 6. Broker mismatch risk is acknowledged

External data may not match Exness execution conditions.

Differences may include:

- broker server timezone.
- session gaps.
- weekend bars.
- gold symbol conventions.
- bid/ask construction.
- spread regime.
- liquidity around news.
- stop-out behavior.
- quote filtering.

Because of this, an external data source can support research, but it does not automatically prove live tradability on Exness.

### 7. Loader tests are required

Before external data is trusted, tests must be added for the new loader or adapter.

The tests should verify:

- timestamp parsing.
- timezone conversion to UTC.
- required column mapping.
- OHLC validation.
- duplicate handling.
- missing required column errors.
- representative USDJPY sample loading.
- representative XAUUSD sample loading.

### 8. Raw data remains uncommitted

Raw external M1 data must not be committed to git.

Local raw data should remain under:

    C:\Users\equin\Documents\institutional-ea\data\raw

The root-anchored gitignore rule must remain:

    /data/

It must not be changed to:

    data/

The unanchored form previously risked excluding source code under:

    C:\Users\equin\Documents\institutional-ea\quantcore\data

## Rejected shortcuts

The following are explicitly rejected:

- Using a random CSV without provenance.
- Tuning H017 parameters to the current short 2026 M1 window.
- Treating the short-window positive return as validated edge.
- Mixing H4 data from one source with M1 data from another source without documenting the mismatch.
- Silently changing broker, account server, or symbol mapping.
- Assuming UTC timestamps without proof.
- Assuming external XAUUSD bars match Exness XAUUSD execution.
- Committing raw M1 files to git.
- Moving to live trading before research-grade event validation.

## Required next work before accepting external M1

Before external M1 data can be used as research evidence, create a dedicated implementation phase that includes:

1. A documented source selection.
2. A small sample file inspection.
3. A loader or adapter design.
4. Loader-validation tests.
5. A coverage report using the same research sufficiency rules.
6. A recorded H017 event validation run.
7. A comparison note against broker-native MT5 data behavior.

## Consequences

This decision slows down the path to H017 promotion, but it protects the project from false confidence.

The project remains infrastructure-first.

H017 remains:

- alive.
- not promotable.
- blocked by insufficient M1 history.
- unsuitable for live trading based on current evidence.

The next acceptable step is not strategy tuning.

The next acceptable step is controlled evaluation of a better M1 data source under documented rules.
