from __future__ import annotations

import json
from pathlib import Path

from quantcore.execution.h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate import (
    AUTHORIZATION_KEYS,
    EXPECTED_DECISION_STATUS,
    EXPECTED_IDENTIFIER,
    EXPECTED_MAGIC,
    EXPECTED_MODEL_SYMBOL,
    EXPECTED_MT5_POSITION_TYPE,
    EXPECTED_REQUESTED_ACTION,
    EXPECTED_RUNTIME_SYMBOL,
    EXPECTED_SIDE,
    EXPECTED_TICKET,
    EXPECTED_VOLUME,
    FAIL_VERDICT,
    OK_OPERATOR_STATE,
    PACKET_TYPE,
    PASS_VERDICT,
    SCHEMA_VERSION,
    STRATEGY,
    UPSTREAM_PACKET_TYPES,
    build_pre_action_evidence_aggregate_record,
    load_latest_jsonl_record,
    read_jsonl,
    validate_aggregate_record,
    verify_jsonl_path,
    write_jsonl_record,
)

NOW = "2026-05-12T04:00:00Z"
OLD = "2026-05-12T03:40:00Z"


def _auth_false() -> dict[str, bool]:
    return {key: False for key in AUTHORIZATION_KEYS}


def _base_upstream(key: str, *, observed_at: str = NOW) -> dict:
    record = {
        "schema_version": "1.0",
        "strategy": STRATEGY,
        "packet_type": UPSTREAM_PACKET_TYPES[key],
        "observed_at_utc": observed_at,
        "verdict": PASS_VERDICT,
        "violations": [],
        "effective_new_entries_blocked": True,
        **_auth_false(),
        "operator_state": f"{key}_OK_BUT_ACTION_NOT_AUTHORIZED",
        "operator_next_action": "KEEP_BLOCKED",
    }
    if key in {"unified_runtime_supervision", "exact_ticket_governance"}:
        record.update(
            {
                "exact_canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
                "exact_canary_observed": True,
                "h024_position_count": 1,
                "h024_order_count": 0,
                "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
                "model_symbol": EXPECTED_MODEL_SYMBOL,
                "side": EXPECTED_SIDE,
                "mt5_position_type": EXPECTED_MT5_POSITION_TYPE,
                "volume": EXPECTED_VOLUME,
                "magic": EXPECTED_MAGIC,
                "ticket": EXPECTED_TICKET,
                "identifier": EXPECTED_IDENTIFIER,
            }
        )
    if key == "exact_ticket_governance":
        record.update({"human_decision": EXPECTED_DECISION_STATUS})
    if key == "decision_artifact":
        record.update(
            {
                "decision_timestamp_utc": observed_at,
                "decision_status": EXPECTED_DECISION_STATUS,
                "requested_action": EXPECTED_REQUESTED_ACTION,
                "exact_ticket": EXPECTED_TICKET,
                "exact_identifier": EXPECTED_IDENTIFIER,
                "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
                "model_symbol": EXPECTED_MODEL_SYMBOL,
                "side": EXPECTED_SIDE,
                "mt5_position_type": EXPECTED_MT5_POSITION_TYPE,
                "volume": EXPECTED_VOLUME,
                "magic": EXPECTED_MAGIC,
            }
        )
    return record


def _upstreams(**overrides) -> dict:
    records = {key: _base_upstream(key) for key in UPSTREAM_PACKET_TYPES}
    records.update(overrides)
    return records


def test_happy_path_passes_and_authorizes_nothing() -> None:
    record = build_pre_action_evidence_aggregate_record(
        _upstreams(), observed_at_utc=NOW, user_reported_position_open_over_three_bars=True
    )
    assert record["schema_version"] == SCHEMA_VERSION
    assert record["strategy"] == STRATEGY
    assert record["packet_type"] == PACKET_TYPE
    assert record["verdict"] == PASS_VERDICT
    assert record["operator_state"] == OK_OPERATOR_STATE
    assert record["operator_context"]["user_reported_position_open_over_three_bars"] is True
    assert record["operator_context"]["bar_age_is_action_authorization"] is False
    assert record["effective_new_entries_blocked"] is True
    for key in AUTHORIZATION_KEYS:
        assert record[key] is False
        assert record["authorizations"][key] is False
    assert validate_aggregate_record(record) == []


def test_missing_upstream_fails_closed() -> None:
    records = _upstreams()
    records.pop("no_mutation_gate")
    record = build_pre_action_evidence_aggregate_record(records, observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("missing or non-object upstream record" in violation for violation in record["violations"])


def test_upstream_non_pass_fails_closed() -> None:
    gate = _base_upstream("no_mutation_gate")
    gate["verdict"] = FAIL_VERDICT
    record = build_pre_action_evidence_aggregate_record(_upstreams(no_mutation_gate=gate), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("upstream verdict is not PASS" in violation for violation in record["violations"])


def test_stale_upstream_fails_closed() -> None:
    gate = _base_upstream("no_mutation_gate", observed_at=OLD)
    record = build_pre_action_evidence_aggregate_record(
        _upstreams(no_mutation_gate=gate), observed_at_utc=NOW, max_upstream_age_seconds=60
    )
    assert record["verdict"] == FAIL_VERDICT
    assert any("stale" in violation for violation in record["violations"])


def test_future_ambiguous_upstream_fails_closed() -> None:
    gate = _base_upstream("no_mutation_gate", observed_at="2026-05-12T04:10:00Z")
    record = build_pre_action_evidence_aggregate_record(
        _upstreams(no_mutation_gate=gate), observed_at_utc=NOW, future_tolerance_seconds=10
    )
    assert record["verdict"] == FAIL_VERDICT
    assert any("too far in the future" in violation for violation in record["violations"])


def test_embedded_upstream_violations_fail_closed() -> None:
    gate = _base_upstream("no_mutation_gate")
    gate["violations"] = ["unsafe"]
    record = build_pre_action_evidence_aggregate_record(_upstreams(no_mutation_gate=gate), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("embedded violations" in violation for violation in record["violations"])


def test_any_authorization_true_fails_closed() -> None:
    gate = _base_upstream("no_mutation_gate")
    gate["order_send_authorized"] = True
    record = build_pre_action_evidence_aggregate_record(_upstreams(no_mutation_gate=gate), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("order_send_authorized" in violation for violation in record["violations"])


def test_effective_new_entries_not_blocked_fails_closed() -> None:
    gate = _base_upstream("no_mutation_gate")
    gate["effective_new_entries_blocked"] = False
    record = build_pre_action_evidence_aggregate_record(_upstreams(no_mutation_gate=gate), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("effective_new_entries_blocked" in violation for violation in record["violations"])


def test_ticket_mismatch_fails_closed() -> None:
    decision = _base_upstream("decision_artifact")
    decision["exact_ticket"] = 123
    record = build_pre_action_evidence_aggregate_record(_upstreams(decision_artifact=decision), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("ticket mismatch" in violation for violation in record["violations"])


def test_identifier_mismatch_fails_closed() -> None:
    decision = _base_upstream("decision_artifact")
    decision["exact_identifier"] = 123
    record = build_pre_action_evidence_aggregate_record(_upstreams(decision_artifact=decision), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("identifier mismatch" in violation for violation in record["violations"])


def test_identity_mismatch_fails_closed() -> None:
    decision = _base_upstream("decision_artifact")
    decision["runtime_symbol"] = "USDJPYm"
    record = build_pre_action_evidence_aggregate_record(_upstreams(decision_artifact=decision), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("runtime_symbol mismatch" in violation for violation in record["violations"])


def test_missing_required_decision_identity_fails_closed() -> None:
    decision = _base_upstream("decision_artifact")
    decision.pop("exact_ticket")
    decision.pop("ticket", None)
    record = build_pre_action_evidence_aggregate_record(_upstreams(decision_artifact=decision), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("missing required exact canary identity field ticket" in violation for violation in record["violations"])


def test_canary_not_observed_fails_closed() -> None:
    unified = _base_upstream("unified_runtime_supervision")
    unified["exact_canary_observed"] = False
    record = build_pre_action_evidence_aggregate_record(
        _upstreams(unified_runtime_supervision=unified), observed_at_utc=NOW
    )
    assert record["verdict"] == FAIL_VERDICT
    assert any("exact canary observed" in violation for violation in record["violations"])


def test_ambiguous_decision_action_fails_closed() -> None:
    decision = _base_upstream("decision_artifact")
    decision["requested_action"] = "CLOSE_NOW"
    record = build_pre_action_evidence_aggregate_record(_upstreams(decision_artifact=decision), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("requested_action" in violation for violation in record["violations"])


def test_governance_close_modify_intent_fails_closed() -> None:
    governance = _base_upstream("exact_ticket_governance")
    governance["requested_action"] = "MODIFY_SL"
    record = build_pre_action_evidence_aggregate_record(
        _upstreams(exact_ticket_governance=governance), observed_at_utc=NOW
    )
    assert record["verdict"] == FAIL_VERDICT
    assert any("requested_action is not non-authorizing" in violation for violation in record["violations"])


def test_verifier_rejects_aggregate_with_embedded_violations(tmp_path: Path) -> None:
    record = build_pre_action_evidence_aggregate_record(_upstreams(), observed_at_utc=NOW)
    record["violations"] = ["tampered"]
    path = tmp_path / "aggregate.jsonl"
    write_jsonl_record(path, record)
    ok, violations, records = verify_jsonl_path(path, require_pass=True)
    assert not ok
    assert len(records) == 1
    assert any("embedded violations" in violation for violation in violations)


def test_verifier_rejects_require_pass_on_fail_record(tmp_path: Path) -> None:
    records = _upstreams()
    records.pop("decision_artifact")
    record = build_pre_action_evidence_aggregate_record(records, observed_at_utc=NOW)
    path = tmp_path / "aggregate.jsonl"
    write_jsonl_record(path, record)
    ok, violations, _ = verify_jsonl_path(path, require_pass=True)
    assert not ok
    assert any("--require-pass" in violation for violation in violations)


def test_jsonl_reader_rejects_malformed_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text("{not-json}\n", encoding="utf-8")
    records, errors = read_jsonl(path)
    assert errors
    ok, violations, _ = verify_jsonl_path(path, require_pass=True)
    assert not ok
    assert violations


def test_load_latest_jsonl_record(tmp_path: Path) -> None:
    first = {"a": 1}
    second = {"a": 2}
    path = tmp_path / "records.jsonl"
    path.write_text(json.dumps(first) + "\n" + json.dumps(second) + "\n", encoding="utf-8")
    assert load_latest_jsonl_record(path) == second


def test_verifier_rejects_top_level_authorization_tamper(tmp_path: Path) -> None:
    record = build_pre_action_evidence_aggregate_record(_upstreams(), observed_at_utc=NOW)
    record["order_send_authorized"] = True
    path = tmp_path / "aggregate.jsonl"
    write_jsonl_record(path, record)
    ok, violations, _ = verify_jsonl_path(path, require_pass=True)
    assert not ok
    assert any("order_send_authorized" in violation for violation in violations)


def test_expected_identity_does_not_mask_observed_ticket_mismatch() -> None:
    decision = _base_upstream("decision_artifact")
    decision["expected"] = {"exact_ticket": EXPECTED_TICKET}
    decision["observed"] = {"exact_ticket": 123}
    record = build_pre_action_evidence_aggregate_record(_upstreams(decision_artifact=decision), observed_at_utc=NOW)
    assert record["verdict"] == FAIL_VERDICT
    assert any("ticket mismatch" in violation for violation in record["violations"])


def test_static_no_broker_mutation_call_sites_in_new_files() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    files = [
        repo_root / "quantcore" / "execution" / "h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.py",
        repo_root / "scripts" / "build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py",
        repo_root / "scripts" / "verify_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py",
    ]
    forbidden_call_patterns = (
        "order_send(",
        "order_check(",
        "symbol_select(",
    )
    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        compact = text.replace(" ", "")
        for pattern in forbidden_call_patterns:
            assert pattern not in compact
        assert "MetaTrader5" not in text

def test_noisy_runtime_market_data_symbol_does_not_create_identity_mismatch() -> None:
    gate = _base_upstream("no_mutation_gate")
    gate["nested_runtime_market_data"] = {
        "symbols": [
            {
                "symbol": "USDJPYm",
                "bid": 157.563,
                "ask": 157.573,
                "spread_points": 10.0,
            },
            {
                "symbol": "XAUUSDm",
                "bid": 4713.416,
                "ask": 4713.812,
                "spread_points": 396.0,
            },
        ]
    }

    record = build_pre_action_evidence_aggregate_record(
        _upstreams(no_mutation_gate=gate),
        observed_at_utc=NOW,
        user_reported_position_open_over_three_bars=True,
    )

    assert record["verdict"] == PASS_VERDICT
    assert validate_aggregate_record(record) == []

def test_decision_artifact_check_field_observed_values_are_unwrapped() -> None:
    decision = _base_upstream("decision_artifact")
    decision["checks"] = {
        "exact_canary_identity": {
            "fields": {
                "ticket": {"expected": 4413054432, "observed": 4413054432, "passed": True},
                "identifier": {"expected": 4413054432, "observed": 4413054432, "passed": True},
                "runtime_symbol": {"expected": "XAUUSDm", "observed": "XAUUSDm", "passed": True},
                "model_symbol": {"expected": "XAUUSD", "observed": "XAUUSD", "passed": True},
                "side": {"expected": "sell", "observed": "sell", "passed": True},
                "mt5_position_type": {"expected": 1, "observed": 1, "passed": True},
                "volume": {"expected": 0.01, "observed": 0.01, "passed": True},
                "magic": {"expected": 240024, "observed": 240024, "passed": True},
            }
        },
        "operator_intent": {
            "decision_status": {
                "expected": "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
                "observed": "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
                "passed": True,
            },
            "requested_action": {
                "expected": "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
                "observed": "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
                "passed": True,
            },
        },
    }

    record = build_pre_action_evidence_aggregate_record(
        _upstreams(decision_artifact=decision),
        observed_at_utc=NOW,
        user_reported_position_open_over_three_bars=True,
    )

    assert record["verdict"] == PASS_VERDICT
    assert validate_aggregate_record(record) == []


def test_unified_supervision_nested_exact_canary_observed_true_is_accepted() -> None:
    unified = _base_upstream("unified_runtime_supervision")
    unified.pop("exact_canary_observed", None)
    unified["runtime_safety_aggregate"] = {
        "record": {
            "canary_summary": {
                "exact_canary_observed": True,
                "exact_canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
            }
        }
    }

    record = build_pre_action_evidence_aggregate_record(
        _upstreams(unified_runtime_supervision=unified),
        observed_at_utc=NOW,
        user_reported_position_open_over_three_bars=True,
    )

    assert record["verdict"] == PASS_VERDICT
    assert validate_aggregate_record(record) == []
