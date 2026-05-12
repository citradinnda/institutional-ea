# H024 Read-Only Black-Swan Guard Packet

This packet is read-only and non-authorizing.

It consumes the H024 runtime safety layer and exact-ticket close/modify preview stack to detect extreme-risk or unsafe runtime conditions. It never creates a live broker request, executable trade request, MT5 request dictionary, close/modify request, entry request, or trading loop instruction.

## Hard boundary

PASS means the black-swan guard found no active extreme-risk condition in the consumed read-only evidence.

PASS does not authorize trading.

PASS does not authorize close/modify.

PASS does not authorize broker mutation.

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
- black_swan_guard_authorizes_trading: false
- black_swan_guard_authorizes_broker_mutation: false
- black_swan_guard_authorizes_close_modify: false
- live_broker_request_constructed: false
- executable_trade_request_constructed: false
- mt5_request_dictionary_constructed: false
- order_check_planned: false
- order_send_planned: false
- symbol_select_planned: false

## Consumed upstream evidence

The packet consumes the latest available JSONL report for:

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

All upstream packets must be present, fresh, PASS, and free of embedded violations. Any unsafe authorization field set to true fails closed.

## Black-swan condition examples

The packet fails closed if it observes or infers:

- missing heartbeat
- stale heartbeat
- stale upstream packet
- malformed upstream packet
- upstream fail-closed verdict
- upstream embedded violation
- active global/manual/symbol lockout
- bid/ask inversion
- extreme spread
- non-positive balance
- non-positive equity
- negative free margin
- low margin level
- extreme equity drawdown ratio
- exact XAUUSDm canary not observed
- unexpected H024 order
- unexpected H024 USDJPY exposure
- extra H024 exposure
- missing exact-ticket identity lock
- unsafe authorization true
- live broker request object
- executable trade request object
- MT5 request dictionary object

## Exact canary lock

The packet preserves the current exact canary identity:

- ticket: 4413054432
- identifier: 4413054432
- runtime symbol: XAUUSDm
- model symbol: XAUUSD
- magic: 240024
- volume: 0.01
- position type: 1

## Passing operator state

`BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED`

## Passing operator next action

`CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED`

## Fail-closed operator state

`FAIL_CLOSED_BLACK_SWAN_GUARD_ACTIVE_OR_UNVERIFIED_NO_TRADING_AUTHORIZED`

## Fail-closed operator next action

`FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED`

## Report

`reports/h024_read_only_black_swan_guard.jsonl`

Keep `reports/` untracked.
