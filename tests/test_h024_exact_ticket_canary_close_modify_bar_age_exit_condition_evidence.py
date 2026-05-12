from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

import pytest

from quantcore.execution import h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence as mod


def _write_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def _base_upstream(packet_type: str, *, observed_at=None, **overrides) -> dict:
    now = observed_at or mod.utc_now()
    record = {
        "schema_version": "1.0.0",
        "strategy": "H024",
        "packet_type": packet_type,
        "observed_at_utc": mod.format_utc(now),
        "verdict": "PASS",
        "violations": [],
        "exact_ticket": mod.EXPECTED_TICKET,
        "exact_identifier": mod.EXPECTED_IDENTIFIER,
        "exact_canary_state": mod.EXPECTED_CANARY_STATE,
        "exact_canary_observed": True,
        "canary_state": mod.EXPECTED_CANARY_STATE,
        "canary_observed": True,
        "h024_position_count": 1,
        "h024_order_count": 0,
        "decision_status": mod.NO_CLOSE_MODIFY_DECISION,
        "requested_action": mod.NO_CLOSE_MODIFY_DECISION,
        "effective_new_entries_blocked": True,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "xauusd_order_authorized": False,
        "usdjpy_order_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
    }
    record.update(overrides)
    return record


def _write_all_upstreams(tmp_path: Path, *, observed_at=None, mutate=None) -> dict[str, Path]:
    packet_types = {
        "no_mutation_gate": "h024_runtime_no_mutation_safety_gate",
        "unified_runtime_supervision": "h024_unified_read_only_post_canary_runtime_supervision",
        "exact_ticket_governance": "h024_exact_ticket_canary_close_modify_governance",
        "decision_artifact": "h024_exact_ticket_canary_close_modify_decision_artifact",
        "pre_action_evidence_aggregate": "h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate",
        "runtime_exposure_inventory": "h024_runtime_exposure_inventory_safety_supervisor",
        "runtime_account_risk_margin": "h024_runtime_account_risk_margin_safety_supervisor",
        "runtime_tick_spread": "h024_runtime_tick_spread_safety_supervisor",
    }
    paths: dict[str, Path] = {}
    for name, packet_type in packet_types.items():
        record = _base_upstream(packet_type, observed_at=observed_at)
        if name == "runtime_account_risk_margin":
            record.update(
                {
                    "account_server": "Exness-MT5Trial6",
                    "account_currency": "USD",
                    "balance": 10000.0,
                    "equity": 10013.0,
                    "profit": 13.0,
                    "margin": 2.36,
                    "free_margin": 10010.64,
                    "margin_level": 424000.0,
                    "margin_used_fraction": 0.00023,
                }
            )
        if name == "runtime_tick_spread":
            record["symbols"] = {
                "XAUUSDm": {
                    "symbol": "XAUUSDm",
                    "verdict": "PASS",
                    "bid": 4715.0,
                    "ask": 4715.3,
                    "spread_points": 300.0,
                    "tick_age_seconds": 0.5,
                },
                "USDJPYm": {
                    "symbol": "USDJPYm",
                    "verdict": "PASS",
                    "bid": 157.7,
                    "ask": 157.71,
                    "spread_points": 10.0,
                    "tick_age_seconds": 0.5,
                },
            }
        if mutate:
            mutate(name, record)
        path = tmp_path / f"{name}.jsonl"
        _write_jsonl(path, record)
        paths[name] = path
    return paths


def test_operator_reported_happy_path_passes(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == mod.PASS_OPERATOR_STATE
    assert record["bar_age_evidence"]["classification"] == "OPERATOR_REPORTED_ONLY"
    assert record["bar_age_evidence"]["operator_reported_only_caveat"] is True
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["close_modify_authorized"] is False
    assert record["trading_loop_authorized"] is False


def test_machine_validated_happy_path_passes(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        machine_validated_over_three_bars=True,
        machine_bar_count=4,
        bar_timeframe="M5",
        position_open_time_utc=mod.format_utc(observed_at - timedelta(minutes=25)),
    )

    assert record["verdict"] == "PASS"
    assert record["bar_age_evidence"]["classification"] == "MACHINE_VALIDATED"
    assert record["bar_age_evidence"]["sufficient_machine_evidence"] is True


def test_missing_upstream_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))
    paths["decision_artifact"] = tmp_path / "missing.jsonl"

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("missing upstream JSONL" in item for item in record["violations"])


def test_stale_upstream_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=1000))

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("stale" in item for item in record["violations"])


def test_future_skewed_upstream_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at + timedelta(seconds=1000))

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("future-skewed" in item for item in record["violations"])


def test_upstream_fail_verdict_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "pre_action_evidence_aggregate":
            record["verdict"] = "FAIL_CLOSED"
            record["violations"] = ["synthetic upstream failure"]

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("pre_action_evidence_aggregate" in item for item in record["violations"])


def test_unsafe_authorization_true_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "no_mutation_gate":
            record["broker_mutation_authorized"] = True

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("unsafe upstream authorization" in item for item in record["violations"])


def test_exact_ticket_mismatch_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "pre_action_evidence_aggregate":
            record["exact_ticket"] = 123

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("exact ticket mismatch" in item for item in record["violations"])


def test_exact_canary_not_observed_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "runtime_exposure_inventory":
            record["exact_canary_observed"] = False
            record["canary_observed"] = False
            record["exact_canary_state"] = "NOT_OBSERVED"
            record["canary_state"] = "NOT_OBSERVED"

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("canary is not observed" in item for item in record["violations"])


def test_extra_h024_order_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "runtime_exposure_inventory":
            record["h024_order_count"] = 1

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("unexpected H024 exposure/order state" in item for item in record["violations"])


def test_decision_artifact_action_implying_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "decision_artifact":
            record["requested_action"] = "CLOSE_NOW"

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("decision artifact" in item for item in record["violations"])


def test_missing_bar_age_evidence_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))

    record = mod.build_record(paths, observed_at=observed_at)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("missing over-three-bars evidence" in item for item in record["violations"])


def test_machine_validation_without_timeframe_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        machine_validated_over_three_bars=True,
        machine_bar_count=4,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("machine-validated bar age claimed" in item for item in record["violations"])


def test_verify_jsonl_happy_path(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)
    output = tmp_path / "record.jsonl"
    mod.write_jsonl(output, record)

    result = mod.verify_jsonl(output, require_pass=True)

    assert result["verifier_verdict"] == "PASS"
    assert result["record_verdict"] == "PASS"
    assert result["broker_mutation_authorized"] is False


def test_verify_require_pass_rejects_fail_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))
    record = mod.build_record(paths, observed_at=observed_at)
    output = tmp_path / "record.jsonl"
    mod.write_jsonl(output, record)

    result = mod.verify_jsonl(output, require_pass=True)

    assert result["verifier_verdict"] == "FAIL"
    assert any("--require-pass" in item for item in result["violations"])


def test_verify_malformed_jsonl_fails(tmp_path: Path) -> None:
    output = tmp_path / "bad.jsonl"
    output.write_text("{bad json\n", encoding="utf-8")

    result = mod.verify_jsonl(output, require_pass=True)

    assert result["verifier_verdict"] == "FAIL"
    assert any("malformed JSONL" in item for item in result["violations"])


def test_validate_wrong_packet_type_fails(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)
    record["packet_type"] = "wrong"

    violations = mod.validate_record(record)

    assert "wrong or missing packet_type" in violations


def test_validate_pass_record_with_authorization_true_fails(tmp_path: Path) -> None:
    observed_at = mod.utc_now()
    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5))
    record = mod.build_record(paths, observed_at=observed_at, position_open_over_three_bars=True)
    record["broker_mutation_authorized"] = True

    violations = mod.validate_record(record)

    assert "broker_mutation_authorized is not false" in violations


def test_static_module_has_no_broker_mutation_call_sites() -> None:
    source = Path(mod.__file__).read_text(encoding="utf-8")

    forbidden_fragments = [
        "MetaTrader5",
        "mt5.",
        ".order_send",
        ".order_check",
        ".symbol_select",
        "TRADE_ACTION",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in source


def test_wrapper_authorization_observed_false_passes_real_packet_shape(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name in {"no_mutation_gate", "pre_action_evidence_aggregate"}:
            record["broker_mutation_authorized"] = {
                "expected": False,
                "observed": False,
                "passed": True,
            }
            record["effective_new_entries_blocked"] = {
                "expected": True,
                "observed": True,
                "passed": True,
            }

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []


def test_wrapper_authorization_observed_true_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "no_mutation_gate":
            record["broker_mutation_authorized"] = {
                "expected": False,
                "observed": True,
                "passed": False,
            }

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("unsafe upstream authorization" in item for item in record["violations"])


def test_wrapper_decision_fields_are_unwrapped(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "decision_artifact":
            record["decision_status"] = {
                "expected": mod.NO_CLOSE_MODIFY_DECISION,
                "observed": mod.NO_CLOSE_MODIFY_DECISION,
                "passed": True,
            }
            record["requested_action"] = {
                "expected": mod.NO_CLOSE_MODIFY_DECISION,
                "observed": mod.NO_CLOSE_MODIFY_DECISION,
                "passed": True,
            }

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "PASS"
    assert record["exit_condition_evidence"]["decision_status"] == mod.NO_CLOSE_MODIFY_DECISION
    assert record["exit_condition_evidence"]["requested_action"] == mod.NO_CLOSE_MODIFY_DECISION


def test_passed_detail_check_for_effective_new_entries_blocked_is_accepted(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name in {"decision_artifact", "pre_action_evidence_aggregate"}:
            record["checks"] = {
                "effective_new_entries_blocked": {
                    "detail": "effective_new_entries_blocked must be true",
                    "passed": True,
                }
            }

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "PASS"
    assert record["violations"] == []


def test_failed_detail_check_for_effective_new_entries_blocked_fails_closed(tmp_path: Path) -> None:
    observed_at = mod.utc_now()

    def mutate(name: str, record: dict) -> None:
        if name == "decision_artifact":
            record["checks"] = {
                "effective_new_entries_blocked": {
                    "detail": "effective_new_entries_blocked must be true",
                    "passed": False,
                }
            }

    paths = _write_all_upstreams(tmp_path, observed_at=observed_at - timedelta(seconds=5), mutate=mutate)

    record = mod.build_record(
        paths,
        observed_at=observed_at,
        position_open_over_three_bars=True,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("unsafe upstream authorization" in item for item in record["violations"])
