from pathlib import Path

EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")
TEXT = EA_SOURCE.read_text(encoding="utf-8")


def test_synthetic_balance_inputs_are_default_off():
    assert "input bool   InpH024SyntheticBalanceEnabled = false;" in TEXT
    assert "input double InpH024SyntheticBalance = 0.0;" in TEXT


def test_synthetic_balance_is_labeled_in_reason_not_schema():
    assert "balance_source=synthetic_research_only" in TEXT
    assert "synthetic_balance=%.2f" in TEXT
    assert "real_account_balance=%.2f" in TEXT
    assert "H024AppendSyntheticBalanceReason(reason)" in TEXT
    assert (
        "timestamp,schema_version,ea_version,symbol,normalized_symbol,timeframe,decision,"
        "direction,entry_price,stop_price,stop_distance_price,tick_size,"
        "tick_value_usd_per_lot,account_balance_usd,risk_fraction,risk_usd,"
        "raw_lots,lots,min_volume,max_volume,volume_step,volume_digits,reason"
    ) in TEXT


def test_synthetic_balance_only_changes_intended_action_sizing_balance():
    assert "double H024SizingAccountBalance()" in TEXT
    assert "const double sizing_account_balance = H024SizingAccountBalance();" in TEXT
    assert "preview_lots = ComputeH024LotSize(\n            sizing_account_balance," in TEXT
    assert "      sizing_account_balance,\n      InpRiskFraction," in TEXT


def test_synthetic_balance_does_not_add_execution_or_chart_automation():
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
