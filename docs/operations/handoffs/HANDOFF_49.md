# HANDOFF 49 - After H018 Guard Scanner And Invalid-Stop Cause Diagnostic

If any older handoff conflicts with this file, this HANDOFF_49 wins.

## Current Repo State

Repository:

- `C:\Users\equin\Documents\institutional-ea`

Branch:

- `main`

Latest pushed commit:

- `11b27df Add H018 invalid stop cause diagnostic`

Recent important commits:

- `11b27df Add H018 invalid stop cause diagnostic`
- `51d6042 Add H018 guard violation diagnostic scanner`
- `33e4fff Add handoff document #48 after friction diagnostic calculator`
- `adb5fab Add diagnostic projected friction calculator`

Working tree should be clean and up to date with `origin/main`.

Current full-test anchor:

- `575 passed`

Last full pytest result:

- `575 passed in 12.94s`

## Human Preference

The user is tired of excessive documentation and process drag.

Do not create governance/docs unless needed.

Proceed with direct engineering actions, but keep safety constraints:

- start with `git status`;
- code changes require focused tests and full `python -m pytest -q`;
- docs-only changes do not require full pytest;
- commit and push completed work;
- do not continue while local commits are unpushed.

## Environment

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 in `.venv`
- No WSL

Do not use Linux heredoc syntax like `python - <<'PY'`.

## Validation / Trading Status

H017 remains:

- failed
- not promotable
- not live-approved

H018 remains:

- not validated
- not promotable
- not live-approved

Do not:

- live trade
- start Phase 4 execution
- tune H017 casually
- add ML
- broaden symbols
- use HistData
- modify raw broker files
- commit raw data
- change `.gitignore` from `/data/` to `data/`

Accepted real-data source remains:

- Exness demo MT5 broker-native exports only
- USDJPY + XAUUSD
- H4 + M1
- strict complete bridge windows only

Accepted strict bridge-window facts:

- `accepted_count=5476`
- first accepted timestamp: `2021-07-02 13:00:00+00:00`
- last accepted timestamp: `2026-04-30 01:00:00+00:00`
- expected M1 bars per H4: `240`
- expected H4 delta: `4h`

## Work Completed After HANDOFF_48

### 1. Strict H018 broker-native validation was explicitly authorized and run

Command used:

- `python .\scripts\run_h017_strict_event_real.py`

Preflight passed exactly.

Validation failed closed with:

- `H017EventInvalidStopError`
- first failure:
  - symbol: `XAUUSD`
  - side: `sell`
  - decision_time: `2021-07-05 17:00:00+00:00`
  - entry_time: `2021-07-05 21:00:00+00:00`
  - entry_raw_price: `1791.212000000`
  - stop_price: `1786.180536020`

For a sell, stop must be above entry. It was below entry.

Classification:

- not a data preflight failure
- not infrastructure failure
- strategy/event validation failure
- H018 not validated

### 2. H018 guard violation diagnostic scanner added

Commit:

- `51d6042 Add H018 guard violation diagnostic scanner`

Files:

- `quantcore/backtest/h018_guard_scan.py`
- `scripts/scan_h018_guard_violations_real.py`
- `tests/test_h018_guard_scan.py`

Purpose:

- diagnostic-only scan across accepted strict windows
- counts guard failures without pretending validation passed
- does not execute fills for promotion
- does not tune, skip, clip, resize, or approve anything

Focused tests:

- `5 passed`

Full tests after this step:

- `571 passed in 13.13s`

Real diagnostic result:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=10952`
- `candidate_count=8275`
- `skipped_intent_count=560`
- `violation_count=2271`

Violation breakdown:

- `invalid_directional_stop`: `1545`
- `maximum_per_trade_usd_gross_leverage`: `527`
- `minimum_stop_distance`: `45`
- `maximum_portfolio_usd_gross_leverage`: `154`

By symbol:

- `XAUUSD`: `874`
- `USDJPY`: `1243`

Interpretation:

- structural issue, not isolated
- H017/H018 current form invalid under strict event execution

### 3. H018 invalid-stop cause diagnostic added

Commit:

- `11b27df Add H018 invalid stop cause diagnostic`

Files:

- `quantcore/backtest/h018_invalid_stop_cause.py`
- `scripts/diagnose_h018_invalid_stop_causes_real.py`
- `tests/test_h018_invalid_stop_cause.py`

Purpose:

Determine whether invalid stops are caused by:

1. stop valid at decision close but crossed by next executable entry open, or
2. stop already invalid at decision close.

Focused tests:

- `4 passed`

Full tests after this step:

- `575 passed in 12.94s`

Real diagnostic result:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=10952`
- `invalid_at_entry_count=1545`

Cause breakdown:

- `already_invalid_at_decision_close`: `1544`
- `crossed_between_decision_close_and_entry_open`: `1`

By symbol:

- `XAUUSD`: `726`
- `USDJPY`: `819`

By side:

- `sell`: `788`
- `buy`: `757`

Interpretation:

This is decisive.

The invalid-stop problem is not mainly next-open gap/crossing.

Almost all invalid stops were already on the wrong side at the decision close itself.

Likely problem class:

- H017 stop/position state mismatch
- stop panel selected for active side may be incompatible with current signal/position state
- strategy may be using Chandelier long/short stop levels while position sign can persist or flip in a way that makes selected protective stop nonsensical
- investigate strategy logic, not execution timing

Do not tune parameters yet.

## Current Diagnostic Scripts

Guard scanner:

```powershell
python .\scripts\scan_h018_guard_violations_real.py
Invalid-stop cause diagnostic:

powershell
python .\scripts\diagnose_h018_invalid_stop_causes_real.py
Strict validation script:

powershell
python .\scripts\run_h017_strict_event_real.py
Do not rerun strict validation as a promotion attempt. It is known to fail closed.

Recommended Next Action
Proceed directly to inspect H017 stop/position generation.

Goal:

Answer why H017 emits positions whose selected stop is already on the wrong side at decision close.

Start with read-only inspection of:

quantcore/strategy/h017.py
quantcore/strategy/signals.py
any chandelier/ATR logic used by H017
Look for:

how positions are derived from signals;
how stops_long and stops_short are computed;
whether long positions always use a stop below decision close;
whether short positions always use a stop above decision close;
whether stop side selection is mismatched to signal sign;
whether positions persist while signal/stop side changes;
whether stop panels are raw Chandelier bands, not actual protective stops for active position state.
Next useful diagnostic, if needed:

count invalid-at-decision stops against H017 signal sign and raw stop panels:
position sign
signal sign
stops_long
stops_short
decision close
whether each panel is directionally valid
do this before changing strategy behavior.
First Action For Next AI
Start with:

powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -8
Expected:

branch main
up to date with origin/main
working tree clean
latest commit 11b27df Add H018 invalid stop cause diagnostic
previous commit 51d6042 Add H018 guard violation diagnostic scanner
Then proceed with read-only inspection of H017 strategy stop/position logic.

No handoff/test/documentation ceremony beyond what is necessary.
