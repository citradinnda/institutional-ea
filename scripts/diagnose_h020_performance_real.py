"""Lightweight H020 strict event performance diagnostic.

This script is diagnostic-only:
- not live-trading approval,
- not Phase 4 approval,
- not strategy promotion by itself.

It reuses the strict H020 broker-native event pipeline, then reports account-level
performance from the returned PortfolioResult.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Any

import pandas as pd

from quantcore.backtest.portfolio import fill_pnl_usd
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)
from quantcore.backtest.h020_strict_event import backtest_h020_strict_event
from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files


@dataclass(frozen=True)
class H020PerformanceSummary:
    accepted_entry_count: int
    executed_entry_count: int
    skipped_entry_count: int
    fill_count: int
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


def summarize_h020_performance(strict_result: Any) -> H020PerformanceSummary:
    """Summarize an H020 strict event result without rerunning validation."""
    backtest = strict_result.backtest
    portfolio = backtest.portfolio
    fills = tuple(backtest.fills)

    pnl_values = [fill_pnl_usd(fill=fill) for fill in fills]
    winning = [pnl for pnl in pnl_values if pnl > 0.0]
    losing = [pnl for pnl in pnl_values if pnl < 0.0]
    flat = [pnl for pnl in pnl_values if pnl == 0.0]

    gross_profit = float(sum(winning))
    gross_loss = float(sum(losing))
    profit_factor = gross_profit / abs(gross_loss) if gross_loss < 0.0 else float("nan")

    returns = portfolio.returns
    mean_fill_return = float(returns.mean()) if len(returns) else float("nan")
    median_fill_return = float(returns.median()) if len(returns) else float("nan")
    fill_return_sharpe = _return_sharpe(returns)

    starting_equity = float(portfolio.starting_equity_usd)
    ending_equity = float(portfolio.ending_equity_usd)
    total_pnl = ending_equity - starting_equity

    return H020PerformanceSummary(
        accepted_entry_count=int(strict_result.accepted_entry_count),
        executed_entry_count=int(strict_result.executed_entry_count),
        skipped_entry_count=int(strict_result.skipped_entry_count),
        fill_count=len(fills),
        starting_equity_usd=starting_equity,
        ending_equity_usd=ending_equity,
        total_pnl_usd=total_pnl,
        total_return=total_pnl / starting_equity,
        max_drawdown=float(portfolio.max_drawdown),
        winning_fill_count=len(winning),
        losing_fill_count=len(losing),
        flat_fill_count=len(flat),
        win_rate=len(winning) / len(fills) if fills else float("nan"),
        gross_profit_usd=gross_profit,
        gross_loss_usd=gross_loss,
        profit_factor=profit_factor,
        mean_fill_return=mean_fill_return,
        median_fill_return=median_fill_return,
        fill_return_sharpe=fill_return_sharpe,
    )


def format_h020_performance_summary(summary: H020PerformanceSummary) -> str:
    """Return a compact human-readable diagnostic report."""
    return "\n".join(
        [
            "H020 strict event performance diagnostic",
            "=" * 60,
            f"accepted_entry_count: {summary.accepted_entry_count}",
            f"executed_entry_count: {summary.executed_entry_count}",
            f"skipped_entry_count: {summary.skipped_entry_count}",
            f"fill_count: {summary.fill_count}",
            "",
            f"starting_equity_usd: {summary.starting_equity_usd:.2f}",
            f"ending_equity_usd: {summary.ending_equity_usd:.2f}",
            f"total_pnl_usd: {summary.total_pnl_usd:.2f}",
            f"total_return: {summary.total_return:.4%}",
            f"max_drawdown: {summary.max_drawdown:.4%}",
            "",
            f"winning_fill_count: {summary.winning_fill_count}",
            f"losing_fill_count: {summary.losing_fill_count}",
            f"flat_fill_count: {summary.flat_fill_count}",
            f"win_rate: {_format_optional_percent(summary.win_rate)}",
            f"gross_profit_usd: {summary.gross_profit_usd:.2f}",
            f"gross_loss_usd: {summary.gross_loss_usd:.2f}",
            f"profit_factor: {_format_optional_float(summary.profit_factor)}",
            "",
            f"mean_fill_return: {_format_optional_percent(summary.mean_fill_return)}",
            f"median_fill_return: {_format_optional_percent(summary.median_fill_return)}",
            f"fill_return_sharpe: {_format_optional_float(summary.fill_return_sharpe)}",
            "",
            "Verdict reminder: this is performance diagnostics only.",
            "No live trading is approved. Phase 4 is not approved.",
        ]
    )


def main() -> None:
    print("H020 strict expanded broker-native performance diagnostic")
    print("=" * 60)

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
        cache_path=USDJPY_H4_PATH.parents[2]
        / "cache"
        / "strict_usdjpy_xauusd_h4_m1_bridge_windows.json",
        cache_key=cache_key,
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
    print("Running strict H020 event backtest...")

    result = backtest_h020_strict_event(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
        starting_equity_usd=10000.0,
    )

    print()
    print(format_h020_performance_summary(summarize_h020_performance(result)))


def _return_sharpe(returns: pd.Series) -> float:
    clean = returns.dropna()
    if len(clean) < 2:
        return float("nan")

    std = float(clean.std(ddof=0))
    if std == 0.0:
        return float("nan")

    return float(clean.mean()) / std


def _format_optional_float(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.6f}"


def _format_optional_percent(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.4%}"


if __name__ == "__main__":
    main()
