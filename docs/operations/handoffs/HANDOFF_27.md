# HANDOFF 27 - Self-Contained Continuation After HistData Path Rejection Checkpoint

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_27 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research: Python quantcore
- Execution: MetaTrader 5 later
- Production target: Oracle Cloud Always Free VPS later
- Monitoring: self-hosted free-tier stack later
- Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in .venv

Do not rush into strategy validation or live trading. The project remains in data infrastructure and research-validation work.

## Non-Negotiable Workflow Rules

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- .venv
- No WSL
- No Linux/macOS shell assumptions

Important PowerShell rule:

Do not use Linux/macOS heredoc syntax like:

    python - <<'PY'

PowerShell does not support that.

Use PowerShell here-strings instead:

    @'
    python code here
    '@ | python -

Tone and workflow:

1. Step-by-step.
2. Numbered steps.
3. Explicit Windows paths.
4. Plain English.
5. Define technical terms inline when needed.
6. Never write code without saying exactly where the file goes and how to run it.
7. One sub-phase per response.
8. Never skip git commits.
9. Never continue while local commits are unpushed.
10. Always read git status.
11. If tests pass but the count drops, treat it as a regression.
12. Do not propose switching to another AI chat unless the user asks.
13. For documentation-only phases, it is okay to provide one consolidated PowerShell block, as long as it includes status, tests, commit, push, final status, git ls-files, and recent log.
14. For code or diagnostics, be more cautious: inspect APIs first and split if needed.

Before writing code that calls internal functions, inspect actual APIs with:

    inspect.signature(...)
    dataclasses.fields(...)

Do not trust remembered function names or keyword names.

After each sub-phase:

1. Run focused tests if applicable.
2. Run full pytest -q.
3. Check git status.
4. Commit.
5. Push.
6. Check git status.
7. Run git ls-files on touched files or directories.
8. Read the output before continuing.

After each response, offer exactly:

    ✅ done
    ⚠️ error — paste it
    🤔 question

## Repository State

Repository root:

    C:\Users\equin\Documents\institutional-ea

Virtual environment:

    C:\Users\equin\Documents\institutional-ea\.venv

Branch:

    main

GitHub remote:

    https://github.com/citradinnda/institutional-ea.git

Current expected latest project commit immediately before this handoff is committed:

    b8f58c5 Document HistData path decision checkpoint

Expected latest commit after this handoff is committed:

    Add handoff document #27 after HistData path decision checkpoint

Recent commit context:

    b8f58c5 Document HistData path decision checkpoint
    b43dfe5 Document H4 construction decision checkpoint
    3cdeaca Document broker H4 M1 alignment diagnostic
    6a48870 Document broker H4 M1 loaded shape inspection
    545b5c7 Add handoff document #26 after broker H4 M1 preflight
    82c68fa Document broker H4 M1 alignment preflight
    043de0d Add broker H4 M1 alignment diagnostic plan
    c85e49c Document H4 construction evidence requirements
    3539fa0 Add H4 construction decision plan
    8512edc Document broker mismatch assessment
    12988a6 Add broker mismatch assessment plan
    f3b576f Add handoff document #25 after broker short-window session diagnostic

Known note:

There are two older consecutive commits with the message Add handoff document #23 after HistData duplicate policy. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    514 passed

Important test-count rule:

- Previous anchor after Phase 3.25 was 509 passed.
- Phase 3.26-b deliberately added 5 HistData duplicate-policy tests.
- Current correct anchor is 514 passed.
- If tests pass but the count drops below 514 without a deliberate test-removal phase, treat it as a regression.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification only.

Ask the user to run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -15
    pytest -q

Expected status after this handoff is committed and pushed:

- On branch main
- Your branch is up to date with origin/main.
- nothing to commit, working tree clean

Expected latest commit:

    Add handoff document #27 after HistData path decision checkpoint

Expected project commit before handoff:

    b8f58c5 Document HistData path decision checkpoint

Expected tests:

    514 passed

Read the output before continuing.

## Gitignore / Raw Data Rules

Important .gitignore rule:

The repo uses root-anchored:

    /data/

Do not change it to unanchored:

    data/

Reason:

An unanchored data/ rule previously risked excluding:

    quantcore/data/

Raw data files under /data/ are gitignored and must not be committed.

Do not commit raw M1/H4 data.

Do not commit large derived data files unless there is an explicit plan saying to do so. Current rule: do not commit raw or large derived data.

## Current Important Paths

Code:

    C:\Users\equin\Documents\institutional-ea\quantcore
    C:\Users\equin\Documents\institutional-ea\scripts
    C:\Users\equin\Documents\institutional-ea\tests

Important data modules:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\loaders.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\mt5_loader.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\dukascopy_loader.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\coverage.py
    C:\Users\equin\Documents\institutional-ea\quantcore\data\preflight.py

Important tests:

    C:\Users\equin\Documents\institutional-ea\tests\test_mt5_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_dukascopy_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_coverage.py
    C:\Users\equin\Documents\institutional-ea\tests\test_preflight.py

Important recent docs:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_PATH_DECISION_CHECKPOINT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_DECISION_CHECKPOINT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_LOADED_SHAPE_INSPECTION.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_PREFLIGHT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_DIAGNOSTIC_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_EVIDENCE_REQUIREMENTS.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_DECISION_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_MISMATCH_ASSESSMENT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_MISMATCH_ASSESSMENT_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_SHORT_WINDOW_SESSION_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_SHORT_WINDOW_SESSION_DIAGNOSTIC_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md

Decision docs:

    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-001-m1-data-acquisition.md
    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-002-external-m1-data-source-evaluation.md
    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-003-histdata-duplicate-handling.md

## H017 Current Status

H017 remains:

- alive
- not promotable
- not ready for live trading
- blocked by insufficient research-grade M1 history
- blocked by source-acceptance uncertainty
- not authorized for HistData validation

Existing realistic event-driven result from broker-native short M1 window:

    fills=470
    starting_equity_usd=10000.00
    ending_equity_usd=16145.60
    total_return_pct=61.46
    max_drawdown_pct=-33.65
    annualized_sharpe=1.3218

Claim result:

    PSR: 0.8662, failed threshold 0.95
    MinTRL feasible: True
    MinTRL required n: 1034
    MinTRL observed n: 470
    DSR: Skipped
    H017 promotable: False

Operational verdict:

    PIPELINE SMOKE PASSED: True
    RESEARCH VALIDATION SUFFICIENT: False

Interpretation:

1. The event pipeline works.
2. Broker-native M1 history is too short.
3. Do not trust the short-window +61.46% return as validated edge.
4. The -33.65% drawdown is a serious risk signal.
5. H017 is alive but not promotable.

Do not run H017 on HistData.

## Strategy / Validation Background

The project uses strict hypothesis discipline because many prior strategies failed.

Immutable strategy graveyard summary:

- H001: Backtest without intrabar SL/TP simulation is fiction. Must use M1 inside H4 bars to resolve fills.
- H002-H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
- H004a: Single-seed models unreliable; use multi-seed ensembles.
- H005: Stacked multi-symbol models fail on heterogeneous instruments; use per-symbol models.
- H006-H007: Confidence filters are not risk management. ML chooses entries; deterministic rules manage risk.
- H008-H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals cannot be risk manager.
- H011-H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk ceiling remained.
- H014-H016: Two-asset USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1 percent per-trade risk was not 1 percent portfolio risk when trades overlapped. Drawdown breach was -19.43 percent.
- H015: Diversification into negative-edge instruments destroys the portfolio.
- H017: H016 plus portfolio heat governor. Alive but not promotable.

Do not broaden to more symbols yet.
Do not add machine learning yet.
Do not tune H017 to vendor quirks or short-window results.

## Core Strategy Conventions

ATR:

- Wilder RMA, not SMA.
- First true range is high - low.
- Seed at index window - 1 with simple mean of first window true ranges.
- Recurrence:

    ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n

Chandelier Exit:

- Long:

    highest_high(lookback) - multiplier * ATR

- Short:

    lowest_low(lookback) + multiplier * ATR

Defaults:

    multiplier = 3.0
    lookback = 22

Vol Target:

- Realized vol at bar t uses returns through t-1 only:

    returns.shift(1).rolling(lookback)

- No lookahead.
- For H4 bars:

    periods_per_year = 1512

Signals:

- Donchian breakout.
- Long:

    close[t] > max(high[t-N ... t-1])

- Short:

    close[t] < min(low[t-N ... t-1])

- Channel uses prior N bars:

    shift(1).rolling(N)

H017:

- Inner-joins USDJPY and XAUUSD timestamps.
- Computes close-to-close returns.
- Uses same returns for vol targeting and heat governor.
- Position is signed risk exposure:

    signal * per_trade_risk * vol_mult * heat_mult

Heat governor:

- Combined heat:

    sqrt(w' (r^2 * C) w)

- Defaults:

    cap = 0.015
    per_trade_risk = 0.01
    correlation_window = 120
    correlation_floor = 0.0

## Phase 3 Event-Driven Backtest Conventions

Phase 3.1 fill rule:

If stop and take-profit are both touched in the same M1 bar, stop wins.

Reason:

M1 OHLC does not reveal tick order inside the minute, so stop-first is conservative.

Phase 3.2 cost model defaults:

USDJPY:

    spread_price = 0.01
    commission_usd_per_lot_per_fill = 7.0
    stop_slippage_atr_fraction = 0.05

XAUUSD:

    spread_price = 0.30
    commission_usd_per_lot_per_fill = 10.0
    stop_slippage_atr_fraction = 0.05

Commission is per fill. A round trip charges entry and exit.

Portfolio P&L:

- XAUUSD P&L is already USD.
- USDJPY P&L is JPY and must be divided by USDJPY conversion price to become USD.

Event bridge timing:

1. H017 decides at H4 timestamp t.
2. Trade opens on next H4 bar open t+1.
3. M1 bars inside [t+1, t+2) resolve stops.
4. If no stop is hit, exposure closes at t+2 open as signal_flip.
5. This is a bridge-layer simplification.

## MT5 / Broker Data State

Broker timezone:

    Europe/Athens

Meaning:

- Winter UTC+2
- Summer UTC+3
- DST-aware

MT5 loader:

    load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

MT5LoadResult fields verified:

    bars
    n_bars
    n_input_rows
    earliest_utc
    latest_utc
    broker_tz

MT5 raw exports are local and gitignored:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Do not commit these raw files.

## Broker H4/M1 Loaded-Shape Inspection Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_LOADED_SHAPE_INSPECTION.md

Commit:

    6a48870 Document broker H4 M1 loaded shape inspection

Status:

- Read-only.
- No HistData used.
- No H017 run.
- No derived data written.
- No raw files modified.

Key result:

- USDJPY H4 classified as h4_spaced.
- XAUUSD H4 classified as h4_spaced.
- Earlier concern that H4.csv might be daily-like was resolved.

Key numbers:

USDJPY H4:

    n_bars: 8708
    earliest_utc: 2018-07-02 21:00:00+00:00
    latest_utc: 2026-04-29 09:00:00+00:00
    dominant_delta: 0 days 04:00:00
    four_hour_delta_pct: 86.252441
    one_day_delta_pct: 8.854944
    classification: h4_spaced

XAUUSD H4:

    n_bars: 8658
    earliest_utc: 2018-06-27 21:00:00+00:00
    latest_utc: 2026-04-30 05:00:00+00:00
    dominant_delta: 0 days 04:00:00
    four_hour_delta_pct: 86.173039
    one_day_delta_pct: 8.871434
    classification: h4_spaced

USDJPY M1:

    n_bars: 97907
    earliest_utc: 2026-01-26 03:09:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    dominant_delta: 0 days 00:01:00
    one_minute_delta_pct: 99.911139

XAUUSD M1:

    n_bars: 97966
    earliest_utc: 2026-01-20 02:22:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    dominant_delta: 0 days 00:01:00
    one_minute_delta_pct: 99.919359

## Broker H4/M1 Alignment Diagnostic Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_DIAGNOSTIC.md

Commit:

    3cdeaca Document broker H4 M1 alignment diagnostic

Status:

- Read-only.
- Broker-only.
- No HistData used.
- No H017 run.
- No derived data written.
- No raw files modified.

Method:

1. Load broker H4 and broker M1.
2. Compare only H4 bars whose next H4 timestamp is exactly 4 hours later.
3. Compare only windows with exactly 240 M1 bars covering [H4 timestamp, H4 timestamp + 4 hours).
4. Aggregate M1 as:
   - open = first M1 open
   - high = max M1 high
   - low = min M1 low
   - close = last M1 close
   - volume = sum M1 volume
5. Compare OHLCV against broker H4.

Key result:

- Broker-native H4 aligned exactly with broker-native M1 aggregation on every fully covered H4 window tested.
- No OHLCV mismatches were found.

USDJPY:

    total_h4_bars: 8708
    candidate_exact_4h_bars: 7510
    candidates_inside_m1_range: 403
    compared_full_m1_windows: 338
    skipped_non_4h_next_delta: 1198
    skipped_outside_m1_range: 7107
    skipped_incomplete_m1_window: 65
    matched_bars: 338
    mismatched_bars: 0
    classification: aligned_on_all_full_m1_windows

XAUUSD:

    total_h4_bars: 8658
    candidate_exact_4h_bars: 7460
    candidates_inside_m1_range: 426
    compared_full_m1_windows: 354
    skipped_non_4h_next_delta: 1198
    skipped_outside_m1_range: 7034
    skipped_incomplete_m1_window: 72
    matched_bars: 354
    mismatched_bars: 0
    classification: aligned_on_all_full_m1_windows

Interpretation:

1. Broker-native H4 is internally consistent with broker-native M1 in the short 2026 overlap.
2. The available broker M1 export remains too short for long research validation.
3. This does not validate H017.
4. This does not accept HistData.
5. This does not prove 2021-2025 broker M1 behavior.

## H4 Construction Decision Checkpoint Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_DECISION_CHECKPOINT.md

Commit:

    b43dfe5 Document H4 construction decision checkpoint

Decision:

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
6. Live trading or production deployment is authorized.
7. The short 2026 broker M1 export is sufficient for long research validation.
8. The broker 2021-2025 historical M1 behavior is proven by the 2026 short-window export.

Current accepted H4 reference for broker-aligned diagnostics:

    Broker-native H4

Current accepted M1 source for broker-only alignment diagnostics:

    Broker-native M1

Current accepted long-history validation source:

    None

Current accepted H017 validation source:

    None

## HistData Acquisition State

The user downloaded approximately five years of M1 data from HistData.

The original HistData files were preserved exactly as downloaded.

The inspected HistData files are currently under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

Important:

- This folder name is misleading because it contains both Dukascopy sample files and HistData files.
- Do not rename or move files until explicitly planned and documented.
- The files are under /data/, so they are gitignored.
- Do not commit raw data.

USDJPY raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv

Inventory:

    size_bytes: 115758784
    sha256: 2aa2840918404b4665f8c79e31ea4a0b691ef85e878f683021cc3c4f7980a29e
    line_count: 1808731
    first observed timestamp row: 2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0
    last observed timestamp row: 2025.12.31,16:57,156.683000,156.685000,156.668000,156.671000,0

XAUUSD raw HistData file:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv

Inventory:

    size_bytes: 117405332
    sha256: e11187138f6aa0b9bbcb75f8fc9423bde6b909a2e9afade01ed952cf6a7b2e13
    line_count: 1726549
    first observed timestamp row: 2021.01.03,18:00,1904.998000,1910.898000,1903.288000,1909.718000,0
    last observed timestamp row: 2025.12.31,16:57,4318.069000,4318.459000,4317.029000,4318.379000,0

Observed HistData raw format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

This differs from Dukascopy.

Therefore:

- Do not call these files Dukascopy files.
- Do not use the Dukascopy loader as the official HistData loader.
- Use the dedicated HistData loader only for explicitly planned diagnostics.

## HistData Loader Current State

Dedicated HistData loader:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py

Public API:

    load_histdata_m1_csv(
        path: str | Path,
        *,
        source_tz: str = "UTC",
        duplicate_policy: DuplicatePolicy = "reject",
    ) -> HistDataM1LoadResult

Duplicate policy type:

    DuplicatePolicy = Literal["reject", "drop_exact"]

Default behavior:

    duplicate_policy="reject"

Default behavior remains strict:

- duplicate timestamps are fatal by default.

Explicit opt-in behavior:

    duplicate_policy="drop_exact"

drop_exact behavior:

1. Removes only exact duplicate OHLCV rows.
2. Requires all rows in each duplicate timestamp group to be identical across:
   - open
   - high
   - low
   - close
   - volume
3. Rejects conflicting duplicate timestamp groups.
4. Does not modify raw files.
5. Does not write derived files.
6. Returns audit metadata.

Current HistDataM1LoadResult fields:

    bars
    n_bars
    n_input_rows
    earliest_utc
    latest_utc
    source_tz
    duplicate_policy
    n_duplicate_rows_removed
    n_duplicate_timestamp_values
    duplicate_timestamp_ranges
    n_missing_minutes
    missing_minutes

Focused HistData loader tests:

    20 passed

Full project test anchor:

    514 passed

## HistData Duplicate Findings

Running strict load_histdata_m1_csv(path) on the real USDJPY HistData file failed with:

    ValueError: HistData M1 CSV at ... has duplicate timestamps.

This was correct protective behavior.

Both USDJPY and XAUUSD had:

    n_duplicate_rows_in_duplicate_groups: 600
    n_duplicate_timestamp_values: 300
    n_conflicting_duplicate_timestamp_values: 0
    all_duplicate_groups_have_identical_ohlcv: True

Duplicate blocks occurred on:

    2021.10.31 19:00 through 19:59
    2022.10.30 19:00 through 19:59
    2023.10.29 19:00 through 19:59
    2024.10.27 19:00 through 19:59
    2025.10.26 19:00 through 19:59

Each duplicated timestamp had exactly two rows.

Interpretation:

- The duplicates strongly suggest a recurring annual daylight-saving-time related duplicate hour.
- But this observation alone did not constitute source acceptance.

## March-July 2023 HistData Anomaly Summary

March-July 2023 was materially abnormal for both symbols.

USDJPY March-July source-session comparison:

    2021 observed_pct: 70.299110
    2022 observed_pct: 70.918664
    2023 observed_pct: 50.115287
    2024 observed_pct: 70.958606
    2025 observed_pct: 71.042121

XAUUSD March-July source-session comparison:

    2021 observed_pct: 67.450980
    2022 observed_pct: 67.410585
    2023 observed_pct: 48.686910
    2024 observed_pct: 67.404230
    2025 observed_pct: 67.517702

Interpretation:

1. March-July 2023 is materially abnormal relative to same-month control years.
2. The anomaly affects both USDJPY and XAUUSD.
3. The anomaly is not explained by weekends alone.
4. The anomaly is not explained by the XAUUSD 17:00 UTC daily break alone.
5. It remains incompatible with research-grade H017 validation.

## Broker Short-Window Session Diagnostic Summary

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_SHORT_WINDOW_SESSION_DIAGNOSTIC.md

Status:

- Read-only diagnostic completed.
- Used local CSV exports only.
- MT5 was not connected.
- H017 was not run.
- HistData was not accepted.

USDJPY broker short-window findings:

    n_bars: 97907
    earliest_utc: 2026-01-26 03:09:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    missing_minutes_inside_symbol_range: 37685

USDJPY broker Sunday observed open clusters:

    20:05 UTC
    19:05 UTC
    18:05 UTC

USDJPY broker Friday observed close clusters:

    19:58 UTC
    18:58 UTC
    17:58 UTC

XAUUSD broker short-window findings:

    n_bars: 97966
    earliest_utc: 2026-01-20 02:22:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    missing_minutes_inside_symbol_range: 46313

XAUUSD broker Sunday observed open clusters:

    21:01 UTC
    20:01 UTC
    19:01 UTC

XAUUSD broker Friday observed close clusters:

    19:57 UTC
    18:57 UTC
    17:57 UTC

XAUUSD broker additional symbol-specific missingness:

    XAUUSD_only_missing_common_minutes: 5496

XAUUSD-only missingness clusters mainly around UTC hours:

    18
    19
    20

Cross-symbol broker common window:

    common_start_utc: 2026-01-26 03:09:00+00:00
    common_end_utc: 2026-04-30 07:00:00+00:00
    common_full_minutes: 135592
    USDJPY_observed_common_minutes: 97907
    XAUUSD_observed_common_minutes: 92411
    overlapping_observed_common_minutes: 92411
    USDJPY_missing_common_minutes: 37685
    XAUUSD_missing_common_minutes: 43181
    overlapping_missing_common_minutes: 37685
    USDJPY_only_missing_common_minutes: 0
    XAUUSD_only_missing_common_minutes: 5496
    USDJPY_common_observed_pct: 72.207062
    XAUUSD_common_observed_pct: 68.153726
    overlapping_observed_pct_of_common_full: 68.153726

Interpretation:

1. Broker-native USDJPY sessions differ materially from HistData USDJPY source-session candidates.
2. Broker-native XAUUSD sessions differ materially from HistData XAUUSD source-session candidates.
3. Broker-native XAUUSD has additional symbol-specific missingness relative to USDJPY.
4. The broker common timeline is constrained by XAUUSD availability.
5. Broker mismatch assessment became an explicit HistData acceptance blocker.
6. The broker short window is useful for session inference but insufficient for research validation.
7. The broker window is 2026, while HistData is 2021-2025; this cannot prove historical broker equivalence.

## HistData Path Decision Checkpoint Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_PATH_DECISION_CHECKPOINT.md

Commit:

    b8f58c5 Document HistData path decision checkpoint

Decision:

HistData is rejected for H017 validation under current evidence.

HistData raw files may remain available for diagnostic reference only.

Current statuses:

1. HistData as H017 validation source: rejected under current evidence.
2. HistData as accepted research source: not accepted.
3. HistData-built H4: not accepted.
4. Broker H4 plus HistData M1 hybrid: not accepted.
5. Derived HistData files: not authorized.
6. H017 validation on HistData: not authorized.
7. Long-history H017 validation source: none accepted.
8. H017 status: alive but not promotable.

The reason is not a single issue. It is the combination of:

1. Duplicate timestamp handling required special documented policy.
2. March-July 2023 is materially abnormal for both symbols.
3. Source-session reconciliation remains unresolved.
4. Broker mismatch assessment remains adverse.
5. Broker-native H4 is now the accepted H4 reference for broker-aligned diagnostics.
6. HistData-built H4 remains unaccepted.
7. Broker H4 plus HistData M1 hybrid remains unaccepted.
8. Using HistData for H017 would risk validating against a source whose session structure and execution bars may not represent the broker.

Remaining allowed HistData uses:

- explicitly planned diagnostics only
- documentation
- source-quality comparison
- raw inventory metadata preservation

Not allowed:

- H017 validation
- strategy tuning
- derived production datasets
- derived H4 files for H017 validation
- broker-H4 plus HistData-M1 hybrid validation
- silent deduplication
- raw file modification
- raw file commits

## Current Project State After HANDOFF_27

Accepted H4 reference for broker-aligned diagnostics:

    Broker-native H4

Accepted M1 source for broker-only alignment diagnostics:

    Broker-native M1

Accepted long-history M1 validation source:

    None

Accepted H017 validation source:

    None

HistData status:

    Not accepted; rejected for H017 validation under current evidence; diagnostic-reference only.

H017 status:

    Alive but not promotable.

Research validation status:

    Blocked.

Broker-native M1 status:

    Internally aligned with broker H4 on short 2026 overlap, but too short for research validation.

Broker-native H4 status:

    Accepted as broker-aligned diagnostic reference only.

Live trading status:

    Not authorized.

## Practical Next Paths

The project now has three practical paths:

1. Try to acquire longer broker-native M1 history from the current broker or another broker-equivalent source.
2. Search for a better non-broker M1 source and subject it to the same source-acceptance discipline.
3. Pause long event-driven validation until better data exists, while keeping H017 as a non-promotable pipeline smoke result.

Preferred next data path:

Pursue longer broker-native or broker-equivalent M1 data, because broker-native H4 is now the accepted signal-timeframe reference for broker-aligned diagnostics.

## Recommended Next Sub-Phase

Recommended next sub-phase:

    Phase 3.26-y - Long broker-native M1 acquisition options checkpoint

Purpose:

1. Decide how to pursue longer broker-native or broker-equivalent M1 history.
2. Keep the work data-infrastructure focused.
3. Do not run H017.
4. Do not accept any new source without source-acceptance diagnostics.
5. Do not write derived data.
6. Do not start Phase 4 execution.
7. Do not do live trading.

Suggested content:

1. Document current accepted broker-aligned reference: broker-native H4.
2. Document that broker-native M1 is aligned but too short.
3. List possible acquisition options:
   - attempt deeper MT5 History Center / broker export
   - ask broker support about M1 history availability
   - consider a broker-equivalent paid/free data source only if licensing and session compatibility can be documented
   - consider pausing validation rather than accepting bad data
4. Define acceptance gates for any future M1 source:
   - raw inventory
   - loader or parser validation
   - timezone/session documentation
   - duplicate policy
   - coverage analysis
   - broker H4 boundary compatibility
   - broker H4/M1 aggregation compatibility where overlap exists
   - event-driven stop-resolution suitability
   - no silent data repair
5. Keep HistData rejected for H017 validation.

## Absolute Do-Not Rules At HANDOFF_27

Do not:

1. Do not run H017 validation on HistData.
2. Do not use HistData for H017 validation.
3. Do not accept HistData as a research source.
4. Do not build HistData H4 for H017 validation.
5. Do not combine broker H4 with HistData M1.
6. Do not tune H017.
7. Do not change the cost model.
8. Do not commit raw HistData CSV files.
9. Do not commit raw MT5 CSV files.
10. Do not call HistData files Dukascopy files.
11. Do not use the Dukascopy loader as the official HistData loader.
12. Do not change .gitignore from /data/ to data/.
13. Do not start Phase 4 execution code.
14. Do not start live trading.
15. Do not ignore the -33.65% drawdown.
16. Do not broaden to more symbols yet.
17. Do not add machine learning yet.
18. Do not continue development while local commits are unpushed.
19. Do not let git status go unread.
20. Do not use Linux/macOS shell syntax in PowerShell.
21. Do not silently deduplicate vendor data.
22. Do not modify raw HistData files.
23. Do not modify raw MT5 files.
24. Do not write derived data files before source acceptance and a specific derived-data write phase.
25. Do not treat the 2023 March-July anomaly as harmless.
26. Do not treat the XAUUSD 17:00 UTC HistData break as accepted broker-equivalent behavior.
27. Do not treat the short 2026 broker window as enough for research validation.
28. Do not infer historical broker 2021-2025 sessions solely from 2026 broker exports.
29. Do not treat broker-native H4 acceptance for diagnostics as H017 validation.
30. Do not treat broker-only H4/M1 alignment as HistData acceptance.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

1. .gitignore once had unrooted data/, which risked excluding quantcore/data/.
2. Some older commits missed files because git add was incomplete.
3. An empty HANDOFF_16.md was accidentally committed once; verify handoff file size and preview before committing.
4. Markdown code fences have been damaged by paste before; avoid nested markdown fences in command blocks.
5. PowerShell does not support Linux heredocs.
6. VS Code can keep unsaved buffers that overwrite edits.
7. If terminal output shows command echo ambiguity, verify with Select-String or file previews before proceeding.
8. Always run tests.
9. Always inspect git status.
10. Always push commits.
11. Always verify git ls-files after commits.
12. Treat test-count drops as regressions.
13. If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after Phase 3.26-x and HANDOFF_27.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
2. Current full-test anchor is 514 passed.
3. Latest expected handoff commit is Add handoff document #27 after HistData path decision checkpoint.
4. Latest expected project commit before the handoff is b8f58c5 Document HistData path decision checkpoint.
5. Broker-native H4 is accepted as the reference H4 signal timeframe for broker-aligned diagnostics only.
6. Broker-native H4 is internally aligned with broker-native M1 over fully covered short 2026 windows.
7. Broker-native M1 remains too short for long research validation.
8. HistData is rejected for H017 validation under current evidence.
9. HistData remains not accepted as a research source.
10. HistData raw files may remain available for diagnostic reference only.
11. Broker H4 plus HistData M1 hybrid is not accepted.
12. HistData-built H4 is not accepted.
13. No long-history M1 validation source is currently accepted.
14. H017 is alive but not promotable.
15. Do not run H017 on HistData.
16. Do not tune H017.
17. Do not start live trading or Phase 4 execution.
18. The next logical sub-phase is Phase 3.26-y: long broker-native M1 acquisition options checkpoint.
19. First task is hygiene verification only. No new code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -15
    pytest -q

Then paste the full output.

✅ done
⚠️ error — paste it
🤔 question
