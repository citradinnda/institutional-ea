from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pandas as pd


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "run_h019_strict_event_real.py"
)


def _load_script_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "run_h019_strict_event_real_under_test",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load run_h019_strict_event_real.py spec.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _ohlcv(index: pd.DatetimeIndex) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100.0 + i for i in range(len(index))],
            "high": [101.0 + i for i in range(len(index))],
            "low": [99.0 + i for i in range(len(index))],
            "close": [100.5 + i for i in range(len(index))],
            "volume": [1000.0 for _ in range(len(index))],
        },
        index=index,
    )


def test_h019_real_runner_run_validation_routes_through_h019(
    monkeypatch: Any,
) -> None:
    module = _load_script_module()

    index = pd.date_range("2024-01-01", periods=4, freq="4h", tz="UTC")
    loaded = module.LoadedMarketData(
        usdjpy_h4=SimpleNamespace(bars=_ohlcv(index)),
        xauusd_h4=SimpleNamespace(bars=_ohlcv(index)),
        usdjpy_m1=SimpleNamespace(bars=_ohlcv(index)),
        xauusd_m1=SimpleNamespace(bars=_ohlcv(index)),
    )
    assessment = SimpleNamespace(
        accepted_timestamps=index[1:3],
    )

    portfolio = SimpleNamespace(
        returns=pd.Series([0.0, 0.01, -0.002], index=index[:3]),
    )
    strict_result = SimpleNamespace(
        backtest=SimpleNamespace(portfolio=portfolio),
    )

    calls: dict[str, Any] = {}

    def fake_assess_bridge_windows(loaded_arg: Any) -> Any:
        calls["assessed_loaded"] = loaded_arg
        return assessment

    def fake_assert_expected_bridge_window_assessment(assessment_arg: Any) -> None:
        calls["asserted_assessment"] = assessment_arg

    def fake_backtest_h019_strict_event(**kwargs: Any) -> Any:
        calls["h019_kwargs"] = kwargs
        return strict_result

    def fake_build_claim(returns: pd.Series, *, periods_per_year: int) -> Any:
        calls["claim_returns"] = returns
        calls["claim_periods_per_year"] = periods_per_year
        return SimpleNamespace(summary="fake claim", promotable=False)

    monkeypatch.setattr(module, "_load_market_data", lambda: loaded)
    monkeypatch.setattr(module, "_assess_bridge_windows", fake_assess_bridge_windows)
    monkeypatch.setattr(
        module,
        "_assert_expected_bridge_window_assessment",
        fake_assert_expected_bridge_window_assessment,
    )
    monkeypatch.setattr(
        module,
        "backtest_h019_strict_event",
        fake_backtest_h019_strict_event,
    )
    monkeypatch.setattr(module, "build_h017_claim", fake_build_claim)

    result = module.run_validation()

    assert result.backtest is strict_result
    assert result.bridge_window_assessment is assessment
    assert result.claim.summary == "fake claim"

    assert calls["assessed_loaded"] is loaded
    assert calls["asserted_assessment"] is assessment

    h019_kwargs = calls["h019_kwargs"]
    assert h019_kwargs["usdjpy_h4"] is loaded.usdjpy_h4.bars
    assert h019_kwargs["xauusd_h4"] is loaded.xauusd_h4.bars
    assert h019_kwargs["usdjpy_m1"] is loaded.usdjpy_m1.bars
    assert h019_kwargs["xauusd_m1"] is loaded.xauusd_m1.bars
    assert h019_kwargs["accepted_entry_times"] is assessment.accepted_timestamps
    assert h019_kwargs["expected_h4_delta"] == module.EXPECTED_H4_DELTA

    assert calls["claim_returns"] is portfolio.returns
    assert calls["claim_periods_per_year"] == module.PERIODS_PER_YEAR_H4


def test_h019_real_runner_imports_h019_strict_route() -> None:
    module = _load_script_module()

    assert (
        module.backtest_h019_strict_event.__module__
        == "quantcore.backtest.h019_strict_event"
    )
