# H4 Construction Decision Plan

Phase: 3.26-q

Status: Plan only

Purpose: Define the decision framework for constructing or selecting H4 bars for future research validation.

This document does not accept HistData as a research source.

This document does not reject HistData permanently.

This document does not build H4 bars.

This document does not write derived data.

This document does not run H017.

This document does not authorize H017 validation on HistData.

## 1. Current Decision State

HistData remains not accepted as a research source.

H017 remains alive but not promotable.

The broker mismatch assessment concluded that HistData remains blocked for H017 validation under current evidence.

Current allowed HistData use:

    Exploratory diagnostics only.

Current blocked HistData uses:

1. H017 research validation.
2. Promotability claims.
3. Broker-equivalent H4 signal construction.
4. Broker-equivalent M1 stop-resolution.
5. Hybrid broker-H4 plus HistData-M1 validation.
6. Final performance claims.
7. Live-trading justification.

This plan addresses the next blocker:

    H4 construction decision.

## 2. Why H4 Construction Matters

H017 is an H4 strategy.

The strategy uses H4 bars for:

1. Donchian breakout signals.
2. ATR calculation.
3. Chandelier exits.
4. Close-to-close returns.
5. Realized volatility estimates.
6. Portfolio heat-governor inputs.
7. Entry timing.
8. Exit timing.

If H4 bars differ, the strategy can differ.

Differences may appear in:

1. Bar timestamps.
2. Bar open prices.
3. Bar highs.
4. Bar lows.
5. Bar closes.
6. Missing bars.
7. Extra bars.
8. Weekly open partial bars.
9. Friday close partial bars.
10. Holiday bars.
11. DST transition bars.
12. XAUUSD daily-break-adjacent bars.

Therefore, H4 construction is not a formatting detail.

It is a strategy-definition decision.

## 3. Existing Source Context

### 3.1 Broker H4 Context

Broker-native H4 exports exist locally under:

    C:\Users\equin\Documents\institutional-ea\data\raw

These files are raw data.

They are gitignored.

They must not be committed.

Broker timezone:

    Europe/Athens

Broker timezone interpretation:

1. Winter: UTC+2.
2. Summer: UTC+3.
3. DST-aware.

MT5 loader API:

    load_mt5_csv(path, broker_tz="Europe/Athens")

Broker-native H4 bars are the closest currently available representation of what the execution broker displays.

However, broker-native H4 history is currently limited and does not solve the insufficient M1 history problem.

### 3.2 HistData M1 Context

HistData raw files are currently under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

This folder name is misleading because it contains HistData files as well as earlier Dukascopy samples.

The HistData files must not be renamed, modified, or committed during this phase.

HistData observed raw format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

Dedicated HistData loader:

    quantcore\data\histdata_loader.py

Official loader API:

    load_histdata_m1_csv(path, *, source_tz="UTC", duplicate_policy="reject")

Default duplicate policy:

    duplicate_policy="reject"

Explicit opt-in exact duplicate policy:

    duplicate_policy="drop_exact"

HistData remains blocked because source-session behavior, broker mismatch, March-July 2023 anomalies, holiday classification, and H4 construction are not yet resolved.

## 4. H4 Construction Options

The decision must consider at least four possible H4 construction options.

## 4.1 Option A - Use Broker-Native H4 For Signals Only

Definition:

Use broker-native H4 bars as the H017 signal source.

Use no HistData-built H4 bars for signal generation.

Potential advantages:

1. Closest representation of the broker chart.
2. Avoids guessing broker H4 boundaries from third-party M1 data.
3. Reduces risk of session-boundary mismatch.
4. Keeps signals aligned with the intended execution environment.

Potential disadvantages:

1. Broker-native H4 history may be too short.
2. Broker-native M1 history is currently too short for research-grade event validation.
3. H4 signals from broker data and M1 stop-resolution from another source would create a hybrid source if combined with HistData M1.
4. Hybrid-source validation requires separate approval.

Current status:

    Not accepted yet.

Reason:

    Broker-native H4 may be useful, but combining it with HistData M1 would require explicit hybrid-source rules and compatibility evidence.

## 4.2 Option B - Build H4 Bars From HistData M1

Definition:

Aggregate HistData M1 bars into H4 bars and use those H4 bars as the H017 signal source.

Potential advantages:

1. Same source supplies both H4 signals and M1 stop-resolution.
2. Avoids broker-H4 plus vendor-M1 source mixing.
3. Provides a longer sample if HistData is accepted.

Potential disadvantages:

1. HistData source sessions currently differ materially from broker short-window sessions.
2. H4 boundaries may not match broker-native H4 boundaries.
3. Weekly open and close bars may differ.
4. XAUUSD daily breaks may differ.
5. DST behavior may differ.
6. March-July 2023 anomaly remains unresolved.
7. Signals may not represent the broker execution environment.

Current status:

    Not accepted.

Reason:

    HistData is not accepted as a research source, and H4 boundaries are not proven broker-compatible.

## 4.3 Option C - Hybrid Broker H4 Signals Plus HistData M1 Stop-Resolution

Definition:

Use broker-native H4 bars for H017 signal generation, then use HistData M1 bars inside the corresponding H4 execution windows to resolve stops and take-profits.

Potential advantages:

1. Signals remain broker-chart aligned.
2. Longer HistData M1 may help test event-driven stop-resolution if compatible.
3. Avoids building H4 signals from a mismatched vendor session.

Potential disadvantages:

1. This creates a hybrid-source backtest.
2. HistData M1 may contain bars where the broker would not have traded.
3. HistData M1 may omit bars where the broker would have traded.
4. Timestamp alignment may be ambiguous around weekly opens, weekly closes, holidays, DST, and XAUUSD daily breaks.
5. False stop-outs or false take-profits may occur.
6. Validation claims may become epistemically weaker than a single-source broker-compatible test.

Current status:

    Not accepted.

Reason:

    Hybrid-source validation is not allowed without an explicit decision record and compatibility tests.

## 4.4 Option D - Reject HistData For H4 And M1 Validation

Definition:

Do not use HistData for H4 construction or M1 stop-resolution.

Continue searching for a better M1 source or more broker-native history.

Potential advantages:

1. Avoids false confidence from incompatible source data.
2. Preserves research integrity.
3. Prevents overfitting to vendor artifacts.
4. Avoids silent session mismatch.

Potential disadvantages:

1. Delays H017 validation.
2. Requires more data acquisition work.
3. May require another vendor or broker export path.
4. May leave H017 alive but blocked for longer.

Current status:

    Possible outcome, not yet final.

Reason:

    HistData has not been accepted, but the final source decision is not yet complete.

## 5. Required H4 Boundary Evidence

Before any H4 construction method is accepted, the project needs evidence comparing broker-native H4 bars with candidate M1-built H4 bars.

Required comparison dimensions:

1. Timestamp boundaries.
2. Open price match.
3. High price match.
4. Low price match.
5. Close price match.
6. Missing H4 bars.
7. Extra H4 bars.
8. Weekly open bars.
9. Friday close bars.
10. DST transition weeks.
11. Holiday weeks.
12. XAUUSD daily-break-adjacent bars.
13. Ordinary control weeks.
14. Cross-symbol timestamp alignment.
15. Effect on H017 indicators.

No such comparison is performed in this phase.

## 6. Required Decision Questions

The H4 construction decision must answer these questions before H017 validation can proceed.

### 6.1 Signal Source Question

Which source defines H017 H4 signals?

Possible answers:

1. Broker-native H4 only.
2. HistData-built H4 only.
3. Another accepted M1 source built into H4.
4. Hybrid design with explicit restrictions.
5. No acceptable source yet.

Current answer:

    No acceptable source yet.

### 6.2 Boundary Rule Question

If H4 bars are built from M1, what boundary rule is used?

Required details:

1. Timezone.
2. Session start.
3. H4 anchor hour.
4. Weekly open handling.
5. Weekly close handling.
6. Partial-bar handling.
7. Holiday handling.
8. DST handling.
9. Symbol-specific daily-break handling.

Current answer:

    Not decided.

### 6.3 Partial-Bar Question

How are partial H4 bars handled?

Examples:

1. Sunday open partial bars.
2. Friday close partial bars.
3. Holiday early-close partial bars.
4. XAUUSD daily-break-adjacent partial bars.
5. Broker maintenance partial bars.

Current answer:

    Not decided.

### 6.4 Missing-M1 Question

What happens if M1 bars are missing inside a candidate H4 bar?

Possible treatments:

1. Reject the H4 bar.
2. Mark the H4 bar incomplete.
3. Exclude affected windows.
4. Allow only if missingness is in known non-tradable intervals.
5. Reject the entire source if missingness is unexplained.

Current answer:

    Not decided.

### 6.5 Hybrid-Source Question

Can broker-native H4 bars be combined with HistData M1 bars?

Current answer:

    Not accepted.

Minimum requirements before this could be considered:

1. Explicit decision record.
2. Broker-H4 and HistData-M1 timestamp alignment rules.
3. Stop-resolution coverage checks.
4. Weekly open compatibility.
5. Weekly close compatibility.
6. XAUUSD daily-break compatibility.
7. Holiday compatibility.
8. DST compatibility.
9. Documented limitations.
10. No promotability claim unless validation remains statistically sufficient.

## 7. No-Lookahead Requirements

Any H4 construction decision must preserve existing no-lookahead rules.

Donchian breakout:

1. Long signal uses close at t greater than prior N-bar high.
2. Short signal uses close at t less than prior N-bar low.
3. Channel uses shifted prior bars only.

ATR:

1. Wilder RMA.
2. First true range is high minus low.
3. Seed at index window minus 1 with the simple mean of the first window true ranges.
4. Recurrence uses only prior ATR and current true range.

Realized volatility:

1. Uses returns through t-1 only.
2. For H4 bars, periods_per_year remains 1512 unless deliberately changed in a separate phase.
3. No current-bar return leakage.

Event bridge timing:

1. H017 decides at H4 timestamp t.
2. Trade opens on next H4 bar open t+1.
3. M1 bars inside [t+1, t+2) resolve stops.
4. If no stop is hit, exposure closes at t+2 open as signal_flip.
5. This bridge-layer simplification remains unchanged unless separately planned.

## 8. H4 Comparison Acceptance Criteria

Potential H4 construction cannot be accepted unless it passes documented criteria.

### 8.1 Required For Broker-Equivalent H4 Acceptance

Candidate H4 bars must show acceptable alignment with broker-native H4 bars across:

1. Ordinary weeks.
2. Weekly opens.
3. Weekly closes.
4. DST transitions.
5. Holidays.
6. XAUUSD daily-break-adjacent periods.
7. March-July 2023 anomaly windows if historical broker evidence exists.
8. Cross-symbol common timestamps.

### 8.2 Clearly Unacceptable Outcomes

H4 construction is unacceptable if:

1. H4 timestamps are offset from broker-native H4 bars.
2. Weekly open bars differ materially.
3. Friday close bars differ materially.
4. Candidate H4 highs or lows differ in ways that change ATR or chandelier exits.
5. Candidate H4 closes differ in ways that change Donchian signals.
6. Missing M1 data is silently aggregated into complete H4 bars.
7. Extra non-broker-tradeable M1 bars are aggregated into H4 bars.
8. DST duplicate handling changes H4 signals without documentation.
9. XAUUSD daily-break behavior is assumed rather than verified.
10. Hybrid source assumptions are hidden.

### 8.3 Conditional Acceptance Possibility

Conditional acceptance may be possible if:

1. Mismatches are isolated.
2. Mismatches are explainable.
3. Exclusion windows are explicit.
4. Sample size remains statistically sufficient.
5. H017 validation metrics remain meaningful.
6. All restrictions are documented before validation.

Conditional acceptance is not granted in this plan.

## 9. Implications For M1 Stop-Resolution

H4 construction and M1 stop-resolution are linked.

For each H4 decision timestamp, the event bridge needs M1 bars inside the next H4 execution window.

Therefore, H4 construction must define:

1. The exact start of the execution window.
2. The exact end of the execution window.
3. Whether both endpoints are inclusive or exclusive.
4. How missing M1 bars are handled.
5. Whether the interval was broker-tradeable.
6. How daily breaks are treated.
7. How weekend gaps are treated.
8. How holidays are treated.
9. How DST duplicate or missing hours are treated.

The existing conservative fill rule remains:

    If stop and take-profit are both touched in the same M1 bar, stop wins.

This rule handles intraminute ambiguity.

It does not solve source mismatch.

## 10. Required Future Work

A future implementation or diagnostic phase should not start by building full derived datasets.

It should first perform compact read-only comparisons.

Recommended future checks:

1. Inspect actual loader APIs with `inspect.signature`.
2. Inspect relevant result dataclass fields with `dataclasses.fields`.
3. Load broker-native H4 CSVs.
4. Load broker-native M1 CSVs if needed.
5. Load HistData M1 with explicit duplicate policy only if needed.
6. Build temporary in-memory candidate H4 bars for small windows only.
7. Compare broker H4 against candidate H4.
8. Report mismatches without writing derived files.
9. Document results before any source decision.
10. Commit and push the diagnostic document.

No code is written in this phase.

## 11. Current H4 Decision

Current decision:

    No H4 construction method is accepted yet.

Current status by option:

1. Broker-native H4 only:
   - Not accepted yet.
   - Candidate for broker-aligned signals.
   - Insufficient by itself for long event validation.

2. HistData-built H4:
   - Not accepted.
   - Blocked by source-session mismatch and source acceptance blockers.

3. Broker H4 plus HistData M1 hybrid:
   - Not accepted.
   - Requires separate decision record and compatibility evidence.

4. Reject HistData for H4 and M1 validation:
   - Possible future outcome.
   - Not final in this document.

## 12. Why H017 Remains Blocked

H017 remains blocked because:

1. Broker-native M1 history is too short.
2. HistData is not accepted as a research source.
3. Broker mismatch assessment found material current-session mismatch risk.
4. H4 construction rules are not decided.
5. M1 stop-resolution compatibility is not proven.
6. Holiday and special-closure classification is incomplete.
7. March-July 2023 anomaly remains unresolved.
8. The existing short-window result failed the PSR threshold and MinTRL observed requirement.

Existing broker-native short-window result remains a pipeline smoke result only:

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

Interpretation:

1. The event pipeline works.
2. The broker-native M1 window is too short.
3. The positive short-window return is not validated edge.
4. The -33.65 percent drawdown remains a serious risk signal.
5. HistData cannot be used to bypass source acceptance and H4 construction blockers.

## 13. Recommended Next Phase

Recommended next phase:

    Phase 3.26-r - H4 construction evidence requirements

Purpose:

1. Define compact read-only diagnostics needed to compare broker-native H4 bars with candidate M1-built H4 bars.
2. Identify exact local files needed.
3. Define comparison windows.
4. Define output fields.
5. Avoid writing derived data.
6. Avoid running H017.
7. Keep HistData unaccepted.
8. Keep H4 construction undecided until evidence is documented.

## 14. Non-Actions In This Phase

This phase did not:

1. Accept HistData.
2. Reject HistData permanently.
3. Build H4 bars.
4. Write derived data.
5. Modify raw data.
6. Modify the HistData loader.
7. Modify the MT5 loader.
8. Modify duplicate handling.
9. Modify `.gitignore`.
10. Run H017.
11. Tune strategy parameters.
12. Change the cost model.
13. Broaden the symbol universe.
14. Add machine learning.
15. Start Phase 4 execution work.
