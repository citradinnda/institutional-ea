from quantcore.execution.h024_demo_order_canary_hard_controls_preflight_packet import (
    REQUEST_DECISION,
    build_demo_order_canary_hard_controls_preflight_packet,
    validate_demo_order_canary_hard_controls_preflight_packet,
)
from quantcore.execution.h024_demo_order_canary_readiness_human_decision import (
    FALSE_AUTHORITY_FLAGS,
    build_demo_order_canary_readiness_human_decision,
)


def _readiness_packet():
    return {
        "schema_version": "h024_standard_demo_demo_order_readiness_packet_v1",
        "kind": "h024_standard_demo_demo_order_readiness_packet",
        "verdict": "PASS",
        "violations": [],
        "demo_order_readiness_packet_constructed": True,
        "account": {"server": "Exness-MT5Trial6", "currency": "USD"},
        "intent": {"runtime_symbol": "XAUUSDm", "final_lots": 0.01},
        "idempotency_key": "h024-test-key",
    }


def _decision(packet):
    return build_demo_order_canary_readiness_human_decision(
        demo_order_readiness_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
        generated_at_utc="2026-05-12T00:00:00Z",
    )


def test_hard_controls_preflight_packet_requests_later_human_canary_review_only():
    packet = _readiness_packet()
    record = build_demo_order_canary_hard_controls_preflight_packet(
        canary_readiness_human_decision=_decision(packet),
        demo_order_readiness_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        max_lot_cap=0.01,
        generated_at_utc="2026-05-12T00:00:00Z",
    )

    assert record["verdict"] == "PASS"
    assert record["approved"] is False
    assert record["decision"] == REQUEST_DECISION
    assert record["required_hard_controls"]["allowed_demo_server_lock"]["value"] == "Exness-MT5Trial6"
    assert record["required_hard_controls"]["account_currency_lock"]["value"] == "USD"
    assert record["required_hard_controls"]["account_context_lock"]["value"] == "standard_demo_only"
    assert record["required_hard_controls"]["runtime_symbol_lock"]["value"] == "XAUUSDm"
    assert record["required_hard_controls"]["kill_switch_allow_state_required"] is True
    assert record["required_hard_controls"]["idempotency_ledger_required"] is True
    assert record["required_hard_controls"]["single_canary_order_limit"]["value"] == 1
    assert record["required_hard_controls"]["post_order_audit_required_if_later_approved"] is True
    assert record["required_hard_controls"]["live_order_forbidden"] is True
    assert record["authority"]["requests_human_demo_order_canary_approval_review"] is True
    assert record["authority"]["demo_order_canary_approved"] is False
    assert record["authority"]["demo_order_placement_approved"] is False
    assert record["authority"]["execution_approved"] is False
    for flag in FALSE_AUTHORITY_FLAGS:
        assert record["preserved_false_authority"][flag] is False

    assert not validate_demo_order_canary_hard_controls_preflight_packet(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        require_pass=True,
    )


def test_hard_controls_preflight_packet_refuses_cap_above_verified_final_lots():
    packet = _readiness_packet()
    record = build_demo_order_canary_hard_controls_preflight_packet(
        canary_readiness_human_decision=_decision(packet),
        demo_order_readiness_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        max_lot_cap=0.02,
        generated_at_utc="2026-05-12T00:00:00Z",
    )

    assert record["verdict"] == "FAIL"
    assert "max_lot_cap_exceeds_upstream_verified_final_lots" in record["violations"]
    assert validate_demo_order_canary_hard_controls_preflight_packet(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        expected_runtime_symbol="XAUUSDm",
        require_pass=True,
    )