from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.strategy.h019 import apply_h019_chandelier_lifecycle
from types import SimpleNamespace

from quantcore.strategy.h017 import H017Config, H017Result
from quantcore.strategy.h019 import run_h019


def _idx(n: int) -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC")


def test_h019_flattens_long_on_same_side_chandelier_breach_and_does_not_reenter_stale_signal() -> None:
    index = _idx(6)

    held_signal = pd.Series([np.nan, 1.0, 1.0, 1.0, 1.0, 1.0], index=index)
    close = pd.Series([100.0, 105.0, 106.0, 99.0, 101.0, 102.0], index=index)
    stops_long = pd.Series([np.nan, 100.0, 101.0, 100.0, 100.0, 100.0], index=index)
    stops_short = pd.Series([np.nan, 110.0, 111.0, 112.0, 113.0, 114.0], index=index)

    result = apply_h019_chandelier_lifecycle(
        held_signal=held_signal,
        close=close,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    assert result.signals.tolist() == [0.0, 1.0, 1.0, 0.0, 0.0, 0.0]
    assert result.entries.tolist() == [False, True, False, False, False, False]
    assert result.exits.tolist() == [False, False, False, True, False, False]
    assert pd.isna(result.selected_stops.iloc[0])
    assert result.selected_stops.iloc[1] == 100.0
    assert result.selected_stops.iloc[2] == 101.0
    assert pd.isna(result.selected_stops.iloc[3])
    assert pd.isna(result.selected_stops.iloc[4])
    assert pd.isna(result.selected_stops.iloc[5])


def test_h019_flattens_short_on_same_side_chandelier_breach_and_does_not_reenter_stale_signal() -> None:
    index = _idx(6)

    held_signal = pd.Series([0.0, -1.0, -1.0, -1.0, -1.0, -1.0], index=index)
    close = pd.Series([100.0, 95.0, 94.0, 101.0, 99.0, 98.0], index=index)
    stops_long = pd.Series([90.0, 89.0, 88.0, 87.0, 86.0, 85.0], index=index)
    stops_short = pd.Series([np.nan, 100.0, 99.0, 100.0, 100.0, 100.0], index=index)

    result = apply_h019_chandelier_lifecycle(
        held_signal=held_signal,
        close=close,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    assert result.signals.tolist() == [0.0, -1.0, -1.0, 0.0, 0.0, 0.0]
    assert result.entries.tolist() == [False, True, False, False, False, False]
    assert result.exits.tolist() == [False, False, False, True, False, False]


def test_h019_can_reenter_only_after_visible_donchian_side_change() -> None:
    index = _idx(8)

    held_signal = pd.Series(
        [0.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0],
        index=index,
    )
    close = pd.Series([100.0, 105.0, 99.0, 101.0, 95.0, 96.0, 106.0, 107.0], index=index)
    stops_long = pd.Series([90.0, 100.0, 100.0, 100.0, 90.0, 90.0, 100.0, 101.0], index=index)
    stops_short = pd.Series([110.0, 110.0, 110.0, 110.0, 100.0, 99.0, 112.0, 113.0], index=index)

    result = apply_h019_chandelier_lifecycle(
        held_signal=held_signal,
        close=close,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    assert result.signals.tolist() == [0.0, 1.0, 0.0, 0.0, -1.0, -1.0, 1.0, 1.0]
    assert result.entries.tolist() == [False, True, False, False, True, False, True, False]
    assert result.exits.tolist() == [False, False, True, False, False, False, False, False]


def test_h019_uses_same_side_stop_panel_only() -> None:
    index = _idx(4)

    held_signal = pd.Series([0.0, 1.0, 1.0, 1.0], index=index)
    close = pd.Series([100.0, 105.0, 99.0, 108.0], index=index)

    # Long stop is breached on bar 2. Short stop is "protective" for a short,
    # but H019 must not switch panels to keep the long alive.
    stops_long = pd.Series([90.0, 100.0, 100.0, 100.0], index=index)
    stops_short = pd.Series([110.0, 110.0, 110.0, 110.0], index=index)

    result = apply_h019_chandelier_lifecycle(
        held_signal=held_signal,
        close=close,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    assert result.signals.tolist() == [0.0, 1.0, 0.0, 0.0]
    assert result.selected_stops.iloc[1] == 100.0
    assert pd.isna(result.selected_stops.iloc[2])
    assert pd.isna(result.selected_stops.iloc[3])


def test_h019_rejects_misaligned_inputs() -> None:
    index = _idx(3)
    other_index = pd.date_range("2024-01-02", periods=3, freq="4h", tz="UTC")

    held_signal = pd.Series([0.0, 1.0, 1.0], index=index)
    close = pd.Series([100.0, 101.0, 102.0], index=other_index)
    stops_long = pd.Series([90.0, 91.0, 92.0], index=index)
    stops_short = pd.Series([110.0, 111.0, 112.0], index=index)

    with pytest.raises(ValueError, match="close.index must equal held_signal.index"):
        apply_h019_chandelier_lifecycle(
            held_signal=held_signal,
            close=close,
            stops_long=stops_long,
            stops_short=stops_short,
        )
def _ohlcv_from_close(close: list[float]) -> pd.DataFrame:
    index = _idx(len(close))
    close_series = pd.Series(close, index=index, dtype="float64")
    open_series = close_series.shift(1).fillna(close_series.iloc[0])
    high = pd.concat([open_series, close_series], axis=1).max(axis=1) + 1.0
    low = pd.concat([open_series, close_series], axis=1).min(axis=1) - 1.0

    return pd.DataFrame(
        {
            "open": open_series,
            "high": high,
            "low": low,
            "close": close_series,
            "volume": 1000.0,
        },
        index=index,
    )


def test_run_h019_recomputes_positions_from_lifecycle_signals(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _idx(5)
    cfg = H017Config.default()

    base_signals = pd.DataFrame(
        {
            "USDJPY": [0.0, 1.0, 1.0, 1.0, 1.0],
            "XAUUSD": [0.0, 0.0, 0.0, 0.0, 0.0],
        },
        index=index,
    )
    base_stops_long = pd.DataFrame(
        {
            "USDJPY": [90.0, 100.0, 100.0, 100.0, 100.0],
            "XAUUSD": [1900.0, 1900.0, 1900.0, 1900.0, 1900.0],
        },
        index=index,
    )
    base_stops_short = pd.DataFrame(
        {
            "USDJPY": [110.0, 110.0, 110.0, 110.0, 110.0],
            "XAUUSD": [2100.0, 2100.0, 2100.0, 2100.0, 2100.0],
        },
        index=index,
    )
    base_vol = pd.DataFrame(
        {
            "USDJPY": [2.0, 2.0, 2.0, 2.0, 2.0],
            "XAUUSD": [1.0, 1.0, 1.0, 1.0, 1.0],
        },
        index=index,
    )

    fake_base = H017Result(
        positions=pd.DataFrame(0.123, index=index, columns=["USDJPY", "XAUUSD"]),
        signals=base_signals,
        stops_long=base_stops_long,
        stops_short=base_stops_short,
        vol_multipliers=base_vol,
        heat_multipliers=pd.DataFrame(1.0, index=index, columns=["USDJPY", "XAUUSD"]),
        heat_pre=pd.Series(0.0, index=index),
        heat_post=pd.Series(0.0, index=index),
        heat_binding=pd.Series(False, index=index),
    )

    def fake_run_h017(
        usdjpy_ohlcv: pd.DataFrame,
        xauusd_ohlcv: pd.DataFrame,
        config: H017Config,
    ) -> H017Result:
        return fake_base

    def fake_heat_governor(
        signals: pd.DataFrame,
        returns: pd.DataFrame,
        heat_config: object,
    ) -> SimpleNamespace:
        assert signals["USDJPY"].tolist() == [0.0, 1.0, 0.0, 0.0, 0.0]
        assert signals["XAUUSD"].tolist() == [0.0, 0.0, 0.0, 0.0, 0.0]

        multipliers = pd.DataFrame(
            0.5,
            index=signals.index,
            columns=["USDJPY", "XAUUSD"],
        )
        return SimpleNamespace(
            multipliers=multipliers,
            portfolio_heat_pre=pd.Series(0.0, index=signals.index),
            portfolio_heat_post=pd.Series(0.0, index=signals.index),
            binding=pd.Series(False, index=signals.index),
        )

    monkeypatch.setattr("quantcore.strategy.h019.run_h017", fake_run_h017)
    monkeypatch.setattr("quantcore.strategy.h019.heat_governor", fake_heat_governor)

    usdjpy = _ohlcv_from_close([100.0, 105.0, 99.0, 101.0, 102.0])
    xauusd = _ohlcv_from_close([2000.0, 2001.0, 2002.0, 2003.0, 2004.0])

    result = run_h019(usdjpy, xauusd, config=cfg)

    assert isinstance(result, H017Result)
    assert result.signals["USDJPY"].tolist() == [0.0, 1.0, 0.0, 0.0, 0.0]
    assert result.positions["USDJPY"].tolist() == [0.0, 0.01, 0.0, 0.0, 0.0]
    assert result.positions["XAUUSD"].tolist() == [0.0, 0.0, 0.0, 0.0, 0.0]


def test_run_h019_preserves_same_side_stop_panels(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _idx(4)
    cfg = H017Config.default()

    stops_long = pd.DataFrame(
        {
            "USDJPY": [90.0, 91.0, 92.0, 93.0],
            "XAUUSD": [1900.0, 1901.0, 1902.0, 1903.0],
        },
        index=index,
    )
    stops_short = pd.DataFrame(
        {
            "USDJPY": [110.0, 111.0, 112.0, 113.0],
            "XAUUSD": [2100.0, 2101.0, 2102.0, 2103.0],
        },
        index=index,
    )

    fake_base = H017Result(
        positions=pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"]),
        signals=pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"]),
        stops_long=stops_long,
        stops_short=stops_short,
        vol_multipliers=pd.DataFrame(1.0, index=index, columns=["USDJPY", "XAUUSD"]),
        heat_multipliers=pd.DataFrame(1.0, index=index, columns=["USDJPY", "XAUUSD"]),
        heat_pre=pd.Series(0.0, index=index),
        heat_post=pd.Series(0.0, index=index),
        heat_binding=pd.Series(False, index=index),
    )

    def fake_run_h017(
        usdjpy_ohlcv: pd.DataFrame,
        xauusd_ohlcv: pd.DataFrame,
        config: H017Config,
    ) -> H017Result:
        return fake_base

    def fake_heat_governor(
        signals: pd.DataFrame,
        returns: pd.DataFrame,
        heat_config: object,
    ) -> SimpleNamespace:
        return SimpleNamespace(
            multipliers=pd.DataFrame(1.0, index=signals.index, columns=signals.columns),
            portfolio_heat_pre=pd.Series(0.0, index=signals.index),
            portfolio_heat_post=pd.Series(0.0, index=signals.index),
            binding=pd.Series(False, index=signals.index),
        )

    monkeypatch.setattr("quantcore.strategy.h019.run_h017", fake_run_h017)
    monkeypatch.setattr("quantcore.strategy.h019.heat_governor", fake_heat_governor)

    usdjpy = _ohlcv_from_close([100.0, 101.0, 102.0, 103.0])
    xauusd = _ohlcv_from_close([2000.0, 2001.0, 2002.0, 2003.0])

    result = run_h019(usdjpy, xauusd, config=cfg)

    pd.testing.assert_frame_equal(result.stops_long, stops_long)
    pd.testing.assert_frame_equal(result.stops_short, stops_short)
