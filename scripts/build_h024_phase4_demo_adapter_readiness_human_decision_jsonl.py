from __future__ import annotations

import argparse

from quantcore.execution.h024_phase4_demo_adapter_readiness_human_decision import (
    DECISION,
    build_human_decision_records_from_file,
    format_verification_summary,
    verify_human_decision_records,
    write_jsonl,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 Phase 4 demo adapter readiness human decision JSONL."
    )
    parser.add_argument("--readiness-packet", required=True, help="Adapter readiness packet JSONL.")
    parser.add_argument("--output", required=True, help="Output human decision JSONL.")
    parser.add_argument("--decision", default=DECISION, help="Human decision to record.")
    parser.add_argument("--decided-by", default="human_operator", help="Human decision actor label.")
    parser.add_argument("--allowed-demo-server", default=None, help="Allowed demo server name.")

    args = parser.parse_args(argv)

    records = build_human_decision_records_from_file(
        args.readiness_packet,
        decision=args.decision,
        decided_by=args.decided_by,
    )
    write_jsonl(args.output, records)

    violations = verify_human_decision_records(
        records,
        allowed_demo_server=args.allowed_demo_server,
        require_approved=True,
    )
    print(format_verification_summary(records, violations))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())