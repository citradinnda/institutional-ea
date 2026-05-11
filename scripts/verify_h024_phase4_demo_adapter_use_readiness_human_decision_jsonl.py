from __future__ import annotations

import argparse

from quantcore.execution.h024_phase4_demo_adapter_use_readiness_human_decision import (
    verify_adapter_use_readiness_human_decision_file,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 Phase 4 demo adapter-use readiness human decision JSONL artifact."
    )
    parser.add_argument(
        "input_jsonl",
        nargs="?",
        default="reports/h024_standard_demo_phase4_demo_adapter_use_readiness_human_decision.jsonl",
    )
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    result = verify_adapter_use_readiness_human_decision_file(
        args.input_jsonl,
        allowed_demo_server=args.allowed_demo_server,
        require_pass=args.require_approved,
    )

    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if result.ok else 'FAIL'}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())