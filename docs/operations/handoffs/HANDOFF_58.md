# HANDOFF 58 - After H021 Positive Bucket Temporal Stability Diagnostic

If any older handoff conflicts with this file, this HANDOFF_58 wins.

This handoff is intentionally self-contained so a new AI can continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is research/backtest infrastructure and strategy hypothesis work.
- No execution approval.
- No live trading approval.
- No Phase 4 approval.

Environment:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 inside `.venv`
- No WSL

Repository root:

- `C:\Users\equin\Documents\institutional-ea`

Virtual environment:

- `C:\Users\equin\Documents\institutional-ea\.venv`

Branch:

- `main`

GitHub remote:

- `https://github.com/citradinnda/institutional-ea.git`

Handoff path:

- `docs\operations\handoffs\HANDOFF_58.md`

## Human Preference

The user is tired of excessive documentation and slow ceremony.

Going forward:

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do not create governance docs unless they preserve a real decision, preserve a handoff, prevent ambiguity, or protect against future confusion.
- Do not create subphases inside subphases.
- Do one real action at a time.
- Prefer direct engineering actions over process theater.
- For docs-only changes, do not run full pytest unless there is a clear reason.
- For code changes, tests are mandatory.

Latest preference:

- The user decided not to update `HYPOTHESIS_LEDGER.md`, `H021_HYPOTHESIS_SEED.md`, or create `H021_GRAVEYARD_RECORD.md` right now.
- Preserve the H021 temporal stability result in this handoff.
- Summarize diagnostic outputs in handoffs instead of pasting full long console tables.

## Non-Negotiable Environment Rules

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10
- `.venv`
- No WSL

Do not use Linux/macOS heredoc syntax such as:

- `python - <<'PY'`

PowerShell does not support that.

Use PowerShell here-strings or normal files only.

## Practical Workflow Rules

General:

1. Start each phase with `git status`.
2. Do one real action at a time.
3. Use explicit Windows paths.
4. Never continue while local commits are unpushed.
5. Always commit and push completed work.
6. Always verify touched files are tracked with `git ls-files` after commit.
7. Do not run real-data validation unless explicitly authorized.
8. Do not start Phase 4 execution unless explicitly authorized.
9. Do not live trade.

Testing:

- Docs-only edit:
  - No full pytest required by default.
  - Use `git diff --check` and `git diff --stat`.
- Code edit:
  - Run focused tests.
  - Run full `python -m pytest -q`.
  - Current full-test anchor: `639 passed`.
- If full tests pass but count drops below `639` without explicit planned test removal, stop and treat as regression.

Git after changes:

- `git diff --check`
- `git diff --stat`
- `git add touched files`
- `git commit`
- `git push`
- `git status`
- `git ls-files touched files`

## Immediate First Action For The Next AI

Do not write code first.

Start with hygiene verification:

- `cd C:\Users\equin\Documents\institutional-ea`
- `.\.venv\Scripts\Activate.ps1`
- `git status`
- `git log --oneline -10`

Expected after this handoff is committed and pushed:

- branch `main`
- up to date with `origin/main`
- working tree clean

Expected latest commit after this handoff:

- `Add handoff document #58 after H021 stability diagnostic`

Recent previous commits should include:

- `4156c34 Add H021 positive bucket stability diagnostic`
- `3cc49e2 Add handoff document #57 after H021 positive bucket search`
- `1b7b55b Add H021 positive bucket search diagnostic`
- `b446f31 Add handoff document #56 after H021 exclusion diagnostics`
- `3c69015 Add H021 candidate exclusion diagnostic`
- `9080eb1 Add H021 stop precursor diagnostic`
- `705ddd3 Add handoff document #55 after H021 decomposition diagnostic`
- `0282cf9 Add H021 trade decomposition diagnostic`
- `2f7e32a Add H021 hypothesis seed`
- `57812f7 Record H020 performance failure`

Do not require pytest for this first check unless code has changed or status is not clean.

## Current Test Anchor

Current full-test anchor after H021 positive bucket temporal stability diagnostic code:

- `639 passed in 22.33s`

Recent anchors:

- after H021 positive bucket temporal stability diagnostic: `639 passed`
- after H021 positive bucket search diagnostic: `633 passed`
- after H021 candidate exclusion diagnostic: `623 passed`
- after H021 stop precursor diagnostic: `616 passed`
- after H021 trade decomposition diagnostic: `611 passed`
- after H020 performance diagnostic script: `607 passed`
- after H020 strict validation work: `605 passed`
- after H020 sizing-intent seed: `600 passed`

If full test count drops below `639` without planned test removal, treat it as a regression.

## Important Current Commits

Newest important commits before this handoff:

- `4156c34 Add H021 positive bucket stability diagnostic`
- `3cc49e2 Add handoff document #57 after H021 positive bucket search`
- `1b7b55b Add H021 positive bucket search diagnostic`
- `b446f31 Add handoff document #56 after H021 exclusion diagnostics`
- `3c69015 Add H021 candidate exclusion diagnostic`
- `9080eb1 Add H021 stop precursor diagnostic`
- `705ddd3 Add handoff document #55 after H021 decomposition diagnostic`
- `0282cf9 Add H021 trade decomposition diagnostic`
- `2f7e32a Add H021 hypothesis seed`
- `57812f7 Record H020 performance failure`

HANDOFF_58 is authoritative and supersedes older handoffs where conflicts exist.

## Important Paths

H020 scripts:

- `scripts\scan_h020_sizing_diagnostics_real.py`
- `scripts\run_h020_strict_event_real.py`
- `scripts\diagnose_h020_performance_real.py`

H021 scripts:

- `scripts\diagnose_h021_trade_decomposition_real.py`
- `scripts\diagnose_h021_stop_precursors_real.py`
- `scripts\diagnose_h021_candidate_exclusions_real.py`
- `scripts\diagnose_h021_positive_bucket_search_real.py`
- `scripts\diagnose_h021_positive_bucket_stability_real.py`

H020/H021 tests:

- `tests\test_h020.py`
- `tests\test_h020_runner.py`
- `tests\test_h020_sizing_diagnostics_real_script.py`
- `tests\test_h020_strict_event.py`
- `tests\test_h020_strict_event_real_script.py`
- `tests\test_h020_performance_real_script.py`
- `tests\test_h021_trade_decomposition_real_script.py`
- `tests\test_h021_stop_precursors_real_script.py`
- `tests\test_h021_candidate_exclusions_real_script.py`
- `tests\test_h021_positive_bucket_search_real_script.py`
- `tests\test_h021_positive_bucket_stability_real_script.py`

Important docs:

- `docs\operations\H019_GRAVEYARD_RECORD.md`
- `docs\operations\H020_HYPOTHESIS_SEED.md`
- `docs\operations\H020_GRAVEYARD_RECORD.md`
- `docs\operations\H021_HYPOTHESIS_SEED.md`
- `docs\operations\HYPOTHESIS_LEDGER.md`
- `docs\operations\handoffs\HANDOFF_58.md`

Important latest docs note:

- Do not assume `H021_GRAVEYARD_RECORD.md` exists.
- Do not assume `H021_HYPOTHESIS_SEED.md` or `HYPOTHESIS_LEDGER.md` contains the temporal stability result.
- The temporal stability result is preserved here instead.

## Data And Source Rules

Accepted source for strict validation/diagnostics:

- Exness demo MT5 broker-native exports only.

Accepted symbols:

- USDJPY
- XAUUSD

Accepted timeframes:

- Broker-native H4
- Broker-native M1

Broker timezone used by loader:

- Europe/Athens
- DST-aware

Accepted strict bridge-window range:

- first common complete H4/M1 bridge window UTC: `2021-07-02 13:00:00+00:00`
- last common complete H4/M1 bridge window UTC: `2026-04-30 01:00:00+00:00`
- accepted bridge-window count: `5476`

A common complete H4/M1 bridge window means:

- USDJPY has a broker-native H4 bar at the H4 timestamp.
- XAUUSD has a broker-native H4 bar at the same H4 timestamp.
- For each symbol, the next H4 timestamp is exactly four hours later.
- For each symbol, the M1 window has exactly 240 M1 bars.
- No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

Do not use:

- HistData for validation/tuning/production dataset creation.
- Broker H4 plus HistData M1 combinations.
- Sparse 2018 through 2021-06 broker-native prefix as dense M1.
- Incomplete H4/M1 windows.

Do not commit:

- raw MT5 CSV files,
- raw HistData files,
- large derived datasets,
- broker/vendor source files.

The repo uses root-anchored `/data/` in `.gitignore`.

Do not change it to unanchored `data/`, because that previously risked excluding `quantcore/data/`.

## Core Backtest Conventions

ATR:

- Wilder RMA, not SMA.
- First true range is high - low.
- Seed at index window - 1 with simple mean of first window true ranges.
- Recurrence: `ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n`.

Chandelier Exit:

- Long: highest_high(lookback) - multiplier * ATR.
- Short: lowest_low(lookback) + multiplier * ATR.
- Current rolling windows include the current bar.
- Defaults: multiplier `3.0`, lookback `22`.

Donchian Signals:

- Long: `close[t] > max(high[t-N ... t-1])`.
- Short: `close[t] < min(low[t-N ... t-1])`.
- Channel uses prior N bars via `shift(1).rolling(N)`.

Event bridge timing:

- Strategy decides at H4 timestamp `t`.
- Trade opens on next H4 bar open `t+1`.
- M1 bars inside next H4 window resolve stops.
- If no stop is hit, exposure closes at following H4 open as `signal_flip`.
- This is a bridge-layer simplification.

Fill rule:

- If stop and take-profit are both touched in the same M1 bar, stop wins.
- Reason: M1 OHLC does not reveal tick order inside the minute.

Cost model defaults:

USDJPY:

- spread_price `0.01`
- commission_usd_per_lot_per_fill `7.0`
- stop_slippage_atr_fraction `0.05`

XAUUSD:

- spread_price `0.30`
- commission_usd_per_lot_per_fill `10.0`
- stop_slippage_atr_fraction `0.05`

Commission is per fill. A round trip charges entry and exit.

Portfolio P&L:

- XAUUSD P&L is already USD.
- USDJPY P&L is JPY and must be divided by USDJPY conversion price to become USD.

## H018 Hard Guards

H018 guards remain hard validation guards. Do not weaken them.

Implemented in:

- `quantcore\backtest\h017_event.py`

Invalid stop geometry:

- Long/buy stop must be below raw H4 entry open.
- Short/sell stop must be above raw H4 entry open.
- Equality is invalid.
- Invalid directional stop geometry fails closed.

Minimum stop distance:

- `raw_stop_distance = abs(raw_h4_entry_open - stop_price)`
- Minimum is one modeled spread:
  - USDJPY `0.01`
  - XAUUSD `0.30`
- Below threshold fails closed.
- Equality passes.

Maximum per-trade USD gross leverage:

- Hard max `10.0x`
- `< 10.0` passes
- `== 10.0` passes
- `> 10.0` fails closed

Maximum portfolio-wide USD gross leverage:

- Hard max `10.0x`
- Long and short exposures are summed gross, not netted.
- `< 10.0` passes
- `== 10.0` passes
- `> 10.0` fails closed

Violation policy:

- Raise explicit error.
- Do not silently skip trades.
- Do not clip position size.
- Do not net long and short notionals.
- Do not warn/log-only and continue.

## Hypothesis Status Summary

- H017 failed.
- H018 is guard/diagnostic work only; not a validated strategy.
- H019 failed and is in the graveyard.
- H020 survived strict guard validation but failed performance badly.
- H021 is diagnostics-first research.
- H021 positive bucket leads failed temporal stability.
- No strategy is currently promotable.
- No live trading is approved.
- Phase 4 is not approved.

## H020 Summary

H020 was a sizing-contract hypothesis on top of H019 lifecycle semantics.

H020 mechanics:

- invalid stop geometry becomes flat/no intent at strategy-intent level,
- below-spread raw stop distance becomes flat/no intent,
- per-trade strategy cap = `9.0x` gross notional,
- portfolio strategy cap = `9.0x` gross notional,
- H018 hard guards remain `10.0x` and unchanged,
- explicit intent objects preserve diagnostics,
- bridge shim converts H020 intent back into H017Result-shaped positions for strict event bridge compatibility.

H020 strict guard validation:

- command: `python .\scripts\run_h020_strict_event_real.py`
- accepted bridge-windows: `5476`
- completed without guard violations.

H020 performance diagnostic:

- command: `python .\scripts\diagnose_h020_performance_real.py`
- accepted_entry_count: `5476`
- executed_entry_count: `5476`
- skipped_entry_count: `3176`
- fill_count: `4158`
- starting_equity_usd: `\$10000.00`
- ending_equity_usd: `\$819.07`
- total_pnl_usd: `-\$9180.93`
- total_return: `-91.8093%`
- max_drawdown: `-91.8860%`
- win_rate: `44.1799%`
- gross_profit_usd: `\$28703.99`
- gross_loss_usd: `-\$37884.92`
- profit_factor: `0.757663`
- fill_return_sharpe: `-0.086278`

Verdict:

- H020 failed performance evaluation.
- H020 is not promotable.
- H020 is not live-approved.
- Phase 4 is not approved.

## H021 Diagnostic 1 - Trade Decomposition

Script:

- `scripts\diagnose_h021_trade_decomposition_real.py`

Commit:

- `0282cf9 Add H021 trade decomposition diagnostic`

Real result summary:

By symbol:

- USDJPY:
  - fills `2827`
  - total_pnl_usd `-7259.73`
  - profit_factor `0.722826`
- XAUUSD:
  - fills `1331`
  - total_pnl_usd `-1921.21`
  - profit_factor `0.835695`

By side:

- Buy:
  - fills `2497`
  - total_pnl_usd `-5224.34`
  - profit_factor `0.766060`
- Sell:
  - fills `1661`
  - total_pnl_usd `-3956.60`
  - profit_factor `0.745606`

By exit reason:

- Signal flip:
  - fills `3678`
  - win_rate `49.9456%`
  - total_pnl_usd `+9503.32`
  - profit_factor `1.494947`
- Stop:
  - fills `480`
  - win_rate `0.0000%`
  - total_pnl_usd `-18684.26`
  - profit_factor `0.000000`

Interpretation:

- H020 losses are not because all trades are bad.
- Signal-flip exits are profitable in aggregate.
- Stop exits are deeply destructive.
- Do not remove stops; stops are structural risk controls.
- The real H021 question became whether likely future stop-outs can be identified before entry using only decision-time information.

## H021 Diagnostic 2 - Stop-Loss Precursors

Script:

- `scripts\diagnose_h021_stop_precursors_real.py`

Commit:

- `9080eb1 Add H021 stop precursor diagnostic`

Real result summary:

- accepted bridge-windows `5476`
- context rows reconstructed `5282`
- fill rows enriched `4158`

Important decision-hour damage:

- decision_hour_utc `05`: fills `585`, stops `117`, stop_rate `20.0000%`, PnL `-2621.09`, PF `0.715453`
- decision_hour_utc `10`: fills `303`, stops `33`, stop_rate `10.8911%`, PnL `-1092.41`, PF `0.601259`
- decision_hour_utc `22`: fills `297`, stops `31`, stop_rate `10.4377%`, PnL `-1025.01`, PF `0.463573`

Stop-distance/spread bucket result:

- `<2x`: stop_rate `94.1176%`, PnL `-217.79`, PF `0.004211`
- `2-5x`: stop_rate `75.0000%`, PnL `-208.99`, PF `0.663358`
- `5-10x`: stop_rate `64.1975%`, PnL `-79.02`, PF `0.952525`
- `10-20x`: stop_rate `47.5248%`, PnL `-1664.75`, PF `0.621684`
- `20-50x`: stop_rate `17.2932%`, PnL `-4018.88`, PF `0.738456`
- `>=50x`: stop_rate `3.7037%`, PnL `-2991.50`, PF `0.808415`

Estimated gross leverage bucket result:

- `<1x`: fills `2934`, stop_rate `7.0893%`, PnL `-3208.78`, PF `0.768747`
- `1-3x`: fills `942`, stop_rate `19.8514%`, PnL `-1771.23`, PF `0.866350`
- `3-6x`: fills `227`, stop_rate `25.9912%`, PnL `-1675.21`, PF `0.752770`
- `6-9x`: fills `55`, stop_rate `47.2727%`, PnL `-2525.70`, PF `0.365494`

Interpretation:

- Stop-outs are meaningfully concentrated.
- Tight stops and high estimated gross leverage are dangerous.
- Wide stops alone do not create profitability; `>=50x` stop-distance still lost `-2991.50`.

## H021 Diagnostic 3 - Candidate Exclusions

Script:

- `scripts\diagnose_h021_candidate_exclusions_real.py`

Commit:

- `3c69015 Add H021 candidate exclusion diagnostic`

Baseline:

- fills `4158`
- stops `480`
- stop_rate `11.5440%`
- total_pnl_usd `-9180.93`
- profit_factor `0.757663`

Best/simple exclusion results:

- Exclude USDJPY all:
  - retained_fills `1331`
  - retained_pnl_usd `-1921.21`
  - retained_profit_factor `0.835695`
- Keep only stop_distance_spread_bucket `>=50x`:
  - retained_fills `2754`
  - retained_pnl_usd `-2991.50`
  - retained_profit_factor `0.808415`
- Exclude decision hours `05`, `10`, `22`:
  - retained_fills `2973`
  - retained_pnl_usd `-4442.42`
  - retained_profit_factor `0.815076`
- Exclude estimated gross leverage `>=3x`:
  - retained_fills `3876`
  - retained_pnl_usd `-4980.02`
  - retained_profit_factor `0.816428`
- Exclude USDJPY sell:
  - retained_fills `3092`
  - retained_pnl_usd `-5543.25`
  - retained_profit_factor `0.796264`

Interpretation:

- Simple exclusions improve losses but do not reveal a profitable retained core.
- Best retained set was XAUUSD only, still negative at `-1921.21`, PF `0.835695`.
- Do not implement a strategy from these exclusion candidates.

## H021 Diagnostic 4 - Positive Bucket Search

Script:

- `scripts\diagnose_h021_positive_bucket_search_real.py`

Commit:

- `1b7b55b Add H021 positive bucket search diagnostic`

Tests:

- focused new tests `10 passed`
- broader H021 focused tests `26 passed`
- full suite `633 passed in 20.30s`

Real result summary:

- accepted bridge-windows `5476`
- context rows reconstructed `5282`
- fill rows enriched `4158`

The diagnostic scanned decision-time observable groups at minimum fill thresholds:

- `>=30`
- `>=50`
- `>=100`

Important in-sample positive bucket leads:

- XAUUSD, stop_distance_spread_bucket `5-10x`:
  - fills `44`
  - stops `20`
  - total_pnl_usd `+639.699759`
  - median_pnl_usd `-7.652802`
  - profit_factor `1.784845`
- XAUUSD sell, decision_hour_utc `01`:
  - fills `94`
  - stops `9`
  - total_pnl_usd `+386.014161`
  - median_pnl_usd `-0.922500`
  - profit_factor `1.732129`
- XAUUSD buy, decision_hour_utc `18`:
  - fills `67`
  - stops `6`
  - total_pnl_usd `+135.666425`
  - median_pnl_usd `+0.948000`
  - profit_factor `1.363435`
- USDJPY sell, decision_hour_utc `06`:
  - fills `100`
  - stops `18`
  - total_pnl_usd `+331.990603`
  - median_pnl_usd `+0.018233`
  - profit_factor `1.281885`
- XAUUSD, decision_hour_utc `17`:
  - fills `146`
  - stops `16`
  - total_pnl_usd `+133.556329`
  - median_pnl_usd `+0.493500`
  - profit_factor `1.151079`
- XAUUSD sell, decision_hour_utc `05`:
  - fills `103`
  - stops `24`
  - total_pnl_usd `+157.742462`
  - median_pnl_usd `-2.620000`
  - profit_factor `1.121236`
- USDJPY buy, decision_hour_utc `01`:
  - fills `253`
  - stops `14`
  - total_pnl_usd `+80.258698`
  - median_pnl_usd `-0.371867`
  - profit_factor `1.040025`
- USDJPY, stop_distance_spread_bucket `>=50x`, estimated_gross_leverage_bucket `1-3x`:
  - fills `434`
  - stops `20`
  - total_pnl_usd `+39.241651`
  - median_pnl_usd `-0.818062`
  - profit_factor `1.008218`

Interpretation:

- Positive decision-time observable buckets exist in-sample.
- These are leads only, not a strategy.
- Many are time-of-day/session artifacts or barely above PF 1.0.
- Temporal stability testing was required before strategy implementation.

## H021 Diagnostic 5 - Positive Bucket Temporal Stability

Script:

- `scripts\diagnose_h021_positive_bucket_stability_real.py`

Tests:

- `tests\test_h021_positive_bucket_stability_real_script.py`

Commit:

- `4156c34 Add H021 positive bucket stability diagnostic`

Tests before commit:

- focused stability tests: `6 passed in 2.88s`
- full suite: `639 passed in 22.33s`

Real command run with explicit user authorization:

- `python .\scripts\diagnose_h021_positive_bucket_stability_real.py`

Real diagnostic setup/result:

- accepted bridge-windows `5476`
- context rows reconstructed `5282`
- fill rows enriched `4158`

Temporal stability result by bucket:

1. USDJPY sell, decision_hour_utc `06`

- overall: fills `100`, stops `18`, PnL `+331.990603`, PF `1.281885`
- first half: PF `1.249592`, PnL `+252.801911`
- second half: PF `1.480255`, PnL `+79.188692`
- losing years:
  - 2021: PF `0.522801`, PnL `-200.228210`
  - 2023: PF `0.470507`, PnL `-113.145685`
  - 2024: PF `0.576388`, PnL `-63.023143`
  - 2026: PF `0.230742`, PnL `-40.117536`
- interpretation: overall positive but calendar-year unstable.

2. XAUUSD sell, decision_hour_utc `01`

- overall: fills `94`, stops `9`, PnL `+386.014161`, PF `1.732129`
- first half: PF `2.596061`, PnL `+416.032839`
- second half: PF `0.887396`, PnL `-30.018678`
- losing years:
  - 2023: PF `0.653475`, PnL `-43.738642`
  - 2024: PF `0.196587`, PnL `-53.267502`
- interpretation: strongest overall PF, but second half turns negative.

3. XAUUSD buy, decision_hour_utc `18`

- overall: fills `67`, stops `6`, PnL `+135.666425`, PF `1.363435`
- first half: PF `1.638984`, PnL `+135.189497`
- second half: PF `1.002949`, PnL `+0.476928`
- losing years:
  - 2022: PF `0.939794`, PnL `-11.485503`
  - 2024: PF `0.899460`, PnL `-10.129191`
  - 2025: PF `0.000000`, PnL `-4.185000`
- interpretation: later period is effectively flat and yearly stability is weak.

4. XAUUSD, decision_hour_utc `17`

- overall: fills `146`, stops `16`, PnL `+133.556329`, PF `1.151079`
- first half: PF `1.266678`, PnL `+151.466344`
- second half: PF `0.943330`, PnL `-17.910014`
- losing years:
  - 2021: PF `0.792673`, PnL `-54.160932`
  - 2024: PF `0.420282`, PnL `-69.889253`
  - 2025: PF `0.838304`, PnL `-3.287900`
- interpretation: overall positive but second half negative.

5. XAUUSD sell, decision_hour_utc `05`

- overall: fills `103`, stops `24`, PnL `+157.742462`, PF `1.121236`
- first half: PF `1.308118`, PnL `+241.157401`
- second half: PF `0.839104`, PnL `-83.414939`
- losing years:
  - 2022: PF `0.665629`, PnL `-172.380793`
  - 2023: PF `0.945927`, PnL `-12.988954`
  - 2024: PF `0.013354`, PnL `-121.248126`
- interpretation: not stable; later period negative.

6. XAUUSD, decision_hour_utc `06`

- overall: fills `143`, stops `29`, PnL `+197.086724`, PF `1.124625`
- first half: PF `0.869371`, PnL `-141.126188`
- second half: PF `1.674976`, PnL `+338.212912`
- losing years:
  - 2021: PF `0.659380`, PnL `-100.709309`
  - 2025: PF `0.110509`, PnL `-46.965944`
- nearly flat year:
  - 2022: PF `1.001718`, PnL `+1.154962`
- interpretation: regime-dependent; not stable enough.

7. USDJPY buy, decision_hour_utc `01`

- overall: fills `253`, stops `14`, PnL `+80.258698`, PF `1.040025`
- first half: PF `1.326516`, PnL `+420.109856`
- second half: PF `0.527051`, PnL `-339.851158`
- losing years:
  - 2023: PF `0.932337`, PnL `-37.925949`
  - 2024: PF `0.449447`, PnL `-189.415106`
  - 2025: PF `0.805930`, PnL `-19.972024`
  - 2026: PF `0.000238`, PnL `-37.175271`
- interpretation: barely positive overall and strongly negative in the second half.

8. USDJPY, stop_distance_spread_bucket `>=50x`, estimated_gross_leverage_bucket `1-3x`

- overall: fills `434`, stops `20`, PnL `+39.241651`, PF `1.008218`
- first half: PF `1.181857`, PnL `+476.831118`
- second half: PF `0.796748`, PnL `-437.589467`
- losing years:
  - 2023: PF `0.875222`, PnL `-204.350631`
  - 2024: PF `0.755236`, PnL `-253.423280`
- interpretation: barely positive overall and negative in the second half.

Overall temporal stability verdict:

- No tested positive bucket passed a practical temporal-stability smell test.
- Positive buckets look like in-sample/session/regime artifacts, not stable positive expectancy.
- A bucket with one or two good periods and several losing periods is not stable.
- PF near 1.0 with unstable splits is likely noise.
- Do not implement trading rules from these buckets.
- Do not promote H020 or H021.
- No live trading is approved.
- Phase 4 is not approved.

## Current H021 Research State

What is known:

- H020 survived strict event guard validation but failed catastrophically on performance.
- H021 decomposition found that signal-flip exits are profitable in aggregate and stop exits are destructive.
- Stop-outs concentrate by tight stop distance, high estimated gross leverage, decision hour, and symbol.
- Simple exclusions improve losses but retain negative expectancy.
- Positive in-sample decision-time buckets exist.
- The tested positive buckets failed temporal stability checks.

Current conclusion:

- H021 positive-bucket-lead path is not promotable under current evidence.
- No H021 strategy has been implemented.
- No H021 strategy is validated.
- No live trading is approved.
- Phase 4 is not approved.

Recommended next action:

- Pause before adding more diagnostics.
- If continuing H021, choose a genuinely new diagnostic angle rather than tuning the unstable positive buckets.
- Potential future diagnostic angles, only if explicitly authorized:
  - compare stop-hit candidates against pre-entry volatility expansion/compression,
  - analyze whether signal-flip winners have common decision-time precursors,
  - test walk-forward pre-registration discipline before any rule is implemented,
  - evaluate whether the H4 one-bar hold/signal-flip bridge simplification is structurally distorting exits.
- Do not implement a strategy directly from the positive bucket search or temporal stability results.

## Absolute Do-Not Rules

Do not:

- live trade,
- approve Phase 4,
- treat H020 guard-validation success as profitability,
- treat H021 positive buckets as a validated strategy,
- implement a strategy directly from in-sample positive buckets,
- revive H020 by casually tuning caps,
- weaken H018 hard guards,
- raise hard leverage limits casually,
- lower modeled costs casually,
- switch stop panels casually,
- remove stops casually,
- broaden symbols,
- add ML,
- use HistData,
- combine broker H4 with HistData M1,
- use sparse 2018 through 2021-06 broker-native prefix as dense M1,
- include incomplete H4/M1 windows,
- impute M1 bars,
- forward-fill or backfill M1 bars,
- synthesize bars,
- modify raw broker files,
- commit raw MT5 CSV files,
- change `.gitignore` from `/data/` to `data/`,
- continue development while local commits are unpushed,
- allow full-test count to drop below `639` without explicit test-removal intent.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

- `.gitignore` once had unrooted `data/`, which risked excluding `quantcore/data`.
- Some older commits missed files because `git add` was incomplete.
- An empty handoff file was accidentally committed once.
- Markdown code fences have been damaged by paste before.
- PowerShell does not support Linux heredocs.
- VS Code can keep unsaved buffers that overwrite edits.
- If terminal output shows command echo ambiguity, verify with `Select-String` or file previews before proceeding.
- Always inspect `git status`.
- Always push commits.
- Always verify `git ls-files` after commits.
- Treat code test-count drops as regressions.
- If terminal output is too large to paste, rerun a compact read-only diagnostic rather than continuing blindly.
- Network/DNS push failures can happen; stop development until `git push` succeeds.

## Exact First Response The Next AI Should Give

Understood. Continuing after HANDOFF_58.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Current branch should be `main`.
- Current full-test anchor is `639 passed`.
- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 failed and is in the graveyard.
- H020 survived strict event guard validation but failed performance badly:
  - ending equity `\$819.07`
  - total return `-91.8093%`
  - max drawdown `-91.8860%`
  - profit factor `0.757663`
- H020 is in the graveyard.
- H021 is diagnostics-first research, not a strategy.
- H021 decomposition showed:
  - signal_flip exits made `+\$9503.32`
  - stop exits lost `-\$18684.26`
- H021 stop precursor diagnostics showed stop-outs concentrate by tight stop distance, high estimated gross leverage, and certain decision hours.
- H021 candidate exclusion diagnostics showed simple exclusions improve losses but do not reveal a profitable core.
- H021 positive bucket search found in-sample positive decision-time buckets.
- H021 temporal stability diagnostic showed those positive bucket leads are not stable enough across time.
- No H021 strategy is validated.
- No live trading is approved.
- Phase 4 is not approved.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.

After hygiene passes, I will continue only with an explicitly authorized next research action.
