from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from quantcore.execution.h024_exact_ticket_canary_close_modify_manual_approval_gate_preview import (
    AUTHORIZATION_FALSE_FIELDS,
    EXPECTED_IDENTIFIER,
    EXPECTED_TICKET,
    build_manual_approval_gate_preview_record,
    write_jsonl,
)

DEFAULT_OUTPUT = "reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl"


def run_checked(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, check=True)


def refresh_upstreams(position_open_over_three_bars: bool) -> None:
    run_checked([sys.executable, "scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py"])
    run_checked([sys.executable, "scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py"])
    run_checked([sys.executable, "scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py"])

    pre_action_command = [
        sys.executable,
        "scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py",
    ]
    if position_open_over_three_bars:
        pre_action_command.append("--position-open-over-three-bars")
    run_checked(pre_action_command)

    bar_age_command = [
        sys.executable,
        "scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py",
    ]
    if position_open_over_three_bars:
        bar_age_command.append("--position-open-over-three-bars")
    run_checked(bar_age_command)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 exact-ticket close/modify manual approval gate preview JSONL packet."
    )
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--no-refresh-upstreams", action="store_true")
    parser.add_argument("--position-open-over-three-bars", action="store_true")
    parser.add_argument("--max-upstream-age-seconds", type=float, default=300.0)
    args = parser.parse_args()

    if not args.no_refresh_upstreams:
        refresh_upstreams(args.position_open_over_three_bars)

    record = build_manual_approval_gate_preview_record(
        max_upstream_age_seconds=args.max_upstream_age_seconds
    )
    output = Path(args.output)
    write_jsonl(record, output)

    print(f"Wrote {output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Operator state: {record['operator_state']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Exact ticket: {EXPECTED_TICKET}")
    print(f"Exact identifier: {EXPECTED_IDENTIFIER}")
    print(f"Effective new entries blocked: {record['effective_new_entries_blocked']}")
    for field in AUTHORIZATION_FALSE_FIELDS:
        print(f"{field}: {record[field]}")
    print(f"manual_approval_gate_preview_authorizes_action: {record['manual_approval_gate_preview_authorizes_action']}")
    print(f"live_broker_request_constructed: {record['live_broker_request_constructed']}")
    print(f"dry_run_request_shape_preview_constructed: {record['dry_run_request_shape_preview_constructed']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
