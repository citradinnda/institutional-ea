from __future__ import annotations

import argparse
import sys

from quantcore.execution.h024_one_shot_demo_canary_observation_analysis import (
    DEFAULT_OUTPUT_PATH,
    read_jsonl,
    verify_observation_analysis_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the H024 canary observation analysis JSONL packet.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    records = read_jsonl(args.path)
    violations: list[str] = []

    if len(records) != 1:
        violations.append(f"expected exactly 1 observation analysis record, observed {len(records)}")

    if records:
        violations.extend(verify_observation_analysis_record(records[0], require_pass=args.require_pass))
        verdict = records[0].get("verdict")
        embedded_count = len(records[0].get("violations", [])) if isinstance(records[0].get("violations"), list) else "unknown"
    else:
        verdict = None
        embedded_count = "unknown"

    print(f"H024 one-shot demo canary observation analysis records: {len(records)}")
    print(f"Violations: {len(violations)}")
    print(f"Embedded violations: {embedded_count}")
    print(f"Verdict: {verdict}")

    for violation in violations:
        print(f"- {violation}")

    if violations:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())