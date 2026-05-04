from __future__ import annotations

from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from quantcore.backtest.h017_event import (
    H017EventBacktestResult,
    H017EventInsolvencyError,
    H017EventInvalidStopError,
    backtest_h017_event_from_result,
)
from quantcore.strategy.h017 import H017Result


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _h4(opens: list[float]) -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-02 00:00"),
            _utc("2024-01-02 04:00"),
            _utc("2024-01-02 08:00"),
        ]
    )
    return pd.DataFrame(
        {
            "open": opens,
            "high": [value + 5.0 for value in opens],
            "low": [value - 5.0 for value in opens],
            "close": opens,
            "volume": [100.0, 100.0, 100.0],
        },
        index=index,
    )


def _m1(rows: list[tuple[str, float, float, float, float]]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [row[1] for row in rows],
            "high": [row[2] for row in rows],
            "low": [row[3] for row in rows],
            "close": [row[4] for row in rows],
        },
        index=pd.DatetimeIndex([_utc(row[0]) for row in rows]),
    )


def _panel(
    *,
    usdjpy: list[float],
    xauusd: list[float],
    name: str,
) -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-02 00:00"),
            _utc("2024-01-02 04:00"),
            _utc("2024-01-02 08:00"),
        ]
    )
    return pd.DataFrame(
        {
            "USDJPY": usdjpy,
            "XAUUSD": xauusd,
        },
        index=index,
    ).rename_axis(name)


def _h017_result(
    *,
    usdjpy_positions: list[float] | None = None,
    xauusd_positions: list[float] | None = None,
    xauusd_stop_long: list[float] | None = None,
    xauusd_stop_short: list[float] | None = None,
    usdjpy_stop_long: list[float] | None = None,
    usdjpy_stop_short: list[float] | None = None,
) -> H017Result:
    positions = _panel(
        usdjpy=usdjpy_positions or [0.0, 0.0, 0.0],
        xauusd=xauusd_positions or [0.0, 0.0, 0.0],
        name="positions",
    )
    signals = positions.copy()
    stops_long = _panel(
        usdjpy=usdjpy_stop_long or [149.0, 149.0, 149.0],
        xauusd=xauusd_stop_long or [1990.0, 1990.0, 1990.0],
        name="stops_long",
    )
    stops_short = _panel(
        usdjpy=usdjpy_stop_short or [151.0, 151.0, 151.0],
        xauusd=xauusd_stop_short or [2010.0, 2010.0, 2010.0],
        name="stops_short",
    )
    zeros = positions * 0.0

    return H017Result(
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
        vol_multipliers=zeros,
        heat_multipliers=zeros,
        heat_pre=zeros,
        heat_post=zeros,
        heat_binding=zeros.astype(bool),
    )


def test_h017_event_result_is_frozen() -> None:
    empty_portfolio = backtest_h017_event_from_result(
        h017_result=_h017_result(),
        usdjpy_h4=_h4([150.0, 150.0, 150.0]),
        xauusd_h4=_h4([2000.0, 2000.0, 2000.0]),
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
            ]
        ),
    )

    with pytest.raises(FrozenInstanceError):
        empty_portfolio.n_bars = 99  # type: ignore[misc]


def test_long_xauusd_trade_opens_on_next_h4_bar_and_pays_costs() -> None:
    result = backtest_h017_event_from_result(
        h017_result=_h017_result(xauusd_positions=[0.01, 0.0, 0.0]),
        usdjpy_h4=_h4([150.0, 150.0, 150.0]),
        xauusd_h4=_h4([2000.0, 2000.0, 2010.0]),
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ("2024-01-02 04:01", 2000.5, 2001.5, 1999.5, 2001.0),
            ]
        ),
    )

    assert len(result.fills) == 1
    fill = result.fills[0]

    assert fill.symbol == "XAUUSD"
    assert fill.side == "buy"
    assert fill.entry_time_utc == _utc("2024-01-02 04:00")
    assert fill.exit_time_utc == _utc("2024-01-02 08:00")
    assert fill.exit_reason == "signal_flip"
    assert fill.lots == pytest.approx(0.10)
    assert fill.entry_price == pytest.approx(2000.15)
    assert fill.exit_price == pytest.approx(2009.85)
    assert fill.pnl_quote == pytest.approx(97.0)
    assert fill.commission == pytest.approx(2.0)
    assert result.portfolio.ending_equity_usd == pytest.approx(10_095.0)


def test_long_xauusd_intrabar_stop_exits_before_forced_h4_close() -> None:
    result = backtest_h017_event_from_result(
        h017_result=_h017_result(xauusd_positions=[0.01, 0.0, 0.0]),
        usdjpy_h4=_h4([150.0, 150.0, 150.0]),
        xauusd_h4=_h4([2000.0, 2000.0, 2010.0]),
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ("2024-01-02 04:01", 2000.5, 2001.0, 1989.0, 1991.0),
            ]
        ),
        slippage_atr_by_symbol={
            "XAUUSD": pd.Series(
                [4.0, 4.0, 4.0],
                index=pd.DatetimeIndex(
                    [
                        _utc("2024-01-02 00:00"),
                        _utc("2024-01-02 04:00"),
                        _utc("2024-01-02 08:00"),
                    ]
                ),
            )
        },
    )

    fill = result.fills[0]

    assert fill.exit_reason == "stop"
    assert fill.exit_time_utc == _utc("2024-01-02 04:01")
    assert fill.exit_price == pytest.approx(1989.65)
    assert fill.slippage == pytest.approx(0.20)
    assert fill.pnl_quote == pytest.approx(-105.0)
    assert fill.commission == pytest.approx(2.0)
    assert result.portfolio.ending_equity_usd == pytest.approx(9_893.0)


def test_short_xauusd_intrabar_stop_uses_short_stop_panel() -> None:
    result = backtest_h017_event_from_result(
        h017_result=_h017_result(xauusd_positions=[-0.01, 0.0, 0.0]),
        usdjpy_h4=_h4([150.0, 150.0, 150.0]),
        xauusd_h4=_h4([2000.0, 2000.0, 1990.0]),
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ("2024-01-02 04:01", 2000.5, 2011.0, 1999.0, 2010.0),
            ]
        ),
        slippage_atr_by_symbol={
            "XAUUSD": pd.Series(
                [4.0, 4.0, 4.0],
                index=pd.DatetimeIndex(
                    [
                        _utc("2024-01-02 00:00"),
                        _utc("2024-01-02 04:00"),
                        _utc("2024-01-02 08:00"),
                    ]
                ),
            )
        },
    )

    fill = result.fills[0]

    assert fill.side == "sell"
    assert fill.exit_reason == "stop"
    assert fill.exit_price == pytest.approx(2010.35)
    assert fill.pnl_quote == pytest.approx(-105.0)
    assert result.portfolio.ending_equity_usd == pytest.approx(9_893.0)


def test_interval_ruin_raises_clear_insolvency_error() -> None:
    with pytest.raises(
        H017EventInsolvencyError,
        match="H017 event backtest insolvency",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[2.0, 0.0, 0.0],
                xauusd_stop_long=[1990.0, 1990.0, 1990.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 2000.0]),
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2001.0, 1989.0, 1990.0),
                ]
            ),
        )

    error = exc_info.value

    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.forced_exit_time == _utc("2024-01-02 08:00")
    assert error.interval_start_equity_usd == pytest.approx(10_000.0)
    assert error.interval_pnl_usd < -10_000.0
    assert error.ending_equity_usd <= 0.0
    assert len(error.interval_fills) == 1

    fill = error.interval_fills[0]
    assert fill.symbol == "XAUUSD"
    assert fill.side == "buy"
    assert fill.exit_reason == "stop"
    assert fill.lots == pytest.approx(20.0)


def test_flat_positions_create_no_fills_and_flat_equity() -> None:
    result = backtest_h017_event_from_result(
        h017_result=_h017_result(),
        usdjpy_h4=_h4([150.0, 150.0, 150.0]),
        xauusd_h4=_h4([2000.0, 2000.0, 2000.0]),
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
            ]
        ),
    )

    assert result.fills == ()
    assert result.portfolio.ending_equity_usd == pytest.approx(10_000.0)
    assert result.portfolio.max_drawdown == pytest.approx(0.0)


def test_nan_stop_skips_trade_because_risk_cannot_be_defined() -> None:
    result = backtest_h017_event_from_result(
        h017_result=_h017_result(
            xauusd_positions=[0.01, 0.0, 0.0],
            xauusd_stop_long=[float("nan"), 1990.0, 1990.0],
        ),
        usdjpy_h4=_h4([150.0, 150.0, 150.0]),
        xauusd_h4=_h4([2000.0, 2000.0, 2010.0]),
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
            ]
        ),
    )

    assert result.fills == ()


def test_long_stop_above_raw_entry_fails_closed() -> None:
    with pytest.raises(
        H017EventInvalidStopError,
        match="H017 event invalid stop geometry",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[0.01, 0.0, 0.0],
                xauusd_stop_long=[2001.0, 1990.0, 1990.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 2010.0]),
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ]
            ),
        )

    error = exc_info.value

    assert error.symbol == "XAUUSD"
    assert error.side == "buy"
    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.entry_raw_price == pytest.approx(2000.0)
    assert error.stop_price == pytest.approx(2001.0)


def test_short_stop_below_raw_entry_fails_closed() -> None:
    with pytest.raises(
        H017EventInvalidStopError,
        match="H017 event invalid stop geometry",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[-0.01, 0.0, 0.0],
                xauusd_stop_short=[1999.0, 2010.0, 2010.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 1990.0]),
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ]
            ),
        )

    error = exc_info.value

    assert error.symbol == "XAUUSD"
    assert error.side == "sell"
    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.entry_raw_price == pytest.approx(2000.0)
    assert error.stop_price == pytest.approx(1999.0)


def test_long_stop_equal_to_raw_entry_fails_closed() -> None:
    with pytest.raises(
        H017EventInvalidStopError,
        match="H017 event invalid stop geometry",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[0.01, 0.0, 0.0],
                xauusd_stop_long=[2000.0, 1990.0, 1990.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 2010.0]),
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ]
            ),
        )

    error = exc_info.value

    assert error.symbol == "XAUUSD"
    assert error.side == "buy"
    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.entry_raw_price == pytest.approx(2000.0)
    assert error.stop_price == pytest.approx(2000.0)


def test_short_stop_equal_to_raw_entry_fails_closed() -> None:
    with pytest.raises(
        H017EventInvalidStopError,
        match="H017 event invalid stop geometry",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[-0.01, 0.0, 0.0],
                xauusd_stop_short=[2000.0, 2010.0, 2010.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 1990.0]),
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ]
            ),
        )

    error = exc_info.value

    assert error.symbol == "XAUUSD"
    assert error.side == "sell"
    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.entry_raw_price == pytest.approx(2000.0)
    assert error.stop_price == pytest.approx(2000.0)


def test_usdjpy_jpy_pnl_is_converted_to_usd_in_portfolio() -> None:
    result = backtest_h017_event_from_result(
        h017_result=_h017_result(usdjpy_positions=[0.01, 0.0, 0.0]),
        usdjpy_h4=_h4([150.0, 150.0, 151.0]),
        xauusd_h4=_h4([2000.0, 2000.0, 2000.0]),
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ("2024-01-02 04:01", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
            ]
        ),
    )

    assert len(result.fills) == 1
    fill = result.fills[0]

    assert fill.symbol == "USDJPY"
    assert fill.lots == pytest.approx(0.15)
    assert fill.entry_price == pytest.approx(150.005)
    assert fill.exit_price == pytest.approx(150.995)
    assert fill.pnl_quote == pytest.approx(14_850.0)
    assert fill.commission == pytest.approx(2.1)
    assert result.portfolio.ending_equity_usd == pytest.approx(
        10_000.0 + (14_850.0 / 150.995) - 2.1
    )


def test_missing_required_h017_symbol_is_rejected() -> None:
    bad = _h017_result(xauusd_positions=[0.01, 0.0, 0.0])
    bad_positions = bad.positions.drop(columns=["XAUUSD"])
    bad = H017Result(
        positions=bad_positions,
        signals=bad.signals,
        stops_long=bad.stops_long,
        stops_short=bad.stops_short,
        vol_multipliers=bad.vol_multipliers,
        heat_multipliers=bad.heat_multipliers,
        heat_pre=bad.heat_pre,
        heat_post=bad.heat_post,
        heat_binding=bad.heat_binding,
    )

    with pytest.raises(ValueError, match="positions missing required symbols"):
        backtest_h017_event_from_result(
            h017_result=bad,
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 2000.0]),
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
                ]
            ),
        )


def test_tz_naive_h4_index_is_rejected() -> None:
    xauusd_h4 = _h4([2000.0, 2000.0, 2000.0])
    xauusd_h4.index = pd.DatetimeIndex(
        [
            pd.Timestamp("2024-01-02 00:00"),
            pd.Timestamp("2024-01-02 04:00"),
            pd.Timestamp("2024-01-02 08:00"),
        ]
    )

    with pytest.raises(ValueError, match="timezone-aware UTC"):
        backtest_h017_event_from_result(
            h017_result=_h017_result(),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=xauusd_h4,
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
                ]
            ),
        )


def test_m1_stop_window_errors_are_not_silently_ignored() -> None:
    with pytest.raises(ValueError, match="trade scan window"):
        backtest_h017_event_from_result(
            h017_result=_h017_result(xauusd_positions=[0.01, 0.0, 0.0]),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 2010.0]),
            usdjpy_m1=_m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            xauusd_m1=_m1(
                [
                    ("2024-01-02 00:01", 2000.0, 2001.0, 1999.0, 2000.5),
                ]
            ),
        )
