# H024 Exact-Ticket Canary Close/Modify Bar-Age And Exit-Condition Evidence

## Status

Read-only evidence packet only.

This packet does not authorize broker mutation, order checks, order sends, entries,
close/modify, XAUUSD orders, USDJPY orders, trading loops, or automatic execution.

A PASS means only that bar-age / exit-condition evidence is coherent for operator
review and that all action paths remain blocked.

## Scope

The packet consumes these upstream JSONL packets:

- H024 runtime no-mutation safety gate
- H024 unified read-only post-canary runtime supervision
- H024 exact-ticket canary close/modify governance specification
- H024 exact-ticket canary close/modify decision artifact validator
- H024 exact-ticket canary close/modify pre-action evidence aggregate
- H024 runtime exposure/inventory safety supervisor
- H024 runtime account risk/margin safety supervisor
- H024 runtime tick/spread safety supervisor

## Exact Canary Identity

The packet is locked to:

- runtime symbol: XAUUSDm
- model symbol: XAUUSD
- side: sell
- MT5 position type: 1
- volume: 0.01
- magic: 240024
- ticket: 4413054432
- identifier: 4413054432
- canary state: OBSERVED_EXACT_KNOWN_CANARY

## Bar-Age Classification

The packet supports two passable classifications:

1. `MACHINE_VALIDATED`
   - Requires machine-validated over-three-bars evidence.
   - Requires a bar timeframe.
   - Requires `machine_bar_count > 3`.

2. `OPERATOR_REPORTED_ONLY`
   - Records the operator statement that the exact canary has been open over
     three bars.
   - Does not treat the statement as machine validation.
   - Does not authorize action.

Missing bar-age evidence fails closed.

## Exit-Condition Evidence

The decision artifact must remain non-authorizing:

- decision status: `NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY`
- requested action: `NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY`

Any action-implying decision fails closed.

## Failure Modes

The packet fails closed on:

- missing upstream JSONL
- malformed upstream JSONL
- upstream verdict not PASS
- stale upstream evidence
- future-skewed upstream evidence
- upstream embedded violations
- any upstream authorization set true
- `effective_new_entries_blocked` not true
- exact ticket mismatch
- exact identifier mismatch
- exact canary not observed
- extra H024 exposure/order
- missing bar-age evidence
- machine validation claimed without sufficient evidence
- action-implying decision artifact
- malformed output packet
- verifier `--require-pass` against a fail-closed record

## Commands

Build:

```powershell
python scripts\build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py --position-open-over-three-bars

Verify:

python scripts\verify_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py reports\h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl --require-pass
Interpretation

PASS means:

exact-ticket bar-age / exit-condition evidence is coherent for read-only review
the exact XAUUSDm canary identity is preserved
the exact canary is observed
no extra H024 exposure/order is observed
risk/spread/exposure snapshots are included
all action paths remain blocked

PASS does not mean:

close authorized
modify authorized
broker request construction authorized
order check authorized
order send authorized
trading authorized
