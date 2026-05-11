from __future__ import annotations

import argparse

from quantcore.execution.h024_demo_adapter_intent_refusal_audit import (
    format_verification_summary,
    read_jsonl,
    verify_audit_records,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 demo adapter intent-ingestion/refusal audit JSONL."
    )
    parser.add_argument("jsonl", help="Refusal audit JSONL to verify.")
    parser.add_argument("--allowed-demo-server", default=None, help="Allowed demo server name.")
    parser.add_argument("--require-refusal", action="store_true", help="Require refusal reasons.")

    args = parser.parse_args(argv)

    records = read_jsonl(args.jsonl)
    violations = verify_audit_records(
        records,
        allowed_demo_server=args.allowed_demo_server,
        require_refusal=args.require_refusal,
    )
    print(format_verification_summary(records, violations))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())