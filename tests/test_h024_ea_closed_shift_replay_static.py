from pathlib import Path


EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


def read_source() -> str:
    return EA_SOURCE.read_text(encoding="utf-8")


def test_h024_log_only_ea_has_closed_shift_replay_input_defaulting_to_current_closed_bar():
    source = read_source()

    assert "input int    InpH024ClosedShift = 1;" in source
    assert "int H024EffectiveClosedShift()" in source
    assert "return 1;" in source
    assert "return 240;" in source


def test_h024_log_only_ea_uses_effective_closed_shift_instead_of_hard_coded_shift():
    source = read_source()

    assert "const int closed_shift = 1;" not in source
    assert source.count("const int closed_shift = H024EffectiveClosedShift();") == 2


def test_h024_closed_shift_replay_does_not_add_trade_api_surface():
    source = read_source()

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
