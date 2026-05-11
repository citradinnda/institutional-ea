"""Pure Python H024 broker metadata preflight contract.

This module validates a review-only H024 proposed demo-order plan against an
explicit, offline broker metadata snapshot.

Research-only boundary:
- no MetaTrader 5 import
- no terminal access
- no broker API access
- no OrderSend / OrderCheck / MqlTradeRequest equivalent
- no demo or live order placement
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Mapping

PLAN_SCHEMA_VERSION = "h024_demo_order_plan_v1"
PLAN_KIND = "PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY"
PREFLIGHT_SCHEMA_VERSION = "h024_broker_metadata_preflight_v1"
PREFLIGHT_KIND = "BROKER_METADATA_PREFLIGHT_REVIEW_ONLY"

DEFAULT_DEMO_SERVER_ALLOWLIST: frozenset[str] = frozenset({"Exness-MT5Trial6"})
_ALLOWED_NORMALIZED_SYMBOLS: frozenset[str] = frozenset({"USDJPY", "XAUUSD"})
_SYMBOL_NORMALIZATION: dict[str, str] = {
    "USDJPY": "USDJPY",
    "USDJPYm": "USDJPY",
    "USDJPYc": "USDJPY",
    "XAUUSD": "XAUUSD",
    "XAUUSDm": "XAUUSD",
    "XAUUSDc": "XAUUSD",
}
_LIVE_LIKE_SERVER_MARKERS: tuple[str, ...] = ("live", "real", "prod", "production")
_FORBIDDEN_EXECUTION_KEYS: frozenset[str] = frozenset(
    {
        "order",
        "order_id",
        "ticket",
        "position",
        "position_id",
        "deal",
        "deal_id",
        "mt5_request",
        "mql_trade_request",
        "broker_request",
        "execution_result",
        "retcode",
        "retcode_external",
        "ordersend",
        "order_send",
        "ordercheck",
        "order_check",
    }
)


class H024BrokerMetadataPreflightError(ValueError):
    """Raised when a proposed plan fails offline broker metadata preflight."""


@dataclass(frozen=True)
class H024SymbolMetadata:
    """Offline broker metadata snapshot for one symbol.

    The snapshot must be supplied explicitly by the caller. This contract does
    not query a terminal or broker.
    """

    symbol: str
    normalized_symbol: str
    account_server: str
    account_currency: str
    tick_size: float
    tick_value: float
    min_volume: float
    max_volume: float
    volume_step: float
    volume_digits: int
    price_digits: int
    metadata_source: str = "manual_offline_snapshot"
    spread_points: float | None = None


@dataclass(frozen=True)
class H024BrokerMetadataPreflight:
    """Review-only broker metadata preflight result.

    This is not an order request and cannot execute. It is a gate artifact for
    reviewing whether a proposed plan is internally consistent with a broker
    metadata snapshot.
    """

    schema_version: str
    preflight_kind: str
    plan_schema_version: str
    plan_kind: str
    symbol: str
    normalized_symbol: str
    account_server: str
    account_currency: str
    account_balance: float
    account_equity: float
    side: str
    entry_price: float
    stop_loss: float
    volume_lots: float
    risk_usd: float
    source_timestamp: str
    source_reason: str
    metadata_source: str
    tick_size: float
    tick_value: float
    min_volume: float
    max_volume: float
    volume_step: float
    volume_digits: int
    price_digits: int
    spread_points: float | None
    estimated_loss_usd: float
    risk_fraction_of_balance: float
    max_risk_fraction: float
    checks: tuple[str, ...]


def build_h024_broker_metadata_preflight(
    plan: Mapping[str, Any] | Any,
    symbol_metadata: H024SymbolMetadata | Mapping[str, Any],
    *,
    allowed_demo_servers: set[str] | frozenset[str] | tuple[str, ...] | list[str] | None = None,
    max_risk_fraction: float = 0.01,
) -> H024BrokerMetadataPreflight:
    """Validate a proposed demo-order plan against offline broker metadata."""

    plan_record = _coerce_mapping(plan, "plan")
    metadata = _coerce_symbol_metadata(symbol_metadata)
    allowlist = _coerce_allowlist(allowed_demo_servers)

    _reject_execution_like_keys(plan_record)
    _validate_max_risk_fraction(max_risk_fraction)

    _expect_equal(plan_record, "schema_version", PLAN_SCHEMA_VERSION)
    _expect_equal(plan_record, "plan_kind", PLAN_KIND)

    symbol = _require_str(plan_record, "symbol")
    normalized_symbol = _require_str(plan_record, "normalized_symbol")
    expected_normalized = _SYMBOL_NORMALIZATION.get(symbol)
    if expected_normalized is None:
        raise H024BrokerMetadataPreflightError(f"unsupported symbol: {symbol!r}")
    if normalized_symbol != expected_normalized:
        raise H024BrokerMetadataPreflightError(
            "normalized_symbol does not match symbol normalization"
        )
    if normalized_symbol not in _ALLOWED_NORMALIZED_SYMBOLS:
        raise H024BrokerMetadataPreflightError(
            f"unsupported normalized_symbol: {normalized_symbol!r}"
        )

    side = _require_str(plan_record, "side")
    if side not in {"BUY", "SELL"}:
        raise H024BrokerMetadataPreflightError(f"unsupported side: {side!r}")

    entry_price = _require_positive_float(plan_record, "entry_price")
    stop_loss = _require_positive_float(plan_record, "stop_loss")
    volume_lots = _require_positive_float(plan_record, "volume_lots")
    risk_usd = _require_positive_float(plan_record, "risk_usd")
    account_balance = _require_positive_float(plan_record, "account_balance")
    account_equity = _require_positive_float(plan_record, "account_equity")
    account_server = _require_str(plan_record, "account_server")
    account_currency = _require_str(plan_record, "account_currency")
    source_timestamp = _require_str(plan_record, "source_timestamp")
    source_reason = _require_str(plan_record, "source_reason")

    if side == "BUY" and stop_loss >= entry_price:
        raise H024BrokerMetadataPreflightError("BUY stop_loss must be below entry_price")
    if side == "SELL" and stop_loss <= entry_price:
        raise H024BrokerMetadataPreflightError("SELL stop_loss must be above entry_price")

    if "WOULD_OPEN:" not in source_reason:
        raise H024BrokerMetadataPreflightError("source_reason must contain WOULD_OPEN:")
    if "mode=log_only_no_execution" not in source_reason:
        raise H024BrokerMetadataPreflightError(
            "source_reason must contain mode=log_only_no_execution"
        )

    _validate_server(account_server, allowlist)
    if account_currency != "USD":
        raise H024BrokerMetadataPreflightError(
            f"unsupported account_currency: {account_currency!r}"
        )

    _validate_metadata_matches_plan(
        metadata,
        symbol=symbol,
        normalized_symbol=normalized_symbol,
        account_server=account_server,
        account_currency=account_currency,
    )

    _validate_price_alignment(entry_price, metadata.tick_size, "entry_price")
    _validate_price_alignment(stop_loss, metadata.tick_size, "stop_loss")
    _validate_volume(volume_lots, metadata)

    stop_distance = abs(entry_price - stop_loss)
    if stop_distance < metadata.tick_size:
        raise H024BrokerMetadataPreflightError(
            "stop distance must be at least one tick"
        )

    estimated_loss_usd = (
        stop_distance / metadata.tick_size * metadata.tick_value * volume_lots
    )
    if estimated_loss_usd <= 0:
        raise H024BrokerMetadataPreflightError("estimated loss must be positive")
    if estimated_loss_usd > risk_usd * 1.000001:
        raise H024BrokerMetadataPreflightError(
            "metadata-estimated loss exceeds intended risk_usd"
        )

    risk_fraction_of_balance = risk_usd / account_balance
    if risk_fraction_of_balance > max_risk_fraction + 1e-12:
        raise H024BrokerMetadataPreflightError(
            "risk_usd exceeds max risk fraction of account balance"
        )

    return H024BrokerMetadataPreflight(
        schema_version=PREFLIGHT_SCHEMA_VERSION,
        preflight_kind=PREFLIGHT_KIND,
        plan_schema_version=PLAN_SCHEMA_VERSION,
        plan_kind=PLAN_KIND,
        symbol=symbol,
        normalized_symbol=normalized_symbol,
        account_server=account_server,
        account_currency=account_currency,
        account_balance=account_balance,
        account_equity=account_equity,
        side=side,
        entry_price=entry_price,
        stop_loss=stop_loss,
        volume_lots=volume_lots,
        risk_usd=risk_usd,
        source_timestamp=source_timestamp,
        source_reason=source_reason,
        metadata_source=metadata.metadata_source,
        tick_size=metadata.tick_size,
        tick_value=metadata.tick_value,
        min_volume=metadata.min_volume,
        max_volume=metadata.max_volume,
        volume_step=metadata.volume_step,
        volume_digits=metadata.volume_digits,
        price_digits=metadata.price_digits,
        spread_points=metadata.spread_points,
        estimated_loss_usd=estimated_loss_usd,
        risk_fraction_of_balance=risk_fraction_of_balance,
        max_risk_fraction=max_risk_fraction,
        checks=(
            "schema_and_plan_kind_checked",
            "demo_server_allowlisted",
            "symbol_metadata_matched",
            "price_tick_alignment_checked",
            "volume_constraints_checked",
            "metadata_loss_within_intended_risk_checked",
            "risk_fraction_cap_checked",
            "review_only_no_execution",
        ),
    )


def as_preflight_record(preflight: H024BrokerMetadataPreflight) -> dict[str, Any]:
    """Return a JSON-serializable preflight record."""

    return asdict(preflight)


def _coerce_mapping(value: Mapping[str, Any] | Any, name: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if is_dataclass(value):
        return asdict(value)
    raise H024BrokerMetadataPreflightError(f"{name} must be a mapping or dataclass")


def _coerce_symbol_metadata(
    value: H024SymbolMetadata | Mapping[str, Any],
) -> H024SymbolMetadata:
    if isinstance(value, H024SymbolMetadata):
        metadata = value
    elif isinstance(value, Mapping):
        metadata = H024SymbolMetadata(
            symbol=_coerce_nonempty_str(value.get("symbol"), "symbol"),
            normalized_symbol=_coerce_nonempty_str(
                value.get("normalized_symbol"), "normalized_symbol"
            ),
            account_server=_coerce_nonempty_str(
                value.get("account_server"), "account_server"
            ),
            account_currency=_coerce_nonempty_str(
                value.get("account_currency"), "account_currency"
            ),
            tick_size=_coerce_positive_float(value.get("tick_size"), "tick_size"),
            tick_value=_coerce_positive_float(value.get("tick_value"), "tick_value"),
            min_volume=_coerce_positive_float(value.get("min_volume"), "min_volume"),
            max_volume=_coerce_positive_float(value.get("max_volume"), "max_volume"),
            volume_step=_coerce_positive_float(
                value.get("volume_step"), "volume_step"
            ),
            volume_digits=_coerce_nonnegative_int(
                value.get("volume_digits"), "volume_digits"
            ),
            price_digits=_coerce_nonnegative_int(
                value.get("price_digits"), "price_digits"
            ),
            metadata_source=_coerce_nonempty_str(
                value.get("metadata_source", "manual_offline_snapshot"),
                "metadata_source",
            ),
            spread_points=_coerce_optional_nonnegative_float(
                value.get("spread_points"), "spread_points"
            ),
        )
    else:
        raise H024BrokerMetadataPreflightError(
            "symbol_metadata must be a mapping or H024SymbolMetadata"
        )

    if metadata.max_volume < metadata.min_volume:
        raise H024BrokerMetadataPreflightError(
            "max_volume must be greater than or equal to min_volume"
        )
    return metadata


def _validate_metadata_matches_plan(
    metadata: H024SymbolMetadata,
    *,
    symbol: str,
    normalized_symbol: str,
    account_server: str,
    account_currency: str,
) -> None:
    if metadata.symbol != symbol:
        raise H024BrokerMetadataPreflightError("metadata symbol does not match plan")
    if metadata.normalized_symbol != normalized_symbol:
        raise H024BrokerMetadataPreflightError(
            "metadata normalized_symbol does not match plan"
        )
    if metadata.account_server != account_server:
        raise H024BrokerMetadataPreflightError(
            "metadata account_server does not match plan"
        )
    if metadata.account_currency != account_currency:
        raise H024BrokerMetadataPreflightError(
            "metadata account_currency does not match plan"
        )


def _validate_server(server: str, allowed_demo_servers: frozenset[str]) -> None:
    lowered = server.lower()
    if any(marker in lowered for marker in _LIVE_LIKE_SERVER_MARKERS):
        raise H024BrokerMetadataPreflightError("live-like server names are rejected")
    if server not in allowed_demo_servers:
        raise H024BrokerMetadataPreflightError(
            f"server is not in the demo allowlist: {server!r}"
        )


def _validate_price_alignment(price: float, tick_size: float, field: str) -> None:
    quotient = price / tick_size
    if abs(quotient - round(quotient)) > 1e-6:
        raise H024BrokerMetadataPreflightError(
            f"{field} is not aligned to tick_size"
        )


def _validate_volume(volume_lots: float, metadata: H024SymbolMetadata) -> None:
    if volume_lots < metadata.min_volume - 1e-12:
        raise H024BrokerMetadataPreflightError("volume_lots is below min_volume")
    if volume_lots > metadata.max_volume + 1e-12:
        raise H024BrokerMetadataPreflightError("volume_lots is above max_volume")

    quotient = (volume_lots - metadata.min_volume) / metadata.volume_step
    if abs(quotient - round(quotient)) > 1e-8:
        raise H024BrokerMetadataPreflightError(
            "volume_lots is not aligned to broker volume_step"
        )

    if _decimal_places(volume_lots) > metadata.volume_digits:
        raise H024BrokerMetadataPreflightError(
            "volume_lots has more decimals than volume_digits permits"
        )


def _decimal_places(value: float) -> int:
    rendered = f"{value:.12f}".rstrip("0").rstrip(".")
    if "." not in rendered:
        return 0
    return len(rendered.split(".", 1)[1])


def _reject_execution_like_keys(record: Mapping[str, Any]) -> None:
    for key in record:
        if str(key).lower() in _FORBIDDEN_EXECUTION_KEYS:
            raise H024BrokerMetadataPreflightError(
                f"execution-like key is forbidden: {key}"
            )


def _expect_equal(record: Mapping[str, Any], field: str, expected: str) -> None:
    actual = record.get(field)
    if actual != expected:
        raise H024BrokerMetadataPreflightError(
            f"{field} must be {expected!r}, got {actual!r}"
        )


def _require_str(record: Mapping[str, Any], key: str) -> str:
    return _coerce_nonempty_str(record.get(key), key)


def _require_positive_float(record: Mapping[str, Any], key: str) -> float:
    return _coerce_positive_float(record.get(key), key)


def _coerce_nonempty_str(value: Any, key: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise H024BrokerMetadataPreflightError(f"{key} must be a non-empty string")
    return value.strip()


def _coerce_positive_float(value: Any, key: str) -> float:
    try:
        coerced = float(value)
    except (TypeError, ValueError) as exc:
        raise H024BrokerMetadataPreflightError(f"{key} must be numeric") from exc
    if coerced <= 0:
        raise H024BrokerMetadataPreflightError(f"{key} must be positive")
    return coerced


def _coerce_optional_nonnegative_float(value: Any, key: str) -> float | None:
    if value is None:
        return None
    try:
        coerced = float(value)
    except (TypeError, ValueError) as exc:
        raise H024BrokerMetadataPreflightError(f"{key} must be numeric") from exc
    if coerced < 0:
        raise H024BrokerMetadataPreflightError(f"{key} must be non-negative")
    return coerced


def _coerce_nonnegative_int(value: Any, key: str) -> int:
    if isinstance(value, bool):
        raise H024BrokerMetadataPreflightError(f"{key} must be an integer")
    try:
        coerced = int(value)
    except (TypeError, ValueError) as exc:
        raise H024BrokerMetadataPreflightError(f"{key} must be an integer") from exc
    if coerced < 0:
        raise H024BrokerMetadataPreflightError(f"{key} must be non-negative")
    return coerced


def _coerce_allowlist(
    allowed_demo_servers: set[str] | frozenset[str] | tuple[str, ...] | list[str] | None,
) -> frozenset[str]:
    if allowed_demo_servers is None:
        return DEFAULT_DEMO_SERVER_ALLOWLIST
    allowlist = frozenset(
        server.strip() for server in allowed_demo_servers if isinstance(server, str)
    )
    if not allowlist:
        raise H024BrokerMetadataPreflightError("allowed_demo_servers must be non-empty")
    return allowlist


def _validate_max_risk_fraction(value: float) -> None:
    try:
        coerced = float(value)
    except (TypeError, ValueError) as exc:
        raise H024BrokerMetadataPreflightError(
            "max_risk_fraction must be numeric"
        ) from exc
    if coerced <= 0 or coerced > 1:
        raise H024BrokerMetadataPreflightError(
            "max_risk_fraction must be in the interval (0, 1]"
        )
