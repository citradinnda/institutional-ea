from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_monitor import (
    EXPECTED_SYMBOL,
    build_monitor_record,
    load_jsonl,
    normalize_mt5_object,
    normalize_mt5_objects,
    utc_now_iso,
    write_jsonl,
)

DEFAULT_OUTPUT = Path("reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl")
DEFAULT_LEDGER = Path("reports/h024_standard_demo_one_shot_demo_canary_ledger.jsonl")
HISTORY_FROM_UTC = datetime(2026, 5, 1, tzinfo=timezone.utc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the H024 one-shot standard-demo canary read-only monitor packet.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    import MetaTrader5 as mt5

    if not mt5.initialize():
        last_error = mt5.last_error()
        raise SystemExit(f"mt5.initialize failed: {last_error}")

    try:
        account_raw = mt5.account_info()
        if account_raw is None:
            raise SystemExit(f"mt5.account_info failed: {mt5.last_error()}")
        positions_raw = mt5.positions_get(symbol=EXPECTED_SYMBOL)
        if positions_raw is None:
            positions_raw = []
        orders_raw = mt5.orders_get(symbol=EXPECTED_SYMBOL)
        if orders_raw is None:
            orders_raw = []
        history_raw = mt5.history_deals_get(HISTORY_FROM_UTC, datetime.now(timezone.utc))
        if history_raw is None:
            history_raw = []
    finally:
        mt5.shutdown()

    record = build_monitor_record(
        generated_at_utc=utc_now_iso(),
        account=normalize_mt5_object(account_raw),
        positions=normalize_mt5_objects(positions_raw),
        pending_orders=normalize_mt5_objects(orders_raw),
        history_deals=normalize_mt5_objects(history_raw),
        ledger_records=load_jsonl(args.ledger),
    )
    write_jsonl(args.output, [record])

    print(f"Wrote {args.output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Lifecycle state: {record['lifecycle_state']}")
    print(f"Exact open canary positions found: {record['observed']['exact_canary_position_count']}")
    print(f"Unexpected H024 pending orders found: {record['observed']['unexpected_h024_pending_order_count']}")
    print(f"Ledger successful canary records found: {record['observed']['ledger_success_count']}")
    if record["open_canary_position"] is not None:
        print(f"Current price: {record['latest_known']['price_current']}")
        print(f"Floating P/L: {record['latest_known']['profit']}")
        print(f"Swap: {record['latest_known']['swap']}")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())