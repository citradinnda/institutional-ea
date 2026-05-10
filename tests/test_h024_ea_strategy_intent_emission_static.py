from pathlib import Path
import re


EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


def _function_body(source: str, name: str) -> str:
    match = re.search(rf"(?:void|int)\s+{name}\s*\([^)]*\)\s*\{{(?P<body>.*?)\n\}}", source, re.DOTALL)
    assert match is not None, f"missing {name}"
    return match.group("body")


def test_h024_strategy_intent_is_emitted_once_per_runtime_callback() -> None:
    source = EA_SOURCE.read_text(encoding="utf-8")

    for callback in ("OnInit", "OnTick", "OnTimer"):
        body = _function_body(source, callback)
        assert body.count("WriteH024StrategyIntentRow();") == 1, callback


def test_h024_strategy_intent_is_not_emitted_on_deinit() -> None:
    source = EA_SOURCE.read_text(encoding="utf-8")
    body = _function_body(source, "OnDeinit")

    assert "WriteH024StrategyIntentRow();" not in body