import pandas as pd
import pytest

from quantcore.strategy.h020 import H020SizingConfig
from quantcore.strategy.h024 import H024SignalConfig
from quantcore.strategy.h024_runner import H024BridgeConfig, run_h024_bridge_shim
from scripts.diagnose_h024_direction_flip_real import (
    DEFAULT_H024_DIRECTION_FLIP_HOLD_H4_BARS,
    build_direction_flip_h017_result,
    format_h024_direction_flip_report,
    run_h024_direction_flip_diagnostic,
)


def _index() -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01 00:00", periods=12, freq="4h", tz="UTC")


def _usdjpy_h4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104, 105, 106, 105, 107, 108, 109, 110],
            "high": [101, 102, 103, 104, 105, 106, 107, 106, 109, 110, 111, 112],
            "low": [99, 100, 101, 102, 103, 104, 105, 104, 106, 107, 108, 109],
            "close": [101, 102, 103, 104, 105, 106, 106.5, 104.5, 108, 109, 110, 111],
        },
        index=_index(),
    )


def _xauusd_h4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [110, 109, 108, 107, 106, 105, 104, 105, 103, 102, 101, 100],
            "high": [111, 110, 109, 108, 107, 106, 105, 106, 104, 103, 102, 101],
            "low": [109, 108, 107, 106, 105, 104, 103, 104, 101, 100, 99, 98],
            "close": [109, 108, 107, 106, 105, 104, 103.5, 105.5, 102, 101, 100, 99],
        },
        index=_index(),
    )


def _m1_from_h4(h4: pd.DataFrame) -> pd.DataFrame:
    rows = []
    index = []
    for timestamp, row in h4.iterrows():
        index.append(timestamp)
        rows.append(
            {
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
            }
        )
    return pd.DataFrame(rows, index=pd.DatetimeIndex(index))


def _bridge_config() -> H024BridgeConfig:
    return H024BridgeConfig(
        signal_config=H024SignalConfig(
            slow_window=5,
            slope_lag=2,
            atr_window=3,
            pullback_window=3,
            min_pullback_atr=0.25,
            max_pullback_atr=3.0,
            min_slope_atr=0.05,
        ),
        sizing_config=H020SizingConfig(
            per_trade_max_gross_leverage=9.0,
            portfolio_max_gross_leverage=9.0,
        ),
        signed_risk_fraction=0.01,
        stop_atr_multiple=2.0,
        atr_window=3,
        starting_equity_usd=10_000.0,
    )


def test_direction_flip_preserves_shape_and_inverts_positions():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()
    h024 = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=_bridge_config(),
    )

    flipped = build_direction_flip_h017_result(
        h024_result=h024,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
    )

    pd.testing.assert_frame_equal(flipped.positions, -h024.positions)
    pd.testing.assert_frame_equal(flipped.signals, -h024.signals)
    assert flipped.stops_long.shape == h024.stops_long.shape
    assert flipped.stops_short.shape == h024.stops_short.shape


def test_direction_flip_diagnostic_runs_on_synthetic_data():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()

    diagnostic = run_h024_direction_flip_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        bridge_config=_bridge_config(),
    )

    assert diagnostic.baseline_summary.hold_h4_bars == DEFAULT_H024_DIRECTION_FLIP_HOLD_H4_BARS
    assert diagnostic.direction_flip_summary.hold_h4_bars == DEFAULT_H024_DIRECTION_FLIP_HOLD_H4_BARS
    assert diagnostic.baseline_summary.accepted_entry_count == len(usdjpy_h4.index)
    assert diagnostic.direction_flip_summary.accepted_entry_count == len(usdjpy_h4.index)


def test_direction_flip_report_contains_control_language():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()

    diagnostic = run_h024_direction_flip_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        bridge_config=_bridge_config(),
    )

    report = format_h024_direction_flip_report(diagnostic)

    assert "H024 direction-flip negative-control diagnostic" in report
    assert "Research only. No demo/live/Phase 4 approval." in report
    assert "Direction-flip total PnL USD" in report
    assert "curve-fit risk increases" in report


def test_direction_flip_rejects_bad_hold_horizon():
    with pytest.raises(ValueError, match="hold_h4_bars must be positive"):
        build_direction_flip_h017_result(
            h024_result=run_h024_bridge_shim(
                usdjpy_ohlcv=_usdjpy_h4(),
                xauusd_ohlcv=_xauusd_h4(),
                config=_bridge_config(),
            ),
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            hold_h4_bars=0,
        )
