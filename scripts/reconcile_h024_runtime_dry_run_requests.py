"""Reconcile H024 runtime intended-action rows into dry-run execution requests.

Research only. No demo/live/Phase 4 approval.
This script reads collected CSVs only. It does not touch MT5 and sends no orders.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from quantcore.execution.h024_dry_run_execution_request import (
    build_h024_dry_run_execution_request,
)
from scripts.verify_h024_ea_preflight_log import (
    INTENDED_ACTION_LOG_ROW_FIELDS,
    verify_h024_ea_preflight_log,
)


@dataclass(frozen=True)
class H024DryRunReconciliationResult:
    rows: int
    intended_action_rows: int
    would_open_rows: int
    dry_run_requests: tuple[dict[str, Any], ...]
    skipped_rows: int
    violations: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.violations


def _extra_csv_fields(row: dict[Any, Any]) -> list[str]:
    extra = row.get(None)
    if extra is None:
        return []
    return [str(value) for value in extra]


def _reconstruct_intended_action_row(row: dict[str, str]) -> dict[str, Any]:
    payload = _extra_csv_fields(row)
    fields = dict(zip(INTENDED_ACTION_LOG_ROW_FIELDS, payload))
    return {"timestamp": row.get("detail", ""), **fields}


def reconcile_h024_runtime_dry_run_requests(
    path: Path,
    *,
    require_request: bool = False,
) -> H024DryRunReconciliationResult:
    verification = verify_h024_ea_preflight_log(path)
    if not verification.passed:
        return H024DryRunReconciliationResult(
            rows=verification.rows,
            intended_action_rows=0,
            would_open_rows=0,
            dry_run_requests=(),
            skipped_rows=0,
            violations=tuple(f"preflight verification: {violation}" for violation in verification.violations),
        )

    violations: list[str] = []
    dry_run_requests: list[dict[str, Any]] = []
    intended_action_rows = 0
    would_open_rows = 0
    skipped_rows = 0

    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    for row_number, row in enumerate(rows, start=2):
        if row.get("event") != "H024_INTENDED_ACTION_ROW":
            continue

        intended_action_rows += 1
        payload = _extra_csv_fields(row)
        if len(payload) != len(INTENDED_ACTION_LOG_ROW_FIELDS):
            violations.append(
                f"row {row_number}: intended-action payload has {len(payload)} fields, "
                f"expected {len(INTENDED_ACTION_LOG_ROW_FIELDS)}"
            )
            continue

        intended_action_row = _reconstruct_intended_action_row(row)
        if intended_action_row.get("decision") == "WOULD_OPEN":
            would_open_rows += 1

        try:
            dry_run_request = build_h024_dry_run_execution_request(intended_action_row)
        except ValueError as exc:
            violations.append(f"row {row_number}: {exc}")
            continue

        if dry_run_request is None:
            skipped_rows += 1
            continue

        dry_run_requests.append(dry_run_request)

    if require_request and not dry_run_requests:
        violations.append("missing required dry-run execution request")

    return H024DryRunReconciliationResult(
        rows=len(rows),
        intended_action_rows=intended_action_rows,
        would_open_rows=would_open_rows,
        dry_run_requests=tuple(dry_run_requests),
        skipped_rows=skipped_rows,
        violations=tuple(violations),
    )


def _write_jsonl(path: Path, requests: tuple[dict[str, Any], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for request in requests:
            handle.write(json.dumps(request, sort_keys=True))
            handle.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--require-request",
        action="store_true",
        help="Fail unless at least one dry-run request is reconstructed.",
    )
    parser.add_argument(
        "--output-jsonl",
        type=Path,
        help="Optional local JSONL output path for reconstructed dry-run requests.",
    )
    args = parser.parse_args(argv)

    result = reconcile_h024_runtime_dry_run_requests(
        args.csv_path,
        require_request=args.require_request,
    )

    print("H024 dry-run execution request reconciliation")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("CSV read only. No MT5 access. No order execution.")
    print()
    print(f"CSV: {args.csv_path}")
    print(f"Rows: {result.rows}")
    print(f"Intended-action rows: {result.intended_action_rows}")
    print(f"WOULD_OPEN rows: {result.would_open_rows}")
    print(f"Dry-run requests: {len(result.dry_run_requests)}")
    print(f"Skipped non-request rows: {result.skipped_rows}")

    if result.violations:
        print()
        print("Violations:")
        for violation in result.violations:
            print(f"- {violation}")
        print()
        print("Verdict: FAIL")
        return 1

    if args.output_jsonl is not None:
        _write_jsonl(args.output_jsonl, result.dry_run_requests)
        print(f"Output JSONL: {args.output_jsonl}")

    print()
    print("Verdict: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
