from __future__ import annotations

from quantcore.execution.h024_broker_request_draft_review_human_decision import (
    DraftReviewHumanDecisionInputs,
    build_draft_review_human_decision,
)


def _valid_draft_envelope() -> dict:
    return {
        "schema": "h024_broker_request_draft_envelope_v1",
        "kind": "BROKER_REQUEST_DRAFT_ENVELOPE",
        "status": "INERT_BROKER_REQUEST_DRAFT_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH",
        "decision": "CONSTRUCT_INERT_BROKER_REQUEST_DRAFT_ONLY_REFUSE_DISPATCH",
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
        "identity": {
            "preview_idempotency_key_carried_forward": "preview-key",
            "draft_idempotency_key": "0" * 64,
        },
        "consumption_flags": {
            "preview_envelope_consumed": True,
            "verified_intent_consumed": True,
            "h020_sizing_consumed_not_reinterpreted": True,
            "kill_switch_allow_state_required": True,
            "idempotency_key_carried_forward": True,
        },
        "draft_flags": {
            "draft_is_non_dispatchable": True,
            "not_mt5_request": True,
            "not_broker_request": True,
            "not_order_payload": True,
            "review_envelope_only": True,
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_preview_construction_approved": True,
            "broker_request_preview_envelope_constructed": True,
            "broker_request_draft_construction_approved": True,
            "broker_request_draft_envelope_constructed": True,
            "actual_broker_request_construction_approved": False,
            "actual_broker_request_constructed": False,
            "mt5_request_construction_approved": False,
            "mt5_request_constructed": False,
            "order_payload_construction_approved": False,
            "order_payload_constructed": False,
            "execution_capable_adapter_use_approved": False,
            "transport_dispatch_attempted": False,
            "dispatch_attempted": False,
            "terminal_mutated": False,
            "broker_state_mutated": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_approved": False,
        },
    }


def test_draft_review_human_decision_approves_review_and_design_review_only() -> None:
    record = build_draft_review_human_decision(
        DraftReviewHumanDecisionInputs(
            draft_envelope=_valid_draft_envelope(),
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["approved_scope"]["may_review_inert_canonical_broker_request_draft"] is True
    assert record["approved_scope"]["may_prepare_mt5_request_shape_design_review"] is True
    assert record["approved_scope"]["may_construct_actual_broker_request"] is False
    assert record["approved_scope"]["may_construct_mt5_request"] is False
    assert record["approved_scope"]["may_construct_order_payload"] is False
    assert record["approved_scope"]["may_dispatch_transport"] is False
    assert record["approved_scope"]["may_execute"] is False
    assert record["authority_flags"]["broker_request_draft_review_approved"] is True
    assert record["authority_flags"]["mt5_request_shape_construction_approved"] is False
    assert record["authority_flags"]["mt5_request_constructed"] is False
    assert record["authority_flags"]["execution_approved"] is False


def test_draft_review_human_decision_fails_if_draft_has_execution_approval() -> None:
    draft = _valid_draft_envelope()
    draft["authority_flags"]["execution_approved"] = True

    record = build_draft_review_human_decision(
        DraftReviewHumanDecisionInputs(
            draft_envelope=draft,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "draft_envelope_forbidden_authority_not_false_execution_approved" in record["violations"]
    assert record["approved_scope"]["may_prepare_mt5_request_shape_design_review"] is False