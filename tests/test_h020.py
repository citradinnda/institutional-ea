from __future__ import annotations

import pandas as pd
import pytest

from quantcore.strategy.h020 import H020SizingConfig, size_h020_interval_intents, generate_h020_intent_panel


def _run_interval(
    *,
    equity_usd: float = 10_000.0,
    usdjpy_risk: float = 0.0,
    xauusd_risk: float = 0.0,
    usdjpy_entry: float = 150.0,
    xauusd_entry: float = 1800.0,
    usdjpy_long_stop: float = 149.0,
    usdjpy_short_stop: float = 151.0,
    xauusd_long_stop: float = 1790.0,
    xauusd_short_stop: float = 1810.0,
    config: H020SizingConfig | None = None,
):
    return size_h020_interval_intents(
        decision_time=pd.Timestamp("2024-01-01 00:00:00", tz="UTC"),
        entry_time=pd.Timestamp("2024-01-01 04:00:00", tz="UTC"),
        equity_usd=equity_usd,
        signed_risk_by_symbol={
            "USDJPY": usdjpy_risk,
            "XAUUSD": xauusd_risk,
        },
        entry_raw_price_by_symbol={
            "USDJPY": usdjpy_entry,
            "XAUUSD": xauusd_entry,
        },
        stops_long_by_symbol={
            "USDJPY": usdjpy_long_stop,
            "XAUUSD": xauusd_long_stop,
        },
        stops_short_by_symbol={
            "USDJPY": usdjpy_short_stop,
            "XAUUSD": xauusd_short_stop,
        },
        config=config,
    )


def test_h020_suppresses_flat_signal() -> None:
    result = _run_interval()

    intent = result.intents["USDJPY"]

    assert intent.suppressed is True
    assert intent.suppression_reason == "flat_signal"
    assert intent.final_lots == 0.0
    assert result.portfolio_gross_leverage == 0.0


def test_h020_suppresses_invalid_stop_geometry() -> None:
    result = _run_interval(
        usdjpy_risk=0.01,
        usdjpy_entry=150.0,
        usdjpy_long_stop=150.0,
    )

    intent = result.intents["USDJPY"]

    assert intent.suppressed is True
    assert intent.suppression_reason == "invalid_stop_geometry"
    assert intent.side == "buy"
    assert intent.raw_stop_distance == 0.0
    assert intent.final_lots == 0.0


def test_h020_suppresses_stop_distance_below_one_spread() -> None:
    result = _run_interval(
        usdjpy_risk=-0.01,
        usdjpy_entry=150.0,
        usdjpy_short_stop=150.005,
    )

    intent = result.intents["USDJPY"]

    assert intent.suppressed is True
    assert intent.suppression_reason == "minimum_stop_distance"
    assert intent.side == "sell"
    assert intent.raw_stop_distance == pytest.approx(0.005)
    assert intent.final_lots == 0.0


def test_h020_caps_per_trade_lots_below_hard_guard() -> None:
    result = _run_interval(
        usdjpy_risk=0.01,
        usdjpy_entry=150.0,
        usdjpy_long_stop=149.98,
    )

    intent = result.intents["USDJPY"]

    assert intent.suppressed is False
    assert intent.risk_based_lots > intent.per_trade_cap_lots
    assert intent.final_lots == intent.per_trade_cap_lots
    assert intent.gross_leverage <= 9.0
    assert intent.final_lots == pytest.approx(0.9)


def test_h020_scales_portfolio_gross_notional_after_per_trade_caps() -> None:
    result = _run_interval(
        usdjpy_risk=0.01,
        xauusd_risk=0.01,
        usdjpy_entry=150.0,
        xauusd_entry=1800.0,
        usdjpy_long_stop=149.85,
        xauusd_long_stop=1798.0,
    )

    usdjpy = result.intents["USDJPY"]
    xauusd = result.intents["XAUUSD"]

    assert result.portfolio_scaled is True
    assert result.portfolio_gross_leverage <= 9.0
    assert usdjpy.final_lots < usdjpy.pre_portfolio_lots
    assert xauusd.final_lots < xauusd.pre_portfolio_lots
    assert usdjpy.suppressed is False
    assert xauusd.suppressed is False


def test_h020_preserves_final_signed_risk_fraction_from_final_lots() -> None:
    result = _run_interval(
        xauusd_risk=-0.01,
        xauusd_entry=1800.0,
        xauusd_short_stop=1810.0,
    )

    intent = result.intents["XAUUSD"]

    assert intent.suppressed is False
    assert intent.side == "sell"
    assert intent.final_lots == pytest.approx(0.1)
    assert intent.final_signed_risk_fraction == pytest.approx(-0.01)


def test_h020_rejects_non_positive_equity() -> None:
    with pytest.raises(ValueError, match="equity_usd must be positive"):
        _run_interval(equity_usd=0.0)


def test_h020_rejects_non_positive_caps() -> None:
    with pytest.raises(ValueError, match="per_trade_max_gross_leverage"):
        _run_interval(config=H020SizingConfig(per_trade_max_gross_leverage=0.0))

def test_h020_generate_intent_panel() -> None:
    timestamps = pd.date_range("2024-01-01 00:00:00", periods=3, freq="4h", tz="UTC")
    positions = pd.DataFrame({
        "USDJPY": [0.01, 0.01, 0.0],
        "XAUUSD": [0.0, -0.01, 0.0],
    }, index=timestamps)
    stops_long = pd.DataFrame({
        "USDJPY": [149.0, 149.0, 149.0],
        "XAUUSD": [1790.0, 1790.0, 1790.0],
    }, index=timestamps)
    stops_short = pd.DataFrame({
        "USDJPY": [151.0, 151.0, 151.0],
        "XAUUSD": [1810.0, 1810.0, 1810.0],
    }, index=timestamps)

    h4_usdjpy = pd.DataFrame({"open": [150.0, 150.5, 151.0]}, index=timestamps)
    h4_xauusd = pd.DataFrame({"open": [1800.0, 1795.0, 1790.0]}, index=timestamps)

    results = generate_h020_intent_panel(
        positions=positions,
        stops_long=stops_long,
        stops_short=stops_short,
        h4_by_symbol={"USDJPY": h4_usdjpy, "XAUUSD": h4_xauusd},
        equity_usd=10000.0,
    )

    assert len(results) == 2

    # Interval 0 -> Entry at Interval 1
    res0 = results[0]
    assert res0.decision_time == timestamps[0]
    assert res0.entry_time == timestamps[1]
    assert "USDJPY" in res0.intents
    assert "XAUUSD" in res0.intents
    assert res0.intents["XAUUSD"].suppressed is True
    assert res0.intents["XAUUSD"].suppression_reason == "flat_signal"
    assert res0.intents["USDJPY"].entry_raw_price == 150.5

    # Interval 1 -> Entry at Interval 2
    res1 = results[1]
    assert "USDJPY" in res1.intents
    assert "XAUUSD" in res1.intents
    assert res1.intents["XAUUSD"].side == "sell"
    assert res1.intents["XAUUSD"].entry_raw_price == 1790.0
