# Broker-Native M1 Acquisition Action Plan

Phase: 3.26-z  
Status: action plan only  
Date: 2026-05-03

## Purpose

This document converts the long broker-native M1 acquisition options checkpoint into a practical action plan.

The goal is to pursue longer broker-native or broker-equivalent M1 history without weakening the project's source-acceptance discipline.

This document does not approve H017 validation, HistData validation, live trading, strategy tuning, source acceptance, or derived-data generation.

## Current State

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

## Non-Negotiable Boundaries

Do not:

1. Run H017 on HistData.
2. Run H017 on any newly acquired source before acceptance.
3. Treat longer data as accepted merely because it is longer.
4. Modify raw data files.
5. Commit raw data files.
6. Write derived datasets during acquisition.
7. Build derived H4 from an unaccepted source for H017 validation.
8. Combine broker H4 with unaccepted external M1 for validation.
9. Tune H017 to short-window or vendor-specific behavior.
10. Start Phase 4 execution work.
11. Start live trading.

## Acquisition Priority

The preferred acquisition order is:

1. Current broker-native M1 from MT5 or broker infrastructure.
2. Broker-provided historical M1 export for the same trading server or account environment.
3. Broker-equivalent external source only if lineage, licensing, timezone, sessions, and compatibility can be documented.
4. Pause validation if no acceptable source exists.

## Action Path A: Attempt Deeper MT5 Broker-Native M1 Export

### Objective

Try to obtain more M1 history for:

- USDJPY
- XAUUSD

from the current broker's MT5 environment.

### Manual MT5 Checklist

Before exporting:

1. Confirm the terminal is connected to the intended broker account.
2. Confirm the symbols are the same symbols intended for eventual execution.
3. Confirm the chart symbol names, including any broker suffix or prefix.
4. Confirm M1 timeframe is selected.
5. Increase maximum bars settings if available in MT5.
6. Restart MT5 after changing history or chart bar settings if needed.
7. Scroll back on M1 charts to force historical loading if needed.
8. Use any available History Center or symbol history download function if supported.
9. Repeat for both USDJPY and XAUUSD.
10. Export raw CSVs without editing them.

### Required Notes During Export

Record manually:

1. Broker name.
2. Account server name.
3. Account type if visible.
4. Symbol exact names.
5. Export date.
6. MT5 terminal build if easily visible.
7. Whether the terminal was connected during export.
8. Earliest visible M1 timestamp before export.
9. Latest visible M1 timestamp before export.
10. Export method used.
11. Any warnings, missing-history messages, or unusual behavior.

### Raw File Handling

If new files are exported:

1. Place them under the gitignored root data folder.
2. Do not modify the exported files.
3. Do not open and resave them in Excel.
4. Do not manually delete rows.
5. Do not manually rename columns.
6. Do not commit them.
7. Do not write derived copies yet.

Suggested location pattern, subject to a future explicit import phase:

- data/raw/broker_native_candidate/YYYYMMDD/USDJPY/M1.csv
- data/raw/broker_native_candidate/YYYYMMDD/XAUUSD/M1.csv

This document does not authorize writing those files through scripts. It only describes a possible manual storage convention if acquisition succeeds.

## Action Path B: Ask Broker Support About Longer M1 History

### Objective

Get written clarification about whether longer broker-native M1 history is available for the relevant trading environment.

### Broker Support Message Template

Subject:

Historical M1 data availability for USDJPY and XAUUSD on my MT5 server

Message:

Hello,

I am trying to understand the historical minute-bar data available for my MT5 account.

Could you please clarify the following for the exact server and account environment used by my account?

1. How many years of M1 history are available for USDJPY?
2. How many years of M1 history are available for XAUUSD?
3. Is the available historical data server-specific?
4. Is the historical M1 data the same data used by the trading server?
5. What timezone is used for MT5 bar timestamps on this server?
6. How are daylight-saving-time transitions handled?
7. What are the normal Sunday open and Friday close times for USDJPY?
8. What are the normal Sunday open and Friday close times for XAUUSD?
9. Does XAUUSD have a daily trading break? If yes, what are the exact server-time and UTC times?
10. Are historical bars bid, ask, midpoint, or another construction?
11. Are spread changes reflected in historical bars?
12. Are commissions reflected anywhere in exported historical data, or only in account execution records?
13. Are historical corrections or backfills applied after the fact?
14. Can M1 history be exported in bulk for 2021 through 2025?
15. Are there any licensing restrictions on using the exported data for private research?
16. Are there symbol suffixes, contract changes, or server migrations that affect historical continuity for USDJPY or XAUUSD?

I am not asking for trading advice. I only need documentation about the historical data available through my account.

Thank you.

### Required Handling Of Broker Reply

If broker support replies:

1. Save the text of the reply outside the repo or in a planned documentation phase.
2. Do not treat the reply as source acceptance by itself.
3. Compare the reply against actual exported data.
4. Record contradictions explicitly.
5. Prefer written broker documentation over informal chat claims when available.

## Action Path C: Evaluate External Broker-Equivalent Sources Only After Broker Path

### Objective

If broker-native history is unavailable or too short, consider external M1 data only under strict source-acceptance controls.

### Minimum Questions For External Sources

Before downloading or buying external data, answer:

1. What exact instrument is provided?
2. Is the data bid, ask, midpoint, trade, or synthetic?
3. What timezone are timestamps in?
4. Are timestamps DST-adjusted?
5. What are Sunday open and Friday close rules?
6. What are XAUUSD daily break rules?
7. Are holidays documented?
8. Is volume tick volume, real volume, or zero-filled?
9. Are duplicate timestamps possible?
10. Are historical corrections applied?
11. Are raw files immutable after download?
12. Is the license compatible with private research?
13. Can raw inventory be preserved?
14. Is there overlap with broker-native H4 and broker-native M1 for compatibility checks?
15. Can M1 aggregate into broker-native H4 boundaries during overlap?

### External Source Warning

A long external M1 history is not automatically better than a short broker-native history.

A longer source with incompatible sessions, unexplained gaps, or mismatched H4 aggregation can create false validation confidence.

## Acceptance Gates Before Any Future H017 Validation

No future M1 source may be used for H017 validation until these gates are complete and documented.

### Gate 1: Raw Inventory

Required:

- File paths.
- File sizes.
- SHA-256 hashes.
- Line counts.
- First observed data row.
- Last observed data row.
- Symbol names.
- Date ranges.
- Raw export method.
- Confirmation that raw files were not modified.

### Gate 2: Loader Or Parser Validation

Required:

- Explicit parser or loader.
- Timestamp format.
- Timezone handling.
- Column mapping.
- OHLCV conversion.
- UTC normalization.
- Malformed-row tests.
- Real-file smoke test.

### Gate 3: Timezone And Session Evidence

Required:

- Source timezone.
- DST behavior.
- Sunday open.
- Friday close.
- XAUUSD daily break.
- Holiday behavior if known.
- Bid, ask, midpoint, or other bar construction.

### Gate 4: Duplicate Policy

Required:

- Duplicate timestamp count.
- Conflicting duplicate group count.
- Exact duplicate group count.
- Policy decision.
- Tests around policy behavior.

Silent deduplication is forbidden.

### Gate 5: Coverage Analysis

Required:

- Missing minutes by symbol.
- Missingness by year.
- Missingness by month.
- Missingness by hour.
- Cross-symbol common window.
- Overlapping observed minutes.
- Abnormal-period identification.

### Gate 6: Broker H4 Boundary Compatibility

Required:

- Candidate M1 coverage around broker H4 timestamps.
- Complete M1 windows for broker H4 intervals.
- Incomplete-window counts.
- DST/session-boundary analysis.

### Gate 7: Broker H4/M1 Aggregation Compatibility

Required where overlap exists:

- Aggregate M1 into broker H4 windows.
- Compare open, high, low, close, and volume where meaningful.
- Count matches.
- Count mismatches.
- Inspect mismatch examples.
- Classify compatibility.

### Gate 8: Event-Driven Stop-Resolution Suitability

Required:

- M1 OHLC availability.
- Sufficient coverage inside H4 holding windows.
- No unexplained active-session gaps.
- No symbol-specific missingness likely to distort stops.
- Conservative same-minute stop-first rule remains applicable.

### Gate 9: Explicit Acceptance Decision

Required:

- Written checkpoint.
- Clear accepted or rejected status.
- Clear allowed uses.
- Clear forbidden uses.
- No implicit promotion from diagnostic source to validation source.

## If Acquisition Succeeds

If longer broker-native or candidate M1 data is acquired, the next phase should be a read-only raw inventory phase.

That phase should not run H017.

That phase should not write derived data.

That phase should only document:

1. Paths.
2. Sizes.
3. Hashes.
4. Line counts.
5. First rows.
6. Last rows.
7. Symbol coverage.
8. Whether the files are raw original exports.

## If Acquisition Fails

If longer broker-native M1 cannot be acquired and no acceptable broker-equivalent source is available, the correct decision is to keep H017 blocked.

A blocked strategy with honest epistemology is preferable to a promoted strategy validated on unaccepted data.

## Current Decision

Proceed with acquisition attempts in this order:

1. Try deeper MT5 broker-native export.
2. Ask broker support for written data availability and session details.
3. Only then consider external broker-equivalent sources.
4. Pause validation rather than using rejected or weak data.

## Explicit Non-Approval

This action plan does not approve:

1. H017 validation.
2. H017 validation on HistData.
3. H017 validation on any newly acquired data.
4. HistData as a research source.
5. External M1 as a research source.
6. Broker H4 plus external M1 hybrid validation.
7. Derived H4 construction.
8. Derived dataset writing.
9. Strategy tuning.
10. Cost model changes.
11. New instruments.
12. Machine learning.
13. Phase 4 execution.
14. Live trading.
