from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from quantcore.execution.h024_execution_safety_controls import (
    IDEMPOTENCY_LEDGER_SCHEMA,
    append_h024_execution_safety_audit_event,
    build_h024_execution_safety_controls_preflight,
)


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


def _read_optional_json(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise SystemExit(f"JSON file is not an object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Build H024 execution safety-controls preflight JSONL.")
    parser.add_argument(
        "execution_safety_controls_design_jsonl",
        type=Path,
        nargs="?",
        default=Path("reports/h024_standard_demo_execution_safety_controls_design.jsonl"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/h024_standard_demo_execution_safety_controls_preflight.jsonl"),
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=Path("reports/h024_standard_demo_execution_safety_controls_audit.jsonl"),
    )
    parser.add_argument("--kill-switch-state-json", type=Path)
    parser.add_argument("--idempotency-ledger-json", type=Path)
    parser.add_argument("--allowed-demo-server", action="append", required=True)
    parser.add_argument("--expected-account-currency", default="USD")
    parser.add_argument("--max-risk-fraction", default="0.01")
    parser.add_argument("--operator-decision", default="NOT_REQUESTED")
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

    kill_switch_state = _read_optional_json(args.kill_switch_state_json)
    idempotency_ledger = _read_optional_json(args.idempotency_ledger_json)
    if idempotency_ledger is None and args.idempotency_ledger_json is None:
        idempotency_ledger = {
            "schema": IDEMPOTENCY_LEDGER_SCHEMA,
            "pending_intent_ids": [],
            "completed_intent_ids": [],
        }

    record = build_h024_execution_safety_controls_preflight(
        source_records[0],
        kill_switch_state=kill_switch_state,
        idempotency_ledger=idempotency_ledger,
        allowed_demo_servers=args.allowed_demo_server,
        expected_account_currency=args.expected_account_currency,
        max_risk_fraction=args.max_risk_fraction,
        operator_decision=args.operator_decision,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")

    audit_event = record.get("immutable_audit_log_event")
    if isinstance(audit_event, dict):
        append_h024_execution_safety_audit_event(args.audit_output, audit_event)

    print(f"Output execution safety-controls preflight JSONL: {args.output}")
    print(f"Output execution safety-controls audit JSONL: {args.audit_output}")
    print("Preflight records: 1")
    print(f"Violations: {len(record.get('violations', []))}")
    for violation in record.get("violations", []):
        print(f"- {violation}")
    print(f"Control status: {record.get('control_status')}")
    print(f"Control decision: {record.get('control_decision')}")
    print(f"Blocked reasons: {len(record.get('blocked_reasons', []))}")
    for reason in record.get("blocked_reasons", []):
        print(f"- {reason}")
    print(f"Execution approved: {record.get('execution_approved')}")
    print(f"Verdict: {record.get('verdict')}")

    return 0 if record.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())