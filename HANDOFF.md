# Project Handoff — Institutional-Grade MT5 EA on Retail Stack

You are continuing an existing project. Read this entire document before responding. Do not invent context that isn't here. When in doubt, ask the user before writing code.

## 1. Identity and Tone

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows. The user is intelligent but is **not** a professional developer. They have already burned through 16 dead strategies (documented graveyard, see §6) and are now building infrastructure-first instead of strategy-first.

Communication rules:
- Step-by-step. Numbered steps. Explicit file paths.
- Plain English explanations of every concept, no jargon dumps.
- Never write code without telling the user where the file goes and how to run it.
- After each sub-phase, give the user three response options: ✅ done, ⚠️ error (paste it), 🤔 question.
- Never skip git commits. Commit after every working sub-phase.
- If the user reports passing tests but the *count* of tests dropped, treat it as a regression and investigate.
- The user is on **Windows + PowerShell + VS Code + Python 3.14 in a `.venv`**. No WSL, no Linux assumptions.

## 2. Project Goal

Build a USDJPY + XAUUSD MT5 expert advisor that has **institutional-grade epistemology** even though the infrastructure is retail (Kaggle for research, MT5 for execution, Oracle Cloud Always Free VPS for production).

The user's full requirements list spans 7 pillars (Scientific Validity, Alpha Quality, Execution & Microstructure, Risk Management, Production Infrastructure, Organizational & Governance, Continuous Improvement). The plan is delivered in **8 phases**:

- **Phase 0** — Foundation (repo, CI, DVC, MLflow). *Partially done — tooling installed, MLflow/DVC deferred.*
- **Phase 1** — Research Framework (the `quantcore` Python package). **IN PROGRESS.**
- **Phase 2** — H017 Strategy Logic (carry forward from H016 + portfolio heat governor).
- **Phase 3** — Realistic event-driven backtest engine with intrabar M1 fills.
- **Phase 4** — MT5 EA shell + Python decision service (thin EA, fat Python via MetaTrader5 lib).
- **Phase 5** — Free-tier VPS deployment (Oracle Cloud Always Free, Wine + MT5, Docker).
- **Phase 6** — Monitoring (Prometheus + Grafana + Loki + Telegram alerts).
- **Phase 7** — Governance & continuous improvement.

The user understands what cannot be done on this stack (true colocation, GIPS audit, multi-region hot failover, third-party pen testing) — and what *can* be matched in epistemology (pre-registration, DSR/PSR/CPCV, deterministic risk, model+data hashing, append-only graveyard).

## 3. Repo Layout (Windows path: `C:\Users\<user>\Documents\institutional-ea`)
institutional-ea/
├── .venv/ # virtual environment (gitignored)
├── .gitignore
├── pyproject.toml # project config, deps include numpy, pandas, scipy,
│ # scikit-learn, lightgbm, pyarrow, pyyaml, matplotlib,
│ # tqdm; dev deps: pytest, pytest-cov, hypothesis,
│ # ruff, black. Python ≥3.11 required.
├── README.md
├── ea_mt5/ # (empty — Phase 4)
├── governance/
│ └── hypotheses/ # YAML hypothesis pre-registrations (Phase 1.x)
├── ops/ # (empty — Phase 5/6)
├── quantcore/ # the package under construction
│ ├── init.py
│ ├── data/
│ │ ├── init.py
│ │ ├── loaders.py # ✅ Phase 1.1
│ │ ├── reconcile.py # ✅ Phase 1.2
│ │ └── outliers.py # ✅ Phase 1.3
│ ├── governance/init.py
│ ├── utils/init.py
│ └── validation/init.py
├── research/ # (empty — Kaggle notebooks go here)
└── tests/
├── init.py
├── test_loaders.py
├── test_reconcile.py
├── test_outliers.py
└── test_smoke.py

text

## 4. Phase 1 Sub-Phase Status

Phase 1 has 14 sub-phases. Progress:

| # | Name | Status |
|---|---|---|
| 1.0 | Project skeleton, venv, pyproject, pre-commit, smoke test | ✅ Done |
| 1.1 | Data loaders (canonical OHLCV, parquet, HistData CSV, resample) | ✅ Done |
| 1.2 | Cross-vendor reconciliation (ATR-scaled tolerance) | ✅ Done |
| 1.3 | Outlier detection (MAD z-score) | ✅ Done |
| 1.4 | **Checksums** (file SHA-256 + DataFrame SHA-256) | ⬅️ NEXT |
| 1.5 | Lookahead guard (run feature_fn on truncated data, assert past values invariant) |  |
| 1.6 | Performance metrics + block-bootstrap CIs (Sharpe, Sortino, Calmar, profit factor, tail ratio, max DD, stationary bootstrap) |  |
| 1.7 | Purged K-Fold with embargo |  |
| 1.8 | Combinatorial Purged Cross-Validation (CPCV) + path assembly |  |
| 1.9 | Walk-forward (rolling/anchored) |  |
| 1.10 | Probabilistic Sharpe + Deflated Sharpe |  |
| 1.11 | Minimum Track Record Length |  |
| 1.12 | White's Reality Check (bootstrap, recentered) |  |
| 1.13 | Multiple testing correction (Bonferroni, Holm, Benjamini-Hochberg) |  |
| 1.14 | Validator orchestrator (single `Validator.run()` returns gate report) |  |

**Test count after Phase 1.3: 31 passing.** (3 smoke + 9 loaders + 9 reconcile + 10 outliers.)

## 5. Conventions Already Established

- **Canonical OHLCV format:** lowercase columns `open, high, low, close, volume`, UTC `DatetimeIndex`, no duplicates, sorted ascending. Enforced by `_ensure_canonical()` in `quantcore/data/loaders.py`.
- **MT5 bar labeling:** `label="left", closed="left"` in resample. The bar's timestamp is its OPEN time.
- **Tolerance comparisons in ATR units**, not absolute price (so the same code works for EURUSD and XAUUSD).
- **Flag, never auto-delete** outliers. Researcher decides.
- **Tests live only in `tests/`. Production code lives only in `quantcore/`. Never mix.**
- **Test count is a coverage signal.** If `pytest` collects fewer items after a change, treat it as a regression.

## 6. Strategy Graveyard (immutable history — H001 through H016)

The user has 16 killed hypotheses. Key lessons distilled:

- **H001:** Backtest without intrabar SL/TP simulation is fiction. → must use M1 within H4 bars to resolve fills.
- **H002–H003:** ATR-based per-symbol stops mandatory; reduce trade frequency to amortize costs.
- **H004a:** Single-seed models unreliable → **multi-seed ensembles**.
- **H005:** Stacked multi-symbol models fail on heterogeneous instruments → **per-symbol models**.
- **H006–H007:** Confidence filters ≠ risk management. ML chooses entries; deterministic rules manage risk.
- **H008–H010:** High Sharpe with kurtosis 38 is unsafe. ML on basic technicals can't be the risk manager.
- **H011–H013:** Deterministic ATR stops + chandelier exits + vol-targeted sizing = real edge on USDJPY. Single-asset has a tail-risk ceiling.
- **H014–H016:** Two-asset USDJPY + XAUUSD reduces kurtosis to 1.69, Sortino 4.69, but **1% per-trade risk does not equal 1% portfolio risk** when trades overlap → drawdown breached at -19.43%.
- **H015:** Diversification into negative-edge instruments destroys the portfolio. Unit-scale bugs are real.

**H017** (the next live candidate) = H016 + a portfolio heat governor that caps simultaneous open risk + correlation-adjusted sizing.

## 7. Handoff Rules to the New AI

1. **Do not rewrite already-completed code.** It exists, it's tested, leave it alone unless the user asks.
2. **Continue from sub-phase 1.4 (Checksums).** That is the next deliverable.
3. **Always produce one sub-phase per response**, never the whole rest of the phase at once.
4. **Always include:** explicit Windows file paths, full code blocks, exact test count expected, a `git commit` line, and the three-options ending (✅ / ⚠️ / 🤔).
5. **Do not assume institutional infrastructure.** Free-tier only: Kaggle for compute, Oracle Cloud Always Free for VPS, Telegram for alerting.
6. **Never break tests.** If the test count would drop, refuse and ask first.
7. **Match prior code style:** type hints, dataclasses for structured returns, `from __future__ import annotations` at top of every file, docstrings explaining *why*, not just *what*.
8. When the user says "continue," produce the next sub-phase.

## 8. Current State at Handoff

- All 31 tests passing.
- Last commit message: "Phase 1.3: MAD-based outlier flagging for OHLCV bars"
- User is ready for **Phase 1.4 — Checksums**.
- After Phase 1 completes, ask the user before starting Phase 2: H017 logic requires choices about heat governor parameters that should be discussed.

## 9. First Reply From New AI Should Be

A short acknowledgement (3-5 sentences) confirming:
- You understand the user's stack (Windows, .venv, VS Code).
- You understand 31 tests are passing and the next deliverable is Phase 1.4 Checksums.
- You will continue with the same step-by-step format.
- One question: ask the user to confirm which Python version their `.venv` is on (currently 3.14.4) so dependency advice is correct.

Then wait for the user to confirm before producing Phase 1.4 code.