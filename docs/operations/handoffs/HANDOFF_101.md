# HANDOFF_101 — FULL SELF-CONTAINED H024 POST-CANARY STATE: XAUUSD CANARY OPEN, USDJPY READINESS ADDED, SAFETY SPEC ADDED, RUNTIME LOCKOUT READER ADDED

If this handoff conflicts with any older handoff, this handoff wins.

This handoff is intentionally self-contained. A new AI must be able to continue from this file alone without opening HANDOFF_100, HANDOFF_99, HANDOFF_98, chat history, or local runtime reports.

The prior authoritative handoff was:

- `docs/operations/handoffs/HANDOFF_100.md`
- commit: `240e1fc Replace misplaced handoff #99 with full handoff #100`

This HANDOFF_101 carries forward the HANDOFF_100 operating boundary and updates it with the post-HANDOFF_100 work:

1. H024 USDJPY broker-readiness packet added.
2. H024 safety supervisor / kill-switch specification added.
3. H024 runtime safety configuration + local lockout reader added.
4. Latest validation outputs and exact repository state.
5. Next recommended work.
6. Exact continuation prompt and expected first response for the next AI.

---

## 0. Current One-Sentence State

H024 has exactly one controlled standard-demo broker-side canary position that was last user-confirmed open on Exness-MT5Trial6: XAUUSDm sell, volume 0.01, magic 240024, order/ticket/identifier 4413054432, entry deal 3788869526, open price 4728.4490000000005, SL 4817.394. The read-only post-canary supervision stack passes. USDJPY broker-readiness now passes as a read-only packet. Safety supervisor / kill-switch specification now passes. Runtime local safety config + lockout reader now passes. No broker mutation, no `order_check`, no `order_send`, no entry, no close/modify, and no trading loop are authorized.

Hard boundary:

- No second H024 entry order.
- Do not rerun the XAUUSDm canary send command.
- No live order.
- No automatic trading loop.
- No scaling.
- No USDJPY order yet.
- No code close/modify unless separately governed and exact-ticket locked.
- No committing `reports/`.
- Strategy edge is not proven by the canary.
- Demo plumbing is meaningfully proven; live deployment is still not close.

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
- Server: `Exness-MT5Trial6`
- Account currency: `USD`
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
- H024 is in post-canary read-only supervision/lifecycle/safety-governance mode.
- Runtime plumbing has been proven through one real standard-demo broker-side order.
- Read-only post-canary supervision is automated.
- USDJPY readiness is read-only verified, but USDJPY trading is not authorized.
- Safety supervisor is specified.
- Local runtime lockout reader exists and is committed.
- Actual broker-facing runtime safety enforcement is still incomplete.

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
- Keep morale grounded: strategy edge is unproven, but runtime plumbing and read-only safety layers are meaningfully advancing.
- The user likes receiving a concise suggested next prompt after each completed milestone. Continue doing this.

Response/implementation style for the next AI:

- Act like a senior quantitative engineer and safety-minded mentor.
- Be direct and exact.
- Preserve safety invariants.
- Prefer big coherent steps that materially move the project forward.
- When a milestone completes, summarize:
  - commit hash,
  - focused tests,
  - full suite result,
  - runtime packet/verifier status,
  - remaining hard boundaries,
  - best next step,
  - suggested next prompt in a copyable text block.

---

## 3. Latest Repository State At HANDOFF_101

Latest known commits:

- `98efc2a Add H024 runtime safety lockout reader`
- `24c347a Add H024 safety supervisor specification`
- `df62439 Add H024 USDJPY broker-readiness packet`
- `240e1fc Replace misplaced handoff #99 with full handoff #100`
- `03fc3ce Add handoff document #99`
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

Expected current git state after committing this handoff:

- Branch: `main`
- Up to date with `origin/main`
- Latest commit should be `Add handoff document #101`
- Untracked `reports/` only
- No modified tracked files

Never commit:

- `reports/`
- raw MT5 exports
- runtime JSON/JSONL files
- local logs
- terminal data files
- local compile logs
- broker/vendor source files
- large derived datasets

---

## 4. Canonical XAUUSDm Canary Facts

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

Latest user-confirmed position state:

After a read-only supervision run, the user said the position was still open.
The next AI should verify current broker state using the read-only supervision runner, because mark-to-market and open/closed state can change.
5. Latest Read-Only Post-Canary Supervision State

One-command read-only supervision runner exists:

python scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
python scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl --require-pass

Latest known output before post-HANDOFF_100 safety work:

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

Stages:

build_monitor: PASS
verify_monitor: PASS
build_lifecycle_decision: PASS
verify_lifecycle_decision: PASS
build_observation_analysis: PASS
verify_observation_analysis: PASS
build_supervisory_state: PASS
verify_supervisory_state: PASS

Important:

Mark-to-market values are not fixed.
The next AI should refresh this state before making operational claims.
6. Post-HANDOFF_100 Work Implemented
A. H024 USDJPY Broker-Readiness Packet

Commit:

df62439 Add H024 USDJPY broker-readiness packet

Files:

quantcore\execution\h024_usdjpy_broker_readiness.py
scripts\build_h024_usdjpy_broker_readiness_jsonl.py
scripts\verify_h024_usdjpy_broker_readiness_jsonl.py
tests\test_h024_usdjpy_broker_readiness.py
docs\operations\H024_USDJPY_BROKER_READINESS_PACKET.md

Runtime output, local only:

reports\h024_usdjpy_broker_readiness.jsonl

Validation at commit:

Focused tests: 9 passed
Full suite: 1428 passed
Runtime packet: PASS
Verifier: PASS
Violations: 0

Purpose:

Read-only USDJPY readiness path. It verifies:

server Exness-MT5Trial6
account currency USD
runtime symbol USDJPYm
model symbol USDJPY
symbol properties
spread/tick sanity
broker-native H4/M1 availability
H020 sizing feasibility
request-shape implications
no existing unexpected H024 USDJPY positions/orders
no broker mutation authorization

Explicit non-authorizations:

broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
usd_jpy_order_authorized: False
trading_loop_authorized: False

Important:

USDJPY is now read-only readiness verified.
USDJPY is still not authorized for any order.
USDJPY must not piggyback on the XAUUSDm canary stack.

Canonical refresh commands:

python scripts\build_h024_usdjpy_broker_readiness_jsonl.py
python scripts\verify_h024_usdjpy_broker_readiness_jsonl.py reports\h024_usdjpy_broker_readiness.jsonl --require-pass
B. H024 Safety Supervisor / Kill-Switch Specification

Commit:

24c347a Add H024 safety supervisor specification

Files:

quantcore\execution\h024_safety_supervisor_spec.py
scripts\build_h024_safety_supervisor_spec_jsonl.py
scripts\verify_h024_safety_supervisor_spec_jsonl.py
tests\test_h024_safety_supervisor_spec.py
docs\operations\H024_SAFETY_SUPERVISOR_SPEC.md

Runtime output, local only:

reports\h024_safety_supervisor_spec.jsonl

Validation at commit:

Focused tests: 10 passed
Full suite: 1438 passed
Safety supervisor spec packet: PASS
Verifier: PASS
Global guards defined: 10
Symbol circuit breaker groups: 2

Global guards defined:

global_no_new_entry_switch
manual_override_lockout_file
daily_loss_lockout
max_floating_loss_lockout
spread_shock_guard
stale_tick_guard
disconnected_terminal_guard
margin_compression_guard
volatility_expansion_black_swan_guard
unexpected_position_order_lockout

Per-symbol circuit breaker groups:

XAUUSD / XAUUSDm
USDJPY / USDJPYm

Per-symbol breakers:

symbol_no_new_entry_breaker
symbol_max_floating_loss_breaker
symbol_spread_shock_breaker
symbol_stale_tick_breaker
symbol_volatility_expansion_black_swan_breaker
symbol_unexpected_position_order_breaker

Explicit non-authorizations:

Broker mutation: False
Order check: False
Order send: False
Entry: False
Close/modify: False
XAUUSD order: False
USDJPY order: False
Trading loop: False
Automatic execution: False

Important:

This is a specification layer, not runtime enforcement.
It defines the required contract and fail-closed semantics.
Runtime enforcement still needs implementation before any loop can exist.

Canonical refresh commands:

python scripts\build_h024_safety_supervisor_spec_jsonl.py
python scripts\verify_h024_safety_supervisor_spec_jsonl.py reports\h024_safety_supervisor_spec.jsonl --require-pass
C. H024 Runtime Safety Configuration + Local Lockout Reader

Commit:

98efc2a Add H024 runtime safety lockout reader

Files:

config\h024_runtime_safety\default_lockout_config.json
config\h024_runtime_safety\lockouts\global_no_new_entry.json
config\h024_runtime_safety\lockouts\manual_override_lockout.json
config\h024_runtime_safety\lockouts\xauusd_no_new_entry.json
config\h024_runtime_safety\lockouts\usdjpy_no_new_entry.json
quantcore\execution\h024_runtime_safety_lockout.py
scripts\build_h024_runtime_safety_lockout_jsonl.py
scripts\verify_h024_runtime_safety_lockout_jsonl.py
tests\test_h024_runtime_safety_lockout.py
docs\operations\H024_RUNTIME_SAFETY_LOCKOUT_READER.md

Runtime output, local only:

reports\h024_runtime_safety_lockout.jsonl

Validation at commit:

Focused tests: 12 passed
Full suite: 1450 passed
Runtime safety lockout packet: PASS
Verifier: PASS
Violations: 0
Operator state: LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Lockout inputs valid: True
Lockout triggered: False
Active lockouts: 0
Fail-closed lockouts: 0
Effective new entries blocked: True
Branch clean after push except untracked reports/

Purpose:

First runtime-local safety enforcement layer. It reads committed local JSON config and lockout files for:

Global no-new-entry lockout.
Manual override lockout.
XAUUSD per-symbol no-new-entry lockout.
USDJPY per-symbol no-new-entry lockout.

It is:

read-only
local-files-only
no MT5 import
no broker calls
no order_check
no order_send
no entry
no close/modify
no trading loop

Fail-closed behavior:

The reader fails closed if:

config file is missing;
config file is malformed;
config root is not a JSON object;
any required lockout path is missing;
any required lockout file is missing;
any required lockout file is malformed;
any lockout file has wrong strategy;
any lockout file has wrong symbol mapping;
any lockout file has non-boolean active;
any config authorization flag is true.

Committed default config:

config\h024_runtime_safety\default_lockout_config.json

Committed default lockout files:

config\h024_runtime_safety\lockouts\global_no_new_entry.json
config\h024_runtime_safety\lockouts\manual_override_lockout.json
config\h024_runtime_safety\lockouts\xauusd_no_new_entry.json
config\h024_runtime_safety\lockouts\usdjpy_no_new_entry.json

Committed defaults are inactive lockouts. This does not authorize trading. It only gives the reader valid inputs.

Important semantics:

LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED means lockout files are valid and inactive.
It does not mean entries are allowed.
effective_new_entries_blocked remains True.
All order/mutation/trading-loop authorizations remain False.

Canonical refresh commands:

python scripts\build_h024_runtime_safety_lockout_jsonl.py
python scripts\verify_h024_runtime_safety_lockout_jsonl.py reports\h024_runtime_safety_lockout.jsonl --require-pass
7. Current Safety State

Approved / true:

Exactly one H024 standard-demo XAUUSDm canary was placed.
The order was broker-side successful on standard demo.
Immediate post-order audit passed.
Read-only monitor passed.
Continue-hold lifecycle decision passed.
Observation analysis passed.
Supervisory state passed.
Read-only supervision runner passed.
One-command read-only supervision automation exists and is committed.
USDJPY broker-readiness packet exists and passes read-only.
Safety supervisor / kill-switch specification exists and passes.
Runtime local safety config + lockout reader exists and passes.
Runtime plumbing is proven through one real standard-demo order.
Read-only post-canary operations are substantially automated.
Local no-new-entry lockout reader now provides the first real local enforcement layer.

Still false / forbidden:

No second H024 entry order.
No live order.
No scaling up.
No automatic trading loop.
No unattended trading.
No USDJPY order.
No additional lots.
No changing strategy family.
No new broker mutation path.
No code close/modify unless separately approved and locked.
No modifying SL/TP unless separately approved and locked.
No manual deletion/tampering with ledgers.
No committing reports/.
No treating one canary success as live deployment approval.
No treating one canary as strategy edge evidence.
No treating lockouts-clear as trading permission.

Live deployment is still not close.

8. Strategy Mechanics Summary

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
long signal = trend up + bearish pullback + long resumption
short signal = trend down + bullish pullback + short resumption
9. H020 / H024 Sizing Boundary

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
side: sell
stop distance: 89.027
SL: 4817.394
magic: 240024

Do not casually change these.

10. Data And Broker Rules

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

raw MT5 CSV files
raw HistData files
large derived datasets
broker/vendor source files
reports/*.csv
reports/*.json
reports/*.jsonl
local runtime CSVs
local compile logs
11. Known Pitfalls

PowerShell:

Avoid Bash heredocs.
Avoid fragile backtick continuations.
Use here-strings and temp scripts.
Use UTF-8 no BOM writes.
Use single-line git add.

Git:

Never commit reports/.
If reports/ is the only untracked item, this is expected.
Commit code/docs/tests/config only.
For docs-only handoff commits, do not run full pytest unless there is a specific reason.

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
Do not treat LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED as permission to trade.
Do not allow a false authorization from one packet to mask a true/unsafe authorization from another. Merge authorization fail-closed.
12. Best Next Major Work Options

Pick one, depending on user intent.

Option A — Refresh Read-Only Supervision

Safe and already automated. Use this first if the user wants to know whether the canary is still coherent/open.

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -15
python scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
python scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl --require-pass

Ask the user to confirm whether the XAUUSDm position is still open in MT5 only if broker state is ambiguous.

Option B — Add Runtime Safety Heartbeat Packet

Recommended next engineering step.

Implement a read-only runtime safety heartbeat that checks:

MT5 initializes.
Account info is available.
Server is Exness-MT5Trial6.
Currency is USD.
Terminal/account heartbeat is fresh.
No broker mutation is authorized.
It consumes or references the runtime safety lockout reader.
It emits JSONL + verifier + tests + docs.
It does not call order_check.
It does not call order_send.
It does not close/modify.
It does not authorize a trading loop.

Suggested commit name:

Add H024 runtime safety heartbeat packet
Option C — Add Runtime Spread/Tick Safety Supervisor

After heartbeat or combined with it if implementation remains coherent.

Read-only checks:

per-symbol tick freshness for XAUUSDm and USDJPYm
bid/ask sanity
spread sanity
stale tick fail-closed
spread shock fail-closed
consumes lockout reader
no mutation authorization

Suggested commit name:

Add H024 runtime tick and spread safety supervisor
Option D — Controlled Close Governance

Only if the user explicitly asks to close/manage the existing XAUUSDm canary through code.

Must be exact-ticket locked:

Server: Exness-MT5Trial6
Account currency: USD
Symbol: XAUUSDm
Ticket/identifier: 4413054432
Magic: 240024
Volume: 0.01
Side: close only the existing sell canary
No extra positions
Exact acknowledgement required
Idempotency close ledger required
Post-close audit required

No code close is authorized by this handoff.

Option E — Continue USDJPY Governance

USDJPY readiness is now read-only verified, but USDJPY order is not authorized.

Potential next USDJPY work:

USDJPY inert request-shape preview
USDJPY canary governance packet
USDJPY final pre-dispatch audit

Do not place a USDJPY order unless a separate explicit human approval path is built and the user explicitly authorizes it.

13. Recommended Next Step

Recommended next step from HANDOFF_101:

Add the H024 runtime safety heartbeat packet.

Reason:

The project now has:

read-only canary supervision,
USDJPY broker-readiness,
safety supervisor specification,
local config + lockout reader.

The next missing safety layer is runtime platform/account heartbeat: proving the terminal/account state is readable and fail-closed before any higher-risk automation can ever be considered.

The heartbeat must still be read-only. It should not implement a trading loop.

Suggested next user prompt:

Let’s implement the H024 runtime safety heartbeat packet. It should be read-only and consume or reference the runtime safety lockout reader. It must verify MT5 initialization, account_info availability, server Exness-MT5Trial6, USD account currency, terminal/account heartbeat freshness where available, and fail closed if runtime state is unavailable or inconsistent. It must authorize no broker mutation, no order_check, no order_send, no entries, no close/modify, and no trading loop. Include module, verifier, tests, scripts, and docs. Keep reports/ untracked.

Continue giving the user suggested next prompts after milestones.

14. Exact First Response For The Next AI

The next AI should say:

Understood. Continuing from HANDOFF_101.

H024 has exactly one controlled standard-demo XAUUSDm canary that was last user-confirmed open on Exness-MT5Trial6: sell, volume 0.01, magic 240024, ticket/identifier 4413054432, entry deal 3788869526, open price 4728.4490000000005, SL 4817.394. The post-canary read-only supervision stack exists and has passed with 8/8 stages. USDJPY broker-readiness now exists and passed read-only. The safety supervisor/kill-switch specification exists and passed. The runtime local safety config + lockout reader exists and passed, with operator state LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED. No broker mutation, order_check, order_send, entry, close/modify, USDJPY order, XAUUSD new order, or trading loop is authorized.

The hard boundary remains: no second H024 entry, no live order, no trading loop, no scaling, no broker mutation, no USDJPY order, and no close/modify unless separately governed and exact-ticket locked.

Please run this verification block:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -15
python scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
python scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl --require-pass
python scripts\build_h024_runtime_safety_lockout_jsonl.py
python scripts\verify_h024_runtime_safety_lockout_jsonl.py reports\h024_runtime_safety_lockout.jsonl --require-pass

Then paste the output and say whether the XAUUSDm canary is still open in MT5.

Recommended next implementation after verification: H024 runtime safety heartbeat packet.

15. Compact Continuation Prompt For Another AI

Use this if you need a short prompt in a new chat:

You are continuing the Institutional EA project from HANDOFF_101.

You are a senior quantitative engineer and mentor helping a solo retail trader on Windows build H024, a USDJPY + XAUUSD MetaTrader 5 expert advisor with institutional-grade safety discipline.

Repository: C:\Users\equin\Documents\institutional-ea
Branch: main
Remote: https://github.com/citradinnda/institutional-ea.git
Python: 3.12.10 in .venv
Shell: Windows PowerShell
Broker/demo: Exness standard demo
Server: Exness-MT5Trial6
Account currency: USD

H024 has exactly one controlled standard-demo broker-side canary. It was not a live order. It was on Exness standard demo server Exness-MT5Trial6, symbol XAUUSDm, sell side, volume 0.01, magic 240024, request comment H024_ONE_SHOT_DEMO_CANARY truncated by MT5 to H024_ONE_SHOT_DE.

Successful canary details:

command used: python scripts\run_h024_one_shot_demo_canary.py --send --acknowledgement I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER
attempt_stage: send_succeeded
order/ticket/identifier: 4413054432
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

Post-canary stack:

immediate post-order audit: PASS
read-only monitor: PASS
lifecycle decision: continue_hold / PASS
observation analysis: PASS
supervisory state: continue_observe_open / PASS
read-only supervision runner: PASS, 8/8 stages

Post-HANDOFF_100 commits:

df62439 Add H024 USDJPY broker-readiness packet
24c347a Add H024 safety supervisor specification
98efc2a Add H024 runtime safety lockout reader

Latest runtime safety lockout state:

focused tests: 12 passed
full suite: 1450 passed
runtime safety lockout packet: PASS
verifier: PASS
operator state: LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED
lockout inputs valid: True
lockout triggered: False
active lockouts: 0
fail-closed lockouts: 0
effective new entries blocked: True
all broker/order/trading authorizations: False
final git state: branch main up to date with origin/main; untracked reports/ only

Hard boundaries:

Do not place another H024 entry order.
Do not run the XAUUSDm send command again.
Do not deploy live.
Do not implement an automatic trading loop.
Do not scale volume.
Do not place a USDJPY order.
Do not modify or close the canary position without separate explicit close governance.
Do not commit reports/.
Do not treat one demo canary as strategy edge evidence.
Do not treat lockouts-clear as trading authorization.

User preferences:

practical progress, not ceremony;
one coherent PowerShell block;
avoid fragile backtick continuations;
code changes require focused tests and usually full suite;
docs-only handoff commits do not need full pytest;
never commit reports/;
after each completed milestone, provide a concise suggested next prompt.

Recommended next step:

Implement the H024 runtime safety heartbeat packet. It should be read-only and consume or reference the runtime safety lockout reader. It must verify MT5 initialization, account_info availability, server Exness-MT5Trial6, USD account currency, terminal/account heartbeat freshness where available, and fail closed if runtime state is unavailable or inconsistent. It must authorize no broker mutation, no order_check, no order_send, no entries, no close/modify, and no trading loop. Include module, verifier, tests, scripts, and docs. Keep reports/ untracked.

16. Handoff Commit Instructions Used For HANDOFF_101

Because this file is docs-only, do not run full pytest solely for the handoff.

Expected commit command:

git status
git add -- "docs\operations\handoffs\HANDOFF_101.md"
git diff --cached --check
git commit -m "Add handoff document #101"
git push
git status

Expected final state:

branch main up to date with origin/main
untracked reports/ only
no modified tracked files