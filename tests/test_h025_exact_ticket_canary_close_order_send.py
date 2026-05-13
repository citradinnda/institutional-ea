import json
import re
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "build_h025_exact_ticket_canary_close_order_send_jsonl.py"
REPORT = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_send.jsonl"


def load_module():
    spec = spec_from_file_location("h025_order_send", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_h025_order_send_script_is_exact_ticket_scoped() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"' in text
    assert 'EXPECTED_SYMBOL = "XAUUSDm"' in text
    assert 'EXPECTED_POSITION_SIDE = "sell"' in text
    assert 'EXPECTED_CLOSE_SIDE = "buy"' in text
    assert "EXPECTED_VOLUME = 0.01" in text
    assert "EXPECTED_TICKET = 4413054432" in text
    assert "EXPECTED_IDENTIFIER = 4413054432" in text
    assert "EXPECTED_MAGIC = 240024" in text
    assert 'EXPECTED_INTENT = "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_ONE_SHOT"' in text


def test_h025_order_send_contains_order_send_with_presend_order_check_but_no_symbol_select() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "mt5.order_check(request)" in text
    assert "mt5.order_send(request)" in text
    assert "mt5.symbol_select" not in text
    assert re.search(r"\bsymbol_select\s*\(", text) is None


def test_h025_order_send_has_no_unattended_loop_or_close_all_authorization() -> None:
    text = SCRIPT.read_text(encoding="utf-8").lower()

    forbidden = [
        "while true",
        "close_all_authorized\": true",
        '"entry_authorized": true',
        '"live_money_authorized": true',
        '"unattended_loop_authorized": true',
    ]

    for item in forbidden:
        assert item not in text


def test_approval_template_is_disabled_by_default() -> None:
    module = load_module()
    template = module.approval_template()

    assert template["schema"] == "h025_exact_ticket_canary_close_order_send_approval.v1"
    assert template["intent"] == "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_ONE_SHOT"
    assert template["operator_approved"] is False
    assert template["order_send_authorized"] is False
    assert template["order_check_authorized"] is True
    assert template["stage3_order_check_required"] is True
    assert template["pre_send_order_check_required"] is True
    assert template["exact_ticket"] == 4413054432
    assert template["exact_identifier"] == 4413054432
    assert template["account_server"] == "Exness-MT5Trial6"
    assert template["symbol"] == "XAUUSDm"
    assert template["side_to_close"] == "sell"
    assert template["close_side"] == "buy"
    assert template["close_all_authorized"] is False
    assert template["entry_authorized"] is False
    assert template["symbol_select_authorized"] is False
    assert template["live_money_authorized"] is False
    assert template["unattended_loop_authorized"] is False


def test_missing_stage3_report_fails_closed_before_order_send(tmp_path: Path) -> None:
    module = load_module()
    original_stage3 = module.STAGE3_REPORT_PATH
    module.STAGE3_REPORT_PATH = tmp_path / "missing_stage3.jsonl"

    try:
        result = module.run_order_send(tmp_path / "approval.json")
    finally:
        module.STAGE3_REPORT_PATH = original_stage3

    assert result == 1
    assert REPORT.exists()

    record = json.loads(REPORT.read_text(encoding="utf-8").splitlines()[0])
    assert record["verdict"] == "FAIL_CLOSED"
    assert record["stage"] == "H025_STAGE_4_STAGE3_PREFLIGHT_VALIDATION"
    assert record["order_check_executed"] is False
    assert record["order_send_authorized"] is False
    assert record["order_send_executed"] is False


def test_invalid_approval_rejected_without_order_send(tmp_path: Path) -> None:
    stage3 = tmp_path / "stage3.jsonl"
    stage3.write_text(json.dumps({
        "verdict": "PASS",
        "stage": "H025_STAGE_3_EXACT_TICKET_CLOSE_ORDER_CHECK",
        "exact_ticket": 4413054432,
        "exact_identifier": 4413054432,
        "symbol": "XAUUSDm",
        "side_to_close": "sell",
        "close_side_checked": "buy",
        "order_check_executed": True,
        "order_send_authorized": False,
        "order_send_executed": False,
        "broker_mutation_authorized": False,
        "order_check_result": {"retcode": 0},
    }) + "\n", encoding="utf-8")

    approval = tmp_path / "approval.json"
    approval.write_text(json.dumps({
        "schema": "h025_exact_ticket_canary_close_order_send_approval.v1",
        "intent": "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_ONE_SHOT",
        "operator_approved": False,
        "order_send_authorized": False,
        "account_server": "Exness-MT5Trial6",
        "symbol": "XAUUSDm",
        "exact_ticket": 4413054432,
        "exact_identifier": 4413054432,
        "magic": 240024,
        "volume": 0.01,
        "side_to_close": "sell",
        "close_side": "buy",
        "stage3_order_check_required": True,
        "pre_send_order_check_required": True,
        "order_check_authorized": True,
        "close_all_authorized": False,
        "entry_authorized": False,
        "symbol_select_authorized": False,
        "live_money_authorized": False,
        "unattended_loop_authorized": False,
        "operator_attestation": "I approve H025 one-shot demo order_send only to close exact ticket 4413054432. I do not approve new entries, close-all, symbol_select, loops, or live-money execution.",
        "expires_at_utc": "2999-01-01T00:00:00+00:00",
    }), encoding="utf-8")

    module = load_module()
    original_stage3 = module.STAGE3_REPORT_PATH
    module.STAGE3_REPORT_PATH = stage3

    try:
        result = module.run_order_send(approval)
    finally:
        module.STAGE3_REPORT_PATH = original_stage3

    assert result == 1

    record = json.loads(REPORT.read_text(encoding="utf-8").splitlines()[0])
    assert record["verdict"] == "FAIL_CLOSED"
    assert record["stage"] == "H025_STAGE_4_APPROVAL_VALIDATION"
    assert record["order_check_executed"] is False
    assert record["order_send_authorized"] is False
    assert record["order_send_executed"] is False
    assert any(v["code"] == "approval_operator_approved_unexpected" for v in record["violations"])
    assert any(v["code"] == "approval_order_send_authorized_unexpected" for v in record["violations"])
