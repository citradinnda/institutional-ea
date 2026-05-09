import pandas as pd
import pytest

from quantcore.backtest.portfolio import fill_pnl_usd
from quantcore.strategy.h020 import H020SizingConfig
from quantcore.strategy.h024 import H024SignalConfig
from quantcore.strategy.h024_runner import H024BridgeConfig, run_h024_bridge_shim
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    backtest_fixed_lifecycle_from_result,
)
from scripts.diagnose_h024_trade_ledger_real import (
    DEFAULT_H024_LEDGER_HOLD_H4_BARS,
    build_h024_trade_ledger,
    format_h024_trade_ledger_audit_report,
    run_h024_trade_ledger_export,
)


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


def _synthetic_h024_result():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()
    h024 = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=_bridge_config(),
    )
    result = backtest_fixed_lifecycle_from_result(
        h017_result=h024,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        hold_h4_bars=DEFAULT_H024_LEDGER_HOLD_H4_BARS,
    )
    return h024, result, usdjpy_h4, xauusd_h4


def test_h024_trade_ledger_builds_fill_level_rows():
    h024, result, usdjpy_h4, xauusd_h4 = _synthetic_h024_result()

    ledger = build_h024_trade_ledger(
        h017_result=h024,
        fixed_lifecycle_result=result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
    )

    assert len(ledger) == len(result.fills)
    assert set(
        [
            "decision_time_utc",
            "stop_price",
            "raw_stop_distance",
            "lots",
            "interval_start_equity_usd",
            "actual_gross_leverage",
            "gross_leverage_vs_10000_usd",
            "pnl_usd",
        ]
    ).issubset(ledger.columns)
    assert (ledger["raw_stop_distance"] > 0.0).all()
    assert (ledger["lots"] > 0.0).all()
    assert (ledger["interval_start_equity_usd"] > 0.0).all()
    assert (ledger["actual_gross_leverage"] > 0.0).all()
    assert ledger["pnl_usd"].sum() == pytest.approx(
        sum(fill_pnl_usd(fill=fill) for fill in result.fills)
    )


def test_h024_trade_ledger_report_contains_audit_sections(tmp_path):
    h024, result, usdjpy_h4, xauusd_h4 = _synthetic_h024_result()
    ledger = build_h024_trade_ledger(
        h017_result=h024,
        fixed_lifecycle_result=result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
    )

    report = format_h024_trade_ledger_audit_report(
        ledger=ledger,
        result=result,
        output_path=tmp_path / "ledger.csv",
        top_n=3,
    )

    assert "H024 hold=3 H4 trade ledger export/audit diagnostic" in report
    assert "Research only. No demo/live/Phase 4 approval." in report
    if not ledger.empty:
        assert "Actual gross leverage audit:" in report
        assert "2023_stop_fills" in report
    if ledger.empty:
        assert "No fills to rank." in report
    else:
        assert "Top 3 losses:" in report
        assert "Top 3 winners:" in report
        assert "2023 audit slice:" in report


def test_h024_trade_ledger_export_writes_csv(tmp_path):
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()
    output_path = tmp_path / "h024_hold3_trade_ledger.csv"

    ledger, result = run_h024_trade_ledger_export(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=_m1_from_h4(usdjpy_h4),
        xauusd_m1=_m1_from_h4(xauusd_h4),
        accepted_entry_times=tuple(usdjpy_h4.index),
        output_path=output_path,
        hold_h4_bars=DEFAULT_H024_LEDGER_HOLD_H4_BARS,
    )

    assert output_path.exists()
    loaded = pd.read_csv(output_path)
    assert len(loaded) == len(ledger) == len(result.fills)
    assert "pnl_usd" in loaded.columns
    assert "interval_start_equity_usd" in loaded.columns
    assert "actual_gross_leverage" in loaded.columns


def test_h024_trade_ledger_rejects_bad_inputs():
    h024, result, usdjpy_h4, xauusd_h4 = _synthetic_h024_result()

    with pytest.raises(ValueError, match="hold_h4_bars must be positive"):
        build_h024_trade_ledger(
            h017_result=h024,
            fixed_lifecycle_result=result,
            usdjpy_h4=usdjpy_h4,
            xauusd_h4=xauusd_h4,
            hold_h4_bars=0,
        )

    with pytest.raises(ValueError, match="reference_equity_usd must be positive"):
        build_h024_trade_ledger(
            h017_result=h024,
            fixed_lifecycle_result=result,
            usdjpy_h4=usdjpy_h4,
            xauusd_h4=xauusd_h4,
            reference_equity_usd=0.0,
        )
