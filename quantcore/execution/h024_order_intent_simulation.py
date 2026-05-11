from __future__ import annotations

from collections.abc import Iterable, Mapping
from decimal import Decimal, InvalidOperation
from typing import Any


PREFLIGHT_SCHEMA = "h024_broker_metadata_preflight_v1"
PREFLIGHT_KIND = "BROKER_METADATA_PREFLIGHT_REVIEW_ONLY"

ORDER_INTENT_SIMULATION_SCHEMA = "h024_order_intent_simulation_v1"
ORDER_INTENT_SIMULATION_KIND = "ORDER_INTENT_SIMULATION_REVIEW_ONLY"

REVIEW_ONLY_MODE = "log_only_no_execution"
SUPPORTED_NORMALIZED_SYMBOLS = frozenset({"USDJPY", "XAUUSD"})
SUPPORTED_SIDES = frozenset({"long", "short"})
SIDE_ALIASES = {
    "long": "long",
    "buy": "long",
    "buymarket": "long",
    "short": "short",
    "sell": "short",
    "sellmarket": "short",
}

FORBIDDEN_EXECUTION_KEYS = frozenset(
    {
        "ticket",
        "deal",
        "result",
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

LOOKUP_ALIASES = {
    "schema": (
        "preflight_schema",
        "record_schema",
        "artifact_schema",
        "broker_metadata_preflight_schema",
        "preflight_record_schema",
    ),
    "kind": (
        "preflight_kind",
        "record_kind",
        "artifact_kind",
        "record_type",
        "preflight_record_type",
        "broker_metadata_preflight_kind",
    ),
    "server": ("account_server", "demo_server", "account_server_name", "server_name"),
    "account_currency": ("currency", "account_currency_code", "deposit_currency"),
    "symbol": ("runtime_symbol", "broker_symbol", "mt5_symbol", "instrument", "instrument_symbol"),
    "normalized_symbol": ("model_symbol", "base_symbol", "canonical_symbol", "normalized_runtime_symbol"),
    "entry": (
        "entry_price",
        "proposed_entry",
        "planned_entry",
        "intent_entry",
        "plan_entry",
        "entry_price_open",
    ),
    "stop": (
        "stop_loss",
        "stop_price",
        "sl",
        "proposed_stop",
        "planned_stop",
        "intent_stop",
        "plan_stop",
    ),
    "volume": (
        "lots",
        "final_lots",
        "volume_lots",
        "final_volume",
        "final_volume_lots",
        "planned_volume",
        "planned_lots",
        "proposed_volume",
        "proposed_lots",
        "proposed_volume_lots",
        "intent_volume",
        "intent_lots",
        "lot_size",
        "quantity_lots",
        "request_volume",
        "request_lots",
    ),
    "risk_fraction": (
        "final_risk_fraction",
        "signed_risk_fraction",
        "risk_fraction_final",
        "final_signed_risk_fraction",
        "signed_final_risk_fraction",
        "abs_risk_fraction",
        "risk_fraction_abs",
        "effective_risk_fraction",
        "proposed_risk_fraction",
        "plan_risk_fraction",
        "intent_risk_fraction",
        "risk_frac",
    ),
    "risk_usd": (
        "risk_amount_usd",
        "risk_amount",
        "intended_risk_usd",
        "proposed_risk_usd",
        "planned_risk_usd",
        "intent_risk_usd",
    ),
    "source_reason": (
        "reason",
        "runtime_reason",
        "intended_action_reason",
        "source_runtime_reason",
        "would_open_reason",
    ),
    "source_timestamp": (
        "runtime_timestamp",
        "log_timestamp",
        "source_time",
        "timestamp",
        "source_runtime_timestamp",
        "intended_action_timestamp",
    ),
    "tick_value": ("tick_value_usd_per_lot", "trade_tick_value", "tick_value_usd"),
    "min_volume": ("volume_min", "lot_min", "min_lots"),
    "max_volume": ("volume_max", "lot_max", "max_lots"),
    "volume_step": ("lot_step", "volume_increment"),
    "account_balance": ("balance", "account_balance_usd", "source_account_balance", "runtime_account_balance"),
}



def build_h024_order_intent_simulation(
    preflight: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> dict[str, Any]:
    """Build a final review-only H024 order-intent simulation artifact.

    This function is deliberately pure Python and has no MT5 imports, no broker calls,
    no terminal access, and no execution-side effects.
    """

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    max_risk = _as_decimal(max_risk_fraction, "max_risk_fraction", violations)

    schema = _find_expected_token(
        preflight,
        PREFLIGHT_SCHEMA,
        (
            "schema",
            "preflight_schema",
            "record_schema",
            "artifact_schema",
            "broker_metadata_preflight_schema",
            "preflight_record_schema",
        ),
    )
    kind = _find_expected_token(
        preflight,
        PREFLIGHT_KIND,
        (
            "kind",
            "preflight_kind",
            "record_kind",
            "artifact_kind",
            "record_type",
            "preflight_record_type",
            "broker_metadata_preflight_kind",
        ),
    )

    raw_schema = _lookup(
        preflight,
        (
            "schema",
            "preflight_schema",
            "record_schema",
            "artifact_schema",
            "broker_metadata_preflight_schema",
            "preflight_record_schema",
        ),
    )
    raw_kind = _lookup(
        preflight,
        (
            "kind",
            "preflight_kind",
            "record_kind",
            "artifact_kind",
            "record_type",
            "preflight_record_type",
            "broker_metadata_preflight_kind",
        ),
    )

    if schema is None:
        if raw_schema is None:
            violations.append("missing_preflight_schema")
        else:
            violations.append(f"unexpected_preflight_schema:{raw_schema}")
    if kind is None:
        if raw_kind is None:
            violations.append("missing_preflight_kind")
        else:
            violations.append(f"unexpected_preflight_kind:{raw_kind}")

    preflight_verdict = _lookup(preflight, ("verdict", "preflight_verdict", "status"))
    if preflight_verdict is not None and str(preflight_verdict).upper() != "PASS":
        violations.append(f"preflight_verdict_not_pass:{preflight_verdict}")

    preflight_violations = _lookup(preflight, ("violations", "preflight_violations", "violation_list"))
    if preflight_violations not in (None, [], (), "", 0):
        violations.append("preflight_has_violations")

    forbidden_paths = _find_forbidden_execution_keys(preflight)
    if forbidden_paths:
        violations.append("preflight_contains_execution_like_fields:" + ",".join(forbidden_paths))

    server = _required_text(
        preflight,
        (
            "server",
            "account_server",
            "account.server",
            "plan.server",
            "proposed_plan.server",
            "demo_order_plan.server",
            "metadata.server",
            "broker_metadata.server",
        ),
        "server",
        violations,
    )
    account_currency = _required_text(
        preflight,
        (
            "account_currency",
            "currency",
            "account.currency",
            "plan.account_currency",
            "proposed_plan.account_currency",
            "demo_order_plan.account_currency",
            "metadata.account_currency",
            "broker_metadata.account_currency",
        ),
        "account_currency",
        violations,
    )
    mode = _required_text(
        preflight,
        (
            "mode",
            "plan.mode",
            "proposed_plan.mode",
            "demo_order_plan.mode",
        ),
        "mode",
        violations,
    )

    symbol = _required_text(
        preflight,
        (
            "symbol",
            "plan.symbol",
            "proposed_plan.symbol",
            "demo_order_plan.symbol",
        ),
        "symbol",
        violations,
    )
    normalized_symbol = _required_text(
        preflight,
        (
            "normalized_symbol",
            "model_symbol",
            "plan.normalized_symbol",
            "plan.model_symbol",
            "proposed_plan.normalized_symbol",
            "demo_order_plan.normalized_symbol",
            "metadata.normalized_symbol",
            "broker_metadata.normalized_symbol",
        ),
        "normalized_symbol",
        violations,
    )
    side = _required_text(
        preflight,
        (
            "side",
            "plan.side",
            "proposed_plan.side",
            "demo_order_plan.side",
        ),
        "side",
        violations,
    )

    source_reason = _required_text(
        preflight,
        (
            "source_reason",
            "reason",
            "source.reason",
            "plan.source_reason",
            "plan.reason",
            "proposed_plan.source_reason",
            "demo_order_plan.source_reason",
        ),
        "source_reason",
        violations,
    )
    source_timestamp = _required_text(
        preflight,
        (
            "source_timestamp",
            "runtime_timestamp",
            "timestamp",
            "source.timestamp",
            "plan.source_timestamp",
            "plan.runtime_timestamp",
            "proposed_plan.source_timestamp",
            "demo_order_plan.source_timestamp",
        ),
        "source_timestamp",
        violations,
    )

    entry = _required_decimal(
        preflight,
        (
            "entry",
            "entry_price",
            "plan.entry",
            "plan.entry_price",
            "proposed_plan.entry",
            "demo_order_plan.entry",
        ),
        "entry",
        violations,
    )
    stop = _required_decimal(
        preflight,
        (
            "stop",
            "stop_loss",
            "stop_price",
            "plan.stop",
            "plan.stop_loss",
            "proposed_plan.stop",
            "demo_order_plan.stop",
        ),
        "stop",
        violations,
    )
    volume = _required_decimal(
        preflight,
        (
            "volume",
            "lots",
            "final_lots",
            "plan.volume",
            "plan.lots",
            "plan.final_lots",
            "proposed_plan.volume",
            "demo_order_plan.volume",
        ),
        "volume",
        violations,
    )
    risk_fraction_errors: list[str] = []
    risk_fraction = _required_decimal(
        preflight,
        (
            "risk_fraction",
            "final_risk_fraction",
            "signed_risk_fraction",
            "risk_fraction_final",
            "final_signed_risk_fraction",
            "plan.risk_fraction",
            "plan.final_risk_fraction",
            "proposed_plan.risk_fraction",
            "demo_order_plan.risk_fraction",
        ),
        "risk_fraction",
        risk_fraction_errors,
    )
    risk_usd = _required_decimal(
        preflight,
        (
            "risk_usd",
            "risk_amount_usd",
            "risk_amount",
            "intended_risk_usd",
            "plan.risk_usd",
            "plan.risk_amount_usd",
            "proposed_plan.risk_usd",
            "demo_order_plan.risk_usd",
        ),
        "risk_usd",
        violations,
    )
    if risk_fraction is None:
        account_balance = _optional_decimal(
            preflight,
            (
                "account_balance",
                "account_balance_usd",
                "balance",
                "source_account_balance",
                "runtime_account_balance",
                "plan.account_balance",
                "plan.account_balance_usd",
                "proposed_plan.account_balance",
                "demo_order_plan.account_balance",
            ),
            "account_balance",
            [],
        )
        if account_balance is not None and account_balance > 0 and risk_usd is not None:
            risk_fraction = abs(risk_usd / account_balance)
        else:
            violations.extend(risk_fraction_errors)

    tick_size = _required_decimal(
        preflight,
        (
            "tick_size",
            "metadata.tick_size",
            "broker_metadata.tick_size",
        ),
        "tick_size",
        violations,
    )
    tick_value = _required_decimal(
        preflight,
        (
            "tick_value",
            "tick_value_usd_per_lot",
            "metadata.tick_value",
            "metadata.tick_value_usd_per_lot",
            "broker_metadata.tick_value",
            "broker_metadata.tick_value_usd_per_lot",
        ),
        "tick_value",
        violations,
    )
    min_volume = _required_decimal(
        preflight,
        (
            "min_volume",
            "volume_min",
            "metadata.min_volume",
            "metadata.volume_min",
            "broker_metadata.min_volume",
            "broker_metadata.volume_min",
        ),
        "min_volume",
        violations,
    )
    max_volume = _required_decimal(
        preflight,
        (
            "max_volume",
            "volume_max",
            "metadata.max_volume",
            "metadata.volume_max",
            "broker_metadata.max_volume",
            "broker_metadata.volume_max",
        ),
        "max_volume",
        violations,
    )
    volume_step = _required_decimal(
        preflight,
        (
            "volume_step",
            "metadata.volume_step",
            "broker_metadata.volume_step",
        ),
        "volume_step",
        violations,
    )
    volume_digits = _required_int(
        preflight,
        (
            "volume_digits",
            "metadata.volume_digits",
            "broker_metadata.volume_digits",
        ),
        "volume_digits",
        violations,
    )
    price_digits = _required_int(
        preflight,
        (
            "price_digits",
            "metadata.price_digits",
            "broker_metadata.price_digits",
        ),
        "price_digits",
        violations,
    )
    spread_points = _optional_decimal(
        preflight,
        (
            "spread_points",
            "metadata.spread_points",
            "broker_metadata.spread_points",
        ),
        "spread_points",
        violations,
    )

    if violations:
        return _failure_record(violations)

    assert max_risk is not None
    assert schema is not None
    assert kind is not None
    assert server is not None
    assert account_currency is not None
    assert mode is not None
    assert symbol is not None
    assert normalized_symbol is not None
    assert side is not None
    assert source_reason is not None
    assert source_timestamp is not None
    assert entry is not None
    assert stop is not None
    assert volume is not None
    assert risk_fraction is not None
    assert risk_usd is not None
    assert tick_size is not None
    assert tick_value is not None
    assert min_volume is not None
    assert max_volume is not None
    assert volume_step is not None
    assert volume_digits is not None
    assert price_digits is not None

    normalized_side = _canonical_side(side)
    normalized_currency = account_currency.upper()
    expected_currency = expected_account_currency.upper()
    normalized_model_symbol = normalized_symbol.upper()
    normalized_runtime_symbol = _normalize_runtime_symbol(symbol)

    if server not in allowed_servers:
        violations.append(f"server_not_allowed:{server}")

    if normalized_currency != expected_currency:
        violations.append(f"unexpected_account_currency:{account_currency}")

    if mode != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{mode}")

    if normalized_model_symbol not in SUPPORTED_NORMALIZED_SYMBOLS:
        violations.append(f"unsupported_normalized_symbol:{normalized_symbol}")

    if normalized_runtime_symbol != normalized_model_symbol:
        violations.append(f"symbol_normalization_mismatch:{symbol}->{normalized_runtime_symbol}!={normalized_model_symbol}")

    if normalized_side not in SUPPORTED_SIDES:
        violations.append(f"unsupported_side:{side}")

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
    if volume <= 0:
        violations.append("volume_must_be_positive")
    if risk_usd <= 0:
        violations.append("risk_usd_must_be_positive")
    if risk_fraction <= 0:
        violations.append("risk_fraction_must_be_positive")
    if max_risk <= 0:
        violations.append("max_risk_fraction_must_be_positive")

    if normalized_side == "long" and stop >= entry:
        violations.append("invalid_long_stop_geometry")
    if normalized_side == "short" and stop <= entry:
        violations.append("invalid_short_stop_geometry")

    if tick_size > 0:
        if not _is_multiple(entry, tick_size):
            violations.append("entry_not_tick_aligned")
        if not _is_multiple(stop, tick_size):
            violations.append("stop_not_tick_aligned")

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

    estimated_loss_usd = (abs(entry - stop) / tick_size) * tick_value * volume if tick_size > 0 else Decimal("NaN")

    if estimated_loss_usd.is_finite() and estimated_loss_usd > risk_usd + Decimal("0.00000001"):
        violations.append("estimated_loss_exceeds_risk_usd")

    if risk_fraction > max_risk:
        violations.append("risk_fraction_exceeds_max_risk_fraction")

    if violations:
        return _failure_record(violations)

    review_only_intent_action = "BUY_MARKET_REVIEW_ONLY" if normalized_side == "long" else "SELL_MARKET_REVIEW_ONLY"

    return {
        "schema": ORDER_INTENT_SIMULATION_SCHEMA,
        "kind": ORDER_INTENT_SIMULATION_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "is_broker_request": False,
        "execution_approved": False,
        "preflight_schema": PREFLIGHT_SCHEMA,
        "preflight_kind": PREFLIGHT_KIND,
        "source_preflight_schema": schema,
        "source_preflight_kind": kind,
        "server": server,
        "account_currency": normalized_currency,
        "symbol": symbol,
        "normalized_symbol": normalized_model_symbol,
        "side": normalized_side,
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
        "safety_checks": {
            "pure_python_review_only": True,
            "no_mt5_access": True,
            "no_broker_mutation": True,
            "no_broker_request_fields": True,
            "no_ticket_fields": True,
            "no_deal_fields": True,
            "no_result_fields": True,
            "manual_approval_still_required": True,
        },
    }


def verify_h024_order_intent_simulation_record(
    record: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> list[str]:
    """Independently verify a review-only order-intent simulation record."""

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    max_risk = _as_decimal(max_risk_fraction, "max_risk_fraction", violations)

    if record.get("schema") != ORDER_INTENT_SIMULATION_SCHEMA:
        violations.append(f"unexpected_schema:{record.get('schema')}")
    if record.get("kind") != ORDER_INTENT_SIMULATION_KIND:
        violations.append(f"unexpected_kind:{record.get('kind')}")
    if str(record.get("verdict", "")).upper() != "PASS":
        violations.append(f"verdict_not_pass:{record.get('verdict')}")
    if record.get("violations") not in ([], ()):
        violations.append("record_has_violations")
    if record.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{record.get('mode')}")
    if record.get("is_broker_request") is not False:
        violations.append("is_broker_request_must_be_false")
    if record.get("execution_approved") is not False:
        violations.append("execution_approved_must_be_false")
    if record.get("preflight_schema") != PREFLIGHT_SCHEMA:
        violations.append(f"unexpected_preflight_schema:{record.get('preflight_schema')}")
    if record.get("preflight_kind") != PREFLIGHT_KIND:
        violations.append(f"unexpected_preflight_kind:{record.get('preflight_kind')}")

    forbidden_paths = _find_forbidden_execution_keys(record)
    if forbidden_paths:
        violations.append("record_contains_execution_like_fields:" + ",".join(forbidden_paths))

    server = _required_text(record, ("server",), "server", violations)
    account_currency = _required_text(record, ("account_currency",), "account_currency", violations)
    symbol = _required_text(record, ("symbol",), "symbol", violations)
    normalized_symbol = _required_text(record, ("normalized_symbol",), "normalized_symbol", violations)
    side = _required_text(record, ("side",), "side", violations)
    review_only_intent_action = _required_text(record, ("review_only_intent_action",), "review_only_intent_action", violations)
    source_reason = _required_text(record, ("source_reason",), "source_reason", violations)
    source_timestamp = _required_text(record, ("source_timestamp",), "source_timestamp", violations)

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
            "manual_approval_still_required",
        ):
            if safety_checks.get(check_name) is not True:
                violations.append(f"safety_check_not_true:{check_name}")

    if violations:
        return sorted(set(violations))

    assert max_risk is not None
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

    normalized_side = _canonical_side(side)
    normalized_model_symbol = normalized_symbol.upper()

    if server not in allowed_servers:
        violations.append(f"server_not_allowed:{server}")
    if account_currency.upper() != expected_account_currency.upper():
        violations.append(f"unexpected_account_currency:{account_currency}")
    if normalized_model_symbol not in SUPPORTED_NORMALIZED_SYMBOLS:
        violations.append(f"unsupported_normalized_symbol:{normalized_symbol}")
    if _normalize_runtime_symbol(symbol) != normalized_model_symbol:
        violations.append(f"symbol_normalization_mismatch:{symbol}")
    if normalized_side not in SUPPORTED_SIDES:
        violations.append(f"unsupported_side:{side}")
    if normalized_side == "long" and review_only_intent_action != "BUY_MARKET_REVIEW_ONLY":
        violations.append("long_action_mismatch")
    if normalized_side == "short" and review_only_intent_action != "SELL_MARKET_REVIEW_ONLY":
        violations.append("short_action_mismatch")

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
    if volume <= 0:
        violations.append("volume_must_be_positive")
    if risk_fraction <= 0:
        violations.append("risk_fraction_must_be_positive")
    if risk_usd <= 0:
        violations.append("risk_usd_must_be_positive")

    if normalized_side == "long" and stop >= entry:
        violations.append("invalid_long_stop_geometry")
    if normalized_side == "short" and stop <= entry:
        violations.append("invalid_short_stop_geometry")

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

    if risk_fraction > max_risk:
        violations.append("risk_fraction_exceeds_max_risk_fraction")

    return sorted(set(violations))


def _failure_record(violations: list[str]) -> dict[str, Any]:
    return {
        "schema": ORDER_INTENT_SIMULATION_SCHEMA,
        "kind": ORDER_INTENT_SIMULATION_KIND,
        "verdict": "FAIL",
        "violations": sorted(set(violations)),
        "mode": REVIEW_ONLY_MODE,
        "is_broker_request": False,
        "execution_approved": False,
    }


def _find_expected_token(mapping: Mapping[str, Any], expected: str, paths: Iterable[str]) -> str | None:
    direct_value = _lookup(mapping, paths)
    if direct_value is not None and _token_matches_expected(str(direct_value), expected):
        return str(direct_value)

    def walk(value: Any) -> str | None:
        if isinstance(value, Mapping):
            for child in value.values():
                found = walk(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = walk(child)
                if found is not None:
                    return found
        elif value is not None and not isinstance(value, bool):
            text_value = str(value).strip()
            if _token_matches_expected(text_value, expected):
                return text_value
        return None

    return walk(mapping)


def _token_matches_expected(value: str, expected: str) -> bool:
    normalized_value = _normalize_key(value)
    normalized_expected = _normalize_key(expected)
    return (
        normalized_value == normalized_expected
        or normalized_value.endswith(normalized_expected)
        or normalized_expected in normalized_value
    )


def _lookup(mapping: Mapping[str, Any], paths: Iterable[str]) -> Any | None:
    path_list = list(paths)

    # First try explicit dotted paths, preserving caller priority.
    for path in path_list:
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

    # Then try a recursive alias search.  This keeps the contract resilient to
    # harmless report-layout changes while still requiring semantically named
    # fields in the verified upstream artifact.
    candidate_keys: list[str] = []
    for path in path_list:
        leaf = path.split(".")[-1]
        candidate_keys.append(leaf)
        candidate_keys.extend(LOOKUP_ALIASES.get(leaf, ()))

    normalized_candidates = {_normalize_key(key) for key in candidate_keys}

    def walk(value: Any) -> Any | None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                if _normalize_key(str(key)) in normalized_candidates and child is not None:
                    return child
            for child in value.values():
                found_value = walk(child)
                if found_value is not None:
                    return found_value
        elif isinstance(value, list):
            for child in value:
                found_value = walk(child)
                if found_value is not None:
                    return found_value
        return None

    return walk(mapping)


def _normalize_key(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())



def _required_text(
    mapping: Mapping[str, Any],
    paths: Iterable[str],
    field_name: str,
    violations: list[str],
) -> str | None:
    value = _lookup(mapping, paths)
    if value is None or str(value).strip() == "":
        if field_name == "mode":
            # Older verified preflight report layouts may prove the mode through
            # their PASS verdict and schema/kind while not carrying the raw mode
            # field forward. The downstream artifact still remains explicitly
            # review-only and non-executing.
            verdict_value = _lookup(mapping, ("verdict", "preflight_verdict", "status"))
            violation_value = _lookup(mapping, ("violations", "preflight_violations", "violation_list"))
            schema_value = _find_expected_token(
                mapping,
                PREFLIGHT_SCHEMA,
                (
                    "schema",
                    "preflight_schema",
                    "record_schema",
                    "artifact_schema",
                    "broker_metadata_preflight_schema",
                    "preflight_record_schema",
                ),
            )
            kind_value = _find_expected_token(
                mapping,
                PREFLIGHT_KIND,
                (
                    "kind",
                    "preflight_kind",
                    "record_kind",
                    "artifact_kind",
                    "record_type",
                    "preflight_record_type",
                    "broker_metadata_preflight_kind",
                ),
            )
            verdict_ok = verdict_value is None or str(verdict_value).upper() == "PASS"
            violations_ok = violation_value in (None, [], (), "", 0)
            if schema_value is not None and kind_value is not None and verdict_ok and violations_ok:
                return REVIEW_ONLY_MODE
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


def _canonical_side(side: str) -> str:
    return SIDE_ALIASES.get(_normalize_key(side), side.lower())


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
    found: list[str] = []
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key)
            key_lower = key.lower()
            path = f"{prefix}.{key}" if prefix else key
            if key_lower in FORBIDDEN_EXECUTION_KEYS:
                found.append(path)
            found.extend(_find_forbidden_execution_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            path = f"{prefix}[{index}]"
            found.extend(_find_forbidden_execution_keys(child, path))
    return found