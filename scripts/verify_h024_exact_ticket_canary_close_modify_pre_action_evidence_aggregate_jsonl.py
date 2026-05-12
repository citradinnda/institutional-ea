from __future__ import annotations

import argparse
from pathlib import Path

from quantcore.execution.h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate import (
    verify_jsonl_path,
)

DEFAULT_INPUT = Path("reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 exact-ticket close/modify pre-action evidence aggregate JSONL packet."
    )
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args(argv)

    ok, violations, records = verify_jsonl_path(args.path, require_pass=args.require_pass)
    print(f"H024 exact-ticket canary close/modify pre-action evidence aggregate records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    if records:
        record = records[-1]
        print(f"Record verdict: {record.get('verdict')}")
        print(f"Verifier verdict: {'PASS' if ok else 'FAIL'}")
        print(f"Operator state: {record.get('operator_state')}")
        print(f"Operator next action: {record.get('operator_next_action')}")
        print(f"Exact ticket: {record.get('expected', {}).get('exact_ticket')}")
        print(f"Exact identifier: {record.get('expected', {}).get('exact_identifier')}")
        print(f"Effective new entries blocked: {record.get('effective_new_entries_blocked')}")
        authorizations = record.get("authorizations", {})
        if isinstance(authorizations, dict):
            for key in sorted(authorizations):
                print(f"{key}: {authorizations[key]}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
