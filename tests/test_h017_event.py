from __future__ import annotations

from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from quantcore.backtest.h017_event import (
    H017EventBacktestResult,
    H017EventInsolvencyError,
    H017EventInvalidStopError,
    H018MaximumPerTradeLeverageError,
    H018MinimumStopDistanceError,
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
                xauusd_positions=[-2.0, 0.0, 0.0],
                xauusd_stop_short=[4000.0, 2010.0, 2010.0],
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
                    ("2024-01-02 04:00", 2000.0, 4001.0, 1999.0, 4000.0),
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
    assert fill.side == "sell"
    assert fill.exit_reason == "stop"
    assert fill.lots == pytest.approx(0.1)


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

def test_h018_minimum_stop_distance_long_below_one_spread_fails_closed() -> None:
    with pytest.raises(
        H018MinimumStopDistanceError,
        match="H018 minimum stop-distance violation",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[0.01, 0.0, 0.0],
                xauusd_stop_long=[1999.80, 1990.0, 1990.0],
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
                    ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
                ]
            ),
        )

    error = exc_info.value

    assert error.rule_name == "raw_stop_distance_at_least_one_modeled_spread"
    assert error.symbol == "XAUUSD"
    assert error.side == "buy"
    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.entry_raw_price == pytest.approx(2000.0)
    assert error.stop_price == pytest.approx(1999.80)
    assert error.raw_stop_distance == pytest.approx(0.20)
    assert error.minimum_stop_distance == pytest.approx(0.30)
    assert error.threshold_basis == "one_modeled_spread"
    assert error.validation_action == "fail_closed"


def test_h018_minimum_stop_distance_short_below_one_spread_fails_closed() -> None:
    with pytest.raises(
        H018MinimumStopDistanceError,
        match="H018 minimum stop-distance violation",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                usdjpy_positions=[-0.01, 0.0, 0.0],
                usdjpy_stop_short=[150.005, 151.0, 151.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 149.0]),
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

    error = exc_info.value

    assert error.rule_name == "raw_stop_distance_at_least_one_modeled_spread"
    assert error.symbol == "USDJPY"
    assert error.side == "sell"
    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.entry_raw_price == pytest.approx(150.0)
    assert error.stop_price == pytest.approx(150.005)
    assert error.raw_stop_distance == pytest.approx(0.005)
    assert error.minimum_stop_distance == pytest.approx(0.01)
    assert error.threshold_basis == "one_modeled_spread"
    assert error.validation_action == "fail_closed"


@pytest.mark.parametrize(
    ("symbol", "side", "stop_price"),
    [
        ("XAUUSD", "buy", 1999.70),
        ("XAUUSD", "sell", 2000.30),
        ("XAUUSD", "buy", 1999.60),
        ("XAUUSD", "sell", 2000.40),
        ("USDJPY", "buy", 149.99),
        ("USDJPY", "sell", 150.01),
    ],
)
def test_h018_minimum_stop_distance_at_or_above_one_spread_passes_guard(
    symbol: str,
    side: str,
    stop_price: float,
) -> None:
    if symbol == "XAUUSD":
        result = backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[0.0001 if side == "buy" else -0.0001, 0.0, 0.0],
                xauusd_stop_long=[stop_price, 1990.0, 1990.0],
                xauusd_stop_short=[stop_price, 2010.0, 2010.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 150.0]),
            xauusd_h4=_h4([2000.0, 2000.0, 2010.0 if side == "buy" else 1990.0]),
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
    else:
        result = backtest_h017_event_from_result(
            h017_result=_h017_result(
                usdjpy_positions=[0.0001 if side == "buy" else -0.0001, 0.0, 0.0],
                usdjpy_stop_long=[stop_price, 149.0, 149.0],
                usdjpy_stop_short=[stop_price, 151.0, 151.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 151.0 if side == "buy" else 149.0]),
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

    assert len(result.fills) == 1
    assert result.fills[0].symbol == symbol
    assert result.fills[0].side == side

@pytest.mark.parametrize(
    ("symbol", "stop_price", "expected_lots", "expected_gross_leverage"),
    [
        ("USDJPY", 149.80, 0.75, 7.5),
        ("USDJPY", 149.85, 1.00, 10.0),
        ("XAUUSD", 1997.00, 0.33, 6.6),
        ("XAUUSD", 1998.00, 0.50, 10.0),
    ],
)
def test_h018_maximum_per_trade_leverage_at_or_below_10x_passes_guard(
    symbol: str,
    stop_price: float,
    expected_lots: float,
    expected_gross_leverage: float,
) -> None:
    if symbol == "USDJPY":
        result = backtest_h017_event_from_result(
            h017_result=_h017_result(
                usdjpy_positions=[0.01, 0.0, 0.0],
                usdjpy_stop_long=[stop_price, 149.0, 149.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 151.0]),
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
    else:
        result = backtest_h017_event_from_result(
            h017_result=_h017_result(
                xauusd_positions=[0.01, 0.0, 0.0],
                xauusd_stop_long=[stop_price, 1990.0, 1990.0],
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
                    ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
                ]
            ),
        )

    assert len(result.fills) == 1
    fill = result.fills[0]
    assert fill.symbol == symbol
    assert fill.side == "buy"
    assert fill.lots == pytest.approx(expected_lots)

    if symbol == "USDJPY":
        notional_usd = fill.lots * 100_000.0
    else:
        notional_usd = fill.lots * 100.0 * 2000.0

    assert notional_usd / 10_000.0 == pytest.approx(expected_gross_leverage)


@pytest.mark.parametrize(
    ("symbol", "stop_price"),
    [
        ("USDJPY", 149.90),
        ("XAUUSD", 1999.00),
    ],
)
def test_h018_maximum_per_trade_leverage_above_10x_fails_closed(
    symbol: str,
    stop_price: float,
) -> None:
    if symbol == "USDJPY":
        kwargs = {
            "h017_result": _h017_result(
                usdjpy_positions=[0.01, 0.0, 0.0],
                usdjpy_stop_long=[stop_price, 149.0, 149.0],
            ),
            "usdjpy_h4": _h4([150.0, 150.0, 151.0]),
            "xauusd_h4": _h4([2000.0, 2000.0, 2000.0]),
            "usdjpy_m1": _m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            "xauusd_m1": _m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
                ]
            ),
        }
    else:
        kwargs = {
            "h017_result": _h017_result(
                xauusd_positions=[0.01, 0.0, 0.0],
                xauusd_stop_long=[stop_price, 1990.0, 1990.0],
            ),
            "usdjpy_h4": _h4([150.0, 150.0, 150.0]),
            "xauusd_h4": _h4([2000.0, 2000.0, 2010.0]),
            "usdjpy_m1": _m1(
                [
                    ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ]
            ),
            "xauusd_m1": _m1(
                [
                    ("2024-01-02 04:00", 2000.0, 2000.5, 1999.5, 2000.0),
                ]
            ),
        }

    with pytest.raises(
        H018MaximumPerTradeLeverageError,
        match="H018 maximum per-trade leverage violation",
    ):
        backtest_h017_event_from_result(**kwargs)


def test_h018_maximum_per_trade_leverage_error_preserves_audit_fields() -> None:
    with pytest.raises(
        H018MaximumPerTradeLeverageError,
        match="H018 maximum per-trade leverage violation",
    ) as exc_info:
        backtest_h017_event_from_result(
            h017_result=_h017_result(
                usdjpy_positions=[0.01, 0.0, 0.0],
                usdjpy_stop_long=[149.90, 149.0, 149.0],
            ),
            usdjpy_h4=_h4([150.0, 150.0, 151.0]),
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

    error = exc_info.value

    assert error.rule_name == "per_trade_usd_gross_leverage_at_or_below_10x_equity"
    assert error.symbol == "USDJPY"
    assert error.side == "buy"
    assert error.decision_time == _utc("2024-01-02 00:00")
    assert error.entry_time == _utc("2024-01-02 04:00")
    assert error.entry_raw_price == pytest.approx(150.0)
    assert error.stop_price == pytest.approx(149.90)
    assert error.raw_stop_distance == pytest.approx(0.10)
    assert error.equity_usd == pytest.approx(10_000.0)
    assert error.lots == pytest.approx(1.50)
    assert error.contract_size == pytest.approx(100_000.0)
    assert error.quote_currency == "JPY"
    assert error.notional_quote == pytest.approx(22_500_000.0)
    assert error.notional_usd == pytest.approx(150_000.0)
    assert error.gross_leverage == pytest.approx(15.0)
    assert error.maximum_gross_leverage == pytest.approx(10.0)
    assert error.threshold_basis == "per_trade_usd_gross_notional_divided_by_equity"
    assert error.validation_action == "fail_closed"

