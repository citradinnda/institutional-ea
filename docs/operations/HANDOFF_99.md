# HANDOFF_99 — FULL SELF-CONTAINED H024 POST-CANARY READ-ONLY SUPERVISION AUTOMATED

If this handoff conflicts with any older handoff, this handoff wins.

This handoff is intentionally self-contained. A new AI must be able to continue the Institutional EA project from this document alone without opening HANDOFF_98, HANDOFF_97, chat history, or local reports first.

---

## 0. Current One-Sentence State

H024 has exactly one controlled standard-demo broker-side canary position open on Exness-MT5Trial6. The canary is XAUUSDm sell, volume 0.01, magic 240024, order/ticket/identifier 4413054432, entry deal 3788869526, open price 4728.4490000000005, SL 4817.394. Immediate post-order audit passed, later monitor passed, continue-hold lifecycle passed, observation analysis passed, supervisory state passed, and the full read-only supervision runner now automates monitor -> lifecycle -> observation analysis -> supervisor with 8/8 stages passing. No broker mutation is authorized.

Hard boundary:

- No second H024 entry order.
- No live order.
- No trading loop.
- No scaling.
- No additional symbols.
- No close/modify unless separately governed and locked.
- No committing `reports/`.

---

## 1. Project Identity And Operating Context

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project:

- Name/context: Institutional EA
- Repository: `C:\Users\equin\Documents\institutional-ea`
- Branch: `main`
- Remote: `https://github.com/citradinnda/institutional-ea.git`
- Python: 3.12.10 inside `.venv`
- Shell: Windows PowerShell
- No WSL
- MetaTrader 5 terminal is installed and usable
- Broker/demo context: Exness standard demo
- Current strategy family: `H024`
- Strategy universe: USDJPY + XAUUSD
- First broker-side canary: XAUUSDm only

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology and safety discipline on a retail stack.

Core operating principle:

A normal trader is trying to be right. This project is building a system that can survive being wrong.

Current mode:

- H024 is not deployed live.
- H024 is not live-approved.
- H024 is in post-canary read-only supervision/lifecycle governance.
- Runtime plumbing has been proven through one real standard-demo broker-side order.
- Strategy edge is not proven by this canary.

---

## 2. User Preference And Working Style

Respect these preferences:

- The user is tired of ceremonial gate proliferation and wants practical progress.
- Do not make tiny incremental changes when a fuller, higher-leverage implementation is appropriate.
- Prefer one coherent PowerShell block when giving commands.
- Avoid fragile PowerShell line continuations/backticks.
- Use boring single-line `git add -- "file1" "file2" ...`.
- For code edits, run relevant focused tests and usually the full suite.
- For docs-only edits, do not run full pytest unless there is a clear reason.
- Never commit `reports/`.
- Do not soften safety boundaries.
- Avoid unnecessary clarifying questions when the next safe step is clear.
- Keep morale grounded: strategy edge is unproven, but runtime plumbing and read-only supervision are meaningfully proven now.

---

## 3. Latest Repository State At HANDOFF_99

Latest known commits:

- `b355ca5 Add H024 canary read-only supervision runner`
- `363c41d Add H024 canary supervisory state packet`
- `88c4286 Harden H024 canary observation mark-to-market extraction`
- `11d26d4 Add H024 canary observation analysis packet`
- `357d517 Add handoff document #98`
- `0841119 Add H024 canary continue-hold lifecycle decision`
- `429d14e Add H024 canary read-only monitor packet`
- `b4b0032 Add handoff document #97`
- `56ca951 Handle H024 canary no-fill retry ledger states`
- `9c81d7d Add H024 one-shot demo canary execution path`

Expected after this handoff is committed:

- Branch: `main`
- Up to date with `origin/main`
- Latest commit should be `Add handoff document #99`
- Untracked `reports/` only
- No modified tracked files

Never commit:

- `reports/`
- raw MT5 exports
- runtime JSON/JSONL files
- local logs
- terminal data files
- local compile logs

---

## 4. Canonical Canary Facts

There is exactly one H024 standard-demo broker-side canary.

Canonical canary identity:

- Server: `Exness-MT5Trial6`
- Account currency: `USD`
- Runtime symbol: `XAUUSDm`
- Model symbol: `XAUUSD`
- Side: sell
- MT5 type: `1`
- Volume: `0.01`
- Magic: `240024`
- Order/ticket/identifier: `4413054432`
- Entry deal: `3788869526`
- Request id: `3072064830`
- Requested price: `4728.367`
- Fill/open price: `4728.4490000000005`
- Stop loss: `4817.394`
- Request comment: `H024_ONE_SHOT_DEMO_CANARY`
- MT5 stored/truncated comment: `H024_ONE_SHOT_DE`
- Order check retcode: `0`
- Order send retcode: `10009`
- Margin from order check: `2.36`

The successful command was:

```powershell
python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER

Do not run that command again.

Reason:

A successful canary already exists. Re-running would attempt a second entry if idempotency failed or was bypassed.

5. Latest Runtime Observation State

Latest known read-only supervision runner output after commit b355ca5:

Read-only supervision runner: PASS
Violations: 0
Completed stages: 8 / 8
First failed stage: None
Operator next action: read_supervisory_state_and_continue_observation
Broker mutation authorized: False
Trading loop authorized: False
USDJPY separate readiness required: True
Kill switches required before trading loop: True
Black-swan guards required before trading loop: True

All stages passed:

build_monitor: PASS
verify_monitor: PASS
build_lifecycle_decision: PASS
verify_lifecycle_decision: PASS
build_observation_analysis: PASS
verify_observation_analysis: PASS
build_supervisory_state: PASS
verify_supervisory_state: PASS

Latest mark-to-market captured in the supervisor stack:

Current price: 4747.721
Floating P/L: -19.27
Swap: 0.0
Adverse move from fill: 19.272
Adverse move fraction of stop: 0.216673

These mark-to-market values are not fixed. They change with broker price.

6. Implemented Post-Canary Layers Since HANDOFF_98
A. Observation Analysis Packet

Commit:

11d26d4 Add H024 canary observation analysis packet

Hardening commit:

88c4286 Harden H024 canary observation mark-to-market extraction

Files:

quantcore\execution\h024_one_shot_demo_canary_observation_analysis.py
scripts\build_h024_one_shot_demo_canary_observation_analysis_jsonl.py
scripts\verify_h024_one_shot_demo_canary_observation_analysis_jsonl.py
tests\test_h024_one_shot_demo_canary_observation_analysis.py
docs\operations\H024_ONE_SHOT_STANDARD_DEMO_CANARY_OBSERVATION_ANALYSIS.md

Output, local only:

reports\h024_standard_demo_one_shot_demo_canary_observation_analysis.jsonl

Purpose:

Durably records execution observations:

requested price vs fill price
slippage: 0.082
slippage adverse to sell: True
order-check margin: 2.36
MT5 comment truncation: True
lifecycle observations
mark-to-market values
explicit conclusion: plumbing validated, strategy edge not validated

It authorizes no mutation.

B. Supervisory State Packet

Commit:

363c41d Add H024 canary supervisory state packet

Files:

quantcore\execution\h024_one_shot_demo_canary_supervisory_state.py
scripts\build_h024_one_shot_demo_canary_supervisory_state_jsonl.py
scripts\verify_h024_one_shot_demo_canary_supervisory_state_jsonl.py
tests\test_h024_one_shot_demo_canary_supervisory_state.py
docs\operations\H024_ONE_SHOT_STANDARD_DEMO_CANARY_SUPERVISORY_STATE.md

Output, local only:

reports\h024_standard_demo_one_shot_demo_canary_supervisory_state.jsonl

Purpose:

Top-level read-only state machine. It consumes monitor, lifecycle, and observation analysis artifacts and emits one operational state.

Current expected state:

Supervisory verdict: PASS
Supervisory state: continue_observe_open
Operator next action: refresh_read_only_monitor_lifecycle_observation_supervisor
Broker mutation authorized: False
Trading loop authorized: False
USDJPY separate readiness required: True

Important bug fixed before commit:

The supervisor originally let an observation packet’s False mask a lifecycle packet’s tampered True mutation flag. The fix made authorization merge fail-closed: if any consumed source says mutation is authorized, supervisor fails.

C. Read-Only Supervision Runner

Commit:

b355ca5 Add H024 canary read-only supervision runner

Files:

quantcore\execution\h024_one_shot_demo_canary_read_only_supervision_run.py
scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py
tests\test_h024_one_shot_demo_canary_read_only_supervision_run.py
docs\operations\H024_ONE_SHOT_STANDARD_DEMO_CANARY_READ_ONLY_SUPERVISION_RUNNER.md

Output, local only:

reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl

Purpose:

Automates the full read-only supervision stack:

monitor -> lifecycle -> observation analysis -> supervisor -> verification

The runner stops at the first failed stage and records a fail-closed summary.

It does not import MetaTrader5 directly. It invokes the monitor script, which uses read-only MT5 calls only.

The runner authorizes no mutation.

7. Current Canonical Command For Read-Only Supervision

The next AI should use this command to refresh current state:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -12
python scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
python scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl --require-pass

Expected if still coherent:

Verdict: PASS
Completed stages: 8 / 8
Broker mutation authorized: False
Trading loop authorized: False
USDJPY separate readiness required: True
Kill switches required before trading loop: True
Black-swan guards required before trading loop: True
Only reports/ untracked
8. Safety State

Approved / true:

Exactly one H024 standard-demo canary was placed.
The order was broker-side successful on standard demo.
Immediate post-order audit passed.
Read-only monitor passed.
Continue-hold lifecycle decision passed.
Observation analysis passed.
Supervisory state passed.
Read-only supervision runner passed.
One-command read-only supervision automation exists and is committed.
Runtime plumbing is proven through a real standard-demo order.
Read-only post-canary operations are now substantially automated.

Still false / forbidden:

No second H024 entry order.
No live order.
No scaling up.
No automatic trading loop.
No unattended trading.
No additional symbols.
No USDJPY canary yet.
No additional lots.
No changing strategy family.
No new entry path.
No close/modify unless separately approved and locked.
No modifying SL/TP unless separately approved and locked.
No manual deletion/tampering with ledgers.
No committing reports/.
No treating one canary success as live deployment approval.
No treating one canary as strategy edge evidence.

Live deployment is still not close.

9. USDJPY Status

USDJPY matters. It is part of the intended H024 universe.

But USDJPY is not authorized by the XAUUSDm canary stack.

Current USDJPY rule:

USDJPY requires a separate broker-readiness path.
Expected Exness standard demo runtime symbol: USDJPYm.
Model symbol: USDJPY.
It needs broker-native data checks, symbol property checks, spread/tick sanity, H020 sizing verification, request-shape preview, and a separately governed canary decision if later justified.
Do not piggyback USDJPY on the XAUUSDm ticket, ledger, monitor, lifecycle, or supervisor.

A good next major branch is:

Add H024 USDJPY broker-readiness packet

It should be read-only and should not place orders.

10. Kill Switches / Black-Swan Guards Roadmap

The user explicitly asked when safety measures like kill switches and black-swan guards will exist.

Answer:

Yes, they are mandatory before any trading loop.

But sequencing matters:

Read-only supervision automation — now implemented.
Controlled close governance for the exact XAUUSDm canary ticket.
Global no-new-entry kill switch.
Manual override lockout file.
Daily loss lockout.
Max floating loss lockout.
Spread shock guard.
Stale tick guard.
Disconnected terminal guard.
Margin compression guard.
Volatility expansion / black-swan guard.
Unexpected position/order lockout.
Per-symbol circuit breakers for XAUUSD and USDJPY.
Only after these: any automatic trading loop.

Do not implement a trading loop before these exist.

A good next major branch after USDJPY readiness or controlled close is:

Add H024 safety supervisor kill-switch specification

This should still be read-only/specification-first unless explicitly building a lockout mechanism.

11. Controlled Close Governance

No code close is authorized by HANDOFF_99.

The user may manually manage risk in MT5.

But any code-governed close must be separately locked to:

Server: Exness-MT5Trial6
Account currency: USD
Symbol: XAUUSDm
Ticket/identifier: 4413054432
Magic: 240024
Volume: 0.01
Side: close only the existing sell canary
No extra positions
Exact acknowledgement
Idempotency close ledger
Post-close audit

Controlled close is a valid next major step if the user asks to manage/close the existing canary through code. Do not build or run it without explicit user request.

12. Strategy Mechanics Summary

H024 is a regime-conditioned pullback-continuation strategy.

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

Signal logic summary:

slow_ma = close rolling 5 mean
atr = Wilder ATR(3)
slope = slow_ma - slow_ma.shift(2)
slope_threshold = atr * 0.05
trend_up = close > slow_ma and slope > slope_threshold
trend_down = close < slow_ma and slope < -slope_threshold
previous_bearish = close.shift(1) < open.shift(1)
previous_bullish = close.shift(1) > open.shift(1)
long_signal = trend_up plus bearish pullback plus long resumption
short_signal = trend_down plus bullish pullback plus short resumption
13. H020 / H024 Sizing Boundary

H024 uses H020 sizing.

Do not bypass H020 sizing.

Do not reconstruct lots manually inside a production adapter.

Do not reinterpret:

signal sizing
stop geometry
volume step
minimum lot
maximum lot
risk fraction

H020 sizing behaviors that must remain respected:

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

For the first canary, the order was locked to:

symbol: XAUUSDm
volume: 0.01
sell
stop distance: 89.027
SL: 4817.394
magic: 240024

Do not casually change these.

14. Data And Broker Rules

Accepted validation source:

Exness demo/terminal broker-native exports/runtime only

Accepted model symbols:

USDJPY
XAUUSD

Observed standard demo runtime symbols:

USDJPYm
XAUUSDm

Observed cent account runtime symbols:

USDJPYc
XAUUSDc

Symbol normalization:

USDJPYm -> USDJPY
XAUUSDm -> XAUUSD
USDJPYc -> USDJPY
XAUUSDc -> XAUUSD

Accepted timeframes:

Broker-native H4
Broker-native M1

Broker timezone used by loader:

Europe/Athens

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
reports/*.csv
reports/*.json
reports/*.jsonl
local runtime CSVs
local compile logs
15. Known Pitfalls

PowerShell:

Avoid Bash heredocs.
Avoid fragile backtick continuations.
Use here-strings and temp scripts.
Use UTF-8 no BOM writes.
Use single-line git add.

Git:

Never commit reports/.
If reports/ is the only untracked item, this is expected.

MT5:

MT5 can reject sends with 10027 if Algo Trading is disabled.
Retcode 10009 means successful trade request execution.
MT5 may truncate comments.
Do not infer live readiness from demo success.
Do not infer strategy edge from one canary.

Semantic pitfalls:

Do not treat one demo canary as deployment.
Do not place a second canary.
Do not add automatic loops.
Do not close/modify without explicit close governance.
Do not treat H024 as live-approved.
Do not commit local runtime artifacts.
16. Best Next Major Work Options

Pick one, depending on user intent.

Option A — Continue Read-Only Supervision

Use the one-command runner.

Safe and already automated.

Option B — Controlled Close Governance

Only if the user explicitly wants a code-governed close or risk conditions require it.

Must be exact-ticket locked and separate from entry logic.

Option C — USDJPY Broker-Readiness Packet

Recommended if the user wants to bring the second symbol into the project properly.

Must be read-only. No USDJPY orders.

Should verify:

Runtime symbol USDJPYm
Model symbol USDJPY
broker account/server/currency
symbol info
spread/tick sanity
H4/M1 availability
H020 sizing feasibility
request-shape implications
no broker mutation authorization
Option D — Safety/Kill-Switch Specification

Recommended before any loop.

Should define:

global no-new-entry switch
manual override lockout
daily loss lockout
max floating loss lockout
spread shock guard
stale tick guard
disconnected terminal guard
margin compression guard
volatility expansion guard
unexpected position/order lockout
per-symbol circuit breakers

Still no trading loop.

17. Exact First Response For The Next AI

The next AI should say:

Understood. Continuing from HANDOFF_99.

H024 has exactly one controlled standard-demo canary open on Exness-MT5Trial6: XAUUSDm sell, volume 0.01, magic 240024, ticket 4413054432, entry deal 3788869526, open price 4728.4490000000005, SL 4817.394. The immediate post-order audit passed, the read-only monitor passed, the continue-hold lifecycle decision passed, observation analysis passed, supervisory state passed, and the one-command read-only supervision runner passed with 8/8 stages. No broker mutation is authorized.

The hard boundary remains: no second H024 entry, no live order, no trading loop, no scaling, no extra symbols, and no close/modify unless separately governed.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -12
python scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
python scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl --require-pass

Then paste the output and say whether the canary is still open in MT5.

18. Compact Continuation Prompt For Another AI

You are continuing the Institutional EA project from HANDOFF_99.

You are a senior quantitative engineer and mentor helping a solo retail trader on Windows build H024, a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade safety discipline.

Repository: C:\Users\equin\Documents\institutional-ea
Branch: main
Remote: https://github.com/citradinnda/institutional-ea.git
Python: 3.12.10 in .venv
Shell: Windows PowerShell
Broker/demo: Exness standard demo
Server: Exness-MT5Trial6

H024 has exactly one controlled standard-demo broker-side canary. It was not a live order. It was on Exness standard demo server Exness-MT5Trial6, symbol XAUUSDm, sell side, volume 0.01, magic 240024, request comment H024_ONE_SHOT_DEMO_CANARY truncated by MT5 to H024_ONE_SHOT_DE.

Successful canary details:

command used: python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER
attempt_stage: send_succeeded
order/ticket: 4413054432
deal: 3788869526
request id: 3072064830
requested price: 4728.367
fill/open price: 4728.4490000000005
stop loss: 4817.394
order_check_result.retcode: 0
order_send_result.retcode: 10009
volume: 0.01
side: sell / MT5 type 1
margin from order check: 2.36

Post-canary state:

immediate post-order audit: PASS
read-only monitor: PASS
lifecycle decision: continue_hold / PASS
observation analysis: PASS
supervisory state: continue_observe_open / PASS
read-only supervision runner: PASS, 8/8 stages

Latest known read-only runner commit:

b355ca5 Add H024 canary read-only supervision runner

Current runner command:

python scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
python scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl --require-pass

Hard boundaries:

Do not place another H024 entry order.
Do not run the send command again.
Do not deploy live.
Do not implement an automatic trading loop.
Do not scale volume.
Do not add USDJPY to trading yet.
Do not modify or close the canary position without separate explicit close governance.
Do not commit reports/.

USDJPY matters but requires a separate broker-readiness path for USDJPYm. It must not piggyback on the XAUUSDm canary stack.

Kill switches and black-swan guards are mandatory before any trading loop. They are not yet implemented. Good next steps are controlled close governance, USDJPY broker-readiness, or safety/kill-switch specification.
