import pandas as pd

from quantcore.backtest.cost_model import DEFAULT_COST_SPECS
from quantcore.strategy.h020 import H020SizingConfig
from quantcore.strategy.h024 import H024SignalConfig
from quantcore.strategy.h024_runner import H024BridgeConfig
from scripts.diagnose_h024_fixed_lifecycle_real import run_h024_fixed_lifecycle_diagnostic
from scripts.diagnose_h024_observed_broker_costs_real import (
    FROZEN_H024_HOLD_H4_BARS,
    OBSERVED_BROKER_COST_SPECS,
    format_h024_observed_broker_cost_report,
    run_h024_observed_broker_cost_diagnostic,
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


def _inputs():
    usdjpy_h4 = _usdjpy_h4()
    xauusd_h4 = _xauusd_h4()
    return {
        "usdjpy_h4": usdjpy_h4,
        "xauusd_h4": xauusd_h4,
        "usdjpy_m1": _m1_from_h4(usdjpy_h4),
        "xauusd_m1": _m1_from_h4(xauusd_h4),
        "accepted_entry_times": tuple(usdjpy_h4.index),
        "bridge_config": _bridge_config(),
    }


def test_default_cost_override_matches_implicit_default_path():
    inputs = _inputs()

    implicit = run_h024_fixed_lifecycle_diagnostic(
        **inputs,
        hold_h4_bars_values=(1,),
    )[0]
    explicit = run_h024_fixed_lifecycle_diagnostic(
        **inputs,
        hold_h4_bars_values=(1,),
        cost_specs_by_symbol=DEFAULT_COST_SPECS,
    )[0]

    assert explicit.summary == implicit.summary
    assert explicit.result.fills == implicit.result.fills


def test_observed_broker_cost_specs_change_commission_and_spread_path():
    inputs = _inputs()

    baseline = run_h024_fixed_lifecycle_diagnostic(
        **inputs,
        hold_h4_bars_values=(1,),
        cost_specs_by_symbol=DEFAULT_COST_SPECS,
    )[0]
    observed = run_h024_fixed_lifecycle_diagnostic(
        **inputs,
        hold_h4_bars_values=(1,),
        cost_specs_by_symbol=OBSERVED_BROKER_COST_SPECS,
    )[0]

    assert baseline.result.fills
    assert observed.result.fills
    assert sum(fill.commission for fill in baseline.result.fills) > 0.0
    assert sum(fill.commission for fill in observed.result.fills) == 0.0
    assert any(
        baseline_fill.entry_price != observed_fill.entry_price
        for baseline_fill, observed_fill in zip(baseline.result.fills, observed.result.fills)
    )


def test_h024_observed_broker_cost_diagnostic_runs_on_synthetic_data():
    diagnostic = run_h024_observed_broker_cost_diagnostic(**_inputs())

    assert diagnostic.baseline.hold_h4_bars == FROZEN_H024_HOLD_H4_BARS
    assert diagnostic.observed_broker_costs.hold_h4_bars == FROZEN_H024_HOLD_H4_BARS
    assert diagnostic.baseline.summary.accepted_entry_count == 12
    assert diagnostic.observed_broker_costs.summary.accepted_entry_count == 12


def test_h024_observed_broker_cost_report_contains_boundaries():
    diagnostic = run_h024_observed_broker_cost_diagnostic(**_inputs())

    report = format_h024_observed_broker_cost_report(diagnostic)

    assert "H024 observed broker cost diagnostic" in report
    assert "Research only. No demo/live/Phase 4 approval." in report
    assert "no parameter optimization" in report
    assert "no 2023 exclusion" in report
    assert "no time/session filters" in report
    assert "Passing this diagnostic still does not approve demo trading, live trading, or Phase 4." in report
