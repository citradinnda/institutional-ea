from pathlib import Path
import re


EA_PATH = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


def _ea_source_without_comments() -> str:
    source = EA_PATH.read_text(encoding="utf-8")
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    source = re.sub(r"//.*", "", source)
    return source


def test_h024_intended_action_helpers_are_wired_into_runtime_emission():
    source = _ea_source_without_comments()

    assert "BuildH024IntendedActionLogHeader(" in source
    assert "BuildH024IntendedActionLogRow(" in source

    header_refs = source.count("BuildH024IntendedActionLogHeader(")
    row_refs = source.count("BuildH024IntendedActionLogRow(")

    assert header_refs >= 2, (
        "BuildH024IntendedActionLogHeader exists, but does not appear to be "
        "called from runtime CSV/header emission yet."
    )
    assert row_refs >= 2, (
        "BuildH024IntendedActionLogRow exists, but does not appear to be "
        "called from runtime intended-action row emission yet."
    )


def test_h024_intended_action_runtime_wiring_remains_log_only():
    source = _ea_source_without_comments()

    forbidden_tokens = [
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
    ]

    violations = [token for token in forbidden_tokens if token in source]
    assert violations == []
