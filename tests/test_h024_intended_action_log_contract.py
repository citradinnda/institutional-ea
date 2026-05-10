import pytest

from quantcore.execution.h024_intended_action_log import (
    H024IntendedActionLogRequest,
    REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS,
    build_h024_intended_action_log_row,
)


EXPECTED_FIELDS = (
    "timestamp",
    "schema_version",
    "ea_version",
    "symbol",
    "normalized_symbol",
    "timeframe",
    "decision",
    "direction",
    "entry_price",
    "stop_price",
    "stop_distance_price",
    "tick_size",
    "tick_value_usd_per_lot",
    "account_balance_usd",
    "risk_fraction",
    "risk_usd",
    "raw_lots",
    "lots",
    "min_volume",
    "max_volume",
    "volume_step",
    "volume_digits",
    "reason",
)


def test_intended_action_log_schema_is_frozen_in_reconstruction_order():
    assert tuple(REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS) == EXPECTED_FIELDS


def test_would_open_row_contains_reconstructable_sizing_and_execution_intent():
    request = H024IntendedActionLogRequest(
        timestamp="2026-05-08T13:00:00+00:00",
        schema_version="h024_intended_action_log_v1",
        ea_version="0.7",
        symbol="USDJPYm",
        normalized_symbol="USDJPY",
        timeframe="H4",
        decision="WOULD_OPEN",
        direction="long",
        entry_price=155.25,
        stop_price=154.25,
        tick_size=0.001,
        tick_value_usd_per_lot=0.65,
        account_balance_usd=10000.0,
        risk_fraction=0.002,
        min_volume=0.01,
        max_volume=200.0,
        volume_step=0.01,
        volume_digits=2,
        reason="signal_ready",
    )

    row = build_h024_intended_action_log_row(request)

    assert tuple(row.keys()) == EXPECTED_FIELDS
    assert row["timestamp"] == "2026-05-08T13:00:00+00:00"
    assert row["schema_version"] == "h024_intended_action_log_v1"
    assert row["ea_version"] == "0.7"
    assert row["symbol"] == "USDJPYm"
    assert row["normalized_symbol"] == "USDJPY"
    assert row["timeframe"] == "H4"
    assert row["decision"] == "WOULD_OPEN"
    assert row["direction"] == "long"

    assert row["entry_price"] == pytest.approx(155.25)
    assert row["stop_price"] == pytest.approx(154.25)
    assert row["stop_distance_price"] == pytest.approx(1.0)
    assert row["tick_size"] == pytest.approx(0.001)
    assert row["tick_value_usd_per_lot"] == pytest.approx(0.65)
    assert row["account_balance_usd"] == pytest.approx(10000.0)
    assert row["risk_fraction"] == pytest.approx(0.002)
    assert row["risk_usd"] == pytest.approx(20.0)

    assert row["raw_lots"] == pytest.approx(0.03076923076923077)
    assert row["lots"] == pytest.approx(0.03)

    assert row["min_volume"] == pytest.approx(0.01)
    assert row["max_volume"] == pytest.approx(200.0)
    assert row["volume_step"] == pytest.approx(0.01)
    assert row["volume_digits"] == 2
    assert row["reason"] == "signal_ready"


def test_blocked_row_is_reconstructable_but_carries_zero_lots():
    request = H024IntendedActionLogRequest(
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

    row = build_h024_intended_action_log_row(request)

    assert tuple(row.keys()) == EXPECTED_FIELDS
    assert row["decision"] == "BLOCKED"
    assert row["direction"] == ""
    assert row["stop_distance_price"] == pytest.approx(0.0)
    assert row["risk_usd"] == pytest.approx(20.0)
    assert row["raw_lots"] == pytest.approx(0.0)
    assert row["lots"] == pytest.approx(0.0)
    assert row["reason"] == "conflict_signal"