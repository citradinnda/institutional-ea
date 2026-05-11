from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from quantcore.execution.h024_order_intent_simulation import build_h024_order_intent_simulation


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


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build H024 review-only order-intent simulation JSONL from broker metadata preflight JSONL."
    )
    parser.add_argument("input_preflight_jsonl", type=Path)
    parser.add_argument("output_order_intent_simulation_jsonl", type=Path)
    parser.add_argument("--allowed-demo-server", action="append", required=True)
    parser.add_argument("--expected-account-currency", default="USD")
    parser.add_argument("--max-risk-fraction", default="0.01")
    args = parser.parse_args()

    preflight_records = _read_jsonl(args.input_preflight_jsonl)
    intent_records = [
        build_h024_order_intent_simulation(
            record,
            allowed_demo_servers=args.allowed_demo_server,
            expected_account_currency=args.expected_account_currency,
            max_risk_fraction=args.max_risk_fraction,
        )
        for record in preflight_records
    ]

    _write_jsonl(args.output_order_intent_simulation_jsonl, intent_records)

    violation_count = sum(len(record.get("violations", [])) for record in intent_records)
    verdict = "PASS" if preflight_records and violation_count == 0 else "FAIL"

    print(f"Input preflight JSONL: {args.input_preflight_jsonl}")
    print(f"Output order-intent simulation JSONL: {args.output_order_intent_simulation_jsonl}")
    print(f"Preflight records read: {len(preflight_records)}")
    print(f"Order-intent simulation records produced: {len(intent_records)}")
    print(f"Violations: {violation_count}")
    if violation_count:
        for index, record in enumerate(intent_records, start=1):
            for violation in record.get("violations", []):
                print(f"- record_{index}:{violation}")
    print(f"Verdict: {verdict}")

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())