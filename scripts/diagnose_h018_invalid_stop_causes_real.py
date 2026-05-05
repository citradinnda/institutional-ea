"""Real-data diagnostic for invalid H018 stop geometry causes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.backtest.h018_invalid_stop_cause import diagnose_invalid_stop_causes
from quantcore.data.bridge_windows import (
    CommonCompleteBridgeWindowAssessment,
    assess_common_complete_h4_m1_windows,
)
from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017 import run_h017


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data" / "raw"

USDJPY_H4_PATH = DATA_ROOT / "USDJPY" / "H4.csv"
XAUUSD_H4_PATH = DATA_ROOT / "XAUUSD" / "H4.csv"
USDJPY_M1_PATH = DATA_ROOT / "USDJPY" / "M1.csv"
XAUUSD_M1_PATH = DATA_ROOT / "XAUUSD" / "M1.csv"

EXPECTED_ACCEPTED_COUNT = 5476
EXPECTED_FIRST_ACCEPTED_TIMESTAMP = pd.Timestamp("2021-07-02 13:00:00", tz="UTC")
EXPECTED_LAST_ACCEPTED_TIMESTAMP = pd.Timestamp("2026-04-30 01:00:00", tz="UTC")
EXPECTED_M1_BARS_PER_H4 = 240
EXPECTED_H4_DELTA = pd.Timedelta(hours=4)


@dataclass(frozen=True)
class LoadedBrokerNativeExports:
    usdjpy_h4: MT5LoadResult
    xauusd_h4: MT5LoadResult
    usdjpy_m1: MT5LoadResult
    xauusd_m1: MT5LoadResult


def _load_broker_native_exports() -> LoadedBrokerNativeExports:
    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="broker-native MT5 exports",
    )

    return LoadedBrokerNativeExports(
        usdjpy_h4=load_mt5_csv(USDJPY_H4_PATH),
        xauusd_h4=load_mt5_csv(XAUUSD_H4_PATH),
        usdjpy_m1=load_mt5_csv(USDJPY_M1_PATH),
        xauusd_m1=load_mt5_csv(XAUUSD_M1_PATH),
    )


def _assess_bridge_windows(
    loaded: LoadedBrokerNativeExports,
) -> CommonCompleteBridgeWindowAssessment:
    return assess_common_complete_h4_m1_windows(
        usdjpy_h4=loaded.usdjpy_h4.bars,
        xauusd_h4=loaded.xauusd_h4.bars,
        usdjpy_m1=loaded.usdjpy_m1.bars,
        xauusd_m1=loaded.xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )


def _assert_expected_bridge_window_assessment(
    assessment: CommonCompleteBridgeWindowAssessment,
) -> None:
    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(
            f"accepted_count mismatch: expected {EXPECTED_ACCEPTED_COUNT}, "
            f"got {assessment.accepted_count}"
        )
    if assessment.first_accepted_timestamp != EXPECTED_FIRST_ACCEPTED_TIMESTAMP:
        raise RuntimeError(
            "first_accepted_timestamp mismatch: "
            f"expected {EXPECTED_FIRST_ACCEPTED_TIMESTAMP}, "
            f"got {assessment.first_accepted_timestamp}"
        )
    if assessment.last_accepted_timestamp != EXPECTED_LAST_ACCEPTED_TIMESTAMP:
        raise RuntimeError(
            "last_accepted_timestamp mismatch: "
            f"expected {EXPECTED_LAST_ACCEPTED_TIMESTAMP}, "
            f"got {assessment.last_accepted_timestamp}"
        )
    if assessment.common_complete_count != assessment.accepted_count:
        raise RuntimeError(
            "common_complete_count does not match accepted_count: "
            f"{assessment.common_complete_count} != {assessment.accepted_count}"
        )


def main() -> None:
    print("H018 invalid stop cause diagnostic")
    print("=" * 60)
    print(f"Broker timezone: {DEFAULT_BROKER_TZ}")
    print("Symbols: USDJPY, XAUUSD")
    print("Source: Exness demo MT5 broker-native H4/M1 exports")
    print("Mode: diagnostic-only; not validation promotion")
    print()

    loaded = _load_broker_native_exports()
    assessment = _assess_bridge_windows(loaded)
    _assert_expected_bridge_window_assessment(assessment)

    print("Strict bridge-window preflight")
    print("-" * 40)
    print(f"accepted_count={assessment.accepted_count}")
    print(f"first_accepted_timestamp={assessment.first_accepted_timestamp}")
    print(f"last_accepted_timestamp={assessment.last_accepted_timestamp}")
    print(f"rejected_count={assessment.rejected_count}")
    print()

    h017_result = run_h017(
        usdjpy_ohlcv=loaded.usdjpy_h4.bars,
        xauusd_ohlcv=loaded.xauusd_h4.bars,
    )

    diagnostic = diagnose_invalid_stop_causes(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": loaded.usdjpy_h4.bars,
            "XAUUSD": loaded.xauusd_h4.bars,
        },
        accepted_entry_times=assessment.accepted_timestamps,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    print("Invalid stop cause summary")
    print("-" * 40)
    print(f"accepted_entry_count={diagnostic.accepted_entry_count}")
    print(f"executed_entry_count={diagnostic.executed_entry_count}")
    print(f"skipped_entry_count={diagnostic.skipped_entry_count}")
    print(f"event_interval_count={diagnostic.event_interval_count}")
    print(f"trade_intent_count={diagnostic.trade_intent_count}")
    print(f"invalid_at_entry_count={diagnostic.invalid_at_entry_count}")
    print(f"cause_counts={diagnostic.cause_counts}")
    print(f"invalid_counts_by_symbol={diagnostic.invalid_counts_by_symbol}")
    print(f"invalid_counts_by_side={diagnostic.invalid_counts_by_side}")
    print()

    print("First invalid stop observations")
    print("-" * 40)
    for obs in diagnostic.observations[:20]:
        print(
            f"cause={obs.cause}, "
            f"symbol={obs.symbol}, "
            f"side={obs.side}, "
            f"decision_time={obs.decision_time}, "
            f"entry_time={obs.entry_time}, "
            f"decision_close={obs.decision_close}, "
            f"entry_open={obs.entry_open}, "
            f"stop_price={obs.stop_price}, "
            f"decision_margin={obs.decision_margin}, "
            f"entry_margin={obs.entry_margin}"
        )

    print()
    print("Interpretation guardrails")
    print("-" * 40)
    print("H018 VALIDATED: False")
    print("H018 PROMOTABLE: False")
    print("LIVE TRADING APPROVED: False")
    print("- crossed_between_decision_close_and_entry_open means the stop was valid at decision close but invalid by next executable open.")
    print("- already_invalid_at_decision_close means the selected stop was already on the wrong side when the signal was made.")
    print("- This diagnostic does not tune H017 or modify validation behavior.")
    print("- This diagnostic does not use HistData.")


if __name__ == "__main__":
    main()
