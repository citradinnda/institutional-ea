from __future__ import annotations

from collections.abc import Iterable, Mapping
from decimal import Decimal
from typing import Any

from quantcore.execution.h024_manual_approval_checkpoint import (
    MANUAL_APPROVAL_CHECKPOINT_KIND,
    MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
    verify_h024_manual_approval_checkpoint_record,
)
from quantcore.execution.h024_order_intent_simulation import REVIEW_ONLY_MODE


DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA = "h024_demo_execution_adapter_design_v1"
DEMO_EXECUTION_ADAPTER_DESIGN_KIND = "DEMO_EXECUTION_ADAPTER_DESIGN_REVIEW_ONLY"
DESIGN_STATUS = "DESIGN_SPEC_ONLY_NOT_IMPLEMENTED"

REQUIRED_DESIGN_SECTIONS = (
    "scope_boundary",
    "input_contract",
    "broker_metadata_contract",
    "manual_approval_contract",
    "risk_controls",
    "observability",
    "failure_modes",
    "future_phase4_review_requirements",
)

REQUIRED_SCOPE_BOUNDARY_FLAGS = {
    "demo_only_design": True,
    "implementation_present": False,
    "adapter_implementation_approved": False,
    "execution_approved": False,
    "demo_order_placement_approved": False,
    "live_order_placement_approved": False,
    "mt5_access_present": False,
    "broker_mutation_present": False,
    "manual_approval_still_required": True,
}

FORBIDDEN_KEY_TOKENS = frozenset(
    {
        "ticket",
        "deal",
        "retcode",
        "brokerrequest",
        "mt5request",
        "mqltraderequest",
        "mqltraderesult",
        "ordersend",
        "ordercheck",
        "positionticket",
        "positionid",
        "dealid",
    }
)


def build_h024_demo_execution_adapter_design(
    checkpoint: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> dict[str, Any]:
    """Build a review-only design artifact for a future demo adapter.

    This is deliberately not an adapter. It does not import MT5, construct a
    broker request, place orders, check orders, or approve execution.
    """

    violations: list[str] = []

    source_violations = verify_h024_manual_approval_checkpoint_record(
        checkpoint,
        allowed_demo_servers=allowed_demo_servers,
        expected_account_currency=expected_account_currency,
        max_risk_fraction=max_risk_fraction,
    )
    violations.extend(f"source_checkpoint:{violation}" for violation in source_violations)

    forbidden_paths = _find_forbidden_keys(checkpoint)
    if forbidden_paths:
        violations.append("source_checkpoint_contains_execution_like_keys:" + ",".join(forbidden_paths))

    if violations:
        return _failure_record(violations)

    extract_violations: list[str] = []
    server = _required_text(checkpoint, ("server",), "server", extract_violations)
    account_currency = _required_text(checkpoint, ("account_currency",), "account_currency", extract_violations)
    symbol = _required_text(checkpoint, ("symbol",), "symbol", extract_violations)
    normalized_symbol = _required_text(checkpoint, ("normalized_symbol",), "normalized_symbol", extract_violations)
    side = _required_text(checkpoint, ("side",), "side", extract_violations)
    review_only_intent_action = _required_text(
        checkpoint,
        ("review_only_intent_action",),
        "review_only_intent_action",
        extract_violations,
    )
    source_timestamp = _required_text(checkpoint, ("source_timestamp",), "source_timestamp", extract_violations)
    source_reason = _required_text(checkpoint, ("source_reason",), "source_reason", extract_violations)

    entry = _required_number(checkpoint, ("entry",), "entry", extract_violations)
    stop = _required_number(checkpoint, ("stop",), "stop", extract_violations)
    volume = _required_number(checkpoint, ("volume",), "volume", extract_violations)
    risk_fraction = _required_number(checkpoint, ("risk_fraction",), "risk_fraction", extract_violations)
    risk_usd = _required_number(checkpoint, ("risk_usd",), "risk_usd", extract_violations)
    estimated_loss_usd = _required_number(checkpoint, ("estimated_loss_usd",), "estimated_loss_usd", extract_violations)

    if extract_violations:
        return _failure_record(extract_violations)

    assert server is not None
    assert account_currency is not None
    assert symbol is not None
    assert normalized_symbol is not None
    assert side is not None
    assert review_only_intent_action is not None
    assert source_timestamp is not None
    assert source_reason is not None
    assert entry is not None
    assert stop is not None
    assert volume is not None
    assert risk_fraction is not None
    assert risk_usd is not None
    assert estimated_loss_usd is not None

    return {
        "schema": DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA,
        "kind": DEMO_EXECUTION_ADAPTER_DESIGN_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "design_status": DESIGN_STATUS,
        "source_checkpoint_schema": MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
        "source_checkpoint_kind": MANUAL_APPROVAL_CHECKPOINT_KIND,
        "server": server,
        "account_currency": account_currency.upper(),
        "symbol": symbol,
        "normalized_symbol": normalized_symbol.upper(),
        "side": side.lower(),
        "review_only_intent_action": review_only_intent_action,
        "entry": entry,
        "stop": stop,
        "volume": volume,
        "risk_fraction": risk_fraction,
        "risk_usd": risk_usd,
        "estimated_loss_usd": estimated_loss_usd,
        "source_timestamp": source_timestamp,
        "source_reason": source_reason,
        "scope_boundary": dict(REQUIRED_SCOPE_BOUNDARY_FLAGS),
        "required_design_sections": list(REQUIRED_DESIGN_SECTIONS),
        "input_contract": {
            "accepted_input_schema": MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
            "accepted_input_kind": MANUAL_APPROVAL_CHECKPOINT_KIND,
            "requires_pending_manual_approval": True,
            "requires_manual_approval_granted_false": True,
            "requires_execution_approved_false": True,
        },
        "broker_metadata_contract": {
            "must_reuse_verified_preflight_metadata": True,
            "must_recheck_symbol_normalization": True,
            "must_recheck_volume_constraints": True,
            "must_recheck_tick_alignment": True,
            "must_recheck_estimated_loss": True,
        },
        "manual_approval_contract": {
            "current_artifact_does_not_grant_approval": True,
            "future_human_approval_required_before_any_adapter_code": True,
            "future_human_approval_required_before_any_demo_order": True,
            "future_human_approval_required_before_any_live_order": True,
        },
        "risk_controls": {
            "max_risk_fraction": float(Decimal(str(max_risk_fraction))),
            "requires_nonzero_stop_distance": True,
            "requires_loss_not_above_risk_budget": True,
            "requires_no_portfolio_bypass": True,
            "requires_h020_sizing_boundary_preserved": True,
        },
        "observability": {
            "must_emit_review_log_before_any_future_execution_path": True,
            "must_preserve_source_runtime_timestamp": True,
            "must_preserve_source_reason": True,
            "must_preserve_manual_approval_reference": True,
        },
        "failure_modes": {
            "reject_unknown_server": True,
            "reject_non_usd_account_currency": True,
            "reject_symbol_mismatch": True,
            "reject_invalid_stop_geometry": True,
            "reject_tick_or_volume_mismatch": True,
            "reject_any_execution_like_payload": True,
        },
        "future_phase4_review_requirements": {
            "requires_separate_adapter_implementation_approval": True,
            "requires_separate_demo_order_approval": True,
            "requires_static_source_verification": True,
            "requires_full_test_suite": True,
            "requires_manual_signoff_artifact": True,
        },
    }


def verify_h024_demo_execution_adapter_design_record(
    record: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> list[str]:
    """Independently verify the review-only demo adapter design artifact."""

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    if record.get("schema") != DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA:
        violations.append(f"unexpected_schema:{record.get('schema')}")
    if record.get("kind") != DEMO_EXECUTION_ADAPTER_DESIGN_KIND:
        violations.append(f"unexpected_kind:{record.get('kind')}")
    if str(record.get("verdict", "")).upper() != "PASS":
        violations.append(f"verdict_not_pass:{record.get('verdict')}")
    if record.get("violations") not in ([], ()):
        violations.append("record_has_violations")
    if record.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{record.get('mode')}")
    if record.get("design_status") != DESIGN_STATUS:
        violations.append(f"unexpected_design_status:{record.get('design_status')}")
    if record.get("source_checkpoint_schema") != MANUAL_APPROVAL_CHECKPOINT_SCHEMA:
        violations.append(f"unexpected_source_checkpoint_schema:{record.get('source_checkpoint_schema')}")
    if record.get("source_checkpoint_kind") != MANUAL_APPROVAL_CHECKPOINT_KIND:
        violations.append(f"unexpected_source_checkpoint_kind:{record.get('source_checkpoint_kind')}")

    forbidden_paths = _find_forbidden_keys(record)
    if forbidden_paths:
        violations.append("record_contains_execution_like_keys:" + ",".join(forbidden_paths))

    server = _required_text(record, ("server",), "server", violations)
    account_currency = _required_text(record, ("account_currency",), "account_currency", violations)
    symbol = _required_text(record, ("symbol",), "symbol", violations)
    normalized_symbol = _required_text(record, ("normalized_symbol",), "normalized_symbol", violations)
    side = _required_text(record, ("side",), "side", violations)
    review_only_intent_action = _required_text(record, ("review_only_intent_action",), "review_only_intent_action", violations)

    risk_fraction = _required_number(record, ("risk_fraction",), "risk_fraction", violations)
    risk_usd = _required_number(record, ("risk_usd",), "risk_usd", violations)
    estimated_loss_usd = _required_number(record, ("estimated_loss_usd",), "estimated_loss_usd", violations)

    scope_boundary = record.get("scope_boundary")
    if not isinstance(scope_boundary, Mapping):
        violations.append("missing_scope_boundary")
    else:
        for key, expected_value in REQUIRED_SCOPE_BOUNDARY_FLAGS.items():
            if scope_boundary.get(key) is not expected_value:
                violations.append(f"scope_boundary_mismatch:{key}")

    required_sections = record.get("required_design_sections")
    if not isinstance(required_sections, list):
        violations.append("missing_required_design_sections")
    elif set(required_sections) != set(REQUIRED_DESIGN_SECTIONS):
        violations.append("required_design_sections_mismatch")

    for section_name in REQUIRED_DESIGN_SECTIONS:
        if not isinstance(record.get(section_name), Mapping) and section_name != "scope_boundary":
            violations.append(f"missing_design_section:{section_name}")

    if violations:
        return sorted(set(violations))

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
    if risk_fraction > float(Decimal(str(max_risk_fraction))):
        violations.append("risk_fraction_exceeds_max_risk_fraction")
    if risk_usd <= 0:
        violations.append("risk_usd_must_be_positive")
    if estimated_loss_usd <= 0:
        violations.append("estimated_loss_usd_must_be_positive")
    if estimated_loss_usd > risk_usd + 0.00000001:
        violations.append("estimated_loss_exceeds_risk_usd")

    return sorted(set(violations))


def _failure_record(violations: list[str]) -> dict[str, Any]:
    return {
        "schema": DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA,
        "kind": DEMO_EXECUTION_ADAPTER_DESIGN_KIND,
        "verdict": "FAIL",
        "violations": sorted(set(violations)),
        "mode": REVIEW_ONLY_MODE,
        "design_status": DESIGN_STATUS,
        "scope_boundary": dict(REQUIRED_SCOPE_BOUNDARY_FLAGS),
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


def _required_number(
    mapping: Mapping[str, Any],
    paths: Iterable[str],
    field_name: str,
    violations: list[str],
) -> float | None:
    value = _lookup(mapping, paths)
    if value is None or isinstance(value, bool):
        violations.append(f"missing_or_invalid_{field_name}")
        return None
    try:
        decimal_value = Decimal(str(value))
    except Exception:
        violations.append(f"missing_or_invalid_{field_name}")
        return None
    if not decimal_value.is_finite():
        violations.append(f"non_finite_{field_name}")
        return None
    return float(decimal_value)


def _normalize_runtime_symbol(symbol: str) -> str:
    upper = symbol.upper()
    if upper.startswith("USDJPY"):
        return "USDJPY"
    if upper.startswith("XAUUSD"):
        return "XAUUSD"
    return upper


def _find_forbidden_keys(value: Any, prefix: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key)
            path = f"{prefix}.{key}" if prefix else key
            normalized_key = _normalize_key(key)
            if normalized_key in FORBIDDEN_KEY_TOKENS:
                found.append(path)
            found.extend(_find_forbidden_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_forbidden_keys(child, f"{prefix}[{index}]"))
    return found


def _normalize_key(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())