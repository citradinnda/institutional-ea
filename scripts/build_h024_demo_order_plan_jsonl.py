"""Build H024 proposed demo-order plan JSONL from dry-run request JSONL.

Research-only boundary:
- no MetaTrader 5 import
- no broker API access
- no OrderSend / OrderCheck equivalent
- no demo or live order placement

The output is an internal review artifact, not an execution request.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from quantcore.execution.h024_demo_order_plan import (
    H024DemoAccountContext,
    H024DemoOrderPlanError,
    build_h024_demo_order_plan,
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


def build_plan_records(
    input_jsonl: Path,
    account_context: H024DemoAccountContext,
    *,
    allowed_demo_servers: Iterable[str] | None = None,
) -> tuple[list[dict[str, Any]], list[str], int]:
    plan_records: list[dict[str, Any]] = []
    violations: list[str] = []
    requests_read = 0

    try:
        rows = list(iter_jsonl_objects(input_jsonl))
    except ValueError as exc:
        return [], [str(exc)], 0

    for line_number, request in rows:
        requests_read += 1
        try:
            plan = build_h024_demo_order_plan(
                request,
                account_context,
                allowed_demo_servers=None
                if allowed_demo_servers is None
                else set(allowed_demo_servers),
            )
        except H024DemoOrderPlanError as exc:
            violations.append(f"line {line_number}: {exc}")
            continue
        plan_records.append(asdict(plan))

    return plan_records, violations, requests_read


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
        description=(
            "Build review-only H024 proposed demo-order plan JSONL from verified "
            "dry-run request JSONL."
        )
    )
    parser.add_argument("input_jsonl", type=Path)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--server", required=True)
    parser.add_argument("--account-currency", required=True)
    parser.add_argument("--account-balance", type=float, required=True)
    parser.add_argument("--account-equity", type=float, required=True)
    parser.add_argument("--broker")
    parser.add_argument("--account-login")
    parser.add_argument(
        "--allowed-demo-server",
        action="append",
        default=None,
        help=(
            "Allowed demo server. May be repeated. If omitted, the contract "
            "default allowlist is used."
        ),
    )
    parser.add_argument(
        "--require-plan",
        action="store_true",
        help="Fail unless at least one proposed plan is produced.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    context = H024DemoAccountContext(
        server=args.server,
        account_currency=args.account_currency,
        account_balance=args.account_balance,
        account_equity=args.account_equity,
        broker=args.broker,
        account_login=args.account_login,
    )

    plans, violations, requests_read = build_plan_records(
        args.input_jsonl,
        context,
        allowed_demo_servers=args.allowed_demo_server,
    )

    if args.require_plan and not plans:
        violations.append("required at least one proposed plan, found 0")

    print("H024 demo-order plan JSONL builder")
    print("=" * 72)
    print("Research only. Review-only proposed plans. No MT5 access. No orders.")
    print(f"Input: {args.input_jsonl}")
    print(f"Output: {args.output_jsonl}")
    print(f"Requests read: {requests_read}")
    print(f"Plans produced: {len(plans)}")
    print(f"Violations: {len(violations)}")

    if violations:
        print()
        print("Violations:")
        for violation in violations:
            print(f"- {violation}")
        print()
        print("Verdict: FAIL")
        return 1

    written = write_jsonl(args.output_jsonl, plans)
    print(f"Plans written: {written}")
    print()
    print("Verdict: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
