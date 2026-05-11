from __future__ import annotations

from quantcore.execution.h024_mt5_request_shape_construction_approval import (
    Mt5RequestShapeConstructionApprovalInputs,
    build_mt5_request_shape_construction_approval,
)
from quantcore.execution.h024_mt5_request_shape_preview_envelope import (
    Mt5RequestShapePreviewEnvelopeInputs,
    build_mt5_request_shape_preview_envelope,
)


def _valid_design_packet() -> dict:
    return {
        "schema": "h024_mt5_request_shape_design_review_packet_v1",
        "kind": "MT5_REQUEST_SHAPE_DESIGN_REVIEW_PACKET",
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
    }


def _approval(packet: dict) -> dict:
    complete_packet = {
        **packet,
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
    return build_mt5_request_shape_construction_approval(
        Mt5RequestShapeConstructionApprovalInputs(
            design_review_packet=complete_packet,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )


def test_shape_preview_envelope_is_inert_and_non_dispatchable() -> None:
    packet = _valid_design_packet()
    approval = _approval(packet)

    record = build_mt5_request_shape_preview_envelope(
        Mt5RequestShapePreviewEnvelopeInputs(
            construction_approval=approval,
            design_review_packet=packet,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["consumption_flags"]["design_review_packet_consumed"] is True
    assert record["consumption_flags"]["h020_sizing_consumed_not_reinterpreted"] is True
    assert record["shape_preview_flags"]["shape_preview_only"] is True
    assert record["shape_preview_flags"]["not_actual_mt5_request"] is True
    assert record["shape_preview_flags"]["not_order_payload"] is True
    assert record["shape_preview_flags"]["not_dispatchable"] is True
    assert record["authority_flags"]["mt5_request_shape_preview_envelope_constructed"] is True
    assert record["authority_flags"]["mt5_request_constructed"] is False
    assert record["authority_flags"]["order_payload_constructed"] is False
    assert record["authority_flags"]["dispatch_attempted"] is False
    assert record["authority_flags"]["execution_approved"] is False

    preview = record["inert_terminal_request_shape_preview"]
    assert preview["field_set_kind"] == "INERT_TERMINAL_REQUEST_SHAPE_REVIEW_FIELDS_NOT_SENDABLE"
    assert preview["direction_review"]["terminal_direction_label_review_only"] == "SELL_DIRECTION_REVIEW_ONLY"


def test_shape_preview_fails_without_construction_approval() -> None:
    packet = _valid_design_packet()
    approval = _approval(packet)
    approval["approved_scope"]["may_construct_inert_mt5_request_shape_preview_envelope"] = False

    record = build_mt5_request_shape_preview_envelope(
        Mt5RequestShapePreviewEnvelopeInputs(
            construction_approval=approval,
            design_review_packet=packet,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "shape_preview_construction_not_approved" in record["violations"]


def test_shape_preview_top_level_is_not_sendable_request_shape() -> None:
    packet = _valid_design_packet()
    approval = _approval(packet)

    record = build_mt5_request_shape_preview_envelope(
        Mt5RequestShapePreviewEnvelopeInputs(
            construction_approval=approval,
            design_review_packet=packet,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    forbidden_top_level = {
        "action",
        "type",
        "volume",
        "price",
        "sl",
        "tp",
        "deviation",
        "magic",
        "comment",
        "type_time",
        "type_filling",
    }
    assert forbidden_top_level.isdisjoint(record.keys())