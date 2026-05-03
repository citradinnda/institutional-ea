# HANDOFF 31 - Continuation After Strict H017 Event Wrapper

If any older handoff conflicts with this file, HANDOFF_31 wins.

## Identity and Operating Mode

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The project goal is a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade validation on a retail stack.

Environment:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
- No WSL
- No Linux/macOS shell assumptions

Repository:

    C:\Users\equin\Documents\institutional-ea

Virtual environment:

    C:\Users\equin\Documents\institutional-ea\.venv

Branch:

    main

Remote:

    https://github.com/citradinnda/institutional-ea.git

## Non-Negotiable Workflow Rules

1. Step-by-step.
2. One sub-phase per response.
3. Always use Windows PowerShell commands.
4. Never use Linux heredocs like `python - <<'PY'`.
5. Use PowerShell here-strings instead:

       @'
       python code
       '@ | python -

6. Never write code without saying exactly where the file goes and how to run it.
7. Always inspect APIs before calling internal functions:

       inspect.signature(...)
       dataclasses.fields(...)

8. Always read `git status` before and after work.
9. Never continue while local commits are unpushed.
10. Run focused tests where applicable.
11. Always run full `pytest -q`.
12. If tests pass but the count drops, treat it as a regression.
13. Always commit and push each completed sub-phase.
14. Always verify touched tracked files with `git ls-files`.
15. Do not propose switching to another AI chat unless the user asks.

After each response, offer exactly:

    ✅ done
    ⚠️ error — paste it
    🤔 question

## Current Repository State

Latest expected commit before this handoff is committed:

    06de306 Add strict H017 event wrapper

Expected latest commit after this handoff is committed:

    Add handoff document #31 after strict H017 event wrapper

Recent commits:

    06de306 Add strict H017 event wrapper
    0c56c8d Document strict bridge-window contiguity diagnostic
    72ae6c1 Document strict bridge-window real-data preflight result
    56dcc56 Add strict common bridge-window preflight
    cdca565 Add handoff document #30 after expanded broker-native H017 preflight plan
    671c347 Document expanded broker-native H017 validation preflight plan

Current full-test anchor:

    532 passed

Test-count history:

- HANDOFF_30 started around `514 passed`.
- `56dcc56 Add strict common bridge-window preflight` added 9 tests, raising to `523 passed`.
- `06de306 Add strict H017 event wrapper` added 9 tests, raising to `532 passed`.
- If tests pass but drop below 532 without an explicit test-removal phase, stop.

## Immediate First Action for Next AI

Do not write code first.

Ask the user to run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -15
    pytest -q

Expected after this handoff is committed and pushed:

- clean working tree
- branch up to date with `origin/main`
- latest commit: `Add handoff document #31 after strict H017 event wrapper`
- previous commit: `06de306 Add strict H017 event wrapper`
- tests: `532 passed`

Read the output before continuing.

## Raw Data and Gitignore Rules

The repo uses root-anchored:

    /data/

Do not change it to unanchored:

    data/

Reason: unanchored `data/` can accidentally exclude `quantcore/data/`.

Raw broker files are local and gitignored:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

Do not commit raw data.

Do not modify raw broker/vendor files.

Do not write derived datasets unless explicitly authorized.

## Key Project Status

H017 status:

- alive
- not promotable
- not ready for live trading
- not yet validated on the expanded broker-native source

Do not:

1. Do not tune H017.
2. Do not change H017 parameters.
3. Do not change the cost model.
4. Do not add symbols.
5. Do not add ML.
6. Do not start Phase 4 execution.
7. Do not live trade.
8. Do not use HistData for H017 validation.
9. Do not run old scripts as expanded validation unless strict rules are enforced.

Old short broker-native smoke result, not validation:

    fills=470
    ending_equity_usd=16145.60
    total_return_pct=61.46
    max_drawdown_pct=-33.65
    annualized_sharpe=1.3218
    PSR=0.8662
    H017 promotable=False

Interpretation:

- pipeline worked,
- sample was too short,
- return is not validated edge,
- drawdown is a serious risk signal.

## Broker Data State

Broker:

    Exness demo MT5

Symbols reported:

    USDJPYm
    XAUUSDm

Loader timezone:

    Europe/Athens

Meaning:

- winter UTC+2
- summer UTC+3
- DST-aware

MT5 loader API:

    load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

Loaded bars shape:

- pandas DataFrame
- timezone-aware UTC DatetimeIndex
- columns: `open`, `high`, `low`, `close`, `volume`

Expanded broker-native diagnostic counts:

USDJPY M1:

    rows/bars: 1785312
    earliest UTC: 2018-07-02 21:00:00+00:00
    latest UTC: 2026-04-30 07:00:00+00:00

USDJPY H4:

    rows/bars: 8713
    earliest UTC: 2018-07-02 21:00:00+00:00
    latest UTC: 2026-04-30 05:00:00+00:00

XAUUSD M1:

    rows/bars: 1704907
    earliest UTC: 2018-06-27 21:00:00+00:00
    latest UTC: 2026-04-30 07:00:00+00:00

XAUUSD H4:

    rows/bars: 8658
    earliest UTC: 2018-06-27 21:00:00+00:00
    latest UTC: 2026-04-30 05:00:00+00:00

Important data-quality facts:

- 2018 through 2021-06 is sparse/daily-like prefix.
- Dense M1 candidate region starts 2021-07.
- Do not treat 2018 through 2021-06 as dense M1 history.
- Do not impute M1.
- Do not forward-fill/backfill M1.
- Do not synthesize M1 bars.

## Expanded Broker-Native Source Acceptance

Expanded broker-native USDJPY and XAUUSD M1/H4 is conditionally accepted for future H017 validation only under strict complete-window rules.

Accepted future validation range:

    first accepted bridge window UTC: 2021-07-02 13:00:00+00:00
    last accepted bridge window UTC: 2026-04-30 01:00:00+00:00

Accepted future bridge-window count:

    5476

Strict bridge-window rule:

A timestamp is accepted only if:

1. USDJPY has H4 bar at timestamp.
2. XAUUSD has H4 bar at same timestamp.
3. USDJPY next H4 timestamp is exactly 4 hours later.
4. XAUUSD next H4 timestamp is exactly 4 hours later.
5. USDJPY M1 window `[timestamp, timestamp + 4 hours)` has exactly 240 bars.
6. XAUUSD M1 window `[timestamp, timestamp + 4 hours)` has exactly 240 bars.
7. No imputation/forward-fill/backfill/synthetic bars.
8. HistData is not used.

## HistData Status

HistData remains rejected for H017 validation.

Not allowed:

- H017 validation on HistData
- accepting HistData as research source
- HistData-built H4 validation
- broker H4 + HistData M1 hybrid
- silent deduplication
- raw file modification
- raw file commit

Allowed only:

- explicitly planned diagnostics
- documentation
- source-quality comparison

## Important Code Paths

Data:

    quantcore\data\mt5_loader.py
    quantcore\data\preflight.py
    quantcore\data\coverage.py
    quantcore\data\bridge_windows.py

Strategy:

    quantcore\strategy\h017.py
    quantcore\strategy\h017_claim.py

Backtest:

    quantcore\backtest\h017_event.py
    quantcore\backtest\h017_strict_event.py
    quantcore\backtest\fill_engine.py
    quantcore\backtest\portfolio.py
    quantcore\backtest\cost_model.py

Tests:

    tests\test_bridge_windows.py
    tests\test_h017_event.py
    tests\test_h017_strict_event.py
    tests\test_h017.py
    tests\test_h017_claim.py
    tests\test_mt5_loader.py

Old real scripts:

    scripts\run_h017_event_real.py
    scripts\run_h017_real.py

Do not run `scripts\run_h017_event_real.py` as expanded validation. It does not enforce the strict 5476-window rule.

## Work Completed Since HANDOFF_30

### Phase 3.26-am - Strict complete-window preflight/filter

Commit:

    56dcc56 Add strict common bridge-window preflight

Added:

    quantcore\data\bridge_windows.py
    tests\test_bridge_windows.py

Full tests:

    523 passed

API:

    assess_common_complete_h4_m1_windows(
        *,
        usdjpy_h4,
        xauusd_h4,
        usdjpy_m1,
        xauusd_m1,
        expected_m1_bars_per_h4=240,
        expected_h4_delta=pd.Timedelta(hours=4),
    ) -> CommonCompleteBridgeWindowAssessment

Dataclasses:

    BridgeWindowRejectionCount
    CommonCompleteBridgeWindowAssessment

Behavior:

- pure function
- accepts already-loaded DataFrames
- requires timezone-aware UTC DatetimeIndex
- requires sorted ascending
- rejects duplicates
- requires OHLC columns
- finds common H4 timestamps
- requires next H4 exactly +4h per symbol
- requires exactly 240 M1 bars per symbol in `[timestamp, timestamp + 4h)`
- returns accepted timestamps and diagnostics
- writes no files
- runs no strategy

### Real-data strict bridge-window preflight

Read-only diagnostic confirmed:

    candidate_common_h4_count: 8654
    usdjpy_complete_count: 5685
    xauusd_complete_count: 6149
    common_complete_count: 5476
    accepted_count: 5476
    first_accepted_timestamp: 2021-07-02 13:00:00+00:00
    last_accepted_timestamp: 2026-04-30 01:00:00+00:00
    usdjpy_only_complete_count: 209
    xauusd_only_complete_count: 673
    rejected_count: 3178

Rejection counts:

    usdjpy_m1_count_not_expected: 2969
    usdjpy_missing_next_h4_timestamp: 1
    usdjpy_non_4h_next_h4_delta: 1179
    xauusd_m1_count_not_expected: 2505
    xauusd_missing_next_h4_timestamp: 1
    xauusd_non_4h_next_h4_delta: 1193

No H017 run was performed.

### Phase 3.26-an - Document strict real-data preflight result

Commit:

    72ae6c1 Document strict bridge-window real-data preflight result

Added:

    docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT.md
    docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_PREFLIGHT_RESULT_OUTPUT.txt

Full tests:

    523 passed

### Phase 3.26-ao - Contiguity diagnostic

Commit:

    0c56c8d Document strict bridge-window contiguity diagnostic

Added:

    docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC.md
    docs\operations\BROKER_NATIVE_EXPANDED_STRICT_BRIDGE_WINDOW_CONTIGUITY_DIAGNOSTIC_OUTPUT.txt

Full tests:

    523 passed

Critical result:

    accepted_count: 5476
    adjacent_deltas_checked: 5475
    four_hour_adjacent_deltas: 4148
    non_four_hour_adjacent_deltas: 1327

Implication:

Do not implement strict validation by simply filtering H4 to accepted timestamps.

Reason:

The event engine uses adjacent H4/H017 rows:

    decision_time = index[i - 1]
    entry_time = index[i]
    forced_exit_time = index[i + 1]

If H4 is filtered to accepted timestamps only, the next retained timestamp may be 8 hours, 12 hours, weekend gap, or more later, causing wrong forced exits.

Future runner must preserve native H4 interval semantics and execute only intervals where:

    entry_time in accepted_entry_times
    forced_exit_time == entry_time + 4 hours

### Phase 3.26-ap - Strict H017 event wrapper

Commit:

    06de306 Add strict H017 event wrapper

Added/modified:

    quantcore\backtest\h017_strict_event.py
    tests\test_h017_strict_event.py
    quantcore\backtest\__init__.py

Focused tests:

    9 passed

Related tests:

    19 passed

Full tests:

    532 passed

New dataclass:

    StrictH017EventBacktestResult

Fields:

    backtest
    accepted_entry_times
    executed_entry_times
    skipped_entry_times
    accepted_entry_count
    executed_entry_count
    skipped_entry_count
    expected_h4_delta

New APIs:

    backtest_h017_strict_event_driven(...)
    backtest_h017_strict_event_from_result(...)

Behavior:

- preserves native H4/H017 index
- runs/accepts H017Result
- for each event interval:
  - decision_time = index[i - 1]
  - entry_time = index[i]
  - forced_exit_time = index[i + 1]
- executes only if:
  - entry_time is in accepted_entry_times
  - forced_exit_time - entry_time == expected_h4_delta
- otherwise forces the decision exposure flat by zeroing positions at the relevant decision_time
- calls existing `backtest_h017_event_from_result(...)`
- does not modify original event engine
- synthetic tests only
- no real-data validation run yet

Package exports updated with:

    StrictH017EventBacktestResult
    backtest_h017_strict_event_driven
    backtest_h017_strict_event_from_result

## Current API Snapshot

Strict bridge preflight:

    quantcore.data.bridge_windows.assess_common_complete_h4_m1_windows(...)

Strict event wrapper:

    quantcore.backtest.h017_strict_event.backtest_h017_strict_event_driven(...)
    quantcore.backtest.h017_strict_event.backtest_h017_strict_event_from_result(...)

Existing event engine:

    quantcore.backtest.h017_event.backtest_h017_event_driven(...)
    quantcore.backtest.h017_event.backtest_h017_event_from_result(...)

H017 strategy:

    quantcore.strategy.h017.run_h017(...)

Claim:

    quantcore.strategy.h017_claim.build_h017_claim(...)

Before using any of these in new code, inspect exact signatures again.

## Recommended Next Path

Next logical sub-phase:

    Phase 3.26-aq - strict expanded broker-native validation runner preflight/design inspection

Do not run H017 immediately.

First do read-only inspection of:

    quantcore\backtest\h017_strict_event.py
    tests\test_h017_strict_event.py
    quantcore\data\bridge_windows.py
    scripts\run_h017_event_real.py
    quantcore\strategy\h017_claim.py

Then design a new strict real-data validation script, likely:

    scripts\run_h017_strict_event_real.py

The script should:

1. Load four broker-native MT5 exports.
2. Run `assess_common_complete_h4_m1_windows(...)`.
3. Assert:
       accepted_count == 5476
       first_accepted_timestamp == 2021-07-02 13:00:00+00:00
       last_accepted_timestamp == 2026-04-30 01:00:00+00:00
4. Preserve native H4 data, not H4 filtered only to accepted timestamps.
5. Pass `assessment.accepted_timestamps` as accepted entry times to `backtest_h017_strict_event_driven(...)`.
6. Build H017 claim from the strict wrapper backtest returns.
7. Print:
   - loader summaries
   - strict bridge-window assessment
   - strict executed/skipped counts
   - backtest summary
   - claim summary
   - explicit verdict that H017 is not automatically promotable
8. Do not write derived datasets.
9. Do not change H017 parameters.
10. Do not change cost model.

However, before implementing the script, consider adding tests for any reusable formatting/helper functions if they are put into a module. If it remains a manual script only, use careful read-only API inspection first.

## Absolute Do-Not Rules

Do not:

1. Do not run expanded H017 validation until the next AI confirms hygiene and reviews the strict wrapper.
2. Do not use old `scripts\run_h017_event_real.py` as expanded validation.
3. Do not filter H4 to accepted timestamps only.
4. Do not include incomplete H4/M1 windows.
5. Do not use windows with fewer or more than exactly 240 M1 bars per symbol.
6. Do not impute.
7. Do not forward-fill.
8. Do not backfill.
9. Do not synthesize bars.
10. Do not use HistData for validation.
11. Do not tune H017.
12. Do not change H017 parameters.
13. Do not change the cost model.
14. Do not broaden to more symbols.
15. Do not add ML.
16. Do not modify raw broker files.
17. Do not commit raw data.
18. Do not write derived datasets without authorization.
19. Do not start live trading.
20. Do not ignore the prior -33.65 percent drawdown.
21. Do not continue while commits are unpushed.
22. Do not skip full pytest.
23. Do not allow test count below 532 without explicit test-removal phase.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after HANDOFF_31.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is `532 passed`.
3. Latest expected commit is `Add handoff document #31 after strict H017 event wrapper`.
4. Previous expected commit is `06de306 Add strict H017 event wrapper`.
5. Strict bridge-window preflight exists in `quantcore/data/bridge_windows.py`.
6. Real-data strict preflight confirmed exactly `5476` accepted windows from `2021-07-02 13:00:00+00:00` through `2026-04-30 01:00:00+00:00`.
7. Accepted timestamps are not contiguous enough to filter H4 directly.
8. Strict event wrapper exists in `quantcore/backtest/h017_strict_event.py`.
9. The wrapper preserves native H4/H017 index and executes only accepted +4h entry intervals.
10. H017 is still alive but not promotable.
11. No old real-data event script should be used as expanded validation.
12. Do not tune H017, change cost model, use HistData, or live trade.
13. First task is hygiene verification only.

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
