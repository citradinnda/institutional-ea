from __future__ import annotations

import argparse

from quantcore.execution.h024_broker_request_draft_review_human_decision import (
    DraftReviewHumanDecisionInputs,
    build_draft_review_human_decision,
    load_single_jsonl_record,
    write_single_jsonl_record,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--draft-envelope",
        default="reports/h024_standard_demo_broker_request_draft_envelope.jsonl",
    )
    parser.add_argument(
        "--output",
        default="reports/h024_standard_demo_broker_request_draft_review_human_decision.jsonl",
    )
    parser.add_argument("--allowed-demo-server", required=True)
    args = parser.parse_args()

    draft_envelope = load_single_jsonl_record(args.draft_envelope)
    record = build_draft_review_human_decision(
        DraftReviewHumanDecisionInputs(
            draft_envelope=draft_envelope,
            allowed_demo_server=args.allowed_demo_server,
        )
    )
    write_single_jsonl_record(args.output, record)

    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())