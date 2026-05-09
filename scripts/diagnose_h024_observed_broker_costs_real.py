"""H024 observed broker cost diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

The diagnostic reruns frozen H024 hold=3 under observed Exness MT5
spread/commission facts from the broker symbol-spec audit. It does not tune
parameters, exclude 2023, add time/session filters, or alter H024 signal logic.

Do not run on real broker-native data without explicit user authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import pandas as pd

from quantcore.backtest.cost_model import DEFAULT_COST_SPECS, SymbolCostSpec
from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h024_runner import H024BridgeConfig
from scripts.diagnose_h021_fixed_lifecycle_variants_real import format_lifecycle_summary_table
from scripts.diagnose_h024_fixed_lifecycle_real import (
    BRIDGE_WINDOW_CACHE_PATH,
    H024DiagnosticRun,
    format_h024_group_reports,
    run_h024_fixed_lifecycle_diagnostic,
)
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)

FROZEN_H024_HOLD_H4_BARS = 3

OBSERVED_BROKER_COST_SPECS: dict[str, SymbolCostSpec] = {
    "USDJPY": SymbolCostSpec(
        symbol="USDJPY",
        spread_price=0.018,
        commission_usd_per_lot_per_fill=0.0,
        stop_slippage_atr_fraction=0.05,
    ),
    "XAUUSD": SymbolCostSpec(
        symbol="XAUUSD",
        spread_price=0.36,
        commission_usd_per_lot_per_fill=0.0,
        stop_slippage_atr_fraction=0.05,
    ),
}


@dataclass(frozen=True)
class H024ObservedBrokerCostDiagnostic:
    baseline: H024DiagnosticRun
    observed_broker_costs: H024DiagnosticRun


def run_h024_observed_broker_cost_diagnostic(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    bridge_config: H024BridgeConfig | None = None,
    starting_equity_usd: float = 10_000.0,
) -> H024ObservedBrokerCostDiagnostic:
    """Run frozen H024 hold=3 baseline versus observed broker costs."""

    baseline = run_h024_fixed_lifecycle_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars_values=(FROZEN_H024_HOLD_H4_BARS,),
        bridge_config=bridge_config,
        starting_equity_usd=starting_equity_usd,
        cost_specs_by_symbol=DEFAULT_COST_SPECS,
    )[0]

    observed = run_h024_fixed_lifecycle_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars_values=(FROZEN_H024_HOLD_H4_BARS,),
        bridge_config=bridge_config,
        starting_equity_usd=starting_equity_usd,
        cost_specs_by_symbol=OBSERVED_BROKER_COST_SPECS,
    )[0]

    return H024ObservedBrokerCostDiagnostic(
        baseline=baseline,
        observed_broker_costs=observed,
    )


def format_h024_observed_broker_cost_report(
    diagnostic: H024ObservedBrokerCostDiagnostic,
) -> str:
    """Format baseline versus observed-broker-cost H024 report."""

    baseline = diagnostic.baseline.summary
    observed = diagnostic.observed_broker_costs.summary

    delta_pnl = observed.total_pnl_usd - baseline.total_pnl_usd
    delta_pf = observed.profit_factor - baseline.profit_factor

    sections = [
        "H024 observed broker cost diagnostic",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        "Frozen setup:",
        f"- H024 hold={FROZEN_H024_HOLD_H4_BARS} H4",
        "- no parameter optimization",
        "- no 2023 exclusion",
        "- no time/session filters",
        "",
        "Observed MT5 broker cost facts:",
        "- USDJPY spread_price=0.018, commission_usd_per_lot_per_fill=0.0, stop_slippage_atr_fraction=0.05",
        "- XAUUSD spread_price=0.36, commission_usd_per_lot_per_fill=0.0, stop_slippage_atr_fraction=0.05",
        "",
        format_lifecycle_summary_table(
            (baseline, observed),
            title="Baseline modeled costs vs observed broker costs",
        ),
        "",
        "Delta observed minus baseline:",
        f"- total_pnl_usd: {delta_pnl:.2f}",
        f"- profit_factor: {delta_pf:.6f}",
        "",
        "Interpretation standard:",
        "- If H024 remains positive with PF >= 1.15, broker-cost reconciliation improves.",
        "- If H024 fails or materially degrades below acceptance thresholds, H024 remains research-only and broker-cost mismatch blocks deployment.",
        "- Passing this diagnostic still does not approve demo trading, live trading, or Phase 4.",
        "",
        "Observed broker cost split report:",
        format_h024_group_reports(diagnostic.observed_broker_costs.result),
    ]

    return "\n".join(sections)


def main() -> None:
    print("H024 observed broker cost diagnostic")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print()

    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="broker-native MT5 exports",
    )

    print("Loading exports...")
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

    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print("Running frozen H024 observed-broker-cost diagnostic...")
    print()

    diagnostic = run_h024_observed_broker_cost_diagnostic(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
    )
    print(format_h024_observed_broker_cost_report(diagnostic))


if __name__ == "__main__":
    main()
