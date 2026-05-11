from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal, InvalidOperation
from typing import Any

from quantcore.execution.h024_demo_execution_adapter_design import (
    DEMO_EXECUTION_ADAPTER_DESIGN_KIND,
    DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA,
    DESIGN_STATUS,
    verify_h024_demo_execution_adapter_design_record,
)
from quantcore.execution.h024_manual_approval_checkpoint import (
    APPROVAL_STATUS,
    MANUAL_APPROVAL_CHECKPOINT_KIND,
    MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
    verify_h024_manual_approval_checkpoint_record,
)
from quantcore.execution.h024_order_intent_simulation import REVIEW_ONLY_MODE


PHASE4_READINESS_REVIEW_SCHEMA = "h024_phase4_readiness_review_v1"
PHASE4_READINESS_REVIEW_KIND = "PHASE4_READINESS_REVIEW_REQUEST_REVIEW_ONLY"
READY_STATUS = "READY_FOR_PHASE4_REVIEW_REQUEST"
NOT_READY_STATUS = "NOT_READY_FOR_PHASE4_REVIEW_REQUEST"

DRY_RUN_REQUESTS_ARTIFACT = "dry_run_requests"
DEMO_ORDER_PLANS_ARTIFACT = "demo_order_plans"
BROKER_METADATA_PREFLIGHT_ARTIFACT = "broker_metadata_preflight"
ORDER_INTENT_SIMULATION_ARTIFACT = "order_intent_simulation"
MANUAL_APPROVAL_CHECKPOINT_ARTIFACT = "manual_approval_checkpoint"
DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT = "demo_execution_adapter_design"

REQUIRED_ARTIFACT_KEYS = (
    DRY_RUN_REQUESTS_ARTIFACT,
    DEMO_ORDER_PLANS_ARTIFACT,
    BROKER_METADATA_PREFLIGHT_ARTIFACT,
    ORDER_INTENT_SIMULATION_ARTIFACT,
    MANUAL_APPROVAL_CHECKPOINT_ARTIFACT,
    DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT,
)

EXPECTED_ARTIFACT_RECORD_COUNTS = {key: 1 for key in REQUIRED_ARTIFACT_KEYS}

REQUIRED_READINESS_CHECKS = (
    "all_independent_artifact_verifiers_passed",
    "exactly_one_record_per_required_artifact",
    "manual_checkpoint_pending_not_granted",
    "demo_adapter_design_spec_only_not_implemented",
    "phase4_not_approved",
    "demo_order_placement_not_approved",
    "live_order_placement_not_approved",
    "execution_adapter_not_approved",
    "execution_not_approved",
    "human_review_still_required",
    "no_execution_like_fields_detected",
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


def build_h024_phase4_readiness_review(
    artifacts: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    artifact_verifications: Mapping[str, Mapping[str, Any]],
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> dict[str, Any]:
    """Build a single review-only Phase 4 readiness-request artifact.

    This is deliberately not Phase 4 approval, not execution approval, not demo
    order approval, and not adapter implementation approval. It aggregates the
    existing verified review-only artifacts into a request-ready checklist.
    """

    violations: list[str] = []
    normalized_artifacts: dict[str, list[Mapping[str, Any]]] = {}

    for key in REQUIRED_ARTIFACT_KEYS:
        raw_records = artifacts.get(key)
        if raw_records is None:
            violations.append(f"missing_artifact:{key}")
            normalized_artifacts[key] = []
            continue
        records = list(raw_records)
        normalized_artifacts[key] = records
        expected_count = EXPECTED_ARTIFACT_RECORD_COUNTS[key]
        if len(records) != expected_count:
            violations.append(f"artifact_record_count_mismatch:{key}:expected_{expected_count}:actual_{len(records)}")
        for index, record in enumerate(records, start=1):
            if not isinstance(record, Mapping):
                violations.append(f"artifact_record_not_object:{key}:{index}")

    for key in REQUIRED_ARTIFACT_KEYS:
        verifier = artifact_verifications.get(key)
        if not isinstance(verifier, Mapping):
            violations.append(f"missing_independent_verification:{key}")
            continue
        if str(verifier.get("verdict", "")).upper() != "PASS":
            violations.append(f"independent_verifier_not_pass:{key}:{verifier.get('verdict')}")
        if verifier.get("violations") not in (None, [], ()):
            violations.append(f"independent_verifier_reported_violations:{key}")
        verifier_count = verifier.get("record_count")
        if verifier_count is not None and verifier_count != len(normalized_artifacts.get(key, [])):
            violations.append(f"independent_verifier_record_count_mismatch:{key}")

    manual_records = normalized_artifacts.get(MANUAL_APPROVAL_CHECKPOINT_ARTIFACT, [])
    design_records = normalized_artifacts.get(DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT, [])

    for index, record in enumerate(manual_records, start=1):
        if isinstance(record, Mapping):
            record_violations = verify_h024_manual_approval_checkpoint_record(
                record,
                allowed_demo_servers=allowed_demo_servers,
                expected_account_currency=expected_account_currency,
                max_risk_fraction=max_risk_fraction,
            )
            violations.extend(f"manual_checkpoint_{index}:{violation}" for violation in record_violations)

    for index, record in enumerate(design_records, start=1):
        if isinstance(record, Mapping):
            record_violations = verify_h024_demo_execution_adapter_design_record(
                record,
                allowed_demo_servers=allowed_demo_servers,
                expected_account_currency=expected_account_currency,
                max_risk_fraction=max_risk_fraction,
            )
            violations.extend(f"demo_execution_adapter_design_{index}:{violation}" for violation in record_violations)

    forbidden_paths = _find_forbidden_execution_keys(normalized_artifacts)
    if forbidden_paths:
        violations.append("source_artifacts_contain_execution_like_fields:" + ",".join(forbidden_paths))

    manual = manual_records[0] if len(manual_records) == 1 and isinstance(manual_records[0], Mapping) else {}
    design = design_records[0] if len(design_records) == 1 and isinstance(design_records[0], Mapping) else {}

    shared_violations: list[str] = []
    server = _required_text(manual, ("server",), "server", shared_violations)
    account_currency = _required_text(manual, ("account_currency",), "account_currency", shared_violations)
    symbol = _required_text(manual, ("symbol",), "symbol", shared_violations)
    normalized_symbol = _required_text(manual, ("normalized_symbol",), "normalized_symbol", shared_violations)
    side = _required_text(manual, ("side",), "side", shared_violations)
    review_only_intent_action = _required_text(
        manual,
        ("review_only_intent_action",),
        "review_only_intent_action",
        shared_violations,
    )
    source_timestamp = _required_text(manual, ("source_timestamp",), "source_timestamp", shared_violations)
    source_reason = _required_text(manual, ("source_reason",), "source_reason", shared_violations)
    risk_fraction = _required_decimal(manual, ("risk_fraction",), "risk_fraction", shared_violations)
    risk_usd = _required_decimal(manual, ("risk_usd",), "risk_usd", shared_violations)
    estimated_loss_usd = _required_decimal(manual, ("estimated_loss_usd",), "estimated_loss_usd", shared_violations)

    if design:
        for field_name, manual_value in (
            ("server", server),
            ("account_currency", account_currency),
            ("symbol", symbol),
            ("normalized_symbol", normalized_symbol),
            ("side", side),
            ("review_only_intent_action", review_only_intent_action),
            ("source_timestamp", source_timestamp),
            ("source_reason", source_reason),
        ):
            design_value = design.get(field_name)
            if manual_value is not None and str(design_value).strip() != str(manual_value).strip():
                violations.append(f"manual_design_field_mismatch:{field_name}")

    violations.extend(shared_violations)

    artifact_counts = {key: len(normalized_artifacts.get(key, [])) for key in REQUIRED_ARTIFACT_KEYS}
    verifier_summary = _summarize_verifications(artifact_verifications)

    if violations:
        return _failure_record(
            violations,
            artifact_counts=artifact_counts,
            artifact_verifications=verifier_summary,
        )

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

    readiness_checks = {key: True for key in REQUIRED_READINESS_CHECKS}

    return {
        "schema": PHASE4_READINESS_REVIEW_SCHEMA,
        "kind": PHASE4_READINESS_REVIEW_KIND,
        "verdict": "PASS",
        "violations": [],
        "mode": REVIEW_ONLY_MODE,
        "review_request_status": READY_STATUS,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "source_manual_checkpoint_schema": MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
        "source_manual_checkpoint_kind": MANUAL_APPROVAL_CHECKPOINT_KIND,
        "source_manual_approval_status": APPROVAL_STATUS,
        "source_manual_approval_granted": False,
        "source_demo_execution_adapter_design_schema": DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA,
        "source_demo_execution_adapter_design_kind": DEMO_EXECUTION_ADAPTER_DESIGN_KIND,
        "source_demo_execution_adapter_design_status": DESIGN_STATUS,
        "artifact_counts": artifact_counts,
        "artifact_verifications": verifier_summary,
        "readiness_checks": readiness_checks,
        "source_chain_summary": {
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
        },
        "approval_boundary": {
            "this_artifact_is_not_phase4_approval": True,
            "this_artifact_is_not_demo_order_approval": True,
            "this_artifact_is_not_live_order_approval": True,
            "this_artifact_is_not_execution_adapter_approval": True,
            "this_artifact_is_not_adapter_implementation_approval": True,
            "this_artifact_is_not_execution_approval": True,
            "future_human_phase4_review_required": True,
            "future_separate_adapter_implementation_approval_required": True,
            "future_separate_demo_order_placement_approval_required": True,
            "future_separate_live_order_placement_approval_required": True,
        },
    }


def verify_h024_phase4_readiness_review_record(
    record: Mapping[str, Any],
    *,
    allowed_demo_servers: Iterable[str],
    expected_account_currency: str = "USD",
    max_risk_fraction: Decimal | str | float = Decimal("0.01"),
) -> list[str]:
    """Independently verify a Phase 4 readiness-request artifact."""

    violations: list[str] = []

    allowed_servers = {str(server) for server in allowed_demo_servers if str(server).strip()}
    if not allowed_servers:
        violations.append("missing_allowed_demo_servers")

    max_risk = _as_decimal(max_risk_fraction, "max_risk_fraction", violations)

    if record.get("schema") != PHASE4_READINESS_REVIEW_SCHEMA:
        violations.append(f"unexpected_schema:{record.get('schema')}")
    if record.get("kind") != PHASE4_READINESS_REVIEW_KIND:
        violations.append(f"unexpected_kind:{record.get('kind')}")
    if str(record.get("verdict", "")).upper() != "PASS":
        violations.append(f"verdict_not_pass:{record.get('verdict')}")
    if record.get("violations") not in ([], ()):
        violations.append("record_has_violations")
    if record.get("mode") != REVIEW_ONLY_MODE:
        violations.append(f"unexpected_mode:{record.get('mode')}")
    if record.get("review_request_status") != READY_STATUS:
        violations.append(f"unexpected_review_request_status:{record.get('review_request_status')}")

    for field_name in (
        "phase4_approved",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_adapter_approved",
        "adapter_implementation_approved",
        "execution_approved",
        "source_manual_approval_granted",
    ):
        if record.get(field_name) is not False:
            violations.append(f"{field_name}_must_be_false")

    if record.get("human_review_still_required") is not True:
        violations.append("human_review_still_required_must_be_true")

    if record.get("source_manual_checkpoint_schema") != MANUAL_APPROVAL_CHECKPOINT_SCHEMA:
        violations.append(f"unexpected_source_manual_checkpoint_schema:{record.get('source_manual_checkpoint_schema')}")
    if record.get("source_manual_checkpoint_kind") != MANUAL_APPROVAL_CHECKPOINT_KIND:
        violations.append(f"unexpected_source_manual_checkpoint_kind:{record.get('source_manual_checkpoint_kind')}")
    if record.get("source_manual_approval_status") != APPROVAL_STATUS:
        violations.append(f"unexpected_source_manual_approval_status:{record.get('source_manual_approval_status')}")
    if record.get("source_demo_execution_adapter_design_schema") != DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA:
        violations.append(
            f"unexpected_source_demo_execution_adapter_design_schema:{record.get('source_demo_execution_adapter_design_schema')}"
        )
    if record.get("source_demo_execution_adapter_design_kind") != DEMO_EXECUTION_ADAPTER_DESIGN_KIND:
        violations.append(
            f"unexpected_source_demo_execution_adapter_design_kind:{record.get('source_demo_execution_adapter_design_kind')}"
        )
    if record.get("source_demo_execution_adapter_design_status") != DESIGN_STATUS:
        violations.append(
            f"unexpected_source_demo_execution_adapter_design_status:{record.get('source_demo_execution_adapter_design_status')}"
        )

    forbidden_paths = _find_forbidden_execution_keys(record)
    if forbidden_paths:
        violations.append("record_contains_execution_like_fields:" + ",".join(forbidden_paths))

    artifact_counts = record.get("artifact_counts")
    if not isinstance(artifact_counts, Mapping):
        violations.append("missing_artifact_counts")
    else:
        for key, expected_count in EXPECTED_ARTIFACT_RECORD_COUNTS.items():
            if artifact_counts.get(key) != expected_count:
                violations.append(f"artifact_count_mismatch:{key}")

    artifact_verifications = record.get("artifact_verifications")
    if not isinstance(artifact_verifications, Mapping):
        violations.append("missing_artifact_verifications")
    else:
        for key in REQUIRED_ARTIFACT_KEYS:
            verification = artifact_verifications.get(key)
            if not isinstance(verification, Mapping):
                violations.append(f"missing_artifact_verification:{key}")
                continue
            if str(verification.get("verdict", "")).upper() != "PASS":
                violations.append(f"artifact_verification_not_pass:{key}")
            if verification.get("record_count") != EXPECTED_ARTIFACT_RECORD_COUNTS[key]:
                violations.append(f"artifact_verification_count_mismatch:{key}")

    readiness_checks = record.get("readiness_checks")
    if not isinstance(readiness_checks, Mapping):
        violations.append("missing_readiness_checks")
    else:
        for check_name in REQUIRED_READINESS_CHECKS:
            if readiness_checks.get(check_name) is not True:
                violations.append(f"readiness_check_not_true:{check_name}")

    approval_boundary = record.get("approval_boundary")
    if not isinstance(approval_boundary, Mapping):
        violations.append("missing_approval_boundary")
    else:
        for check_name in (
            "this_artifact_is_not_phase4_approval",
            "this_artifact_is_not_demo_order_approval",
            "this_artifact_is_not_live_order_approval",
            "this_artifact_is_not_execution_adapter_approval",
            "this_artifact_is_not_adapter_implementation_approval",
            "this_artifact_is_not_execution_approval",
            "future_human_phase4_review_required",
            "future_separate_adapter_implementation_approval_required",
            "future_separate_demo_order_placement_approval_required",
            "future_separate_live_order_placement_approval_required",
        ):
            if approval_boundary.get(check_name) is not True:
                violations.append(f"approval_boundary_check_not_true:{check_name}")

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

    return sorted(set(violations))


def _failure_record(
    violations: list[str],
    *,
    artifact_counts: Mapping[str, int] | None = None,
    artifact_verifications: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "schema": PHASE4_READINESS_REVIEW_SCHEMA,
        "kind": PHASE4_READINESS_REVIEW_KIND,
        "verdict": "FAIL",
        "violations": sorted(set(violations)),
        "mode": REVIEW_ONLY_MODE,
        "review_request_status": NOT_READY_STATUS,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "adapter_implementation_approved": False,
        "execution_approved": False,
        "human_review_still_required": True,
        "artifact_counts": dict(artifact_counts or {}),
        "artifact_verifications": dict(artifact_verifications or {}),
    }


def _summarize_verifications(
    artifact_verifications: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    for key in REQUIRED_ARTIFACT_KEYS:
        raw = artifact_verifications.get(key, {})
        summary[key] = {
            "verdict": str(raw.get("verdict", "")).upper(),
            "record_count": raw.get("record_count"),
            "verifier": raw.get("verifier"),
            "return_code": raw.get("return_code"),
        }
    return summary


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