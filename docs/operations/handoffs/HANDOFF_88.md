# HANDOFF_88 — H024 Replay Sweep Runtime Result + Synthetic Balance Diagnostic

If any older handoff conflicts with this one, this handoff wins.

This document is intended to be fully self-contained. A new AI should be able to continue safely from this document without opening older handoffs first.

## 0. One-Sentence State

H024 remains research-only and is not demo/live/Phase 4 approved; replay sweep mode has now been manually validated on Exness Standard Cent symbols, the runtime verifier was fixed to allow replay-sweep markers, the XAUUSDc replay sweep again produced a log-only BLOCKED short signal with positive entry/stop, and a default-off synthetic balance diagnostic has been implemented, compiled, tested, committed, and pushed.

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current strategy family:

- H024

Current stage:

- Execution-safety preparation
- Cent-account log-only runtime validation
- Synthetic research-only sizing diagnostics

The user is eager to deploy and intends eventually to start with:

- 10000 USC on an Exness Standard Cent account

Do not soften deployment boundaries.

Correct direct deployment answer:

- H024 is meaningfully closer under the 10000 USC cent-account route, but it is still not demo/live/Phase 4 deployable.

## 2. Human Preference

The user is tired of ceremony and wants practical progress.

Going forward:

- Keep responses practical and concise.
- Prefer one copy/paste PowerShell block when commands are needed.
- Do one real action at a time.
- Do not create governance docs unless they preserve a real result, preserve a handoff, prevent ambiguity, or protect against future confusion.
- For docs-only edits, do not run full pytest unless there is a clear reason.
- For code edits, tests are mandatory.
- Avoid long real-data diagnostics casually.
- For real-data diagnostics, get explicit authorization or make a clear safety-bound decision.
- Never soften deployment boundaries because H024 is promising.

Important recent frustration:

A replay-sweep patch attempt previously went wrong because tests were committed without implementation. The user noticed repeated failures and explicitly challenged whether the errors were being read. Be careful. Inspect actual source before patching. Do not blindly repeat failing patch scripts.

## 3. Environment

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 inside .venv
- No WSL

Repository root:

- C:\Users\equin\Documents\institutional-ea

Virtual environment:

- C:\Users\equin\Documents\institutional-ea\.venv

Branch:

- main

GitHub remote:

- https://github.com/citradinnda/institutional-ea.git

MetaEditor:

- C:\Program Files\MetaTrader 5\MetaEditor64.exe

Terminal data dir:

- C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075

Terminal EA source:

- C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5

Compiled EX5:

- C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5

Terminal runtime CSV:

- C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\h024_ea_log_only_preflight.csv

Repo runtime CSV:

- reports\h024_ea_log_only_preflight.csv

reports/ is local and intentionally untracked.

Do not commit reports/.

## 4. Expected Repo State After This Handoff Is Committed

Expected:

- On branch main
- Your branch is up to date with origin/main
- Untracked files: reports/
- Nothing added to commit except untracked reports/

Expected latest commit after this handoff is committed:

- Add handoff document #88

Expected latest code commit before handoff:

- fb95bd9 Add H024 synthetic balance diagnostic

Recent important commits:

- fb95bd9 Add H024 synthetic balance diagnostic
- fc5918c Document H024 replay sweep runtime result
- ff9f500 Allow H024 replay sweep runtime markers
- 344847d Add handoff document #87
- 7bf1728 Add H024 log-only replay sweep mode
- d67eff3 Revert "Add H024 log-only replay sweep mode"
- 7c1b69a Add H024 log-only replay sweep mode
- 993b274 Document H024 cent-symbol blocked replay result

Important note:

- 7c1b69a was a bad commit. It accidentally added only failing replay-sweep static tests without the EA implementation. It made main red. It was immediately reverted by d67eff3.
- The correct replay-sweep implementation landed in 7bf1728.
- The synthetic balance diagnostic landed in fb95bd9.

## 5. Non-Negotiable Safety Boundary

H024 remains:

- Research-only
- Pre-deployment only
- Not demo-approved
- Not live-approved
- Not Phase 4-approved
- Not approved for order execution
- Not approved for any execution adapter

Forbidden in current stage:

- OrderSend
- OrderSendAsync
- OrderCheck
- CTrade
- #include <Trade...>
- MqlTradeRequest
- MqlTradeResult
- PositionOpen
- PositionClose
- PositionModify
- Pending order helpers

Also not approved:

- EA chart attach/detach automation
- GUI automation
- MT5 launcher/profile mutation affecting live terminals
- Order-send automation
- Demo/live execution adapter
- Raising risk to force executable candidates
- Treating feasibility scans as deployment approval
- Treating BLOCKED rows as executable
- Reconstructing dry-run execution requests from BLOCKED rows

Allowed so far:

- Manual EA attach/remove
- Copy EA source to terminal Experts
- Compile EA with MetaEditor
- Reset/collect runtime CSV
- Verify runtime CSV
- Summarize intended-action rows
- Historical log-only replay using InpH024ClosedShift
- Log-only replay sweep using InpH024ReplaySweepEnabled
- CSV-read-only dry-run request reconciliation
- Pure Python dry-run execution request contracts
- Runtime BLOCKED sizing diagnostics verification
- Pure Python minimum-volume feasibility summary
- Pure Python executable candidate shift scanning
- Pure Python exact capital threshold scanning
- Pure Python risk-fraction threshold comparison
- Read-only MT5 account/symbol-info probes
- Read-only MT5 order_calc_profit probes
- Pure Python cent-account USC feasibility scanner support
- Cent-symbol runtime CSV verifier/summarizer support
- Cent-symbol local runtime target preflight
- Clean cent-symbol log-only runtime collection and verification
- Synthetic research-only balance diagnostic, default off, log-only only

## 6. H024 Strategy Mechanics Summary

H024 is a regime-conditioned pullback-continuation hypothesis.

Mechanics:

- Defines directional regime using slow H4 trend state.
- Waits for pullback against that regime.
- Enters only if price resumes in regime direction after pullback.
- Does not use H021 time/session buckets.
- Does not reuse Donchian breakout trigger.
- Uses H020 sizing contract.
- Returns H017-compatible bridge shim.
- Uses H018 hard guard semantics.
- Baseline candidate: hold = 3 H4, stop ATR multiple = 2.0.

Frozen signal defaults:

- slow_window = 5
- slope_lag = 2
- atr_window = 3
- pullback_window = 3
- min_pullback_atr = 0.25
- max_pullback_atr = 3.0
- min_slope_atr = 0.05

Signal logic summary:

- slow_ma = close rolling 5 mean
- atr = Wilder ATR(3)
- slope = slow_ma - slow_ma.shift(2)
- slope_threshold = atr * 0.05
- trend_up = close > slow_ma and slope > slope_threshold
- trend_down = close < slow_ma and slope < -slope_threshold
- previous_bearish = close.shift(1) < open.shift(1)
- previous_bullish = close.shift(1) > open.shift(1)
- long_signal = trend_up plus bearish pullback plus long resumption
- short_signal = trend_down plus bullish pullback plus short resumption

## 7. H020 / H024 Sizing Boundary

H024 uses H020 sizing.

Important H020 behaviors:

- Computes explicit pre-trade lot intents.
- Suppresses flat signals.
- Suppresses invalid stop geometry.
- Suppresses stop distances below one spread.
- Computes risk-based lots.
- Applies per-trade gross notional caps.
- Applies portfolio gross notional scaling.
- Rounds lots down to broker lot step.
- Suppresses lots below broker minimum lot.
- Preserves final signed risk fraction from final executable lots.

Therefore:

- Cent-account scans must not bypass H020 sizing.
- The cent scanner routes balances through cent-account USC instrument specs, not by pretending 10000 USC equals 10000 USD.
- Synthetic balance diagnostics must remain clearly labeled as synthetic and must not be confused with real account evidence.

## 8. Data Rules

Accepted validation source:

- Exness demo/terminal broker-native exports only

Accepted model symbols:

- USDJPY
- XAUUSD

Current cent account runtime symbols:

- USDJPYc
- XAUUSDc

Previously observed standard-like symbols:

- USDJPYm
- XAUUSDm

Symbol normalization:

- USDJPYc -> USDJPY
- XAUUSDc -> XAUUSD
- USDJPYm -> USDJPY
- XAUUSDm -> XAUUSD

Accepted timeframes:

- Broker-native H4
- Broker-native M1

Broker timezone used by loader:

- Europe/Athens

Do not use:

- HistData for validation/tuning/production dataset creation
- Broker H4 plus HistData M1 combinations
- Sparse 2018 through 2021-06 broker-native prefix as dense M1
- Incomplete H4/M1 windows

Do not commit:

- Raw MT5 CSV files
- Raw HistData files
- Large derived datasets
- Broker/vendor source files
- reports/*.csv
- reports/*.json
- Local runtime CSVs
- Local compile logs

## 9. Core Files

H024 core:

- quantcore\strategy\h024.py
- quantcore\strategy\h024_runner.py

H020 sizing contract:

- quantcore\strategy\h020.py
- tests\test_h020.py

Position sizing reference:

- quantcore\strategy\h024_position_sizer.py
- tests\test_h024_position_sizing.py

Execution/log contracts:

- quantcore\execution\h024_intended_action_log.py
- quantcore\execution\h024_dry_run_execution_request.py
- quantcore\execution\h024_dry_run.py
- tests\test_h024_intended_action_log_contract.py
- tests\test_h024_dry_run_execution_request_contract.py
- tests\test_h024_intended_action_blocked_sizing_diagnostics.py

EA/runtime:

- ea_mt5\Experts\H024_LogOnly_Preflight.mq5
- scripts\run_h024_mt5_log_only_preflight_local.py
- scripts\verify_h024_ea_preflight_log.py
- scripts\summarize_h024_ea_intended_action_runtime.py
- scripts\verify_h024_ea_source_static.py
- scripts\reconcile_h024_runtime_dry_run_requests.py
- scripts\summarize_h024_blocked_sizing_diagnostics.py

Feasibility / capital threshold tools:

- scripts\summarize_h024_min_volume_feasibility.py
- scripts\scan_h024_executable_candidate_shifts.py
- scripts\scan_h024_capital_thresholds.py

Cent account support:

- scripts\scan_h024_executable_candidate_shifts.py
- tests\test_h024_cent_account_specs.py

Cent-symbol runtime validation support:

- scripts\verify_h024_ea_preflight_log.py
- scripts\summarize_h024_ea_intended_action_runtime.py
- scripts\run_h024_mt5_log_only_preflight_local.py
- tests\test_h024_cent_symbol_runtime_validation.py
- tests\test_h024_mt5_log_only_preflight_local_helper.py

Replay sweep support:

- ea_mt5\Experts\H024_LogOnly_Preflight.mq5
- tests\test_h024_ea_replay_sweep_static.py

Synthetic balance diagnostic support:

- ea_mt5\Experts\H024_LogOnly_Preflight.mq5
- tests\test_h024_ea_synthetic_balance_static.py

Important docs:

- docs\operations\H024_REPLAY_SWEEP_RUNTIME_RESULT.md
- docs\operations\H024_CENT_SYMBOL_REPLAY_BLOCKED_RUNTIME_RESULT.md
- docs\operations\H024_CENT_ACCOUNT_SYMBOL_FEASIBILITY_PROBE_RESULT.md
- docs\operations\H024_BALANCE_EXECUTABLE_CANDIDATE_DENSITY_RESULT.md
- docs\operations\H024_100USD_1PCT_FEASIBILITY_BOUNDARY.md
- docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_MODE_RESULT.md
- docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_RESULT.md
- docs\operations\H024_EXACT_CAPITAL_THRESHOLD_RESULT.md
- docs\operations\H024_CAPITAL_FEASIBILITY_FRONTIER_RESULT.md
- docs\operations\H024_EXECUTABLE_CANDIDATE_SHIFT_SCAN_RESULT.md
- docs\operations\H024_MIN_VOLUME_FEASIBILITY_RESULT.md
- docs\operations\H024_BLOCKED_SIZING_DIAGNOSTICS_RUNTIME_RESULT.md
- docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
- docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
- docs\operations\handoffs\HANDOFF_83.md
- docs\operations\handoffs\HANDOFF_84.md
- docs\operations\handoffs\HANDOFF_85.md
- docs\operations\handoffs\HANDOFF_86.md
- docs\operations\handoffs\HANDOFF_87.md
- docs\operations\handoffs\HANDOFF_88.md

## 10. EA Current Facts

EA source:

- ea_mt5\Experts\H024_LogOnly_Preflight.mq5

MQL5 property version before this handoff family:

- #property version "0.600"

Runtime schema:

- h024_ea_log_only_preflight_v2

EA input version:

- InpEaVersion = "0.6"

Intended-action schema:

- h024_intended_action_log_v1

Core replay input:

- InpH024ClosedShift = 1

Replay cap:

- 1 <= effective closed shift <= 240

Normal mode:

- Uses InpH024ClosedShift.
- Clamps below 1 to 1.
- Clamps above 240 to 240.
- Preserves old literal static-test strings:
  - if(InpH024ClosedShift < 1)
  - if(InpH024ClosedShift > 240)

Sweep mode inputs:

- InpH024ReplaySweepEnabled = false
- InpH024ReplaySweepStartShift = 1
- InpH024ReplaySweepEndShift = 1
- InpH024ReplaySweepMaxRows = 20

Sweep mode temporarily sets:

- g_h024_replay_sweep_override_shift = shift

Then calls for each shift:

- WriteH024StateObservationRow()
- WriteH024IntendedActionRuntimeRow()

Sweep markers:

- H024_REPLAY_SWEEP
- H024_REPLAY_SWEEP_SHIFT
- H024_REPLAY_SWEEP_DONE

Synthetic balance diagnostic inputs:

- InpH024SyntheticBalanceEnabled = false
- InpH024SyntheticBalance = 0.0

Synthetic balance helper functions added:

- H024SizingAccountBalance()
- H024SyntheticBalanceReasonSuffix()
- H024AppendSyntheticBalanceReason()

Synthetic diagnostic behavior:

- Default off.
- Only affects intended-action sizing balance.
- Does not alter account_balance/equity fields in normal preflight columns.
- Appends explicit reason suffix when enabled:
  - balance_source=synthetic_research_only
  - synthetic_balance=...
  - real_account_balance=...
- It is log-only and research-only.
- It is not real account evidence.
- It is not demo/live/Phase 4 approval.

OnInit behavior:

- Writes normal init/context rows.
- If sweep disabled:
  - Writes normal single state/intended-action rows.
- If sweep enabled:
  - Writes intended-action header once.
  - Sweeps configured shifts.
  - Writes state and intended-action rows per shift.
- Does not repeat sweep on tick/timer.

OnTick / OnTimer behavior:

- If sweep is disabled, writes normal state/intent/intended-action runtime rows.
- If sweep is enabled, does not repeat sweep rows.

## 11. Runtime Intended-Action Behavior

Runtime intended-action behavior:

- NO_ACTION rows can carry zero entry/stop/lots.
- Signal rows derive entry/stop from closed H4 bar and ATR stop.
- If signal sizing is executable, row may remain WOULD_OPEN.
- If signal sizing is below broker minimum volume, row becomes BLOCKED:volume_below_min_for_would_open.
- BLOCKED signal rows preserve positive entry/stop/stop-distance when available.
- BLOCKED signal rows force final executable lots to 0.
- Dry-run reconciler must not emit requests from BLOCKED rows.

Important current reality:

- Real account balance observed so far is 0.00 USC.
- The observed cent-symbol replay signal paths became BLOCKED because real account balance was zero.
- Synthetic balance diagnostics can be used to see what sizing would look like at a research-only synthetic balance, but this does not replace real-balance evidence.

## 12. Clean Cent Runtime Result From HANDOFF_86

Clean cent runtime collection facts:

- Rows: 78
- Violations: 0
- Verdict: PASS

Intended-action summary:

- CSV: reports\h024_ea_log_only_preflight.csv
- Total rows: 78
- Intended-action header rows: 2
- Intended-action data rows: 12

USDJPYc:

- headers: 1
- rows: 6
- normalized: USDJPY
- WOULD_OPEN: 0
- BLOCKED: 0
- NO_ACTION: 6

XAUUSDc:

- headers: 1
- rows: 6
- normalized: XAUUSD
- WOULD_OPEN: 0
- BLOCKED: 0
- NO_ACTION: 6

Interpretation:

- Clean cent-symbol runtime path passed, but no signal was observed.

## 13. Cent Candidate Scan Evidence

Command previously used:

- python scripts\scan_h024_executable_candidate_shifts.py --balance 10000 --risk-fraction 0.01 --cent-account-usc-specs --output-csv reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv --max-rows 20

Result:

- balance: 10000.00
- risk_fraction: 0.010000
- instrument_specs: Exness Standard Cent USC specs
- executable_candidate_rows: 1364
- Verdict: PASS

Inside the EA cap:

- total_candidates = 1364
- candidates_within_current_ea_replay_cap_240 = 25

Important rows inside cap:

- XAUUSD sell, decision 2026-03-17T22:00:00+00:00, entry 2026-03-18T02:00:00+00:00, shift 229, final_risk -0.008352
- USDJPY sell, decision 2026-03-18T02:00:00+00:00, entry 2026-03-18T06:00:00+00:00, shift 228, final_risk -0.009907
- XAUUSD sell, decision 2026-03-18T06:00:00+00:00, entry 2026-03-18T10:00:00+00:00, shift 227, final_risk -0.008657

Important insight:

- The scanner uses broker CSV-derived shift alignment.
- Runtime MT5 H4 indexing can differ slightly.
- A tight sweep around candidate shifts is safer than replaying one exact shift.

## 14. Manual Replay Attempts And Replay Sweep Runtime Result

Far-history replay failed due to the EA replay cap of 240.

Manual tight sweep eventually found a signal path.

Earlier manually swept result:

- XAUUSDc produced BLOCKED short rows.
- Signal was BLOCKED because account balance was 0.00 USC.
- This was documented in docs\operations\H024_CENT_SYMBOL_REPLAY_BLOCKED_RUNTIME_RESULT.md.

Replay sweep runtime result after 7bf1728:

Manual MT5 replay sweep was performed.

USDJPYc H4 inputs:

- InpH024ReplaySweepEnabled = true
- InpH024ReplaySweepStartShift = 226
- InpH024ReplaySweepEndShift = 228
- InpH024ReplaySweepMaxRows = 10

XAUUSDc H4 inputs:

- InpH024ReplaySweepEnabled = true
- InpH024ReplaySweepStartShift = 227
- InpH024ReplaySweepEndShift = 229
- InpH024ReplaySweepMaxRows = 10

Initial collection result before verifier fix:

- Rows: 419
- Violations: 10
- All violations were unexpected replay-sweep marker events:
  - H024_REPLAY_SWEEP
  - H024_REPLAY_SWEEP_SHIFT
  - H024_REPLAY_SWEEP_DONE

Intended-action summary still passed:

- Total rows: 419
- Intended-action header rows: 4
- Intended-action data rows: 38

USDJPYc:

- headers: 2
- rows: 14
- normalized: USDJPY
- WOULD_OPEN: 0
- BLOCKED: 0
- NO_ACTION: 14

XAUUSDc:

- headers: 2
- rows: 24
- normalized: XAUUSD
- WOULD_OPEN: 0
- BLOCKED: 1
- NO_ACTION: 23

Observed replay sweep markers:

USDJPYc:

- H024_REPLAY_SWEEP start_shift=226;end_shift=228;max_rows=10
- H024_REPLAY_SWEEP_SHIFT closed_shift=226
- H024_REPLAY_SWEEP_SHIFT closed_shift=227
- H024_REPLAY_SWEEP_SHIFT closed_shift=228
- H024_REPLAY_SWEEP_DONE rows_written=3

XAUUSDc:

- H024_REPLAY_SWEEP start_shift=227;end_shift=229;max_rows=10
- H024_REPLAY_SWEEP_SHIFT closed_shift=227
- H024_REPLAY_SWEEP_SHIFT closed_shift=228
- H024_REPLAY_SWEEP_SHIFT closed_shift=229
- H024_REPLAY_SWEEP_DONE rows_written=3

Unique blocked signal row:

- symbol: XAUUSDc
- action: BLOCKED
- side: short
- closed_h4_time: 2026.03.18 08:00:00
- entry: 4930.0480000000
- stop: 5019.1630000000
- raw_lots: 0.0000000000
- final_lots: 0.0000000000
- reason: BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;source=H024_STATE_OBSERVATION;mode=log_only_no_execution

After verifier fix in ff9f500:

- Rows: 419
- Violations: 0
- Verdict: PASS

This was documented in:

- docs\operations\H024_REPLAY_SWEEP_RUNTIME_RESULT.md

Commit:

- fc5918c Document H024 replay sweep runtime result

## 15. Verifier Fix

Issue:

- scripts\verify_h024_ea_preflight_log.py rejected replay-sweep markers as unexpected events.

Fix:

- Added allowed events:
  - H024_REPLAY_SWEEP
  - H024_REPLAY_SWEEP_SHIFT
  - H024_REPLAY_SWEEP_DONE

Commit:

- ff9f500 Allow H024 replay sweep runtime markers

Focused verification after fix:

- 31 passed in 2.56s

Full suite after fix:

- 958 passed in 38.98s

## 16. Synthetic Balance Diagnostic Added In fb95bd9

Reason:

- The user currently has zero money.
- Funding the cent account just to satisfy a validation gate is not appropriate.
- A synthetic research-only diagnostic allows the EA to compute intended-action sizing for a hypothetical balance without pretending it is real account evidence.

Commit:

- fb95bd9 Add H024 synthetic balance diagnostic

Files changed:

- ea_mt5\Experts\H024_LogOnly_Preflight.mq5
- tests\test_h024_ea_synthetic_balance_static.py

New EA inputs:

- input bool InpH024SyntheticBalanceEnabled = false;
- input double InpH024SyntheticBalance = 0.0;

New helpers:

- H024SizingAccountBalance()
- H024SyntheticBalanceReasonSuffix()
- H024AppendSyntheticBalanceReason()

Behavior:

- Default off.
- If disabled, sizing uses AccountInfoDouble(ACCOUNT_BALANCE).
- If enabled and InpH024SyntheticBalance > 0.0, intended-action sizing uses InpH024SyntheticBalance.
- If enabled and synthetic balance <= 0.0, intended-action sizing uses 0.0.
- Intended-action reason is appended with:
  - balance_source=synthetic_research_only
  - synthetic_balance=...
  - real_account_balance=...
- The intended-action CSV schema was not changed.
- The synthetic marker is in the reason field.
- This only affects intended-action sizing balance.
- It does not alter account_balance/equity preflight columns.
- It does not add execution or chart automation.

Static tests added:

- test_synthetic_balance_inputs_are_default_off
- test_synthetic_balance_is_labeled_in_reason_not_schema
- test_synthetic_balance_only_changes_intended_action_sizing_balance
- test_synthetic_balance_does_not_add_execution_or_chart_automation

Validation after synthetic diagnostic:

Focused tests:

- 14 passed in 1.28s

Static EA verifier:

- Violations: 0
- Verdict: PASS

MetaEditor compile/copy helper:

- MetaEditor compile return code: 1
- EX5 refreshed: True
- Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Full test suite:

- 962 passed in 26.86s

## 17. Known Pitfalls

MetaEditor returns code 1 even when compile succeeds.

Expected acceptable compile result:

- MetaEditor compile return code: 1
- EX5 refreshed: True
- Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

One-symbol verifier may fail if the other cent symbol is missing.

For full cent-symbol verifier pass, attach both:

- USDJPYc
- XAUUSDc

BLOCKED is not executable.

A row with BLOCKED:volume_below_min_for_would_open must not be treated as a dry-run request or execution candidate.

Runtime account balance is currently 0.00 USC.

This is the main reason no real executable WOULD_OPEN row exists.

Scanner shift and MT5 runtime shift can be offset.

Use sweeps around candidates rather than only one exact shift.

Synthetic balance is not real account evidence.

A synthetic WOULD_OPEN row would only prove the EA can calculate a hypothetical intended-action row. It would not prove the real account could open the position.

## 18. Recommended Next Runtime Validation

Next practical step:

Run the replay sweep again with synthetic balance enabled on XAUUSDc, then collect and verify.

Manual MT5 attach for XAUUSDc H4:

- InpH024ReplaySweepEnabled = true
- InpH024ReplaySweepStartShift = 227
- InpH024ReplaySweepEndShift = 229
- InpH024ReplaySweepMaxRows = 10
- InpH024SyntheticBalanceEnabled = true
- InpH024SyntheticBalance = 10000.0

Optional USDJPYc H4 attach:

- InpH024ReplaySweepEnabled = true
- InpH024ReplaySweepStartShift = 226
- InpH024ReplaySweepEndShift = 228
- InpH024ReplaySweepMaxRows = 10
- InpH024SyntheticBalanceEnabled = true
- InpH024SyntheticBalance = 10000.0

Expected useful evidence if XAUUSDc signal repeats:

- It may produce WOULD_OPEN with nonzero raw_lots/final_lots if synthetic sizing clears minimum volume.
- The reason must include balance_source=synthetic_research_only.
- It must also include real_account_balance=0.00 or the actual real account balance.
- This is synthetic evidence only.

Commands after manual attach/remove:

- python scripts\run_h024_mt5_log_only_preflight_local.py --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" --cent-account-symbols --collect
- python scripts\summarize_h024_ea_intended_action_runtime.py reports\h024_ea_log_only_preflight.csv --cent-account-symbols

Before manual attach, reset old CSVs:

- Remove terminal runtime CSV.
- Remove reports\h024_ea_log_only_preflight.csv.
- Keep reports/ untracked.

## 19. Recommended Next Engineering Options

Option A — Synthetic runtime evidence, no money required:

- Run XAUUSDc replay sweep with InpH024SyntheticBalanceEnabled = true and InpH024SyntheticBalance = 10000.0.
- Collect runtime CSV.
- Verify CSV.
- Summarize intended actions.
- Extract synthetic WOULD_OPEN/BLOCKED rows.
- Document as synthetic-only evidence.

Option B — Improve verifier awareness:

- Add verifier checks that if balance_source=synthetic_research_only appears, reason must also include synthetic_balance= and real_account_balance=.
- This is not strictly required before first synthetic runtime run, but it would reduce ambiguity.

Option C — Improve summarizer awareness:

- Update summarizer to display synthetic rows separately.
- This is useful if synthetic diagnostics will be repeated.

Option D — Real-balance evidence later:

- When the user has funds, rerun log-only replay sweep with real balance.
- This remains the cleanest evidence for real runtime executable WOULD_OPEN sizing.
- Do not pressure user to fund the account.

## 20. Current Deployment Verdict

H024 is closer, but still:

- not demo-approved
- not live-approved
- not Phase 4-approved
- not execution-approved

The blocker is still:

- No executable real-runtime WOULD_OPEN row with nonzero final lots has been observed.

Synthetic balance diagnostic can produce research-only hypothetical evidence, but it does not remove the real-runtime evidence blocker.

## 21. What Not To Do Next

Do not add:

- OrderSend
- OrderCheck
- CTrade
- MqlTradeRequest
- MqlTradeResult
- Execution adapter
- Demo trading
- Live trading
- Phase 4 approval
- Chart attach automation
- GUI automation

Do not treat the blocked runtime signal as executable.

Do not reconstruct dry-run execution requests from blocked rows.

Do not imply replay sweep mode is execution automation. It is not.

Do not imply synthetic balance rows are real account evidence. They are not.

## 22. Exact Commands For Current Verification

Repo state:

- cd C:\Users\equin\Documents\institutional-ea
- .\.venv\Scripts\Activate.ps1
- git status
- git log --oneline -10

Full test suite:

- python -m pytest -q

Expected latest full-test anchor:

- 962 passed in 26.86s

Static EA verifier:

- python scripts\verify_h024_ea_source_static.py

Expected:

- Violations: 0
- Verdict: PASS

Compile/copy EA:

- python scripts\run_h024_mt5_log_only_preflight_local.py --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" --cent-account-symbols

Expected acceptable:

- MetaEditor compile return code: 1
- EX5 refreshed: True
- Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

## 23. Immediate First Action For Next AI

Ask the user to run:

- cd C:\Users\equin\Documents\institutional-ea
- .\.venv\Scripts\Activate.ps1
- git status
- git log --oneline -10

Expected after this handoff is committed and pushed:

- On branch main
- Your branch is up to date with origin/main
- Untracked files: reports/
- Latest commit: Add handoff document #88
- Latest code commit before handoff: fb95bd9 Add H024 synthetic balance diagnostic

## 24. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_88.

I understand:

- H024 remains research-only and is not demo/live/Phase 4 approved.
- No execution adapter, no OrderSend, no OrderCheck, no CTrade, no MqlTradeRequest.
- The Exness Standard Cent route uses USDJPYc and XAUUSDc, normalized to USDJPY and XAUUSD.
- The real account balance observed so far is 0.00 USC.
- Replay sweep mode has been manually validated on cent symbols.
- XAUUSDc produced a log-only BLOCKED short signal with positive entry/stop during replay sweep.
- The runtime verifier was fixed in ff9f500 to allow replay-sweep marker events.
- The replay sweep runtime result was documented in fc5918c.
- A default-off synthetic balance diagnostic was implemented in fb95bd9.
- The synthetic diagnostic is log-only, research-only, and not real account evidence.
- Latest full test anchor is 962 passed in 26.86s.
- The next safe step is to run a synthetic-balance replay sweep manually in MT5, not to add execution code.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
