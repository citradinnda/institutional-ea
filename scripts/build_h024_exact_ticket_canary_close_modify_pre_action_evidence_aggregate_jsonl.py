from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from quantcore.execution.h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate import (
    build_pre_action_evidence_aggregate_record,
    load_latest_jsonl_record,
    write_jsonl_record,
)

DEFAULT_OUTPUT = Path("reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl")
DEFAULT_UPSTREAM_PATHS = {
    "no_mutation_gate": Path("reports/h024_runtime_no_mutation_safety_gate.jsonl"),
    "unified_runtime_supervision": Path(
        "reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl"
    ),
    "exact_ticket_governance": Path(
        "reports/h024_exact_ticket_canary_close_modify_governance.jsonl"
    ),
    "decision_artifact": Path(
        "reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl"
    ),
}
UPSTREAM_BUILDERS = (
    Path("scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py"),
    Path("scripts/build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py"),
    Path("scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py"),
    Path("scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py"),
)


def _run_builder(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing upstream builder: {path}")
    completed = subprocess.run([sys.executable, str(path)], check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Upstream builder failed: {path} exit={completed.returncode}")


def _load_upstreams(paths: dict[str, Path]) -> dict:
    upstreams = {}
    for key, path in paths.items():
        upstreams[key] = load_latest_jsonl_record(path)
    return upstreams


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build the H024 exact-ticket close/modify read-only pre-action evidence "
            "aggregate JSONL packet."
        )
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip-upstream-build", action="store_true")
    parser.add_argument("--max-upstream-age-seconds", type=float, default=300.0)
    parser.add_argument("--position-open-over-three-bars", action="store_true")
    for key, default_path in DEFAULT_UPSTREAM_PATHS.items():
        parser.add_argument(f"--{key.replace('_', '-')}-path", type=Path, default=default_path)
    args = parser.parse_args(argv)

    if not args.skip_upstream_build:
        for builder in UPSTREAM_BUILDERS:
            _run_builder(builder)

    paths = {
        "no_mutation_gate": args.no_mutation_gate_path,
        "unified_runtime_supervision": args.unified_runtime_supervision_path,
        "exact_ticket_governance": args.exact_ticket_governance_path,
        "decision_artifact": args.decision_artifact_path,
    }
    upstreams = _load_upstreams(paths)
    record = build_pre_action_evidence_aggregate_record(
        upstreams,
        max_upstream_age_seconds=args.max_upstream_age_seconds,
        user_reported_position_open_over_three_bars=args.position_open_over_three_bars,
    )
    write_jsonl_record(args.output, record)

    print(f"Wrote {args.output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Operator state: {record['operator_state']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Exact ticket: {record['expected']['exact_ticket']}")
    print(f"Exact identifier: {record['expected']['exact_identifier']}")
    print(
        "User reported position open over three bars: "
        f"{record['operator_context']['user_reported_position_open_over_three_bars']}"
    )
    print(f"Effective new entries blocked: {record['effective_new_entries_blocked']}")
    for key, value in record["authorizations"].items():
        print(f"{key}: {value}")
    for key, summary in record["upstream_summaries"].items():
        print(
            f"Upstream {key}: verdict={summary.get('verdict')} "
            f"age_seconds={summary.get('age_seconds')} "
            f"embedded_violations={summary.get('embedded_violation_count')}"
        )
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
