"""H024 direction-flip negative-control diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

Purpose:
- test whether frozen H024 hold=3 has directional edge,
- invert H024's executed directions without optimizing parameters,
- preserve accepted bridge windows, lifecycle, modeled costs, and H018 guards.

If the inverted control also performs well, H024 curve-fit risk increases.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd

from quantcore.backtest.portfolio import fill_pnl_usd
from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h024_runner import H024BridgeConfig, run_h024_bridge_shim
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    H021FixedLifecycleBacktestResult,
    H021FixedLifecycleSummary,
    backtest_fixed_lifecycle_from_result,
    format_lifecycle_summary_table,
    summarize_lifecycle_backtest,
)
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

DEFAULT_H024_DIRECTION_FLIP_HOLD_H4_BARS = 3
_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class H024DirectionFlipDiagnosticResult:
    baseline: H021FixedLifecycleBacktestResult
    direction_flip: H021FixedLifecycleBacktestResult
    baseline_summary: H021FixedLifecycleSummary
    direction_flip_summary: H021FixedLifecycleSummary


def build_direction_flip_h017_result(
    *,
    h024_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    hold_h4_bars: int = DEFAULT_H024_DIRECTION_FLIP_HOLD_H4_BARS,
) -> H017Result:
    """Invert H024 directions and mirror stop distance around raw entry open.

    The event bridge validates stops against the raw entry open at t+1. A naïve
    sign flip can create invalid stop geometry when the market gaps. This
    negative control instead preserves each original raw stop distance and
    mirrors it to the opposite side of the raw entry open.
    """

    if hold_h4_bars <= 0:
        raise ValueError("hold_h4_bars must be positive")

    decision_index = _require_utc_index(h024_result.positions.index, name="positions.index")
    h4_by_symbol = {
        "USDJPY": _with_utc_index(usdjpy_h4),
        "XAUUSD": _with_utc_index(xauusd_h4),
    }

    flipped_positions = -h024_result.positions.copy()
    flipped_signals = -h024_result.signals.copy()
    flipped_stops_long = pd.DataFrame(float("nan"), index=decision_index, columns=_SYMBOLS)
    flipped_stops_short = pd.DataFrame(float("nan"), index=decision_index, columns=_SYMBOLS)

    for entry_location in range(1, len(decision_index) - hold_h4_bars):
        decision_time = pd.Timestamp(decision_index[entry_location - 1]).tz_convert("UTC")
        entry_time = pd.Timestamp(decision_index[entry_location]).tz_convert("UTC")

        for symbol in _SYMBOLS:
            signed_risk = float(h024_result.positions.at[decision_time, symbol])
            if pd.isna(signed_risk) or signed_risk == 0.0:
                continue

            entry_raw_price = float(h4_by_symbol[symbol].at[entry_time, "open"])

            if signed_risk > 0.0:
                original_stop = float(h024_result.stops_long.at[decision_time, symbol])
            else:
                original_stop = float(h024_result.stops_short.at[decision_time, symbol])

            if pd.isna(original_stop):
                continue

            raw_stop_distance = abs(entry_raw_price - original_stop)
            if raw_stop_distance <= 0.0:
                continue

            flipped_signed_risk = -signed_risk
            if flipped_signed_risk > 0.0:
                flipped_stops_long.at[decision_time, symbol] = entry_raw_price - raw_stop_distance
            else:
                flipped_stops_short.at[decision_time, symbol] = entry_raw_price + raw_stop_distance

    return H017Result(
        positions=flipped_positions,
        signals=flipped_signals,
        stops_long=flipped_stops_long,
        stops_short=flipped_stops_short,
        vol_multipliers=h024_result.vol_multipliers.copy(),
        heat_multipliers=h024_result.heat_multipliers.copy(),
        heat_pre=h024_result.heat_pre.copy(),
        heat_post=h024_result.heat_post.copy(),
        heat_binding=h024_result.heat_binding.copy(),
    )


def run_h024_direction_flip_diagnostic(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    hold_h4_bars: int = DEFAULT_H024_DIRECTION_FLIP_HOLD_H4_BARS,
    bridge_config: H024BridgeConfig | None = None,
    starting_equity_usd: float = 10_000.0,
) -> H024DirectionFlipDiagnosticResult:
    """Run frozen H024 and its direction-flipped negative control."""

    h024_result = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=bridge_config,
    )

    baseline = backtest_fixed_lifecycle_from_result(
        h017_result=h024_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars=hold_h4_bars,
        starting_equity_usd=starting_equity_usd,
    )

    direction_flip_result = build_direction_flip_h017_result(
        h024_result=h024_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        hold_h4_bars=hold_h4_bars,
    )

    direction_flip = backtest_fixed_lifecycle_from_result(
        h017_result=direction_flip_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars=hold_h4_bars,
        starting_equity_usd=starting_equity_usd,
    )

    return H024DirectionFlipDiagnosticResult(
        baseline=baseline,
        direction_flip=direction_flip,
        baseline_summary=summarize_lifecycle_backtest(baseline),
        direction_flip_summary=summarize_lifecycle_backtest(direction_flip),
    )


def format_h024_direction_flip_report(
    diagnostic: H024DirectionFlipDiagnosticResult,
) -> str:
    rows = [
        diagnostic.baseline_summary,
        diagnostic.direction_flip_summary,
    ]
    baseline_pnl = diagnostic.baseline_summary.total_pnl_usd
    flipped_pnl = diagnostic.direction_flip_summary.total_pnl_usd
    pnl_delta = baseline_pnl - flipped_pnl

    sections = [
        "H024 direction-flip negative-control diagnostic",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        format_lifecycle_summary_table(
            rows,
            title="Baseline H024 vs direction-flip control",
        ),
        "",
        f"Baseline total PnL USD: {baseline_pnl:.2f}",
        f"Direction-flip total PnL USD: {flipped_pnl:.2f}",
        f"Baseline minus direction-flip PnL USD: {pnl_delta:.2f}",
        "",
        "Interpretation rule:",
        "- Direction flip should be materially worse than frozen H024.",
        "- If direction flip is also strong, H024 curve-fit risk increases.",
        "- This diagnostic cannot approve demo/live/Phase 4.",
    ]
    return "\n".join(sections)


def main() -> None:
    print("H024 direction-flip negative-control diagnostic")
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
    print("Running baseline and direction-flip control...")
    print()

    diagnostic = run_h024_direction_flip_diagnostic(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
    )
    print(format_h024_direction_flip_report(diagnostic))


def _with_utc_index(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result.index = _require_utc_index(result.index, name="frame.index")
    return result


def _require_utc_index(index: pd.Index, *, name: str) -> pd.DatetimeIndex:
    if not isinstance(index, pd.DatetimeIndex):
        raise ValueError(f"{name} must be a DatetimeIndex")
    if index.tz is None:
        raise ValueError(f"{name} must be timezone-aware")
    return index.tz_convert("UTC")


if __name__ == "__main__":
    main()
