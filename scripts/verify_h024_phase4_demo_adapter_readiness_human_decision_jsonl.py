from __future__ import annotations

import argparse

from quantcore.execution.h024_phase4_demo_adapter_readiness_human_decision import (
    format_verification_summary,
    read_jsonl,
    verify_human_decision_records,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 Phase 4 demo adapter readiness human decision JSONL."
    )
    parser.add_argument("jsonl", help="Human decision JSONL to verify.")
    parser.add_argument("--allowed-demo-server", default=None, help="Allowed demo server name.")
    parser.add_argument("--require-approved", action="store_true", help="Require the review approval decision.")

    args = parser.parse_args(argv)

    records = read_jsonl(args.jsonl)
    violations = verify_human_decision_records(
        records,
        allowed_demo_server=args.allowed_demo_server,
        require_approved=args.require_approved,
    )
    print(format_verification_summary(records, violations))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())