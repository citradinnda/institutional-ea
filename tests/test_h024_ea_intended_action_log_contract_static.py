from pathlib import Path

from quantcore.execution.h024_intended_action_log import (
    REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS,
)


EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")

FORBIDDEN_EXECUTION_SURFACE = (
    "OrderSend",
    "OrderSendAsync",
    "OrderCheck",
    "CTrade",
    "#include <Trade",
    "MqlTradeRequest",
    "MqlTradeResult",
    "PositionOpen",
    "PositionClose",
    "PositionModify",
)


def _source_text() -> str:
    assert EA_SOURCE.exists(), f"EA source missing: {EA_SOURCE}"
    return EA_SOURCE.read_text(encoding="utf-8")


def test_h024_ea_intended_action_log_declares_schema_and_builders():
    source = _source_text()

    assert 'H024_INTENDED_ACTION_LOG_SCHEMA_VERSION = "h024_intended_action_log_v1"' in source
    assert "BuildH024IntendedActionLogHeader" in source
    assert "BuildH024IntendedActionLogRow" in source


def test_h024_ea_intended_action_log_header_matches_python_contract():
    source = _source_text()
    expected_header = ",".join(REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS)

    assert expected_header in source

    for field in REQUIRED_H024_INTENDED_ACTION_LOG_FIELDS:
        assert field in source


def test_h024_ea_intended_action_log_remains_execution_api_free():
    source = _source_text()

    for forbidden in FORBIDDEN_EXECUTION_SURFACE:
        assert forbidden not in source