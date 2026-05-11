from __future__ import annotations

from quantcore.execution.h024_mt5_request_shape_construction_approval import (
    Mt5RequestShapeConstructionApprovalInputs,
    build_mt5_request_shape_construction_approval,
)


def _valid_design_packet() -> dict:
    return {
        "schema": "h024_mt5_request_shape_design_review_packet_v1",
        "kind": "MT5_REQUEST_SHAPE_DESIGN_REVIEW_PACKET",
        "status": "READY_FOR_HUMAN_MT5_REQUEST_SHAPE_REVIEW_NO_REQUEST_CONSTRUCTION",
        "decision": "REQUEST_HUMAN_MT5_REQUEST_SHAPE_REVIEW_NO_MT5_NO_DISPATCH",
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
        "design_scope": {
            "design_review_only": True,
            "describes_future_request_shape_constraints": True,
            "constructs_mt5_request": False,
            "constructs_order_payload": False,
            "constructs_actual_broker_request": False,
            "dispatches_transport": False,
            "mutates_terminal_or_broker_state": False,
            "approves_execution": False,
        },
        "future_shape_constraints": {
            "must_be_derived_only_from_reviewed_draft_envelope": True,
            "must_carry_idempotency_forward": True,
            "must_consume_h020_sizing_without_reinterpretation": True,
            "must_require_kill_switch_allow_state": True,
            "must_remain_inert_until_separately_approved": True,
            "must_not_import_or_call_metatrader5": True,
            "must_not_dispatch": True,
            "must_not_mutate_terminal_or_broker_state": True,
            "must_not_place_demo_or_live_order": True,
        },
        "source_conceptual_draft_summary": {
            "normalized_symbol": "XAUUSD",
            "runtime_symbol": "XAUUSDm",
            "conceptual_side": "sell_review_only",
            "h020_final_lots": 0.01,
            "entry_reference_price": 4930.041,
            "protective_stop_reference_price": 5019.068,
            "sizing_source": "H020_CONSUMED_NOT_REINTERPRETED",
            "execution_shape": "NOT_MT5_REQUEST_NOT_ORDER_PAYLOAD_NOT_DISPATCHABLE",
        },
        "authority_flags": {
            "phase4_approved": True,
            "broker_request_draft_review_approved": True,
            "mt5_request_shape_design_review_packet_constructed": True,
            "mt5_request_shape_construction_approved": False,
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


def test_construction_approval_allows_only_inert_shape_preview() -> None:
    record = build_mt5_request_shape_construction_approval(
        Mt5RequestShapeConstructionApprovalInputs(
            design_review_packet=_valid_design_packet(),
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["approved_scope"]["may_construct_inert_mt5_request_shape_preview_envelope"] is True
    assert record["approved_scope"]["may_construct_mt5_request"] is False
    assert record["approved_scope"]["may_construct_order_payload"] is False
    assert record["approved_scope"]["may_dispatch_transport"] is False
    assert record["approved_scope"]["may_execute"] is False
    assert record["authority_flags"]["mt5_request_shape_construction_approved"] is True
    assert record["authority_flags"]["mt5_request_constructed"] is False
    assert record["authority_flags"]["order_payload_constructed"] is False
    assert record["authority_flags"]["execution_approved"] is False


def test_construction_approval_fails_if_design_packet_constructs_request() -> None:
    packet = _valid_design_packet()
    packet["design_scope"]["constructs_mt5_request"] = True

    record = build_mt5_request_shape_construction_approval(
        Mt5RequestShapeConstructionApprovalInputs(
            design_review_packet=packet,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "design_scope_forbidden_not_false_constructs_mt5_request" in record["violations"]
    assert record["approved_scope"]["may_construct_inert_mt5_request_shape_preview_envelope"] is False