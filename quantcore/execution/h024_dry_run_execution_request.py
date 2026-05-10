from __future__ import annotations

from typing import Any

from quantcore.execution.h024_intended_action_log import (
    REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS,
)


H024_DRY_RUN_EXECUTION_REQUEST_SCHEMA_VERSION = "h024_dry_run_execution_request_v1"

REQUIRED_H024_DRY_RUN_EXECUTION_REQUEST_FIELDS = (
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


def build_h024_dry_run_execution_request(
    intended_action_row: dict[str, Any],
) -> dict[str, Any] | None:
    missing_fields = [
        field
        for field in REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS
        if field not in intended_action_row
    ]
    if missing_fields:
        raise ValueError(f"missing intended-action fields: {missing_fields}")

    if intended_action_row["decision"] != "WOULD_OPEN":
        return None

    direction = intended_action_row["direction"]
    if direction == "long":
        side = "BUY"
    elif direction == "short":
        side = "SELL"
    else:
        raise ValueError(f"unsupported WOULD_OPEN direction: {direction!r}")

    volume_lots = float(intended_action_row["lots"])
    entry_price = float(intended_action_row["entry_price"])
    stop_loss = float(intended_action_row["stop_price"])
    risk_usd = float(intended_action_row["risk_usd"])

    if volume_lots <= 0.0:
        raise ValueError("WOULD_OPEN row must have positive lots")
    if entry_price <= 0.0:
        raise ValueError("WOULD_OPEN row must have positive entry_price")
    if stop_loss <= 0.0:
        raise ValueError("WOULD_OPEN row must have positive stop_price")
    if entry_price == stop_loss:
        raise ValueError("WOULD_OPEN row entry_price and stop_price must differ")
    if risk_usd <= 0.0:
        raise ValueError("WOULD_OPEN row must have positive risk_usd")

    return {
        "schema_version": H024_DRY_RUN_EXECUTION_REQUEST_SCHEMA_VERSION,
        "source_schema_version": intended_action_row["schema_version"],
        "timestamp": intended_action_row["timestamp"],
        "symbol": intended_action_row["symbol"],
        "normalized_symbol": intended_action_row["normalized_symbol"],
        "timeframe": intended_action_row["timeframe"],
        "request_kind": "DRY_RUN_MARKET_OPEN",
        "side": side,
        "volume_lots": volume_lots,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "risk_usd": risk_usd,
        "source_reason": intended_action_row["reason"],
    }
