from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS = (
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


@dataclass(frozen=True)
class H024IntendedActionLogRequest:
    timestamp: str
    schema_version: str
    ea_version: str
    symbol: str
    normalized_symbol: str
    timeframe: str
    decision: str
    direction: str
    entry_price: float
    stop_price: float
    tick_size: float
    tick_value_usd_per_lot: float
    account_balance_usd: float
    risk_fraction: float
    min_volume: float
    max_volume: float
    volume_step: float
    volume_digits: int
    reason: str


def _compute_raw_and_final_lots(request: H024IntendedActionLogRequest) -> tuple[float, float]:
    if request.decision != "WOULD_OPEN":
        return 0.0, 0.0

    stop_distance_price = abs(request.entry_price - request.stop_price)
    risk_usd = request.account_balance_usd * request.risk_fraction

    if (
        request.entry_price <= 0.0
        or request.stop_price <= 0.0
        or stop_distance_price <= 0.0
        or request.tick_size <= 0.0
        or request.tick_value_usd_per_lot <= 0.0
        or request.account_balance_usd <= 0.0
        or request.risk_fraction <= 0.0
        or request.min_volume <= 0.0
        or request.max_volume <= 0.0
        or request.volume_step <= 0.0
        or request.volume_digits < 0
    ):
        return 0.0, 0.0

    stop_distance_ticks = stop_distance_price / request.tick_size
    loss_usd_per_lot = stop_distance_ticks * request.tick_value_usd_per_lot

    if loss_usd_per_lot <= 0.0:
        return 0.0, 0.0

    raw_lots = risk_usd / loss_usd_per_lot
    capped_lots = min(raw_lots, request.max_volume)
    stepped_lots = math.floor(capped_lots / request.volume_step) * request.volume_step

    if stepped_lots < request.min_volume:
        return raw_lots, 0.0

    return raw_lots, round(stepped_lots, request.volume_digits)


def build_h024_intended_action_log_row(
    request: H024IntendedActionLogRequest,
) -> dict[str, Any]:
    stop_distance_price = (
        abs(request.entry_price - request.stop_price)
        if request.decision == "WOULD_OPEN"
        else 0.0
    )
    risk_usd = request.account_balance_usd * request.risk_fraction
    raw_lots, lots = _compute_raw_and_final_lots(request)

    return {
        "timestamp": request.timestamp,
        "schema_version": request.schema_version,
        "ea_version": request.ea_version,
        "symbol": request.symbol,
        "normalized_symbol": request.normalized_symbol,
        "timeframe": request.timeframe,
        "decision": request.decision,
        "direction": request.direction,
        "entry_price": request.entry_price,
        "stop_price": request.stop_price,
        "stop_distance_price": stop_distance_price,
        "tick_size": request.tick_size,
        "tick_value_usd_per_lot": request.tick_value_usd_per_lot,
        "account_balance_usd": request.account_balance_usd,
        "risk_fraction": request.risk_fraction,
        "risk_usd": risk_usd,
        "raw_lots": raw_lots,
        "lots": lots,
        "min_volume": request.min_volume,
        "max_volume": request.max_volume,
        "volume_step": request.volume_step,
        "volume_digits": request.volume_digits,
        "reason": request.reason,
    }