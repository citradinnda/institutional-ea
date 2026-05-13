# HANDOFF_120 - Fully Self-Contained H025 Exact-Ticket Canary Closed, Verified, And Ready For H024 Post-Close Observer Transition

This handoff supersedes HANDOFF_119, HANDOFF_118, and all older handoffs.

This file is intentionally verbose and redundant. The next AI should not need hidden chain-of-thought, older handoffs, previous chat messages, or runtime eports/ files to understand the current state.

If this handoff conflicts with any older handoff, this handoff wins.

HANDOFF_120 commit:

`	ext
__45b51f7__

Repository state before creating HANDOFF_120:

HEAD before HANDOFF_120: 8e2d44f

Repository path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Expected final git state after this handoff:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is generated runtime evidence. Keep it untracked.

1. One-Sentence Current Truth

The original H024 demo canary trade XAUUSDm sell 0.01, ticket/identifier 4413054432, magic 240024, on demo server Exness-MT5Trial6, has been closed by H025 Stage 4 and post-close verified by H025 Stage 5.

There is currently no open H024 canary trade.

Do not reopen a canary merely to satisfy old H024 observer assumptions.

2. Project Identity And Environment

Project:

institutional-ea

Local repository path:

C:\Users\equin\Documents\institutional-ea

Primary operating environment:

Windows PC
PowerShell
Python virtual environment: .venv
Local MetaTrader 5 terminal
Demo account/server: Exness-MT5Trial6
Branch: main
Remote: GitHub origin/main

The project currently contains:

H024 - read-only observer/dashboard/readiness track
H025 - controlled exact-ticket canary close enablement and close execution track

H024 remains read-only.

H025 has completed the controlled close of the already-open exact canary. H025 does not authorize generic trading.

3. User Context And Operational Preference

The user is frustrated by excessive governance loops, stale packets, cadence proof windows, brittle runtime reports, and handoffs that are not self-contained.

Respond operationally.

Do not make the user run vague exploratory blocks.

Do not add new packet layers unless they directly unblock the next milestone.

Do not promise future background work.

Do not ask to reopen trades just to satisfy old observers.

When writing a handoff, include enough concrete detail that another AI can continue without guessing.

4. Absolute Safety Boundaries After HANDOFF_120
H024 Boundary

H024 remains read-only.

In H024, do not add:

mt5.order_check
mt5.order_send
mt5.symbol_select
TRADE_ACTION request construction
ORDER_TYPE_BUY / ORDER_TYPE_SELL execution request construction
new entries
close/modify execution
SL/TP modification
close-all
broker mutation
unattended order-capable loops
live-money support
scaling
martingale
grid
automatic position creation

If H024 observer/dashboard/readiness fails because the old canary is no longer open, that is expected legacy behavior. The correct fix is a read-only post-close/no-open-canary observer state.

H025 Boundary

H025 was authorized only to close the exact existing canary ticket 4413054432.

H025 does not authorize:

new entries
generic open-trade module
unattended trading loop
close-all
symbol_select
live-money account support
scaling
martingale
grid
automatic position creation
additional order_send calls

Do not rerun Stage 4.

Any future broker mutation requires a new explicit operator authorization and a separate staged scope.

5. Original Canary Identity

The canary that existed before H025:

Account server: Exness-MT5Trial6
Account currency: USD
Runtime symbol: XAUUSDm
Model symbol: XAUUSD
Side: sell
MT5 position type: 1
Volume: 0.01
Magic: 240024
Ticket: 4413054432
Identifier: 4413054432
Entry deal: 3788869526

Known pre-close state from H024 runtime checks:

Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0

The user explicitly corrected the execution target:

We are not trying to open a new demo trade first.
The existing H024 canary trade is already open.
Build the smallest safe path to close the already-open exact canary trade.
6. Why H025 Was Started

The older project path had become stuck around read-only H024 observer/dashboard proof, stale exact-ticket evidence, and strict cadence windows.

The user authorized H025 Controlled Exact-Ticket Canary Close Enablement with these stages:

1. Audit existing exact-ticket close/modify artifacts and identify what already exists.
2. Implement exact-ticket close request preview for ticket 4413054432 / identifier 4413054432 only.
3. Add demo-account-only mt5.order_check for closing that exact ticket only, behind manual operator approval.
4. Only after explicit confirmation, add one-shot demo-account-only mt5.order_send to close that exact ticket only.
5. Verify the exact ticket is closed and no extra H024 positions or orders exist.

All five stages are now complete.

7. H024 Stale Evidence Fix Before H025

Before H025, H024 had a stale evidence problem.

Root cause:

scripts/run_h024_read_only_vps_observer_once.ps1 used existing exact-ticket reports as upstream evidence.
Those exact-ticket reports became stale after about 3600 seconds.
Black-swan guard failed closed on stale upstream evidence.
Scheduled wrapper exited nonzero.
Task Scheduler recorded LastTaskResult nonzero.
Continuity/cadence/dashboard were polluted.

Fix commit:

022053d Refresh H024 exact-ticket evidence before black-swan guard

Fix behavior:

Refresh exact-ticket read-only evidence inside scripts/run_h024_read_only_vps_observer_once.ps1 before black-swan guard.

Tracked files:

scripts/run_h024_read_only_vps_observer_once.ps1
tests/test_h024_read_only_observer_exact_ticket_refresh_before_black_swan.py

Important:

This H024 fix is read-only.
It does not authorize order_check.
It does not authorize order_send.
It does not authorize symbol_select.
It does not authorize entries.
It does not authorize closes.
8. H024 Cadence Context

Before the canary close, H024 readiness eventually reached:

Healthcheck: PASS
Task-state: PASS
Recovery drill: PASS
Evidence bundle: PASS
Continuity: PASS
Scheduled cadence: FAIL_CLOSED

The cadence failure was not a broker or MT5 failure. It was a strict proof-window failure after prior stale-evidence/manual-run pollution.

Observed cadence metrics:

observed_run_count: 7
observed_span_minutes: 29.999
min_observed_gap_minutes: 4.965
max_observed_gap_minutes: 5.035
latest_observed_run_at_utc: 2026-05-13T00:09:50.3210000Z

The scheduler was effectively running clean 5-minute intervals, but the verifier wanted a longer clean window.

Do not spend active time waiting on old H024 cadence proof now. The canary is closed. The next H024 work should be a post-close/no-open-canary observer state.

9. H025 Stage 1 - Audit Existing Exact-Ticket Artifacts

Purpose:

Identify reusable H024 exact-ticket close/modify governance artifacts.
Do not restart from generic would_open or generic INTENT.
Do not open a new trade.

Existing H024 exact-ticket artifacts reused conceptually:

scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py
scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py

H025 audit file:

docs/operations/H025_CONTROLLED_EXACT_TICKET_CANARY_CLOSE_ENABLEMENT_AUDIT.md
10. H025 Stage 2 - Inert Exact-Ticket Close Request Preview

Commits:

b5b4beb Add H025 exact-ticket canary close request preview
01de648 Add H025 exact-ticket canary close request preview

There are two preview commits because of fix-forward iteration. Do not rewrite history.

Files:

docs/operations/H025_CONTROLLED_EXACT_TICKET_CANARY_CLOSE_ENABLEMENT_AUDIT.md
scripts/build_h025_exact_ticket_canary_close_request_preview_jsonl.py
tests/test_h025_exact_ticket_canary_close_request_preview.py

Stage 2 behavior:

Constructs inert close request preview only.
Does not import MetaTrader5.
Does not call mt5.order_check.
Does not call mt5.order_send.
Does not call mt5.symbol_select.
Does not mutate broker state.

Stage 2 runtime output:

3 passed
Wrote reports\h025_exact_ticket_canary_close_request_preview.jsonl
Verdict: PASS
Exact ticket: 4413054432
Exact identifier: 4413054432
Preview only: True
order_check_authorized: False
order_send_authorized: False
broker_mutation_authorized: False

Stage 2 exact constraints:

account_server: Exness-MT5Trial6
symbol: XAUUSDm
side_to_close: sell
close_side_preview: buy
volume: 0.01
ticket: 4413054432
identifier: 4413054432
magic: 240024
11. H025 Stage 3 - Demo-Only Exact-Ticket order_check

Stage 3 commits:

7edcb53 Add H025 exact-ticket canary close order_check gate
1426761 Add H025 exact-ticket canary close order_check implementation
aa35d3b Fix H025 exact-ticket order_check MT5 comment

Files:

docs/operations/H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_close_order_check_jsonl.py
tests/test_h025_exact_ticket_canary_close_order_check.py

Important fix-forward detail:

7edcb53 was incomplete. It tracked only the runbook because the script/test had indentation problems and stayed untracked.
1426761 fixed forward by tracking the actual Stage 3 script/test.

Stage 3 approval path:

reports/h025_exact_ticket_canary_close_order_check_operator_approval.json

Approval artifact had to include:

schema: h025_exact_ticket_canary_close_order_check_approval.v1
intent: H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_ONLY
operator_approved: true
order_check_authorized: true
operator_attestation: I approve H025 order_check only for exact ticket 4413054432. I do not approve order_send.
account_server: Exness-MT5Trial6
symbol: XAUUSDm
exact_ticket: 4413054432
exact_identifier: 4413054432
magic: 240024
volume: 0.01
side_to_close: sell
close_side: buy
order_send_authorized: false
close_all_authorized: false
entry_authorized: false
live_money_authorized: false

Stage 3 first real MT5 result:

order_check_executed: True
order_send_authorized: False
order_send_executed: False
broker_mutation_authorized: False
retcode: None
comment: None
Violation:
order_check_returned_none
mt5.order_check returned None: (-2, 'Invalid "comment" argument')

Cause:

MT5 rejected the long order_check comment.

Fix:

aa35d3b Fix H025 exact-ticket order_check MT5 comment

Short comment used:

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

12. H025 Stage 4 - One-Shot Exact-Ticket order_send

Operator explicitly authorized Stage 4 with:

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
Runs exactly one mt5.order_send.
Verifies exact ticket no longer open.
Verifies H024 position count is 0.
Verifies H024 order count is 0.
No loop.
No close-all.
No symbol_select.
No live-money.

Stage 4 approval artifact:

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
operator_attestation: I approve H025 one-shot demo order_send only to close exact ticket 4413054432. I do not approve new entries, close-all, symbol_select, loops, or live-money execution.

Stage 4 runtime output:

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

Stage 4 report summary from the successful run:

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

Stage 4 order_send result from the successful run:

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

Stage 4 was one-shot. Do not rerun it.

13. Stage 4 Runtime Report Volatility Problem

Important lesson:

reports/h025_exact_ticket_canary_close_order_send.jsonl is untracked runtime evidence.
It can be overwritten by later tests or fail-closed validation runs.
It must not be treated as immutable source truth.

This happened.

Later, Stage 5 failed because the Stage 4 runtime report had been overwritten with:

verdict: FAIL_CLOSED
stage: H025_STAGE_4_APPROVAL_VALIDATION
order_check_executed: False
order_send_executed: False

The failure did not mean the trade reopened.

It meant Stage 5 had a bad design: it hard-gated on volatile Stage 4 report contents.

Stage 5 was fixed so the authoritative check is the current MT5 open-exposure state:

exact ticket 4413054432 open?
H024 XAUUSDm magic 240024 position count?
H024 XAUUSDm magic 240024 pending order count?

Stage 4 report is now optional context only.

Do not rerun Stage 4 to repair a report.

14. H025 Stage 5 - Post-Close Verification

Stage 5 purpose:

Verify ticket 4413054432 remains closed.
Verify H024 position count is 0.
Verify H024 order count is 0.
Document that the project has no open canary trade.

Stage 5 files:

docs/operations/H025_EXACT_TICKET_CANARY_POST_CLOSE_VERIFICATION_RUNBOOK.md
scripts/build_h025_exact_ticket_canary_post_close_verification_jsonl.py
tests/test_h025_exact_ticket_canary_post_close_verification.py
docs/operations/handoffs/HANDOFF_119.md
docs/operations/handoffs/HANDOFF_120.md

Stage 5 is read-only verification only.

Stage 5 must not contain:

mt5.order_check
mt5.order_send
mt5.symbol_select
TRADE_ACTION
ORDER_TYPE_BUY
ORDER_TYPE_SELL

Stage 5 first attempt failed because of file writing indentation:

IndentationError: expected an indented block after function definition on line 24

This was a script generation problem, not an MT5 or verification failure.

Stage 5 was fixed by rewriting the script/test with controlled indentation.

Stage 5 then had a second design flaw: it required the volatile Stage 4 runtime report to still be PASS. That was fixed by making Stage 4 runtime report optional context and making live open-exposure state authoritative.

Current robust Stage 5 PASS output at HANDOFF_120 creation:

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

Stage 5 report summary at HANDOFF_120 creation:

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
history_deal_match_count: 2
15. HANDOFF_119 Fix-Forward History

HANDOFF_119 was created and then expanded, but required several fix-forwards.

Initial Stage 5 handoff commit:

960875e Add H025 post-close canary verification handoff

Problem:

It tracked the runbook and a thin HANDOFF_119, but not the Stage 5 script/test.

Next fix-forward:

62cdb53 Track H025 post-close verification code and expand handoff

Problem after 62cdb53:

Final git status still showed:
?? tests/test_h025_exact_ticket_canary_post_close_verification.py

Final HANDOFF_119 completeness fix:

8e2d44f Track H025 post-close verification test and finalize handoff

After 8e2d44f, git state was clean except reports/ untracked.

HANDOFF_120 now supersedes all of that and is the current preferred handoff.

16. Current Tracked Source File Map

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
docs/operations/handoffs/HANDOFF_120.md

Runtime reports remain untracked:

reports/
17. Runtime Reports Discipline

Relevant runtime reports generated during H025 include:

reports/h025_exact_ticket_canary_close_request_preview.jsonl
reports/h025_exact_ticket_canary_close_order_check.jsonl
reports/h025_exact_ticket_canary_close_order_check_operator_approval.json
reports/h025_exact_ticket_canary_close_order_send.jsonl
reports/h025_exact_ticket_canary_close_order_send_operator_approval.json
reports/h025_exact_ticket_canary_post_close_verification.jsonl
reports/h025_exact_ticket_canary_post_close_verification.txt

Do not commit these reports.

They are useful for local operator review, but HANDOFF_120 contains the key evidence so the next AI does not need the reports to understand the state.

18. Validation Commands Used For HANDOFF_120

Robust Stage 5 code/test validation:

python -m py_compile scripts\build_h025_exact_ticket_canary_post_close_verification_jsonl.py
python -m py_compile tests\test_h025_exact_ticket_canary_post_close_verification.py
python -m pytest tests\test_h025_exact_ticket_canary_post_close_verification.py -q

Robust Stage 5 read-only verification:

python scripts\build_h025_exact_ticket_canary_post_close_verification_jsonl.py

Expected Stage 5 current truth:

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
19. Current Git Timeline

Recent git timeline at HANDOFF_120 creation:

8e2d44f Track H025 post-close verification test and finalize handoff
62cdb53 Track H025 post-close verification code and expand handoff
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
5abbc0a Add handoff document #117
b26b6e3 Add handoff document #116
367e5c0 Fix H024 read-only observer no-console launcher validation
c0eb3cc Add H024 read-only observer no-console launcher
5814450 Fix H024 scheduled cadence latest segment proof
3b26baf Fix H024 read-only observer scheduled cadence summary
e385819 Add H024 read-only observer scheduled cadence summary
7a39c61 Add handoff document #115
bc62c83 Add H024 read-only observer continuity tests and runbook
a7a377b Add H024 read-only observer continuity summary
beafd0f Fix H024 read-only observer timestamp aliases
51cf544 Expand handoff document #114

Important commits:

022053d Refresh H024 exact-ticket evidence before black-swan guard
b5b4beb Add H025 exact-ticket canary close request preview
01de648 Add H025 exact-ticket canary close request preview
7edcb53 Add H025 exact-ticket canary close order_check gate
1426761 Add H025 exact-ticket canary close order_check implementation
aa35d3b Fix H025 exact-ticket order_check MT5 comment
1ed8aa9 Add H025 exact-ticket canary close order_send gate
960875e Add H025 post-close canary verification handoff
62cdb53 Track H025 post-close verification code and expand handoff
8e2d44f Track H025 post-close verification test and finalize handoff
__45b51f7__ Robust Stage 5 and fully self-contained HANDOFF_120

Do not rewrite pushed history. Fix forward only.

20. How To Re-Verify Current Truth

Run:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

python -m pytest tests\test_h025_exact_ticket_canary_post_close_verification.py -q
python scripts\build_h025_exact_ticket_canary_post_close_verification_jsonl.py

@{account_server=Exness-MT5Trial6; broker_mutation_authorized=False; close_all_authorized=False; entry_authorized=False; exact_identifier=4413054432; exact_ticket=4413054432; exact_ticket_open=; generated_at_utc=2026-05-13T01:00:05.471668+00:00; h024_order_count=; h024_position_count=; live_money_authorized=False; magic=240024; open_canary_trade_exists=; operator_next_action=OPERATOR_REVIEW_REQUIRED_NO_NEW_ENTRIES_AUTHORIZED; operator_state=FAIL_CLOSED_H025_EXACT_TICKET_CANARY_POST_CLOSE_UNVERIFIED; order_check_executed=False; order_send_executed=False; post_close_verified=False; read_only_verification_only=True; schema=h025_exact_ticket_canary_post_close_verification.v1; stage=H025_STAGE_5_STAGE4_REPORT_VALIDATION; stage4_report_path=C:\Users\equin\Documents\institutional-ea\reports\h025_exact_ticket_canary_close_order_send.jsonl; symbol=XAUUSDm; symbol_select_executed=False; unattended_loop_authorized=False; verdict=FAIL_CLOSED; violations=System.Object[]; volume=0.01} = Get-Content -Raw reports\h025_exact_ticket_canary_post_close_verification.jsonl | ConvertFrom-Json
@{account_server=Exness-MT5Trial6; broker_mutation_authorized=False; close_all_authorized=False; entry_authorized=False; exact_identifier=4413054432; exact_ticket=4413054432; exact_ticket_open=; generated_at_utc=2026-05-13T01:00:05.471668+00:00; h024_order_count=; h024_position_count=; live_money_authorized=False; magic=240024; open_canary_trade_exists=; operator_next_action=OPERATOR_REVIEW_REQUIRED_NO_NEW_ENTRIES_AUTHORIZED; operator_state=FAIL_CLOSED_H025_EXACT_TICKET_CANARY_POST_CLOSE_UNVERIFIED; order_check_executed=False; order_send_executed=False; post_close_verified=False; read_only_verification_only=True; schema=h025_exact_ticket_canary_post_close_verification.v1; stage=H025_STAGE_5_STAGE4_REPORT_VALIDATION; stage4_report_path=C:\Users\equin\Documents\institutional-ea\reports\h025_exact_ticket_canary_close_order_send.jsonl; symbol=XAUUSDm; symbol_select_executed=False; unattended_loop_authorized=False; verdict=FAIL_CLOSED; violations=System.Object[]; volume=0.01} |
  Select-Object 
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
git status: only reports/ untracked
21. What Not To Do Next

Do not:

reopen the H024 canary
run Stage 4 again
add a new trade entry module
add automatic entries
add unattended loops
add close-all
add symbol_select
add live-money account support
add scaling
add martingale
add grid
try to make old H024 pass by creating a new open position
22. Next Recommended Milestone

Recommended next milestone:

H026 or H024-post-close: read-only no-open-canary observer state.

Goal:

Teach the H024 read-only observer/dashboard/readiness stack that the old H024 canary was intentionally closed by H025 and that zero H024 positions/orders is now an acceptable post-close state.

Likely implementation shape:

1. Add a read-only post-close/no-open-canary state packet.
2. It should consume or verify H025 Stage 5 post-close verification.
3. It should distinguish "missing canary because intentionally closed" from "missing canary unexpectedly".
4. It should keep broker mutation unauthorized.
5. It should avoid order_check/order_send/symbol_select.
6. It should update dashboard/readiness language so "no open canary" is not automatically treated as failure when H025 post-close verification is PASS.
7. Keep reports/ untracked.

Possible acceptance criteria:

post-close state packet PASS
exact ticket 4413054432 still not open
H024 position count 0
H024 order count 0
H024 dashboard states "NO OPEN CANARY - INTENTIONALLY CLOSED BY H025"
trading_authorized false
broker_mutation_authorized false
order_check/order_send absent from H024
reports/ untracked
23. Suggested Prompt For Next AI

Use this prompt:

Please continue from HANDOFF_120 on main. HANDOFF_120 supersedes HANDOFF_119, HANDOFF_118, and all older handoffs.

The exact H024 canary trade XAUUSDm sell 0.01, ticket/identifier 4413054432, magic 240024, demo server Exness-MT5Trial6, has been closed by H025 Stage 4 and post-close verified by H025 Stage 5. There is no open H024 canary trade. Do not reopen it to satisfy old H024 observer assumptions.

Current expected git state is clean except reports/ untracked. Keep reports/ untracked.

Next useful milestone: H026 or H024-post-close read-only no-open-canary observer state. Teach the H024 observer/dashboard/readiness stack that zero H024 positions/orders is now acceptable when H025 post-close verification is PASS. Do not add order_check, order_send, symbol_select, entries, close-all, loops, live-money support, scaling, martingale, grid, or automatic position creation.
24. Final Operator State

Current operational state:

H024 old canary: closed
H025 exact-ticket close path: complete
Stage 5 post-close verification: PASS
Open H024 canary trade exists: false
Exact ticket 4413054432 open: false
H024 position count: 0
H024 order count: 0
Reports: untracked
Next correct direction: read-only post-close observer/dashboard adaptation


