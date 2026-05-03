# External M1 Source Shortlist

## Purpose

This document records the first external M1 data sources to evaluate after broker-native MT5 failed to provide enough M1 history.

This is not an acceptance decision.

This is a shortlist for controlled evaluation.

The governing decision record is:

    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-002-external-m1-data-source-evaluation.md

## Current blocker

H017 needs longer M1 data for both:

- USDJPY
- XAUUSD

The current broker-native MT5 M1 files only cover a short 2026 window.

Current research verdict remains:

    RESEARCH VALIDATION SUFFICIENT: False

H017 remains:

- alive
- not promotable
- blocked by insufficient M1 history
- unsuitable for live trading based on current evidence

## Evaluation rule

No source on this shortlist is trusted automatically.

Before any source can support H017 promotion, it must pass:

- provenance documentation
- timestamp and timezone validation
- OHLC integrity checks
- coverage measurement
- loader-validation tests
- event-driven H017 validation
- comparison against broker-native MT5 behavior where possible

Raw data must not be committed to git.

## Candidate ranking as of 2026-05-03

### Candidate 1 — Dukascopy Historical Data Export / JForex

#### Status

Primary candidate for first evaluation.

#### Why this is first

Dukascopy is the best first external candidate because it appears to offer historical data across forex and commodities, with downloadable CSV data and multiple timeframes.

This matters because H017 needs both:

- USDJPY
- XAUUSD or an equivalent spot-gold instrument

#### Expected advantages

- Likely broad historical coverage.
- Likely supports both forex and commodity-style instruments.
- CSV export path exists.
- JForex Historical Data Manager may provide a controlled manual acquisition path.
- More suitable than a random internet CSV because the data source is identifiable.

#### Main risks

- Dukascopy timestamps and session rules may not match Exness MT5.
- XAUUSD symbol naming may differ.
- Price type may be bid, ask, mid, or source-specific.
- Weekend/session gaps may differ from Exness.
- Spread behavior may not match the existing cost model.
- External data cannot prove live tradability on Exness by itself.

#### Required evaluation before use

Before accepting Dukascopy data for research-grade H017 validation:

1. Download a small USDJPY M1 sample.
2. Download a small XAUUSD M1 sample.
3. Inspect exact columns.
4. Inspect timestamp timezone and bar-open/bar-close convention.
5. Confirm symbol mapping.
6. Confirm whether prices are bid, ask, or another convention.
7. Build or adapt a loader.
8. Add loader-validation tests.
9. Measure coverage using the existing coverage guard.
10. Run the event-driven H017 validation script or a dedicated equivalent.

### Candidate 2 — HistData

#### Status

Secondary candidate.

#### Why this is second

HistData appears to provide M1 data in multiple formats including MT4/MT5 and Generic ASCII.

It may be useful if Dukascopy cannot provide a usable controlled export.

#### Expected advantages

- M1 data is explicitly available.
- Multiple file formats are available.
- Could be easy to inspect manually.

#### Main risks

- Symbol availability must be verified.
- XAUUSD availability must be verified.
- Timestamp semantics must be verified.
- Source provenance and construction must be documented.
- Broker mismatch versus Exness remains unresolved.
- Any paid or automated update path must be documented separately.

#### Required evaluation before use

Before accepting HistData data for research-grade H017 validation:

1. Confirm USDJPY M1 availability.
2. Confirm XAUUSD M1 availability.
3. Download small samples only.
4. Inspect exact schema.
5. Verify timestamps and timezone.
6. Add loader-validation tests.
7. Measure coverage.
8. Record the vendor mismatch risk.

### Candidate 3 — TrueFX

#### Status

Not a complete first candidate.

#### Why this is not first

TrueFX may be useful for institutional-style FX tick data, and it documents GMT timestamps.

However, it appears oriented toward major currency pairs. That may help USDJPY, but it does not obviously solve XAUUSD.

Using TrueFX for USDJPY while using a different source for XAUUSD would introduce a cross-source mismatch.

#### Expected advantages

- Institutional FX orientation.
- Tick-level data.
- GMT timestamp convention is documented.

#### Main risks

- Does not clearly solve XAUUSD.
- May force mixed-source validation.
- Mixed-source validation is not acceptable without a separate mismatch review.
- Tick data would require aggregation rules before use as M1 bars.

#### Required evaluation before use

Only consider TrueFX if:

1. XAUUSD is confirmed unavailable from better unified sources.
2. A separate mixed-source decision is written.
3. Tick-to-M1 aggregation rules are specified.
4. Loader-validation tests are added.

### Candidate 4 — FirstRate Data

#### Status

Paid/reference candidate, not first.

#### Why this is not first

FirstRate Data appears to provide historical intraday FX bars including USDJPY and multiple intraday timeframes.

However, visible FX availability does not by itself establish a unified USDJPY plus spot-XAUUSD source for this project.

#### Expected advantages

- Commercial data source.
- Intraday OHLCV bars are available for FX.
- USDJPY appears in the listed FX dataset family.

#### Main risks

- XAUUSD availability in the same source family must be verified.
- Timezone may differ from Exness MT5.
- Paid-data terms and redistribution limits must be documented.
- Commercial data is not automatically better unless provenance and schema are clear.

#### Required evaluation before use

Only consider FirstRate Data if:

1. USDJPY and XAUUSD availability are both confirmed.
2. Terms and local-use limits are documented.
3. Timezone convention is documented.
4. Samples are inspected before purchase or full ingestion.
5. Loader-validation tests are added.

## Current recommendation

Evaluate Dukascopy first.

Do not build a loader yet.

The next safe step is to acquire small sample files only, inspect their exact schema, and then decide whether a dedicated Dukascopy loader phase is justified.

## Explicit non-goals

Do not tune H017.

Do not promote H017.

Do not go live.

Do not commit raw external data.

Do not silently mix data sources.

Do not assume external XAUUSD matches Exness XAUUSD.

Do not accept any source without loader-validation tests.

## Next operational step

If proceeding with Dukascopy evaluation, acquire very small samples first.

Suggested sample target:

- USDJPY M1 for one trading day
- XAUUSD M1 for one trading day

Store samples locally under data/raw only.

Do not commit the samples.

After sample acquisition, inspect:

- filename
- columns
- first rows
- timestamp format
- timezone assumption
- OHLC integrity
- duplicate timestamps
- missing bars
