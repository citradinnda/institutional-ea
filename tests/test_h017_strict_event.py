from __future__ import annotations

from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from quantcore.backtest.h017_strict_event import (
    StrictH017EventBacktestResult,
    backtest_h017_strict_event_from_result,
)
from quantcore.strategy.h017 import H017Result


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _h4(index: pd.DatetimeIndex, opens: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": opens,
            "high": [value + 5.0 for value in opens],
            "low": [value - 5.0 for value in opens],
            "close": opens,
            "volume": [100.0 for _ in opens],
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
    index: pd.DatetimeIndex,
    *,
    usdjpy: list[float],
    xauusd: list[float],
    name: str,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "USDJPY": usdjpy,
            "XAUUSD": xauusd,
        },
        index=index,
    ).rename_axis(name)


def _h017_result(
    index: pd.DatetimeIndex,
    *,
    usdjpy_positions: list[float] | None = None,
    xauusd_positions: list[float] | None = None,
) -> H017Result:
    positions = _panel(
        index,
        usdjpy=usdjpy_positions or [0.0 for _ in index],
        xauusd=xauusd_positions or [0.0 for _ in index],
        name="positions",
    )
    signals = positions.copy()
    stops_long = _panel(
        index,
        usdjpy=[149.0 for _ in index],
        xauusd=[1990.0 for _ in index],
        name="stops_long",
    )
    stops_short = _panel(
        index,
        usdjpy=[151.0 for _ in index],
        xauusd=[2010.0 for _ in index],
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


def test_strict_result_is_frozen() -> None:
    index = pd.date_range("2024-01-02 00:00", periods=3, freq="4h", tz="UTC")
    h4 = _h4(index, [2000.0, 2000.0, 2010.0])
    result = backtest_h017_strict_event_from_result(
        h017_result=_h017_result(index),
        usdjpy_h4=h4,
        xauusd_h4=h4,
        usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
        xauusd_m1=_m1([("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5)]),
        accepted_entry_times=pd.DatetimeIndex([_utc("2024-01-02 04:00")]),
    )

    with pytest.raises(FrozenInstanceError):
        result.executed_entry_count = 99  # type: ignore[misc]


def test_strict_wrapper_executes_accepted_four_hour_entry_window() -> None:
    index = pd.date_range("2024-01-02 00:00", periods=3, freq="4h", tz="UTC")
    usdjpy_h4 = _h4(index, [150.0, 150.0, 150.0])
    xauusd_h4 = _h4(index, [2000.0, 2000.0, 2010.0])

    result = backtest_h017_strict_event_from_result(
        h017_result=_h017_result(index, xauusd_positions=[0.01, 0.0, 0.0]),
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ("2024-01-02 04:01", 2000.5, 2001.5, 1999.5, 2001.0),
            ]
        ),
        accepted_entry_times=pd.DatetimeIndex([_utc("2024-01-02 04:00")]),
    )

    assert isinstance(result, StrictH017EventBacktestResult)
    assert result.accepted_entry_count == 1
    assert result.executed_entry_count == 1
    assert result.skipped_entry_count == 0
    assert result.executed_entry_times.equals(
        pd.DatetimeIndex([_utc("2024-01-02 04:00")])
    )
    assert len(result.backtest.fills) == 1
    assert result.backtest.fills[0].symbol == "XAUUSD"
    assert result.backtest.fills[0].exit_time_utc == _utc("2024-01-02 08:00")


def test_strict_wrapper_forces_unaccepted_entry_window_flat() -> None:
    index = pd.date_range("2024-01-02 00:00", periods=3, freq="4h", tz="UTC")
    usdjpy_h4 = _h4(index, [150.0, 150.0, 150.0])
    xauusd_h4 = _h4(index, [2000.0, 2000.0, 2010.0])

    result = backtest_h017_strict_event_from_result(
        h017_result=_h017_result(index, xauusd_positions=[0.01, 0.0, 0.0]),
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
        xauusd_m1=_m1([("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5)]),
        accepted_entry_times=pd.DatetimeIndex([], tz="UTC"),
    )

    assert result.accepted_entry_count == 0
    assert result.executed_entry_count == 0
    assert result.skipped_entry_count == 1
    assert result.skipped_entry_times.equals(
        pd.DatetimeIndex([_utc("2024-01-02 04:00")])
    )
    assert result.backtest.fills == ()
    assert result.backtest.portfolio.ending_equity_usd == pytest.approx(10_000.0)


def test_strict_wrapper_skips_accepted_entry_when_forced_exit_is_not_next_four_hours() -> None:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-02 00:00"),
            _utc("2024-01-02 04:00"),
            _utc("2024-01-02 12:00"),
        ]
    )
    usdjpy_h4 = _h4(index, [150.0, 150.0, 150.0])
    xauusd_h4 = _h4(index, [2000.0, 2000.0, 2010.0])

    result = backtest_h017_strict_event_from_result(
        h017_result=_h017_result(index, xauusd_positions=[0.01, 0.0, 0.0]),
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
        xauusd_m1=_m1([("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5)]),
        accepted_entry_times=pd.DatetimeIndex([_utc("2024-01-02 04:00")]),
    )

    assert result.accepted_entry_count == 1
    assert result.executed_entry_count == 0
    assert result.skipped_entry_count == 1
    assert result.backtest.fills == ()


def test_strict_wrapper_preserves_native_index_and_does_not_filter_across_gaps() -> None:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-02 00:00"),
            _utc("2024-01-02 04:00"),
            _utc("2024-01-02 08:00"),
            _utc("2024-01-02 20:00"),
            _utc("2024-01-03 00:00"),
        ]
    )
    usdjpy_h4 = _h4(index, [150.0, 150.0, 150.0, 150.0, 150.0])
    xauusd_h4 = _h4(index, [2000.0, 2000.0, 2010.0, 2000.0, 2010.0])

    result = backtest_h017_strict_event_from_result(
        h017_result=_h017_result(
            index,
            xauusd_positions=[0.01, 0.01, 0.01, 0.0, 0.0],
        ),
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1(
            [
                ("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0),
                ("2024-01-02 20:00", 150.0, 150.1, 149.9, 150.0),
            ]
        ),
        xauusd_m1=_m1(
            [
                ("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5),
                ("2024-01-02 20:00", 2000.0, 2001.0, 1999.0, 2000.5),
            ]
        ),
        accepted_entry_times=pd.DatetimeIndex(
            [
                _utc("2024-01-02 04:00"),
                _utc("2024-01-02 20:00"),
            ]
        ),
    )

    assert result.executed_entry_times.equals(
        pd.DatetimeIndex(
            [
                _utc("2024-01-02 04:00"),
                _utc("2024-01-02 20:00"),
            ]
        )
    )
    assert result.skipped_entry_times.equals(
        pd.DatetimeIndex([_utc("2024-01-02 08:00")])
    )
    assert len(result.backtest.fills) == 2
    assert [fill.entry_time_utc for fill in result.backtest.fills] == [
        _utc("2024-01-02 04:00"),
        _utc("2024-01-02 20:00"),
    ]


def test_strict_wrapper_rejects_naive_accepted_entry_times() -> None:
    index = pd.date_range("2024-01-02 00:00", periods=3, freq="4h", tz="UTC")
    h4 = _h4(index, [2000.0, 2000.0, 2010.0])

    with pytest.raises(ValueError, match="timezone-aware UTC"):
        backtest_h017_strict_event_from_result(
            h017_result=_h017_result(index),
            usdjpy_h4=h4,
            xauusd_h4=h4,
            usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
            xauusd_m1=_m1([("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5)]),
            accepted_entry_times=pd.DatetimeIndex([pd.Timestamp("2024-01-02 04:00")]),
        )


def test_strict_wrapper_rejects_duplicate_accepted_entry_times() -> None:
    index = pd.date_range("2024-01-02 00:00", periods=3, freq="4h", tz="UTC")
    h4 = _h4(index, [2000.0, 2000.0, 2010.0])

    with pytest.raises(ValueError, match="duplicate"):
        backtest_h017_strict_event_from_result(
            h017_result=_h017_result(index),
            usdjpy_h4=h4,
            xauusd_h4=h4,
            usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
            xauusd_m1=_m1([("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5)]),
            accepted_entry_times=pd.DatetimeIndex(
                [
                    _utc("2024-01-02 04:00"),
                    _utc("2024-01-02 04:00"),
                ]
            ),
        )


def test_strict_wrapper_rejects_unsorted_accepted_entry_times() -> None:
    index = pd.date_range("2024-01-02 00:00", periods=4, freq="4h", tz="UTC")
    h4 = _h4(index, [2000.0, 2000.0, 2010.0, 2020.0])

    with pytest.raises(ValueError, match="sorted ascending"):
        backtest_h017_strict_event_from_result(
            h017_result=_h017_result(index),
            usdjpy_h4=h4,
            xauusd_h4=h4,
            usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
            xauusd_m1=_m1([("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5)]),
            accepted_entry_times=pd.DatetimeIndex(
                [
                    _utc("2024-01-02 08:00"),
                    _utc("2024-01-02 04:00"),
                ]
            ),
        )


def test_strict_wrapper_rejects_invalid_expected_h4_delta() -> None:
    index = pd.date_range("2024-01-02 00:00", periods=3, freq="4h", tz="UTC")
    h4 = _h4(index, [2000.0, 2000.0, 2010.0])

    with pytest.raises(ValueError, match="expected_h4_delta"):
        backtest_h017_strict_event_from_result(
            h017_result=_h017_result(index),
            usdjpy_h4=h4,
            xauusd_h4=h4,
            usdjpy_m1=_m1([("2024-01-02 04:00", 150.0, 150.1, 149.9, 150.0)]),
            xauusd_m1=_m1([("2024-01-02 04:00", 2000.0, 2001.0, 1999.0, 2000.5)]),
            accepted_entry_times=pd.DatetimeIndex([_utc("2024-01-02 04:00")]),
            expected_h4_delta=pd.Timedelta(0),
        )
