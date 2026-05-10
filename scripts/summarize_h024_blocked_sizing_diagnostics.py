from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Iterable


def _norm(value: object) -> str:
    return str(value).strip().lower()


def _find_col(header: list[str], *names: str, required: bool = True) -> int | None:
    lookup = {_norm(name): i for i, name in enumerate(header)}
    for name in names:
        key = _norm(name)
        if key in lookup:
            return lookup[key]
    if required:
        raise ValueError(f"missing expected column {names}; available={header}")
    return None


def _is_intended_action_header(row: list[str]) -> bool:
    lowered = {_norm(c) for c in row}
    return (
        "decision" in lowered
        and "entry_price" in lowered
        and ("stop_price" in lowered or "stop_loss" in lowered)
        and ("raw_lots" in lowered or "raw_volume_lots" in lowered)
        and ("lots" in lowered or "volume_lots" in lowered)
    )


def _as_float(value: object) -> float:
    try:
        return float(str(value).strip())
    except Exception:
        return float("nan")


def iter_intended_action_records(csv_path: Path) -> tuple[list[dict[str, str]], Counter[int], int]:
    with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
        physical_rows = list(csv.reader(handle))

    row_length_histogram: Counter[int] = Counter(len(row) for row in physical_rows)
    current_header: list[str] | None = None
    header_count = 0
    records: list[dict[str, str]] = []

    for row in physical_rows:
        if _is_intended_action_header(row):
            current_header = row
            header_count += 1
            continue

        if current_header is None:
            continue

        if len(row) != len(current_header):
            continue

        decision_i = _find_col(current_header, "decision")
        decision = str(row[decision_i]).strip().upper()
        if decision.startswith(("WOULD_OPEN", "BLOCKED", "NO_ACTION")):
            records.append(dict(zip(current_header, row)))

    return records, row_length_histogram, header_count


def validate_blocked_sizing_diagnostics(records: Iterable[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    blocked = [
        row for row in records
        if str(row.get("decision", "")).strip().upper().startswith("BLOCKED")
    ]

    violations: list[str] = []

    if not blocked:
        return blocked, ["no BLOCKED intended-action rows found"]

    for idx, row in enumerate(blocked, start=1):
        symbol = row.get("symbol", "<unknown>")
        label = f"blocked_row={idx} symbol={symbol}"

        entry = _as_float(row.get("entry_price"))
        stop = _as_float(row.get("stop_price", row.get("stop_loss")))
        stop_distance = _as_float(row.get("stop_distance_price", row.get("stop_distance")))
        raw_lots = _as_float(row.get("raw_lots", row.get("raw_volume_lots")))
        lots = _as_float(row.get("lots", row.get("volume_lots")))
        min_volume_raw = row.get("min_volume", row.get("volume_min"))
        min_volume = _as_float(min_volume_raw) if min_volume_raw not in (None, "") else None
        reason = row.get("reason", row.get("source_reason", row.get("decision", "")))

        if not entry > 0:
            violations.append(f"{label}: entry_price not positive: {entry}")
        if not stop > 0:
            violations.append(f"{label}: stop_price not positive: {stop}")
        if not stop_distance > 0:
            violations.append(f"{label}: stop_distance_price not positive: {stop_distance}")
        if not raw_lots > 0:
            violations.append(f"{label}: raw_lots not positive: {raw_lots}")
        if lots != 0:
            violations.append(f"{label}: final lots should be 0 for BLOCKED row: {lots}")
        if min_volume is not None and not raw_lots < min_volume:
            violations.append(f"{label}: raw_lots should be below min_volume: raw={raw_lots} min={min_volume}")
        if "volume_below_min_for_would_open" not in str(reason):
            violations.append(f"{label}: reason should contain volume_below_min_for_would_open: {reason}")

    return blocked, violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify H024 BLOCKED runtime rows preserve positive sizing diagnostics without becoming executable."
    )
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    records, row_lengths, header_count = iter_intended_action_records(args.csv_path)
    blocked, violations = validate_blocked_sizing_diagnostics(records)

    print("H024 blocked sizing diagnostics verification")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print()
    print(f"CSV: {args.csv_path}")
    print(f"Row length histogram: {dict(sorted(row_lengths.items()))}")
    print(f"Intended-action header rows found: {header_count}")
    print(f"Intended-action data rows found: {len(records)}")
    print(f"BLOCKED rows checked: {len(blocked)}")
    print()

    shown = set()
    for row in blocked:
        key = (
            row.get("symbol"),
            row.get("normalized_symbol"),
            row.get("decision"),
            row.get("entry_price"),
            row.get("stop_price", row.get("stop_loss")),
            row.get("stop_distance_price", row.get("stop_distance")),
            row.get("raw_lots", row.get("raw_volume_lots")),
            row.get("lots", row.get("volume_lots")),
            row.get("min_volume", row.get("volume_min")),
            row.get("reason", row.get("source_reason", "")),
        )
        if key in shown:
            continue
        shown.add(key)
        print(
            f"{key[0]} {key[1]} | {key[2]} | "
            f"entry={key[3]} stop={key[4]} dist={key[5]} "
            f"raw_lots={key[6]} lots={key[7]} min_volume={key[8]} | {key[9]}"
        )
        if len(shown) >= 20:
            break

    if violations:
        print()
        print("Verdict: FAIL")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print()
    print("Verdict: PASS")
    print("BLOCKED rows preserve positive entry/stop/stop-distance/raw-lots diagnostics while keeping executable lots at 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
