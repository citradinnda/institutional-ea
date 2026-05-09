"""H024 dry-run/log-only execution-preparation primitives.

This module must remain incapable of placing orders. It contains no MT5 import
and no order-send function. It only converts candidate trade intent into
structured log records.

Research/preparation only. No demo/live/Phase 4 approval.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal, Mapping

ActionKind = Literal["WOULD_OPEN", "NO_ACTION", "BLOCKED"]
Side = Literal["buy", "sell"]


SYMBOL_MAPPING: Mapping[str, str] = {
    "USDJPY": "USDJPYm",
    "XAUUSD": "XAUUSDm",
}

MAXIMUM_PER_TRADE_GROSS_LEVERAGE = 10.0


@dataclass(frozen=True)
class DryRunConfig:
    """Safety mode for dry-run execution preparation.

    ``kill_switch_enabled`` defaults false. That means no trade intent may move
    past BLOCKED until the caller explicitly enables the dry-run calculation
    gate. Even then, this module can only emit WOULD_* log records.
    """

    mode: Literal["dry_run"] = "dry_run"
    kill_switch_enabled: bool = False


@dataclass(frozen=True)
class BrokerSymbolFacts:
    model_symbol: str
    broker_symbol: str
    contract_size: float
    quote_currency: str
    volume_min: float
    volume_max: float
    volume_step: float
    stops_level_points: float
    freeze_level_points: float
    point: float
    digits: int


@dataclass(frozen=True)
class TradeCandidate:
    model_symbol: str
    side: Side | None
    timestamp_utc: str
    equity_usd: float
    signed_risk_fraction: float
    raw_entry_price: float
    raw_stop_price: float
    raw_lots: float


@dataclass(frozen=True)
class DryRunAction:
    action: ActionKind
    model_symbol: str
    broker_symbol: str | None
    side: Side | None
    timestamp_utc: str
    reason: str
    raw_lots: float
    normalized_lots: float
    raw_entry_price: float
    raw_stop_price: float
    raw_stop_distance: float
    notional_quote: float
    notional_usd: float
    per_trade_gross_leverage: float
    kill_switch_enabled: bool
    mode: str


def default_broker_symbol_facts() -> dict[str, BrokerSymbolFacts]:
    """Return reconciled Exness MT5 facts for H024 symbols."""

    return {
        "USDJPY": BrokerSymbolFacts(
            model_symbol="USDJPY",
            broker_symbol="USDJPYm",
            contract_size=100_000.0,
            quote_currency="JPY",
            volume_min=0.01,
            volume_max=300.0,
            volume_step=0.01,
            stops_level_points=0.0,
            freeze_level_points=0.0,
            point=0.001,
            digits=3,
        ),
        "XAUUSD": BrokerSymbolFacts(
            model_symbol="XAUUSD",
            broker_symbol="XAUUSDm",
            contract_size=100.0,
            quote_currency="USD",
            volume_min=0.01,
            volume_max=200.0,
            volume_step=0.01,
            stops_level_points=0.0,
            freeze_level_points=0.0,
            point=0.001,
            digits=3,
        ),
    }


def build_dry_run_action(
    *,
    config: DryRunConfig,
    candidate: TradeCandidate,
    broker_facts_by_symbol: Mapping[str, BrokerSymbolFacts] | None = None,
) -> DryRunAction:
    """Convert one H024 candidate into a dry-run action log.

    The function never places, modifies, closes, or deletes orders.
    """

    if config.mode != "dry_run":
        raise ValueError("only dry_run mode is implemented")

    facts_by_symbol = (
        default_broker_symbol_facts()
        if broker_facts_by_symbol is None
        else dict(broker_facts_by_symbol)
    )
    model_symbol = candidate.model_symbol.upper()

    facts = facts_by_symbol.get(model_symbol)
    if facts is None:
        return _blocked(candidate=candidate, reason="unsupported symbol", config=config)

    if facts.broker_symbol != SYMBOL_MAPPING.get(model_symbol):
        return _blocked(candidate=candidate, reason="unexpected broker symbol mapping", config=config)

    if candidate.side is None:
        return _base_action(
            action="NO_ACTION",
            candidate=candidate,
            facts=facts,
            reason="flat signal",
            normalized_lots=0.0,
            notional_quote=0.0,
            notional_usd=0.0,
            gross_leverage=0.0,
            config=config,
        )

    if not config.kill_switch_enabled:
        return _blocked(
            candidate=candidate,
            reason="blocked by kill switch",
            config=config,
            facts=facts,
        )

    stop_distance = _raw_stop_distance(candidate)
    if candidate.side == "buy" and candidate.raw_stop_price >= candidate.raw_entry_price:
        return _blocked(candidate=candidate, reason="invalid long stop geometry", config=config, facts=facts)
    if candidate.side == "sell" and candidate.raw_stop_price <= candidate.raw_entry_price:
        return _blocked(candidate=candidate, reason="invalid short stop geometry", config=config, facts=facts)

    minimum_stop_distance = facts.stops_level_points * facts.point
    if stop_distance < minimum_stop_distance and not math.isclose(
        stop_distance,
        minimum_stop_distance,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        return _blocked(candidate=candidate, reason="blocked by minimum stop distance", config=config, facts=facts)

    normalized_lots = normalize_lots_down(
        raw_lots=candidate.raw_lots,
        volume_min=facts.volume_min,
        volume_max=facts.volume_max,
        volume_step=facts.volume_step,
    )
    if normalized_lots == 0.0:
        return _blocked(candidate=candidate, reason="blocked by volume normalization", config=config, facts=facts)

    notional_quote = normalized_lots * facts.contract_size * candidate.raw_entry_price
    notional_usd = _notional_usd(
        notional_quote=notional_quote,
        entry_price=candidate.raw_entry_price,
        quote_currency=facts.quote_currency,
    )
    gross_leverage = notional_usd / candidate.equity_usd

    if gross_leverage > MAXIMUM_PER_TRADE_GROSS_LEVERAGE and not math.isclose(
        gross_leverage,
        MAXIMUM_PER_TRADE_GROSS_LEVERAGE,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        return _base_action(
            action="BLOCKED",
            candidate=candidate,
            facts=facts,
            reason="blocked by per-trade leverage",
            normalized_lots=normalized_lots,
            notional_quote=notional_quote,
            notional_usd=notional_usd,
            gross_leverage=gross_leverage,
            config=config,
        )

    return _base_action(
        action="WOULD_OPEN",
        candidate=candidate,
        facts=facts,
        reason="dry-run intent only; no order sent",
        normalized_lots=normalized_lots,
        notional_quote=notional_quote,
        notional_usd=notional_usd,
        gross_leverage=gross_leverage,
        config=config,
    )


def normalize_lots_down(
    *,
    raw_lots: float,
    volume_min: float,
    volume_max: float,
    volume_step: float,
) -> float:
    """Round lots down to the broker step without exceeding requested risk."""

    if raw_lots < 0.0:
        raise ValueError("raw_lots must be >= 0.0")
    _validate_positive("volume_min", volume_min)
    _validate_positive("volume_max", volume_max)
    _validate_positive("volume_step", volume_step)

    if raw_lots < volume_min:
        return 0.0

    steps = math.floor((raw_lots + 1e-12) / volume_step)
    rounded = round(steps * volume_step, 10)

    if rounded < volume_min:
        return 0.0
    if rounded > volume_max:
        return 0.0

    return rounded


def _blocked(
    *,
    candidate: TradeCandidate,
    reason: str,
    config: DryRunConfig,
    facts: BrokerSymbolFacts | None = None,
) -> DryRunAction:
    return _base_action(
        action="BLOCKED",
        candidate=candidate,
        facts=facts,
        reason=reason,
        normalized_lots=0.0,
        notional_quote=0.0,
        notional_usd=0.0,
        gross_leverage=0.0,
        config=config,
    )


def _base_action(
    *,
    action: ActionKind,
    candidate: TradeCandidate,
    facts: BrokerSymbolFacts | None,
    reason: str,
    normalized_lots: float,
    notional_quote: float,
    notional_usd: float,
    gross_leverage: float,
    config: DryRunConfig,
) -> DryRunAction:
    return DryRunAction(
        action=action,
        model_symbol=candidate.model_symbol.upper(),
        broker_symbol=facts.broker_symbol if facts is not None else None,
        side=candidate.side,
        timestamp_utc=candidate.timestamp_utc,
        reason=reason,
        raw_lots=float(candidate.raw_lots),
        normalized_lots=float(normalized_lots),
        raw_entry_price=float(candidate.raw_entry_price),
        raw_stop_price=float(candidate.raw_stop_price),
        raw_stop_distance=_raw_stop_distance(candidate),
        notional_quote=float(notional_quote),
        notional_usd=float(notional_usd),
        per_trade_gross_leverage=float(gross_leverage),
        kill_switch_enabled=config.kill_switch_enabled,
        mode=config.mode,
    )


def _raw_stop_distance(candidate: TradeCandidate) -> float:
    return abs(float(candidate.raw_entry_price) - float(candidate.raw_stop_price))


def _notional_usd(*, notional_quote: float, entry_price: float, quote_currency: str) -> float:
    if entry_price <= 0.0:
        raise ValueError("entry_price must be positive")
    if quote_currency.upper() == "USD":
        return float(notional_quote)
    if quote_currency.upper() == "JPY":
        return float(notional_quote) / float(entry_price)
    raise ValueError(f"unsupported quote currency {quote_currency!r}")


def _validate_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0.0")
