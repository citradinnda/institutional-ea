# HANDOFF 23 - Self-Contained Continuation After HistData Duplicate Policy

You are continuing an existing project. Read this entire handoff before responding. Do not invent context. When in doubt, ask before writing code.

This HANDOFF_23 file is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_23 wins.

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

Current expected latest commit after this handoff is committed:

    Add handoff document #23 after HistData duplicate policy

Current expected project commit immediately before this handoff:

    c41943a Add explicit HistData exact duplicate policy

Recent expected commit context:

    c41943a Add explicit HistData exact duplicate policy
    6e53c9e Add HistData duplicate handling decision record
    e05025b Document HistData loader real-file duplicate check
    ccedcbb Add tested HistData M1 CSV loader
    ffe80ff Record HistData M1 acquisition inventory
    9588046 Add handoff document #21 after Dukascopy coverage plan
    de27e02 Add Dukascopy coverage check plan
    ef57b8c Document Dukascopy loader sample check
    36e6dc0 Add handoff document #20 after Dukascopy loader
    5a2bf46 Add tested Dukascopy CSV loader
    a0a3085 Add Dukascopy loader API inspection notes

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
    git log --oneline -12
    pytest -q

Expected status after this handoff is committed and pushed:

- On branch main
- Your branch is up to date with `origin/main`.
- nothing to commit, working tree clean

Expected latest commit:

    Add handoff document #23 after HistData duplicate policy

Expected project commit before handoff:

    c41943a Add explicit HistData exact duplicate policy

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

Do not commit large derived data files unless there is an explicit plan saying to do so. Current rule: do not commit raw or derived large data.

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

## Phase 3.24 Completed

Phase 3.24 name:

    Freeze and inventory HistData M1 acquisition

Files added:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_ACQUISITION_INVENTORY.md

Purpose:

1. Pivot from Dukascopy-only evaluation to HistData inventory.
2. Preserve distinction between HistData and Dukascopy.
3. Record file locations, sizes, SHA256 hashes, line counts, first lines, and last lines.
4. Avoid loading, backtesting, renaming, moving, or accepting the data before documentation.
5. Preserve raw-data non-commit rules.

## Phase 3.25 Completed

Phase 3.25 name:

    Inspect HistData raw format and design/add a dedicated tested HistData loader

Key commits:

    ccedcbb Add tested HistData M1 CSV loader
    e05025b Document HistData loader real-file duplicate check

Files added:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_LOADER_REAL_FILE_CHECK.md

Original Phase 3.25 focused test result:

    15 passed

Original full test result after Phase 3.25:

    509 passed

Purpose:

1. Add a dedicated HistData loader.
2. Support observed no-header comma-separated HistData format.
3. Preserve source identity as HistData.
4. Reject duplicate timestamps before canonicalization.
5. Reject non-monotonic timestamps before canonicalization.
6. Validate OHLC and volume.
7. Report missing minutes.
8. Keep timezone assumption explicit.
9. Do not accept HistData as a research source yet.

## Phase 3.25 Real-File Loader Check

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

## Phase 3.26-a Completed

Phase 3.26-a name:

    Create HistData duplicate-handling decision record

Commit:

    6e53c9e Add HistData duplicate handling decision record

File added:

    C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-003-histdata-duplicate-handling.md

Decision summary:

1. Raw HistData files must remain unchanged.
2. Strict duplicate rejection remains the default.
3. Silent deduplication is not allowed.
4. Conflicting duplicate timestamp groups are always fatal.
5. Exact duplicate OHLCV rows may be removed only through explicit audited handling.
6. Any duplicate-handling implementation must be tested and documented.
7. HistData remains unaccepted until duplicate handling, provenance, and coverage checks are complete.

## Phase 3.26-b Completed

Phase 3.26-b name:

    Add explicit tested exact-duplicate handling to the HistData loader

Commit:

    c41943a Add explicit HistData exact duplicate policy

Files updated:

    C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py
    C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py

Focused test result:

    20 passed

Full test result:

    514 passed

Purpose:

1. Keep strict default duplicate behavior.
2. Add explicit opt-in exact duplicate handling.
3. Reject conflicting duplicate timestamp groups.
4. Preserve audit metadata in the loader result.
5. Do not modify raw files.
6. Do not write derived files yet.
7. Do not run H017.
8. Do not accept HistData yet.

Updated public loader API:

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

Updated `HistDataM1LoadResult` fields:

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

Important tests added/updated:

1. Default metadata reports `duplicate_policy="reject"`.
2. Default policy rejects exact duplicates.
3. `drop_exact` removes identical duplicate rows.
4. `drop_exact` rejects conflicting duplicates.
5. Unknown duplicate policy is rejected.
6. `drop_exact` still rejects non-monotonic timestamps.
7. Frozen result dataclass includes new fields.

New correct full-test anchor:

    514 passed

## Current HistData Status

HistData is not accepted as a research source yet.

Completed:

1. Raw files inventoried.
2. Dedicated loader added.
3. Loader tests added.
4. Loader real-file duplicate failure documented.
5. Duplicate handling decision record added.
6. Explicit `drop_exact` policy added and tested.

Not completed:

1. Running loader on real files with `duplicate_policy="drop_exact"` and documenting output.
2. Derived-data provenance plan.
3. Missing-minute coverage analysis.
4. Weekend behavior analysis.
5. XAUUSD metals break behavior analysis.
6. Timezone/source-session reconciliation.
7. Broker mismatch assessment versus Exness.
8. Final source acceptance/rejection decision.
9. H017 validation using HistData.

## Recommended Next Sub-Phase

Recommended next sub-phase:

    Phase 3.26-c - Run HistData loader on real files with explicit drop_exact policy and document result

Purpose:

1. Run `load_histdata_m1_csv(..., duplicate_policy="drop_exact")` on both real local HistData files.
2. Confirm exact duplicate metadata matches prior diagnostics.
3. Confirm canonical output is UTC, monotonic, duplicate-free, and structurally valid.
4. Record missing-minute counts and first/last missing minutes.
5. Document results in an operations file.
6. Do not write derived files yet.
7. Do not run H017.
8. Do not accept HistData yet.

Suggested read-only command after hygiene:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1

    @'
    from pathlib import Path

    from quantcore.data.histdata_loader import load_histdata_m1_csv

    paths = [
        Path(r"C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv"),
        Path(r"C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv"),
    ]

    for path in paths:
        print()
        print("=" * 100)
        print("path:", path)
        print("exists:", path.exists())

        result = load_histdata_m1_csv(path, duplicate_policy="drop_exact")

        print("n_input_rows:", result.n_input_rows)
        print("n_bars:", result.n_bars)
        print("earliest_utc:", result.earliest_utc)
        print("latest_utc:", result.latest_utc)
        print("source_tz:", result.source_tz)
        print("duplicate_policy:", result.duplicate_policy)
        print("n_duplicate_rows_removed:", result.n_duplicate_rows_removed)
        print("n_duplicate_timestamp_values:", result.n_duplicate_timestamp_values)
        print("duplicate_timestamp_ranges:", result.duplicate_timestamp_ranges)
        print("n_missing_minutes:", result.n_missing_minutes)
        print("first_missing_minutes:", result.missing_minutes[:20])
        print("last_missing_minutes:", result.missing_minutes[-20:] if result.missing_minutes else ())
        print("columns:", list(result.bars.columns))
        print("tz:", result.bars.index.tz)
        print("is_monotonic_increasing:", result.bars.index.is_monotonic_increasing)
        print("has_duplicates:", result.bars.index.has_duplicates)
        print("non_positive_ohlc_rows:", int((result.bars[["open", "high", "low", "close"]] <= 0).any(axis=1).sum()))
        print("bad_ohlc_rows:", int((
            (result.bars["high"] < result.bars["open"])
            | (result.bars["high"] < result.bars["low"])
            | (result.bars["high"] < result.bars["close"])
            | (result.bars["low"] > result.bars["open"])
            | (result.bars["low"] > result.bars["high"])
            | (result.bars["low"] > result.bars["close"])
        ).sum()))
        print("negative_volume_rows:", int((result.bars["volume"] < 0).sum()))
        print("zero_volume_rows:", int((result.bars["volume"] == 0).sum()))
    '@ | python -

    git status

If successful, document in:

    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_DROP_EXACT_REAL_FILE_CHECK.md

Do not commit raw data.

## Absolute Do-Not Rules At HANDOFF_23

Do not:

1. Do not run H017 validation on HistData yet.
2. Do not combine HistData M1 with Exness H4 silently.
3. Do not tune H017.
4. Do not change the cost model.
5. Do not commit raw HistData CSV files.
6. Do not call HistData files Dukascopy files.
7. Do not use the Dukascopy loader as the official HistData loader.
8. Do not accept HistData as a research source until loader validation, provenance, duplicate policy, and coverage checks are complete.
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
20. Do not write derived data files before a documented derived-data provenance plan.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

1. `.gitignore` once had unrooted `data/`, which risked excluding `quantcore/data/`.
2. Some older commits missed files because `git add` was incomplete.
3. An empty `HANDOFF_16.md` was accidentally committed once; verify handoff file size and preview before committing.
4. Markdown code fences have been damaged by paste before; if a Markdown file is damaged, overwrite from the top.
5. PowerShell does not support Linux heredocs.
6. VS Code can keep unsaved buffers that overwrite edits.
7. If terminal output shows command echo ambiguity, verify with `Select-String` or file previews before proceeding.
8. Always run tests.
9. Always inspect `git status`.
10. Always push commits.
11. Always verify `git ls-files` after commits.
12. Treat test-count drops as regressions.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after Phase 3.26-b and HANDOFF_23.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is `514 passed`.
3. Latest expected handoff commit is `Add handoff document #23 after HistData duplicate policy`.
4. Latest expected project commit before the handoff is `c41943a Add explicit HistData exact duplicate policy`.
5. HistData raw files are inventoried but not accepted as a research source.
6. The raw HistData files are under `C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples`, which is a misleading folder name.
7. The dedicated HistData loader exists at `quantcore\data\histdata_loader.py`.
8. The loader supports strict default `duplicate_policy="reject"`.
9. The loader also supports explicit opt-in `duplicate_policy="drop_exact"`.
10. Conflicting duplicate timestamp groups remain fatal.
11. Raw files must not be modified or committed.
12. H017 is alive but not promotable.
13. Do not run H017 validation on HistData yet.
14. The next logical sub-phase is Phase 3.26-c: run the HistData loader on real files with explicit `drop_exact` policy and document the output.
15. First task is hygiene verification only. No new code yet.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -12
    pytest -q

Then paste the full output.

✅ done
⚠️ error — paste it
🤔 question
