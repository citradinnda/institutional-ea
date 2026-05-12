from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor import (  # noqa: E402
    DEFAULT_OUTPUT_PATH,
    collect_h024_runtime_exposure_inventory_safety_supervisor,
    write_jsonl,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the H024 runtime exposure/inventory safety supervisor JSONL packet.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Output JSONL path. Default: {DEFAULT_OUTPUT_PATH}",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    record = collect_h024_runtime_exposure_inventory_safety_supervisor()
    output_path = Path(args.output)
    write_jsonl(output_path, [record])

    observed = record.get("observed", {})

    print(f"Wrote {output_path}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations', []))}")
    print(f"Operator state: {record.get('operator_state')}")
    print(f"Canary state: {observed.get('canary_state') if isinstance(observed, dict) else None}")
    print(f"H024 position count: {observed.get('h024_position_count') if isinstance(observed, dict) else None}")
    print(f"H024 order count: {observed.get('h024_order_count') if isinstance(observed, dict) else None}")
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

    for position in record.get("h024_positions", []):
        print(
            "H024 position "
            f"symbol={position.get('runtime_symbol')} "
            f"ticket={position.get('ticket')} "
            f"identifier={position.get('identifier')} "
            f"magic={position.get('magic')} "
            f"volume={position.get('volume')} "
            f"type={position.get('position_type')} "
            f"verdict={position.get('verdict')}"
        )

    for order in record.get("h024_orders", []):
        print(
            "H024 order "
            f"symbol={order.get('runtime_symbol')} "
            f"ticket={order.get('ticket')} "
            f"magic={order.get('magic')} "
            f"volume={order.get('volume')} "
            f"type={order.get('order_type')} "
            f"verdict={order.get('verdict')}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())