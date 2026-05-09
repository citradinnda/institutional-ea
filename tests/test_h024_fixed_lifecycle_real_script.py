import pandas as pd
import pytest

from quantcore.strategy.h020 import H020SizingConfig
from quantcore.strategy.h024 import H024SignalConfig
from quantcore.strategy.h024_runner import H024BridgeConfig
from scripts.diagnose_h024_fixed_lifecycle_real import (
    DEFAULT_H024_HOLD_H4_BARS,
    format_h024_diagnostic_report,
    format_h024_group_reports,
    run_h024_fixed_lifecycle_diagnostic,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _index() -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01 00:00", periods=12, freq="4h", tz="UTC")


def _usdjpy_h4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104, 105, 106, 105, 107, 108, 109, 110],
            "high": [101, 102, 103, 104, 105, 106, 107, 106, 109, 110, 111, 112],
            "low": [99, 100, 101, 102, 103, 104, 105, 104, 106, 107, 108, 109],
            "close": [101, 102, 103, 104, 105, 106, 106.5, 104.5, 108, 109, 110, 111],
        },
        index=_index(),
    )


def _xauusd_h4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [110, 109, 108, 107, 106, 105, 104, 105, 103, 102, 101, 100],
            "high": [111, 110, 109, 108, 107, 106, 105, 106, 104, 103, 102, 101],
            "low": [109, 108, 107, 106, 105, 104, 103, 104, 101, 100, 99, 98],
            "close": [109, 108, 107, 106, 105, 104, 103.5, 105.5, 102, 101, 100, 99],
        },
        index=_index(),
    )


def _m1_from_h4(h4: pd.DataFrame) -> pd.DataFrame:
    rows = []
    index = []
    for timestamp, row in h4.iterrows():
        index.append(timestamp)
        rows.append(
            {
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
            }
        )
    return pd.DataFrame(rows, index=pd.DatetimeIndex(index))


def _bridge_config() -> H024BridgeConfig:
    return H024BridgeConfig(
        signal_config=H024SignalConfig(
            slow_window=5,
            slope_lag=2,
            atr_window=3,
            pullback_window=3,
            min_pullback_atr=0.25,
            max_pullback_atr=3.0,
            min_slope_atr=0.05,
        ),
        sizing_config=H020SizingConfig(
            per_trade_max_gross_leverage=9.0,
            portfolio_max_gross_leverage=9.0,
        ),
        signed_risk_fraction=0.01,
        stop_atr_multiple=2.0,
        atr_window=3,
        starting_equity_usd=10_000.0,
    )


def test_h024_default_hold_horizons_are_pre_registered():
    assert DEFAULT_H024_HOLD_H4_BARS == (1, 2, 3, 4)


def test_h024_fixed_lifecycle_diagnostic_runs_on_synthetic_data():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()
    accepted = tuple(usdjpy_h4.index)

    runs = run_h024_fixed_lifecycle_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=accepted,
        hold_h4_bars_values=(1, 2),
        bridge_config=_bridge_config(),
    )

    assert [run.hold_h4_bars for run in runs] == [1, 2]
    assert all(run.summary.accepted_entry_count == len(accepted) for run in runs)
    assert all(run.summary.fill_count >= 1 for run in runs)
    assert "By symbol:" in runs[0].group_report
    assert "Chronological thirds:" in runs[0].group_report


def test_h024_diagnostic_report_contains_warning_and_summary_table():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()

    runs = run_h024_fixed_lifecycle_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        hold_h4_bars_values=(1,),
        bridge_config=_bridge_config(),
    )

    report = format_h024_diagnostic_report(runs)

    assert "H024 pullback-continuation fixed lifecycle diagnostic" in report
    assert "H024 fixed lifecycle summary" in report
    assert "No demo trading is approved. No live trading is approved. Phase 4 is not approved." in report
    assert "Detailed split report: hold=1 H4" in report


def test_h024_group_report_formatter_uses_keyword_helper_arguments():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()

    run = run_h024_fixed_lifecycle_diagnostic(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        hold_h4_bars_values=(1,),
        bridge_config=_bridge_config(),
    )[0]

    report = format_h024_group_reports(run.result)

    assert "By symbol:" in report
    assert "By side:" in report
    assert "Chronological halves:" in report
    assert "Chronological thirds:" in report
    assert "By calendar year:" in report
    assert "label | fills" in report


def test_h024_fixed_lifecycle_diagnostic_rejects_bad_inputs():
    with pytest.raises(ValueError, match="starting_equity_usd must be positive"):
        run_h024_fixed_lifecycle_diagnostic(
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
            xauusd_m1=_m1_from_h4(_xauusd_h4()),
            accepted_entry_times=tuple(_index()),
            starting_equity_usd=0.0,
            bridge_config=_bridge_config(),
        )

    with pytest.raises(ValueError, match="hold_h4_bars_values must be non-empty"):
        run_h024_fixed_lifecycle_diagnostic(
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
            xauusd_m1=_m1_from_h4(_xauusd_h4()),
            accepted_entry_times=tuple(_index()),
            hold_h4_bars_values=(),
            bridge_config=_bridge_config(),
        )

    with pytest.raises(ValueError, match="hold_h4_bars values must be positive"):
        run_h024_fixed_lifecycle_diagnostic(
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
            xauusd_m1=_m1_from_h4(_xauusd_h4()),
            accepted_entry_times=tuple(_index()),
            hold_h4_bars_values=(0,),
            bridge_config=_bridge_config(),
        )
