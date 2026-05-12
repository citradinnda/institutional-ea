# HANDOFF_109 — Fully Self-Contained H024 Read-Only Black-Swan Guard Handoff

This handoff is the source of truth for the next AI.

It supersedes HANDOFF_108 and all older handoffs. It preserves every hard safety boundary and captures the completed H024 read-only black-swan guard milestone, including the initial unverified commit, the fix-forward commit, validation outputs, current canary state, final git state, and the next recommended read-only deployment-readiness milestone.

This document is intentionally redundant and self-contained so the next AI does not need to guess repo state, validation state, safety posture, runtime posture, implementation files, failure history, or next steps.

---

## 1. Required Behavior For The Next AI

The next AI must:

1. Read this handoff completely before acting.
2. Preserve every hard safety boundary.
3. Treat all H024 runtime/governance/decision/evidence/preview/guard/deployment-readiness work as read-only unless a future milestone explicitly says otherwise.
4. Never infer that a passing safety/governance/decision/evidence/preview/guard packet authorizes trading.
5. Never call broker mutation functions.
6. Never call order_check.
7. Never call order_send.
8. Never create entries.
9. Never close or modify the current XAUUSDm canary.
10. Never place USDJPY orders.
11. Never place XAUUSD orders.
12. Never scale the existing canary.
13. Never run a trading loop.
14. Never call symbol_select from new safety/governance/decision/evidence/preview/guard/deployment-readiness code.
15. Never build a live broker request from governance, decision, evidence, preview, guard, or deployment-readiness artifacts.
16. Keep reports/ untracked.
17. Fail closed on missing, malformed, stale, inconsistent, ambiguous, unsafe, or unverifiable state.
18. Include module, verifier, tests, scripts, and docs for every new milestone.
19. Prefer focused tests and packet builder/verifier during iteration. Run the full suite only at major boundaries or when explicitly requested.
20. After each milestone, give:
    - concise status summary
    - commit hash
    - final git state
    - one concise suggested next prompt

The user likes concise suggested next prompts after each milestone. Keep doing that.

The user is fatigued by long loops and repeated full-suite runs. Do not make them run thousands of tests during every micro-fix. Use focused tests and builder/verifier during iteration, then run the full suite only at major boundaries or when explicitly needed.

---

## 2. Repo State At This Handoff

Project:

institutional-ea

Local repo path:

C:\Users\equin\Documents\institutional-ea

Branch:

main

Remote:

origin/main

Latest confirmed pushed commit:

67cfc43 Fix H024 black-swan guard validation and timestamp handling

Relevant immediate history:

67cfc43 Fix H024 black-swan guard validation and timestamp handling
f62de7c Add H024 read-only black-swan guard
1a8ec4f Add H024 exact-ticket close modify execution readiness dry-run schema preview
ba9692b Add handoff document #108
e0921f2 Add H024 exact-ticket close modify operator decision v2 preview
9f6e65c Add handoff document #107
8761a57 Add H024 exact-ticket close modify manual approval gate preview

Expected final git status after committing this handoff:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

reports/ is runtime/generated output. It must stay untracked.

---

## 3. Hard Safety Boundary

The current H024 state is post-canary, read-only, no-mutation.

Do not do any of these:

- Do not create a second H024 entry.
- Do not place a live order.
- Do not place a demo order.
- Do not place a USDJPY order.
- Do not place a XAUUSD order.
- Do not scale the existing XAUUSDm canary.
- Do not call order_check.
- Do not call order_send.
- Do not close the XAUUSDm canary.
- Do not modify the XAUUSDm canary.
- Do not modify SL/TP.
- Do not run a trading loop.
- Do not mutate broker/account/symbol state.
- Do not call symbol_select from new safety/governance/decision/evidence/preview/guard/deployment-readiness code.
- Do not build a live broker request from governance, decision, evidence, preview, guard, or deployment-readiness artifacts.
- Do not build an executable trade request dictionary.
- Do not treat any passing safety/governance/decision/evidence/preview/guard/deployment-readiness packet as permission to trade.
- Do not add reports/ to git.

Close/modify is not authorized.

It is not almost authorized.

It is not safe because the canary is known.

It remains prohibited unless a future exact-ticket governance path is separately specified, reviewed, and still initially read-only.

A PASS means the relevant packet is coherent and all action paths remain blocked.

PASS does not authorize action.

Any unsafe ambiguity must fail closed.

---

## 4. Current Known Canary

There is exactly one known H024 standard-demo XAUUSDm canary.

Known identity:

- Server: Exness-MT5Trial6
- Account currency: USD
- Runtime symbol: XAUUSDm
- Model symbol: XAUUSD
- Side: sell
- MT5 position type: 1
- Volume: 0.01
- Magic: 240024
- Ticket/identifier: 4413054432
- Entry deal: 3788869526
- Open price: 4728.4490000000005
- Stop loss: 4817.394

Latest validated black-swan guard state:

- Exact ticket: 4413054432
- Exact identifier: 4413054432
- black_swan_guard_clear: True
- black_swan_guard_triggered: False
- effective_new_entries_blocked: True
- broker_mutation_authorized: False
- order_check_authorized: False
- order_send_authorized: False
- entry_authorized: False
- close_modify_authorized: False
- xauusd_order_authorized: False
- usdjpy_order_authorized: False
- trading_loop_authorized: False
- automatic_execution_authorized: False
- black_swan_guard_authorizes_trading: False
- live_broker_request_constructed: False
- executable_trade_request_constructed: False
- mt5_request_dictionary_constructed: False

The position being open over three bars remains classified upstream as:

OPERATOR_REPORTED_ONLY

This is non-authorizing context only.

It does not authorize:

- close
- modify
- scale
- new entry
- USDJPY order
- XAUUSD order
- order_check
- order_send
- trading loop
- broker request construction

---

## 5. Existing H024 Stack Summary

### 5.1 Runtime Safety Lockout Reader

Commit:

98efc2a Add H024 runtime safety lockout reader

Purpose:

Read committed default safety config and local lockout state. Supports global no-new-entry, manual override lockout, and per-symbol XAUUSD/USDJPY no-new-entry lockouts.

Passing operator state:

LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Key files:

- config/h024_runtime_safety/default_lockout_config.json
- quantcore/execution/h024_runtime_safety_lockout.py
- scripts/build_h024_runtime_safety_lockout_jsonl.py
- scripts/verify_h024_runtime_safety_lockout_jsonl.py
- tests/test_h024_runtime_safety_lockout.py

### 5.2 Runtime Safety Heartbeat Packet

Commit:

187e9dd Add H024 runtime safety heartbeat packet

Purpose:

Read-only MT5 runtime heartbeat. Verifies MT5 initialization, account availability, expected server, USD account currency, and terminal/account heartbeat freshness where available.

Passing operator state:

RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED

Expected server:

Exness-MT5Trial6

Expected currency:

USD

### 5.3 Runtime Tick/Spread Safety Supervisor

Commit:

abecff8 Add H024 runtime tick and spread safety supervisor

Purpose:

Read-only market-data supervisor. Verifies XAUUSDm and USDJPYm tick availability, bid/ask sanity, ask > bid, positive spread, spread thresholds, tick freshness, and symbol visibility/readability without selecting symbols.

Important:

Do not call symbol_select.

Passing operator state:

TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED

### 5.4 Runtime Exposure/Inventory Safety Supervisor

Commit:

0db61fa Add H024 runtime exposure inventory safety supervisor

Purpose:

Read-only inventory supervisor. Allows only no H024 inventory or the exact known XAUUSDm canary. Rejects H024 USDJPY position/order, H024 pending/open order, extra H024 position, and mismatched XAUUSDm canary identity.

Known canary allowed fields:

- symbol: XAUUSDm
- ticket or identifier: 4413054432
- magic: 240024
- volume: 0.01
- type: 1

Passing operator state:

EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED

### 5.5 Runtime Account Risk/Margin Safety Supervisor

Commit:

1c331c6 Add H024 runtime account risk margin safety supervisor

Purpose:

Read-only account risk/margin supervisor. Verifies server, USD account context, balance sanity, equity sanity, margin sanity, free margin sanity, margin level sanity where available, floating PnL consistency where available, and canary exposure boundedness.

Passing operator state:

ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED

Important field-shape lesson:

The runtime account packet may expose free margin as margin_free rather than free_margin. Downstream extractors should support aliases when consuming real MT5-derived packets.

### 5.6 Runtime Safety Aggregate Supervisor

Commit:

8e8979c Add H024 runtime safety aggregate supervisor

Purpose:

Aggregates all runtime safety packets into one fail-closed operator verdict. Prevents cherry-picking one passing packet while ignoring failing upstream evidence.

Passing operator state:

RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED

### 5.7 Unified Read-Only Post-Canary Runtime Supervision

Commit:

224371a Add H024 unified read-only runtime supervision

Purpose:

Operator-facing wrapper combining one-shot canary read-only supervision and runtime safety aggregate supervisor.

Passing operator state:

UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED

### 5.8 Runtime No-Mutation Safety Gate Contract

Commit:

5249ad1 Add H024 runtime no-mutation safety gate

Purpose:

Read-only no-mutation gate contract. Future broker-facing code must check this gate. The gate proves current state blocks broker mutation, entries, close/modify, order_check, order_send, XAUUSD order, USDJPY order, trading loop, and automatic execution.

Passing operator state:

NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED

Known frozen legacy exceptions:

- run_h024_one_shot_demo_canary.py
- h024_one_shot_demo_canary.py
- log_h024_mt5_terminal_preflight.py

These are historical/pre-gate artifacts only. They are not current authorization.

---

## 6. Exact-Ticket Close/Modify Governance, Decision, Evidence, And Preview Stack

### 6.1 Exact-Ticket Close/Modify Governance Specification Packet

Original commit:

94d3b96 Add H024 exact-ticket canary close modify governance spec

Follow-up fix:

b82d48c Fix H024 exact-ticket governance canary state evidence

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED

Purpose:

Defines read-only governance requirements that must be coherent before any future exact-ticket canary close/modify could even be considered.

It does not authorize close/modify.

### 6.2 Exact-Ticket Close/Modify Decision Artifact Validator

Commit:

9f061c1 Add H024 exact-ticket close modify decision artifact validator

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED

Purpose:

Validates explicit human/operator decision artifact schema for exact-ticket close/modify governance while still authorizing no action.

### 6.3 Exact-Ticket Close/Modify Pre-Action Evidence Aggregate

Initial implementation:

86774c4 Add H024 exact-ticket close modify pre-action evidence aggregate

Intermediate fix:

10b4a14 Fix H024 pre-action evidence aggregate identity validation

Final validated fix:

e370a60 Fix H024 pre-action aggregate upstream validation path

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED

Purpose:

Consumes and cross-checks runtime no-mutation gate, unified runtime supervision, governance, decision artifact, and fresh runtime account/exposure/tick evidence.

### 6.4 Exact-Ticket Close/Modify Bar-Age And Exit-Condition Evidence

Commit:

8065262 Add H024 exact-ticket close modify bar-age exit-condition evidence

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED

Current passing classification:

OPERATOR_REPORTED_ONLY

Purpose:

Converts the operator statement that the exact XAUUSDm canary has been open for over three bars into structured read-only evidence while authorizing no action.

### 6.5 Exact-Ticket Close/Modify Manual Approval Gate Preview

Commit:

8761a57 Add H024 exact-ticket close modify manual approval gate preview

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED

Purpose:

Defines a strict read-only manual approval gate preview for future operator review of closing or modifying only the known XAUUSDm canary ticket/identifier 4413054432.

### 6.6 Exact-Ticket Close/Modify Operator Decision V2 Preview

Commit:

e0921f2 Add H024 exact-ticket close modify operator decision v2 preview

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED

Purpose:

Upgrades the static exact-ticket close/modify decision artifact into a stricter read-only operator-intent preview schema that can express future manual intent to close or modify only the known XAUUSDm canary while still authorizing no action.

Important fix from that milestone:

The account risk/margin snapshot extractor now supports margin_free/free_margin aliases.

### 6.7 Exact-Ticket Close/Modify Execution Readiness Dry-Run Schema Preview

Commit:

1a8ec4f Add H024 exact-ticket close modify execution readiness dry-run schema preview

Passing operator state:

EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED

Purpose:

Defines an abstract, non-executable execution-readiness dry-run schema preview for a possible future exact-ticket close/modify path.

It still:

- constructs no live broker request
- constructs no executable trade request dictionary
- calls no order_check
- calls no order_send
- calls no symbol_select
- authorizes no close/modify
- authorizes no entry
- authorizes no trading loop

Final validation for this milestone:

- Focused tests: 14 passed
- Builder: PASS
- Verifier: PASS
- Violations: 0
- Final git state: only reports/ untracked

---

## 7. Milestone Completed In HANDOFF_109

### H024 Read-Only Black-Swan Guard Packet

Initial implementation commit:

f62de7c Add H024 read-only black-swan guard

Final validated fix-forward commit:

67cfc43 Fix H024 black-swan guard validation and timestamp handling

Purpose:

Adds a read-only fail-closed black-swan guard packet that consumes the H024 runtime safety layer and exact-ticket close/modify preview stack to detect extreme-risk or unsafe runtime conditions while authorizing no action.

It consumes latest available JSONL reports for:

- runtime heartbeat
- runtime lockout reader
- runtime tick/spread supervisor
- runtime exposure/inventory supervisor
- runtime account risk/margin supervisor
- runtime safety aggregate
- unified read-only runtime supervision
- runtime no-mutation safety gate
- exact-ticket close/modify governance
- exact-ticket decision artifact validator
- pre-action evidence aggregate
- bar-age and exit-condition evidence
- manual approval gate preview
- operator decision v2 preview
- execution readiness dry-run schema preview

It detects/fails closed on:

- missing upstream report
- malformed upstream JSONL
- stale upstream evidence
- upstream verdict not PASS
- upstream embedded violations
- unsafe authorization true
- active global/manual/symbol lockout
- heartbeat disconnected/account unavailable where represented
- bid/ask inversion
- extreme spread
- non-positive account balance
- non-positive account equity
- negative free margin
- low margin level
- extreme equity-to-balance drawdown ratio
- known exact-ticket XAUUSDm canary not observed
- unexpected H024 pending/open orders
- unexpected H024 USDJPY exposure
- extra H024 exposure
- missing exact canary identity lock
- executable broker/trade request object
- live broker request object
- MT5 request dictionary object
- order_check request object
- order_send request object

Passing operator state:

BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED

Passing operator next action:

CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED

Fail-closed operator state:

FAIL_CLOSED_BLACK_SWAN_GUARD_ACTIVE_OR_UNVERIFIED_NO_TRADING_AUTHORIZED

Fail-closed operator next action:

FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED

Key files added by f62de7c:

- quantcore/execution/h024_read_only_black_swan_guard.py
- scripts/build_h024_read_only_black_swan_guard_jsonl.py
- scripts/verify_h024_read_only_black_swan_guard_jsonl.py
- tests/test_h024_read_only_black_swan_guard.py
- docs/operations/H024_READ_ONLY_BLACK_SWAN_GUARD.md

Report path:

reports/h024_read_only_black_swan_guard.jsonl

---

## 8. HANDOFF_109 Failure History And Lessons

### 8.1 Initial test failure: duplicate keyword overrides

Initial focused test run after f62de7c generation:

- collected 17 items
- 11 passed
- 6 failed

Failures were in tests that used override dictionaries for default upstream fixture fields.

Representative failure:

TypeError: _base_upstream_record() got multiple values for keyword argument 'manual_override_lockout_active'

Root cause:

The test helper constructed upstream records with explicit defaults plus **overrides. If overrides contained a duplicate field such as bid, spread, margin_free, margin_level, h024_order_count, or manual_override_lockout_active, Python received duplicate keyword arguments.

Resolution:

The fix-forward commit 67cfc43 added _merge_defaults(defaults, overrides) so defaults are merged first and overrides are applied once.

Lesson:

For generated test fixtures, merge defaults into a dict before passing **kwargs. Do not pass explicit keyword defaults and **overrides in the same call when tests intentionally override those keys.

### 8.2 Initial real builder fail-closed: lockout timestamp shape

Initial real black-swan builder output:

Verdict: FAIL_CLOSED
Violations: 1
Operator state: FAIL_CLOSED_BLACK_SWAN_GUARD_ACTIVE_OR_UNVERIFIED_NO_TRADING_AUTHORIZED
Operator next action: FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED
black_swan_guard_clear: False
black_swan_guard_triggered: True

Verifier output:

Violations: 2
Verifier verdict: FAIL
VIOLATION: record 1: embedded violation: runtime_lockout_reader: missing or malformed observed_at_utc
VIOLATION: record 1: --require-pass rejects verdict FAIL_CLOSED

Root cause:

The real runtime lockout reader packet did not expose the timestamp under the exact top-level observed_at_utc shape expected by the initial black-swan guard implementation.

Resolution:

The fix-forward commit 67cfc43 added upstream timestamp alias handling through TIMESTAMP_KEYS and upstream_timestamp_value(), supporting:

- observed_at_utc
- generated_at_utc
- created_at_utc
- evaluated_at_utc
- built_at_utc
- timestamp_utc
- timestamp

It also searches nested records for these timestamp keys.

Lesson:

Downstream aggregate/guard packets must consume real upstream packet shapes robustly. Timestamp extraction must support canonical and alias keys, including nested packet fields.

### 8.3 Native command failure did not stop first block

The first implementation block continued after pytest and verifier failures and created commit f62de7c.

Root cause:

PowerShell does not automatically stop on native command nonzero exit codes just because $ErrorActionPreference = "Stop" is set.

Resolution:

Subsequent blocks used a Run-Native helper that checks $LASTEXITCODE and throws.

Lesson:

For future PowerShell command blocks, wrap native commands such as python, pytest, git diff, git commit, and git push with Run-Native or explicitly check $LASTEXITCODE.

### 8.4 Push failed once due DNS/network

Initial push after f62de7c failed:

fatal: unable to access 'https://github.com/citradinnda/institutional-ea.git/': Could not resolve host: github.com

Root cause:

Temporary DNS/network failure.

Resolution:

After the fix-forward commit 67cfc43, git push succeeded and pushed both f62de7c and 67cfc43.

### 8.5 Shell syntax mistakes during fix-forward

Two non-repo issues occurred while patching:

1. PowerShell interpolation bug:
   - throw "Command failed with exit code $LASTEXITCODE: ..."
   - PowerShell treated $LASTEXITCODE: as invalid scoped-variable syntax.
   - Fixed with ${LASTEXITCODE}.

2. Bash heredoc used in PowerShell:
   - python - <<'PY'
   - PowerShell does not support Bash heredoc redirection.
   - Fixed by using PowerShell file text operations instead.

Lesson:

Use PowerShell-native syntax only in command blocks for this user.

---

## 9. Validation Status At HANDOFF_109

### 9.1 Final Focused Test Validation

Final focused test run:

collected 17 items

tests\test_h024_read_only_black_swan_guard.py ................. [100%]

17 passed in 4.53s

### 9.2 Runtime Lockout Refresh

Final lockout builder output:

Wrote reports\h024_runtime_safety_lockout.jsonl
Verdict: PASS
Violations: 0
Operator state: LOCKOUTS_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Lockout inputs valid: True
Lockout triggered: False
Active lockouts: 0
Fail-closed lockouts: 0
Effective new entries blocked: True
Broker mutation authorized: False
Order check authorized: False
Order send authorized: False
Entry authorized: False
Close/modify authorized: False
XAUUSD order authorized: False
USDJPY order authorized: False
Trading loop authorized: False
Automatic execution authorized: False

### 9.3 Execution Readiness Dry-Run Schema Preview Refresh

Final execution readiness builder output:

Wrote reports\h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW
Exact ticket: 4413054432
Exact identifier: 4413054432
effective_new_entries_blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
execution_readiness_dry_run_schema_preview_constructed: True
execution_readiness_dry_run_schema_preview_authorizes_execution: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False

### 9.4 Black-Swan Guard Builder

Final black-swan guard builder output:

Wrote reports\h024_read_only_black_swan_guard.jsonl
Verdict: PASS
Violations: 0
Operator state: BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Operator next action: CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
black_swan_guard_clear: True
black_swan_guard_triggered: False
effective_new_entries_blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
black_swan_guard_authorizes_trading: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False

### 9.5 Black-Swan Guard Verifier

Final black-swan guard verifier output:

H024 read-only black-swan guard records: 1
Violations: 0
Verifier verdict: PASS
Record verdict: PASS
Operator state: BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Operator next action: CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
black_swan_guard_clear: True
black_swan_guard_triggered: False
effective_new_entries_blocked: True
broker_mutation_authorized: False
order_check_authorized: False
order_send_authorized: False
entry_authorized: False
close_modify_authorized: False
xauusd_order_authorized: False
usdjpy_order_authorized: False
trading_loop_authorized: False
automatic_execution_authorized: False
black_swan_guard_authorizes_trading: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False

### 9.6 Commit And Push

Initial implementation commit:

[main f62de7c] Add H024 read-only black-swan guard
 5 files changed, 1492 insertions(+)
 create mode 100644 docs/operations/H024_READ_ONLY_BLACK_SWAN_GUARD.md
 create mode 100644 quantcore/execution/h024_read_only_black_swan_guard.py
 create mode 100644 scripts/build_h024_read_only_black_swan_guard_jsonl.py
 create mode 100644 scripts/verify_h024_read_only_black_swan_guard_jsonl.py
 create mode 100644 tests/test_h024_read_only_black_swan_guard.py

Fix-forward commit:

[main 67cfc43] Fix H024 black-swan guard validation and timestamp handling
 2 files changed, 94 insertions(+), 43 deletions(-)

Push output:

To https://github.com/citradinnda/institutional-ea.git
   1a8ec4f..67cfc43  main -> main

Final git status after push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

Final log:

67cfc43 (HEAD -> main, origin/main) Fix H024 black-swan guard validation and timestamp handling
f62de7c Add H024 read-only black-swan guard
1a8ec4f Add H024 exact-ticket close modify execution readiness dry-run schema preview
ba9692b Add handoff document #108
e0921f2 Add H024 exact-ticket close modify operator decision v2 preview
9f6e65c Add handoff document #107
8761a57 Add H024 exact-ticket close modify manual approval gate preview

---

## 10. Verification Block For The Next AI

The next AI should start by asking the user to run this block:

cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

git status
git log --oneline -10

python -m pytest tests\test_h024_read_only_black_swan_guard.py

python scripts\build_h024_runtime_safety_lockout_jsonl.py
python scripts\build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars
python scripts\build_h024_read_only_black_swan_guard_jsonl.py
python scripts\verify_h024_read_only_black_swan_guard_jsonl.py reports\h024_read_only_black_swan_guard.jsonl --require-pass

git status

Expected:

- HEAD is 67cfc43 or a later handoff commit.
- Focused black-swan guard tests pass.
- Runtime lockout builder PASS.
- Execution readiness dry-run schema preview builder PASS.
- Black-swan guard builder PASS.
- Black-swan guard verifier PASS.
- Violations: 0.
- black_swan_guard_clear: True.
- black_swan_guard_triggered: False.
- All authorization fields remain false.
- live_broker_request_constructed false.
- executable_trade_request_constructed false.
- mt5_request_dictionary_constructed false.
- Final git status shows only reports/ untracked, unless a new handoff has just been created.

If upstream evidence is stale, refresh upstream packets immediately before building dependent packets. Staleness is expected fail-closed behavior and not necessarily a code bug.

---

## 11. Core Implementation Pattern For Future Milestones

Every new H024 runtime/governance/decision/evidence/preview/guard/deployment-readiness milestone should include:

- quantcore/execution/<module>.py
- scripts/build_<packet>_jsonl.py
- scripts/verify_<packet>_jsonl.py
- tests/test_<packet>.py
- docs/operations/<PACKET_DOC>.md

Every packet should include:

- schema_version
- strategy = H024
- packet_type
- observed_at_utc
- expected
- observed or upstream records/summaries
- checks
- authorizations
- effective_new_entries_blocked = True
- broker_mutation_authorized = False
- order_check_authorized = False
- order_send_authorized = False
- entry_authorized = False
- close_modify_authorized = False
- xauusd_order_authorized = False
- usdjpy_order_authorized = False
- trading_loop_authorized = False
- automatic_execution_authorized = False
- live_broker_request_constructed = False
- executable_trade_request_constructed = False
- mt5_request_dictionary_constructed = False
- operator_state
- operator_next_action
- violations
- verdict

Verifier should fail closed on:

- missing records
- malformed JSONL
- wrong schema version
- wrong strategy
- wrong packet type
- missing/malformed/stale upstream
- unexpected PASS with embedded violations
- any authorization not false
- effective_new_entries_blocked not true
- executable broker/trade request object
- --require-pass with record verdict not PASS

Tests should include:

- passing happy path
- missing input fails closed
- malformed input fails closed
- stale input fails closed
- wrong strategy or packet type fails closed
- unsafe authorization true fails verifier
- missing authorization fails verifier
- embedded violations fail verifier
- --require-pass rejects fail-closed record
- static no-mutation checks when relevant
- real upstream packet shape regressions
- field alias regressions when consuming MT5-derived account/risk/tick/exposure/lockout packets
- PowerShell workflow should use Run-Native or explicit LASTEXITCODE checks for native commands

---

## 12. Commit Discipline

For every milestone:

git status

python -m pytest <focused test file>

python <build script>
python <verify script> <report path> --require-pass

git status
git add -- <only intended tracked files>
git diff --cached --check
git commit -m "<clear commit message>"
git push
git status

Important:

PowerShell does not stop automatically on native command nonzero exit codes. Use a helper like:

function Run-Native {
    param(
        [Parameter(Mandatory=$true)][string]$Exe,
        [Parameter(ValueFromRemainingArguments=$true)][string[]]$Args
    )
    & $Exe @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Exe $($Args -join ' ')"
    }
}

For major milestones, run:

python -m pytest

But do not make the user rerun the full suite after every tiny patch. Use focused tests and packet verifiers for iteration.

Never add reports/.

Never commit if the milestone verifier fails under --require-pass.

Expected final status after commit and push:

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present

---

## 13. Static Safety Expectations

Known frozen legacy exceptions:

- run_h024_one_shot_demo_canary.py
- h024_one_shot_demo_canary.py
- log_h024_mt5_terminal_preflight.py

These are frozen legacy/pre-gate artifacts. They are not authorized by the no-mutation gate.

For decision/governance/evidence/preview/guard/deployment-readiness code specifically, no new broker mutation call sites are acceptable.

Do not introduce:

- order_send
- order_check
- symbol_select
- MetaTrader5 mutation call sites
- trade request construction for live close/modify
- SL/TP modify requests
- close requests
- trading loops

Read-only introspection and JSON/JSONL packet construction are acceptable when fail-closed and non-authorizing.

---

## 14. Operator Language To Preserve

Use these interpretations consistently:

PASS = read-only safety/governance/decision/evidence/preview/guard/deployment-readiness packet is coherent
PASS != trading authorized
PASS != close/modify authorized
PASS != order_check authorized
PASS != order_send authorized
PASS != broker mutation authorized
PASS != live broker request authorized

Preferred wording:

- OK but trading not authorized
- OK but action not authorized
- fail closed
- read-only observation
- operator review required
- no broker mutation authorized
- current state remains blocked
- action not authorized
- preview only
- coherent for operator review only
- black-swan guard clear but trading not authorized

Avoid wording like:

- ready to trade
- safe to execute
- approved to close
- approved to modify
- can proceed with order
- close approved
- modify approved
- ready for broker request
- deployment means trading enabled

---

## 15. Deployment Reality Check

The user wants this fully automated on a VPS and eventually trading.

Current realistic status:

Read-only VPS deployment/monitoring mode is close.

Live broker-affecting trading is still deliberately not close.

Already implemented:

- runtime lockouts
- heartbeat
- tick/spread supervisor
- exposure/inventory supervisor
- account risk/margin supervisor
- runtime safety aggregate
- unified read-only runtime supervision
- no-mutation gate
- exact-ticket close/modify governance packet
- decision artifact validator
- pre-action evidence aggregate
- bar-age/exit-condition evidence
- manual approval gate preview
- operator decision v2 preview
- execution readiness dry-run schema preview
- read-only black-swan guard

Still not authorized:

- order_check
- order_send
- live broker request construction
- executable request dictionary
- close/modify
- SL/TP modification
- new entry
- trading loop
- automatic execution

Therefore, the next deployment-oriented milestone should still be read-only: a VPS deployment readiness aggregate and operator runbook packet.

---

## 16. Recommended Next Milestone

Recommended next milestone:

H024 read-only VPS deployment readiness aggregate and observer runbook packet

Purpose:

Move toward real VPS automation without enabling trading. This packet should verify that the system is ready to run as a read-only observer on a VPS, with fail-closed runtime packet generation and operator-visible reports, while still authorizing no broker mutation and no trading loop.

It should consume:

- runtime heartbeat
- runtime lockout reader
- tick/spread supervisor
- exposure/inventory supervisor
- account risk/margin supervisor
- runtime safety aggregate
- unified runtime supervision
- runtime no-mutation safety gate
- exact-ticket close/modify governance stack
- operator decision v2 preview
- execution readiness dry-run schema preview
- read-only black-swan guard

It should produce:

h024_read_only_vps_deployment_readiness_aggregate

Suggested module:

quantcore/execution/h024_read_only_vps_deployment_readiness_aggregate.py

Suggested scripts:

scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py
scripts/verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py

Suggested tests:

tests/test_h024_read_only_vps_deployment_readiness_aggregate.py

Suggested docs:

docs/operations/H024_READ_ONLY_VPS_DEPLOYMENT_READINESS_AGGREGATE.md

Suggested report path:

reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl

Suggested commit message:

Add H024 read-only VPS deployment readiness aggregate

It must include:

- exact canary identity lock
- upstream freshness checks
- black-swan guard consumption
- lockout reader consumption
- no-mutation gate consumption
- read-only observer mode declaration
- report output expectations
- local logs/reports path checks
- scheduled-run command preview that is non-executable or operator-review-only
- no broker mutation authorization
- no order_check authorization
- no order_send authorization
- no close/modify authorization
- no new entry authorization
- no executable trade request
- no live broker request
- no trading loop
- no symbol_select
- fail-closed if any upstream packet is missing/stale/fail-closed
- fail-closed if black-swan guard is triggered
- fail-closed if reports/ cannot be written
- fail-closed if any generated deployment/runbook command implies trading or mutation

Passing state should mean:

Read-only VPS observer deployment readiness is coherent for operator review.

Passing state must not mean:

- trading is authorized
- close/modify is authorized
- VPS should run a trading loop
- broker request construction is authorized
- order_check/order_send is authorized

---

## 17. Suggested Next Prompt For Another AI

Give the next AI this prompt:

Please read docs/operations/handoffs/HANDOFF_109.md carefully and follow it exactly. It is fully self-contained and supersedes older handoffs. Continue from there, preserve all hard safety boundaries, and keep giving me concise suggested next prompts after each milestone.

First verify the local base state from HANDOFF_109. Then implement the H024 read-only VPS deployment readiness aggregate and observer runbook packet. It must consume runtime heartbeat, runtime lockout reader, tick/spread supervisor, exposure/inventory supervisor, account risk/margin supervisor, runtime safety aggregate, unified read-only runtime supervision, runtime no-mutation safety gate, the exact-ticket close/modify governance/decision/evidence/preview stack, execution readiness dry-run schema preview, and the read-only black-swan guard. It must verify read-only observer deployment readiness for VPS automation without enabling trading. It must fail closed on missing, malformed, stale, ambiguous, inconsistent, unsafe, or unverifiable upstream evidence. It must authorize no broker mutation, no order_check, no order_send, no entries, no close/modify, no executable trade request, no live broker request, no symbol_select, and no trading loop. Include module, verifier, tests, scripts, and docs. Keep reports/ untracked. Use focused tests and packet verifiers during iteration, and do not make me run the full suite after every tiny patch.

---

## 18. How The Next AI Should Start

The next AI should respond:

Understood. Continuing from HANDOFF_109 at validated fix-forward commit 67cfc43. Current state is read-only H024 post-canary runtime supervision with a no-mutation gate, exact-ticket close/modify governance/decision/evidence/preview stack, execution-readiness dry-run schema preview, and read-only black-swan guard. All broker mutation and trading paths remain blocked. Please run the HANDOFF_109 verification block so I can confirm local state before the read-only VPS deployment readiness aggregate milestone.

Then provide the verification block from Section 10.

---

## 19. Final Reminder

Current H024 posture:

- Observe only.
- Supervise only.
- Specify governance only.
- Validate decision artifacts only.
- Aggregate read-only evidence only.
- Classify bar-age / exit-condition evidence only.
- Preview manual approval gate only.
- Preview operator decision v2 only.
- Preview execution-readiness dry-run schema only.
- Guard black-swan conditions read-only only.
- Fail closed.
- Authorize nothing.
- Keep reports/ untracked.

The next milestone should move toward VPS read-only observer deployment, not live trading.

Do not skip safety boundaries.

Do not trade.

Do not close or modify.

Do not build a live broker request.

Do not build an executable trade request dictionary.

Do not run a trading loop.

Important operator preference / project direction:

The user is tired of endless governance-only milestones. Do not keep inventing more governance, preview, simulator, or abstract schema layers unless they directly unlock deployment progress.

Current honest project status:
- Safety/governance architecture is strong.
- Read-only supervision is mature enough to move toward VPS observer deployment.
- Actual live automated trading is still blocked and must remain blocked for now.
- The next useful phase is operationalization, not another abstract approval artifact.

Priority now:
1. Get the system running as a read-only VPS observer.
2. Produce repeatable scheduled report generation.
3. Produce an operator runbook with exact commands.
4. Verify logs/reports paths, environment assumptions, Python venv, MT5 availability, and fail-closed behavior.
5. Make it easy to run continuously without trading.
6. Only after read-only VPS observer mode is stable should the project move toward execution-path rehearsal.

Do not say “deployment” if you only mean another governance document.
Deployment now means:
- VPS-compatible read-only runner
- scheduled packet generation
- black-swan guard included
- no-mutation gate included
- health/status output
- clear operator commands
- no order_check
- no order_send
- no symbol_select
- no broker mutation
- no trading loop that can place orders
- reports/ remains untracked

The user wants real progress toward automation. Respect that by building operational read-only infrastructure next, not another theoretical schema unless it is strictly necessary for the VPS observer runner.

Hard boundary:
No live trading yet. No close/modify. No executable trade request. No broker mutation. But stop over-rotating into endless governance. Build the read-only VPS observer deployment readiness and runner path next.

The user wants operational read-only VPS automation now, not another never-ending governance ladder. Preserve safety, but build something runnable.