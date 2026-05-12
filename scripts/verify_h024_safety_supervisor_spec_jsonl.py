from __future__ import annotations

import argparse

from quantcore.execution.h024_safety_supervisor_spec import (
    load_jsonl,
    verify_h024_safety_supervisor_spec_records,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify H024 read-only safety supervisor specification JSONL.")
    parser.add_argument("path")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    records = load_jsonl(args.path)
    summary = verify_h024_safety_supervisor_spec_records(records, require_pass=args.require_pass)

    print(f"H024 safety supervisor spec records: {summary['record_count']}")
    print(f"Violations: {len(summary['violations'])}")
    print(f"Embedded violations: {len(summary['embedded_violations'])}")
    print(f"Record verdict: {summary['record_verdict']}")
    print(f"Verifier verdict: {summary['verdict']}")
    print(f"Global guards: {summary['global_guard_count']}")
    print(f"Symbol circuit breaker groups: {summary['symbol_count']}")
    print(f"Broker mutation authorized: {summary['broker_mutation_authorized']}")
    print(f"Order check authorized: {summary['order_check_authorized']}")
    print(f"Order send authorized: {summary['order_send_authorized']}")
    print(f"Entry authorized: {summary['entry_authorized']}")
    print(f"Close/modify authorized: {summary['close_modify_authorized']}")
    print(f"XAUUSD order authorized: {summary['xauusd_order_authorized']}")
    print(f"USDJPY order authorized: {summary['usdjpy_order_authorized']}")
    print(f"Trading loop authorized: {summary['trading_loop_authorized']}")
    print(f"Automatic execution authorized: {summary['automatic_execution_authorized']}")

    if summary["violations"]:
        for violation in summary["violations"]:
            print(f"- {violation}")

    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())