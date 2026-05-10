from pathlib import Path
import re


EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


def _source() -> str:
    return EA_SOURCE.read_text(encoding="utf-8")


def test_mql_intended_action_builder_preserves_raw_lots_for_blocked_price_rows():
    source = _source()
    match = re.search(
        r"string\s+BuildH024IntendedActionLogRow\s*\([^)]*\)\s*\{.*?\n\}",
        source,
        flags=re.DOTALL,
    )
    assert match is not None
    body = match.group(0)

    assert 'if(entry_price > 0.0 && stop_price > 0.0)' in body
    assert 'stop_distance_price = MathAbs(entry_price - stop_price);' in body
    assert 'raw_lots = risk_usd / loss_usd_per_lot;' in body
    assert 'if(decision == "WOULD_OPEN")' in body
    assert 'lots = ComputeH024LotSize(' in body


def test_mql_blocked_sizing_diagnostic_patch_still_has_no_trade_api_surface():
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
