# H024 Exact-Ticket Canary Close/Modify Pre-Action Evidence Aggregate

This packet is a read-only evidence aggregate for the known H024 XAUUSDm canary. It does not authorize trading, close, modify, order checks, order sends, broker request construction, or a trading loop.

## Required upstream packets

The aggregate consumes the latest records from:

- `reports/h024_runtime_no_mutation_safety_gate.jsonl`
- `reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl`
- `reports/h024_exact_ticket_canary_close_modify_governance.jsonl`
- `reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl`

Each upstream packet must be present, parseable, fresh, `PASS`, free of embedded violations, non-authorizing, and mutually consistent with the exact known canary.

## Exact canary lock

The aggregate preserves:

- ticket: `4413054432`
- identifier: `4413054432`
- runtime symbol: `XAUUSDm`
- model symbol: `XAUUSD`
- side: `sell`
- MT5 position type: `1`
- volume: `0.01`
- magic: `240024`
- required canary state: `OBSERVED_EXACT_KNOWN_CANARY`

The decision artifact must explicitly carry the exact ticket, identifier, and canary identity. Any mismatch fails closed.

## Operator context

The builder can record that the operator reported the position has been open for over three bars. That field is context only. Bar age does not authorize action and does not authorize broker request construction.

## Passing meaning

`PASS` means the read-only pre-action evidence bundle is coherent for operator review and all action paths remain blocked.

`PASS` does not mean close is authorized, modify is authorized, order_check is authorized, order_send is authorized, broker mutation is authorized, XAUUSD order is authorized, USDJPY order is authorized, automatic execution is authorized, or a trading loop is authorized.

## Fail-closed behavior

The aggregate fails closed on missing, malformed, stale, ambiguous, inconsistent, unsafe, or non-PASS upstream evidence; embedded upstream violations; exact ticket/identifier mismatch; exact canary identity mismatch; the exact canary not being observed where required; unsafe operator decision intent; any action authorization being true; or `effective_new_entries_blocked` not being true.

## Commands

```powershell
python scripts\build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py --position-open-over-three-bars
python scripts\verify_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py reports\h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl --require-pass
```

## Identity extraction scope

The aggregate validates exact canary identity only from relevant canary, H024 position, governance, decision, and expected identity contexts. It must not treat unrelated runtime market-data symbols, such as USDJPYm tick/spread evidence, as canary identity mismatches. USDJPY H024 exposure/order evidence remains unsafe and must fail closed through the upstream exposure/inventory and aggregate checks.

## Fix-forward validation note

The aggregate validates exact canary identity only from exact-canary, H024 position, governance, decision-artifact, and exact-ticket contexts. Runtime tick/spread expected symbol coverage can legitimately include USDJPYm and must not be interpreted as a XAUUSDm canary identity mismatch. Decision-artifact check-field wrappers using expected/observed/passed are interpreted through their observed value. This preserves fail-closed identity validation while avoiding false mismatches from unrelated read-only market-data evidence.
