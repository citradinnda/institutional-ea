"""Audit MT5 order-behavior facts before any H024 execution work.

Research-only audit.

This is not:
- demo approval,
- live approval,
- Phase 4 approval,
- EA execution approval.

Expected input:

    reports/h024_mt5_order_behavior.csv

The CSV is intended to be exported from the user's Exness MT5 terminal/account.
It must contain one row per broker symbol, currently USDJPYm and XAUUSDm.

Required columns:

    symbol
    trade_mode
    execution_mode
    order_filling_modes
    order_modes
    volume_min
    volume_max
    volume_step
    stops_level_points
    freeze_level_points
    point
    digits
    spread_float

This audit checks static execution constraints only. It does not place orders.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

DEFAULT_INPUT_PATH = (
    Path(__file__).resolve().parents[1] / "reports" / "h024_mt5_order_behavior.csv"
)

EXPECTED_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")
REQUIRED_COLUMNS: tuple[str, ...] = (
    "symbol",
    "trade_mode",
    "execution_mode",
    "order_filling_modes",
    "order_modes",
    "volume_min",
    "volume_max",
    "volume_step",
    "stops_level_points",
    "freeze_level_points",
    "point",
    "digits",
    "spread_float",
)

EXPECTED_POINT_BY_SYMBOL: Mapping[str, float] = {
    "USDJPY": 0.001,
    "XAUUSD": 0.001,
}
EXPECTED_DIGITS_BY_SYMBOL: Mapping[str, int] = {
    "USDJPY": 3,
    "XAUUSD": 3,
}
EXPECTED_VOLUME_STEP_BY_SYMBOL: Mapping[str, float] = {
    "USDJPY": 0.01,
    "XAUUSD": 0.01,
}
MAXIMUM_EXPECTED_VOLUME_MIN_BY_SYMBOL: Mapping[str, float] = {
    "USDJPY": 0.01,
    "XAUUSD": 0.01,
}


@dataclass(frozen=True)
class OrderBehaviorCheck:
    symbol: str
    field: str
    expected: str
    observed: str
    status: str


@dataclass(frozen=True)
class OrderBehaviorAudit:
    checks: tuple[OrderBehaviorCheck, ...]
    mismatch_count: int

    @property
    def passed(self) -> bool:
        return self.mismatch_count == 0


def normalize_symbol(symbol: str) -> str:
    """Normalize observed Exness suffixes to model symbols."""

    value = symbol.strip().upper()
    if value.endswith("M"):
        value = value[:-1]
    return value


def load_order_behavior_rows(path: Path) -> tuple[dict[str, str], ...]:
    """Load order-behavior CSV rows."""

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("order behavior CSV has no header")

        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"order behavior CSV missing required columns: {missing}")

        rows = tuple(dict(row) for row in reader)

    if not rows:
        raise ValueError("order behavior CSV has no rows")

    return rows


def audit_order_behavior_rows(rows: Iterable[Mapping[str, str]]) -> OrderBehaviorAudit:
    """Audit normalized symbol rows against minimum execution-readiness facts."""

    by_symbol: dict[str, Mapping[str, str]] = {}
    checks: list[OrderBehaviorCheck] = []

    for row in rows:
        normalized = normalize_symbol(str(row["symbol"]))
        if normalized in by_symbol:
            checks.append(
                OrderBehaviorCheck(
                    symbol=normalized,
                    field="symbol",
                    expected="one row per normalized symbol",
                    observed="duplicate row",
                    status="mismatch",
                )
            )
            continue
        by_symbol[normalized] = row

    for symbol in EXPECTED_SYMBOLS:
        row = by_symbol.get(symbol)
        if row is None:
            checks.append(
                OrderBehaviorCheck(
                    symbol=symbol,
                    field="symbol",
                    expected="present",
                    observed="missing",
                    status="mismatch",
                )
            )
            continue

        checks.extend(_audit_symbol_row(symbol=symbol, row=row))

    mismatch_count = sum(1 for check in checks if check.status != "ok")
    return OrderBehaviorAudit(checks=tuple(checks), mismatch_count=mismatch_count)


def format_order_behavior_audit(audit: OrderBehaviorAudit) -> str:
    """Format an order-behavior audit report."""

    lines = [
        "H024 MT5 order behavior audit",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        "symbol | field | expected | observed | status",
    ]

    for check in audit.checks:
        lines.append(
            " | ".join(
                [
                    check.symbol,
                    check.field,
                    check.expected,
                    check.observed,
                    check.status,
                ]
            )
        )

    lines.extend(
        [
            "",
            f"Mismatch count: {audit.mismatch_count}",
            "",
            f"Verdict: {'PASS' if audit.passed else 'FAIL'}",
            "",
            "Interpretation:",
            "- PASS means these static MT5 order-behavior facts are reconciled.",
            "- FAIL blocks dry-run/log-only EA work until reconciled.",
            "- PASS does not approve demo trading, live trading, Phase 4, or EA execution.",
        ]
    )

    return "\n".join(lines)


def _audit_symbol_row(*, symbol: str, row: Mapping[str, str]) -> tuple[OrderBehaviorCheck, ...]:
    return (
        _check_text_set(
            symbol=symbol,
            field="trade_mode",
            observed=row["trade_mode"],
            allowed={"4", "FULL", "SYMBOL_TRADE_MODE_FULL"},
            expected="FULL / SYMBOL_TRADE_MODE_FULL / 4",
        ),
        _check_non_empty(symbol=symbol, field="execution_mode", observed=row["execution_mode"]),
        _check_non_empty(
            symbol=symbol,
            field="order_filling_modes",
            observed=row["order_filling_modes"],
        ),
        _check_non_empty(symbol=symbol, field="order_modes", observed=row["order_modes"]),
        _check_float_at_most(
            symbol=symbol,
            field="volume_min",
            observed=row["volume_min"],
            threshold=MAXIMUM_EXPECTED_VOLUME_MIN_BY_SYMBOL[symbol],
        ),
        _check_float_at_least(
            symbol=symbol,
            field="volume_max",
            observed=row["volume_max"],
            threshold=MAXIMUM_EXPECTED_VOLUME_MIN_BY_SYMBOL[symbol],
        ),
        _check_float_equal(
            symbol=symbol,
            field="volume_step",
            observed=row["volume_step"],
            expected=EXPECTED_VOLUME_STEP_BY_SYMBOL[symbol],
        ),
        _check_float_at_least(
            symbol=symbol,
            field="stops_level_points",
            observed=row["stops_level_points"],
            threshold=0.0,
        ),
        _check_float_at_least(
            symbol=symbol,
            field="freeze_level_points",
            observed=row["freeze_level_points"],
            threshold=0.0,
        ),
        _check_float_equal(
            symbol=symbol,
            field="point",
            observed=row["point"],
            expected=EXPECTED_POINT_BY_SYMBOL[symbol],
        ),
        _check_int_equal(
            symbol=symbol,
            field="digits",
            observed=row["digits"],
            expected=EXPECTED_DIGITS_BY_SYMBOL[symbol],
        ),
        _check_text_set(
            symbol=symbol,
            field="spread_float",
            observed=row["spread_float"],
            allowed={"TRUE", "FALSE", "0", "1"},
            expected="true/false/0/1",
        ),
    )


def _check_non_empty(*, symbol: str, field: str, observed: str) -> OrderBehaviorCheck:
    value = observed.strip()
    return OrderBehaviorCheck(
        symbol=symbol,
        field=field,
        expected="non-empty",
        observed=value,
        status="ok" if value else "mismatch",
    )


def _check_text_set(
    *,
    symbol: str,
    field: str,
    observed: str,
    allowed: set[str],
    expected: str,
) -> OrderBehaviorCheck:
    value = observed.strip().upper()
    return OrderBehaviorCheck(
        symbol=symbol,
        field=field,
        expected=expected,
        observed=observed.strip(),
        status="ok" if value in allowed else "mismatch",
    )


def _check_float_equal(
    *,
    symbol: str,
    field: str,
    observed: str,
    expected: float,
) -> OrderBehaviorCheck:
    value = _parse_float(field=field, observed=observed)
    return OrderBehaviorCheck(
        symbol=symbol,
        field=field,
        expected=f"{expected:.10g}",
        observed=f"{value:.10g}",
        status="ok" if abs(value - expected) <= 1e-12 else "mismatch",
    )


def _check_float_at_most(
    *,
    symbol: str,
    field: str,
    observed: str,
    threshold: float,
) -> OrderBehaviorCheck:
    value = _parse_float(field=field, observed=observed)
    return OrderBehaviorCheck(
        symbol=symbol,
        field=field,
        expected=f"<= {threshold:.10g}",
        observed=f"{value:.10g}",
        status="ok" if value <= threshold else "mismatch",
    )


def _check_float_at_least(
    *,
    symbol: str,
    field: str,
    observed: str,
    threshold: float,
) -> OrderBehaviorCheck:
    value = _parse_float(field=field, observed=observed)
    return OrderBehaviorCheck(
        symbol=symbol,
        field=field,
        expected=f">= {threshold:.10g}",
        observed=f"{value:.10g}",
        status="ok" if value >= threshold else "mismatch",
    )


def _check_int_equal(
    *,
    symbol: str,
    field: str,
    observed: str,
    expected: int,
) -> OrderBehaviorCheck:
    value = _parse_int(field=field, observed=observed)
    return OrderBehaviorCheck(
        symbol=symbol,
        field=field,
        expected=str(expected),
        observed=str(value),
        status="ok" if value == expected else "mismatch",
    )


def _parse_float(*, field: str, observed: str) -> float:
    try:
        return float(observed)
    except ValueError as exc:
        raise ValueError(f"{field} must be numeric, observed={observed!r}") from exc


def _parse_int(*, field: str, observed: str) -> int:
    try:
        return int(observed)
    except ValueError as exc:
        raise ValueError(f"{field} must be an integer, observed={observed!r}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to MT5 order behavior CSV export.",
    )
    args = parser.parse_args()

    rows = load_order_behavior_rows(args.input)
    audit = audit_order_behavior_rows(rows)
    print(format_order_behavior_audit(audit))

    if not audit.passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
