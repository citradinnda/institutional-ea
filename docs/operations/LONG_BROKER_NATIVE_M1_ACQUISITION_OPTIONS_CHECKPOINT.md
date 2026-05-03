# Long Broker-Native M1 Acquisition Options Checkpoint

Phase: 3.26-y  
Status: checkpoint only  
Date: 2026-05-03

## Purpose

This checkpoint documents the next practical data-infrastructure path after rejecting HistData for H017 validation under current evidence.

The goal is to preserve strict source-acceptance discipline while deciding how to pursue longer M1 history suitable for event-driven validation.

This document does not approve strategy validation, live trading, HistData validation, or derived-data generation.

## Current Accepted References

### Accepted H4 reference for broker-aligned diagnostics

Broker-native H4 is accepted as the reference H4 signal timeframe for broker-aligned diagnostics only.

Reason:

- Broker-native H4 was inspected and classified as H4-spaced.
- Broker-native H4 aligned exactly with broker-native M1 aggregation on all fully covered short-window 2026 overlap windows tested.
- Broker-native H4 is therefore the current best available reference for broker-aligned signal-timeframe diagnostics.

This does not mean H017 is validated.

### Accepted M1 source for broker-only diagnostics

Broker-native M1 is accepted for broker-only short-window diagnostics only.

Reason:

- Broker-native M1 aligned with broker-native H4 over the available fully covered windows.
- The available broker-native M1 export is too short for long research validation.

### Accepted long-history M1 validation source

None.

### Accepted H017 validation source

None.

## HistData Status

HistData remains rejected for H017 validation under current evidence.

HistData is not accepted as a research source.

HistData raw files may remain available for diagnostic reference only.

The broker H4 plus HistData M1 hybrid remains not accepted.

HistData-built H4 remains not accepted.

Derived HistData files are not authorized.

H017 must not be run on HistData.

## Why The Current State Is Blocked

H017 remains alive but not promotable.

The event-driven pipeline smoke result showed that the infrastructure can run, but the available broker-native M1 history is too short for research-grade validation.

The current blockers are:

1. No accepted long-history M1 validation source.
2. Broker-native M1 history is internally aligned but too short.
3. HistData has unresolved source-acceptance problems.
4. HistData session behavior and broker session behavior remain materially mismatched.
5. March-July 2023 HistData coverage is materially abnormal for both USDJPY and XAUUSD.
6. Broker-native H4 is accepted only as a broker-aligned diagnostic reference, not as proof of long-history M1 sufficiency.
7. The short 2026 broker window cannot prove 2021-2025 broker-equivalent behavior.

## Practical Acquisition Options

The preferred next data path is to pursue longer broker-native or broker-equivalent M1 data.

The practical options are listed below in order of epistemic preference.

### Option 1: Attempt deeper MT5 broker-native history export

Description:

Try to acquire more M1 history directly from the current broker through MetaTrader 5, broker history settings, symbol history downloads, or repeated export attempts.

Benefits:

- Highest broker-session relevance.
- Best chance of matching the broker-native H4 reference.
- Avoids vendor-session mismatch if sufficient history is available.

Risks:

- The broker may not provide enough M1 history.
- Download depth may vary by terminal, symbol, account type, server, or broker policy.
- The resulting data still requires raw inventory and coverage diagnostics.

Acceptance implication:

Even if longer broker-native M1 is acquired, it must still pass formal source-acceptance diagnostics before H017 validation.

### Option 2: Ask broker support about M1 history availability

Description:

Contact broker support and ask whether longer historical M1 data is available for USDJPY and XAUUSD on the same server or account environment used for trading.

Questions to ask:

1. How many years of M1 history are available for USDJPY and XAUUSD?
2. Is the history server-specific?
3. Is the historical data the same data used by the trading server?
4. What timezone is used by exported bars?
5. Are daylight-saving-time transitions documented?
6. Are XAUUSD daily breaks documented?
7. Are historical corrections or backfills applied?
8. Can historical M1 data be exported in bulk?
9. Are there licensing or redistribution restrictions?
10. Are bid, ask, or midpoint bars provided?

Benefits:

- May reveal whether the current broker can supply sufficient data.
- Helps document source lineage and session rules.
- Can clarify whether MT5 export limits are technical or policy-based.

Risks:

- Support answers may be incomplete or informal.
- Written documentation may not be available.
- Even broker-provided data must still be tested.

Acceptance implication:

Broker support statements are useful evidence, but not a substitute for empirical coverage, duplicate, session, and H4/M1 compatibility checks.

### Option 3: Consider broker-equivalent external M1 data only with strict evidence

Description:

Consider a non-broker M1 data source only if its licensing, timestamp convention, session behavior, symbol definitions, and compatibility with broker-native H4 can be documented and tested.

Benefits:

- May provide the long history needed for event-driven validation.
- Could unblock research if it is demonstrably broker-equivalent enough for the intended validation use.

Risks:

- External data may use different sessions.
- External data may use different liquidity, quote construction, spreads, holidays, or XAUUSD breaks.
- Vendor M1 data may not reproduce broker H4 bars.
- Vendor quality problems may be subtle and strategy-impacting.

Acceptance implication:

No external M1 source should be used for H017 validation unless it passes the full source-acceptance gate.

### Option 4: Pause long event-driven validation until better data exists

Description:

Do not force validation on weak data. Keep H017 as a non-promotable pipeline smoke result and pause long event-driven validation until a better source is available.

Benefits:

- Avoids false confidence.
- Preserves research integrity.
- Prevents tuning to vendor quirks or short-window artifacts.
- Prevents converting a data problem into a strategy-selection error.

Risks:

- Slows progress.
- Leaves H017 unresolved.
- Requires patience and disciplined refusal to overfit.

Acceptance implication:

This is preferable to validating H017 on rejected or unaccepted data.

## Required Acceptance Gates For Any Future M1 Source

Any future long-history M1 source must pass these gates before it can be used for H017 validation.

### Gate 1: Raw inventory

Required evidence:

- Exact file paths.
- File sizes.
- SHA-256 hashes.
- Line counts.
- First observed data row.
- Last observed data row.
- Symbol names.
- Date ranges.
- Whether files are raw original exports or transformed copies.

Rule:

Raw files must remain unmodified and must not be committed.

### Gate 2: Parser or loader validation

Required evidence:

- Explicit loader or parser.
- Timestamp parsing rules.
- Timezone parameter.
- Column mapping.
- OHLCV type conversion.
- UTC normalization.
- Tests for expected format.
- Tests for malformed rows.

Rule:

Do not reuse a loader built for another vendor unless the format and semantics are explicitly compatible.

### Gate 3: Timezone and session documentation

Required evidence:

- Source timezone.
- DST handling.
- Sunday open behavior.
- Friday close behavior.
- Daily breaks, especially for XAUUSD.
- Holiday behavior if available.
- Whether bars represent bid, ask, midpoint, or another construction.

Rule:

Timezone and session assumptions must be explicit. Silent assumptions are not allowed.

### Gate 4: Duplicate policy

Required evidence:

- Duplicate timestamp count.
- Duplicate rows inside duplicate groups.
- Conflicting duplicate timestamp groups.
- Exact duplicate timestamp groups.
- Documented policy for rejection or explicit opt-in removal.

Rule:

Silent deduplication is not allowed.

### Gate 5: Coverage analysis

Required evidence:

- Missing minutes inside symbol range.
- Missingness by year.
- Missingness by month.
- Missingness by hour.
- Cross-symbol common window.
- Cross-symbol overlapping observed minutes.
- Identification of abnormal periods.
- Same-month control comparisons for suspicious gaps.

Rule:

Material anomalies must be documented and explained before source acceptance.

### Gate 6: Broker H4 boundary compatibility

Required evidence:

- Comparison between source M1 timestamps and broker-native H4 boundaries.
- Ability to construct complete M1 windows for broker H4 intervals.
- Identification of incomplete H4 windows.
- DST and session-boundary behavior around broker H4 timestamps.

Rule:

A long M1 source must be compatible with the broker-native H4 signal reference if it is to support broker-aligned event-driven validation.

### Gate 7: Broker H4/M1 aggregation compatibility where overlap exists

Required evidence:

Where the candidate M1 source overlaps broker-native H4:

- Aggregate M1 into H4 windows.
- Compare open, high, low, close, and volume if available.
- Count matched bars.
- Count mismatched bars.
- Document mismatch examples.
- Classify compatibility.

Rule:

Exact or explainably near-exact compatibility is required before treating the source as broker-equivalent for stop-resolution research.

### Gate 8: Event-driven stop-resolution suitability

Required evidence:

- M1 OHLC availability.
- Continuous enough M1 windows to resolve stops.
- No systematic missingness during active trading periods.
- No unexplained symbol-specific gaps that would distort stop or take-profit fills.
- Conservative same-minute stop-first policy remains applicable.

Rule:

The source must be suitable for M1-in-H4 stop-resolution. H4-only validation is not sufficient.

### Gate 9: No silent data repair

Required evidence:

- Any filtering must be explicitly planned.
- Any dropped rows must be counted.
- Any rejected rows must be counted.
- Any derived data must be separately authorized.
- Any source acceptance decision must be documented.

Rule:

No silent repair, no silent imputation, no silent deduplication, and no undocumented transformations.

## Explicit Non-Approvals

This checkpoint does not approve:

1. H017 validation.
2. H017 validation on HistData.
3. HistData as a research source.
4. HistData-built H4.
5. Broker H4 plus HistData M1 hybrid validation.
6. Derived HistData datasets.
7. Derived production datasets.
8. Strategy tuning.
9. Cost model changes.
10. New symbols.
11. Machine learning.
12. Phase 4 execution work.
13. Live trading.

## Decision

The next preferred path is to pursue longer broker-native M1 history first.

If longer broker-native M1 cannot be acquired, a broker-equivalent external M1 source may be considered only after a formal source-acceptance plan.

If no acceptable source is available, long event-driven validation should remain paused rather than using rejected or weak data.

## Current Final State

Accepted H4 reference for broker-aligned diagnostics:

- Broker-native H4.

Accepted M1 source for broker-only short-window diagnostics:

- Broker-native M1.

Accepted long-history M1 validation source:

- None.

Accepted H017 validation source:

- None.

HistData status:

- Rejected for H017 validation under current evidence.
- Not accepted as a research source.
- Diagnostic-reference only.

H017 status:

- Alive.
- Not promotable.
- Not ready for live trading.

Research validation status:

- Blocked pending acceptable long-history M1 data.
