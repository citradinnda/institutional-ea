import pandas as pd
import pytest

from quantcore.strategy.h020 import H020SizingConfig
from quantcore.strategy.h024 import H024SignalConfig
from quantcore.strategy.h024_runner import H024BridgeConfig, run_h024_bridge_shim
from scripts.diagnose_h024_timestamp_shuffle_real import (
    DEFAULT_H024_TIMESTAMP_SHUFFLE_HOLD_H4_BARS,
    build_timestamp_shuffled_h017_result,
    format_h024_timestamp_shuffle_report,
    run_h024_timestamp_shuffle_diagnostic,
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


def test_timestamp_shuffle_preserves_shape_and_is_deterministic():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()
    h024 = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=_bridge_config(),
    )

    first = build_timestamp_shuffled_h017_result(
        h024_result=h024,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        accepted_entry_times=tuple(usdjpy_h4.index),
        seed=123,
    )
    second = build_timestamp_shuffled_h017_result(
        h024_result=h024,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        accepted_entry_times=tuple(usdjpy_h4.index),
        seed=123,
    )

    pd.testing.assert_frame_equal(first.positions, second.positions)
    assert first.positions.shape == h024.positions.shape
    assert first.stops_long.shape == h024.stops_long.shape
    assert first.stops_short.shape == h024.stops_short.shape


def test_timestamp_shuffle_diagnostic_runs_on_synthetic_data():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()

    diagnostic = run_h024_timestamp_shuffle_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        shuffle_runs=3,
        seed=100,
        bridge_config=_bridge_config(),
    )

    assert diagnostic.baseline_summary.hold_h4_bars == DEFAULT_H024_TIMESTAMP_SHUFFLE_HOLD_H4_BARS
    assert len(diagnostic.shuffle_summaries) == 3
    assert [row.seed for row in diagnostic.shuffle_summaries] == [100, 101, 102]


def test_timestamp_shuffle_report_contains_exceedance_language():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()

    diagnostic = run_h024_timestamp_shuffle_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        shuffle_runs=3,
        seed=100,
        bridge_config=_bridge_config(),
    )

    report = format_h024_timestamp_shuffle_report(diagnostic)

    assert "H024 timestamp-shuffle negative-control diagnostic" in report
    assert "Timestamp-shuffle distribution:" in report
    assert "Empirical exceedance rate:" in report
    assert "curve-fit risk increases" in report


def test_timestamp_shuffle_rejects_bad_inputs():
    with pytest.raises(ValueError, match="shuffle_runs must be positive"):
        run_h024_timestamp_shuffle_diagnostic(
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
            xauusd_m1=_m1_from_h4(_xauusd_h4()),
            accepted_entry_times=tuple(_index()),
            shuffle_runs=0,
            bridge_config=_bridge_config(),
        )

    with pytest.raises(ValueError, match="hold_h4_bars must be positive"):
        build_timestamp_shuffled_h017_result(
            h024_result=run_h024_bridge_shim(
                usdjpy_ohlcv=_usdjpy_h4(),
                xauusd_ohlcv=_xauusd_h4(),
                config=_bridge_config(),
            ),
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            accepted_entry_times=tuple(_index()),
            seed=1,
            hold_h4_bars=0,
        )
