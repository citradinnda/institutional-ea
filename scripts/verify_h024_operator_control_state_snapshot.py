from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from quantcore.execution.h024_operator_control_state import verify_h024_operator_control_state_snapshot


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise SystemExit(f"JSON file is not an object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify H024 operator control-state snapshot JSON.")
    parser.add_argument("operator_control_state_snapshot_json", type=Path)
    parser.add_argument("--allowed-demo-server", action="append", required=True)
    parser.add_argument("--expected-account-currency", default="USD")
    parser.add_argument("--max-risk-fraction", default="0.01")
    args = parser.parse_args()

    record = _read_json(args.operator_control_state_snapshot_json)

    violations = verify_h024_operator_control_state_snapshot(
        record,
        allowed_demo_servers=args.allowed_demo_server,
        expected_account_currency=args.expected_account_currency,
        max_risk_fraction=args.max_risk_fraction,
    )
    verdict = "PASS" if not violations else "FAIL"

    print(f"Input operator control-state snapshot JSON: {args.operator_control_state_snapshot_json}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    print(f"Verdict: {verdict}")

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())