from __future__ import annotations

import json

import pytest

from quantcore.execution.h024_broker_request_construction_readiness_packet import (
    BOUNDARY_KIND,
    BOUNDARY_SCHEMA,
    DECISION,
    KIND,
    NOOP_INVOCATION_DECISION,
    NOOP_INVOCATION_KIND,
    NOOP_INVOCATION_SCHEMA,
    SCHEMA,
    STATUS,
    build_broker_request_construction_readiness_packet_record,
    read_single_jsonl_record,
    verify_broker_request_construction_readiness_packet_record,
    write_single_jsonl_record,
)


def noop_invocation_record() -> dict:
    return {
        "schema": NOOP_INVOCATION_SCHEMA,
        "kind": NOOP_INVOCATION_KIND,
        "status": "NOOP_ADAPTER_USE_INVOKED_REFUSED_BROKER_TRANSPORT",
        "decision": NOOP_INVOCATION_DECISION,
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
    }


def boundary_record() -> dict:
    return {
        "schema": BOUNDARY_SCHEMA,
        "kind": BOUNDARY_KIND,
        "status": "ADAPTER_IMPLEMENTATION_BOUNDARY_STATIC_VERIFIED",
        "decision": "ALLOW_IMPLEMENTATION_SURFACE_REVIEW_ONLY_NO_EXECUTION",
        "verdict": "PASS",
        "violations": [],
        "scanned_adapter_boundary_files": 15,
        "prohibited_findings": [],
    }


def build_record() -> dict:
    return build_broker_request_construction_readiness_packet_record(
        noop_use_invocation_audit=noop_invocation_record(),
        boundary_static_verifier=boundary_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )


def test_builds_pass_packet_from_valid_inputs() -> None:
    record = build_record()

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["violations"] == []


def test_requests_broker_request_construction_readiness_only() -> None:
    record = build_record()

    assert (
        record["readiness"]["requested_human_review"]
        == "broker_request_construction_readiness_only"
    )
    assert record["authority"]["broker_request_construction_approved"] is False
    assert record["mutation_safety"]["broker_request_constructed"] is False


@pytest.mark.parametrize(
    "authority_key",
    [
        "broker_request_construction_approved",
        "execution_adapter_use_approved",
        "execution_adapter_approved",
        "broker_request_approved",
        "mt5_execution_approved",
        "terminal_mutation_approved",
        "demo_order_placement_approved",
        "live_order_placement_approved",
        "execution_approved",
    ],
)
def test_fails_if_any_blocked_authority_flag_is_true(authority_key: str) -> None:
    record = build_record()
    record["authority"][authority_key] = True

    result = verify_broker_request_construction_readiness_packet_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(authority_key in violation for violation in result.violations)


@pytest.mark.parametrize(
    "mutation_key",
    [
        "broker_request_constructed",
        "mt5_request_constructed",
        "order_payload_constructed",
        "transport_dispatch_attempted",
        "dispatch_attempted",
        "terminal_mutated",
        "broker_state_mutated",
    ],
)
def test_fails_if_any_mutation_or_dispatch_flag_is_true(mutation_key: str) -> None:
    record = build_record()
    record["mutation_safety"][mutation_key] = True

    result = verify_broker_request_construction_readiness_packet_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(mutation_key in violation for violation in result.violations)


def test_fails_if_noop_invocation_upstream_is_not_pass() -> None:
    invocation = noop_invocation_record()
    invocation["verdict"] = "FAIL"

    record = build_broker_request_construction_readiness_packet_record(
        noop_use_invocation_audit=invocation,
        boundary_static_verifier=boundary_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("noop_use_invocation_audit" in v for v in record["violations"])


def test_fails_if_noop_invocation_decision_changes() -> None:
    invocation = noop_invocation_record()
    invocation["decision"] = "ALLOW"

    record = build_broker_request_construction_readiness_packet_record(
        noop_use_invocation_audit=invocation,
        boundary_static_verifier=boundary_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("noop_use_invocation_audit" in v for v in record["violations"])


def test_fails_if_boundary_static_verifier_has_violations() -> None:
    boundary = boundary_record()
    boundary["violations"] = ["bad"]

    record = build_broker_request_construction_readiness_packet_record(
        noop_use_invocation_audit=noop_invocation_record(),
        boundary_static_verifier=boundary,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("boundary_static_verifier" in v for v in record["violations"])


def test_fails_if_required_constraint_is_false() -> None:
    record = build_record()
    record["required_next_capability_constraints"]["must_not_import_metatrader5"] = False

    result = verify_broker_request_construction_readiness_packet_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert "must_not_import_metatrader5 must be true" in result.violations


def test_verifies_allowed_demo_server() -> None:
    result = verify_broker_request_construction_readiness_packet_record(
        build_record(),
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert result.ok


def test_fails_wrong_allowed_demo_server() -> None:
    result = verify_broker_request_construction_readiness_packet_record(
        build_record(),
        allowed_demo_server="WrongServer",
        require_pass=True,
    )

    assert not result.ok
    assert "allowed demo server not observed: WrongServer" in result.violations


def test_round_trips_jsonl(tmp_path) -> None:
    record = build_record()
    path = tmp_path / "broker_request_construction_readiness_packet.jsonl"

    write_single_jsonl_record(path, record)
    loaded = read_single_jsonl_record(path)

    assert loaded == json.loads(json.dumps(record, sort_keys=True))