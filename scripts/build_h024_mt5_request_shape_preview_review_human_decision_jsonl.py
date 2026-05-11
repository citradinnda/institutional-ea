from __future__ import annotations

import argparse

from quantcore.execution.h024_mt5_request_shape_preview_review_human_decision import (
    Mt5RequestShapePreviewReviewHumanDecisionInputs,
    build_mt5_request_shape_preview_review_human_decision,
    load_single_jsonl_record,
    write_single_jsonl_record,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--shape-preview-envelope",
        default="reports/h024_standard_demo_mt5_request_shape_preview_envelope.jsonl",
    )
    parser.add_argument(
        "--output",
        default="reports/h024_standard_demo_mt5_request_shape_preview_review_human_decision.jsonl",
    )
    parser.add_argument("--allowed-demo-server", required=True)
    args = parser.parse_args()

    shape_preview = load_single_jsonl_record(args.shape_preview_envelope)
    record = build_mt5_request_shape_preview_review_human_decision(
        Mt5RequestShapePreviewReviewHumanDecisionInputs(
            shape_preview_envelope=shape_preview,
            allowed_demo_server=args.allowed_demo_server,
        )
    )
    write_single_jsonl_record(args.output, record)

    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())