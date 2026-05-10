from pathlib import Path
import re


EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


def _source() -> str:
    return EA_SOURCE.read_text(encoding="utf-8")


def _function_body(source: str, name: str) -> str:
    match = re.search(
        rf"\b(?:void|bool|string|double|int)\s+{name}\s*\([^)]*\)\s*\{{.*?\n\}}",
        source,
        flags=re.DOTALL,
    )
    assert match is not None
    return match.group(0)


def test_runtime_would_open_entry_stop_are_derived_from_closed_h4_bar_and_atr() -> None:
    source = _source()

    assert "bool H024RuntimeEntryStopPrices(" in source
    assert "const int closed_shift = H024EffectiveClosedShift();" in source
    assert "const int atr_window = 3;" in source
    assert "const double stop_atr_multiple = 2.0;" in source
    assert "CopyRates(_Symbol, PERIOD_H4, 0, required_bars, rates)" in source
    assert "const double atr = WilderAtrForClosedBar(rates, closed_shift, atr_window);" in source
    assert "entry_price = NormalizeDouble(rates[closed_shift].close, price_digits);" in source
    assert "stop_price = NormalizeDouble(entry_price - (atr * stop_atr_multiple), price_digits);" in source
    assert "stop_price = NormalizeDouble(entry_price + (atr * stop_atr_multiple), price_digits);" in source


def test_runtime_intended_action_row_no_longer_passes_zero_entry_stop_for_would_open() -> None:
    source = _source()
    body = _function_body(source, "WriteH024IntendedActionRuntimeRow")

    assert "double entry_price = 0.0;" in body
    assert "double stop_price = 0.0;" in body
    assert "string intended_decision = decision;" in body
    assert "string intended_reason = intent_detail;" in body
    assert "H024RuntimeEntryStopPrices(direction, entry_price, stop_price)" in body
    assert "BLOCKED:invalid_entry_stop_for_would_open;" in body
    assert "BLOCKED:volume_below_min_for_would_open;" in body

    assert "      intended_decision,\n      direction,\n      entry_price,\n      stop_price," in body
    assert "      decision,\n      direction,\n      0.0,\n      0.0," not in body
    assert "      volume_digits,\n      intended_reason" in body


def test_runtime_price_patch_still_has_no_trade_api_surface() -> None:
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
