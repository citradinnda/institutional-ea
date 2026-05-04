# HANDOFF 24 - Self-Contained Continuation After HistData Focused 2023 Session-Break Analysis

You are continuing an existing project. Read this entire handoff before responding. Do not invent context. When in doubt, ask before writing code.

This HANDOFF_24 file is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_24 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, or poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research: Python `quantcore`
- Execution: MetaTrader 5 later
- Production target: Oracle Cloud Always Free VPS later
- Monitoring: self-hosted free-tier stack later
- Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in `.venv`

Do not rush into strategy validation or live trading. This project is currently still in data infrastructure / research-validation work.

## Non-Negotiable Workflow Rules

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
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
10. Always read `git status`.
11. If tests pass but the count drops, treat it as a regression.
12. Do not propose switching to another AI chat unless the user asks.

Before writing code that calls internal functions, inspect actual APIs with:

    inspect.signature(...)
    dataclasses.fields(...)

Do not trust remembered function names or keyword names.

After each sub-phase:

1. Run focused tests if applicable.
2. Run full `pytest -q`.
3. Check `git status`.
4. Commit.
5. Push.
6. Check `git status`.
7. Run `git ls-files <touched-dirs>/`.
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

Current expected latest project commit immediately before this handoff:

    fc97826 Document HistData focused 2023 session-break analysis

Current expected latest commit after this handoff is committed:

    Add handoff document #24 after HistData focused 2023 analysis

Recent expected commit context:

    fc97826 Document HistData focused 2023 session-break analysis
    7dbe4f2 Document HistData coverage and session analysis
    2f600cf Add HistData coverage and session analysis plan
    f09917b Add HistData derived-data provenance plan
    bba281a Fix HistData drop_exact check markdown formatting
    908f3ab Document HistData drop_exact real-file check
    1257ec3 Add handoff document #23 after HistData duplicate policy
    21ae512 Add handoff document #23 after HistData duplicate policy
    c41943a Add explicit HistData exact duplicate policy
    6e53c9e Add HistData duplicate handling decision record
    e05025b Document HistData loader real-file duplicate check
    ccedcbb Add tested HistData M1 CSV loader

Note:

There are two consecutive commits with the message `Add handoff document #23 after HistData duplicate policy`. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    514 passed

Important test-count rule:

- Previous anchor after Phase 3.25 was `509 passed`.
- Phase 3.26-b deliberately added 5 HistData duplicate-policy tests.
- New correct anchor is `514 passed`.
- If tests pass but the count drops below `514` without a deliberate test-removal phase, treat it as a regression.

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
- Your branch is up to date with `origin/main`.
- nothing to commit, working tree clean

Expected latest commit:

    Add handoff document #24 after HistData focused 2023 analysis

Expected project commit before handoff:

    fc97826 Document HistData focused 2023 session-break analysis

Expected tests:

    514 passed

Read the output before continuing.

## Gitignore / Raw Data Rules

Important `.gitignore` rule:

The repo uses root-anchored:

    /data/

Do not change it to unanchored:

    data/

Reason:

An unanchored `data/` rule previously risked excluding:

    quantcore/data/

Raw data files under `/data/` are gitignored and must not be committed.

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

Important docs:

    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-001-m1-data-acquisition.md
    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-002-external-m1-data-source-evaluation.md
    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-003-histdata-duplicate-handling.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_ACQUISITION_INVENTORY.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_LOADER_REAL_FILE_CHECK.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_DROP_EXACT_REAL_FILE_CHECK.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_DERIVED_DATA_PROVENANCE_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_COVERAGE_SESSION_ANALYSIS_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_COVERAGE_SESSION_ANALYSIS.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_FOCUSED_2023_SESSION_BREAK_ANALYSIS.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\DUKASCOPY_M1_SAMPLE_INSPECTION.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\DUKASCOPY_LOADER_SAMPLE_CHECK.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\DUKASCOPY_COVERAGE_CHECK_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\MT5_M1_ACQUISITION_ATTEMPTS.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md

## H017 Current Status

H017 remains:

- alive
- not promotable
- not ready for live trading
- blocked by insufficient research-grade M1 history

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
3. Do not trust the short-window `+61.46%` return as validated edge.
4. The `-33.65%` drawdown is a serious risk signal.
5. H017 is alive but not promotable.

Do not run H017 on HistData yet.

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

MT5 raw exports are local and gitignored:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Current broker-native M1 coverage is insufficient.

Real-data event smoke previously showed:

    USDJPY M1 earliest: 2026-01-26 03:09:00+00:00
    USDJPY M1 latest: 2026-04-30 07:00:00+00:00
    XAUUSD M1 earliest: 2026-01-20 02:22:00+00:00
    XAUUSD M1 latest: 2026-04-30 07:00:00+00:00

Research sufficient:

    False

## Dukascopy Status

Dukascopy was the first external M1 candidate under evaluation.

Tiny sample files are local and gitignored under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

Dukascopy sample files:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USD-JPY_Minute_2024-01-03_UTC.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAU-USD_Minute_2024-01-03_UTC.csv

Observed Dukascopy format:

    UTC,Open,High,Low,Close,Volume

Observed timestamp example:

    03.01.2024 00:00:00.000 UTC

Dukascopy loader exists:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\dukascopy_loader.py

Public API:

    load_dukascopy_csv(path: str | Path) -> DukascopyLoadResult

Dukascopy is still not accepted as a research source.

Do not use Dukascopy data as H017 validation evidence yet.

## HistData Acquisition State

The user downloaded approximately five years of M1 data from HistData.

The original HistData files were preserved exactly as downloaded.

This is important because it preserves a clean provenance chain.

The inspected HistData files are currently under:

    C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples

Important:

- This folder name is misleading because it contains both Dukascopy sample files and HistData files.
- Do not rename or move files until explicitly planned and documented.
- The files are under `/data/`, so they are gitignored.
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

Example:

    2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0

This differs from Dukascopy.

Therefore:

- Do not call these files Dukascopy files.
- Do not use the Dukascopy loader as the official HistData loader.
- Use the dedicated HistData loader.

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

`drop_exact` behavior:

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

Current `HistDataM1LoadResult` fields:

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

Duplicate timestamp range type:

    DuplicateTimestampRange = tuple[pd.Timestamp, pd.Timestamp, int]

Meaning:

    (start_utc, end_utc, n_duplicate_timestamp_values_in_range)

Focused HistData loader tests:

    20 passed

Full project test anchor:

    514 passed

## HistData Duplicate Findings

Running strict `load_histdata_m1_csv(path)` on the real USDJPY HistData file failed with:

    ValueError: HistData M1 CSV at ... has duplicate timestamps.

This was correct protective behavior.

Duplicate diagnostics were then run on both real files.

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
- But this is an observation, not acceptance.
- HistData remains not accepted.

## Completed HistData Phases Since HANDOFF_23

### Phase 3.26-c - Run HistData loader on real files with explicit drop_exact policy and document result

Commits:

    908f3ab Document HistData drop_exact real-file check
    bba281a Fix HistData drop_exact check markdown formatting

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_DROP_EXACT_REAL_FILE_CHECK.md

Purpose:

1. Run `load_histdata_m1_csv(..., duplicate_policy="drop_exact")` on both real local HistData files.
2. Confirm exact duplicate metadata matches prior diagnostics.
3. Confirm canonical output is UTC, monotonic, duplicate-free, and structurally valid.
4. Record missing-minute counts and first/last missing minutes.
5. Do not write derived files.
6. Do not run H017.
7. Do not accept HistData.

Result summary:

USDJPY:

    n_input_rows: 1808731
    n_bars: 1808431
    earliest_utc: 2021-01-03 17:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 816687
    zero_volume_rows: 1808431
    index UTC: True
    monotonic: True
    duplicates after load: False
    bad OHLC rows: 0
    negative volume rows: 0

XAUUSD:

    n_input_rows: 1726549
    n_bars: 1726249
    earliest_utc: 2021-01-03 18:00:00+00:00
    latest_utc: 2025-12-31 16:57:00+00:00
    duplicate_policy: drop_exact
    n_duplicate_rows_removed: 300
    n_duplicate_timestamp_values: 300
    n_missing_minutes: 898809
    zero_volume_rows: 1726249
    index UTC: True
    monotonic: True
    duplicates after load: False
    bad OHLC rows: 0
    negative volume rows: 0

### Phase 3.26-d - Create derived-data provenance plan before writing canonical HistData outputs

Commit:

    f09917b Add HistData derived-data provenance plan

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_DERIVED_DATA_PROVENANCE_PLAN.md

Purpose:

1. Document rules before any cleaned/canonical HistData files are written.
2. Preserve raw-data immutability.
3. Define metadata required for any future derived files.
4. Keep derived large files out of git.
5. Prevent silent vendor-data mutation.
6. Do not run H017.
7. Do not accept HistData.

Key rule:

Future derived HistData files should live under:

    C:\Users\equin\Documents\institutional-ea\data\derived\histdata_m1\

They remain gitignored by `/data/`.

No derived files have been written yet.

### Phase 3.26-e - HistData M1 coverage and session analysis plan

Commit:

    2f600cf Add HistData coverage and session analysis plan

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_COVERAGE_SESSION_ANALYSIS_PLAN.md

Purpose:

1. Plan how to interpret large missing-minute counts.
2. Separate expected non-trading minutes from suspicious missing trading minutes.
3. Keep analysis read-only.
4. Do not run H017.
5. Do not accept HistData.

### Phase 3.26-f - Run and document first coverage/session diagnostic

Commit:

    7dbe4f2 Document HistData coverage and session analysis

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_COVERAGE_SESSION_ANALYSIS.md

Read-only diagnostic result:

USDJPY:

    naive full-range coverage: 68.889513 percent
    naive missing minutes: 816687
    provisional weekend missing minutes: 674547
    provisional non-weekend missing minutes: 142140
    missing weekend pct of missing: 82.595535 percent
    n_missing_gaps: 7609
    daily max observed bars: 1440

XAUUSD:

    naive full-range coverage: 65.760414 percent
    naive missing minutes: 898809
    provisional weekend missing minutes: 688151
    provisional non-weekend missing minutes: 210658
    missing weekend pct of missing: 76.56254 percent
    n_missing_gaps: 2181
    daily max observed bars: 1380

Cross-symbol missing overlap:

    USDJPY_missing_minutes: 816687
    XAUUSD_missing_minutes: 898809
    overlapping_missing_minutes: 790807
    USDJPY_only_missing_minutes: 25880
    XAUUSD_only_missing_minutes: 108002
    overlap_pct_of_USDJPY_missing: 96.831099
    overlap_pct_of_XAUUSD_missing: 87.983876

Key interpretation:

1. Large naive missing-minute counts are mostly weekend/closure/session related.
2. XAUUSD has a strong 17:00 UTC missingness signature.
3. 2023 is abnormal for both symbols.
4. HistData remains not accepted.

### Phase 3.26-g - Focused HistData 2023 and session-break analysis

Commit:

    fc97826 Document HistData focused 2023 session-break analysis

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_FOCUSED_2023_SESSION_BREAK_ANALYSIS.md

Purpose:

1. Focus on elevated 2023 missingness.
2. Classify USDJPY short non-weekend gaps.
3. Confirm XAUUSD recurring 17:00 UTC break pattern.
4. Summarize suspicious non-weekend gaps.
5. Continue avoiding H017 and derived-data writes.

Compact diagnostic findings:

USDJPY:

    n_missing_minutes: 816687
    n_missing_gaps: 7609
    n_non_weekend_gaps: 6359
    n_non_weekend_gaps_longer_than_60_minutes: 93

USDJPY non-weekend gap duration buckets:

    1 minute: 4385
    2 minutes: 723
    3-5 minutes: 522
    6-15 minutes: 48
    16-60 minutes: 588
    61-240 minutes: 86
    241-1440 minutes: 6
    >1440 minutes: 1

USDJPY short non-weekend gaps:

    n_usdjpy_non_weekend_gaps: 6359
    n_usdjpy_short_non_weekend_gaps_duration_1_to_5: 5630
    pct_short_of_non_weekend_gaps: 88.535933

USDJPY short gap counts by duration:

    1 minute: 4385
    2 minutes: 723
    3 minutes: 339
    4 minutes: 137
    5 minutes: 46

USDJPY short gap counts by year:

    2021: 2657
    2022: 842
    2023: 494
    2024: 794
    2025: 843

USDJPY short gaps are concentrated around UTC hours:

    16 UTC: 852
    17 UTC: 2309
    18 UTC: 621

USDJPY longest non-weekend gaps included:

    2024-12-31 16:59:00+00:00 through 2025-01-01 17:03:00+00:00, duration 1445 minutes
    2021-05-31 00:00:00+00:00 through 2021-05-31 19:59:00+00:00, duration 1200 minutes
    2023-12-25 02:59:00+00:00 through 2023-12-25 17:03:00+00:00, duration 845 minutes
    2024-12-25 03:00:00+00:00 through 2024-12-25 17:03:00+00:00, duration 844 minutes
    2025-12-25 02:59:00+00:00 through 2025-12-25 16:59:00+00:00, duration 841 minutes

XAUUSD:

    n_missing_minutes: 898809
    n_missing_gaps: 2181
    n_non_weekend_gaps: 1895
    n_non_weekend_gaps_longer_than_60_minutes: 165

XAUUSD non-weekend gap duration buckets:

    1 minute: 279
    2 minutes: 27
    3-5 minutes: 17
    6-15 minutes: 3
    16-60 minutes: 1404
    61-240 minutes: 151
    241-1440 minutes: 11
    >1440 minutes: 3

XAUUSD non-weekend gaps by year:

    2021: 234
    2022: 259
    2023: 919
    2024: 253
    2025: 230

XAUUSD 17:00 UTC break candidate summary:

    n_calendar_days_checked: 1822
    n_full_60_minute_17utc_break_days: 1742
    n_partial_17utc_break_days: 6
    n_no_17utc_break_days: 74

XAUUSD 17:00 UTC break by year:

    2021: 347 full, 0 partial, 15 no break
    2022: 350 full, 2 partial, 13 no break
    2023: 354 full, 1 partial, 10 no break
    2024: 347 full, 2 partial, 17 no break
    2025: 344 full, 1 partial, 19 no break

Exact XAUUSD gap rows starting at 17:00, lasting 60 minutes, ending 17:59:

    total: 866
    2021: 188
    2022: 187
    2023: 136
    2024: 180
    2025: 175

Interpretation:

XAUUSD has a strong, stable 17:00 UTC session-break signature. It should likely be treated as a metals session break candidate, not as suspicious missingness by itself.

XAUUSD longest non-weekend gaps included:

    2025-12-24 13:44:00+00:00 through 2025-12-25 18:03:00+00:00, duration 1700 minutes
    2024-12-24 13:44:00+00:00 through 2024-12-25 17:59:00+00:00, duration 1696 minutes
    2024-12-31 16:58:00+00:00 through 2025-01-01 17:59:00+00:00, duration 1502 minutes
    2021-05-31 00:00:00+00:00 through 2021-05-31 19:59:00+00:00, duration 1200 minutes
    2023-07-12 12:00:00+00:00 through 2023-07-12 17:59:00+00:00, duration 360 minutes

## 2023 Anomaly Findings

2023 daily count summary:

USDJPY 2023:

    total_observed_bars: 322896
    mean_daily_bars: 884.647
    median_daily_bars: 1019.0
    zero_bar_days: 54
    days_over_1000: 229
    max_daily_bars: 1440

USDJPY 2023 monthly observed bars:

    January: 31883
    February: 25606
    March: 22987
    April: 19952
    May: 23229
    June: 22033
    July: 22213
    August: 33036
    September: 29645
    October: 32075
    November: 31535
    December: 28702

XAUUSD 2023:

    total_observed_bars: 308752
    mean_daily_bars: 845.896
    median_daily_bars: 1018.0
    zero_bar_days: 56
    days_over_1000: 189
    max_daily_bars: 1380

XAUUSD 2023 monthly observed bars:

    January: 28914
    February: 24746
    March: 22608
    April: 19311
    May: 22586
    June: 21412
    July: 21350
    August: 31674
    September: 28330
    October: 30764
    November: 29824
    December: 27233

2023 missing overlap:

    USDJPY_2023_missing_minutes: 202704
    XAUUSD_2023_missing_minutes: 216848
    overlap_2023_missing_minutes: 181172
    USDJPY_only_2023_missing_minutes: 21532
    XAUUSD_only_2023_missing_minutes: 35676
    overlap_pct_of_USDJPY_2023_missing: 89.377615
    overlap_pct_of_XAUUSD_2023_missing: 83.547923

2023 overlapping missing minutes by month:

    January: 12757
    February: 13331
    March: 18061
    April: 19346
    May: 17808
    June: 16066
    July: 18647
    August: 11581
    September: 13509
    October: 12507
    November: 11628
    December: 15931

2023 USDJPY-only missing minutes by month:

    February: 1383
    March: 3592
    April: 3902
    May: 3603
    June: 5101
    July: 3780
    August: 23
    September: 46
    October: 58
    November: 37
    December: 7

2023 XAUUSD-only missing minutes by month:

    January: 2969
    February: 2243
    March: 3971
    April: 4543
    May: 4246
    June: 5722
    July: 4643
    August: 1385
    September: 1361
    October: 1369
    November: 1748
    December: 1476

Interpretation:

1. The elevated 2023 issue is concentrated most strongly from March through July.
2. Both symbols improve markedly from August 2023 onward.
3. The 2023 issue is mostly cross-symbol, not isolated to one instrument.
4. March through July 2023 have elevated missingness in both symbols and elevated symbol-specific missingness.
5. This suggests a source-wide or session-definition issue during that period, not merely normal XAUUSD metals breaks.
6. This is a major unresolved source-quality blocker.

## Current HistData Status

HistData is not accepted as a research source yet.

Completed:

1. Raw files inventoried.
2. Dedicated loader added.
3. Loader tests added.
4. Loader real-file duplicate failure documented.
5. Duplicate handling decision record added.
6. Explicit `drop_exact` policy added and tested.
7. Real-file `drop_exact` loader output documented.
8. Derived-data provenance plan documented.
9. Coverage/session analysis plan documented.
10. First coverage/session analysis documented.
11. Focused 2023/session-break analysis documented.

Not completed:

1. Focused March-July 2023 anomaly investigation.
2. Explicit holiday and special-closure classification.
3. Source-session reconciliation.
4. Broker mismatch assessment versus Exness.
5. H4 construction decision.
6. Final HistData source acceptance/rejection decision.
7. H017 validation using HistData.

Do not run H017 on HistData yet.

## Recommended Next Sub-Phase

Recommended next sub-phase:

    Phase 3.26-h - Focused March-July 2023 HistData anomaly investigation

Purpose:

1. identify whether the March-July 2023 issue is source-wide,
2. list the largest 2023 non-weekend gaps,
3. compare daily observed bar counts before, during, and after the anomaly,
4. classify whether gaps look like systematic source outages, holiday/special closures, or session-definition artifacts,
5. decide whether this anomaly blocks future source acceptance,
6. continue avoiding H017 and derived-data writes.

This should be a read-only diagnostic first.

Do not write reusable code yet unless the diagnostic logic becomes clearly valuable and testable.

Do not write derived data files.

Do not run H017.

Do not accept HistData.

## Suggested Read-Only Diagnostic Direction For Phase 3.26-h

After hygiene verification, design a compact read-only PowerShell here-string script that:

1. Loads both HistData files with `duplicate_policy="drop_exact"`.
2. Inspects the loader API using `inspect.signature(...)`.
3. Builds missing-minute indexes.
4. Groups consecutive missing minutes into gaps.
5. Applies the provisional weekend rule:
   Friday 22:00 UTC through Sunday 21:59 UTC.
6. Focuses on dates from:
   2023-03-01 through 2023-07-31.
7. Reports, for each symbol:
   - total observed bars by month,
   - total missing minutes by month,
   - non-weekend missing gaps by month,
   - top 50 longest non-weekend gaps in this window,
   - daily observed bar counts in this window,
   - days with unusually low observed bars,
   - cross-symbol overlapping missing gaps or missing minutes,
   - whether gaps cluster at specific UTC hours.
8. Compares against control periods:
   - 2023-01-01 through 2023-02-28,
   - 2023-08-01 through 2023-12-31,
   - same months in 2021, 2022, 2024, and 2025 if output remains compact.
9. Ends with:
   - no raw files modified,
   - no derived files written,
   - H017 not run,
   - HistData not accepted.

Keep output compact enough for the user to paste.

## Absolute Do-Not Rules At HANDOFF_24

Do not:

1. Do not run H017 validation on HistData yet.
2. Do not combine HistData M1 with Exness H4 silently.
3. Do not tune H017.
4. Do not change the cost model.
5. Do not commit raw HistData CSV files.
6. Do not call HistData files Dukascopy files.
7. Do not use the Dukascopy loader as the official HistData loader.
8. Do not accept HistData as a research source until loader validation, provenance, duplicate policy, coverage checks, 2023 anomaly investigation, broker mismatch assessment, and final decision are complete.
9. Do not change `.gitignore` from `/data/` to `data/`.
10. Do not start Phase 4 execution code.
11. Do not start live trading.
12. Do not ignore the `-33.65%` drawdown.
13. Do not broaden to more symbols yet.
14. Do not add machine learning yet.
15. Do not continue development while local commits are unpushed.
16. Do not let `git status` go unread.
17. Do not use Linux/macOS shell syntax in PowerShell.
18. Do not silently deduplicate vendor data.
19. Do not modify raw HistData files.
20. Do not write derived data files before source acceptance and a specific derived-data write phase.
21. Do not treat the 2023 March-July anomaly as harmless without evidence.
22. Do not treat the XAUUSD 17:00 UTC break as accepted broker-equivalent behavior until source-session reconciliation is complete.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

1. `.gitignore` once had unrooted `data/`, which risked excluding `quantcore/data/`.
2. Some older commits missed files because `git add` was incomplete.
3. An empty `HANDOFF_16.md` was accidentally committed once; verify handoff file size and preview before committing.
4. Markdown code fences have been damaged by paste before; this handoff intentionally avoids triple-backtick fences.
5. PowerShell does not support Linux heredocs.
6. VS Code can keep unsaved buffers that overwrite edits.
7. If terminal output shows command echo ambiguity, verify with `Select-String` or file previews before proceeding.
8. Always run tests.
9. Always inspect `git status`.
10. Always push commits.
11. Always verify `git ls-files` after commits.
12. Treat test-count drops as regressions.
13. If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after Phase 3.26-g and HANDOFF_24.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is `514 passed`.
3. Latest expected handoff commit is `Add handoff document #24 after HistData focused 2023 analysis`.
4. Latest expected project commit before the handoff is `fc97826 Document HistData focused 2023 session-break analysis`.
5. HistData raw files are inventoried but not accepted as a research source.
6. The raw HistData files are under `C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples`, which is a misleading folder name.
7. The dedicated HistData loader exists at `quantcore\data\histdata_loader.py`.
8. The loader supports strict default `duplicate_policy="reject"`.
9. The loader also supports explicit opt-in `duplicate_policy="drop_exact"`.
10. Conflicting duplicate timestamp groups remain fatal.
11. Raw files must not be modified or committed.
12. No derived HistData files have been written.
13. H017 is alive but not promotable.
14. Do not run H017 validation on HistData yet.
15. The XAUUSD 17:00 UTC break pattern is documented but not yet source-accepted.
16. The March-July 2023 HistData anomaly remains a major unresolved blocker.
17. The next logical sub-phase is Phase 3.26-h: focused March-July 2023 HistData anomaly investigation.
18. First task is hygiene verification only. No new code yet.

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
