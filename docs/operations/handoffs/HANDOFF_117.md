# HANDOFF_117 — Fully Self-Contained H024 Free Local Windows No-Console Natural Scheduler Proof PASS

This handoff supersedes HANDOFF_116, HANDOFF_115, HANDOFF_114, HANDOFF_113, HANDOFF_112, HANDOFF_111, HANDOFF_110, and all older handoffs.

This is the source of truth for the next AI.

It is intentionally redundant and operationally explicit. The next AI should not need hidden chain-of-thought, chat history, older handoffs, or generated `reports/` files to understand where the project is, what has been proven, what must remain forbidden, what commands were run, and what the next read-only milestone should be.

---

## 1. Executive Summary

Project:

```text
institutional-ea
```

Current module/track:

```text
H024
```

Repository path:

```text
C:\Users\equin\Documents\institutional-ea
```

Branch:

```text
main
```

Current target:

```text
free local Windows recurring read-only observer proof
```

This is not Oracle VPS.

This is not paid VPS.

No Oracle VPS is assumed to exist.

No paid Windows VPS should be recommended unless the user explicitly changes direction.

The current completed milestone is:

```text
H024 local Windows no-console scheduled observer natural-run proof: PASS
```

The scheduled observer uses Windows Task Scheduler and now launches through `wscript.exe` with a VBS hidden launcher to avoid visible PowerShell popups while preserving the existing 5-minute interval.

Verified scheduled task action:

```text
Execute:   wscript.exe
Arguments: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs
```

Verified operational packets after consuming existing natural scheduled cadence evidence:

```text
healthcheck               PASS 0 violations
task_state                PASS 0 violations
recovery_drill_preview    PASS 0 violations
evidence_bundle           PASS 0 violations
continuity_summary        PASS 0 violations
scheduled_cadence_summary PASS 0 violations
```

Final git state after verification:

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
```

`reports/` remains generated runtime evidence and must remain untracked.

---

## 2. User Direction And Strategic Constraint

The user explicitly wants free local proof first.

Correct interpretation:

1. Continue with local Windows execution.
2. Use the user’s existing local MT5.
3. Use local PowerShell.
4. Use the local Python virtual environment.
5. Use local Windows Task Scheduler.
6. Use local generated `reports/`.
7. Do not move to Oracle VPS now.
8. Do not move to paid VPS now.
9. Do not turn this into a live-trading EA.
10. Do not drift into abstract governance-only milestones that do not improve local operational proof.

The user has been frustrated by the project becoming too governance-heavy and too many steps before a demo deployment. The correct style is:

```text
operational, concise, read-only, proof-oriented, and self-contained
```

The user also likes receiving the next concise operational prompt after each milestone.

---

## 3. Absolute Safety Boundary

The project remains read-only.

Do not enable trading.

Do not add any of the following:

```text
order_check
order_send
live broker request construction
executable trade request construction
MT5 trade request dictionaries
automatic entries
automatic close/modify
manual approval code that actually closes/modifies
SL/TP modification
broker mutation
symbol_select
order-capable trading loops
code paths that close the canary
code paths that modify the canary
code paths that scale the canary
code paths that place XAUUSD orders
code paths that place USDJPY orders
```

Interpretation rule:

```text
PASS = evidence/check/packet is coherent for read-only observation only.
PASS != authorization to trade.
PASS != authorization to close.
PASS != authorization to modify.
PASS != authorization to call order_check.
PASS != authorization to call order_send.
PASS != authorization to construct broker requests.
PASS != authorization to run an order-capable loop.
```

Forbidden action remains forbidden even if every packet is PASS.

Allowed work:

```text
read-only MT5/account/symbol/position introspection
JSON/JSONL packet generation
verifiers
read-only local runner scripts
read-only scheduler scripts
read-only healthcheck scripts
read-only task-state audit scripts
read-only recovery drill preview scripts
read-only evidence bundle scripts
read-only continuity summary scripts
read-only scheduled cadence summary scripts
local JSON/text/console alerts
log capture and rotation
local evidence aggregation
operator runbooks
focused tests
fail-closed behavior
```

---

## 4. Current Deployment Architecture

Current free-first architecture:

```text
Local Windows PC
+ Windows Task Scheduler
+ wscript.exe
+ hidden VBS launcher
+ scheduled PowerShell wrapper
+ local Python virtual environment
+ local MT5 terminal
+ local Git repository
+ generated reports/
= free recurring read-only observer proof
```

The historical script names still contain `vps`, but the current target is local Windows, not VPS.

Do not interpret `vps` in script names as proof that a VPS exists.

Do not assume Linux.

Do not assume SSH.

Do not assume Oracle Cloud.

Do not assume paid hosting.

---

## 5. Current Scheduled Task State

Task name:

```text
H024 Read Only VPS Observer
```

Current action:

```text
Execute: wscript.exe
Arguments: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs
```

Current cadence:

```text
5 minutes
```

The 5-minute interval must remain unchanged unless the user explicitly requests a change.

Important context:

The user complained that a PowerShell popup appeared every 5 minutes and interrupted work.

Initial attempted action:

```text
powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "<wrapper>"
```

This still flashed.

Current fix:

```text
wscript.exe <raw path to VBS launcher>
```

Verified no-console launcher path:

```text
C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs
```

The correct task-action update shape is:

```powershell
$Action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument $LauncherPath
Set-ScheduledTask -TaskName $TaskName -Action $Action | Out-Null
```

Do not use fragile nested quote escaping such as:

```powershell
-Argument ""$LauncherPath""
```

---

## 6. No-Console Launcher

Launcher file:

```text
scripts/run_h024_read_only_vps_observer_scheduled_hidden.vbs
```

Expected behavior:

1. Create `WScript.Shell`.
2. Set current directory to repo root.
3. Build a PowerShell command that calls the existing scheduled wrapper.
4. Run it hidden with window style `0`.
5. Wait for completion.
6. Preserve the wrapper exit code with `WScript.Quit exitCode`.
7. Make no MT5 calls itself.
8. Make no broker mutation.
9. Make no trading API calls.
10. Authorize no trading.

Expected logical content:

```vbscript
Option Explicit

Dim shell
Dim repoRoot
Dim wrapperPath
Dim command
Dim exitCode

Set shell = CreateObject("WScript.Shell")

repoRoot = "C:\Users\equin\Documents\institutional-ea"
wrapperPath = repoRoot & "\scripts\run_h024_read_only_vps_observer_scheduled.ps1"

shell.CurrentDirectory = repoRoot

command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File " & Chr(34) & wrapperPath & Chr(34)

exitCode = shell.Run(command, 0, True)

WScript.Quit exitCode
```

Related runbook:

```text
docs/operations/H024_READ_ONLY_VPS_OBSERVER_NO_CONSOLE_LAUNCHER_RUNBOOK.md
```

Related test:

```text
tests/test_h024_read_only_vps_observer_hidden_launcher.py
```

Expected hidden launcher test coverage:

```text
launcher exists
launcher delegates to scheduled wrapper
launcher uses shell.Run(command, 0, True)
launcher preserves exit code with WScript.Quit exitCode
launcher contains no trading or broker-mutation terms
runbook documents non-authorizing read-only safety boundary
```

Hidden launcher tests previously passed:

```text
3/3 passed
```

---

## 7. Scheduled Wrapper

Scheduled wrapper:

```text
scripts/run_h024_read_only_vps_observer_scheduled.ps1
```

Purpose:

```text
run one one-shot read-only observer
capture runtime logs
write last-run summary
rotate logs by retention count and age
exit with observer exit code
authorize no trading
```

Default runtime directory:

```text
reports/runtime/h024_read_only_vps_observer
```

Default logs directory:

```text
reports/runtime/h024_read_only_vps_observer/logs
```

Default last-run summary:

```text
reports/runtime/h024_read_only_vps_observer/last_run_summary.json
```

The wrapper is part of the observer proof stack. It must remain read-only.

---

## 8. Known Recent Commit Timeline

The user instructed continuation from commit `b26b6e3` or later on `main`.

Important recent commits and meanings:

```text
b26b6e3 or later
    HANDOFF_116 was committed at or after this point.

5814450 Fix H024 scheduled cadence latest segment proof
    Fixed scheduled cadence builder so it scores the latest contiguous cadence-compatible segment,
    not all historical logs polluted by old manual clustered runs and old gaps.

3b26baf Fix H024 read-only observer scheduled cadence summary
    Fixed PowerShell JSON/text output writing without UTF-8 BOM.
    Added scheduled cadence tests and runbook.

e385819 Add H024 read-only observer scheduled cadence summary
    Initial scheduled cadence summary builder.
    Known intermediate commit; fixed forward by 3b26baf and 5814450.

bc62c83 Add H024 read-only observer continuity tests and runbook
    Added continuity summary tests and runbook.

a7a377b Add H024 read-only observer continuity summary
    Added continuity summary builder.

beafd0f Fix H024 read-only observer timestamp aliases
    Accepted healthcheck checked_at_utc as a valid timestamp alias.
    Fixed recovery drill and evidence bundle timestamp failures.

5a1c4cf Add H024 read-only VPS observer evidence bundle
    Added observer evidence bundle.

4b99dc7 Add H024 read-only VPS task state recovery audit
    Added task-state audit, recovery drill preview, and operator alert surface.
```

Do not rewrite pushed history.

Fix forward.

---

## 9. Completed Current Milestone

The completed milestone was:

```text
Let the no-console scheduled task run naturally for enough 5-minute cadence opportunities.
Then refresh:
- healthcheck
- task-state
- recovery drill preview
- evidence bundle
- continuity summary
- scheduled cadence summary

Verify PASS from real natural no-console scheduler runs.
Do not commit reports/.
```

The user already had more than four 5-minute cadence opportunities, so no additional 20-minute wait was required.

The verification consumed existing natural scheduler evidence.

No manual observer run was needed for the final cadence proof.

---

## 10. Exact Verification Output From Current Milestone

Observed scheduled task action:

```text
=== Verify scheduled task no-console action ===

Arguments             : C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs
Execute               : wscript.exe
WorkingDirectory      :
```

Observed packet refresh:

```text
=== Refresh observer operational packets using existing natural scheduled runs ===

H024 read-only VPS observer healthcheck verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Health packet: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_healthcheck.json

H024 read-only VPS observer task-state verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Task-state packet: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_task_state.json
Operator alert JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_operator_alert.json
Operator alert text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_operator_alert.txt

H024 read-only VPS recovery drill preview verdict: PASS
Operator state: READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Recovery drill packet: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_recovery_drill_preview.json
Operator alert JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_recovery_drill_operator_alert.json
Operator alert text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_recovery_drill_operator_alert.txt

H024 read-only VPS observer evidence bundle verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Evidence bundle JSON: reports/h024_read_only_vps_observer_evidence_bundle.json
Evidence bundle text: reports/h024_read_only_vps_observer_evidence_bundle.txt

H024 read-only VPS observer continuity summary verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Continuity JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_continuity_summary.json
Continuity text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_continuity_summary.txt

H024 read-only VPS observer scheduled cadence summary verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
Scheduled cadence JSON: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_scheduled_cadence_summary.json
Scheduled cadence text: C:\Users\equin\Documents\institutional-ea\reports\h024_read_only_vps_observer_scheduled_cadence_summary.txt
```

Observed PASS/FAIL summary:

```text
packet                    verdict violations operator_state
------                    ------- ---------- --------------
healthcheck               PASS             0 READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
task_state                PASS             0 READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
recovery_drill_preview    PASS             0 READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED
evidence_bundle           PASS             0 READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED
continuity_summary        PASS             0 READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
scheduled_cadence_summary PASS             0 READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
```

Observed final git state:

```text
=== Final git state; reports/ must remain untracked ===

?? reports/

On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  reports/

nothing added to commit but untracked files present
```

Current milestone verdict:

```text
PASS
```

No trading authorized.

---

## 11. Commands Used For Final Verification

The final verification used this shape:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1

$ErrorActionPreference = "Stop"
$Repo = "C:\Users\equin\Documents\institutional-ea"
$TaskName = "H024 Read Only VPS Observer"
$ExpectedLauncher = "$Repo\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs"

$Task = Get-ScheduledTask -TaskName $TaskName
$Action = $Task.Actions[0]
$Action | Format-List *

if ($Action.Execute -ne "wscript.exe") {
    throw "Scheduled task Execute is not wscript.exe. Actual: $($Action.Execute)"
}
if ($Action.Arguments -ne $ExpectedLauncher) {
    throw "Scheduled task Arguments mismatch. Actual: $($Action.Arguments)"
}

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 30
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1 `
  -Root $Repo `
  -ExpectedIntervalMinutes 5 `
  -MinRunCount 4 `
  -MinCadenceWindowMinutes 15 `
  -MaxLatestRunAgeMinutes 30 `
  -MaxPacketAgeMinutes 60 `
  -MaxAllowedGapMinutes 10 `
  -MinInterRunGapMinutes 3
```

Packet checker shape:

```powershell
$Packets = @(
  @{ Name = "healthcheck"; Path = "reports\h024_read_only_vps_observer_healthcheck.json" },
  @{ Name = "task_state"; Path = "reports\h024_read_only_vps_observer_task_state.json" },
  @{ Name = "recovery_drill_preview"; Path = "reports\h024_read_only_vps_recovery_drill_preview.json" },
  @{ Name = "evidence_bundle"; Path = "reports\h024_read_only_vps_observer_evidence_bundle.json" },
  @{ Name = "continuity_summary"; Path = "reports\h024_read_only_vps_observer_continuity_summary.json" },
  @{ Name = "scheduled_cadence_summary"; Path = "reports\h024_read_only_vps_observer_scheduled_cadence_summary.json" }
)

foreach ($Packet in $Packets) {
    $Json = Get-Content -Raw -Path $Packet.Path | ConvertFrom-Json
    [pscustomobject]@{
        packet = $Packet.Name
        verdict = $Json.verdict
        violations = @($Json.violations).Count
        operator_state = $Json.operator_state
    }
}
```

---

## 12. Evidence Interpretation

The PASS state proves:

1. The local Windows scheduled task exists.
2. The scheduled task uses `wscript.exe`.
3. The scheduled task argument is the hidden VBS launcher.
4. The task interval remains 5 minutes.
5. Natural scheduled observer cadence evidence is sufficient for the configured proof.
6. The healthcheck packet is fresh and PASS.
7. The task-state packet is fresh and PASS.
8. The recovery drill preview is fresh and PASS.
9. The observer evidence bundle is fresh and PASS.
10. The continuity summary is fresh and PASS.
11. The scheduled cadence summary is fresh and PASS.
12. The final git state is clean except generated `reports/`.

The PASS state does not prove or authorize:

```text
live trading
broker mutation
order_check
order_send
broker request construction
automatic entries
automatic close/modify
SL/TP modification
symbol_select
order-capable loops
```

---

## 13. Runtime Safety State Preserved

Recent upstream read-only runtime evidence preserved the safety posture.

Observed repeated runtime flags:

```text
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
```

Observed no-mutation gate state:

```text
Verdict: PASS
Violations: 0
Operator state: NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED
Operator next action: KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION
Gate opens mutation path: False
Future broker-facing code must check gate: True
automatic_execution_blocked: True
broker_mutation_blocked: True
close_modify_blocked: True
entry_blocked: True
order_check_blocked: True
order_send_blocked: True
trading_loop_blocked: True
usdjpy_order_blocked: True
xauusd_order_blocked: True
```

Observed black-swan guard state:

```text
Verdict: PASS
Violations: 0
Operator state: BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED
Operator next action: CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED
black_swan_guard_clear: True
black_swan_guard_triggered: False
black_swan_guard_authorizes_trading: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
```

Observed deployment readiness state:

```text
Verdict: PASS
Violations: 0
Operator state: READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED
read_only_observer_workflow_authorized_for_operator_review: True
vps_deployment_readiness_authorizes_trading: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
symbol_select_authorized: False
```

---

## 14. Known Canary State

There is exactly one known H024 demo canary.

Identity:

```text
Server: Exness-MT5Trial6
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
Older open price: 4728.4490000000005
Older stop loss: 4817.394
```

Recent observed state:

```text
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
H024 position symbol: XAUUSDm
ticket: 4413054432
identifier: 4413054432
magic: 240024
volume: 0.01
type: 1
verdict: PASS
```

Recent account/risk examples observed in evidence:

```text
Account server: Exness-MT5Trial6
Account currency: USD
Balance: 10000.0
Equity: approximately 10051-10053 during recent runs
Profit: approximately 51-53 during recent runs
Margin: 2.36
Free margin: approximately 10049-10051 during recent runs
Margin level: approximately 425k
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
```

The user has said the MT5 trade is still open.

This is expected.

The project code must not close it.

If the user wants to close it, the safe path is manual close in MT5 outside this project code.

---

## 15. Existing Runtime Stack Summary

### 15.1 Runtime Safety Lockout Reader

Purpose:

```text
read committed default safety config
read local lockout state
support global no-new-entry
support manual override lockout
support per-symbol XAUUSD/USDJPY no-new-entry lockouts
authorize no trading
```

Recent passing state:

```text
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
```

### 15.2 Runtime Safety Heartbeat

Purpose:

```text
read-only MT5 runtime heartbeat
verify MT5 initialization
verify account availability
verify expected server
verify USD account currency
verify terminal connected state
authorize no trading
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED
MT5 initialized: True
Account server: Exness-MT5Trial6
Account currency: USD
Terminal connected: True
```

### 15.3 Tick/Spread Supervisor

Purpose:

```text
read-only tick/spread supervisor for XAUUSDm and USDJPYm
must not call symbol_select
authorize no trading
```

Recent example states:

```text
USDJPYm: PASS, spread around 10 points
XAUUSDm: PASS, spread around 308 points
Symbol select authorized: False
```

### 15.4 Exposure/Inventory Supervisor

Purpose:

```text
read-only position/order inventory supervisor
allow no H024 inventory or exact known XAUUSDm canary only
reject H024 USDJPY position/order
reject extra H024 position
reject pending/open H024 orders
reject mismatched XAUUSDm identity
authorize no trading
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
```

### 15.5 Account Risk/Margin Supervisor

Purpose:

```text
read-only account risk/margin supervisor
verify server
verify USD account context
verify balance/equity/margin/free margin/margin level sanity
verify canary boundedness
authorize no trading
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED
Account server: Exness-MT5Trial6
Account currency: USD
Canary state: OBSERVED_EXACT_KNOWN_CANARY
H024 position count: 1
H024 order count: 0
```

### 15.6 Runtime Safety Aggregate

Purpose:

```text
aggregate heartbeat, tick/spread, exposure/inventory, and account risk/margin
prevent cherry-picking one passing packet while ignoring failures
authorize no trading
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED
```

### 15.7 Unified Read-Only Runtime Supervision

Purpose:

```text
combine canary supervision and runtime aggregate
authorize no trading
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: UNIFIED_POST_CANARY_RUNTIME_SUPERVISION_OK_BUT_TRADING_NOT_AUTHORIZED
Operator next action: READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED
Canary supervision records: 1
Canary supervision all records passed: True
Runtime aggregate verdict: PASS
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
```

### 15.8 Runtime No-Mutation Safety Gate

Purpose:

```text
prove mutation/order-capable paths remain blocked
require future broker-facing code to check gate
authorize no trading
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED
Gate opens mutation path: False
Future broker-facing code must check gate: True
```

---

## 16. Exact-Ticket Close/Modify Stack Context

All exact-ticket close/modify artifacts remain read-only and non-authorizing.

Despite their names, none of these permit closing or modifying the canary.

### 16.1 Governance

Script:

```text
scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
```

Report:

```text
reports/h024_exact_ticket_canary_close_modify_governance.jsonl
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW
Gate verdict: PASS
Gate opens mutation path: False
Exact canary state: OBSERVED_EXACT_KNOWN_CANARY
Exact canary observed: True
H024 position count: 1
H024 order count: 0
Human decision: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
```

### 16.2 Decision Artifact

Script:

```text
scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
```

Report:

```text
reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
Decision status: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Requested action: NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
Exact ticket: 4413054432
Exact identifier: 4413054432
```

### 16.3 Pre-Action Evidence Aggregate

Script:

```text
scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
```

Report:

```text
reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
User reported position open over three bars: True
```

### 16.4 Bar-Age And Exit-Condition Evidence

Script:

```text
scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars
```

Report:

```text
reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_BUT_ACTION_NOT_AUTHORIZED
Exact ticket: 4413054432
Exact identifier: 4413054432
Bar-age classification: OPERATOR_REPORTED_ONLY
Operator reported position open over three bars: True
Machine validated over three bars: False
```

### 16.5 Manual Approval Gate Preview

Script:

```text
scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py --position-open-over-three-bars
```

Report:

```text
reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
manual_approval_gate_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False
```

### 16.6 Operator Decision V2 Preview

Script:

```text
scripts/build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py --position-open-over-three-bars
```

Report:

```text
reports/h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
operator_decision_v2_preview_authorizes_action: False
live_broker_request_constructed: False
dry_run_request_shape_preview_constructed: False
```

### 16.7 Execution Readiness Dry-Run Schema Preview

Script:

```text
scripts/build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py --position-open-over-three-bars
```

Report:

```text
reports/h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl
```

Recent passing state:

```text
Verdict: PASS
Violations: 0
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED
execution_readiness_dry_run_schema_preview_constructed: True
execution_readiness_dry_run_schema_preview_authorizes_execution: False
live_broker_request_constructed: False
executable_trade_request_constructed: False
mt5_request_dictionary_constructed: False
```

---

## 17. Observer Operational Stack

### 17.1 Healthcheck

Script:

```text
scripts/check_h024_read_only_vps_observer_health.ps1
```

Report:

```text
reports/h024_read_only_vps_observer_healthcheck.json
```

Important timestamp field:

```text
checked_at_utc
```

Recent current proof state:

```text
Verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
```

### 17.2 Task-State Audit

Script:

```text
scripts/check_h024_read_only_vps_observer_task_state.ps1
```

Report:

```text
reports/h024_read_only_vps_observer_task_state.json
```

Alert outputs:

```text
reports/h024_read_only_vps_observer_operator_alert.json
reports/h024_read_only_vps_observer_operator_alert.txt
```

Recent current proof state:

```text
Verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
```

### 17.3 Recovery Drill Preview

Script:

```text
scripts/run_h024_read_only_vps_recovery_drill_preview.ps1
```

Report:

```text
reports/h024_read_only_vps_recovery_drill_preview.json
```

Alert outputs:

```text
reports/h024_read_only_vps_recovery_drill_operator_alert.json
reports/h024_read_only_vps_recovery_drill_operator_alert.txt
```

Purpose:

```text
preview recovery readiness
do not mutate scheduler
do not auto-remediate
do not mutate broker
authorize no trading
```

Recent current proof state:

```text
Verdict: PASS
Operator state: READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
```

### 17.4 Evidence Bundle

Script:

```text
scripts/build_h024_read_only_vps_observer_evidence_bundle.ps1
```

Outputs:

```text
reports/h024_read_only_vps_observer_evidence_bundle.json
reports/h024_read_only_vps_observer_evidence_bundle.txt
```

Recent current proof state:

```text
Verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
```

### 17.5 Continuity Summary

Script:

```text
scripts/build_h024_read_only_vps_observer_continuity_summary.ps1
```

Outputs:

```text
reports/h024_read_only_vps_observer_continuity_summary.json
reports/h024_read_only_vps_observer_continuity_summary.txt
```

Purpose:

```text
consume wrapper summary/logs and observer packets
prove multi-run read-only observer continuity
fail closed on missing/stale/non-PASS evidence
fail closed on unsafe true flags
authorize no trading
```

Recent current proof state:

```text
Verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
```

### 17.6 Scheduled Cadence Summary

Script:

```text
scripts/build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1
```

Outputs:

```text
reports/h024_read_only_vps_observer_scheduled_cadence_summary.json
reports/h024_read_only_vps_observer_scheduled_cadence_summary.txt
```

Purpose:

```text
prove actual Windows Task Scheduler cadence-compatible runs
detect too few logs
detect stale latest run
detect clustered manual runs
detect gaps too large
consume upstream health/task/recovery/bundle/continuity packets
emit JSON/text under reports/
authorize no trading
```

Current key behavior:

```text
score latest contiguous cadence-compatible log segment
do not score all historical logs
```

Recent current proof state:

```text
Verdict: PASS
Operator state: READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED
Violations: 0
```

Parameters used for current proof:

```text
ExpectedIntervalMinutes: 5
MinRunCount: 4
MinCadenceWindowMinutes: 15
MaxLatestRunAgeMinutes: 30
MaxPacketAgeMinutes: 60
MaxAllowedGapMinutes: 10
MinInterRunGapMinutes: 3
```

---

## 18. Focused Test State Before HANDOFF_116

Known source/test validation before HANDOFF_116:

Hidden launcher tests:

```text
3/3 passed
```

Scheduler/cadence focused tests:

```text
33/33 passed
```

Earlier scheduled cadence validation:

```text
focused scheduled cadence tests: 7 passed
broader read-only observer tests: 27 passed
```

The current HANDOFF_117 milestone did not add source code. It consumed operational evidence and writes this handoff.

---

## 19. Known Pitfalls And Correct Responses

### 19.1 PowerShell popups

Symptom:

```text
visible PowerShell window appears every 5 minutes
```

Incorrect assumption:

```text
-WindowStyle Hidden fully solves it
```

Correct current fix:

```text
Windows Task Scheduler -> wscript.exe -> VBS hidden launcher -> scheduled wrapper
```

### 19.2 Fragile VBS scheduled-task argument quoting

Bad:

```powershell
New-ScheduledTaskAction -Execute "wscript.exe" -Argument ""$LauncherPath""
```

Good:

```powershell
New-ScheduledTaskAction -Execute "wscript.exe" -Argument $LauncherPath
```

### 19.3 Old logs polluting cadence proof

Symptom:

```text
scheduled_log_gap_too_large
scheduled_log_clustered
```

Cause:

```text
builder scored all historical logs, including old manual runs and old gaps
```

Fix:

```text
score the latest contiguous cadence-compatible segment
```

Fixed in:

```text
5814450 Fix H024 scheduled cadence latest segment proof
```

### 19.4 PowerShell UTF-8 BOM JSON failure

Symptom:

```text
json.decoder.JSONDecodeError: Unexpected UTF-8 BOM
```

Cause:

```text
PowerShell wrote JSON with UTF-8 BOM
```

Fix:

```text
write JSON/text with UTF8Encoding($false)
```

Fixed in:

```text
3b26baf Fix H024 read-only observer scheduled cadence summary
```

### 19.5 Healthcheck upstream black-swan/deployment failure

Symptom:

```text
black_swan:UPSTREAM_NOT_PASS
black_swan:UPSTREAM_VIOLATIONS_PRESENT
last_run:LAST_RUN_NOT_COMPLETED
last_run:LAST_RUN_EXIT_NONZERO
```

Correct response:

```text
refresh exact-ticket stack
refresh black-swan guard
refresh deployment readiness
allow/run observer as appropriate
rerun healthcheck
do not bypass
do not suppress
do not authorize trading
```

### 19.6 Timestamp alias issue

Historical problem:

```text
healthcheck emitted checked_at_utc
recovery drill/evidence bundle expected generated_at_utc
```

Fix:

```text
accept checked_at_utc as valid timestamp alias while preserving freshness checks
```

Fixed in:

```text
beafd0f Fix H024 read-only observer timestamp aliases
```

---

## 20. Start Commands For The Next AI

Use these first:

```powershell
cd C:\Users\equin\Documents\institutional-ea
.\.venv\Scripts\Activate.ps1
git status
git log --oneline -12
```

Verify scheduled task action:

```powershell
$TaskName = "H024 Read Only VPS Observer"
(Get-ScheduledTask -TaskName $TaskName).Actions | Format-List *
```

Expected:

```text
Execute: wscript.exe
Arguments: C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs
```

Refresh operational proof packets after a future soak:

```powershell
$Repo = "C:\Users\equin\Documents\institutional-ea"

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 30
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_recovery_drill_preview.ps1 -MaxEvidenceAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1 -MaxPacketAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_continuity_summary.ps1 -MinRunCount 2 -MaxPacketAgeMinutes 60 -MaxLatestRunAgeMinutes 60
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1 `
  -Root $Repo `
  -ExpectedIntervalMinutes 5 `
  -MinRunCount 4 `
  -MinCadenceWindowMinutes 15 `
  -MaxLatestRunAgeMinutes 30 `
  -MaxPacketAgeMinutes 60 `
  -MaxAllowedGapMinutes 10 `
  -MinInterRunGapMinutes 3
```

Expected:

```text
healthcheck PASS
task-state PASS
recovery drill preview PASS
evidence bundle PASS
continuity summary PASS
scheduled cadence summary PASS
violations 0
```

If any packet fails closed, inspect violations.

Do not bypass failures.

---

## 21. Commit Discipline

Rules:

```text
Never add reports/.
Never commit generated runtime evidence.
Do not claim success without final git status.
Fix forward rather than rewriting pushed history.
Keep work operational and read-only.
Avoid governance-only work unless explicitly requested.
Avoid paid infrastructure unless explicitly requested.
Keep giving the user concise suggested next prompts after each milestone.
```

Standard pattern:

```powershell
git status
git add -- <source/test/docs only>
git diff --cached --check
git diff --cached --stat
git commit -m "<specific milestone message>"
git push
git status
```

For this handoff, stage only:

```text
docs/operations/handoffs/HANDOFF_117.md
```

Do not stage:

```text
reports/
```

---

## 22. Recommended Next Read-Only Operational Milestone

Recommended next milestone:

```text
H024 local Windows no-console observer extended unattended soak proof
```

Purpose:

1. Keep the current scheduled task unchanged.
2. Keep the current 5-minute interval.
3. Let the no-console observer run naturally for a longer free local window, such as 1-2 hours or overnight if convenient.
4. Confirm the user no longer sees PowerShell popups.
5. Refresh the same six operational packets afterward.
6. Confirm all six remain PASS with zero violations.
7. Keep `reports/` untracked.
8. Do not add trading.
9. Do not add broker mutation.

The next milestone should remain operational proof quality, not governance expansion.

---

## 23. Suggested Prompt For Next AI

Use this prompt next:

```text
Please continue from HANDOFF_117 on main. HANDOFF_117 supersedes HANDOFF_116 and all older handoffs.

The current target is free local Windows recurring read-only observer proof, not Oracle VPS and not paid VPS. The scheduled observer uses Windows Task Scheduler with Execute=wscript.exe and Arguments=C:\Users\equin\Documents\institutional-ea\scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs. The interval remains 5 minutes. The VBS launcher is used to avoid visible PowerShell popups while preserving the scheduled wrapper exit code.

Current completed milestone: local Windows no-console natural scheduler proof passed. Healthcheck, task-state, recovery drill preview, evidence bundle, continuity summary, and scheduled cadence summary all returned PASS with zero violations using natural scheduler cadence evidence. reports/ remained untracked and must remain untracked.

Hard safety boundaries remain absolute: do not enable trading; do not add order_check, order_send, live broker request construction, executable trade request construction, automatic entries, automatic close/modify, SL/TP modification, symbol_select, broker mutation, or order-capable trading loops. PASS does not authorize trading.

Next read-only milestone: perform an extended free local Windows no-console unattended observer soak proof using the existing 5-minute scheduled task. Do not change the interval. After the soak, refresh healthcheck, task-state, recovery drill preview, evidence bundle, continuity summary, and scheduled cadence summary. Verify PASS with zero violations from natural scheduler evidence, keep reports/ untracked, and give me the next concise read-only operational prompt.
```

---

## 24. Final Safety Reminder

Do not trade.

Do not close or modify the canary through code.

Do not make the EA open trades.

Do not make the EA close trades.

Do not build live broker requests.

Do not build executable trade request dictionaries.

Do not run an order-capable trading loop.

Do not call `order_check`.

Do not call `order_send`.

Do not call `symbol_select`.

Do not mutate broker/account/symbol state.

The project is currently proving free local Windows read-only scheduled observer reliability only.