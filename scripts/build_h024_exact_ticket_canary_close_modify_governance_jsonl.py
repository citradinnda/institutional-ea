from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from quantcore.execution.h024_exact_ticket_canary_close_modify_governance import (
    build_governance_packet,
    load_json_object,
    load_latest_jsonl_record,
    write_jsonl_record,
)

DEFAULT_GATE_PATH = Path("reports/h024_runtime_no_mutation_safety_gate.jsonl")
DEFAULT_UNIFIED_PATH = Path("reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl")
DEFAULT_ACCOUNT_PATH = Path("reports/h024_runtime_account_risk_margin_safety_supervisor.jsonl")
DEFAULT_EXPOSURE_PATH = Path("reports/h024_runtime_exposure_inventory_safety_supervisor.jsonl")
DEFAULT_TICK_PATH = Path("reports/h024_runtime_tick_spread_safety_supervisor.jsonl")
DEFAULT_DECISION_PATH = Path(
    "config/h024_runtime_safety/"
    "default_exact_ticket_canary_close_modify_governance_decision.json"
)
DEFAULT_OUTPUT_PATH = Path("reports/h024_exact_ticket_canary_close_modify_governance.jsonl")
READ_ONLY_UPSTREAM_BUILD_SCRIPTS = (
    Path("scripts/build_h024_runtime_safety_lockout_jsonl.py"),
    Path("scripts/build_h024_runtime_safety_heartbeat_jsonl.py"),
    Path("scripts/build_h024_runtime_tick_spread_safety_supervisor_jsonl.py"),
    Path("scripts/build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py"),
    Path("scripts/build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py"),
    Path("scripts/build_h024_runtime_safety_aggregate_supervisor_jsonl.py"),
    Path("scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py"),
)


def _autobuild_read_only_upstream_reports() -> None:
    for script in READ_ONLY_UPSTREAM_BUILD_SCRIPTS:
        if not script.exists():
            continue
        result = subprocess.run([sys.executable, str(script)], check=False)
        if result.returncode != 0:
            print(
                f"Warning: read-only upstream evidence builder failed closed: {script}",
                file=sys.stderr,
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build the read-only H024 exact-ticket canary close/modify "
            "governance specification JSONL packet."
        )
    )
    parser.add_argument("--gate-path", default=DEFAULT_GATE_PATH)
    parser.add_argument("--unified-path", default=DEFAULT_UNIFIED_PATH)
    parser.add_argument("--account-path", default=DEFAULT_ACCOUNT_PATH)
    parser.add_argument("--exposure-path", default=DEFAULT_EXPOSURE_PATH)
    parser.add_argument("--tick-path", default=DEFAULT_TICK_PATH)
    parser.add_argument("--decision-path", default=DEFAULT_DECISION_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--observed-at-utc", default=None)
    parser.add_argument("--max-gate-age-seconds", type=int, default=3600)
    parser.add_argument("--max-snapshot-age-seconds", type=int, default=3600)
    parser.add_argument(
        "--skip-autobuild-upstream",
        action="store_true",
        help=(
            "Do not run the read-only upstream runtime evidence builders before "
            "building the governance packet. Missing evidence still fails closed."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.skip_autobuild_upstream:
        _autobuild_read_only_upstream_reports()

    gate_record = load_latest_jsonl_record(args.gate_path)
    unified_record = load_latest_jsonl_record(args.unified_path)
    account_record = load_latest_jsonl_record(args.account_path)
    exposure_record = load_latest_jsonl_record(args.exposure_path)
    tick_record = load_latest_jsonl_record(args.tick_path)
    decision_record = load_json_object(args.decision_path)

    record = build_governance_packet(
        no_mutation_gate_record=gate_record,
        human_decision_record=decision_record,
        unified_supervision_record=unified_record,
        account_risk_margin_record=account_record,
        exposure_inventory_record=exposure_record,
        tick_spread_record=tick_record,
        observed_at_utc=args.observed_at_utc,
        max_gate_age_seconds=args.max_gate_age_seconds,
        max_snapshot_age_seconds=args.max_snapshot_age_seconds,
    )
    write_jsonl_record(args.output, record)

    observed = record.get("observed", {})
    print(f"Wrote {args.output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Operator state: {record['operator_state']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Gate verdict: {observed.get('gate_verdict')}")
    print(f"Gate opens mutation path: {observed.get('gate_opens_mutation_path')}")
    print(f"Exact canary state: {observed.get('exact_canary_state')}")
    print(f"Exact canary observed: {observed.get('exact_canary_observed')}")
    print(f"H024 position count: {observed.get('h024_position_count')}")
    print(f"H024 order count: {observed.get('h024_order_count')}")
    print(f"Human decision: {observed.get('human_decision')}")
    print(f"Effective new entries blocked: {record['effective_new_entries_blocked']}")
    for key, value in record["authorizations"].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
