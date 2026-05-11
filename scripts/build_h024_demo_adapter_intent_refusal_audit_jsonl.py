from __future__ import annotations

import argparse

from quantcore.execution.h024_demo_adapter_intent_refusal_audit import (
    build_audit_records_from_files,
    format_verification_summary,
    verify_audit_records,
    write_jsonl,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 demo adapter intent-ingestion/refusal audit JSONL."
    )
    parser.add_argument("--skeleton", required=True, help="Fail-closed demo execution adapter skeleton JSONL.")
    parser.add_argument(
        "--order-intent-simulation",
        required=True,
        help="Standard-demo order-intent simulation JSONL.",
    )
    parser.add_argument(
        "--safety-preflight",
        default=None,
        help="Optional execution safety-controls preflight JSONL.",
    )
    parser.add_argument("--output", required=True, help="Output refusal audit JSONL.")
    parser.add_argument("--allowed-demo-server", default=None, help="Allowed demo server name.")

    args = parser.parse_args(argv)

    records = build_audit_records_from_files(
        skeleton_jsonl=args.skeleton,
        order_intent_simulation_jsonl=args.order_intent_simulation,
        safety_preflight_jsonl=args.safety_preflight,
    )
    write_jsonl(args.output, records)

    violations = verify_audit_records(
        records,
        allowed_demo_server=args.allowed_demo_server,
        require_refusal=True,
    )
    print(format_verification_summary(records, violations))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())