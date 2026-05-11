"""Verify H024 proposed demo-order plan JSONL.

Research-only verifier for internal review artifacts. This verifies that the
plan JSONL remains a proposed plan and does not contain execution result fields.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

PLAN_SCHEMA_VERSION = "h024_demo_order_plan_v1"
PLAN_KIND = "PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY"
SOURCE_SCHEMA_VERSION = "h024_intended_action_log_v1"
SOURCE_REQUEST_KIND = "DRY_RUN_MARKET_OPEN"

DEFAULT_DEMO_SERVER_ALLOWLIST: frozenset[str] = frozenset({"Exness-MT5Trial6"})
LIVE_LIKE_SERVER_MARKERS: tuple[str, ...] = ("live", "real", "prod", "production")
ALLOWED_NORMALIZED_SYMBOLS: frozenset[str] = frozenset({"USDJPY", "XAUUSD"})
SYMBOL_NORMALIZATION: dict[str, str] = {
    "USDJPY": "USDJPY",
    "USDJPYm": "USDJPY",
    "USDJPYc": "USDJPY",
    "XAUUSD": "XAUUSD",
    "XAUUSDm": "XAUUSD",
    "XAUUSDc": "XAUUSD",
}
FORBIDDEN_EXECUTION_KEYS: frozenset[str] = frozenset(
    {
        "order",
        "order_id",
        "ticket",
        "position",
        "position_id",
        "deal",
        "deal_id",
        "mt5_request",
        "mql_trade_request",
        "broker_request",
        "execution_result",
        "retcode",
        "retcode_external",
    }
)

REQUIRED_FIELDS: tuple[str, ...] = (
    "schema_version",
    "plan_kind",
    "source_schema_version",
    "source_request_kind",
    "symbol",
    "normalized_symbol",
    "timeframe",
    "side",
    "entry_price",
    "stop_loss",
    "volume_lots",
    "risk_usd",
    "source_timestamp",
    "source_reason",
    "account_server",
    "account_currency",
    "account_balance",
    "account_equity",
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
                yield line_number, {"__json_error__": exc.msg}
                continue
            if not isinstance(value, dict):
                yield line_number, {"__type_error__": "record must be a JSON object"}
                continue
            yield line_number, value


def verify_plan_record(
    record: dict[str, Any],
    *,
    line_number: int,
    allowed_demo_servers: frozenset[str],
) -> list[str]:
    violations: list[str] = []

    if "__json_error__" in record:
        return [f"line {line_number}: invalid JSON: {record['__json_error__']}"]
    if "__type_error__" in record:
        return [f"line {line_number}: {record['__type_error__']}"]

    for key in record:
        if key.lower() in FORBIDDEN_EXECUTION_KEYS:
            violations.append(
                f"line {line_number}: execution-like key is forbidden: {key}"
            )

    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        violations.append(f"line {line_number}: missing fields: {', '.join(missing)}")
        return violations

    _expect_equal(
        violations,
        line_number,
        record,
        "schema_version",
        PLAN_SCHEMA_VERSION,
    )
    _expect_equal(violations, line_number, record, "plan_kind", PLAN_KIND)
    _expect_equal(
        violations,
        line_number,
        record,
        "source_schema_version",
        SOURCE_SCHEMA_VERSION,
    )
    _expect_equal(
        violations,
        line_number,
        record,
        "source_request_kind",
        SOURCE_REQUEST_KIND,
    )

    symbol = _require_nonempty_str(violations, line_number, record, "symbol")
    normalized_symbol = _require_nonempty_str(
        violations, line_number, record, "normalized_symbol"
    )
    expected_normalized = SYMBOL_NORMALIZATION.get(symbol)
    if expected_normalized is None:
        violations.append(f"line {line_number}: unsupported symbol: {symbol!r}")
    elif normalized_symbol != expected_normalized:
        violations.append(
            f"line {line_number}: normalized_symbol does not match symbol"
        )
    if normalized_symbol not in ALLOWED_NORMALIZED_SYMBOLS:
        violations.append(
            f"line {line_number}: unsupported normalized_symbol: {normalized_symbol!r}"
        )

    timeframe = _require_nonempty_str(violations, line_number, record, "timeframe")
    if timeframe != "H4":
        violations.append(f"line {line_number}: unsupported timeframe: {timeframe!r}")

    side = _require_nonempty_str(violations, line_number, record, "side")
    if side not in {"BUY", "SELL"}:
        violations.append(f"line {line_number}: unsupported side: {side!r}")

    entry_price = _require_positive_number(violations, line_number, record, "entry_price")
    stop_loss = _require_positive_number(violations, line_number, record, "stop_loss")
    _require_positive_number(violations, line_number, record, "volume_lots")
    _require_positive_number(violations, line_number, record, "risk_usd")

    if side == "BUY" and entry_price is not None and stop_loss is not None:
        if stop_loss >= entry_price:
            violations.append(f"line {line_number}: BUY stop_loss must be below entry")
    if side == "SELL" and entry_price is not None and stop_loss is not None:
        if stop_loss <= entry_price:
            violations.append(f"line {line_number}: SELL stop_loss must be above entry")

    source_timestamp = _require_nonempty_str(
        violations, line_number, record, "source_timestamp"
    )
    if source_timestamp and len(source_timestamp) < 10:
        violations.append(f"line {line_number}: source_timestamp is too short")

    source_reason = _require_nonempty_str(
        violations, line_number, record, "source_reason"
    )
    if "WOULD_OPEN:" not in source_reason:
        violations.append(f"line {line_number}: source_reason must contain WOULD_OPEN:")
    if "mode=log_only_no_execution" not in source_reason:
        violations.append(
            f"line {line_number}: source_reason must contain mode=log_only_no_execution"
        )

    account_server = _require_nonempty_str(
        violations, line_number, record, "account_server"
    )
    lowered_server = account_server.lower()
    if any(marker in lowered_server for marker in LIVE_LIKE_SERVER_MARKERS):
        violations.append(f"line {line_number}: live-like account_server is rejected")
    if account_server not in allowed_demo_servers:
        violations.append(
            f"line {line_number}: account_server is not in demo allowlist: "
            f"{account_server!r}"
        )

    account_currency = _require_nonempty_str(
        violations, line_number, record, "account_currency"
    )
    if account_currency != "USD":
        violations.append(
            f"line {line_number}: unsupported account_currency: {account_currency!r}"
        )

    _require_positive_number(violations, line_number, record, "account_balance")
    _require_positive_number(violations, line_number, record, "account_equity")

    return violations


def verify_plan_jsonl(
    path: Path,
    *,
    allowed_demo_servers: Iterable[str] | None = None,
) -> tuple[int, list[str]]:
    allowlist = (
        DEFAULT_DEMO_SERVER_ALLOWLIST
        if allowed_demo_servers is None
        else frozenset(allowed_demo_servers)
    )
    if not allowlist:
        return 0, ["allowed demo server list must be non-empty"]

    rows = list(iter_jsonl_objects(path))
    violations: list[str] = []
    for line_number, record in rows:
        violations.extend(
            verify_plan_record(
                record,
                line_number=line_number,
                allowed_demo_servers=allowlist,
            )
        )
    return len(rows), violations


def _expect_equal(
    violations: list[str],
    line_number: int,
    record: dict[str, Any],
    field: str,
    expected: str,
) -> None:
    actual = record.get(field)
    if actual != expected:
        violations.append(
            f"line {line_number}: {field} must be {expected!r}, got {actual!r}"
        )


def _require_nonempty_str(
    violations: list[str],
    line_number: int,
    record: dict[str, Any],
    field: str,
) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        violations.append(f"line {line_number}: {field} must be a non-empty string")
        return ""
    return value.strip()


def _require_positive_number(
    violations: list[str],
    line_number: int,
    record: dict[str, Any],
    field: str,
) -> float | None:
    value = record.get(field)
    try:
        number = float(value)
    except (TypeError, ValueError):
        violations.append(f"line {line_number}: {field} must be numeric")
        return None
    if number <= 0:
        violations.append(f"line {line_number}: {field} must be positive")
        return None
    return number


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify H024 review-only proposed demo-order plan JSONL."
    )
    parser.add_argument("plan_jsonl", type=Path)
    parser.add_argument(
        "--allowed-demo-server",
        action="append",
        default=None,
        help=(
            "Allowed demo server. May be repeated. If omitted, the verifier "
            "default allowlist is used."
        ),
    )
    parser.add_argument(
        "--require-plan",
        action="store_true",
        help="Fail unless at least one proposed plan is present.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    count, violations = verify_plan_jsonl(
        args.plan_jsonl,
        allowed_demo_servers=args.allowed_demo_server,
    )
    if args.require_plan and count == 0:
        violations.append("required at least one proposed plan, found 0")

    print("H024 demo-order plan JSONL verifier")
    print("=" * 72)
    print("Research only. Proposed-plan verification. No MT5 access. No orders.")
    print(f"Input: {args.plan_jsonl}")
    print(f"Plans: {count}")
    print(f"Violations: {len(violations)}")

    if violations:
        print()
        print("Violations:")
        for violation in violations:
            print(f"- {violation}")
        print()
        print("Verdict: FAIL")
        return 1

    print()
    print("Verdict: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
