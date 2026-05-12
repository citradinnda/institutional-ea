from __future__ import annotations

import argparse
from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_monitor import load_jsonl, verify_monitor_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify an H024 one-shot standard-demo canary monitor JSONL packet.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--require-pass", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = load_jsonl(args.path)
    violations = verify_monitor_records(records, require_pass=args.require_pass)
    verdict = "FAIL" if violations else "PASS"
    print(f"H024 one-shot demo canary monitor records: {len(records)}")
    print(f"Violations: {len(violations)}")
    print(f"Verdict: {verdict}")
    if violations:
        for violation in violations:
            print(f"- {violation['code']}: {violation.get('detail')}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())