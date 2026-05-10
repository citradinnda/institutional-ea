from pathlib import Path
import re


EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


def _source() -> str:
    return EA_SOURCE.read_text(encoding="utf-8")


def test_closed_shift_replay_control_is_log_only_and_bounded() -> None:
    source = _source()

    assert 'input int    InpH024ClosedShift = 1;' in source
    assert 'input string InpRuntimeMode = "log_only_preflight";' in source
    assert "int H024EffectiveClosedShift()" in source

    assert "if(InpH024ClosedShift < 1)" in source
    assert "return 1;" in source
    assert "if(InpH024ClosedShift > 240)" in source
    assert "return 240;" in source
    assert "return InpH024ClosedShift;" in source

    assert "const int closed_shift = H024EffectiveClosedShift();" in source


def test_closed_shift_raw_input_is_not_used_outside_bounded_helper() -> None:
    source = _source()

    helper_match = re.search(
        r"int\s+H024EffectiveClosedShift\s*\(\s*\)\s*\{.*?\n\}",
        source,
        flags=re.DOTALL,
    )
    assert helper_match is not None

    source_without_input_declaration = source.replace(
        "input int    InpH024ClosedShift = 1;",
        "",
    )
    source_without_helper = source_without_input_declaration.replace(
        helper_match.group(0),
        "",
    )

    assert "InpH024ClosedShift" not in source_without_helper


def test_closed_shift_replay_ea_still_has_no_trade_api_surface() -> None:
    source = _source()

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

    for token in forbidden_tokens:
        assert token not in source
