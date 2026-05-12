# H024 Runtime Safety Configuration + Lockout Reader

## Purpose

This layer is the first runtime-local H024 safety enforcement component.

It reads a committed safety config and local JSON lockout-state files for:

1. Global no-new-entry lockout.
2. Manual override lockout.
3. XAUUSD per-symbol no-new-entry lockout.
4. USDJPY per-symbol no-new-entry lockout.

It is read-only and local-files-only. It imports no MetaTrader5 package, calls no broker API, places no orders, performs no close/modify action, and authorizes no trading loop.

## Committed Config

Default config:

```text
config/h024_runtime_safety/default_lockout_config.json

Default lockout states:

config/h024_runtime_safety/lockouts/global_no_new_entry.json
config/h024_runtime_safety/lockouts/manual_override_lockout.json
config/h024_runtime_safety/lockouts/xauusd_no_new_entry.json
config/h024_runtime_safety/lockouts/usdjpy_no_new_entry.json

The committed defaults are inactive lockout states. They do not authorize trading. They only provide a valid local input set for the reader.

Fail-Closed Rules

The reader fails closed if:

the config file is missing;
the config file is malformed;
the config root is not a JSON object;
any required lockout path is missing;
any required lockout file is missing;
any required lockout file is malformed;
any lockout file has the wrong strategy;
any lockout file has the wrong symbol mapping;
any lockout file has a non-boolean active value;
any config authorization flag is true.

When fail-closed, the packet keeps:

effective_new_entries_blocked: true
entry_authorized: false
order_check_authorized: false
order_send_authorized: false
broker_mutation_authorized: false
trading_loop_authorized: false
Active Lockout Semantics

An active lockout is not a malformed state. It is a valid blocking state.

If a lockout file is valid and has active: true, the packet can still have verdict: PASS, but the operator state becomes:

LOCKED_BY_ACTIVE_LOCKOUT

No entries are authorized.

Non-Authorization Boundary

The packet must always keep these false:

broker_mutation_authorized
order_check_authorized
order_send_authorized
entry_authorized
close_modify_authorized
xauusd_order_authorized
usdjpy_order_authorized
trading_loop_authorized
automatic_execution_authorized
Commands

Build the local JSONL packet:

python scripts\build_h024_runtime_safety_lockout_jsonl.py

Verify the local JSONL packet:

python scripts\verify_h024_runtime_safety_lockout_jsonl.py reports\h024_runtime_safety_lockout.jsonl --require-pass

Run focused tests:

python -m pytest -q tests\test_h024_runtime_safety_lockout.py
Runtime Artifact

Generated JSONL is local only:

reports\h024_runtime_safety_lockout.jsonl

Do not commit reports/.