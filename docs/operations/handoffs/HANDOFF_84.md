# HANDOFF_84 — H024 Cent-Account Feasibility Unlock and Current Research Boundary

If any older handoff conflicts with this one, this handoff wins.

This continues from HANDOFF_83, but is intended to be fully self-contained. A new AI should be able to continue safely from this document without opening older handoffs first.

---

## 0. One-Sentence State

H024 remains research-only and not deployment-approved, but the intended 10,000 USC Exness Standard Cent path is now mechanically plausible by sizing: the real account exposes `USDJPYc` and `XAUUSDc`, read-only MT5 profit probes showed representative candidates executable by size, and the pure-Python scanner now supports cent-account USC specs with `947 passed`.

---

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology on a retail stack.

Current stage:

Execution-safety preparation after H024 research evidence, now focused on the user's Exness Standard Cent account path.

Current status:

H024 is promising, but still:

- Not demo-approved
- Not live-approved
- Not Phase 4-approved
- Not approved for any order execution
- Not approved for any execution adapter
- Not approved for `OrderSend`, `OrderCheck`, `CTrade`, or `MqlTradeRequest`

The user is eager to deploy and stated they plan to start with `10k USC` for deployment.

Do not soften deployment boundaries.

---

## 2. Human Preference

The user is tired of excessive ceremony.

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

Important sentiment:

The user wants to make the EA survive the future, not fit the past.

The user is eager to deploy. The correct direct answer is:

H024 is meaningfully closer under the 10k USC cent-account route, but it is still not demo/live/Phase 4 deployable.

---

## 3. Environment

Use:

- Windows
- PowerShell
- VS Code
- Python 3.12.10 inside `.venv`
- No WSL

Repository root:

```text
C:\Users\equin\Documents\institutional-ea

Virtual environment:

C:\Users\equin\Documents\institutional-ea\.venv

Branch:

main

GitHub remote:

https://github.com/citradinnda/institutional-ea.git

MetaEditor:

C:\Program Files\MetaTrader 5\MetaEditor64.exe

Terminal data dir:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075

Terminal EA source:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.mq5

Compiled EX5:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\H024_LogOnly_Preflight.ex5

Runtime CSV in terminal:

C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\h024_ea_log_only_preflight.csv

Repo report CSVs are local and intentionally untracked.

Do not commit reports/.

4. Expected Repo State After This Handoff Is Committed

Expected:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Expected latest commit after this handoff is committed:

Add handoff document #84

Expected latest commit before HANDOFF_84 commit:

b446ed9 Add H024 cent account executable scan specs

Current full-test anchor after cent-account scanner support:

947 passed in 17.34s

Focused cent/scanner test anchor:

18 passed in 1.79s

Docs-only commits after the 947 passed anchor do not require pytest.

5. Recent Commit History

Expected recent history before HANDOFF_84 commit:

b446ed9 Add H024 cent account executable scan specs
cd3c153 Document H024 cent account feasibility probe
a2665ea Document H024 executable density thresholds
dbfca1f Expand H024 balance density symbol breakdown
011d3fc Document H024 balance executable candidate density
d1c0a63 Add handoff document #83
6b4bb40 Document H024 risk fraction comparison mode result
f0413f2 Optimize H024 threshold comparison scans
b3cd189 Clean H024 threshold comparison whitespace
782eb16 Add H024 risk fraction threshold comparison mode

Important commits created after HANDOFF_83:

011d3fc Document H024 balance executable candidate density
dbfca1f Expand H024 balance density symbol breakdown
a2665ea Document H024 executable density thresholds
cd3c153 Document H024 cent account feasibility probe
b446ed9 Add H024 cent account executable scan specs
6. Non-Negotiable Safety Boundary

H024 remains:

Research / pre-deployment only
No demo deployment approval
No live trading approval
No Phase 4 execution approval
No order-send capability approved
No execution adapter approved

Forbidden in the log-only EA and current project stage:

OrderSend
OrderSendAsync
OrderCheck
CTrade
#include <Trade...>
MqlTradeRequest
MqlTradeResult
PositionOpen
PositionClose
PositionModify
Pending order helpers

Also not approved:

EA chart attach/detach automation
GUI automation
MT5 launcher/profile mutation affecting live terminals
Order-send automation
Demo/live execution adapter
Raising risk to force executable candidates
Treating feasibility scans as deployment approval

Allowed so far:

Manual EA attach/remove
Copy EA source to terminal Experts
Compile EA with MetaEditor
Reset/collect runtime CSV
Verify runtime CSV
Summarize intended-action rows
Historical log-only replay using InpH024ClosedShift
CSV-read-only dry-run request reconciliation
Pure Python dry-run execution request contracts
Runtime BLOCKED sizing diagnostics verification
Pure Python minimum-volume feasibility summary
Pure Python executable candidate shift scanning
Pure Python exact capital threshold scanning
Pure Python risk-fraction threshold comparison
Optimized pure Python risk-fraction threshold comparison mode
Research-only documentation of threshold results
Read-only MT5 account/symbol-info probes
Read-only MT5 order_calc_profit probes
Pure Python cent-account USC feasibility scanner support
7. Current Deployment Verdict

H024 is still not approved for demo or live.

However, the deployment-relevant feasibility universe changed.

Before HANDOFF_84, the important result was:

At 100 USD / 1% risk on standard-like USDJPYm / XAUUSDm symbols, H024 had no executable historical candidate.

After HANDOFF_84, the user clarified they plan to start with:

10,000 USC

on an Exness Standard Cent account.

The real terminal account probe showed:

Account currency: USC
Available symbols: USDJPYc, XAUUSDc
Unavailable symbols: USDJPYm, XAUUSDm, USDJPY, XAUUSD
Balance at probe time: 0.0 USC

This means prior standard-symbol scans are not the final deployment authority for the cent account.

Current best answer:

The 10k USC cent-account path is mechanically plausible by size, but not deployment-approved.

The blocker has changed from:

minimum volume impossible at 100 USD standard-symbol sizing

to:

need cent-symbol log-only runtime/replay, executable runtime dry-run request, and execution-safety review
8. H024 Mechanics Summary

H024 is a regime-conditioned pullback-continuation hypothesis.

Mechanics:

Defines directional regime using slow H4 trend state.
Waits for pullback against that regime.
Enters only if price resumes in regime direction after pullback.
Does not use H021 time/session buckets.
Does not reuse Donchian breakout trigger.
Uses H020 sizing contract.
Returns H017-compatible bridge shim.
Uses H018 hard guard semantics.
Baseline candidate: hold = 3 H4, stop ATR multiple = 2.0.

Frozen signal defaults:

slow_window = 5
slope_lag = 2
atr_window = 3
pullback_window = 3
min_pullback_atr = 0.25
max_pullback_atr = 3.0
min_slope_atr = 0.05

Signal logic:

slow_ma = close.rolling(5).mean()
atr = Wilder ATR(3)
slope = slow_ma - slow_ma.shift(2)
slope_threshold = atr * 0.05

trend_up = close > slow_ma and slope > slope_threshold
trend_down = close < slow_ma and slope < -slope_threshold

previous_bearish = close.shift(1) < open.shift(1)
previous_bullish = close.shift(1) > open.shift(1)

recent_high_before_signal = high.shift(1).rolling(3).max()
recent_low_before_signal = low.shift(1).rolling(3).min()

long_pullback_depth_atr = (recent_high_before_signal - low.shift(1)) / atr.shift(1)
short_pullback_depth_atr = (high.shift(1) - recent_low_before_signal) / atr.shift(1)

long_pullback_ok = long_pullback_depth_atr between 0.25 and 3.0 inclusive
short_pullback_ok = short_pullback_depth_atr between 0.25 and 3.0 inclusive

long_resumption = close > high.shift(1)
short_resumption = close < low.shift(1)

long_signal = trend_up and previous_bearish and long_pullback_ok and long_resumption
short_signal = trend_down and previous_bullish and short_pullback_ok and short_resumption
9. H020 / H024 Sizing Boundary

H024 uses H020 sizing.

Important H020 behaviors:

Computes explicit pre-trade lot intents.
Suppresses flat signals.
Suppresses invalid stop geometry.
Suppresses stop distances below one spread.
Computes risk-based lots.
Applies per-trade gross notional caps.
Applies portfolio gross notional scaling.
Rounds lots down to broker lot step.
Suppresses lots below broker minimum lot.
Preserves final signed risk fraction from final executable lots.

Therefore, cent-account scans must not bypass H020 sizing.

The cent scanner support added after HANDOFF_83 reuses H024 signal/stop geometry, but still routes balances through H020 sizing using alternate InstrumentSpec values.

This is important:

The cent support is a performance/research-accounting change, not execution approval.

10. Current EA Facts

EA source:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5

MQL5 property version:

#property version "0.600"

Runtime schema:

h024_ea_log_only_preflight_v2

EA input version:

InpEaVersion = "0.6"

Intended-action schema:

h024_intended_action_log_v1

Important current input:

InpH024ClosedShift = 1

Meaning:

Defaults to latest closed H4 bar.
Set manually for historical replay only.
Do not automate chart attach/detach.

Current runtime intended-action behavior:

NO_ACTION rows can carry zero entry/stop/lots.
Signal rows first derive entry/stop from closed H4 bar and ATR stop.
If signal sizing is executable, row may remain WOULD_OPEN.
If signal sizing is below broker minimum volume, row becomes BLOCKED:volume_below_min_for_would_open.
BLOCKED signal rows preserve positive entry, stop, stop_distance, and raw_lots.
BLOCKED signal rows force final executable lots to 0.
Dry-run reconciler does not emit requests from BLOCKED rows.

Cent-account runtime has not yet been fully replayed/log-validated.

11. Data Rules

Accepted validation source:

Exness demo/terminal broker-native exports only

Accepted model symbols:

USDJPY
XAUUSD

Previously observed standard symbols:

USDJPYm
XAUUSDm

Current cent account symbols:

USDJPYc
XAUUSDc

Normalize for model logic:

USDJPYc -> USDJPY
XAUUSDc -> XAUUSD
USDJPYm -> USDJPY
XAUUSDm -> XAUUSD

Accepted timeframes:

Broker-native H4
Broker-native M1

Broker timezone used by loader:

Europe/Athens

DST-aware.

Do not use:

HistData for validation/tuning/production dataset creation
Broker H4 plus HistData M1 combinations
Sparse 2018 through 2021-06 broker-native prefix as dense M1
Incomplete H4/M1 windows

Do not commit:

Raw MT5 CSV files
Raw HistData files
Large derived datasets
Broker/vendor source files
Local reports/*.csv
Local reports/*.json
Local runtime CSVs
Local compile logs
12. Core Files

H024 core:

quantcore\strategy\h024.py
quantcore\strategy\h024_runner.py

H020 sizing contract:

quantcore\strategy\h020.py
tests\test_h020.py

Position sizing reference:

quantcore\strategy\h024_position_sizer.py
tests\test_h024_position_sizing.py

Execution/log contracts:

quantcore\execution\h024_intended_action_log.py
quantcore\execution\h024_dry_run_execution_request.py
quantcore\execution\h024_dry_run.py
tests\test_h024_intended_action_log_contract.py
tests\test_h024_dry_run_execution_request_contract.py
tests\test_h024_intended_action_blocked_sizing_diagnostics.py

EA/runtime:

ea_mt5\Experts\H024_LogOnly_Preflight.mq5
scripts\run_h024_mt5_log_only_preflight_local.py
scripts\verify_h024_ea_preflight_log.py
scripts\summarize_h024_ea_intended_action_runtime.py
scripts\verify_h024_ea_source_static.py
scripts\reconcile_h024_runtime_dry_run_requests.py
scripts\summarize_h024_blocked_sizing_diagnostics.py

Feasibility / capital threshold tools:

scripts\summarize_h024_min_volume_feasibility.py
scripts\scan_h024_executable_candidate_shifts.py
scripts\scan_h024_capital_thresholds.py

Cent-account scanner support:

scripts\scan_h024_executable_candidate_shifts.py
tests\test_h024_cent_account_specs.py

Feasibility / threshold tests:

tests\test_h024_min_volume_feasibility.py
tests\test_h024_executable_candidate_shift_scan.py
tests\test_h024_capital_threshold_scan.py
tests\test_h024_cent_account_specs.py

Important operation docs:

docs\operations\H024_CENT_ACCOUNT_SYMBOL_FEASIBILITY_PROBE_RESULT.md
docs\operations\H024_BALANCE_EXECUTABLE_CANDIDATE_DENSITY_RESULT.md
docs\operations\H024_100USD_1PCT_FEASIBILITY_BOUNDARY.md
docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_MODE_RESULT.md
docs\operations\H024_RISK_FRACTION_THRESHOLD_COMPARISON_RESULT.md
docs\operations\H024_EXACT_CAPITAL_THRESHOLD_RESULT.md
docs\operations\H024_CAPITAL_FEASIBILITY_FRONTIER_RESULT.md
docs\operations\H024_EXECUTABLE_CANDIDATE_SHIFT_SCAN_RESULT.md
docs\operations\H024_MIN_VOLUME_FEASIBILITY_RESULT.md
docs\operations\H024_BLOCKED_SIZING_DIAGNOSTICS_RUNTIME_RESULT.md
docs\operations\H024_EA_INTENDED_ACTION_RUNTIME_RESULT.md
docs\operations\H024_EA_LOG_ONLY_PREFLIGHT_RESULT.md
docs\operations\H024_EA_STATE_OBSERVATION_PARITY_RESULT.md
docs\operations\H024_EA_LOG_ONLY_STRATEGY_INTENT_RUNTIME_RESULT.md
docs\operations\H024_EA_STRATEGY_INTENT_DEDUP_RUNTIME_RESULT.md
docs\operations\H024_EA_WOULD_OPEN_SYNTHETIC_VALIDATION_RESULT.md
docs\operations\H024_DRY_RUN_EA_SAFETY_PLAN.md
docs\operations\H024_DRY_RUN_ACTION_EXPORT_RESULT.md
docs\operations\handoffs\HANDOFF_83.md
docs\operations\handoffs\HANDOFF_84.md
13. Evidence Reality Before HANDOFF_84

Already true before this handoff:

H024 backtest is promising.
Broker-cost reconciliation passed.
MT5 order-behavior facts were audited statically/read-only.
Python terminal/account preflight passed.
Log-only EA exists.
EA compiles into refreshed EX5.
EA has no order-send path.
EA logs runtime preflight rows.
EA logs intended-action header and row events.
Runtime intended-action NO_ACTION rows were observed in real current log-only runtime.
Strict --require-would-open gate exists.
Historical log-only replay previously observed WOULD_OPEN path.
Dry-run request contract exists in pure Python.
Runtime CSV to dry-run request reconciler exists and is CSV-read-only.
Reconciler correctly rejects non-executable rows.
EA derives entry/stop for signal rows.
EA converts under-min-volume signal rows into BLOCKED, not fake WOULD_OPEN.
BLOCKED signal rows preserve sizing diagnostics.
Runtime replay proved positive entry/stop/stop-distance/raw-lots are preserved on BLOCKED rows.
A reusable verifier exists for BLOCKED sizing diagnostics.
A regression test ensures positive BLOCKED diagnostics cannot become dry-run requests.
Minimum-volume feasibility is quantified.
A reusable executable candidate shift scanner exists.
At 100 USD / 1% risk on standard-like m specs, no historical H024 candidate survives sizing into an executable candidate.
A reusable exact capital threshold scanner exists.
At 1% risk on standard-like specs, ANY / USDJPY first executable historical candidate appears at 245 USD.
At 1% risk on standard-like specs, XAUUSD first executable historical candidate appears at 935 USD.
Optimized risk-fraction threshold comparison exists.
HANDOFF_83 was committed.
14. What Changed Since HANDOFF_83
14.1 Preserved Balance Executable Candidate Density

Commit:

011d3fc Document H024 balance executable candidate density

Result at 1% risk on standard-like specs:

100 USD: 0 rows
120 USD: 0 rows
123 USD: 0 rows
164 USD: 0 rows
245 USD: 1 row
327 USD: 16 rows
490 USD: 174 rows
550 USD: 215 rows
935 USD: 569 rows
1000 USD: 595 rows

Interpretation at that time:

245 USD was only a threshold blip.
490 to 550 USD was meaningful USDJPY density.
935 to 1000 USD was where XAUUSD technically began.
14.2 Added Symbol Density Breakdown

Commit:

dbfca1f Expand H024 balance density symbol breakdown

Symbol breakdown showed:

245-550 USD: USDJPY-only
935 USD: 568 USDJPY, 1 XAUUSD
1000 USD: 591 USDJPY, 4 XAUUSD
10000 USD: 669 USDJPY, 695 XAUUSD

Interpretation:

Sub-1k standard-like balances were not serious dual-symbol deployment envelopes.

14.3 Added Wider Density Threshold Sweep

Commit:

a2665ea Document H024 executable density thresholds

Density thresholds at 1% risk on standard-like specs:

Target    ANY threshold    USDJPY threshold    XAUUSD threshold
>= 1 row    245 USD    245 USD    935 USD
>= 10 rows    327 USD    327 USD    1250 USD
>= 50 rows    400 USD    400 USD    1500 USD
>= 100 rows    450 USD    450 USD    1500 USD
>= 200 rows    550 USD    550 USD    2000 USD
>= 500 rows    900 USD    900 USD    5000 USD

Interpretation:

USDJPY became usable much earlier than XAUUSD.
Serious dual-symbol feasibility required far more than 1k standard-like balance.
14.4 User Clarified Deployment Plan: 10k USC

The user said:

fyi im gonna start with 10k usc for the deployment

This changed the relevant symbol/account universe.

14.5 Read-Only MT5 Cent Account Probe

Observed account:

login=183959028
server=Exness-MT5Real25
currency=USC
balance=0.0
equity=0.0
leverage=2000

Observed symbols:

USDJPYc: FOUND
XAUUSDc: FOUND
USDJPYm: NOT_FOUND
XAUUSDm: NOT_FOUND
USDJPY: NOT_FOUND
XAUUSD: NOT_FOUND

Observed USDJPYc spec:

trade_mode=4
currency_base=USD
currency_profit=JPY
currency_margin=USD
digits=3
point=0.001
trade_contract_size=1000.0
volume_min=0.01
volume_step=0.01
volume_max=200.0
trade_tick_size=0.001
trade_tick_value=0.6381865291587425
trade_tick_value_profit=0.6381865291587425
trade_tick_value_loss=0.63825984834946
spread=18

Observed XAUUSDc spec:

trade_mode=4
currency_base=XAU
currency_profit=USD
currency_margin=XAU
digits=3
point=0.001
trade_contract_size=1.0
volume_min=0.01
volume_step=0.01
volume_max=200.0
trade_tick_size=0.001
trade_tick_value=0.1
trade_tick_value_profit=0.1
trade_tick_value_loss=0.1
spread=360
14.6 Read-Only MT5 Profit/Loss Probe

Commit preserving result:

cd3c153 Document H024 cent account feasibility probe

Probe assumptions:

target_balance_for_probe=10000.00 USC
risk_fraction=0.0100
risk_budget=100.00 USC

No order execution. Used only mt5.order_calc_profit.

USDJPYc representative candidate:

symbol=USDJPYc
side=sell
entry=110.015
stop=110.2840593855
contract_size=1000.0
volume_min=0.01
volume_step=0.01
loss_per_1_lot_at_stop=171.730000 USC
loss_per_min_lot_at_stop=1.720000 USC
raw_lots_for_1pct=0.582309
final_lots_after_step=0.580000
final_loss_at_stop=99.600000 USC
final_risk_fraction=0.0099600000
verdict=WOULD_BE_EXECUTABLE_BY_SIZE

XAUUSDc representative candidate:

symbol=XAUUSDc
side=sell
entry=1913.59
stop=1922.9379866787
contract_size=1.0
volume_min=0.01
volume_step=0.01
loss_per_1_lot_at_stop=934.800000 USC
loss_per_min_lot_at_stop=9.300000 USC
raw_lots_for_1pct=0.106975
final_lots_after_step=0.100000
final_loss_at_stop=93.500000 USC
final_risk_fraction=0.0093500000
verdict=WOULD_BE_EXECUTABLE_BY_SIZE

Interpretation:

The cent-account path appears to solve the prior minimum-volume blocker for representative USDJPY and XAUUSD candidates.

14.7 Added Cent Account Executable Scan Specs

Commit:

b446ed9 Add H024 cent account executable scan specs

Changed files:

scripts\scan_h024_executable_candidate_shifts.py
tests\test_h024_cent_account_specs.py

New scanner constant:

CENT_ACCOUNT_USC_INSTRUMENT_SPECS

Purpose:

Allow the existing pure-Python H024 executable candidate scanner to route H020 sizing through Exness Standard Cent account USC specs.

The scanner keeps model symbols normalized:

USDJPY
XAUUSD

but uses cent-account sizing assumptions.

Important modeling detail:

The cent specs keep H020's numeric accounting in account-currency units (USC).

The user's cent account exposes USDJPYc and XAUUSDc, but the H024 research signal geometry remains normalized to USDJPY / XAUUSD.

Contract sizes are therefore scaled into USC-equivalent accounting:

USDJPYc MT5 contract size is 1,000 USD.
H020 converts JPY P/L to account units using the historical USDJPY price.
Multiply by 100 to express result in USC rather than USD:
1,000 * 100 = 100,000.

XAUUSDc MT5 contract size is 1 oz.
H020 sees USD quote P/L.
Multiply by 100 to express result in USC:
1 * 100 = 100.

Cent specs:

CENT_ACCOUNT_USC_INSTRUMENT_SPECS = {
    "USDJPY": InstrumentSpec(
        symbol="USDJPY",
        contract_size=100_000.0,
        quote_currency="JPY",
        lot_step=0.01,
        min_lot=0.01,
    ),
    "XAUUSD": InstrumentSpec(
        symbol="XAUUSD",
        contract_size=100.0,
        quote_currency="USD",
        lot_step=0.01,
        min_lot=0.01,
    ),
}

New scanner flag:

--cent-account-usc-specs

New tests:

tests\test_h024_cent_account_specs.py

Test coverage:

canonical rows remain blocked with default specs at 100 USD
cent USC specs make canonical rows executable at 10000 USC
cent USC specs document observed cent contract accounting

Focused tests after change:

18 passed in 1.79s

Full tests after change:

947 passed in 17.34s
14.8 Cent Account Full Historical Feasibility Scan

Command run:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 10000 `
  --risk-fraction 0.01 `
  --cent-account-usc-specs `
  --output-csv reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv `
  --max-rows 10

Observed output:

H024 executable candidate shift scan
========================================================================
Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.

balance: 10000.00
risk_fraction: 0.010000
instrument_specs: Exness Standard Cent USC specs
executable_candidate_rows: 1364
wrote: reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv

First candidate rows:
XAUUSD sell | decision=2018-07-22 21:00:00+00:00 entry=2018-07-23 21:00:00+00:00 ea_closed_shift=8677 final_risk=-0.008008183852 entry_price=1224.2110000000 stop_price=1244.2314596288
XAUUSD sell | decision=2018-08-05 21:00:00+00:00 entry=2018-08-06 21:00:00+00:00 ea_closed_shift=8665 final_risk=-0.009944268186 entry_price=1208.6910000000 stop_price=1228.5795363717
USDJPY sell | decision=2018-08-07 21:00:00+00:00 entry=2018-08-08 21:00:00+00:00 ea_closed_shift=8663 final_risk=-0.009105292033 entry_price=110.9040000000 stop_price=112.0260147862
XAUUSD sell | decision=2018-08-14 21:00:00+00:00 entry=2018-08-15 21:00:00+00:00 ea_closed_shift=8657 final_risk=-0.008487003145 entry_price=1173.7500000000 stop_price=1194.9675078635
XAUUSD buy | decision=2018-08-23 21:00:00+00:00 entry=2018-08-25 21:00:00+00:00 ea_closed_shift=8649 final_risk=0.009604635126 entry_price=1206.4700000000 stop_price=1182.4584121859
XAUUSD sell | decision=2018-09-03 21:00:00+00:00 entry=2018-09-04 21:00:00+00:00 ea_closed_shift=8640 final_risk=-0.008129273787 entry_price=1191.9900000000 stop_price=1212.3131844664
XAUUSD sell | decision=2018-09-06 21:00:00+00:00 entry=2018-09-08 21:00:00+00:00 ea_closed_shift=8637 final_risk=-0.008291519428 entry_price=1195.0100000000 stop_price=1215.7387985688
USDJPY buy | decision=2018-09-12 21:00:00+00:00 entry=2018-09-13 21:00:00+00:00 ea_closed_shift=8632 final_risk=0.009968071067 entry_price=112.0220000000 stop_price=110.9053567430
USDJPY buy | decision=2018-09-17 21:00:00+00:00 entry=2018-09-18 21:00:00+00:00 ea_closed_shift=8628 final_risk=0.009438809977 entry_price=112.2790000000 stop_price=111.2192198546
XAUUSD sell | decision=2018-09-25 21:00:00+00:00 entry=2018-09-26 21:00:00+00:00 ea_closed_shift=8621 final_risk=-0.009607590133 entry_price=1196.4080000000 stop_price=1215.6231802653

Verdict: PASS
Candidates found only for replay planning; no execution approval implied.

Interpretation:

At 10000 USC / 1% using cent-account USC specs, the historical executable candidate count is:

1364

This includes both USDJPY and XAUUSD.

This is the strongest feasibility result so far for the intended deployment account type.

15. Current Answer Key

If asked "are we ready to demo/live?":

No.

If asked "are we officially Phase 4?":

No.

If asked "did the 10k USC cent account solve the old minimum-volume blocker?":

It appears to solve the sizing/min-volume feasibility blocker in pure-Python scanner and read-only MT5 profit probes, but it does not approve deployment.

If asked "what is the latest full-test anchor?":

947 passed in 17.34s

If asked "what is the latest commit before HANDOFF_84?":

b446ed9 Add H024 cent account executable scan specs

If asked "what changed from HANDOFF_83?":

The relevant deployment account is now an Exness Standard Cent USC account with USDJPYc and XAUUSDc, not standard m symbols. Read-only MT5 profit probes and scanner support show the 10k USC path is mechanically plausible by size.

If asked "does 10k USC equal 10k USD?":

No. It is a cent-account balance denomination. The scanner models USC accounting through cent-contract specs, not by pretending the account is a standard USD account.

If asked "does this approve OrderSend?":

No.

If asked "what is the next gate?":

Cent-symbol log-only runtime/replay and executable runtime dry-run request reconstruction, still without order code.

If asked "what should we not do next?":

Do not add execution adapter, OrderSend, OrderCheck, CTrade, or MqlTradeRequest.

16. Current Important Commands

Verify full suite:

python -m pytest -q

Expected current anchor:

947 passed

Run focused cent/scanner tests:

python -m pytest `
  tests\test_h024_cent_account_specs.py `
  tests\test_h024_executable_candidate_shift_scan.py `
  tests\test_h024_capital_threshold_scan.py `
  -q

Expected focused anchor:

18 passed

Run cent-account 10k USC executable candidate scan:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 10000 `
  --risk-fraction 0.01 `
  --cent-account-usc-specs `
  --output-csv reports\h024_executable_candidate_shifts_10000usc_1pct_cent_specs.csv `
  --max-rows 10

Expected:

instrument_specs: Exness Standard Cent USC specs
executable_candidate_rows: 1364
Verdict: PASS

Run standard default scan for contrast:

python scripts\scan_h024_executable_candidate_shifts.py `
  --balance 100 `
  --risk-fraction 0.01 `
  --output-csv reports\h024_executable_candidate_shifts_100usd_1pct.csv `
  --max-rows 5

Expected:

executable_candidate_rows: 0
Verdict: PASS
Scan completed; no executable candidate shifts found at these settings.
17. What Remains Missing

Critical missing evidence:

Account is currently unfunded in the probe: balance=0.0 USC.
No cent-symbol H024 log-only runtime replay has been completed.
No executable runtime dry-run request has been reconstructed from cent-symbol runtime CSV.
No execution safety review after cent feasibility.
No demo execution adapter exists.
No order placement behavior has been tested.
No order rejection behavior has been tested.
No requote/slippage behavior has been tested.
No position reconciliation exists.
No kill-switch-to-execution boundary has been implemented.
No demo approval.
No live approval.
No Phase 4 approval.
2023 weakness remains real.
18. Recommended Next Work

Best next technical step:

Do not add execution code.

Recommended next safe work:

Preserve the cent-account scanner result in an operation doc if desired.
Inspect and adapt log-only EA/runtime workflow for USDJPYc / XAUUSDc symbol suffix handling.
Run cent-symbol log-only runtime/replay manually.
Verify runtime intended-action rows.
Reconcile runtime CSV into dry-run requests.
Only after an executable cent-symbol runtime dry-run request exists, perform a separate execution safety review.

Do not jump directly to:

OrderSend
OrderCheck
CTrade
MqlTradeRequest
Execution adapter
Demo trading
Live trading
Phase 4
Chart automation
GUI automation
19. Immediate First Action For Next AI

Ask the user to run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected after this handoff is committed:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Expected latest commit:

Add handoff document #84

Then continue from the actual repo state, not from assumptions.

20. Exact First Response The Next AI Should Give

Understood. Continuing from HANDOFF_84.

I understand:

Windows / PowerShell / VS Code / Python 3.12.10 in .venv.
Branch should be main, pushed, tracked tree clean except local reports/.
Current full-test anchor is 947 passed.
Latest pre-handoff code commit is b446ed9 Add H024 cent account executable scan specs.
H024 is still not demo-approved, not live-approved, and not Phase 4-approved.
No OrderSend, no OrderCheck, no CTrade, no MqlTradeRequest, no execution adapter.
User intends to start with 10k USC.
Real terminal account is USC cent account on Exness-MT5Real25; probe balance was 0.0 USC.
Available account symbols are USDJPYc and XAUUSDc; USDJPYm, XAUUSDm, USDJPY, and XAUUSD were not found.
Read-only MT5 order_calc_profit showed representative USDJPYc and XAUUSDc candidates executable by size at 10000 USC / 1%.
The scanner now supports --cent-account-usc-specs.
At 10000 USC / 1% with cent-account USC specs, the scanner found 1364 executable historical candidates.
This solves the prior sizing/min-volume feasibility blocker for the intended cent-account path, but does not approve deployment.
Next safe gate is cent-symbol log-only runtime/replay and executable runtime dry-run request reconstruction.
reports/ stays untracked.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Then paste the full output.
