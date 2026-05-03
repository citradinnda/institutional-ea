# Project Handoff — Institutional-Grade MT5 EA on Retail Stack (Continuation #12)

You are continuing an existing project that has gone through TWELVE AI handoffs. Read this entire document before responding. Do not invent context that isn't here. When in doubt, ask the user before writing code.

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
- **Indicator-binding rule:** Before writing any module that calls `quantcore.indicators` or any other internal function, run `python -c "import inspect; print(inspect.signature(...))"` to verify the actual kwarg names. The §6 conventions describe semantics, NOT exact parameter spelling. Phases 2.4, 2.5, 2.6a, and 2.6b all had to be patched once because of this. (2.6a discovered `ensure_canonical` was actually `_ensure_canonical` — promoted to public via alias. 2.6b had a wrong import path for `H017BacktestResult`.)
- **Walrus-in-assert trap (Phase 2.6a):** Never write `assert X := Y` for an attribute access X — walrus binds only to plain Name targets, not attribute access. Don't use defensive "linter placeholder" lines; if an import is unused, just remove it.
- **Restart-on-cutoff (Phase 2.6c):** If a code block is cut off mid-paste during a response, RESTART the affected file from the top in the next response. Do not try to merge with a partial paste. Per §13.
- **Consolidated-import rule (Phase 2.6b lesson):** Prefer ONE consolidated multi-line import block per source module per consuming file. Splitting `from X import a` and `from X import b` across separate lines invites typos and is how the Phase 2.6b `H017BacktestResult` import bug got introduced even though §10 inspect output was right there.
- **Handoff-request rule (NEW in HANDOFF_12):** When the user asks for a handoff doc (whether mid-conversation or at token end), produce a COMPLETE, FULLY SELF-CONTAINED version. Never abbreviate sections with "[Same as HANDOFF_N §X]" or "[Identical to prior]" — reproduce every section in full. The whole point of the handoff is that the next AI may have NO access to prior handoffs. Inline everything: §6 conventions, §7 graveyard, §8 rules, §14 lessons. Cost: longer doc. Benefit: a new AI receiving only HANDOFF_N.md has 100% of the project's institutional memory in one file. Always optimize for that.

## 2. Project Goal

USDJPY + XAUUSD MT5 expert advisor with institutional-grade epistemology on a retail stack (Kaggle research, MT5 execution, Oracle Cloud Always Free VPS production).

8 phases:

- Phase 0 — Foundation (repo, CI, DVC, MLflow). Partially done — MLflow/DVC deferred.
- Phase 1 — Research Framework (`quantcore` package). ✅ COMPLETE (269 tests).
- Phase 2 — H017 Strategy Logic. ✅ COMPLETE through 2.5 (129 tests).
- Phase 2.6 — Real-data wiring. ✅ COMPLETE (2.6a + 2.6b + 2.6c-i + 2.6c-ii all landed; this handoff doc is 2.6d).
- Phase 3 — Realistic event-driven backtest engine with intrabar M1 fills. ⬅️ NEXT.
- Phase 4 — MT5 EA shell + Python decision service.
- Phase 5 — Free-tier VPS deployment (Oracle Cloud Always Free, Wine + MT5, Docker).
- Phase 6 — Monitoring (Prometheus + Grafana + Loki + Telegram alerts).
- Phase 7 — Governance & continuous improvement.

## 3. Repo Layout — `C:\Users\equin\Documents\institutional-ea`

```
institutional-ea/
├── .venv/                                  (gitignored, Python 3.12.10)
├── .gitignore                              (/data/ root-anchored — do NOT change to data/)
├── pyproject.toml                          (Python ≥3.11; deps: numpy, pandas, scipy,
│                                            scikit-learn, lightgbm, pyarrow, pyyaml,
│                                            matplotlib, tqdm; dev: pytest, pytest-cov,
│                                            hypothesis, ruff, black)
├── README.md
├── HANDOFF_3.md ... HANDOFF_12.md           (history)
├── data/raw/USDJPY/H4.csv                   (gitignored, real Exness MT5 export, 2018-07-03 → 2026-04-29)
├── data/raw/XAUUSD/H4.csv                   (gitignored, real Exness MT5 export, 2018-06-28 → 2026-04-30)
├── ea_mt5/                                  (empty — Phase 4)
├── governance/hypotheses/                   (empty — Phase 1.x)
├── ops/                                     (empty — Phase 5/6)
├── quantcore/
│   ├── __init__.py
│   ├── data/                                (loaders, reconcile, outliers, checksums, mt5_loader, leakage) — 7 files
│   ├── governance/__init__.py
│   ├── utils/__init__.py
│   ├── indicators/                          (atr, chandelier, vol_target) — 4 files
│   ├── validation/                          (lookahead, metrics, purged_kfold, cpcv,
│   │                                         walk_forward, deflated_sharpe, reality_check,
│   │                                         multiple_testing, validator) — 10 files
│   └── strategy/                            (signals, heat_governor, h017, h017_claim) — 5 files
├── research/                                (empty — Kaggle notebooks)
├── scripts/run_h017_real.py                 (Phase 2.6b operational smoke script)
└── tests/                                   (25 test_*.py files at end of Phase 2.6c-ii)
```

## 4. Test Anchor (source of truth)

After Phase 2.6c-ii: **423 passed**. Anchor breakdown:

- **Phase 1: 269 tests** (loaders 9 + reconcile 9 + outliers 10 + smoke 3 + checksums 14 + lookahead 15 + metrics 26 + purged_kfold 20 + cpcv 24 + walk_forward 25 + deflated_sharpe 31 + min_trl 19 + reality_check 19 + multiple_testing 25 + validator 20)
- **Phase 2.1: 35 tests** (atr 15 + chandelier 10 + vol_target 10)
- **Phase 2.2: 28 tests** (signals)
- **Phase 2.3: 26 tests** (heat_governor)
- **Phase 2.4: 23 tests** (h017)
- **Phase 2.5: 17 tests** (h017_claim)
- **Phase 2.6a: 15 tests** (mt5_loader)
- **Phase 2.6c-i: 7 tests** (leakage)
- **Phase 2.6c-ii: 3 tests** (integration_h017_pipeline)
- **Total: 423.** Do not regress below this.

## 5. Phase Status

- Phase 1 — COMPLETE (1.0 through 1.14).
- Phase 2 — COMPLETE through 2.5:
  - 2.1a ATR ✅ (commit `a5ba37a`)
  - 2.1b Chandelier + vol-target ✅ (commit `45ffe47`)
  - 2.2 Per-symbol signals ✅ (commit `313ae55`, 28 tests, Donchian breakout)
  - 2.3 Heat governor ✅ (commit `66e87fa`, 26 tests, H017 fix)
  - 2.4 H017 integration ✅ (commit `adc5e3b`, 23 tests)
  - 2.5 Validator-gated backtest claim ✅ (commit `b14eb5b`, 17 tests)
- Phase 2.6 — COMPLETE:
  - 2.6a MT5 History Center CSV loader ✅ (commit `8c7e535`, 15 tests, Exness Athens-tz aware, `ensure_canonical` public alias)
  - 2.6b Real-data smoke script ✅ (commit `aa4eed8`, 0 tests — operational, `scripts/run_h017_real.py`)
  - 2.6c-i Leakage helpers promoted to library ✅ (commit `fb116ff`, 7 tests, `quantcore/data/leakage.py`)
  - 2.6c-ii Hermetic integration test ✅ (commit `e0923cf`, 3 tests, `tests/test_integration_h017_pipeline.py`)
  - 2.6d HANDOFF_12.md (this document)
- **Phase 3 — NEXT:** Realistic event-driven backtest engine. See §11 for design brief.

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
Live only in `tests/`. Production code lives only in `quantcore/`. Operational scripts live in `scripts/`. Never mix. Test count is a coverage signal — if pytest collects fewer items after a change, treat as regression.

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

### Leakage detection (Phase 2.6c-i)
- `quantcore/data/leakage.py` exposes `detect_d1_leakage`, `trim_to_common_start`, `LeakageScan`, `MIN_H4_BARS_PER_ACTIVE_DAY=4`.
- All four names re-exported from `quantcore.data.__init__`.
- `detect_d1_leakage` finds the FIRST date with >= threshold bars. Naive walk-backward from "last suspect date" is WRONG because forex weekends are sporadically suspect throughout history (~half of all calendar dates). The correct shape of D1-disguised-as-H4 leakage is a CONTIGUOUS run of low-count dates at the START of the series.
- `trim_to_common_start` rejects tz-naive timestamps loudly (silent misalignment is one of the repo's recurring footguns).
- Default broker_tz grouping is "Europe/Athens".

### Actual indicator signatures (verified Phase 2.4 — DO NOT TRUST §6 SEMANTICS FOR KWARG NAMES; ALWAYS RE-VERIFY)
```
average_true_range(df: pd.DataFrame, window: int = 14) -> pd.Series
chandelier_exit(df: pd.DataFrame, atr: pd.Series, multiplier: float = 3.0,
                lookback: int = 22, side: 'Side' = 'long') -> pd.Series
vol_target_size(returns: pd.Series, target_vol_annual: float = 0.1,
                lookback: int = 20, periods_per_year: int = 252,
                max_leverage: float = 3.0) -> pd.Series
```

Critical notes:
- `chandelier_exit` returns ONE Series per side. Call twice (`side="long"`, `side="short"`) to get both.
- `vol_target_size` takes a returns Series, not a DataFrame.
- `vol_target_size`'s `periods_per_year` defaults to 252 (daily). For H4 bars use 1512 (= 6 × 252). `H017Config` defaults to 1512.

### Validator API (verified Phase 2.5 via inspect)
```
probabilistic_sharpe_ratio(returns, sr_benchmark=0.0, periods_per_year=252) -> PSRResult
min_track_record_length_from_returns(returns, sr_benchmark=0.0, confidence=0.95, periods_per_year=252) -> MinTRLResult
deflated_sharpe_ratio(returns, sr_estimates, sr_benchmark=0.0, periods_per_year=252) -> DSRResult
whites_reality_check(returns_matrix, benchmark_returns=None, n_bootstrap=2000, block_length=None, random_state=None) -> RealityCheckResult
bonferroni_correction(p_values, alpha=0.05) -> MultipleTestingResult
holm_correction(p_values, alpha=0.05) -> MultipleTestingResult
benjamini_hochberg(p_values, alpha=0.05) -> MultipleTestingResult
```

### Validator dataclass field names (verified Phase 2.5 — DO NOT GUESS)
- **PSRResult:** `psr, observed_sr, skew, kurtosis, n, sr_benchmark`
- **MinTRLResult:** `min_n, min_n_years, feasible, observed_sr, sr_benchmark, confidence, skew, kurtosis`
- **DSRResult:** `dsr, observed_sr, skew, kurtosis, n, expected_max_sr, n_trials, sr_benchmark_deflated`

### H017 dataclass field names (verified Phase 2.5)
- **H017Result:** `positions, signals, stops_long, stops_short, vol_multipliers, heat_multipliers, heat_pre, heat_post, heat_binding`
- **H017Config:** `atr_window, chandelier_mult, chandelier_lookback, vol_target, vol_lookback, vol_max_leverage, periods_per_year, usdjpy_signal, xauusd_signal, heat`
- `run_h017(usdjpy_ohlcv: pd.DataFrame, xauusd_ohlcv: pd.DataFrame, config: H017Config | None = None) -> H017Result` — NOTE: two DataFrames, NOT a dict.

### H017 claim API (verified Phase 2.5)
- `backtest_h017(usdjpy_ohlcv, xauusd_ohlcv, config=None) -> H017BacktestResult` — **lives in `quantcore.strategy.h017_claim`, NOT `quantcore.strategy.h017`**. Phase 2.6b had a typo here that cost a re-run.
- `build_h017_claim(returns: pd.Series, *, periods_per_year=1512, sr_benchmark=0.0, confidence=0.95, psr_threshold=0.95, sr_estimates=None, dsr_threshold=0.95) -> H017Claim` — takes a returns SERIES, not OHLCV frames. Pipeline: `bt = backtest_h017(...)` → `claim = build_h017_claim(bt.portfolio_returns)`.
- **H017BacktestResult:** `portfolio_returns, per_symbol_returns, positions, n_bars`
- **H017Claim:** `psr, min_trl, dsr, n_trials, periods_per_year, n_bars, promotable, summary`

### MT5 loader API (verified Phase 2.6a)
```
load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult
DEFAULT_BROKER_TZ = "Europe/Athens"
```
- **MT5LoadResult:** `bars, n_bars, n_input_rows, earliest_utc, latest_utc, broker_tz`. Frozen.

### Leakage API (verified Phase 2.6c-i)
```
detect_d1_leakage(bars, broker_tz, min_bars_per_day=4) -> LeakageScan
trim_to_common_start(usdjpy, xauusd, start_date_utc) -> tuple[DataFrame, DataFrame]
MIN_H4_BARS_PER_ACTIVE_DAY = 4
```
- **LeakageScan:** `first_reliable_date, leaked_dates, weekend_dates, total_dates, broker_tz`. Frozen.
- `trim_to_common_start` raises `ValueError` if `start_date_utc.tz is None`.

### Strategy-layer conventions

- **ATR (2.1a):** Wilder RMA (NOT SMA). First TR = `high - low` (no prev close). Seed at `index window-1` = simple mean of first `window` TRs. Then recurrence `ATR[t] = (ATR[t-1]*(n-1) + TR[t]) / n`. Output name `atr{window}`.
- **Chandelier (2.1b):** long = `highest_high(lookback) - mult*ATR`; short = `lowest_low(lookback) + mult*ATR`. Defaults `multiplier=3.0, lookback=22`.
- **Vol-target (2.1b):** realized vol window at bar `t` = `returns[t-lookback..t-1]` EXCLUSIVE of `t` (use `returns.shift(1).rolling(lookback)`). Multiplier = `clip(target_vol / realized_vol, 0, max_leverage)`. Test gotcha: `(series == pytest.approx(x)).all()` does NOT broadcast correctly on pandas Series — use `np.allclose(series.to_numpy(), x)` instead.
- **Signals (2.2):** Donchian breakout. Long when `close[t] > max(high[t-N..t-1])`; short when `close[t] < min(low[t-N..t-1])`. Channel uses PRIOR N bars (`shift(1).rolling(N)`). Hold-vs-flip: signal HOLDS most recent direction between breakouts. Initial state pre-first-breakout is 0. Output: `pd.Series` named `'signal'`, `{-1, 0, +1, NaN}`. NaN during warm-up. USDJPY default `lookback=20` no ATR floor; XAUUSD default `lookback=20` with `min_atr_pct=0.003` requires `atr14` column on input frame.
- **Heat governor (2.3):** Combined heat = `sqrt(w' (r² * C) w)` where `w` is direction vector, `C` is correlation matrix with diagonal 1.0 and off-diagonals floored at `correlation_floor` (default 0.0). Cap default 0.015 (1.5%). Per-trade risk default 0.01 (1%). Correlation window default 120 bars. Proportional scaling when over cap: `k = cap / desired`. Warm-up bars (rolling correlation undefined) use identity matrix → both-on heat = `r·√2 ≈ 1.41% < 1.5% cap`, so no false binding.
- **H017 integration (2.4):** Inner-join on timestamps. Close-to-close `pct_change` returns feed BOTH `vol_target_size` and heat governor (single source of truth per symbol). Position = `signal × per_trade_risk × vol_mult × heat_mult` (signed fraction of equity at risk). Phase 3 backtest converts to lots. `H017Config.default()` factory bakes in reference settings including `periods_per_year=1512`.
- **H017 claim (2.5):** `t+1` position lag — per-bar P&L = `position[t-1] * close.pct_change()[t]`. Position decided at close of bar `t` cannot be traded until bar `t+1`; this is the load-bearing no-look-ahead invariant. Portfolio returns = sum across symbols (per-bar, `skipna=True`) — H017 is a portfolio strategy, per-symbol gating would defeat the heat governor. Zero-cost in 2.5 (spread/slippage/commission belong to Phase 3). Promotable rule: AND of every gate that ran. PSR mandatory (`>= 0.95` default). MinTRL mandatory: `feasible=True AND min_n <= n_bars`. DSR opt-in via `sr_estimates` kwarg (`>= 0.95` default). H017Claim summary is ASCII-only (PowerShell-safe). For DSR on H017, `n_trials=16` (the H001-H016 graveyard size).

### Phase 2.6b real-data finding (LOAD-BEARING — actual ground truth from real Exness data)
- Exness MT5 H4 export delivered DAILY bars labelled as H4 from 2018-07 through 2021-07-01, then switched to genuine H4 on 2021-07-02. SYMMETRIC across both symbols (broker-side export-format change, not a per-symbol artifact).
- After auto-trim: **7719 H4 bars from 2021-07-02 onward** (~5.1 years of clean data).
- H017 zero-cost result on real data:
  - `obs_SR = +0.4920` (annualized, ppy=1512). Positive raw edge, mid-tier for systematic FX.
  - `PSR = 0.8634` (vs 0.95 threshold → FAIL). 86% probability true Sharpe > 0; not enough for 95%-confidence claim.
  - `MinTRL: feasible=True, min_n=17392, have_n=7719`. Need ~11.5 years; have 5.1. Sample-size problem, not edge problem.
  - `non-zero return bars: 7688 / 7719` (99.6%, no suspicious flat regions).
  - **VERDICT: NOT PROMOTABLE.**
- Interpretation: H017 has a qualified positive edge but neither sufficient data length NOR sufficient raw Sharpe to clear PSR 0.95 at this Sharpe level. Phase 3 costs (spread + slippage + commission) will pull Sharpe down further, possibly to +0.15 to +0.30. **This is calibration, not a death sentence.** H017 is alive; Phase 3 is the next test.
- This finding is reproducible: `python scripts\run_h017_real.py` from the repo root replays it deterministically.

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
- **H017** = H016 + portfolio heat governor (caps simultaneous open risk + correlation-adjusted sizing). **ALIVE.** Validator-gated through 2.5. Real-data smoke (2.6b) returned NOT PROMOTABLE at zero cost — qualified edge, insufficient data length AND raw Sharpe to clear PSR 0.95. Awaits Phase 3 realistic-cost backtest.

## 8. Handoff Rules

- Do not rewrite already-completed code. It exists, it's tested, leave it alone unless the user asks.
- Continue from Phase 3 (Phase 2.6 is complete).
- One sub-phase per response.
- Always include: explicit Windows file paths, full code blocks, exact expected test count, `git add` + `git commit` + `git push` lines, post-commit verification (`git status` + `git ls-files`), and the three-options ending.
- Free-tier infrastructure only: Kaggle, Oracle Cloud Always Free, Telegram. No paid services.
- Never break tests. If the test count would drop, refuse and ask first.
- Match prior code style: type hints, dataclasses for structured returns, `from __future__ import annotations`, docstrings explaining WHY.
- When user says "continue," produce the next sub-phase.
- **When user asks for a handoff doc, produce a COMPLETE, FULLY SELF-CONTAINED version (see §1 handoff-request rule).** Do not abbreviate by referencing prior handoffs.

Pre-existing Pylance/static-type warnings (deferred to a future type-cleanup sub-phase, do NOT fix in-line):
- `quantcore/data/outliers.py` (.diff on NDArray)
- `quantcore/data/loaders.py` and `tests/test_loaders.py` (Index.tz_localize / tz_convert / .shift / .tz)
- `quantcore/validation/purged_kfold.py` and `quantcore/validation/cpcv.py` and `tests/test_purged_kfold.py` (DatetimeIndex.asi8)
- `tests/test_checksums.py` (Scalar+float operator)

## 9. Current State at Handoff #12

- Python 3.12.10 in `.venv`.
- Tests: **423 passing** (verify via §10 hygiene commands).
- GitHub remote: `https://github.com/citradinnda/institutional-ea.git` (origin/main expected in sync, working tree clean).
- `quantcore/data/`: 7 files (`__init__.py`, `checksums.py`, `leakage.py`, `loaders.py`, `mt5_loader.py`, `outliers.py`, `reconcile.py`).
- `quantcore/validation/`: 10 files.
- `quantcore/indicators/`: 4 files.
- `quantcore/strategy/`: 5 files.
- `tests/`: 25 `test_*.py` files + `__init__.py` (added `test_leakage.py` in 2.6c-i, `test_integration_h017_pipeline.py` in 2.6c-ii).
- `scripts/run_h017_real.py` exists (Phase 2.6b operational smoke script).
- Real CSVs at `data/raw/USDJPY/H4.csv` (2018-07-03 → 2026-04-29) and `data/raw/XAUUSD/H4.csv` (2018-06-28 → 2026-04-30). Gitignored. Tab-separated, MT5 format with `<DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>` header. **Confirmed:** the 2018-07 → 2021-07-01 portion is daily-bars-disguised-as-H4 across BOTH symbols. Auto-trimmed by `detect_d1_leakage` to a 5.1-year clean region.

Most recent commits (newest first):

```
e0923cf Phase 2.6c-ii: hermetic integration test for H017 real-data pipeline (3 tests, 423 total)
fb116ff Phase 2.6c-i: promote leakage helpers to quantcore.data.leakage (7 tests, 420 total)
aa4eed8 Phase 2.6b: real-data smoke script for H017 (Exness USDJPY+XAUUSD H4, D1-leakage auto-detect)
8288d93 Add handoff document #11 for AI continuity at end of Phase 2.6a (full self-contained version)
8c7e535 Phase 2.6a: MT5 History Center CSV loader (Exness Athens-tz aware) + ensure_canonical public alias (15 tests, 413 total)
2447634 Add handoff document #10 for AI continuity at end of Phase 2.5 (full self-contained version)
b14eb5b Phase 2.5: validator-gated backtest claim for H017 (PSR + MinTRL mandatory, DSR opt-in, t+1 lag, portfolio summation)
6c07213 Add handoff document #9 for AI continuity at Phase 2.5
adc5e3b Phase 2.4: H017 strategy integration (signals + indicators + heat governor -> position panel)
66e87fa Phase 2.3: portfolio heat governor (H017 fix - caps simultaneous open risk with correlation adjustment)
```

Phase 2.6b real-data smoke output (DO NOT TREAT AS A BUG; this is the load-bearing finding):

```
H017 Claim Summary (n=7719, ppy=1512)
  PSR:    psr=0.8634  obs_SR=+0.4920  [FAIL >= 0.95]
  MinTRL: feasible=True  min_n=17392  have_n=7719  [FAIL]
  DSR:    SKIPPED (no sr_estimates provided)
  PROMOTABLE: False
VERDICT: NOT PROMOTABLE
```

User is ready for Phase 3 — realistic event-driven backtest engine.

## 10. Mandatory Hygiene-Verification (run BEFORE producing any new code)

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git log --oneline -10
git ls-files quantcore/ tests/ scripts/
git status
git remote -v
pytest -q
```

Confirm:

- Working tree clean, in sync with origin/main.
- HEAD includes the Phase 2.6c-ii commit `e0923cf` and the HANDOFF_12 commit.
- `quantcore/strategy/` has 5 files; `quantcore/indicators/` has 4 files; `quantcore/validation/` has 10 files; `quantcore/data/` has 7 files.
- 25 `test_*.py` files plus `tests/__init__.py`.
- `scripts/run_h017_real.py` exists.
- `pytest -q` last line = `423 passed` exactly. Anything else = regression, stop and diagnose.

Also run, before writing any code that touches the validator, H017, the MT5 loader, or leakage:

```powershell
python -c "import inspect; from quantcore.validation import validator; print(inspect.getmembers(validator, inspect.isfunction)); print(inspect.getmembers(validator, inspect.isclass))"
```

```powershell
python -c "import dataclasses, inspect; from quantcore.strategy.h017 import H017Result, H017Config, run_h017; from quantcore.strategy.h017_claim import H017BacktestResult, H017Claim, backtest_h017, build_h017_claim; [print(c.__name__, [f.name for f in dataclasses.fields(c)]) for c in [H017Result, H017Config, H017BacktestResult, H017Claim]]; print(inspect.signature(run_h017)); print(inspect.signature(backtest_h017)); print(inspect.signature(build_h017_claim))"
```

```powershell
python -c "import inspect, dataclasses; from quantcore.data.mt5_loader import load_mt5_csv, MT5LoadResult, DEFAULT_BROKER_TZ; print(inspect.signature(load_mt5_csv)); print('MT5LoadResult fields:', [f.name for f in dataclasses.fields(MT5LoadResult)]); print('DEFAULT_BROKER_TZ:', DEFAULT_BROKER_TZ)"
```

```powershell
python -c "import inspect, dataclasses; from quantcore.data.leakage import detect_d1_leakage, trim_to_common_start, LeakageScan, MIN_H4_BARS_PER_ACTIVE_DAY; print(inspect.signature(detect_d1_leakage)); print(inspect.signature(trim_to_common_start)); print('LeakageScan fields:', [f.name for f in dataclasses.fields(LeakageScan)]); print('MIN:', MIN_H4_BARS_PER_ACTIVE_DAY)"
```

This surfaces the actual APIs so you don't repeat the Phase 2.4 / 2.5 / 2.6a / 2.6b kwarg-mismatch bugs.

## 11. Phase 3 Design Brief — DO NOT pre-write, confirm with user first

**Goal:** Replace the zero-cost `backtest_h017` in `quantcore/strategy/h017_claim.py` with a bar-by-bar event-driven engine that produces realistic fills, costs, and equity curves. Phase 2.6b proved H017 has a qualified positive edge at zero cost; Phase 3 measures whether that edge survives realistic execution.

### Sub-phase split (lean)

- **3.1 — Fill engine.** New module `quantcore/backtest/fill_engine.py`. Iterates H4 bars sequentially. For each bar with an active position, drops to M1 within that H4 bar to resolve SL/TP fills realistically. Produces structured `Fill` per trade.
- **3.2 — Cost model.** New module `quantcore/backtest/cost_model.py`. Spread + slippage + commission per fill. Defaults below.
- **3.3 — Portfolio accounting.** New module `quantcore/backtest/portfolio.py`. Equity curve, position rebalance from H017's signed-fraction-of-equity output, drawdown tracking. Replaces zero-cost return summation.

Estimated tests: 12 + 10 + 10 = ~32. Anchor target after Phase 3: ~455.

### Cost model defaults (lean — confirm with user)

- USDJPY: 1 pip spread + 7 USD/lot commission.
- XAUUSD: 30 cent spread + 10 USD/lot commission.
- Slippage: ATR-scaled (0.05 × ATR) on stop fills, zero on limit fills.
- Account: 10000 USD starting equity.

### Open questions for the user before writing code

- **Q1 (most important): M1 data source.** The user has H4 CSVs only. Three options:
  - **(a) Approximate intrabar fill timing using H4 OHLC.** Worst-of-day for stops, best for limits, conservative slippage. Fast to write, less realistic.
  - **(b) Acquire genuine M1 data from MT5 History Center for the same date range (2021-07-02 onward).** The user exports M1 CSVs the same way they did H4. The Phase 2.6a loader generalizes trivially (the function doesn't actually care about the timeframe label).
  - **(c) Hybrid:** H4 OHLC for the body, fall to M1 only when a stop/TP would have triggered intrabar.
  - **Lean: (b).** This is the difference between H001's "backtest is fiction" and a real institutional-grade fill engine. If the user has Exness MT5 already open, this is a one-time export effort.

- **Q2: New `quantcore/backtest/` package, or fold into `quantcore/strategy/`?**
  - Lean: **new `quantcore/backtest/` package.** Backtesting is a distinct concern from strategy logic. `quantcore/strategy/` has the H017 decision panel; `quantcore/backtest/` has the fill simulator. Clean separation will help Phase 4 (the live decision service can reuse `strategy/` without dragging in `backtest/`).

- **Q3: `Fill` dataclass shape (preview, not final):**
  ```
  @dataclass(frozen=True)
  class Fill:
      symbol: str
      side: Literal["buy", "sell"]
      entry_time_utc: pd.Timestamp
      entry_price: float
      exit_time_utc: pd.Timestamp
      exit_price: float
      lots: float
      pnl_quote: float          # in quote currency before commission
      commission: float          # in account currency (USD)
      slippage: float            # in price units, applied to entry/exit
      exit_reason: Literal["stop", "tp", "signal_flip", "end_of_data"]
  ```
  - Confirm with user before locking.

- **Q4: Position-sizing convention for live equity.** H017 returns "signed fraction of equity at risk" (e.g. +0.012 = 1.2% long). The fill engine needs to convert that to lots. Lean: at each rebalance, `lots = (target_risk_fraction * current_equity) / (atr_at_entry * pip_value_per_lot)`. Round to broker step (0.01 lot for both Exness pairs).

- **Q5: Rebalance frequency.** Lean: **on every H4 bar**, sized at the bar that produced the signal, opened on the next bar's open (consistent with the t+1 lag invariant). No mid-bar re-sizing.

### What does NOT change in Phase 3

- H017's strategy logic (`quantcore/strategy/h017.py`). The signal panel is the input to the fill engine, not the other way around.
- The validator framework. Phase 3 produces a returns series; we feed that to the existing `build_h017_claim`.
- The leakage detector. Phase 3 inputs use the post-trim region from 2.6b.

After Phase 3 lands, we re-run the smoke script with the cost-modelled engine and update the load-bearing finding in §6. PSR / MinTRL will likely degrade. The question is whether they degrade catastrophically (H017 → graveyard) or marginally (H017 → live with caveats, or H017 → needs entry filter).

## 12. After Phase 3

- **Phase 4 — MT5 EA shell + Python decision service.** ZeroMQ or named-pipe IPC between the MQL5 EA and the Python service. The Python side holds H017 logic; the EA is a thin client that asks "what should I do this bar?" Includes a circuit breaker for connection loss.
- **Phase 5 — Free-tier VPS deployment.** Oracle Cloud Always Free tier (ARM Ampere). Wine + MT5 + Docker. Python service co-located. Auto-restart on reboot.
- **Phase 6 — Monitoring.** Prometheus (metrics), Grafana (dashboards), Loki (log aggregation), Telegram alerts. Self-hosted on the same VPS.
- **Phase 7 — Governance & continuous improvement.** Hypothesis lifecycle (open/test/promote/retire), shadow trading, walk-forward refresh schedule, model degradation alarms.

## 13. Token-Budget Discipline & New-AI Failure Protocol

- Prefer ONE complete file per response when introducing a new module. ALWAYS finish the current code block before stopping.
- If user reports a cut-off, **RESTART that file from the top in the next response — do not try to "continue from" a partial paste**. Phase 2.6c learned this the hard way.
- Save HANDOFF documents BEFORE the conversation gets long.
- When the user says "your token is nearing its end," prioritize: (1) finishing whatever code block is in flight, (2) writing/updating the next handoff doc, (3) committing the handoff doc.
- **CRITICAL — New AI failure protocol:** This project has had multiple failed handoff attempts where new AIs returned "No response provided" after receiving the handoff doc. THIS IS NOT THE USER'S FAULT and NOT a problem with the handoff doc — it's a platform-side issue. When the user reports this, DO NOT suggest making the handoff "smaller", DO NOT tell them to try a fresh chat, DO NOT apologize repeatedly. Instead, just CONTINUE THE WORK YOURSELF in the current chat. Phases 1.10 through 1.14, 2.1 through 2.5, 2.6a, 2.6b, and 2.6c were all completed this way after new-AI handoff attempts silently failed.

## 14. Repo Hygiene Lessons From Prior Sessions (DO NOT REPEAT)

This project has had silent git-tracking failures, all caught only because `git status` was actually read:

- `.gitignore` had `data/` (unrooted), silently excluding `quantcore/data/`. Fixed with `/data/` (root-anchored).
- Phase 1.5's commit was incomplete — `lookahead.py` was never `git add`-ed despite the commit message claiming otherwise.
- Phase 1.8's commit was incomplete — `cpcv.py` and the `__init__.py` export update were never committed.
- Phase 2.4: Indicator kwarg names in §6 conventions describe SEMANTICS, not exact spelling. Always run `inspect.signature` before calling internal functions from a new module. Phase 2.4 had to be patched because `mult=` was assumed when the real kwarg is `multiplier=`, and `vol_target_size` takes a Series of returns, not a DataFrame.
- Phase 2.5: Negative-test helpers must produce variance > 0. `probabilistic_sharpe_ratio` raises `ValueError` on std < 1e-12 (Sharpe is mathematically undefined when there is no dispersion). Tests trying to assert "promotable=False on zero returns" using `np.zeros` will fail at the validator, not at the gate. Use `rng.normal(0.0, small_sigma, n)` for no-edge negative tests.
- Phase 2.6a: The canonical OHLCV enforcer was named `_ensure_canonical` (private) when §6 docs treated it as part of the public contract. Promoted via alias rather than rename so existing `tests/test_loaders.py` imports survive. Lesson: §6 doc names are semantic; ALWAYS run `inspect.getmembers` and `git grep` before importing.
- Phase 2.6a: `assert X := Y` is invalid syntax for attribute-access X. The walrus operator binds only to plain Name targets. Defensive "linter placeholder" lines are an antipattern — if an import is unused, just remove it.
- Phase 2.6b: My OWN code had `from quantcore.strategy.h017 import H017BacktestResult` when `H017BacktestResult` lives in `h017_claim`. Even when the §10 inspect output is right in front of you, splitting imports across multiple lines invites typos. Prefer a SINGLE consolidated import block per source module per consuming file.
- Phase 2.6b: First leakage-detector heuristic ("walk backward from last suspect date") was wrong because forex weekends are sporadically suspect throughout the entire history. Correct heuristic: "first date meeting threshold = first reliable date." 49% of calendar dates failing the threshold should have been the giveaway that the heuristic was treating off-days as leakage.
- Phase 2.6b: The `git push` failed with `Could not resolve host: github.com` — a transient network issue, not a project bug. The local commit (`c004d87`) was unaffected. When this happens, just retry `git push` later; if you need to fix the unpushed commit, `git commit --amend --no-edit` is safe because origin doesn't know about it yet.
- Phase 2.6c-i: The leakage helpers were originally written inline in `scripts/run_h017_real.py`. Per §6 ("production code lives only in `quantcore/`"), they were promoted to `quantcore/data/leakage.py` with public re-exports from `quantcore/data/__init__.py`. The script then imports from the library. Lesson: anything that warrants tests warrants library status.
- Phase 2.6c-ii: When writing synthetic MT5 CSVs for tests, skip weekends (`weekday() < 5`) — otherwise the Saturday/Sunday bars will fight the leakage detector's classification (correctly counted as low-density off-days), and the test counts won't match expectations.
- Phase 2.6c-ii: VS Code can silently keep an unsaved buffer that overwrites your edits when you re-save. If a code change "doesn't take effect," verify with `Get-Content <file> | Select-Object -First 60` BEFORE diagnosing as a logic bug. The Phase 2.6b import-error reappearance (after we'd already fixed it once) was caused by exactly this.
- HANDOFF docs: When the user requests a handoff, produce the COMPLETE doc, never abbreviated. See §1 handoff-request rule and §8 ("When user asks for a handoff doc, produce a COMPLETE, FULLY SELF-CONTAINED version"). HANDOFF_11 was the first time this was done thoroughly; HANDOFF_12 continues that standard.

Mitigations now mandatory every sub-phase:

- Every sub-phase ends with THREE git commands: `git add ...`, `git commit -m ...`, `git push`.
- After every commit, the user runs `git status` AND `git ls-files <newly-touched-dirs>/`. The AI MUST read this output and confirm before moving on.
- If `git status` ever shows untracked files in `quantcore/` or `tests/` that aren't `__pycache__`, treat it as a defect and stop.
- Test-count drops are regressions. Always count files before and after.
- Before writing a module that calls existing internal functions, run `inspect.signature` AND `dataclasses.fields` to verify kwarg names and field names.
- Prefer ONE consolidated multi-line import block per source module (Phase 2.6b lesson).
- If a code block is cut off mid-paste, RESTART the affected file from the top — do not try to merge with a partial (Phase 2.6c lesson).

## 15. Future-Scope Question Already Raised by User

The user has asked whether the EA can be tested across "a whole bunch of pairs and anything Exness offers." The validation framework is symbol-agnostic. The strategy layer is intentionally scoped to USDJPY + XAUUSD because of H015 (diversification into negative-edge instruments destroys the portfolio).

When this comes up again (typically post-Phase 4):

- Each new symbol is its own hypothesis cycle (open H018, H019, ...).
- Per-symbol model (H005), per-symbol ATR stops, per-symbol inclusion in the H017 heat governor.
- Mechanical scaling is free; edge validation per symbol is not.
- Do NOT broaden the symbol universe before H017 is live and stable on the two-asset core.

## First Reply From New AI Should Be

A short acknowledgement (3–5 sentences) confirming:

- Stack: Windows, .venv, VS Code, Python 3.12.10, PowerShell.
- Test count anchor: 423 (verify via §10 hygiene commands).
- Phase 2.6 is COMPLETE. Next deliverable is Phase 3 — realistic event-driven backtest engine. Per §11 design brief, the FIRST thing to confirm with the user is Q1 (M1 data source: approximate from H4 OHLC, or have the user export real M1 CSVs from MT5 History Center).
- Same step-by-step format (Windows paths, full code, expected test count, git add/commit/push, post-commit verification, three-options ending).

DO NOT produce code yet — wait for hygiene-verification output, the user's answers to Q1–Q5, AND the user's "continue" / ✅.