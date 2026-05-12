from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from quantcore.execution.h024_runtime_safety_heartbeat import (  # noqa: E402
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    collect_h024_runtime_safety_heartbeat,
    write_jsonl,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the H024 runtime safety heartbeat JSONL packet.")
    parser.add_argument(
        "--output",
        default="reports/h024_runtime_safety_heartbeat.jsonl",
        help="Output JSONL path. Default: reports/h024_runtime_safety_heartbeat.jsonl",
    )
    parser.add_argument("--expected-server", default=EXPECTED_SERVER)
    parser.add_argument("--expected-currency", default=EXPECTED_ACCOUNT_CURRENCY)
    return parser


def main() -> int:
    args = _parser().parse_args()
    record = collect_h024_runtime_safety_heartbeat(
        expected_server=args.expected_server,
        expected_currency=args.expected_currency,
    )
    output_path = Path(args.output)
    write_jsonl(output_path, [record])

    observed = record.get("observed", {})
    account = observed.get("account") or {}
    terminal = observed.get("terminal") or {}

    print(f"Wrote {output_path}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations', []))}")
    print(f"Operator state: {record.get('operator_state')}")
    print(f"MT5 initialized: {observed.get('mt5_initialize_result')}")
    print(f"Account server: {account.get('server') if isinstance(account, dict) else None}")
    print(f"Account currency: {account.get('currency') if isinstance(account, dict) else None}")
    print(f"Terminal connected: {terminal.get('connected') if isinstance(terminal, dict) else None}")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())