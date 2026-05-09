"""H024 pullback-continuation fixed lifecycle diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

The diagnostic uses the H024 bridge shim as the signal source, preserves H018
hard execution guards through the existing fixed-lifecycle event path, and
reports portfolio performance plus split diagnostics.

Do not run on real broker-native data without explicit user authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd

from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h024_runner import H024BridgeConfig, run_h024_bridge_shim
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    H021FixedLifecycleBacktestResult,
    H021FixedLifecycleSummary,
    backtest_fixed_lifecycle_from_result,
    format_group_summary_table,
    format_lifecycle_summary_table,
    summarize_chronological_halves,
    summarize_chronological_thirds,
    summarize_fills_by_field,
    summarize_fills_by_year,
    summarize_lifecycle_backtest,
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

DEFAULT_H024_HOLD_H4_BARS: tuple[int, ...] = (1, 2, 3, 4)
BRIDGE_WINDOW_CACHE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "cache"
    / "strict_usdjpy_xauusd_h4_m1_bridge_windows.json"
)


@dataclass(frozen=True)
class H024DiagnosticRun:
    hold_h4_bars: int
    result: H021FixedLifecycleBacktestResult
    summary: H021FixedLifecycleSummary
    group_report: str


def run_h024_fixed_lifecycle_diagnostic(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    hold_h4_bars_values: Sequence[int] = DEFAULT_H024_HOLD_H4_BARS,
    bridge_config: H024BridgeConfig | None = None,
    starting_equity_usd: float = 10_000.0,
) -> tuple[H024DiagnosticRun, ...]:
    """Run H024 fixed-lifecycle diagnostics from already-loaded bars."""

    if starting_equity_usd <= 0.0:
        raise ValueError("starting_equity_usd must be positive")
    if not hold_h4_bars_values:
        raise ValueError("hold_h4_bars_values must be non-empty")

    h024_result = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=bridge_config,
    )

    runs: list[H024DiagnosticRun] = []
    for hold_h4_bars in hold_h4_bars_values:
        if hold_h4_bars <= 0:
            raise ValueError("hold_h4_bars values must be positive")

        result = backtest_fixed_lifecycle_from_result(
            h017_result=h024_result,
            usdjpy_h4=usdjpy_h4,
            xauusd_h4=xauusd_h4,
            usdjpy_m1=usdjpy_m1,
            xauusd_m1=xauusd_m1,
            accepted_entry_times=accepted_entry_times,
            hold_h4_bars=hold_h4_bars,
            starting_equity_usd=starting_equity_usd,
        )
        summary = summarize_lifecycle_backtest(result)
        runs.append(
            H024DiagnosticRun(
                hold_h4_bars=hold_h4_bars,
                result=result,
                summary=summary,
                group_report=format_h024_group_reports(result),
            )
        )

    return tuple(runs)


def format_h024_diagnostic_report(runs: Sequence[H024DiagnosticRun]) -> str:
    """Format the complete H024 diagnostic output."""

    summaries = [run.summary for run in runs]
    sections = [
        "H024 pullback-continuation fixed lifecycle diagnostic",
        "=" * 72,
        format_lifecycle_summary_table(
            summaries,
            title="H024 fixed lifecycle summary",
        ),
        "",
        "Verdict reminder: this is research diagnostics only.",
        "No demo trading is approved. No live trading is approved. Phase 4 is not approved.",
    ]

    for run in runs:
        sections.extend(
            [
                "",
                f"Detailed split report: hold={run.hold_h4_bars} H4",
                run.group_report,
            ]
        )

    return "\n".join(sections)


def format_h024_group_reports(result: H021FixedLifecycleBacktestResult) -> str:
    """Format H024 split reports using keyword-only helper calls.

    This explicitly covers the reporting path that previously failed in H023.
    """

    return "\n\n".join(
        [
            "By symbol:",
            format_group_summary_table(
                summarize_fills_by_field(result.fills, field="symbol"),
                title="By symbol",
            ),
            "By side:",
            format_group_summary_table(
                summarize_fills_by_field(result.fills, field="side"),
                title="By side",
            ),
            "Chronological halves:",
            format_group_summary_table(
                summarize_chronological_halves(result.fills),
                title="Chronological halves",
            ),
            "Chronological thirds:",
            format_group_summary_table(
                summarize_chronological_thirds(result.fills),
                title="Chronological thirds",
            ),
            "By calendar year:",
            format_group_summary_table(
                summarize_fills_by_year(result.fills),
                title="By calendar year",
            ),
        ]
    )


def main() -> None:
    print("H024 pullback-continuation fixed lifecycle diagnostic")
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
    print("Running H024 fixed-lifecycle diagnostic...")
    print()

    runs = run_h024_fixed_lifecycle_diagnostic(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
    )
    print(format_h024_diagnostic_report(runs))


if __name__ == "__main__":
    main()
