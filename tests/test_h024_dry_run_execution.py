from pathlib import Path

import pytest

from quantcore.execution.h024_dry_run import (
    BrokerSymbolFacts,
    DryRunConfig,
    TradeCandidate,
    build_dry_run_action,
    normalize_lots_down,
)


def _candidate(**overrides):
    values = {
        "model_symbol": "USDJPY",
        "side": "buy",
        "timestamp_utc": "2026-05-09T00:00:00+00:00",
        "equity_usd": 10_000.0,
        "signed_risk_fraction": 0.01,
        "raw_entry_price": 150.0,
        "raw_stop_price": 149.5,
        "raw_lots": 0.20,
    }
    values.update(overrides)
    return TradeCandidate(**values)


def test_dry_run_defaults_to_kill_switch_blocked():
    action = build_dry_run_action(
        config=DryRunConfig(),
        candidate=_candidate(),
    )

    assert action.action == "BLOCKED"
    assert action.reason == "blocked by kill switch"
    assert action.kill_switch_enabled is False
    assert action.normalized_lots == 0.0


def test_dry_run_emits_would_open_without_order_ticket_or_send_result():
    action = build_dry_run_action(
        config=DryRunConfig(kill_switch_enabled=True),
        candidate=_candidate(),
    )

    assert action.action == "WOULD_OPEN"
    assert action.reason == "dry-run intent only; no order sent"
    assert action.broker_symbol == "USDJPYm"
    assert action.normalized_lots == 0.20
    assert action.notional_usd == pytest.approx(20_000.0)
    assert action.per_trade_gross_leverage == pytest.approx(2.0)
    assert not hasattr(action, "order_ticket")
    assert not hasattr(action, "position_ticket")
    assert not hasattr(action, "order_send_result")


def test_flat_signal_emits_no_action_even_when_kill_switch_disabled():
    action = build_dry_run_action(
        config=DryRunConfig(),
        candidate=_candidate(side=None, raw_lots=0.0),
    )

    assert action.action == "NO_ACTION"
    assert action.reason == "flat signal"
    assert action.normalized_lots == 0.0


def test_unknown_symbol_fails_closed():
    action = build_dry_run_action(
        config=DryRunConfig(kill_switch_enabled=True),
        candidate=_candidate(model_symbol="EURUSD"),
    )

    assert action.action == "BLOCKED"
    assert action.reason == "unsupported symbol"
    assert action.broker_symbol is None


def test_unexpected_broker_symbol_mapping_fails_closed():
    facts = {
        "USDJPY": BrokerSymbolFacts(
            model_symbol="USDJPY",
            broker_symbol="USDJPY",
            contract_size=100_000.0,
            quote_currency="JPY",
            volume_min=0.01,
            volume_max=300.0,
            volume_step=0.01,
            stops_level_points=0.0,
            freeze_level_points=0.0,
            point=0.001,
            digits=3,
        )
    }

    action = build_dry_run_action(
        config=DryRunConfig(kill_switch_enabled=True),
        candidate=_candidate(),
        broker_facts_by_symbol=facts,
    )

    assert action.action == "BLOCKED"
    assert action.reason == "unexpected broker symbol mapping"


def test_invalid_stop_geometry_fails_closed():
    action = build_dry_run_action(
        config=DryRunConfig(kill_switch_enabled=True),
        candidate=_candidate(raw_stop_price=150.0),
    )

    assert action.action == "BLOCKED"
    assert action.reason == "invalid long stop geometry"


def test_volume_normalization_rounds_down_and_blocks_invalid_sizes():
    assert normalize_lots_down(
        raw_lots=0.026,
        volume_min=0.01,
        volume_max=300.0,
        volume_step=0.01,
    ) == 0.02

    assert normalize_lots_down(
        raw_lots=0.009,
        volume_min=0.01,
        volume_max=300.0,
        volume_step=0.01,
    ) == 0.0

    assert normalize_lots_down(
        raw_lots=301.0,
        volume_min=0.01,
        volume_max=300.0,
        volume_step=0.01,
    ) == 0.0


def test_per_trade_leverage_violation_fails_closed_with_audit_fields():
    action = build_dry_run_action(
        config=DryRunConfig(kill_switch_enabled=True),
        candidate=_candidate(raw_lots=2.0),
    )

    assert action.action == "BLOCKED"
    assert action.reason == "blocked by per-trade leverage"
    assert action.normalized_lots == 2.0
    assert action.per_trade_gross_leverage == pytest.approx(20.0)


def test_only_dry_run_mode_is_implemented():
    with pytest.raises(ValueError, match="only dry_run mode is implemented"):
        build_dry_run_action(
            config=DryRunConfig(mode="demo_execution"),  # type: ignore[arg-type]
            candidate=_candidate(),
        )


def test_module_contains_no_mt5_order_send_dependency():
    source = Path("quantcore/execution/h024_dry_run.py").read_text(encoding="utf-8-sig")

    assert "MetaTrader5" not in source
    assert "mt5." not in source
    assert "order_send" not in source
    assert "OrderSend" not in source
