# HistData Holiday and Special-Closure Classification Plan

Status: plan only  
Phase: 3.26-i  
Source status after this plan: not accepted as a research source  
H017 status after this plan: not run, not promotable

## Purpose

This document defines the planned classification method for HistData missing-minute gaps before any future source-acceptance decision.

The immediate reason for this plan is the documented March-July 2023 HistData anomaly.

That anomaly showed materially abnormal coverage in both USDJPY and XAUUSD from:

- 2023-03-01 00:00 UTC through 2023-07-31 23:59 UTC

The anomaly was cross-symbol and not explainable by the provisional weekend rule alone.

Before HistData can be accepted as a research source, missing-minute gaps must be classified using explicit rules rather than informal judgment.

This plan is documentation only.

No raw files are modified.  
No derived files are written.  
H017 is not run.  
HistData is not accepted.

## Inputs Already Known

Raw HistData files currently inspected:

- C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv
- C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Important note:

The folder name `dukascopy_samples` is misleading. These two files are HistData files, not Dukascopy files.

Dedicated loader:

- quantcore.data.histdata_loader.load_histdata_m1_csv

Known loader signature:

- load_histdata_m1_csv(path: str | Path, *, source_tz: str = "UTC", duplicate_policy: DuplicatePolicy = "reject") -> HistDataM1LoadResult

Known duplicate policy:

- Default: duplicate_policy="reject"
- Explicit diagnostic opt-in: duplicate_policy="drop_exact"

The explicit `drop_exact` policy removes only exact duplicate OHLCV rows and rejects conflicting duplicate timestamp groups.

## Existing Evidence

Prior documents:

- docs/operations/HISTDATA_M1_ACQUISITION_INVENTORY.md
- docs/operations/HISTDATA_M1_LOADER_REAL_FILE_CHECK.md
- docs/operations/HISTDATA_M1_DROP_EXACT_REAL_FILE_CHECK.md
- docs/operations/HISTDATA_DERIVED_DATA_PROVENANCE_PLAN.md
- docs/operations/HISTDATA_M1_COVERAGE_SESSION_ANALYSIS_PLAN.md
- docs/operations/HISTDATA_M1_COVERAGE_SESSION_ANALYSIS.md
- docs/operations/HISTDATA_FOCUSED_2023_SESSION_BREAK_ANALYSIS.md
- docs/operations/HISTDATA_MARCH_JULY_2023_ANOMALY_INVESTIGATION.md

Key existing findings:

1. Both USDJPY and XAUUSD have exact duplicate timestamp groups around recurring late-October DST-related hours.
2. The dedicated HistData loader can load the files with explicit `duplicate_policy="drop_exact"`.
3. The loaded output is UTC, monotonic, duplicate-free, and structurally valid after exact duplicate removal.
4. Large naive missing-minute counts are mostly weekend or session related.
5. XAUUSD has a strong recurring 17:00 UTC break signature.
6. March-July 2023 is materially abnormal for both symbols.
7. The March-July 2023 issue is strongly cross-symbol.
8. The March-July 2023 issue is not explained by the provisional weekend rule alone.
9. HistData remains blocked pending holiday classification, source-session reconciliation, broker mismatch assessment, H4 construction decision, and final source acceptance or rejection.

## Classification Philosophy

The classification system must be conservative.

A missing gap should not be treated as acceptable merely because it resembles a holiday, early close, or session break.

Every accepted missingness category must have:

1. an explicit rule,
2. an auditable label,
3. a symbol scope,
4. a time window,
5. a reason code,
6. a confidence level,
7. a note about whether it is source-specific, market-specific, or broker-specific.

The goal is not to erase missingness.  
The goal is to classify missingness so that source-quality risk is visible.

## Planned Gap Categories

Each missing-minute gap should eventually receive one primary category.

### 1. Normal Weekend Closure

Definition:

A missing period that falls fully inside the provisional weekend closure window.

Current provisional rule:

- Friday 22:00 UTC through Sunday 21:59 UTC

Current status:

- Provisional only.
- Not yet final.
- Must be reconciled against source sessions and broker sessions.

Important caution:

A gap that touches the weekend boundary but starts early on Friday is not automatically a normal weekend closure.

### 2. Standard Daily Session Break

Definition:

A recurring daily break that appears consistently in the vendor data for a symbol.

Known candidate:

- XAUUSD recurring 17:00 UTC missingness.

Current status:

- Candidate only.
- Not yet accepted as broker-equivalent.
- Requires source-session reconciliation and broker mismatch assessment.

Important caution:

USDJPY should not inherit XAUUSD metals-session assumptions.

### 3. Holiday Full Closure

Definition:

A full or near-full weekday closure consistent with a known market holiday or global trading closure.

Known candidate from current evidence:

- 2023-04-07 showed zero observed weekday bars for both USDJPY and XAUUSD in the March-July 2023 focus diagnostic.

Current status:

- Candidate only.
- Requires explicit holiday classification.

Important caution:

A zero-bar weekday is not automatically acceptable. It must be classified.

### 4. Holiday Early Close

Definition:

A shortened trading day consistent with a known market holiday, special closure, or liquidity-provider schedule.

Observed candidates:

Many large March-July 2023 Friday gaps ended at:

- 21:59 UTC

Examples include gaps beginning around:

- 15:00 UTC
- 16:00 UTC
- 17:00 UTC

Current status:

- Candidate only.
- Requires explicit classification.

Important caution:

Repeated Friday early cutoffs may be a vendor session artifact rather than a true market closure.

### 5. Symbol-Specific Session Rule

Definition:

A gap that applies to one symbol but not the other because of instrument-specific trading hours.

Likely examples:

- Metals-specific XAUUSD breaks.
- Possible gold holiday or exchange-related closures.
- Possible FX-specific gaps that should not apply to metals.

Current status:

- Not yet formally classified.

Important caution:

The project trades both USDJPY and XAUUSD. Symbol-specific session rules must not be merged into one generic calendar without evidence.

### 6. Cross-Symbol Source Outage Candidate

Definition:

A missing period that overlaps heavily across USDJPY and XAUUSD and is not explained by weekend, holiday, early close, or known session rules.

Observed issue:

The March-July 2023 anomaly had high cross-symbol missing-minute overlap.

Current status:

- Major unresolved blocker.

Important caution:

Cross-symbol overlap may indicate a real shared closure, but it may also indicate a vendor data outage or vendor session-definition problem.

### 7. Symbol-Specific Source Defect Candidate

Definition:

A missing gap that affects one symbol and is not explained by that symbol's expected session, holiday, or market closure behavior.

Observed issue:

The March-July 2023 focus diagnostic showed substantial USDJPY-only and XAUUSD-only missing minutes even after measuring overlap.

Current status:

- Unresolved.

Important caution:

Symbol-specific missingness can distort cross-symbol portfolio simulation, especially when the strategy inner-joins timestamps.

### 8. DST Transition Artifact

Definition:

A gap or duplicate pattern plausibly caused by daylight-saving-time transition handling.

Known existing duplicate pattern:

Both symbols had exact duplicate timestamp groups around late October:

- 2021-10-31 19:00 through 19:59
- 2022-10-30 19:00 through 19:59
- 2023-10-29 19:00 through 19:59
- 2024-10-27 19:00 through 19:59
- 2025-10-26 19:00 through 19:59

Current status:

- Exact duplicate removal is implemented only through explicit opt-in `duplicate_policy="drop_exact"`.
- DST-related interpretation remains an observation, not source acceptance.

Important caution:

DST artifacts must remain auditable and must not be silently repaired.

### 9. Suspicious Unclassified Gap

Definition:

Any gap that does not fit an accepted category.

Current status:

- These gaps block source acceptance until reviewed or until a conservative policy is defined.

Important caution:

Unclassified gaps must remain visible. They must not be ignored.

## Planned Classification Fields

Future diagnostic output should classify gaps into records with fields similar to:

- symbol
- gap_start_utc
- gap_end_utc
- duration_minutes
- observed_before_utc
- observed_after_utc
- provisional_weekend_overlap_minutes
- category
- reason_code
- confidence
- cross_symbol_overlap_flag
- cross_symbol_overlap_minutes
- is_symbol_specific
- is_source_wide_candidate
- requires_manual_review
- notes

This is only a planned schema.  
No derived files are being written in this phase.

## Proposed Reason Codes

Candidate reason codes:

- NORMAL_WEEKEND_PROVISIONAL
- DAILY_SESSION_BREAK_CANDIDATE
- HOLIDAY_FULL_CLOSE_CANDIDATE
- HOLIDAY_EARLY_CLOSE_CANDIDATE
- SYMBOL_SESSION_RULE_CANDIDATE
- CROSS_SYMBOL_SOURCE_OUTAGE_CANDIDATE
- SYMBOL_SPECIFIC_SOURCE_DEFECT_CANDIDATE
- DST_TRANSITION_ARTIFACT_CANDIDATE
- SUSPICIOUS_UNCLASSIFIED_GAP

Reason codes ending in `_CANDIDATE` are not acceptance labels.

A candidate label means:

- the pattern resembles a known closure type,
- but the source remains unaccepted until reconciliation is complete.

## Confidence Levels

Future gap classification should use conservative confidence levels:

### High Confidence

Use only when a gap is fully explained by a documented rule already accepted for this project.

Current examples:

- None yet, except possibly provisional weekend closure for triage purposes.

### Medium Confidence

Use when a gap matches a strong recurring pattern but has not yet been reconciled against broker sessions.

Candidate examples:

- XAUUSD 17:00 UTC daily break.
- Repeated Friday early-close-like gaps ending at 21:59 UTC.

### Low Confidence

Use when a gap resembles a holiday or session effect but lacks explicit confirmation.

Candidate examples:

- one-off holiday-like gaps,
- symbol-specific partial closures,
- unusual low-bar weekdays.

### Unclassified

Use when no convincing rule exists.

Unclassified gaps should block source acceptance unless they are immaterial under a documented threshold.

No such threshold has been accepted yet.

## Planned Diagnostic Approach

The next read-only diagnostic should:

1. Load both HistData files with explicit `duplicate_policy="drop_exact"`.
2. Build full minute indexes for each symbol.
3. Build missing-minute indexes.
4. Group consecutive missing minutes into gaps.
5. Apply the provisional weekend rule.
6. Identify daily session-break candidates.
7. Identify full weekday zero-bar days.
8. Identify early-close candidates.
9. Identify cross-symbol overlapping missing gaps.
10. Identify symbol-only missing gaps.
11. Produce compact counts by category candidate.
12. Produce a list of unresolved suspicious gaps.
13. Confirm:
    - no raw files modified,
    - no derived files written,
    - H017 not run,
    - HistData not accepted.

## Specific Questions To Answer Next

The next diagnostic should answer:

1. How many March-July 2023 non-weekend missing minutes can be explained by repeated Friday early-close-like gaps?
2. How many can be explained by XAUUSD daily 17:00 UTC break candidates?
3. How many can be explained by full-holiday candidates such as 2023-04-07?
4. How many remain suspicious and unclassified?
5. Are the repeated Friday early-close-like gaps present in other years?
6. Are the repeated Friday early-close-like gaps equally present in both symbols?
7. Are these gaps source-wide or symbol-specific?
8. Do these gaps align with the future broker execution session that will be used by the MT5 EA?
9. Would using these data to construct H4 bars materially distort signal timing?
10. Would inner-joining USDJPY and XAUUSD timestamps hide or amplify the source defect?

## Acceptance Implications

HistData cannot be accepted if:

1. large non-weekend gaps remain unclassified,
2. March-July 2023 remains materially different from control periods without explanation,
3. source session rules cannot be reconciled with the broker execution environment,
4. H4 bars would be constructed from inconsistent or source-truncated M1 sessions,
5. cross-symbol missingness would distort portfolio-level H017 simulation,
6. symbol-specific missingness would cause biased inner joins,
7. suspicious gaps are silently ignored.

HistData may become conditionally usable only if:

1. missingness is mostly explainable by documented sessions, weekends, holidays, and early closes,
2. remaining suspicious gaps are small enough under a documented conservative threshold,
3. broker mismatch is explicitly assessed,
4. H4 construction rules are fixed before validation,
5. source limitations are recorded in a final decision document.

No such acceptance has occurred yet.

## Explicit Non-Goals

This phase does not:

1. write reusable classification code,
2. write derived data,
3. modify raw data,
4. repair gaps,
5. fill missing minutes,
6. interpolate prices,
7. resample to H4,
8. run H017,
9. tune H017,
10. accept HistData,
11. reject HistData permanently.

## Current Decision

HistData remains not accepted as a research source.

The next recommended sub-phase is:

Phase 3.26-j - Read-only candidate classification of March-July 2023 HistData gaps

That diagnostic should classify gap candidates under the rules in this plan while keeping all labels provisional.

## Safety Confirmation

- raw_files_modified: False
- derived_files_written: False
- H017_run: False
- HistData_accepted_as_research_source: False
- plan_only: True
