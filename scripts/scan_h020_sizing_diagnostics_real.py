"""Scan real broker-native data for H020 sizing diagnostics.

Diagnostic-only:
- does not execute fills,
- does not skip or clip trades silently in event validation,
- proves whether the H020 sizing contract successfully prevents hard guard violations,
- does not promote H020,
- does not approve live trading.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.data.bridge_windows import (
    CommonCompleteBridgeWindowAssessment,
    assess_common_complete_h4_m1_windows,
)
from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h019 import run_h019
from quantcore.strategy.h020 import (
    H020IntervalSizingResult,
    H020SizingConfig,
    generate_h020_intent_panel,
)

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


@dataclass(frozen=True)
class H020SizingDiagnosticRun:
    bridge_window_assessment: CommonCompleteBridgeWindowAssessment
    panels: list[H020IntervalSizingResult]


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
        raise RuntimeError(f"accepted_count mismatch: {assessment.accepted_count}")


def build_h020_sizing_diagnostic(
    loaded: LoadedBrokerNativeExports,
) -> H020SizingDiagnosticRun:
    assessment = _assess_bridge_windows(loaded)
    _assert_expected_bridge_window_assessment(assessment)

    h019_result = run_h019(
        usdjpy_ohlcv=loaded.usdjpy_h4.bars,
        xauusd_ohlcv=loaded.xauusd_h4.bars,
    )

    panels = generate_h020_intent_panel(
        positions=h019_result.positions,
        stops_long=h019_result.stops_long,
        stops_short=h019_result.stops_short,
        h4_by_symbol={
            "USDJPY": loaded.usdjpy_h4.bars,
            "XAUUSD": loaded.xauusd_h4.bars,
        },
        equity_usd=10000.0,
        config=H020SizingConfig.default(),
    )

    return H020SizingDiagnosticRun(
        bridge_window_assessment=assessment,
        panels=panels,
    )


def main() -> None:
    print("H020 sizing contract diagnostic scan")
    print("=" * 60)
    print("Source: Exness demo MT5 broker-native H4/M1 exports")
    print()

    loaded = _load_broker_native_exports()
    diagnostic = build_h020_sizing_diagnostic(loaded)
    
    assessment = diagnostic.bridge_window_assessment
    panels = diagnostic.panels

    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print()

    accepted_timestamps = set(assessment.accepted_timestamps)
    accepted_panels = [p for p in panels if p.entry_time in accepted_timestamps]

    total_intents = 0
    suppressed_count = 0
    executed_count = 0
    suppression_reasons: dict[str, int] = {}
    
    max_per_trade_leverage = 0.0
    max_portfolio_leverage = 0.0
    portfolio_scales_applied = 0

    for panel in accepted_panels:
        if panel.portfolio_scaled:
            portfolio_scales_applied += 1
        
        max_portfolio_leverage = max(max_portfolio_leverage, panel.portfolio_gross_leverage)
        
        for intent in panel.intents.values():
            if intent.suppression_reason == "flat_signal":
                continue  # Ignore warmups and intentional flats
                
            total_intents += 1
            if intent.suppressed:
                suppressed_count += 1
                reason = intent.suppression_reason or "unknown"
                suppression_reasons[reason] = suppression_reasons.get(reason, 0) + 1
            else:
                executed_count += 1
                max_per_trade_leverage = max(max_per_trade_leverage, intent.gross_leverage)

    print("H020 Sizing Summary (Over Accepted Windows)")
    print("-" * 40)
    print(f"total_non_flat_intents={total_intents}")
    print(f"executed_intents={executed_count}")
    print(f"suppressed_intents={suppressed_count}")
    print(f"suppression_reasons={suppression_reasons}")
    print(f"portfolio_scales_applied={portfolio_scales_applied}")
    print()
    print("H018 Hard Guard Verification")
    print("-" * 40)
    print(f"max_per_trade_gross_leverage_seen={max_per_trade_leverage:.6f} (Limit: 10.0)")
    print(f"max_portfolio_gross_leverage_seen={max_portfolio_leverage:.6f} (Limit: 10.0)")
    print(f"invalid_stop_geometry_emissions={suppression_reasons.get('invalid_stop_geometry', 0)}")
    print(f"minimum_stop_distance_emissions={suppression_reasons.get('minimum_stop_distance', 0)}")
    print()

    print("Interpretation guardrails")
    print("-" * 40)
    print("H020 VALIDATED: False")
    print("H020 PROMOTABLE: False")
    print("LIVE TRADING APPROVED: False")


if __name__ == "__main__":
    main()
