import pandas as pd
import pytest

from quantcore.strategy.h017 import H017Result
from scripts.diagnose_h022_risk_lifecycle_variants_real import (
    DEFAULT_H022_VARIANTS,
    H022RiskLifecycleVariant,
    apply_h022_risk_lifecycle_transform,
    format_h022_summary_table,
    summarize_h022_result,
    backtest_h022_risk_lifecycle_variant,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _h4() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-01 00:00"),
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 12:00"),
            _utc("2024-01-01 16:00"),
        ]
    )
    return pd.DataFrame(
        {
            "open": [100.0, 102.0, 104.0, 106.0, 108.0],
            "high": [101.0, 103.0, 105.0, 107.0, 109.0],
            "low": [99.0, 101.0, 103.0, 105.0, 107.0],
            "close": [100.5, 102.5, 104.5, 106.5, 108.5],
        },
        index=index,
    )


def _m1_no_stop() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 05:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 09:00"),
            _utc("2024-01-01 12:00"),
            _utc("2024-01-01 13:00"),
        ]
    )
    return pd.DataFrame(
        {
            "open": [102.0, 102.2, 104.0, 104.2, 106.0, 106.2],
            "high": [103.0, 103.2, 105.0, 105.2, 107.0, 107.2],
            "low": [101.0, 101.2, 103.0, 103.2, 105.0, 105.2],
            "close": [102.5, 102.7, 104.5, 104.7, 106.5, 106.7],
        },
        index=index,
    )


def _h017_result() -> H017Result:
    index = _h4().index
    columns = ["USDJPY", "XAUUSD"]

    positions = pd.DataFrame(0.0, index=index, columns=columns)
    positions.at[_utc("2024-01-01 00:00"), "XAUUSD"] = 0.04
    positions.at[_utc("2024-01-01 04:00"), "XAUUSD"] = 0.04
    positions.at[_utc("2024-01-01 08:00"), "XAUUSD"] = 0.04

    stops_long = pd.DataFrame(90.0, index=index, columns=columns)
    stops_short = pd.DataFrame(120.0, index=index, columns=columns)
    zeros = pd.DataFrame(0.0, index=index, columns=columns)

    return H017Result(
        positions=positions,
        stops_long=stops_long,
        stops_short=stops_short,
        signals=zeros,
        vol_multipliers=zeros,
        heat_multipliers=zeros,
        heat_pre=zeros,
        heat_post=zeros,
        heat_binding=zeros,
    )


def test_default_h022_variants_are_pre_registered_and_structural():
    labels = [variant.label for variant in DEFAULT_H022_VARIANTS]

    assert "scale_0_50_hold_1" in labels
    assert "scale_0_25_min_stop_50x_hold_2" in labels
    assert all(variant.position_scale <= 1.0 for variant in DEFAULT_H022_VARIANTS)
    assert all(variant.hold_h4_bars in {1, 2} for variant in DEFAULT_H022_VARIANTS)


def test_transform_scales_positions_without_changing_stops():
    source = _h017_result()
    variant = H022RiskLifecycleVariant(
        label="unit",
        hold_h4_bars=1,
        position_scale=0.50,
        min_stop_distance_spread_ratio=None,
    )

    transformed = apply_h022_risk_lifecycle_transform(
        h017_result=source,
        usdjpy_h4=_h4(),
        xauusd_h4=_h4(),
        variant=variant,
    )

    assert transformed.positions.at[_utc("2024-01-01 00:00"), "XAUUSD"] == pytest.approx(0.02)
    assert transformed.positions.at[_utc("2024-01-01 04:00"), "XAUUSD"] == pytest.approx(0.02)
    assert transformed.stops_long.equals(source.stops_long)
    assert transformed.stops_short.equals(source.stops_short)


def test_transform_skips_tight_stop_distance_spread_geometry():
    source = _h017_result()
    source.stops_long.at[_utc("2024-01-01 00:00"), "XAUUSD"] = 101.80

    variant = H022RiskLifecycleVariant(
        label="unit",
        hold_h4_bars=1,
        position_scale=0.50,
        min_stop_distance_spread_ratio=2.0,
    )

    transformed = apply_h022_risk_lifecycle_transform(
        h017_result=source,
        usdjpy_h4=_h4(),
        xauusd_h4=_h4(),
        variant=variant,
    )

    assert transformed.positions.at[_utc("2024-01-01 00:00"), "XAUUSD"] == 0.0
    assert transformed.positions.at[_utc("2024-01-01 04:00"), "XAUUSD"] == pytest.approx(0.02)


def test_transform_rejects_invalid_variant_values():
    with pytest.raises(ValueError, match="hold_h4_bars must be positive"):
        apply_h022_risk_lifecycle_transform(
            h017_result=_h017_result(),
            usdjpy_h4=_h4(),
            xauusd_h4=_h4(),
            variant=H022RiskLifecycleVariant(
                label="bad",
                hold_h4_bars=0,
                position_scale=0.50,
                min_stop_distance_spread_ratio=None,
            ),
        )

    with pytest.raises(ValueError, match="position_scale"):
        apply_h022_risk_lifecycle_transform(
            h017_result=_h017_result(),
            usdjpy_h4=_h4(),
            xauusd_h4=_h4(),
            variant=H022RiskLifecycleVariant(
                label="bad",
                hold_h4_bars=1,
                position_scale=1.25,
                min_stop_distance_spread_ratio=None,
            ),
        )


def test_h022_backtest_and_summary_format_on_synthetic_data():
    result = backtest_h022_risk_lifecycle_variant(
        h017_result=_h017_result(),
        usdjpy_h4=_h4(),
        xauusd_h4=_h4(),
        usdjpy_m1=_m1_no_stop(),
        xauusd_m1=_m1_no_stop(),
        accepted_entry_times=(
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
        ),
        variant=H022RiskLifecycleVariant(
            label="unit",
            hold_h4_bars=1,
            position_scale=0.50,
            min_stop_distance_spread_ratio=None,
        ),
        starting_equity_usd=10_000.0,
    )

    summary = summarize_h022_result(result)
    formatted = format_h022_summary_table((summary,))

    assert summary.label == "unit"
    assert summary.fill_count >= 1
    assert "H022 risk/lifecycle variant summary" in formatted
    assert "unit" in formatted
