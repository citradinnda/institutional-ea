from __future__ import annotations

import argparse

from quantcore.execution.h024_one_shot_demo_canary_supervisory_state import (
    DEFAULT_OUTPUT_PATH,
    read_jsonl,
    verify_supervisory_state_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the H024 canary supervisory state JSONL packet.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    records = read_jsonl(args.path)
    violations: list[str] = []

    if len(records) != 1:
        violations.append(f"expected exactly 1 supervisory state record, observed {len(records)}")

    if records:
        violations.extend(verify_supervisory_state_record(records[0], require_pass=args.require_pass))
        verdict = records[0].get("supervisory_verdict")
        state = records[0].get("supervisory_state")
        embedded_count = len(records[0].get("violations", [])) if isinstance(records[0].get("violations"), list) else "unknown"
        review_count = len(records[0].get("review_triggers", [])) if isinstance(records[0].get("review_triggers"), list) else "unknown"
    else:
        verdict = None
        state = None
        embedded_count = "unknown"
        review_count = "unknown"

    print(f"H024 one-shot demo canary supervisory state records: {len(records)}")
    print(f"Violations: {len(violations)}")
    print(f"Embedded violations: {embedded_count}")
    print(f"Review triggers: {review_count}")
    print(f"Supervisory verdict: {verdict}")
    print(f"Supervisory state: {state}")

    for violation in violations:
        print(f"- {violation}")

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
