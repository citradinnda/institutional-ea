from __future__ import annotations

import argparse
from pathlib import Path

from quantcore.execution.h024_safety_supervisor_spec import (
    build_h024_safety_supervisor_spec_record,
    write_jsonl,
)


DEFAULT_OUTPUT = "reports/h024_safety_supervisor_spec.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build H024 read-only safety supervisor specification JSONL.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    record = build_h024_safety_supervisor_spec_record()
    output_path = write_jsonl(record, Path(args.output))

    print(f"Wrote {output_path}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations', []))}")
    print(f"Implementation status: {record.get('implementation_status')}")
    print(f"Global guards: {len(record.get('global_guards', {}))}")
    print(f"Symbol circuit breaker groups: {len(record.get('symbol_circuit_breakers', {}))}")
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