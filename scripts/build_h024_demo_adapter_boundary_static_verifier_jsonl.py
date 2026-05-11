from __future__ import annotations

import argparse

from quantcore.execution.h024_demo_adapter_boundary_static_verifier import (
    build_static_verifier_records,
    format_verification_summary,
    verify_static_verifier_records,
    write_jsonl,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 demo adapter boundary static verifier JSONL."
    )
    parser.add_argument("--output", required=True, help="Output static verifier JSONL.")
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root used to resolve relative target paths.",
    )
    parser.add_argument(
        "--target",
        action="append",
        default=None,
        help="Optional target path to scan. May be supplied multiple times. Defaults to the known H024 demo adapter implementation surface.",
    )
    args = parser.parse_args(argv)

    records = build_static_verifier_records(args.target, root=args.root)
    write_jsonl(args.output, records)

    violations = verify_static_verifier_records(records, require_pass=True)
    print(format_verification_summary(records, violations))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())