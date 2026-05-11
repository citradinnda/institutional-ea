from __future__ import annotations

from collections.abc import Iterable, Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from quantcore.execution.h024_order_intent_simulation import (
    ORDER_INTENT_SIMULATION_KIND,
    ORDER_INTENT_SIMULATION_SCHEMA,
    REVIEW_ONLY_MODE,
    verify_h024_order_intent_simulation_record,
)


MANUAL_APPROVAL_CHECKPOINT_SCHEMA = "h024_manual_approval_checkpoint_v1"
MANUAL_APPROVAL_CHECKPOINT_KIND = "MANUAL_APPROVAL_CHECKPOINT_REVIEW_ONLY"
APPROVAL_STATUS = "PENDING_MANUAL_APPROVAL"

REQUIRED_MANUAL_APPROVAL_ITEMS = (
    "confirm_h024_is_not_phase4_approved",
    "confirm_demo_order_placement_is_not_approved",
    "confirm_live_order_placement_is_not_approved",
    "confirm_no_execution_adapter_is_approved",
    "confirm_source_intent_fields_reviewed",
    "confirm_broker_metadata_and_risk_reviewed",
    "confirm_future_human_approval_required_before_any_execution_code",
)

FORBIDDEN_EXECUTION_KEYS = frozenset(
    {
        "ticket",
        "deal",
        "retcode",
        "broker_request",
        "mt5_request",
        "mql_trade_request",
        "mqltraderequest",
        "mql_trade_result",
        "mqltraderesult",
        "order_send",
        "ordersend",
        "order_check",
        "ordercheck",
        "order_send_result",
        "order_check_result",
        "position_ticket",
        "position_id",
        "deal_id",
    }
)


def build_h024_manual_approval_checkpoint(
    intent: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> dict[str, Any]:
    """Build a review-only manual approval checkpoint from a verified intent.

    This is not approval. It creates the artifact a human must inspect before
    any later, separately approved execution-adapter work could even be discussed.
    """

    violations: list[str] = []

    source_violations = verify_h024_order_intent_simulation_record(
        intent,
        allowed_demo_servers=allowed_demo_servers,
        expected_account_currency=expected_account_currency,
        max_risk_fraction=max_risk_fraction,
    )
    violations.extend(f"source_intent:{violation}" for violation in source_violations)

    forbidden_paths = _find_forbidden_execution_keys(intent)
    if forbidden_paths:
        violations.append("source_intent_contains_execution_like_fields:" + ",".join(forbidden_paths))

    if violations:
        return _failure_record(violations)

    extract_violations: list[str] = []
    server = _required_text(intent, ("server",), "server", extract_violations)
    account_currency = _required_text(intent, ("account_currency",), "account_currency", extract_violations)
    symbol = _required_text(intent, ("symbol",), "symbol", extract_violations)
    normalized_symbol = _required_text(intent, ("normalized_symbol",), "normalized_symbol", extract_violations)
    side = _required_text(intent, ("side",), "side", extract_violations)
    review_only_intent_action = _required_text(
        intent,
        ("review_only_intent_action",),
        "review_only_intent_action",
        extract_violations,
    )
    source_reason = _required_text(intent, ("source_reason",), "source_reason", extract_violations)
    source_timestamp = _required_text(intent, ("source_timestamp",), "source_timestamp", extract_violations)

    entry = _required_decimal(intent, ("entry",), "entry", extract_violations)
    stop = _required_decimal(intent, ("stop",), "stop", extract_violations)
    volume = _required_decimal(intent, ("volume",), "volume", extract_violations)
    risk_fraction = _required_decimal(intent, ("risk_fraction",), "risk_fraction", extract_violations)
    risk_usd = _required_decimal(intent, ("risk_usd",), "risk_usd", extract_violations)
    estimated_loss_usd = _required_decimal(intent, ("estimated_loss_usd",), "estimated_loss_usd", extract_violations)

    broker_metadata = intent.get("broker_metadata")
    if not isinstance(broker_metadata, Mapping):
        extract_violations.append("missing_broker_metadata")
        broker_metadata = {}

    tick_size = _required_decimal(intent, ("broker_metadata.tick_size",), "tick_size", extract_violations)
    tick_value = _required_decimal(intent, ("broker_metadata.tick_value",), "tick_value", extract_violations)
    min_volume = _required_decimal(intent, ("broker_metadata.min_volume",), "min_volume", extract_violations)
    max_volume = _required_decimal(intent, ("broker_metadata.max_volume",), "max_volume", extract_violations)
    volume_step = _required_decimal(intent, ("broker_metadata.volume_step",), "volume_step", extract_violations)
    volume_digits = _required_int(intent, ("broker_metadata.volume_digits",), "volume_digits", extract_violations)
    price_digits = _required_int(intent, ("broker_metadata.price_digits",), "price_digits", extract_violations)
    spread_points = _optional_decimal(intent, ("broker_metadata.spread_points",), "spread_points", extract_violations)

    if extract_violations:
        return _failure_record(extract_violations)

    assert server is not None
    assert account_currency is not None
    assert symbol is not None
    assert normalized_symbol is not None
    assert side is not None
    assert review_only_intent_action is not None
    assert source_reason is not None
    assert source_timestamp is not None
    assert entry is not None
    assert stop is not None
    assert volume is not None
    assert risk_fraction is not None
    assert risk_usd is not None
    assert estimated_loss_usd is not None
    assert tick_size is not None
    assert tick_value is not None
    assert min_volume is not None
    assert max_volume is not None
    assert volume_step is not None
    assert volume_digits is not None
    assert price_digits is not None

    return {
        "schema": MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
        "kind": MANUAL_APPROVAL_CHECKPOINT_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "approval_status": APPROVAL_STATUS,
        "manual_approval_required": True,
        "manual_approval_granted": False,
        "execution_approved": False,
        "is_broker_request": False,
        "source_intent_schema": ORDER_INTENT_SIMULATION_SCHEMA,
        "source_intent_kind": ORDER_INTENT_SIMULATION_KIND,
        "server": server,
        "account_currency": account_currency.upper(),
        "symbol": symbol,
        "normalized_symbol": normalized_symbol.upper(),
        "side": side.lower(),
        "review_only_intent_action": review_only_intent_action,
        "entry": _json_number(entry),
        "stop": _json_number(stop),
        "volume": _json_number(volume),
        "risk_fraction": _json_number(risk_fraction),
        "risk_usd": _json_number(risk_usd),
        "estimated_loss_usd": _json_number(estimated_loss_usd),
        "source_reason": source_reason,
        "source_timestamp": source_timestamp,
        "broker_metadata": {
            "tick_size": _json_number(tick_size),
            "tick_value": _json_number(tick_value),
            "min_volume": _json_number(min_volume),
            "max_volume": _json_number(max_volume),
            "volume_step": _json_number(volume_step),
            "volume_digits": volume_digits,
            "price_digits": price_digits,
            "spread_points": None if spread_points is None else _json_number(spread_points),
        },
        "required_manual_approval_items": list(REQUIRED_MANUAL_APPROVAL_ITEMS),
        "safety_checks": {
            "pure_python_review_only": True,
            "no_mt5_access": True,
            "no_broker_mutation": True,
            "no_broker_request_fields": True,
            "no_ticket_fields": True,
            "no_deal_fields": True,
            "no_result_fields": True,
            "no_execution_adapter_approved": True,
            "manual_approval_still_required": True,
        },
    }


def verify_h024_manual_approval_checkpoint_record(
    record: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> list[str]:
    """Independently verify a review-only manual approval checkpoint."""

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    max_risk = _as_decimal(max_risk_fraction, "max_risk_fraction", violations)

    if record.get("schema") != MANUAL_APPROVAL_CHECKPOINT_SCHEMA:
        violations.append(f"unexpected_schema:{record.get('schema')}")
    if record.get("kind") != MANUAL_APPROVAL_CHECKPOINT_KIND:
        violations.append(f"unexpected_kind:{record.get('kind')}")
    if str(record.get("verdict", "")).upper() != "PASS":
        violations.append(f"verdict_not_pass:{record.get('verdict')}")
    if record.get("violations") not in ([], ()):
        violations.append("record_has_violations")
    if record.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{record.get('mode')}")
    if record.get("approval_status") != APPROVAL_STATUS:
        violations.append(f"unexpected_approval_status:{record.get('approval_status')}")
    if record.get("manual_approval_required") is not True:
        violations.append("manual_approval_required_must_be_true")
    if record.get("manual_approval_granted") is not False:
        violations.append("manual_approval_granted_must_be_false")
    if record.get("execution_approved") is not False:
        violations.append("execution_approved_must_be_false")
    if record.get("is_broker_request") is not False:
        violations.append("is_broker_request_must_be_false")
    if record.get("source_intent_schema") != ORDER_INTENT_SIMULATION_SCHEMA:
        violations.append(f"unexpected_source_intent_schema:{record.get('source_intent_schema')}")
    if record.get("source_intent_kind") != ORDER_INTENT_SIMULATION_KIND:
        violations.append(f"unexpected_source_intent_kind:{record.get('source_intent_kind')}")

    forbidden_paths = _find_forbidden_execution_keys(record)
    if forbidden_paths:
        violations.append("record_contains_execution_like_fields:" + ",".join(forbidden_paths))

    required_items = record.get("required_manual_approval_items")
    if not isinstance(required_items, list):
        violations.append("missing_required_manual_approval_items")
    elif set(required_items) != set(REQUIRED_MANUAL_APPROVAL_ITEMS):
        violations.append("required_manual_approval_items_mismatch")

    safety_checks = record.get("safety_checks")
    if not isinstance(safety_checks, Mapping):
        violations.append("missing_safety_checks")
    else:
        for check_name in (
            "pure_python_review_only",
            "no_mt5_access",
            "no_broker_mutation",
            "no_broker_request_fields",
            "no_ticket_fields",
            "no_deal_fields",
            "no_result_fields",
            "no_execution_adapter_approved",
            "manual_approval_still_required",
        ):
            if safety_checks.get(check_name) is not True:
                violations.append(f"safety_check_not_true:{check_name}")

    server = _required_text(record, ("server",), "server", violations)
    account_currency = _required_text(record, ("account_currency",), "account_currency", violations)
    symbol = _required_text(record, ("symbol",), "symbol", violations)
    normalized_symbol = _required_text(record, ("normalized_symbol",), "normalized_symbol", violations)
    side = _required_text(record, ("side",), "side", violations)
    review_only_intent_action = _required_text(record, ("review_only_intent_action",), "review_only_intent_action", violations)

    entry = _required_decimal(record, ("entry",), "entry", violations)
    stop = _required_decimal(record, ("stop",), "stop", violations)
    volume = _required_decimal(record, ("volume",), "volume", violations)
    risk_fraction = _required_decimal(record, ("risk_fraction",), "risk_fraction", violations)
    risk_usd = _required_decimal(record, ("risk_usd",), "risk_usd", violations)
    estimated_loss_usd = _required_decimal(record, ("estimated_loss_usd",), "estimated_loss_usd", violations)

    tick_size = _required_decimal(record, ("broker_metadata.tick_size",), "tick_size", violations)
    tick_value = _required_decimal(record, ("broker_metadata.tick_value",), "tick_value", violations)
    min_volume = _required_decimal(record, ("broker_metadata.min_volume",), "min_volume", violations)
    max_volume = _required_decimal(record, ("broker_metadata.max_volume",), "max_volume", violations)
    volume_step = _required_decimal(record, ("broker_metadata.volume_step",), "volume_step", violations)
    volume_digits = _required_int(record, ("broker_metadata.volume_digits",), "volume_digits", violations)
    price_digits = _required_int(record, ("broker_metadata.price_digits",), "price_digits", violations)

    if violations:
        return sorted(set(violations))

    assert max_risk is not None
    assert server is not None
    assert account_currency is not None
    assert symbol is not None
    assert normalized_symbol is not None
    assert side is not None
    assert review_only_intent_action is not None
    assert entry is not None
    assert stop is not None
    assert volume is not None
    assert risk_fraction is not None
    assert risk_usd is not None
    assert estimated_loss_usd is not None
    assert tick_size is not None
    assert tick_value is not None
    assert min_volume is not None
    assert max_volume is not None
    assert volume_step is not None
    assert volume_digits is not None
    assert price_digits is not None

    if server not in allowed_servers:
        violations.append(f"server_not_allowed:{server}")
    if account_currency.upper() != expected_account_currency.upper():
        violations.append(f"unexpected_account_currency:{account_currency}")

    normalized_model_symbol = normalized_symbol.upper()
    if normalized_model_symbol not in {"USDJPY", "XAUUSD"}:
        violations.append(f"unsupported_normalized_symbol:{normalized_symbol}")
    if _normalize_runtime_symbol(symbol) != normalized_model_symbol:
        violations.append(f"symbol_normalization_mismatch:{symbol}")

    normalized_side = side.lower()
    if normalized_side not in {"long", "short"}:
        violations.append(f"unsupported_side:{side}")
    if normalized_side == "long" and review_only_intent_action != "BUY_MARKET_REVIEW_ONLY":
        violations.append("long_action_mismatch")
    if normalized_side == "short" and review_only_intent_action != "SELL_MARKET_REVIEW_ONLY":
        violations.append("short_action_mismatch")

    if normalized_side == "long" and stop >= entry:
        violations.append("invalid_long_stop_geometry")
    if normalized_side == "short" and stop <= entry:
        violations.append("invalid_short_stop_geometry")

    if tick_size <= 0:
        violations.append("tick_size_must_be_positive")
    if tick_value <= 0:
        violations.append("tick_value_must_be_positive")
    if min_volume <= 0:
        violations.append("min_volume_must_be_positive")
    if max_volume < min_volume:
        violations.append("max_volume_below_min_volume")
    if volume_step <= 0:
        violations.append("volume_step_must_be_positive")

    if tick_size > 0:
        if not _is_multiple(entry, tick_size):
            violations.append("entry_not_tick_aligned")
        if not _is_multiple(stop, tick_size):
            violations.append("stop_not_tick_aligned")
        recomputed_loss = (abs(entry - stop) / tick_size) * tick_value * volume
        if abs(recomputed_loss - estimated_loss_usd) > Decimal("0.00000001"):
            violations.append("estimated_loss_mismatch")
        if estimated_loss_usd > risk_usd + Decimal("0.00000001"):
            violations.append("estimated_loss_exceeds_risk_usd")

    if volume < min_volume:
        violations.append("volume_below_min_volume")
    if volume > max_volume:
        violations.append("volume_above_max_volume")
    if volume_step > 0 and not _is_multiple(volume - min_volume, volume_step):
        violations.append("volume_not_step_aligned")
    if _decimal_places(volume) > volume_digits:
        violations.append("volume_exceeds_volume_digits")
    if _decimal_places(entry) > price_digits:
        violations.append("entry_exceeds_price_digits")
    if _decimal_places(stop) > price_digits:
        violations.append("stop_exceeds_price_digits")
    if risk_fraction <= 0:
        violations.append("risk_fraction_must_be_positive")
    if risk_fraction > max_risk:
        violations.append("risk_fraction_exceeds_max_risk_fraction")

    return sorted(set(violations))


def _failure_record(violations: list[str]) -> dict[str, Any]:
    return {
        "schema": MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
        "kind": MANUAL_APPROVAL_CHECKPOINT_KIND,
        "verdict": "FAIL",
        "violations": sorted(set(violations)),
        "mode": REVIEW_ONLY_MODE,
        "approval_status": APPROVAL_STATUS,
        "manual_approval_required": True,
        "manual_approval_granted": False,
        "execution_approved": False,
        "is_broker_request": False,
    }


def _lookup(mapping: Mapping[str, Any], paths: Iterable[str]) -> Any | None:
    for path in paths:
        current: Any = mapping
        found = True
        for part in path.split("."):
            if isinstance(current, Mapping) and part in current:
                current = current[part]
            else:
                found = False
                break
        if found and current is not None:
            return current
    return None


def _required_text(
    mapping: Mapping[str, Any],
    paths: Iterable[str],
    field_name: str,
    violations: list[str],
) -> str | None:
    value = _lookup(mapping, paths)
    if value is None or str(value).strip() == "":
        violations.append(f"missing_{field_name}")
        return None
    return str(value).strip()


def _required_decimal(
    mapping: Mapping[str, Any],
    paths: Iterable[str],
    field_name: str,
    violations: list[str],
) -> Decimal | None:
    return _as_decimal(_lookup(mapping, paths), field_name, violations)


def _optional_decimal(
    mapping: Mapping[str, Any],
    paths: Iterable[str],
    field_name: str,
    violations: list[str],
) -> Decimal | None:
    value = _lookup(mapping, paths)
    if value is None or value == "":
        return None
    return _as_decimal(value, field_name, violations)


def _required_int(
    mapping: Mapping[str, Any],
    paths: Iterable[str],
    field_name: str,
    violations: list[str],
) -> int | None:
    decimal_value = _required_decimal(mapping, paths, field_name, violations)
    if decimal_value is None:
        return None
    if decimal_value != decimal_value.to_integral_value():
        violations.append(f"{field_name}_must_be_integer")
        return None
    return int(decimal_value)


def _as_decimal(value: Any, field_name: str, violations: list[str]) -> Decimal | None:
    if value is None or isinstance(value, bool):
        violations.append(f"missing_or_invalid_{field_name}")
        return None
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError):
        violations.append(f"missing_or_invalid_{field_name}")
        return None
    if not decimal_value.is_finite():
        violations.append(f"non_finite_{field_name}")
        return None
    return decimal_value


def _normalize_runtime_symbol(symbol: str) -> str:
    upper = symbol.upper()
    if upper.startswith("USDJPY"):
        return "USDJPY"
    if upper.startswith("XAUUSD"):
        return "XAUUSD"
    return upper


def _is_multiple(value: Decimal, quantum: Decimal) -> bool:
    if quantum <= 0:
        return False
    quotient = value / quantum
    return quotient == quotient.to_integral_value()


def _decimal_places(value: Decimal) -> int:
    normalized = value.normalize()
    return max(0, -normalized.as_tuple().exponent)


def _json_number(value: Decimal) -> int | float:
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def _find_forbidden_execution_keys(value: Any, prefix: str = "") -> list[str]:
    forbidden_normalized = {_normalize_key(key) for key in FORBIDDEN_EXECUTION_KEYS}
    found: list[str] = []
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key)
            path = f"{prefix}.{key}" if prefix else key
            if _normalize_key(key) in forbidden_normalized:
                found.append(path)
            found.extend(_find_forbidden_execution_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            path = f"{prefix}[{index}]"
            found.extend(_find_forbidden_execution_keys(child, path))
    return found


def _normalize_key(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())