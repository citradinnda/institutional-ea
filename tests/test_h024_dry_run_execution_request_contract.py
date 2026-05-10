import pytest

from quantcore.execution.h024_dry_run_execution_request import (
    H024_DRY_RUN_EXECUTION_REQUEST_SCHEMA_VERSION,
    REQUIRED_H024_DRY_RUN_EXECUTION_REQUEST_FIELDS,
    build_h024_dry_run_execution_request,
)
from quantcore.execution.h024_intended_action_log import (
    H024IntendedActionLogRequest,
    build_h024_intended_action_log_row,
)


def _would_open_row(direction: str = "long") -> dict:
    if direction == "long":
        entry_price = 155.25
        stop_price = 154.25
    else:
        entry_price = 154.25
        stop_price = 155.25

    return build_h024_intended_action_log_row(
        H024IntendedActionLogRequest(
            timestamp="2026-05-08T13:00:00+00:00",
            schema_version="h024_intended_action_log_v1",
            ea_version="0.7",
            symbol="USDJPYm",
            normalized_symbol="USDJPY",
            timeframe="H4",
            decision="WOULD_OPEN",
            direction=direction,
            entry_price=entry_price,
            stop_price=stop_price,
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
    )


def _blocked_row() -> dict:
    return build_h024_intended_action_log_row(
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
            reason="kill_switch_blocked",
        )
    )


def test_dry_run_request_schema_is_frozen_in_reconstruction_order():
    assert REQUIRED_H024_DRY_RUN_EXECUTION_REQUEST_FIELDS == (
        "schema_version",
        "source_schema_version",
        "timestamp",
        "symbol",
        "normalized_symbol",
        "timeframe",
        "request_kind",
        "side",
        "volume_lots",
        "entry_price",
        "stop_loss",
        "risk_usd",
        "source_reason",
    )


def test_would_open_long_row_builds_buy_dry_run_request():
    request = build_h024_dry_run_execution_request(_would_open_row("long"))

    assert request is not None
    assert tuple(request.keys()) == REQUIRED_H024_DRY_RUN_EXECUTION_REQUEST_FIELDS
    assert request["schema_version"] == H024_DRY_RUN_EXECUTION_REQUEST_SCHEMA_VERSION
    assert request["source_schema_version"] == "h024_intended_action_log_v1"
    assert request["timestamp"] == "2026-05-08T13:00:00+00:00"
    assert request["symbol"] == "USDJPYm"
    assert request["normalized_symbol"] == "USDJPY"
    assert request["timeframe"] == "H4"
    assert request["request_kind"] == "DRY_RUN_MARKET_OPEN"
    assert request["side"] == "BUY"
    assert request["volume_lots"] == pytest.approx(0.03)
    assert request["entry_price"] == pytest.approx(155.25)
    assert request["stop_loss"] == pytest.approx(154.25)
    assert request["risk_usd"] == pytest.approx(20.0)
    assert request["source_reason"] == "signal_ready"


def test_would_open_short_row_builds_sell_dry_run_request():
    request = build_h024_dry_run_execution_request(_would_open_row("short"))

    assert request is not None
    assert request["side"] == "SELL"
    assert request["entry_price"] == pytest.approx(154.25)
    assert request["stop_loss"] == pytest.approx(155.25)


def test_blocked_row_builds_no_dry_run_request():
    assert build_h024_dry_run_execution_request(_blocked_row()) is None


def test_missing_intended_action_field_is_rejected():
    row = _would_open_row("long")
    del row["lots"]

    with pytest.raises(ValueError, match="missing intended-action fields"):
        build_h024_dry_run_execution_request(row)


def test_would_open_zero_lots_is_rejected():
    row = _would_open_row("long")
    row["lots"] = 0.0

    with pytest.raises(ValueError, match="positive lots"):
        build_h024_dry_run_execution_request(row)


def test_would_open_invalid_direction_is_rejected():
    row = _would_open_row("long")
    row["direction"] = "sideways"

    with pytest.raises(ValueError, match="unsupported WOULD_OPEN direction"):
        build_h024_dry_run_execution_request(row)
