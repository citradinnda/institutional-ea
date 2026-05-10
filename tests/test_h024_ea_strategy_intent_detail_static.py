from pathlib import Path


EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


FORBIDDEN_EXECUTION_TOKENS = (
    "OrderSend",
    "OrderSendAsync",
    "OrderCheck",
    "CTrade",
    "#include <Trade",
    "PositionOpen",
    "PositionClose",
    "PositionModify",
    "MqlTradeRequest",
    "MqlTradeResult",
    "order ticket",
    "position ticket",
    "execution adapter",
    "order-send result",
)

FORBIDDEN_WOULD_OPEN_DETAIL_TOKENS = (
    "lots=",
    "volume=",
    "risk=",
    "entry=",
    "stop=",
    "take_profit=",
    "tp=",
    "sl=",
    "ticket=",
    "order=",
    "position=",
)


def _source() -> str:
    return EA_SOURCE.read_text(encoding="utf-8")


def _h024_strategy_intent_detail_body(source: str) -> str:
    start = source.index("string H024StrategyIntentDetail()")
    end = source.index("void WriteH024StrategyIntentRow()", start)
    return source[start:end]


def test_h024_strategy_intent_detail_has_no_execution_surface() -> None:
    body = _h024_strategy_intent_detail_body(_source())

    for token in FORBIDDEN_EXECUTION_TOKENS:
        assert token not in body


def test_h024_strategy_intent_detail_uses_closed_h4_log_only_inputs() -> None:
    body = _h024_strategy_intent_detail_body(_source())

    assert "CopyRates(_Symbol, PERIOD_H4, 0, 256, rates)" in body
    assert "ArraySetAsSeries(rates, true);" in body
    assert "const int closed_shift = 1;" in body
    assert 'return "NO_ACTION:strategy_unavailable_insufficient_h4_warmup";' in body
    assert "if(copied < 10)" in body


def test_h024_strategy_intent_signal_equations_are_frozen() -> None:
    body = _h024_strategy_intent_detail_body(_source())

    assert (
        "const bool long_signal_observed = trend_up && previous_bearish && "
        "long_pullback_ok && long_resumption;"
    ) in body
    assert (
        "const bool short_signal_observed = trend_down && previous_bullish && "
        "short_pullback_ok && short_resumption;"
    ) in body


def test_h024_strategy_intent_conflict_fails_closed_before_would_open() -> None:
    body = _h024_strategy_intent_detail_body(_source())

    conflict_pos = body.index("if(long_signal_observed && short_signal_observed)")
    blocked_pos = body.index('return "BLOCKED:strategy_conflict_log_only";')
    long_pos = body.index("if(long_signal_observed)", blocked_pos)
    short_pos = body.index("if(short_signal_observed)", long_pos)

    assert conflict_pos < blocked_pos < long_pos < short_pos


def test_h024_strategy_intent_would_open_details_are_constrained_log_only() -> None:
    body = _h024_strategy_intent_detail_body(_source())

    expected_long = (
        '"WOULD_OPEN:side=long;closed_h4_time=%s;'
        'source=H024_STATE_OBSERVATION;mode=log_only_no_execution"'
    )
    expected_short = (
        '"WOULD_OPEN:side=short;closed_h4_time=%s;'
        'source=H024_STATE_OBSERVATION;mode=log_only_no_execution"'
    )

    assert expected_long in body
    assert expected_short in body
    assert body.count("WOULD_OPEN:side=") == 2
    assert "TimeToString(rates[closed_shift].time, TIME_DATE | TIME_SECONDS)" in body

    for token in FORBIDDEN_WOULD_OPEN_DETAIL_TOKENS:
        assert token not in body


def test_h024_strategy_intent_no_signal_detail_is_log_only() -> None:
    body = _h024_strategy_intent_detail_body(_source())

    assert (
        '"NO_ACTION:strategy_no_signal;closed_h4_time=%s;'
        'mode=log_only_no_execution"'
    ) in body
