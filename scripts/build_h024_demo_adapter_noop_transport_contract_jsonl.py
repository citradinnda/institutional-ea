from __future__ import annotations

import argparse

from quantcore.execution.h024_demo_adapter_noop_transport_contract import (
    build_noop_transport_contract_from_files,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 demo adapter no-op transport contract JSONL artifact."
    )
    parser.add_argument(
        "readiness_human_decision_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_phase4_demo_adapter_readiness_human_decision.jsonl",
    )
    parser.add_argument(
        "intent_refusal_audit_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_intent_refusal_audit.jsonl",
    )
    parser.add_argument(
        "output_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_demo_adapter_noop_transport_contract.jsonl",
    )
    parser.add_argument(
        "--boundary-static-verifier-jsonl",
        default="reports/h024_standard_demo_demo_adapter_boundary_static_verifier.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    args = parser.parse_args()

    record = build_noop_transport_contract_from_files(
        readiness_human_decision_jsonl=args.readiness_human_decision_jsonl,
        intent_refusal_audit_jsonl=args.intent_refusal_audit_jsonl,
        output_jsonl=args.output_jsonl,
        boundary_static_verifier_jsonl=args.boundary_static_verifier_jsonl,
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