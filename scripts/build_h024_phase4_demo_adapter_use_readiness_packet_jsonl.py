from __future__ import annotations

import argparse

from quantcore.execution.h024_phase4_demo_adapter_use_readiness_packet import (
    build_adapter_use_readiness_packet_from_files,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 Phase 4 demo adapter-use readiness packet JSONL artifact."
    )
    parser.add_argument(
        "noop_transport_contract_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_noop_transport_contract.jsonl",
    )
    parser.add_argument(
        "boundary_static_verifier_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl",
    )
    parser.add_argument(
        "output_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_phase4_demo_adapter_use_readiness_packet.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    args = parser.parse_args()

    record = build_adapter_use_readiness_packet_from_files(
        noop_transport_contract_jsonl=args.noop_transport_contract_jsonl,
        boundary_static_verifier_jsonl=args.boundary_static_verifier_jsonl,
        output_jsonl=args.output_jsonl,
        allowed_demo_server=args.allowed_demo_server,
    )

    print(f"Output: {args.output_jsonl}")
    print(f"Status: {record['status']}")
    print(f"Decision: {record['decision']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())