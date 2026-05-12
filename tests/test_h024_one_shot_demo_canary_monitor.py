from __future__ import annotations

from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_monitor import (
    EXPECTED_CURRENCY,
    EXPECTED_ENTRY_DEAL,
    EXPECTED_MAGIC,
    EXPECTED_POSITION_TICKET,
    EXPECTED_PRICE_OPEN,
    EXPECTED_SERVER,
    EXPECTED_SL,
    EXPECTED_SYMBOL,
    EXPECTED_TYPE,
    EXPECTED_VOLUME,
    READ_ONLY_MT5_CALLS,
    build_monitor_record,
    verify_monitor_records,
)


def account(**overrides):
    base = {
        "login": 123456,
        "server": EXPECTED_SERVER,
        "currency": EXPECTED_CURRENCY,
        "trade_mode": 0,
        "balance": 10000.0,
        "equity": 9998.45,
        "margin": 2.36,
        "margin_free": 9996.09,
        "margin_level": 423647.0,
    }
    base.update(overrides)
    return base


def position(**overrides):
    base = {
        "ticket": EXPECTED_POSITION_TICKET,
        "identifier": EXPECTED_POSITION_TICKET,
        "symbol": EXPECTED_SYMBOL,
        "magic": EXPECTED_MAGIC,
        "type": EXPECTED_TYPE,
        "volume": EXPECTED_VOLUME,
        "price_open": EXPECTED_PRICE_OPEN,
        "price_current": 4730.0,
        "profit": -1.55,
        "swap": 0.0,
        "sl": EXPECTED_SL,
        "tp": 0.0,
        "comment": "H024_ONE_SHOT_DE",
    }
    base.update(overrides)
    return base


def entry_deal(**overrides):
    base = {
        "deal": EXPECTED_ENTRY_DEAL,
        "position_id": EXPECTED_POSITION_TICKET,
        "order": EXPECTED_POSITION_TICKET,
        "symbol": EXPECTED_SYMBOL,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "entry": 0,
        "type": EXPECTED_TYPE,
    }
    base.update(overrides)
    return base


def close_deal(**overrides):
    base = {
        "deal": EXPECTED_ENTRY_DEAL + 10,
        "position_id": EXPECTED_POSITION_TICKET,
        "order": EXPECTED_POSITION_TICKET + 10,
        "symbol": EXPECTED_SYMBOL,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "entry": 1,
        "type": 0,
    }
    base.update(overrides)
    return base


def ledger_success(**overrides):
    base = {
        "allowed_demo_server": EXPECTED_SERVER,
        "attempt_stage": "send_succeeded",
        "symbol": EXPECTED_SYMBOL,
        "order_send_result": {"order": EXPECTED_POSITION_TICKET, "deal": EXPECTED_ENTRY_DEAL, "retcode": 10009},
        "request": {"magic": EXPECTED_MAGIC, "volume": EXPECTED_VOLUME, "type": EXPECTED_TYPE, "sl": EXPECTED_SL},
    }
    base.update(overrides)
    return base


def monitor_record(**overrides):
    base = {
        "generated_at_utc": "2026-05-12T00:00:00Z",
        "account": account(),
        "positions": [position()],
        "pending_orders": [],
        "history_deals": [entry_deal()],
        "ledger_records": [ledger_success()],
    }
    base.update(overrides)
    return build_monitor_record(**base)


def violation_codes(record):
    return {violation["code"] for violation in record["violations"]}


def test_open_canary_position_passes():
    record = monitor_record()
    assert record["verdict"] == "PASS"
    assert record["lifecycle_state"] == "open"
    assert record["observed"]["exact_canary_position_count"] == 1
    assert record["observed"]["ledger_success_count"] == 1
    assert record["latest_known"]["profit"] == -1.55


def test_closed_canary_with_matching_history_passes():
    record = monitor_record(positions=[], history_deals=[entry_deal(), close_deal()])
    assert record["verdict"] == "PASS"
    assert record["lifecycle_state"] == "closed_explained"
    assert record["observed"]["matching_close_deal_count"] == 1


def test_wrong_server_fails():
    record = monitor_record(account=account(server="OtherServer"))
    assert record["verdict"] == "FAIL"
    assert "account_server_mismatch" in violation_codes(record)


def test_extra_h024_position_fails():
    record = monitor_record(positions=[position(), position(ticket=999, identifier=999, price_open=4800.0)])
    assert record["verdict"] == "FAIL"
    assert "unexpected_h024_positions" in violation_codes(record)


def test_pending_h024_order_fails():
    order = {"ticket": 100, "symbol": EXPECTED_SYMBOL, "magic": EXPECTED_MAGIC, "volume_current": 0.01, "comment": "H024_ONE_SHOT_DE"}
    record = monitor_record(pending_orders=[order])
    assert record["verdict"] == "FAIL"
    assert "unexpected_h024_pending_orders" in violation_codes(record)


def test_second_entry_deal_fails():
    second_entry = entry_deal(deal=EXPECTED_ENTRY_DEAL + 1, position_id=EXPECTED_POSITION_TICKET + 1, order=EXPECTED_POSITION_TICKET + 1)
    record = monitor_record(history_deals=[entry_deal(), second_entry])
    assert record["verdict"] == "FAIL"
    assert "second_h024_entry_deal_detected" in violation_codes(record)


def test_duplicate_successful_ledger_fails():
    record = monitor_record(ledger_records=[ledger_success(), ledger_success()])
    assert record["verdict"] == "FAIL"
    assert "ledger_success_count_mismatch" in violation_codes(record)


def test_no_open_position_without_close_history_fails():
    record = monitor_record(positions=[], history_deals=[entry_deal()])
    assert record["verdict"] == "FAIL"
    assert record["lifecycle_state"] == "no_open_position_without_matching_close_history"
    assert "no_open_position_without_matching_close_history" in violation_codes(record)


def test_packet_verifier_requires_single_pass_record():
    record = monitor_record()
    assert verify_monitor_records([record], require_pass=True) == []
    assert verify_monitor_records([], require_pass=True)[0]["code"] == "monitor_record_count_mismatch"


def test_monitor_declares_read_only_mt5_call_contract():
    record = monitor_record()
    assert record["mt5_read_only_calls_allowed"] == READ_ONLY_MT5_CALLS
    assert "mt5.order_send" in record["mt5_mutating_calls_declared_forbidden"]
    assert "mt5.order_check" in record["mt5_mutating_calls_declared_forbidden"]


def test_builder_script_contains_no_mutating_mt5_calls():
    source = Path("scripts/build_h024_one_shot_demo_canary_monitor_jsonl.py").read_text(encoding="utf-8")
    for forbidden_call in ("mt5.order_send", "mt5.order_check"):
        assert forbidden_call not in source