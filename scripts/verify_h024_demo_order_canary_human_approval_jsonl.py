from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from quantcore.execution.h024_demo_order_canary_human_approval import (
    validate_demo_order_canary_human_approval,
)


def _read_jsonl_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} is not a JSON object")
            records.append(value)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl_path")
    parser.add_argument("--allowed-demo-server", required=True)
    parser.add_argument("--expected-runtime-symbol", default="XAUUSDm")
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()

    records = _read_jsonl_records(Path(args.jsonl_path))
    violations: list[str] = []
    if len(records) != 1:
        violations.append(f"expected_exactly_one_record_found_{len(records)}")
    for index, record in enumerate(records):
        for violation in validate_demo_order_canary_human_approval(
            record,
            allowed_demo_server=args.allowed_demo_server,
            expected_runtime_symbol=args.expected_runtime_symbol,
            require_approved=args.require_approved,
        ):
            violations.append(f"record_{index}:{violation}")

    print(f"H024 demo-order canary human approval records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    verdict = "PASS" if not violations else "FAIL"
    print(f"Verdict: {verdict}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())