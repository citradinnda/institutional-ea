from __future__ import annotations

import argparse

from quantcore.execution.h024_broker_request_preview_envelope import (
    build_preview_envelope_from_files,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build H024 inert broker-request preview envelope JSONL."
    )
    parser.add_argument(
        "preview_construction_approval_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_broker_request_preview_construction_approval.jsonl",
    )
    parser.add_argument(
        "order_intent_simulation_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_order_intent_simulation.jsonl",
    )
    parser.add_argument(
        "allow_state_preflight_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_execution_safety_controls_allow_state_preflight.jsonl",
    )
    parser.add_argument(
        "output_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_broker_request_preview_envelope.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    args = parser.parse_args()

    record = build_preview_envelope_from_files(
        preview_construction_approval_jsonl=args.preview_construction_approval_jsonl,
        order_intent_simulation_jsonl=args.order_intent_simulation_jsonl,
        allow_state_preflight_jsonl=args.allow_state_preflight_jsonl,
        output_jsonl=args.output_jsonl,
        allowed_demo_server=args.allowed_demo_server,
    )

    print(f"Output: {args.output_jsonl}")
    print(f"Status: {record['status']}")
    print(f"Decision: {record['decision']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())