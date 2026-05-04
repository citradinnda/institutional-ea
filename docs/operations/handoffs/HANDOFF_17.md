HANDOFF 17 — Continuation After Phase 3.11
You are continuing an existing project. Read this entire prompt before responding. Do not invent context. When in doubt, ask before writing code.

Project Identity
You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

The user is intelligent but is NOT a professional developer. They have already burned through 16 dead strategies and are now building infrastructure-first.

Tone and workflow rules are non-negotiable:

Step-by-step.
Numbered steps.
Explicit Windows file paths.
Plain English.
Define every technical term inline.
Never write code without saying exactly where the file goes and how to run it.
One sub-phase per response.
Never skip git commits.
Provide exact:
git add ...
git commit -m "..."
git push
After every commit, instruct the user to run:
git status
git ls-files <touched-dirs>/
Read the user's output before continuing.
Do not let git status go unread.
If tests pass but the COUNT drops, treat it as a regression.
Current stack:
Windows
PowerShell
VS Code
Python 3.12.10
.venv
No WSL
No Linux assumptions
Before writing code that calls internal functions, inspect actual APIs with:
inspect.signature(...)
dataclasses.fields(...)
Do not trust remembered keyword names.
Prefer one consolidated multi-line import block per source module per consuming file.
If a code block is cut off mid-paste, restart the affected file from the top.
If asked for a handoff document, write a complete self-contained version. Never say “same as previous handoff.”
Do not propose switching to a new AI chat.
After each sub-phase, give exactly these three response options:
✅ done
⚠️ error — paste it
🤔 question
Project Goal
Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

Research: Python quantcore, eventually Kaggle notebooks.
Execution: MetaTrader 5.
Production: Oracle Cloud Always Free VPS.
Monitoring: self-hosted free-tier monitoring stack.
User machine: Windows, PowerShell, VS Code, Python 3.12.10 in .venv.
The project is infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, or poor risk control.

Repository
Repo root:

text
C:\Users\equin\Documents\institutional-ea
Virtual environment:

text
C:\Users\equin\Documents\institutional-ea\.venv
GitHub remote:

text
https://github.com/citradinnda/institutional-ea.git
Branch:

text
main
Current Verified State At Handoff
Latest verified commit:

text
75db15d Add MT5 M1 export operations checklist
Latest verified pushed log:

text
75db15d (HEAD -> main, origin/main) Add MT5 M1 export operations checklist
a0263ac Update handoff document #16 with continuation context
ff6ee51 Add handoff document #16 after M1 data decision record
d64a1e1 Polish M1 data acquisition decision record formatting
b1365c7 Add M1 data acquisition decision record
Latest verified repo status after push:

text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
Latest verified tracked docs:

text
docs/decisions/DR-001-m1-data-acquisition.md
docs/operations/MT5_M1_EXPORT_CHECKLIST.md
Current full-test anchor:

text
482 passed
Latest verified test output:

text
482 passed in 14.63s
Important: test count must remain 482 unless a deliberate test-adding phase increases it. If tests pass but the count drops, treat it as a regression.

Immediate First Action For The Next AI
Do NOT write code first.

Start with hygiene verification only.

Ask the user to run:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -5
pytest -q
Expected status:

text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
Expected latest commit:

text
75db15d Add MT5 M1 export operations checklist
Expected tests:

text
482 passed
Read the output before continuing.

Just Completed Phase
Phase 3.11 — Add local MT5 M1 export operations checklist
Commit:

text
75db15d Add MT5 M1 export operations checklist
File added:

text
C:\Users\equin\Documents\institutional-ea\docs\operations\MT5_M1_EXPORT_CHECKLIST.md
Purpose:

Give the user a practical checklist for obtaining longer M1 exports from MetaTrader 5.
Reduce operational mistakes during local data acquisition.
Make clear where to place M1 files.
Make clear not to commit raw data.
Preserve correct .gitignore understanding.
Include validation command:
powershell
python scripts\run_h017_event_real.py
Include expected success marker:
text
RESEARCH VALIDATION SUFFICIENT: True
Include interpretation if still false:
text
Pipeline may work, but research validation is still insufficient.
Phase 3.11 was documentation-only. It did not change strategy logic, backtest logic, costs, loaders, tests, or execution code.

Recommended Next Sub-Phase
Recommended next sub-phase:

Phase 3.12 — Add a run log template for real-data event validation attempts
Suggested path:

text
C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md
Purpose:

Give the user a repeatable place to record future outputs from:
powershell
python scripts\run_h017_event_real.py
Track each M1 acquisition attempt consistently.
Record whether research validation became sufficient.
Prevent accidental cherry-picking of favorable short-window results.
Keep operational evidence separate from strategy tuning.
This should be documentation-only unless the user explicitly asks otherwise.

Suggested contents:

Title.
Purpose.
Instructions: run the real event smoke script after each M1 export attempt.
Template fields:
Run date.
Data source.
Broker/account environment.
USDJPY M1 earliest timestamp.
USDJPY M1 latest timestamp.
XAUUSD M1 earliest timestamp.
XAUUSD M1 latest timestamp.
Clean common event window start.
Clean common event window end.
Common H4 bar count.
Minimum required H4 bars.
RESEARCH VALIDATION SUFFICIENT.
Fill count.
Ending equity.
Max drawdown.
Sharpe.
H017 promotable.
Notes.
Warning that if RESEARCH VALIDATION SUFFICIENT: False, the run is pipeline evidence, not promotable research evidence.
Warning not to tune strategy parameters to the short M1 window.
Warning not to silently switch data vendors.
Suggested inspection before creating it:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
Get-ChildItem -Path C:\Users\equin\Documents\institutional-ea\docs -Recurse | Select-Object FullName, Length
git ls-files docs/
If clean, create:

text
C:\Users\equin\Documents\institutional-ea\docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md
Then run:

powershell
pytest -q
Expected:

text
482 passed
Then commit:

powershell
git add docs\operations\H017_EVENT_VALIDATION_RUN_LOG.md
git commit -m "Add H017 event validation run log template"
git push
git status
git ls-files docs/
git log --oneline -5
Do not continue until the user pastes the output and you read it.

Major Phase Status
Eight major phases:

Phase 0 — Foundation

Partially done.
Repo, package structure, tests, and tooling are usable.
MLflow and DVC deferred.
Phase 1 — Research Framework

Complete.
Phase 2 — H017 Strategy Logic

Complete through real-data wiring.
H017 alive but not promotable.
Phase 3 — Realistic event-driven backtest engine

In progress.
Complete through Phase 3.11.
Phase 3.12 recommended next.
Phase 4 — MT5 EA shell + Python decision service

Not started.
Phase 5 — Free-tier VPS deployment

Not started.
Phase 6 — Monitoring

Not started.
Phase 7 — Governance and continuous improvement

Not started beyond existing hypothesis discipline.
Recent Completed Work
Phase 3.8 — Event-smoke operational preflight hardening
Commit:

text
e79158c Phase 3.8: add event smoke data preflight checks
Files added:

text
quantcore/data/preflight.py
tests/test_preflight.py
File updated:

text
scripts/run_h017_event_real.py
Full test count increased from 476 to 482.

Purpose:

Fail early with clear operator-facing messages if required local MT5 exports are missing.
Keep real-data smoke script errors readable.
Avoid confusing later tracebacks from pandas or the MT5 loader.
Preserve infrastructure-first discipline.
Do not change strategy logic, cost assumptions, fill logic, or validation conclusions.
Preflight API:

python
@dataclass(frozen=True)
class RequiredFileStatus:
    path: Path
    exists: bool

@dataclass(frozen=True)
class RequiredFilesReport:
    statuses: tuple[RequiredFileStatus, ...]
    missing_paths: tuple[Path, ...]
    all_present: bool

def assess_required_files(paths: Sequence[str | Path]) -> RequiredFilesReport

def require_existing_files(
    paths: Sequence[str | Path],
    *,
    label: str = "Required file",
) -> RequiredFilesReport
The event-smoke script calls:

python
require_existing_files(
    [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
    label="MT5 export",
)
Phase 3.9 — HANDOFF_15.md
Commit:

text
d7239f4 Add handoff document #15 after Phase 3.8 preflight hardening
File:

text
HANDOFF_15.md
Verified:

File is tracked.
Commit pushed.
Repo clean.
Full tests still 482 passed.
Phase 3.10-b — M1 data acquisition decision record
Commit:

text
b1365c7 Add M1 data acquisition decision record
File added:

text
docs/decisions/DR-001-m1-data-acquisition.md
Purpose:

Record that the next infrastructure blocker is insufficient M1 history.
Document that H017 must not be promoted based on the current short 2026 M1 window.
Document that broker-native Exness MT5 History Center export is the preferred first acquisition path.
Document that switching vendors must be a separate decision record and loader-validation phase.
Phase 3.10-c — Polish DR-001 Markdown formatting
Commit:

text
d64a1e1 Polish M1 data acquisition decision record formatting
File updated:

text
docs/decisions/DR-001-m1-data-acquisition.md
Reason:

The initial decision record content was correct, but the Markdown formatting around code fences and headings needed cleanup.

HANDOFF_16 Repair
An empty HANDOFF_16.md was accidentally committed first as:

text
ff6ee51 Add handoff document #16 after M1 data decision record
It was corrected by:

text
a0263ac Update handoff document #16 with continuation context
Important lesson:

For future handoff files, check file size and first lines before committing.

Phase 3.11 — MT5 M1 Export Checklist
Commit:

text
75db15d Add MT5 M1 export operations checklist
File added:

text
docs/operations/MT5_M1_EXPORT_CHECKLIST.md
During creation, the first paste damaged Markdown code fences. The file was overwritten from the top using indented command blocks instead of triple-backtick blocks. Final verification showed:

File size: 5224 bytes.
No triple-backtick matches.
Tests: 482 passed.
Commit pushed.
Repo clean.
Current Repo Layout Highlights
Important paths:

text
C:\Users\equin\Documents\institutional-ea\quantcore
C:\Users\equin\Documents\institutional-ea\scripts
C:\Users\equin\Documents\institutional-ea\tests
C:\Users\equin\Documents\institutional-ea\data\raw
C:\Users\equin\Documents\institutional-ea\docs\decisions
C:\Users\equin\Documents\institutional-ea\docs\operations
Important recent files:

text
C:\Users\equin\Documents\institutional-ea\quantcore\data\coverage.py
C:\Users\equin\Documents\institutional-ea\tests\test_coverage.py
C:\Users\equin\Documents\institutional-ea\quantcore\data\preflight.py
C:\Users\equin\Documents\institutional-ea\tests\test_preflight.py
C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-001-m1-data-acquisition.md
C:\Users\equin\Documents\institutional-ea\docs\operations\MT5_M1_EXPORT_CHECKLIST.md
C:\Users\equin\Documents\institutional-ea\HANDOFF_16.md
Real data files are local and gitignored:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
Do not commit raw data.

Important .gitignore note:

The rule is root-anchored:

text
/data/
Do NOT change it to unanchored:

text
data/
Reason:

Unanchored data/ previously risked excluding:

text
quantcore/data/
Phase 3 Summary
Phase 3.1 — Fill engine
Commit:

text
8302380 Phase 3.1: add M1 intrabar fill engine foundation
Files:

text
quantcore/backtest/fill_engine.py
tests/test_fill_engine.py
Important fill rule:

If stop and take-profit are both touched in the same M1 bar, stop wins.

This is conservative because M1 OHLC does not reveal tick order inside the minute.

Phase 3.2 — Cost model
Commit:

text
e257928 Phase 3.2: add broker execution cost model
Files:

text
quantcore/backtest/cost_model.py
tests/test_cost_model.py
Defaults:

USDJPY:

text
spread_price = 0.01
commission_usd_per_lot_per_fill = 7.0
stop_slippage_atr_fraction = 0.05
XAUUSD:

text
spread_price = 0.30
commission_usd_per_lot_per_fill = 10.0
stop_slippage_atr_fraction = 0.05
Commission is per fill. A round trip charges entry and exit.

Phase 3.3 — Portfolio accounting
Commit:

text
a6a6b15 Phase 3.3: add USD portfolio accounting primitives
Files:

text
quantcore/backtest/portfolio.py
tests/test_portfolio.py
Important P&L rule:

XAUUSD P&L is already USD.
USDJPY P&L is JPY and must be divided by the USDJPY conversion price to become USD.
Phase 3.4 — H017 event-driven backtest bridge
Commit:

text
b97723a Phase 3.4: add H017 event-driven backtest bridge
Files:

text
quantcore/backtest/h017_event.py
tests/test_h017_event.py
Timing convention:

H017 decides at H4 timestamp t.
Trade opens on next H4 bar open t+1.
M1 bars inside [t+1, t+2) resolve stops.
If no stop is hit, exposure closes at t+2 open as signal_flip.
This is a bridge-layer simplification. H017 outputs per-bar target risk exposure, not persistent broker order tickets.

Phase 3.5 — Real-data event smoke script
Commit:

text
bf5dc22 Phase 3.5: add real-data H017 event smoke script
File:

text
scripts/run_h017_event_real.py
Purpose:

Load real Exness H4 and M1 exports.
Detect and trim H4 D1-disguised-as-H4 leakage.
Trim M1 to common clean window.
Run event-driven H017 backtest.
Build H017 claim from realistic event-driven returns.
Print fill count, equity, drawdown, Sharpe, and claim.
Phase 3.6 — Add M1 coverage guard to event smoke
Commit:

text
34cf34b Phase 3.6: add M1 coverage guard to event smoke
File:

text
scripts/run_h017_event_real.py
Purpose:

Distinguish pipeline smoke success from research-grade validation sufficiency.

Current M1 common window is too short.

Phase 3.7 — Promote M1 coverage guard to tested library code
Commit:

text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
Files:

text
quantcore/data/coverage.py
tests/test_coverage.py
scripts/run_h017_event_real.py
Focused tests:

powershell
pytest tests\test_coverage.py -q
Expected:

text
7 passed
Coverage API:

python
@dataclass(frozen=True)
class CoverageAssessment:
    desired_m1_start_utc: pd.Timestamp
    actual_common_start_utc: pd.Timestamp
    actual_common_end_utc: pd.Timestamp
    n_common_h4_bars: int
    minimum_research_h4_bars: int
    meets_desired_m1_start: bool
    has_minimum_h4_bars: bool
    research_sufficient: bool
    reasons: tuple[str, ...]
Main function:

python
assess_m1_research_coverage(
    *,
    desired_m1_start_utc: object,
    actual_common_start_utc: object,
    actual_common_end_utc: object,
    n_common_h4_bars: int,
    minimum_research_h4_bars: int,
) -> CoverageAssessment
Behavior:

Converts naive timestamps to UTC.
Converts aware timestamps to UTC.
Rejects negative H4 bar count.
Rejects non-positive minimum H4 bar count.
Rejects empty/reversed windows.
research_sufficient=True only if actual common start is at or before desired M1 start AND common H4 bars >= minimum.
Current Real Data State
Real H4 files:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
Real M1 files:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
These are gitignored.

Current verified real-data event smoke output before DR-001 included:

text
USDJPY H4: rows=8708 bars=8708 earliest=2018-07-02 21:00:00+00:00 latest=2026-04-29 09:00:00+00:00
XAUUSD H4: rows=8658 bars=8658 earliest=2018-06-27 21:00:00+00:00 latest=2026-04-30 05:00:00+00:00
USDJPY M1: rows=97907 bars=97907 earliest=2026-01-26 03:09:00+00:00 latest=2026-04-30 07:00:00+00:00
XAUUSD M1: rows=97966 bars=97966 earliest=2026-01-20 02:22:00+00:00 latest=2026-04-30 07:00:00+00:00
H4 leakage scan:

text
USDJPY H4: first_reliable_date=2021-07-02 00:00:00 leaked_dates=933 weekend_dates=256 total_dates=2442
XAUUSD H4: first_reliable_date=2021-07-02 00:00:00 leaked_dates=933 weekend_dates=257 total_dates=2435
Clean common event window:

text
start_utc=2026-01-26 03:09:00+00:00
end_utc=2026-04-29 09:00:00+00:00
USDJPY H4 bars=417
XAUUSD H4 bars=411
USDJPY M1 bars=96587
XAUUSD M1 bars=91154
Coverage guard:

text
desired_m1_start_utc=2021-07-02 00:00:00+00:00
actual_common_start_utc=2026-01-26 03:09:00+00:00
actual_common_end_utc=2026-04-29 09:00:00+00:00
n_common_h4_bars=411
minimum_research_h4_bars=1512
meets_desired_m1_start=False
has_minimum_h4_bars=False
research_sufficient=False
Event-driven backtest:

text
symbols=('USDJPY', 'XAUUSD')
n_bars=411
fills=470
starting_equity_usd=10000.00
ending_equity_usd=16145.60
total_return_pct=61.46
max_drawdown_pct=-33.65
annualized_sharpe=1.3218
Claim:

text
H017 Claim Summary (n=470, ppy=1512)
  PSR:    psr=0.8662  obs_SR=+1.3218  [FAIL >= 0.95]
  MinTRL: feasible=True  min_n=1034  have_n=470  [FAIL]
  DSR:    SKIPPED (no sr_estimates provided)
  PROMOTABLE: False
Operational verdict:

text
PIPELINE SMOKE PASSED: True
RESEARCH VALIDATION SUFFICIENT: False
Interpretation:

The event pipeline works.
Available M1 history is too short to treat this as research-grade validation.
Do not trust the +61.46% short-window return as validated edge.
The -33.65% drawdown is a serious risk signal, but still not a research-grade full-period conclusion.
Broker and Data Conventions
Broker timezone:

text
Europe/Athens
Meaning:

Winter UTC+2.
Summer UTC+3.
DST-aware.
MT5 loader:

python
load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult
The loader:

Localizes raw MT5 wall-clock timestamps to Athens.
Converts to UTC.
Enforces canonical OHLCV.
MT5 History Center columns:

text
<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>
Mapping:

text
<TICKVOL> -> volume
Dropped:

text
<VOL>
<SPREAD>
Reason:

OTC FX real volume is usually zero.
Spread re-enters through cost model, not canonical OHLCV.
DST localization:

text
ambiguous="infer"
nonexistent="shift_forward"
H4 leakage issue:

Exness MT5 H4 export delivered daily bars disguised as H4 from 2018-07 through 2021-07-01.
Genuine H4 starts on 2021-07-02.
This issue appears symmetrically across USDJPY and XAUUSD.
Correct leakage heuristic:

D1-disguised-as-H4 leakage appears as a contiguous low-count region at the START of the series.
Do not walk backward from the last suspect date.
Forex weekends create sporadic low-count days throughout history.
Correct heuristic is first date with at least threshold bars.
Strategy Logic Conventions
ATR:

Wilder RMA, not SMA.
First true range is high - low.
Seed at index window - 1 with simple mean of first window true ranges.
Recurrence:
text
ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n
Chandelier Exit:

Long:

text
highest_high(lookback) - multiplier * ATR
Short:

text
lowest_low(lookback) + multiplier * ATR
Defaults:

text
multiplier = 3.0
lookback = 22
Vol Target:

Realized vol at bar t uses returns through t-1 only:

text
returns.shift(1).rolling(lookback)
No lookahead.

For H4 bars:

text
periods_per_year = 1512
Signals:

Donchian breakout.

Long:

text
close[t] > max(high[t-N ... t-1])
Short:

text
close[t] < min(low[t-N ... t-1])
Channel uses prior N bars:

text
shift(1).rolling(N)
Output:

text
-1, 0, +1, NaN
Defaults:

text
USDJPY lookback 20, no ATR floor
XAUUSD lookback 20, min_atr_pct = 0.003, requires atr14 column
Heat Governor:

Combined heat:

text
sqrt(w' (r² * C) w)
Where:

w is direction vector.
C is correlation matrix.
diagonal is 1.0.
off-diagonals floored at correlation_floor.
Defaults:

text
cap = 0.015
per_trade_risk = 0.01
correlation_window = 120
correlation_floor = 0.0
Warm-up uses identity matrix.

H017 Integration:

H017 inner-joins USDJPY and XAUUSD timestamps.
H017 computes close-to-close returns.
H017 uses same returns for vol targeting and heat governor.
Position is signed risk exposure.
Position:

text
signal × per_trade_risk × vol_mult × heat_mult
Zero-Cost H017 Result
Phase 2.6b zero-cost real H4 result after leakage trim:

text
7719 H4 bars from 2021-07-02 onward
Claim:

text
H017 Claim Summary (n=7719, ppy=1512)
  PSR:    psr=0.8634  obs_SR=+0.4920  [FAIL >= 0.95]
  MinTRL: feasible=True  min_n=17392  have_n=7719  [FAIL]
  DSR:    SKIPPED (no sr_estimates provided)
  PROMOTABLE: False
Interpretation:

H017 has qualified positive edge at zero cost.
It is not statistically promotable.
It needs more data and/or higher raw Sharpe.
Realistic costs likely reduce Sharpe.
This does not kill H017; it calibrates expectations.
Zero-cost script:

powershell
python scripts\run_h017_real.py
Important APIs
Before using these, inspect signatures in the repo.

Known recent signatures:

python
run_h017(
    usdjpy_ohlcv: pd.DataFrame,
    xauusd_ohlcv: pd.DataFrame,
    config: H017Config | None = None,
) -> H017Result

backtest_h017(
    usdjpy_ohlcv,
    xauusd_ohlcv,
    config=None,
) -> H017BacktestResult

build_h017_claim(
    returns: pd.Series,
    *,
    periods_per_year: int = 1512,
    sr_benchmark: float = 0.0,
    confidence: float = 0.95,
    psr_threshold: float = 0.95,
    sr_estimates: np.ndarray | pd.Series | None = None,
    dsr_threshold: float = 0.95,
) -> H017Claim

backtest_h017_event_driven(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    config: H017Config | None = None,
    starting_equity_usd: float = 10000.0,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
) -> H017EventBacktestResult

load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult

detect_d1_leakage(
    bars: pd.DataFrame,
    broker_tz: str,
    min_bars_per_day: int = 4,
) -> LeakageScan

trim_to_common_start(
    usdjpy: pd.DataFrame,
    xauusd: pd.DataFrame,
    start_date_utc: pd.Timestamp,
) -> tuple[pd.DataFrame, pd.DataFrame]
Strategy Graveyard
Immutable history:

H001: Backtest without intrabar SL/TP simulation is fiction. Must use M1 within H4 bars to resolve fills.
H002–H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
H004a: Single-seed models unreliable; use multi-seed ensembles.
H005: Stacked multi-symbol models fail on heterogeneous instruments; use per-symbol models.
H006–H007: Confidence filters are not risk management. ML chooses entries; deterministic rules manage risk.
H008–H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals cannot be risk manager.
H011–H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk ceiling remained.
H014–H016: Two-asset USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1% per-trade risk was not 1% portfolio risk when trades overlapped. Drawdown breach was -19.43%.
H015: Diversification into negative-edge instruments destroys the portfolio.
H017: H016 plus portfolio heat governor. Alive but not promotable at zero cost on real data.
Known Deferred Static Warnings
Do not fix these inline unless doing a dedicated type-cleanup phase:

text
quantcore/data/outliers.py
.diff on NDArray

quantcore/data/loaders.py
pandas Index timezone method warnings

tests/test_loaders.py
pandas timezone warnings

quantcore/validation/purged_kfold.py
DatetimeIndex.asi8

quantcore/validation/cpcv.py
DatetimeIndex.asi8

tests/test_purged_kfold.py
DatetimeIndex.asi8

tests/test_checksums.py
scalar + float operator warning
Important Repo Hygiene Lessons
Do not repeat these mistakes:

.gitignore once had data/ unrooted, which silently excluded quantcore/data/.
Phase 1.5 commit was incomplete because lookahead.py was not added.
Phase 1.8 commit was incomplete because cpcv.py and __init__.py export update were not added.
Phase 2.4 had wrong indicator kwarg assumptions.
Phase 2.5 zero-return negative tests failed because PSR rejects zero variance. Use small-noise returns.
Phase 2.6a discovered _ensure_canonical was private. It was promoted via alias.
Phase 2.6a hit the walrus-in-assert trap. Do not use assert X := Y.
Phase 2.6b imported H017BacktestResult from the wrong module.
Phase 2.6b first leakage heuristic was wrong.
Phase 2.6c-ii synthetic MT5 CSV tests must skip weekends.
VS Code can keep unsaved buffers that overwrite edits.
Handoff docs must be complete and self-contained.
Phase 3.7 had an old GitHub DNS push failure, later resolved.
Phase 3.8 initially had a singular/plural test expectation mismatch:
actual one-file error was “MT5 export not found”
test initially expected “MT5 exports not found”
this was fixed before commit.
Phase 3.10-c push initially failed due to GitHub DNS/network issue, then succeeded on retry.
An empty HANDOFF_16.md was accidentally committed first; verify file sizes when creating handoff documents.
Phase 3.11 first checklist paste damaged Markdown code fences. It was fixed by overwriting the file from the top with indented code blocks.
Mandatory mitigations:

Always run tests.
Always inspect git status.
Always commit and push.
Always verify git ls-files after commits.
Treat test-count drops as regressions.
Do not continue new development while remote is behind unless explicitly instructed.
For handoff docs, check file length and first lines before committing.
If a Markdown file with code fences is damaged by paste, overwrite the affected file from the top.
Strategic Interpretation At Current Point
Current institutional conclusion:

Pipeline capability improved.
Research confidence did not improve enough to promote H017.
Operational discipline was preserved.
Main blocker is insufficient M1 history for research-grade event validation.
Phase 3.11 added an operational checklist to help acquire longer M1 data safely.
H017 is:

alive
not promotable
not ready for live trading based on current evidence
blocked by insufficient M1 history for research-grade event validation
Do NOT:

Broaden to more symbols yet.
Tune H017 parameters yet.
Add machine learning yet.
Treat the 2026 short-window +61.46% return as validated edge.
Ignore the -33.65% drawdown.
Switch data vendors silently.
Start Phase 4 code unless the user explicitly chooses that path after Phase 3 status is documented.
Start new development while local commits are unpushed.
Commit raw data.
Change /data/ in .gitignore to data/.
Exact First Response The Next AI Should Give
The next AI should respond briefly:

“Understood. I’m continuing after Phase 3.11.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Current full-test anchor is 482 passed.
Latest verified commit is 75db15d Add MT5 M1 export operations checklist.
H017 is alive but not promotable.
Realistic event pipeline works, but current M1 coverage is too short for research-grade validation.
DR-001 exists at:
C:\Users\equin\Documents\institutional-ea\docs\decisions\DR-001-m1-data-acquisition.md
The MT5 M1 export checklist exists at:
C:\Users\equin\Documents\institutional-ea\docs\operations\MT5_M1_EXPORT_CHECKLIST.md
Recommended next sub-phase is Phase 3.12: add a real-data event validation run log template.
First task is hygiene verification only. No new code yet.
Please run:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -5
pytest -q
Then paste the full output.”

✅ done
⚠️ error — paste it
🤔 question