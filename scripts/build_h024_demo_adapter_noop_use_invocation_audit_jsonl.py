from __future__ import annotations

import argparse

from quantcore.execution.h024_demo_adapter_noop_use_invocation_audit import (
    build_noop_use_invocation_audit_from_files,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 demo adapter no-op use invocation audit JSONL artifact."
    )
    parser.add_argument(
        "noop_use_approval_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_noop_use_approval.jsonl",
    )
    parser.add_argument(
        "noop_transport_contract_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_noop_transport_contract.jsonl",
    )
    parser.add_argument(
        "output_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_noop_use_invocation_audit.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    args = parser.parse_args()

    record = build_noop_use_invocation_audit_from_files(
        noop_use_approval_jsonl=args.noop_use_approval_jsonl,
        noop_transport_contract_jsonl=args.noop_transport_contract_jsonl,
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