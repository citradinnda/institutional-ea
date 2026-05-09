import pandas as pd
import pytest

from scripts.diagnose_h024_robustness_real import (
    DEFAULT_H024_ROBUSTNESS_COST_MULTIPLIERS,
    DEFAULT_H024_ROBUSTNESS_HOLD_H4_BARS,
    DEFAULT_H024_ROBUSTNESS_STOP_ATR_MULTIPLES,
    H024RobustnessScenario,
    default_h024_robustness_scenarios,
    format_h024_robustness_summary,
    run_h024_robustness_diagnostic,
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
    return pd.DataFrame(
        [
            {
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
            }
            for _, row in h4.iterrows()
        ],
        index=h4.index,
    )


def test_h024_robustness_defaults_are_narrow_and_hold_3_only():
    assert DEFAULT_H024_ROBUSTNESS_HOLD_H4_BARS == 3
    assert DEFAULT_H024_ROBUSTNESS_STOP_ATR_MULTIPLES == (1.5, 2.0, 2.5)
    assert DEFAULT_H024_ROBUSTNESS_COST_MULTIPLIERS == (1.0, 1.25, 1.5)

    scenarios = default_h024_robustness_scenarios()

    assert len(scenarios) == 9
    assert scenarios[0].label == "stop_atr_1.50_cost_1.00x"
    assert scenarios[-1].label == "stop_atr_2.50_cost_1.50x"


def test_h024_robustness_runs_on_synthetic_data():
    scenarios = (
        H024RobustnessScenario(
            label="baseline",
            stop_atr_multiple=2.0,
            cost_multiplier=1.0,
        ),
    )

    results = run_h024_robustness_diagnostic(
        usdjpy_h4=_usdjpy_h4(),
        xauusd_h4=_xauusd_h4(),
        usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
        xauusd_m1=_m1_from_h4(_xauusd_h4()),
        accepted_entry_times=tuple(_index()),
        scenarios=scenarios,
    )

    assert len(results) == 1
    assert results[0].scenario.label == "baseline"
    assert results[0].run.hold_h4_bars == 3
    assert results[0].run.summary.accepted_entry_count == len(_index())


def test_h024_robustness_summary_is_stable():
    results = run_h024_robustness_diagnostic(
        usdjpy_h4=_usdjpy_h4(),
        xauusd_h4=_xauusd_h4(),
        usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
        xauusd_m1=_m1_from_h4(_xauusd_h4()),
        accepted_entry_times=tuple(_index()),
        scenarios=(
            H024RobustnessScenario(
                label="baseline",
                stop_atr_multiple=2.0,
                cost_multiplier=1.0,
            ),
        ),
    )

    report = format_h024_robustness_summary(results)

    assert "H024 hold=3 targeted robustness diagnostic" in report
    assert "scenario | stop_atr | cost_mult" in report
    assert "baseline | 2.00 | 1.00" in report
    assert "No demo trading is approved. No live trading is approved. Phase 4 is not approved." in report


def test_h024_robustness_rejects_bad_scenarios():
    with pytest.raises(ValueError, match="scenarios must be non-empty"):
        run_h024_robustness_diagnostic(
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
            xauusd_m1=_m1_from_h4(_xauusd_h4()),
            accepted_entry_times=tuple(_index()),
            scenarios=(),
        )

    with pytest.raises(ValueError, match="cost_multiplier must not reduce modeled costs"):
        run_h024_robustness_diagnostic(
            usdjpy_h4=_usdjpy_h4(),
            xauusd_h4=_xauusd_h4(),
            usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
            xauusd_m1=_m1_from_h4(_xauusd_h4()),
            accepted_entry_times=tuple(_index()),
            scenarios=(
                H024RobustnessScenario(
                    label="bad",
                    stop_atr_multiple=2.0,
                    cost_multiplier=0.75,
                ),
            ),
        )
