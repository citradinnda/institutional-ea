import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "build_h025_exact_ticket_canary_close_request_preview_jsonl.py"
REPORT = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_request_preview.jsonl"


def test_h025_preview_script_exists_and_is_exact_ticket_scoped() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "EXPECTED_ACCOUNT_SERVER = \"Exness-MT5Trial6\"" in text
    assert "EXPECTED_SYMBOL = \"XAUUSDm\"" in text
    assert "EXPECTED_POSITION_SIDE = \"sell\"" in text
    assert "EXPECTED_CLOSE_SIDE = \"buy\"" in text
    assert "EXPECTED_VOLUME = 0.01" in text
    assert "EXPECTED_TICKET = 4413054432" in text
    assert "EXPECTED_IDENTIFIER = 4413054432" in text
    assert "EXPECTED_MAGIC = 240024" in text


def test_h025_preview_has_no_broker_mutation_calls() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    forbidden_patterns = [
        r"\bimport\s+MetaTrader5\b",
        r"\bfrom\s+MetaTrader5\s+import\b",
        r"\bmt5\.",
        r"\border_send\s*\(",
        r"\.order_send\s*\(",
        r"\border_check\s*\(",
        r"\.order_check\s*\(",
        r"\bsymbol_select\s*\(",
        r"\.symbol_select\s*\(",
    ]

    for pattern in forbidden_patterns:
        assert re.search(pattern, text) is None, f"forbidden broker-mutation pattern found: {pattern}"


def test_h025_preview_builder_outputs_inert_exact_ticket_record() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert REPORT.exists(), f"missing report: {REPORT}"

    records = [
        json.loads(line)
        for line in REPORT.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert len(records) == 1
    record = records[0]

    assert record["schema"] == "h025_exact_ticket_canary_close_request_preview.v1"
    assert record["stage"] == "H025_STAGE_2_EXACT_TICKET_CLOSE_REQUEST_PREVIEW"
    assert record["verdict"] == "PASS"
    assert record["exact_ticket"] == 4413054432
    assert record["exact_identifier"] == 4413054432
    assert record["account_server"] == "Exness-MT5Trial6"
    assert record["symbol"] == "XAUUSDm"
    assert record["side_to_close"] == "sell"
    assert record["close_side_preview"] == "buy"
    assert record["volume"] == 0.01
    assert record["magic"] == 240024

    assert record["preview_only"] is True
    assert record["inert_close_request_shape_constructed"] is True
    assert record["live_mt5_request_constructed"] is False
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["entry_authorized"] is False
    assert record["close_modify_authorized"] is False
    assert record["unattended_loop_authorized"] is False
    assert record["close_all_authorized"] is False
    assert record["live_money_authorized"] is False

    preview = record["close_request_preview"]
    assert preview["shape_kind"] == "INERT_EXACT_TICKET_CLOSE_REQUEST_PREVIEW_ONLY"
    assert preview["not_submitable_to_mt5"] is True
    assert preview["account_server_required"] == "Exness-MT5Trial6"
    assert preview["symbol_required"] == "XAUUSDm"
    assert preview["position_ticket_required"] == 4413054432
    assert preview["position_identifier_required"] == 4413054432
    assert preview["magic_required"] == 240024
    assert preview["position_side_to_close"] == "sell"
    assert preview["close_side_preview"] == "buy"
    assert preview["volume_required"] == 0.01
    assert preview["manual_operator_approval_required_before_order_check"] is True
    assert preview["manual_operator_confirmation_required_before_order_send"] is True
