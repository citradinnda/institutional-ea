from __future__ import annotations

import argparse
from pathlib import Path

from quantcore.execution.h024_runtime_safety_lockout import (
    DEFAULT_CONFIG_PATH,
    build_h024_runtime_safety_lockout_record,
    write_jsonl,
)


DEFAULT_OUTPUT = "reports/h024_runtime_safety_lockout.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build H024 read-only runtime safety lockout JSONL.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    record = build_h024_runtime_safety_lockout_record(config_path=Path(args.config))
    output_path = write_jsonl(record, Path(args.output))

    print(f"Wrote {output_path}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations', []))}")
    print(f"Operator state: {record.get('operator_state')}")
    print(f"Lockout inputs valid: {record.get('lockout_inputs_valid')}")
    print(f"Lockout triggered: {record.get('lockout_triggered')}")
    print(f"Active lockouts: {len(record.get('active_lockouts', []))}")
    print(f"Fail-closed lockouts: {len(record.get('fail_closed_lockouts', []))}")
    print(f"Effective new entries blocked: {record.get('effective_new_entries_blocked')}")
    print(f"Broker mutation authorized: {record.get('broker_mutation_authorized')}")
    print(f"Order check authorized: {record.get('order_check_authorized')}")
    print(f"Order send authorized: {record.get('order_send_authorized')}")
    print(f"Entry authorized: {record.get('entry_authorized')}")
    print(f"Close/modify authorized: {record.get('close_modify_authorized')}")
    print(f"XAUUSD order authorized: {record.get('xauusd_order_authorized')}")
    print(f"USDJPY order authorized: {record.get('usdjpy_order_authorized')}")
    print(f"Trading loop authorized: {record.get('trading_loop_authorized')}")
    print(f"Automatic execution authorized: {record.get('automatic_execution_authorized')}")

    return 0 if record.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())