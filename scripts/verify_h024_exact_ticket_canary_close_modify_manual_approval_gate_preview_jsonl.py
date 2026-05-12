from __future__ import annotations

import argparse
from pathlib import Path

from quantcore.execution.h024_exact_ticket_canary_close_modify_manual_approval_gate_preview import (
    AUTHORIZATION_FALSE_FIELDS,
    EXPECTED_IDENTIFIER,
    EXPECTED_TICKET,
    verify_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the H024 exact-ticket close/modify manual approval gate preview JSONL packet."
    )
    parser.add_argument("path")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    records, violations = verify_report(Path(args.path), require_pass=args.require_pass)

    print(f"H024 exact-ticket canary close/modify manual approval gate preview records: {len(records)}")
    print(f"Violations: {len(violations)}")
    if records:
        record = records[-1]
        print(f"Record verdict: {record.get('verdict')}")
        print(f"Verifier verdict: {'PASS' if not violations else 'FAIL_CLOSED'}")
        print(f"Operator state: {record.get('operator_state')}")
        print(f"Operator next action: {record.get('operator_next_action')}")
        print(f"Exact ticket: {EXPECTED_TICKET}")
        print(f"Exact identifier: {EXPECTED_IDENTIFIER}")
        print(f"Effective new entries blocked: {record.get('effective_new_entries_blocked')}")
        for field in AUTHORIZATION_FALSE_FIELDS:
            print(f"{field}: {record.get(field)}")
        print(
            "manual_approval_gate_preview_authorizes_action: "
            f"{record.get('manual_approval_gate_preview_authorizes_action')}"
        )
        print(f"live_broker_request_constructed: {record.get('live_broker_request_constructed')}")
        print(
            "dry_run_request_shape_preview_constructed: "
            f"{record.get('dry_run_request_shape_preview_constructed')}"
        )

    for violation in violations:
        print(f"VIOLATION: {violation}")

    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
