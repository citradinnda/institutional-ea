# HANDOFF 23 - Superseding Update After HistData Duplicate Policy

You are continuing an existing project. Read this entire prompt before responding. Do not invent context. When in doubt, ask before writing code.

This HANDOFF_23 file is intentionally structured like prior handoffs:

1. This top section is the newest superseding update.
2. Older handoff files remain in the repository for complete history.
3. If any older detail conflicts with this HANDOFF_23 update, HANDOFF_23 wins.
4. Do not ignore older context; it contains project rules, strategy history, repo hygiene lessons, and do-not rules.

## Current Verified State At HANDOFF_23

Repository root:

- `C:\Users\equin\Documents\institutional-ea`

Virtual environment:

- `C:\Users\equin\Documents\institutional-ea\.venv`

Branch:

- `main`

GitHub remote:

- `https://github.com/citradinnda/institutional-ea.git`

Current expected latest commits after this handoff sequence:

1. `Add explicit HistData exact duplicate policy`
2. `Add handoff document #23 after HistData duplicate policy`

Current full-test anchor:

- `514 passed`

Important test-count rule:

- Previous full-test anchor after Phase 3.25 was `509 passed`.
- Phase 3.26-b deliberately added 5 HistData duplicate-policy tests.
- New correct full-test anchor is `514 passed`.
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

Expected status after this HANDOFF_23 document is committed and pushed:

- On branch main
- Your branch is up to date with `origin/main`.
- nothing to commit, working tree clean

Expected latest commit:

- `Add handoff document #23 after HistData duplicate policy`

Expected project commit immediately before handoff:

- `Add explicit HistData exact duplicate policy`

Expected tests:

- `514 passed`

Read the output before continuing.

## Phase 3.25 Completed

Phase 3.25 name:

- Inspect HistData raw format and design/add a dedicated tested HistData loader

Key commits:

- `Add tested HistData M1 CSV loader`
- `Document HistData loader real-file duplicate check`

Files added:

- `C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py`
- `C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py`
- `C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_LOADER_REAL_FILE_CHECK.md`

Original Phase 3.25 focused test result:

- `15 passed`

Original full test result after Phase 3.25:

- `509 passed`

Purpose:

1. Add a dedicated HistData loader instead of pretending HistData is Dukascopy.
2. Support the observed no-header comma-separated HistData format.
3. Preserve source identity as HistData.
4. Reject duplicate timestamps before canonicalization.
5. Reject non-monotonic timestamps.
6. Validate OHLC and volume.
7. Report missing minutes.
8. Keep timezone assumption explicit.
9. Do not accept HistData as a research source yet.

Observed HistData raw format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

Example:

    2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0

This differs from observed Dukascopy format:

    UTC,Open,High,Low,Close,Volume

Therefore:

- Do not call these files Dukascopy files.
- Do not use the Dukascopy loader as the official HistData loader.

## Phase 3.25 Real-File Check Result

The dedicated HistData loader was run against the real local HistData files.

Raw files checked:

- `C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv`
- `C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv`

Important:

- The folder name `dukascopy_samples` is misleading because it contains both Dukascopy sample files and HistData files.
- Do not rename or move files unless explicitly planned and documented.
- The files are under `/data/`, which is gitignored.
- Do not commit raw data.

Initial strict loader result:

- USDJPY failed with duplicate timestamps.
- This was correct protective behavior.

Duplicate diagnostic result for both USDJPY and XAUUSD:

- `n_duplicate_rows_in_duplicate_groups: 600`
- `n_duplicate_timestamp_values: 300`
- `n_conflicting_duplicate_timestamp_values: 0`
- `all_duplicate_groups_have_identical_ohlcv: True`

Duplicate blocks occur on:

- `2021.10.31 19:00` through `19:59`
- `2022.10.30 19:00` through `19:59`
- `2023.10.29 19:00` through `19:59`
- `2024.10.27 19:00` through `19:59`
- `2025.10.26 19:00` through `19:59`

Interpretation:

- The pattern strongly suggests a recurring daylight-saving-time related duplicate hour.
- But that explanation is not enough by itself to accept HistData.
- HistData remains not accepted.

## Phase 3.26-a Completed

Phase 3.26-a name:

- Create HistData duplicate-handling decision record

Commit:

- `Add HistData duplicate handling decision record`

File added:

- `C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-003-histdata-duplicate-handling.md`

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

- Add explicit tested exact-duplicate handling to the HistData loader

Expected commit:

- `Add explicit HistData exact duplicate policy`

Files updated:

- `C:\Users\equin\Documents\institutional-ea\quantcore\data\histdata_loader.py`
- `C:\Users\equin\Documents\institutional-ea\tests\test_histdata_loader.py`

Focused test result:

- `20 passed`

Full test result:

- `514 passed`

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

- `bars`
- `n_bars`
- `n_input_rows`
- `earliest_utc`
- `latest_utc`
- `source_tz`
- `duplicate_policy`
- `n_duplicate_rows_removed`
- `n_duplicate_timestamp_values`
- `duplicate_timestamp_ranges`
- `n_missing_minutes`
- `missing_minutes`

Duplicate timestamp range type:

    DuplicateTimestampRange = tuple[pd.Timestamp, pd.Timestamp, int]

Meaning:

    (start_utc, end_utc, n_duplicate_timestamp_values_in_range)

New/updated tests include:

1. default metadata reports `duplicate_policy="reject"`
2. default policy rejects exact duplicates
3. `drop_exact` removes identical duplicate rows
4. `drop_exact` rejects conflicting duplicates
5. unknown duplicate policy is rejected
6. `drop_exact` still rejects non-monotonic timestamps
7. frozen result dataclass includes new fields

New correct full-test anchor:

- `514 passed`

## HistData Raw Files Inventoried Earlier

USDJPY file:

- `C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\USDJPY_2021_2025_Raw_HistData.csv`
- `size_bytes: 115758784`
- `sha256: 2aa2840918404b4665f8c79e31ea4a0b691ef85e878f683021cc3c4f7980a29e`
- `line_count: 1808731`
- first observed timestamp row: `2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0`
- last observed timestamp row: `2025.12.31,16:57,156.683000,156.685000,156.668000,156.671000,0`

XAUUSD file:

- `C:\Users\equin\Documents\institutional-ea\data\raw\dukascopy_samples\XAUUSD_2021_2025_Raw_HistData.csv`
- `size_bytes: 117405332`
- `sha256: e11187138f6aa0b9bbcb75f8fc9423bde6b909a2e9afade01ed952cf6a7b2e13`
- `line_count: 1726549`
- first observed timestamp row: `2021.01.03,18:00,1904.998000,1910.898000,1903.288000,1909.718000,0`
- last observed timestamp row: `2025.12.31,16:57,4318.069000,4318.459000,4317.029000,4318.379000,0`

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
2. Derived data provenance plan.
3. Missing-minute coverage analysis.
4. Weekend behavior analysis.
5. XAUUSD metals break behavior analysis.
6. Timezone/source-session reconciliation.
7. Broker mismatch assessment versus Exness.
8. Final source acceptance/rejection decision.
9. H017 validation using HistData.

## Recommended Next Sub-Phase

Recommended next sub-phase:

### Phase 3.26-c - Run HistData loader on real files with explicit `drop_exact` policy and document result

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

- `C:\Users\equin\Documents\institutional-ea\docs\operations\HISTDATA_M1_DROP_EXACT_REAL_FILE_CHECK.md`

Do not commit raw data.

## Current H017 Status

H017 remains:

- alive
- not promotable
- not ready for live trading
- blocked by insufficient research-grade M1 history

Existing realistic event-driven result from broker-native short M1 window:

- `fills=470`
- `starting_equity_usd=10000.00`
- `ending_equity_usd=16145.60`
- `total_return_pct=61.46`
- `max_drawdown_pct=-33.65`
- `annualized_sharpe=1.3218`

Claim result:

- `PSR: 0.8662`, failed threshold `0.95`
- `MinTRL feasible: True`
- `MinTRL required n: 1034`
- `MinTRL observed n: 470`
- `DSR: Skipped`
- `H017 promotable: False`

Operational verdict:

- `PIPELINE SMOKE PASSED: True`
- `RESEARCH VALIDATION SUFFICIENT: False`

Interpretation:

1. The event pipeline works.
2. Available broker-native M1 history is too short.
3. Do not trust the short-window `+61.46%` return as validated edge.
4. The `-33.65%` drawdown is a serious risk signal.
5. H017 is alive but not promotable.

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

## Workflow Rules

The project uses:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
- No WSL
- No Linux/macOS shell assumptions

Important PowerShell rule:

Do not use:

    python - <<'PY'

Use PowerShell here-strings instead:

    @'
    python code here
    '@ | python -

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

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. I am continuing after Phase 3.26-b and HANDOFF_23.

I understand:

1. Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
2. Current full-test anchor is `514 passed`.
3. Latest expected handoff commit is `Add handoff document #23 after HistData duplicate policy`.
4. Latest expected project commit before the handoff is `Add explicit HistData exact duplicate policy`.
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
