from __future__ import annotations

import json

import pytest

from quantcore.execution.h024_broker_request_preview_envelope import (
    APPROVAL_DECISION,
    APPROVAL_KIND,
    APPROVAL_SCHEMA,
    PREVIEW_DECISION,
    PREVIEW_KIND,
    PREVIEW_SCHEMA,
    READINESS_DECISION,
    READINESS_KIND,
    READINESS_SCHEMA,
    build_preview_construction_approval_record,
    build_preview_envelope_record,
    read_single_jsonl_record,
    verify_preview_construction_approval_record,
    verify_preview_envelope_record,
    write_single_jsonl_record,
)


def readiness_packet() -> dict:
    return {
        "schema": READINESS_SCHEMA,
        "kind": READINESS_KIND,
        "status": "READY_FOR_HUMAN_BROKER_REQUEST_CONSTRUCTION_REVIEW_NO_EXECUTION",
        "decision": READINESS_DECISION,
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
    }


def approval_record() -> dict:
    return build_preview_construction_approval_record(
        readiness_packet=readiness_packet(),
        allowed_demo_server="Exness-MT5Trial6",
    )


def order_intent() -> dict:
    return {
        "schema": "h024_order_intent_simulation_v1",
        "kind": "ORDER_INTENT_SIMULATION",
        "verdict": "PASS",
        "violations": [],
        "server": "Exness-MT5Trial6",
        "intent": {
            "intent_id": "abc123",
            "symbol": "XAUUSDm",
            "normalized_symbol": "XAUUSD",
            "side": "short",
            "timeframe": "H4",
            "entry": "4930.041",
            "stop": "5019.068",
            "final_lots": "0.01",
            "risk_fraction": "0.01",
        },
    }


def allow_state() -> dict:
    return {
        "schema": "h024_execution_safety_controls_allow_state_preflight_v1",
        "kind": "EXECUTION_SAFETY_CONTROLS_ALLOW_STATE_PREFLIGHT",
        "status": "PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL",
        "verdict": "PASS",
        "violations": [],
        "server": "Exness-MT5Trial6",
    }


def preview_record() -> dict:
    return build_preview_envelope_record(
        preview_construction_approval=approval_record(),
        order_intent_simulation=order_intent(),
        allow_state_preflight=allow_state(),
        allowed_demo_server="Exness-MT5Trial6",
    )


def test_builds_preview_construction_approval() -> None:
    record = approval_record()

    assert record["schema"] == APPROVAL_SCHEMA
    assert record["kind"] == APPROVAL_KIND
    assert record["decision"] == APPROVAL_DECISION
    assert record["verdict"] == "PASS"
    assert record["authority"]["broker_request_preview_construction_approved"] is True
    assert record["authority"]["broker_request_construction_approved"] is False


def test_approval_fails_if_readiness_packet_is_not_pass() -> None:
    packet = readiness_packet()
    packet["verdict"] = "FAIL"

    record = build_preview_construction_approval_record(
        readiness_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("readiness_packet" in v for v in record["violations"])


@pytest.mark.parametrize(
    "authority_key",
    [
        "broker_request_construction_approved",
        "execution_adapter_use_approved",
        "execution_adapter_approved",
        "broker_request_approved",
        "mt5_execution_approved",
        "terminal_mutation_approved",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_approved",
    ],
)
def test_approval_fails_if_blocked_authority_flag_is_true(authority_key: str) -> None:
    record = approval_record()
    record["authority"][authority_key] = True

    result = verify_preview_construction_approval_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(authority_key in v for v in result.violations)


def test_builds_inert_preview_envelope_from_intent() -> None:
    record = preview_record()

    assert record["schema"] == PREVIEW_SCHEMA
    assert record["kind"] == PREVIEW_KIND
    assert record["decision"] == PREVIEW_DECISION
    assert record["verdict"] == "PASS"
    assert record["preview_envelope"]["preview_envelope_constructed"] is True
    assert record["preview_envelope"]["not_mt5_request"] is True
    assert record["preview_envelope"]["not_broker_request"] is True
    assert record["preview_envelope"]["not_order_payload"] is True
    assert record["mutation_safety"]["transport_dispatch_attempted"] is False


def test_preview_attaches_stable_idempotency_key() -> None:
    first = preview_record()
    second = preview_record()

    assert first["preview_envelope"]["idempotency_key"].startswith("h024-preview-")
    assert first["preview_envelope"]["idempotency_key"] == second["preview_envelope"]["idempotency_key"]


@pytest.mark.parametrize(
    "mutation_key",
    [
        "broker_request_constructed",
        "mt5_request_constructed",
        "order_payload_constructed",
        "transport_dispatch_attempted",
        "dispatch_attempted",
        "terminal_mutated",
        "broker_state_mutated",
    ],
)
def test_preview_fails_if_any_mutation_or_dispatch_flag_is_true(mutation_key: str) -> None:
    record = preview_record()
    record["mutation_safety"][mutation_key] = True

    result = verify_preview_envelope_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(mutation_key in v for v in result.violations)


@pytest.mark.parametrize(
    "required_true_key",
    [
        "preview_envelope_constructed",
        "verified_intent_consumed",
        "h020_sizing_consumed_not_reinterpreted",
        "idempotency_key_attached",
        "kill_switch_allow_state_required",
        "request_construction_refused_beyond_preview",
    ],
)
def test_preview_fails_if_required_preview_flag_is_false(required_true_key: str) -> None:
    record = preview_record()
    record["preview_envelope"][required_true_key] = False

    result = verify_preview_envelope_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(required_true_key in v for v in result.violations)


def test_preview_fails_if_approval_is_not_pass() -> None:
    approval = approval_record()
    approval["verdict"] = "FAIL"

    record = build_preview_envelope_record(
        preview_construction_approval=approval,
        order_intent_simulation=order_intent(),
        allow_state_preflight=allow_state(),
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("preview_construction_approval" in v for v in record["violations"])


def test_preview_fails_wrong_demo_server() -> None:
    result = verify_preview_envelope_record(
        preview_record(),
        allowed_demo_server="WrongServer",
        require_pass=True,
    )

    assert not result.ok
    assert "allowed demo server not observed: WrongServer" in result.violations


def test_round_trips_approval_and_preview_jsonl(tmp_path) -> None:
    approval = approval_record()
    preview = preview_record()

    approval_path = tmp_path / "approval.jsonl"
    preview_path = tmp_path / "preview.jsonl"

    write_single_jsonl_record(approval_path, approval)
    write_single_jsonl_record(preview_path, preview)

    assert read_single_jsonl_record(approval_path) == json.loads(json.dumps(approval, sort_keys=True))
    assert read_single_jsonl_record(preview_path) == json.loads(json.dumps(preview, sort_keys=True))