from pathlib import Path

import pytest

from scripts.verify_h024_dry_run_actions import (
    format_verification_report,
    load_action_rows,
    verify_action_rows,
)


HEADER = (
    "action,model_symbol,broker_symbol,side,timestamp_utc,reason,raw_lots,"
    "normalized_lots,raw_entry_price,raw_stop_price,raw_stop_distance,"
    "notional_quote,notional_usd,per_trade_gross_leverage,"
    "kill_switch_enabled,mode\n"
)


def _would_open_row(**overrides):
    row = {
        "action": "WOULD_OPEN",
        "model_symbol": "USDJPY",
        "broker_symbol": "USDJPYm",
        "side": "buy",
        "timestamp_utc": "2026-05-09T00:00:00+00:00",
        "reason": "dry-run intent only; no order sent",
        "raw_lots": "0.20",
        "normalized_lots": "0.20",
        "raw_entry_price": "150.0",
        "raw_stop_price": "149.5",
        "raw_stop_distance": "0.5",
        "notional_quote": "3000000.0",
        "notional_usd": "20000.0",
        "per_trade_gross_leverage": "2.0",
        "kill_switch_enabled": "True",
        "mode": "dry_run",
    }
    row.update(overrides)
    return row


def test_verify_action_rows_passes_valid_rows():
    rows = (
        _would_open_row(),
        {
            **_would_open_row(),
            "action": "NO_ACTION",
            "side": "",
            "broker_symbol": "USDJPYm",
            "raw_lots": "0.0",
            "normalized_lots": "0.0",
            "notional_quote": "0.0",
            "notional_usd": "0.0",
            "per_trade_gross_leverage": "0.0",
        },
    )

    result = verify_action_rows(rows)

    assert result.passed
    assert result.would_open_count == 1
    assert result.no_action_count == 1
    assert result.violation_count == 0


def test_verify_action_rows_fails_missing_would_open_audit_fields():
    result = verify_action_rows(
        (
            _would_open_row(
                broker_symbol="",
                normalized_lots="0.0",
                kill_switch_enabled="False",
            ),
        )
    )

    assert not result.passed
    assert result.violation_count == 3
    assert any("missing broker_symbol" in violation for violation in result.violations)
    assert any("normalized_lots must be > 0" in violation for violation in result.violations)
    assert any("kill_switch_enabled must be true/1" in violation for violation in result.violations)


def test_verify_action_rows_fails_unsupported_action_and_mode():
    result = verify_action_rows(
        (
            _would_open_row(action="SENT", mode="demo_execution"),
        )
    )

    assert not result.passed
    assert any("unsupported action" in violation for violation in result.violations)


def test_load_action_rows_rejects_forbidden_execution_fields(tmp_path: Path):
    path = tmp_path / "bad.csv"
    path.write_text(
        HEADER.replace("\n", ",order_ticket\n")
        + "WOULD_OPEN,USDJPY,USDJPYm,buy,2026-05-09T00:00:00+00:00,reason,0.2,0.2,150,149.5,0.5,3000000,20000,2,True,dry_run,123\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="forbidden execution fields"):
        load_action_rows(path)


def test_load_action_rows_rejects_missing_required_fields(tmp_path: Path):
    path = tmp_path / "bad.csv"
    path.write_text("action,model_symbol\nWOULD_OPEN,USDJPY\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required fields"):
        load_action_rows(path)


def test_load_action_rows_accepts_valid_csv(tmp_path: Path):
    path = tmp_path / "actions.csv"
    path.write_text(
        HEADER
        + "WOULD_OPEN,USDJPY,USDJPYm,buy,2026-05-09T00:00:00+00:00,reason,0.2,0.2,150,149.5,0.5,3000000,20000,2,True,dry_run\n",
        encoding="utf-8",
    )

    rows = load_action_rows(path)

    assert len(rows) == 1
    assert rows[0]["action"] == "WOULD_OPEN"


def test_report_preserves_deployment_boundary():
    result = verify_action_rows((_would_open_row(),))

    report = format_verification_report(result)

    assert "H024 dry-run action log verification" in report
    assert "Research only. No demo/live/Phase 4 approval." in report
    assert "This verifier does not approve demo trading, live trading, or Phase 4." in report


def test_verifier_contains_no_mt5_runtime_dependency():
    source = Path("scripts/verify_h024_dry_run_actions.py").read_text(encoding="utf-8-sig")

    assert "import MetaTrader5" not in source
    assert "from MetaTrader5" not in source
    assert "mt5." not in source
    assert ".order_send(" not in source
    assert "OrderSend(" not in source
