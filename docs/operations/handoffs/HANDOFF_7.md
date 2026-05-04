# Project Handoff — Institutional-Grade MT5 EA on Retail Stack (Continuation #7)

You are continuing an existing project that has already gone through SEVEN AI handoffs. Read this entire document before responding. Do not invent context that isn't here. When in doubt, ask the user before writing code.

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
- DO NOT propose switching to a new AI chat. If the user reports the new AI returning "No response provided," continue the work directly.

## 2. Project Goal

USDJPY + XAUUSD MT5 expert advisor with institutional-grade epistemology on a retail stack (Kaggle research, MT5 execution, Oracle Cloud Always Free VPS production).

8 phases:

- Phase 0 — Foundation (repo, CI, DVC, MLflow). Partially done — MLflow/DVC deferred.
- Phase 1 — Research Framework (`quantcore` package). IN PROGRESS — at sub-phase 1.14 (LAST SUB-PHASE OF PHASE 1).
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
├── HANDOFF_6.md  (kept for history)
├── HANDOFF_7.md  (this document)
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
│       ├── reality_check.py  (Phase 1.12 — White's Reality Check)
│       └── multiple_testing.py  (Phase 1.13 — Bonferroni, Holm, BH)
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
    ├── test_reality_check.py  (19 tests)
    └── test_multiple_testing.py  (25 tests)
```

## 4. Phase 1 Sub-Phase Status

- 1.0 Skeleton, venv, pyproject, pre-commit, smoke test ✅ Done
- 1.1 Data loaders ✅ Done
- 1.2 Cross-vendor reconciliation ✅ Done
- 1.3 Outlier detection ✅ Done
- 1.4 Checksums ✅ Done
- 1.5 Lookahead guard ✅ Done
- 1.6 Performance metrics + stationary-bootstrap CIs ✅ Done
- 1.7 Purged K-Fold ✅ Done
- 1.8 CPCV + path assembly ✅ Done
- 1.9 Walk-forward (rolling and anchored) ✅ Done
- 1.10 Probabilistic Sharpe + Deflated Sharpe ✅ Done (31 tests)
- 1.11 Minimum Track Record Length ✅ Done (19 tests)
- 1.12 White's Reality Check ✅ Done (19 tests)
- 1.13 Multiple-testing correction (Bonferroni, Holm, Benjamini-Hochberg) ✅ Done (25 tests)
- **1.14 Validator orchestrator ⬅️ NEXT (LAST SUB-PHASE OF PHASE 1)**

**Test count after Phase 1.13: 249 passing.** Anchor breakdown: loaders 9 + reconcile 9 + outliers 10 + smoke 3 + checksums 14 + lookahead 15 + metrics 26 + purged_kfold 20 + cpcv 24 + walk_forward 25 + deflated_sharpe 31 + min_trl 19 + reality_check 19 + multiple_testing 25 = 249. The pytest output `249 passed` is the source of truth — do not regress below this.

NOTE: If user has not yet completed Phase 1.13 at the time of this handoff, the most recent committed state may be Phase 1.12 (224 tests, HEAD `4ba085c` or similar). Verify the actual state via the hygiene commands in §9 before assuming.

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
- CPCV uses lexicographic combination ordering. With k>=2 a single combination can legitimately appear multiple times in one path-column.
- WalkForward exposes `mode: Literal["rolling", "anchored"]`. One class, two modes.
- TZ-aware t1 trap (1.9 lesson): `pd.Series.values` on a tz-aware datetime Series strips the timezone. Use `series.iloc[idx]` and `.to_numpy()` AFTER the comparison.
- **PSR/DSR/MinTRL convention**: PSR/DSR/MinTRL formulas operate on PER-PERIOD Sharpe ratios. The `observed_sr` field in result dataclasses is ANNUALIZED for human display. The `sr_benchmark` argument is annualized and translated internally as `sr_benchmark / sqrt(periods_per_year)`.
- **MinTRL infeasible sentinel**: When `observed_sr <= sr_benchmark`, return `min_n=-1`, `min_n_years=float('inf')`, `feasible=False`. Do NOT raise.
- **Sample-mean drift trap**: Tests asserting "PSR ≈ 0.5 for zero-mean returns" must EXPLICITLY center with `r = r - r.mean()`. The invariant is `SR_hat = 0 ⇒ PSR = 0.5`, not "true mean = 0 ⇒ PSR ≈ 0.5".
- **White's Reality Check convention**: stationary bootstrap, default `block_length = round(T^(1/3))`. Recenter each strategy by subtracting its own observed mean excess. Test statistic `sqrt(T) * max_k(d_k)`. Sample row-indices ONCE per replication and apply to ALL K columns to preserve cross-strategy dependence. p-value = fraction of bootstrap reps with `V_bar_b >= V_bar`.
- **Bootstrap test tolerance**: Statistical tests on bootstrap output should use generous tolerance bands. Bootstrap p-values fluctuate by ~1/sqrt(B). Use `n_bootstrap=200-500` in tests for speed; production callers use 2000+.
- **Multiple-testing convention**: All three corrections (Bonferroni, Holm, BH) return the same `MultipleTestingResult` dataclass with `p_values_raw`, `p_values_adjusted`, `rejected`, `alpha`, `method`, `n_tests`. Adjusted p-values are returned in caller's input order (not sorted). Both Holm and BH use sort + monotone-fix (cummax for Holm, reverse-cummin for BH) so `adjusted <= alpha` is equivalent to the textbook step-down/step-up rules.
- **FWER vs FDR**: Bonferroni and Holm control Family-Wise Error Rate (strict). Benjamini-Hochberg controls False Discovery Rate (more powerful, more permissive). Use FWER for live-trading go/no-go gates; use FDR for early-stage feature screening.

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
- Continue from sub-phase 1.14 (Validator orchestrator).
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

## 8. Current State at Handoff #7

- Python 3.12.10 in `.venv`.
- Tests: see §4 (249 if 1.13 committed, 224 if not yet — verify).
- GitHub remote: `https://github.com/citradinnda/institutional-ea.git` (origin/main expected in sync, working tree clean).
- All `quantcore/validation/` files tracked: `__init__.py`, `cpcv.py`, `deflated_sharpe.py`, `lookahead.py`, `metrics.py`, `multiple_testing.py` (if 1.13 committed), `purged_kfold.py`, `reality_check.py`, `walk_forward.py`. That's 9 files after 1.13, 8 before.
- All five `quantcore/data/` files tracked.
- All `tests/test_*.py` files tracked plus `tests/__init__.py`. 14 test files after 1.13, 13 before.

Most recent commits expected at handoff time (newest first; the 1.13 line may be absent if the user hasn't yet committed it):

- (newest) `Phase 1.13: multiple-testing corrections (Bonferroni, Holm, Benjamini-Hochberg)` — if committed
- `4ba085c` Add handoff document #6 for AI continuity at Phase 1.13
- `95d72e0` Phase 1.12: White's Reality Check with stationary bootstrap and recentering
- `af24d0f` Add handoff document #5 for AI continuity at Phase 1.12
- `a349424` Phase 1.11: minimum track record length with PSR-inverse + from-returns convenience
- `e8cbbc3` Phase 1.10: probabilistic Sharpe and deflated Sharpe with PSR/DSR dataclasses
- `0b04ffd` Add handoff document #4 for AI continuity at Phase 1.10
- `1150c95` Phase 1.9: walk-forward CV
- `8450b5a` Add handoff document #3 for AI continuity at Phase 1.9
- `8f100ee` Phase 1.8 hygiene

**User is ready for Phase 1.14 — the Validator orchestrator (the LAST sub-phase of Phase 1).**

## 9. First Reply From New AI Should Be

A short acknowledgement (3–5 sentences) confirming:

- Stack: Windows, `.venv`, VS Code, Python 3.12.10, PowerShell.
- Test count (verify via hygiene commands), next deliverable is Phase 1.14 — Validator orchestrator (closing Phase 1).
- Same step-by-step format (Windows paths, full code, expected test count, git add/commit/push, post-commit verification, three-options ending).
- DO NOT produce Phase 1.14 code yet — wait for hygiene-verification output AND user's "continue" / ✅.

Mandatory hygiene-verification step BEFORE producing Phase 1.14 code:

```powershell
git log --oneline -10
git ls-files quantcore/ tests/
git status
git remote -v
pytest -q
```

Confirm:

- Working tree clean, in sync with `origin/main`.
- All expected `quantcore/validation/` files tracked (9 if 1.13 committed, 8 if not).
- All expected `tests/test_*.py` files tracked (14 if 1.13 committed, 13 if not).
- pytest passes — exact count must match §4 expectations.

**If the user has NOT yet completed Phase 1.13, do that first.** Phase 1.13 spec is in §13 below; produce it before 1.14.

### Optional design questions to ask before writing Phase 1.14 code

1. **Module name.** Suggested: `quantcore/validation/validator.py` containing the `Validator` class plus a `ValidatorReport` dataclass that aggregates all the gate results.

2. **API shape.** Suggested:
   - `Validator(periods_per_year=252, alpha=0.05, sr_benchmark=0.0, confidence=0.95, n_bootstrap=2000, random_state=None)` — config-style constructor.
   - `Validator.run(returns, sr_estimates=None, candidate_returns_matrix=None, p_values=None, mt_method="holm") -> ValidatorReport` — runs the full gate battery.
   - Gates run: PSR, DSR (if `sr_estimates` given), MinTRL, Reality Check (if `candidate_returns_matrix` given), multiple-testing correction (if `p_values` given).
   - Each gate is OPTIONAL based on inputs provided. The PSR + MinTRL gates are mandatory (always run).

3. **Pass/fail logic.** Suggested: each gate produces a boolean `passed` flag. The aggregate `ValidatorReport.all_passed` is the AND of all gates that ran. Individual gate results are stored as dataclass fields so callers can drill in.

4. **`ValidatorReport` shape.** Suggested:
```python
@dataclass(frozen=True)
class ValidatorReport:
    psr: PSRResult
    psr_passed: bool  # psr.psr >= 1 - alpha
    min_trl: MinTRLResult
    min_trl_passed: bool  # min_trl.feasible and min_trl.min_n <= n_observed
    dsr: DSRResult | None
    dsr_passed: bool | None  # dsr.dsr >= 1 - alpha if run
    reality_check: RealityCheckResult | None
    reality_check_passed: bool | None  # rc.p_value <= alpha if run
    multiple_testing: MultipleTestingResult | None
    multiple_testing_passed: bool | None  # at least one rejection if run
    all_passed: bool
    n_gates_run: int
    summary: str  # human-readable one-paragraph summary
```

5. **References.** All gates already cite their sources; the Validator just composes them. Module docstring should explain the gate philosophy: each gate catches a different failure mode (PSR for sample size + non-normality, MinTRL for track-record adequacy, DSR for selection bias on Sharpe, RC for selection bias on returns, multi-test for general p-value families).

Estimated test count for 1.14: ~20 tests (per-gate pass/fail, aggregation, optional-input handling, end-to-end smoke). Target after 1.14: ~269 if starting from 249, ~244 if starting from 224.

## 10. Repo Hygiene Lessons From Prior Sessions (DO NOT REPEAT)

This project has had THREE silent git-tracking failures, all caught by `git status` after the fact:

- `.gitignore` had `data/` (unrooted), silently excluding `quantcore/data/`. Fixed with `/data/` (root-anchored).
- Phase 1.5's commit was incomplete — `lookahead.py` was never `git add`-ed despite the commit message claiming otherwise.
- Phase 1.8's commit was incomplete — `cpcv.py` and the `__init__.py` export update were never committed. Discovered immediately because `git status` was actually read out loud and reviewed by the AI. **VERIFY THE STATUS, do not just print the command.**

Mitigations now mandatory every sub-phase:

- Every sub-phase ends with THREE git commands: `git add ...`, `git commit -m ...`, `git push`.
- After every commit, the user runs `git status` AND `git ls-files <newly-touched-dirs>/`. The AI MUST read this output and confirm before moving on.
- If `git status` ever shows untracked files in `quantcore/` or `tests/` that aren't `__pycache__`, treat it as a defect and stop.

## 11. Future-Scope Question Already Raised by the User

The user has asked whether the EA can be tested across "a whole bunch of pairs and anything Exness offers." The validation framework is symbol-agnostic. The strategy layer is intentionally scoped to USDJPY + XAUUSD because of H015.

When this comes up again (typically post-Phase 4):

- Each new symbol is its own hypothesis cycle (open H018, H019, ...).
- Per-symbol model (H005), per-symbol ATR stops, per-symbol inclusion in the H017 heat governor.
- Mechanical scaling is free; edge validation per symbol is not.
- Do NOT broaden the symbol universe before H017 is live and stable on the two-asset core.

## 12. Token-Budget Discipline & New-AI Failure Protocol

- Prefer ONE complete file per response when introducing a new module. ALWAYS finish the current code block before stopping.
- If user reports a cut-off, restart that step from the beginning of the affected file/block — do not try to "continue from" a partial paste.
- Save HANDOFF documents BEFORE the conversation gets long.
- When the user says "your token is nearing its end," prioritize: (1) finishing whatever code block is in flight, (2) writing/updating the next handoff doc, (3) committing the handoff doc.
- **CRITICAL — New AI failure protocol**: This project has had multiple failed handoff attempts where new AIs (in different chat windows) returned "No response provided" after receiving the handoff document. THIS IS NOT THE USER'S FAULT and NOT a problem with the handoff doc — it's a platform-side issue (likely rate limiting, timeout, or model-version glitch). When the user reports this, DO NOT:
  - Suggest making the handoff "smaller" or "simpler"
  - Tell them to try again with a fresh chat
  - Apologize repeatedly
  
  Instead, just CONTINUE THE WORK YOURSELF in the current chat. Phases 1.10, 1.11, 1.12, and 1.13 were all completed this way after new-AI handoff attempts silently failed. The original chat continued past five planned handoff points and delivered everything successfully.

## 13. Phase 1.13 Spec (in case user hasn't completed it yet)

If hygiene check shows test count is 224 (not 249) and `multiple_testing.py` is absent, produce Phase 1.13 first. Spec:

**File:** `quantcore/validation/multiple_testing.py`

Public API:
- `bonferroni_correction(p_values, alpha=0.05) -> MultipleTestingResult` — adjusted = `min(K * raw, 1.0)`.
- `holm_correction(p_values, alpha=0.05) -> MultipleTestingResult` — sort ascending, multiplier `(K - j + 1)`, cummax to enforce monotonicity, clip to 1.0.
- `benjamini_hochberg(p_values, alpha=0.05) -> MultipleTestingResult` — sort ascending, multiplier `K/j`, REVERSE cummin, clip to 1.0.

`MultipleTestingResult` fields: `p_values_raw`, `p_values_adjusted`, `rejected`, `alpha`, `method`, `n_tests`. Adjusted p-values returned in CALLER'S input order, not sorted.

Test file: `tests/test_multiple_testing.py`, 25 tests covering: structural (frozen dataclass, metadata), per-method known-example numerics, monotonicity-in-sorted-order, cross-method power ordering (BH ⊇ Holm ⊇ Bonferroni at the same alpha for same data), input-order preservation, pandas/list/array acceptance, K=1 passthrough, validation (empty, NaN, out-of-range, bad alpha, 2D).

Expected test count after 1.13: 249.

## 14. Phase 1.10–1.13 Specific Notes

- PSR (1.10), DSR (1.10), MinTRL (1.11) live in `quantcore/validation/deflated_sharpe.py`. Symbols: `PSRResult`, `DSRResult`, `MinTRLResult`, `probabilistic_sharpe_ratio`, `deflated_sharpe_ratio`, `min_track_record_length`, `min_track_record_length_from_returns`, `expected_max_sharpe`.
- White's Reality Check (1.12) lives in `quantcore/validation/reality_check.py`. Symbols: `RealityCheckResult`, `whites_reality_check`.
- Multiple-testing (1.13) lives in `quantcore/validation/multiple_testing.py`. Symbols: `MultipleTestingResult`, `bonferroni_correction`, `holm_correction`, `benjamini_hochberg`.
- PSR formula: `Phi( (SR_hat - SR*) * sqrt(n - 1) / sqrt(1 - skew*SR_hat + (kurt/4)*SR_hat^2) )` where `kurt` is EXCESS kurtosis and SRs are PER-PERIOD.
- DSR deflates the benchmark by `expected_max_sharpe(n_trials, sr_variance)`. When `n_trials == 1` or `sr_variance == 0`, deflation is exactly 0 and DSR == PSR.
- MinTRL formula: `n_min = 1 + (1 - skew*SR + (kurt/4)*SR^2) * (z / (SR - SR*))^2` with `z = Φ⁻¹(confidence)`. `ceil`-rounded. Infeasible iff `SR - SR* <= 1e-12`.
- White's Reality Check: stationary bootstrap, default block length `round(T^(1/3))`. Recenter each strategy by subtracting its own observed mean excess. Sample row-indices ONCE per bootstrap rep and apply to all K columns. Test statistic `sqrt(T) * max_k(d_k)`. p-value = fraction of reps with bootstrap statistic >= observed.
- Multiple-testing: all three corrections share `MultipleTestingResult`. Adjusted p-values let callers re-threshold without recomputing. `rejected = adjusted <= alpha` for all three methods. Power ordering at fixed alpha: BH ⊇ Holm ⊇ Bonferroni (BH rejects everything Holm does, Holm rejects everything Bonferroni does).

## 15. After Phase 1.14: Phase 1 closes. Next is Phase 2.

Phase 2 is H017 strategy logic: H016's two-asset (USDJPY + XAUUSD) trend-following with ATR stops + chandelier exits + vol-targeted sizing, PLUS the portfolio heat governor that caps simultaneous open risk and applies correlation-adjusted position sizing. This is where the validation framework gets used in anger. Phase 2 is NOT just "write a strategy" — it's "write a strategy and gate every claim about it through the Validator." Expect roughly:

- 2.1 Indicator helpers (ATR, chandelier, vol target).
- 2.2 Per-symbol signal generators (deterministic, NOT ML — see graveyard H006/H007).
- 2.3 Heat governor (open-risk accountant + correlation-adjusted sizing).
- 2.4 Strategy-level integration (H017 = H016 + heat governor).
- 2.5 Validator-gated backtest claim (PSR + MinTRL + DSR vs the H001-H016 baseline pool).

Don't pre-write Phase 2. Confirm Phase 1.14 lands first, run a final 249-test smoke, commit, push, and only then propose Phase 2.1.