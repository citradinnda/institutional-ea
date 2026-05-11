from __future__ import annotations

from quantcore.execution.h024_demo_order_readiness_packet import (
    DemoOrderReadinessPacketInputs,
    build_demo_order_readiness_packet,
)
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
        },
        "inert_terminal_request_shape_preview": {
            "field_set_kind": "INERT_TERMINAL_REQUEST_SHAPE_REVIEW_FIELDS_NOT_SENDABLE",
            "instrument_identity_review": {"normalized_symbol": "XAUUSD", "runtime_symbol": "XAUUSDm"},
            "direction_review": {"terminal_direction_label_review_only": "SELL_DIRECTION_REVIEW_ONLY"},
            "quantity_review": {"h020_final_lots": 0.01, "sizing_source": "H020_CONSUMED_NOT_REINTERPRETED"},
            "price_reference_review": {
                "entry_reference_price": 4930.041,
                "protective_stop_reference_price": 5019.068,
                "reference_only_not_sendable_instruction": True,
            },
            "transport_review": {"dispatch_instruction_absent": True, "non_dispatchable": True},
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


def _human_decision(shape_preview: dict) -> dict:
    return build_mt5_request_shape_preview_review_human_decision(
        Mt5RequestShapePreviewReviewHumanDecisionInputs(
            shape_preview_envelope={
                **shape_preview,
                "shape_preview_flags": {
                    **shape_preview["shape_preview_flags"],
                    "contains_no_transport_instruction": True,
                    "contains_no_terminal_mutation_instruction": True,
                },
            },
            allowed_demo_server="Exness-MT5Trial6",
        )
    )


def test_demo_order_readiness_packet_requests_review_without_order_authority() -> None:
    shape_preview = _valid_shape_preview()
    human_decision = _human_decision(shape_preview)

    record = build_demo_order_readiness_packet(
        DemoOrderReadinessPacketInputs(
            shape_preview_review_human_decision=human_decision,
            shape_preview_envelope=shape_preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["readiness_scope"]["packet_is_review_only"] is True
    assert record["readiness_scope"]["requests_human_demo_order_canary_review"] is True
    assert record["readiness_scope"]["approves_demo_order_canary"] is False
    assert record["readiness_scope"]["approves_demo_order_placement"] is False
    assert record["readiness_scope"]["constructs_mt5_request"] is False
    assert record["readiness_scope"]["constructs_order_payload"] is False
    assert record["readiness_scope"]["dispatches_transport"] is False
    assert record["readiness_scope"]["approves_execution"] is False
    assert record["authority_flags"]["demo_order_canary_review_requested"] is True
    assert record["authority_flags"]["demo_order_canary_approved"] is False
    assert record["authority_flags"]["demo_order_placement_approved"] is False
    assert record["authority_flags"]["execution_approved"] is False


def test_demo_order_readiness_packet_fails_if_human_decision_does_not_allow_it() -> None:
    shape_preview = _valid_shape_preview()
    human_decision = _human_decision(shape_preview)
    human_decision["approved_scope"]["may_prepare_demo_order_readiness_packet"] = False

    record = build_demo_order_readiness_packet(
        DemoOrderReadinessPacketInputs(
            shape_preview_review_human_decision=human_decision,
            shape_preview_envelope=shape_preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "demo_order_readiness_not_allowed" in record["violations"]