from __future__ import annotations

import argparse

from quantcore.execution.h024_broker_request_construction_readiness_packet import (
    verify_broker_request_construction_readiness_packet_file,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 broker-request construction readiness packet JSONL artifact."
    )
    parser.add_argument(
        "input_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_broker_request_construction_readiness_packet.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    result = verify_broker_request_construction_readiness_packet_file(
        args.input_jsonl,
        allowed_demo_server=args.allowed_demo_server,
        require_pass=args.require_pass,
    )

    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if result.ok else 'FAIL'}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())