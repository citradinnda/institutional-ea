import pytest

from quantcore.execution.h024_intended_action_log import (
    H024IntendedActionLogRequest,
    build_h024_intended_action_log_row,
)


def test_blocked_signal_row_preserves_raw_sizing_diagnostics_but_zero_final_lots():
    row = build_h024_intended_action_log_row(
        H024IntendedActionLogRequest(
            timestamp="2026-05-10T08:23:22+00:00",
            schema_version="h024_intended_action_log_v1",
            ea_version="0.6",
            symbol="USDJPYm",
            normalized_symbol="USDJPY",
            timeframe="H4",
            decision="BLOCKED",
            direction="short",
            entry_price=155.821,
            stop_price=158.163,
            tick_size=0.001,
            tick_value_usd_per_lot=0.6381865292,
            account_balance_usd=1246.45,
            risk_fraction=0.01,
            min_volume=0.01,
            max_volume=300.0,
            volume_step=0.01,
            volume_digits=2,
            reason="BLOCKED:volume_below_min_for_would_open",
        )
    )

    assert row["decision"] == "BLOCKED"
    assert row["direction"] == "short"
    assert row["entry_price"] == pytest.approx(155.821)
    assert row["stop_price"] == pytest.approx(158.163)
    assert row["stop_distance_price"] == pytest.approx(2.342)
    assert row["risk_usd"] == pytest.approx(12.4645)
    assert row["raw_lots"] == pytest.approx(0.0083397, rel=1e-4)
    assert row["lots"] == pytest.approx(0.0)


def test_blocked_no_price_row_still_carries_zero_sizing_fields():
    row = build_h024_intended_action_log_row(
        H024IntendedActionLogRequest(
            timestamp="2026-05-08T13:00:00+00:00",
            schema_version="h024_intended_action_log_v1",
            ea_version="0.7",
            symbol="XAUUSDm",
            normalized_symbol="XAUUSD",
            timeframe="H4",
            decision="BLOCKED",
            direction="",
            entry_price=0.0,
            stop_price=0.0,
            tick_size=0.01,
            tick_value_usd_per_lot=1.0,
            account_balance_usd=10000.0,
            risk_fraction=0.002,
            min_volume=0.01,
            max_volume=200.0,
            volume_step=0.01,
            volume_digits=2,
            reason="conflict_signal",
        )
    )

    assert row["stop_distance_price"] == pytest.approx(0.0)
    assert row["raw_lots"] == pytest.approx(0.0)
    assert row["lots"] == pytest.approx(0.0)
