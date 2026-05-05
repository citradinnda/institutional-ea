# HANDOFF 53 - After H020 Sizing Intent Contract Seed

If any older handoff conflicts with this file, this HANDOFF_53 wins.

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
- Python: 3.12.10 inside `.venv`
- No WSL

Repository root:

- `C:\Users\equin\Documents\institutional-ea`

Virtual environment:

- `C:\Users\equin\Documents\institutional-ea\.venv`

Branch:

- `main`

GitHub remote:

- `https://github.com/citradinnda/institutional-ea.git`

Handoff folder:

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs`

This handoff path:

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_53.md`

## Human Preference

The user is tired of excessive documentation and slow ceremony.

Going forward:

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do not create governance docs unless they preserve a real decision, preserve a handoff, prevent ambiguity, or protect against future confusion.
- Do one real action at a time.
- For docs-only changes, do not run full pytest unless there is a clear reason.
- For code changes, tests are mandatory.
- For code touching strategy, event engine, sizing, accounting, data loading, validation, or diagnostics:
  - run focused tests if applicable,
  - run full `python -m pytest -q`,
  - compare test count to anchor,
  - commit,
  - push.

Current full-test anchor after H020 sizing intent code:

- `600 passed`

If full tests pass but count drops below `600` without an explicit test-removal phase, treat it as a regression.

Do not continue development while local commits are unpushed.

Always read `git status` before starting a new phase.

## Non-Negotiable Environment Rules

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
- No WSL

PowerShell rule:

Do not use Linux/macOS heredoc syntax like:

- `python - <<'PY'`

PowerShell does not support that.

Use PowerShell here-strings or normal file editing.

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Expected after this handoff is committed and pushed:

- On branch `main`
- Branch up to date with `origin/main`
- Nothing to commit, working tree clean
- Latest commit should be `Add handoff document #53 after H020 sizing intent`
- Previous important commit should be `Add H020 sizing intent contract`

Do not require pytest for this first check unless code has changed or status is not clean.

## Recent Expected Commits

Recent expected commits include:

- `Add handoff document #53 after H020 sizing intent`
- `Add H020 sizing intent contract`
- `Fix H020 sizing contract formatting`
- `Lock H020 sizing contract`
- `Record H019 guard severity diagnostics`
- `Add guard diagnostic severity fields`
- `Record H019 guard diagnostic for H020`
- `Add H019 guard diagnostic scanner`
- `Expand handoff document #52 after H019 failure`
- `Document H019 failure and seed H020`

## Current Test Anchor

Latest full test result before this handoff:

- `600 passed in 13.31s`

This was after adding:

- `quantcore/strategy/h020.py`
- `tests/test_h020.py`

Focused H020 test result:

- `8 passed in 1.57s`

If full test count drops below `600` without planned test removal, stop.

## Important Paths

Code:

- `quantcore`
- `scripts`
- `tests`

Strategy files:

- `quantcore\strategy\h017.py`
- `quantcore\strategy\h019.py`
- `quantcore\strategy\h020.py`
- `quantcore\strategy\signals.py`
- `quantcore\strategy\heat_governor.py`

H020 files:

- `quantcore\strategy\h020.py`
- `tests\test_h020.py`

H019 files:

- `quantcore\strategy\h019.py`
- `quantcore\backtest\h019_strict_event.py`
- `scripts\run_h019_strict_event_real.py`
- `scripts\scan_h019_guard_violations_real.py`
- `tests\test_h019.py`
- `tests\test_h019_strict_event.py`
- `tests\test_h019_strict_event_real_script.py`
- `tests\test_h019_guard_scan_real_script.py`

Guard scanner:

- `quantcore\backtest\h018_guard_scan.py`
- `scripts\scan_h018_guard_violations_real.py`
- `scripts\scan_h019_guard_violations_real.py`
- `tests\test_h018_guard_scan.py`

Docs:

- `docs\operations\H019_GRAVEYARD_RECORD.md`
- `docs\operations\H020_HYPOTHESIS_SEED.md`
- `docs\operations\handoffs\HANDOFF_53.md`

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

Local raw files exist and are gitignored:

- `data\raw\USDJPY\H4.csv`
- `data\raw\USDJPY\M1.csv`
- `data\raw\XAUUSD\H4.csv`
- `data\raw\XAUUSD\M1.csv`

Reported exact MT5 symbols:

- `USDJPYm`
- `XAUUSDm`

Broker timezone used by loader:

- `Europe/Athens`

Accepted strict bridge-window contract:

- First common complete H4/M1 bridge window UTC: `2021-07-02 13:00:00+00:00`
- Last common complete H4/M1 bridge window UTC: `2026-04-30 01:00:00+00:00`
- Accepted common complete H4/M1 windows: `5476`

Do not commit raw data.

Do not modify raw broker files.

Do not use HistData for H017/H018/H019/H020 validation.

Do not use incomplete windows.

Do not impute, forward-fill, backfill, or synthesize M1 bars.

Root `.gitignore` must keep root-anchored:

- `/data/`

Do not change it to unanchored:

- `data/`

Reason: unanchored `data/` can accidentally exclude `quantcore/data`.

## Strategy Status

Current verdicts:

- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 failed and is in the graveyard.
- H020 is now partially implemented as a sizing-intent contract seed.
- H020 is not validated.
- H020 is not promotable.
- No live trading is approved.
- Phase 4 execution is not approved.

## H019 Summary

H019 was created to fix the stale-held-signal versus stop-lifecycle mismatch.

H019 identity:

- Donchian entry/flip trigger.
- Same-side Chandelier lifecycle exit.
- Flat after same-side stop breach.
- No stale held-signal re-entry after stop-out.
- No opposite-panel switching.
- H018 guards remain strict.

H019 strict broker-native validation:

- Strict bridge preflight passed with `5476` accepted complete windows.
- Validation failed closed on `H018MaximumPerTradeLeverageError`.

First H019 failure:

- symbol: `USDJPY`
- side: `buy`
- decision_time: `2021-07-05 21:00:00+00:00`
- entry_time: `2021-07-06 01:00:00+00:00`
- entry_raw_price: `110.840000000`
- stop_price: `110.741028558`
- raw_stop_distance: `0.098971442`
- equity_usd: `9872.94`
- lots: `1.20`
- notional_usd: `120000.000000000`
- gross_leverage: `12.154432565`
- max allowed: `10.000000000`

Interpretation:

- Not a data-preflight failure.
- Not infrastructure failure.
- H018 leverage guard behaved correctly.
- H019 is not validated or promotable.

## H019/H020 Guard Diagnostic Result

A diagnostic scanner was added:

- `scripts\scan_h019_guard_violations_real.py`
- `tests\test_h019_guard_scan_real_script.py`

It reuses:

- `quantcore.backtest.h018_guard_scan.scan_h018_guard_violations`

but routes an H019-shaped `H017Result` through the scanner.

Real diagnostic command run:

    python .\scripts\scan_h019_guard_violations_real.py

Diagnostic-only. Not validation.

Strict bridge-window preflight passed:

- `accepted_entry_count=5476`
- `first_accepted_timestamp=2021-07-02 13:00:00+00:00`
- `last_accepted_timestamp=2026-04-30 01:00:00+00:00`

Diagnostic summary:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=5736`
- `candidate_count=5052`
- `skipped_intent_count=424`
- `violation_count=302`

Violation counts by guard:

- `maximum_per_trade_usd_gross_leverage`: `239`
- `invalid_directional_stop`: `2`
- `minimum_stop_distance`: `19`
- `maximum_portfolio_usd_gross_leverage`: `42`

Violation counts by symbol:

- `USDJPY`: `205`
- `XAUUSD`: `55`

Portfolio-wide violations are symbolless, so symbol totals exclude `42`.

Violation counts by side:

- `buy`: `155`
- `sell`: `105`

Portfolio-wide violations are sideless.

Severity diagnostics:

Per-trade gross leverage violations:

- count: `239`
- min: `10.090896`
- median: `15.700000`
- p95: `79.820000`
- max: `429.700000`

Portfolio gross leverage violations:

- count: `42`
- min: `10.062785`
- median: `11.205005`
- p95: `15.568125`
- max: `16.938916`

Minimum stop-distance ratio violations, measured as raw stop distance divided by minimum modeled spread:

- count: `19`
- min: `0.114372`
- median: `0.571525`
- p95: `0.951577`
- max: `0.960424`

Interpretation:

- H019 materially fixed stale stop lifecycle mismatch.
- Prior H018 invalid directional stops: `1545`.
- H019 invalid directional stops: `2`.
- Remaining blocker is sizing/leverage.
- Per-trade cap alone is insufficient because portfolio overlap can still breach the hard guard.
- H020 must include both per-trade and portfolio gross notional constraints.
- H020 must explicitly handle minimum stop-distance and residual invalid-stop cases.

## H020 Sizing Contract Decision

H020 is a sizing-contract hypothesis, not lifecycle repair.

H020 keeps:

- H019 Donchian entry/flip plus stateful same-side Chandelier lifecycle semantics.
- Same-side Chandelier stops.
- H018 hard validation guards.
- Strict broker-native complete-window validation requirements.

H020 must not weaken event-engine guards.

### Pre-Trade Suppression

Before sizing a candidate trade, H020 checks intended raw-entry stop geometry.

If same-side stop is non-protective at intended raw entry:

- long/buy stop is not below raw entry, or
- short/sell stop is not above raw entry,

then H020 emits flat/no lot intent for that symbol.

If raw stop distance is below one modeled spread for the symbol, H020 emits flat/no lot intent.

This is strategy-level intent suppression.

It is not:

- event-engine silent skipping,
- event-engine clipping,
- validation pass-through,
- guard weakening.

Event engine must still fail closed if hard guard violations reach validation.

### Risk-Based Lots

For each valid candidate trade, H020 first computes risk-based lots from:

- equity,
- signed risk fraction,
- raw entry price,
- same-side stop distance,
- contract size,
- quote currency conversion,
- lot step,
- minimum lot.

### Per-Trade Notional Cap

H020 computes max per-trade lots from strategy-level USD gross notional cap.

Decision:

- H020 strategy per-trade cap: `9.0x` equity.
- H018 hard guard remains `10.0x`.

For each candidate:

- `candidate_lots = min(risk_based_lots, per_trade_notional_cap_lots)`

Lots are rounded down to lot step.

If rounded lots fall below minimum lot, H020 emits flat/no lot intent.

### Portfolio Gross Notional Cap

H020 enforces portfolio-wide strategy-level USD gross notional cap before validation.

Decision:

- H020 strategy portfolio cap: `9.0x` equity.
- H018 hard portfolio guard remains `10.0x`.

If combined candidate USD gross notional exceeds cap:

- scale all active candidate lots down proportionally,
- round down to lot step,
- recompute notionals after rounding,
- emit flat/no lot intent for any symbol whose rounded lots fall below minimum lot.

Long and short notionals are summed gross, not netted.

### Representation

H020 should not pretend signed risk fraction alone is enough.

H020 outputs should make visible:

- raw risk-based lots,
- per-trade-cap lots,
- portfolio-scaled lots,
- final emitted lots,
- whether symbol was suppressed,
- suppression reason,
- raw stop distance,
- per-trade gross leverage estimate,
- portfolio gross leverage estimate.

Strict event bridge may need to be extended to consume explicit lots safely.

If a temporary bridge shim converts final lots back into risk-fraction-shaped output, it must be tested and documented as a bridge shim, not H020 strategy truth.

## H020 Code Implemented In This Session

New file:

- `quantcore\strategy\h020.py`

New tests:

- `tests\test_h020.py`

Focused tests passed:

- `8 passed in 1.57s`

Full tests passed:

- `600 passed in 13.31s`

### Implemented H020 Types

In `quantcore.strategy.h020`:

- `H020SizingConfig`
- `H020SymbolSizingIntent`
- `H020IntervalSizingResult`
- `size_h020_interval_intents(...)`

`H020SizingConfig` defaults:

- `per_trade_max_gross_leverage = 9.0`
- `portfolio_max_gross_leverage = 9.0`

`H020SymbolSizingIntent` fields:

- `symbol`
- `side`
- `signed_risk_fraction`
- `entry_raw_price`
- `stop_price`
- `raw_stop_distance`
- `risk_based_lots`
- `per_trade_cap_lots`
- `pre_portfolio_lots`
- `final_lots`
- `final_signed_risk_fraction`
- `notional_usd`
- `gross_leverage`
- `suppressed`
- `suppression_reason`

`H020IntervalSizingResult` fields:

- `decision_time`
- `entry_time`
- `equity_usd`
- `intents`
- `portfolio_notional_usd`
- `portfolio_gross_leverage`
- `portfolio_scaled`

### Implemented H020 Behavior

`size_h020_interval_intents(...)`:

- rejects non-positive equity,
- rejects non-positive caps,
- handles flat signals as suppressed with reason `flat_signal`,
- suppresses non-protective same-side stop geometry with reason `invalid_stop_geometry`,
- suppresses below-spread raw stop distance with reason `minimum_stop_distance`,
- computes risk-based lots using existing `size_position_from_risk`,
- computes per-trade max-notional lots using `9.0x` default cap,
- emits `min(risk_based_lots, per_trade_cap_lots)`,
- rounds down to broker lot step,
- suppresses below-min-lot result after per-trade cap with reason `below_min_lot_after_per_trade_cap`,
- applies portfolio gross-notional proportional scale when combined active notional exceeds `9.0x`,
- rounds down after portfolio scale,
- suppresses below-min-lot result after portfolio scale with reason `below_min_lot_after_portfolio_scale`,
- computes final signed risk fraction from final lots and actual stop risk,
- computes USD notional and gross leverage.

### H020 Tests Added

`tests\test_h020.py` covers:

- flat-signal suppression,
- invalid stop geometry suppression,
- below-spread stop-distance suppression,
- per-trade lot cap below hard guard,
- portfolio gross notional scaling after per-trade caps,
- final signed risk fraction from final lots,
- non-positive equity rejection,
- non-positive cap rejection.

## Important Caveat About H020 Current State

H020 currently implements only standalone interval sizing intent.

It does not yet:

- run H019 lifecycle end-to-end,
- produce a full panel of H020 intents,
- integrate with strict event bridge,
- run H020 guard diagnostic,
- run strict H020 broker-native validation.

H020 is still not validated or promotable.

## Recommended Next Engineering Action

Do not run real H020 validation yet.

Next code step should likely be one of:

1. Build H020 panel-level sizing over an H019 result:
   - iterate decision/entry intervals,
   - use H019 positions as starting signed risk budget,
   - use H4 next-open raw entry prices,
   - use same-side stops,
   - output explicit H020 intent panels/diagnostics.

2. Or build a strict event bridge extension that can consume explicit H020 lot intents safely.

Recommended safer order:

- First build H020 panel-level sizing diagnostics with synthetic tests.
- Then build H020 guard scanner using explicit intents.
- Only after diagnostics show zero hard guard violations should strict validation be considered.
- Do not run strict H020 broker-native validation without explicit user authorization.

## Absolute Do-Not Rules

Do not:

- Do not live trade.
- Do not approve Phase 4.
- Do not treat diagnostics as validation.
- Do not weaken H018 guards.
- Do not raise 10x hard guard casually.
- Do not silently clip lots in event engine.
- Do not silently skip violating trades in event engine.
- Do not treat H020 strategy suppression as validation skipping.
- Do not use HistData.
- Do not commit raw MT5 CSV files.
- Do not modify raw broker files.
- Do not use incomplete H4/M1 windows.
- Do not impute, forward-fill, backfill, or synthesize bars.
- Do not broaden symbols.
- Do not add ML.
- Do not tune parameters casually.
- Do not change cost model casually.
- Do not change broker specs casually.
- Do not continue if local commits are unpushed.
- Do not let full test count drop below `600` without explicit test-removal intent.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. Continuing after HANDOFF_53.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Current branch should be `main`.
- Latest expected commit should be `Add handoff document #53 after H020 sizing intent`.
- Current full-test anchor is `600 passed`.
- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 failed and is in the graveyard.
- H019 fixed most stale-stop lifecycle issues but failed strict validation on leverage.
- H019/H020 diagnostic showed `302` remaining H019 guard violations, dominated by `239` per-trade leverage violations and `42` portfolio leverage violations.
- H020 sizing contract is locked: 9x strategy per-trade cap, 9x strategy portfolio cap, flat/no intent for invalid stop geometry or below-spread stop distance.
- H020 currently has standalone interval sizing intent code in `quantcore/strategy/h020.py` with tests in `tests/test_h020.py`.
- H020 is not validated, not promotable, and live trading is not approved.
- Next likely step is H020 panel-level sizing diagnostics with synthetic tests, not real validation.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Then paste the full output.

After hygiene passes, I will help continue H020 panel-level sizing diagnostics before any strict real-data validation.
