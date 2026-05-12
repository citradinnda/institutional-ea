# H024 Exact-Ticket Canary Close/Modify Execution Readiness Dry-Run Schema Preview

This packet is read-only and non-authorizing.

It previews an abstract execution-readiness dry-run schema for a possible future exact-ticket close/modify path for the known H024 XAUUSDm canary. It does not build a live broker request. It does not build an executable trade request dictionary. It does not call broker functions. It does not authorize close, modify, order_check, order_send, entry, XAUUSD order, USDJPY order, automatic execution, or a trading loop.

## Hard boundary

PASS means the dry-run schema preview is coherent for read-only operator review only.

PASS does not mean execution is authorized.

The packet must keep these fields blocked:

- effective_new_entries_blocked: true
- broker_mutation_authorized: false
- order_check_authorized: false
- order_send_authorized: false
- entry_authorized: false
- close_modify_authorized: false
- xauusd_order_authorized: false
- usdjpy_order_authorized: false
- trading_loop_authorized: false
- automatic_execution_authorized: false
- execution_readiness_dry_run_schema_preview_authorizes_execution: false
- dry_run_request_shape_preview_authorizes_execution: false
- live_broker_request_constructed: false
- executable_trade_request_constructed: false
- mt5_request_dictionary_constructed: false
- order_check_planned: false
- order_send_planned: false
- symbol_select_planned: false

## Exact canary lock

The only allowed canary identity is:

- ticket: 4413054432
- identifier: 4413054432
- runtime symbol: XAUUSDm
- model symbol: XAUUSD
- magic: 240024
- volume: 0.01
- position type: 1

## Consumed upstream evidence

The packet consumes the latest available JSONL report for:

- runtime no-mutation safety gate
- unified read-only runtime supervision
- exact-ticket close/modify governance
- exact-ticket decision artifact validator
- pre-action evidence aggregate
- bar-age and exit-condition evidence
- manual approval gate preview
- operator decision v2 preview
- runtime exposure/inventory
- runtime account risk/margin
- runtime tick/spread

All upstream packets must be present, fresh, PASS, and free of embedded violations. Any unsafe authorization field set to true fails closed.

## Abstract dry-run schema preview

The packet constructs only an abstract, non-executable dry-run schema preview. It may contain references to:

- target ticket and identifier
- runtime/model symbol identity
- magic, volume, and position type
- operator decision v2 preview
- manual approval gate preview
- pre-action evidence aggregate
- bar-age and exit-condition evidence
- account/risk/margin snapshot
- tick/spread snapshot
- exposure/inventory snapshot

It must not contain:

- live broker request
- executable trade request
- MT5 request dictionary
- order_check request
- order_send request
- symbol_select request
- close/modify request
- new entry request
- trading loop instruction

## Fail-closed cases

The packet fails closed on:

- missing upstream report
- malformed upstream JSONL
- stale upstream evidence
- upstream verdict not PASS
- upstream embedded violations
- unsafe authorization true
- exact ticket mismatch
- exact identifier mismatch
- runtime symbol mismatch
- model symbol mismatch
- magic mismatch
- volume mismatch
- position type mismatch
- ambiguous operator decision v2 preview fields
- executable broker/trade request object
- live broker request construction
- MT5 request dictionary construction
- order_check planned or authorized
- order_send planned or authorized
- symbol_select planned
- close/modify authorized
- trading loop authorized

## Passing operator state

`EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED`

## Passing operator next action

`KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW`

## Fail-closed operator state

`FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_BLOCKED`

## Fail-closed operator next action

`FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED`

## Report

`reports/h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl`

Keep `reports/` untracked.
