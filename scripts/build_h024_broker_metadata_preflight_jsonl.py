"""Build H024 broker metadata preflight JSONL from proposed plan JSONL.

Research-only boundary:
- no MetaTrader 5 import
- no terminal access
- no broker API access
- no order placement
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

from quantcore.execution.h024_broker_metadata_preflight import (
    H024BrokerMetadataPreflightError,
    as_preflight_record,
    build_h024_broker_metadata_preflight,
)


def iter_jsonl_objects(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"line {line_number}: invalid JSON: {exc.msg}"
                ) from exc
            if not isinstance(value, dict):
                raise ValueError(f"line {line_number}: record must be a JSON object")
            yield line_number, value


def load_metadata_by_symbol(path: Path) -> dict[str, dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid metadata JSON: {exc.msg}") from exc

    top_level_source = None
    raw_symbols: list[Any]

    if isinstance(payload, dict) and isinstance(payload.get("symbols"), list):
        top_level_source = payload.get("metadata_source")
        raw_symbols = payload["symbols"]
    elif isinstance(payload, list):
        raw_symbols = payload
    elif isinstance(payload, dict) and "symbol" in payload:
        raw_symbols = [payload]
    elif isinstance(payload, dict):
        raw_symbols = list(payload.values())
    else:
        raise ValueError("metadata JSON must be an object, list, or symbols object")

    metadata_by_symbol: dict[str, dict[str, Any]] = {}
    for index, raw_symbol in enumerate(raw_symbols, start=1):
        if not isinstance(raw_symbol, dict):
            raise ValueError(f"metadata item {index} must be an object")
        record = dict(raw_symbol)
        if top_level_source is not None and "metadata_source" not in record:
            record["metadata_source"] = top_level_source
        symbol = record.get("symbol")
        if not isinstance(symbol, str) or not symbol.strip():
            raise ValueError(f"metadata item {index} is missing symbol")
        if symbol in metadata_by_symbol:
            raise ValueError(f"duplicate metadata for symbol: {symbol}")
        metadata_by_symbol[symbol] = record

    return metadata_by_symbol


def build_preflight_records(
    plan_jsonl: Path,
    metadata_json: Path,
    *,
    allowed_demo_servers: Iterable[str] | None = None,
    max_risk_fraction: float = 0.01,
) -> tuple[list[dict[str, Any]], list[str], int]:
    try:
        metadata_by_symbol = load_metadata_by_symbol(metadata_json)
    except ValueError as exc:
        return [], [str(exc)], 0

    try:
        rows = list(iter_jsonl_objects(plan_jsonl))
    except ValueError as exc:
        return [], [str(exc)], 0

    records: list[dict[str, Any]] = []
    violations: list[str] = []
    plans_read = 0

    for line_number, plan in rows:
        plans_read += 1
        symbol = plan.get("symbol")
        metadata = metadata_by_symbol.get(symbol)
        if metadata is None:
            violations.append(f"line {line_number}: missing metadata for symbol {symbol!r}")
            continue

        try:
            preflight = build_h024_broker_metadata_preflight(
                plan,
                metadata,
                allowed_demo_servers=None
                if allowed_demo_servers is None
                else set(allowed_demo_servers),
                max_risk_fraction=max_risk_fraction,
            )
        except H024BrokerMetadataPreflightError as exc:
            violations.append(f"line {line_number}: {exc}")
            continue

        records.append(as_preflight_record(preflight))

    return records, violations, plans_read


def write_jsonl(path: Path, records: Iterable[Mapping[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
            count += 1
    return count


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build H024 review-only broker metadata preflight JSONL."
    )
    parser.add_argument("plan_jsonl", type=Path)
    parser.add_argument("--metadata-json", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--allowed-demo-server", action="append", default=None)
    parser.add_argument("--max-risk-fraction", type=float, default=0.01)
    parser.add_argument("--require-preflight", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    records, violations, plans_read = build_preflight_records(
        args.plan_jsonl,
        args.metadata_json,
        allowed_demo_servers=args.allowed_demo_server,
        max_risk_fraction=args.max_risk_fraction,
    )

    if args.require_preflight and not records:
        violations.append("required at least one preflight record, found 0")

    print("H024 broker metadata preflight JSONL builder")
    print("=" * 72)
    print("Research only. Offline metadata review. No MT5 access. No orders.")
    print(f"Plan input: {args.plan_jsonl}")
    print(f"Metadata input: {args.metadata_json}")
    print(f"Output: {args.output_jsonl}")
    print(f"Plans read: {plans_read}")
    print(f"Preflight records produced: {len(records)}")
    print(f"Violations: {len(violations)}")

    if violations:
        print()
        print("Violations:")
        for violation in violations:
            print(f"- {violation}")
        print()
        print("Verdict: FAIL")
        return 1

    written = write_jsonl(args.output_jsonl, records)
    print(f"Preflight records written: {written}")
    print()
    print("Verdict: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
