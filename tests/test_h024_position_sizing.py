import re
from pathlib import Path

import pytest

from quantcore.strategy.h024_position_sizer import (
    H024PositionSizeRequest,
    H024PositionSizer,
)


def _compute(
    *,
    account_balance_usd=10000.0,
    risk_fraction=0.01,
    entry_price=100.0,
    stop_price=99.5,
    tick_size=0.01,
    tick_value_usd_per_lot=1.0,
    volume_step=0.01,
    min_volume=0.01,
    max_volume=100.0,
    volume_digits=2,
):
    request = H024PositionSizeRequest(
        account_balance_usd=account_balance_usd,
        risk_fraction=risk_fraction,
        entry_price=entry_price,
        stop_price=stop_price,
        tick_size=tick_size,
        tick_value_usd_per_lot=tick_value_usd_per_lot,
        volume_step=volume_step,
        min_volume=min_volume,
        max_volume=max_volume,
        volume_digits=volume_digits,
    )
    return H024PositionSizer(request).compute()


def test_position_size_uses_fixed_risk_stop_ticks_and_tick_value():
    result = _compute(
        account_balance_usd=10000.0,
        risk_fraction=0.01,
        entry_price=100.0,
        stop_price=99.5,
        tick_size=0.01,
        tick_value_usd_per_lot=1.0,
    )

    assert result.risk_usd == pytest.approx(100.0)
    assert result.stop_distance_price == pytest.approx(0.5)
    assert result.stop_distance_ticks == pytest.approx(50.0)
    assert result.loss_usd_per_lot == pytest.approx(50.0)
    assert result.raw_lots == pytest.approx(2.0)
    assert result.lots == pytest.approx(2.0)


def test_position_size_rounds_down_to_broker_volume_step():
    result = _compute(
        account_balance_usd=10000.0,
        risk_fraction=0.01,
        entry_price=100.0,
        stop_price=99.4,
        tick_size=0.01,
        tick_value_usd_per_lot=1.0,
        volume_step=0.01,
    )

    assert result.raw_lots == pytest.approx(1.6666666667)
    assert result.lots == pytest.approx(1.66)


def test_position_size_returns_zero_when_min_volume_would_exceed_risk():
    result = _compute(
        account_balance_usd=1000.0,
        risk_fraction=0.001,
        entry_price=100.0,
        stop_price=90.0,
        tick_size=0.01,
        tick_value_usd_per_lot=1.0,
        volume_step=0.01,
        min_volume=0.01,
    )

    assert result.raw_lots == pytest.approx(0.001)
    assert result.lots == pytest.approx(0.0)


def test_position_size_caps_to_broker_max_volume_without_rounding_up():
    result = _compute(
        account_balance_usd=100000.0,
        risk_fraction=0.10,
        entry_price=100.0,
        stop_price=99.0,
        tick_size=0.01,
        tick_value_usd_per_lot=1.0,
        volume_step=0.01,
        max_volume=5.0,
    )

    assert result.raw_lots == pytest.approx(100.0)
    assert result.lots == pytest.approx(5.0)


def test_position_size_supports_xauusd_style_tick_contract():
    result = _compute(
        account_balance_usd=10000.0,
        risk_fraction=0.01,
        entry_price=2000.0,
        stop_price=1996.0,
        tick_size=0.01,
        tick_value_usd_per_lot=1.0,
        volume_step=0.01,
    )

    assert result.stop_distance_ticks == pytest.approx(400.0)
    assert result.loss_usd_per_lot == pytest.approx(400.0)
    assert result.lots == pytest.approx(0.25)


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"entry_price": 100.0, "stop_price": 100.0}, "stop distance"),
        ({"tick_size": 0.0}, "tick_size"),
        ({"tick_value_usd_per_lot": 0.0}, "tick_value"),
        ({"risk_fraction": 0.0}, "risk_fraction"),
        ({"risk_fraction": 1.5}, "risk_fraction"),
        ({"volume_step": 0.0}, "volume_step"),
        ({"max_volume": 0.001, "min_volume": 0.01}, "max_volume"),
    ],
)
def test_position_size_fails_closed_on_invalid_inputs(overrides, message):
    kwargs = {
        "account_balance_usd": 10000.0,
        "risk_fraction": 0.01,
        "entry_price": 100.0,
        "stop_price": 99.5,
        "tick_size": 0.01,
        "tick_value_usd_per_lot": 1.0,
        "volume_step": 0.01,
        "min_volume": 0.01,
        "max_volume": 100.0,
    }
    kwargs.update(overrides)

    with pytest.raises(ValueError, match=message):
        _compute(**kwargs)


def _strip_comments_and_strings(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    source = re.sub(r"//.*", "", source)
    source = re.sub(r'"(?:\\.|[^"\\])*"', '""', source)
    return source


def test_log_only_ea_source_remains_execution_api_free():
    source_path = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")
    source = _strip_comments_and_strings(source_path.read_text(encoding="utf-8", errors="ignore"))

    forbidden_tokens = [
        "OrderSend(",
        "OrderSendAsync(",
        "OrderCheck(",
        "CTrade",
        "#include <Trade",
        "MqlTradeRequest",
        "MqlTradeResult",
        "PositionOpen(",
        "PositionClose(",
        "PositionModify(",
    ]

    offenders = [token for token in forbidden_tokens if token in source]
    assert offenders == []