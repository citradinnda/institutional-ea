from types import SimpleNamespace

import pandas as pd
import pytest

from quantcore.backtest.fill_engine import Fill
from quantcore.backtest.portfolio import build_portfolio_result
from scripts.diagnose_h020_performance_real import (
    format_h020_performance_summary,
    summarize_h020_performance,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def test_summarize_h020_performance_reports_portfolio_metrics():
    fills = (
        Fill(
            symbol="XAUUSD",
            side="buy",
            entry_time_utc=_utc("2024-01-01 00:00"),
            entry_price=2000.0,
            exit_time_utc=_utc("2024-01-01 04:00"),
            exit_price=2001.02,
            lots=1.0,
            pnl_quote=102.0,
            commission=2.0,
            slippage=0.0,
            exit_reason="signal_flip",
        ),
        Fill(
            symbol="XAUUSD",
            side="sell",
            entry_time_utc=_utc("2024-01-01 04:00"),
            entry_price=2001.0,
            exit_time_utc=_utc("2024-01-01 08:00"),
            exit_price=2001.48,
            lots=1.0,
            pnl_quote=-48.0,
            commission=2.0,
            slippage=0.0,
            exit_reason="stop_loss",
        ),
    )
    portfolio = build_portfolio_result(fills=fills, starting_equity_usd=10_000.0)
    strict_result = SimpleNamespace(
        accepted_entry_count=2,
        executed_entry_count=2,
        skipped_entry_count=0,
        backtest=SimpleNamespace(portfolio=portfolio, fills=fills),
    )

    summary = summarize_h020_performance(strict_result)

    assert summary.accepted_entry_count == 2
    assert summary.executed_entry_count == 2
    assert summary.skipped_entry_count == 0
    assert summary.fill_count == 2
    assert summary.starting_equity_usd == pytest.approx(10_000.0)
    assert summary.ending_equity_usd == pytest.approx(10_050.0)
    assert summary.total_pnl_usd == pytest.approx(50.0)
    assert summary.total_return == pytest.approx(0.005)
    assert summary.max_drawdown == pytest.approx(10_050.0 / 10_100.0 - 1.0)
    assert summary.winning_fill_count == 1
    assert summary.losing_fill_count == 1
    assert summary.flat_fill_count == 0
    assert summary.win_rate == pytest.approx(0.5)
    assert summary.gross_profit_usd == pytest.approx(100.0)
    assert summary.gross_loss_usd == pytest.approx(-50.0)
    assert summary.profit_factor == pytest.approx(2.0)


def test_format_h020_performance_summary_preserves_no_live_trading_warning():
    fills = ()
    portfolio = build_portfolio_result(fills=fills, starting_equity_usd=10_000.0)
    strict_result = SimpleNamespace(
        accepted_entry_count=0,
        executed_entry_count=0,
        skipped_entry_count=0,
        backtest=SimpleNamespace(portfolio=portfolio, fills=fills),
    )

    report = format_h020_performance_summary(summarize_h020_performance(strict_result))

    assert "H020 strict event performance diagnostic" in report
    assert "ending_equity_usd: 10000.00" in report
    assert "No live trading is approved. Phase 4 is not approved." in report
