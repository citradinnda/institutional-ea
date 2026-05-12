from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from quantcore.execution.h024_runtime_no_mutation_safety_gate import (  # noqa: E402
    DEFAULT_OUTPUT_PATH,
    collect_h024_runtime_no_mutation_safety_gate,
    write_jsonl,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the H024 runtime no-mutation safety gate JSONL packet.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Output JSONL path. Default: {DEFAULT_OUTPUT_PATH}",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    record = collect_h024_runtime_no_mutation_safety_gate()
    output_path = Path(args.output)
    write_jsonl(output_path, [record])

    gate_result = record.get("gate_result", {})
    unified = record.get("unified_supervision", {}).get("record", {})

    print(f"Wrote {output_path}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations', []))}")
    print(f"Operator state: {record.get('operator_state')}")
    print(f"Operator next action: {record.get('operator_next_action')}")
    print(f"Unified supervision verdict: {unified.get('verdict') if isinstance(unified, dict) else None}")
    print(f"Unified operator next action: {unified.get('operator_next_action') if isinstance(unified, dict) else None}")
    print(f"Gate opens mutation path: {gate_result.get('gate_opens_any_mutation_path') if isinstance(gate_result, dict) else None}")
    print(f"Future broker-facing code must check gate: {gate_result.get('future_broker_facing_code_must_check_gate') if isinstance(gate_result, dict) else None}")
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

    if isinstance(gate_result, dict):
        for key in sorted(key for key in gate_result if key.endswith("_blocked")):
            print(f"{key}: {gate_result.get(key)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())