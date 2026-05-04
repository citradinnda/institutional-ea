# Project Handoff — Institutional-Grade MT5 EA on Retail Stack (Continuation #5)

You are continuing an existing project that has already gone through FIVE AI handoffs. Read this entire document before responding. Do not invent context that isn't here. When in doubt, ask the user before writing code.

## 1. Identity and Tone

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows. The user is intelligent but is NOT a professional developer. They have already burned through 16 dead strategies (graveyard, see §6) and are now building infrastructure-first.

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

## 2. Project Goal

USDJPY + XAUUSD MT5 expert advisor with institutional-grade epistemology on a retail stack (Kaggle research, MT5 execution, Oracle Cloud Always Free VPS production).

8 phases:

- Phase 0 — Foundation (repo, CI, DVC, MLflow). Partially done — MLflow/DVC deferred.
- Phase 1 — Research Framework (`quantcore` package). IN PROGRESS — at sub-phase 1.12.
- Phase 2 — H017 Strategy Logic (H016 + portfolio heat governor).
- Phase 3 — Realistic event-driven backtest engine with intrabar M1 fills.
- Phase 4 — MT5 EA shell + Python decision service.
- Phase 5 — Free-tier VPS deployment (Oracle Cloud Always Free, Wine + MT5, Docker).
- Phase 6 — Monitoring (Prometheus + Grafana + Loki + Telegram alerts).
- Phase 7 — Governance & continuous improvement.

## 3. Repo Layout — `C:\Users\equin\Documents\institutional-ea\`

```
institutional-ea/
├── .venv/  (gitignored, Python 3.12.10)
├── .gitignore  (/data/ root-anchored — do NOT change to data/)
├── pyproject.toml  (Python ≥3.11; deps: numpy, pandas, scipy,
│                   scikit-learn, lightgbm, pyarrow, pyyaml,
│                   matplotlib, tqdm; dev: pytest, pytest-cov,
│                   hypothesis, ruff, black)
├── README.md
├── HANDOFF_3.md  (kept for history)
├── HANDOFF_4.md  (kept for history)
├── HANDOFF_5.md  (this document)
├── ea_mt5/  (empty — Phase 4)
├── governance/hypotheses/  (empty — Phase 1.x)
├── ops/  (empty — Phase 5/6)
├── quantcore/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py  (re-exports Checksum + hash/verify helpers)
│   │   ├── loaders.py  (Phase 1.1)
│   │   ├── reconcile.py  (Phase 1.2)
│   │   ├── outliers.py  (Phase 1.3)
│   │   └── checksums.py  (Phase 1.4)
│   ├── governance/__init__.py
│   ├── utils/__init__.py
│   └── validation/
│       ├── __init__.py  (exports all symbols below)
│       ├── lookahead.py  (Phase 1.5)
│       ├── metrics.py  (Phase 1.6)
│       ├── purged_kfold.py  (Phase 1.7)
│       ├── cpcv.py  (Phase 1.8)
│       ├── walk_forward.py  (Phase 1.9)
│       └── deflated_sharpe.py  (Phase 1.10 + 1.11 — PSR, DSR, MinTRL)
├── research/  (empty — Kaggle notebooks)
└── tests/
    ├── __init__.py
    ├── test_loaders.py  (9 tests)
    ├── test_reconcile.py  (9 tests)
    ├── test_outliers.py  (10 tests)
    ├── test_smoke.py  (3 tests)
    ├── test_checksums.py  (14 tests)
    ├── test_lookahead.py  (15 tests)
    ├── test_metrics.py  (26 tests)
    ├── test_purged_kfold.py  (20 tests)
    ├── test_cpcv.py  (24 tests)
    ├── test_walk_forward.py  (25 tests)
    ├── test_deflated_sharpe.py  (31 tests)
    └── test_min_trl.py  (19 tests)
```

## 4. Phase 1 Sub-Phase Status

- 1.0 Skeleton, venv, pyproject, pre-commit, smoke test ✅ Done
- 1.1 Data loaders (canonical OHLCV, parquet, HistData CSV, resample) ✅ Done
- 1.2 Cross-vendor reconciliation (ATR-scaled tolerance) ✅ Done
- 1.3 Outlier detection (MAD z-score) ✅ Done
- 1.4 Checksums (file SHA-256 + DataFrame SHA-256) ✅ Done
- 1.5 Lookahead guard (prefix-truncation invariant) ✅ Done
- 1.6 Performance metrics + stationary-bootstrap CIs ✅ Done
- 1.7 Purged K-Fold with embargo (optional t1 series) ✅ Done
- 1.8 Combinatorial Purged CV (CPCV) + path assembly matrix ✅ Done
- 1.9 Walk-forward (rolling and anchored, embargo + tz-aware t1 purge) ✅ Done
- 1.10 Probabilistic Sharpe + Deflated Sharpe ✅ Done (31 tests)
- 1.11 Minimum Track Record Length (MinTRL) ✅ Done (19 tests)
- **1.12 White's Reality Check (bootstrap, recentered) ⬅️ NEXT**
- 1.13 Multiple testing correction (Bonferroni, Holm, Benjamini-Hochberg) pending
- 1.14 Validator orchestrator (`Validator.run()` returns gate report) pending

**Test count after Phase 1.11: 205 passing.** Anchor breakdown: loaders 9 + reconcile 9 + outliers 10 + smoke 3 + checksums 14 + lookahead 15 + metrics 26 + purged_kfold 20 + cpcv 24 + walk_forward 25 + deflated_sharpe 31 + min_trl 19 = 205. The pytest output `205 passed` is the source of truth — do not regress below this.

## 5. Conventions Already Established

- Canonical OHLCV: lowercase columns `open, high, low, close, volume`, UTC `DatetimeIndex`, no duplicates, sorted ascending. Enforced by `_ensure_canonical()` in `quantcore/data/loaders.py`.
- MT5 bar labeling: `label="left", closed="left"` in resample. Bar timestamp = its OPEN time.
- Tolerance comparisons in ATR units, not absolute price.
- Flag, never auto-delete, outliers.
- Tests live only in `tests/`. Production code lives only in `quantcore/`. Never mix.
- Test count is a coverage signal. If pytest collects fewer items after a change, treat it as a regression.
- Structured returns are `@dataclass(frozen=True)` with self-describing fields (no bare tuples).
- Float comparisons use a tolerance (`< 1e-12`), not `== 0`.
- Block-bootstrap CIs use the stationary bootstrap (Politis–Romano 1994) with default expected block length = `n^(1/3)`. Percentile CIs (not BCa).
- Lookahead guard truncations default to 4 strategic points (early/middle/late/last); explicit truncations required for operations sensitive to specific bar positions (e.g. `bfill`).
- Purged K-Fold (1.7), CPCV (1.8), and WalkForward (1.9) all take an OPTIONAL `t1` series for per-label end times; if omitted, only embargo applies (fine for fixed-horizon labels).
- CPCV uses lexicographic combination ordering (`itertools.combinations(range(N), k)`); `path_assembly_matrix()` is greedy in that order. With k>=2 a single combination can legitimately appear multiple times in one path-column. Do not assert "distinct combo per column."
- WalkForward exposes `mode: Literal["rolling", "anchored"]`, `train_size`, `test_size`, `step_size` (defaults to `test_size`), `embargo_pct`, `t1`. One class, two modes — DO NOT split it. Returns `WalkForwardSplit` frozen dataclass.
- TZ-aware t1 trap (1.9 lesson): `pd.Series.values` on a tz-aware datetime Series strips the timezone. Use `series.iloc[idx]` and `.to_numpy()` AFTER the comparison.
- **PSR/DSR/MinTRL convention (1.10/1.11)**: PSR/DSR/MinTRL formulas operate on PER-PERIOD Sharpe ratios. The `observed_sr` field in result dataclasses is ANNUALIZED for human display (matches `metrics.sharpe_ratio`). The `sr_benchmark` argument is annualized and translated internally as `sr_benchmark / sqrt(periods_per_year)`. Do not mix conventions.
- **MinTRL infeasible sentinel (1.11 lesson)**: When `observed_sr <= sr_benchmark`, return `min_n=-1`, `min_n_years=float('inf')`, `feasible=False`. Do NOT raise. Type-stable, easy to filter.
- **Sample-mean drift trap (1.10 lesson)**: Tests that assert "PSR ≈ 0.5 for zero-mean returns" must EXPLICITLY center the sample with `r = r - r.mean()`. Drawing 5000 N(0, σ²) samples gives a non-zero realized mean that drives PSR off 0.5 in a seed-dependent way. The mathematical invariant is `SR_hat = 0 ⇒ PSR = 0.5`, not "true mean = 0 ⇒ PSR ≈ 0.5".

## 6. Strategy Graveyard (immutable history — H001 through H016)

- H001: Backtest without intrabar SL/TP simulation is fiction → must use M1 within H4 bars to resolve fills.
- H002–H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
- H004a: Single-seed models unreliable → multi-seed ensembles.
- H005: Stacked multi-symbol models fail on heterogeneous instruments → per-symbol models.
- H006–H007: Confidence filters ≠ risk management. ML chooses entries; deterministic rules manage risk.
- H008–H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals can't be the risk manager.
- H011–H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing = real edge on USDJPY. Single-asset has a tail-risk ceiling.
- H014–H016: Two-asset USDJPY+XAUUSD reduces kurtosis to 1.69, Sortino 4.69, but 1% per-trade risk ≠ 1% portfolio risk when trades overlap → DD breach -19.43%.
- H015: Diversification into negative-edge instruments destroys the portfolio. (Critical for any future "more pairs" decision — see §11.)
- H017 = H016 + portfolio heat governor (caps simultaneous open risk + correlation-adjusted sizing).

## 7. Handoff Rules

- Do not rewrite already-completed code. It exists, it's tested, leave it alone unless the user asks.
- Continue from sub-phase 1.12 (White's Reality Check).
- One sub-phase per response.
- Always include: explicit Windows file paths, full code blocks, exact expected test count, `git add` + `git commit` + `git push` lines, post-commit verification (`git status` + `git ls-files`), and the three-options ending.
- Free-tier infrastructure only: Kaggle, Oracle Cloud Always Free, Telegram. No paid services.
- Never break tests. If the test count would drop, refuse and ask first.
- Match prior code style: type hints, dataclasses for structured returns, `from __future__ import annotations`, docstrings explaining WHY.
- When user says "continue," produce the next sub-phase.
- Pre-existing Pylance/static-type warnings (deferred to a future type-cleanup sub-phase, do NOT fix in-line):
  - `quantcore/data/outliers.py` (`.diff` on `NDArray`)
  - `quantcore/data/loaders.py` and `tests/test_loaders.py` (`Index.tz_localize` / `tz_convert` / `.shift` / `.tz`)
  - `quantcore/validation/purged_kfold.py` and `quantcore/validation/cpcv.py` and `tests/test_purged_kfold.py` (`DatetimeIndex.asi8`)
  - `tests/test_checksums.py` (Scalar+float operator)

## 8. Current State at Handoff #5

- Python 3.12.10 in `.venv`.
- All 205 tests passing.
- GitHub remote: `https://github.com/citradinnda/institutional-ea.git` (origin/main in sync, working tree clean at last verification).
- All seven `quantcore/validation/` files tracked: `__init__.py`, `cpcv.py`, `deflated_sharpe.py`, `lookahead.py`, `metrics.py`, `purged_kfold.py`, `walk_forward.py`.
- All five `quantcore/data/` files tracked: `__init__.py`, `loaders.py`, `reconcile.py`, `outliers.py`, `checksums.py`.
- All twelve `tests/test_*.py` files tracked plus `tests/__init__.py`.

Most recent commits at handoff time (newest first):

- `a349424` Phase 1.11: minimum track record length with PSR-inverse + from-returns convenience
- `e8cbbc3` Phase 1.10: probabilistic Sharpe and deflated Sharpe with PSR/DSR dataclasses
- `0b04ffd` Add handoff document #4 for AI continuity at Phase 1.10
- `1150c95` Phase 1.9: walk-forward CV with rolling and anchored modes, embargo and tz-aware t1 purge
- `8450b5a` Add handoff document #3 for AI continuity at Phase 1.9
- `8f100ee` Phase 1.8 hygiene: track cpcv.py and validation/init.py exports (silent miss)
- `36b99b0` Phase 1.8 fix: relax CPCV path-assembly column test (k>=2 allows repeated combos)
- `2e70375` Phase 1.7: purged K-Fold cross-validation with embargo and optional t1
- `04ea220` Repo hygiene: track Phase 1.5 lookahead.py and stage all missed validation/init.py updates
- `eed4730` Repo hygiene: fix .gitignore that excluded quantcore/data, restore tracked production sources

**User is ready for Phase 1.12 — White's Reality Check.**

## 9. First Reply From New AI Should Be

A short acknowledgement (3–5 sentences) confirming:

- Stack: Windows, `.venv`, VS Code, Python 3.12.10, PowerShell.
- 205 tests passing, next deliverable is Phase 1.12 — White's Reality Check (bootstrap, recentered).
- Same step-by-step format (Windows paths, full code, expected test count, git add/commit/push, post-commit verification, three-options ending).
- DO NOT produce Phase 1.12 code yet — wait for the user to type "continue" or ✅ AND wait for the hygiene-verification output (§10).

Mandatory hygiene-verification step BEFORE producing Phase 1.12 code: ask the user to paste the output of:

```powershell
git log --oneline -10
git ls-files quantcore/ tests/
git status
git remote -v
```

Confirm:

- HEAD = `a349424` (Phase 1.11) on main, in sync with `origin/main`.
- Working tree clean.
- All 7 expected `quantcore/validation/` files tracked (incl. `deflated_sharpe.py`).
- All 5 expected `quantcore/data/` files tracked.
- All 12 `tests/test_*.py` files tracked plus `tests/__init__.py`.

If anything is wrong, fix the hygiene first; do not proceed.

### Optional design questions to ask before writing Phase 1.12 code

1. **Module name.** Suggested: `quantcore/validation/reality_check.py` containing White's Reality Check (Hansen's SPA test deferred to a future sub-phase if the user wants it). Default if user says "you decide": single file `reality_check.py`.

2. **API shape.** Suggested:
   - `whites_reality_check(returns_matrix: np.ndarray | pd.DataFrame, benchmark_returns: np.ndarray | pd.Series | None = None, n_bootstrap: int = 2000, block_length: int | None = None, periods_per_year: int = 252, random_state: int | None = None) -> RealityCheckResult`
   - `returns_matrix` shape `(T, K)` where K is the number of competing strategies; each column is a per-period return series.
   - `benchmark_returns` shape `(T,)`; defaults to all-zeros (i.e. raw returns, not excess).
   - Block length defaults to `T^(1/3)` (matches the stationary bootstrap convention from Phase 1.6).
   - `RealityCheckResult(p_value: float, best_strategy_idx: int, best_observed_mean_excess: float, n_bootstrap: int, n_strategies: int, block_length: int)` — frozen dataclass.
   - Returns the **recentered** bootstrap p-value: probability that the best bootstrapped mean excess return >= the observed best mean excess return, under the null that no strategy beats the benchmark.

3. **Bootstrap convention.** Stationary bootstrap (Politis–Romano 1994), matching Phase 1.6 metrics. WHY: serial correlation in returns means iid bootstrap underestimates p-values. Default if user says "you decide": stationary bootstrap with `p = 1/block_length`.

4. **Recentering.** White's null is "no strategy beats the benchmark on average." Recenter each strategy's returns by subtracting its own observed mean excess return BEFORE bootstrapping. WHY: under the null, the expected mean excess is zero; recentering makes the bootstrap distribution match the null. Default: yes, recenter (this is what makes it "White's Reality Check," not just a naïve bootstrap).

5. **References to cite in docstrings.**
   - White, H. (2000). "A Reality Check for Data Snooping." *Econometrica*, 68(5), 1097–1126.
   - Politis, D. N., & Romano, J. P. (1994). "The Stationary Bootstrap." *JASA*, 89(428), 1303–1313.

## 10. Repo Hygiene Lessons From Prior Sessions (DO NOT REPEAT)

This project has had THREE silent git-tracking failures, all caught by `git status` after the fact:

- `.gitignore` had `data/` (unrooted), silently excluding `quantcore/data/`. Fixed with `/data/` (root-anchored). Diagnostic: `git check-ignore -v <path>`.
- Phase 1.5's commit was incomplete — `lookahead.py` was never `git add`-ed despite the commit message claiming otherwise. Discovered two sub-phases later.
- Phase 1.8's commit was incomplete — `cpcv.py` and the `__init__.py` export update were never committed. The "Phase 1.8 fix" commit only included the test file. Discovered immediately because the `git status` output was actually read out loud and reviewed by the AI. **This is the protocol going forward: VERIFY THE STATUS, do not just print the command.**

Mitigations now mandatory every sub-phase:

- Every sub-phase ends with THREE git commands: `git add ...`, `git commit -m ...`, `git push`.
- After every commit, the user runs `git status` (must show "working tree clean") AND `git ls-files <newly-touched-dirs>/` (must list every new file). The AI MUST read this output and confirm before moving on. Do not advance to the next sub-phase if `git status` is unverified.
- If `git status` ever shows untracked files in `quantcore/` or `tests/` that aren't `__pycache__`, treat it as a defect and stop.
- The remote is GitHub (`origin = https://github.com/citradinnda/institutional-ea.git`). Local-only is unsafe.

## 11. Future-Scope Question Already Raised by the User

The user has asked whether the EA can be tested across "a whole bunch of pairs and anything Exness offers." The validation framework (`quantcore/validation/`) is fully symbol-agnostic and already supports any return series. The strategy layer is intentionally scoped to USDJPY + XAUUSD because of H015: diversification into a negative-edge instrument destroys the portfolio.

When this comes up again (typically post-Phase 4), the answer is:

- Each new symbol is its own hypothesis cycle (open H018, H019, ...).
- Per-symbol model (H005), per-symbol ATR-calibrated stops (already scale-invariant), per-symbol inclusion in the H017 heat governor with correlation-adjusted sizing.
- Mechanical scaling is free; edge validation per symbol is not.
- Do NOT broaden the symbol universe before H017 is live and stable on the two-asset core.

If the user requests broader symbols earlier, push back politely and reference H015.

## 12. Token-Budget Discipline

Prior continuations have ended with the AI's response cut off mid-code-block. Mitigations:

- Prefer ONE complete file per response when introducing a new module. If a file would exceed safe length, split it across responses but ALWAYS finish the current code block before stopping.
- If user reports a cut-off, restart that step from the beginning of the affected file/block — do not try to "continue from" a partial paste. (This happened in Phase 1.10 — the docstring was cut off mid-reference; the file was restarted cleanly and worked first try.)
- Save HANDOFF documents BEFORE the conversation gets long. Recommend the user commit handoff docs as soon as they're written.
- When the user says "your token is nearing its end," prioritize: (1) finishing whatever code block is in flight, (2) writing/updating the next handoff doc, (3) committing the handoff doc. Defer everything else to the next session.

## 13. Phase 1.10 + 1.11 Specific Notes (for the new AI's reference)

- Both PSR (1.10) and MinTRL (1.11) live in `quantcore/validation/deflated_sharpe.py`. The file also contains DSR. They share `_per_period_sharpe`, `_sample_skew`, `_sample_excess_kurtosis`, `_psr_from_moments`, `_to_1d_array` helpers.
- Public symbols exported from `quantcore.validation`: `PSRResult`, `DSRResult`, `MinTRLResult`, `probabilistic_sharpe_ratio`, `deflated_sharpe_ratio`, `min_track_record_length`, `min_track_record_length_from_returns`, `expected_max_sharpe`.
- PSR formula: `Phi( (SR_hat - SR*) * sqrt(n - 1) / sqrt(1 - skew*SR_hat + (kurt/4)*SR_hat^2) )` where `kurt` is EXCESS kurtosis (Gaussian = 0) and SRs are PER-PERIOD.
- DSR deflates the benchmark by `expected_max_sharpe(n_trials, sr_variance)`, where `sr_variance` is `Var[SR estimates across trials, ddof=1]` (per-period). When `n_trials == 1` or `sr_variance == 0`, deflation is exactly 0 and DSR == PSR.
- `expected_max_sharpe` formula: `sqrt(V[SR]) * ((1 - γ) * Φ⁻¹(1 - 1/N) + γ * Φ⁻¹(1 - 1/(N·e)))` where γ is Euler-Mascheroni ≈ 0.5772.
- MinTRL formula: `n_min = 1 + (1 - skew*SR + (kurt/4)*SR^2) * (z / (SR - SR*))^2` with `z = Φ⁻¹(confidence)`. Result is `ceil`-rounded to the smallest integer n satisfying PSR >= confidence. Infeasible iff `SR - SR* <= 1e-12`.
- `min_track_record_length` takes pre-computed moments; `min_track_record_length_from_returns` derives them via the same helpers PSR uses (so they cannot disagree on the same sample).
- Annualization convention: PSR/DSR/MinTRL probabilities computed on PER-PERIOD SR. The `observed_sr` dataclass field is ANNUALIZED via `metrics.sharpe_ratio`. `sr_benchmark` argument is annualized; translated to per-period as `sr_benchmark / sqrt(periods_per_year)` internally.
- Test files: `tests/test_deflated_sharpe.py` (31 tests, covers PSR + DSR + `expected_max_sharpe`), `tests/test_min_trl.py` (19 tests, covers MinTRL + the convenience wrapper + the PSR↔MinTRL round-trip).
- The `test_psr_zero_mean_returns_about_half` test EXPLICITLY centers the sample (`r = r - r.mean()`) and asserts exact equality to 0.5. Don't change this — drift-free centering is the only stable form of this assertion.