from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.strategy.h019 import apply_h019_chandelier_lifecycle


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