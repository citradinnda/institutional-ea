import json
from pathlib import Path

import pytest

from scripts.verify_h024_mt5_terminal_preflight import (
    format_preflight_verification,
    load_preflight_report,
    verify_preflight_report,
)


def _valid_payload():
    return {
        "account": {
            "currency": "USD",
            "trade_allowed": True,
            "trade_expert": True,
        },
        "approval_boundary": "No demo/live/Phase 4 approval.",
        "forbidden_call_attempts": [],
        "forbidden_calls_checked": [
            "order_send",
            "order_check",
            "order_calc_margin",
            "order_calc_profit",
            "positions_get",
            "orders_get",
            "history_orders_get",
            "history_deals_get",
        ],
        "mt5_initialized": True,
        "passed": True,
        "research_only": True,
        "symbols": [
            {
                "ask": 156.694,
                "bid": 156.676,
                "broker_symbol": "USDJPYm",
                "digits": 3,
                "execution_mode": 2,
                "freeze_level_points": 0,
                "model_symbol": "USDJPY",
                "order_filling_modes": 3,
                "order_modes": 127,
                "point": 0.001,
                "selected": True,
                "spread": 18,
                "status": "ok",
                "stops_level_points": 0,
                "trade_mode": 4,
                "visible_after_select": True,
                "volume_max": 300.0,
                "volume_min": 0.01,
                "volume_step": 0.01,
            },
            {
                "ask": 4715.669,
                "bid": 4715.309,
                "broker_symbol": "XAUUSDm",
                "digits": 3,
                "execution_mode": 2,
                "freeze_level_points": 0,
                "model_symbol": "XAUUSD",
                "order_filling_modes": 3,
                "order_modes": 127,
                "point": 0.001,
                "selected": True,
                "spread": 360,
                "status": "ok",
                "stops_level_points": 0,
                "trade_mode": 4,
                "visible_after_select": True,
                "volume_max": 200.0,
                "volume_min": 0.01,
                "volume_step": 0.01,
            },
        ],
        "terminal": {
            "connected": True,
            "tradeapi_disabled": False,
        },
    }


def test_verify_preflight_report_passes_valid_payload():
    verification = verify_preflight_report(_valid_payload())

    assert verification.passed
    assert verification.violation_count == 0


def test_verify_preflight_report_fails_forbidden_call_attempt():
    payload = _valid_payload()
    payload["forbidden_call_attempts"] = ["order_send"]

    verification = verify_preflight_report(payload)

    assert not verification.passed
    assert any(
        check.section == "root"
        and check.field == "forbidden_call_attempts"
        and check.status == "violation"
        for check in verification.checks
    )


def test_verify_preflight_report_fails_missing_required_symbol():
    payload = _valid_payload()
    payload["symbols"] = payload["symbols"][:1]

    verification = verify_preflight_report(payload)

    assert not verification.passed
    assert any(
        check.section == "XAUUSD"
        and check.field == "model_symbol"
        and check.status == "violation"
        for check in verification.checks
    )


def test_verify_preflight_report_fails_bad_symbol_facts():
    payload = _valid_payload()
    payload["symbols"][0] = dict(
        payload["symbols"][0],
        broker_symbol="USDJPY",
        bid=0,
        volume_step=0.1,
    )

    verification = verify_preflight_report(payload)

    assert not verification.passed
    assert any(
        check.section == "USDJPY"
        and check.field == "broker_symbol"
        and check.status == "violation"
        for check in verification.checks
    )
    assert any(
        check.section == "USDJPY"
        and check.field == "bid"
        and check.status == "violation"
        for check in verification.checks
    )
    assert any(
        check.section == "USDJPY"
        and check.field == "volume_step"
        and check.status == "violation"
        for check in verification.checks
    )


def test_format_preflight_verification_preserves_boundary():
    verification = verify_preflight_report(_valid_payload())

    text = format_preflight_verification(verification)

    assert "H024 MT5 terminal/account preflight verification" in text
    assert "Research only. No demo/live/Phase 4 approval." in text
    assert "This verifier does not approve demo trading, live trading, or Phase 4." in text


def test_load_preflight_report_reads_json(tmp_path: Path):
    path = tmp_path / "preflight.json"
    path.write_text(json.dumps(_valid_payload()), encoding="utf-8")

    payload = load_preflight_report(path)

    assert payload["passed"] is True
    assert payload["symbols"][0]["broker_symbol"] == "USDJPYm"


def test_load_preflight_report_rejects_non_object_json(tmp_path: Path):
    path = tmp_path / "preflight.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="root must be an object"):
        load_preflight_report(path)
