from quantcore.execution.h024_demo_order_canary_human_approval import (
    FALSE_AFTER_CANARY_APPROVAL_FLAGS,
    build_demo_order_canary_human_approval,
)
from quantcore.execution.h024_final_pre_dispatch_audit_packet import (
    AUDIT_DECISION,
    build_final_pre_dispatch_audit_packet,
    validate_final_pre_dispatch_audit_packet,
)


def _preflight_packet():
    return {
        "schema_version": "h024_demo_order_canary_hard_controls_preflight_packet_v1",
        "kind": "h024_demo_order_canary_hard_controls_preflight_packet",
        "verdict": "PASS",
        "decision": "REQUEST_HUMAN_DEMO_ORDER_CANARY_APPROVAL_WITH_HARD_CONTROLS_NO_ORDER_PLACEMENT",
        "allowed_demo_server": "Exness-MT5Trial6",
        "expected_runtime_symbol": "XAUUSDm",
        "violations": [],
        "required_hard_controls": {
            "allowed_demo_server_lock": {"required": True, "value": "Exness-MT5Trial6"},
            "account_currency_lock": {"required": True, "value": "USD"},
            "account_context_lock": {"required": True, "value": "standard_demo_only"},
            "runtime_symbol_lock": {"required": True, "value": "XAUUSDm"},
            "kill_switch_allow_state_required": True,
            "idempotency_ledger_required": True,
            "max_lot_cap": {
                "required": True,
                "value": 0.01,
                "unit": "lots",
                "must_not_exceed_upstream_h020_final_lots": True,
                "upstream_verified_final_lots": 0.01,
            },
            "single_canary_order_limit": {"required": True, "value": 1},
            "post_order_audit_required_if_later_approved": True,
            "pre_dispatch_final_audit_required_if_later_approved": True,
            "human_demo_order_canary_approval_required_before_any_order_path": True,
            "live_order_forbidden": True,
        },
        "authority": {
            "hard_controls_preflight_packet_constructed": True,
            "requests_human_demo_order_canary_approval_review": True,
        },
    }


def _approval(packet):
    return build_demo_order_canary_human_approval(
        hard_controls_preflight_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        generated_at_utc="2026-05-12T00:00:00Z",
    )


def test_final_pre_dispatch_audit_passes_and_allows_next_engineering_step_only():
    packet = _preflight_packet()
    record = build_final_pre_dispatch_audit_packet(
        canary_human_approval=_approval(packet),
        hard_controls_preflight_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        max_lot_cap=0.01,
        generated_at_utc="2026-05-12T00:00:00Z",
    )

    assert record["verdict"] == "PASS"
    assert record["approved"] is False
    assert record["pre_dispatch_audit_passed"] is True
    assert record["decision"] == AUDIT_DECISION
    assert record["authority"]["demo_order_canary_approved"] is True
    assert record["authority"]["one_shot_execution_capable_demo_path_implementation_allowed"] is True
    assert record["authority"]["actual_mt5_request_constructed"] is False
    assert record["authority"]["order_payload_constructed"] is False
    assert record["authority"]["transport_dispatch_attempted"] is False
    assert record["authority"]["demo_order_placement_approved"] is False
    assert record["authority"]["execution_approved"] is False
    assert record["verified_controls"]["single_canary_order_limit"] == 1
    assert record["verified_controls"]["max_lot_cap"] == 0.01
    for flag in FALSE_AFTER_CANARY_APPROVAL_FLAGS:
        assert record["preserved_false_authority"][flag] is False

    assert not validate_final_pre_dispatch_audit_packet(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        max_lot_cap=0.01,
        require_pass=True,
    )


def test_final_pre_dispatch_audit_refuses_mismatched_lot_cap():
    packet = _preflight_packet()
    record = build_final_pre_dispatch_audit_packet(
        canary_human_approval=_approval(packet),
        hard_controls_preflight_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        max_lot_cap=0.02,
        generated_at_utc="2026-05-12T00:00:00Z",
    )

    assert record["verdict"] == "FAIL"
    assert "max_lot_cap_mismatch" in record["violations"]
    assert validate_final_pre_dispatch_audit_packet(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        max_lot_cap=0.02,
        require_pass=True,
    )