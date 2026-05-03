# H4 Construction Decision Checkpoint

Date created: 2026-05-03T22:51:43+09:00

## Purpose

This document records Phase 3.26-w: H4 construction decision checkpoint.

The purpose is to convert the recent broker H4/M1 evidence into a bounded operational decision without overreaching into HistData acceptance, H017 validation, or live-trading readiness.

## Decision summary

Broker-native H4 is accepted as the reference H4 signal timeframe for broker-aligned diagnostics.

This is a narrow decision.

It means:

1. Broker-native H4 files may be used as the H4 reference when checking broker-aligned data behavior.
2. Broker-native H4 files may be used as the signal-timeframe reference in future broker-only diagnostics.
3. Broker-native H4 files are internally consistent with broker-native M1 over the fully covered windows tested.
4. Broker-native H4 is currently preferred over HistData-built H4 for broker-alignment evidence.

It does not mean:

1. HistData is accepted as a research source.
2. HistData-built H4 is accepted.
3. A broker H4 plus HistData M1 hybrid is accepted.
4. H017 is validated.
5. H017 may be run on HistData for validation.
6. Any live-trading or production deployment is authorized.
7. The short 2026 broker M1 export is sufficient for long research validation.
8. The broker's 2021-2025 historical M1 behavior is proven by the 2026 short-window export.

## Evidence considered

### Broker H4/M1 loaded-shape inspection

Document:

`C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_LOADED_SHAPE_INSPECTION.md`

Commit:

`6a48870 Document broker H4 M1 loaded shape inspection`

Result:

1. USDJPY H4 was classified as H4-spaced.
2. XAUUSD H4 was classified as H4-spaced.
3. USDJPY H4 dominant timestamp delta was 4 hours.
4. XAUUSD H4 dominant timestamp delta was 4 hours.
5. The earlier raw-preview concern that files named H4.csv might be daily-like was resolved.
6. The M1 files were also confirmed to be primarily one-minute spaced.

Key numbers:

1. USDJPY H4 four-hour delta pct: 86.252441.
2. XAUUSD H4 four-hour delta pct: 86.173039.
3. USDJPY M1 one-minute delta pct: 99.911139.
4. XAUUSD M1 one-minute delta pct: 99.919359.

### Broker-only H4/M1 alignment diagnostic

Document:

`C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_DIAGNOSTIC.md`

Commit:

`3cdeaca Document broker H4 M1 alignment diagnostic`

Result:

1. Broker-native H4 bars aligned exactly with broker-native M1 aggregation on every fully covered H4 window tested.
2. No OHLCV mismatches were found in fully covered windows.
3. The diagnostic was broker-only and read-only.
4. HistData was not loaded.
5. H017 was not run.

Key numbers:

1. USDJPY compared full M1-covered H4 windows: 338.
2. USDJPY matched bars: 338.
3. USDJPY mismatched bars: 0.
4. USDJPY classification: aligned_on_all_full_m1_windows.
5. XAUUSD compared full M1-covered H4 windows: 354.
6. XAUUSD matched bars: 354.
7. XAUUSD mismatched bars: 0.
8. XAUUSD classification: aligned_on_all_full_m1_windows.

## Decision details

### Option 1: Broker-native H4 only

Status:

Accepted for broker-aligned diagnostics.

Rationale:

1. The broker H4 files are confirmed to be primarily H4-spaced.
2. Broker H4 OHLCV aligns exactly with broker M1 aggregation on all fully covered tested windows.
3. The broker H4 files provide the most direct available evidence of the broker's own signal timeframe.
4. This avoids silently building H4 from a source whose sessions and breaks remain unresolved.

Limitations:

1. Broker-native M1 history remains too short for research validation.
2. The broker H4 files extend back to 2018, but the available broker M1 export only covers a short 2026 window.
3. Broker H4 by itself cannot provide intrabar M1 stop-resolution history for a long event-driven validation.
4. This decision does not prove historical broker M1 behavior for 2021-2025.

### Option 2: HistData-built H4

Status:

Not accepted.

Rationale:

1. HistData remains blocked by source-acceptance uncertainty.
2. March-July 2023 remains materially abnormal.
3. Source-session reconciliation is unresolved.
4. Broker mismatch assessment remains a blocker.
5. Building H4 from HistData could create a signal timeframe that does not match the broker's own H4 boundaries.

### Option 3: Broker H4 plus HistData M1 hybrid

Status:

Not accepted.

Rationale:

1. Broker H4/M1 alignment has been shown only for broker-native M1, not HistData M1.
2. HistData M1 session behavior differs materially from broker-native 2026 short-window behavior.
3. A hybrid would combine signal bars from one source with intrabar execution bars from another source.
4. This could create false stop/target outcomes or false signal/execution timing compatibility.
5. A separate hybrid-compatibility decision record would be required before this approach could be used.

### Option 4: Reject HistData for H4 and M1 validation

Status:

Not final.

Rationale:

1. HistData has not been accepted.
2. HistData has serious unresolved blockers.
3. But this checkpoint does not make the final accept/reject decision for HistData.
4. The correct current status remains diagnostic-only, not accepted.

## Operational decision

Current accepted H4 reference for broker-aligned diagnostics:

`Broker-native H4`

Current accepted M1 source for broker-only alignment diagnostics:

`Broker-native M1`

Current accepted long-history validation source:

`None`

Current accepted H017 validation source:

`None`

Current HistData status:

`Not accepted`

Current H017 status:

`Alive but not promotable`

## What this enables next

This checkpoint enables future broker-aligned diagnostics to use broker-native H4 as the reference H4 signal timeframe.

Possible next diagnostics include:

1. Documenting the broker H4 boundary schedule across DST regimes.
2. Comparing broker H4 timestamp patterns to HistData candidate H4 construction boundaries.
3. Quantifying how much HistData M1 would be missing or misaligned if forced into broker H4 windows.
4. Deciding whether continued HistData reconciliation is worth the effort or whether HistData should be rejected for H017 validation.

## What remains blocked

The following remain blocked:

1. H017 validation on HistData.
2. H017 validation using a broker-H4 plus HistData-M1 hybrid.
3. HistData-built H4.
4. Derived HistData H4 files.
5. Derived HistData M1 files.
6. Live trading.
7. Phase 4 execution work.
8. Broader symbol expansion.
9. Machine-learning additions.
10. Strategy tuning to vendor quirks.

## Required future decision before H017 validation

Before H017 can be validated on any long M1 history, the project still needs one of the following:

1. A long broker-native M1 dataset that aligns with broker-native H4, or
2. A formally accepted non-broker M1 source with documented compatibility to broker-native H4 boundaries and sessions, or
3. A final decision to reject available non-broker data and pause long event-driven validation until better data exists.

## Guardrails preserved

1. No HistData was loaded for this checkpoint.
2. H017 was not run.
3. No raw broker files were modified.
4. No raw HistData files were modified.
5. No derived data files were written.
6. No source-acceptance decision for HistData was made.
7. No live-trading readiness was claimed.
8. The current full-test anchor remains 514 passed.
