# HANDOFF_119 - Fully Self-Contained H025 Exact-Ticket Canary Close Completed, Post-Close Verified, And No-Open-Canary Transition

This handoff supersedes HANDOFF_118 for the H025 controlled exact-ticket canary close sequence.

This file is intentionally redundant. The next AI should not need hidden chain-of-thought, chat history, old runtime `reports/`, or older handoffs to understand the current state.

Fix-forward commit that makes this handoff complete and tracks the Stage 5 code/test:

```text
__d615c14__

Repository path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Final expected git state:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime evidence and must remain untracked.

1. Project Identity

Project:

institutional-ea

Environment:

Local Windows PC
PowerShell
Python virtual environment at .venv
Local MT5 terminal
Demo account on Exness-MT5Trial6
Git branch main

The project had an H024 read-only observer/dashboard track and then a separate H025 controlled exact-ticket close-enable/close-execute track.

H024 remains read-only.

H025 was authorized only to close the already-open exact canary ticket, not to build general trading.

2. Critical Current Outcome

The previously open H024 demo canary trade is now closed.

Closed canary identity:

Account server: Exness-MT5Trial6
Runtime symbol: XAUUSDm
Model symbol: XAUUSD
Original side: sell
MT5 position type before close: 1
Close side sent: buy
Volume: 0.01
Ticket: 4413054432
Identifier: 4413054432
Magic: 240024
Entry deal: 3788869526
Close deal: 3796464680
Close order: 4421682057

Stage 4 executed a one-shot exact-ticket close only.

Stage 5 verified post-close state.

Current verified state:

post_close_verified: True
open_canary_trade_exists: False
exact_ticket_open: False
h024_position_count: 0
h024_order_count: 0
history_deal_match_count: 2

The project currently has no open H024 canary trade.

Do not reopen a canary merely to satisfy old H024 observer assumptions.

3. Safety Boundary After This Handoff
H024

H024 remains read-only.

H024 must not add or contain:

order_check
order_send
symbol_select
new entries
close/modify execution
close-all
broker mutation
unattended order-capable loops
live-money account support
scaling
martingale
grid
automatic position creation

If H024 dashboard/readiness/observer now fails because the old canary is no longer open, that is expected legacy behavior. The correct next milestone is a read-only post-close/no-open-canary observer state. Do not reopen a trade to make old H024 checks pass.

H025

H025 completed the controlled exact-ticket close path for ticket 4413054432.

H025 does not authorize:

new entries
generic open-trade module
unattended trading loop
close-all
symbol_select
live-money account
scaling
martingale
grid
automatic position creation
another order_send

Any future broker mutation requires a new explicit operator authorization and a separate staged scope.

4. Why H025 Was Started

The user corrected the target: the project was not trying to open a new demo trade first. The existing H024 canary trade was already open:

XAUUSDm sell 0.01
ticket/identifier: 4413054432
magic: 240024
demo account: Exness-MT5Trial6

H025 goal was the smallest safe path to close that already-open exact canary trade.

Original H025 staged plan:

1. Audit existing exact-ticket close/modify artifacts and identify what already exists.
2. Implement exact-ticket close request preview for ticket 4413054432 / identifier 4413054432 only.
3. Add demo-account-only mt5.order_check for closing that exact ticket only, behind manual operator approval.
4. Only after explicit confirmation, add one-shot demo-account-only mt5.order_send to close that exact ticket only.
5. Verify the exact ticket is closed and no extra H024 positions or orders exist.

All five stages are now complete.

5. H024 Fix Completed Before H025 Close

Before H025, H024 had a stale exact-ticket evidence problem. The scheduled observer used old exact-ticket reports as black-swan guard upstream evidence. Those reports became stale after about 3600 seconds, which made black-swan guard fail closed, which then polluted scheduled wrapper/task-state/continuity/cadence/dashboard readiness.

H024 minimum source fix:

022053d Refresh H024 exact-ticket evidence before black-swan guard

Purpose:

Refresh exact-ticket read-only evidence inside scripts/run_h024_read_only_vps_observer_once.ps1 before black-swan guard.

Important:

This H024 fix is read-only.
It does not authorize order_check.
It does not authorize order_send.
It does not authorize symbol_select.
It does not authorize entries or closes.

Known H024 dashboard/cadence note:

Before the H025 close, the H024 dashboard readiness chain eventually reached:

Healthcheck: PASS
Task-state: PASS
Recovery drill: PASS
Evidence bundle: PASS
Continuity: PASS
Scheduled cadence: FAIL_CLOSED

The scheduled cadence failure was not a new broker issue. The cadence metrics showed clean 5-minute spacing but not yet enough fresh clean scheduled runs:

observed_run_count: 7
observed_span_minutes: 29.999
min_observed_gap_minutes: 4.965
max_observed_gap_minutes: 5.035

H024 cadence wanted a longer proof window, roughly 12 runs / 55 minutes. Do not spend active time staring at it. Also, after the canary close, H024 may fail for the better reason that there is intentionally no open canary.

6. H025 Stage 1/2 - Audit And Inert Close Preview

Stage 1/2 committed and pushed:

b5b4beb Add H025 exact-ticket canary close request preview
01de648 Add H025 exact-ticket canary close request preview

There are two nearby/duplicate preview commits because of fix-forward iteration. Do not rewrite history.

Files:

docs/operations/H025_CONTROLLED_EXACT_TICKET_CANARY_CLOSE_ENABLEMENT_AUDIT.md
scripts/build_h025_exact_ticket_canary_close_request_preview_jsonl.py
tests/test_h025_exact_ticket_canary_close_request_preview.py

Stage 1/2 purpose:

Audit existing H024 exact-ticket close/modify governance artifacts.
Create an inert exact-ticket close request preview.
Do not call MT5 order_check.
Do not call MT5 order_send.
Do not close the trade.

Stage 1/2 proof:

3 passed
Wrote reports\h025_exact_ticket_canary_close_request_preview.jsonl
Verdict: PASS
Exact ticket: 4413054432
Exact identifier: 4413054432
Preview only: True
order_check_authorized: False
order_send_authorized: False
broker_mutation_authorized: False
7. H025 Stage 3 - Demo-Only Exact-Ticket order_check

Stage 3 commits:

7edcb53 Add H025 exact-ticket canary close order_check gate
1426761 Add H025 exact-ticket canary close order_check implementation
aa35d3b Fix H025 exact-ticket order_check MT5 comment

Files:

docs/operations/H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_close_order_check_jsonl.py
tests/test_h025_exact_ticket_canary_close_order_check.py

There was an intermediate bad commit:

7edcb53

It only tracked the runbook because the script/test were malformed and left untracked. This was fixed forward by:

1426761

Then the first real order_check reached MT5 but failed because MT5 rejected the long comment:

order_check_executed: True
order_send_authorized: False
order_send_executed: False
broker_mutation_authorized: False
retcode: None
comment: None
Violation:
order_check_returned_none
mt5.order_check returned None: (-2, 'Invalid "comment" argument')

Fix:

aa35d3b Fix H025 exact-ticket order_check MT5 comment

The comment was shortened to:

H025_CLOSE_CHECK

Stage 3 final proof:

Verdict: PASS
stage: H025_STAGE_3_EXACT_TICKET_CLOSE_ORDER_CHECK
operator_state: H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_COMPLETED_NO_CLOSE_SENT
exact_ticket: 4413054432
exact_identifier: 4413054432
symbol: XAUUSDm
side_to_close: sell
close_side_checked: buy
order_check_executed: True
order_send_authorized: False
order_send_executed: False
broker_mutation_authorized: False
retcode: 0
comment: Done

Stage 3 checked request:

action: 1
comment: H025_CLOSE_CHECK
deviation: 50
magic: 240024
position: 4413054432
price: 4719.96
symbol: XAUUSDm
type: 0
type_filling: 1
type_time: 0
volume: 0.01

Stage 3 did not close the trade.

8. H025 Stage 4 - One-Shot Exact-Ticket order_send

The operator explicitly authorized Stage 4 with:

Authorize H025 Stage 4: one-shot demo-account-only mt5.order_send to close exact ticket 4413054432 only. No new entries, no close-all, no loop, no symbol_select, no live-money account.

Stage 4 commit:

1ed8aa9 Add H025 exact-ticket canary close order_send gate

Files:

docs/operations/H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_close_order_send_jsonl.py
tests/test_h025_exact_ticket_canary_close_order_send.py

Stage 4 implementation behavior:

Requires Stage 3 PASS report.
Requires fresh explicit Stage 4 approval artifact.
Checks account server Exness-MT5Trial6.
Checks exact ticket 4413054432.
Checks exact identifier 4413054432.
Checks symbol XAUUSDm.
Checks magic 240024.
Checks volume 0.01.
Checks sell position type.
Checks exactly one H024 XAUUSDm magic 240024 position before send.
Checks zero H024 XAUUSDm magic 240024 pending orders before send.
Runs pre-send mt5.order_check.
Runs one mt5.order_send.
Verifies exact ticket no longer open.
Verifies H024 position count is 0.
Verifies H024 order count is 0.
No loop.
No close-all.
No symbol_select.
No live-money.

Stage 4 approval artifact content included:

schema: h025_exact_ticket_canary_close_order_send_approval.v1
intent: H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_ONE_SHOT
operator_approved: true
order_send_authorized: true
order_check_authorized: true
stage3_order_check_required: true
pre_send_order_check_required: true
account_server: Exness-MT5Trial6
symbol: XAUUSDm
exact_ticket: 4413054432
exact_identifier: 4413054432
magic: 240024
volume: 0.01
side_to_close: sell
close_side: buy
close_all_authorized: false
entry_authorized: false
symbol_select_authorized: false
unattended_loop_authorized: false
live_money_authorized: false

Stage 4 execution output:

Wrote reports\h025_exact_ticket_canary_close_order_send.jsonl
Verdict: PASS
Operator state: H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_COMPLETED_AND_VERIFIED
Exact ticket: 4413054432
Exact identifier: 4413054432
order_check_executed: True
order_send_executed: True
broker_mutation_authorized: True
send_retcode: 10009
send_comment: 'H025_CLOSE_SEND'
post_send_exact_ticket_open: False
post_send_h024_position_count: 0
post_send_h024_order_count: 0
Stage 4 script exit code: 0

Stage 4 report summary:

verdict: PASS
stage: H025_STAGE_4_EXACT_TICKET_CLOSE_ORDER_SEND
operator_state: H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_COMPLETED_AND_VERIFIED
exact_ticket: 4413054432
exact_identifier: 4413054432
symbol: XAUUSDm
side_to_close: sell
close_side_sent: buy
order_check_executed: True
order_send_executed: True
post_send_exact_ticket_open: False
post_send_h024_position_count: 0
post_send_h024_order_count: 0
order_send_authorized: True
broker_mutation_authorized: True

Stage 4 order_send result:

ask: 4718.719
bid: 4718.411
comment: H025_CLOSE_SEND
deal: 3796464680
order: 4421682057
price: 4718.719
request_id: 3072064831
retcode: 10009
retcode_external: 0
volume: 0.01

Stage 4 post-send result:

post-send H024 positions: none
post-send H024 orders: none

Stage 4 was the only authorized close execution.

Do not rerun Stage 4.

9. H025 Stage 5 - Post-Close Verification

Stage 5 first attempt had a writer indentation error:

IndentationError: expected an indented block after function definition on line 24

This was not a logic or MT5 verification failure. It was fixed by rewriting the Stage 5 script/test with controlled indentation.

There was an incomplete Stage 5 handoff commit:

960875e Add H025 post-close canary verification handoff

Problem with 960875e:

It tracked the runbook and a too-thin HANDOFF_119, but final git status still showed:
?? scripts/build_h025_exact_ticket_canary_post_close_verification_jsonl.py
?? tests/test_h025_exact_ticket_canary_post_close_verification.py

Therefore 960875e alone is not complete.

This fix-forward commit tracks the missing Stage 5 script/test and expands HANDOFF_119:

__d615c14__

Stage 5 files:

docs/operations/H025_EXACT_TICKET_CANARY_POST_CLOSE_VERIFICATION_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_post_close_verification_jsonl.py
tests/test_h025_exact_ticket_canary_post_close_verification.py
docs/operations/handoffs/HANDOFF_119.md

Stage 5 test output:

4 passed

Stage 5 runtime output:

H025 exact-ticket canary post-close verification verdict: PASS
Operator state: H025_EXACT_TICKET_CANARY_POST_CLOSE_VERIFIED_NO_OPEN_CANARY
Violations: 0
Exact ticket: 4413054432
Exact identifier: 4413054432
post_close_verified: True
open_canary_trade_exists: False
exact_ticket_open: False
h024_position_count: 0
h024_order_count: 0
history_deal_match_count: 2

Stage 5 report summary:

verdict: PASS
stage: H025_STAGE_5_POST_CLOSE_VERIFICATION
operator_state: H025_EXACT_TICKET_CANARY_POST_CLOSE_VERIFIED_NO_OPEN_CANARY
exact_ticket: 4413054432
exact_identifier: 4413054432
symbol: XAUUSDm
post_close_verified: True
open_canary_trade_exists: False
exact_ticket_open: False
h024_position_count: 0
h024_order_count: 0
read_only_verification_only: True
order_check_executed: False
order_send_executed: False
broker_mutation_authorized: False

Stage 5 is read-only. It must not contain:

mt5.order_check
mt5.order_send
mt5.symbol_select
TRADE_ACTION
ORDER_TYPE_BUY
ORDER_TYPE_SELL
10. Runtime Reports Discipline

Runtime reports are intentionally generated under reports/ and must remain untracked.

Known relevant runtime evidence includes:

reports/h025_exact_ticket_canary_close_request_preview.jsonl
reports/h025_exact_ticket_canary_close_order_check.jsonl
reports/h025_exact_ticket_canary_close_order_check_operator_approval.json
reports/h025_exact_ticket_canary_close_order_send.jsonl
reports/h025_exact_ticket_canary_close_order_send_operator_approval.json
reports/h025_exact_ticket_canary_post_close_verification.jsonl
reports/h025_exact_ticket_canary_post_close_verification.txt

Do not commit reports/.

11. Current Source File Map

H024 read-only observer fix:

scripts/run_h024_read_only_vps_observer_once.ps1
tests/test_h024_read_only_observer_exact_ticket_refresh_before_black_swan.py

H025 Stage 1/2:

docs/operations/H025_CONTROLLED_EXACT_TICKET_CANARY_CLOSE_ENABLEMENT_AUDIT.md
scripts/build_h025_exact_ticket_canary_close_request_preview_jsonl.py
tests/test_h025_exact_ticket_canary_close_request_preview.py

H025 Stage 3:

docs/operations/H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_close_order_check_jsonl.py
tests/test_h025_exact_ticket_canary_close_order_check.py

H025 Stage 4:

docs/operations/H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_close_order_send_jsonl.py
tests/test_h025_exact_ticket_canary_close_order_send.py

H025 Stage 5:

docs/operations/H025_EXACT_TICKET_CANARY_POST_CLOSE_VERIFICATION_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_post_close_verification_jsonl.py
tests/test_h025_exact_ticket_canary_post_close_verification.py
docs/operations/handoffs/HANDOFF_119.md
12. Recent Git Timeline

Recent known commits:

960875e Add H025 post-close canary verification handoff
1ed8aa9 Add H025 exact-ticket canary close order_send gate
aa35d3b Fix H025 exact-ticket order_check MT5 comment
1426761 Add H025 exact-ticket canary close order_check implementation
7edcb53 Add H025 exact-ticket canary close order_check gate
01de648 Add H025 exact-ticket canary close request preview
b5b4beb Add H025 exact-ticket canary close request preview
022053d Refresh H024 exact-ticket evidence before black-swan guard
5625b8f Expand handoff document #118
047fcf7 Add H024 local read-only demo dashboard
3261878 Add H024 free local read-only demo readiness packet

Current fix-forward commit:

__d615c14__

Recent git log before this fix-forward:

__960875e Add H025 post-close canary verification handoff
1ed8aa9 Add H025 exact-ticket canary close order_send gate
aa35d3b Fix H025 exact-ticket order_check MT5 comment
1426761 Add H025 exact-ticket canary close order_check implementation
7edcb53 Add H025 exact-ticket canary close order_check gate
01de648 Add H025 exact-ticket canary close request preview
b5b4beb Add H025 exact-ticket canary close request preview
022053d Refresh H024 exact-ticket evidence before black-swan guard
5625b8f Expand handoff document #118
047fcf7 Add H024 local read-only demo dashboard
3261878 Add H024 free local read-only demo readiness packet
5abbc0a Add handoff document #117
b26b6e3 Add handoff document #116
367e5c0 Fix H024 read-only observer no-console launcher validation
c0eb3cc Add H024 read-only observer no-console launcher__

Do not rewrite pushed history. Fix forward only.

13. Commands To Re-Verify Current Truth

Use this read-only command to verify Stage 5 again:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

python -m pytest tests\test_h025_exact_ticket_canary_post_close_verification.py -q
python scripts\build_h025_exact_ticket_canary_post_close_verification_jsonl.py

$Report = Get-Content -Raw reports\h025_exact_ticket_canary_post_close_verification.jsonl | ConvertFrom-Json
$Report |
  Select-Object `
    verdict,
    post_close_verified,
    open_canary_trade_exists,
    exact_ticket_open,
    h024_position_count,
    h024_order_count,
    read_only_verification_only,
    order_check_executed,
    order_send_executed,
    broker_mutation_authorized |
  Format-List

git status --short

Expected:

verdict: PASS
post_close_verified: True
open_canary_trade_exists: False
exact_ticket_open: False
h024_position_count: 0
h024_order_count: 0
read_only_verification_only: True
order_check_executed: False
order_send_executed: False
broker_mutation_authorized: False
git status: reports/ only untracked
14. Next Recommended Milestone

Recommended next milestone:

H026 or H024-post-close: read-only no-open-canary observer state.

Goal:

Teach the H024 read-only observer/dashboard/readiness stack that the H024 canary was intentionally closed by H025 and that zero H024 positions/orders is now an acceptable post-close state.

This should be read-only and should not reopen the trade.

It should probably:

1. Add a post-close/no-open-canary state packet.
2. Teach exposure inventory / dashboard to distinguish "missing canary because intentionally closed" from "missing canary unexpectedly".
3. Preserve H024 no-mutation boundaries.
4. Keep reports/ untracked.

Do not build yet unless explicitly asked:

new open-trade module
automated entries
unattended loop
close-all
live-money support
scaling
martingale
grid
automatic position creation
15. Operator Instruction For Next AI

Continue from HANDOFF_119 on main.

The exact H024 canary ticket 4413054432 has been closed and post-close verified. There is no open H024 canary trade. Do not reopen it to satisfy old H024 observer assumptions.

First useful next work is a read-only post-close/no-open-canary observer state so H024 dashboard/readiness can represent the new truth without requiring an open canary.

Keep reports/ untracked.

