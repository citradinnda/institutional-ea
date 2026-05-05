# HANDOFF 54 - After H020 Strict Validation Success

If any older handoff conflicts with this file, this HANDOFF_54 wins.

This handoff is intentionally self-contained enough for a new AI to continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:
- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is research/backtest infrastructure, not execution.
- No live trading is approved.
- Phase 4 execution is not approved.

Environment:
- OS: Windows
- Shell: PowerShell
- Editor: VS Code
- Python: 3.12.10 inside .venv
- No WSL

Repository root:
- C:\Users\equin\Documents\institutional-ea

Virtual environment:
- C:\Users\equin\Documents\institutional-ea\.venv

Branch:
- main

GitHub remote:
- https://github.com/citradinnda/institutional-ea.git

Handoff path:
- C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_54.md

## Human Preference

The user is tired of excessive documentation and slow ceremony.

Going forward:
- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do not create governance docs unless they preserve a real decision, prevent ambiguity, or protect a handoff.
- Do one real action at a time.
- For code changes, tests are mandatory.
- For code touching strategy, event engine, sizing, accounting, data loading, validation, or diagnostics:
  - run focused tests if applicable
  - run full python -m pytest -q
  - compare test count to anchor
  - commit
  - push

Current full-test anchor after H020 strict validation:
- 605 passed

If full tests pass but count drops below 605 without an explicit test-removal phase, treat it as a regression. Always read git status before starting a new phase.

## Non-Negotiable Environment Rules

Use Windows, PowerShell, VS Code, Python 3.12.10, and .venv.
Do not use Linux/macOS heredoc syntax (<<'EOF'). Use PowerShell here-strings (@").

## Immediate First Action For The Next AI

Do not write code first. Start with hygiene verification:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Expected after this handoff is committed and pushed:
- On branch main
- Branch up to date with origin/main
- Nothing to commit, working tree clean
- Latest commit should be Add handoff document #54 after H020 validation success

## Data And Source Rules

Broker:
- Exness demo MT5

Accepted validation source:
- Broker-native Exness demo MT5 exports only.

Accepted symbols:
- USDJPY
- XAUUSD

Accepted timeframes:
- Broker-native H4
- Broker-native M1

Broker timezone used by loader:
- Europe/Athens

Accepted strict bridge-window contract:
- First common complete H4/M1 bridge window UTC: 2021-07-02 13:00:00+00:00
- Last common complete H4/M1 bridge window UTC: 2026-04-30 01:00:00+00:00
- Accepted common complete H4/M1 windows: 5476

Do not commit raw data. Do not use HistData for H017/H018/H019/H020 validation. Do not impute, forward-fill, backfill, or synthesize M1 bars. Root .gitignore must keep root-anchored /data/.

## Strategy Status

Current verdicts:
- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 failed and is in the graveyard (failed leverage guard).
- **H020 passed strict event-driven validation.**
- H020 is NOT yet promotable (performance/edge is unknown).
- No live trading is approved.
- Phase 4 execution is not approved.

## H020 Milestone: Strict Validation Passed

H020 is a sizing-contract hypothesis built on H019 lifecycle semantics. 
It features explicit pre-trade sizing intents:
- 9.0x strategy per-trade gross leverage cap.
- 9.0x strategy portfolio gross leverage cap.
- Explicit flat/no-intent suppression for invalid stop geometry or below-spread stop distance.

### The Bridge Shim
To pipe H020 through the strict H018 event engine without rewriting dynamic compounding mechanics, we built a **bridge shim** (quantcore/strategy/h020_runner.py). The shim evaluates intents at a nominal $10,000 equity and reverse-engineers them into a inal_signed_risk_fraction. Since gross leverage is mathematically independent of equity, this serves as a universally safe routing contract that the existing strict event engine consumes naturally.

### Results
- scripts/scan_h020_sizing_diagnostics_real.py mathematically proved that max per-trade and portfolio gross leverage were hard-capped at exactly 9.000000, well below the 10.0 hard guard limit. 454 intents were explicitly suppressed to avoid structural or micro-lot violations.
- scripts/run_h020_strict_event_real.py was executed. Strict bridge preflight passed with 5476 accepted complete windows. The validation ran to completion **without a single guard violation**.

## Important Paths

H020 core code:
- quantcore\strategy\h020.py
- quantcore\strategy\h020_runner.py (Bridge Shim)
- quantcore\backtest\h020_strict_event.py

H020 execution scripts:
- scripts\scan_h020_sizing_diagnostics_real.py
- scripts\run_h020_strict_event_real.py

H020 tests:
- 	ests\test_h020.py
- 	ests\test_h020_runner.py
- 	ests\test_h020_strict_event.py
- 	ests\test_h020_strict_event_real_script.py
- 	ests\test_h020_sizing_diagnostics_real_script.py

## Recommended Next Engineering Action

Now that H020 survives the strict timeline validation, we need to determine if it actually has an edge.

**Next step: Build a performance diagnostic script for H020.**
- Run the validated H020 strict event pipeline.
- Extract the final equity, equity curve, max drawdown, and Sharpe ratio.
- Keep this lightweight to confirm whether the strategy makes money before investing in deeper tearsheet generation.

## Absolute Do-Not Rules

Do not:
- Do not live trade.
- Do not approve Phase 4.
- Do not weaken H018 guards.
- Do not use HistData.
- Do not commit raw MT5 CSV files.
- Do not modify raw broker files.
- Do not let full test count drop below 605 without explicit test-removal intent.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. Continuing after HANDOFF_54.

I understand:
- Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
- Current branch should be main.
- Current full-test anchor is 605 passed.
- H020 successfully passed strict broker-native event validation.
- The H020 sizing contract correctly capped gross leverage at 9.0x and safely filtered invalid stop geometries.
- Live trading is not approved. Phase 4 is not approved.
- Next likely step is building an H020 performance diagnostic script to evaluate edge, drawdown, and Sharpe ratio.

Please run:
    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Then paste the full output. After hygiene passes, I will help build the H020 performance diagnostic script.
