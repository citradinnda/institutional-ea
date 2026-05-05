# HANDOFF 54 - After H020 Strict Validation Success

If any older handoff conflicts with this file, this HANDOFF_54 wins.

This handoff is intentionally self-contained. It contains the complete project rules, the strategy graveyard, and the precise state of the H020 sizing hypothesis so a new AI can continue safely.

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
- Python: 3.12.10 inside `.venv`
- No WSL

Repository root:
- `C:\Users\equin\Documents\institutional-ea`
Virtual environment:
- `C:\Users\equin\Documents\institutional-ea\.venv`
Branch:
- `main`

## Human Preference & Workflow Rules

The user is tired of excessive documentation and slow ceremony.

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do not use Linux/macOS heredoc syntax (`<<'EOF'`). Use PowerShell here-strings (`@'` or `@"`) or standard file editing.
- Do not create governance docs unless they preserve a real decision or prevent ambiguity.
- Do one real action at a time.
- For code changes, tests are mandatory.
- If full tests pass but the count drops below the anchor without an explicit test-removal phase, treat it as a regression.
- Always read `git status` before starting a new phase.
- Never write code without saying exactly where the file goes and how to run it.

Current full-test anchor after H020 strict validation:
- `605 passed`

## Data And Source Acceptance Rules

Broker:
- Exness demo MT5

Accepted validation source:
- Broker-native Exness demo MT5 exports only.
- Symbols: `USDJPY` and `XAUUSD` (Exported as `USDJPYm` / `XAUUSDm`)
- Timeframes: Broker-native H4 and M1
- Broker timezone used by loader: `Europe/Athens`

Accepted strict bridge-window contract:
- First common complete H4/M1 bridge window UTC: `2021-07-02 13:00:00+00:00`
- Last common complete H4/M1 bridge window UTC: `2026-04-30 01:00:00+00:00`
- Accepted common complete H4/M1 windows: `5476`

A common complete window means both symbols have an H4 bar, the next H4 bar is exactly 4 hours later, and there are exactly 240 M1 bars inside that window.

Strict Rules:
- Do not commit raw data. Root `.gitignore` must keep root-anchored `/data/`.
- Do not modify raw broker files.
- Do not use HistData for H017/H018/H019/H020 validation.
- Do not impute, forward-fill, backfill, or synthesize M1 bars.

## Strategy Graveyard Summary

To understand H020, you must understand why previous iterations failed.

- H001-H010: Proved that backtests without intrabar SL/TP simulation are fiction. ML on basic technicals cannot be a risk manager.
- H011-H016: Added Deterministic ATR stops, Chandelier exits, and vol-targeted sizing. Showed edge on USDJPY, but 1% per-trade risk was not 1% portfolio risk when trades overlapped.
- H017: Added a portfolio heat governor. Failed strict expanded broker-native event validation by insolvency before guards, then failed closed under H018-style guards.
- H018: Diagnostic work only. Revealed massive structural strategy/execution mismatches (specifically, stale held signals hitting stop lifecycles).
- H019: Stateful Donchian/Chandelier lifecycle. It fixed the stale-stop mismatch but failed closed on the H018 `10.0x` maximum per-trade leverage guard when stop distances were too tight.

## Current Strategy: H020 (Sizing Contract)

H020 is a sizing-contract hypothesis built on H019's lifecycle semantics (Donchian entry, stateful Chandelier exit).

### The H020 Mechanics
Instead of relying purely on a signed risk fraction, H020 uses an explicit pre-trade sizing contract:
1. Calculates risk-based lots from equity, stop distance, and contract size.
2. Hard-caps per-trade lots to a `9.0x` strategy gross leverage limit.
3. Hard-caps combined portfolio lots to a `9.0x` strategy gross leverage limit.
4. explicitly suppresses (returns flat) if stop geometry is invalid, stop distance is below spread, or scaled lots fall below broker `min_lot`.

### The Bridge Shim
To pass H020 through the strict H018 event engine without rewriting dynamic compounding mechanics, we built `quantcore/strategy/h020_runner.py`. 
This shim evaluates the intents at a nominal $10,000 equity and reverse-engineers them into a universally safe `final_signed_risk_fraction`. Since gross leverage is mathematically independent of equity, this serves as a safe routing contract.

### The Milestone
H020 successfully passed the strict broker-native event validation (`scripts/run_h020_strict_event_real.py`). It mathematically capped leverage and navigated 5476 strict windows without a single guard violation. 

Current verdicts:
- H020 passed strict event-driven validation.
- H020 is NOT yet promotable. Performance (Edge, Drawdown) is currently UNKNOWN.
- No live trading is approved. Phase 4 is not approved.

## Important Paths

H020 Code:
- `quantcore\strategy\h020.py`
- `quantcore\strategy\h020_runner.py`
- `quantcore\backtest\h020_strict_event.py`

H020 Scripts:
- `scripts\scan_h020_sizing_diagnostics_real.py`
- `scripts\run_h020_strict_event_real.py`

Tests:
- `tests\test_h020.py`
- `tests\test_h020_runner.py`
- `tests\test_h020_strict_event.py`
- `tests\test_h020_strict_event_real_script.py`
- `tests\test_h020_sizing_diagnostics_real_script.py`

## Recommended Next Engineering Action

Now that H020 survives the strict timeline validation without guard violations, we need to determine if it actually makes money.

**Next step: Build a performance diagnostic script for H020.**
- Run the validated H020 strict event pipeline.
- Extract the final equity, equity curve, max drawdown, and Sharpe ratio.
- Keep this lightweight to confirm whether the strategy has an edge before investing in deeper tearsheet generation.

## Absolute Do-Not Rules

- Do not live trade.
- Do not approve Phase 4.
- Do not weaken H018 guards.
- Do not raise the 10x hard guard casually.
- Do not use HistData.
- Do not let full test count drop below `605`.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. Continuing after HANDOFF_54.

I understand:
- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Current branch should be `main`.
- Current full-test anchor is `605 passed`.
- H019 is in the graveyard; it failed strict leverage guards.
- H020 is a sizing-contract hypothesis using a 9.0x leverage cap and explicit lot-suppression logic.
- H020 successfully passed strict broker-native event validation across 5476 complete windows without a single guard violation via the `h020_runner.py` bridge shim.
- H020's performance (edge, equity curve, drawdown) is currently unknown.
- Live trading is not approved. Phase 4 is not approved.
- Next step is building an H020 performance diagnostic script to evaluate the edge.

Please run:
    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Then paste the full output. After hygiene passes, I will help build the H020 performance diagnostic script.
