import json
import re
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "build_h025_exact_ticket_canary_close_order_check_jsonl.py"
REPORT = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_check.jsonl"


def load_module():
    spec = spec_from_file_location("h025_order_check", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_h025_order_check_script_is_exact_ticket_scoped() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"' in text
    assert 'EXPECTED_SYMBOL = "XAUUSDm"' in text
    assert 'EXPECTED_POSITION_SIDE = "sell"' in text
    assert 'EXPECTED_CLOSE_SIDE = "buy"' in text
    assert "EXPECTED_VOLUME = 0.01" in text
    assert "EXPECTED_TICKET = 4413054432" in text
    assert "EXPECTED_IDENTIFIER = 4413054432" in text
    assert "EXPECTED_MAGIC = 240024" in text
    assert 'EXPECTED_INTENT = "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_ONLY"' in text


def test_h025_order_check_contains_order_check_but_no_order_send_or_symbol_select() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "mt5.order_check(request)" in text

    forbidden = [
        r"\border_send\s*\(",
        r"\.order_send\s*\(",
        r"\bsymbol_select\s*\(",
        r"\.symbol_select\s*\(",
    ]

    for pattern in forbidden:
        assert re.search(pattern, text) is None, f"forbidden execution pattern found: {pattern}"


def test_approval_template_is_disabled_by_default() -> None:
    module = load_module()
    template = module.approval_template()

    assert template["schema"] == "h025_exact_ticket_canary_close_order_check_approval.v1"
    assert template["intent"] == "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_ONLY"
    assert template["operator_approved"] is False
    assert template["order_check_authorized"] is False
    assert template["order_send_authorized"] is False
    assert template["exact_ticket"] == 4413054432
    assert template["exact_identifier"] == 4413054432
    assert template["account_server"] == "Exness-MT5Trial6"
    assert template["symbol"] == "XAUUSDm"
    assert template["side_to_close"] == "sell"
    assert template["close_side"] == "buy"


def test_missing_approval_fails_closed_before_order_check(tmp_path: Path) -> None:
    missing = tmp_path / "missing_approval.json"

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--approval-json", str(missing)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert REPORT.exists()

    record = json.loads(REPORT.read_text(encoding="utf-8").splitlines()[0])
    assert record["verdict"] == "FAIL_CLOSED"
    assert record["stage"] == "H025_STAGE_3_APPROVAL_VALIDATION"
    assert record["order_check_executed"] is False
    assert record["order_send_authorized"] is False
    assert record["order_send_executed"] is False
    assert record["broker_mutation_authorized"] is False
    assert record["exact_ticket"] == 4413054432
    assert record["exact_identifier"] == 4413054432


def test_invalid_approval_rejected_without_order_check(tmp_path: Path) -> None:
    approval = tmp_path / "approval.json"
    approval.write_text(
        json.dumps({
            "schema": "h025_exact_ticket_canary_close_order_check_approval.v1",
            "intent": "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_ONLY",
            "operator_approved": False,
            "order_check_authorized": False,
            "account_server": "Exness-MT5Trial6",
            "symbol": "XAUUSDm",
            "exact_ticket": 4413054432,
            "exact_identifier": 4413054432,
            "magic": 240024,
            "volume": 0.01,
            "side_to_close": "sell",
            "close_side": "buy",
            "order_send_authorized": False,
            "close_all_authorized": False,
            "entry_authorized": False,
            "live_money_authorized": False,
            "operator_attestation": "I approve H025 order_check only. I do not approve order_send.",
            "expires_at_utc": "2999-01-01T00:00:00+00:00",
        }),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--approval-json", str(approval)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1

    record = json.loads(REPORT.read_text(encoding="utf-8").splitlines()[0])
    assert record["verdict"] == "FAIL_CLOSED"
    assert record["order_check_executed"] is False
    assert record["order_send_executed"] is False
    assert any(v["code"] == "approval_operator_approved_unexpected" for v in record["violations"])
    assert any(v["code"] == "approval_order_check_authorized_unexpected" for v in record["violations"])
