from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pandas as pd

from quantcore.backtest.h019_strict_event import (
    backtest_h019_strict_event,
    backtest_h019_strict_event_from_result,
)
from quantcore.strategy.h017 import H017Config, H017Result


def _idx(n: int) -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC")


def _ohlcv(n: int) -> pd.DataFrame:
    index = _idx(n)
    return pd.DataFrame(
        {
            "open": [100.0 + i for i in range(n)],
            "high": [101.0 + i for i in range(n)],
            "low": [99.0 + i for i in range(n)],
            "close": [100.5 + i for i in range(n)],
            "volume": [1000.0 for _ in range(n)],
        },
        index=index,
    )


def _fake_h017_result(index: pd.DatetimeIndex) -> H017Result:
    columns = ["USDJPY", "XAUUSD"]
    frame = pd.DataFrame(0.0, index=index, columns=columns)
    return H017Result(
        positions=frame.copy(),
        signals=frame.copy(),
        stops_long=frame.copy(),
        stops_short=frame.copy(),
        vol_multipliers=frame.copy(),
        heat_multipliers=frame.copy(),
        heat_pre=pd.Series(0.0, index=index),
        heat_post=pd.Series(0.0, index=index),
        heat_binding=pd.Series(False, index=index),
    )


def test_backtest_h019_strict_event_routes_run_h019_result_to_strict_bridge(
    monkeypatch: Any,
) -> None:
    usdjpy_h4 = _ohlcv(4)
    xauusd_h4 = _ohlcv(4)
    config = H017Config.default()
    fake_result = _fake_h017_result(usdjpy_h4.index)
    calls: dict[str, Any] = {}

    def fake_run_h019(
        *,
        usdjpy_ohlcv: pd.DataFrame,
        xauusd_ohlcv: pd.DataFrame,
        config: H017Config | None,
    ) -> H017Result:
        calls["run_h019_usdjpy"] = usdjpy_ohlcv
        calls["run_h019_xauusd"] = xauusd_ohlcv
        calls["run_h019_config"] = config
        return fake_result

    def fake_bridge(
        *,
        h017_result: H017Result,
        usdjpy_h4: pd.DataFrame,
        xauusd_h4: pd.DataFrame,
        **kwargs: Any,
    ) -> SimpleNamespace:
        calls["bridge_result"] = h017_result
        calls["bridge_usdjpy_h4"] = usdjpy_h4
        calls["bridge_xauusd_h4"] = xauusd_h4
        calls["bridge_kwargs"] = kwargs
        return SimpleNamespace(ok=True)

    monkeypatch.setattr(
        "quantcore.backtest.h019_strict_event.run_h019",
        fake_run_h019,
    )
    monkeypatch.setattr(
        "quantcore.backtest.h019_strict_event.backtest_h017_strict_event_from_result",
        fake_bridge,
    )

    result = backtest_h019_strict_event(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        config=config,
        accepted_entry_times="accepted",
        usdjpy_m1="usdjpy_m1",
        xauusd_m1="xauusd_m1",
        starting_equity_usd=100_000.0,
    )

    assert result.ok is True
    assert calls["run_h019_usdjpy"] is usdjpy_h4
    assert calls["run_h019_xauusd"] is xauusd_h4
    assert calls["run_h019_config"] is config
    assert calls["bridge_result"] is fake_result
    assert calls["bridge_usdjpy_h4"] is usdjpy_h4
    assert calls["bridge_xauusd_h4"] is xauusd_h4
    assert calls["bridge_kwargs"]["accepted_entry_times"] == "accepted"
    assert calls["bridge_kwargs"]["usdjpy_m1"] == "usdjpy_m1"
    assert calls["bridge_kwargs"]["xauusd_m1"] == "xauusd_m1"
    assert calls["bridge_kwargs"]["starting_equity_usd"] == 100_000.0


def test_backtest_h019_strict_event_from_result_routes_to_existing_bridge(
    monkeypatch: Any,
) -> None:
    h019_result = _fake_h017_result(_idx(3))
    calls: dict[str, Any] = {}

    def fake_bridge(
        *,
        h017_result: H017Result,
        **kwargs: Any,
    ) -> SimpleNamespace:
        calls["bridge_result"] = h017_result
        calls["bridge_kwargs"] = kwargs
        return SimpleNamespace(ok=True)

    monkeypatch.setattr(
        "quantcore.backtest.h019_strict_event.backtest_h017_strict_event_from_result",
        fake_bridge,
    )

    result = backtest_h019_strict_event_from_result(
        h019_result=h019_result,
        accepted_entry_times="accepted",
        starting_equity_usd=50_000.0,
    )

    assert result.ok is True
    assert calls["bridge_result"] is h019_result
    assert calls["bridge_kwargs"]["accepted_entry_times"] == "accepted"
    assert calls["bridge_kwargs"]["starting_equity_usd"] == 50_000.0
