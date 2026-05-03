# Project Handoff — Institutional-Grade MT5 EA on Retail Stack (Continuation #14)

You are continuing an existing project that has gone through many AI handoffs. Read this entire document before responding. Do not invent context that is not here. When in doubt, ask the user before writing code.

## 1. Identity and Tone

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows. The user is intelligent but is NOT a professional developer. They have already burned through 16 dead strategies and are now building infrastructure-first.

Communication rules are non-negotiable:

- Step-by-step.
- Numbered steps.
- Explicit Windows file paths, for example:
  - `C:\Users\equin\Documents\institutional-ea\quantcore\data\coverage.py`
- Plain English.
- Define every technical term inline.
- Never write code without telling the user where the file goes and how to run it.
- After each sub-phase, give three response options:
  - ✅ done
  - ⚠️ error — paste it
  - 🤔 question
- Never skip git commits.
- Provide exact:
  - `git add ...`
  - `git commit -m "..."`
  - `git push`
- After EVERY commit, instruct the user to run:
  - `git status`
  - `git ls-files <touched-dirs>/`
- Read their output BEFORE moving on.
- Do not let `git status` go unread.
- If user reports passing tests but the COUNT dropped, treat as regression.
- Stack:
  - Windows
  - PowerShell
  - VS Code
  - Python 3.12.10
  - `.venv`
  - No WSL
  - No Linux assumptions
- One sub-phase per response.
- Code style:
  - `from __future__ import annotations` at top of every Python file.
  - type hints.
  - `@dataclass(frozen=True)` for structured returns.
  - docstrings explaining WHY, not just WHAT.
- Do NOT propose switching to a new AI chat. The user may already be doing that because the prior AI token budget is nearly exhausted. Continue directly.
- Before writing any module that calls internal functions, run `inspect.signature(...)` and, for dataclasses, `dataclasses.fields(...)` to verify the actual API.
- Do not trust remembered kwarg names.
- Prefer one consolidated multi-line import block per source module per consuming file.
- If a code block is cut off mid-paste, restart the affected file from the top in the next response. Do not try to merge with a partial paste.
- When the user asks for a handoff doc, produce a complete, fully self-contained version. Never write “same as prior handoff.”

## 2. Project Goal

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research:
  - Kaggle notebooks eventually.
- Execution:
  - MetaTrader 5.
- Production:
  - Oracle Cloud Always Free VPS.
- Monitoring:
  - self-hosted free-tier stack.
- User machine:
  - Windows.
  - PowerShell.
  - VS Code.
  - Python 3.12.10 in `.venv`.

The project is infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, or poor risk control.

Eight major phases:

1. Phase 0 — Foundation  
   Repo, CI, DVC, MLflow. Partially done. MLflow/DVC deferred.

2. Phase 1 — Research Framework  
   `quantcore` package. COMPLETE.

3. Phase 2 — H017 Strategy Logic  
   COMPLETE through real-data wiring.

4. Phase 3 — Realistic event-driven backtest engine  
   IN PROGRESS. Completed through Phase 3.7 locally. Phase 3.7 is committed locally but not pushed because GitHub DNS failed.

5. Phase 4 — MT5 EA shell + Python decision service.

6. Phase 5 — Free-tier VPS deployment  
   Oracle Cloud Always Free, Wine + MT5, Docker.

7. Phase 6 — Monitoring  
   Prometheus + Grafana + Loki + Telegram alerts.

8. Phase 7 — Governance & continuous improvement.

## 3. Repo Location

Repo root:

```text
C:\Users\equin\Documents\institutional-ea
Python venv:

text
C:\Users\equin\Documents\institutional-ea\.venv
GitHub remote:

text
https://github.com/citradinnda/institutional-ea.git
Expected branch:

text
main
4. Current Critical State
The latest local commit is:

text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
But push failed because of DNS/network:

text
fatal: unable to access 'https://github.com/citradinnda/institutional-ea.git/': Could not resolve host: github.com
The user then ran:

powershell
git status
git ls-files quantcore\data tests scripts
Output showed:

text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
(use "git push" to publish your local commits)

nothing to commit, working tree clean
So the local repo is clean, but remote GitHub is behind by one commit.

VERY IMPORTANT:

Do not write new code until this local commit is pushed successfully.
First action for the next AI should be to ask the user to retry:
powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git push
git status
git log --oneline -5
Expected after successful push:

text
Your branch is up to date with 'origin/main'.
and:

text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
should appear in git log --oneline -5.

5. Current Test Anchor
After Phase 3.7, the new source-of-truth test anchor is:

text
476 passed
This is up from the previous anchor:

text
469 passed
because Phase 3.7 added 7 tests in:

text
C:\Users\equin\Documents\institutional-ea\tests\test_coverage.py
The user verified:

text
pytest tests\test_coverage.py -q
7 passed in 1.32s
and:

text
pytest -q
476 passed in 11.95s
If a future full test run produces fewer than 476 passed, treat it as a regression.

6. Current Git History, Newest First
The latest known local history is:

text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
34cf34b Phase 3.6: add M1 coverage guard to event smoke
bf5dc22 Phase 3.5: add real-data H017 event smoke script
bb09cce Add handoff document #13 after Phase 3.4 event backtest bridge
b97723a Phase 3.4: add H017 event-driven backtest bridge
a6a6b15 Phase 3.3: add USD portfolio accounting primitives
e257928 Phase 3.2: add broker execution cost model
8302380 Phase 3.1: add M1 intrabar fill engine foundation
7fd956a Add handoff document #12 for AI continuity at end of Phase 2.6
e0923cf Phase 2.6c-ii: hermetic integration test for H017 real-data pipeline
Again: 850a915 is local and must still be pushed.

7. Current Important Layout
Important current layout:

text
institutional-ea/
├── .venv/                                  gitignored, Python 3.12.10
├── .gitignore                              /data/ root-anchored — do NOT change to data/
├── pyproject.toml
├── README.md
├── HANDOFF_3.md ... HANDOFF_13.md
├── data/
│   └── raw/
│       ├── USDJPY/
│       │   ├── H4.csv                      gitignored real Exness MT5 export
│       │   └── M1.csv                      gitignored real Exness MT5 export, starts around 2026
│       └── XAUUSD/
│           ├── H4.csv                      gitignored real Exness MT5 export
│           └── M1.csv                      gitignored real Exness MT5 export, starts around 2026
├── ea_mt5/                                 empty — Phase 4
├── governance/hypotheses/                  empty — future governance work
├── ops/                                    empty — Phase 5/6
├── quantcore/
│   ├── __init__.py
│   ├── backtest/
│   │   ├── __init__.py
│   │   ├── cost_model.py
│   │   ├── fill_engine.py
│   │   ├── h017_event.py
│   │   └── portfolio.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── checksums.py
│   │   ├── coverage.py                     added in Phase 3.7
│   │   ├── leakage.py
│   │   ├── loaders.py
│   │   ├── mt5_loader.py
│   │   ├── outliers.py
│   │   └── reconcile.py
│   ├── governance/
│   │   └── __init__.py
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── atr.py
│   │   ├── chandelier.py
│   │   └── vol_target.py
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── h017.py
│   │   ├── h017_claim.py
│   │   ├── heat_governor.py
│   │   └── signals.py
│   ├── utils/
│   │   └── __init__.py
│   └── validation/
│       ├── __init__.py
│       ├── cpcv.py
│       ├── deflated_sharpe.py
│       ├── lookahead.py
│       ├── metrics.py
│       ├── multiple_testing.py
│       ├── purged_kfold.py
│       ├── reality_check.py
│       ├── validator.py
│       └── walk_forward.py
├── research/                               empty — Kaggle notebooks later
├── scripts/
│   ├── run_h017_event_real.py              Phase 3.5/3.6/3.7 real-data event smoke
│   └── run_h017_real.py                    Phase 2.6b zero-cost real-data smoke
└── tests/
    ├── __init__.py
    ├── test_coverage.py                    added in Phase 3.7
    └── many other tests
Note: In one pasted git ls-files output, markdown rendering may have displayed __init__.py as init.py because underscores were interpreted strangely. Do not assume the actual files were renamed. The tests passed.

8. Phase Status
Phase 0 — Foundation
Partially done. Repo, Python package structure, tests, and tooling are usable. MLflow and DVC are deferred.

Phase 1 — Research Framework
Complete.

Includes:

Data loaders.
Reconciliation.
Outlier flagging.
Checksums.
Lookahead guards.
Purged K-Fold.
CPCV.
Walk-forward validation.
Deflated Sharpe.
White’s Reality Check.
Multiple testing corrections.
Validator orchestrator.
Phase 2 — H017 Strategy Logic
Complete.

Important commits:

text
a5ba37a Phase 2.1a: ATR
45ffe47 Phase 2.1b: Chandelier + vol-target
313ae55 Phase 2.2: per-symbol Donchian signals
66e87fa Phase 2.3: portfolio heat governor
adc5e3b Phase 2.4: H017 integration
b14eb5b Phase 2.5: validator-gated H017 claim
8c7e535 Phase 2.6a: MT5 CSV loader
aa4eed8 Phase 2.6b: real-data smoke script
fb116ff Phase 2.6c-i: leakage helpers promoted to library
e0923cf Phase 2.6c-ii: hermetic integration test
Phase 3 — Realistic Event-Driven Backtest Engine
In progress.

Completed:

Phase 3.1 — Fill engine
Commit:

text
8302380 Phase 3.1: add M1 intrabar fill engine foundation
Files:

text
quantcore/backtest/fill_engine.py
tests/test_fill_engine.py
Important rule:

If stop and take-profit are both touched in the same M1 bar, stop wins. This is conservative because M1 OHLC does not reveal tick order inside the minute.

Phase 3.2 — Cost model
Commit:

text
e257928 Phase 3.2: add broker execution cost model
Files:

text
quantcore/backtest/cost_model.py
tests/test_cost_model.py
Defaults:

text
USDJPY:
  spread_price = 0.01
  commission_usd_per_lot_per_fill = 7.0
  stop_slippage_atr_fraction = 0.05

XAUUSD:
  spread_price = 0.30
  commission_usd_per_lot_per_fill = 10.0
  stop_slippage_atr_fraction = 0.05
Commission is per fill. A round trip charges entry + exit.

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
Important timing convention:

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
The script ran successfully.

Key output before Phase 3.6 guard:

text
fills=470
ending_equity_usd=16145.60
total_return_pct=61.46
max_drawdown_pct=-33.65
annualized_sharpe=1.3218
PROMOTABLE: False
Do not treat this as validated edge because M1 history only covers 2026.

Phase 3.6 — Add M1 coverage guard to event smoke
Commit:

text
34cf34b Phase 3.6: add M1 coverage guard to event smoke
File:

text
scripts/run_h017_event_real.py
Purpose:

Make the script explicitly distinguish pipeline smoke success from research-grade validation sufficiency.
Current M1 common window is too short.
Verified script output included:

text
Coverage guard
desired_m1_start_utc=2021-07-02 00:00:00+00:00
actual_common_start_utc=2026-01-26 03:09:00+00:00
actual_common_end_utc=2026-04-29 09:00:00+00:00
n_common_h4_bars=411
minimum_research_h4_bars=1512
meets_desired_m1_start=False
has_minimum_h4_bars=False
research_sufficient=False
and:

text
PIPELINE SMOKE PASSED: True
RESEARCH VALIDATION SUFFICIENT: False
Phase 3.7 — Promote M1 coverage guard to tested library code
Commit:

text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
IMPORTANT: This commit is LOCAL ONLY at handoff time. Push failed due GitHub DNS. Must push before doing anything else.

Files added/changed:

text
quantcore/data/coverage.py
tests/test_coverage.py
scripts/run_h017_event_real.py
Test count increased:

text
469 passed
to:

text
476 passed
New focused test output:

text
pytest tests\test_coverage.py -q
7 passed
Full test output:

text
pytest -q
476 passed
The script still ran successfully after refactor and printed:

text
PIPELINE SMOKE PASSED: True
RESEARCH VALIDATION SUFFICIENT: False
9. Current Real Data State
Real H4 files:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
Real M1 files:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
These are gitignored because /data/ is root-anchored in .gitignore. Do not commit data files.

The user reported that MT5 maxed out M1 export at 2026. Current M1 coverage from the smoke script:

text
USDJPY M1: rows=97907 bars=97907 earliest=2026-01-26 03:09:00+00:00 latest=2026-04-30 07:00:00+00:00
XAUUSD M1: rows=97966 bars=97966 earliest=2026-01-20 02:22:00+00:00 latest=2026-04-30 07:00:00+00:00
Current H4 clean region after leakage detection:

text
first_reliable_date=2021-07-02 00:00:00
But because M1 begins in 2026, common event-driven validation window is only:

text
2026-01-26 03:09:00+00:00 to 2026-04-29 09:00:00+00:00
Current common H4 bars:

text
n_common_h4_bars=411
Research minimum used by the guard:

text
minimum_research_h4_bars=1512
That is one approximate H4 trading year using H017’s current periods-per-year setting.

10. Important API Signatures Verified Recently
The user ran inspection before Phase 3.5.

H017 strategy and claim APIs
python
run_h017(
    usdjpy_ohlcv: pd.DataFrame,
    xauusd_ohlcv: pd.DataFrame,
    config: H017Config | None = None,
) -> H017Result
python
backtest_h017(
    usdjpy_ohlcv,
    xauusd_ohlcv,
    config=None,
) -> H017BacktestResult
python
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
H017Result fields:

text
positions
signals
stops_long
stops_short
vol_multipliers
heat_multipliers
heat_pre
heat_post
heat_binding
H017Config fields:

text
atr_window
chandelier_mult
chandelier_lookback
vol_target
vol_lookback
vol_max_leverage
periods_per_year
usdjpy_signal
xauusd_signal
heat
H017Claim fields:

text
psr
min_trl
dsr
n_trials
periods_per_year
n_bars
promotable
summary
Backtest APIs
Fill fields:

text
symbol
side
entry_time_utc
entry_price
exit_time_utc
exit_price
lots
pnl_quote
commission
slippage
exit_reason
H017EventBacktestResult fields:

text
h017
portfolio
fills
n_bars
symbols
Main event functions:

python
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
python
backtest_h017_event_from_result(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    starting_equity_usd: float = 10000.0,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
) -> H017EventBacktestResult
MT5 loader API
python
load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult
MT5LoadResult fields:

text
bars
n_bars
n_input_rows
earliest_utc
latest_utc
broker_tz
Default broker timezone:

text
Europe/Athens
Leakage API
python
detect_d1_leakage(
    bars: pd.DataFrame,
    broker_tz: str,
    min_bars_per_day: int = 4,
) -> LeakageScan
python
trim_to_common_start(
    usdjpy: pd.DataFrame,
    xauusd: pd.DataFrame,
    start_date_utc: pd.Timestamp,
) -> tuple[pd.DataFrame, pd.DataFrame]
LeakageScan fields:

text
first_reliable_date
leaked_dates
weekend_dates
total_dates
broker_tz
Note from runtime: leaked_dates and weekend_dates are integers/counts in actual runtime, not collections. The script has _count_or_len(...) to support either representation.

New Phase 3.7 coverage API
File:

text
quantcore/data/coverage.py
Contains:

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
Converts timezone-aware timestamps to UTC.
Rejects negative H4 bar count.
Rejects non-positive minimum H4 bar count.
Rejects empty or reversed windows.
Returns research_sufficient=True only if:
actual common start is at or before desired M1 start, and
common H4 bars are at least minimum required bars.
11. Strategy Logic Conventions
ATR
Wilder RMA, not SMA.

First true range is high - low.

Seed at index window - 1 with simple mean of first window true ranges.

Recurrence:

text
ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n
Chandelier Exit
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
Vol Target
Realized vol at bar t uses returns through t-1 only:

python
returns.shift(1).rolling(lookback)
No lookahead.

For H4 bars:

text
periods_per_year = 1512
Signals
Donchian breakout:

Long:

text
close[t] > max(high[t-N ... t-1])
Short:

text
close[t] < min(low[t-N ... t-1])
Channel uses prior N bars:

python
shift(1).rolling(N)
Output:

text
-1, 0, +1, NaN
Name:

text
signal
Warm-up is NaN.

Default:

text
USDJPY lookback 20, no ATR floor
XAUUSD lookback 20, min_atr_pct = 0.003, requires atr14 column
Heat Governor
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

H017 Integration
H017:

inner-joins USDJPY and XAUUSD timestamps.
computes close-to-close returns.
uses same returns for vol targeting and heat governor.
Position:

text
signal × per_trade_risk × vol_mult × heat_mult
Position is signed fraction of equity at risk.

Phase 3 converts this to lots.

H017 Claim
Phase 2.5 zero-cost backtest rule:

text
P&L[t] = position[t-1] * close.pct_change()[t]
This t+1 lag is load-bearing:

position decided at close of bar t.
cannot trade until bar t+1.
Portfolio returns are sum across symbols.

Zero-cost result is only a calibration reference, not realistic execution.

12. Real-Data Findings So Far
Phase 2.6b Zero-Cost H017 Result
Real Exness H4 data after leakage trim:

text
7719 H4 bars from 2021-07-02 onward
Zero-cost H017 result:

text
H017 Claim Summary (n=7719, ppy=1512)
  PSR:    psr=0.8634  obs_SR=+0.4920  [FAIL >= 0.95]
  MinTRL: feasible=True  min_n=17392  have_n=7719  [FAIL]
  DSR:    SKIPPED (no sr_estimates provided)
  PROMOTABLE: False
VERDICT: NOT PROMOTABLE
Interpretation:

H017 has qualified positive edge at zero cost.
It is not statistically promotable.
It needs more data and/or higher raw Sharpe.
Phase 3 realistic costs likely reduce Sharpe.
This does not automatically kill H017; it calibrates expectations.
Script to reproduce zero-cost result:

powershell
python scripts\run_h017_real.py
Phase 3.5/3.6 Realistic Event Smoke Result
Current M1 data is only 2026 onward.

Script:

powershell
python scripts\run_h017_event_real.py
Key output:

text
USDJPY M1 earliest=2026-01-26 03:09:00+00:00
XAUUSD M1 earliest=2026-01-20 02:22:00+00:00
Common clean window:

text
start_utc=2026-01-26 03:09:00+00:00
end_utc=2026-04-29 09:00:00+00:00
USDJPY H4 bars=417
XAUUSD H4 bars=411
USDJPY M1 bars=96587
XAUUSD M1 bars=91154
Event result:

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
Coverage guard:

text
PIPELINE SMOKE PASSED: True
RESEARCH VALIDATION SUFFICIENT: False
Interpretation:

Infrastructure works.
M1 coverage is too short for research-grade validation.
High return over this tiny window is not trusted.
Max drawdown of -33.65% is a serious risk signal.
13. MT5 Data Conventions
Broker timezone:

text
Europe/Athens
This means:

winter: UTC+2.
summer: UTC+3.
DST-aware.
MT5 loader:

localizes raw wall-clock timestamp to Athens.
converts to UTC.
calls canonical OHLCV enforcement.
Example:

text
CSV bar 2024.06.03 04:00:00
Athens summer UTC+3
becomes 2024-06-03 01:00:00 UTC
MT5 History Center export columns:

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

OTC FX real <VOL> is usually zero.
Spread may re-enter via cost model, not canonical OHLCV.
DST localization:

python
ambiguous="infer"
nonexistent="shift_forward"
H4 leakage issue:

Exness MT5 H4 export delivered daily bars disguised as H4 from 2018-07 through 2021-07-01.
Genuine H4 starts on 2021-07-02.
This issue appears symmetrically across USDJPY and XAUUSD.
Use leakage detector to auto-trim.
Correct leakage heuristic:

D1-disguised-as-H4 leakage appears as a contiguous low-count region at the START of the series.
Do not walk backward from the last suspect date.
Forex weekends create sporadic low-count days throughout history.
Correct heuristic is first date with at least threshold bars.
14. Strategy Graveyard
Immutable history:

text
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
15. Known Deferred Static Warnings
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
16. Repo Hygiene Lessons
Do not repeat these mistakes:

.gitignore once had data/ unrooted, which silently excluded quantcore/data/. It was fixed to /data/.
Phase 1.5 commit was incomplete because lookahead.py was not added.
Phase 1.8 commit was incomplete because cpcv.py and __init__.py export update were not added.
Phase 2.4 had wrong indicator kwarg assumptions. Always inspect signatures.
Phase 2.5 zero-return negative tests failed because PSR rejects zero variance. Use small-noise returns.
Phase 2.6a discovered _ensure_canonical was private. It was promoted via alias.
Phase 2.6a also hit the walrus-in-assert trap. Do not use assert X := Y.
Phase 2.6b imported H017BacktestResult from the wrong module. Use consolidated imports.
Phase 2.6b first leakage heuristic was wrong. Correct leakage shape is contiguous low-count start region.
Phase 2.6b git push failed once due to DNS/network; local commit was fine.
Phase 2.6c-i promoted leakage helpers from script to library because tested logic belongs in quantcore/.
Phase 2.6c-ii synthetic MT5 CSV tests must skip weekends.
VS Code can keep unsaved buffers that overwrite edits. If a change seems ignored, verify with Get-Content.
Handoff docs must be complete and self-contained.
Phase 3.7 also had a git push DNS failure; local commit is clean and ahead by 1.
Mandatory mitigations:

Every sub-phase ends with:
git add ...
git commit -m "..."
git push
After every commit:
git status
git ls-files <touched-dirs>/
The AI must read output before continuing.
Test-count drops are regressions.
Inspect internal APIs before calling them.
Prefer consolidated imports.
If a code block is cut off, restart the file from the top.
17. First Reply For The Next AI
The next AI should NOT write code.

It should say it understands:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Current test anchor is 476 passed.
Phase 3.7 is committed locally as:
text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
But git push failed due GitHub DNS.
The repo is clean but ahead of origin by 1 commit.
First task is to retry the push and verify sync.
It should ask the user to run:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git push
git status
git log --oneline -5
pytest -q
Expected:

text
Your branch is up to date with 'origin/main'.
and:

text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
and:

text
476 passed
Only after reading that output should it continue.

18. Recommended Next Sub-Phase After Push Is Fixed
After Phase 3.7 is successfully pushed, recommended next sub-phase is probably:

text
Phase 3.8 — Add tested event-smoke result formatting or operational preflight hardening
But do not jump into that automatically.

Possible next directions:

Add tests around script-level formatting/preflight behavior only if useful.
Add a handoff document HANDOFF_14.md after Phase 3.7 is pushed.
Investigate options for deeper historical M1 data, but be careful:
Do not silently switch data vendors.
Vendor differences can invalidate broker-specific execution assumptions.
H4 came from Exness, so M1 should ideally come from the same Exness server.
Do not broaden symbols yet.
Do not tweak strategy logic yet.
The user previously asked if the EA can be tested across many pairs and anything Exness offers. Correct answer:

The validation framework is symbol-agnostic.
The strategy is intentionally scoped to USDJPY + XAUUSD because H015 showed that diversification into negative-edge instruments destroys the portfolio.
Each new symbol must become its own hypothesis: H018, H019, etc.
Mechanical scaling is easy. Edge validation per symbol is not.
Do not broaden the universe before H017 is live/stable on the two-asset core.
19. Exact Current Commands To Recover
First, recover failed push:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git push
git status
git log --oneline -5
pytest -q
If push fails again with DNS:

Do not recommit.
The commit already exists locally.
Ask the user to check internet/DNS and retry later.
Keep reminding that local repo is clean but remote is behind.
If push succeeds, then optionally add a handoff file in the repo:

text
C:\Users\equin\Documents\institutional-ea\HANDOFF_14.md
But only do that as its own sub-phase with tests/status/commit/push.

20. Last User State
The user’s last verified output before this handoff:

text
pytest tests\test_coverage.py -q
7 passed in 1.32s
text
pytest -q
476 passed in 11.95s
Commit:

text
[main 850a915] Phase 3.7: promote M1 coverage guard to tested library code
3 files changed, 209 insertions(+), 43 deletions(-)
create mode 100644 quantcore/data/coverage.py
create mode 100644 tests/test_coverage.py
Push failed:

text
fatal: unable to access 'https://github.com/citradinnda/institutional-ea.git/': Could not resolve host: github.com
Post-failed-push status:

text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
(use "git push" to publish your local commits)

nothing to commit, working tree clean
Continue from here.

## 21. Immediate Next AI Behavior

The next AI must start conservatively.

It should NOT:
- Write new code.
- Modify files.
- Re-run patches.
- Recommit Phase 3.7.
- Assume GitHub is synced.

It should first say something like:

“I understand Phase 3.7 is already committed locally as `850a915`, but the push failed because GitHub DNS could not resolve. The working tree is clean and local `main` is ahead of `origin/main` by 1 commit. Before any new code, we need to retry the push and verify the repository is synced.”

Then it should ask the user to run exactly:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git push
git status
git log --oneline -5
pytest -q
Expected after successful push:

text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
Expected git log --oneline -5 should include:

text
850a915 Phase 3.7: promote M1 coverage guard to tested library code
34cf34b Phase 3.6: add M1 coverage guard to event smoke
bf5dc22 Phase 3.5: add real-data H017 event smoke script
bb09cce Add handoff document #13 after Phase 3.4 event backtest bridge
b97723a Phase 3.4: add H017 event-driven backtest bridge
Expected full test output:

text
476 passed
If git push fails again with DNS:

text
Could not resolve host: github.com
then the AI should say:

This is a network/DNS problem, not a code problem.
The Phase 3.7 commit is already safe locally.
Do not recommit.
Retry git push later when internet/DNS is working.
Do not continue to new development while the remote is behind.
22. Phase 3.7 Files and Expected Content Summary
Phase 3.7 added:

text
C:\Users\equin\Documents\institutional-ea\quantcore\data\coverage.py
C:\Users\equin\Documents\institutional-ea\tests\test_coverage.py
and refactored:

text
C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
quantcore\data\coverage.py
Purpose:

Houses reusable, tested M1 coverage assessment logic.
Prevents short M1 event-smoke windows from being mistaken for research-grade validation.
Core public API:

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
python
def assess_m1_research_coverage(
    *,
    desired_m1_start_utc: object,
    actual_common_start_utc: object,
    actual_common_end_utc: object,
    n_common_h4_bars: int,
    minimum_research_h4_bars: int,
) -> CoverageAssessment:
Important behavior:

Naive timestamps are localized to UTC.
Timezone-aware timestamps are converted to UTC.
Negative n_common_h4_bars raises ValueError.
Non-positive minimum_research_h4_bars raises ValueError.
Empty/reversed windows raise ValueError.
research_sufficient=True only when:
actual common start is at or before desired M1 start, and
common H4 bar count is at least the required minimum.
tests\test_coverage.py
Contains 7 tests.

Expected focused output:

text
pytest tests\test_coverage.py -q
7 passed
Tests cover:

Short recent sample fails.
Full sufficient sample passes.
Earlier-than-needed M1 start passes.
Naive timestamps become UTC.
Aware timestamps convert to UTC.
Negative bar count is rejected.
Empty/reversed windows are rejected.
scripts\run_h017_event_real.py
Now imports the tested coverage logic:

python
from quantcore.data.coverage import CoverageAssessment, assess_m1_research_coverage
The script still handles operational orchestration:

Load MT5 H4 and M1 files.
Detect H4 leakage.
Trim to clean common window.
Assess M1 research coverage.
Run event-driven H017 backtest.
Build H017 claim.
Print operational verdict.
Expected current output still includes:

text
PIPELINE SMOKE PASSED: True
RESEARCH VALIDATION SUFFICIENT: False
because MT5 only exported M1 from 2026 onward.

23. Important Note About Weird Pasted Formatting
In the user’s pasted output, some file content displayed oddly:

text
from future import annotations
and:

text
REPO_ROOT = Path(file).resolve().parents[1]
and some indentation appeared missing.

However:

pytest tests\test_coverage.py -q passed with 7 tests.
python scripts\run_h017_event_real.py ran successfully.
pytest -q passed with 476 tests.
The Phase 3.7 commit succeeded.
Therefore, this was likely a display/markdown paste artifact in the chat, not actual broken source code.

Do not “fix” these unless a real file inspection or test failure proves they are broken.

If concerned, ask the user to run:

powershell
Get-Content quantcore\data\coverage.py -TotalCount 80
Get-Content tests\test_coverage.py -TotalCount 80
Get-Content scripts\run_h017_event_real.py -TotalCount 40
pytest -q
But do not do this before resolving the failed git push.

24. Recommended Next Sub-Phase After Push
Once 850a915 is pushed and verified, the recommended next action is probably:

text
Phase 3.8 — Add HANDOFF_14.md after Phase 3.7
Reason:

The project has just completed an important infrastructure milestone.
Phase 3.7 changed the current test anchor from 469 passed to 476 passed.
There was a failed push that future context must preserve.
A handoff document in the repo protects continuity.
If doing this, create:

text
C:\Users\equin\Documents\institutional-ea\HANDOFF_14.md
It must be complete and self-contained. Do not write “same as previous handoff.”

Suggested commit message:

text
Add handoff document #14 after Phase 3.7 coverage guard promotion
Commands after creating the file:

powershell
git add HANDOFF_14.md
git commit -m "Add handoff document #14 after Phase 3.7 coverage guard promotion"
git push
git status
git ls-files HANDOFF_14.md
But only do this after:

powershell
git push
git status
pytest -q
confirms Phase 3.7 is synced and 476 passed.

25. What Not To Do Next
Do not immediately:

Broaden to more symbols.
Add machine learning.
Tune H017 parameters.
Reduce risk because of the short 2026 result.
Trust the +61.46% short-window return.
Treat the -33.65% drawdown as final research-grade evidence.
Change cost assumptions without a dedicated phase.
Switch data vendors without explicitly documenting broker mismatch risk.
Rewrite the event bridge into persistent positions without a dedicated design phase.
Start Phase 4 MT5 EA shell before the Phase 3 status is documented.
26. Strategic Interpretation At This Exact Point
The current project status is:

H017 is alive but not promotable.
Zero-cost real H4 validation showed positive but statistically insufficient edge.
Realistic event-driven infrastructure now runs on real H4 + M1 data.
Current broker-exported M1 history is too short for research-grade validation.
The infrastructure correctly prevents us from overtrusting the short 2026 event result.
Test coverage increased and important coverage logic was promoted into quantcore.
The only immediate problem is GitHub DNS preventing push of the latest local commit.
Current institutional-grade conclusion:

text
Pipeline capability improved.
Research confidence did not improve enough to promote H017.
Operational discipline was preserved.
27. Exact First Response The Next AI Should Give
The next AI’s first response should be short and should not write code.

It should say:

text
Understood. I’m continuing from Phase 3.7.

I understand:
1. Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
2. Current full-test anchor is 476 passed.
3. Phase 3.7 was committed locally as:
   850a915 Phase 3.7: promote M1 coverage guard to tested library code
4. The push failed because GitHub DNS could not resolve.
5. The working tree is clean, but local main is ahead of origin/main by 1 commit.
6. First task is to retry the push and verify sync. No new code yet.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git push
git status
git log --oneline -5
pytest -q

Then paste the full output.
Then it should offer:

text
✅ done — pasted outputs
⚠️ error — paste it
🤔 question
28. Final Continuity Anchor
At the moment this handoff was written, the last verified user state was:

text
Local commit:
850a915 Phase 3.7: promote M1 coverage guard to tested library code

Push:
FAILED due DNS

Status:
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
nothing to commit, working tree clean

Focused tests:
7 passed

Full tests:
476 passed
Continue from this exact state.