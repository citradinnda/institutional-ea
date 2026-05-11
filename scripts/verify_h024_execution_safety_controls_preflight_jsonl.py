from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from quantcore.execution.h024_execution_safety_controls import (
    verify_h024_execution_safety_controls_preflight_record,
)


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
    parser = argparse.ArgumentParser(description="Verify H024 execution safety-controls preflight JSONL.")
    parser.add_argument("execution_safety_controls_preflight_jsonl", type=Path)
    parser.add_argument("--allowed-demo-server", action="append", required=True)
    parser.add_argument("--expected-account-currency", default="USD")
    parser.add_argument("--max-risk-fraction", default="0.01")
    parser.add_argument("--require-preflight", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args()

    records = _read_jsonl(args.execution_safety_controls_preflight_jsonl)

    violations: list[str] = []
    if args.require_preflight and len(records) != 1:
        violations.append(f"expected_exactly_one_execution_safety_controls_preflight_record:{len(records)}")

    for index, record in enumerate(records, start=1):
        record_violations = verify_h024_execution_safety_controls_preflight_record(
            record,
            allowed_demo_servers=args.allowed_demo_server,
            expected_account_currency=args.expected_account_currency,
            max_risk_fraction=args.max_risk_fraction,
        )
        violations.extend(f"record_{index}:{violation}" for violation in record_violations)
        if args.require_blocked and record.get("control_decision") != "BLOCK":
            violations.append(f"record_{index}:expected_block_decision:{record.get('control_decision')}")

    verdict = "PASS" if not violations else "FAIL"

    print(f"Input execution safety-controls preflight JSONL: {args.execution_safety_controls_preflight_jsonl}")
    print(f"Preflight records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    print(f"Verdict: {verdict}")

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())