from types import SimpleNamespace

import pandas as pd
import pytest

from quantcore.backtest.h018_guard_scan import (
    H018GuardScanResult,
    scan_h018_guard_violations_from_masked_result,
)


def _times() -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01", periods=4, freq="4h", tz="UTC")


def _h4_panel(times: pd.DatetimeIndex, open_price: float) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [open_price] * len(times),
            "high": [open_price + 1.0] * len(times),
            "low": [open_price - 1.0] * len(times),
            "close": [open_price] * len(times),
        },
        index=times,
    )


def _h017_like_result(
    *,
    times: pd.DatetimeIndex,
    usdjpy_position: float = 0.0,
    xauusd_position: float = 0.0,
    usdjpy_long_stop: float = 149.0,
    usdjpy_short_stop: float = 151.0,
    xauusd_long_stop: float = 1790.0,
    xauusd_short_stop: float = 1810.0,
) -> SimpleNamespace:
    positions = pd.DataFrame(0.0, index=times, columns=["USDJPY", "XAUUSD"])
    positions.at[times[0], "USDJPY"] = usdjpy_position
    positions.at[times[0], "XAUUSD"] = xauusd_position

    stops_long = pd.DataFrame(
        {
            "USDJPY": [usdjpy_long_stop] * len(times),
            "XAUUSD": [xauusd_long_stop] * len(times),
        },
        index=times,
    )
    stops_short = pd.DataFrame(
        {
            "USDJPY": [usdjpy_short_stop] * len(times),
            "XAUUSD": [xauusd_short_stop] * len(times),
        },
        index=times,
    )

    return SimpleNamespace(
        positions=positions,
        stops_long=stops_long,
        stops_short=stops_short,
    )


def test_scan_counts_invalid_directional_stop_and_continues() -> None:
    times = _times()
    h017_result = _h017_like_result(
        times=times,
        xauusd_position=-0.01,
        xauusd_short_stop=1786.0,
    )

    result = scan_h018_guard_violations_from_masked_result(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": _h4_panel(times, 150.0),
            "XAUUSD": _h4_panel(times, 1791.0),
        },
    )

    assert result.trade_intent_count == 1
    assert result.candidate_count == 0
    assert result.violation_count == 1
    assert result.violation_counts_by_guard == {"invalid_directional_stop": 1}
    assert result.violation_counts_by_symbol == {"XAUUSD": 1}

    violation = result.violations[0]
    assert violation.symbol == "XAUUSD"
    assert violation.side == "sell"
    assert violation.entry_raw_price == 1791.0
    assert violation.stop_price == 1786.0


def test_scan_valid_candidate_has_no_violations() -> None:
    times = _times()
    h017_result = _h017_like_result(
        times=times,
        xauusd_position=0.01,
        xauusd_long_stop=1790.0,
    )

    result = scan_h018_guard_violations_from_masked_result(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": _h4_panel(times, 150.0),
            "XAUUSD": _h4_panel(times, 1800.0),
        },
    )

    assert result.trade_intent_count == 1
    assert result.candidate_count == 1
    assert result.violation_count == 0


def test_scan_counts_minimum_stop_distance_violation() -> None:
    times = _times()
    h017_result = _h017_like_result(
        times=times,
        xauusd_position=0.01,
        xauusd_long_stop=1799.9,
    )

    result = scan_h018_guard_violations_from_masked_result(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": _h4_panel(times, 150.0),
            "XAUUSD": _h4_panel(times, 1800.0),
        },
    )

    assert result.trade_intent_count == 1
    assert result.candidate_count == 0
    assert result.violation_count == 1
    assert result.violation_counts_by_guard == {"minimum_stop_distance": 1}


def test_scan_rejects_non_positive_starting_equity() -> None:
    times = _times()
    h017_result = _h017_like_result(times=times)

    with pytest.raises(ValueError, match="starting_equity_usd must be positive"):
        scan_h018_guard_violations_from_masked_result(
            h017_result=h017_result,
            h4_by_symbol={
                "USDJPY": _h4_panel(times, 150.0),
                "XAUUSD": _h4_panel(times, 1800.0),
            },
            starting_equity_usd=0.0,
        )


def test_empty_scan_result_properties() -> None:
    result = H018GuardScanResult(
        event_interval_count=0,
        trade_intent_count=0,
        candidate_count=0,
        skipped_intent_count=0,
        accepted_entry_count=None,
        executed_entry_count=None,
        skipped_entry_count=None,
        violations=(),
    )

    assert result.violation_count == 0
    assert result.violation_counts_by_guard == {}
    assert result.violation_counts_by_symbol == {}
