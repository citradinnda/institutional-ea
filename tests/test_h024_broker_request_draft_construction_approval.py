from __future__ import annotations

from quantcore.execution.h024_broker_request_draft_construction_approval import (
    DraftConstructionApprovalInputs,
    build_draft_construction_approval,
)


def _valid_preview_envelope() -> dict:
    return {
        "schema": "h024_broker_request_preview_envelope_v1",
        "kind": "BROKER_REQUEST_PREVIEW_ENVELOPE",
        "status": "PREVIEW_ENVELOPE_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH",
        "decision": "CONSTRUCT_PREVIEW_ENVELOPE_ONLY_REFUSE_DISPATCH",
        "allowed_demo_server": "Exness-MT5Trial6",
        "preview_idempotency_key": "preview-key",
        "consumption_flags": {
            "verified_intent_consumed": True,
            "h020_sizing_consumed_not_reinterpreted": True,
            "kill_switch_allow_state_required": True,
        },
        "draft_flags": {
            "not_mt5_request": True,
            "not_order_payload": True,
        },
        "authority_flags": {
            "actual_broker_request_constructed": False,
            "broker_request_constructed": False,
            "mt5_request_constructed": False,
            "order_payload_constructed": False,
            "transport_dispatch_attempted": False,
            "dispatch_attempted": False,
            "terminal_mutated": False,
            "broker_state_mutated": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_approved": False,
        },
    }


def test_draft_construction_approval_passes_for_valid_preview_envelope() -> None:
    record = build_draft_construction_approval(
        DraftConstructionApprovalInputs(
            preview_envelope=_valid_preview_envelope(),
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["approved_scope"]["may_construct_inert_canonical_broker_request_draft_envelope"] is True
    assert record["approved_scope"]["may_construct_actual_broker_request"] is False
    assert record["approved_scope"]["may_construct_mt5_request"] is False
    assert record["approved_scope"]["may_construct_order_payload"] is False
    assert record["approved_scope"]["may_dispatch_transport"] is False
    assert record["approved_scope"]["may_execute"] is False
    assert record["authority_flags"]["broker_request_draft_construction_approved"] is True
    assert record["authority_flags"]["actual_broker_request_constructed"] is False
    assert record["authority_flags"]["mt5_request_constructed"] is False
    assert record["authority_flags"]["order_payload_constructed"] is False


def test_draft_construction_approval_fails_if_preview_envelope_contains_execution_authority() -> None:
    preview = _valid_preview_envelope()
    preview["authority_flags"]["execution_approved"] = True

    record = build_draft_construction_approval(
        DraftConstructionApprovalInputs(
            preview_envelope=preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "preview_envelope_forbidden_true_execution_approved" in record["violations"]
    assert record["approved_scope"]["may_construct_inert_canonical_broker_request_draft_envelope"] is False


def test_draft_construction_approval_fails_without_idempotency_key() -> None:
    preview = _valid_preview_envelope()
    del preview["preview_idempotency_key"]

    record = build_draft_construction_approval(
        DraftConstructionApprovalInputs(
            preview_envelope=preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "preview_envelope_missing_idempotency_key" in record["violations"]