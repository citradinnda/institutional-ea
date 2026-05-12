# H024 Exact-Ticket Canary Close/Modify Governance Specification

This packet is a read-only governance specification for the exact known H024
standard-demo XAUUSDm canary. It defines prerequisites that must exist before
any future close/modify could even be considered.

It does **not** close the canary. It does **not** modify the canary. It does
**not** build a live broker request. It does **not** call `order_check`,
`order_send`, `symbol_select`, or any close/modify helper. It does **not** run a
trading loop.

## Scope

Known canary identity:

```text
ticket/identifier: 4413054432
runtime symbol: XAUUSDm
model symbol: XAUUSD
side: sell
MT5 type: 1
volume: 0.01
magic: 240024
```

A packet `PASS` means only:

```text
the read-only governance specification is coherent
the exact-ticket lock is observed
the runtime no-mutation gate is PASS and still closed
the pre-close risk snapshot bundle is present/fresh
the explicit decision artifact is specification-only and non-authorizing
all close/modify and broker mutation paths remain blocked
```

A packet `PASS` never means:

```text
close is authorized
modify is authorized
order_check is authorized
order_send is authorized
entry is authorized
XAUUSD order is authorized
USDJPY order is authorized
a trading loop is authorized
automatic execution is authorized
```

## Required Inputs

Default build command:

```powershell
python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
```

Default input paths:

```text
reports/h024_runtime_no_mutation_safety_gate.jsonl
reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl
reports/h024_runtime_account_risk_margin_safety_supervisor.jsonl
reports/h024_runtime_exposure_inventory_safety_supervisor.jsonl
reports/h024_runtime_tick_spread_safety_supervisor.jsonl
config/h024_runtime_safety/default_exact_ticket_canary_close_modify_governance_decision.json
```

Default output path:

```text
reports/h024_exact_ticket_canary_close_modify_governance.jsonl
```

The upstream report paths are read-only evidence inputs. The governance builder also accepts equivalent embedded upstream records from the no-mutation gate packet and fails closed when required evidence is missing or malformed.

`reports/` is generated runtime output and must remain untracked.

## Governance Requirements

The packet requires:

1. Exact ticket/identifier lock:
   - ticket or identifier `4413054432`.

2. Exact known canary identity:
   - `XAUUSDm`
   - model symbol `XAUUSD`
   - side `sell`
   - MT5 type `1`
   - volume `0.01`
   - magic `240024`.

3. Runtime no-mutation safety gate:
   - gate packet is present.
   - gate is `PASS`.
   - gate is not explicitly untrusted.
   - gate is fresh.
   - `gate_opens_mutation_path` is `false`.
   - all authorization flags are `false`.
   - `effective_new_entries_blocked` is `true`.

4. Unified post-canary runtime supervision:
   - present or summarized by the gate packet.
   - verdict is `PASS`.

5. No USDJPY H024 exposure/order:
   - no positive USDJPY H024 position/order count.

6. No additional H024 exposure/order:
   - exactly one H024 position when the exact known canary is observed.
   - zero H024 orders.

7. Explicit human decision artifact:
   - separate JSON artifact exists.
   - schema, strategy, and artifact type match.
   - decision is explicit.
   - decision is specification-only and requests no action.
   - artifact targets the exact known canary.
   - artifact is not stale.
   - all authorization flags are false.

8. Pre-close risk snapshot bundle:
   - account risk/margin snapshot.
   - exposure/inventory snapshot.
   - tick/spread snapshot.
   - snapshot data is present and fresh.

## Failure Modes

The packet fails closed on:

```text
missing or malformed runtime no-mutation gate
gate not PASS
gate opens any mutation path
gate explicitly untrusted
missing or non-PASS unified supervision
missing exact canary state
ticket/identifier ambiguity
canary identity mismatch
USDJPY H024 exposure/order
additional H024 exposure/order
any H024 order
missing/malformed/stale/ambiguous human decision artifact
missing/malformed/stale pre-close risk snapshot
any authorization true
effective_new_entries_blocked not true
```

## Verification

Run:

```powershell
python scripts\verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py reports\h024_exact_ticket_canary_close_modify_governance.jsonl --require-pass
```

Expected passing state is still non-authorizing:

```text
Verifier verdict: PASS
Record verdict: PASS
Operator state: EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED
Operator next action: KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW
```

## Commit Discipline

Use:

```powershell
python -m pytest tests\test_h024_exact_ticket_canary_close_modify_governance.py
python -m pytest

python scripts\build_h024_runtime_no_mutation_safety_gate_jsonl.py
python scripts\verify_h024_runtime_no_mutation_safety_gate_jsonl.py reports\h024_runtime_no_mutation_safety_gate.jsonl --require-pass

python scripts\build_h024_exact_ticket_canary_close_modify_governance_jsonl.py
python scripts\verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py reports\h024_exact_ticket_canary_close_modify_governance.jsonl --require-pass

git status
git add -- `
  config/h024_runtime_safety/default_exact_ticket_canary_close_modify_governance_decision.json `
  quantcore/execution/h024_exact_ticket_canary_close_modify_governance.py `
  scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py `
  scripts/verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py `
  tests/test_h024_exact_ticket_canary_close_modify_governance.py `
  docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE.md
git diff --cached --check
git commit -m "Add H024 exact-ticket canary close modify governance spec"
git push
git status
```

Do not add `reports/`.


## Builder Runtime Evidence Behavior

The builder runs the existing read-only upstream runtime evidence builders by default before loading the governance inputs. This refreshes lockout, heartbeat, tick/spread, exposure/inventory, account risk/margin, aggregate, and unified supervision reports. These upstream builders are read-only evidence producers; they do not authorize broker mutation. Use `--skip-autobuild-upstream` only for tests or offline verification, in which case missing upstream evidence fails closed.


## Runtime Canary State Compatibility

The governance packet accepts the exact observed canary state from compatible upstream runtime reports that expose either `exact_canary_state` or the exposure/account supervisor `canary_state` alias. The alias is accepted only for `OBSERVED_EXACT_KNOWN_CANARY`; missing, mismatched, ambiguous, or stale evidence still fails closed and never authorizes close/modify.
