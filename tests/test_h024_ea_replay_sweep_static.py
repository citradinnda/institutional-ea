from pathlib import Path

EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")
TEXT = EA_SOURCE.read_text(encoding="utf-8")


def test_replay_sweep_inputs_are_research_only_and_bounded():
    assert "input bool   InpH024ReplaySweepEnabled = false;" in TEXT
    assert "input int    InpH024ReplaySweepStartShift = 1;" in TEXT
    assert "input int    InpH024ReplaySweepEndShift = 1;" in TEXT
    assert "input int    InpH024ReplaySweepMaxRows = 20;" in TEXT
    assert "if(InpH024ReplaySweepStartShift > 240)" in TEXT
    assert "if(end_shift > 240)" in TEXT
    assert "if(InpH024ReplaySweepMaxRows > 240)" in TEXT


def test_replay_sweep_uses_effective_shift_override():
    assert "int g_h024_replay_sweep_override_shift = 0;" in TEXT
    assert "bool g_h024_replay_sweep_written = false;" in TEXT
    assert "if(g_h024_replay_sweep_override_shift > 0)" in TEXT
    assert "requested_shift = g_h024_replay_sweep_override_shift;" in TEXT
    assert "g_h024_replay_sweep_override_shift = shift;" in TEXT
    assert "g_h024_replay_sweep_override_shift = 0;" in TEXT


def test_replay_sweep_emits_state_and_intended_rows_once_per_attach():
    assert '"H024_REPLAY_SWEEP"' in TEXT
    assert '"H024_REPLAY_SWEEP_SHIFT"' in TEXT
    assert '"H024_REPLAY_SWEEP_DONE"' in TEXT
    assert "WriteH024StateObservationRow();" in TEXT
    assert "WriteH024IntendedActionRuntimeRow();" in TEXT
    assert "if(g_h024_replay_sweep_written)" in TEXT
    assert "g_h024_replay_sweep_written = true;" in TEXT


def test_on_tick_and_timer_do_not_repeat_sweep_rows():
    assert TEXT.count("if(!InpH024ReplaySweepEnabled)") >= 2
    assert "WriteH024ReplaySweepRows();" in TEXT


def test_replay_sweep_does_not_add_execution_or_chart_automation():
    forbidden = [
        "OrderSend",
        "OrderSendAsync",
        "OrderCheck",
        "CTrade",
        "MqlTradeRequest",
        "MqlTradeResult",
        "PositionOpen",
        "PositionClose",
        "PositionModify",
        "ChartApplyTemplate",
        "ChartOpen",
        "ExpertRemove",
    ]
    for token in forbidden:
        assert token not in TEXT
