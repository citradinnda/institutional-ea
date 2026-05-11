from __future__ import annotations

from copy import deepcopy

from quantcore.execution.h024_demo_execution_adapter_design import build_h024_demo_execution_adapter_design
from quantcore.execution.h024_manual_approval_checkpoint import (
    APPROVAL_STATUS,
    MANUAL_APPROVAL_CHECKPOINT_KIND,
    MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
    REQUIRED_MANUAL_APPROVAL_ITEMS,
)
from quantcore.execution.h024_order_intent_simulation import (
    ORDER_INTENT_SIMULATION_KIND,
    ORDER_INTENT_SIMULATION_SCHEMA,
    REVIEW_ONLY_MODE,
)
from quantcore.execution.h024_phase4_readiness_review import (
    BROKER_METADATA_PREFLIGHT_ARTIFACT,
    DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT,
    DEMO_ORDER_PLANS_ARTIFACT,
    DRY_RUN_REQUESTS_ARTIFACT,
    MANUAL_APPROVAL_CHECKPOINT_ARTIFACT,
    ORDER_INTENT_SIMULATION_ARTIFACT,
    PHASE4_READINESS_REVIEW_KIND,
    PHASE4_READINESS_REVIEW_SCHEMA,
    READY_STATUS,
    REQUIRED_ARTIFACT_KEYS,
    build_h024_phase4_readiness_review,
    verify_h024_phase4_readiness_review_record,
)


ALLOWED_SERVER = "Exness-MT5Trial6"


def _manual_checkpoint_record() -> dict:
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
        "server": ALLOWED_SERVER,
        "account_currency": "USD",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "side": "short",
        "review_only_intent_action": "SELL_MARKET_REVIEW_ONLY",
        "entry": 4930.041,
        "stop": 5019.068,
        "volume": 0.01,
        "risk_fraction": 0.01,
        "risk_usd": 100.0,
        "estimated_loss_usd": 89.027,
        "source_reason": "h024_fixture_would_open",
        "source_timestamp": "2026.05.11 07:45:49",
        "broker_metadata": {
            "tick_size": 0.001,
            "tick_value": 0.1,
            "min_volume": 0.01,
            "max_volume": 200.0,
            "volume_step": 0.01,
            "volume_digits": 2,
            "price_digits": 3,
            "spread_points": 200,
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


def _artifact_records() -> dict:
    manual = _manual_checkpoint_record()
    design = build_h024_demo_execution_adapter_design(
        manual,
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    assert design["verdict"] == "PASS"

    return {
        DRY_RUN_REQUESTS_ARTIFACT: [{"schema": "dry_run_request_fixture", "verdict": "PASS"}],
        DEMO_ORDER_PLANS_ARTIFACT: [{"schema": "demo_order_plan_fixture", "verdict": "PASS"}],
        BROKER_METADATA_PREFLIGHT_ARTIFACT: [{"schema": "broker_metadata_preflight_fixture", "verdict": "PASS"}],
        ORDER_INTENT_SIMULATION_ARTIFACT: [{"schema": "order_intent_simulation_fixture", "verdict": "PASS"}],
        MANUAL_APPROVAL_CHECKPOINT_ARTIFACT: [manual],
        DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT: [design],
    }


def _artifact_verifications() -> dict:
    return {
        key: {
            "verdict": "PASS",
            "record_count": 1,
            "verifier": f"verify_{key}.py",
            "return_code": 0,
            "violations": [],
        }
        for key in REQUIRED_ARTIFACT_KEYS
    }


def test_build_phase4_readiness_review_passes_without_granting_approval() -> None:
    record = build_h024_phase4_readiness_review(
        _artifact_records(),
        artifact_verifications=_artifact_verifications(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["schema"] == PHASE4_READINESS_REVIEW_SCHEMA
    assert record["kind"] == PHASE4_READINESS_REVIEW_KIND
    assert record["verdict"] == "PASS"
    assert record["review_request_status"] == READY_STATUS
    assert record["phase4_approved"] is False
    assert record["demo_order_placement_approved"] is False
    assert record["live_order_placement_approved"] is False
    assert record["execution_adapter_approved"] is False
    assert record["adapter_implementation_approved"] is False
    assert record["execution_approved"] is False
    assert record["human_review_still_required"] is True
    assert record["source_chain_summary"]["server"] == ALLOWED_SERVER
    assert record["source_chain_summary"]["normalized_symbol"] == "XAUUSD"

    assert verify_h024_phase4_readiness_review_record(record, allowed_demo_servers=[ALLOWED_SERVER]) == []


def test_build_phase4_readiness_review_rejects_manual_approval_granted() -> None:
    artifacts = _artifact_records()
    artifacts[MANUAL_APPROVAL_CHECKPOINT_ARTIFACT][0]["manual_approval_granted"] = True

    record = build_h024_phase4_readiness_review(
        artifacts,
        artifact_verifications=_artifact_verifications(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["verdict"] == "FAIL"
    assert any("manual_approval_granted_must_be_false" in violation for violation in record["violations"])
    assert record["phase4_approved"] is False
    assert record["execution_approved"] is False


def test_build_phase4_readiness_review_rejects_failed_independent_verifier() -> None:
    verifications = _artifact_verifications()
    verifications[DEMO_ORDER_PLANS_ARTIFACT]["verdict"] = "FAIL"
    verifications[DEMO_ORDER_PLANS_ARTIFACT]["violations"] = ["fixture_failure"]

    record = build_h024_phase4_readiness_review(
        _artifact_records(),
        artifact_verifications=verifications,
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["verdict"] == "FAIL"
    assert any(f"independent_verifier_not_pass:{DEMO_ORDER_PLANS_ARTIFACT}" in violation for violation in record["violations"])
    assert any(
        f"independent_verifier_reported_violations:{DEMO_ORDER_PLANS_ARTIFACT}" in violation
        for violation in record["violations"]
    )


def test_build_phase4_readiness_review_requires_one_record_per_artifact() -> None:
    artifacts = _artifact_records()
    artifacts[DRY_RUN_REQUESTS_ARTIFACT] = []

    record = build_h024_phase4_readiness_review(
        artifacts,
        artifact_verifications=_artifact_verifications(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )

    assert record["verdict"] == "FAIL"
    assert any(f"artifact_record_count_mismatch:{DRY_RUN_REQUESTS_ARTIFACT}" in violation for violation in record["violations"])


def test_verify_phase4_readiness_review_rejects_any_approval_flip() -> None:
    record = build_h024_phase4_readiness_review(
        _artifact_records(),
        artifact_verifications=_artifact_verifications(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(record)
    mutated["phase4_approved"] = True

    violations = verify_h024_phase4_readiness_review_record(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert "phase4_approved_must_be_false" in violations


def test_verify_phase4_readiness_review_rejects_execution_like_keys() -> None:
    record = build_h024_phase4_readiness_review(
        _artifact_records(),
        artifact_verifications=_artifact_verifications(),
        allowed_demo_servers=[ALLOWED_SERVER],
    )
    mutated = deepcopy(record)
    mutated["mql_trade_request"] = {"symbol": "XAUUSDm"}

    violations = verify_h024_phase4_readiness_review_record(mutated, allowed_demo_servers=[ALLOWED_SERVER])

    assert any(violation.startswith("record_contains_execution_like_fields:") for violation in violations)