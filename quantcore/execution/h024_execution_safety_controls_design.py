from __future__ import annotations

from collections.abc import Iterable, Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from quantcore.execution.h024_order_intent_simulation import REVIEW_ONLY_MODE
from quantcore.execution.h024_phase4_readiness_review import (
    PHASE4_READINESS_REVIEW_KIND,
    PHASE4_READINESS_REVIEW_SCHEMA,
    READY_STATUS,
    verify_h024_phase4_readiness_review_record,
)


EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA = "h024_execution_safety_controls_design_v1"
EXECUTION_SAFETY_CONTROLS_DESIGN_KIND = "EXECUTION_SAFETY_CONTROLS_DESIGN_REVIEW_ONLY"
DESIGN_STATUS = "SAFETY_CONTROLS_DESIGN_SPEC_ONLY_NOT_IMPLEMENTED"

REQUIRED_CONTROL_SECTIONS = (
    "scope_boundary",
    "kill_switch_contract",
    "idempotency_contract",
    "immutable_audit_log_contract",
    "operator_workflow_contract",
    "failure_modes",
    "future_phase4_review_requirements",
)

REQUIRED_SCOPE_BOUNDARY_FLAGS = {
    "design_only": True,
    "implementation_present": False,
    "mt5_access_present": False,
    "broker_mutation_present": False,
    "broker_request_construction_present": False,
    "execution_approved": False,
    "demo_order_placement_approved": False,
    "live_order_placement_approved": False,
    "execution_adapter_approved": False,
    "adapter_implementation_approved": False,
    "human_review_still_required": True,
}

REQUIRED_KILL_SWITCH_FLAGS = {
    "must_default_to_blocked_until_explicitly_enabled": True,
    "must_support_global_disable": True,
    "must_support_symbol_disable": True,
    "must_support_strategy_disable": True,
    "must_support_max_orders_per_session_guard": True,
    "must_support_max_daily_loss_guard": True,
    "must_fail_closed_on_missing_or_invalid_state": True,
    "must_emit_reason_for_every_block": True,
}

REQUIRED_IDEMPOTENCY_FLAGS = {
    "must_define_stable_intent_id": True,
    "intent_id_must_include_strategy_symbol_side_entry_stop_volume_source_timestamp": True,
    "must_reject_duplicate_pending_intent": True,
    "must_reject_duplicate_completed_intent": True,
    "must_fail_closed_on_ambiguous_prior_state": True,
    "must_never_retry_without_recorded_terminal_state": True,
}

REQUIRED_AUDIT_LOG_FLAGS = {
    "must_append_only": True,
    "must_record_source_phase4_readiness_reference": True,
    "must_record_operator_decision": True,
    "must_record_preflight_snapshot": True,
    "must_record_idempotency_key": True,
    "must_record_kill_switch_state": True,
    "must_record_all_rejections": True,
    "must_be_readable_without_mt5": True,
}

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


def build_h024_execution_safety_controls_design(
    phase4_readiness_review: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> dict[str, Any]:
    """Build a review-only safety-controls design artifact.

    This specifies kill-switch, idempotency, and immutable audit-log controls
    needed before any future adapter implementation discussion. It does not
    implement MT5 access, construct broker requests, place orders, or approve
    execution.
    """

    violations: list[str] = []

    source_violations = verify_h024_phase4_readiness_review_record(
        phase4_readiness_review,
        allowed_demo_servers=allowed_demo_servers,
        expected_account_currency=expected_account_currency,
        max_risk_fraction=max_risk_fraction,
    )
    violations.extend(f"source_phase4_readiness_review:{violation}" for violation in source_violations)

    forbidden_paths = _find_forbidden_execution_keys(phase4_readiness_review)
    if forbidden_paths:
        violations.append("source_phase4_review_contains_execution_like_fields:" + ",".join(forbidden_paths))

    if phase4_readiness_review.get("review_request_status") != READY_STATUS:
        violations.append(f"source_phase4_review_not_ready:{phase4_readiness_review.get('review_request_status')}")
    if phase4_readiness_review.get("phase4_approved") is not False:
        violations.append("source_phase4_approved_must_be_false")
    if phase4_readiness_review.get("execution_approved") is not False:
        violations.append("source_execution_approved_must_be_false")
    if phase4_readiness_review.get("demo_order_placement_approved") is not False:
        violations.append("source_demo_order_placement_approved_must_be_false")
    if phase4_readiness_review.get("live_order_placement_approved") is not False:
        violations.append("source_live_order_placement_approved_must_be_false")
    if phase4_readiness_review.get("execution_adapter_approved") is not False:
        violations.append("source_execution_adapter_approved_must_be_false")
    if phase4_readiness_review.get("adapter_implementation_approved") is not False:
        violations.append("source_adapter_implementation_approved_must_be_false")

    source_chain = phase4_readiness_review.get("source_chain_summary")
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

    stable_intent_components = {
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

    return {
        "schema": EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
        "kind": EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "design_status": DESIGN_STATUS,
        "source_phase4_readiness_schema": PHASE4_READINESS_REVIEW_SCHEMA,
        "source_phase4_readiness_kind": PHASE4_READINESS_REVIEW_KIND,
        "source_phase4_readiness_status": READY_STATUS,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "scope_boundary": dict(REQUIRED_SCOPE_BOUNDARY_FLAGS),
        "required_control_sections": list(REQUIRED_CONTROL_SECTIONS),
        "source_chain_summary": stable_intent_components,
        "kill_switch_contract": dict(REQUIRED_KILL_SWITCH_FLAGS),
        "idempotency_contract": {
            **REQUIRED_IDEMPOTENCY_FLAGS,
            "stable_intent_id_components": list(stable_intent_components.keys()),
        },
        "immutable_audit_log_contract": dict(REQUIRED_AUDIT_LOG_FLAGS),
        "operator_workflow_contract": {
            "must_require_human_review_before_adapter_implementation": True,
            "must_require_human_review_before_demo_order_placement": True,
            "must_require_human_review_before_live_order_placement": True,
            "must_surface_all_blocking_reasons": True,
            "must_not_auto_promote_from_readiness_to_execution": True,
        },
        "failure_modes": {
            "reject_missing_kill_switch_state": True,
            "reject_invalid_kill_switch_state": True,
            "reject_duplicate_intent_id": True,
            "reject_missing_audit_log_sink": True,
            "reject_non_append_only_audit_log": True,
            "reject_any_execution_like_payload": True,
            "fail_closed_on_unhandled_exception": True,
        },
        "future_phase4_review_requirements": {
            "requires_kill_switch_implementation_before_adapter": True,
            "requires_idempotency_implementation_before_adapter": True,
            "requires_immutable_audit_log_implementation_before_adapter": True,
            "requires_static_source_verification": True,
            "requires_full_test_suite": True,
            "requires_separate_human_approval_for_adapter_implementation": True,
            "requires_separate_human_approval_for_demo_order": True,
            "requires_separate_human_approval_for_live_order": True,
        },
    }


def verify_h024_execution_safety_controls_design_record(
    record: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> list[str]:
    """Independently verify the review-only safety-controls design artifact."""

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    max_risk = _as_decimal(max_risk_fraction, "max_risk_fraction", violations)

    if record.get("schema") != EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA:
        violations.append(f"unexpected_schema:{record.get('schema')}")
    if record.get("kind") != EXECUTION_SAFETY_CONTROLS_DESIGN_KIND:
        violations.append(f"unexpected_kind:{record.get('kind')}")
    if str(record.get("verdict", "")).upper() != "PASS":
        violations.append(f"verdict_not_pass:{record.get('verdict')}")
    if record.get("violations") not in ([], ()):
        violations.append("record_has_violations")
    if record.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{record.get('mode')}")
    if record.get("design_status") != DESIGN_STATUS:
        violations.append(f"unexpected_design_status:{record.get('design_status')}")
    if record.get("source_phase4_readiness_schema") != PHASE4_READINESS_REVIEW_SCHEMA:
        violations.append(f"unexpected_source_phase4_readiness_schema:{record.get('source_phase4_readiness_schema')}")
    if record.get("source_phase4_readiness_kind") != PHASE4_READINESS_REVIEW_KIND:
        violations.append(f"unexpected_source_phase4_readiness_kind:{record.get('source_phase4_readiness_kind')}")
    if record.get("source_phase4_readiness_status") != READY_STATUS:
        violations.append(f"unexpected_source_phase4_readiness_status:{record.get('source_phase4_readiness_status')}")

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

    scope_boundary = record.get("scope_boundary")
    if not isinstance(scope_boundary, Mapping):
        violations.append("missing_scope_boundary")
    else:
        for key, expected in REQUIRED_SCOPE_BOUNDARY_FLAGS.items():
            if scope_boundary.get(key) is not expected:
                violations.append(f"scope_boundary_mismatch:{key}")

    required_sections = record.get("required_control_sections")
    if not isinstance(required_sections, list):
        violations.append("missing_required_control_sections")
    elif set(required_sections) != set(REQUIRED_CONTROL_SECTIONS):
        violations.append("required_control_sections_mismatch")

    for section_name in REQUIRED_CONTROL_SECTIONS:
        if section_name == "scope_boundary":
            continue
        if not isinstance(record.get(section_name), Mapping):
            violations.append(f"missing_control_section:{section_name}")

    _verify_required_flags(record.get("kill_switch_contract"), REQUIRED_KILL_SWITCH_FLAGS, "kill_switch_contract", violations)
    _verify_required_flags(record.get("idempotency_contract"), REQUIRED_IDEMPOTENCY_FLAGS, "idempotency_contract", violations)
    _verify_required_flags(
        record.get("immutable_audit_log_contract"),
        REQUIRED_AUDIT_LOG_FLAGS,
        "immutable_audit_log_contract",
        violations,
    )

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

    idempotency_contract = record.get("idempotency_contract")
    if isinstance(idempotency_contract, Mapping):
        components = idempotency_contract.get("stable_intent_id_components")
        if not isinstance(components, list):
            violations.append("missing_stable_intent_id_components")
        else:
            required_components = {
                "strategy",
                "server",
                "symbol",
                "normalized_symbol",
                "side",
                "review_only_intent_action",
                "risk_fraction",
                "source_timestamp",
            }
            missing = required_components.difference(set(components))
            if missing:
                violations.append("stable_intent_id_components_missing:" + ",".join(sorted(missing)))

    return sorted(set(violations))


def _failure_record(violations: list[str]) -> dict[str, Any]:
    return {
        "schema": EXECUTION_SAFETY_CONTROLS_DESIGN_SCHEMA,
        "kind": EXECUTION_SAFETY_CONTROLS_DESIGN_KIND,
        "verdict": "FAIL",
        "violations": sorted(set(violations)),
        "mode": REVIEW_ONLY_MODE,
        "design_status": DESIGN_STATUS,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "scope_boundary": dict(REQUIRED_SCOPE_BOUNDARY_FLAGS),
    }


def _verify_required_flags(
    section: Any,
    required_flags: Mapping[str, bool],
    section_name: str,
    violations: list[str],
) -> None:
    if not isinstance(section, Mapping):
        violations.append(f"missing_{section_name}")
        return
    for key, expected in required_flags.items():
        if section.get(key) is not expected:
            violations.append(f"{section_name}_flag_mismatch:{key}")


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