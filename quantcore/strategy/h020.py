from __future__ import annotations

"""H020 notional-aware sizing contract.

H020 is a sizing-contract hypothesis built on H019 lifecycle semantics.

This module intentionally does not execute fills and does not weaken H018
event-engine guards. It computes explicit pre-trade lot intents that can be
diagnosed before any strict event validation.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import pandas as pd

from quantcore.backtest.cost_model import get_default_cost_spec
from quantcore.backtest.portfolio import (
    InstrumentSpec,
    PositionSize,
    get_default_instrument_spec,
    quote_pnl_to_usd,
    round_lots_down,
    size_position_from_risk,
)


_SYMBOLS = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class H020SizingConfig:
    """Strategy-level notional caps below the H018 hard guard."""

    per_trade_max_gross_leverage: float = 9.0
    portfolio_max_gross_leverage: float = 9.0

    @classmethod
    def default(cls) -> "H020SizingConfig":
        return cls()


@dataclass(frozen=True)
class H020SymbolSizingIntent:
    """Explicit H020 lot intent for one symbol at one decision interval."""

    symbol: str
    side: str | None
    signed_risk_fraction: float
    entry_raw_price: float | None
    stop_price: float | None
    raw_stop_distance: float | None
    risk_based_lots: float
    per_trade_cap_lots: float
    pre_portfolio_lots: float
    final_lots: float
    final_signed_risk_fraction: float
    notional_usd: float
    gross_leverage: float
    suppressed: bool
    suppression_reason: str | None


@dataclass(frozen=True)
class H020IntervalSizingResult:
    """H020 sizing output for one decision/entry interval."""

    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    equity_usd: float
    intents: Mapping[str, H020SymbolSizingIntent]
    portfolio_notional_usd: float
    portfolio_gross_leverage: float
    portfolio_scaled: bool


def size_h020_interval_intents(
    *,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    equity_usd: float,
    signed_risk_by_symbol: Mapping[str, float],
    entry_raw_price_by_symbol: Mapping[str, float],
    stops_long_by_symbol: Mapping[str, float],
    stops_short_by_symbol: Mapping[str, float],
    config: H020SizingConfig | None = None,
    instrument_specs: Mapping[str, InstrumentSpec] | None = None,
) -> H020IntervalSizingResult:
    """Compute H020 notional-aware lot intents for one interval.

    Suppression here is strategy-level intent suppression. The event engine must
    still fail closed if a hard-guard violation reaches validation.
    """

    if equity_usd <= 0.0:
        raise ValueError("equity_usd must be positive")

    cfg = config if config is not None else H020SizingConfig.default()
    _validate_config(cfg)

    specs = (
        MappingProxyType(
            {symbol: get_default_instrument_spec(symbol) for symbol in _SYMBOLS}
        )
        if instrument_specs is None
        else instrument_specs
    )

    pre_portfolio: dict[str, H020SymbolSizingIntent] = {}

    for symbol in _SYMBOLS:
        spec = specs[symbol]
        signed_risk_fraction = float(signed_risk_by_symbol.get(symbol, 0.0))

        intent = _build_pre_portfolio_intent(
            symbol=symbol,
            signed_risk_fraction=signed_risk_fraction,
            equity_usd=equity_usd,
            entry_raw_price_by_symbol=entry_raw_price_by_symbol,
            stops_long_by_symbol=stops_long_by_symbol,
            stops_short_by_symbol=stops_short_by_symbol,
            config=cfg,
            instrument_spec=spec,
        )
        pre_portfolio[symbol] = intent

    active_notional = sum(intent.notional_usd for intent in pre_portfolio.values())
    cap_notional = cfg.portfolio_max_gross_leverage * float(equity_usd)
    portfolio_scaled = active_notional > cap_notional and active_notional > 0.0

    if not portfolio_scaled:
        return H020IntervalSizingResult(
            decision_time=pd.Timestamp(decision_time),
            entry_time=pd.Timestamp(entry_time),
            equity_usd=float(equity_usd),
            intents=MappingProxyType(pre_portfolio),
            portfolio_notional_usd=active_notional,
            portfolio_gross_leverage=active_notional / float(equity_usd),
            portfolio_scaled=False,
        )

    scale = cap_notional / active_notional
    scaled: dict[str, H020SymbolSizingIntent] = {}

    for symbol, intent in pre_portfolio.items():
        spec = specs[symbol]
        if intent.final_lots <= 0.0:
            scaled[symbol] = intent
            continue

        scaled_lots = round_lots_down(
            raw_lots=intent.final_lots * scale,
            lot_step=spec.lot_step,
            min_lot=spec.min_lot,
        )
        scaled[symbol] = _replace_lots(
            intent=intent,
            lots=scaled_lots,
            equity_usd=equity_usd,
            instrument_spec=spec,
            suppression_reason=(
                "below_min_lot_after_portfolio_scale"
                if scaled_lots == 0.0
                else None
            ),
        )

    portfolio_notional = sum(intent.notional_usd for intent in scaled.values())

    return H020IntervalSizingResult(
        decision_time=pd.Timestamp(decision_time),
        entry_time=pd.Timestamp(entry_time),
        equity_usd=float(equity_usd),
        intents=MappingProxyType(scaled),
        portfolio_notional_usd=portfolio_notional,
        portfolio_gross_leverage=portfolio_notional / float(equity_usd),
        portfolio_scaled=True,
    )


def _build_pre_portfolio_intent(
    *,
    symbol: str,
    signed_risk_fraction: float,
    equity_usd: float,
    entry_raw_price_by_symbol: Mapping[str, float],
    stops_long_by_symbol: Mapping[str, float],
    stops_short_by_symbol: Mapping[str, float],
    config: H020SizingConfig,
    instrument_spec: InstrumentSpec,
) -> H020SymbolSizingIntent:
    side = _side_from_signed_risk(signed_risk_fraction)
    if side is None:
        return _flat_intent(
            symbol=symbol,
            signed_risk_fraction=signed_risk_fraction,
            side=None,
            suppression_reason="flat_signal",
        )

    entry_raw_price = float(entry_raw_price_by_symbol[symbol])
    stop_price = float(
        stops_long_by_symbol[symbol] if side == "buy" else stops_short_by_symbol[symbol]
    )

    protective = (
        stop_price < entry_raw_price if side == "buy" else stop_price > entry_raw_price
    )
    raw_stop_distance = abs(entry_raw_price - stop_price)

    if not protective:
        return _flat_intent(
            symbol=symbol,
            signed_risk_fraction=signed_risk_fraction,
            side=side,
            entry_raw_price=entry_raw_price,
            stop_price=stop_price,
            raw_stop_distance=raw_stop_distance,
            suppression_reason="invalid_stop_geometry",
        )

    minimum_stop_distance = float(get_default_cost_spec(symbol).spread_price)
    if raw_stop_distance < minimum_stop_distance:
        return _flat_intent(
            symbol=symbol,
            signed_risk_fraction=signed_risk_fraction,
            side=side,
            entry_raw_price=entry_raw_price,
            stop_price=stop_price,
            raw_stop_distance=raw_stop_distance,
            suppression_reason="minimum_stop_distance",
        )

    risk_size = size_position_from_risk(
        symbol=symbol,
        signed_risk_fraction=signed_risk_fraction,
        equity_usd=equity_usd,
        entry_price=entry_raw_price,
        stop_distance_price=raw_stop_distance,
        instrument_spec=instrument_spec,
    )

    per_trade_cap_lots = _max_notional_lots(
        symbol=symbol,
        equity_usd=equity_usd,
        entry_raw_price=entry_raw_price,
        max_gross_leverage=config.per_trade_max_gross_leverage,
        instrument_spec=instrument_spec,
    )

    pre_portfolio_lots = min(risk_size.lots, per_trade_cap_lots)

    if pre_portfolio_lots == 0.0:
        return _flat_intent(
            symbol=symbol,
            signed_risk_fraction=signed_risk_fraction,
            side=side,
            entry_raw_price=entry_raw_price,
            stop_price=stop_price,
            raw_stop_distance=raw_stop_distance,
            risk_based_lots=risk_size.lots,
            per_trade_cap_lots=per_trade_cap_lots,
            suppression_reason="below_min_lot_after_per_trade_cap",
        )

    return _intent_from_lots(
        symbol=symbol,
        side=side,
        signed_risk_fraction=signed_risk_fraction,
        entry_raw_price=entry_raw_price,
        stop_price=stop_price,
        raw_stop_distance=raw_stop_distance,
        risk_based_lots=risk_size.lots,
        per_trade_cap_lots=per_trade_cap_lots,
        pre_portfolio_lots=pre_portfolio_lots,
        final_lots=pre_portfolio_lots,
        equity_usd=equity_usd,
        instrument_spec=instrument_spec,
    )


def _side_from_signed_risk(signed_risk_fraction: float) -> str | None:
    if signed_risk_fraction > 0.0:
        return "buy"
    if signed_risk_fraction < 0.0:
        return "sell"
    return None


def _max_notional_lots(
    *,
    symbol: str,
    equity_usd: float,
    entry_raw_price: float,
    max_gross_leverage: float,
    instrument_spec: InstrumentSpec,
) -> float:
    max_notional_usd = float(equity_usd) * float(max_gross_leverage)
    notional_per_lot_usd = _notional_usd(
        symbol=symbol,
        lots=1.0,
        entry_raw_price=entry_raw_price,
        instrument_spec=instrument_spec,
    )

    return round_lots_down(
        raw_lots=max_notional_usd / notional_per_lot_usd,
        lot_step=instrument_spec.lot_step,
        min_lot=instrument_spec.min_lot,
    )


def _intent_from_lots(
    *,
    symbol: str,
    side: str,
    signed_risk_fraction: float,
    entry_raw_price: float,
    stop_price: float,
    raw_stop_distance: float,
    risk_based_lots: float,
    per_trade_cap_lots: float,
    pre_portfolio_lots: float,
    final_lots: float,
    equity_usd: float,
    instrument_spec: InstrumentSpec,
) -> H020SymbolSizingIntent:
    notional_usd = _notional_usd(
        symbol=symbol,
        lots=final_lots,
        entry_raw_price=entry_raw_price,
        instrument_spec=instrument_spec,
    )
    actual_risk_usd = _actual_risk_usd(
        symbol=symbol,
        lots=final_lots,
        entry_raw_price=entry_raw_price,
        raw_stop_distance=raw_stop_distance,
        instrument_spec=instrument_spec,
    )
    final_signed_risk_fraction = actual_risk_usd / float(equity_usd)
    if side == "sell":
        final_signed_risk_fraction *= -1.0

    return H020SymbolSizingIntent(
        symbol=symbol,
        side=side,
        signed_risk_fraction=float(signed_risk_fraction),
        entry_raw_price=float(entry_raw_price),
        stop_price=float(stop_price),
        raw_stop_distance=float(raw_stop_distance),
        risk_based_lots=float(risk_based_lots),
        per_trade_cap_lots=float(per_trade_cap_lots),
        pre_portfolio_lots=float(pre_portfolio_lots),
        final_lots=float(final_lots),
        final_signed_risk_fraction=float(final_signed_risk_fraction),
        notional_usd=float(notional_usd),
        gross_leverage=float(notional_usd) / float(equity_usd),
        suppressed=False,
        suppression_reason=None,
    )


def _replace_lots(
    *,
    intent: H020SymbolSizingIntent,
    lots: float,
    equity_usd: float,
    instrument_spec: InstrumentSpec,
    suppression_reason: str | None,
) -> H020SymbolSizingIntent:
    if lots == 0.0:
        return _flat_intent(
            symbol=intent.symbol,
            signed_risk_fraction=intent.signed_risk_fraction,
            side=intent.side,
            entry_raw_price=intent.entry_raw_price,
            stop_price=intent.stop_price,
            raw_stop_distance=intent.raw_stop_distance,
            risk_based_lots=intent.risk_based_lots,
            per_trade_cap_lots=intent.per_trade_cap_lots,
            pre_portfolio_lots=intent.pre_portfolio_lots,
            suppression_reason=suppression_reason,
        )

    return _intent_from_lots(
        symbol=intent.symbol,
        side=intent.side or "buy",
        signed_risk_fraction=intent.signed_risk_fraction,
        entry_raw_price=float(intent.entry_raw_price),
        stop_price=float(intent.stop_price),
        raw_stop_distance=float(intent.raw_stop_distance),
        risk_based_lots=intent.risk_based_lots,
        per_trade_cap_lots=intent.per_trade_cap_lots,
        pre_portfolio_lots=intent.pre_portfolio_lots,
        final_lots=lots,
        equity_usd=equity_usd,
        instrument_spec=instrument_spec,
    )


def _flat_intent(
    *,
    symbol: str,
    signed_risk_fraction: float,
    side: str | None,
    suppression_reason: str,
    entry_raw_price: float | None = None,
    stop_price: float | None = None,
    raw_stop_distance: float | None = None,
    risk_based_lots: float = 0.0,
    per_trade_cap_lots: float = 0.0,
    pre_portfolio_lots: float = 0.0,
) -> H020SymbolSizingIntent:
    return H020SymbolSizingIntent(
        symbol=symbol,
        side=side,
        signed_risk_fraction=float(signed_risk_fraction),
        entry_raw_price=entry_raw_price,
        stop_price=stop_price,
        raw_stop_distance=raw_stop_distance,
        risk_based_lots=float(risk_based_lots),
        per_trade_cap_lots=float(per_trade_cap_lots),
        pre_portfolio_lots=float(pre_portfolio_lots),
        final_lots=0.0,
        final_signed_risk_fraction=0.0,
        notional_usd=0.0,
        gross_leverage=0.0,
        suppressed=True,
        suppression_reason=suppression_reason,
    )


def _notional_usd(
    *,
    symbol: str,
    lots: float,
    entry_raw_price: float,
    instrument_spec: InstrumentSpec,
) -> float:
    if lots == 0.0:
        return 0.0

    if instrument_spec.quote_currency.upper() == "JPY":
        return float(lots) * instrument_spec.contract_size

    if instrument_spec.quote_currency.upper() == "USD":
        return float(lots) * instrument_spec.contract_size * float(entry_raw_price)

    raise ValueError(f"unsupported quote currency {instrument_spec.quote_currency!r}")


def _actual_risk_usd(
    *,
    symbol: str,
    lots: float,
    entry_raw_price: float,
    raw_stop_distance: float,
    instrument_spec: InstrumentSpec,
) -> float:
    risk_quote = float(lots) * instrument_spec.contract_size * float(raw_stop_distance)
    return quote_pnl_to_usd(
        symbol=symbol,
        pnl_quote=risk_quote,
        conversion_price=entry_raw_price,
        instrument_spec=instrument_spec,
    )


def _validate_config(config: H020SizingConfig) -> None:
    if config.per_trade_max_gross_leverage <= 0.0:
        raise ValueError("per_trade_max_gross_leverage must be positive")
    if config.portfolio_max_gross_leverage <= 0.0:
        raise ValueError("portfolio_max_gross_leverage must be positive")

def generate_h020_intent_panel(
    *,
    positions: pd.DataFrame,
    stops_long: pd.DataFrame,
    stops_short: pd.DataFrame,
    h4_by_symbol: Mapping[str, pd.DataFrame],
    equity_usd: float = 10000.0,
    config: H020SizingConfig | None = None,
    instrument_specs: Mapping[str, InstrumentSpec] | None = None,
) -> list[H020IntervalSizingResult]:
    """Iterate decision intervals and generate H020 explicit sizing intents."""
    results = []
    symbols = list(positions.columns)
    timestamps = positions.index

    for i in range(len(timestamps) - 1):
        decision_time = timestamps[i]
        entry_time = timestamps[i + 1]

        signed_risk_by_symbol = {}
        entry_raw_price_by_symbol = {}
        sl_long = {}
        sl_short = {}

        for sym in symbols:
            risk = positions.at[decision_time, sym]
            if pd.isna(risk) or risk == 0.0:
                continue

            df = h4_by_symbol.get(sym)
            if df is None or entry_time not in df.index:
                continue

            signed_risk_by_symbol[sym] = float(risk)
            entry_raw_price_by_symbol[sym] = float(df.at[entry_time, "open"])
            sl_long[sym] = float(stops_long.at[decision_time, sym])
            sl_short[sym] = float(stops_short.at[decision_time, sym])

        if not signed_risk_by_symbol:
            continue

        res = size_h020_interval_intents(
            decision_time=decision_time,
            entry_time=entry_time,
            equity_usd=equity_usd,
            signed_risk_by_symbol=signed_risk_by_symbol,
            entry_raw_price_by_symbol=entry_raw_price_by_symbol,
            stops_long_by_symbol=sl_long,
            stops_short_by_symbol=sl_short,
            config=config,
            instrument_specs=instrument_specs,
        )
        results.append(res)

    return results
