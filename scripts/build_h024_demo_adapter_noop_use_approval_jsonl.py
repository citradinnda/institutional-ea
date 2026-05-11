from __future__ import annotations

import argparse

from quantcore.execution.h024_demo_adapter_noop_use_approval import (
    build_noop_use_approval_from_files,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 demo adapter no-op use approval JSONL artifact."
    )
    parser.add_argument(
        "adapter_use_readiness_human_decision_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_phase4_demo_adapter_use_readiness_human_decision.jsonl",
    )
    parser.add_argument(
        "output_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_noop_use_approval.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    args = parser.parse_args()

    record = build_noop_use_approval_from_files(
        adapter_use_readiness_human_decision_jsonl=(
            args.adapter_use_readiness_human_decision_jsonl
        ),
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