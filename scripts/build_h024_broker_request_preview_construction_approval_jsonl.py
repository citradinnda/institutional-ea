from __future__ import annotations

import argparse

from quantcore.execution.h024_broker_request_preview_envelope import (
    build_preview_construction_approval_from_files,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build H024 broker-request preview construction approval JSONL."
    )
    parser.add_argument(
        "readiness_packet_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_broker_request_construction_readiness_packet.jsonl",
    )
    parser.add_argument(
        "output_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_broker_request_preview_construction_approval.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    args = parser.parse_args()

    record = build_preview_construction_approval_from_files(
        readiness_packet_jsonl=args.readiness_packet_jsonl,
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