from __future__ import annotations

from types import SimpleNamespace

from quantcore.execution.h024_runtime_safety_heartbeat import EXPECTED_ACCOUNT_CURRENCY, EXPECTED_SERVER
from quantcore.execution.h024_runtime_tick_spread_safety_supervisor import (
    FORBIDDEN_AUTHORIZATION_KEYS,
    collect_h024_runtime_tick_spread_safety_supervisor,
    verify_h024_runtime_tick_spread_safety_supervisor_records,
)

NOW = 1_700_000_000.0
_MISSING = object()


class FakeMT5:
    def __init__(
        self,
        *,
        initialize_result: bool = True,
        account_info: object = _MISSING,
        terminal_info: object = _MISSING,
        symbol_info_by_symbol: dict[str, object | None] | None = None,
        tick_by_symbol: dict[str, object | None] | None = None,
    ) -> None:
        self.calls: list[str] = []
        self._initialize_result = initialize_result
        self._account_info = (
            SimpleNamespace(server=EXPECTED_SERVER, currency=EXPECTED_ACCOUNT_CURRENCY, login=123456)
            if account_info is _MISSING
            else account_info
        )
        self._terminal_info = (
            SimpleNamespace(connected=True, trade_allowed=True)
            if terminal_info is _MISSING
            else terminal_info
        )
        self._symbol_info_by_symbol = symbol_info_by_symbol or {
            "XAUUSDm": SimpleNamespace(name="XAUUSDm", visible=True, point=0.001, digits=3),
            "USDJPYm": SimpleNamespace(name="USDJPYm", visible=True, point=0.001, digits=3),
        }
        self._tick_by_symbol = tick_by_symbol or {
            "XAUUSDm": SimpleNamespace(bid=4728.100, ask=4728.300, time_msc=int(NOW * 1000), time=int(NOW)),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=int(NOW * 1000), time=int(NOW)),
        }

    def initialize(self) -> bool:
        self.calls.append("initialize")
        return self._initialize_result

    def account_info(self) -> object | None:
        self.calls.append("account_info")
        return self._account_info

    def terminal_info(self) -> object | None:
        self.calls.append("terminal_info")
        return self._terminal_info

    def last_error(self) -> tuple[int, str]:
        self.calls.append("last_error")
        return (0, "OK")

    def version(self) -> tuple[int, int, str]:
        self.calls.append("version")
        return (500, 0, "fake")

    def symbol_info(self, symbol: str) -> object | None:
        self.calls.append(f"symbol_info:{symbol}")
        return self._symbol_info_by_symbol.get(symbol)

    def symbol_info_tick(self, symbol: str) -> object | None:
        self.calls.append(f"symbol_info_tick:{symbol}")
        return self._tick_by_symbol.get(symbol)

    def symbol_select(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("symbol_select must never be called by tick/spread supervisor")

    def order_check(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_check must never be called by tick/spread supervisor")

    def order_send(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_send must never be called by tick/spread supervisor")


def test_successful_supervisor_passes_but_authorizes_nothing() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == "TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert record["effective_new_entries_blocked"] is True
    assert record["symbol_select_authorized"] is False
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        assert record["authorizations"][key] is False
        assert record[key] is False
    assert {item["runtime_symbol"] for item in record["symbols"]} == {"XAUUSDm", "USDJPYm"}


def test_supervisor_calls_no_symbol_select_order_check_or_order_send() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "PASS"
    assert "symbol_select" not in fake.calls
    assert "order_check" not in fake.calls
    assert "order_send" not in fake.calls


def test_heartbeat_failure_fails_closed() -> None:
    fake = FakeMT5(account_info=SimpleNamespace(server="Wrong-Server", currency=EXPECTED_ACCOUNT_CURRENCY))

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED_TICK_SPREAD_SUPERVISOR_BLOCKED"
    assert record["effective_new_entries_blocked"] is True
    assert any(check["name"] == "runtime_safety_heartbeat_passed" and not check["passed"] for check in record["checks"])


def test_missing_symbol_info_fails_closed() -> None:
    fake = FakeMT5(symbol_info_by_symbol={"XAUUSDm": None, "USDJPYm": SimpleNamespace(name="USDJPYm", visible=True, point=0.001)})

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    xauusd = next(item for item in record["symbols"] if item["runtime_symbol"] == "XAUUSDm")
    assert any(check["name"] == "symbol_info_available" and not check["passed"] for check in xauusd["checks"])


def test_missing_tick_fails_closed() -> None:
    fake = FakeMT5(tick_by_symbol={"XAUUSDm": None, "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=int(NOW * 1000))})

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    xauusd = next(item for item in record["symbols"] if item["runtime_symbol"] == "XAUUSDm")
    assert any(check["name"] == "tick_available" and not check["passed"] for check in xauusd["checks"])


def test_invisible_symbol_fails_closed() -> None:
    fake = FakeMT5(
        symbol_info_by_symbol={
            "XAUUSDm": SimpleNamespace(name="XAUUSDm", visible=False, point=0.001),
            "USDJPYm": SimpleNamespace(name="USDJPYm", visible=True, point=0.001),
        }
    )

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    xauusd = next(item for item in record["symbols"] if item["runtime_symbol"] == "XAUUSDm")
    assert any(check["name"] == "symbol_visible_selection_ready" and not check["passed"] for check in xauusd["checks"])


def test_invalid_bid_ask_fails_closed() -> None:
    fake = FakeMT5(
        tick_by_symbol={
            "XAUUSDm": SimpleNamespace(bid=4728.300, ask=4728.100, time_msc=int(NOW * 1000)),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=int(NOW * 1000)),
        }
    )

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    xauusd = next(item for item in record["symbols"] if item["runtime_symbol"] == "XAUUSDm")
    assert any(check["name"] == "ask_above_bid" and not check["passed"] for check in xauusd["checks"])


def test_excessive_spread_fails_closed() -> None:
    fake = FakeMT5(
        tick_by_symbol={
            "XAUUSDm": SimpleNamespace(bid=4728.100, ask=4738.100, time_msc=int(NOW * 1000)),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=int(NOW * 1000)),
        }
    )

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    xauusd = next(item for item in record["symbols"] if item["runtime_symbol"] == "XAUUSDm")
    assert any(check["name"] == "spread_points_within_threshold" and not check["passed"] for check in xauusd["checks"])


def test_stale_tick_fails_closed() -> None:
    stale_time = int((NOW - 7200.0) * 1000)
    fake = FakeMT5(
        tick_by_symbol={
            "XAUUSDm": SimpleNamespace(bid=4728.100, ask=4728.300, time_msc=stale_time),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=int(NOW * 1000)),
        }
    )

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    xauusd = next(item for item in record["symbols"] if item["runtime_symbol"] == "XAUUSDm")
    assert any(check["name"] == "tick_fresh_within_threshold" and not check["passed"] for check in xauusd["checks"])


def test_invalid_point_fails_closed() -> None:
    fake = FakeMT5(
        symbol_info_by_symbol={
            "XAUUSDm": SimpleNamespace(name="XAUUSDm", visible=True, point=0.0),
            "USDJPYm": SimpleNamespace(name="USDJPYm", visible=True, point=0.001),
        }
    )

    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    assert record["verdict"] == "FAIL"
    xauusd = next(item for item in record["symbols"] if item["runtime_symbol"] == "XAUUSDm")
    assert any(check["name"] == "symbol_point_positive" and not check["passed"] for check in xauusd["checks"])


def test_verifier_requires_all_authorizations_false() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)
    record["authorizations"]["order_send_authorized"] = True

    verification = verify_h024_runtime_tick_spread_safety_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNSAFE_AUTHORIZATION_TRUE"
        for violation in verification["verification_violations"]
    )


def test_verifier_require_pass_rejects_fail_closed_record() -> None:
    fake = FakeMT5(
        tick_by_symbol={
            "XAUUSDm": SimpleNamespace(bid=4728.100, ask=4728.300, time_msc=int((NOW - 7200.0) * 1000)),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=int(NOW * 1000)),
        }
    )
    record = collect_h024_runtime_tick_spread_safety_supervisor(mt5_client=fake, now_epoch_seconds=NOW)

    verification = verify_h024_runtime_tick_spread_safety_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RECORD_VERDICT_NOT_PASS"
        for violation in verification["verification_violations"]
    )