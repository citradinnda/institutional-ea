from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal, InvalidOperation
from typing import Any

from quantcore.execution.h024_execution_safety_controls import (
    IDEMPOTENCY_LEDGER_SCHEMA,
    KILL_SWITCH_STATE_SCHEMA,
    compute_h024_stable_intent_id,
)
from quantcore.execution.h024_execution_safety_controls_design import (
    DESIGN_STATUS as SAFETY_CONTROLS_DESIGN_STATUS,
    EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
    EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
    verify_h024_execution_safety_controls_design_record,
)
from quantcore.execution.h024_order_intent_simulation import REVIEW_ONLY_MODE


OPERATOR_CONTROL_STATE_SNAPSHOT_SCHEMA = "h024_operator_control_state_snapshot_v1"
OPERATOR_CONTROL_STATE_SNAPSHOT_KIND = "OPERATOR_CONTROL_STATE_SNAPSHOT_REVIEW_ONLY"
SNAPSHOT_STATUS = "ALLOW_STATE_REVIEW_ONLY_NOT_EXECUTION_APPROVAL"

FORBIDDEN_EXECUTION_KEYS = frozenset(
    {
        "ticket",
        "deal",
        "retcode",
        "broker_request",
        "brokerrequest",
        "mt5_request",
        "mt5request",
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
        "positionticket",
        "positionid",
        "deal_id",
        "dealid",
    }
)


def build_h024_operator_control_state_snapshot(
    safety_controls_design: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
    max_orders_per_session: int = 1,
    orders_this_session: int = 0,
    daily_loss_limit_usd: Decimal | str | float = Decimal("1000"),
    realized_loss_today_usd: Decimal | str | float = Decimal("0"),
    pending_intent_ids: Sequence[str] | None = None,
    completed_intent_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Build explicit operator control-state artifacts for review-only preflight.

    This snapshot supplies allow-state for the pure-Python safety controls. It
    does not approve Phase 4, execution, adapter implementation, demo orders, or
    live orders.
    """

    violations: list[str] = []

    source_violations = verify_h024_execution_safety_controls_design_record(
        safety_controls_design,
        allowed_demo_servers=allowed_demo_servers,
        expected_account_currency=expected_account_currency,
        max_risk_fraction=max_risk_fraction,
    )
    violations.extend(f"source_safety_controls_design:{violation}" for violation in source_violations)

    forbidden_paths = _find_forbidden_execution_keys(safety_controls_design)
    if forbidden_paths:
        violations.append("source_safety_controls_design_contains_execution_like_fields:" + ",".join(forbidden_paths))

    source_chain = safety_controls_design.get("source_chain_summary")
    if not isinstance(source_chain, Mapping):
        violations.append("missing_source_chain_summary")
        source_chain = {}

    extract_violations: list[str] = []
    server = _required_text(source_chain, ("server",), "server", extract_violations)
    account_currency = _required_text(source_chain, ("account_currency",), "account_currency", extract_violations)
    symbol = _required_text(source_chain, ("symbol",), "symbol", extract_violations)
    normalized_symbol = _required_text(source_chain, ("normalized_symbol",), "normalized_symbol", extract_violations)
    side = _required_text(source_chain, ("side",), "side", extract_violations)
    review_only_intent_action = _required_text(
        source_chain,
        ("review_only_intent_action",),
        "review_only_intent_action",
        extract_violations,
    )
    source_timestamp = _required_text(source_chain, ("source_timestamp",), "source_timestamp", extract_violations)
    source_reason = _required_text(source_chain, ("source_reason",), "source_reason", extract_violations)
    risk_fraction = _required_decimal(source_chain, ("risk_fraction",), "risk_fraction", extract_violations)
    risk_usd = _required_decimal(source_chain, ("risk_usd",), "risk_usd", extract_violations)
    estimated_loss_usd = _required_decimal(source_chain, ("estimated_loss_usd",), "estimated_loss_usd", extract_violations)
    daily_loss_limit = _as_decimal(daily_loss_limit_usd, "daily_loss_limit_usd", extract_violations)
    realized_loss_today = _as_decimal(realized_loss_today_usd, "realized_loss_today_usd", extract_violations)

    if not isinstance(max_orders_per_session, int) or isinstance(max_orders_per_session, bool):
        extract_violations.append("max_orders_per_session_must_be_integer")
    elif max_orders_per_session <= 0:
        extract_violations.append("max_orders_per_session_must_be_positive")

    if not isinstance(orders_this_session, int) or isinstance(orders_this_session, bool):
        extract_violations.append("orders_this_session_must_be_integer")
    elif orders_this_session < 0:
        extract_violations.append("orders_this_session_must_be_non_negative")
    elif isinstance(max_orders_per_session, int) and not isinstance(max_orders_per_session, bool) and orders_this_session >= max_orders_per_session:
        extract_violations.append("orders_this_session_must_be_below_max_orders_per_session")

    pending_ids = _as_string_list(list(pending_intent_ids or ()), "pending_intent_ids", extract_violations)
    completed_ids = _as_string_list(list(completed_intent_ids or ()), "completed_intent_ids", extract_violations)

    violations.extend(extract_violations)

    if violations:
        return _failure_record(violations)

    assert server is not None
    assert account_currency is not None
    assert symbol is not None
    assert normalized_symbol is not None
    assert side is not None
    assert review_only_intent_action is not None
    assert source_timestamp is not None
    assert source_reason is not None
    assert risk_fraction is not None
    assert risk_usd is not None
    assert estimated_loss_usd is not None
    assert daily_loss_limit is not None
    assert realized_loss_today is not None
    assert pending_ids is not None
    assert completed_ids is not None

    source_chain_summary = {
        "strategy": "H024",
        "server": server,
        "account_currency": account_currency.upper(),
        "symbol": symbol,
        "normalized_symbol": normalized_symbol.upper(),
        "side": side.lower(),
        "review_only_intent_action": review_only_intent_action,
        "risk_fraction": _json_number(risk_fraction),
        "risk_usd": _json_number(risk_usd),
        "estimated_loss_usd": _json_number(estimated_loss_usd),
        "source_timestamp": source_timestamp,
        "source_reason": source_reason,
    }

    stable_intent_id = compute_h024_stable_intent_id(source_chain_summary)

    kill_switch_state = {
        "schema": KILL_SWITCH_STATE_SCHEMA,
        "global_enabled": True,
        "strategy_enabled": {"H024": True},
        "symbol_enabled": {normalized_symbol.upper(): True},
        "max_orders_per_session": max_orders_per_session,
        "orders_this_session": orders_this_session,
        "daily_loss_limit_usd": _json_number(daily_loss_limit),
        "realized_loss_today_usd": _json_number(realized_loss_today),
    }

    idempotency_ledger = {
        "schema": IDEMPOTENCY_LEDGER_SCHEMA,
        "pending_intent_ids": pending_ids,
        "completed_intent_ids": completed_ids,
    }

    return {
        "schema": OPERATOR_CONTROL_STATE_SNAPSHOT_SCHEMA,
        "kind": OPERATOR_CONTROL_STATE_SNAPSHOT_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "snapshot_status": SNAPSHOT_STATUS,
        "source_safety_controls_design_schema": EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
        "source_safety_controls_design_kind": EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
        "source_safety_controls_design_status": SAFETY_CONTROLS_DESIGN_STATUS,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "stable_intent_id": stable_intent_id,
        "source_chain_summary": source_chain_summary,
        "kill_switch_state": kill_switch_state,
        "idempotency_ledger": idempotency_ledger,
        "snapshot_boundary": {
            "pure_python_review_only": True,
            "operator_control_state_only": True,
            "not_phase4_approval": True,
            "not_demo_order_approval": True,
            "not_live_order_approval": True,
            "not_execution_adapter_approval": True,
            "not_adapter_implementation_approval": True,
            "not_execution_approval": True,
            "no_mt5_access": True,
            "no_broker_request_construction": True,
            "no_broker_mutation": True,
        },
    }


def verify_h024_operator_control_state_snapshot(
    record: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> list[str]:
    """Independently verify a review-only operator control-state snapshot."""

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    max_risk = _as_decimal(max_risk_fraction, "max_risk_fraction", violations)

    if record.get("schema") != OPERATOR_CONTROL_STATE_SNAPSHOT_SCHEMA:
        violations.append(f"unexpected_schema:{record.get('schema')}")
    if record.get("kind") != OPERATOR_CONTROL_STATE_SNAPSHOT_KIND:
        violations.append(f"unexpected_kind:{record.get('kind')}")
    if str(record.get("verdict", "")).upper() != "PASS":
        violations.append(f"verdict_not_pass:{record.get('verdict')}")
    if record.get("violations") not in ([], ()):
        violations.append("record_has_violations")
    if record.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{record.get('mode')}")
    if record.get("snapshot_status") != SNAPSHOT_STATUS:
        violations.append(f"unexpected_snapshot_status:{record.get('snapshot_status')}")
    if record.get("source_safety_controls_design_schema") != EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA:
        violations.append(f"unexpected_source_safety_controls_design_schema:{record.get('source_safety_controls_design_schema')}")
    if record.get("source_safety_controls_design_kind") != EXECUTION_SAFETY_CONTROLS_DESIGN_KIND:
        violations.append(f"unexpected_source_safety_controls_design_kind:{record.get('source_safety_controls_design_kind')}")
    if record.get("source_safety_controls_design_status") != SAFETY_CONTROLS_DESIGN_STATUS:
        violations.append(f"unexpected_source_safety_controls_design_status:{record.get('source_safety_controls_design_status')}")

    for field_name in (
        "phase4_approved",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_adapter_approved",
        "adapter_implementation_approved",
        "execution_approved",
    ):
        if record.get(field_name) is not False:
            violations.append(f"{field_name}_must_be_false")

    if record.get("human_review_still_required") is not True:
        violations.append("human_review_still_required_must_be_true")

    forbidden_paths = _find_forbidden_execution_keys(record)
    if forbidden_paths:
        violations.append("record_contains_execution_like_fields:" + ",".join(forbidden_paths))

    source_chain = record.get("source_chain_summary")
    if not isinstance(source_chain, Mapping):
        violations.append("missing_source_chain_summary")
        return sorted(set(violations))

    server = _required_text(source_chain, ("server",), "server", violations)
    account_currency = _required_text(source_chain, ("account_currency",), "account_currency", violations)
    symbol = _required_text(source_chain, ("symbol",), "symbol", violations)
    normalized_symbol = _required_text(source_chain, ("normalized_symbol",), "normalized_symbol", violations)
    side = _required_text(source_chain, ("side",), "side", violations)
    review_only_intent_action = _required_text(source_chain, ("review_only_intent_action",), "review_only_intent_action", violations)
    risk_fraction = _required_decimal(source_chain, ("risk_fraction",), "risk_fraction", violations)
    risk_usd = _required_decimal(source_chain, ("risk_usd",), "risk_usd", violations)
    estimated_loss_usd = _required_decimal(source_chain, ("estimated_loss_usd",), "estimated_loss_usd", violations)

    stable_intent_id = _required_text(record, ("stable_intent_id",), "stable_intent_id", violations)
    expected_stable_intent_id = compute_h024_stable_intent_id(source_chain)
    if stable_intent_id is not None and stable_intent_id != expected_stable_intent_id:
        violations.append("stable_intent_id_mismatch")
    if stable_intent_id is not None and not _is_sha256_hex(stable_intent_id):
        violations.append("stable_intent_id_not_sha256_hex")

    kill_switch_violations = _verify_allow_kill_switch_state(
        record.get("kill_switch_state"),
        expected_strategy="H024",
        expected_normalized_symbol=None if normalized_symbol is None else normalized_symbol.upper(),
    )
    violations.extend(f"kill_switch_state:{violation}" for violation in kill_switch_violations)

    idempotency_violations = _verify_empty_idempotency_ledger(
        record.get("idempotency_ledger"),
        stable_intent_id=stable_intent_id,
    )
    violations.extend(f"idempotency_ledger:{violation}" for violation in idempotency_violations)

    snapshot_boundary = record.get("snapshot_boundary")
    if not isinstance(snapshot_boundary, Mapping):
        violations.append("missing_snapshot_boundary")
    else:
        for key in (
            "pure_python_review_only",
            "operator_control_state_only",
            "not_phase4_approval",
            "not_demo_order_approval",
            "not_live_order_approval",
            "not_execution_adapter_approval",
            "not_adapter_implementation_approval",
            "not_execution_approval",
            "no_mt5_access",
            "no_broker_request_construction",
            "no_broker_mutation",
        ):
            if snapshot_boundary.get(key) is not True:
                violations.append(f"snapshot_boundary_check_not_true:{key}")

    if violations:
        return sorted(set(violations))

    assert max_risk is not None
    assert server is not None
    assert account_currency is not None
    assert symbol is not None
    assert normalized_symbol is not None
    assert side is not None
    assert review_only_intent_action is not None
    assert risk_fraction is not None
    assert risk_usd is not None
    assert estimated_loss_usd is not None

    if server not in allowed_servers:
        violations.append(f"server_not_allowed:{server}")
    if account_currency.upper() != expected_account_currency.upper():
        violations.append(f"unexpected_account_currency:{account_currency}")
    if normalized_symbol.upper() not in {"USDJPY", "XAUUSD"}:
        violations.append(f"unsupported_normalized_symbol:{normalized_symbol}")
    if _normalize_runtime_symbol(symbol) != normalized_symbol.upper():
        violations.append(f"symbol_normalization_mismatch:{symbol}")
    if side.lower() not in {"long", "short"}:
        violations.append(f"unsupported_side:{side}")
    if side.lower() == "long" and review_only_intent_action != "BUY_MARKET_REVIEW_ONLY":
        violations.append("long_action_mismatch")
    if side.lower() == "short" and review_only_intent_action != "SELL_MARKET_REVIEW_ONLY":
        violations.append("short_action_mismatch")
    if risk_fraction <= 0:
        violations.append("risk_fraction_must_be_positive")
    if risk_fraction > max_risk:
        violations.append("risk_fraction_exceeds_max_risk_fraction")
    if risk_usd <= 0:
        violations.append("risk_usd_must_be_positive")
    if estimated_loss_usd <= 0:
        violations.append("estimated_loss_usd_must_be_positive")
    if estimated_loss_usd > risk_usd + Decimal("0.00000001"):
        violations.append("estimated_loss_exceeds_risk_usd")

    return sorted(set(violations))


def _verify_allow_kill_switch_state(
    state: Any,
    *,
    expected_strategy: str,
    expected_normalized_symbol: str | None,
) -> list[str]:
    violations: list[str] = []

    if not isinstance(state, Mapping):
        return ["missing_kill_switch_state"]
    if state.get("schema") != KILL_SWITCH_STATE_SCHEMA:
        violations.append(f"unexpected_schema:{state.get('schema')}")
    if state.get("global_enabled") is not True:
        violations.append("global_enabled_must_be_true")

    strategy_enabled = state.get("strategy_enabled")
    if not isinstance(strategy_enabled, Mapping):
        violations.append("strategy_enabled_must_be_object")
    elif strategy_enabled.get(expected_strategy) is not True:
        violations.append(f"strategy_not_enabled:{expected_strategy}")

    symbol_enabled = state.get("symbol_enabled")
    if not isinstance(symbol_enabled, Mapping):
        violations.append("symbol_enabled_must_be_object")
    elif expected_normalized_symbol is not None and symbol_enabled.get(expected_normalized_symbol) is not True:
        violations.append(f"symbol_not_enabled:{expected_normalized_symbol}")

    max_orders = _as_decimal(state.get("max_orders_per_session"), "max_orders_per_session", violations)
    orders_this_session = _as_decimal(state.get("orders_this_session"), "orders_this_session", violations)
    daily_loss_limit = _as_decimal(state.get("daily_loss_limit_usd"), "daily_loss_limit_usd", violations)
    realized_loss = _as_decimal(state.get("realized_loss_today_usd"), "realized_loss_today_usd", violations)

    if max_orders is not None and max_orders <= 0:
        violations.append("max_orders_per_session_must_be_positive")
    if orders_this_session is not None and orders_this_session < 0:
        violations.append("orders_this_session_must_be_non_negative")
    if max_orders is not None and orders_this_session is not None and orders_this_session >= max_orders:
        violations.append("orders_this_session_must_be_below_max_orders_per_session")
    if daily_loss_limit is not None and daily_loss_limit <= 0:
        violations.append("daily_loss_limit_usd_must_be_positive")
    if realized_loss is not None and realized_loss < 0:
        violations.append("realized_loss_today_usd_must_be_non_negative")
    if daily_loss_limit is not None and realized_loss is not None and realized_loss >= daily_loss_limit:
        violations.append("realized_loss_today_must_be_below_daily_loss_limit")

    return violations


def _verify_empty_idempotency_ledger(
    ledger: Any,
    *,
    stable_intent_id: str | None,
) -> list[str]:
    violations: list[str] = []

    if not isinstance(ledger, Mapping):
        return ["missing_idempotency_ledger"]
    if ledger.get("schema") != IDEMPOTENCY_LEDGER_SCHEMA:
        violations.append(f"unexpected_schema:{ledger.get('schema')}")

    pending_ids = _as_string_list(ledger.get("pending_intent_ids"), "pending_intent_ids", violations)
    completed_ids = _as_string_list(ledger.get("completed_intent_ids"), "completed_intent_ids", violations)

    if pending_ids is not None:
        if len(pending_ids) != len(set(pending_ids)):
            violations.append("duplicate_pending_intent_ids")
        if stable_intent_id is not None and stable_intent_id in set(pending_ids):
            violations.append("stable_intent_id_already_pending")
    if completed_ids is not None:
        if len(completed_ids) != len(set(completed_ids)):
            violations.append("duplicate_completed_intent_ids")
        if stable_intent_id is not None and stable_intent_id in set(completed_ids):
            violations.append("stable_intent_id_already_completed")
    if pending_ids is not None and completed_ids is not None and set(pending_ids).intersection(set(completed_ids)):
        violations.append("ambiguous_intent_ids_in_pending_and_completed")

    return violations


def _failure_record(violations: list[str]) -> dict[str, Any]:
    return {
        "schema": OPERATOR_CONTROL_STATE_SNAPSHOT_SCHEMA,
        "kind": OPERATOR_CONTROL_STATE_SNAPSHOT_KIND,
        "verdict": "FAIL",
        "violations": sorted(set(violations)),
        "mode": REVIEW_ONLY_MODE,
        "snapshot_status": SNAPSHOT_STATUS,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
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


def _as_string_list(value: Any, field_name: str, violations: list[str]) -> list[str] | None:
    if not isinstance(value, list):
        violations.append(f"{field_name}_must_be_list")
        return None
    output: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            violations.append(f"{field_name}_{index}_must_be_nonempty_string")
            continue
        output.append(item.strip())
    return output


def _json_number(value: Decimal) -> int | float:
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def _normalize_runtime_symbol(symbol: str) -> str:
    upper = symbol.upper()
    if upper.startswith("USDJPY"):
        return "USDJPY"
    if upper.startswith("XAUUSD"):
        return "XAUUSD"
    return upper


def _is_sha256_hex(value: str) -> bool:
    if len(value) != 64:
        return False
    return all(character in "0123456789abcdef" for character in value.lower())


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
            found.extend(_find_forbidden_execution_keys(child, f"{prefix}[{index}]"))
    return found


def _normalize_key(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())