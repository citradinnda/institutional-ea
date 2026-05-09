import pandas as pd
import pytest

from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h020 import H020SizingConfig
from quantcore.strategy.h024 import H024SignalConfig
from quantcore.strategy.h024_runner import H024BridgeConfig, run_h024_bridge_shim


def _utc_range(count: int) -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01 00:00", periods=count, freq="4h", tz="UTC")


def _long_signal_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104, 105, 106, 105, 107, 108],
            "high": [101, 102, 103, 104, 105, 106, 107, 106, 109, 110],
            "low": [99, 100, 101, 102, 103, 104, 105, 104, 106, 107],
            "close": [101, 102, 103, 104, 105, 106, 106.5, 104.5, 108, 109],
        },
        index=_utc_range(10),
    )


def _short_signal_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [110, 109, 108, 107, 106, 105, 104, 105, 103, 102],
            "high": [111, 110, 109, 108, 107, 106, 105, 106, 104, 103],
            "low": [109, 108, 107, 106, 105, 104, 103, 104, 101, 100],
            "close": [109, 108, 107, 106, 105, 104, 103.5, 105.5, 102, 101],
        },
        index=_utc_range(10),
    )


def _config() -> H024BridgeConfig:
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


def test_h024_bridge_shim_returns_h017_compatible_result():
    result = run_h024_bridge_shim(
        usdjpy_ohlcv=_long_signal_frame(),
        xauusd_ohlcv=_short_signal_frame(),
        config=_config(),
    )

    assert isinstance(result, H017Result)
    assert list(result.positions.columns) == ["USDJPY", "XAUUSD"]
    assert list(result.signals.columns) == ["USDJPY", "XAUUSD"]
    assert list(result.stops_long.columns) == ["USDJPY", "XAUUSD"]
    assert list(result.stops_short.columns) == ["USDJPY", "XAUUSD"]


def test_h024_bridge_shim_preserves_raw_signal_intent_panel():
    result = run_h024_bridge_shim(
        usdjpy_ohlcv=_long_signal_frame(),
        xauusd_ohlcv=_short_signal_frame(),
        config=_config(),
    )

    assert result.signals["USDJPY"].iloc[8] == pytest.approx(0.01)
    assert result.signals["XAUUSD"].iloc[8] == pytest.approx(-0.01)
    assert result.signals.drop(index=result.signals.index[8]).eq(0.0).all().all()


def test_h024_bridge_shim_sized_positions_use_h020_timing():
    result = run_h024_bridge_shim(
        usdjpy_ohlcv=_long_signal_frame(),
        xauusd_ohlcv=_short_signal_frame(),
        config=_config(),
    )

    # The decision at index 8 can be sized because there is an entry bar at index 9.
    assert result.positions["USDJPY"].iloc[8] > 0.0
    assert result.positions["XAUUSD"].iloc[8] < 0.0

    # The final bar has no next entry bar and therefore no sized bridge position.
    assert result.positions.iloc[-1].eq(0.0).all()


def test_h024_bridge_shim_creates_protective_stop_geometry():
    result = run_h024_bridge_shim(
        usdjpy_ohlcv=_long_signal_frame(),
        xauusd_ohlcv=_short_signal_frame(),
        config=_config(),
    )

    decision_time = result.positions.index[8]
    entry_time = result.positions.index[9]
    usdjpy_entry = _long_signal_frame().at[entry_time, "open"]
    xauusd_entry = _short_signal_frame().at[entry_time, "open"]

    assert result.stops_long.at[decision_time, "USDJPY"] < usdjpy_entry
    assert result.stops_short.at[decision_time, "XAUUSD"] > xauusd_entry


def test_h024_bridge_shim_suppresses_when_no_next_entry_bar():
    short_frame = _long_signal_frame().iloc[:9].copy()

    result = run_h024_bridge_shim(
        usdjpy_ohlcv=short_frame,
        xauusd_ohlcv=_short_signal_frame().iloc[:9].copy(),
        config=_config(),
    )

    assert result.signals["USDJPY"].iloc[-1] == pytest.approx(0.01)
    assert result.signals["XAUUSD"].iloc[-1] == pytest.approx(-0.01)
    assert result.positions.iloc[-1].eq(0.0).all()


def test_h024_bridge_shim_aligns_to_common_symbol_index():
    usdjpy = _long_signal_frame()
    xauusd = pd.concat(
        [
            _short_signal_frame().iloc[:5],
            pd.DataFrame(
                {
                    "open": [999.0],
                    "high": [1000.0],
                    "low": [998.0],
                    "close": [999.5],
                },
                index=pd.DatetimeIndex([pd.Timestamp("2024-01-03 00:00", tz="UTC")]),
            ),
            _short_signal_frame().iloc[5:],
        ]
    ).sort_index()

    result = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy,
        xauusd_ohlcv=xauusd,
        config=_config(),
    )

    assert result.positions.index.equals(usdjpy.index)
    assert pd.Timestamp("2024-01-03 00:00", tz="UTC") not in result.positions.index


def test_h024_bridge_shim_rejects_no_common_indices():
    usdjpy = _long_signal_frame()
    xauusd = _short_signal_frame().copy()
    xauusd.index = pd.date_range("2024-02-01 00:00", periods=len(xauusd), freq="4h", tz="UTC")

    with pytest.raises(ValueError, match="no common H4 timestamps"):
        run_h024_bridge_shim(
            usdjpy_ohlcv=usdjpy,
            xauusd_ohlcv=xauusd,
            config=_config(),
        )


def test_h024_bridge_shim_rejects_bad_config():
    with pytest.raises(ValueError, match="signed_risk_fraction must be positive"):
        run_h024_bridge_shim(
            usdjpy_ohlcv=_long_signal_frame(),
            xauusd_ohlcv=_short_signal_frame(),
            config=H024BridgeConfig(signed_risk_fraction=0.0),
        )

    with pytest.raises(ValueError, match="stop_atr_multiple must be positive"):
        run_h024_bridge_shim(
            usdjpy_ohlcv=_long_signal_frame(),
            xauusd_ohlcv=_short_signal_frame(),
            config=H024BridgeConfig(stop_atr_multiple=0.0),
        )


def test_h024_bridge_shim_rejects_bad_h4_frame():
    bad = _long_signal_frame().drop(columns=["open"])

    with pytest.raises(ValueError, match="USDJPY missing required OHLC columns"):
        run_h024_bridge_shim(
            usdjpy_ohlcv=bad,
            xauusd_ohlcv=_short_signal_frame(),
            config=_config(),
        )

    with pytest.raises(ValueError, match="USDJPY must use a DatetimeIndex"):
        run_h024_bridge_shim(
            usdjpy_ohlcv=_long_signal_frame().reset_index(drop=True),
            xauusd_ohlcv=_short_signal_frame(),
            config=_config(),
        )
