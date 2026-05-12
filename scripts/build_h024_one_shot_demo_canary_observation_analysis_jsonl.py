from __future__ import annotations

import argparse
import sys

from quantcore.execution.h024_one_shot_demo_canary_observation_analysis import (
    DEFAULT_LEDGER_PATH,
    DEFAULT_LIFECYCLE_DECISION_PATH,
    DEFAULT_MONITOR_PATH,
    DEFAULT_OUTPUT_PATH,
    DEFAULT_POST_ORDER_AUDIT_PATH,
    build_observation_analysis,
    write_jsonl,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the H024 canary observation analysis JSONL packet.")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER_PATH))
    parser.add_argument("--post-order-audit", default=str(DEFAULT_POST_ORDER_AUDIT_PATH))
    parser.add_argument("--monitor", default=str(DEFAULT_MONITOR_PATH))
    parser.add_argument("--lifecycle-decision", default=str(DEFAULT_LIFECYCLE_DECISION_PATH))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    args = parser.parse_args()

    record = build_observation_analysis(
        ledger_path=args.ledger,
        post_order_audit_path=args.post_order_audit,
        monitor_path=args.monitor,
        lifecycle_decision_path=args.lifecycle_decision,
    )
    write_jsonl(args.output, [record])

    execution = record["execution_observations"]
    lifecycle = record["lifecycle_observations"]
    latest = record["latest_mark_to_market"]

    print(f"Wrote {args.output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Slippage absolute: {execution['slippage_absolute']}")
    print(f"Slippage adverse to sell: {execution['slippage_adverse_to_sell']}")
    print(f"Order-check margin: {execution['order_check_margin']}")
    print(f"MT5 comment truncated: {execution['comment_truncated']}")
    print(f"Monitor lifecycle state: {lifecycle['monitor_lifecycle_state']}")
    print(f"Lifecycle decision: {lifecycle['lifecycle_decision']}")
    print(f"Broker mutation authorized: {record['broker_mutation_authorized']}")
    print(f"Edge inference authorized: {record['edge_inference_authorized']}")
    print(f"Current price: {latest['current_price']}")
    print(f"Floating P/L: {latest['floating_pl']}")
    print(f"Swap: {latest['swap']}")

    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())