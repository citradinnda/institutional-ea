from __future__ import annotations

import ast
import json
from datetime import datetime, timezone
from pathlib import Path

from quantcore.execution.h024_exact_ticket_canary_close_modify_governance import (
    AUTHORIZATION_KEYS,
    DECISION_ARTIFACT_TYPE,
    EXPECTED_MAGIC,
    EXPECTED_TICKET,
    PACKET_TYPE,
    SCHEMA_VERSION,
    STRATEGY,
    build_governance_packet,
    validate_governance_record,
    verify_jsonl_file,
    write_jsonl_record,
)


NOW = "2026-05-12T03:20:00Z"


def _authorizations_false() -> dict[str, bool]:
    return {key: False for key in AUTHORIZATION_KEYS}


def _decision(**overrides):
    base = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "artifact_type": DECISION_ARTIFACT_TYPE,
        "decision": "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
        "decision_is_explicit": True,
        "close_modify_requested": False,
        "target": {
            "ticket": EXPECTED_TICKET,
            "identifier": EXPECTED_TICKET,
            "runtime_symbol": "XAUUSDm",
            "model_symbol": "XAUUSD",
            "side": "sell",
            "position_type": 1,
            "volume": 0.01,
            "magic": EXPECTED_MAGIC,
        },
        "valid_until_utc": "2099-01-01T00:00:00Z",
        "effective_new_entries_blocked": True,
        **_authorizations_false(),
    }
    base.update(overrides)
    return base


def _gate(**overrides):
    base = {
        "schema_version": "1.0",
        "strategy": STRATEGY,
        "packet_type": "h024_runtime_no_mutation_safety_gate",
        "observed_at_utc": NOW,
        "trusted": True,
        "verdict": "PASS",
        "violations": [],
        "operator_state": "NO_MUTATION_GATE_CONTRACT_ACTIVE_TRADING_NOT_AUTHORIZED",
        "operator_next_action": (
            "KEEP_ALL_BROKER_MUTATION_BLOCKED_CONTINUE_READ_ONLY_SUPERVISION"
        ),
        "gate_opens_mutation_path": False,
        "future_broker_facing_code_must_check_gate": True,
        "effective_new_entries_blocked": True,
        **_authorizations_false(),
        "unified_supervision_record": {
            "schema_version": "1.0",
            "strategy": STRATEGY,
            "packet_type": "h024_unified_read_only_post_canary_runtime_supervision",
            "observed_at_utc": NOW,
            "verdict": "PASS",
            "violations": [],
            "exact_canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
            "exact_canary_observed": True,
            "h024_position_count": 1,
            "h024_order_count": 0,
            "position": {
                "symbol": "XAUUSDm",
                "model_symbol": "XAUUSD",
                "side": "sell",
                "type": 1,
                "volume": 0.01,
                "magic": 240024,
                "ticket": 4413054432,
                "identifier": 4413054432,
            },
            "runtime_aggregate_record": {
                "packet_type": "h024_runtime_safety_aggregate_supervisor",
                "verdict": "PASS",
                "upstream": [
                    {
                        "packet_type": "h024_runtime_tick_spread_safety_supervisor",
                        "observed_at_utc": NOW,
                        "verdict": "PASS",
                        "spread_points": 10,
                    },
                    {
                        "packet_type": "h024_runtime_exposure_inventory_safety_supervisor",
                        "observed_at_utc": NOW,
                        "verdict": "PASS",
                        "exact_canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
                        "exact_canary_observed": True,
                        "h024_position_count": 1,
                        "h024_order_count": 0,
                    },
                    {
                        "packet_type": "h024_runtime_account_risk_margin_safety_supervisor",
                        "observed_at_utc": NOW,
                        "verdict": "PASS",
                        "margin_level": 400000.0,
                    },
                ],
            },
        },
    }
    base.update(overrides)
    return base


_DEFAULT = object()


def _build(gate=_DEFAULT, decision=_DEFAULT):
    return build_governance_packet(
        no_mutation_gate_record=_gate() if gate is _DEFAULT else gate,
        human_decision_record=_decision() if decision is _DEFAULT else decision,
        observed_at_utc=NOW,
        max_gate_age_seconds=3600,
        max_snapshot_age_seconds=3600,
    )


def test_builds_passing_read_only_governance_spec_packet():
    record = _build()
    assert record["verdict"] == "PASS"
    assert record["packet_type"] == PACKET_TYPE
    assert record["effective_new_entries_blocked"] is True
    assert all(record[key] is False for key in AUTHORIZATION_KEYS)
    assert record["broker_mutation_blocked"] is True
    assert record["close_modify_blocked"] is True


def test_missing_no_mutation_gate_fails_closed():
    record = _build(gate=None)
    assert record["verdict"] == "FAIL"
    assert "FAIL_CLOSED" in record["operator_state"]
    assert any("runtime_no_mutation_gate_record_present" in v for v in record["violations"])


def test_wrong_gate_packet_type_fails_closed():
    gate = _gate(packet_type="wrong_packet")
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("runtime_no_mutation_gate_identity" in v for v in record["violations"])


def test_gate_not_pass_fails_closed():
    gate = _gate(verdict="FAIL")
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("runtime_no_mutation_gate_pass" in v for v in record["violations"])


def test_gate_opening_mutation_path_fails_closed():
    gate = _gate(gate_opens_mutation_path=True)
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any(
        "runtime_no_mutation_gate_keeps_mutation_path_closed" in v
        for v in record["violations"]
    )


def test_unsafe_gate_authorization_fails_closed():
    gate = _gate(order_send_authorized=True)
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("runtime_no_mutation_gate_authorizations_false" in v for v in record["violations"])


def test_unified_supervision_not_pass_fails_closed():
    gate = _gate()
    gate["unified_supervision_record"]["verdict"] = "FAIL"
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any(
        "unified_post_canary_runtime_supervision_pass" in v for v in record["violations"]
    )


def test_missing_exact_canary_fails_closed():
    gate = _gate()
    gate["unified_supervision_record"]["exact_canary_state"] = "NOT_OBSERVED"
    gate["unified_supervision_record"]["exact_canary_observed"] = False
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("exact_known_canary_identity_match" in v for v in record["violations"])


def test_usdjpy_h024_exposure_fails_closed():
    gate = _gate(usdjpy_h024_position_count=1)
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("no_usdjpy_h024_exposure_or_order" in v for v in record["violations"])


def test_additional_h024_exposure_fails_closed():
    gate = _gate()
    gate["unified_supervision_record"]["h024_position_count"] = 2
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("no_additional_h024_exposure_or_order" in v for v in record["violations"])


def test_any_h024_order_fails_closed():
    gate = _gate()
    gate["unified_supervision_record"]["h024_order_count"] = 1
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("no_additional_h024_exposure_or_order" in v for v in record["violations"])


def test_missing_decision_artifact_fails_closed():
    record = _build(decision=None)
    assert record["verdict"] == "FAIL"
    assert any("explicit_human_decision_artifact_present" in v for v in record["violations"])


def test_ambiguous_or_action_decision_fails_closed():
    decision = _decision(decision="APPROVE_CLOSE", close_modify_requested=True)
    record = _build(decision=decision)
    assert record["verdict"] == "FAIL"
    assert any(
        "explicit_human_decision_is_spec_only_and_unambiguous" in v
        for v in record["violations"]
    )


def test_stale_decision_artifact_fails_closed():
    decision = _decision(valid_until_utc="2020-01-01T00:00:00Z")
    record = _build(decision=decision)
    assert record["verdict"] == "FAIL"
    assert any("explicit_human_decision_not_stale" in v for v in record["violations"])


def test_missing_pre_close_snapshot_fails_closed():
    gate = _gate()
    del gate["unified_supervision_record"]["runtime_aggregate_record"]
    gate["unified_supervision_record"].pop("h024_position_count")
    gate["unified_supervision_record"].pop("h024_order_count")
    gate["unified_supervision_record"].pop("exact_canary_state")
    gate["unified_supervision_record"].pop("exact_canary_observed")
    record = _build(gate=gate)
    assert record["verdict"] == "FAIL"
    assert any("pre_close_account_risk_margin_snapshot_present" in v for v in record["violations"])


def test_verifier_accepts_passing_record_and_rejects_fail_closed(tmp_path):
    passing = _build()
    pass_path = tmp_path / "pass.jsonl"
    write_jsonl_record(pass_path, passing)
    result = verify_jsonl_file(pass_path, require_pass=True)
    assert result.verifier_verdict == "PASS"

    failing = _build(decision=None)
    fail_path = tmp_path / "fail.jsonl"
    write_jsonl_record(fail_path, failing)
    result = verify_jsonl_file(fail_path, require_pass=True)
    assert result.verifier_verdict == "FAIL"
    assert any("require-pass set" in violation for violation in result.violations)


def test_verifier_rejects_missing_or_unsafe_authorization(tmp_path):
    record = _build()
    del record["order_check_authorized"]
    path = tmp_path / "missing_auth.jsonl"
    write_jsonl_record(path, record)
    result = verify_jsonl_file(path)
    assert result.verifier_verdict == "FAIL"
    assert any("missing top-level authorization flag order_check_authorized" in v for v in result.violations)

    unsafe = _build()
    unsafe["authorizations"]["order_send_authorized"] = True
    path = tmp_path / "unsafe_auth.jsonl"
    write_jsonl_record(path, unsafe)
    result = verify_jsonl_file(path)
    assert result.verifier_verdict == "FAIL"
    assert any("unsafe nested authorization flag order_send_authorized" in v for v in result.violations)


def test_verifier_rejects_malformed_jsonl(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text("{not json}\n", encoding="utf-8")
    result = verify_jsonl_file(path, require_pass=True)
    assert result.verifier_verdict == "FAIL"
    assert any("malformed JSON" in violation for violation in result.violations)


def test_new_python_files_have_no_broker_mutation_call_sites():
    repo_root = Path(__file__).resolve().parents[1]
    candidates = [
        repo_root / "quantcore/execution/h024_exact_ticket_canary_close_modify_governance.py",
        repo_root / "scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py",
        repo_root / "scripts/verify_h024_exact_ticket_canary_close_modify_governance_jsonl.py",
    ]
    forbidden_attrs = {"order_check", "order_send", "symbol_select"}
    for candidate in candidates:
        tree = ast.parse(candidate.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            assert not (
                isinstance(node, ast.Attribute) and node.attr in forbidden_attrs
            ), f"{candidate} contains forbidden MT5 mutation/preflight call {node.attr}"
            assert not (
                isinstance(node, ast.Import)
                and any(alias.name == "MetaTrader5" for alias in node.names)
            ), f"{candidate} imports MetaTrader5"
            assert not (
                isinstance(node, ast.ImportFrom)
                and node.module == "MetaTrader5"
            ), f"{candidate} imports MetaTrader5"
