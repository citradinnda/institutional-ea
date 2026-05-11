from __future__ import annotations

import argparse

from quantcore.execution.h024_broker_request_draft_envelope import (
    DraftEnvelopeInputs,
    build_draft_envelope,
    load_single_jsonl_record,
    write_single_jsonl_record,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--draft-construction-approval",
        default="reports/h024_standard_demo_broker_request_draft_construction_approval.jsonl",
    )
    parser.add_argument(
        "--preview-envelope",
        default="reports/h024_standard_demo_broker_request_preview_envelope.jsonl",
    )
    parser.add_argument(
        "--output",
        default="reports/h024_standard_demo_broker_request_draft_envelope.jsonl",
    )
    parser.add_argument("--allowed-demo-server", required=True)
    args = parser.parse_args()

    approval = load_single_jsonl_record(args.draft_construction_approval)
    preview_envelope = load_single_jsonl_record(args.preview_envelope)
    record = build_draft_envelope(
        DraftEnvelopeInputs(
            draft_construction_approval=approval,
            preview_envelope=preview_envelope,
            allowed_demo_server=args.allowed_demo_server,
        )
    )
    write_single_jsonl_record(args.output, record)

    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())