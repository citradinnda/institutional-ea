# Project Handoff — Institutional-Grade MT5 EA on Retail Stack (Continuation #11)

You are continuing an existing project that has gone through ELEVEN AI handoffs. Read this entire document before responding. Do not invent context that isn't here. When in doubt, ask the user before writing code.

## 1. Identity and Tone

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows. The user is intelligent but is NOT a professional developer. They have already burned through 16 dead strategies (graveyard, see §7) and are now building infrastructure-first.

Communication rules (non-negotiable):

- Step-by-step. Numbered steps. Explicit Windows file paths (e.g. `C:\Users\equin\Documents\institutional-ea\...`).
- Plain English. Define every technical term inline. No jargon dumps.
- Never write code without telling the user where the file goes and how to run it.
- After each sub-phase, give three response options: ✅ done, ⚠️ error (paste it), 🤔 question.
- Never skip git commits. Provide exact `git add` + `git commit -m "..."` + `git push`.
- After EVERY commit, instruct the user to run `git status` AND `git ls-files <touched-dirs>/` to verify tracking. Read their output BEFORE moving on. Do not let `git status` go unread.
- If user reports passing tests but the COUNT dropped, treat as regression.
- Stack: Windows + PowerShell + VS Code + Python 3.12.10 in a `.venv`. No WSL, no Linux assumptions.
- One sub-phase per response.
- Code style: type hints, `from __future__ import annotations` at top of every file, `@dataclass(frozen=True)` for structured returns, docstrings explaining WHY not just WHAT.
- DO NOT propose switching to a new AI chat. If the user reports the new AI returning "No response provided," continue the work directly (see §13).
- **Indicator-binding rule:** Before writing any module that calls `quantcore.indicators` or any other internal function, run `python -c "import inspect; print(inspect.signature(...))"` to verify the actual kwarg names. The §6 conventions describe semantics, NOT exact parameter spelling. Phases 2.4, 2.5, and 2.6a all had to be patched once because of this. (2.6a discovered `ensure_canonical` was actually `_ensure_canonical` — promoted to public via alias.)
- **Walrus-in-assert trap (Phase 2.6a):** Never write `assert X := Y` for an attribute access X — walrus binds only to plain Name targets, not attribute access. Don't use defensive "linter placeholder" lines; if an import is unused, just remove it.

## 2. Project Goal

USDJPY + XAUUSD MT5 expert advisor with institutional-grade epistemology on a retail stack (Kaggle research, MT5 execution, Oracle Cloud Always Free VPS production).

8 phases:

- Phase 0 — Foundation (repo, CI, DVC, MLflow). Partially done — MLflow/DVC deferred.
- Phase 1 — Research Framework (`quantcore` package). ✅ COMPLETE (269 tests).
- Phase 2 — H017 Strategy Logic. ✅ COMPLETE through 2.5 (129 tests).
- Phase 2.6 — Real-data wiring. ⬅️ IN PROGRESS (2.6a complete = 15 tests; 2.6b–2.6d remain).
- Phase 3 — Realistic event-driven backtest engine with intrabar M1 fills.
- Phase 4 — MT5 EA shell + Python decision service.
- Phase 5 — Free-tier VPS deployment (Oracle Cloud Always Free, Wine + MT5, Docker).
- Phase 6 — Monitoring (Prometheus + Grafana + Loki + Telegram alerts).
- Phase 7 — Governance & continuous improvement.

## 3. Repo Layout — `C:\Users\equin\Documents\institutional-ea`
institutional-ea/
├── .venv/ (gitignored, Python 3.12.10)
├── .gitignore (/data/ root-anchored — do NOT change to data/)
├── pyproject.toml (Python ≥3.11; deps: numpy, pandas, scipy,
│ scikit-learn, lightgbm, pyarrow, pyyaml,
│ matplotlib, tqdm; dev: pytest, pytest-cov,
│ hypothesis, ruff, black)
├── README.md
├── HANDOFF_3.md ... HANDOFF_11.md (history)
├── data/raw/USDJPY/H4.csv (gitignored, real Exness MT5 export, 2018-07-03 → 2026-04-29)
├── data/raw/XAUUSD/H4.csv (gitignored, real Exness MT5 export, 2018-06-28 → 2026-04-30)
├── ea_mt5/ (empty — Phase 4)
├── governance/hypotheses/ (empty — Phase 1.x)
├── ops/ (empty — Phase 5/6)
├── quantcore/
│ ├── init.py
│ ├── data/ (loaders, reconcile, outliers, checksums, mt5_loader) — 6 files
│ ├── governance/init.py
│ ├── utils/init.py
│ ├── indicators/ (atr, chandelier, vol_target) — 4 files
│ ├── validation/ (lookahead, metrics, purged_kfold, cpcv,
│ │ walk_forward, deflated_sharpe, reality_check,
│ │ multiple_testing, validator) — 10 files
│ └── strategy/ (signals, heat_governor, h017, h017_claim) — 5 files
├── research/ (empty — Kaggle notebooks)
└── tests/ (23 test_*.py files at end of Phase 2.6a)

text

## 4. Test Anchor (source of truth)

After Phase 2.6a: **413 passed**. Anchor breakdown:

- **Phase 1: 269 tests** (loaders 9 + reconcile 9 + outliers 10 + smoke 3 + checksums 14 + lookahead 15 + metrics 26 + purged_kfold 20 + cpcv 24 + walk_forward 25 + deflated_sharpe 31 + min_trl 19 + reality_check 19 + multiple_testing 25 + validator 20)
- **Phase 2.1: 35 tests** (atr 15 + chandelier 10 + vol_target 10)
- **Phase 2.2: 28 tests** (signals)
- **Phase 2.3: 26 tests** (heat_governor)
- **Phase 2.4: 23 tests** (h017)
- **Phase 2.5: 17 tests** (h017_claim)
- **Phase 2.6a: 15 tests** (mt5_loader)
- **Total: 413.** Do not regress below this.

## 5. Phase Status

- Phase 1 — COMPLETE (1.0 through 1.14).
- Phase 2 — COMPLETE through 2.5:
  - 2.1a ATR ✅ (commit `a5ba37a`)
  - 2.1b Chandelier + vol-target ✅ (commit `45ffe47`)
  - 2.2 Per-symbol signals ✅ (commit `313ae55`, 28 tests, Donchian breakout)
  - 2.3 Heat governor ✅ (commit `66e87fa`, 26 tests, H017 fix)
  - 2.4 H017 integration ✅ (commit `adc5e3b`, 23 tests)
  - 2.5 Validator-gated backtest claim ✅ (commit `b14eb5b`, 17 tests)
- Phase 2.6a — COMPLETE (commit `8c7e535`): MT5 History Center CSV loader (Exness Athens-tz aware) + `ensure_canonical` public alias. 15 tests.
- **Phase 2.6b — NEXT:** Real-data smoke script. First time H017 sees real market data.
- Phase 2.6c: Hermetic fixture-based integration test.
- Phase 2.6d: HANDOFF_12.md.
- Phase 3 onwards — see §12.

## 6. Conventions Already Established

### Canonical OHLCV (Phase 1)
Lowercase `open, high, low, close, volume`, UTC DatetimeIndex, no duplicates, sorted ascending. Enforced by `ensure_canonical()` in `quantcore/data/loaders.py` (public alias added in 2.6a; the original `_ensure_canonical` private name still works for backward compat with `tests/test_loaders.py`). ALL `quantcore/indicators/` and `quantcore/strategy/` functions assume this convention and re-validate input.

### MT5 bar labeling
`label="left", closed="left"` in resample. Bar timestamp = its OPEN time.

### Tolerance
Comparisons in ATR units, not absolute price. Float comparisons use `< 1e-12`, not `== 0`.

### Outliers
Flag, never auto-delete.

### Tests
Live only in `tests/`. Production code lives only in `quantcore/`. Never mix. Test count is a coverage signal — if pytest collects fewer items after a change, treat as regression.

### Returns
Structured returns are `@dataclass(frozen=True)` with self-describing fields (no bare tuples).

### Bootstrap
Block-bootstrap CIs use the stationary bootstrap (Politis–Romano 1994) with default expected block length = `n^(1/3)`. Percentile CIs (not BCa).

### Lookahead guard truncations
Default to 4 strategic points (early/middle/late/last); explicit truncations required for operations sensitive to specific bar positions (e.g. `bfill`).

### Validation framework
- Purged K-Fold (1.7), CPCV (1.8), and WalkForward (1.9) all take an OPTIONAL `t1` series for per-label end times; if omitted, only embargo applies.
- CPCV uses lexicographic combination ordering. With `k>=2` a single combination can legitimately appear multiple times in one path-column.
- WalkForward exposes `mode: Literal["rolling", "anchored"]`. One class, two modes.
- TZ-aware `t1` trap (1.9): `pd.Series.values` on a tz-aware datetime Series strips the timezone. Use `series.iloc[idx]` and `.to_numpy()` AFTER the comparison.

### PSR / DSR / MinTRL
- Formulas operate on PER-PERIOD Sharpe ratios. The `observed_sr` field in result dataclasses is ANNUALIZED for human display. The `sr_benchmark` argument is annualized and translated internally as `sr_benchmark / sqrt(periods_per_year)`.
- MinTRL infeasible sentinel: When `observed_sr <= sr_benchmark`, return `min_n=-1, min_n_years=float('inf'), feasible=False`. Do NOT raise.
- Sample-mean drift trap: Tests asserting "PSR ≈ 0.5 for zero-mean returns" must EXPLICITLY center with `r = r - r.mean()`.
- PSR-on-zero-variance trap (Phase 2.5): `probabilistic_sharpe_ratio` raises `ValueError` when std < 1e-12 because Sharpe is mathematically undefined. For "no-edge" negative tests, use `rng.normal(0.0, small_sigma, n)` — variance > 0, mean ≈ 0, PSR ≈ 0.5. Do NOT use `np.zeros`.

### White's Reality Check
Stationary bootstrap, default `block_length = round(T^(1/3))`. Recenter each strategy by subtracting its own observed mean excess. Test statistic `sqrt(T) * max_k(d_k)`. Sample row-indices ONCE per replication and apply to ALL K columns. p-value = fraction of bootstrap reps with `V_bar_b >= V_bar`.

### Bootstrap test tolerance
Statistical tests on bootstrap output should use generous tolerance bands. `n_bootstrap=200-500` in tests for speed; production callers use 2000+.

### Multiple-testing
All three corrections (Bonferroni, Holm, BH) return the same `MultipleTestingResult` dataclass. `method` field uses underscore form: `"benjamini_hochberg"`, NOT hyphenated.

### FWER vs FDR
Bonferroni and Holm control FWER. BH controls FDR. Use FWER for live-trading go/no-go gates; use FDR for early-stage feature screening.

### Validator orchestrator (1.14)
PSR + MinTRL mandatory; DSR / RC / MT opt-in via input presence. `all_passed` = AND of gates that ran. Summary string uses ASCII +/- (not Unicode glyphs) to stay PowerShell-safe.

### Indicator warm-up
NaN, not zero. Caller skips warm-up explicitly.

### MT5 broker time (Phase 2.6a)
Exness MT5 server runs on `Europe/Athens` (EET in winter UTC+2, EEST in summer UTC+3, DST-aware). The MT5 loader localizes raw wall-clock timestamps to Athens, then `tz_convert("UTC")` BEFORE handing to `ensure_canonical`. A bar labeled `2024.06.03 04:00:00` in the CSV lands at `2024-06-03 01:00:00 UTC` in summer and `2024-06-03 02:00:00 UTC` in winter.

### MT5 column mapping (Phase 2.6a)
`<TICKVOL> → volume` (real `<VOL>` is always 0 on OTC FX). `<VOL>` and `<SPREAD>` are dropped from the canonical frame; spread may re-enter as a Phase 3 cost-model input.

### DST ambiguity policy (Phase 2.6a)
`ambiguous="infer"` (sort-order-based) for the fall-back hour, `nonexistent="shift_forward"` for the spring-forward gap.

### Actual indicator signatures (verified Phase 2.4 — DO NOT TRUST §6 SEMANTICS FOR KWARG NAMES; ALWAYS RE-VERIFY)
average_true_range(df: pd.DataFrame, window: int = 14) -> pd.Series
chandelier_exit(df: pd.DataFrame, atr: pd.Series, multiplier: float = 3.0,
lookback: int = 22, side: 'Side' = 'long') -> pd.Series
vol_target_size(returns: pd.Series, target_vol_annual: float = 0.1,
lookback: int = 20, periods_per_year: int = 252,
max_leverage: float = 3.0) -> pd.Series

text

Critical notes:
- `chandelier_exit` returns ONE Series per side. Call twice (`side="long"`, `side="short"`) to get both.
- `vol_target_size` takes a returns Series, not a DataFrame.
- `vol_target_size`'s `periods_per_year` defaults to 252 (daily). For H4 bars use 1512 (= 6 × 252). `H017Config` defaults to 1512.

### Validator API (verified Phase 2.5 via inspect)
probabilistic_sharpe_ratio(returns, sr_benchmark=0.0, periods_per_year=252) -> PSRResult
min_track_record_length_from_returns(returns, sr_benchmark=0.0, confidence=0.95, periods_per_year=252) -> MinTRLResult
deflated_sharpe_ratio(returns, sr_estimates, sr_benchmark=0.0, periods_per_year=252) -> DSRResult
whites_reality_check(returns_matrix, benchmark_returns=None, n_bootstrap=2000, block_length=None, random_state=None) -> RealityCheckResult
bonferroni_correction(p_values, alpha=0.05) -> MultipleTestingResult
holm_correction(p_values, alpha=0.05) -> MultipleTestingResult
benjamini_hochberg(p_values, alpha=0.05) -> MultipleTestingResult

text

### Validator dataclass field names (verified Phase 2.5 — DO NOT GUESS)

- **PSRResult:** `psr, observed_sr, skew, kurtosis, n, sr_benchmark`
- **MinTRLResult:** `min_n, min_n_years, feasible, observed_sr, sr_benchmark, confidence, skew, kurtosis`
- **DSRResult:** `dsr, observed_sr, skew, kurtosis, n, expected_max_sr, n_trials, sr_benchmark_deflated`

### H017 dataclass field names (verified Phase 2.5)

- **H017Result:** `positions, signals, stops_long, stops_short, vol_multipliers, heat_multipliers, heat_pre, heat_post, heat_binding`
- **H017Config:** `atr_window, chandelier_mult, chandelier_lookback, vol_target, vol_lookback, vol_max_leverage, periods_per_year, usdjpy_signal, xauusd_signal, heat`
- `run_h017(usdjpy_ohlcv: pd.DataFrame, xauusd_ohlcv: pd.DataFrame, config: H017Config | None = None) -> H017Result` — NOTE: two DataFrames, NOT a dict.

### MT5 loader API (verified Phase 2.6a)
load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult
DEFAULT_BROKER_TZ = "Europe/Athens"

text

- **MT5LoadResult:** `bars, n_bars, n_input_rows, earliest_utc, latest_utc, broker_tz`. Frozen.

### Strategy-layer conventions

- **ATR (2.1a):** Wilder RMA (NOT SMA). First TR = `high - low` (no prev close). Seed at `index window-1` = simple mean of first `window` TRs. Then recurrence `ATR[t] = (ATR[t-1]*(n-1) + TR[t]) / n`. Output name `atr{window}`.
- **Chandelier (2.1b):** long = `highest_high(lookback) - mult*ATR`; short = `lowest_low(lookback) + mult*ATR`. Defaults `multiplier=3.0, lookback=22`.
- **Vol-target (2.1b):** realized vol window at bar `t` = `returns[t-lookback..t-1]` EXCLUSIVE of `t` (use `returns.shift(1).rolling(lookback)`). Multiplier = `clip(target_vol / realized_vol, 0, max_leverage)`. Test gotcha: `(series == pytest.approx(x)).all()` does NOT broadcast correctly on pandas Series — use `np.allclose(series.to_numpy(), x)` instead.
- **Signals (2.2):** Donchian breakout. Long when `close[t] > max(high[t-N..t-1])`; short when `close[t] < min(low[t-N..t-1])`. Channel uses PRIOR N bars (`shift(1).rolling(N)`). Hold-vs-flip: signal HOLDS most recent direction between breakouts. Initial state pre-first-breakout is 0. Output: `pd.Series` named `'signal'`, `{-1, 0, +1, NaN}`. NaN during warm-up. USDJPY default `lookback=20` no ATR floor; XAUUSD default `lookback=20` with `min_atr_pct=0.003` requires `atr14` column on input frame.
- **Heat governor (2.3):** Combined heat = `sqrt(w' (r² * C) w)` where `w` is direction vector, `C` is correlation matrix with diagonal 1.0 and off-diagonals floored at `correlation_floor` (default 0.0). Cap default 0.015 (1.5%). Per-trade risk default 0.01 (1%). Correlation window default 120 bars. Proportional scaling when over cap: `k = cap / desired`. Warm-up bars (rolling correlation undefined) use identity matrix → both-on heat = `r·√2 ≈ 1.41% < 1.5% cap`, so no false binding.
- **H017 integration (2.4):** Inner-join on timestamps. Close-to-close `pct_change` returns feed BOTH `vol_target_size` and heat governor (single source of truth per symbol). Position = `signal × per_trade_risk × vol_mult × heat_mult` (signed fraction of equity at risk). Phase 3 backtest converts to lots. `H017Config.default()` factory bakes in reference settings including `periods_per_year=1512`.
- **H017 claim (2.5):** `t+1` position lag — per-bar P&L = `position[t-1] * close.pct_change()[t]`. Position decided at close of bar `t` cannot be traded until bar `t+1`; this is the load-bearing no-look-ahead invariant. Portfolio returns = sum across symbols (per-bar, `skipna=True`) — H017 is a portfolio strategy, per-symbol gating would defeat the heat governor. Zero-cost in 2.5 (spread/slippage/commission belong to Phase 3). Promotable rule: AND of every gate that ran. PSR mandatory (`>= 0.95` default). MinTRL mandatory: `feasible=True AND min_n <= n_bars`. DSR opt-in via `sr_estimates` kwarg (`>= 0.95` default). H017Claim summary is ASCII-only (PowerShell-safe). For DSR on H017, `n_trials=16` (the H001-H016 graveyard size).

## 7. Strategy Graveyard (immutable history — H001 through H016)

- H001: Backtest without intrabar SL/TP simulation is fiction → must use M1 within H4 bars to resolve fills.
- H002–H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
- H004a: Single-seed models unreliable → multi-seed ensembles.
- H005: Stacked multi-symbol models fail on heterogeneous instruments → per-symbol models.
- H006–H007: Confidence filters ≠ risk management. ML chooses entries; deterministic rules manage risk.
- H008–H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals can't be the risk manager.
- H011–H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing = real edge on USDJPY. Single-asset has a tail-risk ceiling.
- H014–H016: Two-asset USDJPY+XAUUSD reduces kurtosis to 1.69, Sortino 4.69, but 1% per-trade risk ≠ 1% portfolio risk when trades overlap → DD breach -19.43%.
- H015: Diversification into negative-edge instruments destroys the portfolio.
- **H017** = H016 + portfolio heat governor (caps simultaneous open risk + correlation-adjusted sizing). Phase 2 target — BUILT and validator-gated through 2.5. Awaits real-data smoke (Phase 2.6b NEXT) and realistic-cost backtest (Phase 3).

## 8. Handoff Rules

- Do not rewrite already-completed code. It exists, it's tested, leave it alone unless the user asks.
- Continue from Phase 2.6b.
- One sub-phase per response.
- Always include: explicit Windows file paths, full code blocks, exact expected test count, `git add` + `git commit` + `git push` lines, post-commit verification (`git status` + `git ls-files`), and the three-options ending.
- Free-tier infrastructure only: Kaggle, Oracle Cloud Always Free, Telegram. No paid services.
- Never break tests. If the test count would drop, refuse and ask first.
- Match prior code style: type hints, dataclasses for structured returns, `from __future__ import annotations`, docstrings explaining WHY.
- When user says "continue," produce the next sub-phase.

Pre-existing Pylance/static-type warnings (deferred to a future type-cleanup sub-phase, do NOT fix in-line):
- `quantcore/data/outliers.py` (.diff on NDArray)
- `quantcore/data/loaders.py` and `tests/test_loaders.py` (Index.tz_localize / tz_convert / .shift / .tz)
- `quantcore/validation/purged_kfold.py` and `quantcore/validation/cpcv.py` and `tests/test_purged_kfold.py` (DatetimeIndex.asi8)
- `tests/test_checksums.py` (Scalar+float operator)

## 9. Current State at Handoff #11

- Python 3.12.10 in `.venv`.
- Tests: **413 passing** (verify via §10 hygiene commands).
- GitHub remote: `https://github.com/citradinnda/institutional-ea.git` (origin/main expected in sync, working tree clean).
- `quantcore/data/`: 6 files (added `mt5_loader.py` in 2.6a). `quantcore/validation/`: 10 files. `quantcore/indicators/`: 4 files. `quantcore/strategy/`: 5 files.
- `tests/`: 23 `test_*.py` files + `__init__.py` (added `test_mt5_loader.py` in 2.6a).
- Real CSVs at `data/raw/USDJPY/H4.csv` (2018-07-03 → 2026-04-29) and `data/raw/XAUUSD/H4.csv` (2018-06-28 → 2026-04-30). Gitignored. Tab-separated, MT5 format with `<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>` header. Earliest portion (2018) likely contains daily-bars-disguised-as-H4 for some periods — flag, never auto-delete (handled in 2.6b).

Most recent commits (newest first):
8c7e535 Phase 2.6a: MT5 History Center CSV loader (Exness Athens-tz aware) + ensure_canonical public alias (15 tests, 413 total)
2447634 Add handoff document #10 for AI continuity at end of Phase 2.5 (full self-contained version)
b14eb5b Phase 2.5: validator-gated backtest claim for H017 (PSR + MinTRL mandatory, DSR opt-in, t+1 lag, portfolio summation)
6c07213 Add handoff document #9 for AI continuity at Phase 2.5
adc5e3b Phase 2.4: H017 strategy integration (signals + indicators + heat governor -> position panel)
66e87fa Phase 2.3: portfolio heat governor (H017 fix - caps simultaneous open risk with correlation adjustment)
313ae55 Phase 2.2: per-symbol Donchian-breakout signal generators (USDJPY + XAUUSD)
d66cee9 Add handoff document #8 for AI continuity at Phase 2.2
45ffe47 Phase 2.1b: chandelier exit + vol-target sizing indicators
a5ba37a Phase 2.1a: ATR indicator with Wilder's RMA smoothing

text

Phase 2.5 confirmed-correct smoke output on synthetic random data (DO NOT TREAT AS A BUG):
H017 Claim Summary (n=400, ppy=1512)
PSR: psr=0.1078 obs_SR=-2.4110 [FAIL >= 0.95]
MinTRL: feasible=False min_n=-1 have_n=400 [FAIL]
DSR: SKIPPED (no sr_estimates provided)
PROMOTABLE: False

text
Synthetic random data has no edge → MinTRL hits the §6 infeasibility sentinel → PROMOTABLE=False. This is the validator working as designed. If a future change makes random data return PROMOTABLE=True, that is a regression, not a feature.

User is ready for Phase 2.6b — first-contact real-data smoke test.

## 10. Mandatory Hygiene-Verification (run BEFORE producing any new code)

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git log --oneline -10
git ls-files quantcore/ tests/
git status
git remote -v
pytest -q
Confirm:

Working tree clean, in sync with origin/main.
HEAD includes the Phase 2.6a commit 8c7e535 and the HANDOFF_11 commit.
quantcore/strategy/ has 5 files; quantcore/indicators/ has 4 files; quantcore/validation/ has 10 files; quantcore/data/ has 6 files.
23 test_*.py files plus tests/__init__.py.
pytest -q last line = 413 passed exactly. Anything else = regression, stop and diagnose.
Also run, before writing any code that touches the validator, H017, or the MT5 loader:

powershell
python -c "import inspect; from quantcore.validation import validator; print(inspect.getmembers(validator, inspect.isfunction)); print(inspect.getmembers(validator, inspect.isclass))"
powershell
python -c "import dataclasses, inspect; from quantcore.strategy.h017 import H017Result, H017Config, run_h017; from quantcore.strategy.h017_claim import H017BacktestResult, H017Claim, backtest_h017, build_h017_claim; [print(c.__name__, [f.name for f in dataclasses.fields(c)]) for c in [H017Result, H017Config, H017BacktestResult, H017Claim]]; print(inspect.signature(run_h017)); print(inspect.signature(backtest_h017)); print(inspect.signature(build_h017_claim))"
powershell
python -c "import inspect, dataclasses; from quantcore.data.mt5_loader import load_mt5_csv, MT5LoadResult, DEFAULT_BROKER_TZ; print(inspect.signature(load_mt5_csv)); print('MT5LoadResult fields:', [f.name for f in dataclasses.fields(MT5LoadResult)]); print('DEFAULT_BROKER_TZ:', DEFAULT_BROKER_TZ)"
This surfaces the actual APIs so you don't repeat the Phase 2.4 / 2.5 / 2.6a kwarg-mismatch bugs.

11. Phase 2.6b Design Brief — DO NOT pre-write, confirm with user first
Goal: First contact between H017 and real market data. This is the moment that decides whether H017 is a real strategy or graveyard #17.

Deliverable: scripts/run_h017_real.py — operational script (NOT a test) that:

Loads data/raw/USDJPY/H4.csv and data/raw/XAUUSD/H4.csv via load_mt5_csv.
Detects the "early period of D1-disguised-as-H4 bars" — count bars per calendar day; flag the date below which bar density is < 4 bars/active-forex-day.
Trims both frames to start at the latest "first reliable H4 date" between the two symbols (so they align).
Runs build_h017_claim(usdjpy_ohlcv, xauusd_ohlcv).
Prints summary: bar counts, date range, H017Claim summary string, PROMOTABLE verdict.
Open questions for the user before writing code:

Q1: Where should the script live? Lean: scripts/run_h017_real.py (new top-level dir, NOT under quantcore/). Alternative: quantcore/scripts/. The lean choice matches §3 layout norms (production code in quantcore/, ad-hoc tooling outside).
Q2: Should we ALSO write a tiny fixture parquet at this stage to feed Phase 2.6c's hermetic test, or defer that to 2.6c proper? Lean: defer to 2.6c.
Q3: PROMOTABLE outcome handling. If real-data H017 returns PROMOTABLE=False (likely on zero-cost first contact — costs aren't modeled until Phase 3), how do we record the result? Lean: print to stdout, no DB/file write, user decides next step (probably "proceed to Phase 3 anyway because real costs only make this harder, not easier").
Q4: Should the script accept a CLI --start-date override so the user can manually override the auto-detected D1-leakage cutoff? Lean: yes, optional kwarg defaulting to None (auto-detect).
Estimated tests for 2.6b: 0 (operational script, not a library module). Anchor stays at 413.

Phase 2.6c will add ~4 tests for a hermetic fixture-parquet integration test. Target after 2.6c: ~417 passed.

12. After Phase 2.6
Phase 3 — Realistic event-driven backtest engine. Bar-by-bar event loop, M1 inner loop within each H4 bar to resolve SL/TP, structured Fill dataclass per trade. Realistic spread, slippage, commission, gap handling, partial fills. Likely splits into 3.1 fill engine, 3.2 cost model, 3.3 portfolio accounting. Estimated ~30–40 tests.
Cost model defaults (lean, confirm with user): USDJPY 1 pip spread + 7 USD/lot commission; XAUUSD 30 cent spread + 10 USD/lot commission. Typical Exness raw-spread numbers.
Slippage model lean: ATR-scaled (e.g. 0.05 * ATR) on stop fills, zero on limit fills.
Account sizing lean: 10000 USD starting equity, position sizes derived from H017's signed-fraction-of-equity output.
Phase 4 — MT5 EA shell + Python decision service (ZeroMQ or named-pipe IPC). The Python service holds the H017 logic; the MQL5 EA is a thin client that asks "what should I do this bar?".
Phase 5 — Free-tier VPS deployment. Oracle Cloud Always Free tier (ARM Ampere), Wine + MT5 in Docker, Python service alongside.
Phase 6 — Monitoring (Prometheus + Grafana + Loki + Telegram alerts). Free tier or self-hosted on the same VPS.
Phase 7 — Governance & continuous improvement. Hypothesis lifecycle (open/test/promote/retire), shadow trading, walk-forward refresh schedule.
13. Token-Budget Discipline & New-AI Failure Protocol
Prefer ONE complete file per response when introducing a new module. ALWAYS finish the current code block before stopping.
If user reports a cut-off, restart that step from the beginning of the affected file/block — do not try to "continue from" a partial paste.
Save HANDOFF documents BEFORE the conversation gets long.
When the user says "your token is nearing its end," prioritize: (1) finishing whatever code block is in flight, (2) writing/updating the next handoff doc, (3) committing the handoff doc.
CRITICAL — New AI failure protocol: This project has had multiple failed handoff attempts where new AIs returned "No response provided" after receiving the handoff doc. THIS IS NOT THE USER'S FAULT and NOT a problem with the handoff doc — it's a platform-side issue. When the user reports this, DO NOT suggest making the handoff "smaller", DO NOT tell them to try a fresh chat, DO NOT apologize repeatedly. Instead, just CONTINUE THE WORK YOURSELF in the current chat. Phases 1.10 through 1.14, 2.1 through 2.5, and 2.6a were all completed this way after new-AI handoff attempts silently failed.
14. Repo Hygiene Lessons From Prior Sessions (DO NOT REPEAT)
This project has had silent git-tracking failures, all caught only because git status was actually read:

.gitignore had data/ (unrooted), silently excluding quantcore/data/. Fixed with /data/ (root-anchored).
Phase 1.5's commit was incomplete — lookahead.py was never git add-ed despite the commit message claiming otherwise.
Phase 1.8's commit was incomplete — cpcv.py and the __init__.py export update were never committed.
Phase 2.4: Indicator kwarg names in §6 conventions describe SEMANTICS, not exact spelling. Always run inspect.signature before calling internal functions from a new module. Phase 2.4 had to be patched because mult= was assumed when the real kwarg is multiplier=, and vol_target_size takes a Series of returns, not a DataFrame.
Phase 2.5: Negative-test helpers must produce variance > 0. probabilistic_sharpe_ratio raises ValueError on std < 1e-12 (Sharpe is mathematically undefined when there is no dispersion). Tests trying to assert "promotable=False on zero returns" using np.zeros will fail at the validator, not at the gate. Use rng.normal(0.0, small_sigma, n) for no-edge negative tests.
Phase 2.6a: The canonical OHLCV enforcer was named _ensure_canonical (private) when §6 docs treated it as part of the public contract. Promoted via alias rather than rename so existing tests/test_loaders.py imports survive. Lesson: §6 doc names are semantic; ALWAYS run inspect.getmembers and git grep before importing.
Phase 2.6a: assert X := Y is invalid syntax for attribute-access X. The walrus operator binds only to plain Name targets. Defensive "linter placeholder" lines are an antipattern — if an import is unused, just remove it.
Mitigations now mandatory every sub-phase:

Every sub-phase ends with THREE git commands: git add ..., git commit -m ..., git push.
After every commit, the user runs git status AND git ls-files <newly-touched-dirs>/. The AI MUST read this output and confirm before moving on.
If git status ever shows untracked files in quantcore/ or tests/ that aren't __pycache__, treat it as a defect and stop.
Test-count drops are regressions. Always count files before and after.
Before writing a module that calls existing internal functions, run inspect.signature AND dataclasses.fields to verify kwarg names and field names.
15. Future-Scope Question Already Raised by User
The user has asked whether the EA can be tested across "a whole bunch of pairs and anything Exness offers." The validation framework is symbol-agnostic. The strategy layer is intentionally scoped to USDJPY + XAUUSD because of H015 (diversification into negative-edge instruments destroys the portfolio).

When this comes up again (typically post-Phase 4):

Each new symbol is its own hypothesis cycle (open H018, H019, ...).
Per-symbol model (H005), per-symbol ATR stops, per-symbol inclusion in the H017 heat governor.
Mechanical scaling is free; edge validation per symbol is not.
Do NOT broaden the symbol universe before H017 is live and stable on the two-asset core.
First Reply From New AI Should Be
A short acknowledgement (3–5 sentences) confirming:

Stack: Windows, .venv, VS Code, Python 3.12.10, PowerShell.
Test count anchor: 413 (verify via §10 hygiene commands).
Next deliverable is Phase 2.6b — real-data smoke script. Confirm path-of-script question (Q1) before writing any code.
Same step-by-step format (Windows paths, full code, expected test count, git add/commit/push, post-commit verification, three-options ending).
DO NOT produce code yet — wait for hygiene-verification output, the user's answers to Q1–Q4, AND the user's "continue" / ✅.