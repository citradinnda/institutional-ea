from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from quantcore.backtest.cost_model import (
    DEFAULT_COST_SPECS,
    ExecutionCost,
    SymbolCostSpec,
    get_default_cost_spec,
    price_with_execution_costs,
)


def test_default_usdjpy_cost_spec_matches_phase_3_assumption() -> None:
    spec = get_default_cost_spec("USDJPY")

    assert spec.symbol == "USDJPY"
    assert spec.spread_price == pytest.approx(0.01)
    assert spec.commission_usd_per_lot_per_fill == pytest.approx(7.0)
    assert spec.stop_slippage_atr_fraction == pytest.approx(0.05)


def test_default_xauusd_cost_spec_matches_phase_3_assumption() -> None:
    spec = get_default_cost_spec("xauusd")

    assert spec.symbol == "XAUUSD"
    assert spec.spread_price == pytest.approx(0.30)
    assert spec.commission_usd_per_lot_per_fill == pytest.approx(10.0)
    assert spec.stop_slippage_atr_fraction == pytest.approx(0.05)


def test_default_cost_specs_are_immutable_mapping() -> None:
    with pytest.raises(TypeError):
        DEFAULT_COST_SPECS["EURUSD"] = SymbolCostSpec(  # type: ignore[index]
            symbol="EURUSD",
            spread_price=0.0001,
            commission_usd_per_lot_per_fill=7.0,
        )


def test_execution_cost_is_frozen() -> None:
    cost = ExecutionCost(
        symbol="XAUUSD",
        side="buy",
        action="entry",
        raw_price=2000.0,
        fill_price=2000.15,
        lots=1.0,
        spread_paid_price=0.15,
        slippage_price=0.0,
        commission_usd=10.0,
    )

    with pytest.raises(FrozenInstanceError):
        cost.fill_price = 1999.0  # type: ignore[misc]


def test_buy_entry_pays_ask_half_spread_plus_commission() -> None:
    cost = price_with_execution_costs(
        symbol="XAUUSD",
        side="buy",
        action="entry",
        raw_price=2000.0,
        lots=2.0,
    )

    assert cost.fill_price == pytest.approx(2000.15)
    assert cost.spread_paid_price == pytest.approx(0.15)
    assert cost.slippage_price == pytest.approx(0.0)
    assert cost.commission_usd == pytest.approx(20.0)


def test_sell_entry_hits_bid_half_spread_plus_commission() -> None:
    cost = price_with_execution_costs(
        symbol="USDJPY",
        side="sell",
        action="entry",
        raw_price=150.00,
        lots=1.5,
    )

    assert cost.fill_price == pytest.approx(149.995)
    assert cost.spread_paid_price == pytest.approx(0.005)
    assert cost.slippage_price == pytest.approx(0.0)
    assert cost.commission_usd == pytest.approx(10.5)


def test_long_stop_exit_pays_bid_and_atr_slippage() -> None:
    cost = price_with_execution_costs(
        symbol="XAUUSD",
        side="buy",
        action="exit",
        raw_price=2000.0,
        lots=1.0,
        exit_reason="stop",
        atr=4.0,
    )

    assert cost.fill_price == pytest.approx(1999.65)
    assert cost.spread_paid_price == pytest.approx(0.15)
    assert cost.slippage_price == pytest.approx(0.20)
    assert cost.commission_usd == pytest.approx(10.0)


def test_short_stop_exit_pays_ask_and_atr_slippage() -> None:
    cost = price_with_execution_costs(
        symbol="USDJPY",
        side="sell",
        action="exit",
        raw_price=150.00,
        lots=1.0,
        exit_reason="stop",
        atr=0.20,
    )

    assert cost.fill_price == pytest.approx(150.015)
    assert cost.spread_paid_price == pytest.approx(0.005)
    assert cost.slippage_price == pytest.approx(0.01)
    assert cost.commission_usd == pytest.approx(7.0)


def test_take_profit_exit_pays_spread_but_no_slippage() -> None:
    cost = price_with_execution_costs(
        symbol="XAUUSD",
        side="buy",
        action="exit",
        raw_price=2010.0,
        lots=1.0,
        exit_reason="tp",
        atr=4.0,
    )

    assert cost.fill_price == pytest.approx(2009.85)
    assert cost.spread_paid_price == pytest.approx(0.15)
    assert cost.slippage_price == pytest.approx(0.0)


def test_stop_exit_requires_atr_for_slippage() -> None:
    with pytest.raises(ValueError, match="atr is required"):
        price_with_execution_costs(
            symbol="XAUUSD",
            side="buy",
            action="exit",
            raw_price=2000.0,
            lots=1.0,
            exit_reason="stop",
        )


def test_unknown_symbol_is_rejected_loudly() -> None:
    with pytest.raises(ValueError, match="unsupported symbol"):
        get_default_cost_spec("EURUSD")
