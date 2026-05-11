from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from quantcore.execution.h024_demo_order_canary_readiness_human_decision import (
    build_demo_order_canary_readiness_human_decision,
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


def _read_single_record(path: Path) -> dict[str, Any]:
    records = _read_jsonl_records(path)
    if len(records) != 1:
        raise ValueError(f"expected exactly one JSONL record in {path}, found {len(records)}")
    return records[0]


def _write_jsonl_record(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo-order-readiness-packet", default="reports/h024_standard_demo_demo_order_readiness_packet.jsonl")
    parser.add_argument("--output", default="reports/h024_standard_demo_demo_order_canary_readiness_human_decision.jsonl")
    parser.add_argument("--allowed-demo-server", required=True)
    parser.add_argument("--reviewer", default="human")
    args = parser.parse_args()

    readiness_packet = _read_single_record(Path(args.demo_order_readiness_packet))
    record = build_demo_order_canary_readiness_human_decision(
        demo_order_readiness_packet=readiness_packet,
        allowed_demo_server=args.allowed_demo_server,
        reviewer=args.reviewer,
    )
    _write_jsonl_record(Path(args.output), record)
    print(f"Wrote H024 demo-order canary readiness human decision: {args.output}")
    print(f"Verdict: {record.get('verdict')}")
    print(f"Violations: {len(record.get('violations') or [])}")
    return 0 if record.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())