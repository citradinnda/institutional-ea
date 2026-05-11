"""Verify H024 broker metadata preflight JSONL.

This verifier checks review-only offline preflight artifacts. It rejects
execution-like fields and validates symbol, account, price, volume, and risk
constraints from the preflight record itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

PREFLIGHT_SCHEMA_VERSION = "h024_broker_metadata_preflight_v1"
PREFLIGHT_KIND = "BROKER_METADATA_PREFLIGHT_REVIEW_ONLY"
PLAN_SCHEMA_VERSION = "h024_demo_order_plan_v1"
PLAN_KIND = "PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY"

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
        "ordersend",
        "order_send",
        "ordercheck",
        "order_check",
    }
)
REQUIRED_CHECKS: frozenset[str] = frozenset(
    {
        "schema_and_plan_kind_checked",
        "demo_server_allowlisted",
        "symbol_metadata_matched",
        "price_tick_alignment_checked",
        "volume_constraints_checked",
        "metadata_loss_within_intended_risk_checked",
        "risk_fraction_cap_checked",
        "review_only_no_execution",
    }
)
REQUIRED_FIELDS: tuple[str, ...] = (
    "schema_version",
    "preflight_kind",
    "plan_schema_version",
    "plan_kind",
    "symbol",
    "normalized_symbol",
    "account_server",
    "account_currency",
    "account_balance",
    "account_equity",
    "side",
    "entry_price",
    "stop_loss",
    "volume_lots",
    "risk_usd",
    "source_timestamp",
    "source_reason",
    "metadata_source",
    "tick_size",
    "tick_value",
    "min_volume",
    "max_volume",
    "volume_step",
    "volume_digits",
    "price_digits",
    "estimated_loss_usd",
    "risk_fraction_of_balance",
    "max_risk_fraction",
    "checks",
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


def verify_preflight_record(
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

    _expect_equal(violations, line_number, record, "schema_version", PREFLIGHT_SCHEMA_VERSION)
    _expect_equal(violations, line_number, record, "preflight_kind", PREFLIGHT_KIND)
    _expect_equal(violations, line_number, record, "plan_schema_version", PLAN_SCHEMA_VERSION)
    _expect_equal(violations, line_number, record, "plan_kind", PLAN_KIND)

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

    side = _require_nonempty_str(violations, line_number, record, "side")
    if side not in {"BUY", "SELL"}:
        violations.append(f"line {line_number}: unsupported side: {side!r}")

    entry_price = _require_positive_number(violations, line_number, record, "entry_price")
    stop_loss = _require_positive_number(violations, line_number, record, "stop_loss")
    volume_lots = _require_positive_number(violations, line_number, record, "volume_lots")
    risk_usd = _require_positive_number(violations, line_number, record, "risk_usd")
    account_balance = _require_positive_number(
        violations, line_number, record, "account_balance"
    )
    _require_positive_number(violations, line_number, record, "account_equity")
    tick_size = _require_positive_number(violations, line_number, record, "tick_size")
    tick_value = _require_positive_number(violations, line_number, record, "tick_value")
    min_volume = _require_positive_number(violations, line_number, record, "min_volume")
    max_volume = _require_positive_number(violations, line_number, record, "max_volume")
    volume_step = _require_positive_number(violations, line_number, record, "volume_step")
    estimated_loss = _require_positive_number(
        violations, line_number, record, "estimated_loss_usd"
    )
    risk_fraction = _require_positive_number(
        violations, line_number, record, "risk_fraction_of_balance"
    )
    max_risk_fraction = _require_positive_number(
        violations, line_number, record, "max_risk_fraction"
    )

    volume_digits = _require_nonnegative_int(
        violations, line_number, record, "volume_digits"
    )
    _require_nonnegative_int(violations, line_number, record, "price_digits")

    _require_nonempty_str(violations, line_number, record, "source_timestamp")
    source_reason = _require_nonempty_str(
        violations, line_number, record, "source_reason"
    )
    if "WOULD_OPEN:" not in source_reason:
        violations.append(f"line {line_number}: source_reason must contain WOULD_OPEN:")
    if "mode=log_only_no_execution" not in source_reason:
        violations.append(
            f"line {line_number}: source_reason must contain mode=log_only_no_execution"
        )

    _require_nonempty_str(violations, line_number, record, "metadata_source")

    checks = record.get("checks")
    if not isinstance(checks, list) or not all(isinstance(item, str) for item in checks):
        violations.append(f"line {line_number}: checks must be a list of strings")
    elif not REQUIRED_CHECKS.issubset(set(checks)):
        violations.append(f"line {line_number}: checks is missing required checks")

    if side == "BUY" and entry_price is not None and stop_loss is not None:
        if stop_loss >= entry_price:
            violations.append(f"line {line_number}: BUY stop_loss must be below entry")
    if side == "SELL" and entry_price is not None and stop_loss is not None:
        if stop_loss <= entry_price:
            violations.append(f"line {line_number}: SELL stop_loss must be above entry")

    if (
        entry_price is not None
        and stop_loss is not None
        and volume_lots is not None
        and tick_size is not None
        and tick_value is not None
        and estimated_loss is not None
    ):
        expected_loss = abs(entry_price - stop_loss) / tick_size * tick_value * volume_lots
        if abs(expected_loss - estimated_loss) > max(1e-8, expected_loss * 1e-8):
            violations.append(f"line {line_number}: estimated_loss_usd mismatch")
        if risk_usd is not None and estimated_loss > risk_usd * 1.000001:
            violations.append(
                f"line {line_number}: estimated_loss_usd exceeds risk_usd"
            )

    if tick_size is not None and entry_price is not None:
        _check_tick_alignment(violations, line_number, entry_price, tick_size, "entry_price")
    if tick_size is not None and stop_loss is not None:
        _check_tick_alignment(violations, line_number, stop_loss, tick_size, "stop_loss")

    if (
        volume_lots is not None
        and min_volume is not None
        and max_volume is not None
        and volume_step is not None
    ):
        if max_volume < min_volume:
            violations.append(f"line {line_number}: max_volume is below min_volume")
        if volume_lots < min_volume - 1e-12:
            violations.append(f"line {line_number}: volume_lots is below min_volume")
        if volume_lots > max_volume + 1e-12:
            violations.append(f"line {line_number}: volume_lots is above max_volume")
        quotient = (volume_lots - min_volume) / volume_step
        if abs(quotient - round(quotient)) > 1e-8:
            violations.append(
                f"line {line_number}: volume_lots is not aligned to volume_step"
            )
        if volume_digits is not None and _decimal_places(volume_lots) > volume_digits:
            violations.append(
                f"line {line_number}: volume_lots exceeds volume_digits"
            )

    if (
        risk_usd is not None
        and account_balance is not None
        and risk_fraction is not None
        and max_risk_fraction is not None
    ):
        expected_fraction = risk_usd / account_balance
        if abs(expected_fraction - risk_fraction) > max(1e-12, expected_fraction * 1e-10):
            violations.append(f"line {line_number}: risk_fraction_of_balance mismatch")
        if risk_fraction > max_risk_fraction + 1e-12:
            violations.append(f"line {line_number}: risk fraction exceeds maximum")

    return violations


def verify_preflight_jsonl(
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
            verify_preflight_record(
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


def _require_nonnegative_int(
    violations: list[str],
    line_number: int,
    record: dict[str, Any],
    field: str,
) -> int | None:
    value = record.get(field)
    if isinstance(value, bool):
        violations.append(f"line {line_number}: {field} must be an integer")
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        violations.append(f"line {line_number}: {field} must be an integer")
        return None
    if number < 0:
        violations.append(f"line {line_number}: {field} must be non-negative")
        return None
    return number


def _check_tick_alignment(
    violations: list[str],
    line_number: int,
    price: float,
    tick_size: float,
    field: str,
) -> None:
    quotient = price / tick_size
    if abs(quotient - round(quotient)) > 1e-6:
        violations.append(f"line {line_number}: {field} is not aligned to tick_size")


def _decimal_places(value: float) -> int:
    rendered = f"{value:.12f}".rstrip("0").rstrip(".")
    if "." not in rendered:
        return 0
    return len(rendered.split(".", 1)[1])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify H024 broker metadata preflight JSONL."
    )
    parser.add_argument("preflight_jsonl", type=Path)
    parser.add_argument("--allowed-demo-server", action="append", default=None)
    parser.add_argument("--require-preflight", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    count, violations = verify_preflight_jsonl(
        args.preflight_jsonl,
        allowed_demo_servers=args.allowed_demo_server,
    )
    if args.require_preflight and count == 0:
        violations.append("required at least one preflight record, found 0")

    print("H024 broker metadata preflight JSONL verifier")
    print("=" * 72)
    print("Research only. Offline metadata verification. No MT5 access. No orders.")
    print(f"Input: {args.preflight_jsonl}")
    print(f"Preflight records: {count}")
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
