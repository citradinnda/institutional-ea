"""Verify H024 dry-run/log-only action CSV safety.

Research/preparation only.

This verifies a local dry-run action log. It does not import MT5 and cannot
place, modify, close, or delete orders.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

DEFAULT_INPUT_PATH = (
    Path(__file__).resolve().parents[1] / "reports" / "h024_dry_run_actions.csv"
)

FORBIDDEN_FIELDS: tuple[str, ...] = (
    "order_ticket",
    "position_ticket",
    "order_send_result",
    "retcode",
    "deal",
    "request_id",
)

REQUIRED_FIELDS: tuple[str, ...] = (
    "action",
    "model_symbol",
    "broker_symbol",
    "side",
    "timestamp_utc",
    "reason",
    "raw_lots",
    "normalized_lots",
    "raw_entry_price",
    "raw_stop_price",
    "raw_stop_distance",
    "notional_quote",
    "notional_usd",
    "per_trade_gross_leverage",
    "kill_switch_enabled",
    "mode",
)

WOULD_OPEN_REQUIRED_NON_EMPTY: tuple[str, ...] = (
    "model_symbol",
    "broker_symbol",
    "side",
    "timestamp_utc",
    "reason",
)

WOULD_OPEN_REQUIRED_POSITIVE_FLOATS: tuple[str, ...] = (
    "raw_lots",
    "normalized_lots",
    "raw_entry_price",
    "raw_stop_distance",
    "notional_quote",
    "notional_usd",
    "per_trade_gross_leverage",
)


@dataclass(frozen=True)
class DryRunActionLogVerification:
    row_count: int
    would_open_count: int
    no_action_count: int
    blocked_count: int
    violation_count: int
    violations: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return self.violation_count == 0


def load_action_rows(path: Path) -> tuple[dict[str, str], ...]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("dry-run action CSV has no header")

        fieldnames = tuple(reader.fieldnames)
        missing = [field for field in REQUIRED_FIELDS if field not in fieldnames]
        if missing:
            raise ValueError(f"dry-run action CSV missing required fields: {missing}")

        forbidden = [field for field in FORBIDDEN_FIELDS if field in fieldnames]
        if forbidden:
            raise ValueError(f"dry-run action CSV contains forbidden execution fields: {forbidden}")

        rows = tuple(dict(row) for row in reader)

    if not rows:
        raise ValueError("dry-run action CSV has no rows")

    return rows


def verify_action_rows(rows: Iterable[Mapping[str, str]]) -> DryRunActionLogVerification:
    row_tuple = tuple(rows)
    violations: list[str] = []
    counts = {"WOULD_OPEN": 0, "NO_ACTION": 0, "BLOCKED": 0}

    for i, row in enumerate(row_tuple, start=2):
        action = row["action"]
        if action not in counts:
            violations.append(f"line {i}: unsupported action={action!r}")
            continue

        counts[action] += 1

        if row["mode"] != "dry_run":
            violations.append(f"line {i}: mode must be dry_run, observed={row['mode']!r}")

        if action == "WOULD_OPEN":
            violations.extend(_verify_would_open_row(row=row, line_number=i))

    return DryRunActionLogVerification(
        row_count=len(row_tuple),
        would_open_count=counts["WOULD_OPEN"],
        no_action_count=counts["NO_ACTION"],
        blocked_count=counts["BLOCKED"],
        violation_count=len(violations),
        violations=tuple(violations),
    )


def format_verification_report(result: DryRunActionLogVerification) -> str:
    lines = [
        "H024 dry-run action log verification",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        f"Rows: {result.row_count}",
        f"WOULD_OPEN: {result.would_open_count}",
        f"NO_ACTION: {result.no_action_count}",
        f"BLOCKED: {result.blocked_count}",
        f"Violations: {result.violation_count}",
        "",
        f"Verdict: {'PASS' if result.passed else 'FAIL'}",
    ]

    if result.violations:
        lines.append("")
        lines.append("Violations:")
        lines.extend(f"- {violation}" for violation in result.violations)

    lines.extend(
        [
            "",
            "Safety boundary:",
            "- This verifier does not approve demo trading, live trading, or Phase 4.",
            "- This verifier only checks the local dry-run log shape and required audit fields.",
        ]
    )

    return "\n".join(lines)


def _verify_would_open_row(*, row: Mapping[str, str], line_number: int) -> list[str]:
    violations: list[str] = []

    for field in WOULD_OPEN_REQUIRED_NON_EMPTY:
        if not row[field].strip():
            violations.append(f"line {line_number}: WOULD_OPEN missing {field}")

    for field in WOULD_OPEN_REQUIRED_POSITIVE_FLOATS:
        value = _parse_float(row[field], field=field, line_number=line_number)
        if value <= 0.0:
            violations.append(f"line {line_number}: WOULD_OPEN {field} must be > 0, observed={value}")

    if row["kill_switch_enabled"].strip().lower() not in {"true", "1"}:
        violations.append(
            f"line {line_number}: WOULD_OPEN kill_switch_enabled must be true/1"
        )

    return violations


def _parse_float(value: str, *, field: str, line_number: int) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"line {line_number}: {field} must be numeric, observed={value!r}"
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to h024_dry_run_actions.csv.",
    )
    args = parser.parse_args()

    rows = load_action_rows(args.input)
    result = verify_action_rows(rows)
    print(format_verification_report(result))

    if not result.passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
