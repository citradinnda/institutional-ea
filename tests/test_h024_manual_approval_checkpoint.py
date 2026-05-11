from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from quantcore.execution.h024_manual_approval_checkpoint import (
    APPROVAL_STATUS,
    MANUAL_APPROVAL_CHECKPOINT_KIND,
    MANUAL_APPROVAL_CHECKPOINT_SCHEMA,
    build_h024_manual_approval_checkpoint,
    verify_h024_manual_approval_checkpoint_record,
)


ROOT = Path(__file__).resolve().parents[1]


def _sample_intent() -> dict:
    return {
        "schema": "h024_order_intent_simulation_v1",
        "kind": "ORDER_INTENT_SIMULATION_REVIEW_ONLY",
        "verdict": "PASS",
        "violations": [],
        "mode": "log_only_no_execution",
        "is_broker_request": False,
        "execution_approved": False,
        "preflight_schema": "h024_broker_metadata_preflight_v1",
        "preflight_kind": "BROKER_METADATA_PREFLIGHT_REVIEW_ONLY",
        "server": "Exness-MT5Trial6",
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
        "source_reason": "unit_test_would_open",
        "source_timestamp": "2026.05.11 07:45:49",
        "broker_metadata": {
            "tick_size": 0.001,
            "tick_value": 0.1,
            "min_volume": 0.01,
            "max_volume": 200.0,
            "volume_step": 0.01,
            "volume_digits": 2,
            "price_digits": 3,
            "spread_points": 16.0,
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


def _build(intent: dict | None = None) -> dict:
    return build_h024_manual_approval_checkpoint(
        intent or _sample_intent(),
        allowed_demo_servers=["Exness-MT5Trial6"],
    )


def test_builds_pending_manual_approval_checkpoint_from_valid_intent() -> None:
    record = _build()

    assert record["schema"] == MANUAL_APPROVAL_CHECKPOINT_SCHEMA
    assert record["kind"] == MANUAL_APPROVAL_CHECKPOINT_KIND
    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["approval_status"] == APPROVAL_STATUS
    assert record["manual_approval_required"] is True
    assert record["manual_approval_granted"] is False
    assert record["execution_approved"] is False
    assert record["is_broker_request"] is False
    assert record["side"] == "short"
    assert record["review_only_intent_action"] == "SELL_MARKET_REVIEW_ONLY"

    assert verify_h024_manual_approval_checkpoint_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    ) == []


def test_rejects_source_intent_that_fails_independent_verifier() -> None:
    intent = _sample_intent()
    intent["server"] = "Exness-Real"

    record = _build(intent)

    assert record["verdict"] == "FAIL"
    assert any("source_intent:server_not_allowed" in violation for violation in record["violations"])


def test_rejects_execution_like_fields_in_source_intent() -> None:
    intent = _sample_intent()
    intent["ticket"] = "forbidden"

    record = _build(intent)

    assert record["verdict"] == "FAIL"
    assert any("source_intent_contains_execution_like_fields" in violation for violation in record["violations"])


def test_verifier_rejects_checkpoint_that_claims_approval() -> None:
    record = _build()
    record["manual_approval_granted"] = True
    record["approval_status"] = "APPROVED"

    violations = verify_h024_manual_approval_checkpoint_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    )

    assert "manual_approval_granted_must_be_false" in violations
    assert "unexpected_approval_status:APPROVED" in violations


def test_verifier_rejects_missing_required_manual_approval_items() -> None:
    record = _build()
    record["required_manual_approval_items"] = []

    violations = verify_h024_manual_approval_checkpoint_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    )

    assert "required_manual_approval_items_mismatch" in violations


def test_jsonl_builder_and_verifier_accept_utf8_bom_input(tmp_path: Path) -> None:
    input_path = tmp_path / "intent.jsonl"
    output_path = tmp_path / "checkpoint.jsonl"
    input_path.write_text(json.dumps(_sample_intent()) + "\n", encoding="utf-8-sig")

    build_result = subprocess.run(
        [
            sys.executable,
            "scripts/build_h024_manual_approval_checkpoint_jsonl.py",
            str(input_path),
            str(output_path),
            "--allowed-demo-server",
            "Exness-MT5Trial6",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert build_result.returncode == 0, build_result.stdout + build_result.stderr
    assert "Verdict: PASS" in build_result.stdout

    verify_result = subprocess.run(
        [
            sys.executable,
            "scripts/verify_h024_manual_approval_checkpoint_jsonl.py",
            str(output_path),
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-checkpoint",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert verify_result.returncode == 0, verify_result.stdout + verify_result.stderr
    assert "Manual approval checkpoint records: 1" in verify_result.stdout
    assert "Verdict: PASS" in verify_result.stdout