# HANDOFF_100 — FULL SELF-CONTAINED H024 POST-CANARY STATE: READ-ONLY SUPERVISION AUTOMATED, XAUUSD CANARY OPEN, USDJPY NOT YET AUTHORIZED

If this handoff conflicts with any older handoff, this handoff wins.

This handoff is intentionally self-contained. It includes:

1. The complete current-state layer after HANDOFF_98.
2. The post-HANDOFF_98 commits and runtime outputs.
3. The exact current operating boundary.
4. A fully carried-forward prior base handoff appended verbatim below.

A new AI must be able to continue from this file alone without opening HANDOFF_99, HANDOFF_98, HANDOFF_97, chat history, or local runtime reports.

Important corrective note:

- A previous `HANDOFF_99.md` was accidentally committed under `docs/operations/`.
- That path was wrong for the handoff series.
- This HANDOFF_100 replaces it as the authoritative handoff.
- The corrective commit should delete the misplaced `docs/operations/HANDOFF_99.md`.

---

## 0. Current One-Sentence State

H024 has exactly one controlled standard-demo broker-side canary position open on Exness-MT5Trial6. The canary is XAUUSDm sell, volume 0.01, magic 240024, order/ticket/identifier 4413054432, entry deal 3788869526, open price 4728.4490000000005, SL 4817.394. The immediate post-order audit passed, the read-only monitor passed, the continue-hold lifecycle decision passed, observation analysis passed, supervisory state passed, and the full one-command read-only supervision runner now automates monitor -> lifecycle -> observation analysis -> supervisor with 8/8 stages passing. No broker mutation is authorized.

Hard boundary:

- No second H024 entry order.
- No live order.
- No trading loop.
- No scaling.
- No additional symbols.
- No USDJPY order yet.
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
- Read-only post-canary supervision is now automated.
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
- The user wants “big steps” that materially move the project forward.

---

## 3. Latest Repository State At HANDOFF_100

Latest known commits before this corrective handoff:

- `03fc3ce Add handoff document #99` — misplaced in `docs/operations/`; should be removed by this corrective commit.
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
- `f9451e6 Add H024 final demo canary pre-dispatch gates`
- `a2dfc76 Add H024 demo-order canary hard-controls preflight`

Expected after this HANDOFF_100 corrective commit:

- Branch: `main`
- Up to date with `origin/main`
- Latest commit should be something like `Replace misplaced handoff #99 with full handoff #100`
- Misplaced `docs/operations/HANDOFF_99.md` removed
- Correct `HANDOFF_100.md` created beside the existing handoff series
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

The successful broker-side send command was:

```powershell
python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER

Do not run that command again.

Reason:

A successful canary already exists. Re-running would attempt a second entry if idempotency failed or was bypassed.

5. Latest Runtime Observation State

Latest known one-command read-only supervision run output after commit b355ca5:

Wrote reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl
Verdict: PASS
Violations: 0
Completed stages: 8 / 8
First failed stage: None
Operator next action: read_supervisory_state_and_continue_observation
Broker mutation authorized: False
Trading loop authorized: False
USDJPY separate readiness required: True
Kill switches required before trading loop: True
Black-swan guards required before trading loop: True

All runner stages passed:

build_monitor: PASS
verify_monitor: PASS
build_lifecycle_decision: PASS
verify_lifecycle_decision: PASS
build_observation_analysis: PASS
verify_observation_analysis: PASS
build_supervisory_state: PASS
verify_supervisory_state: PASS

Latest mark-to-market captured by the supervisor stack:

Current price: 4747.721
Floating P/L: -19.27
Swap: 0.0
Adverse move from fill: 19.272
Adverse move fraction of stop: 0.216673

These mark-to-market values are not fixed. They change with broker price.

6. Validation Since HANDOFF_98

Observation-analysis implementation:

Focused tests: 7 passed
Initial build/verifier: PASS, but mark-to-market printed as None
Full suite after initial observation packet: 1401 passed
Commit: 11d26d4 Add H024 canary observation analysis packet

Observation-analysis hardening:

Fixed recursive mark-to-market extraction
Added requirement that open-state observation packets expose current price, floating P/L, and swap
Focused tests: 9 passed
Grouped canary tests: 37 passed
Full suite: 1403 passed
Commit: 88c4286 Harden H024 canary observation mark-to-market extraction

Supervisory state packet:

Initial test exposed important merge bug: lifecycle mutation True could be masked by observation False
Fixed authorization merge to fail closed if any consumed packet says mutation is authorized
Focused tests: 9 passed
Grouped canary/supervisor tests: 46 passed
Full suite: 1412 passed
Runtime supervisor: PASS / continue_observe_open
Commit: 363c41d Add H024 canary supervisory state packet

Read-only supervision runner:

Focused runner tests: 7 passed
Runner runtime: PASS, 8 / 8 stages
Verifier: PASS
Grouped canary/supervision tests: 53 passed
Full suite: 1419 passed
Commit: b355ca5 Add H024 canary read-only supervision runner

Misplaced handoff:

Commit 03fc3ce Add handoff document #99 created docs/operations/HANDOFF_99.md
User correctly rejected it as too thin and in the wrong directory
This HANDOFF_100 corrective commit should remove it and create a full self-contained handoff in the correct handoff directory
7. Implemented Post-Canary Layers Since HANDOFF_98
A. Observation Analysis Packet

Commits:

11d26d4 Add H024 canary observation analysis packet
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

The supervisor originally allowed an observation packet’s False to mask a lifecycle packet’s tampered True mutation flag. The fix made authorization merge fail-closed: if any consumed source says mutation is authorized, the supervisor fails.

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

Stage order:

build monitor
verify monitor
build lifecycle decision
verify lifecycle decision
build observation analysis
verify observation analysis
build supervisory state
verify supervisory state

The runner stops at the first failed stage and records a fail-closed summary.

It does not import MetaTrader5 directly. It invokes the monitor script, which uses read-only MT5 calls only.

The runner authorizes no mutation.

8. Current Canonical Command For Read-Only Supervision

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
9. Current Safety State

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

10. USDJPY Status

USDJPY matters. It is part of the intended H024 universe.

But USDJPY is not authorized by the XAUUSDm canary stack.

Current USDJPY rule:

USDJPY requires a separate broker-readiness path.
Expected Exness standard demo runtime symbol: USDJPYm.
Model symbol: USDJPY.
It needs broker-native data checks, symbol property checks, spread/tick sanity, H020 sizing verification, request-shape preview, and a separately governed canary decision if later justified.
Do not piggyback USDJPY on the XAUUSDm ticket, ledger, monitor, lifecycle, supervisor, or read-only runner.

A good next major branch is:

Add H024 USDJPY broker-readiness packet

It should be read-only and should not place orders.

11. Kill Switches / Black-Swan Guards Roadmap

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

12. Controlled Close Governance

No code close is authorized by HANDOFF_100.

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

13. Strategy Mechanics Summary

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
14. H020 / H024 Sizing Boundary

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

15. Data And Broker Rules

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
16. Known Pitfalls

PowerShell:

Avoid Bash heredocs.
Avoid fragile backtick continuations.
Use here-strings and temp scripts.
Use UTF-8 no BOM writes.
Use single-line git add.

Git:

Never commit reports/.
If reports/ is the only untracked item, this is expected.
Do not rewrite pushed history for this handoff correction; use a corrective commit.

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
17. Best Next Major Work Options

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
spread and tick sanity
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

18. Exact First Response For The Next AI

The next AI should say:

Understood. Continuing from HANDOFF_100.

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

19. Compact Continuation Prompt For Another AI

You are continuing the Institutional EA project from HANDOFF_100.

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

20. Full Base Context Is Included Below

The complete prior handoff follows verbatim. It is intentionally retained in this HANDOFF_100 document so future context does not depend on a prior file.nnFULL PRIOR HANDOFF BASE CONTEXT CARRIED FORWARD VERBATIM FROM: # HANDOFF_97 — H024 First Standard-Demo Canary Successfully Placed, Immediate Post-Order Audit PASS

If this handoff conflicts with any older handoff, this handoff wins.

This handoff is intentionally self-contained. A new AI must be able to continue safely without opening HANDOFF_96 or older handoffs first.

## 0. One-Sentence State

H024 has now crossed the first real broker-side standard-demo canary boundary: exactly one locked 0.01-lot XAUUSDm sell canary order was successfully placed on the Exness standard demo server `Exness-MT5Trial6`, with magic `240024`, MT5 order/ticket `4413054432`, deal `3788869526`, open price `4728.4490000000005`, SL `4817.394`, and an immediate read-only post-order audit verified exactly one open H024 canary position with zero violations. No second H024 entry order is allowed, no live trading is allowed, no automation loop is allowed, and the next safe work is read-only monitoring plus lifecycle/close governance.

## 1. Project Identity

You are acting as a senior quantitative engineer and mentor to a solo retail trader on Windows.

Project name/context:

- Institutional EA
- Repository: `C:\Users\equin\Documents\institutional-ea`
- Branch: `main`
- GitHub remote: `https://github.com/citradinnda/institutional-ea.git`
- Python: 3.12.10 inside `.venv`
- Shell: Windows PowerShell
- No WSL
- MetaTrader 5 terminal is installed and usable
- MT5 broker/demo context: Exness standard demo
- Current strategy family: `H024`
- Strategy universe: USDJPY + XAUUSD, but the first canary was XAUUSDm only

Project goal:

Build a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade epistemology and safety discipline on a retail stack.

Current state:

- H024 has progressed from research/readiness into a first controlled standard-demo broker-side canary.
- It is still not deployed.
- It is still not live-approved.
- It is still not allowed to place a second H024 entry.
- It is still not allowed to run an automated trading loop.
- It is still not allowed to scale volume.
- It is now in post-canary observation/lifecycle-governance mode.

Core operating principle:

A normal trader is trying to be right. This project is building a system that can survive being wrong.

## 2. User Preference And Working Style

The user is tired of ceremonial gate proliferation and wants practical progress.

Respect these preferences:

- Do not make tiny incremental changes when a fuller, higher-leverage implementation is appropriate.
- Prefer one coherent PowerShell block when giving commands.
- Avoid fragile PowerShell line continuations/backticks.
- Use boring single-line `git add -- "file1" "file2" ...`.
- For code edits, run relevant focused tests and usually the full suite.
- For docs-only edits, do not run full pytest unless there is a clear reason.
- Never commit `reports/`.
- Do not soften safety boundaries.
- Avoid asking unnecessary clarifying questions when the next safe step is clear.
- Keep morale grounded: strategy edge is still unproven in deployment, but runtime plumbing is meaningfully proven now.

## 3. Exact Repository State To Verify

Latest important commits known:

- `9c81d7d Add H024 one-shot demo canary execution path`
- `f9451e6 Add H024 final demo canary pre-dispatch gates`
- `a2dfc76 Add H024 demo-order canary hard-controls preflight`
- `b3fb88d Add handoff document #96`
- `8132f11 Add H024 demo-order readiness packet`
- `3288883 Add H024 MT5 request-shape preview gate`
- `846fcb2 Add H024 draft review and MT5 shape design review`
- `8747771 Add H024 broker-request draft envelope`

There may also be a later commit:

- `Handle H024 canary no-fill retry ledger states`

This commit may or may not already exist depending on whether the user completed the retry-ledger patch commit before creating this handoff. The successful broker-side retry strongly suggests the local code handled the prior `10027` no-fill ledger state correctly.

At the start of the next session, verify:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10

Expected:

Branch main
Up to date with origin/main
Untracked reports/ only
No modified tracked files, unless the no-fill retry patch remains uncommitted
If quantcore\execution\h024_one_shot_demo_canary.py or tests\test_h024_one_shot_demo_canary.py are modified, inspect and commit them after tests

Do not commit:

reports/
any raw MT5 exports
local JSON/JSONL runtime reports
local logs
any terminal data files
4. Strategy Mechanics Summary

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
5. H020 / H024 Sizing Boundary

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

Do not casually change any of these for follow-up work.

6. Data And Broker Rules

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
7. Phase/Governance Progression Before Canary

H024 had already completed these gates before the broker-side canary:

Phase 4 approved
Demo adapter implementation approved
Fail-closed skeleton implemented
Real standard-demo intent ingestion/refusal audit implemented
Adapter boundary static verifier implemented and expanded
Phase 4 demo adapter readiness packet implemented
Human adapter-readiness review decision implemented
No-op transport contract implemented
Adapter-use readiness packet implemented
Human adapter-use readiness decision implemented
Pure-Python no-op adapter-use approval implemented
No-op adapter-use invocation audit implemented
Broker-request construction readiness packet implemented
Preview-only broker-request construction approval implemented
Inert broker-request preview envelope implemented
Inert canonical broker-request draft construction approval implemented
Inert canonical broker-request draft envelope implemented
Broker-request draft review human decision implemented
MT5 request-shape design review packet implemented
MT5 request-shape construction approval implemented for inert preview only
Inert MT5 request-shape preview envelope implemented
MT5 request-shape preview review human decision implemented
Demo-order readiness packet implemented
Demo-order canary readiness human decision implemented
Canary hard-controls preflight packet implemented
Explicit one-canary human approval artifact implemented
Final inert pre-dispatch audit packet implemented
One-shot standard-demo canary execution path implemented
One-shot standard-demo canary actually invoked once
Immediate post-order audit passed

Important prior validation anchors:

Canary hard-controls preflight commit:

Commit: a2dfc76 Add H024 demo-order canary hard-controls preflight
Canary readiness human decision: PASS
Canary hard-controls preflight packet: PASS
Boundary verifier scanned 53 files
Prohibited findings: 0
Static EA verifier: PASS
Focused tests: 5 passed
Full suite: 1361 passed

Final pre-dispatch gates commit:

Commit: f9451e6 Add H024 final demo canary pre-dispatch gates
Demo-order canary human approval: PASS
Final pre-dispatch audit packet: PASS
Boundary verifier scanned 59 files
Prohibited findings: 0
Static EA verifier: PASS
Focused tests: 5 passed
Full suite: 1366 passed

One-shot execution path commit:

Commit: 9c81d7d Add H024 one-shot demo canary execution path
Source static verifier: PASS
One-shot canary tests: 7 passed
Existing boundary static verifier artifact: PASS
Boundary verifier scanned 59 files
Prohibited findings: 0
Final pre-dispatch audit packet: PASS
Full suite: 1373 passed in 24.67s
8. One-Shot Canary Implementation Files

One-shot canary implementation:

quantcore\execution\h024_one_shot_demo_canary.py
scripts\run_h024_one_shot_demo_canary.py
scripts\verify_h024_one_shot_demo_canary_source_static.py
tests\test_h024_one_shot_demo_canary.py
docs\operations\H024_ONE_SHOT_STANDARD_DEMO_CANARY_EXECUTION_PATH.md

Final canary gates:

quantcore\execution\h024_demo_order_canary_human_approval.py
quantcore\execution\h024_final_pre_dispatch_audit_packet.py
scripts\build_h024_demo_order_canary_human_approval_jsonl.py
scripts\verify_h024_demo_order_canary_human_approval_jsonl.py
scripts\build_h024_final_pre_dispatch_audit_packet_jsonl.py
scripts\verify_h024_final_pre_dispatch_audit_packet_jsonl.py
docs\operations\H024_STANDARD_DEMO_ORDER_CANARY_HUMAN_APPROVAL_RESULT.md
docs\operations\H024_FINAL_PRE_DISPATCH_AUDIT_PACKET_RESULT.md

Canary hard controls:

quantcore\execution\h024_demo_order_canary_readiness_human_decision.py
quantcore\execution\h024_demo_order_canary_hard_controls_preflight_packet.py
scripts\build_h024_demo_order_canary_readiness_human_decision_jsonl.py
scripts\verify_h024_demo_order_canary_readiness_human_decision_jsonl.py
scripts\build_h024_demo_order_canary_hard_controls_preflight_packet_jsonl.py
scripts\verify_h024_demo_order_canary_hard_controls_preflight_packet_jsonl.py

Boundary static verifier:

quantcore\execution\h024_demo_adapter_boundary_static_verifier.py
Expected latest scan count before adding monitor files: 59 files
Prohibited findings: 0

EA static verifier:

scripts\verify_h024_ea_source_static.py
EA source:
ea_mt5\Experts\H024_LogOnly_Preflight.mq5
9. One-Shot Canary Execution Path Behavior

The runner:

scripts\run_h024_one_shot_demo_canary.py

Default dry run:

python scripts\run_h024_one_shot_demo_canary.py

Dry run behavior:

Imports MetaTrader5
Calls mt5.initialize
Reads final pre-dispatch audit packet
Reads terminal account/symbol/tick state
Builds request
Does not call order_check
Does not call order_send
Prints request
Calls mt5.shutdown

Send path:

python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER

Send behavior:

Requires exact acknowledgement string
Requires final pre-dispatch audit PASS
Requires server Exness-MT5Trial6
Requires account currency USD
Requires symbol XAUUSDm
Requires volume 0.01
Requires max lot cap 0.01
Requires SL distance 89.027
Requires no existing XAUUSDm position
Requires no existing XAUUSDm pending order
Requires idempotency ledger not to contain prior successful canary
Calls order_check
Calls order_send
Appends result to:
reports/h024_standard_demo_one_shot_demo_canary_ledger.jsonl

Do not run send again.

10. The 10027 Incident And Ledger Patch

First send attempt failed with:

Refused: order_send_failed_retcode_10027

Interpretation:

MT5 terminal-side Algo Trading was disabled.
This was not a strategy failure.
This was not a broker fill.
This was a client-terminal no-fill refusal.

After enabling Algo Trading, retry succeeded.

Important patch behavior:

10027 no-fill refusal may be retried.
Unknown send attempts must block retry.
A successful canary must be ledgered as send_succeeded.
Future repeated sends must be blocked.
A legacy ledger row with attempt_stage = send_attempted and order_send_result.retcode = 10027 should be classified as known no-fill and allowed to retry once.
Any actual successful prior send must block.

If the patch is uncommitted, commit it with:

python -m pytest -q tests\test_h024_one_shot_demo_canary.py
python scripts\verify_h024_one_shot_demo_canary_source_static.py
python -m pytest -q
git add -- "quantcore\execution\h024_one_shot_demo_canary.py" "tests\test_h024_one_shot_demo_canary.py"
git diff --cached --check
git commit -m "Handle H024 canary no-fill retry ledger states"
git push

Do this only if git status shows those files modified.

11. Successful Broker-Side Canary Event

The actual successful command was:

python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER

Successful output:

{
  "allowed_demo_server": "Exness-MT5Trial6",
  "attempt_stage": "send_succeeded",
  "canary_comment": "H024_ONE_SHOT_DEMO_CANARY",
  "generated_at_utc": "2026-05-11T15:51:39Z",
  "order_check_result": {
    "balance": 10000.0,
    "comment": "Done",
    "equity": 10000.0,
    "margin": 2.36,
    "margin_free": 9997.64,
    "margin_level": 423728.81355932204,
    "profit": 0.0,
    "retcode": 0
  },
  "order_send_result": {
    "ask": 4728.7570000000005,
    "bid": 4728.4490000000005,
    "comment": "H024_ONE_SHOT_DE",
    "deal": 3788869526,
    "order": 4413054432,
    "price": 4728.4490000000005,
    "request_id": 3072064830,
    "retcode": 10009,
    "retcode_external": 0,
    "volume": 0.01
  },
  "request": {
    "action": 1,
    "comment": "H024_ONE_SHOT_DEMO_CANARY",
    "deviation": 50,
    "magic": 240024,
    "price": 4728.367,
    "sl": 4817.394,
    "symbol": "XAUUSDm",
    "type": 1,
    "type_filling": 1,
    "type_time": 0,
    "volume": 0.01
  },
  "strategy": "H024",
  "symbol": "XAUUSDm"
}

Interpretation:

attempt_stage: send_succeeded
order_send_result.retcode: 10009
MT5 send succeeded
order_check_result.retcode: 0
Symbol: XAUUSDm
Side: sell, because MT5 type 1
Volume: 0.01
Magic: 240024
Request comment: H024_ONE_SHOT_DEMO_CANARY
MT5 stored/truncated comment: H024_ONE_SHOT_DE
Requested price: 4728.367
Fill price: 4728.4490000000005
SL: 4817.394
Deal: 3788869526
Order/ticket: 4413054432
Request ID: 3072064830
Margin from order check: 2.36

This is the first successful H024 broker-side standard-demo canary.

12. Immediate Post-Order Audit

After the successful send, a read-only audit script was run.

Audit file written locally:

reports/h024_standard_demo_one_shot_demo_canary_post_order_audit.jsonl

Do not commit this file.

Audit output:

Wrote reports\h024_standard_demo_one_shot_demo_canary_post_order_audit.jsonl
Verdict: PASS
Violations: 0
Open canary positions found: 1

Verified open position:

{
  "comment": "H024_ONE_SHOT_DE",
  "external_id": "",
  "identifier": 4413054432,
  "magic": 240024,
  "price_current": 4731.158,
  "price_open": 4728.4490000000005,
  "profit": -2.71,
  "reason": 3,
  "sl": 4817.394,
  "swap": 0.0,
  "symbol": "XAUUSDm",
  "ticket": 4413054432,
  "time": 1778514693,
  "time_msc": 1778514693230,
  "time_update": 1778514693,
  "time_update_msc": 1778514693230,
  "tp": 0.0,
  "type": 1,
  "volume": 0.01
}

Audit interpretation:

Post-order audit verdict: PASS
Violations: 0
Exactly one open H024 canary position found
Ticket/order: 4413054432
Identifier: 4413054432
Symbol: XAUUSDm
Magic: 240024
Type: 1 sell
Volume: 0.01
Open price: 4728.4490000000005
Current price at audit: 4731.158
Floating P/L at audit: -2.71
SL: 4817.394
TP: 0.0
Swap: 0.0
Comment: H024_ONE_SHOT_DE

This audit confirms the position exists and matches expectations.

13. Current Safety State

Approved / true:

Exactly one H024 standard-demo canary was placed.
The order was broker-side successful on standard demo.
Post-order audit passed.
One open H024 canary position exists as of the audit.
Runtime plumbing is now proven through a real standard-demo order.
The one-shot path can be used as evidence and infrastructure.

Still false / forbidden:

No second H024 entry order
No live order
No scaling up
No automatic trading loop
No unattended trading
No additional symbols
No additional lots
No changing strategy family
No new entry path
No close/modify unless separately approved and locked
No modifying SL/TP unless separately approved and locked
No manual deletion/tampering with the ledger
No committing reports/
No treating one canary success as live deployment approval

Live deployment is still not close.

The project is now in post-canary monitoring/lifecycle governance.

14. Operational Guidance Right Now

Do not run:

python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER

again.

Reason:

A successful canary already exists.
Re-running would attempt a second entry if idempotency failed or was bypassed.
The correct next step is monitoring and close governance, not another entry.

Do not close the position ad hoc through code unless the user explicitly asks and a close path is locked.

Manual intervention rule:

The user may always manually manage risk in MT5 if needed.
But from the project automation side, closing/modifying must be governed separately.
15. Recommended Next Engineering Step

Next safe, practical, high-leverage work:

Build a read-only post-canary monitor packet.

Suggested implementation:

quantcore\execution\h024_one_shot_demo_canary_monitor.py
scripts\build_h024_one_shot_demo_canary_monitor_jsonl.py
scripts\verify_h024_one_shot_demo_canary_monitor_jsonl.py
tests\test_h024_one_shot_demo_canary_monitor.py
doc:
docs\operations\H024_ONE_SHOT_STANDARD_DEMO_CANARY_MONITOR_RESULT.md

Output:

reports\h024_standard_demo_one_shot_demo_canary_monitor.jsonl

Calls allowed:

mt5.initialize
mt5.account_info
mt5.positions_get
mt5.orders_get
mt5.history_deals_get
mt5.shutdown

Calls forbidden in monitor:

order_check
order_send
any close call
any modify call
any GUI automation
any chart attach/detach automation

Monitor should verify:

account server is Exness-MT5Trial6
account currency is USD
account is demo if trade_mode is available
one of these states:
exactly one open H024 canary position exists, matching ticket/symbol/magic/volume/SL; or
no open position exists, but a matching close/deal history explains closure
no additional H024 positions exist
no unexpected H024 pending orders exist
no second H024 entry deal after deal 3788869526
ledger contains exactly one successful canary record
latest known current price, floating P/L, swap, equity, margin are recorded

Expected open-position match:

ticket/order/identifier: 4413054432
symbol: XAUUSDm
magic: 240024
volume: 0.01
type: 1 sell
open price: 4728.4490000000005
SL: 4817.394
comment prefix: H024_ONE_SHOT_DE

Do not require floating P/L to equal -2.71; that was just the immediate audit value and will change.

16. Possible Next Lifecycle Steps After Monitor

After one or more read-only monitor packets, possible paths are:

A. Continue hold:

Create review-only lifecycle decision packet saying hold remains acceptable.
No mutation.

B. Prepare controlled close:

Only if user explicitly wants the canary closed or risk conditions require closure.

Close path must be separately governed and locked:

exact ticket 4413054432
symbol XAUUSDm
magic 240024
volume 0.01
server Exness-MT5Trial6
account currency USD
close only this position
exact acknowledgement required
idempotency close ledger required
post-close audit required

C. Research post-canary observations:

Compare actual slippage/fill/margin/order_check result to expected.
Do not use the single canary as proof of edge.
Treat it as plumbing validation, not performance validation.
17. Known Pitfalls

PowerShell:

Avoid Bash heredocs.
Avoid fragile backtick continuations.
Use here-strings and temp scripts.
Use UTF-8 no BOM writes.
Use single-line git add.

Git:

Never commit reports/.
If reports/ is the only untracked item, this is expected.
Commit code/docs/tests only.

MT5:

MT5 can reject sends with 10027 if Algo Trading is disabled.
Enable Algo Trading in the toolbar and Tools -> Options -> Expert Advisors.
retcode 10009 means successful trade request execution.
MT5 may truncate comments.
Do not infer live readiness from demo success.

Semantic pitfalls:

Do not treat one demo canary as deployment.
Do not treat demo success as edge proof.
Do not place a second canary.
Do not add automatic loops.
Do not close/modify without explicit close governance.
Do not treat H024 as live-approved.
Do not commit local runtime artifacts.
18. Exact First Response The Next AI Should Give

The next AI should say:

Understood. Continuing from HANDOFF_97.

I understand that H024 has now placed exactly one controlled standard-demo broker-side canary order on Exness-MT5Trial6: XAUUSDm, sell, volume 0.01, magic 240024, order/ticket 4413054432, deal 3788869526, fill price 4728.4490000000005, SL 4817.394. The immediate post-order audit passed with zero violations and verified exactly one open canary position.

I also understand the hard boundary: no second H024 entry order, no live order, no trading loop, no scaling, no extra symbols, and no close/modify unless separately governed. The next safe work is read-only post-canary monitoring and lifecycle governance.

Please run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -10
python scripts\verify_h024_one_shot_demo_canary_source_static.py
python scripts\verify_h024_final_pre_dispatch_audit_packet_jsonl.py reports\h024_standard_demo_final_pre_dispatch_audit_packet.jsonl --allowed-demo-server Exness-MT5Trial6 --expected-runtime-symbol XAUUSDm --max-lot-cap 0.01 --require-pass
python -m pytest -q tests\test_h024_one_shot_demo_canary.py

Then paste the output and say whether the H024 canary position is still open in MT5.

19. Compact Continuation Prompt For Another AI

You are continuing the Institutional EA project from HANDOFF_97.

You are a senior quantitative engineer and mentor helping a solo retail trader on Windows build H024, a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade safety discipline.

H024 has now placed exactly one controlled standard-demo broker-side canary. It was not a live order. It was on Exness standard demo server Exness-MT5Trial6, symbol XAUUSDm, sell side, volume 0.01, magic 240024, request comment H024_ONE_SHOT_DEMO_CANARY truncated by MT5 to H024_ONE_SHOT_DE.

Successful canary details:

command used:
python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER
attempt_stage: send_succeeded
order/ticket: 4413054432
deal: 3788869526
request id: 3072064830
requested price: 4728.367
fill price: 4728.4490000000005
stop loss: 4817.394
order_check_result.retcode: 0
order_send_result.retcode: 10009
volume: 0.01
side: sell / MT5 type 1
margin from order check: 2.36

Immediate post-order audit:

output file: reports/h024_standard_demo_one_shot_demo_canary_post_order_audit.jsonl
verdict: PASS
violations: 0
open canary positions found: 1
verified open position:
ticket: 4413054432
identifier: 4413054432
symbol: XAUUSDm
magic: 240024
type: 1 sell
volume: 0.01
price_open: 4728.4490000000005
price_current at audit: 4731.158
profit at audit: -2.71
SL: 4817.394
TP: 0.0
swap: 0.0
comment: H024_ONE_SHOT_DE

Important commits:

9c81d7d Add H024 one-shot demo canary execution path
f9451e6 Add H024 final demo canary pre-dispatch gates
a2dfc76 Add H024 demo-order canary hard-controls preflight
b3fb88d Add handoff document #96
8132f11 Add H024 demo-order readiness packet

There may also be a later commit:

Handle H024 canary no-fill retry ledger states

If not committed, inspect and commit changes to:

quantcore/execution/h024_one_shot_demo_canary.py
tests/test_h024_one_shot_demo_canary.py

Hard boundaries now:

Do not place another H024 entry order.
Do not run the send command again.
Do not deploy live.
Do not implement an automatic trading loop.
Do not scale volume.
Do not add symbols.
Do not modify or close the canary position without separate explicit close governance.
Do not commit reports/.
Next work should be read-only post-canary monitoring and lifecycle governance.

Recommended next work:

Build a read-only post-canary monitor packet that checks current MT5 account and position state using read-only calls only. It should verify server Exness-MT5Trial6, currency USD, symbol XAUUSDm, ticket/order 4413054432, magic 240024, volume 0.01, SL 4817.394, and no extra H024 orders. It must not call order_check, order_send, close, modify, or mutate anything.

User preferences:

Practical progress, not ceremony.
One coherent PowerShell block.
Code changes require tests.
Avoid fragile PowerShell line continuations.
Never commit reports/.
