import pandas as pd
import pytest

from quantcore.backtest.fill_engine import Fill
from scripts.diagnose_h021_trade_decomposition_real import (
    format_decomposition_table,
    summarize_fills_by_fields,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _xauusd_fill(
    *,
    side: str,
    exit_reason: str,
    pnl_quote: float,
    commission: float,
    exit_hour: int,
) -> Fill:
    return Fill(
        symbol="XAUUSD",
        side=side,
        entry_time_utc=_utc(f"2024-01-01 {exit_hour - 4:02d}:00"),
        entry_price=2000.0,
        exit_time_utc=_utc(f"2024-01-01 {exit_hour:02d}:00"),
        exit_price=2001.0,
        lots=1.0,
        pnl_quote=pnl_quote,
        commission=commission,
        slippage=0.0,
        exit_reason=exit_reason,
    )


def test_summarize_fills_by_symbol_side_and_exit_reason():
    fills = (
        _xauusd_fill(side="buy", exit_reason="signal_flip", pnl_quote=110.0, commission=10.0, exit_hour=4),
        _xauusd_fill(side="buy", exit_reason="stop_loss", pnl_quote=-40.0, commission=10.0, exit_hour=8),
        _xauusd_fill(side="sell", exit_reason="stop_loss", pnl_quote=-20.0, commission=10.0, exit_hour=12),
    )

    rows = summarize_fills_by_fields(
        fills,
        group_fields=("symbol", "side", "exit_reason"),
    )

    by_group = {row.group: row for row in rows}

    buy_signal = by_group[
        (("symbol", "XAUUSD"), ("side", "buy"), ("exit_reason", "signal_flip"))
    ]
    assert buy_signal.fill_count == 1
    assert buy_signal.winning_fill_count == 1
    assert buy_signal.total_pnl_usd == pytest.approx(100.0)
    assert buy_signal.profit_factor != buy_signal.profit_factor

    buy_stop = by_group[
        (("symbol", "XAUUSD"), ("side", "buy"), ("exit_reason", "stop_loss"))
    ]
    assert buy_stop.fill_count == 1
    assert buy_stop.losing_fill_count == 1
    assert buy_stop.total_pnl_usd == pytest.approx(-50.0)

    sell_stop = by_group[
        (("symbol", "XAUUSD"), ("side", "sell"), ("exit_reason", "stop_loss"))
    ]
    assert sell_stop.fill_count == 1
    assert sell_stop.losing_fill_count == 1
    assert sell_stop.total_pnl_usd == pytest.approx(-30.0)


def test_summarize_fills_by_symbol_aggregates_after_cost_pnl():
    fills = (
        _xauusd_fill(side="buy", exit_reason="signal_flip", pnl_quote=110.0, commission=10.0, exit_hour=4),
        _xauusd_fill(side="sell", exit_reason="stop_loss", pnl_quote=-20.0, commission=10.0, exit_hour=8),
    )

    rows = summarize_fills_by_fields(fills, group_fields=("symbol",))

    assert len(rows) == 1
    row = rows[0]
    assert row.group == (("symbol", "XAUUSD"),)
    assert row.fill_count == 2
    assert row.winning_fill_count == 1
    assert row.losing_fill_count == 1
    assert row.win_rate == pytest.approx(0.5)
    assert row.total_pnl_usd == pytest.approx(70.0)
    assert row.gross_profit_usd == pytest.approx(100.0)
    assert row.gross_loss_usd == pytest.approx(-30.0)
    assert row.profit_factor == pytest.approx(100.0 / 30.0)


def test_summarize_fills_rejects_unknown_group_field():
    fill = _xauusd_fill(
        side="buy",
        exit_reason="signal_flip",
        pnl_quote=110.0,
        commission=10.0,
        exit_hour=4,
    )

    with pytest.raises(ValueError, match="unsupported group field"):
        summarize_fills_by_fields((fill,), group_fields=("session",))


def test_format_decomposition_table_keeps_diagnostic_warning_visible():
    fills = (
        _xauusd_fill(side="buy", exit_reason="signal_flip", pnl_quote=110.0, commission=10.0, exit_hour=4),
    )
    rows = summarize_fills_by_fields(fills, group_fields=("symbol",))

    table = format_decomposition_table(rows, title="By symbol")

    assert "By symbol" in table
    assert "symbol=XAUUSD" in table
    assert "total_pnl_usd" in table
    assert "100.00" in table
