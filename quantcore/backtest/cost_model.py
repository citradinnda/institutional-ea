from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, Mapping

Side = Literal["buy", "sell"]
FillAction = Literal["entry", "exit"]
ExitReason = Literal["stop", "tp", "signal_flip", "end_of_data"]


@dataclass(frozen=True)
class SymbolCostSpec:
    """Broker execution assumptions for one symbol.

    Costs are isolated from the strategy because a valid trading signal can
    still be untradable after spread, slippage, and commission. Keeping this
    model explicit prevents Phase 3 from silently mixing alpha logic with broker
    microstructure assumptions.

    ``spread_price`` is the full bid/ask spread in price units. For example,
    USDJPY with a 1 pip spread uses ``0.01`` because one JPY pip is 0.01. XAUUSD
    with a 30 cent spread uses ``0.30``.

    ``commission_usd_per_lot_per_fill`` is deliberately per fill, not round
    turn. A round-turn trade has at least two fills: entry and exit.
    """

    symbol: str
    spread_price: float
    commission_usd_per_lot_per_fill: float
    stop_slippage_atr_fraction: float = 0.05


@dataclass(frozen=True)
class ExecutionCost:
    """The cost-adjusted result of one entry or exit fill.

    ``fill_price`` is the price that should be passed into the fill/accounting
    layer. ``spread_paid_price`` and ``slippage_price`` are kept separately so
    tests and future audit logs can explain exactly why a fill moved away from
    the raw strategy price.
    """

    symbol: str
    side: Side
    action: FillAction
    raw_price: float
    fill_price: float
    lots: float
    spread_paid_price: float
    slippage_price: float
    commission_usd: float


DEFAULT_COST_SPECS: Mapping[str, SymbolCostSpec] = MappingProxyType(
    {
        "USDJPY": SymbolCostSpec(
            symbol="USDJPY",
            spread_price=0.01,
            commission_usd_per_lot_per_fill=7.0,
            stop_slippage_atr_fraction=0.05,
        ),
        "XAUUSD": SymbolCostSpec(
            symbol="XAUUSD",
            spread_price=0.30,
            commission_usd_per_lot_per_fill=10.0,
            stop_slippage_atr_fraction=0.05,
        ),
    }
)


def get_default_cost_spec(symbol: str) -> SymbolCostSpec:
    """Return the default cost spec for a supported symbol.

    The function rejects unknown symbols loudly because applying USDJPY costs to
    another JPY pair, or XAUUSD costs to another metal/CFD, would create a
    realistic-looking but false backtest.
    """

    normalized = symbol.upper()
    try:
        return DEFAULT_COST_SPECS[normalized]
    except KeyError as exc:
        supported = ", ".join(sorted(DEFAULT_COST_SPECS))
        raise ValueError(f"unsupported symbol {symbol!r}; supported: {supported}") from exc


def price_with_execution_costs(
    *,
    symbol: str,
    side: Side,
    action: FillAction,
    raw_price: float,
    lots: float,
    cost_spec: SymbolCostSpec | None = None,
    exit_reason: ExitReason | None = None,
    atr: float | None = None,
) -> ExecutionCost:
    """Apply spread, stop slippage, and commission to one fill.

    For entries:
    - a long/buy position pays the ask, modelled as ``raw + half_spread``;
    - a short/sell position sells the bid, modelled as ``raw - half_spread``.

    For exits:
    - exiting a long/buy position sells the bid, modelled as ``raw - half_spread``;
    - exiting a short/sell position buys the ask, modelled as ``raw + half_spread``.

    Stop slippage only applies to stop exits. Take-profit, signal-flip, and
    end-of-data exits pay spread and commission but do not receive ATR slippage.
    """

    _validate_side(side)
    _validate_action(action)
    _validate_positive("raw_price", raw_price)
    _validate_positive("lots", lots)

    spec = cost_spec if cost_spec is not None else get_default_cost_spec(symbol)
    _validate_cost_spec(spec)

    if spec.symbol.upper() != symbol.upper():
        raise ValueError("cost_spec symbol must match symbol")

    half_spread = spec.spread_price / 2.0
    spread_adjustment = _spread_adjustment(
        side=side,
        action=action,
        half_spread=half_spread,
    )

    slippage = _stop_slippage(
        action=action,
        exit_reason=exit_reason,
        atr=atr,
        stop_slippage_atr_fraction=spec.stop_slippage_atr_fraction,
    )
    slippage_adjustment = _slippage_adjustment(side=side, slippage=slippage)

    fill_price = float(raw_price + spread_adjustment + slippage_adjustment)
    commission_usd = float(lots * spec.commission_usd_per_lot_per_fill)

    return ExecutionCost(
        symbol=spec.symbol,
        side=side,
        action=action,
        raw_price=float(raw_price),
        fill_price=fill_price,
        lots=float(lots),
        spread_paid_price=half_spread,
        slippage_price=slippage,
        commission_usd=commission_usd,
    )


def _validate_side(side: Side) -> None:
    if side not in ("buy", "sell"):
        raise ValueError("side must be 'buy' or 'sell'")


def _validate_action(action: FillAction) -> None:
    if action not in ("entry", "exit"):
        raise ValueError("action must be 'entry' or 'exit'")


def _validate_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0.0")


def _validate_cost_spec(spec: SymbolCostSpec) -> None:
    if spec.spread_price < 0.0:
        raise ValueError("spread_price must be >= 0.0")
    if spec.commission_usd_per_lot_per_fill < 0.0:
        raise ValueError("commission_usd_per_lot_per_fill must be >= 0.0")
    if spec.stop_slippage_atr_fraction < 0.0:
        raise ValueError("stop_slippage_atr_fraction must be >= 0.0")


def _spread_adjustment(
    *,
    side: Side,
    action: FillAction,
    half_spread: float,
) -> float:
    if action == "entry":
        return half_spread if side == "buy" else -half_spread

    return -half_spread if side == "buy" else half_spread


def _stop_slippage(
    *,
    action: FillAction,
    exit_reason: ExitReason | None,
    atr: float | None,
    stop_slippage_atr_fraction: float,
) -> float:
    if action != "exit" or exit_reason != "stop":
        return 0.0

    if atr is None:
        raise ValueError("atr is required for stop-exit slippage")

    _validate_positive("atr", atr)
    return float(atr * stop_slippage_atr_fraction)


def _slippage_adjustment(*, side: Side, slippage: float) -> float:
    if slippage == 0.0:
        return 0.0

    return -slippage if side == "buy" else slippage
