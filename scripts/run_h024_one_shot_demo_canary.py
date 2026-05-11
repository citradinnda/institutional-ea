from __future__ import annotations

import argparse
import json
from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary import (
    ACKNOWLEDGEMENT_TEXT,
    CanaryExecutionRefusal,
    OneShotDemoCanaryConfig,
    execute_one_shot_demo_canary,
    read_single_jsonl_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the H024 one-shot standard-demo canary path. "
            "By default this builds the request only. --send plus exact acknowledgement is required to place one demo order."
        )
    )
    parser.add_argument("--final-audit-packet", default="reports/h024_standard_demo_final_pre_dispatch_audit_packet.jsonl")
    parser.add_argument("--ledger", default="reports/h024_standard_demo_one_shot_demo_canary_ledger.jsonl")
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--side", choices=["buy", "sell"], default="sell")
    parser.add_argument("--volume", type=float, default=0.01)
    parser.add_argument("--max-lot-cap", type=float, default=0.01)
    parser.add_argument("--sl-distance-price", type=float, default=89.027)
    parser.add_argument("--deviation-points", type=int, default=50)
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--acknowledgement", default="")
    args = parser.parse_args()

    config = OneShotDemoCanaryConfig(
        allowed_demo_server=args.allowed_demo_server,
        symbol=args.symbol,
        side=args.side,
        volume=args.volume,
        max_lot_cap=args.max_lot_cap,
        sl_distance_price=args.sl_distance_price,
        deviation_points=args.deviation_points,
        send=args.send,
        acknowledgement=args.acknowledgement,
    )

    if args.send and args.acknowledgement != ACKNOWLEDGEMENT_TEXT:
        print(f"Refused: --send requires --acknowledgement {ACKNOWLEDGEMENT_TEXT!r}")
        return 2

    final_audit_packet = read_single_jsonl_record(Path(args.final_audit_packet))

    try:
        import MetaTrader5 as mt5  # type: ignore[import-not-found]
    except ImportError:
        print("Refused: MetaTrader5 package is not installed in this Python environment.")
        return 2

    if not mt5.initialize():
        print(f"Refused: mt5.initialize() failed: {mt5.last_error()}")
        return 2

    try:
        result = execute_one_shot_demo_canary(
            terminal=mt5,
            final_audit_packet=final_audit_packet,
            ledger_path=Path(args.ledger),
            config=config,
        )
    except CanaryExecutionRefusal as exc:
        print(f"Refused: {exc}")
        return 2
    finally:
        mt5.shutdown()

    print(json.dumps(result, indent=2, sort_keys=True))
    if args.send:
        print("H024 one-shot standard-demo canary send path completed.")
    else:
        print("Dry run only: request built, no order_check/order_send attempted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())