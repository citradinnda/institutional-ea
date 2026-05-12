from __future__ import annotations

import argparse
from pathlib import Path

import MetaTrader5 as mt5

from quantcore.execution.h024_usdjpy_broker_readiness import (
    build_h024_usdjpy_broker_readiness_record,
    write_jsonl,
)


DEFAULT_OUTPUT = "reports/h024_usdjpy_broker_readiness.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build H024 USDJPY read-only broker-readiness JSONL.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    record = build_h024_usdjpy_broker_readiness_record(mt5)
    output_path = write_jsonl(record, Path(args.output))

    print(f"Wrote {output_path}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations', []))}")
    print(f"Runtime symbol: {record.get('runtime_symbol')}")
    print(f"Model symbol: {record.get('model_symbol')}")
    print(f"Broker mutation authorized: {record.get('broker_mutation_authorized')}")
    print(f"Order check authorized: {record.get('order_check_authorized')}")
    print(f"Order send authorized: {record.get('order_send_authorized')}")
    print(f"USDJPY order authorized: {record.get('usd_jpy_order_authorized')}")
    print(f"Trading loop authorized: {record.get('trading_loop_authorized')}")

    return 0 if record.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())