"""Pure Python H024 proposed demo-order plan contract.

This module intentionally has no MetaTrader 5 dependency and performs no side
effects. It converts an already-verified H024 dry-run request into an internal
plan object for review at the Phase 4 readiness boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

DRY_RUN_SCHEMA_VERSION = "h024_dry_run_execution_request_v1"
DRY_RUN_REQUEST_KIND = "DRY_RUN_MARKET_OPEN"
INTENDED_ACTION_SCHEMA_VERSION = "h024_intended_action_log_v1"

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
_LIVE_LIKE_SERVER_MARKERS: tuple[str, ...] = (
    "live",
    "real",
    "prod",
    "production",
)


class H024DemoOrderPlanError(ValueError):
    """Raised when an H024 dry-run request cannot become a proposed plan."""


@dataclass(frozen=True)
class H024DemoAccountContext:
    """Explicit account/server context required to build a proposed plan."""

    server: str
    account_currency: str
    account_balance: float
    account_equity: float
    broker: str | None = None
    account_login: str | None = None


@dataclass(frozen=True)
class H024DemoOrderPlan:
    """Internal proposed order plan for review only.

    The plan is not a broker request and cannot place an order. It is a typed
    copy of the reviewed intent plus explicit demo-account context.
    """

    schema_version: str
    plan_kind: str
    source_schema_version: str
    source_request_kind: str
    symbol: str
    normalized_symbol: str
    timeframe: str
    side: str
    entry_price: float
    stop_loss: float
    volume_lots: float
    risk_usd: float
    source_timestamp: str
    source_reason: str
    account_server: str
    account_currency: str
    account_balance: float
    account_equity: float
    broker: str | None = None
    account_login: str | None = None


def build_h024_demo_order_plan(
    request: Mapping[str, Any],
    account_context: H024DemoAccountContext | Mapping[str, Any],
    *,
    allowed_demo_servers: set[str] | frozenset[str] | tuple[str, ...] | list[str] | None = None,
) -> H024DemoOrderPlan:
    """Build an internal proposed demo-order plan from a dry-run request.

    `allowed_demo_servers` is an explicit safety boundary. Unknown servers are
    rejected even if their names look demo-like. Live-like names are rejected
    before allowlist matching.
    """

    if not isinstance(request, Mapping):
        raise H024DemoOrderPlanError("request must be a mapping")

    context = _coerce_account_context(account_context)
    allowlist = _coerce_allowlist(allowed_demo_servers)
    _validate_account_context(context, allowlist)

    schema_version = _require_str(request, "schema_version")
    if schema_version != DRY_RUN_SCHEMA_VERSION:
        raise H024DemoOrderPlanError(f"unsupported schema_version: {schema_version!r}")

    request_kind = _require_str(request, "request_kind")
    if request_kind != DRY_RUN_REQUEST_KIND:
        raise H024DemoOrderPlanError(f"unsupported request_kind: {request_kind!r}")

    source_schema = _require_str(request, "source_schema_version")
    if source_schema != INTENDED_ACTION_SCHEMA_VERSION:
        raise H024DemoOrderPlanError(
            f"unsupported source_schema_version: {source_schema!r}"
        )

    symbol = _require_str(request, "symbol")
    normalized_symbol = _require_str(request, "normalized_symbol")
    expected_normalized = _SYMBOL_NORMALIZATION.get(symbol)
    if expected_normalized is None:
        raise H024DemoOrderPlanError(f"unsupported symbol: {symbol!r}")
    if normalized_symbol != expected_normalized:
        raise H024DemoOrderPlanError(
            "normalized_symbol does not match symbol normalization"
        )
    if normalized_symbol not in _ALLOWED_NORMALIZED_SYMBOLS:
        raise H024DemoOrderPlanError(
            f"unsupported normalized_symbol: {normalized_symbol!r}"
        )

    timeframe = _require_str(request, "timeframe")
    if timeframe != "H4":
        raise H024DemoOrderPlanError(f"unsupported timeframe: {timeframe!r}")

    side = _require_str(request, "side")
    if side not in {"BUY", "SELL"}:
        raise H024DemoOrderPlanError(f"unsupported side: {side!r}")

    entry_price = _require_positive_float(request, "entry_price")
    stop_loss = _require_positive_float(request, "stop_loss")
    risk_usd = _require_positive_float(request, "risk_usd")
    volume_lots = _require_positive_float(request, "volume_lots")

    if side == "BUY" and stop_loss >= entry_price:
        raise H024DemoOrderPlanError("BUY stop_loss must be below entry_price")
    if side == "SELL" and stop_loss <= entry_price:
        raise H024DemoOrderPlanError("SELL stop_loss must be above entry_price")

    source_timestamp = _require_str(request, "timestamp")
    source_reason = _require_str(request, "source_reason")
    if "WOULD_OPEN:" not in source_reason:
        raise H024DemoOrderPlanError("source_reason must contain WOULD_OPEN:")
    if "mode=log_only_no_execution" not in source_reason:
        raise H024DemoOrderPlanError(
            "source_reason must contain mode=log_only_no_execution"
        )

    return H024DemoOrderPlan(
        schema_version="h024_demo_order_plan_v1",
        plan_kind="PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY",
        source_schema_version=source_schema,
        source_request_kind=request_kind,
        symbol=symbol,
        normalized_symbol=normalized_symbol,
        timeframe=timeframe,
        side=side,
        entry_price=entry_price,
        stop_loss=stop_loss,
        volume_lots=volume_lots,
        risk_usd=risk_usd,
        source_timestamp=source_timestamp,
        source_reason=source_reason,
        account_server=context.server,
        account_currency=context.account_currency,
        account_balance=context.account_balance,
        account_equity=context.account_equity,
        broker=context.broker,
        account_login=context.account_login,
    )


def _coerce_account_context(
    account_context: H024DemoAccountContext | Mapping[str, Any],
) -> H024DemoAccountContext:
    if isinstance(account_context, H024DemoAccountContext):
        return account_context
    if not isinstance(account_context, Mapping):
        raise H024DemoOrderPlanError("account_context must be a mapping or dataclass")

    return H024DemoAccountContext(
        server=_coerce_nonempty_str(account_context.get("server"), "server"),
        account_currency=_coerce_nonempty_str(
            account_context.get("account_currency"), "account_currency"
        ),
        account_balance=_coerce_positive_float(
            account_context.get("account_balance"), "account_balance"
        ),
        account_equity=_coerce_positive_float(
            account_context.get("account_equity"), "account_equity"
        ),
        broker=_coerce_optional_str(account_context.get("broker")),
        account_login=_coerce_optional_str(account_context.get("account_login")),
    )


def _coerce_allowlist(
    allowed_demo_servers: set[str] | frozenset[str] | tuple[str, ...] | list[str] | None,
) -> frozenset[str]:
    if allowed_demo_servers is None:
        return DEFAULT_DEMO_SERVER_ALLOWLIST

    allowlist = frozenset(
        server.strip() for server in allowed_demo_servers if isinstance(server, str)
    )
    if not allowlist:
        raise H024DemoOrderPlanError("allowed_demo_servers must be non-empty")
    return allowlist


def _validate_account_context(
    context: H024DemoAccountContext,
    allowed_demo_servers: frozenset[str],
) -> None:
    server_lower = context.server.lower()
    if any(marker in server_lower for marker in _LIVE_LIKE_SERVER_MARKERS):
        raise H024DemoOrderPlanError("live-like server names are rejected")
    if context.server not in allowed_demo_servers:
        raise H024DemoOrderPlanError(
            f"server is not in the demo allowlist: {context.server!r}"
        )
    if context.account_currency != "USD":
        raise H024DemoOrderPlanError(
            f"unsupported account_currency: {context.account_currency!r}"
        )


def _require_str(request: Mapping[str, Any], key: str) -> str:
    return _coerce_nonempty_str(request.get(key), key)


def _require_positive_float(request: Mapping[str, Any], key: str) -> float:
    return _coerce_positive_float(request.get(key), key)


def _coerce_nonempty_str(value: Any, key: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise H024DemoOrderPlanError(f"{key} must be a non-empty string")
    return value.strip()


def _coerce_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise H024DemoOrderPlanError("optional string fields must be strings")
    stripped = value.strip()
    return stripped or None


def _coerce_positive_float(value: Any, key: str) -> float:
    try:
        coerced = float(value)
    except (TypeError, ValueError) as exc:
        raise H024DemoOrderPlanError(f"{key} must be numeric") from exc
    if coerced <= 0:
        raise H024DemoOrderPlanError(f"{key} must be positive")
    return coerced
