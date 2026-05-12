# H024 Exact-Ticket Canary Close/Modify Decision Artifact Validator

This packet validates the explicit human/operator decision artifact schema referenced by the H024 exact-ticket canary close/modify governance packet.

It is read-only only.

A passing packet means:

- the decision artifact is syntactically coherent;
- the decision artifact is fresh;
- the exact ticket/identifier and XAUUSDm canary identity match the known canary;
- the operator intent fields are explicit and non-ambiguous;
- the operator attestation fields preserve the no-mutation posture;
- all action paths remain blocked.

A passing packet does not authorize:

- broker mutation;
- order-check activity;
- order-send activity;
- entry;
- close/modify;
- XAUUSD order activity;
- USDJPY order activity;
- trading loop execution;
- automatic execution.

## Known exact canary

```text
server: Exness-MT5Trial6
account_currency: USD
runtime_symbol: XAUUSDm
model_symbol: XAUUSD
side: sell
mt5_position_type: 1
volume: 0.01
magic: 240024
ticket: 4413054432
identifier: 4413054432
entry_deal: 3788869526
```

## Files

```text
config/h024_runtime_safety/default_exact_ticket_canary_close_modify_decision_artifact.json
quantcore/execution/h024_exact_ticket_canary_close_modify_decision_artifact.py
scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
scripts/verify_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
tests/test_h024_exact_ticket_canary_close_modify_decision_artifact.py
docs/operations/H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT.md
```

## Report path

```text
reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl
```

`reports/` remains untracked.

## Operator states

Passing state:

```text
EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED
```

Passing next action:

```text
KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_DECISION_ARTIFACT_REVIEW
```

Fail-closed state:

```text
FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_BLOCKED
```

Fail-closed next action:

```text
FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED
```

## Required artifact schema

The validator requires:

- `schema_version = 1`
- `strategy = H024`
- `artifact_type = h024_exact_ticket_canary_close_modify_decision_artifact`
- non-empty `decision_id`
- fresh `decision_timestamp_utc`
- non-expired `expires_at_utc`
- exact canary identity
- explicit non-ambiguous `operator_intent`
- `intent_scope = READ_ONLY_GOVERNANCE_REVIEW_ONLY`
- `immediate_action_requested = false`
- complete operator attestation preserving no-mutation posture
- `effective_new_entries_blocked = true`
- every authorization field set to false

Allowed requested actions are review-only labels:

```text
NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY
REQUEST_EXACT_TICKET_CLOSE_REVIEW_ONLY
REQUEST_EXACT_TICKET_MODIFY_REVIEW_ONLY
REQUEST_EXACT_TICKET_CLOSE_MODIFY_REVIEW_ONLY
```

These labels only describe read-only governance review intent. They do not authorize a live action.

## Failure modes

The packet fails closed on:

- missing artifact;
- malformed artifact;
- wrong schema version;
- wrong strategy;
- wrong artifact type;
- stale or future decision timestamp;
- expired decision;
- missing or stale attestation timestamp;
- ticket/identifier mismatch;
- runtime symbol mismatch;
- model symbol mismatch;
- side/type mismatch;
- volume mismatch;
- magic mismatch;
- missing operator intent;
- ambiguous operator intent;
- immediate action request;
- unsupported requested action;
- missing operator attestation;
- contradictory attestation;
- missing authorization field;
- any true authorization field;
- `effective_new_entries_blocked` not true;
- any broker/execution request payload key.

## Validation commands

```powershell
python -m pytest tests\test_h024_exact_ticket_canary_close_modify_decision_artifact.py
python -m pytest
python scripts\build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py
python scripts\verify_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py reports\h024_exact_ticket_canary_close_modify_decision_artifact.jsonl --require-pass
```

Expected verifier outcome:

```text
Verifier verdict: PASS
Record verdict: PASS
Violations: 0
Effective new entries blocked: True
all authorizations: False
```

## Safety interpretation

```text
PASS = decision artifact schema/coherence is valid
PASS != close authorized
PASS != modify authorized
PASS != broker mutation authorized
PASS != trading authorized
```
