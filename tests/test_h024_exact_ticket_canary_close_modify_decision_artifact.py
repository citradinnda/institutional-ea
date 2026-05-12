from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json

from quantcore.execution.h024_exact_ticket_canary_close_modify_decision_artifact import (
    ARTIFACT_TYPE,
    AUTHORIZATION_FIELDS,
    EXPECTED_CANARY,
    PACKET_TYPE,
    PASS_OPERATOR_NEXT_ACTION,
    PASS_OPERATOR_STATE,
    SCHEMA_VERSION,
    STRATEGY,
    build_default_decision_artifact,
    validate_decision_artifact,
    verify_jsonl,
    write_jsonl_record,
)

NOW = datetime(2026, 5, 12, 4, 0, 0, tzinfo=timezone.utc)


def valid_artifact() -> dict:
    return build_default_decision_artifact(now=NOW)


def record_for(artifact: dict) -> dict:
    return validate_decision_artifact(artifact, now=NOW)


def test_valid_default_decision_artifact_passes_read_only() -> None:
    record = record_for(valid_artifact())
    assert record["verdict"] == "PASS"
    assert record["operator_state"] == PASS_OPERATOR_STATE
    assert record["operator_next_action"] == PASS_OPERATOR_NEXT_ACTION
    assert record["violations"] == []


def test_pass_record_keeps_every_authorization_false() -> None:
    record = record_for(valid_artifact())
    assert record["effective_new_entries_blocked"] is True
    for field in AUTHORIZATION_FIELDS:
        assert record["authorizations"][field] is False


def test_valid_review_only_close_intent_passes_without_authorization() -> None:
    artifact = valid_artifact()
    artifact["operator_intent"]["requested_action"] = "REQUEST_EXACT_TICKET_CLOSE_REVIEW_ONLY"
    record = record_for(artifact)
    assert record["verdict"] == "PASS"
    assert record["authorizations"]["close_modify_authorized"] is False


def test_missing_artifact_fails_closed() -> None:
    record = validate_decision_artifact(None, now=NOW)
    assert record["verdict"] == "FAIL_CLOSED"
    assert record["authorizations"]["broker_mutation_authorized"] is False


def test_wrong_schema_version_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["schema_version"] = 2
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_wrong_strategy_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["strategy"] = "H025"
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_wrong_artifact_type_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["artifact_type"] = "wrong_packet"
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_stale_decision_timestamp_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["decision_timestamp_utc"] = (NOW - timedelta(seconds=301)).isoformat().replace("+00:00", "Z")
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_future_decision_timestamp_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["decision_timestamp_utc"] = (NOW + timedelta(seconds=31)).isoformat().replace("+00:00", "Z")
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_expired_decision_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["expires_at_utc"] = (NOW - timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_naive_timestamp_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["decision_timestamp_utc"] = "2026-05-12T04:00:00"
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_exact_ticket_mismatch_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["exact_canary"]["ticket"] = 4413054433
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_exact_identifier_mismatch_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["exact_canary"]["identifier"] = 4413054433
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_runtime_symbol_mismatch_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["exact_canary"]["runtime_symbol"] = "XAUUSD"
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_model_symbol_mismatch_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["exact_canary"]["model_symbol"] = "USDJPY"
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_side_or_type_mismatch_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["exact_canary"]["side"] = "buy"
    artifact["exact_canary"]["mt5_position_type"] = 0
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_volume_mismatch_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["exact_canary"]["volume"] = 0.02
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_magic_mismatch_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["exact_canary"]["magic"] = 240025
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_missing_operator_intent_fails_closed() -> None:
    artifact = valid_artifact()
    artifact.pop("operator_intent")
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_ambiguous_operator_intent_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["operator_intent"]["intent_is_ambiguous"] = True
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_immediate_action_intent_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["operator_intent"]["immediate_action_requested"] = True
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_unsupported_operator_intent_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["operator_intent"]["requested_action"] = "CLOSE_NOW"
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_missing_attestation_fails_closed() -> None:
    artifact = valid_artifact()
    artifact.pop("operator_attestation")
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_contradictory_attestation_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["operator_attestation"]["attests_no_order_send_authorized"] = False
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_any_true_authorization_fails_closed() -> None:
    for field in AUTHORIZATION_FIELDS:
        artifact = valid_artifact()
        artifact["authorizations"][field] = True
        record = record_for(artifact)
        assert record["verdict"] == "FAIL_CLOSED", field
        assert record["authorizations"][field] is False


def test_missing_authorization_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["authorizations"].pop("order_check_authorized")
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_effective_new_entries_not_blocked_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["effective_new_entries_blocked"] = False
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_forbidden_broker_request_shape_fails_closed() -> None:
    artifact = valid_artifact()
    artifact["broker_request"] = {"ticket": EXPECTED_CANARY["ticket"]}
    assert record_for(artifact)["verdict"] == "FAIL_CLOSED"


def test_verifier_accepts_pass_jsonl(tmp_path) -> None:
    path = tmp_path / "packet.jsonl"
    write_jsonl_record(record_for(valid_artifact()), path)
    summary = verify_jsonl(path, require_pass=True)
    assert summary["verifier_verdict"] == "PASS"
    assert summary["record_count"] == 1


def test_verifier_rejects_fail_closed_when_require_pass(tmp_path) -> None:
    artifact = valid_artifact()
    artifact["strategy"] = "H025"
    path = tmp_path / "packet.jsonl"
    write_jsonl_record(record_for(artifact), path)
    summary = verify_jsonl(path, require_pass=True)
    assert summary["verifier_verdict"] == "FAIL"


def test_verifier_rejects_pass_with_embedded_violations(tmp_path) -> None:
    record = record_for(valid_artifact())
    record["violations"] = ["synthetic embedded violation"]
    path = tmp_path / "packet.jsonl"
    write_jsonl_record(record, path)
    summary = verify_jsonl(path, require_pass=True)
    assert summary["verifier_verdict"] == "FAIL"


def test_verifier_rejects_wrong_packet_type(tmp_path) -> None:
    record = record_for(valid_artifact())
    record["packet_type"] = "wrong"
    path = tmp_path / "packet.jsonl"
    write_jsonl_record(record, path)
    summary = verify_jsonl(path, require_pass=True)
    assert summary["verifier_verdict"] == "FAIL"


def test_verifier_rejects_unsafe_record_authorization(tmp_path) -> None:
    record = record_for(valid_artifact())
    record["authorizations"]["order_send_authorized"] = True
    path = tmp_path / "packet.jsonl"
    write_jsonl_record(record, path)
    summary = verify_jsonl(path, require_pass=True)
    assert summary["verifier_verdict"] == "FAIL"


def test_verifier_rejects_malformed_jsonl(tmp_path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text("not-json\n", encoding="utf-8")
    summary = verify_jsonl(path, require_pass=True)
    assert summary["verifier_verdict"] == "FAIL"


def test_verifier_rejects_empty_jsonl(tmp_path) -> None:
    path = tmp_path / "empty.jsonl"
    path.write_text("", encoding="utf-8")
    summary = verify_jsonl(path, require_pass=True)
    assert summary["verifier_verdict"] == "FAIL"


def test_constants_match_packet_identity() -> None:
    assert SCHEMA_VERSION == 1
    assert STRATEGY == "H024"
    assert PACKET_TYPE == ARTIFACT_TYPE
    assert EXPECTED_CANARY["ticket"] == 4413054432
    assert EXPECTED_CANARY["identifier"] == 4413054432
