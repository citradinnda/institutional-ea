from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quantcore.execution.h024_exact_ticket_canary_close_modify_decision_artifact import (
    verify_jsonl,
)

DEFAULT_INPUT = Path("reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 exact-ticket canary close/modify decision artifact JSONL packet."
    )
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    summary = verify_jsonl(args.path, require_pass=args.require_pass)
    records = summary["records"]
    print(f"H024 exact-ticket canary close/modify decision artifact records: {summary['record_count']}")
    print(f"Violations: {len(summary['violations'])}")
    print(f"Embedded violations: {summary['embedded_violations']}")
    if records:
        record = records[-1]
        print(f"Record verdict: {record.get('verdict')}")
        print(f"Verifier verdict: {summary['verifier_verdict']}")
        print(f"Operator state: {record.get('operator_state')}")
        print(f"Operator next action: {record.get('operator_next_action')}")
        print(f"Requested action: {record.get('observed', {}).get('requested_action')}")
        print(f"Effective new entries blocked: {record.get('effective_new_entries_blocked')}")
        authorizations = record.get("authorizations", {})
        if isinstance(authorizations, dict):
            for field, value in authorizations.items():
                print(f"{field}: {value}")
    for violation in summary["violations"]:
        print(f"VIOLATION: {violation}")
    return 0 if summary["verifier_verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
