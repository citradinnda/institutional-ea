"""Summarize H024 EA intended-action rows from a log-only preflight CSV.

Research only. No demo/live/Phase 4 approval.
This script reads collected CSVs only. It does not touch MT5.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path


EXPECTED_SYMBOLS = ("USDJPYm", "XAUUSDm")
EXPECTED_NORMALIZED_SYMBOLS = {
    "USDJPYm": "USDJPY",
    "XAUUSDm": "XAUUSD",
}
EXPECTED_EVENTS = {"H024_INTENDED_ACTION_HEADER", "H024_INTENDED_ACTION_ROW"}
EXPECTED_SCHEMA_VERSION = "h024_intended_action_log_v1"
EXPECTED_DECISIONS = {"WOULD_OPEN", "BLOCKED", "NO_ACTION"}
EXPECTED_WOULD_OPEN_DIRECTIONS = {"long", "short"}

INTENDED_ACTION_ROW_FIELDS = [
    "schema_version",
    "ea_version",
    "symbol",
    "normalized_symbol",
    "timeframe",
    "decision",
    "direction",
    "entry_price",
    "stop_price",
    "stop_distance_price",
    "tick_size",
    "tick_value_usd_per_lot",
    "account_balance_usd",
    "risk_fraction",
    "risk_usd",
    "raw_lots",
    "lots",
    "min_volume",
    "max_volume",
    "volume_step",
    "volume_digits",
    "reason",
]

NUMERIC_FIELDS = [
    "entry_price",
    "stop_price",
    "stop_distance_price",
    "tick_size",
    "tick_value_usd_per_lot",
    "account_balance_usd",
    "risk_fraction",
    "risk_usd",
    "raw_lots",
    "lots",
    "min_volume",
    "max_volume",
    "volume_step",
]


def _extra_fields(row: dict[str, str]) -> list[str]:
    extra = row.get(None)  # type: ignore[arg-type]
    if extra is None:
        return []
    return [str(value) for value in extra]


def _is_finite_number(value: str) -> bool:
    try:
        parsed = float(value)
    except ValueError:
        return False
    return math.isfinite(parsed)


def summarize_runtime_csv(path: Path, *, require_would_open: bool = False) -> tuple[list[str], list[str]]:
    violations: list[str] = []
    lines: list[str] = []

    if not path.exists():
        return [], [f"missing CSV: {path}"]

    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return [], ["CSV has no data rows"]

    intended_rows = [row for row in rows if row.get("event") in EXPECTED_EVENTS]
    header_rows = [row for row in intended_rows if row.get("event") == "H024_INTENDED_ACTION_HEADER"]
    action_rows = [row for row in intended_rows if row.get("event") == "H024_INTENDED_ACTION_ROW"]

    if not header_rows:
        violations.append("missing H024_INTENDED_ACTION_HEADER row")
    if not action_rows:
        violations.append("missing H024_INTENDED_ACTION_ROW rows")

    header_symbols = Counter(row.get("symbol", "") for row in header_rows)
    action_symbols = Counter(row.get("symbol", "") for row in action_rows)

    decisions_by_symbol: dict[str, Counter[str]] = defaultdict(Counter)
    normalized_by_symbol: dict[str, set[str]] = defaultdict(set)
    total_would_open = 0

    for row_number, row in enumerate(rows, start=2):
        if row.get("event") != "H024_INTENDED_ACTION_ROW":
            continue

        payload = _extra_fields(row)
        if len(payload) != len(INTENDED_ACTION_ROW_FIELDS):
            violations.append(
                f"row {row_number}: expected {len(INTENDED_ACTION_ROW_FIELDS)} intended-action payload fields, "
                f"got {len(payload)}"
            )
            continue

        fields = dict(zip(INTENDED_ACTION_ROW_FIELDS, payload))
        symbol = fields.get("symbol", "")
        decision = fields.get("decision", "")
        normalized_symbol = fields.get("normalized_symbol", "")

        decisions_by_symbol[symbol][decision] += 1
        normalized_by_symbol[symbol].add(normalized_symbol)

        if decision == "WOULD_OPEN":
            total_would_open += 1

        if fields.get("schema_version") != EXPECTED_SCHEMA_VERSION:
            violations.append(f"row {row_number}: bad schema_version {fields.get('schema_version')!r}")
        if fields.get("timeframe") != "H4":
            violations.append(f"row {row_number}: bad timeframe {fields.get('timeframe')!r}")
        if symbol != row.get("symbol"):
            violations.append(f"row {row_number}: payload symbol does not match base symbol")
        if symbol in EXPECTED_NORMALIZED_SYMBOLS and normalized_symbol != EXPECTED_NORMALIZED_SYMBOLS[symbol]:
            violations.append(
                f"row {row_number}: expected normalized_symbol {EXPECTED_NORMALIZED_SYMBOLS[symbol]!r}, "
                f"got {normalized_symbol!r}"
            )
        if decision not in EXPECTED_DECISIONS:
            violations.append(f"row {row_number}: bad decision {decision!r}")
        if decision == "WOULD_OPEN" and fields.get("direction") not in EXPECTED_WOULD_OPEN_DIRECTIONS:
            violations.append(f"row {row_number}: WOULD_OPEN requires long or short direction")
        if not fields.get("reason", "").strip():
            violations.append(f"row {row_number}: reason is empty")

        for numeric_field in NUMERIC_FIELDS:
            if not _is_finite_number(fields.get(numeric_field, "")):
                violations.append(f"row {row_number}: bad numeric field {numeric_field}={fields.get(numeric_field)!r}")

        try:
            int(fields.get("volume_digits", ""))
        except ValueError:
            violations.append(f"row {row_number}: bad integer field volume_digits={fields.get('volume_digits')!r}")

    for symbol in EXPECTED_SYMBOLS:
        if header_symbols[symbol] < 1:
            violations.append(f"missing intended-action header for {symbol}")
        if action_symbols[symbol] < 1:
            violations.append(f"missing intended-action rows for {symbol}")

    if require_would_open and total_would_open < 1:
        violations.append("missing required runtime WOULD_OPEN intended-action row")

    lines.append("H024 intended-action runtime summary")
    lines.append("=" * 72)
    lines.append("Research only. No demo/live/Phase 4 approval.")
    lines.append("")
    lines.append(f"CSV: {path}")
    lines.append(f"Total rows: {len(rows)}")
    lines.append(f"Intended-action header rows: {len(header_rows)}")
    lines.append(f"Intended-action data rows: {len(action_rows)}")
    if require_would_open:
        lines.append("Required WOULD_OPEN rows: at least 1")
        lines.append(f"Observed WOULD_OPEN rows: {total_would_open}")
    lines.append("")

    for symbol in EXPECTED_SYMBOLS:
        lines.append(f"{symbol}:")
        lines.append(f"  headers: {header_symbols[symbol]}")
        lines.append(f"  rows: {action_symbols[symbol]}")
        normalized = ", ".join(sorted(normalized_by_symbol.get(symbol, set()))) or "none"
        lines.append(f"  normalized: {normalized}")
        for decision in ("WOULD_OPEN", "BLOCKED", "NO_ACTION"):
            lines.append(f"  {decision}: {decisions_by_symbol[symbol][decision]}")
        lines.append("")

    if violations:
        lines.append("Verdict: FAIL")
    else:
        lines.append("Verdict: PASS")

    return lines, violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--require-would-open",
        action="store_true",
        help="Fail unless at least one valid runtime WOULD_OPEN intended-action row is present.",
    )
    args = parser.parse_args(argv)

    lines, violations = summarize_runtime_csv(args.csv_path, require_would_open=args.require_would_open)
    for line in lines:
        print(line)

    if violations:
        print("")
        print("Violations:")
        for violation in violations:
            print(f"- {violation}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())