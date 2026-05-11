from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from quantcore.execution.h024_order_intent_simulation import (
    ORDER_INTENT_SIMULATION_KIND,
    ORDER_INTENT_SIMULATION_SCHEMA,
    build_h024_order_intent_simulation,
    verify_h024_order_intent_simulation_record,
)


ROOT = Path(__file__).resolve().parents[1]


def _sample_preflight() -> dict:
    return {
        "schema": "h024_broker_metadata_preflight_v1",
        "kind": "BROKER_METADATA_PREFLIGHT_REVIEW_ONLY",
        "verdict": "PASS",
        "violations": [],
        "mode": "log_only_no_execution",
        "server": "Exness-MT5Trial6",
        "account_currency": "USD",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "side": "short",
        "entry": 4930.041,
        "stop": 5019.068,
        "volume": 0.01,
        "risk_fraction": 0.01,
        "risk_usd": 100.0,
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
    }


def _build(record: dict | None = None) -> dict:
    return build_h024_order_intent_simulation(
        record or _sample_preflight(),
        allowed_demo_servers=["Exness-MT5Trial6"],
    )


def test_builds_review_only_order_intent_simulation_from_valid_preflight() -> None:
    record = _build()

    assert record["schema"] == ORDER_INTENT_SIMULATION_SCHEMA
    assert record["kind"] == ORDER_INTENT_SIMULATION_KIND
    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["mode"] == "log_only_no_execution"
    assert record["is_broker_request"] is False
    assert record["execution_approved"] is False
    assert record["review_only_intent_action"] == "SELL_MARKET_REVIEW_ONLY"
    assert record["estimated_loss_usd"] == pytest.approx(89.027)

    assert verify_h024_order_intent_simulation_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    ) == []


@pytest.mark.parametrize(
    ("field", "value", "expected_violation"),
    [
        ("schema", "wrong_schema", "unexpected_preflight_schema"),
        ("kind", "WRONG_KIND", "unexpected_preflight_kind"),
        ("server", "Exness-Real", "server_not_allowed"),
        ("account_currency", "EUR", "unexpected_account_currency"),
        ("mode", "execution_enabled", "unexpected_mode"),
        ("normalized_symbol", "EURUSD", "unsupported_normalized_symbol"),
        ("side", "flat", "unsupported_side"),
    ],
)
def test_rejects_invalid_identity_and_safety_fields(field: str, value: object, expected_violation: str) -> None:
    preflight = _sample_preflight()
    preflight[field] = value

    record = _build(preflight)

    assert record["verdict"] == "FAIL"
    assert any(expected_violation in violation for violation in record["violations"])


def test_rejects_invalid_short_stop_geometry() -> None:
    preflight = _sample_preflight()
    preflight["stop"] = 4900.0

    record = _build(preflight)

    assert record["verdict"] == "FAIL"
    assert "invalid_short_stop_geometry" in record["violations"]


def test_rejects_tick_misalignment() -> None:
    preflight = _sample_preflight()
    preflight["entry"] = 4930.0415

    record = _build(preflight)

    assert record["verdict"] == "FAIL"
    assert "entry_not_tick_aligned" in record["violations"]


def test_rejects_volume_step_misalignment() -> None:
    preflight = _sample_preflight()
    preflight["volume"] = 0.015

    record = _build(preflight)

    assert record["verdict"] == "FAIL"
    assert "volume_not_step_aligned" in record["violations"]
    assert "volume_exceeds_volume_digits" in record["violations"]


def test_rejects_loss_above_risk_budget() -> None:
    preflight = _sample_preflight()
    preflight["risk_usd"] = 1.0

    record = _build(preflight)

    assert record["verdict"] == "FAIL"
    assert "estimated_loss_exceeds_risk_usd" in record["violations"]


def test_rejects_execution_like_fields_in_preflight() -> None:
    preflight = _sample_preflight()
    preflight["ticket"] = "forbidden"

    record = _build(preflight)

    assert record["verdict"] == "FAIL"
    assert any("preflight_contains_execution_like_fields" in violation for violation in record["violations"])


def test_verifier_rejects_execution_like_fields_in_intent_record() -> None:
    record = _build()
    record["deal"] = "forbidden"

    violations = verify_h024_order_intent_simulation_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    )

    assert any("record_contains_execution_like_fields" in violation for violation in violations)


def test_jsonl_builder_and_verifier_accept_utf8_bom_input(tmp_path: Path) -> None:
    input_path = tmp_path / "preflight.jsonl"
    output_path = tmp_path / "intent.jsonl"
    input_path.write_text(json.dumps(_sample_preflight()) + "\n", encoding="utf-8-sig")

    build_result = subprocess.run(
        [
            sys.executable,
            "scripts/build_h024_order_intent_simulation_jsonl.py",
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
            "scripts/verify_h024_order_intent_simulation_jsonl.py",
            str(output_path),
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-intent",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert verify_result.returncode == 0, verify_result.stdout + verify_result.stderr
    assert "Order-intent simulation records: 1" in verify_result.stdout
    assert "Verdict: PASS" in verify_result.stdout
def test_build_accepts_nested_real_report_style_aliases() -> None:
    preflight = {
        "schema": "h024_broker_metadata_preflight_v1",
        "kind": "BROKER_METADATA_PREFLIGHT_REVIEW_ONLY",
        "verdict": "PASS",
        "violations": [],
        "account_context": {
            "server": "Exness-MT5Trial6",
            "currency": "USD",
        },
        "source_plan": {
            "mode": "log_only_no_execution",
            "runtime_symbol": "XAUUSDm",
            "model_symbol": "XAUUSD",
            "side": "short",
            "entry_price": 4930.041,
            "stop_loss": 5019.068,
            "final_lots": 0.01,
            "final_risk_fraction": 0.01,
            "risk_amount_usd": 100.0,
            "runtime_reason": "nested_alias_would_open",
            "runtime_timestamp": "2026.05.11 07:45:49",
        },
        "metadata_snapshot": {
            "tick_size": 0.001,
            "tick_value_usd_per_lot": 0.1,
            "volume_min": 0.01,
            "volume_max": 200.0,
            "volume_step": 0.01,
            "volume_digits": 2,
            "price_digits": 3,
            "spread_points": 16.0,
        },
    }

    record = build_h024_order_intent_simulation(
        preflight,
        allowed_demo_servers=["Exness-MT5Trial6"],
    )

    assert record["verdict"] == "PASS"
    assert verify_h024_order_intent_simulation_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    ) == []

def test_build_accepts_wrapped_preflight_schema_kind_and_derived_risk_fraction() -> None:
    preflight = {
        "wrapper": {
            "preflight_record_schema": "h024_broker_metadata_preflight_v1",
            "preflight_record_type": "H024_BROKER_METADATA_PREFLIGHT_REVIEW_ONLY",
            "status": "PASS",
        },
        "account": {
            "server_name": "Exness-MT5Trial6",
            "deposit_currency": "USD",
            "account_balance_usd": 10000.0,
        },
        "source": {
            "runtime_symbol": "XAUUSDm",
            "canonical_symbol": "XAUUSD",
            "side": "short",
            "entry_price": 4930.041,
            "stop_loss": 5019.068,
            "final_volume_lots": 0.01,
            "risk_amount_usd": 100.0,
            "runtime_reason": "wrapped_would_open",
            "runtime_timestamp": "2026.05.11 07:45:49",
        },
        "metadata": {
            "tick_size": 0.001,
            "tick_value_usd_per_lot": 0.1,
            "volume_min": 0.01,
            "volume_max": 200.0,
            "volume_step": 0.01,
            "volume_digits": 2,
            "price_digits": 3,
            "spread_points": 16.0,
        },
    }

    record = build_h024_order_intent_simulation(
        preflight,
        allowed_demo_servers=["Exness-MT5Trial6"],
    )

    assert record["verdict"] == "PASS"
    assert record["risk_fraction"] == 0.01
    assert verify_h024_order_intent_simulation_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    ) == []

def test_build_accepts_broker_style_sell_side_alias() -> None:
    preflight = _sample_preflight()
    preflight["side"] = "SELL"

    record = build_h024_order_intent_simulation(
        preflight,
        allowed_demo_servers=["Exness-MT5Trial6"],
    )

    assert record["verdict"] == "PASS"
    assert record["side"] == "short"
    assert record["review_only_intent_action"] == "SELL_MARKET_REVIEW_ONLY"
    assert verify_h024_order_intent_simulation_record(
        record,
        allowed_demo_servers=["Exness-MT5Trial6"],
    ) == []
