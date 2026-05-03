# HANDOFF 26 - Self-Contained Continuation After Broker H4/M1 Preflight

You are continuing an existing project. Read this entire handoff before responding.

This handoff is intentionally self-contained enough for a new AI to continue safely.

If any older handoff conflicts with this file, this HANDOFF_26 wins.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is not a professional developer. They are building infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, and poor risk control.

The project goal is to build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research: Python `quantcore`
- Execution: MetaTrader 5 later
- Production target: Oracle Cloud Always Free VPS later
- Monitoring: self-hosted free-tier stack later
- Current machine: Windows, PowerShell, VS Code, Python 3.12.10 in `.venv`

Do not rush into strategy validation or live trading. The project is still in data infrastructure / research-validation work.

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
13. For documentation-only phases, it is okay to provide one consolidated PowerShell block, as long as it includes status, tests, commit, push, final status, `git ls-files`, and recent log.
14. For code or diagnostics, be more cautious: inspect APIs first and split if needed.

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
7. Run `git ls-files <touched-dirs>/` or `git ls-files <touched-file>`.
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

    82c68fa Document broker H4 M1 alignment preflight

Expected latest commit after this handoff is committed:

    Add handoff document #26 after broker H4 M1 preflight

Recent commit context:

    82c68fa Document broker H4 M1 alignment preflight
    043de0d Add broker H4 M1 alignment diagnostic plan
    c85e49c Document H4 construction evidence requirements
    3539fa0 Add H4 construction decision plan
    8512edc Document broker mismatch assessment
    12988a6 Add broker mismatch assessment plan
    f3b576f Add handoff document #25 after broker short-window session diagnostic
    662a740 Document broker short-window session diagnostic
    889f0ba Add broker short-window session diagnostic plan
    e3c56b6 Document HistData weekly daily source session diagnostics

Known note:

There are two older consecutive commits with the message `Add handoff document #23 after HistData duplicate policy`. This is known and not blocking. Do not rewrite history.

Current full-test anchor:

    514 passed

Important test-count rule:

- Previous anchor after Phase 3.25 was `509 passed`.
- Phase 3.26-b deliberately added 5 HistData duplicate-policy tests.
- Current correct anchor is `514 passed`.
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

    Add handoff document #26 after broker H4 M1 preflight

Expected project commit before handoff:

    82c68fa Document broker H4 M1 alignment preflight

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

Recent important docs:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_PREFLIGHT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_DIAGNOSTIC_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_EVIDENCE_REQUIREMENTS.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\H4_CONSTRUCTION_DECISION_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_MISMATCH_ASSESSMENT.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_MISMATCH_ASSESSMENT_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_SHORT_WINDOW_SESSION_DIAGNOSTIC.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_SHORT_WINDOW_SESSION_DIAGNOSTIC_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_WEEKLY_DAILY_SOURCE_SESSION_DIAGNOSTICS.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_SOURCE_SESSION_RECONCILIATION_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_MARCH_JULY_2023_GAP_CANDIDATE_CLASSIFICATION.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_HOLIDAY_SPECIAL_CLOSURE_CLASSIFICATION_PLAN.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_MARCH_JULY_2023_ANOMALY_INVESTIGATION.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_FOCUSED_2023_SESSION_BREAK_ANALYSIS.md
    C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_COVERAGE_SESSION_ANALYSIS.md
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

MT5LoadResult fields verified in Phase 3.26-t preflight:

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

Current broker-native M1 coverage remains insufficient for research validation.

Known broker-native M1 coverage from latest short-window diagnostic:

USDJPY:

    n_bars: 97907
    earliest_utc: 2026-01-26 03:09:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    missing_minutes_inside_symbol_range: 37685

XAUUSD:

    n_bars: 97966
    earliest_utc: 2026-01-20 02:22:00+00:00
    latest_utc: 2026-04-30 07:00:00+00:00
    missing_minutes_inside_symbol_range: 46313

## Broker H4/M1 Preflight Completed

Document:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_ALIGNMENT_PREFLIGHT.md

Status:

- Preflight complete.
- Read-only.
- No HistData used.
- No H017 run.
- No derived data written.
- No raw files modified.

Broker raw files found:

USDJPY H4:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    size_bytes=548498
    last_write_time=05/03/2026 10:35:35

USDJPY M1:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    size_bytes=5978537
    last_write_time=05/03/2026 14:10:25

XAUUSD H4:

    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    size_bytes=594386
    last_write_time=05/03/2026 10:35:13

XAUUSD M1:

    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
    size_bytes=6556675
    last_write_time=05/03/2026 14:10:53

Raw preview showed MT5-style columns:

    <DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>

Important H4 preview caution:

The first two visible rows of both broker H4 files showed `00:00:00` on consecutive dates.

This may indicate one of several possibilities:

1. The preview only happened to show daily boundary rows.
2. The broker H4 export may have unusual timestamp spacing.
3. The file may not actually contain H4 bars despite the file name.
4. The export settings may have selected the wrong timeframe.
5. The loader or diagnostic must inspect timestamp deltas before assuming the timeframe.

Current status:

    Unresolved.

Required next check:

    Inspect loaded H4 timestamp deltas and time-of-day distribution for both symbols.

Do not assume the H4 files are valid H4 bars until this is checked.

## HistData Acquisition State

The user downloaded approximately five years of M1 data from HistData.

The original HistData files were preserved exactly as downloaded.

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

Focused HistData loader tests:

    20 passed

Full project test anchor:

    514 passed

## HistData Duplicate Findings

Running strict `load_histdata_m1_csv(path)` on the real USDJPY HistData file failed with:

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
- But this is an observation, not acceptance.
- HistData remains not accepted.

## HistData Status

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
12. March-July 2023 anomaly investigation documented.
13. Holiday and special-closure classification plan documented.
14. March-July 2023 gap candidate classification documented.
15. Source-session reconciliation plan documented.
16. Weekly/daily HistData source-session diagnostics documented.
17. Broker short-window session diagnostic plan documented.
18. Broker short-window session diagnostic documented.
19. Broker mismatch assessment plan documented.
20. Broker mismatch assessment documented.
21. H4 construction decision plan documented.
22. H4 construction evidence requirements documented.
23. Broker H4/M1 alignment diagnostic plan documented.
24. Broker H4/M1 alignment preflight documented.

Not completed:

1. Broker H4/M1 loaded-shape inspection.
2. Broker H4/M1 alignment diagnostic implementation.
3. Explicit holiday and special-closure final classification.
4. H4 construction decision.
5. Final HistData source acceptance/rejection decision.
6. H017 validation using HistData.

Do not run H017 on HistData yet.

## March-July 2023 HistData Anomaly Summary

March-July 2023 was materially abnormal for both symbols.

USDJPY March-July source-session comparison:

    2021 observed_pct: 70.299110, observed_bars: 154883, missing_minutes: 65437, full_missing_hour_days_all: 1060
    2022 observed_pct: 70.918664, observed_bars: 156248, missing_minutes: 64072, full_missing_hour_days_all: 1057
    2023 observed_pct: 50.115287, observed_bars: 110414, missing_minutes: 109906, full_missing_hour_days_all: 1828
    2024 observed_pct: 70.958606, observed_bars: 156336, missing_minutes: 63984, full_missing_hour_days_all: 1057
    2025 observed_pct: 71.042121, observed_bars: 156520, missing_minutes: 63800, full_missing_hour_days_all: 1050

XAUUSD March-July source-session comparison:

    2021 observed_pct: 67.450980, observed_bars: 148608, missing_minutes: 71712, full_missing_hour_days_all: 1195
    2022 observed_pct: 67.410585, observed_bars: 148519, missing_minutes: 71801, full_missing_hour_days_all: 1195
    2023 observed_pct: 48.686910, observed_bars: 107267, missing_minutes: 113053, full_missing_hour_days_all: 1883
    2024 observed_pct: 67.404230, observed_bars: 148505, missing_minutes: 71815, full_missing_hour_days_all: 1195
    2025 observed_pct: 67.517702, observed_bars: 148755, missing_minutes: 71565, full_missing_hour_days_all: 1191

Interpretation:

1. March-July 2023 is materially abnormal relative to same-month control years.
2. The anomaly affects both USDJPY and XAUUSD.
3. The anomaly is not explained by weekends alone.
4. The anomaly is not explained by the XAUUSD 17:00 UTC daily break alone.
5. It remains a major source-quality blocker.

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
5. Broker mismatch assessment is now an explicit HistData acceptance blocker.
6. The broker short window is useful for session inference but insufficient for research validation.
7. The broker window is 2026, while HistData is 2021-2025; this cannot prove historical broker equivalence.

## Broker Mismatch / H4 Decision State

Broker mismatch assessment result:

    HistData remains blocked for H017 validation.

Current source status:

    Not accepted.

Current allowed status:

    Exploratory diagnostics only.

Reason:

    Current evidence shows material mismatch between HistData source-session candidates and the broker-native 2026 short-window behavior. The mismatch affects weekly opens, weekly closes, XAUUSD daily breaks, cross-symbol alignment, H4 boundary construction, and M1 stop-resolution reliability.

Important caveat:

    The 2026 broker short-window evidence does not prove the broker's full 2021-2025 historical behavior. It does, however, establish enough current broker mismatch risk to block acceptance until more broker evidence and an H4 construction decision exist.

H4 construction decision state:

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
   - Not final yet.

## Current HistData Decision

HistData remains not accepted as a research source.

Do not use HistData for H017 validation yet.

Do not write derived HistData files yet.

Do not combine HistData M1 with broker H4 silently.

Do not build H4 bars from HistData yet.

Do not tune H017 to HistData.

## Recommended Next Sub-Phase

Recommended next sub-phase:

    Phase 3.26-u - Broker H4/M1 loaded-shape inspection

Purpose:

1. Load broker-native H4 and M1 CSVs using the verified MT5 loader API.
2. Inspect loaded DataFrame shape, columns, index, timestamp deltas, and time-of-day distribution.
3. Verify whether the files named H4 are actually H4-spaced.
4. Keep the diagnostic read-only.
5. Write no derived data.
6. Avoid HistData.
7. Avoid H017.
8. Commit a result document before implementing any reusable diagnostic script.

Important:

This is still not H017 validation. This is broker data-shape inspection only.

## Suggested Direction For Phase 3.26-u

After hygiene verification, run a compact read-only PowerShell here-string that:

1. Imports:
   - `inspect`
   - `dataclasses`
   - `collections.Counter`
   - `pathlib.Path`
   - `pandas as pd` if needed
   - `load_mt5_csv`
   - `MT5LoadResult`

2. Prints:
   - `inspect.signature(load_mt5_csv)`
   - dataclass fields of `MT5LoadResult`

3. Loads:
   - `data\raw\USDJPY\H4.csv`
   - `data\raw\USDJPY\M1.csv`
   - `data\raw\XAUUSD\H4.csv`
   - `data\raw\XAUUSD\M1.csv`

4. For each loaded result, prints:
   - symbol
   - timeframe label from file name
   - path
   - `n_input_rows`
   - `n_bars`
   - `earliest_utc`
   - `latest_utc`
   - `broker_tz`
   - DataFrame columns
   - index type
   - index timezone
   - first 5 rows
   - last 5 rows

5. For each loaded result, computes timestamp deltas:
   - `bars.index.to_series().diff().dropna()`
   - value counts for top deltas
   - minimum delta
   - median delta
   - maximum delta

6. For H4 files specifically, prints:
   - UTC time-of-day distribution
   - whether the dominant delta is 4 hours or not
   - whether many deltas are 1 day
   - a clear warning if the file appears daily rather than H4

7. Writes no files.

8. Does not load HistData.

9. Does not run H017.

After the read-only inspection, document the results in:

    C:\Users\equin\Documents\institutional-ea\docs\operations\BROKER_H4_M1_LOADED_SHAPE_INSPECTION.md

Then run full tests, commit, push, final status, and `git ls-files`.

## Absolute Do-Not Rules At HANDOFF_26

Do not:

1. Do not run H017 validation on HistData.
2. Do not combine HistData M1 with broker H4 silently.
3. Do not tune H017.
4. Do not change the cost model.
5. Do not commit raw HistData CSV files.
6. Do not commit raw MT5 CSV files.
7. Do not call HistData files Dukascopy files.
8. Do not use the Dukascopy loader as the official HistData loader.
9. Do not accept HistData as a research source until loader validation, provenance, duplicate policy, coverage checks, 2023 anomaly investigation, source-session reconciliation, broker mismatch assessment, H4 construction decision, and final decision are complete.
10. Do not change `.gitignore` from `/data/` to `data/`.
11. Do not start Phase 4 execution code.
12. Do not start live trading.
13. Do not ignore the `-33.65%` drawdown.
14. Do not broaden to more symbols yet.
15. Do not add machine learning yet.
16. Do not continue development while local commits are unpushed.
17. Do not let `git status` go unread.
18. Do not use Linux/macOS shell syntax in PowerShell.
19. Do not silently deduplicate vendor data.
20. Do not modify raw HistData files.
21. Do not modify raw MT5 files.
22. Do not write derived data files before source acceptance and a specific derived-data write phase.
23. Do not treat the 2023 March-July anomaly as harmless without evidence.
24. Do not treat the XAUUSD 17:00 UTC HistData break as accepted broker-equivalent behavior until broker compatibility is proven.
25. Do not treat the short 2026 broker window as enough for research validation.
26. Do not infer historical broker 2021-2025 sessions solely from 2026 broker exports.
27. Do not assume files named `H4.csv` are actually H4-spaced until timestamp deltas are inspected.

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

Understood. I am continuing after Phase 3.26-t and HANDOFF_26.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is `514 passed`.
3. Latest expected handoff commit is `Add handoff document #26 after broker H4 M1 preflight`.
4. Latest expected project commit before the handoff is `82c68fa Document broker H4 M1 alignment preflight`.
5. HistData raw files are inventoried but not accepted as a research source.
6. The raw HistData files are under `C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples`, which is a misleading folder name.
7. The dedicated HistData loader exists at `quantcore\data\histdata_loader.py`.
8. Raw files must not be modified or committed.
9. No derived HistData files have been written.
10. H017 is alive but not promotable.
11. Do not run H017 validation on HistData yet.
12. The March-July 2023 HistData anomaly remains a major unresolved blocker.
13. Broker mismatch assessment blocks HistData acceptance.
14. No H4 construction method is accepted yet.
15. Broker H4/M1 preflight found the expected raw broker files and verified the MT5 loader API.
16. The H4 file previews showed `00:00:00` on consecutive dates, so loaded timestamp deltas must be inspected before assuming the files are true H4.
17. The next logical sub-phase is Phase 3.26-u: broker H4/M1 loaded-shape inspection.
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
