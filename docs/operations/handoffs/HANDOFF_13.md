# Project Handoff — Institutional-Grade MT5 EA on Retail Stack (Continuation #13)

You are continuing an existing project that has gone through THIRTEEN AI handoffs. Read this entire document before responding. Do not invent context that isn't here. When in doubt, ask the user before writing code.

## 1. Identity and Tone

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows. The user is intelligent but is NOT a professional developer. They have already burned through 16 dead strategies and are now building infrastructure-first.

Communication rules are non-negotiable:

- Step-by-step.
- Numbered steps.
- Explicit Windows file paths, for example:
  - `C:\Users\equin\Documents\institutional-ea\quantcore\backtest\h017_event.py`
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
  - `from __future__ import annotations` at top of every file
  - type hints
  - `@dataclass(frozen=True)` for structured returns
  - docstrings explaining WHY, not just WHAT
- Do NOT propose switching to a new AI chat. If the user says the new AI returned “No response provided,” continue the work directly in the current chat.
- Before writing any module that calls internal functions, run `inspect.signature(...)` and, for dataclasses, `dataclasses.fields(...)` to verify the actual API.
- Do not trust remembered kwarg names. Earlier phases had bugs from assuming internal API names.
- Prefer one consolidated multi-line import block per source module per consuming file.
- If a code block is cut off mid-paste, restart the affected file from the top in the next response. Do not try to merge with a partial paste.
- When the user asks for a handoff doc, produce a complete, fully self-contained version. Never write “same as prior handoff.” The next AI may have no access to earlier handoffs.

## 2. Project Goal

Build a USDJPY + XAUUSD MT5 expert advisor with institutional-grade epistemology on a retail stack.

Target environment:

- Research:
  - Kaggle notebooks eventually
- Execution:
  - MetaTrader 5
- Production:
  - Oracle Cloud Always Free VPS
- Monitoring:
  - self-hosted free-tier stack
- User machine:
  - Windows
  - PowerShell
  - VS Code
  - Python 3.12.10 in `.venv`

The project is deliberately infrastructure-first because prior strategy attempts failed due to weak validation, fictional backtesting, or poor risk control.

Eight major phases:

1. Phase 0 — Foundation  
   Repo, CI, DVC, MLflow. Partially done. MLflow/DVC deferred.

2. Phase 1 — Research Framework  
   `quantcore` package. COMPLETE.

3. Phase 2 — H017 Strategy Logic  
   COMPLETE through real-data wiring.

4. Phase 3 — Realistic event-driven backtest engine  
   IN PROGRESS. Completed through Phase 3.4.

5. Phase 4 — MT5 EA shell + Python decision service.

6. Phase 5 — Free-tier VPS deployment  
   Oracle Cloud Always Free, Wine + MT5, Docker.

7. Phase 6 — Monitoring  
   Prometheus + Grafana + Loki + Telegram alerts.

8. Phase 7 — Governance & continuous improvement.

## 3. Repo Location and Layout

Repo root:

```text
C:\Users\equin\Documents\institutional-ea
Current important layout after Phase 3.4:

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
│       │   └── H4.csv                      gitignored real Exness MT5 export
│       └── XAUUSD/
│           └── H4.csv                      gitignored real Exness MT5 export
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
│   └── run_h017_real.py                    Phase 2.6b zero-cost real-data smoke
└── tests/
    ├── __init__.py
    ├── test_atr.py
    ├── test_chandelier.py
    ├── test_checksums.py
    ├── test_cost_model.py
    ├── test_cpcv.py
    ├── test_deflated_sharpe.py
    ├── test_fill_engine.py
    ├── test_h017.py
    ├── test_h017_claim.py
    ├── test_h017_event.py
    ├── test_heat_governor.py
    ├── test_integration_h017_pipeline.py
    ├── test_leakage.py
    ├── test_loaders.py
    ├── test_lookahead.py
    ├── test_metrics.py
    ├── test_min_trl.py
    ├── test_mt5_loader.py
    ├── test_multiple_testing.py
    ├── test_outliers.py
    ├── test_portfolio.py
    ├── test_purged_kfold.py
    ├── test_reality_check.py
    ├── test_reconcile.py
    ├── test_signals.py
    ├── test_smoke.py
    ├── test_validator.py
    ├── test_vol_target.py
    └── test_walk_forward.py
4. Current Test Anchor
After Phase 3.4:

text
469 passed
This is the current source-of-truth anchor. Do not regress below this.

Recent user-verified output:

text
pytest tests\test_h017_event.py -q
10 passed

pytest -q
469 passed
The user also verified:

text
git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
5. Current Git State
Most recent commits, newest first:

text
b97723a Phase 3.4: add H017 event-driven backtest bridge
a6a6b15 Phase 3.3: add USD portfolio accounting primitives
e257928 Phase 3.2: add broker execution cost model
8302380 Phase 3.1: add M1 intrabar fill engine foundation
7fd956a Add handoff document #12 for AI continuity at end of Phase 2.6 (full self-contained version)
e0923cf Phase 2.6c-ii: hermetic integration test for H017 real-data pipeline (3 tests, 423 total)
fb116ff Phase 2.6c-i: promote leakage helpers to quantcore.data.leakage (7 tests, 420 total)
aa4eed8 Phase 2.6b: real-data smoke script for H017 (Exness USDJPY+XAUUSD H4, D1-leakage auto-detect)
8288d93 Add handoff document #11 for AI continuity at end of Phase 2.6a (full self-contained version)
8c7e535 Phase 2.6a: MT5 History Center CSV loader (Exness Athens-tz aware) + ensure_canonical public alias (15 tests, 413 total)
GitHub remote:

text
https://github.com/citradinnda/institutional-ea.git
Expected branch:

text
main
Expected sync state:

text
main up to date with origin/main
6. Mandatory Hygiene Verification Before Any New Code
Before writing any new code, ask the user to run:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git log --oneline -10
git ls-files quantcore/ tests/ scripts/
git status
git remote -v
pytest -q
Confirm:

Working tree clean.
Branch is up to date with origin/main.
HEAD includes:
b97723a Phase 3.4: add H017 event-driven backtest bridge
the HANDOFF_13 commit, if this handoff has been saved/committed.
pytest -q ends with exactly:
text
469 passed
If the count drops, stop and diagnose.

Before writing any module that calls validator, H017, MT5 loader, leakage, or backtest internals, run inspect commands.

Core H017 inspection:

powershell
python -c "import dataclasses, inspect; from quantcore.strategy.h017 import H017Result, H017Config, run_h017; from quantcore.strategy.h017_claim import H017BacktestResult, H017Claim, backtest_h017, build_h017_claim; [print(c.__name__, [f.name for f in dataclasses.fields(c)]) for c in [H017Result, H017Config, H017BacktestResult, H017Claim]]; print(inspect.signature(run_h017)); print(inspect.signature(backtest_h017)); print(inspect.signature(build_h017_claim))"
Backtest inspection:

powershell
python -c "import dataclasses, inspect; from quantcore.backtest.fill_engine import Fill, simulate_bracket_trade; from quantcore.backtest.cost_model import SymbolCostSpec, ExecutionCost, get_default_cost_spec, price_with_execution_costs; from quantcore.backtest.portfolio import InstrumentSpec, PositionSize, PortfolioResult, get_default_instrument_spec, size_position_from_risk, fill_pnl_usd, build_portfolio_result; from quantcore.backtest.h017_event import H017EventBacktestResult, backtest_h017_event_driven, backtest_h017_event_from_result; [print(c.__name__, [f.name for f in dataclasses.fields(c)]) for c in [Fill, SymbolCostSpec, ExecutionCost, InstrumentSpec, PositionSize, PortfolioResult, H017EventBacktestResult]]; print(inspect.signature(simulate_bracket_trade)); print(inspect.signature(price_with_execution_costs)); print(inspect.signature(size_position_from_risk)); print(inspect.signature(fill_pnl_usd)); print(inspect.signature(build_portfolio_result)); print(inspect.signature(backtest_h017_event_driven)); print(inspect.signature(backtest_h017_event_from_result))"
MT5 loader inspection:

powershell
python -c "import inspect, dataclasses; from quantcore.data.mt5_loader import load_mt5_csv, MT5LoadResult, DEFAULT_BROKER_TZ; print(inspect.signature(load_mt5_csv)); print('MT5LoadResult fields:', [f.name for f in dataclasses.fields(MT5LoadResult)]); print('DEFAULT_BROKER_TZ:', DEFAULT_BROKER_TZ)"
Leakage inspection:

powershell
python -c "import inspect, dataclasses; from quantcore.data.leakage import detect_d1_leakage, trim_to_common_start, LeakageScan, MIN_H4_BARS_PER_ACTIVE_DAY; print(inspect.signature(detect_d1_leakage)); print(inspect.signature(trim_to_common_start)); print('LeakageScan fields:', [f.name for f in dataclasses.fields(LeakageScan)]); print('MIN:', MIN_H4_BARS_PER_ACTIVE_DAY)"
7. Phase Status
Phase 0 — Foundation
Partially done. Repo, Python package structure, tests, and tooling are usable. MLflow and DVC are deferred.

Phase 1 — Research Framework
Complete.

Includes:

Data loaders
Reconciliation
Outlier flagging
Checksums
Lookahead guards
Purged K-Fold
CPCV
Walk-forward validation
Deflated Sharpe
White’s Reality Check
Multiple testing corrections
Validator orchestrator
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
Added 12 tests.

Key API:

python
@dataclass(frozen=True)
class Fill:
    symbol: str
    side: Literal["buy", "sell"]
    entry_time_utc: pd.Timestamp
    entry_price: float
    exit_time_utc: pd.Timestamp
    exit_price: float
    lots: float
    pnl_quote: float
    commission: float
    slippage: float
    exit_reason: Literal["stop", "tp", "signal_flip", "end_of_data"]
Key function:

python
simulate_bracket_trade(...)
Important fill-engine rule:

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
Added 11 tests.

Key dataclasses:

python
@dataclass(frozen=True)
class SymbolCostSpec:
    symbol: str
    spread_price: float
    commission_usd_per_lot_per_fill: float
    stop_slippage_atr_fraction: float = 0.05

@dataclass(frozen=True)
class ExecutionCost:
    symbol: str
    side: Literal["buy", "sell"]
    action: Literal["entry", "exit"]
    raw_price: float
    fill_price: float
    lots: float
    spread_paid_price: float
    slippage_price: float
    commission_usd: float
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
Important note:

Commission is currently per fill.
The Phase 3.4 bridge currently uses price_with_execution_costs for entry and exit, so a round trip charges entry + exit.
However tests in Phase 3.4 revealed expected commission values like XAUUSD 0.10 lots -> 2.0, implying 10 USD/lot/fill × 0.10 lots × 2 fills.
Do not silently change this.
Phase 3.3 — Portfolio accounting
Commit:

text
a6a6b15 Phase 3.3: add USD portfolio accounting primitives
Files:

text
quantcore/backtest/portfolio.py
tests/test_portfolio.py
Added 13 tests.

Key dataclasses:

python
@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    contract_size: float
    quote_currency: str
    lot_step: float = 0.01
    min_lot: float = 0.01

@dataclass(frozen=True)
class PositionSize:
    symbol: str
    side: Literal["buy", "sell"] | None
    signed_risk_fraction: float
    lots: float
    target_risk_usd: float
    actual_risk_usd: float
    notional_quote: float

@dataclass(frozen=True)
class PortfolioResult:
    fills: tuple[Fill, ...]
    starting_equity_usd: float
    ending_equity_usd: float
    equity_curve: pd.Series
    returns: pd.Series
    drawdowns: pd.Series
    max_drawdown: float
Defaults:

text
USDJPY:
  contract_size = 100,000
  quote_currency = JPY
  lot_step = 0.01
  min_lot = 0.01

XAUUSD:
  contract_size = 100
  quote_currency = USD
  lot_step = 0.01
  min_lot = 0.01
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
Added 10 tests.

Current Phase 3.4 API:

python
@dataclass(frozen=True)
class H017EventBacktestResult:
    h017: H017Result
    portfolio: PortfolioResult
    fills: tuple[Fill, ...]
    n_bars: int
    symbols: tuple[str, ...]
Functions:

python
backtest_h017_event_driven(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    config: H017Config | None = None,
    starting_equity_usd: float = 10_000.0,
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
    starting_equity_usd: float = 10_000.0,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
) -> H017EventBacktestResult
Important timing convention in Phase 3.4:

H017 decides at H4 timestamp t.
Trade opens on next H4 bar open t+1.
M1 bars inside [t+1, t+2) resolve stops.
If no stop is hit, exposure closes at t+2 open as signal_flip.
This is a bridge-layer simplification. H017 outputs per-bar target risk exposure, not persistent broker order tickets.
Important caution:

Phase 3.4 is a bridge, not the final production-grade portfolio simulator.
It is good enough to begin real-data event-driven smoke testing once M1 CSVs exist.
Later refinement may be needed for persistent positions/rebalances if results justify it.
8. Conventions Already Established
Canonical OHLCV
Canonical bar frames use:

text
open, high, low, close, volume
Rules:

lowercase columns
UTC timezone-aware DatetimeIndex
sorted ascending
no duplicates
ensure_canonical() exists in:

text
quantcore/data/loaders.py
Original private _ensure_canonical still exists for backward compatibility.

MT5 bar labeling
Use:

python
label="left", closed="left"
Bar timestamp is the bar OPEN time.

Tolerance
Comparisons in ATR units, not absolute price.
Float comparisons use tolerance, commonly < 1e-12, not exact equality.
Outliers
Flag, never auto-delete.

Tests
Tests live only in tests/.
Production code lives only in quantcore/.
Operational scripts live in scripts/.
Test count is a coverage signal.
If pytest collects fewer items after a change, treat it as regression.
Returns
Structured returns are frozen dataclasses:

python
@dataclass(frozen=True)
No bare tuples for meaningful multi-field returns.

Bootstrap
Block-bootstrap CIs use stationary bootstrap.
Default expected block length is n^(1/3).
Percentile CIs, not BCa.
Lookahead guard truncations
Default to four strategic truncation points:

early
middle
late
last
Use explicit truncations for operations sensitive to exact bar positions.

Validation framework
Purged K-Fold, CPCV, and WalkForward all accept optional t1.

If t1 is omitted, only embargo applies.

CPCV:

lexicographic combination ordering
with k >= 2, a single combination can legitimately appear multiple times in one path-column
WalkForward:

one class
mode: Literal["rolling", "anchored"]
Timezone trap:

pd.Series.values on timezone-aware datetimes strips timezone.
Use series.iloc[idx] and .to_numpy() only after timezone-safe comparison.
PSR / DSR / MinTRL
Important:

Formulas operate on per-period Sharpe.
Result field observed_sr is annualized for human display.
sr_benchmark argument is annualized and converted internally as:
sr_benchmark / sqrt(periods_per_year)
MinTRL infeasible sentinel:

text
observed_sr <= sr_benchmark
Return:

text
min_n = -1
min_n_years = inf
feasible = False
Do not raise.

Zero-variance trap:

probabilistic_sharpe_ratio raises ValueError when std < 1e-12.
For no-edge negative tests, use small random variance, not np.zeros.
White’s Reality Check
Rules:

stationary bootstrap
default block length round(T^(1/3))
recenter each strategy by subtracting its own observed mean excess
statistic is sqrt(T) * max_k(d_k)
sample row indices once per bootstrap replication and apply to all K columns
p-value is fraction of bootstrap reps with bootstrapped statistic >= observed statistic
Multiple testing
All corrections return the same dataclass.

Methods:

Bonferroni
Holm
Benjamini-Hochberg
Field value for BH:

text
benjamini_hochberg
not hyphenated.

FWER vs FDR:

Bonferroni and Holm control FWER.
BH controls FDR.
Use FWER for live-trading go/no-go gates.
Use FDR for early feature screening.
Validator orchestrator
PSR and MinTRL mandatory.
DSR / Reality Check / Multiple Testing opt-in based on inputs.
all_passed is AND of gates that ran.
Summary uses ASCII +/- only, not Unicode glyphs.
Indicator warm-up
NaN, not zero. Caller skips warm-up explicitly.

9. MT5 Data Conventions
Broker timezone
Exness MT5 server uses:

text
Europe/Athens
This means:

winter: UTC+2
summer: UTC+3
DST-aware
MT5 loader:

localizes raw wall-clock timestamp to Athens
converts to UTC
calls canonical OHLCV enforcement
Example:

CSV bar 2024.06.03 04:00:00
Athens summer UTC+3
becomes 2024-06-03 01:00:00 UTC
MT5 CSV columns
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
DST ambiguity
For localization:

python
ambiguous="infer"
nonexistent="shift_forward"
Existing real H4 CSVs
Current real files:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
These are gitignored.

Confirmed issue:

Exness MT5 H4 export delivered daily bars disguised as H4 from 2018-07 through 2021-07-01.
Genuine H4 starts on 2021-07-02.
This issue appears symmetrically across USDJPY and XAUUSD.
Use leakage detector to auto-trim.
Clean region after trim:

text
2021-07-02 onward
7719 H4 bars
Required next real M1 CSVs
Before real event-driven H017 smoke testing, user must export:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
Same MT5 History Center format as H4.

Important:

M1 files are expected to be large.
They are gitignored because /data/ is root-anchored in .gitignore.
Do not commit data files.
10. Actual APIs and Field Names
These have been verified in prior phases. Still inspect again before calling from new code.

Indicator signatures
python
average_true_range(df: pd.DataFrame, window: int = 14) -> pd.Series
python
chandelier_exit(
    df: pd.DataFrame,
    atr: pd.Series,
    multiplier: float = 3.0,
    lookback: int = 22,
    side: Side = "long",
) -> pd.Series
python
vol_target_size(
    returns: pd.Series,
    target_vol_annual: float = 0.1,
    lookback: int = 20,
    periods_per_year: int = 252,
    max_leverage: float = 3.0,
) -> pd.Series
Important:

chandelier_exit returns one Series per side.
Call twice for long and short.
vol_target_size takes returns Series, not DataFrame.
For H4 bars, periods_per_year = 1512.
H017 API
python
run_h017(
    usdjpy_ohlcv: pd.DataFrame,
    xauusd_ohlcv: pd.DataFrame,
    config: H017Config | None = None,
) -> H017Result
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
H017 claim API
backtest_h017 lives in:

text
quantcore.strategy.h017_claim
not in quantcore.strategy.h017.

Signatures:

python
backtest_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None) -> H017BacktestResult
python
build_h017_claim(
    returns: pd.Series,
    *,
    periods_per_year: int = 1512,
    sr_benchmark: float = 0.0,
    confidence: float = 0.95,
    psr_threshold: float = 0.95,
    sr_estimates = None,
    dsr_threshold: float = 0.95,
) -> H017Claim
H017BacktestResult fields:

text
portfolio_returns
per_symbol_returns
positions
n_bars
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
Leakage API
python
detect_d1_leakage(
    bars,
    broker_tz,
    min_bars_per_day=4,
) -> LeakageScan
python
trim_to_common_start(
    usdjpy,
    xauusd,
    start_date_utc,
) -> tuple[pd.DataFrame, pd.DataFrame]
LeakageScan fields:

text
first_reliable_date
leaked_dates
weekend_dates
total_dates
broker_tz
Constant:

text
MIN_H4_BARS_PER_ACTIVE_DAY = 4
Important leakage lesson:

D1-disguised-as-H4 leakage appears as a contiguous low-count region at the START of the series.
Do not walk backward from the last suspect date.
Forex weekends create sporadic low-count days throughout history.
Correct heuristic is first date with at least threshold bars.
Backtest APIs after Phase 3.4
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
simulate_bracket_trade signature:

python
simulate_bracket_trade(
    *,
    symbol: str,
    side: Side,
    entry_time_utc: pd.Timestamp,
    entry_price: float,
    lots: float,
    m1_bars: pd.DataFrame,
    stop_price: float | None = None,
    take_profit_price: float | None = None,
    forced_exit_time_utc: pd.Timestamp | None = None,
    forced_exit_price: float | None = None,
    contract_size: float = 1.0,
    commission: float = 0.0,
    stop_slippage: float = 0.0,
) -> Fill
Cost model:

python
get_default_cost_spec(symbol: str) -> SymbolCostSpec
python
price_with_execution_costs(
    *,
    symbol: str,
    side: Side,
    action: FillAction,
    raw_price: float,
    lots: float,
    cost_spec: SymbolCostSpec | None = None,
    exit_reason: ExitReason | None = None,
    atr: float | None = None,
) -> ExecutionCost
Portfolio:

python
get_default_instrument_spec(symbol: str) -> InstrumentSpec
python
size_position_from_risk(
    *,
    symbol: str,
    signed_risk_fraction: float,
    equity_usd: float,
    entry_price: float,
    stop_distance_price: float,
    instrument_spec: InstrumentSpec | None = None,
) -> PositionSize
python
fill_pnl_usd(
    *,
    fill: Fill,
    conversion_price: float | None = None,
    instrument_spec: InstrumentSpec | None = None,
) -> float
python
build_portfolio_result(
    *,
    fills: Sequence[Fill],
    starting_equity_usd: float = 10000.0,
) -> PortfolioResult
H017 event:

python
backtest_h017_event_driven(...)
python
backtest_h017_event_from_result(...)
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

USDJPY lookback 20, no ATR floor
XAUUSD lookback 20, min_atr_pct = 0.003, requires atr14 column
Heat Governor
Combined heat:

text
sqrt(w' (r² * C) w)
Where:

w is direction vector
C is correlation matrix
diagonal is 1.0
off-diagonals floored at correlation_floor
Defaults:

text
cap = 0.015
per_trade_risk = 0.01
correlation_window = 120
correlation_floor = 0.0
Warm-up uses identity matrix.

H017 Integration
H017:

inner-joins USDJPY and XAUUSD timestamps
computes close-to-close returns
uses same returns for vol targeting and heat governor
position:
text
signal × per_trade_risk × vol_mult × heat_mult
Position is signed fraction of equity at risk.

Phase 3 converts this to lots.

H017 Claim
Phase 2.5 zero-cost backtest rule:

text
P&L[t] = position[t-1] * close.pct_change()[t]
This t+1 lag is load-bearing:

position decided at close of bar t
cannot trade until bar t+1
Portfolio returns are sum across symbols.

Zero-cost result is only a calibration reference, not realistic execution.

12. Load-Bearing Real-Data Finding From Phase 2.6b
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
Phase 3 realistic costs will likely reduce Sharpe.
This does not automatically kill H017; it calibrates expectations.
Script to reproduce zero-cost result:

powershell
python scripts\run_h017_real.py
13. Strategy Graveyard
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
14. Current Phase 3 Design and Next Step
Phase 3 goal:

Replace fictional zero-cost return summation with realistic event-driven execution:

M1 intrabar fill simulation
spread
slippage
commission
lot sizing
USD account equity curve
drawdowns
returns series compatible with existing validator
Completed:

text
3.1 Fill engine
3.2 Cost model
3.3 Portfolio accounting
3.4 H017 event-driven bridge
Next recommended sub-phase:

text
Phase 3.5 — Real-data event smoke script for H017 event-driven backtest
Purpose:

Add an operational script, probably:
text
C:\Users\equin\Documents\institutional-ea\scripts\run_h017_event_real.py
It should:
Load H4 USDJPY and XAUUSD using existing load_mt5_csv.
Load M1 USDJPY and XAUUSD using same loader.
Detect and trim D1-disguised-as-H4 leakage on H4.
Trim H4 and M1 to common clean region.
Run backtest_h017_event_driven.
Build H017 claim using build_h017_claim(result.portfolio.returns, periods_per_year=1512).
Print fill count, equity, max drawdown, annualized Sharpe/claim summary, and verdict.
But this step is blocked until the user has exported:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
Alternative if user has not exported M1 yet:

text
Phase 3.5a — Add a preflight script that checks for M1 files and prints exact export instructions.
Recommended path:

Ask user whether M1 CSV files exist.
If not, give MT5 History Center export instructions.
If yes, run hygiene and inspect commands.
Then write scripts/run_h017_event_real.py.
15. MT5 M1 Export Instructions To Give User If Needed
Ask user to export M1 from MT5 History Center for the same broker/symbols:

Required files:

text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
Expected columns:

text
<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>
Important:

Same Exness account/server as H4.
Export as tab-separated MT5 History Center CSV.
Prefer full available range, but at minimum from:
text
2021-07-02 onward
Do not commit these files.
After export, ask user to run:

powershell
cd C:\Users\equin\Documents\institutional-ea
Get-ChildItem data\raw\USDJPY
Get-ChildItem data\raw\XAUUSD
Confirm M1.csv exists in both folders.

16. Known Deferred Static Warnings
Do not fix these inline unless doing a dedicated type-cleanup phase:

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
17. Repo Hygiene Lessons From Prior Sessions
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
18. Future Scope Question Already Raised By User
The user asked whether the EA can be tested across “a whole bunch of pairs and anything Exness offers.”

Correct answer:

The validation framework is symbol-agnostic.
The strategy is intentionally scoped to USDJPY + XAUUSD because H015 showed that diversification into negative-edge instruments destroys the portfolio.
Each new symbol must become its own hypothesis:
H018
H019
etc.
Mechanical scaling is easy.
Edge validation per symbol is not.
Do not broaden the universe before H017 is live/stable on the two-asset core.
19. New AI First Reply Should Be
The next AI should reply with a short acknowledgement, not code.

It should say:

It understands the stack:

Windows
PowerShell
VS Code
Python 3.12.10 in .venv
It understands the current test anchor:

text
469 passed
It understands current phase status:

Phase 2.6 complete
Phase 3.1 through 3.4 complete
latest Phase 3 commit is b97723a
next likely step is Phase 3.5 real-data event smoke, but that needs M1 CSVs
It should ask the user to run hygiene verification:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git log --oneline -10
git status
pytest -q
It should ask whether these files exist:
text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
It should not write code until:
hygiene output is pasted
M1 availability is known
user says continue / ✅
20. Current User State At Handoff #13
The last completed user-verified sub-phase was Phase 3.4.

User pasted:

text
pytest tests\test_h017_event.py -q
10 passed

pytest -q
469 passed

git commit:
b97723a Phase 3.4: add H017 event-driven backtest bridge

git status:
nothing to commit, working tree clean
Tracked backtest files:

text
quantcore/backtest/__init__.py
quantcore/backtest/cost_model.py
quantcore/backtest/fill_engine.py
quantcore/backtest/h017_event.py
quantcore/backtest/portfolio.py
Tracked new tests:

text
tests/test_cost_model.py
tests/test_fill_engine.py
tests/test_h017_event.py
tests/test_portfolio.py
The user then asked for this handoff because the current AI token budget is nearing its end.

Continue from here.