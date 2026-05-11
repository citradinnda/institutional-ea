from __future__ import annotations

from quantcore.execution.h024_broker_request_draft_construction_approval import (
    DraftConstructionApprovalInputs,
    build_draft_construction_approval,
)
from quantcore.execution.h024_broker_request_draft_envelope import (
    DraftEnvelopeInputs,
    build_draft_envelope,
)


def _valid_preview_envelope() -> dict:
    return {
        "schema": "h024_broker_request_preview_envelope_v1",
        "kind": "BROKER_REQUEST_PREVIEW_ENVELOPE",
        "status": "PREVIEW_ENVELOPE_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH",
        "decision": "CONSTRUCT_PREVIEW_ENVELOPE_ONLY_REFUSE_DISPATCH",
        "allowed_demo_server": "Exness-MT5Trial6",
        "preview_idempotency_key": "preview-key",
        "canonical_preview_fields": {
            "normalized_symbol": "XAUUSD",
            "runtime_symbol": "XAUUSDm",
            "side": "short",
            "final_lots": 0.01,
            "entry": 4930.041,
            "stop": 5019.068,
            "risk_fraction": 0.01,
            "closed_h4_time": "2026.03.18 08:00:00",
            "timeframe": "H4",
        },
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


def _approval(preview: dict) -> dict:
    return build_draft_construction_approval(
        DraftConstructionApprovalInputs(
            preview_envelope=preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )


def test_draft_envelope_passes_and_preserves_non_execution_boundary() -> None:
    preview = _valid_preview_envelope()
    approval = _approval(preview)

    record = build_draft_envelope(
        DraftEnvelopeInputs(
            draft_construction_approval=approval,
            preview_envelope=preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["consumption_flags"]["preview_envelope_consumed"] is True
    assert record["consumption_flags"]["verified_intent_consumed"] is True
    assert record["consumption_flags"]["h020_sizing_consumed_not_reinterpreted"] is True
    assert record["consumption_flags"]["kill_switch_allow_state_required"] is True
    assert record["consumption_flags"]["idempotency_key_carried_forward"] is True
    assert record["draft_flags"]["draft_is_non_dispatchable"] is True
    assert record["draft_flags"]["not_mt5_request"] is True
    assert record["draft_flags"]["not_broker_request"] is True
    assert record["draft_flags"]["not_order_payload"] is True
    assert record["authority_flags"]["actual_broker_request_constructed"] is False
    assert record["authority_flags"]["mt5_request_constructed"] is False
    assert record["authority_flags"]["order_payload_constructed"] is False
    assert record["authority_flags"]["dispatch_attempted"] is False
    assert record["authority_flags"]["execution_approved"] is False

    conceptual = record["canonical_conceptual_review_fields"]
    assert conceptual["field_set_kind"] == "CANONICAL_CONCEPTUAL_REVIEW_FIELDS_NOT_EXECUTABLE_REQUEST"
    assert conceptual["normalized_symbol"] == "XAUUSD"
    assert conceptual["runtime_symbol"] == "XAUUSDm"
    assert conceptual["conceptual_side"] == "sell_review_only"
    assert conceptual["h020_final_lots"] == 0.01
    assert conceptual["sizing_source"] == "H020_CONSUMED_NOT_REINTERPRETED"
    assert conceptual["execution_shape"] == "NOT_MT5_REQUEST_NOT_ORDER_PAYLOAD_NOT_DISPATCHABLE"


def test_draft_envelope_fails_if_approval_does_not_pass() -> None:
    preview = _valid_preview_envelope()
    approval = _approval(preview)
    approval["verdict"] = "FAIL"

    record = build_draft_envelope(
        DraftEnvelopeInputs(
            draft_construction_approval=approval,
            preview_envelope=preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    assert record["verdict"] == "FAIL"
    assert "draft_construction_approval_not_pass" in record["violations"]


def test_draft_envelope_is_not_shaped_like_mql_trade_request() -> None:
    preview = _valid_preview_envelope()
    approval = _approval(preview)

    record = build_draft_envelope(
        DraftEnvelopeInputs(
            draft_construction_approval=approval,
            preview_envelope=preview,
            allowed_demo_server="Exness-MT5Trial6",
        )
    )

    forbidden_top_level_fields = {
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
    assert forbidden_top_level_fields.isdisjoint(record.keys())
    assert set(record["forbidden_execution_fields_absent_by_design"]) == forbidden_top_level_fields