import json
import re
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "build_h025_exact_ticket_canary_post_close_verification_jsonl.py"


def load_module():
    spec = spec_from_file_location("h025_post_close", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_post_close_verification_script_is_exact_ticket_scoped() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"' in text
    assert 'EXPECTED_SYMBOL = "XAUUSDm"' in text
    assert "EXPECTED_VOLUME = 0.01" in text
    assert "EXPECTED_TICKET = 4413054432" in text
    assert "EXPECTED_IDENTIFIER = 4413054432" in text
    assert "EXPECTED_MAGIC = 240024" in text


def test_post_close_verification_is_read_only_no_order_capable_calls() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    forbidden = [
        r"\border_send\s*\(",
        r"\.order_send\s*\(",
        r"\border_check\s*\(",
        r"\.order_check\s*\(",
        r"\bsymbol_select\s*\(",
        r"\.symbol_select\s*\(",
        r"\bTRADE_ACTION\b",
        r"\bORDER_TYPE_BUY\b",
        r"\bORDER_TYPE_SELL\b",
    ]

    for pattern in forbidden:
        assert re.search(pattern, text) is None, f"forbidden post-close verification pattern found: {pattern}"


def test_missing_stage4_report_fails_closed_before_mt5(tmp_path: Path) -> None:
    module = load_module()

    original_stage4 = module.STAGE4_REPORT_PATH
    original_jsonl = module.OUTPUT_JSONL_PATH
    original_text = module.OUTPUT_TEXT_PATH

    module.STAGE4_REPORT_PATH = tmp_path / "missing_stage4.jsonl"
    module.OUTPUT_JSONL_PATH = tmp_path / "post_close.jsonl"
    module.OUTPUT_TEXT_PATH = tmp_path / "post_close.txt"

    try:
        result = module.run_post_close_verification()
    finally:
        module.STAGE4_REPORT_PATH = original_stage4
        module.OUTPUT_JSONL_PATH = original_jsonl
        module.OUTPUT_TEXT_PATH = original_text

    assert result == 1

    record = json.loads((tmp_path / "post_close.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert record["verdict"] == "FAIL_CLOSED"
    assert record["stage"] == "H025_STAGE_5_STAGE4_REPORT_VALIDATION"
    assert record["order_check_executed"] is False
    assert record["order_send_executed"] is False
    assert record["broker_mutation_authorized"] is False
    assert record["post_close_verified"] is False


def test_invalid_stage4_report_rejected_before_mt5(tmp_path: Path) -> None:
    module = load_module()

    stage4 = tmp_path / "stage4.jsonl"
    stage4.write_text(
        json.dumps(
            {
                "verdict": "FAIL_CLOSED",
                "stage": "H025_STAGE_4_EXACT_TICKET_CLOSE_ORDER_SEND",
                "exact_ticket": 4413054432,
                "exact_identifier": 4413054432,
                "symbol": "XAUUSDm",
                "volume": 0.01,
                "order_check_executed": True,
                "order_send_executed": False,
                "post_send_exact_ticket_open": True,
                "post_send_h024_position_count": 1,
                "post_send_h024_order_count": 0,
                "order_send_result": {"retcode": 0},
            }
        )
        + "\n",
        encoding="utf-8",
    )

    original_stage4 = module.STAGE4_REPORT_PATH
    original_jsonl = module.OUTPUT_JSONL_PATH
    original_text = module.OUTPUT_TEXT_PATH

    module.STAGE4_REPORT_PATH = stage4
    module.OUTPUT_JSONL_PATH = tmp_path / "post_close.jsonl"
    module.OUTPUT_TEXT_PATH = tmp_path / "post_close.txt"

    try:
        result = module.run_post_close_verification()
    finally:
        module.STAGE4_REPORT_PATH = original_stage4
        module.OUTPUT_JSONL_PATH = original_jsonl
        module.OUTPUT_TEXT_PATH = original_text

    assert result == 1

    record = json.loads((tmp_path / "post_close.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert record["verdict"] == "FAIL_CLOSED"
    assert record["stage"] == "H025_STAGE_5_STAGE4_REPORT_VALIDATION"
    assert any(v["code"] == "stage4_verdict_unexpected" for v in record["violations"])
    assert any(v["code"] == "stage4_order_send_executed_unexpected" for v in record["violations"])
    assert any(v["code"] == "stage4_post_send_exact_ticket_open_unexpected" for v in record["violations"])
    assert record["order_check_executed"] is False
    assert record["order_send_executed"] is False
