from __future__ import annotations

import pandas as pd
import pytest

from quantcore.data.bridge_windows import (
    CommonCompleteBridgeWindowAssessment,
    assess_common_complete_h4_m1_windows,
)


def _ohlc_frame(index: pd.DatetimeIndex) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": range(len(index)),
            "high": range(len(index)),
            "low": range(len(index)),
            "close": range(len(index)),
            "volume": range(len(index)),
        },
        index=index,
    )


def _h4_index(periods: int, *, start: str = "2021-07-02 13:00:00") -> pd.DatetimeIndex:
    return pd.date_range(start, periods=periods, freq="4h", tz="UTC")


def _m1_index(periods: int, *, start: str = "2021-07-02 13:00:00") -> pd.DatetimeIndex:
    return pd.date_range(start, periods=periods, freq="min", tz="UTC")


def _rejection_dict(result: CommonCompleteBridgeWindowAssessment) -> dict[str, int]:
    return {item.reason: item.count for item in result.rejection_counts}


def test_assess_common_complete_h4_m1_windows_accepts_exact_common_windows() -> None:
    h4 = _ohlc_frame(_h4_index(3))
    m1 = _ohlc_frame(_m1_index(480))

    result = assess_common_complete_h4_m1_windows(
        usdjpy_h4=h4,
        xauusd_h4=h4,
        usdjpy_m1=m1,
        xauusd_m1=m1,
    )

    assert isinstance(result, CommonCompleteBridgeWindowAssessment)
    assert result.candidate_common_h4_count == 3
    assert result.accepted_count == 2
    assert result.common_complete_count == 2
    assert result.usdjpy_complete_count == 2
    assert result.xauusd_complete_count == 2
    assert result.usdjpy_only_complete_count == 0
    assert result.xauusd_only_complete_count == 0
    assert result.rejected_count == 1
    assert result.accepted_timestamps.equals(_h4_index(2))
    assert result.first_accepted_timestamp == pd.Timestamp("2021-07-02 13:00:00", tz="UTC")
    assert result.last_accepted_timestamp == pd.Timestamp("2021-07-02 17:00:00", tz="UTC")


def test_assess_common_complete_h4_m1_windows_rejects_symbol_with_missing_m1_bar() -> None:
    h4 = _ohlc_frame(_h4_index(3))
    usdjpy_m1 = _ohlc_frame(_m1_index(480))
    xauusd_m1_index = _m1_index(480).delete(10)
    xauusd_m1 = _ohlc_frame(xauusd_m1_index)

    result = assess_common_complete_h4_m1_windows(
        usdjpy_h4=h4,
        xauusd_h4=h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
    )

    assert result.accepted_timestamps.equals(
        pd.DatetimeIndex([pd.Timestamp("2021-07-02 17:00:00", tz="UTC")])
    )
    assert result.accepted_count == 1
    assert result.usdjpy_complete_count == 2
    assert result.xauusd_complete_count == 1
    assert result.usdjpy_only_complete_count == 1
    assert result.xauusd_only_complete_count == 0
    assert result.rejected_count == 2
    assert _rejection_dict(result)["xauusd_m1_count_not_expected"] == 2


def test_assess_common_complete_h4_m1_windows_rejects_non_four_hour_next_h4_delta() -> None:
    usdjpy_h4_index = pd.DatetimeIndex(
        [
            pd.Timestamp("2021-07-02 13:00:00", tz="UTC"),
            pd.Timestamp("2021-07-02 17:00:00", tz="UTC"),
            pd.Timestamp("2021-07-03 01:00:00", tz="UTC"),
        ]
    )
    xauusd_h4_index = _h4_index(3)
    usdjpy_h4 = _ohlc_frame(usdjpy_h4_index)
    xauusd_h4 = _ohlc_frame(xauusd_h4_index)
    m1 = _ohlc_frame(_m1_index(480))

    result = assess_common_complete_h4_m1_windows(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=m1,
        xauusd_m1=m1,
    )

    assert result.accepted_timestamps.equals(
        pd.DatetimeIndex([pd.Timestamp("2021-07-02 13:00:00", tz="UTC")])
    )
    assert result.usdjpy_complete_count == 1
    assert result.xauusd_complete_count == 2
    assert result.xauusd_only_complete_count == 1
    assert _rejection_dict(result)["usdjpy_non_4h_next_h4_delta"] == 1


def test_assess_common_complete_h4_m1_windows_uses_common_h4_intersection_only() -> None:
    usdjpy_h4 = _ohlc_frame(_h4_index(4))
    xauusd_h4 = _ohlc_frame(_h4_index(3))
    m1 = _ohlc_frame(_m1_index(720))

    result = assess_common_complete_h4_m1_windows(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=m1,
        xauusd_m1=m1,
    )

    assert result.candidate_common_h4_count == 3
    assert result.accepted_count == 2


def test_assess_common_complete_h4_m1_windows_rejects_naive_index() -> None:
    h4 = _ohlc_frame(_h4_index(3))
    m1 = _ohlc_frame(_m1_index(480))
    naive_h4 = h4.copy()
    naive_h4.index = naive_h4.index.tz_localize(None)

    with pytest.raises(ValueError, match="timezone-aware UTC"):
        assess_common_complete_h4_m1_windows(
            usdjpy_h4=naive_h4,
            xauusd_h4=h4,
            usdjpy_m1=m1,
            xauusd_m1=m1,
        )


def test_assess_common_complete_h4_m1_windows_rejects_unsorted_index() -> None:
    h4 = _ohlc_frame(_h4_index(3))
    m1 = _ohlc_frame(_m1_index(480))
    unsorted_m1 = m1.iloc[[1, 0, *range(2, len(m1))]]

    with pytest.raises(ValueError, match="sorted ascending"):
        assess_common_complete_h4_m1_windows(
            usdjpy_h4=h4,
            xauusd_h4=h4,
            usdjpy_m1=unsorted_m1,
            xauusd_m1=m1,
        )


def test_assess_common_complete_h4_m1_windows_rejects_duplicate_index() -> None:
    h4 = _ohlc_frame(_h4_index(3))
    m1 = _ohlc_frame(_m1_index(480))
    duplicate_h4 = pd.concat([h4, h4.iloc[[0]]]).sort_index()

    with pytest.raises(ValueError, match="duplicate timestamps"):
        assess_common_complete_h4_m1_windows(
            usdjpy_h4=duplicate_h4,
            xauusd_h4=h4,
            usdjpy_m1=m1,
            xauusd_m1=m1,
        )


def test_assess_common_complete_h4_m1_windows_rejects_missing_ohlc_columns() -> None:
    h4 = _ohlc_frame(_h4_index(3))
    m1 = _ohlc_frame(_m1_index(480))
    missing_close = h4.drop(columns=["close"])

    with pytest.raises(ValueError, match="missing"):
        assess_common_complete_h4_m1_windows(
            usdjpy_h4=missing_close,
            xauusd_h4=h4,
            usdjpy_m1=m1,
            xauusd_m1=m1,
        )


def test_assess_common_complete_h4_m1_windows_rejects_invalid_expected_counts() -> None:
    h4 = _ohlc_frame(_h4_index(3))
    m1 = _ohlc_frame(_m1_index(480))

    with pytest.raises(ValueError, match="expected_m1_bars_per_h4"):
        assess_common_complete_h4_m1_windows(
            usdjpy_h4=h4,
            xauusd_h4=h4,
            usdjpy_m1=m1,
            xauusd_m1=m1,
            expected_m1_bars_per_h4=0,
        )
