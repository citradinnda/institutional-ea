from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from quantcore.execution.h024_execution_safety_controls_design import (
    DESIGN_STATUS as SAFETY_CONTROLS_DESIGN_STATUS,
    EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
    EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
    verify_h024_execution_safety_controls_design_record,
)
from quantcore.execution.h024_order_intent_simulation import REVIEW_ONLY_MODE


EXECUTION_SAFETY_CONTROLS_PREFLIGHT_SCHEMA = "h024_execution_safety_controls_preflight_v1"
EXECUTION_SAFETY_CONTROLS_PREFLIGHT_KIND = "EXECUTION_SAFETY_CONTROLS_PREFLIGHT_REVIEW_ONLY"

KILL_SWITCH_STATE_SCHEMA = "h024_execution_kill_switch_state_v1"
IDEMPOTENCY_LEDGER_SCHEMA = "h024_execution_idempotency_ledger_v1"
AUDIT_EVENT_SCHEMA = "h024_execution_safety_audit_event_v1"
AUDIT_EVENT_KIND = "EXECUTION_SAFETY_CONTROLS_AUDIT_EVENT_REVIEW_ONLY"

CONTROL_STATUS_BLOCKED = "SAFETY_CONTROLS_BLOCKED_REVIEW_ONLY"
CONTROL_STATUS_PASS = "SAFETY_CONTROLS_PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL"

CONTROL_DECISION_BLOCK = "BLOCK"
CONTROL_DECISION_PASS_REVIEW_ONLY = "PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL"

REQUIRED_KILL_SWITCH_STATE_FIELDS = (
    "schema",
    "global_enabled",
    "strategy_enabled",
    "symbol_enabled",
    "max_orders_per_session",
    "orders_this_session",
    "daily_loss_limit_usd",
    "realized_loss_today_usd",
)

REQUIRED_LEDGER_FIELDS = (
    "schema",
    "pending_intent_ids",
    "completed_intent_ids",
)

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


def build_h024_execution_safety_controls_preflight(
    safety_controls_design: Mapping[str, Any],
    *,
    kill_switch_state: Mapping[str, Any] | None,
    idempotency_ledger: Mapping[str, Any] | None,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
    operator_decision: str = "NOT_REQUESTED",
) -> dict[str, Any]:
    """Evaluate pure-Python execution safety controls in review-only mode.

    This is not an execution adapter. It does not import MT5, construct broker
    requests, check orders, send orders, or approve execution. Missing or
    invalid control state fails closed into a BLOCK decision.
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

    intent_components = {
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
    stable_intent_id = compute_h024_stable_intent_id(intent_components)

    kill_switch_blockers, kill_switch_summary = _evaluate_kill_switch_state(
        kill_switch_state,
        strategy="H024",
        normalized_symbol=normalized_symbol.upper(),
    )
    idempotency_blockers, idempotency_summary = _evaluate_idempotency_ledger(
        idempotency_ledger,
        stable_intent_id=stable_intent_id,
    )

    blocked_reasons = sorted(set(kill_switch_blockers + idempotency_blockers))
    control_decision = CONTROL_DECISION_BLOCK if blocked_reasons else CONTROL_DECISION_PASS_REVIEW_ONLY
    control_status = CONTROL_STATUS_BLOCKED if blocked_reasons else CONTROL_STATUS_PASS

    audit_event = _build_audit_event(
        stable_intent_id=stable_intent_id,
        control_decision=control_decision,
        control_status=control_status,
        blocked_reasons=blocked_reasons,
        operator_decision=operator_decision,
        source_chain_summary=intent_components,
    )

    return {
        "schema": EXECUTION_SAFETY_CONTROLS_PREFLIGHT_SCHEMA,
        "kind": EXECUTION_SAFETY_CONTROLS_PREFLIGHT_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "source_safety_controls_design_schema": EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
        "source_safety_controls_design_kind": EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
        "source_safety_controls_design_status": SAFETY_CONTROLS_DESIGN_STATUS,
        "control_status": control_status,
        "control_decision": control_decision,
        "blocked_reasons": blocked_reasons,
        "stable_intent_id": stable_intent_id,
        "operator_decision": str(operator_decision),
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "source_chain_summary": intent_components,
        "kill_switch_evaluation": kill_switch_summary,
        "idempotency_evaluation": idempotency_summary,
        "immutable_audit_log_event": audit_event,
        "safety_boundary": {
            "pure_python_review_only": True,
            "no_mt5_access": True,
            "no_broker_mutation": True,
            "no_broker_request_construction": True,
            "no_order_send": True,
            "no_order_check": True,
            "no_execution_adapter": True,
            "not_execution_approval": True,
        },
    }


def verify_h024_execution_safety_controls_preflight_record(
    record: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> list[str]:
    """Independently verify a review-only safety-controls preflight record."""

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    max_risk = _as_decimal(max_risk_fraction, "max_risk_fraction", violations)

    if record.get("schema") != EXECUTION_SAFETY_CONTROLS_PREFLIGHT_SCHEMA:
        violations.append(f"unexpected_schema:{record.get('schema')}")
    if record.get("kind") != EXECUTION_SAFETY_CONTROLS_PREFLIGHT_KIND:
        violations.append(f"unexpected_kind:{record.get('kind')}")
    if str(record.get("verdict", "")).upper() != "PASS":
        violations.append(f"verdict_not_pass:{record.get('verdict')}")
    if record.get("violations") not in ([], ()):
        violations.append("record_has_violations")
    if record.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{record.get('mode')}")
    if record.get("source_safety_controls_design_schema") != EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA:
        violations.append(f"unexpected_source_safety_controls_design_schema:{record.get('source_safety_controls_design_schema')}")
    if record.get("source_safety_controls_design_kind") != EXECUTION_SAFETY_CONTROLS_DESIGN_KIND:
        violations.append(f"unexpected_source_safety_controls_design_kind:{record.get('source_safety_controls_design_kind')}")
    if record.get("source_safety_controls_design_status") != SAFETY_CONTROLS_DESIGN_STATUS:
        violations.append(f"unexpected_source_safety_controls_design_status:{record.get('source_safety_controls_design_status')}")

    forbidden_paths = _find_forbidden_execution_keys(record)
    if forbidden_paths:
        violations.append("record_contains_execution_like_fields:" + ",".join(forbidden_paths))

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

    control_status = str(record.get("control_status", ""))
    control_decision = str(record.get("control_decision", ""))
    blocked_reasons = record.get("blocked_reasons")
    if control_status not in {CONTROL_STATUS_BLOCKED, CONTROL_STATUS_PASS}:
        violations.append(f"unexpected_control_status:{control_status}")
    if control_decision not in {CONTROL_DECISION_BLOCK, CONTROL_DECISION_PASS_REVIEW_ONLY}:
        violations.append(f"unexpected_control_decision:{control_decision}")
    if not isinstance(blocked_reasons, list):
        violations.append("blocked_reasons_must_be_list")
    elif control_decision == CONTROL_DECISION_BLOCK and not blocked_reasons:
        violations.append("blocked_decision_requires_blocked_reasons")
    elif control_decision == CONTROL_DECISION_PASS_REVIEW_ONLY and blocked_reasons:
        violations.append("pass_decision_must_not_have_blocked_reasons")
    if control_status == CONTROL_STATUS_BLOCKED and control_decision != CONTROL_DECISION_BLOCK:
        violations.append("blocked_status_decision_mismatch")
    if control_status == CONTROL_STATUS_PASS and control_decision != CONTROL_DECISION_PASS_REVIEW_ONLY:
        violations.append("pass_status_decision_mismatch")

    stable_intent_id = _required_text(record, ("stable_intent_id",), "stable_intent_id", violations)
    if stable_intent_id is not None and not _is_sha256_hex(stable_intent_id):
        violations.append("stable_intent_id_not_sha256_hex")

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

    expected_intent_id = compute_h024_stable_intent_id(source_chain)
    if stable_intent_id is not None and stable_intent_id != expected_intent_id:
        violations.append("stable_intent_id_mismatch")

    kill_switch_evaluation = record.get("kill_switch_evaluation")
    if not isinstance(kill_switch_evaluation, Mapping):
        violations.append("missing_kill_switch_evaluation")
    idempotency_evaluation = record.get("idempotency_evaluation")
    if not isinstance(idempotency_evaluation, Mapping):
        violations.append("missing_idempotency_evaluation")

    audit_event = record.get("immutable_audit_log_event")
    if not isinstance(audit_event, Mapping):
        violations.append("missing_immutable_audit_log_event")
    else:
        audit_violations = verify_h024_execution_safety_audit_event(audit_event, expected_stable_intent_id=stable_intent_id)
        violations.extend(f"audit_event:{violation}" for violation in audit_violations)

    safety_boundary = record.get("safety_boundary")
    if not isinstance(safety_boundary, Mapping):
        violations.append("missing_safety_boundary")
    else:
        for key in (
            "pure_python_review_only",
            "no_mt5_access",
            "no_broker_mutation",
            "no_broker_request_construction",
            "no_order_send",
            "no_order_check",
            "no_execution_adapter",
            "not_execution_approval",
        ):
            if safety_boundary.get(key) is not True:
                violations.append(f"safety_boundary_check_not_true:{key}")

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


def verify_h024_execution_safety_audit_event(
    audit_event: Mapping[str, Any],
    *,
    expected_stable_intent_id: str | None,
) -> list[str]:
    violations: list[str] = []

    if audit_event.get("schema") != AUDIT_EVENT_SCHEMA:
        violations.append(f"unexpected_schema:{audit_event.get('schema')}")
    if audit_event.get("kind") != AUDIT_EVENT_KIND:
        violations.append(f"unexpected_kind:{audit_event.get('kind')}")
    if audit_event.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{audit_event.get('mode')}")
    if audit_event.get("append_only_required") is not True:
        violations.append("append_only_required_must_be_true")
    if audit_event.get("execution_approved") is not False:
        violations.append("execution_approved_must_be_false")

    stable_intent_id = _required_text(audit_event, ("stable_intent_id",), "stable_intent_id", violations)
    if expected_stable_intent_id is not None and stable_intent_id != expected_stable_intent_id:
        violations.append("stable_intent_id_mismatch")
    if stable_intent_id is not None and not _is_sha256_hex(stable_intent_id):
        violations.append("stable_intent_id_not_sha256_hex")

    event_hash = _required_text(audit_event, ("event_hash",), "event_hash", violations)
    if event_hash is not None and not _is_sha256_hex(event_hash):
        violations.append("event_hash_not_sha256_hex")

    if audit_event.get("control_decision") not in {CONTROL_DECISION_BLOCK, CONTROL_DECISION_PASS_REVIEW_ONLY}:
        violations.append(f"unexpected_control_decision:{audit_event.get('control_decision')}")
    if not isinstance(audit_event.get("blocked_reasons"), list):
        violations.append("blocked_reasons_must_be_list")

    if violations:
        return sorted(set(violations))

    assert event_hash is not None
    expected_hash = _hash_without_event_hash(audit_event)
    if event_hash != expected_hash:
        violations.append("event_hash_mismatch")

    return sorted(set(violations))


def append_h024_execution_safety_audit_event(path: Path, audit_event: Mapping[str, Any]) -> None:
    """Append one audit event as JSONL without truncating the target file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        json.dump(dict(audit_event), handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def compute_h024_stable_intent_id(intent_components: Mapping[str, Any]) -> str:
    required = (
        "strategy",
        "server",
        "account_currency",
        "symbol",
        "normalized_symbol",
        "side",
        "review_only_intent_action",
        "risk_fraction",
        "risk_usd",
        "estimated_loss_usd",
        "source_timestamp",
        "source_reason",
    )
    canonical = {key: intent_components.get(key) for key in required}
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_audit_event(
    *,
    stable_intent_id: str,
    control_decision: str,
    control_status: str,
    blocked_reasons: Sequence[str],
    operator_decision: str,
    source_chain_summary: Mapping[str, Any],
) -> dict[str, Any]:
    event_without_hash = {
        "schema": AUDIT_EVENT_SCHEMA,
        "kind": AUDIT_EVENT_KIND,
        "mode": REVIEW_ONLY_MODE,
        "append_only_required": True,
        "stable_intent_id": stable_intent_id,
        "control_decision": control_decision,
        "control_status": control_status,
        "blocked_reasons": list(blocked_reasons),
        "operator_decision": str(operator_decision),
        "source_chain_summary": dict(source_chain_summary),
        "execution_approved": False,
    }
    return {**event_without_hash, "event_hash": _hash_mapping(event_without_hash)}


def _hash_without_event_hash(value: Mapping[str, Any]) -> str:
    payload = dict(value)
    payload.pop("event_hash", None)
    return _hash_mapping(payload)


def _hash_mapping(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _evaluate_kill_switch_state(
    state: Mapping[str, Any] | None,
    *,
    strategy: str,
    normalized_symbol: str,
) -> tuple[list[str], dict[str, Any]]:
    blockers: list[str] = []
    summary: dict[str, Any] = {
        "schema": KILL_SWITCH_STATE_SCHEMA,
        "input_present": isinstance(state, Mapping),
        "strategy": strategy,
        "normalized_symbol": normalized_symbol,
        "fail_closed": True,
    }

    if not isinstance(state, Mapping):
        blockers.append("missing_kill_switch_state")
        summary["state_valid"] = False
        return blockers, summary

    missing_fields = [field for field in REQUIRED_KILL_SWITCH_STATE_FIELDS if field not in state]
    blockers.extend(f"missing_kill_switch_field:{field}" for field in missing_fields)

    if state.get("schema") != KILL_SWITCH_STATE_SCHEMA:
        blockers.append(f"unexpected_kill_switch_schema:{state.get('schema')}")

    if state.get("global_enabled") is not True:
        blockers.append("kill_switch_global_not_enabled")

    strategy_enabled = state.get("strategy_enabled")
    if not isinstance(strategy_enabled, Mapping):
        blockers.append("missing_strategy_enabled_map")
        strategy_value = None
    else:
        strategy_value = strategy_enabled.get(strategy)
        if strategy_value is not True:
            blockers.append(f"strategy_not_enabled:{strategy}")

    symbol_enabled = state.get("symbol_enabled")
    if not isinstance(symbol_enabled, Mapping):
        blockers.append("missing_symbol_enabled_map")
        symbol_value = None
    else:
        symbol_value = symbol_enabled.get(normalized_symbol)
        if symbol_value is not True:
            blockers.append(f"symbol_not_enabled:{normalized_symbol}")

    max_orders = _as_int(state.get("max_orders_per_session"), "max_orders_per_session", blockers)
    current_orders = _as_int(state.get("orders_this_session"), "orders_this_session", blockers)
    if max_orders is not None and max_orders <= 0:
        blockers.append("max_orders_per_session_must_be_positive")
    if current_orders is not None and current_orders < 0:
        blockers.append("orders_this_session_must_be_non_negative")
    if max_orders is not None and current_orders is not None and max_orders > 0 and current_orders >= max_orders:
        blockers.append("max_orders_per_session_reached")

    daily_loss_limit = _as_decimal(state.get("daily_loss_limit_usd"), "daily_loss_limit_usd", blockers)
    realized_loss = _as_decimal(state.get("realized_loss_today_usd"), "realized_loss_today_usd", blockers)
    if daily_loss_limit is not None and daily_loss_limit <= 0:
        blockers.append("daily_loss_limit_usd_must_be_positive")
    if realized_loss is not None and realized_loss < 0:
        blockers.append("realized_loss_today_usd_must_be_non_negative")
    if daily_loss_limit is not None and realized_loss is not None and daily_loss_limit > 0 and realized_loss >= daily_loss_limit:
        blockers.append("daily_loss_limit_reached")

    summary.update(
        {
            "state_valid": not blockers,
            "global_enabled": state.get("global_enabled"),
            "strategy_enabled": strategy_value,
            "symbol_enabled": symbol_value,
            "max_orders_per_session": max_orders,
            "orders_this_session": current_orders,
            "daily_loss_limit_usd": None if daily_loss_limit is None else _json_number(daily_loss_limit),
            "realized_loss_today_usd": None if realized_loss is None else _json_number(realized_loss),
        }
    )
    return blockers, summary


def _evaluate_idempotency_ledger(
    ledger: Mapping[str, Any] | None,
    *,
    stable_intent_id: str,
) -> tuple[list[str], dict[str, Any]]:
    blockers: list[str] = []
    summary: dict[str, Any] = {
        "schema": IDEMPOTENCY_LEDGER_SCHEMA,
        "input_present": isinstance(ledger, Mapping),
        "stable_intent_id": stable_intent_id,
        "fail_closed": True,
    }

    if not isinstance(ledger, Mapping):
        blockers.append("missing_idempotency_ledger")
        summary["ledger_valid"] = False
        return blockers, summary

    missing_fields = [field for field in REQUIRED_LEDGER_FIELDS if field not in ledger]
    blockers.extend(f"missing_idempotency_ledger_field:{field}" for field in missing_fields)

    if ledger.get("schema") != IDEMPOTENCY_LEDGER_SCHEMA:
        blockers.append(f"unexpected_idempotency_ledger_schema:{ledger.get('schema')}")

    pending_ids = _as_string_list(ledger.get("pending_intent_ids"), "pending_intent_ids", blockers)
    completed_ids = _as_string_list(ledger.get("completed_intent_ids"), "completed_intent_ids", blockers)

    if pending_ids is not None and len(pending_ids) != len(set(pending_ids)):
        blockers.append("duplicate_pending_intent_ids_in_ledger")
    if completed_ids is not None and len(completed_ids) != len(set(completed_ids)):
        blockers.append("duplicate_completed_intent_ids_in_ledger")

    pending_set = set(pending_ids or [])
    completed_set = set(completed_ids or [])
    if pending_set.intersection(completed_set):
        blockers.append("ambiguous_intent_ids_in_pending_and_completed")
    if stable_intent_id in pending_set:
        blockers.append("duplicate_pending_intent_id")
    if stable_intent_id in completed_set:
        blockers.append("duplicate_completed_intent_id")

    summary.update(
        {
            "ledger_valid": not blockers,
            "pending_intent_count": len(pending_ids or []),
            "completed_intent_count": len(completed_ids or []),
            "stable_intent_seen_pending": stable_intent_id in pending_set,
            "stable_intent_seen_completed": stable_intent_id in completed_set,
        }
    )
    return blockers, summary


def _failure_record(violations: list[str]) -> dict[str, Any]:
    return {
        "schema": EXECUTION_SAFETY_CONTROLS_PREFLIGHT_SCHEMA,
        "kind": EXECUTION_SAFETY_CONTROLS_PREFLIGHT_KIND,
        "verdict": "FAIL",
        "violations": sorted(set(violations)),
        "mode": REVIEW_ONLY_MODE,
        "control_status": CONTROL_STATUS_BLOCKED,
        "control_decision": CONTROL_DECISION_BLOCK,
        "blocked_reasons": ["source_validation_failed"],
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


def _as_int(value: Any, field_name: str, violations: list[str]) -> int | None:
    decimal_value = _as_decimal(value, field_name, violations)
    if decimal_value is None:
        return None
    if decimal_value != decimal_value.to_integral_value():
        violations.append(f"{field_name}_must_be_integer")
        return None
    return int(decimal_value)


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