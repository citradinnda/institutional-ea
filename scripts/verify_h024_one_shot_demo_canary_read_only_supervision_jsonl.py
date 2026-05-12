from __future__ import annotations

import argparse

from quantcore.execution.h024_one_shot_demo_canary_read_only_supervision_run import (
    DEFAULT_OUTPUT_PATH,
    read_jsonl,
    verify_supervision_run_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the H024 canary read-only supervision run JSONL packet.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    records = read_jsonl(args.path)
    violations: list[str] = []

    if len(records) != 1:
        violations.append(f"expected exactly 1 read-only supervision run record, observed {len(records)}")

    if records:
        violations.extend(verify_supervision_run_record(records[0], require_pass=args.require_pass))
        verdict = records[0].get("verdict")
        embedded_count = len(records[0].get("violations", [])) if isinstance(records[0].get("violations"), list) else "unknown"
        completed = records[0].get("completed_stage_count")
        total = records[0].get("stage_count")
    else:
        verdict = None
        embedded_count = "unknown"
        completed = None
        total = None

    print(f"H024 one-shot demo canary read-only supervision run records: {len(records)}")
    print(f"Violations: {len(violations)}")
    print(f"Embedded violations: {embedded_count}")
    print(f"Completed stages: {completed} / {total}")
    print(f"Verdict: {verdict}")

    for violation in violations:
        print(f"- {violation}")

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
