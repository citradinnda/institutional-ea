"""H022 risk/lifecycle variant diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

H022 tests structurally different risk/lifecycle contracts on top of the H020
bridge shim while preserving H018 hard guards. The initial variants intentionally
avoid H021 positive time/session bucket mining.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, Sequence

import pandas as pd

from quantcore.backtest.fill_engine import Fill
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h020_runner import run_h020_bridge_shim
from quantcore.data.bridge_windows import assess_common_complete_h4_m1_windows
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    H021FixedLifecycleBacktestResult,
    H021FixedLifecycleSummary,
    backtest_fixed_lifecycle_from_result,
    format_group_summary_table,
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

_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")
_SPREAD_PRICE_BY_SYMBOL: dict[str, float] = {
    "USDJPY": 0.01,
    "XAUUSD": 0.30,
}


@dataclass(frozen=True)
class H022RiskLifecycleVariant:
    label: str
    hold_h4_bars: int
    position_scale: float
    min_stop_distance_spread_ratio: float | None


@dataclass(frozen=True)
class H022RiskLifecycleBacktestResult:
    variant: H022RiskLifecycleVariant
    transformed_signal: H017Result
    lifecycle_result: H021FixedLifecycleBacktestResult


@dataclass(frozen=True)
class H022RiskLifecycleSummary:
    label: str
    hold_h4_bars: int
    position_scale: float
    min_stop_distance_spread_ratio: float | None
    accepted_entry_count: int
    executed_entry_count: int
    skipped_entry_count: int
    lifecycle_skip_count: int
    incomplete_horizon_skip_count: int
    flat_entry_count: int
    fill_count: int
    stop_count: int
    stop_rate: float
    ending_equity_usd: float
    total_pnl_usd: float
    total_return: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    fill_return_sharpe: float


DEFAULT_H022_VARIANTS: tuple[H022RiskLifecycleVariant, ...] = (
    H022RiskLifecycleVariant(
        label="scale_0_50_hold_1",
        hold_h4_bars=1,
        position_scale=0.50,
        min_stop_distance_spread_ratio=None,
    ),
    H022RiskLifecycleVariant(
        label="scale_0_50_hold_2",
        hold_h4_bars=2,
        position_scale=0.50,
        min_stop_distance_spread_ratio=None,
    ),
    H022RiskLifecycleVariant(
        label="scale_0_25_hold_1",
        hold_h4_bars=1,
        position_scale=0.25,
        min_stop_distance_spread_ratio=None,
    ),
    H022RiskLifecycleVariant(
        label="scale_0_25_hold_2",
        hold_h4_bars=2,
        position_scale=0.25,
        min_stop_distance_spread_ratio=None,
    ),
    H022RiskLifecycleVariant(
        label="scale_0_50_min_stop_20x_hold_1",
        hold_h4_bars=1,
        position_scale=0.50,
        min_stop_distance_spread_ratio=20.0,
    ),
    H022RiskLifecycleVariant(
        label="scale_0_50_min_stop_20x_hold_2",
        hold_h4_bars=2,
        position_scale=0.50,
        min_stop_distance_spread_ratio=20.0,
    ),
    H022RiskLifecycleVariant(
        label="scale_0_25_min_stop_50x_hold_1",
        hold_h4_bars=1,
        position_scale=0.25,
        min_stop_distance_spread_ratio=50.0,
    ),
    H022RiskLifecycleVariant(
        label="scale_0_25_min_stop_50x_hold_2",
        hold_h4_bars=2,
        position_scale=0.25,
        min_stop_distance_spread_ratio=50.0,
    ),
)


def apply_h022_risk_lifecycle_transform(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    variant: H022RiskLifecycleVariant,
) -> H017Result:
    """Apply ex-ante risk/lifecycle signal transform.

    Rules:
    - Scale all non-flat intended positions by ``position_scale``.
    - Optionally skip positions whose decision-time raw stop distance is less
      than ``min_stop_distance_spread_ratio`` times the modeled spread.
    - Do not change stops, costs, H018 hard guards, symbols, or timeframes.
    """
    if variant.hold_h4_bars <= 0:
        raise ValueError("hold_h4_bars must be positive")
    if variant.position_scale <= 0.0 or variant.position_scale > 1.0:
        raise ValueError("position_scale must be in the interval (0, 1]")
    if (
        variant.min_stop_distance_spread_ratio is not None
        and variant.min_stop_distance_spread_ratio <= 0.0
    ):
        raise ValueError("min_stop_distance_spread_ratio must be positive when provided")

    positions = h017_result.positions.copy(deep=True)
    decision_index = _require_utc_index(positions.index, name="positions.index")
    positions.index = decision_index

    h4_by_symbol = {
        "USDJPY": _with_utc_index(usdjpy_h4),
        "XAUUSD": _with_utc_index(xauusd_h4),
    }

    for location, decision_time in enumerate(decision_index):
        if location + 1 >= len(decision_index):
            positions.loc[decision_time, :] = 0.0
            continue

        entry_time = pd.Timestamp(decision_index[location + 1]).tz_convert("UTC")

        for symbol in _SYMBOLS:
            raw_position = float(positions.at[decision_time, symbol])
            if raw_position == 0.0:
                continue

            if entry_time not in h4_by_symbol[symbol].index:
                positions.at[decision_time, symbol] = 0.0
                continue

            if variant.min_stop_distance_spread_ratio is not None:
                stop_frame = h017_result.stops_long if raw_position > 0.0 else h017_result.stops_short
                stop_price = float(stop_frame.at[decision_time, symbol])
                entry_open = float(h4_by_symbol[symbol].at[entry_time, "open"])
                spread_price = _SPREAD_PRICE_BY_SYMBOL[symbol]
                stop_distance_spread_ratio = abs(entry_open - stop_price) / spread_price

                if stop_distance_spread_ratio < variant.min_stop_distance_spread_ratio:
                    positions.at[decision_time, symbol] = 0.0
                    continue

            positions.at[decision_time, symbol] = raw_position * variant.position_scale

    return H017Result(
        positions=positions,
        stops_long=h017_result.stops_long.copy(deep=True),
        stops_short=h017_result.stops_short.copy(deep=True),
        signals=h017_result.signals.copy(deep=True),
        vol_multipliers=h017_result.vol_multipliers.copy(deep=True),
        heat_multipliers=h017_result.heat_multipliers.copy(deep=True),
        heat_pre=h017_result.heat_pre.copy(deep=True),
        heat_post=h017_result.heat_post.copy(deep=True),
        heat_binding=h017_result.heat_binding.copy(deep=True),
    )


def backtest_h022_risk_lifecycle_variant(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Iterable[pd.Timestamp],
    variant: H022RiskLifecycleVariant,
    starting_equity_usd: float = 10_000.0,
) -> H022RiskLifecycleBacktestResult:
    transformed = apply_h022_risk_lifecycle_transform(
        h017_result=h017_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        variant=variant,
    )

    lifecycle_result = backtest_fixed_lifecycle_from_result(
        h017_result=transformed,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars=variant.hold_h4_bars,
        starting_equity_usd=starting_equity_usd,
    )

    return H022RiskLifecycleBacktestResult(
        variant=variant,
        transformed_signal=transformed,
        lifecycle_result=lifecycle_result,
    )


def summarize_h022_result(result: H022RiskLifecycleBacktestResult) -> H022RiskLifecycleSummary:
    lifecycle_summary = summarize_lifecycle_backtest(result.lifecycle_result)
    variant = result.variant

    return H022RiskLifecycleSummary(
        label=variant.label,
        hold_h4_bars=variant.hold_h4_bars,
        position_scale=variant.position_scale,
        min_stop_distance_spread_ratio=variant.min_stop_distance_spread_ratio,
        accepted_entry_count=lifecycle_summary.accepted_entry_count,
        executed_entry_count=lifecycle_summary.executed_entry_count,
        skipped_entry_count=lifecycle_summary.skipped_entry_count,
        lifecycle_skip_count=lifecycle_summary.lifecycle_skip_count,
        incomplete_horizon_skip_count=lifecycle_summary.incomplete_horizon_skip_count,
        flat_entry_count=lifecycle_summary.flat_entry_count,
        fill_count=lifecycle_summary.fill_count,
        stop_count=lifecycle_summary.stop_count,
        stop_rate=lifecycle_summary.stop_rate,
        ending_equity_usd=lifecycle_summary.ending_equity_usd,
        total_pnl_usd=lifecycle_summary.total_pnl_usd,
        total_return=lifecycle_summary.total_return,
        max_drawdown=lifecycle_summary.max_drawdown,
        win_rate=lifecycle_summary.win_rate,
        profit_factor=lifecycle_summary.profit_factor,
        fill_return_sharpe=lifecycle_summary.fill_return_sharpe,
    )


def summarize_h022_results(
    results: Sequence[H022RiskLifecycleBacktestResult],
) -> tuple[H022RiskLifecycleSummary, ...]:
    return tuple(summarize_h022_result(result) for result in results)


def format_h022_summary_table(
    rows: Sequence[H022RiskLifecycleSummary],
    *,
    title: str = "H022 risk/lifecycle variant summary",
) -> str:
    lines = [title]
    if not rows:
        lines.append("(no rows)")
        return "\n".join(lines)

    lines.append(
        "label | hold_h4_bars | position_scale | min_stop_distance_spread_ratio | "
        "accepted | executed | skipped | lifecycle_skips | incomplete_horizon_skips | "
        "flat_entries | fills | stops | stop_rate | ending_equity_usd | total_pnl_usd | "
        "total_return | max_drawdown | win_rate | profit_factor | fill_return_sharpe"
    )

    for row in rows:
        lines.append(
            " | ".join(
                [
                    row.label,
                    str(row.hold_h4_bars),
                    _format_float(row.position_scale),
                    _format_optional_float(row.min_stop_distance_spread_ratio),
                    str(row.accepted_entry_count),
                    str(row.executed_entry_count),
                    str(row.skipped_entry_count),
                    str(row.lifecycle_skip_count),
                    str(row.incomplete_horizon_skip_count),
                    str(row.flat_entry_count),
                    str(row.fill_count),
                    str(row.stop_count),
                    _format_percent(row.stop_rate),
                    _format_money(row.ending_equity_usd),
                    _format_money(row.total_pnl_usd),
                    _format_percent(row.total_return),
                    _format_percent(row.max_drawdown),
                    _format_percent(row.win_rate),
                    _format_float(row.profit_factor),
                    _format_float(row.fill_return_sharpe),
                ]
            )
        )

    return "\n".join(lines)


def main() -> None:
    print("H022 risk/lifecycle variant diagnostic")
    print("=" * 45)
    print("Research diagnostic only. No live trading. No Phase 4.")
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

    assessment = assess_common_complete_h4_m1_windows(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(f"accepted_count mismatch: {assessment.accepted_count}")

    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print("Building H020 bridge shim...")
    print()

    shim = run_h020_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4.bars,
        xauusd_ohlcv=xauusd_h4.bars,
    )

    results = tuple(
        backtest_h022_risk_lifecycle_variant(
            h017_result=shim,
            usdjpy_h4=usdjpy_h4.bars,
            xauusd_h4=xauusd_h4.bars,
            usdjpy_m1=usdjpy_m1.bars,
            xauusd_m1=xauusd_m1.bars,
            accepted_entry_times=assessment.accepted_timestamps,
            variant=variant,
            starting_equity_usd=10_000.0,
        )
        for variant in DEFAULT_H022_VARIANTS
    )

    summaries = summarize_h022_results(results)
    print(format_h022_summary_table(summaries))
    print()

    for result in results:
        lifecycle_result = result.lifecycle_result
        print("=" * 80)
        print(f"Variant {result.variant.label} detail")
        print("=" * 80)
        print(format_group_summary_table(
            summarize_fills_by_field(lifecycle_result.fills, field="symbol"),
            title="By symbol",
        ))
        print()
        print(format_group_summary_table(
            summarize_fills_by_field(lifecycle_result.fills, field="side"),
            title="By side",
        ))
        print()
        print(format_group_summary_table(
            summarize_fills_by_year(lifecycle_result.fills),
            title="By exit year",
        ))
        print()
        print(format_group_summary_table(
            summarize_chronological_halves(lifecycle_result.fills),
            title="Chronological halves",
        ))
        print()
        print(format_group_summary_table(
            summarize_chronological_thirds(lifecycle_result.fills),
            title="Chronological thirds",
        ))
        print()

    print("Pre-registered interpretation reminder:")
    print("- A variant is not promotable unless it clears the H022 seed pass criteria.")
    print("- This diagnostic does not approve demo trading, live trading, or Phase 4.")


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


def _format_optional_float(value: float | None) -> str:
    if value is None:
        return "none"
    return _format_float(value)


def _format_float(value: float) -> str:
    if isnan(value):
        return "nan"
    if value == float("inf"):
        return "inf"
    return f"{value:.6f}"


def _format_money(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.2f}"


def _format_percent(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.4%}"


if __name__ == "__main__":
    main()
