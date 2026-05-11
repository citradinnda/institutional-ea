from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from quantcore.execution.h024_operator_control_state import build_h024_operator_control_state_snapshot


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"JSONL line {line_number} is not an object")
            records.append(value)
    return records


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build H024 operator control-state snapshot JSON artifacts.")
    parser.add_argument(
        "execution_safety_controls_design_jsonl",
        type=Path,
        nargs="?",
        default=Path("reports/h024_standard_demo_execution_safety_controls_design.jsonl"),
    )
    parser.add_argument(
        "--snapshot-output",
        type=Path,
        default=Path("reports/h024_standard_demo_operator_control_state_snapshot.json"),
    )
    parser.add_argument(
        "--kill-switch-output",
        type=Path,
        default=Path("reports/h024_standard_demo_kill_switch_state_snapshot.json"),
    )
    parser.add_argument(
        "--idempotency-ledger-output",
        type=Path,
        default=Path("reports/h024_standard_demo_idempotency_ledger_snapshot.json"),
    )
    parser.add_argument("--allowed-demo-server", action="append", required=True)
    parser.add_argument("--expected-account-currency", default="USD")
    parser.add_argument("--max-risk-fraction", default="0.01")
    parser.add_argument("--max-orders-per-session", type=int, default=1)
    parser.add_argument("--orders-this-session", type=int, default=0)
    parser.add_argument("--daily-loss-limit-usd", default="1000")
    parser.add_argument("--realized-loss-today-usd", default="0")
    args = parser.parse_args()

    verifier_command = [
        sys.executable,
        "scripts/verify_h024_execution_safety_controls_design_jsonl.py",
        str(args.execution_safety_controls_design_jsonl),
    ]
    for server in args.allowed_demo_server:
        verifier_command.extend(["--allowed-demo-server", server])
    verifier_command.extend(
        [
            "--expected-account-currency",
            args.expected_account_currency,
            "--max-risk-fraction",
            args.max_risk_fraction,
            "--require-design",
        ]
    )

    verifier = subprocess.run(verifier_command, check=False, capture_output=True, text=True)
    if verifier.returncode != 0:
        print(verifier.stdout)
        print(verifier.stderr, file=sys.stderr)
        raise SystemExit("Source execution safety-controls design verifier failed")

    source_records = _read_jsonl(args.execution_safety_controls_design_jsonl)
    if len(source_records) != 1:
        raise SystemExit(f"Expected exactly one execution safety-controls design record, found {len(source_records)}")

    snapshot = build_h024_operator_control_state_snapshot(
        source_records[0],
        allowed_demo_servers=args.allowed_demo_server,
        expected_account_currency=args.expected_account_currency,
        max_risk_fraction=args.max_risk_fraction,
        max_orders_per_session=args.max_orders_per_session,
        orders_this_session=args.orders_this_session,
        daily_loss_limit_usd=args.daily_loss_limit_usd,
        realized_loss_today_usd=args.realized_loss_today_usd,
    )

    _write_json(args.snapshot_output, snapshot)
    if snapshot.get("verdict") == "PASS":
        _write_json(args.kill_switch_output, snapshot["kill_switch_state"])
        _write_json(args.idempotency_ledger_output, snapshot["idempotency_ledger"])

    print(f"Output operator control-state snapshot JSON: {args.snapshot_output}")
    print(f"Output kill-switch state JSON: {args.kill_switch_output}")
    print(f"Output idempotency ledger JSON: {args.idempotency_ledger_output}")
    print(f"Violations: {len(snapshot.get('violations', []))}")
    for violation in snapshot.get("violations", []):
        print(f"- {violation}")
    print(f"Snapshot status: {snapshot.get('snapshot_status')}")
    print(f"Stable intent id: {snapshot.get('stable_intent_id')}")
    print(f"Phase 4 approved: {snapshot.get('phase4_approved')}")
    print(f"Demo order placement approved: {snapshot.get('demo_order_placement_approved')}")
    print(f"Live order placement approved: {snapshot.get('live_order_placement_approved')}")
    print(f"Execution approved: {snapshot.get('execution_approved')}")
    print(f"Verdict: {snapshot.get('verdict')}")

    return 0 if snapshot.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())