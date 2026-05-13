import json
import re
from datetime import datetime, timezone
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


def test_stage4_runtime_report_is_optional_context_not_hard_gate() -> None:
    module = load_module()

    assert module.summarize_stage4_runtime_report(None)["present"] is False
    assert module.summarize_stage4_runtime_report(None)["usable_pass_evidence"] is False

    failed_stage4 = {
        "verdict": "FAIL_CLOSED",
        "stage": "H025_STAGE_4_APPROVAL_VALIDATION",
        "exact_ticket": 4413054432,
        "exact_identifier": 4413054432,
        "order_send_executed": False,
    }
    summary = module.summarize_stage4_runtime_report(failed_stage4)

    assert summary["present"] is True
    assert summary["usable_pass_evidence"] is False
    assert summary["verdict"] == "FAIL_CLOSED"
    assert "volatile runtime context" in summary["note"]


def test_build_record_passes_on_zero_current_open_exposure_even_if_stage4_context_bad() -> None:
    module = load_module()

    record = module.build_record(
        account={"server": "Exness-MT5Trial6"},
        exact_positions=[],
        h024_positions=[],
        h024_orders=[],
        history_deal_matches=[],
        stage4_summary={"present": True, "usable_pass_evidence": False},
        history_start=datetime(2026, 5, 13, tzinfo=timezone.utc),
        history_end=datetime(2026, 5, 13, tzinfo=timezone.utc),
    )

    assert record["verdict"] == "PASS"
    assert record["post_close_verified"] is True
    assert record["open_canary_trade_exists"] is False
    assert record["exact_ticket_open"] is False
    assert record["h024_position_count"] == 0
    assert record["h024_order_count"] == 0
    assert record["order_check_executed"] is False
    assert record["order_send_executed"] is False
    assert record["broker_mutation_authorized"] is False


def test_build_record_fails_if_exact_ticket_or_h024_exposure_remains() -> None:
    module = load_module()

    record = module.build_record(
        account={"server": "Exness-MT5Trial6"},
        exact_positions=[{"ticket": 4413054432}],
        h024_positions=[{"ticket": 4413054432, "magic": 240024}],
        h024_orders=[{"ticket": 123, "magic": 240024}],
        history_deal_matches=[],
        stage4_summary={"present": False, "usable_pass_evidence": False},
        history_start=datetime(2026, 5, 13, tzinfo=timezone.utc),
        history_end=datetime(2026, 5, 13, tzinfo=timezone.utc),
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert record["post_close_verified"] is False
    assert record["exact_ticket_open"] is True
    assert record["open_canary_trade_exists"] is True
    codes = {violation["code"] for violation in record["violations"]}
    assert "exact_ticket_still_open" in codes
    assert "h024_positions_remain" in codes
    assert "h024_orders_remain" in codes
