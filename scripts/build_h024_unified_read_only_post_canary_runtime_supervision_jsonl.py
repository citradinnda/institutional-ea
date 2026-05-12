from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from quantcore.execution.h024_unified_read_only_post_canary_runtime_supervision import (  # noqa: E402
    DEFAULT_OUTPUT_PATH,
    collect_h024_unified_read_only_post_canary_runtime_supervision,
    write_jsonl,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the H024 unified read-only post-canary runtime supervision JSONL packet.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help=f"Output JSONL path. Default: {DEFAULT_OUTPUT_PATH}",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision()
    output_path = Path(args.output)
    write_jsonl(output_path, [record])

    canary = record.get("canary_read_only_supervision", {}).get("summary", {})
    aggregate = record.get("runtime_safety_aggregate", {}).get("summary", {})
    exact_canary = record.get("exact_known_canary", {})

    print(f"Wrote {output_path}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations', []))}")
    print(f"Operator state: {record.get('operator_state')}")
    print(f"Operator next action: {record.get('operator_next_action')}")
    print(f"Canary supervision records: {canary.get('record_count')}")
    print(f"Canary supervision all records passed: {canary.get('all_records_passed')}")
    print(f"Canary operator next action: {canary.get('operator_next_action')}")
    print(f"Runtime aggregate verdict: {aggregate.get('verdict')}")
    print(f"Runtime aggregate operator state: {aggregate.get('operator_state')}")
    print(f"Exact canary state: {exact_canary.get('state')}")
    print(f"Exact canary observed: {exact_canary.get('observed')}")
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

    for summary in aggregate.get("upstream_summaries", []) or []:
        print(
            "Runtime aggregate upstream "
            f"{summary.get('source')}: "
            f"verdict={summary.get('verdict')} "
            f"age_seconds={summary.get('age_seconds')} "
            f"embedded_violations={summary.get('embedded_violation_count')}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())