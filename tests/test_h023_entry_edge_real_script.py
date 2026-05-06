import pandas as pd
import pytest

from quantcore.strategy.h017 import H017Result
from scripts.diagnose_h023_entry_edge_real import (
    DEFAULT_H023_FORWARD_HORIZONS,
    assess_h023_bridge_windows,
    backtest_h023_entry_edge_forward_horizon,
    format_h023_summary_table,
    h023_signal_source_from_h020_bridge_shim_result,
    summarize_h023_entry_edge_result,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _h4() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-01 00:00"),
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 12:00"),
            _utc("2024-01-01 16:00"),
            _utc("2024-01-01 20:00"),
        ]
    )
    return pd.DataFrame(
        {
            "open": [100.0, 101.0, 103.0, 104.0, 105.0, 106.0],
            "high": [101.0, 103.5, 104.5, 105.5, 106.5, 107.5],
            "low": [99.0, 100.5, 102.5, 103.5, 104.5, 105.5],
            "close": [100.5, 103.0, 104.0, 105.0, 106.0, 107.0],
            "volume": [1, 1, 1, 1, 1, 1],
        },
        index=index,
    )


def _m1() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 12:00"),
            _utc("2024-01-01 16:00"),
            _utc("2024-01-01 20:00"),
        ]
    )
    return pd.DataFrame(
        {
            "open": [101.0, 103.0, 104.0, 105.0, 106.0],
            "high": [103.0, 104.0, 105.0, 106.0, 107.0],
            "low": [100.5, 102.5, 103.5, 104.5, 105.5],
            "close": [103.0, 104.0, 105.0, 106.0, 107.0],
        },
        index=index,
    )


def _h017_result() -> H017Result:
    index = _h4().index
    columns = ["USDJPY", "XAUUSD"]

    positions = pd.DataFrame(0.0, index=index, columns=columns)
    positions.at[_utc("2024-01-01 00:00"), "USDJPY"] = 0.01
    positions.at[_utc("2024-01-01 00:00"), "XAUUSD"] = -0.01
    positions.at[_utc("2024-01-01 04:00"), "USDJPY"] = 0.01
    positions.at[_utc("2024-01-01 04:00"), "XAUUSD"] = -0.01
    positions.at[_utc("2024-01-01 08:00"), "USDJPY"] = 0.01
    positions.at[_utc("2024-01-01 08:00"), "XAUUSD"] = -0.01

    stops_long = pd.DataFrame(95.0, index=index, columns=columns)
    stops_short = pd.DataFrame(110.0, index=index, columns=columns)

    signals = positions.mask(positions == 0.0, 0.0)
    multipliers = pd.DataFrame(1.0, index=index, columns=columns)
    heat = pd.Series(0.0, index=index)

    return H017Result(
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
        vol_multipliers=multipliers,
        heat_multipliers=multipliers,
        heat_pre=heat,
        heat_post=heat,
        heat_binding=pd.Series(False, index=index),
    )


def test_default_h023_forward_horizons_are_pre_registered_and_simple():
    assert DEFAULT_H023_FORWARD_HORIZONS == (1, 2, 3, 4, 6, 8)


def test_h023_rejects_invalid_forward_horizon():
    with pytest.raises(ValueError, match="forward_h4_bars must be positive"):
        backtest_h023_entry_edge_forward_horizon(
            h017_result=_h017_result(),
            usdjpy_h4=_h4(),
            xauusd_h4=_h4(),
            usdjpy_m1=_m1(),
            xauusd_m1=_m1(),
            accepted_entry_times=[_utc("2024-01-01 04:00")],
            forward_h4_bars=0,
        )


def test_h023_forward_horizon_uses_no_stop_exit_even_when_stop_touched():
    h4 = _h4()
    m1 = _m1().copy()
    m1.at[_utc("2024-01-01 04:00"), "low"] = 90.0

    result = backtest_h023_entry_edge_forward_horizon(
        h017_result=_h017_result(),
        usdjpy_h4=h4,
        xauusd_h4=h4,
        usdjpy_m1=m1,
        xauusd_m1=m1,
        accepted_entry_times=[
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 12:00"),
        ],
        forward_h4_bars=1,
    )

    assert result.executed_entry_count == 3
    assert len(result.fills) == 6
    assert {fill.exit_reason for fill in result.fills} == {"signal_flip"}


def test_h023_summary_and_format_on_synthetic_data():
    result = backtest_h023_entry_edge_forward_horizon(
        h017_result=_h017_result(),
        usdjpy_h4=_h4(),
        xauusd_h4=_h4(),
        usdjpy_m1=_m1(),
        xauusd_m1=_m1(),
        accepted_entry_times=[
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 12:00"),
        ],
        forward_h4_bars=1,
    )

    summary = summarize_h023_entry_edge_result(result)
    table = format_h023_summary_table([summary])

    assert summary.forward_h4_bars == 1
    assert summary.accepted_entry_count == 3
    assert summary.executed_entry_count == 3
    assert summary.fill_count == 6
    assert "Horizon" in table
    assert "1 H4" in table
    assert "PF" in table


def test_h023_skips_incomplete_forward_horizon():
    result = backtest_h023_entry_edge_forward_horizon(
        h017_result=_h017_result(),
        usdjpy_h4=_h4(),
        xauusd_h4=_h4(),
        usdjpy_m1=_m1(),
        xauusd_m1=_m1(),
        accepted_entry_times=[_utc("2024-01-01 20:00")],
        forward_h4_bars=1,
    )

    assert result.accepted_entry_count == 1
    assert result.executed_entry_count == 0
    assert result.incomplete_horizon_skip_count == 1
    assert len(result.fills) == 0
def test_h023_bridge_window_helper_uses_existing_usdjpy_xauusd_api():
    h4 = _h4().iloc[:2].copy()
    m1 = pd.DataFrame(
        {
            "open": [101.0],
            "high": [102.0],
            "low": [100.0],
            "close": [101.5],
        },
        index=pd.DatetimeIndex([_utc("2024-01-01 00:00")]),
    )

    assessment = assess_h023_bridge_windows(
        usdjpy_h4=h4,
        xauusd_h4=h4,
        usdjpy_m1=m1,
        xauusd_m1=m1,
        expected_m1_bars_per_h4=1,
        expected_h4_delta=pd.Timedelta(hours=4),
    )

    assert assessment.accepted_count == 1
    assert list(assessment.accepted_timestamps) == [_utc("2024-01-01 00:00")]
def test_h023_uses_h020_bridge_shim_h017_result_directly():
    source = _h017_result()

    assert h023_signal_source_from_h020_bridge_shim_result(source) is source

    with pytest.raises(TypeError, match="must be an H017Result"):
        h023_signal_source_from_h020_bridge_shim_result(object())
