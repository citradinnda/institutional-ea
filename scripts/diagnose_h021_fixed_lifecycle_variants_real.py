"""H021 fixed lifecycle variant diagnostic.

Pre-registered diagnostic for comparing complete fixed H4 lifecycle variants.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

The diagnostic uses the H020 bridge shim as the signal source, preserves H018
hard execution guards, and runs non-overlapping fixed lifecycle portfolio
backtests for hold horizons such as 1/2/3/4 H4 bars.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, Mapping, Sequence

import pandas as pd

from quantcore.backtest.fill_engine import Fill
from quantcore.backtest.h017_event import (
    _build_symbol_interval_candidate,
    _build_symbol_interval_fill,
    _validate_maximum_portfolio_usd_gross_leverage,
)
from quantcore.backtest.portfolio import PortfolioResult, build_portfolio_result, fill_pnl_usd
from quantcore.data.bridge_windows import assess_common_complete_h4_m1_windows
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h020_runner import run_h020_bridge_shim
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)

DEFAULT_HOLD_H4_BARS: tuple[int, ...] = (1, 2, 3, 4)
_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class H021FixedLifecycleBacktestResult:
    hold_h4_bars: int
    accepted_entry_count: int
    executed_entry_count: int
    skipped_entry_count: int
    lifecycle_skip_count: int
    incomplete_horizon_skip_count: int
    flat_entry_count: int
    fills: tuple[Fill, ...]
    portfolio: PortfolioResult


@dataclass(frozen=True)
class H021FixedLifecycleSummary:
    hold_h4_bars: int
    accepted_entry_count: int
    executed_entry_count: int
    skipped_entry_count: int
    lifecycle_skip_count: int
    incomplete_horizon_skip_count: int
    flat_entry_count: int
    fill_count: int
    stop_count: int
    stop_rate: float
    starting_equity_usd: float
    ending_equity_usd: float
    total_pnl_usd: float
    total_return: float
    max_drawdown: float
    winning_fill_count: int
    losing_fill_count: int
    flat_fill_count: int
    win_rate: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float
    mean_fill_return: float
    median_fill_return: float
    fill_return_sharpe: float


@dataclass(frozen=True)
class H021GroupSummary:
    label: str
    fill_count: int
    stop_count: int
    stop_rate: float
    total_pnl_usd: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float
    win_rate: float


def backtest_fixed_lifecycle_from_result(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Iterable[pd.Timestamp],
    hold_h4_bars: int,
    starting_equity_usd: float = 10_000.0,
) -> H021FixedLifecycleBacktestResult:
    """Run a non-overlapping fixed-horizon lifecycle portfolio backtest.

    Entry timing:
    - decision at H4 timestamp t,
    - entry at next H4 timestamp t+1,
    - forced exit at entry_time + hold_h4_bars H4 bars,
    - M1 stops can exit earlier.

    Non-overlap rule:
    - after opening a lifecycle at entry_time, no new lifecycle can open before
      its forced_exit_time.
    """
    if hold_h4_bars <= 0:
        raise ValueError("hold_h4_bars must be positive")
    if starting_equity_usd <= 0.0:
        raise ValueError("starting_equity_usd must be positive")

    h4_by_symbol = {
        "USDJPY": _with_utc_index(usdjpy_h4),
        "XAUUSD": _with_utc_index(xauusd_h4),
    }
    m1_by_symbol = {
        "USDJPY": _with_utc_index(usdjpy_m1),
        "XAUUSD": _with_utc_index(xauusd_m1),
    }

    decision_index = _require_utc_index(h017_result.positions.index, name="positions.index")
    accepted = tuple(sorted(pd.Timestamp(ts).tz_convert("UTC") for ts in accepted_entry_times))
    accepted_set = set(accepted)

    fills: list[Fill] = []
    current_equity = float(starting_equity_usd)
    next_eligible_entry_time: pd.Timestamp | None = None

    executed_entry_count = 0
    lifecycle_skip_count = 0
    incomplete_horizon_skip_count = 0
    flat_entry_count = 0

    for entry_time in accepted:
        if next_eligible_entry_time is not None and entry_time < next_eligible_entry_time:
            lifecycle_skip_count += 1
            continue

        if entry_time not in decision_index:
            incomplete_horizon_skip_count += 1
            continue

        entry_location = decision_index.get_loc(entry_time)
        if not isinstance(entry_location, int):
            raise ValueError(f"non-unique entry_time in decision index: {entry_time}")

        decision_location = entry_location - 1
        forced_exit_location = entry_location + hold_h4_bars

        if decision_location < 0 or forced_exit_location >= len(decision_index):
            incomplete_horizon_skip_count += 1
            continue

        horizon_times = tuple(decision_index[entry_location + offset] for offset in range(hold_h4_bars))
        if any(pd.Timestamp(ts).tz_convert("UTC") not in accepted_set for ts in horizon_times):
            incomplete_horizon_skip_count += 1
            continue

        decision_time = pd.Timestamp(decision_index[decision_location]).tz_convert("UTC")
        forced_exit_time = pd.Timestamp(decision_index[forced_exit_location]).tz_convert("UTC")
        interval_start_equity = current_equity

        interval_candidates = []
        for symbol in _SYMBOLS:
            candidate = _build_symbol_interval_candidate(
                symbol=symbol,
                h017_result=h017_result,
                h4_bars=h4_by_symbol[symbol],
                decision_time=decision_time,
                entry_time=entry_time,
                forced_exit_time=forced_exit_time,
                equity_usd=interval_start_equity,
            )
            if candidate is not None:
                interval_candidates.append(candidate)

        if not interval_candidates:
            flat_entry_count += 1
            continue

        _validate_maximum_portfolio_usd_gross_leverage(
            decision_time=decision_time,
            entry_time=entry_time,
            interval_start_equity_usd=interval_start_equity,
            candidates=interval_candidates,
        )

        interval_pnl_usd = 0.0
        for candidate in interval_candidates:
            fill = _build_symbol_interval_fill(
                candidate=candidate,
                m1_bars=m1_by_symbol[candidate.symbol],
                slippage_atr_by_symbol=None,
            )
            fills.append(fill)
            interval_pnl_usd += fill_pnl_usd(fill=fill)

        current_equity += interval_pnl_usd
        if current_equity <= 0.0:
            raise RuntimeError(
                "fixed lifecycle variant reached non-positive equity: "
                f"entry_time={entry_time}, forced_exit_time={forced_exit_time}, "
                f"ending_equity_usd={current_equity:.2f}"
            )

        executed_entry_count += 1
        next_eligible_entry_time = forced_exit_time

    sorted_fills = tuple(sorted(fills, key=lambda fill: fill.exit_time_utc))
    portfolio = build_portfolio_result(
        fills=sorted_fills,
        starting_equity_usd=starting_equity_usd,
    )

    accepted_entry_count = len(accepted)
    skipped_entry_count = accepted_entry_count - executed_entry_count

    return H021FixedLifecycleBacktestResult(
        hold_h4_bars=hold_h4_bars,
        accepted_entry_count=accepted_entry_count,
        executed_entry_count=executed_entry_count,
        skipped_entry_count=skipped_entry_count,
        lifecycle_skip_count=lifecycle_skip_count,
        incomplete_horizon_skip_count=incomplete_horizon_skip_count,
        flat_entry_count=flat_entry_count,
        fills=sorted_fills,
        portfolio=portfolio,
    )


def summarize_lifecycle_backtest(
    result: H021FixedLifecycleBacktestResult,
) -> H021FixedLifecycleSummary:
    fills = tuple(result.fills)
    pnl_values = [fill_pnl_usd(fill=fill) for fill in fills]
    winning = [pnl for pnl in pnl_values if pnl > 0.0]
    losing = [pnl for pnl in pnl_values if pnl < 0.0]
    flat = [pnl for pnl in pnl_values if pnl == 0.0]

    gross_profit = float(sum(winning))
    gross_loss = float(sum(losing))
    stop_count = sum(1 for fill in fills if fill.exit_reason == "stop")

    returns = result.portfolio.returns
    starting_equity = float(result.portfolio.starting_equity_usd)
    ending_equity = float(result.portfolio.ending_equity_usd)
    total_pnl = ending_equity - starting_equity

    return H021FixedLifecycleSummary(
        hold_h4_bars=result.hold_h4_bars,
        accepted_entry_count=result.accepted_entry_count,
        executed_entry_count=result.executed_entry_count,
        skipped_entry_count=result.skipped_entry_count,
        lifecycle_skip_count=result.lifecycle_skip_count,
        incomplete_horizon_skip_count=result.incomplete_horizon_skip_count,
        flat_entry_count=result.flat_entry_count,
        fill_count=len(fills),
        stop_count=stop_count,
        stop_rate=stop_count / len(fills) if fills else float("nan"),
        starting_equity_usd=starting_equity,
        ending_equity_usd=ending_equity,
        total_pnl_usd=total_pnl,
        total_return=total_pnl / starting_equity,
        max_drawdown=float(result.portfolio.max_drawdown),
        winning_fill_count=len(winning),
        losing_fill_count=len(losing),
        flat_fill_count=len(flat),
        win_rate=len(winning) / len(fills) if fills else float("nan"),
        gross_profit_usd=gross_profit,
        gross_loss_usd=gross_loss,
        profit_factor=_profit_factor(gross_profit_usd=gross_profit, gross_loss_usd=gross_loss),
        mean_fill_return=float(returns.mean()) if len(returns) else float("nan"),
        median_fill_return=float(returns.median()) if len(returns) else float("nan"),
        fill_return_sharpe=_return_sharpe(returns),
    )


def summarize_fills_by_field(
    fills: Iterable[Fill],
    *,
    field: str,
) -> tuple[H021GroupSummary, ...]:
    grouped: dict[str, list[Fill]] = {}
    for fill in fills:
        if field == "symbol":
            label = fill.symbol
        elif field == "side":
            label = fill.side
        else:
            raise ValueError("field must be 'symbol' or 'side'")
        grouped.setdefault(label, []).append(fill)

    return tuple(
        _summarize_fill_group(label=label, fills=grouped[label])
        for label in sorted(grouped)
    )


def summarize_fills_by_year(fills: Iterable[Fill]) -> tuple[H021GroupSummary, ...]:
    grouped: dict[str, list[Fill]] = {}
    for fill in fills:
        year = str(pd.Timestamp(fill.exit_time_utc).tz_convert("UTC").year)
        grouped.setdefault(year, []).append(fill)

    return tuple(
        _summarize_fill_group(label=label, fills=grouped[label])
        for label in sorted(grouped)
    )


def summarize_chronological_halves(fills: Sequence[Fill]) -> tuple[H021GroupSummary, ...]:
    ordered = tuple(sorted(fills, key=lambda fill: fill.exit_time_utc))
    split = len(ordered) // 2
    return (
        _summarize_fill_group(label="first_half", fills=ordered[:split]),
        _summarize_fill_group(label="second_half", fills=ordered[split:]),
    )


def summarize_chronological_thirds(fills: Sequence[Fill]) -> tuple[H021GroupSummary, ...]:
    ordered = tuple(sorted(fills, key=lambda fill: fill.exit_time_utc))
    n = len(ordered)
    first_end = n // 3
    second_end = (2 * n) // 3
    return (
        _summarize_fill_group(label="third_1", fills=ordered[:first_end]),
        _summarize_fill_group(label="third_2", fills=ordered[first_end:second_end]),
        _summarize_fill_group(label="third_3", fills=ordered[second_end:]),
    )


def format_lifecycle_summary_table(
    rows: Sequence[H021FixedLifecycleSummary],
    *,
    title: str = "H021 fixed lifecycle variant summary",
) -> str:
    lines = [title]
    if not rows:
        lines.append("(no rows)")
        return "\n".join(lines)

    lines.append(
        "hold_h4_bars | accepted | executed | skipped | lifecycle_skips | "
        "incomplete_horizon_skips | flat_entries | fills | stops | stop_rate | "
        "ending_equity_usd | total_pnl_usd | total_return | max_drawdown | "
        "win_rate | gross_profit_usd | gross_loss_usd | profit_factor | "
        "fill_return_sharpe"
    )

    for row in rows:
        lines.append(
            " | ".join(
                [
                    str(row.hold_h4_bars),
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
                    _format_money(row.gross_profit_usd),
                    _format_money(row.gross_loss_usd),
                    _format_float(row.profit_factor),
                    _format_float(row.fill_return_sharpe),
                ]
            )
        )

    return "\n".join(lines)


def format_group_summary_table(
    rows: Sequence[H021GroupSummary],
    *,
    title: str,
) -> str:
    lines = [title]
    if not rows:
        lines.append("(no rows)")
        return "\n".join(lines)

    lines.append(
        "label | fills | stops | stop_rate | total_pnl_usd | "
        "gross_profit_usd | gross_loss_usd | profit_factor | win_rate"
    )
    for row in rows:
        lines.append(
            " | ".join(
                [
                    row.label,
                    str(row.fill_count),
                    str(row.stop_count),
                    _format_percent(row.stop_rate),
                    _format_money(row.total_pnl_usd),
                    _format_money(row.gross_profit_usd),
                    _format_money(row.gross_loss_usd),
                    _format_float(row.profit_factor),
                    _format_percent(row.win_rate),
                ]
            )
        )
    return "\n".join(lines)


def main() -> None:
    print("H021 fixed lifecycle variant diagnostic")
    print("=" * 45)
    print("Diagnostic only. No live trading. No Phase 4.")
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
        backtest_fixed_lifecycle_from_result(
            h017_result=shim,
            usdjpy_h4=usdjpy_h4.bars,
            xauusd_h4=xauusd_h4.bars,
            usdjpy_m1=usdjpy_m1.bars,
            xauusd_m1=xauusd_m1.bars,
            accepted_entry_times=assessment.accepted_timestamps,
            hold_h4_bars=hold_h4_bars,
            starting_equity_usd=10_000.0,
        )
        for hold_h4_bars in DEFAULT_HOLD_H4_BARS
    )
    summaries = tuple(summarize_lifecycle_backtest(result) for result in results)

    print(format_lifecycle_summary_table(summaries))
    print()

    for result in results:
        print("=" * 80)
        print(f"Hold {result.hold_h4_bars} H4 bars detail")
        print("=" * 80)
        print(format_group_summary_table(
            summarize_fills_by_field(result.fills, field="symbol"),
            title="By symbol",
        ))
        print()
        print(format_group_summary_table(
            summarize_fills_by_field(result.fills, field="side"),
            title="By side",
        ))
        print()
        print(format_group_summary_table(
            summarize_fills_by_year(result.fills),
            title="By exit year",
        ))
        print()
        print(format_group_summary_table(
            summarize_chronological_halves(result.fills),
            title="Chronological halves",
        ))
        print()
        print(format_group_summary_table(
            summarize_chronological_thirds(result.fills),
            title="Chronological thirds",
        ))
        print()

    print("Pre-registered interpretation reminder:")
    print("- A variant is not promotable unless it clears the stated PF, return, drawdown,")
    print("  symbol concentration, and temporal split criteria.")
    print("- Passing this diagnostic would still mean research candidate only.")
    print("- No demo trading is approved. No live trading is approved. Phase 4 is not approved.")


def _summarize_fill_group(*, label: str, fills: Sequence[Fill]) -> H021GroupSummary:
    pnl_values = [fill_pnl_usd(fill=fill) for fill in fills]
    winning = [pnl for pnl in pnl_values if pnl > 0.0]
    losing = [pnl for pnl in pnl_values if pnl < 0.0]
    stop_count = sum(1 for fill in fills if fill.exit_reason == "stop")
    gross_profit = float(sum(winning))
    gross_loss = float(sum(losing))

    return H021GroupSummary(
        label=label,
        fill_count=len(fills),
        stop_count=stop_count,
        stop_rate=stop_count / len(fills) if fills else float("nan"),
        total_pnl_usd=float(sum(pnl_values)),
        gross_profit_usd=gross_profit,
        gross_loss_usd=gross_loss,
        profit_factor=_profit_factor(gross_profit_usd=gross_profit, gross_loss_usd=gross_loss),
        win_rate=len(winning) / len(fills) if fills else float("nan"),
    )


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


def _profit_factor(*, gross_profit_usd: float, gross_loss_usd: float) -> float:
    if gross_loss_usd < 0.0:
        return gross_profit_usd / abs(gross_loss_usd)
    if gross_profit_usd > 0.0:
        return float("inf")
    return float("nan")


def _return_sharpe(returns: pd.Series) -> float:
    clean = returns.dropna()
    if len(clean) < 2:
        return float("nan")
    std = float(clean.std(ddof=0))
    if std == 0.0:
        return float("nan")
    return float(clean.mean()) / std


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
