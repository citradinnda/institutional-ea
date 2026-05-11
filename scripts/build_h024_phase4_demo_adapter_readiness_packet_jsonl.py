from __future__ import annotations

import argparse

from quantcore.execution.h024_phase4_demo_adapter_readiness_packet import (
    build_readiness_packet_records_from_files,
    format_verification_summary,
    verify_readiness_packet_records,
    write_jsonl,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 Phase 4 demo adapter readiness packet JSONL."
    )
    parser.add_argument("--skeleton", required=True, help="Fail-closed demo execution adapter skeleton JSONL.")
    parser.add_argument(
        "--intent-refusal-audit",
        required=True,
        help="Demo adapter intent-ingestion/refusal audit JSONL.",
    )
    parser.add_argument(
        "--boundary-static-verifier",
        required=True,
        help="Demo adapter boundary static verifier JSONL.",
    )
    parser.add_argument("--output", required=True, help="Output readiness packet JSONL.")
    parser.add_argument("--allowed-demo-server", default=None, help="Allowed demo server name.")

    args = parser.parse_args(argv)

    records = build_readiness_packet_records_from_files(
        skeleton_jsonl=args.skeleton,
        intent_refusal_audit_jsonl=args.intent_refusal_audit,
        boundary_static_verifier_jsonl=args.boundary_static_verifier,
    )
    write_jsonl(args.output, records)

    violations = verify_readiness_packet_records(
        records,
        allowed_demo_server=args.allowed_demo_server,
        require_ready=True,
    )
    print(format_verification_summary(records, violations))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())