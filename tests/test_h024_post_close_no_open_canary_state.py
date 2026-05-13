from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.build_h024_post_close_no_open_canary_state_jsonl import (
    EXPECTED_DASHBOARD_WORDING,
    build_packet,
)


SCRIPT_PATH = Path("scripts/build_h024_post_close_no_open_canary_state_jsonl.py")


def write_stage5(path: Path, **overrides: object) -> None:
    payload = {
        "verdict": "PASS",
        "stage": "H025_STAGE_5_POST_CLOSE_VERIFICATION",
        "operator_state": "H025_EXACT_TICKET_CANARY_POST_CLOSE_VERIFIED_NO_OPEN_CANARY",
        "post_close_verified": True,
        "open_canary_trade_exists": False,
        "exact_ticket_open": False,
        "h024_position_count": 0,
        "h024_order_count": 0,
        "read_only_verification_only": True,
        "broker_mutation_authorized": False,
        "trading_authorized": False,
        "history_deal_match_count": 2,
    }
    payload.update(overrides)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def test_passes_when_stage5_confirms_intentional_post_close_zero_exposure(tmp_path: Path) -> None:
    stage5 = tmp_path / "stage5.jsonl"
    write_stage5(stage5)

    packet = build_packet(stage5)

    assert packet["verdict"] == "PASS"
    assert packet["canary_absence_classification"] == "INTENTIONALLY_CLOSED_BY_H025"
    assert packet["exact_ticket"] == 4413054432
    assert packet["exact_identifier"] == 4413054432
    assert packet["symbol"] == "XAUUSDm"
    assert packet["magic"] == 240024
    assert packet["exact_ticket_open"] is False
    assert packet["h024_position_count"] == 0
    assert packet["h024_order_count"] == 0
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["dashboard_wording"] == EXPECTED_DASHBOARD_WORDING
    assert packet["readiness_wording"] == EXPECTED_DASHBOARD_WORDING
    assert packet["dashboard_state"] == EXPECTED_DASHBOARD_WORDING
    assert packet["readiness_state"] == EXPECTED_DASHBOARD_WORDING
    assert packet["violations"] == []


@pytest.mark.parametrize(
    ("override_key", "override_value", "expected_code"),
    [
        ("verdict", "FAIL_CLOSED", "stage5_verdict_not_pass"),
        ("post_close_verified", False, "post_close_not_verified"),
        ("open_canary_trade_exists", True, "open_canary_trade_exists_unexpected"),
        ("exact_ticket_open", True, "exact_ticket_still_open"),
        ("h024_position_count", 1, "h024_position_count_not_zero"),
        ("h024_order_count", 1, "h024_order_count_not_zero"),
    ],
)
def test_fails_closed_when_stage5_does_not_confirm_safe_post_close_state(
    tmp_path: Path,
    override_key: str,
    override_value: object,
    expected_code: str,
) -> None:
    stage5 = tmp_path / "stage5.jsonl"
    write_stage5(stage5, **{override_key: override_value})

    packet = build_packet(stage5)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["canary_absence_classification"] == "UNEXPECTED_MISSING_CANARY_OR_STAGE5_UNVERIFIED"
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == expected_code for v in packet["violations"])


def test_fails_closed_when_stage5_report_is_missing(tmp_path: Path) -> None:
    packet = build_packet(tmp_path / "missing.jsonl")

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["canary_absence_classification"] == "UNEXPECTED_MISSING_CANARY_OR_STAGE5_UNVERIFIED"
    assert packet["post_close_verified"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == "stage5_report_unreadable" for v in packet["violations"])


def test_fails_closed_when_stage5_report_is_malformed(tmp_path: Path) -> None:
    stage5 = tmp_path / "stage5.jsonl"
    stage5.write_text("{not json}\n", encoding="utf-8")

    packet = build_packet(stage5)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["canary_absence_classification"] == "UNEXPECTED_MISSING_CANARY_OR_STAGE5_UNVERIFIED"
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == "stage5_report_unreadable" for v in packet["violations"])


def test_cli_writes_jsonl_and_text_outputs(tmp_path: Path) -> None:
    stage5 = tmp_path / "stage5.jsonl"
    output_jsonl = tmp_path / "post_close.jsonl"
    output_text = tmp_path / "post_close.txt"
    write_stage5(stage5)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--stage5-report",
            str(stage5),
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
    assert EXPECTED_DASHBOARD_WORDING in text
    assert "Trading authorized: False" in text
    assert "Broker mutation authorized: False" in text


def test_cli_returns_nonzero_for_unverified_stage5(tmp_path: Path) -> None:
    stage5 = tmp_path / "stage5.jsonl"
    output_jsonl = tmp_path / "post_close.jsonl"
    output_text = tmp_path / "post_close.txt"
    write_stage5(stage5, verdict="FAIL_CLOSED")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--stage5-report",
            str(stage5),
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
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False


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
