from __future__ import annotations

import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, Mapping, Sequence

import pandas as pd

from quantcore.backtest.fill_engine import Fill

SideOrFlat = Literal["buy", "sell"] | None


@dataclass(frozen=True)
class InstrumentSpec:
    """Broker/accounting facts needed to convert fills into USD equity.

    Strategy code should not hard-code contract sizes or quote-currency rules.
    Those are broker/accounting assumptions, not alpha assumptions. Keeping them
    here lets Phase 3 measure whether H017 survives realistic execution without
    contaminating the strategy layer.

    ``contract_size`` means quote-currency units per 1.0 price move for one
    standard lot. For XAUUSD, one lot is commonly 100 ounces, so a 1.0 USD move
    is 100 USD per lot. For USDJPY, one standard FX lot is 100,000 USD, so a
    1.0 JPY move is 100,000 JPY per lot.
    """

    symbol: str
    contract_size: float
    quote_currency: str
    lot_step: float = 0.01
    min_lot: float = 0.01


@dataclass(frozen=True)
class PositionSize:
    """Result of converting a signed risk fraction into broker lots.

    H017 outputs a signed fraction of equity at risk, not lots. This dataclass
    preserves the translation so later audit logs can show both the strategy's
    intent and the executable broker size after lot-step rounding.
    """

    symbol: str
    side: SideOrFlat
    signed_risk_fraction: float
    lots: float
    target_risk_usd: float
    actual_risk_usd: float
    notional_quote: float


@dataclass(frozen=True)
class PortfolioResult:
    """USD equity accounting result from a sequence of completed fills.

    The fill engine produces trade-level execution facts. Portfolio accounting
    turns those fills into account-level equity, returns, and drawdowns. Keeping
    this result separate makes it possible to feed the final returns series into
    the existing validator without changing the validator framework.
    """

    fills: tuple[Fill, ...]
    starting_equity_usd: float
    ending_equity_usd: float
    equity_curve: pd.Series
    returns: pd.Series
    drawdowns: pd.Series
    max_drawdown: float


DEFAULT_INSTRUMENT_SPECS: Mapping[str, InstrumentSpec] = MappingProxyType(
    {
        "USDJPY": InstrumentSpec(
            symbol="USDJPY",
            contract_size=100_000.0,
            quote_currency="JPY",
            lot_step=0.01,
            min_lot=0.01,
        ),
        "XAUUSD": InstrumentSpec(
            symbol="XAUUSD",
            contract_size=100.0,
            quote_currency="USD",
            lot_step=0.01,
            min_lot=0.01,
        ),
    }
)


def get_default_instrument_spec(symbol: str) -> InstrumentSpec:
    """Return broker/accounting assumptions for a supported symbol.

    Unknown symbols are rejected loudly because using USDJPY or XAUUSD contract
    assumptions on another Exness instrument would produce a polished but false
    equity curve.
    """

    normalized = symbol.upper()
    try:
        return DEFAULT_INSTRUMENT_SPECS[normalized]
    except KeyError as exc:
        supported = ", ".join(sorted(DEFAULT_INSTRUMENT_SPECS))
        raise ValueError(f"unsupported symbol {symbol!r}; supported: {supported}") from exc


def size_position_from_risk(
    *,
    symbol: str,
    signed_risk_fraction: float,
    equity_usd: float,
    entry_price: float,
    stop_distance_price: float,
    instrument_spec: InstrumentSpec | None = None,
) -> PositionSize:
    """Convert H017's signed risk fraction into rounded broker lots.

    The strategy says, for example, "risk +1% of equity long." The broker needs
    a lot size. This function uses the stop distance to estimate dollars at risk
    per lot, then rounds down to the broker lot step. Rounding down is deliberate:
    a backtest should not quietly risk more than the strategy requested.

    ``signed_risk_fraction`` may be positive for long, negative for short, or
    zero for flat.
    """

    _validate_positive("equity_usd", equity_usd)
    _validate_positive("entry_price", entry_price)
    _validate_positive("stop_distance_price", stop_distance_price)

    spec = instrument_spec if instrument_spec is not None else get_default_instrument_spec(symbol)
    _validate_instrument_spec(spec)

    if spec.symbol.upper() != symbol.upper():
        raise ValueError("instrument_spec symbol must match symbol")

    if signed_risk_fraction == 0.0:
        return PositionSize(
            symbol=spec.symbol,
            side=None,
            signed_risk_fraction=0.0,
            lots=0.0,
            target_risk_usd=0.0,
            actual_risk_usd=0.0,
            notional_quote=0.0,
        )

    side: SideOrFlat = "buy" if signed_risk_fraction > 0.0 else "sell"
    target_risk_usd = abs(float(signed_risk_fraction)) * float(equity_usd)

    risk_per_lot_quote = float(stop_distance_price) * spec.contract_size
    risk_per_lot_usd = quote_pnl_to_usd(
        symbol=spec.symbol,
        pnl_quote=risk_per_lot_quote,
        conversion_price=entry_price,
        instrument_spec=spec,
    )

    _validate_positive("risk_per_lot_usd", risk_per_lot_usd)

    raw_lots = target_risk_usd / risk_per_lot_usd
    lots = round_lots_down(
        raw_lots=raw_lots,
        lot_step=spec.lot_step,
        min_lot=spec.min_lot,
    )

    actual_risk_usd = lots * risk_per_lot_usd
    notional_quote = lots * spec.contract_size * entry_price

    return PositionSize(
        symbol=spec.symbol,
        side=side,
        signed_risk_fraction=float(signed_risk_fraction),
        lots=lots,
        target_risk_usd=target_risk_usd,
        actual_risk_usd=actual_risk_usd,
        notional_quote=notional_quote,
    )


def round_lots_down(
    *,
    raw_lots: float,
    lot_step: float,
    min_lot: float,
) -> float:
    """Round broker lots down to the nearest allowed lot step.

    Returning zero when the rounded size is below ``min_lot`` is safer than
    forcing a minimum trade. Forcing the minimum can turn a tiny intended risk
    into an oversized live position on small accounts.
    """

    if raw_lots < 0.0:
        raise ValueError("raw_lots must be >= 0.0")
    _validate_positive("lot_step", lot_step)
    _validate_positive("min_lot", min_lot)

    steps = math.floor((raw_lots + 1e-12) / lot_step)
    rounded = round(steps * lot_step, 10)

    if rounded < min_lot:
        return 0.0

    return rounded


def quote_pnl_to_usd(
    *,
    symbol: str,
    pnl_quote: float,
    conversion_price: float | None = None,
    instrument_spec: InstrumentSpec | None = None,
) -> float:
    """Convert instrument quote-currency P&L into USD account P&L.

    XAUUSD already quotes in USD, so no conversion is needed. USDJPY quotes in
    JPY; because the price is JPY per 1 USD, JPY P&L converts to USD as
    ``pnl_jpy / usdjpy_price``.
    """

    spec = instrument_spec if instrument_spec is not None else get_default_instrument_spec(symbol)
    _validate_instrument_spec(spec)

    if spec.symbol.upper() != symbol.upper():
        raise ValueError("instrument_spec symbol must match symbol")

    quote_currency = spec.quote_currency.upper()

    if quote_currency == "USD":
        return float(pnl_quote)

    if quote_currency == "JPY":
        if conversion_price is None:
            raise ValueError("conversion_price is required for JPY quote-currency P&L")
        _validate_positive("conversion_price", conversion_price)
        return float(pnl_quote) / float(conversion_price)

    raise ValueError(f"unsupported quote currency {spec.quote_currency!r}")


def fill_pnl_usd(
    *,
    fill: Fill,
    conversion_price: float | None = None,
    instrument_spec: InstrumentSpec | None = None,
) -> float:
    """Return account-currency P&L for one completed fill after commission.

    ``Fill.pnl_quote`` is intentionally before commission and may be in quote
    currency. This function converts it to USD and subtracts the USD commission
    exactly once.
    """

    spec = instrument_spec if instrument_spec is not None else get_default_instrument_spec(fill.symbol)

    effective_conversion_price = conversion_price
    if effective_conversion_price is None and spec.quote_currency.upper() == "JPY":
        effective_conversion_price = fill.exit_price

    gross_usd = quote_pnl_to_usd(
        symbol=fill.symbol,
        pnl_quote=fill.pnl_quote,
        conversion_price=effective_conversion_price,
        instrument_spec=spec,
    )

    return gross_usd - float(fill.commission)


def build_portfolio_result(
    *,
    fills: Sequence[Fill],
    starting_equity_usd: float = 10_000.0,
) -> PortfolioResult:
    """Build an equity curve from completed fills.

    Fills must be sorted by exit time. The engine is event-driven, so silently
    reordering fills would hide bugs in the caller. If two fills exit at the same
    timestamp, their input order is preserved.
    """

    _validate_positive("starting_equity_usd", starting_equity_usd)

    fill_tuple = tuple(fills)
    if not fill_tuple:
        empty = pd.Series(dtype=float)
        empty.index = pd.DatetimeIndex([], tz="UTC")
        equity_curve = empty.rename("equity_usd")
        returns = empty.rename("returns")
        drawdowns = empty.rename("drawdown")
        return PortfolioResult(
            fills=fill_tuple,
            starting_equity_usd=float(starting_equity_usd),
            ending_equity_usd=float(starting_equity_usd),
            equity_curve=equity_curve,
            returns=returns,
            drawdowns=drawdowns,
            max_drawdown=0.0,
        )

    _validate_fills_sorted(fill_tuple)

    equity = float(starting_equity_usd)
    equity_values: list[float] = []
    return_values: list[float] = []
    timestamps: list[pd.Timestamp] = []

    for fill in fill_tuple:
        exit_time = _require_utc_timestamp("fill.exit_time_utc", fill.exit_time_utc)
        previous_equity = equity
        equity += fill_pnl_usd(fill=fill)

        equity_values.append(equity)
        return_values.append((equity - previous_equity) / previous_equity)
        timestamps.append(exit_time)

    index = pd.DatetimeIndex(timestamps, tz="UTC")
    equity_curve = pd.Series(equity_values, index=index, name="equity_usd")
    returns = pd.Series(return_values, index=index, name="returns")
    drawdowns = (equity_curve / equity_curve.cummax() - 1.0).rename("drawdown")

    return PortfolioResult(
        fills=fill_tuple,
        starting_equity_usd=float(starting_equity_usd),
        ending_equity_usd=float(equity_curve.iloc[-1]),
        equity_curve=equity_curve,
        returns=returns,
        drawdowns=drawdowns,
        max_drawdown=float(drawdowns.min()),
    )


def _validate_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0.0")


def _validate_instrument_spec(spec: InstrumentSpec) -> None:
    _validate_positive("contract_size", spec.contract_size)
    _validate_positive("lot_step", spec.lot_step)
    _validate_positive("min_lot", spec.min_lot)

    if not spec.symbol:
        raise ValueError("symbol must be non-empty")
    if not spec.quote_currency:
        raise ValueError("quote_currency must be non-empty")


def _require_utc_timestamp(name: str, timestamp: pd.Timestamp) -> pd.Timestamp:
    ts = pd.Timestamp(timestamp)

    if ts.tz is None:
        raise ValueError(f"{name} must be timezone-aware UTC")

    return ts.tz_convert("UTC")


def _validate_fills_sorted(fills: tuple[Fill, ...]) -> None:
    previous: pd.Timestamp | None = None

    for fill in fills:
        current = _require_utc_timestamp("fill.exit_time_utc", fill.exit_time_utc)

        if previous is not None and current < previous:
            raise ValueError("fills must be sorted by exit_time_utc")

        previous = current
