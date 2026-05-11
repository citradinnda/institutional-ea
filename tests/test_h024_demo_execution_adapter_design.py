from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from quantcore.execution.h024_demo_execution_adapter_design import (
    DEMO_EXECUTION_ADAPTER_DESIGN_KIND,
    DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA,
    DESIGN_STATUS,
    build_h024_demo_execution_adapter_design,
    verify_h024_demo_execution_adapter_design_record,
)
from quantcore.execution.h024_manual_approval_checkpoint import build_h024_manual_approval_checkpoint


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


def _sample_checkpoint() -> dict:
    return build_h024_manual_approval_checkpoint(
        _sample_intent(),
        allowed_demo_servers=["Exness-MT5Trial6"],
    )


def _build(checkpoint: dict | None = None) -> dict:
    return build_h024_demo_execution_adapter_design(
        checkpoint or _sample_checkpoint(),
        allowed_demo_servers=["Exness-MT5Trial6"],
    )


def test_builds_demo_adapter_design_without_granting_approval() -> None:
    record = _build()

    assert record["schema"] == DEMO_EXECUTION_ADAPTER_DESIGN_SCHEMA
    assert record["kind"] == DEMO_EXECUTION_ADAPTER_DESIGN_KIND
    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["design_status"] == DESIGN_STATUS
    assert record["scope_boundary"]["implementation_present"] is False
    assert record["scope_boundary"]["adapter_implementation_approved"] is False
    assert record["scope_boundary"]["execution_approved"] is False
    assert record["scope_boundary"]["manual_approval_still_required"] is True

    assert verify_h024_demo_execution_adapter_design_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    ) == []


def test_rejects_source_checkpoint_that_fails_verification() -> None:
    checkpoint = _sample_checkpoint()
    checkpoint["server"] = "Exness-Real"

    record = _build(checkpoint)

    assert record["verdict"] == "FAIL"
    assert any("source_checkpoint:server_not_allowed" in violation for violation in record["violations"])


def test_rejects_execution_like_keys_in_source_checkpoint() -> None:
    checkpoint = _sample_checkpoint()
    checkpoint["ticket"] = "forbidden"

    record = _build(checkpoint)

    assert record["verdict"] == "FAIL"
    assert any("source_checkpoint_contains_execution_like_keys" in violation for violation in record["violations"])


def test_verifier_rejects_design_that_claims_implementation_approval() -> None:
    record = _build()
    record["scope_boundary"]["implementation_present"] = True
    record["scope_boundary"]["adapter_implementation_approved"] = True
    record["scope_boundary"]["execution_approved"] = True

    violations = verify_h024_demo_execution_adapter_design_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    )

    assert "scope_boundary_mismatch:implementation_present" in violations
    assert "scope_boundary_mismatch:adapter_implementation_approved" in violations
    assert "scope_boundary_mismatch:execution_approved" in violations


def test_jsonl_builder_and_verifier_accept_utf8_bom_input(tmp_path: Path) -> None:
    input_path = tmp_path / "checkpoint.jsonl"
    output_path = tmp_path / "design.jsonl"
    input_path.write_text(json.dumps(_sample_checkpoint()) + "\n", encoding="utf-8-sig")

    build_result = subprocess.run(
        [
            sys.executable,
            "scripts/build_h024_demo_execution_adapter_design_jsonl.py",
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
            "scripts/verify_h024_demo_execution_adapter_design_jsonl.py",
            str(output_path),
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-design",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert verify_result.returncode == 0, verify_result.stdout + verify_result.stderr
    assert "Design records: 1" in verify_result.stdout
    assert "Verdict: PASS" in verify_result.stdout


def test_design_module_has_no_mt5_or_trade_api_call_patterns() -> None:
    source = (ROOT / "quantcore/execution/h024_demo_execution_adapter_design.py").read_text(encoding="utf-8")

    forbidden_call_patterns = (
        "MetaTrader5",
        "import mt5",
        "from mt5",
        "OrderSend(",
        "OrderSendAsync(",
        "OrderCheck(",
        "MqlTradeRequest(",
        "MqlTradeResult(",
        "CTrade(",
    )

    for pattern in forbidden_call_patterns:
        assert pattern not in source