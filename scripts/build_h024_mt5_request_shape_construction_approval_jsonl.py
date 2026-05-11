from __future__ import annotations

import argparse

from quantcore.execution.h024_mt5_request_shape_construction_approval import (
    Mt5RequestShapeConstructionApprovalInputs,
    build_mt5_request_shape_construction_approval,
    load_single_jsonl_record,
    write_single_jsonl_record,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--design-review-packet",
        default="reports/h024_standard_demo_mt5_request_shape_design_review_packet.jsonl",
    )
    parser.add_argument(
        "--output",
        default="reports/h024_standard_demo_mt5_request_shape_construction_approval.jsonl",
    )
    parser.add_argument("--allowed-demo-server", required=True)
    args = parser.parse_args()

    packet = load_single_jsonl_record(args.design_review_packet)
    record = build_mt5_request_shape_construction_approval(
        Mt5RequestShapeConstructionApprovalInputs(
            design_review_packet=packet,
            allowed_demo_server=args.allowed_demo_server,
        )
    )
    write_single_jsonl_record(args.output, record)

    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())