from __future__ import annotations

import argparse
from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_lifecycle_decision import build_from_monitor_jsonl

DEFAULT_MONITOR = Path("reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl")
DEFAULT_OUTPUT = Path("reports/h024_standard_demo_one_shot_demo_canary_lifecycle_decision.jsonl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the H024 one-shot standard-demo canary review-only lifecycle decision packet.")
    parser.add_argument("--monitor", type=Path, default=DEFAULT_MONITOR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    record = build_from_monitor_jsonl(monitor_path=args.monitor, output_path=args.output)

    latest_known = record.get("latest_known") or {}

    print(f"Wrote {args.output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Decision: {record['decision']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Broker mutation authorized: {record['safety_contract']['broker_mutation_authorized']}")
    print(f"MT5 call authorized: {record['safety_contract']['mt5_call_authorized']}")
    print(f"Close authorized: {record['safety_contract']['close_authorized']}")
    print(f"Current price: {latest_known.get('price_current')}")
    print(f"Floating P/L: {latest_known.get('profit')}")
    print(f"Swap: {latest_known.get('swap')}")

    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())