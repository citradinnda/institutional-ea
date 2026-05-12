from __future__ import annotations

import argparse

from quantcore.execution.h024_one_shot_demo_canary_read_only_supervision_run import (
    DEFAULT_OUTPUT_PATH,
    run_read_only_supervision,
    write_jsonl,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full H024 canary read-only supervision stack.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    args = parser.parse_args()

    record = run_read_only_supervision()
    write_jsonl(args.output, [record])

    print(f"Wrote {args.output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Completed stages: {record['completed_stage_count']} / {record['stage_count']}")
    print(f"First failed stage: {record['first_failed_stage']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Broker mutation authorized: {record['broker_mutation_authorized']}")
    print(f"Trading loop authorized: {record['trading_loop_authorized']}")
    print(f"USDJPY separate readiness required: {record['automation_boundary']['usd_jpy_requires_separate_readiness']}")
    print(f"Kill switches required before trading loop: {record['automation_boundary']['kill_switches_required_before_trading_loop']}")
    print(f"Black-swan guards required before trading loop: {record['automation_boundary']['black_swan_guards_required_before_trading_loop']}")

    for stage in record["stages"]:
        print(f"{stage['name']}: {'PASS' if stage['passed'] else 'FAIL'}")

    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
