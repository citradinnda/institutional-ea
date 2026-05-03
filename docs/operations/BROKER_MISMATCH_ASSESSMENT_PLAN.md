# Broker Mismatch Assessment Plan

Phase: 3.26-o

Status: Plan only

Purpose: Define how to assess whether the HistData M1 source is compatible enough with the broker execution environment to support future research validation.

This document is intentionally documentation-first. It does not accept HistData, does not run H017, does not build H4 bars, and does not write derived data.

## 1. Current Decision State

HistData remains not accepted as a research source.

H017 remains alive but not promotable.

H017 must not be validated on HistData until the following blockers are resolved:

1. Loader validation is complete.
2. Raw-file provenance is documented.
3. Duplicate handling policy is explicit.
4. Coverage and session diagnostics are complete.
5. The March-July 2023 anomaly is classified.
6. HistData source sessions are reconciled.
7. Broker mismatch assessment is complete.
8. H4 construction rules are decided.
9. A final HistData acceptance or rejection decision is documented.

This plan addresses blocker 7 only: broker mismatch assessment.

## 2. Inputs Already Available

### 2.1 HistData Inputs

HistData files are local raw CSV files under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

This folder name is misleading because it contains HistData files as well as earlier Dukascopy samples.

The HistData files must not be renamed, modified, or committed during this phase.

Current HistData files:

1. USDJPY:
   - File: USDJPY_2021_2025_Raw_HistData.csv
   - Range observed: 2021-01-03 through 2025-12-31
   - Format: YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

2. XAUUSD:
   - File: XAUUSD_2021_2025_Raw_HistData.csv
   - Range observed: 2021-01-03 through 2025-12-31
   - Format: YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

The dedicated HistData loader is:

    quantcore\data\histdata_loader.py

The official HistData loader API is:

    load_histdata_m1_csv(path, *, source_tz="UTC", duplicate_policy="reject")

The default duplicate policy remains strict:

    duplicate_policy="reject"

Explicit opt-in exact duplicate removal is available:

    duplicate_policy="drop_exact"

### 2.2 Broker Inputs

Broker-native MT5 CSV exports are local raw files under:

    C:\Users\equin\Documents\institutional-ea\data\raw

These files must not be modified or committed.

Broker timezone:

    Europe/Athens

Meaning:

1. Winter: UTC+2
2. Summer: UTC+3
3. DST-aware

The MT5 loader API is:

    load_mt5_csv(path, broker_tz="Europe/Athens")

The broker short-window diagnostic used local CSV exports only.

MT5 was not connected.

H017 was not run.

HistData was not accepted.

## 3. Known Broker Short-Window Evidence

The broker short-window evidence is from 2026 only.

It is useful for session inference but insufficient for historical research validation.

It must not be used to infer complete broker behavior across 2021-2025.

### 3.1 USDJPY Broker Evidence

Observed broker-native USDJPY M1 range:

- Earliest UTC: 2026-01-26 03:09:00+00:00
- Latest UTC: 2026-04-30 07:00:00+00:00
- Bars: 97,907
- Missing minutes inside symbol range: 37,685

Observed Sunday open clusters:

- 20:05 UTC
- 19:05 UTC
- 18:05 UTC

Observed Friday close clusters:

- 19:58 UTC
- 18:58 UTC
- 17:58 UTC

### 3.2 XAUUSD Broker Evidence

Observed broker-native XAUUSD M1 range:

- Earliest UTC: 2026-01-20 02:22:00+00:00
- Latest UTC: 2026-04-30 07:00:00+00:00
- Bars: 97,966
- Missing minutes inside symbol range: 46,313

Observed Sunday open clusters:

- 21:01 UTC
- 20:01 UTC
- 19:01 UTC

Observed Friday close clusters:

- 19:57 UTC
- 18:57 UTC
- 17:57 UTC

Additional XAUUSD-only missingness relative to USDJPY:

- XAUUSD-only missing common minutes: 5,496
- Main UTC-hour clusters: 18, 19, 20

### 3.3 Broker Common Window

Broker common window:

- Common start UTC: 2026-01-26 03:09:00+00:00
- Common end UTC: 2026-04-30 07:00:00+00:00
- Common full minutes: 135,592
- USDJPY observed common minutes: 97,907
- XAUUSD observed common minutes: 92,411
- Overlapping observed common minutes: 92,411
- USDJPY missing common minutes: 37,685
- XAUUSD missing common minutes: 43,181
- Overlapping missing common minutes: 37,685
- USDJPY-only missing common minutes: 0
- XAUUSD-only missing common minutes: 5,496
- USDJPY common observed percent: 72.207062
- XAUUSD common observed percent: 68.153726
- Overlapping observed percent of common full minutes: 68.153726

## 4. Known HistData Source-Session Evidence

### 4.1 USDJPY HistData Source Session Candidates

USDJPY HistData source-session candidates:

1. Sunday opens are mostly around 17:00 UTC.
2. Some Sunday open variants appear around 16:00, 18:00, and 19:00 UTC.
3. Friday closes are mostly around 16:59 UTC.
4. Recurring Friday early-close-like observations appear around 15:59 UTC.
5. 2023 has abnormal 14:59 and 15:59 UTC Friday closes.
6. 2023 Sunday opens are more dispersed than other years.

### 4.2 XAUUSD HistData Source Session Candidates

XAUUSD HistData source-session candidates:

1. Sunday opens are mostly around 18:00 UTC.
2. Some Sunday open variants appear around 17:00, 19:00, and 20:00 UTC.
3. Friday closes are mostly around 16:59 UTC.
4. Early-close-like Friday outliers are present.
5. A strong recurring full missing-hour signature appears around 17:00 UTC.

XAUUSD 17:00 UTC full missing-hour counts:

- 2021: 143
- 2022: 143
- 2023: 147
- 2024: 139
- 2025: 138

The XAUUSD 17:00 UTC break is not accepted as broker-equivalent behavior yet.

USDJPY must not inherit XAUUSD metals-session assumptions.

## 5. Core Assessment Question

The core question is:

Can HistData M1 bars be used to approximate the broker execution environment closely enough for H017 research validation?

This question must be answered separately for:

1. H4 signal construction.
2. M1 stop-resolution inside H4 bars.
3. Cross-symbol portfolio alignment.
4. Cost and slippage realism.
5. Holiday and special-closure handling.

A source can be unsuitable for one purpose while still being useful for another.

Example:

HistData might be rejected for H4 signal construction but retained for exploratory M1 stop-resolution diagnostics.

That outcome must be explicitly documented. It must not happen silently.

## 6. Mismatch Categories

The broker mismatch assessment must evaluate at least the following categories.

### 6.1 Weekly Open Mismatch

Definition:

Difference between the first observed trading minute after the weekend in HistData and the first observed trading minute after the weekend in broker-native data.

Known issue:

HistData USDJPY Sunday opens are mostly around 17:00 UTC, while the 2026 broker short window shows USDJPY Sunday open clusters around 18:05, 19:05, and 20:05 UTC.

HistData XAUUSD Sunday opens are mostly around 18:00 UTC, while the 2026 broker short window shows XAUUSD Sunday open clusters around 19:01, 20:01, and 21:01 UTC.

Why this matters:

1. H4 bar construction depends on session open.
2. First-week bars may differ materially.
3. Signals may appear or disappear.
4. Stops may be resolvable in one source but absent in another.

### 6.2 Weekly Close Mismatch

Definition:

Difference between the final observed trading minute before the weekend in HistData and the final observed trading minute before the weekend in broker-native data.

Known issue:

HistData Friday closes are mostly around 16:59 UTC, while the 2026 broker short window shows later Friday close clusters.

Why this matters:

1. Friday H4 bars may not align.
2. Weekend exposure assumptions may differ.
3. Signal-flip and forced-close behavior may differ.
4. Stop-resolution windows near Friday close may not be comparable.

### 6.3 Daily Break Mismatch

Definition:

Difference in recurring intraday missing periods between HistData and broker-native data.

Known issue:

HistData XAUUSD has a strong 17:00 UTC missing-hour signature.

Broker-native XAUUSD short-window data shows additional XAUUSD-only missingness clustered mainly around UTC hours 18, 19, and 20.

Why this matters:

1. Daily breaks create untradeable intervals.
2. Stop and take-profit touch detection can be distorted if the source has bars when the broker does not, or lacks bars when the broker has them.
3. XAUUSD daily breaks may differ materially between vendors and brokers.

### 6.4 DST and Session-Regime Mismatch

Definition:

Difference caused by daylight-saving-time transitions, timezone conversion, or session schedule regimes.

Known issue:

HistData exact duplicate timestamp blocks appear annually around late October:

- 2021-10-31 19:00 through 19:59
- 2022-10-30 19:00 through 19:59
- 2023-10-29 19:00 through 19:59
- 2024-10-27 19:00 through 19:59
- 2025-10-26 19:00 through 19:59

These duplicate blocks are consistent with a daylight-saving-time-related duplicate hour, but that is only an observation, not acceptance.

Why this matters:

1. DST can shift weekly opens and closes.
2. H4 bars can be offset by one hour.
3. Duplicate timestamps can create ambiguous execution paths.
4. A source that represents DST differently from the broker may not be valid for broker-specific validation.

### 6.5 Symbol-Specific Missingness Mismatch

Definition:

Difference in missing-minute behavior between USDJPY and XAUUSD within the same source, and difference between each source and broker behavior.

Known issue:

Broker-native XAUUSD has 5,496 XAUUSD-only missing common minutes relative to USDJPY in the 2026 common window.

Why this matters:

1. Portfolio heat depends on simultaneous symbol observations.
2. Inner joins can silently discard periods.
3. Symbol-specific missingness may create false diversification evidence.
4. XAUUSD often has different session behavior from FX symbols.

### 6.6 Cross-Symbol Alignment Mismatch

Definition:

Difference in the set of timestamps where both USDJPY and XAUUSD are available.

Why this matters:

H017 uses a two-symbol portfolio and inner-joins USDJPY and XAUUSD timestamps.

If HistData and broker-native common timelines differ, the strategy may observe different returns, different volatility estimates, different heat-governor states, and different exposure timing.

### 6.7 H4 Boundary Mismatch

Definition:

Difference between H4 bars constructed from HistData M1 and H4 bars used by the broker.

Why this matters:

H017 signals are H4-based.

If H4 boundaries differ, then the following can differ:

1. Donchian breakout signals.
2. ATR values.
3. Chandelier exit values.
4. Realized volatility estimates.
5. Portfolio heat estimates.
6. Entry timing.
7. Exit timing.

This is a critical blocker because using HistData M1 for stop-resolution while using broker H4 for signals may create a hybrid source. That may be acceptable only if explicitly planned, tested, and documented.

### 6.8 Stop-Resolution M1 Coverage Mismatch

Definition:

Difference in M1 bar availability inside the H4 execution windows used to resolve stops and take-profits.

Why this matters:

Phase 3 event-driven backtesting uses M1 bars inside H4 intervals to resolve stop and take-profit touches.

If HistData has M1 bars during periods where the broker would not trade, it can create false fills.

If HistData lacks M1 bars during periods where the broker would trade, it can miss real stop-outs or profit-takes.

Same-minute stop and take-profit ambiguity remains governed by the existing conservative rule:

If stop and take-profit are both touched in the same M1 bar, stop wins.

### 6.9 Holiday and Special-Closure Mismatch

Definition:

Difference in holiday closures, early closes, late opens, and other special market schedules.

Known issue:

March-July 2023 contains material abnormalities for both symbols.

The zero-bar weekday candidate 2023-04-07 is provisionally classified as a holiday full-close candidate, not accepted yet.

Why this matters:

1. Holiday behavior can explain legitimate missingness.
2. Source outages can mimic holiday closures.
3. Incorrect classification can cause false rejection or false acceptance.
4. H017 validation must not treat source defects as market reality.

## 7. Acceptable Versus Unacceptable Mismatch Criteria

These criteria are provisional. They define what the assessment must decide, not the final outcome.

### 7.1 Clearly Acceptable Mismatches

A mismatch may be acceptable if all of the following are true:

1. It is small in duration.
2. It occurs in a known non-tradable interval.
3. It is consistent across years or explainable by a documented exchange or broker schedule.
4. It does not affect H4 signal bars.
5. It does not affect M1 stop-resolution windows.
6. It does not materially change cross-symbol alignment.
7. It is documented and reproducible.

Example candidate:

A documented metals daily break may be acceptable for XAUUSD if broker evidence confirms the same break behavior.

Current status:

This is not yet confirmed.

### 7.2 Conditionally Acceptable Mismatches

A mismatch may be conditionally acceptable if it can be handled with explicit exclusions or source-use restrictions.

Possible conditional treatments:

1. Exclude affected dates.
2. Exclude affected weekly open or close intervals.
3. Use HistData only for exploratory diagnostics.
4. Use HistData only for M1 stop-resolution after H4 boundaries are broker-aligned.
5. Use HistData only outside known anomalous periods.
6. Use HistData only for one symbol if the other is rejected.

Any conditional acceptance must include:

1. The affected timestamps.
2. The affected symbol or symbols.
3. The exact exclusion rule.
4. The reason for the exclusion.
5. The expected effect on sample size.
6. Whether PSR, MinTRL, and DSR remain meaningful after exclusions.

### 7.3 Unacceptable Mismatches

A mismatch is unacceptable if any of the following are true:

1. H4 signal bars are materially different from broker H4 bars.
2. Weekly opens or closes are offset enough to change tradeable H4 windows.
3. M1 stop-resolution windows contain bars that would not be tradable at the broker.
4. M1 stop-resolution windows omit bars that would be tradable at the broker.
5. Cross-symbol alignment materially differs from broker behavior.
6. Missingness is concentrated in abnormal source-outage patterns.
7. Holiday closures cannot be separated from vendor defects.
8. The March-July 2023 anomaly remains unexplained and materially affects validation.
9. The source requires undocumented manual cleaning.
10. The source requires silent assumptions about broker equivalence.

Under any unacceptable condition, HistData must not be used for H017 research validation.

## 8. How To Compare HistData 2021-2025 With Broker 2026 Without Overclaiming

The comparison must be explicit about time mismatch.

HistData covers 2021-2025.

Broker-native short-window evidence covers January-April 2026.

Therefore:

1. The broker evidence can identify current broker session behavior.
2. The broker evidence can reveal whether HistData is obviously inconsistent with the current broker.
3. The broker evidence cannot prove that broker sessions in 2021-2025 matched 2026.
4. The broker evidence cannot prove that HistData was broker-equivalent historically.
5. Any acceptance based only on this comparison must be conditional and conservative.

Required language:

- Allowed: "The 2026 broker short window suggests a current broker session mismatch."
- Not allowed: "HistData is historically incompatible with the broker for all of 2021-2025."
- Allowed: "The mismatch is an acceptance blocker until more evidence is collected."
- Not allowed: "The short broker window proves the historical session schedule."

## 9. Required Additional Evidence

The broker mismatch assessment should request or collect additional evidence before any final source decision.

### 9.1 MT5 Symbol Specification Evidence

Required if available:

1. Broker server timezone.
2. Symbol trading sessions for USDJPY.
3. Symbol trading sessions for XAUUSD.
4. Contract size.
5. Tick size.
6. Tick value.
7. Digits.
8. Spread behavior if available.
9. Swap and rollover schedule if relevant.
10. Any documented metals daily break.

This evidence should come from MT5 symbol specifications or broker documentation.

### 9.2 Additional Broker Exports

Additional exports should be requested if available:

1. More M1 history for USDJPY.
2. More M1 history for XAUUSD.
3. Broker H4 exports for the same symbols.
4. Exports around DST transition weeks.
5. Exports around known holidays.
6. Exports around March-July if historical broker data is available.
7. Exports around year-end and New Year.
8. Exports around Good Friday and Christmas.

Minimum useful additional windows:

1. A spring DST transition window.
2. An autumn DST transition window.
3. A Good Friday week.
4. A Christmas/New Year week.
5. Several ordinary control weeks.

### 9.3 Broker H4 Comparison Evidence

Before HistData can be used for H4 signal construction, constructed HistData H4 bars must be compared against broker-native H4 bars.

The comparison should include:

1. Timestamp boundaries.
2. Open.
3. High.
4. Low.
5. Close.
6. Missing bars.
7. Extra bars.
8. DST transition behavior.
9. Weekly open bars.
10. Weekly close bars.
11. Holiday bars.

No H4 construction decision is made in this plan.

## 10. Possible Outcomes

The broker mismatch assessment may produce one of the following outcomes.

### 10.1 Reject HistData

HistData should be rejected if mismatches are material, unexplained, or incompatible with broker execution.

Consequences:

1. Do not run H017 validation on HistData.
2. Continue searching for another M1 source.
3. Keep HistData only as a rejected-source diagnostic record.
4. Do not build production research around HistData.

### 10.2 Conditionally Accept HistData With Exclusions

HistData may be conditionally accepted only if all material mismatches can be isolated, explained, and excluded.

Consequences:

1. Define exact exclusion windows.
2. Recompute sample size after exclusions.
3. Reassess whether PSR, MinTRL, and DSR remain valid.
4. Document the exclusions before any H017 validation.
5. Prevent silent use of excluded windows.

### 10.3 Use HistData Only For M1 Stop-Resolution

HistData may be considered only for M1 stop-resolution if:

1. Broker H4 bars remain the signal source.
2. HistData M1 bars are proven compatible inside broker H4 execution windows.
3. Session mismatches are excluded or shown not to affect stop-resolution.
4. The hybrid-source design is explicitly approved in a decision record.

This is not currently accepted.

### 10.4 Use HistData Only For Exploratory Diagnostics

HistData may be useful only for diagnostics if it is too mismatched for validation but still informative.

Allowed exploratory uses may include:

1. Loader testing.
2. Coverage diagnostics.
3. Session anomaly studies.
4. Duplicate-policy testing.
5. Research tooling smoke tests.

Not allowed:

1. H017 validation.
2. Promotability claims.
3. Live-trading justification.
4. Final performance claims.

### 10.5 Continue Searching For Another M1 Source

If HistData cannot meet broker compatibility requirements, the correct outcome may be to search for a better M1 source.

Requirements for another source would include:

1. Clear provenance.
2. Transparent timezone.
3. Broker-compatible or reconstructable sessions.
4. Sufficient M1 depth.
5. Stable duplicate handling.
6. Verifiable coverage.
7. Acceptable licensing or usage terms.
8. Ability to support H4 construction and M1 stop-resolution.

## 11. Implications For H4 Construction

H4 construction is blocked until broker mismatch assessment is complete.

Open questions:

1. Should H4 bars be constructed from HistData M1?
2. Should broker-native H4 bars remain the signal source?
3. If using broker-native H4 and HistData M1, how are timestamps aligned?
4. How are weekly open partial bars handled?
5. How are Friday close partial bars handled?
6. How are XAUUSD daily breaks handled?
7. How are holidays and special closures handled?
8. How are DST transition weeks handled?

Any H4 construction rule must preserve the existing no-lookahead conventions:

1. Donchian channels use prior N bars only.
2. Vol targeting uses returns through t-1 only.
3. ATR uses the established Wilder RMA convention.
4. Event bridge timing opens trades on the next H4 bar open.

## 12. Implications For M1 Stop-Resolution

M1 stop-resolution is blocked until source compatibility is resolved.

Required checks before use:

1. Confirm M1 coverage inside every H4 execution window.
2. Detect missing M1 windows that could hide stop or take-profit touches.
3. Detect extra M1 windows that the broker would not have traded.
4. Confirm daily breaks.
5. Confirm weekly opens.
6. Confirm weekly closes.
7. Confirm holiday closures.
8. Confirm DST transition behavior.
9. Confirm cross-symbol alignment.
10. Preserve conservative same-minute stop-first handling.

## 13. Why H017 Remains Blocked

H017 remains blocked because the source data is not accepted.

Existing broker-native short-window event-driven result:

- Fills: 470
- Starting equity: 10000.00 USD
- Ending equity: 16145.60 USD
- Total return: 61.46 percent
- Max drawdown: -33.65 percent
- Annualized Sharpe: 1.3218

Existing claim result:

- PSR: 0.8662
- PSR threshold: 0.95
- MinTRL feasible: True
- MinTRL required n: 1034
- MinTRL observed n: 470
- DSR: Skipped
- H017 promotable: False

Operational verdict:

- Pipeline smoke passed: True
- Research validation sufficient: False

Interpretation:

1. The event pipeline works.
2. Broker-native M1 history is too short.
3. The short-window positive return is not validated edge.
4. The -33.65 percent drawdown is a serious risk signal.
5. H017 is alive but not promotable.
6. HistData cannot be used to unblock H017 until source acceptance is complete.

## 14. Phase 3.26-o Deliverable

This phase delivers only this broker mismatch assessment plan.

It does not:

1. Accept HistData.
2. Reject HistData.
3. Run H017.
4. Build H4 bars.
5. Write derived data.
6. Modify raw data.
7. Tune strategy parameters.
8. Change the cost model.
9. Change duplicate handling behavior.
10. Change `.gitignore`.

## 15. Recommended Next Phase

Recommended next phase after this plan:

    Phase 3.26-p - Broker mismatch assessment

Expected purpose:

1. Compare documented HistData source-session behavior against broker short-window behavior.
2. Identify material mismatches by category.
3. Separate current-broker evidence from historical claims.
4. Define additional evidence requirements.
5. Decide whether HistData remains a candidate source, is conditionally usable, or should be rejected.
6. Keep H017 blocked until a final source decision is documented.
