from collections import namedtuple
from pathlib import Path

from scripts.log_h024_mt5_terminal_preflight import (
    FORBIDDEN_MT5_CALL_NAMES,
    ForbiddenMt5CallError,
    GuardedMt5Reader,
    build_terminal_preflight_report,
    format_terminal_preflight_report,
    write_terminal_preflight_report,
)


TerminalInfo = namedtuple("TerminalInfo", "connected trade_allowed name")
AccountInfo = namedtuple("AccountInfo", "login server currency leverage trade_allowed")
SymbolInfo = namedtuple(
    "SymbolInfo",
    (
        "visible trade_mode trade_exemode filling_mode order_mode volume_min volume_max "
        "volume_step trade_stops_level trade_freeze_level point digits spread spread_float"
    ),
)
TickInfo = namedtuple("TickInfo", "bid ask time")


class FakeMt5:
    def __init__(self):
        self.calls = []
        self.symbols = {
            "USDJPYm": SymbolInfo(
                visible=True,
                trade_mode=4,
                trade_exemode=2,
                filling_mode=3,
                order_mode=127,
                volume_min=0.01,
                volume_max=300.0,
                volume_step=0.01,
                trade_stops_level=0,
                trade_freeze_level=0,
                point=0.001,
                digits=3,
                spread=18,
                spread_float=True,
            ),
            "XAUUSDm": SymbolInfo(
                visible=True,
                trade_mode=4,
                trade_exemode=2,
                filling_mode=3,
                order_mode=127,
                volume_min=0.01,
                volume_max=200.0,
                volume_step=0.01,
                trade_stops_level=0,
                trade_freeze_level=0,
                point=0.001,
                digits=3,
                spread=360,
                spread_float=True,
            ),
        }
        self.ticks = {
            "USDJPYm": TickInfo(bid=155.001, ask=155.019, time=1710000000),
            "XAUUSDm": TickInfo(bid=2300.100, ask=2300.460, time=1710000001),
        }

    def initialize(self):
        self.calls.append("initialize")
        return True

    def shutdown(self):
        self.calls.append("shutdown")

    def last_error(self):
        self.calls.append("last_error")
        return (0, "ok")

    def terminal_info(self):
        self.calls.append("terminal_info")
        return TerminalInfo(connected=True, trade_allowed=True, name="fake terminal")

    def account_info(self):
        self.calls.append("account_info")
        return AccountInfo(
            login=123456,
            server="Exness-Demo",
            currency="USD",
            leverage=200,
            trade_allowed=True,
        )

    def symbol_info(self, symbol):
        self.calls.append(("symbol_info", symbol))
        return self.symbols.get(symbol)

    def symbol_select(self, symbol, enable):
        self.calls.append(("symbol_select", symbol, enable))
        return symbol in self.symbols and enable

    def symbol_info_tick(self, symbol):
        self.calls.append(("symbol_info_tick", symbol))
        return self.ticks.get(symbol)


class FakeMt5WithForbidden(FakeMt5):
    def order_send(self, request):  # pragma: no cover - must never be called
        raise AssertionError("order_send must not be called")


def test_terminal_preflight_report_passes_with_fake_mt5():
    mt5 = FakeMt5()

    report = build_terminal_preflight_report(mt5)

    assert report.passed
    assert report.mt5_initialized
    assert len(report.symbols) == 2
    assert {symbol.model_symbol for symbol in report.symbols} == {"USDJPY", "XAUUSD"}
    assert all(symbol.status == "ok" for symbol in report.symbols)
    assert report.forbidden_call_attempts == ()
    assert "shutdown" in mt5.calls


def test_terminal_preflight_does_not_fail_just_because_order_send_exists():
    mt5 = FakeMt5WithForbidden()

    report = build_terminal_preflight_report(mt5)

    assert report.passed
    assert report.forbidden_call_attempts == ()
    assert "order_send" in FORBIDDEN_MT5_CALL_NAMES
    assert all(call != "order_send" for call in mt5.calls)


def test_guarded_mt5_blocks_forbidden_call_attempt():
    guarded = GuardedMt5Reader(FakeMt5())

    blocked_order_send = guarded.order_send

    try:
        blocked_order_send({"symbol": "USDJPYm"})
    except ForbiddenMt5CallError as exc:
        assert "order_send" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("order_send attempt should be blocked")

    assert guarded.forbidden_call_attempts == ["order_send"]


def test_terminal_preflight_report_fails_when_symbol_tick_missing():
    mt5 = FakeMt5()
    del mt5.ticks["XAUUSDm"]

    report = build_terminal_preflight_report(mt5)

    assert not report.passed
    xauusd = next(symbol for symbol in report.symbols if symbol.model_symbol == "XAUUSD")
    assert xauusd.status == "fail"
    assert xauusd.reason == "symbol_info_tick unavailable"


def test_terminal_preflight_report_handles_initialize_failure():
    class FailingMt5(FakeMt5):
        def initialize(self):
            self.calls.append("initialize")
            return False

    mt5 = FailingMt5()

    report = build_terminal_preflight_report(mt5)

    assert not report.passed
    assert not report.mt5_initialized
    assert report.symbols == ()


def test_write_terminal_preflight_report_writes_json(tmp_path: Path):
    path = tmp_path / "preflight.json"
    report = build_terminal_preflight_report(FakeMt5())

    write_terminal_preflight_report(report, path)

    text = path.read_text(encoding="utf-8")
    assert '"passed": true' in text
    assert '"broker_symbol": "USDJPYm"' in text
    assert "No demo/live/Phase 4 approval." in text


def test_format_terminal_preflight_report_preserves_deployment_boundary(tmp_path: Path):
    output_path = tmp_path / "preflight.json"
    report = build_terminal_preflight_report(FakeMt5())

    text = format_terminal_preflight_report(report, output_path)

    assert "H024 MT5 terminal/account preflight" in text
    assert "Research only. No demo/live/Phase 4 approval." in text
    assert "PASS does not approve demo trading, live trading, Phase 4, or EA execution." in text
