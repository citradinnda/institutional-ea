from __future__ import annotations

from dataclasses import dataclass

from quantcore.backtest.cost_model import SymbolCostSpec, get_default_cost_spec
from quantcore.backtest.portfolio import (
    InstrumentSpec,
    get_default_instrument_spec,
    quote_pnl_to_usd,
)


@dataclass(frozen=True)
class ProjectedRoundTripFriction:
    """Diagnostic-only projected round-trip trading-cost burden.

    This object is intentionally not a guard. It records a conservative
    pre-trade estimate of spread, commission, and stop-slippage burden so later
    diagnostics can study whether a threshold is justified.
    """

    symbol: str
    lots: float
    entry_price: float
    atr: float
    spread_price: float
    stop_slippage_price: float
    spread_burden_usd: float
    commission_burden_usd: float
    stop_slippage_burden_usd: float
    total_burden_usd: float

    def fraction_of_equity(self, equity_usd: float) -> float:
        if equity_usd <= 0.0:
            raise ValueError("equity_usd must be > 0.0")

        return self.total_burden_usd / float(equity_usd)


def project_worst_case_round_trip_friction(
    *,
    symbol: str,
    lots: float,
    entry_price: float,
    atr: float,
    cost_spec: SymbolCostSpec | None = None,
    instrument_spec: InstrumentSpec | None = None,
) -> ProjectedRoundTripFriction:
    """Project conservative round-trip friction in USD.

    The estimate includes:

    - one full modeled spread for the round trip;
    - two commissions, entry and exit;
    - modeled stop slippage as ``atr * stop_slippage_atr_fraction``.

    This is a diagnostic primitive only. It does not choose a threshold and does
    not approve, reject, skip, or resize trades.
    """

    _validate_positive("lots", lots)
    _validate_positive("entry_price", entry_price)
    _validate_positive("atr", atr)

    normalized_symbol = symbol.upper()
    effective_cost_spec = cost_spec if cost_spec is not None else get_default_cost_spec(symbol)
    effective_instrument_spec = (
        instrument_spec
        if instrument_spec is not None
        else get_default_instrument_spec(symbol)
    )

    if effective_cost_spec.symbol.upper() != normalized_symbol:
        raise ValueError("cost_spec symbol must match symbol")

    if effective_instrument_spec.symbol.upper() != normalized_symbol:
        raise ValueError("instrument_spec symbol must match symbol")

    spread_burden_usd = _price_move_burden_usd(
        symbol=normalized_symbol,
        price_move=effective_cost_spec.spread_price,
        lots=lots,
        entry_price=entry_price,
        instrument_spec=effective_instrument_spec,
    )

    stop_slippage_price = float(atr) * effective_cost_spec.stop_slippage_atr_fraction
    stop_slippage_burden_usd = _price_move_burden_usd(
        symbol=normalized_symbol,
        price_move=stop_slippage_price,
        lots=lots,
        entry_price=entry_price,
        instrument_spec=effective_instrument_spec,
    )

    commission_burden_usd = float(
        2.0 * lots * effective_cost_spec.commission_usd_per_lot_per_fill
    )

    total_burden_usd = (
        spread_burden_usd + commission_burden_usd + stop_slippage_burden_usd
    )

    return ProjectedRoundTripFriction(
        symbol=effective_instrument_spec.symbol,
        lots=float(lots),
        entry_price=float(entry_price),
        atr=float(atr),
        spread_price=float(effective_cost_spec.spread_price),
        stop_slippage_price=stop_slippage_price,
        spread_burden_usd=spread_burden_usd,
        commission_burden_usd=commission_burden_usd,
        stop_slippage_burden_usd=stop_slippage_burden_usd,
        total_burden_usd=total_burden_usd,
    )


def _price_move_burden_usd(
    *,
    symbol: str,
    price_move: float,
    lots: float,
    entry_price: float,
    instrument_spec: InstrumentSpec,
) -> float:
    if price_move < 0.0:
        raise ValueError("price_move must be >= 0.0")

    burden_quote = float(price_move) * float(lots) * instrument_spec.contract_size

    return quote_pnl_to_usd(
        symbol=symbol,
        pnl_quote=burden_quote,
        conversion_price=entry_price,
        instrument_spec=instrument_spec,
    )


def _validate_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0.0")