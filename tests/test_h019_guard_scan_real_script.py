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
    / "scan_h019_guard_violations_real.py"
)


def _load_script_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "scan_h019_guard_violations_real_under_test",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load scan_h019_guard_violations_real.py spec.")

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


def test_h019_guard_diagnostic_routes_h019_result_through_existing_scanner(
    monkeypatch: Any,
) -> None:
    module = _load_script_module()

    index = pd.date_range("2024-01-01", periods=4, freq="4h", tz="UTC")
    loaded = module.LoadedBrokerNativeExports(
        usdjpy_h4=SimpleNamespace(bars=_ohlcv(index)),
        xauusd_h4=SimpleNamespace(bars=_ohlcv(index)),
        usdjpy_m1=SimpleNamespace(bars=_ohlcv(index)),
        xauusd_m1=SimpleNamespace(bars=_ohlcv(index)),
    )
    assessment = SimpleNamespace(
        accepted_timestamps=index[1:3],
    )
    h019_result = SimpleNamespace(positions="h019 positions")
    scan = SimpleNamespace(violation_count=0)

    calls: dict[str, Any] = {}

    def fake_assess_bridge_windows(loaded_arg: Any) -> Any:
        calls["assessed_loaded"] = loaded_arg
        return assessment

    def fake_assert_expected_bridge_window_assessment(assessment_arg: Any) -> None:
        calls["asserted_assessment"] = assessment_arg

    def fake_run_h019(**kwargs: Any) -> Any:
        calls["h019_kwargs"] = kwargs
        return h019_result

    def fake_scan_h018_guard_violations(**kwargs: Any) -> Any:
        calls["scan_kwargs"] = kwargs
        return scan

    monkeypatch.setattr(module, "_assess_bridge_windows", fake_assess_bridge_windows)
    monkeypatch.setattr(
        module,
        "_assert_expected_bridge_window_assessment",
        fake_assert_expected_bridge_window_assessment,
    )
    monkeypatch.setattr(module, "run_h019", fake_run_h019)
    monkeypatch.setattr(
        module,
        "scan_h018_guard_violations",
        fake_scan_h018_guard_violations,
    )

    result = module.build_h019_guard_diagnostic(loaded)

    assert result.bridge_window_assessment is assessment
    assert result.scan is scan

    assert calls["assessed_loaded"] is loaded
    assert calls["asserted_assessment"] is assessment

    h019_kwargs = calls["h019_kwargs"]
    assert h019_kwargs["usdjpy_ohlcv"] is loaded.usdjpy_h4.bars
    assert h019_kwargs["xauusd_ohlcv"] is loaded.xauusd_h4.bars

    scan_kwargs = calls["scan_kwargs"]
    assert scan_kwargs["h017_result"] is h019_result
    assert scan_kwargs["h4_by_symbol"]["USDJPY"] is loaded.usdjpy_h4.bars
    assert scan_kwargs["h4_by_symbol"]["XAUUSD"] is loaded.xauusd_h4.bars
    assert scan_kwargs["accepted_entry_times"] is assessment.accepted_timestamps
    assert scan_kwargs["expected_h4_delta"] == module.EXPECTED_H4_DELTA


def test_h019_guard_diagnostic_imports_h019_strategy_route() -> None:
    module = _load_script_module()

    assert module.run_h019.__module__ == "quantcore.strategy.h019"
