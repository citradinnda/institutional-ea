from types import SimpleNamespace

import pandas as pd

from quantcore.backtest.h018_invalid_stop_cause import (
    diagnose_invalid_stop_causes_from_masked_result,
)


def _times() -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01", periods=4, freq="4h", tz="UTC")


def _h4_panel(
    times: pd.DatetimeIndex,
    *,
    decision_close: float,
    entry_open: float,
) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "open": [100.0] * len(times),
            "high": [101.0] * len(times),
            "low": [99.0] * len(times),
            "close": [100.0] * len(times),
        },
        index=times,
    )
    frame.at[times[0], "close"] = decision_close
    frame.at[times[1], "open"] = entry_open
    return frame


def _h017_like_result(
    *,
    times: pd.DatetimeIndex,
    symbol: str,
    position: float,
    stop_price: float,
) -> SimpleNamespace:
    positions = pd.DataFrame(0.0, index=times, columns=["USDJPY", "XAUUSD"])
    positions.at[times[0], symbol] = position

    stops_long = pd.DataFrame(1.0, index=times, columns=["USDJPY", "XAUUSD"])
    stops_short = pd.DataFrame(9999.0, index=times, columns=["USDJPY", "XAUUSD"])

    if position > 0.0:
        stops_long.at[times[0], symbol] = stop_price
    else:
        stops_short.at[times[0], symbol] = stop_price

    return SimpleNamespace(
        positions=positions,
        stops_long=stops_long,
        stops_short=stops_short,
    )


def test_classifies_buy_stop_crossed_between_decision_and_entry() -> None:
    times = _times()
    h017_result = _h017_like_result(
        times=times,
        symbol="USDJPY",
        position=0.01,
        stop_price=99.5,
    )

    result = diagnose_invalid_stop_causes_from_masked_result(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": _h4_panel(times, decision_close=100.0, entry_open=99.0),
            "XAUUSD": _h4_panel(times, decision_close=1800.0, entry_open=1800.0),
        },
    )

    assert result.trade_intent_count == 1
    assert result.invalid_at_entry_count == 1
    assert result.cause_counts == {"crossed_between_decision_close_and_entry_open": 1}

    obs = result.observations[0]
    assert obs.valid_at_decision_close is True
    assert obs.valid_at_entry_open is False
    assert obs.decision_margin == 0.5
    assert obs.entry_margin == -0.5


def test_classifies_sell_stop_already_invalid_at_decision() -> None:
    times = _times()
    h017_result = _h017_like_result(
        times=times,
        symbol="XAUUSD",
        position=-0.01,
        stop_price=1790.0,
    )

    result = diagnose_invalid_stop_causes_from_masked_result(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": _h4_panel(times, decision_close=150.0, entry_open=150.0),
            "XAUUSD": _h4_panel(times, decision_close=1800.0, entry_open=1801.0),
        },
    )

    assert result.trade_intent_count == 1
    assert result.invalid_at_entry_count == 1
    assert result.cause_counts == {"already_invalid_at_decision_close": 1}

    obs = result.observations[0]
    assert obs.valid_at_decision_close is False
    assert obs.valid_at_entry_open is False
    assert obs.decision_margin == -10.0
    assert obs.entry_margin == -11.0


def test_valid_at_entry_stop_is_not_reported() -> None:
    times = _times()
    h017_result = _h017_like_result(
        times=times,
        symbol="XAUUSD",
        position=0.01,
        stop_price=1790.0,
    )

    result = diagnose_invalid_stop_causes_from_masked_result(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": _h4_panel(times, decision_close=150.0, entry_open=150.0),
            "XAUUSD": _h4_panel(times, decision_close=1800.0, entry_open=1801.0),
        },
    )

    assert result.trade_intent_count == 1
    assert result.invalid_at_entry_count == 0
    assert result.cause_counts == {}
    assert result.observations == ()


def test_empty_short_index_returns_empty_diagnostic() -> None:
    times = pd.date_range("2024-01-01", periods=2, freq="4h", tz="UTC")
    h017_result = SimpleNamespace(
        positions=pd.DataFrame(0.0, index=times, columns=["USDJPY", "XAUUSD"]),
        stops_long=pd.DataFrame(1.0, index=times, columns=["USDJPY", "XAUUSD"]),
        stops_short=pd.DataFrame(9999.0, index=times, columns=["USDJPY", "XAUUSD"]),
    )

    result = diagnose_invalid_stop_causes_from_masked_result(
        h017_result=h017_result,
        h4_by_symbol={
            "USDJPY": _h4_panel(times, decision_close=150.0, entry_open=150.0),
            "XAUUSD": _h4_panel(times, decision_close=1800.0, entry_open=1800.0),
        },
    )

    assert result.event_interval_count == 0
    assert result.trade_intent_count == 0
    assert result.invalid_at_entry_count == 0
