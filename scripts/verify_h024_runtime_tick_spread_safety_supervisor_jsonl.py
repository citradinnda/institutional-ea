from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from quantcore.execution.h024_runtime_tick_spread_safety_supervisor import (  # noqa: E402
    read_jsonl,
    verify_h024_runtime_tick_spread_safety_supervisor_records,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify the H024 runtime tick/spread safety supervisor JSONL packet.")
    parser.add_argument("path", help="Path to H024 runtime tick/spread safety supervisor JSONL.")
    parser.add_argument("--require-pass", action="store_true", help="Fail unless every supervisor record verdict is PASS.")
    return parser


def main() -> int:
    args = _parser().parse_args()
    records = read_jsonl(args.path)
    verification = verify_h024_runtime_tick_spread_safety_supervisor_records(records, require_pass=args.require_pass)

    embedded_violations = sum(len(record.get("violations", [])) for record in records)
    first_record = records[0] if records else {}

    print(f"H024 runtime tick/spread safety supervisor records: {verification.get('record_count')}")
    print(f"Violations: {len(verification.get('verification_violations', []))}")
    print(f"Embedded violations: {embedded_violations}")
    print(f"Record verdict: {first_record.get('verdict') if isinstance(first_record, dict) else None}")
    print(f"Verifier verdict: {verification.get('verifier_verdict')}")
    print(f"Operator state: {first_record.get('operator_state') if isinstance(first_record, dict) else None}")
    print(f"Effective new entries blocked: {first_record.get('effective_new_entries_blocked') if isinstance(first_record, dict) else None}")
    print(f"Symbol select authorized: {first_record.get('symbol_select_authorized') if isinstance(first_record, dict) else None}")
    print(f"Broker mutation authorized: {first_record.get('broker_mutation_authorized') if isinstance(first_record, dict) else None}")
    print(f"Order check authorized: {first_record.get('order_check_authorized') if isinstance(first_record, dict) else None}")
    print(f"Order send authorized: {first_record.get('order_send_authorized') if isinstance(first_record, dict) else None}")
    print(f"Entry authorized: {first_record.get('entry_authorized') if isinstance(first_record, dict) else None}")
    print(f"Close/modify authorized: {first_record.get('close_modify_authorized') if isinstance(first_record, dict) else None}")
    print(f"XAUUSD order authorized: {first_record.get('xauusd_order_authorized') if isinstance(first_record, dict) else None}")
    print(f"USDJPY order authorized: {first_record.get('usdjpy_order_authorized') if isinstance(first_record, dict) else None}")
    print(f"Trading loop authorized: {first_record.get('trading_loop_authorized') if isinstance(first_record, dict) else None}")
    print(f"Automatic execution authorized: {first_record.get('automatic_execution_authorized') if isinstance(first_record, dict) else None}")

    if isinstance(first_record, dict):
        for symbol_record in first_record.get("symbols", []):
            observed = symbol_record.get("observed", {})
            print(
                "Symbol "
                f"{symbol_record.get('runtime_symbol')}: "
                f"verdict={symbol_record.get('verdict')} "
                f"spread_points={observed.get('spread_points')} "
                f"tick_age_seconds={observed.get('tick_age_seconds')}"
            )

    return 0 if verification.get("verifier_verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())