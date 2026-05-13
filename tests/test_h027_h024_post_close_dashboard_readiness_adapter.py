from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.build_h027_h024_post_close_dashboard_readiness_adapter_jsonl import (
    EXPECTED_WORDING,
    build_packet,
)


SCRIPT_PATH = Path("scripts/build_h027_h024_post_close_dashboard_readiness_adapter_jsonl.py")


def write_h026(path: Path, **overrides: object) -> None:
    payload = {
        "verdict": "PASS",
        "operator_state": "H026_H024_POST_CLOSE_NO_OPEN_CANARY_INTENTIONALLY_CLOSED_BY_H025",
        "canary_absence_classification": "INTENTIONALLY_CLOSED_BY_H025",
        "dashboard_wording": EXPECTED_WORDING,
        "readiness_wording": EXPECTED_WORDING,
        "exact_ticket": 4413054432,
        "exact_identifier": 4413054432,
        "symbol": "XAUUSDm",
        "magic": 240024,
        "exact_ticket_open": False,
        "h024_position_count": 0,
        "h024_order_count": 0,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "entry_authorized": False,
        "close_all_authorized": False,
        "live_money_authorized": False,
    }
    payload.update(overrides)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def test_passes_when_h026_post_close_state_is_verified(tmp_path: Path) -> None:
    h026 = tmp_path / "h026.jsonl"
    write_h026(h026)

    packet = build_packet(h026)

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == "H027_H024_DASHBOARD_READINESS_ACCEPTS_H025_POST_CLOSE_NO_OPEN_CANARY"
    assert packet["dashboard_state"] == EXPECTED_WORDING
    assert packet["readiness_state"] == EXPECTED_WORDING
    assert packet["h024_dashboard_compatible"] is True
    assert packet["h024_readiness_compatible"] is True
    assert packet["legacy_open_canary_required"] is False
    assert packet["post_close_no_open_canary_accepted"] is True
    assert packet["exact_ticket_open"] is False
    assert packet["h024_position_count"] == 0
    assert packet["h024_order_count"] == 0
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["violations"] == []


@pytest.mark.parametrize(
    ("override_key", "override_value", "expected_code"),
    [
        ("verdict", "FAIL_CLOSED", "h026_verdict_not_pass"),
        ("canary_absence_classification", "UNEXPECTED_MISSING_CANARY_OR_H026_UNVERIFIED", "h026_absence_not_intentionally_closed"),
        ("exact_ticket_open", True, "exact_ticket_open_not_false"),
        ("h024_position_count", 1, "h024_position_count_not_zero"),
        ("h024_order_count", 1, "h024_order_count_not_zero"),
        ("trading_authorized", True, "h026_trading_authorized_not_false"),
        ("broker_mutation_authorized", True, "h026_broker_mutation_authorized_not_false"),
        ("dashboard_wording", "OLD FAILURE WORDING", "dashboard_wording_unexpected"),
        ("readiness_wording", "OLD FAILURE WORDING", "readiness_wording_unexpected"),
    ],
)
def test_fails_closed_when_h026_is_not_safe_for_dashboard_readiness(
    tmp_path: Path,
    override_key: str,
    override_value: object,
    expected_code: str,
) -> None:
    h026 = tmp_path / "h026.jsonl"
    write_h026(h026, **{override_key: override_value})

    packet = build_packet(h026)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["dashboard_state"] == "NO_OPEN_CANARY_UNVERIFIED"
    assert packet["readiness_state"] == "NO_OPEN_CANARY_UNVERIFIED"
    assert packet["h024_dashboard_compatible"] is False
    assert packet["h024_readiness_compatible"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == expected_code for v in packet["violations"])


def test_fails_closed_when_h026_report_is_missing(tmp_path: Path) -> None:
    packet = build_packet(tmp_path / "missing_h026.jsonl")

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["operator_state"] == "FAIL_CLOSED_H027_H026_POST_CLOSE_STATE_UNAVAILABLE"
    assert packet["dashboard_state"] == "NO_OPEN_CANARY_UNVERIFIED"
    assert packet["readiness_state"] == "NO_OPEN_CANARY_UNVERIFIED"
    assert packet["h024_dashboard_compatible"] is False
    assert packet["h024_readiness_compatible"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == "h026_report_unreadable" for v in packet["violations"])


def test_fails_closed_when_h026_report_is_malformed(tmp_path: Path) -> None:
    h026 = tmp_path / "h026.jsonl"
    h026.write_text("{not json}\n", encoding="utf-8")

    packet = build_packet(h026)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["dashboard_state"] == "NO_OPEN_CANARY_UNVERIFIED"
    assert packet["readiness_state"] == "NO_OPEN_CANARY_UNVERIFIED"
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == "h026_report_unreadable" for v in packet["violations"])


def test_cli_writes_jsonl_and_text_outputs(tmp_path: Path) -> None:
    h026 = tmp_path / "h026.jsonl"
    output_jsonl = tmp_path / "h027.jsonl"
    output_text = tmp_path / "h027.txt"
    write_h026(h026)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--h026-report",
            str(h026),
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
    assert packet["dashboard_state"] == EXPECTED_WORDING
    assert packet["readiness_state"] == EXPECTED_WORDING
    assert packet["h024_dashboard_compatible"] is True
    assert packet["h024_readiness_compatible"] is True
    assert EXPECTED_WORDING in text
    assert "Trading authorized: False" in text
    assert "Broker mutation authorized: False" in text


def test_cli_returns_nonzero_when_h026_is_unverified(tmp_path: Path) -> None:
    h026 = tmp_path / "h026.jsonl"
    output_jsonl = tmp_path / "h027.jsonl"
    output_text = tmp_path / "h027.txt"
    write_h026(h026, verdict="FAIL_CLOSED")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--h026-report",
            str(h026),
            "--output-jsonl",
            str(output_jsonl),
            "--output-text",
            str(output_text),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    packet = json.loads(output_jsonl.read_text(encoding="utf-8"))
    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["h024_dashboard_compatible"] is False
    assert packet["h024_readiness_compatible"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False


def test_h027_script_is_read_only_and_contains_no_broker_execution_api() -> None:
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
