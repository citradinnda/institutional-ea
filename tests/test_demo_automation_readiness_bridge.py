from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.build_demo_automation_readiness_bridge_jsonl import (
    ALLOWED_DEMO_SYMBOLS,
    BANNED_SYMBOLS,
    EXPECTED_POST_CLOSE_STATE,
    MAX_PORTFOLIO_HEAT_PCT,
    MAX_RISK_PER_TRADE_PCT,
    build_packet,
)


SCRIPT_PATH = Path("scripts/build_demo_automation_readiness_bridge_jsonl.py")


def write_completion(path: Path, **overrides: object) -> None:
    payload = {
        "verdict": "PASS",
        "operator_state": "H024_POST_CLOSE_OPERATIONAL_COMPLETION_ACCEPTED",
        "post_close_operational_state": EXPECTED_POST_CLOSE_STATE,
        "demo_automation_readiness_transition_allowed": True,
        "demo_automation_next_target": "DEMO_AUTOMATION_READINESS_BRIDGE",
        "exact_ticket_open": False,
        "h024_position_count": 0,
        "h024_order_count": 0,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
    }
    payload.update(overrides)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def test_passes_when_h024_post_close_completion_allows_demo_automation_bridge(tmp_path: Path) -> None:
    completion = tmp_path / "completion.jsonl"
    write_completion(completion)

    packet = build_packet(completion)

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == "DEMO_AUTOMATION_READINESS_BRIDGE_ACCEPTED"
    assert packet["demo_automation_bridge_state"] == "READY_FOR_INERT_DEMO_ENTRY_REQUEST_PREVIEW"
    assert packet["ready_for_inert_demo_entry_preview"] is True
    assert packet["controlled_demo_automation_track_open"] is True
    assert packet["first_order_capable_step_authorized"] is False
    assert packet["next_target"] == "INERT_DEMO_ENTRY_REQUEST_PREVIEW"
    assert packet["allowed_demo_symbols"] == ["USDJPYm", "XAUUSDm"]
    assert packet["banned_symbols"] == ["EURUSDm", "GBPUSDm", "US500m"]
    assert packet["max_risk_per_trade_pct"] == 0.5
    assert packet["max_portfolio_heat_pct"] == 1.0
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["order_check_authorized"] is False
    assert packet["order_send_authorized"] is False
    assert packet["symbol_select_authorized"] is False
    assert packet["unattended_loop_authorized"] is False
    assert packet["executable_trade_request_authorized"] is False
    assert packet["violations"] == []


@pytest.mark.parametrize(
    ("key", "value", "expected_code"),
    [
        ("verdict", "FAIL_CLOSED", "completion_verdict_not_pass"),
        ("operator_state", "WRONG", "completion_operator_state_unexpected"),
        ("post_close_operational_state", "WRONG", "post_close_operational_state_unexpected"),
        ("demo_automation_readiness_transition_allowed", False, "completion_transition_not_allowed"),
        ("demo_automation_next_target", "WRONG", "completion_next_target_unexpected"),
        ("exact_ticket_open", True, "exact_ticket_open_not_false"),
        ("h024_position_count", 1, "h024_position_count_not_zero"),
        ("h024_order_count", 1, "h024_order_count_not_zero"),
        ("trading_authorized", True, "completion_trading_authorized_not_false"),
        ("broker_mutation_authorized", True, "completion_broker_mutation_authorized_not_false"),
    ],
)
def test_fails_closed_when_completion_report_is_not_safe_for_bridge(
    tmp_path: Path,
    key: str,
    value: object,
    expected_code: str,
) -> None:
    completion = tmp_path / "completion.jsonl"
    write_completion(completion, **{key: value})

    packet = build_packet(completion)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["demo_automation_bridge_state"] == "UNVERIFIED"
    assert packet["ready_for_inert_demo_entry_preview"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["order_check_authorized"] is False
    assert packet["order_send_authorized"] is False
    assert packet["symbol_select_authorized"] is False
    assert any(v["code"] == expected_code for v in packet["violations"])


def test_fails_closed_when_completion_report_is_missing(tmp_path: Path) -> None:
    packet = build_packet(tmp_path / "missing_completion.jsonl")

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["operator_state"] == "FAIL_CLOSED_DEMO_AUTOMATION_BRIDGE_COMPLETION_EVIDENCE_UNAVAILABLE"
    assert packet["demo_automation_bridge_state"] == "UNVERIFIED"
    assert packet["ready_for_inert_demo_entry_preview"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == "completion_report_unreadable" for v in packet["violations"])


def test_fails_closed_when_completion_report_is_malformed(tmp_path: Path) -> None:
    completion = tmp_path / "completion.jsonl"
    completion.write_text("{not json}\n", encoding="utf-8")

    packet = build_packet(completion)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["demo_automation_bridge_state"] == "UNVERIFIED"
    assert packet["ready_for_inert_demo_entry_preview"] is False
    assert any(v["code"] == "completion_report_unreadable" for v in packet["violations"])


def test_symbol_and_risk_policy_matches_strategy_graveyard_carry_forward() -> None:
    assert ALLOWED_DEMO_SYMBOLS == ["USDJPYm", "XAUUSDm"]
    assert BANNED_SYMBOLS == ["EURUSDm", "GBPUSDm", "US500m"]
    assert MAX_RISK_PER_TRADE_PCT == 0.5
    assert MAX_PORTFOLIO_HEAT_PCT == 1.0


def test_cli_writes_jsonl_and_text_outputs(tmp_path: Path) -> None:
    completion = tmp_path / "completion.jsonl"
    output_jsonl = tmp_path / "bridge.jsonl"
    output_text = tmp_path / "bridge.txt"
    write_completion(completion)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--completion-report",
            str(completion),
            "--output-jsonl",
            str(output_jsonl),
            "--output-text",
            str(output_text),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    packet = json.loads(output_jsonl.read_text(encoding="utf-8"))
    text = output_text.read_text(encoding="utf-8")

    assert packet["verdict"] == "PASS"
    assert packet["ready_for_inert_demo_entry_preview"] is True
    assert packet["next_target"] == "INERT_DEMO_ENTRY_REQUEST_PREVIEW"
    assert "Allowed demo symbols: USDJPYm, XAUUSDm" in text
    assert "Order check authorized: False" in text
    assert "Order send authorized: False" in text


def test_script_is_read_only_and_contains_no_broker_execution_api() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")

    forbidden_snippets = [
        "import MetaTrader5",
        "from MetaTrader5",
        "mt5.",
        "order_send(",
        "order_check(",
        "symbol_select(",
        "TRADE_ACTION",
        "ORDER_TYPE_BUY",
        "ORDER_TYPE_SELL",
    ]

    for snippet in forbidden_snippets:
        assert snippet not in source
