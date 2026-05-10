# HANDOFF_86 — H024 Clean Cent-Symbol Runtime Validation + Collect Helper Fix

If any older handoff conflicts with this one, this handoff wins.

This continues from HANDOFF_85 and is intended to be fully self-contained. A new AI should be able to continue safely from this document without opening older handoffs first.

---

## 0. One-Sentence State

H024 remains research-only and not deployment-approved, but the Exness Standard Cent log-only runtime path has now produced a clean validated cent-symbol runtime CSV for `USDJPYc` / `XAUUSDc`; the helper bug that falsely validated cent collections against default `USDJPYm` / `XAUUSDm` symbols was fixed, committed, pushed, and tested with `953 passed`.

---

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current stage:

Execution-safety preparation after H024 research evidence, now focused on the user's Exness Standard Cent account route.

Current status:

H024 is promising, but still:

- Not demo-approved
- Not live-approved
- Not Phase 4-approved
- Not approved for any order execution
- Not approved for any execution adapter
- Not approved for `OrderSend`, `OrderCheck`, `CTrade`, or `MqlTradeRequest`

The user is eager to deploy and plans to start with `10k USC` on an Exness Standard Cent account.

Do not soften deployment boundaries.

---

## 2. Human Preference

The user is tired of excessive ceremony.

Going forward:

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do one real action at a time.
- Do not create governance docs unless they preserve a real result, preserve a handoff, prevent ambiguity, or protect against future confusion.
- For docs-only edits, do not run full pytest unless there is a clear reason.
- For code edits, tests are mandatory.
- Avoid long real-data diagnostics casually.
- For real-data diagnostics, get explicit authorization or make a clear safety-bound decision.
- Never soften deployment boundaries because H024 is promising.

Important sentiment:

The user wants to make the EA survive the future, not fit the past.

The correct direct answer about deployment is:

H024 is meaningfully closer under the 10k USC cent-account route, but it is still not demo/live/Phase 4 deployable.

---

## 3. Environment

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 inside `.venv`
- No WSL

Repository root:

```text
C:\Users\equin\Documents\institutional-ea
```

Virtual environment:

```text
C:\Users\equin\Documents\institutional-ea\.venv
```

Branch:

```text
main
```

GitHub remote:

```text
https://github.com/citradinnda/institutional-ea.git
```

MetaEditor:

```text
C:\Program Files\MetaTrader 5\MetaEditor64.exe
```

Terminal data dir:

```text
C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075
```

Terminal EA source:

```text
C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5
```

Compiled EX5:

```text
C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5
```

Runtime CSV in terminal:

```text
C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\h024_ea_log_only_preflight.csv
```

Repo report CSVs are local and intentionally untracked.

Do not commit `reports/`.

---

## 4. Expected Repo State After This Handoff Is Committed

Expected:

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
```

Expected latest commit after this handoff is committed:

```text
Add handoff document #86
```

Expected latest commit before HANDOFF_86 commit:

```text
ff18be2 Fix H024 cent collect verifier symbols
```

Current full-test anchor after helper fix:

```text
953 passed in 17.92s
```

Focused cent/local-helper anchor after helper fix:

```text
21 passed in 0.85s
```

Diff check before commit:

```text
git diff --check
# clean / no output
```

---

## 5. Recent Commit History

Expected recent history before HANDOFF_86 commit:

```text
ff18be2 Fix H024 cent collect verifier symbols
2ddaf90 Add handoff document #85
6a8e017 Fix H024 cent preflight helper CLI path
26d6393 Add H024 cent symbol runtime validation support
eb4aa84 Add handoff document #84
b446ed9 Add H024 cent account executable scan specs
cd3c153 Document H024 cent account feasibility probe
a2665ea Document H024 executable density thresholds
dbfca1f Expand H024 balance density symbol breakdown
011d3fc Document H024 balance executable candidate density
```

Important commits after HANDOFF_85:

```text
ff18be2 Fix H024 cent collect verifier symbols
```

---

## 6. Non-Negotiable Safety Boundary

H024 remains:

- Research / pre-deployment only
- No demo deployment approval
- No live trading approval
- No Phase 4 execution approval
- No order-send capability approved
- No execution adapter approved

Forbidden in the log-only EA and current project stage:

- `OrderSend`
- `OrderSendAsync`
- `OrderCheck`
- `CTrade`
- `#include <Trade...>`
- `MqlTradeRequest`
- `MqlTradeResult`
- `PositionOpen`
- `PositionClose`
- `PositionModify`
- Pending order helpers

Also not approved:

- EA chart attach/detach automation
- GUI automation
- MT5 launcher/profile mutation affecting live terminals
- Order-send automation
- Demo/live execution adapter
- Raising risk to force executable candidates
- Treating feasibility scans as deployment approval

Allowed so far:

- Manual EA attach/remove
- Copy EA source to terminal Experts
- Compile EA with MetaEditor
- Reset/collect runtime CSV
- Verify runtime CSV
- Summarize intended-action rows
- Historical log-only replay using `InpH024ClosedShift`
- CSV-read-only dry-run request reconciliation
- Pure Python dry-run execution request contracts
- Runtime BLOCKED sizing diagnostics verification
- Pure Python minimum-volume feasibility summary
- Pure Python executable candidate shift scanning
- Pure Python exact capital threshold scanning
- Pure Python risk-fraction threshold comparison
- Optimized pure Python risk-fraction threshold comparison mode
- Research-only documentation of threshold results
- Read-only MT5 account/symbol-info probes
- Read-only MT5 order_calc_profit probes
- Pure Python cent-account USC feasibility scanner support
- Cent-symbol runtime CSV verifier/summarizer support
- Cent-symbol local runtime target preflight
- Clean cent-symbol log-only runtime collection and verification

---

## 7. Current Deployment Verdict

H024 is still not approved for demo or live.

However, the deployment-relevant feasibility universe changed.

Before HANDOFF_84, the important result was:

At 100 USD / 1% risk on standard-like `USDJPYm` / `XAUUSDm` symbols, H024 had no executable historical candidate.

After HANDOFF_84, the user clarified they plan to start with:

```text
10,000 USC
```

on an Exness Standard Cent account.

The real terminal account probe showed:

- Account currency: `USC`
- Available symbols: `USDJPYc`, `XAUUSDc`
- Unavailable symbols: `USDJPYm`, `XAUUSDm`, `USDJPY`, `XAUUSD`
- Balance at probe time: `0.0 USC`

This means prior standard-symbol scans are not the final deployment authority for the cent account.

Current best answer:

The 10k USC cent-account path is mechanically plausible by size, and clean cent-symbol log-only runtime validation has now passed, but this does not approve deployment.

The blocker has changed from:

```text
minimum volume impossible at 100 USD standard-symbol sizing
```

to:

```text
need cent-symbol historical log-only replay that produces executable WOULD_OPEN rows, executable runtime dry-run request reconstruction, and execution-safety review
```

---

## 8. H024 Mechanics Summary

H024 is a regime-conditioned pullback-continuation hypothesis.

Mechanics:

- Defines directional regime using slow H4 trend state.
- Waits for pullback against that regime.
- Enters only if price resumes in regime direction after pullback.
- Does not use H021 time/session buckets.
- Does not reuse Donchian breakout trigger.
- Uses H020 sizing contract.
- Returns H017-compatible bridge shim.
- Uses H018 hard guard semantics.
- Baseline candidate: hold = 3 H4, stop ATR multiple = 2.0.

Frozen signal defaults:

```text
slow_window = 5
slope_lag = 2
atr_window = 3
pullback_window = 3
min_pullback_atr = 0.25
max_pullback_atr = 3.0
min_slope_atr = 0.05
```

Signal logic:

```text
slow_ma = close.rolling(5).mean()
atr = Wilder ATR(3)
slope = slow_ma - slow_ma.shift(2)
slope_threshold = atr * 0.05

trend_up = close > slow_ma and slope > slope_threshold
trend_down = close < slow_ma and slope < -slope_threshold

previous_bearish = close.shift(1) < open.shift(1)
previous_bullish = close.shift(1) > open.shift(1)

recent_high_before_signal = high.shift(1).rolling(3).max()
recent_low_before_signal = low.shift(1).rolling(3).min()

long_pullback_depth_atr = (recent_high_before_signal - low.shift(1)) / atr.shift(1)
short_pullback_depth_atr = (high.shift(1) - recent_low_before_signal) / atr.shift(1)

long_pullback_ok = long_pullback_depth_atr between 0.25 and 3.0 inclusive
short_pullback_ok = short_pullback_depth_atr between 0.25 and 3.0 inclusive

long_resumption = close > high.shift(1)
short_resumption = close < low.shift(1)

long_signal = trend_up and previous_bearish and long_pullback_ok and long_resumption
short_signal = trend_down and previous_bullish and short_pullback_ok and short_resumption
```

---

## 9. H020 / H024 Sizing Boundary

H024 uses H020 sizing.

Important H020 behaviors:

- Computes explicit pre-trade lot intents.
- Suppresses flat signals.
- Suppresses invalid stop geometry.
- Suppresses stop distances below one spread.
- Computes risk-based lots.
- Applies per-trade gross notional caps.
- Applies portfolio gross notional scaling.
- Rounds lots down to broker lot step.
- Suppresses lots below broker minimum lot.
- Preserves final signed risk fraction from final executable lots.

Therefore, cent-account scans must not bypass H020 sizing.

The cent scanner support reuses H024 signal/stop geometry, but routes balances through H020 sizing using alternate InstrumentSpec values.

This is important:

The cent support is a performance/research-accounting change, not execution approval.

---

## 10. Current EA Facts

EA source:

```text
ea_mt5\Experts\H024_LogOnly_Preflight.mq5
```

MQL5 property version:

```text
#property version "0.600"
```

Runtime schema:

```text
h024_ea_log_only_preflight_v2
```

EA input version:

```text
InpEaVersion = "0.6"
```

Intended-action schema:

```text
h024_intended_action_log_v1
```

Important current input:

```text
InpH024ClosedShift = 1
```

Meaning:

Defaults to latest closed H4 bar. Set manually for historical replay only. Do not automate chart attach/detach.

Current runtime intended-action behavior:

- `NO_ACTION` rows can carry zero entry/stop/lots.
- Signal rows first derive entry/stop from closed H4 bar and ATR stop.
- If signal sizing is executable, row may remain `WOULD_OPEN`.
- If signal sizing is below broker minimum volume, row becomes `BLOCKED:volume_below_min_for_would_open`.
- `BLOCKED` signal rows preserve positive entry, stop, stop_distance, and raw_lots.
- `BLOCKED` signal rows force final executable lots to 0.
- Dry-run reconciler does not emit requests from `BLOCKED` rows.

Clean cent-symbol runtime has now been collected and verified, but it only observed `NO_ACTION` rows.

---

## 11. Data Rules

Accepted validation source:

- Exness demo/terminal broker-native exports only

Accepted model symbols:

- `USDJPY`
- `XAUUSD`

Previously observed standard symbols:

- `USDJPYm`
- `XAUUSDm`

Current cent account symbols:

- `USDJPYc`
- `XAUUSDc`

Normalize for model logic:

- `USDJPYc` -> `USDJPY`
- `XAUUSDc` -> `XAUUSD`
- `USDJPYm` -> `USDJPY`
- `XAUUSDm` -> `XAUUSD`

Accepted timeframes:

- Broker-native H4
- Broker-native M1

Broker timezone used by loader:

```text
Europe/Athens
```

DST-aware.

Do not use:

- HistData for validation/tuning/production dataset creation
- Broker H4 plus HistData M1 combinations
- Sparse 2018 through 2021-06 broker-native prefix as dense M1
- Incomplete H4/M1 windows

Do not commit:

- Raw MT5 CSV files
- Raw HistData files
- Large derived datasets
- Broker/vendor source files
- Local `reports/*.csv`
- Local `reports/*.json`
- Local runtime CSVs
- Local compile logs

---

## 12. Core Files

H024 core:

```text
quantcore\strategy\h024.py
quantcore\strategy\h024_runner.py
```

H020 sizing contract:

```text
quantcore\strategy\h020.py
tests\test_h020.py
```

Position sizing reference:

```text
quantcore\strategy\h024_position_sizer.py
tests\test_h024_position_sizing.py
```

Execution/log contracts:

```text
quantcore\execution\h024_intended_action_log.py
quantcore\execution\h024_dry_run_execution_request.py
quantcore\execution\h024_dry_run.py
tests\test_h024_intended_action_log_contract.py
tests\test_h024_dry_run_execution_request_contract.py
tests\test_h024_intended_action_blocked_sizing_diagnostics.py
```

EA/runtime:

```text
ea_mt5\Experts\H024_LogOnly_Preflight.mq5
scripts\run_h024_mt5_log_only_preflight_local.py
scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\verify_h024_ea_source_static.py
scripts\reconcile_h024_runtime_dry_run_requests.py
scripts\summarize_h024_blocked_sizing_diagnostics.py
```

Feasibility / capital threshold tools:

```text
scripts\summarize_h024_min_volume_feasibility.py
scripts\scan_h024_executable_candidate_shifts.py
scripts\scan_h024_capital_thresholds.py
```

Cent-account scanner support:

```text
scripts\scan_h024_executable_candidate_shifts.py
tests\test_h024_cent_account_specs.py
```

Cent-symbol runtime validation support:

```text
scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\run_h024_mt5_log_only_preflight_local.py
tests\test_h024_cent_symbol_runtime_validation.py
tests\test_h024_mt5_log_only_preflight_local_helper.py
```

Important operation docs:

```text
docs\operations\H024_CENT_ACCOUNT_SYMBOL_FEASIBILITY_PROBE_RESULT.md
docs\operations\H024_BALANCE_EXECUTABLE_CANDIDATE_DENSITY_RESULT.md
docs\operations\H024_100USD_1PCT_FEASIBILITY_BOUNDARY.md
docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_MODE_RESULT.md
docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_RESULT.md
docs\operations\H024_EXACT_CAPITAL_THRESHOLD_RESULT.md
docs\operations\H024_CAPITAL_FEASIBILITY_FRONTIER_RESULT.md
docs\operations\H024_EXECUTABLE_CANDIDATE_SHIFT_SCAN_RESULT.md
docs\operations\H024_MIN_VOLUME_FEASIBILITY_RESULT.md
docs\operations\H024_BLOCKED_SIZING_DIAGNOSTICS_RUNTIME_RESULT.md
docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
docs\operations\H024_EA_WOULD_OPEN_SYNTHETIC_VALIDATION_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\handoffs\HANDOFF_83.md
docs\operations\handoffs\HANDOFF_84.md
docs\operations\handoffs\HANDOFF_85.md
docs\operations\handoffs\HANDOFF_86.md
```

---

## 13. Evidence Reality Before HANDOFF_86

Already true before this handoff:

- H024 backtest is promising.
- Broker-cost reconciliation passed.
- MT5 order-behavior facts were audited statically/read-only.
- Python terminal/account preflight passed.
- Log-only EA exists.
- EA compiles into refreshed EX5.
- EA has no order-send path.
- EA logs runtime preflight rows.
- EA logs intended-action header and row events.
- Runtime intended-action `NO_ACTION` rows were observed in real current log-only runtime.
- Strict `--require-would-open` gate exists.
- Historical log-only replay previously observed `WOULD_OPEN` path.
- Dry-run request contract exists in pure Python.
- Runtime CSV to dry-run request reconciler exists and is CSV-read-only.
- Reconciler correctly rejects non-executable rows.
- EA derives entry/stop for signal rows.
- EA converts under-min-volume signal rows into `BLOCKED`, not fake `WOULD_OPEN`.
- `BLOCKED` signal rows preserve sizing diagnostics.
- Runtime replay proved positive entry/stop/stop-distance/raw-lots are preserved on `BLOCKED` rows.
- A reusable verifier exists for `BLOCKED` sizing diagnostics.
- A regression test ensures positive `BLOCKED` diagnostics cannot become dry-run requests.
- Minimum-volume feasibility is quantified.
- A reusable executable candidate shift scanner exists.
- At 100 USD / 1% risk on standard-like m specs, no historical H024 candidate survives sizing into an executable candidate.
- A reusable exact capital threshold scanner exists.
- At 1% risk on standard-like specs, ANY / USDJPY first executable historical candidate appears at 245 USD.
- At 1% risk on standard-like specs, XAUUSD first executable historical candidate appears at 935 USD.
- Optimized risk-fraction threshold comparison exists.
- Read-only MT5 account/symbol probes showed the real account is USC cent and exposes `USDJPYc` / `XAUUSDc`.
- Read-only MT5 order_calc_profit probes showed representative `USDJPYc` and `XAUUSDc` candidates executable by size at 10000 USC / 1%.
- Pure-Python cent-account scanner support exists.
- At 10000 USC / 1% with cent-account USC specs, scanner found 1364 executable historical candidates.
- Runtime verifier/summarizer/helper support explicit `--cent-account-symbols`.
- Cent-symbol local runtime target preflight passed with expected symbols `USDJPYc`, `XAUUSDc`, `Violations: 0`, `Verdict: PASS`.
- HANDOFF_85 was committed as `2ddaf90`.

---

## 14. What Changed Since HANDOFF_85

### 14.1 Clean Cent-Symbol Log-Only Runtime Was Collected and Verified

Manual process:

1. User reset/cleared prior mixed runtime CSVs.
2. User manually attached and removed the log-only EA on `USDJPYc H4`.
3. User manually attached and removed the log-only EA on `XAUUSDc H4`.
4. The runtime CSV was collected to:

```text
reports\h024_ea_log_only_preflight.csv
```

Clean runtime collection facts:

```text
Rows: 78
```

Direct cent-symbol verifier:

```text
python scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_preflight.csv --cent-account-symbols
```

Result:

```text
Rows: 78
Violations: 0
Verdict: PASS
```

Direct cent-symbol intended-action summary:

```text
python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_preflight.csv --cent-account-symbols
```

Result:

```text
CSV: reports\h024_ea_log_only_preflight.csv
Total rows: 78
Intended-action header rows: 2
Intended-action data rows: 12

USDJPYc:
  headers: 1
  rows: 6
  normalized: USDJPY
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

XAUUSDc:
  headers: 1
  rows: 6
  normalized: XAUUSD
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

Verdict: PASS
```

Interpretation:

Clean cent-symbol log-only runtime validation passed, but it only observed `NO_ACTION` rows.

This does not approve demo or live deployment.

### 14.2 Mixed CSV Failure Was Correctly Diagnosed

Before the clean reset, the collected CSV had both old standard-symbol rows and new cent-symbol rows:

- `USDJPYm`
- `XAUUSDm`
- `USDJPYc`
- `XAUUSDc`

Expected behavior:

- Default verifier rejects cent symbols.
- Cent-symbol verifier rejects old m symbols.
- A clean cent-only CSV is required when using `--cent-account-symbols`.

The later clean cent-only CSV verified successfully.

### 14.3 Found and Fixed Helper Collect Validation Bug

Observed bug:

This command:

```text
python scripts\run_h024_mt5_log_only_preflight_local.py --terminal-data-dir ... --metaeditor ... --cent-account-symbols --collect
```

collected the clean cent CSV, but still validated it against default symbols:

```text
USDJPYm
XAUUSDm
```

Bug location:

```text
scripts\run_h024_mt5_log_only_preflight_local.py
```

Before fix:

```python
rows, violations = run_verify(report_path)
```

After fix:

```python
rows, violations = run_verify(report_path, expected_symbols=expected_symbols)
```

Regression test added:

```text
tests\test_h024_mt5_log_only_preflight_local_helper.py
```

Test concept:

Ensure collect path forwards the selected expected symbols to verifier.

Focused test after fix:

```text
21 passed in 0.85s
```

Re-running helper collect after fix:

```text
Collected runtime CSV to: reports\h024_ea_log_only_preflight.csv
Rows: 78
Violations: 0

Verdict: PASS
```

Full test after fix:

```text
953 passed in 17.92s
```

Commit:

```text
ff18be2 Fix H024 cent collect verifier symbols
```

Pushed to origin/main.

---

## 15. Current Answer Key

If asked "are we ready to demo/live?":

No.

If asked "are we officially Phase 4?":

No.

If asked "did the clean cent runtime pass?":

Yes. Clean `USDJPYc` / `XAUUSDc` log-only runtime CSV verified with `Violations: 0`, and intended-action summary passed.

If asked "did it produce an executable signal?":

No. It produced only `NO_ACTION` rows:

- `USDJPYc`: 6 `NO_ACTION`
- `XAUUSDc`: 6 `NO_ACTION`
- `WOULD_OPEN`: 0
- `BLOCKED`: 0

If asked "what bug was fixed?":

The local helper's `--collect --cent-account-symbols` path collected the CSV but verified it against default `USDJPYm` / `XAUUSDm`. It now forwards `expected_symbols` into `run_verify`.

If asked "what is the latest full-test anchor?":

```text
953 passed in 17.92s
```

If asked "what is the latest commit before HANDOFF_86?":

```text
ff18be2 Fix H024 cent collect verifier symbols
```

If asked "does 10k USC equal 10k USD?":

No. It is a cent-account balance denomination. The scanner models USC accounting through cent-contract specs, not by pretending the account is a standard USD account.

If asked "does this approve OrderSend?":

No.

If asked "what is the next gate?":

Cent-symbol historical log-only replay to observe a valid `WOULD_OPEN` row, then runtime CSV verification/summarization with `--cent-account-symbols`, then executable runtime dry-run request reconstruction if a valid `WOULD_OPEN` row is observed.

If asked "what should we not do next?":

Do not add execution adapter, `OrderSend`, `OrderCheck`, `CTrade`, or `MqlTradeRequest`.

---

## 16. Current Important Commands

Verify full suite:

```powershell
python -m pytest -q
```

Expected current anchor:

```text
953 passed
```

Run focused cent/local-helper tests:

```powershell
python -m pytest `
  tests\test_h024_mt5_log_only_preflight_local_helper.py `
  tests\test_h024_cent_symbol_runtime_validation.py `
  -q
```

Expected focused anchor:

```text
21 passed
```

Run cent-symbol local runtime target preflight:

```powershell
python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --automation-target-preflight `
  --cent-account-symbols
```

Expected:

```text
expected_symbols: USDJPYc, XAUUSDc
Violations: 0
Verdict: PASS
```

Collect and verify current clean cent-symbol runtime CSV after manual attach/remove:

```powershell
python scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --cent-account-symbols `
  --collect
```

Expected for current clean collection:

```text
Rows: 78
Violations: 0
Verdict: PASS
```

Direct cent-symbol verifier:

```powershell
python scripts\verify_h024_ea_preflight_log.py `
  reports\h024_ea_log_only_preflight.csv `
  --cent-account-symbols
```

Expected:

```text
Violations: 0
Verdict: PASS
```

Direct cent-symbol intended-action summary:

```powershell
python scripts\summarize_h024_ea_intended_action_runtime.py `
  reports\h024_ea_log_only_preflight.csv `
  --cent-account-symbols
```

Expected current summary:

```text
USDJPYc:
  rows: 6
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

XAUUSDc:
  rows: 6
  WOULD_OPEN: 0
  BLOCKED: 0
  NO_ACTION: 6

Verdict: PASS
```

Run cent-account 10k USC executable candidate scan:

```powershell
python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 10000 `
  --risk-fraction 0.01 `
  --cent-account-usc-specs `
  --output-csv reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv `
  --max-rows 10
```

Expected:

```text
instrument_specs: Exness Standard Cent USC specs
executable_candidate_rows: 1364
Verdict: PASS
```

Run standard default scan for contrast:

```powershell
python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 5
```

Expected:

```text
executable_candidate_rows: 0
Verdict: PASS
Scan completed; no executable candidate shifts found at these settings.
```

---

## 17. What Remains Missing

Critical missing evidence:

- Account was unfunded during the probe: balance = `0.0 USC`.
- Clean cent-symbol current runtime produced only `NO_ACTION`.
- No cent-symbol historical replay has yet produced a verified `WOULD_OPEN` row.
- No executable runtime dry-run request has been reconstructed from cent-symbol runtime CSV.
- No execution safety review after cent feasibility.
- No demo execution adapter exists.
- No order placement behavior has been tested.
- No order rejection behavior has been tested.
- No requote/slippage behavior has been tested.
- No position reconciliation exists.
- No kill-switch-to-execution boundary has been implemented.
- No demo approval.
- No live approval.
- No Phase 4 approval.
- 2023 weakness remains real.

---

## 18. Recommended Next Work

Best next technical step:

Do not add execution code.

Recommended next safe work:

1. Use historical log-only replay on cent symbols using manual `InpH024ClosedShift` changes.
2. Find a cent-symbol runtime row that produces `WOULD_OPEN`.
3. Collect the CSV with `--cent-account-symbols`.
4. Verify and summarize the CSV.
5. Only if a valid executable `WOULD_OPEN` row is observed, reconcile runtime CSV into dry-run requests.
6. Only after an executable cent-symbol runtime dry-run request exists, perform a separate execution-safety review.

Do not jump directly to:

- `OrderSend`
- `OrderCheck`
- `CTrade`
- `MqlTradeRequest`
- Execution adapter
- Demo trading
- Live trading
- Phase 4
- Chart automation
- GUI automation

---

## 19. Immediate First Action For Next AI

Ask the user to run:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10
```

Expected after this handoff is committed:

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
```

Expected latest commit:

```text
Add handoff document #86
```

Then continue from the actual repo state, not from assumptions.

---

## 20. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_86.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Branch should be `main`, pushed, tracked tree clean except local `reports/`.
- Latest pre-handoff commit is `ff18be2 Fix H024 cent collect verifier symbols`.
- Current full-test anchor is `953 passed in 17.92s`.
- H024 is still not demo-approved, not live-approved, and not Phase 4-approved.
- No `OrderSend`, no `OrderCheck`, no `CTrade`, no `MqlTradeRequest`, no execution adapter.
- User intends to start with `10k USC`.
- Real terminal account is USC cent account on Exness-MT5Real25; probe balance was `0.0 USC`.
- Available account symbols are `USDJPYc` and `XAUUSDc`; `USDJPYm`, `XAUUSDm`, `USDJPY`, and `XAUUSD` were not found.
- Read-only MT5 order_calc_profit showed representative `USDJPYc` and `XAUUSDc` candidates executable by size at `10000 USC / 1%`.
- The scanner supports `--cent-account-usc-specs`.
- At `10000 USC / 1%` with cent-account USC specs, the scanner found `1364` executable historical candidates.
- Runtime verifier/summarizer/helper support explicit `--cent-account-symbols`.
- Clean cent-symbol log-only runtime passed: `Rows: 78`, `Violations: 0`, `Verdict: PASS`.
- Intended-action summary passed: `USDJPYc` 6 `NO_ACTION`, `XAUUSDc` 6 `NO_ACTION`, no `WOULD_OPEN`, no `BLOCKED`.
- The helper collect bug was fixed so `--collect --cent-account-symbols` verifies against `USDJPYc` / `XAUUSDc`.
- This validates the cent-symbol log-only runtime path but does not approve deployment.
- Next safe gate is cent-symbol historical log-only replay to obtain a verified executable `WOULD_OPEN`, then dry-run request reconstruction.
- `reports/` stays untracked.

Please run:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10
```

Then paste the full output.
