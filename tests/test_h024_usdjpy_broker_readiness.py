from __future__ import annotations

from types import SimpleNamespace

from quantcore.execution.h024_usdjpy_broker_readiness import (
    MAGIC,
    RUNTIME_SYMBOL,
    build_h024_usdjpy_broker_readiness_record,
    verify_h024_usdjpy_broker_readiness_records,
)


class Obj(SimpleNamespace):
    def _asdict(self):
        return dict(vars(self))


class FakeMT5:
    TIMEFRAME_H4 = 16388
    TIMEFRAME_M1 = 1

    def __init__(self):
        self.initialized = False
        self.shutdown_called = False
        self.account = Obj(server="Exness-MT5Trial6", currency="USD", balance=10000.0, equity=10000.0, margin_free=10000.0)
        self.symbol = Obj(
            name=RUNTIME_SYMBOL,
            visible=True,
            trade_mode=4,
            point=0.001,
            trade_tick_size=0.001,
            trade_contract_size=100000.0,
            volume_min=0.01,
            volume_step=0.01,
            volume_max=200.0,
            spread=15,
            digits=3,
            filling_mode=1,
        )
        self.tick = Obj(bid=155.000, ask=155.015, time=1778514693)
        self.h4_rates = [{"time": i, "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.0} for i in range(50)]
        self.m1_rates = [{"time": i, "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.0} for i in range(200)]
        self.positions = []
        self.orders = []

    def initialize(self):
        self.initialized = True
        return True

    def shutdown(self):
        self.shutdown_called = True
        return True

    def account_info(self):
        return self.account

    def symbol_info(self, symbol):
        assert symbol == RUNTIME_SYMBOL
        return self.symbol

    def symbol_info_tick(self, symbol):
        assert symbol == RUNTIME_SYMBOL
        return self.tick

    def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
        assert symbol == RUNTIME_SYMBOL
        assert start_pos == 0
        if timeframe == self.TIMEFRAME_H4:
            return self.h4_rates[:count]
        if timeframe == self.TIMEFRAME_M1:
            return self.m1_rates[:count]
        raise AssertionError(f"Unexpected timeframe: {timeframe}")

    def positions_get(self, symbol=None):
        assert symbol == RUNTIME_SYMBOL
        return self.positions

    def orders_get(self, symbol=None):
        assert symbol == RUNTIME_SYMBOL
        return self.orders

    def order_check(self, request):
        raise AssertionError("order_check must not be called by USDJPY broker-readiness")

    def order_send(self, request):
        raise AssertionError("order_send must not be called by USDJPY broker-readiness")


def test_usdjpy_readiness_passes_for_clean_read_only_state():
    mt5 = FakeMT5()

    record = build_h024_usdjpy_broker_readiness_record(mt5, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["runtime_symbol"] == "USDJPYm"
    assert record["model_symbol"] == "USDJPY"
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["usd_jpy_order_authorized"] is False
    assert record["trading_loop_authorized"] is False
    assert record["requires_separate_canary_governance"] is True
    assert record["h020_sizing_feasibility"]["candidate_floor_lot_feasible"] is True
    assert mt5.shutdown_called is True


def test_verifier_accepts_pass_record_when_require_pass():
    mt5 = FakeMT5()
    record = build_h024_usdjpy_broker_readiness_record(mt5, generated_at_utc="2026-05-12T00:00:00Z")

    summary = verify_h024_usdjpy_broker_readiness_records([record], require_pass=True)

    assert summary["verdict"] == "PASS"
    assert summary["violations"] == []


def test_fails_closed_for_wrong_server():
    mt5 = FakeMT5()
    mt5.account.server = "Some-Other-Server"

    record = build_h024_usdjpy_broker_readiness_record(mt5)

    assert record["verdict"] == "FAIL"
    assert "unexpected_account_server" in record["violations"]


def test_fails_closed_when_h024_usdjpy_position_exists():
    mt5 = FakeMT5()
    mt5.positions = [Obj(symbol=RUNTIME_SYMBOL, magic=MAGIC, ticket=123, volume=0.01)]

    record = build_h024_usdjpy_broker_readiness_record(mt5)

    assert record["verdict"] == "FAIL"
    assert "unexpected_h024_usdjpy_position_exists" in record["violations"]


def test_fails_closed_when_h024_usdjpy_pending_order_exists():
    mt5 = FakeMT5()
    mt5.orders = [Obj(symbol=RUNTIME_SYMBOL, magic=MAGIC, ticket=456, volume_current=0.01)]

    record = build_h024_usdjpy_broker_readiness_record(mt5)

    assert record["verdict"] == "FAIL"
    assert "unexpected_h024_usdjpy_pending_order_exists" in record["violations"]


def test_fails_closed_for_crossed_tick():
    mt5 = FakeMT5()
    mt5.tick = Obj(bid=155.020, ask=155.010, time=1778514693)

    record = build_h024_usdjpy_broker_readiness_record(mt5)

    assert record["verdict"] == "FAIL"
    assert "crossed_tick_bid_ask" in record["violations"]


def test_fails_closed_for_insufficient_broker_native_rates():
    mt5 = FakeMT5()
    mt5.h4_rates = []
    mt5.m1_rates = []

    record = build_h024_usdjpy_broker_readiness_record(mt5)

    assert record["verdict"] == "FAIL"
    assert "insufficient_broker_native_h4_bars" in record["violations"]
    assert "insufficient_broker_native_m1_bars" in record["violations"]


def test_verifier_rejects_any_mutation_authorization_even_if_record_says_pass():
    mt5 = FakeMT5()
    record = build_h024_usdjpy_broker_readiness_record(mt5)
    record["broker_mutation_authorized"] = True

    summary = verify_h024_usdjpy_broker_readiness_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "broker_mutation_authorized_must_be_false" in summary["violations"]


def test_verifier_rejects_order_send_authorization_even_if_record_says_pass():
    mt5 = FakeMT5()
    record = build_h024_usdjpy_broker_readiness_record(mt5)
    record["order_send_authorized"] = True
    record["request_shape_implications"]["order_send_authorized_now"] = True

    summary = verify_h024_usdjpy_broker_readiness_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "order_send_authorized_must_be_false" in summary["violations"]
    assert "request_shape_order_send_authorized_now_must_be_false" in summary["violations"]