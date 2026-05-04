# Project Handoff — Institutional-Grade MT5 EA on Retail Stack (Continuation #6)

You are continuing an existing project that has already gone through SIX AI handoffs. Read this entire document before responding. Do not invent context that isn't here. When in doubt, ask the user before writing code.

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
- DO NOT propose switching to a new AI chat. If the user reports the new AI returning "No response provided," continue the work directly. The handoff doc is for emergencies; producing the next sub-phase yourself is always the better path.

## 2. Project Goal

USDJPY + XAUUSD MT5 expert advisor with institutional-grade epistemology on a retail stack (Kaggle research, MT5 execution, Oracle Cloud Always Free VPS production).

8 phases:

- Phase 0 — Foundation (repo, CI, DVC, MLflow). Partially done — MLflow/DVC deferred.
- Phase 1 — Research Framework (`quantcore` package). IN PROGRESS — at sub-phase 1.13.
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
├── HANDOFF_5.md  (kept for history)
├── HANDOFF_6.md  (this document)
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
│       ├── deflated_sharpe.py  (Phase 1.10 + 1.11 — PSR, DSR, MinTRL)
│       └── reality_check.py  (Phase 1.12 — White's Reality Check)
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
    ├── test_min_trl.py  (19 tests)
    └── test_reality_check.py  (19 tests)
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
- 1.12 White's Reality Check (stationary bootstrap, recentered) ✅ Done (19 tests)
- **1.13 Multiple-testing correction (Bonferroni, Holm, Benjamini-Hochberg) ⬅️ NEXT**
- 1.14 Validator orchestrator (`Validator.run()` returns gate report) pending

**Test count after Phase 1.12: 224 passing.** Anchor breakdown: loaders 9 + reconcile 9 + outliers 10 + smoke 3 + checksums 14 + lookahead 15 + metrics 26 + purged_kfold 20 + cpcv 24 + walk_forward 25 + deflated_sharpe 31 + min_trl 19 + reality_check 19 = 224. The pytest output `224 passed` is the source of truth — do not regress below this.

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
- Purged K-Fold (1.7), CPCV (1.8), and WalkForward (1.9) all take an OPTIONAL `t1` series for per-label end times; if omitted, only embargo applies.
- CPCV uses lexicographic combination ordering (`itertools.combinations(range(N), k)`); `path_assembly_matrix()` is greedy in that order. With k>=2 a single combination can legitimately appear multiple times in one path-column. Do not assert "distinct combo per column."
- WalkForward exposes `mode: Literal["rolling", "anchored"]`. One class, two modes — DO NOT split it.
- TZ-aware t1 trap (1.9 lesson): `pd.Series.values` on a tz-aware datetime Series strips the timezone. Use `series.iloc[idx]` and `.to_numpy()` AFTER the comparison.
- **PSR/DSR/MinTRL convention (1.10/1.11)**: PSR/DSR/MinTRL formulas operate on PER-PERIOD Sharpe ratios. The `observed_sr` field in result dataclasses is ANNUALIZED for human display. The `sr_benchmark` argument is annualized and translated internally as `sr_benchmark / sqrt(periods_per_year)`. Do not mix conventions.
- **MinTRL infeasible sentinel (1.11 lesson)**: When `observed_sr <= sr_benchmark`, return `min_n=-1`, `min_n_years=float('inf')`, `feasible=False`. Do NOT raise.
- **Sample-mean drift trap (1.10 lesson)**: Tests that assert "PSR ≈ 0.5 for zero-mean returns" must EXPLICITLY center the sample with `r = r - r.mean()`. The mathematical invariant is `SR_hat = 0 ⇒ PSR = 0.5`, not "true mean = 0 ⇒ PSR ≈ 0.5".
- **White's Reality Check convention (1.12)**: stationary bootstrap with default `block_length = round(T^(1/3))`. Recenter each strategy's excess returns by subtracting its own observed mean before bootstrapping (this enforces the null inside the bootstrap world). Test statistic is `V_bar = sqrt(T) * max_k(d_k)` where `d_k` is per-strategy mean excess. Sample row-indices ONCE per replication and apply to ALL K columns to preserve cross-strategy dependence. p-value = fraction of bootstrap reps with `V_bar_b >= V_bar`. 1D input is treated as K=1.
- **Bootstrap test tolerance (1.12 lesson)**: Statistical tests on bootstrap output should use generous tolerance bands (e.g. `p > 0.05` for "high p-value under null", not exact equality). Bootstrap p-values fluctuate by ~1/sqrt(B). Use `n_bootstrap=200-500` in tests for speed; production callers use 2000+.

## 6. Strategy Graveyard (immutable history — H001 through H016)

- H001: Backtest without intrabar SL/TP simulation is fiction → must use M1 within H4 bars to resolve fills.
- H002–H003: ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
- H004a: Single-seed models unreliable → multi-seed ensembles.
- H005: Stacked multi-symbol models fail on heterogeneous instruments → per-symbol models.
- H006–H007: Confidence filters ≠ risk management. ML chooses entries; deterministic rules manage risk.
- H008–H010: High Sharpe with kurtosis 38 is unsafe. ML on basic technicals can't be the risk manager.
- H011–H013: Deterministic ATR stops + chandelier exits + vol-targeted sizing = real edge on USDJPY. Single-asset has a tail-risk ceiling.
- H014–H016: Two-asset USDJPY+XAUUSD reduces kurtosis to 1.69, Sortino 4.69, but 1% per-trade risk ≠ 1% portfolio risk when trades overlap → DD breach -19.43%.
- H015: Diversification into negative-edge instruments destroys the portfolio.
- H017 = H016 + portfolio heat governor (caps simultaneous open risk + correlation-adjusted sizing).

## 7. Handoff Rules

- Do not rewrite already-completed code. It exists, it's tested, leave it alone unless the user asks.
- Continue from sub-phase 1.13 (multiple-testing correction).
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

## 8. Current State at Handoff #6

- Python 3.12.10 in `.venv`.
- All 224 tests passing.
- GitHub remote: `https://github.com/citradinnda/institutional-ea.git` (origin/main in sync, working tree clean at last verification).
- All eight `quantcore/validation/` files tracked: `__init__.py`, `cpcv.py`, `deflated_sharpe.py`, `lookahead.py`, `metrics.py`, `purged_kfold.py`, `reality_check.py`, `walk_forward.py`.
- All five `quantcore/data/` files tracked.
- All thirteen `tests/test_*.py` files tracked plus `tests/__init__.py`.

Most recent commits at handoff time (newest first):

- `95d72e0` Phase 1.12: White's Reality Check with stationary bootstrap and recentering
- `af24d0f` Add handoff document #5 for AI continuity at Phase 1.12
- `a349424` Phase 1.11: minimum track record length with PSR-inverse + from-returns convenience
- `e8cbbc3` Phase 1.10: probabilistic Sharpe and deflated Sharpe with PSR/DSR dataclasses
- `0b04ffd` Add handoff document #4 for AI continuity at Phase 1.10
- `1150c95` Phase 1.9: walk-forward CV with rolling and anchored modes, embargo and tz-aware t1 purge
- `8450b5a` Add handoff document #3 for AI continuity at Phase 1.9
- `8f100ee` Phase 1.8 hygiene: track cpcv.py and validation/init.py exports (silent miss)
- `36b99b0` Phase 1.8 fix: relax CPCV path-assembly column test (k>=2 allows repeated combos)
- `2e70375` Phase 1.7: purged K-Fold cross-validation with embargo and optional t1

**User is ready for Phase 1.13 — multiple-testing correction (Bonferroni, Holm, Benjamini-Hochberg).**

## 9. First Reply From New AI Should Be

A short acknowledgement (3–5 sentences) confirming:

- Stack: Windows, `.venv`, VS Code, Python 3.12.10, PowerShell.
- 224 tests passing, next deliverable is Phase 1.13 — multiple-testing correction (Bonferroni, Holm, Benjamini-Hochberg).
- Same step-by-step format (Windows paths, full code, expected test count, git add/commit/push, post-commit verification, three-options ending).
- DO NOT produce Phase 1.13 code yet — wait for the user to type "continue" or ✅ AND wait for the hygiene-verification output (§10).

Mandatory hygiene-verification step BEFORE producing Phase 1.13 code: ask the user to paste the output of:

```powershell
git log --oneline -10
git ls-files quantcore/ tests/
git status
git remote -v
```

Confirm:

- HEAD = `95d72e0` (Phase 1.12) on main, in sync with `origin/main`.
- Working tree clean.
- All 8 expected `quantcore/validation/` files tracked (incl. `reality_check.py`).
- All 5 expected `quantcore/data/` files tracked.
- All 13 `tests/test_*.py` files tracked plus `tests/__init__.py`.

If anything is wrong, fix the hygiene first; do not proceed.

### Optional design questions to ask before writing Phase 1.13 code

1. **Module name.** Suggested: `quantcore/validation/multiple_testing.py` containing all three corrections (Bonferroni, Holm-Bonferroni, Benjamini-Hochberg FDR) plus a unified `MultipleTestingResult` dataclass. Default if user says "you decide": single file `multiple_testing.py`.

2. **API shape.** Suggested:
   - `bonferroni_correction(p_values, alpha=0.05) -> MultipleTestingResult`
   - `holm_correction(p_values, alpha=0.05) -> MultipleTestingResult`
   - `benjamini_hochberg(p_values, alpha=0.05) -> MultipleTestingResult`
   - All accept 1D array-likes of p-values; all return the same dataclass.
   - `MultipleTestingResult(p_values_raw, p_values_adjusted, rejected, alpha, method, n_tests)` — frozen dataclass with `rejected` as a boolean array of which nulls are rejected at level `alpha`.

3. **FWER vs FDR.** Bonferroni and Holm control Family-Wise Error Rate (FWER) — strict. Benjamini-Hochberg controls False Discovery Rate (FDR) — more powerful, less conservative. Default: include all three; let the caller pick based on their tolerance for false positives. Document the trade-off in the module docstring.

4. **Adjusted p-values vs reject/accept.** Suggested: return BOTH. Adjusted p-values let downstream callers re-threshold without recomputing; the `rejected` boolean is the convenience output for `alpha=0.05` workflows. Default: yes, return both.

5. **References to cite in docstrings.**
   - Bonferroni, C. E. (1936). "Teoria statistica delle classi e calcolo delle probabilità."
   - Holm, S. (1979). "A Simple Sequentially Rejective Multiple Test Procedure." *Scandinavian Journal of Statistics*, 6(2), 65–70.
   - Benjamini, Y., & Hochberg, Y. (1995). "Controlling the False Discovery Rate." *JRSS B*, 57(1), 289–300.

## 10. Repo Hygiene Lessons From Prior Sessions (DO NOT REPEAT)

This project has had THREE silent git-tracking failures, all caught by `git status` after the fact:

- `.gitignore` had `data/` (unrooted), silently excluding `quantcore/data/`. Fixed with `/data/` (root-anchored). Diagnostic: `git check-ignore -v <path>`.
- Phase 1.5's commit was incomplete — `lookahead.py` was never `git add`-ed despite the commit message claiming otherwise.
- Phase 1.8's commit was incomplete — `cpcv.py` and the `__init__.py` export update were never committed. Discovered immediately because the `git status` output was actually read out loud and reviewed by the AI. **Protocol going forward: VERIFY THE STATUS, do not just print the command.**

Mitigations now mandatory every sub-phase:

- Every sub-phase ends with THREE git commands: `git add ...`, `git commit -m ...`, `git push`.
- After every commit, the user runs `git status` (must show "working tree clean") AND `git ls-files <newly-touched-dirs>/` (must list every new file). The AI MUST read this output and confirm before moving on.
- If `git status` ever shows untracked files in `quantcore/` or `tests/` that aren't `__pycache__`, treat it as a defect and stop.
- The remote is GitHub (`origin = https://github.com/citradinnda/institutional-ea.git`).

## 11. Future-Scope Question Already Raised by the User

The user has asked whether the EA can be tested across "a whole bunch of pairs and anything Exness offers." The validation framework (`quantcore/validation/`) is fully symbol-agnostic. The strategy layer is intentionally scoped to USDJPY + XAUUSD because of H015.

When this comes up again (typically post-Phase 4):

- Each new symbol is its own hypothesis cycle (open H018, H019, ...).
- Per-symbol model (H005), per-symbol ATR-calibrated stops, per-symbol inclusion in the H017 heat governor with correlation-adjusted sizing.
- Mechanical scaling is free; edge validation per symbol is not.
- Do NOT broaden the symbol universe before H017 is live and stable on the two-asset core.

## 12. Token-Budget Discipline

- Prefer ONE complete file per response when introducing a new module. ALWAYS finish the current code block before stopping.
- If user reports a cut-off, restart that step from the beginning of the affected file/block — do not try to "continue from" a partial paste. (This happened in Phase 1.10; the file was restarted cleanly and worked first try.)
- Save HANDOFF documents BEFORE the conversation gets long. Recommend committing handoff docs as soon as they're written.
- When the user says "your token is nearing its end," prioritize: (1) finishing whatever code block is in flight, (2) writing/updating the next handoff doc, (3) committing the handoff doc.
- **If the user reports the new AI returning "No response provided," DO NOT try to bounce them again. Just continue the work yourself.** This happened between handoffs #5 and #6 — the user retried multiple new AIs, all failed silently, and the original AI continued through Phase 1.12 directly.

## 13. Phase 1.10–1.12 Specific Notes

- PSR (1.10), DSR (1.10), and MinTRL (1.11) live in `quantcore/validation/deflated_sharpe.py`. Public symbols: `PSRResult`, `DSRResult`, `MinTRLResult`, `probabilistic_sharpe_ratio`, `deflated_sharpe_ratio`, `min_track_record_length`, `min_track_record_length_from_returns`, `expected_max_sharpe`.
- White's Reality Check (1.12) lives in `quantcore/validation/reality_check.py`. Public symbols: `RealityCheckResult`, `whites_reality_check`.
- PSR formula: `Phi( (SR_hat - SR*) * sqrt(n - 1) / sqrt(1 - skew*SR_hat + (kurt/4)*SR_hat^2) )` where `kurt` is EXCESS kurtosis and SRs are PER-PERIOD.
- DSR deflates the benchmark by `expected_max_sharpe(n_trials, sr_variance)`. When `n_trials == 1` or `sr_variance == 0`, deflation is exactly 0 and DSR == PSR.
- MinTRL formula: `n_min = 1 + (1 - skew*SR + (kurt/4)*SR^2) * (z / (SR - SR*))^2` with `z = Φ⁻¹(confidence)`. `ceil`-rounded. Infeasible iff `SR - SR* <= 1e-12`.
- White's Reality Check: stationary bootstrap, default block length `round(T^(1/3))`. Recenter each strategy by subtracting its own observed mean excess. Sample row-indices ONCE per bootstrap rep and apply to all K columns. Test statistic `sqrt(T) * max_k(d_k)`. p-value = fraction of reps with bootstrap statistic >= observed.
- All bootstrap tests use `n_bootstrap` between 200–500 for speed and tolerance bands like `p > 0.05` rather than tight equality. Production callers should use `n_bootstrap=2000+`.
- Test files: `tests/test_deflated_sharpe.py` (31), `tests/test_min_trl.py` (19), `tests/test_reality_check.py` (19).