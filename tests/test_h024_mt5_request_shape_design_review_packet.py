from __future__ import annotations

from quantcore.execution.h024_broker_request_draft_review_human_decision import (
    DraftReviewHumanDecisionInputs,
    build_draft_review_human_decision,
)
from quantcore.execution.h024_mt5_request_shape_design_review_packet import (
    Mt5RequestShapeDesignReviewInputs,
    build_mt5_request_shape_design_review_packet,
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
        "canonical_conceptual_review_fields": {
            "normalized_symbol": "XAUUSD",
            "runtime_symbol": "XAUUSDm",
            "conceptual_side": "sell_review_only",
            "h020_final_lots": 0.01,
            "entry_reference_price": 4930.041,
            "protective_stop_reference_price": 5019.068,
            "sizing_source": "H020_CONSUMED_NOT_REINTERPRETED",
            "execution_shape": "NOT_MT5_REQUEST_NOT_ORDER_PAYLOAD_NOT_DISPATCHABLE",
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
            "actual_broker_request_constructed": False,
            "mt5_request_constructed": False,
            "order_payload_constructed": False,
            "dispatch_attempted": False,
            "terminal_mutated": False,
            "broker_state_mutated": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_approved": False,
        },
    }


def _valid_human_decision(draft: dict) -> dict:
    return build_draft_review_human_decision(
        DraftReviewHumanDecisionInputs(
            draft_envelope={
                **draft,
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
                "authority_flags": {
                    **draft["authority_flags"],
                    "actual_broker_request_construction_approved": False,
                    "mt5_request_construction_approved": False,
                    "order_payload_construction_approved": False,
                    "execution_capable_adapter_use_approved": False,
                    "transport_dispatch_attempted": False,
                    "order_payload_constructed": False,
                },
            },
            allowed_demo_server="Exness-MT5Trial6",
        )
    )


def test_mt5_request_shape_design_review_packet_is_design_only() -> None:
    draft = _valid_draft_envelope()
    human_decision = _valid_human_decision(draft)

    record = build_mt5_request_shape_design_review_packet(
        Mt5RequestShapeDesignReviewInputs(
            draft_review_human_decision=human_decision,
            draft_envelope=draft,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["design_scope"]["design_review_only"] is True
    assert record["design_scope"]["describes_future_request_shape_constraints"] is True
    assert record["design_scope"]["constructs_mt5_request"] is False
    assert record["design_scope"]["constructs_order_payload"] is False
    assert record["design_scope"]["constructs_actual_broker_request"] is False
    assert record["design_scope"]["dispatches_transport"] is False
    assert record["design_scope"]["approves_execution"] is False
    assert record["future_shape_constraints"]["must_consume_h020_sizing_without_reinterpretation"] is True
    assert record["future_shape_constraints"]["must_not_import_or_call_metatrader5"] is True
    assert record["authority_flags"]["mt5_request_shape_construction_approved"] is False
    assert record["authority_flags"]["mt5_request_constructed"] is False
    assert record["authority_flags"]["order_payload_constructed"] is False
    assert record["authority_flags"]["execution_approved"] is False


def test_mt5_request_shape_design_review_packet_fails_without_human_decision_approval() -> None:
    draft = _valid_draft_envelope()
    human_decision = _valid_human_decision(draft)
    human_decision["approved_scope"]["may_prepare_mt5_request_shape_design_review"] = False

    record = build_mt5_request_shape_design_review_packet(
        Mt5RequestShapeDesignReviewInputs(
            draft_review_human_decision=human_decision,
            draft_envelope=draft,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "mt5_request_shape_design_review_not_allowed" in record["violations"]