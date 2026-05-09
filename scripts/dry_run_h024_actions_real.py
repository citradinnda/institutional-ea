"""Generate H024 dry-run/log-only action records from broker-native data.

Research/preparation only.

This is not:
- demo approval,
- live approval,
- Phase 4 approval,
- EA execution approval.

This script writes intended dry-run actions only. It does not import MT5 and
cannot place, modify, close, or delete orders.
"""
from __future__ import annotations

from pathlib import Path

from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.execution.h024_dry_run import DryRunConfig
from quantcore.execution.h024_dry_run_log import (
    build_h024_dry_run_actions,
    summarize_dry_run_actions,
    write_dry_run_actions_csv,
)
from quantcore.strategy.h024_runner import run_h024_bridge_shim
from scripts.diagnose_h024_fixed_lifecycle_real import BRIDGE_WINDOW_CACHE_PATH
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "reports" / "h024_dry_run_actions.csv"


def main() -> None:
    print("H024 dry-run/log-only action export")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("No MT5 order-send capability is present in this script.")
    print()

    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="broker-native MT5 exports",
    )

    usdjpy_h4 = load_mt5_csv(USDJPY_H4_PATH)
    xauusd_h4 = load_mt5_csv(XAUUSD_H4_PATH)
    usdjpy_m1 = load_mt5_csv(USDJPY_M1_PATH)
    xauusd_m1 = load_mt5_csv(XAUUSD_M1_PATH)

    cache_key = build_common_complete_bridge_window_cache_key(
        source_paths={
            "usdjpy_h4": USDJPY_H4_PATH,
            "xauusd_h4": XAUUSD_H4_PATH,
            "usdjpy_m1": USDJPY_M1_PATH,
            "xauusd_m1": XAUUSD_M1_PATH,
        },
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )
    assessment = assess_common_complete_h4_m1_windows_cached(
        cache_path=BRIDGE_WINDOW_CACHE_PATH,
        cache_key=cache_key,
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(
            "accepted_count mismatch: "
            f"expected={EXPECTED_ACCEPTED_COUNT}, observed={assessment.accepted_count}"
        )

    h024_result = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4.bars,
        xauusd_ohlcv=xauusd_h4.bars,
    )

    actions = build_h024_dry_run_actions(
        h017_result=h024_result,
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        accepted_entry_times=assessment.accepted_timestamps,
        config=DryRunConfig(kill_switch_enabled=True),
        starting_equity_usd=10_000.0,
        hold_h4_bars=3,
    )
    write_dry_run_actions_csv(actions=actions, output_path=OUTPUT_PATH)

    summary = summarize_dry_run_actions(actions)
    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print(f"Wrote: {OUTPUT_PATH}")
    print(f"WOULD_OPEN: {summary['WOULD_OPEN']}")
    print(f"NO_ACTION: {summary['NO_ACTION']}")
    print(f"BLOCKED: {summary['BLOCKED']}")
    print()
    print("Dry-run output only. No demo/live/Phase 4 approval.")


if __name__ == "__main__":
    main()
