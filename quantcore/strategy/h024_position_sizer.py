from __future__ import annotations

from dataclasses import dataclass
from math import floor, isfinite


@dataclass(frozen=True)
class H024PositionSizeRequest:
    account_balance_usd: float
    risk_fraction: float
    entry_price: float
    stop_price: float
    tick_size: float
    tick_value_usd_per_lot: float
    volume_step: float
    min_volume: float
    max_volume: float
    volume_digits: int = 2


@dataclass(frozen=True)
class H024PositionSizeResult:
    risk_usd: float
    stop_distance_price: float
    stop_distance_ticks: float
    loss_usd_per_lot: float
    raw_lots: float
    lots: float


class H024PositionSizer:
    """Pure-math H024/H020-style fixed-risk position sizing reference."""

    def __init__(self, request: H024PositionSizeRequest):
        self.request = request

    def compute(self) -> H024PositionSizeResult:
        request = self.request
        self._validate_request(request)

        risk_usd = request.account_balance_usd * request.risk_fraction
        stop_distance_price = abs(request.entry_price - request.stop_price)
        if stop_distance_price <= 0:
            raise ValueError("stop distance must be positive")

        stop_distance_ticks = stop_distance_price / request.tick_size
        loss_usd_per_lot = stop_distance_ticks * request.tick_value_usd_per_lot
        if loss_usd_per_lot <= 0:
            raise ValueError("loss per lot must be positive")

        raw_lots = risk_usd / loss_usd_per_lot
        capped_lots = min(raw_lots, request.max_volume)
        stepped_lots = self._floor_to_step(capped_lots, request.volume_step)

        if stepped_lots < request.min_volume:
            final_lots = 0.0
        else:
            final_lots = round(stepped_lots, request.volume_digits)

        return H024PositionSizeResult(
            risk_usd=risk_usd,
            stop_distance_price=stop_distance_price,
            stop_distance_ticks=stop_distance_ticks,
            loss_usd_per_lot=loss_usd_per_lot,
            raw_lots=raw_lots,
            lots=final_lots,
        )

    def compute_lot_size(self) -> float:
        return self.compute().lots

    @staticmethod
    def _floor_to_step(value: float, step: float) -> float:
        return floor((value + 1e-12) / step) * step

    @staticmethod
    def _validate_request(request: H024PositionSizeRequest) -> None:
        numeric_values = {
            "account_balance_usd": request.account_balance_usd,
            "risk_fraction": request.risk_fraction,
            "entry_price": request.entry_price,
            "stop_price": request.stop_price,
            "tick_size": request.tick_size,
            "tick_value_usd_per_lot": request.tick_value_usd_per_lot,
            "volume_step": request.volume_step,
            "min_volume": request.min_volume,
            "max_volume": request.max_volume,
        }

        for name, value in numeric_values.items():
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")

        if request.account_balance_usd <= 0:
            raise ValueError("account_balance_usd must be positive")
        if request.risk_fraction <= 0 or request.risk_fraction > 1:
            raise ValueError("risk_fraction must be in (0, 1]")
        if request.entry_price <= 0 or request.stop_price <= 0:
            raise ValueError("entry_price and stop_price must be positive")
        if request.tick_size <= 0:
            raise ValueError("tick_size must be positive")
        if request.tick_value_usd_per_lot <= 0:
            raise ValueError("tick_value_usd_per_lot must be positive")
        if request.volume_step <= 0:
            raise ValueError("volume_step must be positive")
        if request.min_volume < 0:
            raise ValueError("min_volume must be non-negative")
        if request.max_volume <= 0:
            raise ValueError("max_volume must be positive")
        if request.max_volume < request.min_volume:
            raise ValueError("max_volume must be greater than or equal to min_volume")
        if request.volume_digits < 0:
            raise ValueError("volume_digits must be non-negative")