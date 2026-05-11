from __future__ import annotations

import argparse

from quantcore.execution.h024_demo_adapter_boundary_static_verifier import (
    format_verification_summary,
    read_jsonl,
    verify_static_verifier_records,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 demo adapter boundary static verifier JSONL."
    )
    parser.add_argument("jsonl", help="Static verifier JSONL to verify.")
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Require a clean PASS verifier artifact.",
    )
    args = parser.parse_args(argv)

    records = read_jsonl(args.jsonl)
    violations = verify_static_verifier_records(records, require_pass=args.require_pass)
    print(format_verification_summary(records, violations))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())