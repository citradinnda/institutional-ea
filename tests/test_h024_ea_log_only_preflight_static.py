from pathlib import Path


EA_PATH = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")


def test_h024_log_only_preflight_ea_exists() -> None:
    assert EA_PATH.exists()


def test_h024_log_only_preflight_has_runtime_hooks_and_logging() -> None:
    text = EA_PATH.read_text(encoding="ascii")

    required = [
        "InpKillSwitchBlocked = true",
        "InpTimerSeconds = 1",
        "int OnInit()",
        "void OnTick()",
        "void OnTimer()",
        "void OnDeinit(const int reason)",
        "EventSetTimer(InpTimerSeconds)",
        "EventKillTimer()",
        "FileOpen(",
        "FileWrite(",
        "FileFlush(",
        "AccountInfoString(ACCOUNT_COMPANY)",
        "AccountInfoInteger(ACCOUNT_LEVERAGE)",
        "TerminalInfoInteger(TERMINAL_CONNECTED)",
        "MQLInfoInteger(MQL_TRADE_ALLOWED)",
        "SymbolInfoTick(_Symbol, tick)",
        "SYMBOL_TRADE_STOPS_LEVEL",
        "SYMBOL_TRADE_FREEZE_LEVEL",
        "void WriteIntentRow()",
        '"INTENT"',
        '"NO_ACTION:kill_switch_blocked"',
    ]

    for token in required:
        assert token in text


def test_h024_log_only_preflight_has_no_execution_surface_tokens() -> None:
    text = EA_PATH.read_text(encoding="ascii").lower()

    forbidden = [
        "ordersend",
        "ordercheck",
        "ctrade",
        "#include <trade",
        "positionopen",
        "positionclose",
        "buy(",
        "sell(",
        "buylimit",
        "selllimit",
        "buystop",
        "sellstop",
        "trade.",
        "mqltraderequest",
        "mqltraderesult",
        "trade_action_deal",
        "trade_action_pending",
        "trade_action_sltp",
    ]

    for token in forbidden:
        assert token not in text
