from pathlib import Path

import pytest

from scripts.audit_h024_mt5_order_behavior import (
    audit_order_behavior_rows,
    format_order_behavior_audit,
    load_order_behavior_rows,
    normalize_symbol,
)


HEADER = (
    "symbol,trade_mode,execution_mode,order_filling_modes,order_modes,"
    "volume_min,volume_max,volume_step,stops_level_points,freeze_level_points,"
    "point,digits,spread_float\n"
)


def _valid_rows():
    return (
        {
            "symbol": "USDJPYm",
            "trade_mode": "FULL",
            "execution_mode": "MARKET",
            "order_filling_modes": "FOK,IOC",
            "order_modes": "MARKET,SL,TP",
            "volume_min": "0.01",
            "volume_max": "300",
            "volume_step": "0.01",
            "stops_level_points": "0",
            "freeze_level_points": "0",
            "point": "0.001",
            "digits": "3",
            "spread_float": "true",
        },
        {
            "symbol": "XAUUSDm",
            "trade_mode": "4",
            "execution_mode": "MARKET",
            "order_filling_modes": "FOK,IOC",
            "order_modes": "MARKET,SL,TP",
            "volume_min": "0.01",
            "volume_max": "200",
            "volume_step": "0.01",
            "stops_level_points": "0",
            "freeze_level_points": "0",
            "point": "0.001",
            "digits": "3",
            "spread_float": "1",
        },
    )


def test_normalize_symbol_removes_exness_m_suffix():
    assert normalize_symbol("USDJPYm") == "USDJPY"
    assert normalize_symbol("XAUUSDm") == "XAUUSD"
    assert normalize_symbol("USDJPY") == "USDJPY"


def test_order_behavior_audit_passes_valid_synthetic_rows():
    audit = audit_order_behavior_rows(_valid_rows())

    assert audit.passed
    assert audit.mismatch_count == 0
    assert len(audit.checks) > 0


def test_order_behavior_audit_fails_missing_symbol():
    rows = (_valid_rows()[0],)

    audit = audit_order_behavior_rows(rows)

    assert not audit.passed
    assert any(
        check.symbol == "XAUUSD"
        and check.field == "symbol"
        and check.status == "mismatch"
        for check in audit.checks
    )


def test_order_behavior_audit_fails_execution_constraint_mismatch():
    rows = list(_valid_rows())
    rows[0] = dict(rows[0], volume_step="0.1", trade_mode="DISABLED")

    audit = audit_order_behavior_rows(rows)

    assert not audit.passed
    assert any(
        check.symbol == "USDJPY"
        and check.field == "volume_step"
        and check.status == "mismatch"
        for check in audit.checks
    )
    assert any(
        check.symbol == "USDJPY"
        and check.field == "trade_mode"
        and check.status == "mismatch"
        for check in audit.checks
    )


def test_order_behavior_report_preserves_deployment_boundary():
    audit = audit_order_behavior_rows(_valid_rows())

    report = format_order_behavior_audit(audit)

    assert "H024 MT5 order behavior audit" in report
    assert "Research only. No demo/live/Phase 4 approval." in report
    assert "PASS does not approve demo trading, live trading, Phase 4, or EA execution." in report


def test_load_order_behavior_rows_rejects_missing_columns(tmp_path: Path):
    path = tmp_path / "bad.csv"
    path.write_text("symbol,trade_mode\nUSDJPYm,FULL\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_order_behavior_rows(path)


def test_load_order_behavior_rows_reads_valid_csv(tmp_path: Path):
    path = tmp_path / "order_behavior.csv"
    path.write_text(
        HEADER
        + "USDJPYm,FULL,MARKET,\"FOK,IOC\",\"MARKET,SL,TP\",0.01,300,0.01,0,0,0.001,3,true\n"
        + "XAUUSDm,4,MARKET,\"FOK,IOC\",\"MARKET,SL,TP\",0.01,200,0.01,0,0,0.001,3,1\n",
        encoding="utf-8",
    )

    rows = load_order_behavior_rows(path)

    assert len(rows) == 2
    assert rows[0]["symbol"] == "USDJPYm"
