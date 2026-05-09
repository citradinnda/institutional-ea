from pathlib import Path

import pandas as pd

from quantcore.execution.h024_dry_run import DryRunConfig
from quantcore.execution.h024_dry_run_log import (
    build_h024_dry_run_actions,
    summarize_dry_run_actions,
    write_dry_run_actions_csv,
)
from quantcore.strategy.h017 import H017Result


def _index() -> pd.DatetimeIndex:
    return pd.date_range("2026-01-01 00:00", periods=8, freq="4h", tz="UTC")


def _h4(open_values):
    idx = _index()
    return pd.DataFrame(
        {
            "open": open_values,
            "high": [value + 1.0 for value in open_values],
            "low": [value - 1.0 for value in open_values],
            "close": [value + 0.5 for value in open_values],
        },
        index=idx,
    )


def _result() -> H017Result:
    idx = _index()
    positions = pd.DataFrame(
        {
            "USDJPY": [0.0, 0.01, 0.0, 0.0, -0.01, 0.0, 0.0, 0.0],
            "XAUUSD": [0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0],
        },
        index=idx,
    )
    signals = positions.copy()
    stops_long = pd.DataFrame(
        {
            "USDJPY": [99.0, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0],
            "XAUUSD": [1900.0, 1901.0, 1902.0, 1903.0, 1904.0, 1905.0, 1906.0, 1907.0],
        },
        index=idx,
    )
    stops_short = pd.DataFrame(
        {
            "USDJPY": [101.0, 102.0, 103.0, 104.0, 110.0, 111.0, 112.0, 113.0],
            "XAUUSD": [1910.0, 1911.0, 1912.0, 1913.0, 1914.0, 1915.0, 1916.0, 1917.0],
        },
        index=idx,
    )
    zeros = pd.DataFrame(0.0, index=idx, columns=["USDJPY", "XAUUSD"])
    zero_series = pd.Series(0.0, index=idx)

    return H017Result(
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
        vol_multipliers=zeros,
        heat_multipliers=zeros,
        heat_pre=zero_series,
        heat_post=zero_series,
        heat_binding=pd.Series(False, index=idx),
    )


def test_build_h024_dry_run_actions_blocks_when_kill_switch_disabled():
    actions = build_h024_dry_run_actions(
        h017_result=_result(),
        usdjpy_h4=_h4([100, 101, 102, 103, 104, 105, 106, 107]),
        xauusd_h4=_h4([1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907]),
        accepted_entry_times=tuple(_index()),
        config=DryRunConfig(),
        hold_h4_bars=1,
    )

    assert actions
    assert any(action.action == "BLOCKED" for action in actions)
    assert all(action.action != "WOULD_OPEN" for action in actions)


def test_build_h024_dry_run_actions_emits_would_open_when_enabled():
    actions = build_h024_dry_run_actions(
        h017_result=_result(),
        usdjpy_h4=_h4([100, 101, 102, 103, 104, 105, 106, 107]),
        xauusd_h4=_h4([1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907]),
        accepted_entry_times=tuple(_index()),
        config=DryRunConfig(kill_switch_enabled=True),
        hold_h4_bars=1,
    )

    summary = summarize_dry_run_actions(actions)

    assert summary["WOULD_OPEN"] >= 1
    assert summary["NO_ACTION"] >= 1
    assert all(not hasattr(action, "order_ticket") for action in actions)


def test_write_dry_run_actions_csv(tmp_path: Path):
    actions = build_h024_dry_run_actions(
        h017_result=_result(),
        usdjpy_h4=_h4([100, 101, 102, 103, 104, 105, 106, 107]),
        xauusd_h4=_h4([1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907]),
        accepted_entry_times=tuple(_index()),
        config=DryRunConfig(kill_switch_enabled=True),
        hold_h4_bars=1,
    )

    output_path = tmp_path / "actions.csv"
    write_dry_run_actions_csv(actions=actions, output_path=output_path)

    text = output_path.read_text(encoding="utf-8")
    assert "action,model_symbol,broker_symbol" in text
    assert "WOULD_OPEN" in text


def test_dry_run_log_modules_contain_no_mt5_order_send_dependency():
    for path in (
        Path("quantcore/execution/h024_dry_run_log.py"),
        Path("scripts/dry_run_h024_actions_real.py"),
    ):
        source = path.read_text(encoding="utf-8-sig")
        assert "MetaTrader5" not in source
        assert "mt5." not in source
        assert "order_send" not in source
        assert "OrderSend" not in source
