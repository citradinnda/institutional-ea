# HANDOFF 55 - After H020 Graveyard And H021 First Decomposition Diagnostic

If any older handoff conflicts with this file, this HANDOFF_55 wins.

This handoff is intentionally self-contained so a new AI can continue safely without reading older handoffs first.

## Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

- Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.
- Current stage is research/backtest infrastructure and strategy hypothesis work.
- No execution approval.
- No live trading approval.
- No Phase 4 approval.

Target environment:

- Research: Python package `quantcore`
- Execution target later: MetaTrader 5 expert advisor
- Production target later: Oracle Cloud Always Free VPS
- Monitoring later: self-hosted free-tier stack

Current machine:

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

Handoff folder:

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs`

This handoff path:

- `C:\Users\equin\Documents\institutional-ea\docs\operations\handoffs\HANDOFF_55.md`

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

Use PowerShell here-strings only when useful. For long docs, VS Code manual editing is acceptable.

## Practical Workflow Rules

General:

1. Start each phase with `git status`.
2. Do one real action at a time.
3. Use explicit Windows paths.
4. Use plain English.
5. Define technical terms inline when needed.
6. Never write code without saying exactly where the file goes and how to run it.
7. Never continue while local commits are unpushed.
8. Always commit and push completed work.
9. Always verify touched files are tracked with `git ls-files` after commit.
10. Do not run real-data validation unless explicitly authorized.
11. Do not start Phase 4 execution unless explicitly authorized.
12. Do not live trade.

Testing:

- Docs-only edit:
  - No full pytest required by default.
  - Use `git diff --check` and `git diff --stat`.
- Code edit:
  - Run focused tests.
  - Run full `python -m pytest -q`.
  - Current full-test anchor: `611 passed`.
- If full tests pass but count drops below `611` without explicit planned test removal, stop and treat as regression.

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

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Expected after this handoff is committed and pushed:

- On branch `main`
- Branch up to date with `origin/main`
- Nothing to commit, working tree clean
- Latest commit should be `Add handoff document #55 after H021 decomposition diagnostic`
- Recent previous commits should include:
  - `Add H021 trade decomposition diagnostic`
  - `Add H021 hypothesis seed`
  - `Record H020 performance failure`
  - `Add H020 performance diagnostic script`

Do not require pytest for this first check unless code has changed or status is not clean.

## Current Test Anchor

Current full-test anchor after H021 trade decomposition diagnostic code:

- `611 passed in 27.66s`

Previous anchors:

- after H020 performance diagnostic script: `607 passed`
- after H020 strict validation work: `605 passed`
- after H020 sizing-intent seed: `600 passed`

If full test count drops below `611` without planned test removal, treat it as a regression.

## Important Current Commits

Recent important commits, newest first before this handoff:

- `0282cf9 Add H021 trade decomposition diagnostic`
- `2f7e32a Add H021 hypothesis seed`
- `57812f7 Record H020 performance failure`
- `4d0bb73 Add H020 performance diagnostic script`
- `71eeb41 Add handoff document #53 after H020 sizing intent`
- `52e0d39 Add comprehensive handoff document #54 after H020 validation success`
- `58f8373 Add handoff document #54 after H020 validation success`
- `7e0826f Fix H017Result missing arguments in H020 bridge shim`
- `80f44c8 Fix H017Result instantiation in H020 bridge shim`
- `9dd78de Add H020 strict event bridge and real validation runner`
- `97678db Add H020 sizing intent real-data diagnostic scanner`
- `68fc638 Add H020 panel intent generator`
- `b3664d6 Add H020 sizing intent contract`

Important note:

- There was a confusing sequence where a stale H53 handoff commit appeared after H54 work.
- HANDOFF_55 is now authoritative and supersedes both H53 and H54.

## Important Paths

Code:

- `quantcore`
- `scripts`
- `tests`

Strategy files:

- `quantcore\strategy\h017.py`
- `quantcore\strategy\h019.py`
- `quantcore\strategy\h020.py`
- `quantcore\strategy\h020_runner.py`
- `quantcore\strategy\signals.py`
- `quantcore\strategy\heat_governor.py`

Event/strict bridge files:

- `quantcore\backtest\h017_event.py`
- `quantcore\backtest\h017_strict_event.py`
- `quantcore\backtest\h019_strict_event.py`
- `quantcore\backtest\h020_strict_event.py`

Portfolio/accounting:

- `quantcore\backtest\portfolio.py`
- `quantcore\backtest\cost_model.py`
- `quantcore\backtest\fill_engine.py`

H020 scripts:

- `scripts\scan_h020_sizing_diagnostics_real.py`
- `scripts\run_h020_strict_event_real.py`
- `scripts\diagnose_h020_performance_real.py`

H021 scripts:

- `scripts\diagnose_h021_trade_decomposition_real.py`

H020/H021 tests:

- `tests\test_h020.py`
- `tests\test_h020_runner.py`
- `tests\test_h020_sizing_diagnostics_real_script.py`
- `tests\test_h020_strict_event.py`
- `tests\test_h020_strict_event_real_script.py`
- `tests\test_h020_performance_real_script.py`
- `tests\test_h021_trade_decomposition_real_script.py`

Important docs:

- `docs\operations\H019_GRAVEYARD_RECORD.md`
- `docs\operations\H020_HYPOTHESIS_SEED.md`
- `docs\operations\H020_GRAVEYARD_RECORD.md`
- `docs\operations\H021_HYPOTHESIS_SEED.md`
- `docs\operations\handoffs\HANDOFF_55.md`

## Gitignore And Raw Data Rules

The repo uses root-anchored:

- `/data/`

Do not change it to unanchored:

- `data/`

Reason:

- An unanchored `data/` rule previously risked excluding `quantcore/data/`.

Do not commit:

- raw MT5 CSV files,
- raw HistData files,
- large derived datasets,
- broker/vendor source files.

Do not modify raw broker files.

## Broker And Data State

Broker:

- Exness

Account environment:

- Demo

Server:

- MT5

Broker timezone used by loader:

- `Europe/Athens`
- Winter UTC+2
- Summer UTC+3
- DST-aware

MT5 loader signature:

- `load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult`

Expanded broker-native raw exports exist locally and are gitignored:

- `data\raw\USDJPY\H4.csv`
- `data\raw\USDJPY\M1.csv`
- `data\raw\XAUUSD\H4.csv`
- `data\raw\XAUUSD\M1.csv`

Reported exact MT5 symbols:

- `USDJPYm`
- `XAUUSDm`

Do not commit these raw files.

## Source Acceptance Status

Accepted source for strict validation/diagnostics:

- Exness demo MT5 broker-native exports only.

Accepted symbols:

- USDJPY
- XAUUSD

Accepted timeframes:

- Broker-native H4
- Broker-native M1

Accepted strict bridge-window range:

- First common complete H4/M1 bridge window UTC: `2021-07-02 13:00:00+00:00`
- Last common complete H4/M1 bridge window UTC: `2026-04-30 01:00:00+00:00`

Accepted bridge-window count:

- `5476`

A common complete H4/M1 bridge window means:

- USDJPY has a broker-native H4 bar at the H4 timestamp.
- XAUUSD has a broker-native H4 bar at the same H4 timestamp.
- For each symbol, the next H4 timestamp is exactly four hours later.
- For each symbol, the M1 window has exactly 240 M1 bars.
- No M1 imputation, forward-fill, backfill, or synthetic bar insertion is used.

Do not treat 2018 through 2021-06 as dense M1 history. The expanded files have a sparse daily-like prefix before the dense M1 candidate region, which starts at 2021-07 for both symbols.

HistData remains rejected for H017/H018/H019/H020/H021 validation or tuning under current evidence.

Do not use HistData for:

- validation,
- tuning,
- production dataset creation,
- broker H4 + HistData M1 combinations.

## Core Strategy And Backtest Conventions

ATR:

- Wilder RMA, not SMA.
- First true range is high - low.
- Seed at index window - 1 with simple mean of first window true ranges.
- Recurrence:
  - `ATR[t] = (ATR[t-1] * (n - 1) + TR[t]) / n`

Chandelier Exit:

- Long: `highest_high(lookback) - multiplier * ATR`
- Short: `lowest_low(lookback) + multiplier * ATR`
- Current rolling windows include the current bar.
- Defaults:
  - multiplier `3.0`
  - lookback `22`

Donchian Signals:

- Long: `close[t] > max(high[t-N ... t-1])`
- Short: `close[t] < min(low[t-N ... t-1])`
- Channel uses prior N bars via `shift(1).rolling(N)`.

Event bridge timing:

- Strategy decides at H4 timestamp t.
- Trade opens on next H4 bar open t+1.
- M1 bars inside next H4 window resolve stops.
- If no stop is hit, exposure closes at following H4 open as `signal_flip`.
- This is a bridge-layer simplification.

Fill rule:

- If stop and take-profit are both touched in the same M1 bar, stop wins.
- Reason: M1 OHLC does not reveal tick order inside the minute.

Cost model defaults:

USDJPY:

- spread_price = `0.01`
- commission_usd_per_lot_per_fill = `7.0`
- stop_slippage_atr_fraction = `0.05`

XAUUSD:

- spread_price = `0.30`
- commission_usd_per_lot_per_fill = `10.0`
- stop_slippage_atr_fraction = `0.05`

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

- Hard max = `10.0x`
- A single trade may not create more than 10x account equity in USD-converted gross notional exposure.
- Boundary:
  - `< 10.0` passes
  - `== 10.0` passes
  - `> 10.0` fails closed

Maximum portfolio-wide USD gross leverage:

- Hard max = `10.0x`
- Total USD-converted gross notional exposure opened by all symbols in one event interval may not exceed 10x account equity.
- Long and short exposures are summed gross, not netted.
- Boundary:
  - `< 10.0` passes
  - `== 10.0` passes
  - `> 10.0` fails closed

Violation policy:

- Raise explicit error.
- Do not silently skip any trade in the event engine.
- Do not clip any position size in the event engine.
- Do not net long and short notionals.
- Do not warn and continue.
- Do not log-only continue.

## Strategy Graveyard Summary

Immutable summary:

- H001: Backtests without intrabar SL/TP simulation are fiction. Must use M1 inside H4 bars to resolve fills.
- H002-H003: ATR-based per-symbol stops mandatory; trade frequency must amortize costs.
- H004a-H005: Single-seed ML and stacked multi-symbol ML were unreliable. If ML ever returns, use multi-seed and per-symbol modeling.
- H006-H010: Confidence filters are not risk management. ML on basic technicals cannot be a risk manager.
- H011-H013: Deterministic ATR stops + Chandelier exits + vol-targeted sizing showed edge on USDJPY, but single-asset tail risk remained.
- H014-H016: USDJPY + XAUUSD reduced kurtosis and improved Sortino, but 1% per-trade risk was not 1% portfolio risk when trades overlapped. Drawdown breached -19.43%.
- H017: H016 plus portfolio heat governor. Failed strict expanded broker-native event validation by insolvency before guards, then failed closed under H018-style guards.
- H018: Guard and diagnostic work revealed structural strategy/execution mismatch. H018 was not a validated strategy.
- H019: Stateful Donchian/Chandelier lifecycle fixed stale-stop first blocker but failed closed on H018 per-trade leverage guard. H019 is in the graveyard.
- H020: Explicit sizing contract fixed guard-survivability but failed performance. H020 is in the graveyard.
- H021: Active diagnostics-first research phase. No strategy is validated.

Current verdicts:

- H017 failed.
- H018 diagnostic/guard work only; not validated.
- H019 failed.
- H020 failed performance.
- H021 is not a strategy yet.
- No strategy is currently promotable.
- No live trading is approved.
- Phase 4 execution is not approved.

## H019 Summary

H019 introduced:

- Donchian entry/flip trigger.
- Same-side Chandelier lifecycle exit.
- Flat state after same-side stop breach.
- No re-entry from stale held Donchian direction.
- No opposite-panel switching.
- H018 guards remain strict.

Strict broker-native H019 validation:

- Preflight passed over `5476` accepted complete windows.
- Failed closed on `H018MaximumPerTradeLeverageError`.

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
- maximum_gross_leverage: `10.000000000`

H019/H020 diagnostic after H019:

- total remaining H019 guard violations: `302`
- per-trade leverage: `239`
- portfolio leverage: `42`
- minimum stop-distance: `19`
- invalid directional stop: `2`

Per-trade leverage severity:

- median `15.70x`
- p95 `79.82x`
- max `429.70x`

## H020 Implementation Summary

H020 was a sizing-contract hypothesis on top of H019 lifecycle semantics.

Implemented files include:

- `quantcore\strategy\h020.py`
- `quantcore\strategy\h020_runner.py`
- `quantcore\backtest\h020_strict_event.py`
- `scripts\scan_h020_sizing_diagnostics_real.py`
- `scripts\run_h020_strict_event_real.py`
- `scripts\diagnose_h020_performance_real.py`
- corresponding H020 tests.

H020 mechanics:

- invalid stop geometry becomes flat/no intent at strategy-intent level,
- below-spread raw stop distance becomes flat/no intent,
- per-trade strategy cap = `9.0x` gross notional,
- portfolio strategy cap = `9.0x` gross notional,
- H018 hard guards remain `10.0x` and unchanged,
- explicit intent objects preserve diagnostics,
- bridge shim converts H020 intent back into H017Result-shaped `positions` for strict event bridge compatibility.

Important caveat:

- The bridge shim evaluates intents at nominal `\$10,000` equity and reverse-engineers final safe signed risk fractions.
- This was a routing shim, not the strategy truth.
- It was tested and used to pass through the strict H018 event layer.

## H020 Strict Guard Validation Result

Command:

- `python .\scripts\run_h020_strict_event_real.py`

Result:

- strict accepted bridge-windows: `5476`
- completed successfully without guard violations.

Interpretation:

- H020 survived strict event/guard validation.
- This proved safe representation under current bridge constraints.
- It did not prove profitability.

## H020 Performance Failure

Performance diagnostic script:

- `scripts\diagnose_h020_performance_real.py`

Command:

- `python .\scripts\diagnose_h020_performance_real.py`

Real result:

- accepted_entry_count: `5476`
- executed_entry_count: `5476`
- skipped_entry_count: `3176`
- fill_count: `4158`
- starting_equity_usd: `\$10000.00`
- ending_equity_usd: `\$819.07`
- total_pnl_usd: `-\$9180.93`
- total_return: `-91.8093%`
- max_drawdown: `-91.8860%`
- winning_fill_count: `1837`
- losing_fill_count: `2321`
- flat_fill_count: `0`
- win_rate: `44.1799%`
- gross_profit_usd: `\$28703.99`
- gross_loss_usd: `-\$37884.92`
- profit_factor: `0.757663`
- mean_fill_return: `-0.0579%`
- median_fill_return: `-0.0375%`
- fill_return_sharpe: `-0.086278`

Verdict:

- H020 failed performance evaluation.
- H020 is not promotable.
- H020 is not live-approved.
- Phase 4 is not approved.

H020 graveyard record:

- `docs\operations\H020_GRAVEYARD_RECORD.md`

Key lesson:

- H020 separated execution survivability from profitability.
- It achieved the first and failed the second.

## H021 Start

H021 was started in:

- `docs\operations\H021_HYPOTHESIS_SEED.md`

H021 purpose:

- H021 is not another sizing patch.
- H021 must search for positive expectancy before adding more execution machinery.

Core question:

- Can USDJPY + XAUUSD produce a cost-amortized, event-safe edge under strict broker-native H4/M1 simulation?

H021 should preserve:

- strict broker-native Exness complete-window validation only,
- M1 intrabar stop resolution inside H4 decisions,
- conservative stop-first fill rule,
- modeled spread, commission, and slippage,
- H018 hard guards unchanged,
- no raw-data mutation,
- no HistData,
- no live trading.

H021 should not begin by increasing risk or leverage.

H021 should begin by reducing bad trades.

Likely research directions:

1. Cost-amortization filters.
2. Regime gating.
3. Entry selectivity.
4. Exit asymmetry.
5. Symbol-specific behavior.

## H021 First Diagnostic: Trade Decomposition

Implemented files:

- `scripts\diagnose_h021_trade_decomposition_real.py`
- `tests\test_h021_trade_decomposition_real_script.py`

Commit:

- `0282cf9 Add H021 trade decomposition diagnostic`

Tests after implementation:

- focused H021 test: `4 passed`
- H020 performance + H021 diagnostic focused tests: `6 passed`
- full test suite: `611 passed in 27.66s`

Real command run:

- `python .\scripts\diagnose_h021_trade_decomposition_real.py`

Real diagnostic result:

By symbol:

- USDJPY:
  - fills: `2827`
  - win_rate: `44.2872%`
  - total_pnl_usd: `-7259.73`
  - mean_pnl_usd: `-2.57`
  - median_pnl_usd: `-0.94`
  - profit_factor: `0.722826`
- XAUUSD:
  - fills: `1331`
  - win_rate: `43.9519%`
  - total_pnl_usd: `-1921.21`
  - mean_pnl_usd: `-1.44`
  - median_pnl_usd: `-1.47`
  - profit_factor: `0.835695`

By side:

- buy:
  - fills: `2497`
  - win_rate: `45.8550%`
  - total_pnl_usd: `-5224.34`
  - mean_pnl_usd: `-2.09`
  - median_pnl_usd: `-0.75`
  - profit_factor: `0.766060`
- sell:
  - fills: `1661`
  - win_rate: `41.6616%`
  - total_pnl_usd: `-3956.60`
  - mean_pnl_usd: `-2.38`
  - median_pnl_usd: `-1.47`
  - profit_factor: `0.745606`

By exit reason:

- signal_flip:
  - fills: `3678`
  - win_rate: `49.9456%`
  - total_pnl_usd: `+9503.32`
  - mean_pnl_usd: `+2.58`
  - median_pnl_usd: `-0.00`
  - profit_factor: `1.494947`
- stop:
  - fills: `480`
  - win_rate: `0.0000%`
  - total_pnl_usd: `-18684.26`
  - mean_pnl_usd: `-38.93`
  - median_pnl_usd: `-27.45`
  - profit_factor: `0.000000`

By symbol / side / exit reason:

- USDJPY buy signal_flip:
  - fills `1606`
  - total_pnl_usd `+3657.99`
  - profit_factor `1.444201`
- USDJPY buy stop:
  - fills `155`
  - total_pnl_usd `-7280.03`
  - mean_pnl_usd `-46.97`
  - median_pnl_usd `-34.00`
- USDJPY sell signal_flip:
  - fills `932`
  - total_pnl_usd `+1347.77`
  - profit_factor `1.236805`
- USDJPY sell stop:
  - fills `134`
  - total_pnl_usd `-4985.46`
  - mean_pnl_usd `-37.20`
  - median_pnl_usd `-20.77`
- XAUUSD buy signal_flip:
  - fills `626`
  - total_pnl_usd `+2324.15`
  - profit_factor `1.804076`
- XAUUSD buy stop:
  - fills `110`
  - total_pnl_usd `-3926.44`
  - mean_pnl_usd `-35.69`
  - median_pnl_usd `-28.49`
- XAUUSD sell signal_flip:
  - fills `514`
  - total_pnl_usd `+2173.41`
  - profit_factor `1.911772`
- XAUUSD sell stop:
  - fills `81`
  - total_pnl_usd `-2492.32`
  - mean_pnl_usd `-30.77`
  - median_pnl_usd `-24.05`

Interpretation:

- H020 losses are not because all trades are bad.
- Every `signal_flip` bucket is profitable.
- Every `stop` bucket is deeply negative.
- Stop exits are the destructive component:
  - `480` stop fills caused `-18684.26`.
  - `3678` signal-flip fills made `+9503.32`.
- USDJPY stop losses are the largest damage:
  - USDJPY buy stops `-7280.03`
  - USDJPY sell stops `-4985.46`

Current H021 research question:

- Can we identify likely future stop-outs before entry, using only information available at decision time?

Do not jump to removing stops. Stops are structural risk controls. The evidence says entries that later hit stops are the problem.

## Recommended Next Engineering Action

Next action should be read-only inspection first, not code.

Need inspect whether `Fill` stores enough context to link back to decision time and stop distance, or whether H021 must reconstruct decision context from H020/H019 panels.

Recommended next command:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    Get-Content .\quantcore\backtest\fill_engine.py
    Select-String -Path .\quantcore\backtest\h017_event.py -Pattern "Fill\(|decision_time|entry_time_utc|exit_reason|stop_distance|stop_price" -Context 2,3

Then decide between:

Option A:

- Reconstruct decision context externally from H020 panels:
  - decision_time = previous H4 timestamp before fill entry,
  - entry_time = fill.entry_time_utc,
  - use H020 intent panel for stop distance, leverage, suppression metadata,
  - group stop rate and P&L by decision-time features.

Option B:

- Extend event fill diagnostics to preserve decision context in a separate diagnostic object, not by mutating raw `Fill` unless necessary.

Preferred next diagnostic:

- H021 stop-loss precursor decomposition.

Candidate fields:

- symbol
- side
- exit_reason
- P&L after costs
- decision_time
- entry_time
- decision hour UTC
- entry hour UTC
- raw stop distance
- stop distance as spread multiple
- stop distance bucket
- final signed risk fraction
- estimated gross leverage bucket if available
- maybe volatility or ATR state later

Goal:

- Identify whether future stop-outs are concentrated in decision-time observable regimes.

Do not implement a new strategy until diagnostics show a plausible, non-fictional source of positive expectancy.

## Absolute Do-Not Rules

Do not:

- live trade,
- approve Phase 4,
- treat H020 guard-validation success as profitability,
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
- allow full-test count to drop below `611` without explicit test-removal intent.

## Known Repo Hygiene Lessons

Do not repeat these mistakes:

- `.gitignore` once had unrooted `data/`, which risked excluding `quantcore/data`.
- Some older commits missed files because `git add` was incomplete.
- An empty `HANDOFF_16.md` was accidentally committed once.
- A mistaken empty root-level `HANDOFF_43.md` was created once and was not to be committed.
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
- For long handoffs, use VS Code manual editing or a PowerShell here-string.
- A broad text replacement once accidentally inserted `H018MaximumPortfolioGrossLeverageError` into existing per-trade `pytest.raises` calls. Focused tests caught it.

## Exact First Response The Next AI Should Give

The next AI should respond briefly:

Understood. Continuing after HANDOFF_55.

I understand:

- Windows / PowerShell / VS Code / Python 3.12.10 in `.venv`.
- Current branch should be `main`.
- Current full-test anchor is `611 passed`.
- H017 failed.
- H018 is guard/diagnostic work, not a validated strategy.
- H019 failed and is in the graveyard.
- H020 survived strict event guard validation but failed performance badly:
  - ending equity `\$819.07`,
  - total return `-91.8093%`,
  - max drawdown `-91.8860%`,
  - profit factor `0.757663`.
- H020 is in the graveyard.
- H021 has started as diagnostics-first research, not a new strategy.
- H021 first decomposition showed:
  - signal_flip exits made `+9503.32`,
  - stop exits lost `-18684.26`,
  - every signal_flip bucket was profitable,
  - every stop bucket was deeply negative.
- Current H021 question is whether likely future stop-outs can be identified before entry using only decision-time information.
- No live trading is approved. Phase 4 is not approved.

Please run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    git status
    git log --oneline -10

Then paste the full output.

After hygiene passes, I will inspect fill/event context before building H021 stop-loss precursor diagnostics.
