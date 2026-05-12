from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quantcore.execution.h024_exact_ticket_canary_close_modify_decision_artifact import (
    DEFAULT_MAX_AGE_SECONDS,
    load_decision_artifact_template,
    materialize_decision_artifact_template,
    validate_decision_artifact,
    write_jsonl_record,
)

DEFAULT_INPUT = Path(
    "config/h024_runtime_safety/default_exact_ticket_canary_close_modify_decision_artifact.json"
)
DEFAULT_OUTPUT = Path("reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the H024 exact-ticket canary close/modify decision artifact JSONL packet."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-age-seconds", type=int, default=DEFAULT_MAX_AGE_SECONDS)
    args = parser.parse_args()

    template = load_decision_artifact_template(args.input)
    artifact = materialize_decision_artifact_template(
        template, max_age_seconds=args.max_age_seconds
    )
    record = validate_decision_artifact(artifact, max_age_seconds=args.max_age_seconds)
    write_jsonl_record(record, args.output)

    print(f"Wrote {args.output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Operator state: {record['operator_state']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Decision status: {record['observed'].get('decision_status')}")
    print(f"Requested action: {record['observed'].get('requested_action')}")
    print(f"Exact ticket: {record['observed'].get('exact_canary', {}).get('ticket')}")
    print(f"Exact identifier: {record['observed'].get('exact_canary', {}).get('identifier')}")
    print(f"Effective new entries blocked: {record['effective_new_entries_blocked']}")
    for field, value in record["authorizations"].items():
        print(f"{field}: {value}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
