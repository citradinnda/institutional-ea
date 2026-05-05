import pytest

from quantcore.backtest.cost_model import SymbolCostSpec
from quantcore.backtest.friction import project_worst_case_round_trip_friction
from quantcore.backtest.portfolio import InstrumentSpec


def test_projected_round_trip_friction_for_xauusd_uses_usd_quote_directly() -> None:
    friction = project_worst_case_round_trip_friction(
        symbol="XAUUSD",
        lots=0.50,
        entry_price=2000.0,
        atr=10.0,
    )

    assert friction.symbol == "XAUUSD"
    assert friction.lots == pytest.approx(0.50)
    assert friction.entry_price == pytest.approx(2000.0)
    assert friction.atr == pytest.approx(10.0)
    assert friction.spread_price == pytest.approx(0.30)
    assert friction.stop_slippage_price == pytest.approx(0.50)

    assert friction.spread_burden_usd == pytest.approx(15.0)
    assert friction.commission_burden_usd == pytest.approx(10.0)
    assert friction.stop_slippage_burden_usd == pytest.approx(25.0)
    assert friction.total_burden_usd == pytest.approx(50.0)
    assert friction.fraction_of_equity(10_000.0) == pytest.approx(0.005)


def test_projected_round_trip_friction_for_usdjpy_converts_jpy_burden_to_usd() -> None:
    friction = project_worst_case_round_trip_friction(
        symbol="USDJPY",
        lots=1.00,
        entry_price=150.0,
        atr=0.20,
    )

    assert friction.symbol == "USDJPY"
    assert friction.spread_price == pytest.approx(0.01)
    assert friction.stop_slippage_price == pytest.approx(0.01)

    assert friction.spread_burden_usd == pytest.approx(1000.0 / 150.0)
    assert friction.commission_burden_usd == pytest.approx(14.0)
    assert friction.stop_slippage_burden_usd == pytest.approx(1000.0 / 150.0)
    assert friction.total_burden_usd == pytest.approx((1000.0 / 150.0) + 14.0 + (1000.0 / 150.0))


@pytest.mark.parametrize(
    ("name", "kwargs"),
    [
        ("lots", {"symbol": "XAUUSD", "lots": 0.0, "entry_price": 2000.0, "atr": 10.0}),
        ("entry_price", {"symbol": "XAUUSD", "lots": 0.5, "entry_price": 0.0, "atr": 10.0}),
        ("atr", {"symbol": "XAUUSD", "lots": 0.5, "entry_price": 2000.0, "atr": 0.0}),
    ],
)
def test_projected_round_trip_friction_rejects_non_positive_inputs(
    name: str,
    kwargs: dict[str, float | str],
) -> None:
    with pytest.raises(ValueError, match=f"{name} must be > 0.0"):
        project_worst_case_round_trip_friction(**kwargs)


def test_projected_round_trip_friction_rejects_cost_spec_symbol_mismatch() -> None:
    with pytest.raises(ValueError, match="cost_spec symbol must match symbol"):
        project_worst_case_round_trip_friction(
            symbol="XAUUSD",
            lots=0.5,
            entry_price=2000.0,
            atr=10.0,
            cost_spec=SymbolCostSpec(
                symbol="USDJPY",
                spread_price=0.01,
                commission_usd_per_lot_per_fill=7.0,
            ),
        )


def test_projected_round_trip_friction_rejects_instrument_spec_symbol_mismatch() -> None:
    with pytest.raises(ValueError, match="instrument_spec symbol must match symbol"):
        project_worst_case_round_trip_friction(
            symbol="XAUUSD",
            lots=0.5,
            entry_price=2000.0,
            atr=10.0,
            instrument_spec=InstrumentSpec(
                symbol="USDJPY",
                contract_size=100_000.0,
                quote_currency="JPY",
            ),
        )


def test_projected_round_trip_friction_fraction_of_equity_rejects_non_positive_equity() -> None:
    friction = project_worst_case_round_trip_friction(
        symbol="XAUUSD",
        lots=0.50,
        entry_price=2000.0,
        atr=10.0,
    )

    with pytest.raises(ValueError, match="equity_usd must be > 0.0"):
        friction.fraction_of_equity(0.0)