from __future__ import annotations

from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from quantcore.backtest.fill_engine import Fill, simulate_bracket_trade


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _m1_bars(rows: list[tuple[str, float, float, float, float]]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [row[1] for row in rows],
            "high": [row[2] for row in rows],
            "low": [row[3] for row in rows],
            "close": [row[4] for row in rows],
        },
        index=pd.DatetimeIndex([_utc(row[0]) for row in rows]),
    )


def test_fill_is_frozen() -> None:
    fill = Fill(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        exit_time_utc=_utc("2024-01-02 00:01"),
        exit_price=101.0,
        lots=1.0,
        pnl_quote=1.0,
        commission=0.0,
        slippage=0.0,
        exit_reason="tp",
    )

    with pytest.raises(FrozenInstanceError):
        fill.exit_price = 99.0  # type: ignore[misc]


def test_long_take_profit_before_stop() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 100.5, 99.8, 100.2),
            ("2024-01-02 00:01", 100.2, 101.2, 100.1, 101.0),
            ("2024-01-02 00:02", 101.0, 101.1, 98.0, 98.5),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=2.0,
        m1_bars=bars,
        stop_price=99.0,
        take_profit_price=101.0,
        contract_size=10.0,
    )

    assert fill.exit_reason == "tp"
    assert fill.exit_time_utc == _utc("2024-01-02 00:01")
    assert fill.exit_price == pytest.approx(101.0)
    assert fill.pnl_quote == pytest.approx(20.0)


def test_long_stop_before_take_profit() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 100.3, 99.9, 100.1),
            ("2024-01-02 00:01", 100.1, 100.2, 98.8, 99.0),
            ("2024-01-02 00:02", 99.0, 101.5, 98.9, 101.0),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.0,
        m1_bars=bars,
        stop_price=99.0,
        take_profit_price=101.0,
        contract_size=100.0,
    )

    assert fill.exit_reason == "stop"
    assert fill.exit_time_utc == _utc("2024-01-02 00:01")
    assert fill.exit_price == pytest.approx(99.0)
    assert fill.pnl_quote == pytest.approx(-100.0)


def test_short_take_profit_before_stop() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 100.2, 99.8, 99.9),
            ("2024-01-02 00:01", 99.9, 100.0, 98.8, 99.0),
            ("2024-01-02 00:02", 99.0, 101.5, 98.9, 101.0),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="USDJPY",
        side="sell",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.5,
        m1_bars=bars,
        stop_price=101.0,
        take_profit_price=99.0,
        contract_size=10.0,
    )

    assert fill.exit_reason == "tp"
    assert fill.exit_time_utc == _utc("2024-01-02 00:01")
    assert fill.exit_price == pytest.approx(99.0)
    assert fill.pnl_quote == pytest.approx(15.0)


def test_short_stop_before_take_profit() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 100.1, 99.8, 99.9),
            ("2024-01-02 00:01", 99.9, 101.2, 99.8, 101.0),
            ("2024-01-02 00:02", 101.0, 101.1, 98.5, 99.0),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="USDJPY",
        side="sell",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.0,
        m1_bars=bars,
        stop_price=101.0,
        take_profit_price=99.0,
        contract_size=100.0,
    )

    assert fill.exit_reason == "stop"
    assert fill.exit_time_utc == _utc("2024-01-02 00:01")
    assert fill.exit_price == pytest.approx(101.0)
    assert fill.pnl_quote == pytest.approx(-100.0)


def test_same_m1_bar_long_stop_wins() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 101.5, 98.5, 100.0),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.0,
        m1_bars=bars,
        stop_price=99.0,
        take_profit_price=101.0,
    )

    assert fill.exit_reason == "stop"
    assert fill.exit_price == pytest.approx(99.0)


def test_same_m1_bar_short_stop_wins() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 101.5, 98.5, 100.0),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="USDJPY",
        side="sell",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.0,
        m1_bars=bars,
        stop_price=101.0,
        take_profit_price=99.0,
    )

    assert fill.exit_reason == "stop"
    assert fill.exit_price == pytest.approx(101.0)


def test_no_intrabar_hit_exits_end_of_data_at_last_close() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 100.3, 99.7, 100.1),
            ("2024-01-02 00:01", 100.1, 100.4, 99.8, 100.2),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.0,
        m1_bars=bars,
        stop_price=99.0,
        take_profit_price=101.0,
    )

    assert fill.exit_reason == "end_of_data"
    assert fill.exit_time_utc == _utc("2024-01-02 00:01")
    assert fill.exit_price == pytest.approx(100.2)
    assert fill.pnl_quote == pytest.approx(0.2)


def test_forced_exit_before_later_stop_is_signal_flip() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 100.2, 99.8, 100.1),
            ("2024-01-02 00:01", 100.1, 100.3, 99.9, 100.2),
            ("2024-01-02 00:02", 100.2, 100.3, 98.5, 99.0),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.0,
        m1_bars=bars,
        stop_price=99.0,
        take_profit_price=101.0,
        forced_exit_time_utc=_utc("2024-01-02 00:02"),
        forced_exit_price=100.25,
    )

    assert fill.exit_reason == "signal_flip"
    assert fill.exit_time_utc == _utc("2024-01-02 00:02")
    assert fill.exit_price == pytest.approx(100.25)


def test_stop_slippage_worsens_long_stop_exit() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:00", 100.0, 100.2, 98.9, 99.0),
        ]
    )

    fill = simulate_bracket_trade(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        lots=1.0,
        m1_bars=bars,
        stop_price=99.0,
        stop_slippage=0.2,
    )

    assert fill.exit_reason == "stop"
    assert fill.exit_price == pytest.approx(98.8)
    assert fill.slippage == pytest.approx(0.2)
    assert fill.pnl_quote == pytest.approx(-1.2)


def test_rejects_tz_naive_m1_index() -> None:
    bars = pd.DataFrame(
        {
            "open": [100.0],
            "high": [101.0],
            "low": [99.0],
            "close": [100.0],
        },
        index=pd.DatetimeIndex([pd.Timestamp("2024-01-02 00:00")]),
    )

    with pytest.raises(ValueError, match="timezone-aware UTC"):
        simulate_bracket_trade(
            symbol="XAUUSD",
            side="buy",
            entry_time_utc=_utc("2024-01-02 00:00"),
            entry_price=100.0,
            lots=1.0,
            m1_bars=bars,
            stop_price=99.0,
        )


def test_rejects_unsorted_m1_index() -> None:
    bars = _m1_bars(
        [
            ("2024-01-02 00:01", 100.0, 100.2, 99.8, 100.1),
            ("2024-01-02 00:00", 100.1, 100.3, 99.9, 100.2),
        ]
    )

    with pytest.raises(ValueError, match="sorted ascending"):
        simulate_bracket_trade(
            symbol="XAUUSD",
            side="buy",
            entry_time_utc=_utc("2024-01-02 00:00"),
            entry_price=100.0,
            lots=1.0,
            m1_bars=bars,
            stop_price=99.0,
        )
