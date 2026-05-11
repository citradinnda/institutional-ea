from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from quantcore.execution.h024_execution_safety_controls_design import build_h024_execution_safety_controls_design


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"JSONL line {line_number} is not an object")
            records.append(value)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Build H024 execution safety-controls design JSONL.")
    parser.add_argument(
        "phase4_readiness_review_jsonl",
        type=Path,
        nargs="?",
        default=Path("reports/h024_standard_demo_phase4_readiness_review.jsonl"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/h024_standard_demo_execution_safety_controls_design.jsonl"),
    )
    parser.add_argument("--allowed-demo-server", action="append", required=True)
    parser.add_argument("--expected-account-currency", default="USD")
    parser.add_argument("--max-risk-fraction", default="0.01")
    args = parser.parse_args()

    verifier_command = [
        sys.executable,
        "scripts/verify_h024_phase4_readiness_review_jsonl.py",
        str(args.phase4_readiness_review_jsonl),
    ]
    for server in args.allowed_demo_server:
        verifier_command.extend(["--allowed-demo-server", server])
    verifier_command.extend(
        [
            "--expected-account-currency",
            args.expected_account_currency,
            "--max-risk-fraction",
            args.max_risk_fraction,
            "--require-review",
        ]
    )

    verifier = subprocess.run(verifier_command, check=False, capture_output=True, text=True)
    if verifier.returncode != 0:
        print(verifier.stdout)
        print(verifier.stderr, file=sys.stderr)
        raise SystemExit("Source Phase 4 readiness review verifier failed")

    source_records = _read_jsonl(args.phase4_readiness_review_jsonl)
    if len(source_records) != 1:
        raise SystemExit(f"Expected exactly one Phase 4 readiness review record, found {len(source_records)}")

    record = build_h024_execution_safety_controls_design(
        source_records[0],
        allowed_demo_servers=args.allowed_demo_server,
        expected_account_currency=args.expected_account_currency,
        max_risk_fraction=args.max_risk_fraction,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")

    print(f"Output execution safety-controls design JSONL: {args.output}")
    print("Design records: 1")
    print(f"Violations: {len(record.get('violations', []))}")
    for violation in record.get("violations", []):
        print(f"- {violation}")
    print(f"Design status: {record.get('design_status')}")
    print(f"Phase 4 approved: {record.get('phase4_approved')}")
    print(f"Demo order placement approved: {record.get('demo_order_placement_approved')}")
    print(f"Live order placement approved: {record.get('live_order_placement_approved')}")
    print(f"Execution approved: {record.get('execution_approved')}")
    print(f"Verdict: {record.get('verdict')}")

    return 0 if record.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())