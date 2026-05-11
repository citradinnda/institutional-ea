from __future__ import annotations

from quantcore.execution.h024_mt5_request_shape_preview_review_human_decision import (
    Mt5RequestShapePreviewReviewHumanDecisionInputs,
    build_mt5_request_shape_preview_review_human_decision,
)


def _valid_shape_preview() -> dict:
    return {
        "schema": "h024_mt5_request_shape_preview_envelope_v1",
        "kind": "MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE",
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
        "identity": {"shape_preview_idempotency_key": "0" * 64},
        "consumption_flags": {
            "design_review_packet_consumed": True,
            "reviewed_draft_summary_consumed": True,
            "h020_sizing_consumed_not_reinterpreted": True,
            "kill_switch_allow_state_required": True,
            "idempotency_key_carried_forward": True,
        },
        "shape_preview_flags": {
            "shape_preview_envelope_constructed": True,
            "shape_preview_only": True,
            "not_actual_mt5_request": True,
            "not_actual_broker_request": True,
            "not_order_payload": True,
            "not_dispatchable": True,
            "contains_no_transport_instruction": True,
            "contains_no_terminal_mutation_instruction": True,
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_draft_review_approved": True,
            "mt5_request_shape_design_review_packet_constructed": True,
            "mt5_request_shape_construction_approved": True,
            "mt5_request_shape_preview_envelope_constructed": True,
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


def test_shape_preview_review_decision_allows_readiness_packet_only() -> None:
    record = build_mt5_request_shape_preview_review_human_decision(
        Mt5RequestShapePreviewReviewHumanDecisionInputs(
            shape_preview_envelope=_valid_shape_preview(),
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["approved_scope"]["may_review_inert_mt5_request_shape_preview"] is True
    assert record["approved_scope"]["may_prepare_demo_order_readiness_packet"] is True
    assert record["approved_scope"]["may_place_demo_order"] is False
    assert record["approved_scope"]["may_dispatch_transport"] is False
    assert record["approved_scope"]["may_execute"] is False
    assert record["authority_flags"]["demo_order_readiness_packet_allowed"] is True
    assert record["authority_flags"]["demo_order_canary_approved"] is False
    assert record["authority_flags"]["demo_order_placement_approved"] is False
    assert record["authority_flags"]["execution_approved"] is False


def test_shape_preview_review_decision_fails_if_shape_preview_allows_dispatch() -> None:
    preview = _valid_shape_preview()
    preview["authority_flags"]["dispatch_attempted"] = True

    record = build_mt5_request_shape_preview_review_human_decision(
        Mt5RequestShapePreviewReviewHumanDecisionInputs(
            shape_preview_envelope=preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "shape_preview_forbidden_authority_not_false_dispatch_attempted" in record["violations"]
    assert record["approved_scope"]["may_prepare_demo_order_readiness_packet"] is False