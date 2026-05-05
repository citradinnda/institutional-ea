from types import SimpleNamespace

import pandas as pd

from quantcore.backtest.h018_stop_state_diagnostic import diagnose_h018_stop_state


def _times() -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01", periods=5, freq="4h", tz="UTC")


def _h4_frame(times: pd.DatetimeIndex, closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": closes,
            "high": [value + 1.0 for value in closes],
            "low": [value - 1.0 for value in closes],
            "close": closes,
            "volume": [100.0] * len(times),
        },
        index=times,
    )


def _h017_like_result(times: pd.DatetimeIndex) -> SimpleNamespace:
    signals = pd.DataFrame(
        {
            "USDJPY": [float("nan"), 1.0, 1.0, -1.0, 0.0],
            "XAUUSD": [0.0, 0.0, 0.0, 0.0, 0.0],
        },
        index=times,
    )
    stops_long = pd.DataFrame(
        {
            "USDJPY": [float("nan"), 99.0, 104.0, 90.0, 90.0],
            "XAUUSD": [1700.0, 1700.0, 1700.0, 1700.0, 1700.0],
        },
        index=times,
    )
    stops_short = pd.DataFrame(
        {
            "USDJPY": [200.0, 200.0, 200.0, 102.0, 200.0],
            "XAUUSD": [1900.0, 1900.0, 1900.0, 1900.0, 1900.0],
        },
        index=times,
    )

    return SimpleNamespace(
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
    )


def test_counts_fresh_and_held_signal_stop_state() -> None:
    times = _times()
    result = diagnose_h018_stop_state(
        h017_result=_h017_like_result(times),
        h4_by_symbol={
            "USDJPY": _h4_frame(times, [100.0, 102.0, 103.0, 104.0, 105.0]),
            "XAUUSD": _h4_frame(times, [1800.0, 1801.0, 1802.0, 1803.0, 1804.0]),
        },
    )

    assert result.event_interval_count == 4
    assert result.total_nonzero_signal_count == 3
    assert result.nan_signal_skipped_count == 1
    assert result.flat_signal_skipped_count == 4
    assert result.unavailable_price_or_stop_skipped_count == 0

    assert result.same_side_stop_valid_at_decision_close_count == 1
    assert result.same_side_stop_breached_at_decision_close_count == 2

    assert result.fresh_signal_count == 2
    assert result.held_continuation_count == 1
    assert result.breached_fresh_signal_count == 1
    assert result.breached_held_continuation_count == 1

    assert result.bucket_counts_by_symbol_side == {
        "USDJPY:buy": {
            "total_nonzero_signal_count": 2,
            "same_side_stop_valid_at_decision_close_count": 1,
            "same_side_stop_breached_at_decision_close_count": 1,
            "fresh_signal_count": 1,
            "held_continuation_count": 1,
            "breached_fresh_signal_count": 0,
            "breached_held_continuation_count": 1,
        },
        "USDJPY:sell": {
            "total_nonzero_signal_count": 1,
            "same_side_stop_valid_at_decision_close_count": 0,
            "same_side_stop_breached_at_decision_close_count": 1,
            "fresh_signal_count": 1,
            "held_continuation_count": 0,
            "breached_fresh_signal_count": 1,
            "breached_held_continuation_count": 0,
        },
    }


def test_accepted_entry_times_filter_decision_windows() -> None:
    times = _times()
    result = diagnose_h018_stop_state(
        h017_result=_h017_like_result(times),
        h4_by_symbol={
            "USDJPY": _h4_frame(times, [100.0, 102.0, 103.0, 104.0, 105.0]),
            "XAUUSD": _h4_frame(times, [1800.0, 1801.0, 1802.0, 1803.0, 1804.0]),
        },
        accepted_entry_times=pd.DatetimeIndex([times[2]]),
    )

    assert result.event_interval_count == 4
    assert result.accepted_entry_count == 1
    assert result.skipped_entry_count == 3
    assert result.total_nonzero_signal_count == 1
    assert result.same_side_stop_valid_at_decision_close_count == 1
    assert result.same_side_stop_breached_at_decision_close_count == 0