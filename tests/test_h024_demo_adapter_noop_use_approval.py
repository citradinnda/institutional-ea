from __future__ import annotations

import json

import pytest

from quantcore.execution.h024_demo_adapter_noop_use_approval import (
    DECISION,
    KIND,
    SCHEMA,
    STATUS,
    UPSTREAM_DECISION,
    UPSTREAM_KIND,
    UPSTREAM_SCHEMA,
    build_noop_use_approval_record,
    read_single_jsonl_record,
    verify_noop_use_approval_record,
    write_single_jsonl_record,
)


def upstream_record() -> dict:
    return {
        "schema": UPSTREAM_SCHEMA,
        "kind": UPSTREAM_KIND,
        "status": "ADAPTER_USE_READINESS_REVIEW_APPROVED_NO_EXECUTION_AUTHORITY",
        "decision": UPSTREAM_DECISION,
        "verdict": "PASS",
        "violations": [],
        "allowed_demo_server": "Exness-MT5Trial6",
    }


def build_record() -> dict:
    return build_noop_use_approval_record(
        adapter_use_readiness_human_decision=upstream_record(),
        allowed_demo_server="Exness-MT5Trial6",
    )


def test_builds_pass_noop_use_approval_from_valid_upstream() -> None:
    record = build_record()

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["violations"] == []


def test_approves_noop_adapter_use_only() -> None:
    record = build_record()

    assert record["authority"]["noop_adapter_use_approved"] is True
    assert record["authority"]["noop_adapter_use_only"] is True
    assert record["approved_scope"]["scope"] == "pure_python_noop_adapter_use_only"
    assert record["approved_scope"]["may_invoke_noop_transport_contract"] is True


@pytest.mark.parametrize(
    "authority_key",
    [
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

    result = verify_noop_use_approval_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(authority_key in violation for violation in result.violations)


@pytest.mark.parametrize(
    "scope_key",
    [
        "may_construct_broker_request",
        "may_construct_mt5_request",
        "may_construct_order_payload",
        "may_dispatch_transport",
        "may_mutate_terminal",
        "may_mutate_broker_state",
        "may_place_demo_order",
        "may_place_live_order",
    ],
)
def test_fails_if_any_forbidden_scope_permission_is_true(scope_key: str) -> None:
    record = build_record()
    record["approved_scope"][scope_key] = True

    result = verify_noop_use_approval_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(scope_key in violation for violation in result.violations)


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

    result = verify_noop_use_approval_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert any(mutation_key in violation for violation in result.violations)


def test_fails_if_upstream_is_not_pass() -> None:
    upstream = upstream_record()
    upstream["verdict"] = "FAIL"

    record = build_noop_use_approval_record(
        adapter_use_readiness_human_decision=upstream,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("adapter_use_readiness_human_decision" in v for v in record["violations"])


def test_fails_if_upstream_decision_changes() -> None:
    upstream = upstream_record()
    upstream["decision"] = "APPROVE_ADAPTER_USE"

    record = build_noop_use_approval_record(
        adapter_use_readiness_human_decision=upstream,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert record["verdict"] == "FAIL"
    assert any("adapter_use_readiness_human_decision" in v for v in record["violations"])


def test_fails_if_approval_scope_changes() -> None:
    record = build_record()
    record["approved_scope"]["scope"] = "execution_adapter_use"

    result = verify_noop_use_approval_record(
        record,
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert not result.ok
    assert "scope must be pure_python_noop_adapter_use_only" in result.violations


def test_verifies_allowed_demo_server() -> None:
    result = verify_noop_use_approval_record(
        build_record(),
        allowed_demo_server="Exness-MT5Trial6",
        require_pass=True,
    )

    assert result.ok


def test_fails_wrong_allowed_demo_server() -> None:
    result = verify_noop_use_approval_record(
        build_record(),
        allowed_demo_server="WrongServer",
        require_pass=True,
    )

    assert not result.ok
    assert "allowed demo server not observed: WrongServer" in result.violations


def test_round_trips_jsonl(tmp_path) -> None:
    record = build_record()
    path = tmp_path / "noop_use_approval.jsonl"

    write_single_jsonl_record(path, record)
    loaded = read_single_jsonl_record(path)

    assert loaded == json.loads(json.dumps(record, sort_keys=True))