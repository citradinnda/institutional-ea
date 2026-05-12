from __future__ import annotations

import argparse
from pathlib import Path

from quantcore.execution.h024_exact_ticket_canary_close_modify_governance import (
    verify_jsonl_file,
)

DEFAULT_PATH = Path("reports/h024_exact_ticket_canary_close_modify_governance.jsonl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the read-only H024 exact-ticket canary close/modify "
            "governance specification JSONL packet."
        )
    )
    parser.add_argument("path", nargs="?", default=DEFAULT_PATH)
    parser.add_argument("--require-pass", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = verify_jsonl_file(args.path, require_pass=args.require_pass)
    print(f"H024 exact-ticket canary close/modify governance records: {result.record_count}")
    print(f"Violations: {len(result.violations)}")
    print(f"Embedded violations: {result.embedded_violations}")
    print(f"Record verdict: {result.record_verdict}")
    print(f"Verifier verdict: {result.verifier_verdict}")
    print(f"Operator state: {result.operator_state}")
    print(f"Operator next action: {result.operator_next_action}")
    for violation in result.violations:
        print(f"- {violation}")
    return 0 if result.verifier_verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
