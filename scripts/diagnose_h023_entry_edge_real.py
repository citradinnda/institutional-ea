"""H023 entry-edge falsification diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

H023 asks whether the current H020 bridge-compatible entry source has durable
forward directional value before additional stop/lifecycle engineering is
attempted. It intentionally avoids H021 positive time/session bucket rules.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, Sequence

import pandas as pd

from quantcore.backtest.h017_event import (
    _build_symbol_interval_candidate,
    _validate_maximum_portfolio_usd_gross_leverage,
)
from quantcore.backtest.portfolio import build_portfolio_result, fill_pnl_usd
from quantcore.data.bridge_windows import assess_common_complete_h4_m1_windows
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h020_runner import run_h020_bridge_shim
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    H021FixedLifecycleBacktestResult,
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

DEFAULT_H023_FORWARD_HORIZONS: tuple[int, ...] = (1, 2, 3, 4, 6, 8)
_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class H023EntryEdgeResult:
    forward_h4_bars: int
    accepted_entry_count: int
    executed_entry_count: int
    skipped_entry_count: int
    incomplete_horizon_skip_count: int
    flat_entry_count: int
    fills: tuple
    portfolio: object


@dataclass(frozen=True)
class H023EntryEdgeSummary:
    forward_h4_bars: int
    accepted_entry_count: int
    executed_entry_count: int
    skipped_entry_count: int
    incomplete_horizon_skip_count: int
    flat_entry_count: int
    fill_count: int
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


def backtest_h023_entry_edge_forward_horizon(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Iterable[pd.Timestamp],
    forward_h4_bars: int,
    starting_equity_usd: float = 10_000.0,
) -> H023EntryEdgeResult:
    """Measure fixed-horizon forward entry outcomes without lifecycle stops.

    Entry timing matches the bridge convention:
    - decision at H4 timestamp t,
    - entry at next H4 timestamp t+1,
    - forced exit at entry_time + forward_h4_bars H4 bars.

    This diagnostic still uses the H020/H017 risk geometry to size positions
    and preserve H018 hard guards, but the simulated forward outcome does not
    exit early on the chandelier stop. That isolates directional entry edge
    from the existing stop/lifecycle contract.
    """
    if forward_h4_bars <= 0:
        raise ValueError("forward_h4_bars must be positive")
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

    fills = []
    current_equity = float(starting_equity_usd)
    executed_entry_count = 0
    incomplete_horizon_skip_count = 0
    flat_entry_count = 0

    for entry_time in accepted:
        if entry_time not in decision_index:
            incomplete_horizon_skip_count += 1
            continue

        entry_location = decision_index.get_loc(entry_time)
        if not isinstance(entry_location, int):
            raise ValueError(f"non-unique entry_time in decision index: {entry_time}")

        decision_location = entry_location - 1
        forced_exit_location = entry_location + forward_h4_bars

        if decision_location < 0 or forced_exit_location >= len(decision_index):
            incomplete_horizon_skip_count += 1
            continue

        horizon_times = tuple(
            pd.Timestamp(decision_index[entry_location + offset]).tz_convert("UTC")
            for offset in range(forward_h4_bars)
        )
        if any(timestamp not in accepted_set for timestamp in horizon_times):
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
            fill = _build_h023_forward_fill(
                candidate=candidate,
                m1_bars=m1_by_symbol[candidate.symbol],
            )
            fills.append(fill)
            interval_pnl_usd += fill_pnl_usd(fill=fill)

        current_equity += interval_pnl_usd
        if current_equity <= 0.0:
            raise RuntimeError(
                "H023 entry-edge diagnostic reached non-positive equity: "
                f"entry_time={entry_time}, forced_exit_time={forced_exit_time}, "
                f"ending_equity_usd={current_equity:.2f}"
            )

        executed_entry_count += 1

    sorted_fills = tuple(sorted(fills, key=lambda fill: fill.exit_time_utc))
    portfolio = build_portfolio_result(
        fills=sorted_fills,
        starting_equity_usd=starting_equity_usd,
    )

    accepted_entry_count = len(accepted)
    skipped_entry_count = accepted_entry_count - executed_entry_count

    return H023EntryEdgeResult(
        forward_h4_bars=forward_h4_bars,
        accepted_entry_count=accepted_entry_count,
        executed_entry_count=executed_entry_count,
        skipped_entry_count=skipped_entry_count,
        incomplete_horizon_skip_count=incomplete_horizon_skip_count,
        flat_entry_count=flat_entry_count,
        fills=sorted_fills,
        portfolio=portfolio,
    )


def summarize_h023_entry_edge_result(result: H023EntryEdgeResult) -> H023EntryEdgeSummary:
    lifecycle_like = H021FixedLifecycleBacktestResult(
        hold_h4_bars=result.forward_h4_bars,
        accepted_entry_count=result.accepted_entry_count,
        executed_entry_count=result.executed_entry_count,
        skipped_entry_count=result.skipped_entry_count,
        lifecycle_skip_count=0,
        incomplete_horizon_skip_count=result.incomplete_horizon_skip_count,
        flat_entry_count=result.flat_entry_count,
        fills=result.fills,
        portfolio=result.portfolio,
    )
    summary = summarize_lifecycle_backtest(lifecycle_like)

    return H023EntryEdgeSummary(
        forward_h4_bars=result.forward_h4_bars,
        accepted_entry_count=summary.accepted_entry_count,
        executed_entry_count=summary.executed_entry_count,
        skipped_entry_count=summary.skipped_entry_count,
        incomplete_horizon_skip_count=summary.incomplete_horizon_skip_count,
        flat_entry_count=summary.flat_entry_count,
        fill_count=summary.fill_count,
        ending_equity_usd=summary.ending_equity_usd,
        total_pnl_usd=summary.total_pnl_usd,
        total_return=summary.total_return,
        max_drawdown=summary.max_drawdown,
        winning_fill_count=summary.winning_fill_count,
        losing_fill_count=summary.losing_fill_count,
        flat_fill_count=summary.flat_fill_count,
        win_rate=summary.win_rate,
        gross_profit_usd=summary.gross_profit_usd,
        gross_loss_usd=summary.gross_loss_usd,
        profit_factor=summary.profit_factor,
        mean_fill_return=summary.mean_fill_return,
        median_fill_return=summary.median_fill_return,
        fill_return_sharpe=summary.fill_return_sharpe,
    )


def summarize_h023_entry_edge_results(
    results: Sequence[H023EntryEdgeResult],
) -> tuple[H023EntryEdgeSummary, ...]:
    return tuple(summarize_h023_entry_edge_result(result) for result in results)


def format_h023_summary_table(rows: Sequence[H023EntryEdgeSummary]) -> str:
    header = (
        "Horizon    Accepted    Executed    Skipped    Fills    Ending equity    "
        "PnL    Return    Max DD    PF    Win rate"
    )
    lines = [header]
    for row in rows:
        lines.append(
            f"{row.forward_h4_bars} H4    "
            f"{row.accepted_entry_count}    "
            f"{row.executed_entry_count}    "
            f"{row.skipped_entry_count}    "
            f"{row.fill_count}    "
            f"{_format_money(row.ending_equity_usd)}    "
            f"{_format_money(row.total_pnl_usd)}    "
            f"{_format_percent(row.total_return)}    "
            f"{_format_percent(row.max_drawdown)}    "
            f"{_format_float(row.profit_factor)}    "
            f"{_format_percent(row.win_rate)}"
        )
    return "\n".join(lines)

def format_h023_group_reports(result: H023EntryEdgeResult) -> str:
    """Format all H023 split reports with existing H021 group helpers."""
    sections = [
        format_group_summary_table(
            summarize_fills_by_field(result.fills, field="symbol"),
            title="By symbol:",
        ),
        format_group_summary_table(
            summarize_fills_by_field(result.fills, field="side"),
            title="By side:",
        ),
        format_group_summary_table(
            summarize_chronological_halves(result.fills),
            title="Chronological halves:",
        ),
        format_group_summary_table(
            summarize_chronological_thirds(result.fills),
            title="Chronological thirds:",
        ),
        format_group_summary_table(
            summarize_fills_by_year(result.fills),
            title="By calendar year:",
        ),
    ]
    return "\n\n".join(sections)

def assess_h023_bridge_windows(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    expected_m1_bars_per_h4: int = EXPECTED_M1_BARS_PER_H4,
    expected_h4_delta: pd.Timedelta = EXPECTED_H4_DELTA,
):
    """Assess strict bridge windows using the existing USDJPY/XAUUSD API."""
    return assess_common_complete_h4_m1_windows(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        expected_m1_bars_per_h4=expected_m1_bars_per_h4,
        expected_h4_delta=expected_h4_delta,
    )

def h023_signal_source_from_h020_bridge_shim_result(result: H017Result) -> H017Result:
    """Document that run_h020_bridge_shim returns H017Result directly."""
    if not isinstance(result, H017Result):
        raise TypeError("run_h020_bridge_shim result must be an H017Result")
    return result


def main() -> None:
    print("H023 entry-edge falsification diagnostic")
    print("=" * 43)
    print("Research only. Not demo/live/Phase 4 approval.")
    print()

    require_existing_files(
        [
            USDJPY_H4_PATH,
            USDJPY_M1_PATH,
            XAUUSD_H4_PATH,
            XAUUSD_M1_PATH,
        ]
    )

    usdjpy_h4 = load_mt5_csv(USDJPY_H4_PATH)
    usdjpy_m1 = load_mt5_csv(USDJPY_M1_PATH)
    xauusd_h4 = load_mt5_csv(XAUUSD_H4_PATH)
    xauusd_m1 = load_mt5_csv(XAUUSD_M1_PATH)

    assessment = assess_h023_bridge_windows(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_h4_delta=EXPECTED_H4_DELTA,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
    )
    accepted_entry_times = assessment.accepted_timestamps

    print(f"accepted bridge-windows: {len(accepted_entry_times)}")
    if len(accepted_entry_times) != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(
            f"expected {EXPECTED_ACCEPTED_COUNT} accepted windows, "
            f"got {len(accepted_entry_times)}"
        )

    h020_signal = h023_signal_source_from_h020_bridge_shim_result(
        run_h020_bridge_shim(
            usdjpy_ohlcv=usdjpy_h4.bars,
            xauusd_ohlcv=xauusd_h4.bars,
        )
    )

    results = tuple(
        backtest_h023_entry_edge_forward_horizon(
            h017_result=h020_signal,
            usdjpy_h4=usdjpy_h4.bars,
            xauusd_h4=xauusd_h4.bars,
            usdjpy_m1=usdjpy_m1.bars,
            xauusd_m1=xauusd_m1.bars,
            accepted_entry_times=accepted_entry_times,
            forward_h4_bars=horizon,
        )
        for horizon in DEFAULT_H023_FORWARD_HORIZONS
    )
    summaries = summarize_h023_entry_edge_results(results)

    print()
    print(format_h023_summary_table(summaries))

    for result in results:
        print()
        print(f"=== {result.forward_h4_bars} H4 forward horizon ===")
        print(format_h023_group_reports(result))


def _build_h023_forward_fill(*, candidate, m1_bars: pd.DataFrame):
    """Build a fixed-horizon no-stop fill using existing cost conventions."""
    from dataclasses import replace

    from quantcore.backtest.cost_model import price_with_execution_costs
    from quantcore.backtest.fill_engine import simulate_bracket_trade

    entry_cost = price_with_execution_costs(
        symbol=candidate.symbol,
        side=candidate.side,
        action="entry",
        raw_price=candidate.entry_raw_price,
        lots=candidate.position_size.lots,
    )

    raw_fill = simulate_bracket_trade(
        symbol=candidate.symbol,
        side=candidate.side,
        entry_time_utc=candidate.entry_time,
        entry_price=entry_cost.fill_price,
        lots=candidate.position_size.lots,
        m1_bars=m1_bars,
        stop_price=None,
        take_profit_price=None,
        forced_exit_time_utc=candidate.forced_exit_time,
        forced_exit_price=candidate.forced_exit_raw_price,
        contract_size=candidate.instrument_spec.contract_size,
        commission=0.0,
        stop_slippage=0.0,
    )

    exit_cost = price_with_execution_costs(
        symbol=candidate.symbol,
        side=candidate.side,
        action="exit",
        raw_price=raw_fill.exit_price,
        lots=candidate.position_size.lots,
    )

    adjusted_fill = simulate_bracket_trade(
        symbol=candidate.symbol,
        side=candidate.side,
        entry_time_utc=candidate.entry_time,
        entry_price=entry_cost.fill_price,
        lots=candidate.position_size.lots,
        m1_bars=m1_bars,
        stop_price=None,
        take_profit_price=None,
        forced_exit_time_utc=candidate.forced_exit_time,
        forced_exit_price=exit_cost.fill_price,
        contract_size=candidate.instrument_spec.contract_size,
        commission=entry_cost.commission_usd + exit_cost.commission_usd,
        stop_slippage=0.0,
    )

    return replace(
        adjusted_fill,
        exit_reason="signal_flip",
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
    result = index.tz_convert("UTC")
    if not result.is_monotonic_increasing:
        raise ValueError(f"{name} must be sorted ascending")
    if result.has_duplicates:
        raise ValueError(f"{name} must not contain duplicates")
    return result


def _format_float(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.6f}"


def _format_money(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"${value:.2f}"


def _format_percent(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.4%}"


if __name__ == "__main__":
    main()
