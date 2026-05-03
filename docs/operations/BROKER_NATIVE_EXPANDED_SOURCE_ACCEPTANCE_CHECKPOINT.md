# Broker-Native Expanded Source-Acceptance Checkpoint

Phase: 3.26-ak  
Status: Conditional source acceptance for future H017 validation  
Scope: Expanded broker-native USDJPY and XAUUSD M1/H4 data

## Purpose

This checkpoint makes the explicit source-quality decision required before any H017 validation run can be considered on the expanded broker-native data.

This checkpoint is documentation-only.

No H017 validation was run in this phase.

No strategy tuning was performed.

No derived M1 or H4 datasets were written.

No raw broker-native files were modified.

No raw broker-native files were committed.

## Decision

Expanded broker-native USDJPY and XAUUSD M1/H4 data is conditionally accepted for a future H017 validation phase, subject to the restrictions in this document.

This is not live-trading approval.

This is not H017 promotion.

This is not permission to tune H017.

This is not permission to use HistData.

This is not permission to write derived datasets.

## Accepted Source

Broker: Exness  
Reported account environment: Demo  
Reported server/platform: MT5  
Loader timezone: Europe/Athens  
Loaded timestamp timezone after conversion: UTC

Accepted raw broker-native local inputs:

- data/raw/USDJPY/H4.csv
- data/raw/USDJPY/M1.csv
- data/raw/XAUUSD/H4.csv
- data/raw/XAUUSD/M1.csv

These raw files remain gitignored and must not be committed.

## Accepted Symbols

The conditional acceptance applies only to:

1. USDJPY
2. XAUUSD

No additional symbols are accepted.

No symbol broadening is authorized.

## Accepted Timeframes

The conditional acceptance applies only to:

1. Broker-native M1
2. Broker-native H4

The H4 data is accepted as the broker-native H4 reference.

The M1 data is accepted only for future event-bridge validation under the complete-window restrictions below.

## Explicitly Rejected Sources

HistData remains rejected for H017 validation under current evidence.

The following remain not accepted:

1. HistData as an H017 validation source.
2. HistData as an accepted research source.
3. HistData-built H4 for H017 validation.
4. Broker H4 plus HistData M1 hybrid validation.
5. Any mixed broker/HistData execution-bar validation.
6. Any source requiring silent deduplication.
7. Any source requiring raw vendor-file modification.

## Sparse Prefix Exclusion

The sparse daily-like prefix remains excluded.

The following period must not be used for H017 validation:

- 2018 through 2021-06

The expanded broker-native files have earlier timestamps, but those earlier timestamps are not dense M1 history.

The dense candidate region begins in 2021-07.

## Accepted Common Dense Span

The common broker-native M1 dense span established by diagnostics is:

- Common M1 start UTC: 2021-07-01 21:00:00+00:00
- Common M1 end UTC: 2026-04-30 07:00:00+00:00

Within that span:

- Calendar minutes inclusive: 2539321
- USDJPY observed minutes: 1784379
- XAUUSD observed minutes: 1703974
- Shared observed minutes: 1695042
- USDJPY-only observed minutes: 89337
- XAUUSD-only observed minutes: 8932
- Neither-symbol calendar minutes: 746010
- Shared observed percent of calendar: 66.751781 percent

Calendar missingness includes legitimate weekends, holidays, daily breaks, and instrument-session differences. Calendar missingness is not automatically a data defect.

## Accepted Future H017 Bridge Window Rule

Future H017 validation, if run in a later phase, must use only common complete H4/M1 bridge windows.

A common complete H4/M1 bridge window means:

1. USDJPY has a broker-native H4 bar at the H4 timestamp.
2. XAUUSD has a broker-native H4 bar at the same H4 timestamp.
3. For each symbol, the next H4 timestamp is exactly four hours later.
4. For each symbol, the M1 window `[H4 timestamp, H4 timestamp + 4 hours)` contains exactly 240 M1 bars.
5. No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

The common complete H4/M1 bridge-window diagnostic found:

- Common complete H4/M1 windows: 5476
- First common complete H4/M1 window UTC: 2021-07-02 13:00:00+00:00
- Last common complete H4/M1 window UTC: 2026-04-30 01:00:00+00:00
- USDJPY-only complete H4/M1 windows: 225
- XAUUSD-only complete H4/M1 windows: 673

A future H017 validation phase must log the exact windows used and must confirm that it does not silently include incomplete windows.

## H4/M1 Aggregation Evidence

The expanded H4/M1 aggregation compatibility diagnostic found exact agreement between broker-native M1 aggregation and broker-native H4 OHLCV on all fully covered comparable windows.

USDJPY:

- Compared full M1 windows: 5701
- Matched bars: 5701
- Mismatched bars: 0
- First full M1 window UTC: 2021-07-02 13:00:00+00:00
- Last full M1 window UTC: 2026-04-30 01:00:00+00:00

XAUUSD:

- Compared full M1 windows: 6149
- Matched bars: 6149
- Mismatched bars: 0
- First full M1 window UTC: 2021-07-02 13:00:00+00:00
- Last full M1 window UTC: 2026-04-30 01:00:00+00:00

Interpretation:

The broker-native M1 data is internally compatible with broker-native H4 on all fully covered comparable windows tested.

This was necessary for source acceptance but was not sufficient alone.

## Session-Boundary Evidence

The expanded session-boundary diagnostic found plausible but instrument-specific session behavior.

USDJPY dense-region summary:

- Dense-region bars: 1784379
- Dense-region first UTC timestamp: 2021-07-01 21:00:00+00:00
- Dense-region last UTC timestamp: 2026-04-30 07:00:00+00:00
- Duplicate timestamps in dense region: False
- Observed UTC dates: 1518
- Gap events greater than one minute: 11277
- Most common gap duration: 0 days 00:02:00
- Largest gap duration: 3 days 00:11:00
- Daily-break-like gaps between 30 and 90 minutes: 3
- Small intraday gaps between 2 and 29 minutes: 11005

XAUUSD dense-region summary:

- Dense-region bars: 1703974
- Dense-region first UTC timestamp: 2021-07-01 21:00:00+00:00
- Dense-region last UTC timestamp: 2026-04-30 07:00:00+00:00
- Duplicate timestamps in dense region: False
- Observed UTC dates: 1510
- Gap events greater than one minute: 1428
- Most common gap duration: 0 days 01:04:00
- Largest gap duration: 3 days 01:08:00
- Daily-break-like gaps between 30 and 90 minutes: 958
- Small intraday gaps between 2 and 29 minutes: 167

Interpretation:

XAUUSD shows strong daily-break structure.

USDJPY shows many small missing-minute clusters. This is acceptable only because future validation is restricted to complete H4/M1 bridge windows with exactly 240 M1 bars per symbol.

The small number of Saturday single bars in early July/August 2021 remains a source-quality note. These bars must not justify broadening or weakening the complete-window rule.

## Missingness Evidence

The expanded missingness-by-time-bucket diagnostic used the common calendar span:

- Common calendar start UTC: 2021-07-01 21:00:00+00:00
- Common calendar end UTC: 2026-04-30 07:00:00+00:00
- Calendar minutes inclusive: 2539321

USDJPY:

- Observed minutes: 1784379
- Missing calendar minutes: 754942
- Observed percent of calendar: 70.269926
- Missing cluster count: 11277
- Largest missing cluster in minutes: 4330
- Single-minute missing clusters: 7941
- Small 2-to-29-minute missing clusters: 3064
- Daily-break-like 30-to-90-minute missing clusters: 3
- Weekend-or-longer missing clusters, 721+ minutes: 264

XAUUSD:

- Observed minutes: 1703974
- Missing calendar minutes: 835347
- Observed percent of calendar: 67.103529
- Missing cluster count: 1428
- Largest missing cluster in minutes: 4387
- Single-minute missing clusters: 107
- Small 2-to-29-minute missing clusters: 60
- Daily-break-like 30-to-90-minute missing clusters: 958
- Weekend-or-longer missing clusters, 721+ minutes: 264

Interpretation:

Missingness is materially instrument-specific.

XAUUSD missingness is dominated by expected-looking daily breaks and closures.

USDJPY missingness includes many tiny missing clusters. This requires the strict complete-window rule and prevents any validation approach that assumes continuous M1 availability without checking each H4 window.

## Conditions For Future H017 Validation

A future H017 validation phase is authorized only if all of the following conditions are met:

1. The phase explicitly states it is using the conditionally accepted expanded broker-native source.
2. The phase excludes all data before 2021-07.
3. The phase uses only common complete H4/M1 bridge windows.
4. The phase logs the exact first and last H4 bridge windows used.
5. The phase logs the count of common complete H4/M1 windows used.
6. The phase confirms that each selected symbol-window has exactly 240 M1 bars.
7. The phase does not impute missing M1 bars.
8. The phase does not forward-fill or backfill M1 bars.
9. The phase does not modify raw broker files.
10. The phase does not write derived datasets unless a separate derived-data phase explicitly authorizes it.
11. The phase does not use HistData.
12. The phase does not change H017 strategy rules.
13. The phase does not tune parameters.
14. The phase does not change the cost model.
15. The phase reports results as validation evidence, not live-trading approval.

## Future Validation Window

The accepted future H017 validation bridge-window range is conditionally restricted to:

- First possible common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
- Last possible common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00

A future validation run may use a subset of that range only if the subset rule is documented before seeing results.

No cherry-picking is allowed.

No tuning to this source is allowed.

## Decision State

Decision state:

- Conditionally accepted for future H017 validation with a restricted window and complete-window rule.

Accepted symbols:

- USDJPY
- XAUUSD

Accepted timeframe:

- Broker-native M1 for event bridge
- Broker-native H4 for H017 decisions and broker reference

Accepted UTC start timestamp for possible future bridge validation:

- 2021-07-02 13:00:00+00:00

Accepted UTC end timestamp for possible future bridge validation:

- 2026-04-30 01:00:00+00:00

Excluded sparse prefix:

- 2018 through 2021-06

Excluded windows:

- Any H4/M1 window where either symbol lacks exactly 240 M1 bars inside `[H4 timestamp, H4 timestamp + 4 hours)`.
- Any H4 window where either symbol's next H4 timestamp is not exactly four hours later.
- Any window requiring imputation, forward-fill, backfill, or synthetic bars.
- Any HistData window.
- Any mixed broker/HistData window.

## H017 Status After This Checkpoint

H017 remains:

- alive,
- not promotable,
- not ready for live trading.

This checkpoint permits a future H017 validation phase under the restrictions above.

This checkpoint does not itself run H017.

This checkpoint does not imply that H017 will pass validation.

This checkpoint does not override the previous risk evidence, including the prior broker-native short-window drawdown of -33.65 percent.

## Live-Trading Status

Live trading remains unauthorized.

Phase 4 execution work remains unauthorized.

Production deployment remains unauthorized.

## Next Recommended Phase

The next recommended phase is:

- Phase 3.26-al: Expanded broker-native H017 validation run plan and preflight

That phase should inspect the actual validation/backtest APIs before running anything.

It should confirm how the existing event bridge can enforce the common complete H4/M1 bridge-window rule.

It should still avoid tuning and avoid live-trading assumptions.

## Final Verdict

The expanded broker-native source is now conditionally accepted for a future H017 validation phase, but only under strict complete-window and no-imputation rules.

The sparse prefix remains excluded.

HistData remains rejected for H017 validation.

H017 remains not promotable until future validation evidence says otherwise.
