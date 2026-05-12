from __future__ import annotations

from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_lifecycle_decision import (
    DECISION_CONTINUE_HOLD,
    build_lifecycle_decision_record,
    verify_lifecycle_decision_records,
)


def monitor_record(**overrides):
    base = {
        "schema_version": "h024_one_shot_demo_canary_monitor.v1",
        "generated_at_utc": "2026-05-12T00:00:00Z",
        "strategy": "H024",
        "lifecycle_state": "open",
        "verdict": "PASS",
        "violations": [],
        "expected_canary": {
            "server": "Exness-MT5Trial6",
            "currency": "USD",
            "symbol": "XAUUSDm",
            "side": "sell",
            "magic": 240024,
            "volume": 0.01,
            "position_ticket": 4413054432,
            "entry_deal": 3788869526,
            "price_open": 4728.4490000000005,
            "sl": 4817.394,
        },
        "observed": {
            "exact_canary_position_count": 1,
            "unexpected_h024_pending_order_count": 0,
            "second_entry_deal_count": 0,
            "ledger_success_count": 1,
        },
        "latest_known": {
            "price_current": 4759.074,
            "profit": -30.62,
            "swap": 0.0,
            "equity": 9969.38,
            "margin": 2.36,
            "margin_free": 9967.02,
            "margin_level": 422431.36,
            "balance": 10000.0,
        },
    }
    base.update(overrides)
    return base


def lifecycle_record(source=None):
    return build_lifecycle_decision_record(
        generated_at_utc="2026-05-12T00:00:00Z",
        monitor_record=source or monitor_record(),
    )


def violation_codes(record):
    return {violation["code"] for violation in record["violations"]}


def test_open_passing_monitor_builds_continue_hold_pass_record():
    record = lifecycle_record()
    assert record["verdict"] == "PASS"
    assert record["decision"] == DECISION_CONTINUE_HOLD
    assert record["latest_known"]["profit"] == -30.62
    assert record["safety_contract"]["broker_mutation_authorized"] is False
    assert record["safety_contract"]["mt5_call_authorized"] is False
    assert record["safety_contract"]["close_authorized"] is False
    assert record["safety_contract"]["entry_authorized"] is False


def test_failing_monitor_fails_lifecycle_decision():
    source = monitor_record(verdict="FAIL", violations=[{"code": "example", "detail": {}}])
    record = lifecycle_record(source)
    assert record["verdict"] == "FAIL"
    assert "monitor_verdict_not_pass" in violation_codes(record)
    assert "monitor_embedded_violations_present" in violation_codes(record)


def test_closed_monitor_cannot_be_continue_hold_decision():
    source = monitor_record(lifecycle_state="closed_explained")
    record = lifecycle_record(source)
    assert record["verdict"] == "FAIL"
    assert "monitor_lifecycle_state_not_open_for_hold" in violation_codes(record)


def test_unexpected_pending_order_count_fails():
    source = monitor_record(
        observed={
            "exact_canary_position_count": 1,
            "unexpected_h024_pending_order_count": 1,
            "second_entry_deal_count": 0,
            "ledger_success_count": 1,
        }
    )
    record = lifecycle_record(source)
    assert record["verdict"] == "FAIL"
    assert "monitor_unexpected_h024_pending_order_count_mismatch" in violation_codes(record)


def test_verifier_accepts_single_pass_record():
    record = lifecycle_record()
    assert verify_lifecycle_decision_records([record], require_pass=True) == []


def test_verifier_rejects_missing_or_extra_records():
    assert verify_lifecycle_decision_records([], require_pass=True)[0]["code"] == "lifecycle_decision_record_count_mismatch"
    record = lifecycle_record()
    assert verify_lifecycle_decision_records([record, record], require_pass=True)[0]["code"] == "lifecycle_decision_record_count_mismatch"


def test_verifier_rejects_any_authorized_mutation():
    record = lifecycle_record()
    record["safety_contract"]["broker_mutation_authorized"] = True
    violations = verify_lifecycle_decision_records([record], require_pass=True)
    assert any(violation["code"] == "safety_contract_broker_mutation_authorized_not_false" for violation in violations)


def test_scripts_and_module_contain_no_mt5_or_mutating_broker_calls():
    paths = [
        Path("quantcore/execution/h024_one_shot_demo_canary_lifecycle_decision.py"),
        Path("scripts/build_h024_one_shot_demo_canary_lifecycle_decision_jsonl.py"),
        Path("scripts/verify_h024_one_shot_demo_canary_lifecycle_decision_jsonl.py"),
    ]
    forbidden_tokens = ["MetaTrader5", "mt5.", "order_send", "order_check"]
    for path in paths:
        source = path.read_text(encoding="utf-8")
        for token in forbidden_tokens:
            assert token not in source