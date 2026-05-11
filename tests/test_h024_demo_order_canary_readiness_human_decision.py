from quantcore.execution.h024_demo_order_canary_readiness_human_decision import (
    APPROVAL_DECISION,
    FALSE_AUTHORITY_FLAGS,
    build_demo_order_canary_readiness_human_decision,
    validate_demo_order_canary_readiness_human_decision,
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


def test_canary_readiness_decision_approves_only_review_path():
    record = build_demo_order_canary_readiness_human_decision(
        demo_order_readiness_packet=_readiness_packet(),
        allowed_demo_server="Exness-MT5Trial6",
        generated_at_utc="2026-05-12T00:00:00Z",
    )

    assert record["verdict"] == "PASS"
    assert record["approved"] is True
    assert record["decision"] == APPROVAL_DECISION
    assert record["authority"]["canary_hard_controls_preflight_packet_construction_allowed"] is True
    assert record["authority"]["demo_order_canary_approved"] is False
    assert record["authority"]["demo_order_placement_approved"] is False
    assert record["authority"]["execution_approved"] is False
    assert record["safety_boundary"]["non_dispatchable"] is True
    for flag in FALSE_AUTHORITY_FLAGS:
        assert record["preserved_false_authority"][flag] is False

    assert not validate_demo_order_canary_readiness_human_decision(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_approved=True,
    )


def test_canary_readiness_decision_refuses_bad_server():
    packet = _readiness_packet()
    packet["account"]["server"] = "Unexpected-Server"
    record = build_demo_order_canary_readiness_human_decision(
        demo_order_readiness_packet=packet,
        allowed_demo_server="Exness-MT5Trial6",
        generated_at_utc="2026-05-12T00:00:00Z",
    )

    assert record["verdict"] == "FAIL"
    assert record["approved"] is False
    assert "demo_order_readiness_packet_server_does_not_match_allowed_demo_server" in record["violations"]
    assert validate_demo_order_canary_readiness_human_decision(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_approved=True,
    )