from __future__ import annotations

from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from quantcore.backtest.fill_engine import Fill
from quantcore.backtest.portfolio import (
    DEFAULT_INSTRUMENT_SPECS,
    InstrumentSpec,
    PortfolioResult,
    PositionSize,
    build_portfolio_result,
    fill_pnl_usd,
    get_default_instrument_spec,
    quote_pnl_to_usd,
    round_lots_down,
    size_position_from_risk,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _fill(
    *,
    symbol: str,
    exit_time: str,
    exit_price: float,
    pnl_quote: float,
    commission: float,
) -> Fill:
    return Fill(
        symbol=symbol,
        side="buy",
        entry_time_utc=_utc("2024-01-02 00:00"),
        entry_price=100.0,
        exit_time_utc=_utc(exit_time),
        exit_price=exit_price,
        lots=1.0,
        pnl_quote=pnl_quote,
        commission=commission,
        slippage=0.0,
        exit_reason="signal_flip",
    )


def test_default_instrument_specs_match_phase_3_assumptions() -> None:
    usdjpy = get_default_instrument_spec("USDJPY")
    xauusd = get_default_instrument_spec("xauusd")

    assert usdjpy.symbol == "USDJPY"
    assert usdjpy.contract_size == pytest.approx(100_000.0)
    assert usdjpy.quote_currency == "JPY"
    assert usdjpy.lot_step == pytest.approx(0.01)

    assert xauusd.symbol == "XAUUSD"
    assert xauusd.contract_size == pytest.approx(100.0)
    assert xauusd.quote_currency == "USD"
    assert xauusd.lot_step == pytest.approx(0.01)


def test_default_instrument_specs_are_immutable_mapping() -> None:
    with pytest.raises(TypeError):
        DEFAULT_INSTRUMENT_SPECS["EURUSD"] = InstrumentSpec(  # type: ignore[index]
            symbol="EURUSD",
            contract_size=100_000.0,
            quote_currency="USD",
        )


def test_structured_returns_are_frozen() -> None:
    position = PositionSize(
        symbol="XAUUSD",
        side="buy",
        signed_risk_fraction=0.01,
        lots=0.10,
        target_risk_usd=100.0,
        actual_risk_usd=100.0,
        notional_quote=20_000.0,
    )
    result = PortfolioResult(
        fills=(),
        starting_equity_usd=10_000.0,
        ending_equity_usd=10_000.0,
        equity_curve=pd.Series(dtype=float),
        returns=pd.Series(dtype=float),
        drawdowns=pd.Series(dtype=float),
        max_drawdown=0.0,
    )

    with pytest.raises(FrozenInstanceError):
        position.lots = 0.20  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        result.ending_equity_usd = 9_000.0  # type: ignore[misc]


def test_round_lots_down_to_step_without_overrisking() -> None:
    assert round_lots_down(raw_lots=0.149, lot_step=0.01, min_lot=0.01) == pytest.approx(0.14)
    assert round_lots_down(raw_lots=0.150, lot_step=0.01, min_lot=0.01) == pytest.approx(0.15)


def test_round_lots_below_minimum_returns_zero() -> None:
    assert round_lots_down(raw_lots=0.009, lot_step=0.01, min_lot=0.01) == pytest.approx(0.0)


def test_xauusd_position_sizing_from_signed_risk_fraction() -> None:
    size = size_position_from_risk(
        symbol="XAUUSD",
        signed_risk_fraction=0.01,
        equity_usd=10_000.0,
        entry_price=2_000.0,
        stop_distance_price=10.0,
    )

    assert size.side == "buy"
    assert size.lots == pytest.approx(0.10)
    assert size.target_risk_usd == pytest.approx(100.0)
    assert size.actual_risk_usd == pytest.approx(100.0)
    assert size.notional_quote == pytest.approx(20_000.0)


def test_usdjpy_position_sizing_converts_jpy_risk_to_usd() -> None:
    size = size_position_from_risk(
        symbol="USDJPY",
        signed_risk_fraction=-0.01,
        equity_usd=10_000.0,
        entry_price=150.0,
        stop_distance_price=1.0,
    )

    assert size.side == "sell"
    assert size.lots == pytest.approx(0.15)
    assert size.target_risk_usd == pytest.approx(100.0)
    assert size.actual_risk_usd == pytest.approx(100.0)
    assert size.notional_quote == pytest.approx(2_250_000.0)


def test_flat_risk_fraction_returns_zero_lot_position() -> None:
    size = size_position_from_risk(
        symbol="XAUUSD",
        signed_risk_fraction=0.0,
        equity_usd=10_000.0,
        entry_price=2_000.0,
        stop_distance_price=10.0,
    )

    assert size.side is None
    assert size.lots == pytest.approx(0.0)
    assert size.target_risk_usd == pytest.approx(0.0)
    assert size.actual_risk_usd == pytest.approx(0.0)


def test_quote_pnl_to_usd_handles_usd_and_jpy_quotes() -> None:
    assert quote_pnl_to_usd(symbol="XAUUSD", pnl_quote=125.0) == pytest.approx(125.0)
    assert quote_pnl_to_usd(
        symbol="USDJPY",
        pnl_quote=15_000.0,
        conversion_price=150.0,
    ) == pytest.approx(100.0)


def test_jpy_quote_conversion_requires_conversion_price() -> None:
    with pytest.raises(ValueError, match="conversion_price is required"):
        quote_pnl_to_usd(symbol="USDJPY", pnl_quote=15_000.0)


def test_fill_pnl_usd_subtracts_commission_after_currency_conversion() -> None:
    xau_fill = _fill(
        symbol="XAUUSD",
        exit_time="2024-01-02 00:01",
        exit_price=2_010.0,
        pnl_quote=100.0,
        commission=10.0,
    )
    jpy_fill = _fill(
        symbol="USDJPY",
        exit_time="2024-01-02 00:02",
        exit_price=150.0,
        pnl_quote=15_000.0,
        commission=7.0,
    )

    assert fill_pnl_usd(fill=xau_fill) == pytest.approx(90.0)
    assert fill_pnl_usd(fill=jpy_fill) == pytest.approx(93.0)


def test_build_portfolio_result_tracks_equity_returns_and_drawdown() -> None:
    fills = [
        _fill(
            symbol="XAUUSD",
            exit_time="2024-01-02 00:01",
            exit_price=2_010.0,
            pnl_quote=100.0,
            commission=10.0,
        ),
        _fill(
            symbol="XAUUSD",
            exit_time="2024-01-02 00:02",
            exit_price=1_990.0,
            pnl_quote=-200.0,
            commission=10.0,
        ),
    ]

    result = build_portfolio_result(
        fills=fills,
        starting_equity_usd=10_000.0,
    )

    assert result.ending_equity_usd == pytest.approx(9_880.0)
    assert result.equity_curve.iloc[0] == pytest.approx(10_090.0)
    assert result.equity_curve.iloc[1] == pytest.approx(9_880.0)
    assert result.returns.iloc[0] == pytest.approx(90.0 / 10_000.0)
    assert result.returns.iloc[1] == pytest.approx(-210.0 / 10_090.0)
    assert result.max_drawdown == pytest.approx((9_880.0 / 10_090.0) - 1.0)


def test_build_portfolio_result_rejects_unsorted_fills() -> None:
    fills = [
        _fill(
            symbol="XAUUSD",
            exit_time="2024-01-02 00:02",
            exit_price=2_010.0,
            pnl_quote=100.0,
            commission=10.0,
        ),
        _fill(
            symbol="XAUUSD",
            exit_time="2024-01-02 00:01",
            exit_price=1_990.0,
            pnl_quote=-200.0,
            commission=10.0,
        ),
    ]

    with pytest.raises(ValueError, match="sorted by exit_time_utc"):
        build_portfolio_result(fills=fills)
