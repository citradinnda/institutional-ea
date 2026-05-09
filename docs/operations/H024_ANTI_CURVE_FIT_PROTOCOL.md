# H024 Anti-Curve-Fit Protocol

H024 is a serious research candidate, but it is not deployment-approved.

This protocol freezes the current H024 candidate for anti-curve-fit evaluation.

## Frozen Candidate

Candidate:

- H024 pullback-continuation
- USDJPY + XAUUSD
- Exness demo MT5 broker-native exports only
- broker-native H4/M1 strict bridge windows only
- hold = 3 H4
- stop ATR multiple = 2.0
- baseline modeled costs
- H020 sizing contract
- H018 hard guards unchanged

## Current Evidence

H024 hold=3 has passed:

- preliminary fixed-lifecycle validation
- targeted stop/cost robustness
- chronological validation
- trade-ledger audit
- actual gross leverage audit

Known weakness:

- 2023 remains materially negative
- 2023 must not be excluded or hidden with a year/session/time filter

## Anti-Curve-Fit Rules

Do not change H024 parameters during anti-curve-fit evaluation.

Do not:

- optimize hold horizon
- optimize stop ATR multiple
- optimize regime windows
- optimize pullback thresholds
- add time/session filters
- exclude 2023
- broaden symbols to rescue the result
- use ML
- lower modeled costs
- weaken H018 guards

Any parameter change or filtering idea must become a new hypothesis, not an H024 adjustment.

## Required Negative Controls

Before H024 can be considered for demo-readiness review, it should pass negative-control diagnostics.

Minimum controls:

1. Direction flip control

Same H024 timestamps, sizing path, costs, lifecycle, and bridge windows, but directional exposure is inverted.

Expected result:

- materially worse than frozen H024
- preferably negative or below PF 1.0

2. Timestamp shuffle control

Preserve trade count and symbol/side distribution, but randomize valid entry timestamps without using future information.

Expected result:

- frozen H024 should outperform most shuffled variants

3. 2023 stop-exit audit

Inspect the 17 2023 stop exits directly.

Expected result:

- no post-hoc exclusion rule
- no hidden leverage pathology
- no obvious data quality issue
- clear record of whether losses look like ordinary adverse stop realization

## Interpretation Standard

Passing these controls would reduce curve-fit risk. It would not prove H024 is not curve-fit.

Failing these controls blocks demo-readiness review.

H024 remains:

- not demo-approved
- not live-approved
- not Phase 4-approved
