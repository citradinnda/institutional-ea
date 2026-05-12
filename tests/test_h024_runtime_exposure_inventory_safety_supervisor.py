from __future__ import annotations

import time
from types import SimpleNamespace

from quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor import (
    CANARY_POSITION_TYPE,
    CANARY_RUNTIME_SYMBOL,
    CANARY_TICKET_IDENTIFIER,
    CANARY_VOLUME,
    H024_MAGIC,
    USDJPY_RUNTIME_SYMBOL,
    collect_h024_runtime_exposure_inventory_safety_supervisor,
    verify_h024_runtime_exposure_inventory_safety_supervisor_records,
)
from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
)

NOW = int(time.time())
_MISSING = object()


def canary_position() -> SimpleNamespace:
    return SimpleNamespace(
        ticket=CANARY_TICKET_IDENTIFIER,
        identifier=CANARY_TICKET_IDENTIFIER,
        symbol=CANARY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume=CANARY_VOLUME,
        type=CANARY_POSITION_TYPE,
        comment="H024_ONE_SHOT_DE",
    )


class FakeMT5:
    def __init__(
        self,
        *,
        initialize_result: bool = True,
        account_info: object = _MISSING,
        terminal_info: object = _MISSING,
        symbol_info_by_symbol: dict[str, object | None] | None = None,
        tick_by_symbol: dict[str, object | None] | None = None,
        positions: object = _MISSING,
        orders: object = _MISSING,
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
            "XAUUSDm": SimpleNamespace(bid=4728.100, ask=4728.300, time_msc=NOW * 1000, time=NOW),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=NOW * 1000, time=NOW),
        }
        self._positions = [canary_position()] if positions is _MISSING else positions
        self._orders = [] if orders is _MISSING else orders

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

    def positions_get(self) -> object:
        self.calls.append("positions_get")
        return self._positions

    def orders_get(self) -> object:
        self.calls.append("orders_get")
        return self._orders

    def symbol_select(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("symbol_select must never be called by exposure/inventory supervisor")

    def order_check(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_check must never be called by exposure/inventory supervisor")

    def order_send(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_send must never be called by exposure/inventory supervisor")


def test_exact_known_canary_passes_but_authorizes_nothing() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == "EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert record["observed"]["canary_state"] == "OBSERVED_EXACT_KNOWN_CANARY"
    assert record["observed"]["h024_position_count"] == 1
    assert record["observed"]["h024_order_count"] == 0
    assert record["effective_new_entries_blocked"] is True
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        assert record["authorizations"][key] is False
        assert record[key] is False


def test_no_canary_position_is_allowed_as_flat_h024_inventory() -> None:
    fake = FakeMT5(positions=[])

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert record["observed"]["canary_state"] == "NOT_OBSERVED"
    assert record["observed"]["h024_position_count"] == 0
    assert record["observed"]["h024_order_count"] == 0


def test_supervisor_calls_no_mutation_or_execution_methods() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert "positions_get" in fake.calls
    assert "orders_get" in fake.calls
    assert "symbol_select" not in fake.calls
    assert "order_check" not in fake.calls
    assert "order_send" not in fake.calls


def test_wrong_canary_ticket_fails_closed() -> None:
    wrong = canary_position()
    wrong.ticket = 999
    wrong.identifier = 999
    fake = FakeMT5(positions=[wrong])

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED_EXPOSURE_INVENTORY_BLOCKED"
    assert any(
        position["verdict"] == "FAIL"
        for position in record["h024_positions"]
    )


def test_wrong_canary_volume_fails_closed() -> None:
    wrong = canary_position()
    wrong.volume = 0.02
    fake = FakeMT5(positions=[wrong])

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        check["name"] == "xauusd_h024_position_is_exact_known_canary_if_present" and not check["passed"]
        for position in record["h024_positions"]
        for check in position["checks"]
    )


def test_wrong_canary_magic_fails_closed() -> None:
    wrong = canary_position()
    wrong.magic = 7
    wrong.comment = "H024_ONE_SHOT_DE"
    fake = FakeMT5(positions=[wrong])

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"


def test_usdjpy_h024_position_fails_closed() -> None:
    usd = SimpleNamespace(
        ticket=123,
        identifier=123,
        symbol=USDJPY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume=0.01,
        type=0,
        comment="H024_USDJPY",
    )
    fake = FakeMT5(positions=[usd])

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        violation["code"] == "POSITION_NOT_USDJPY_H024"
        for violation in record["violations"]
    )


def test_h024_order_fails_closed() -> None:
    order = SimpleNamespace(
        ticket=555,
        symbol=CANARY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume_current=0.01,
        type=1,
        comment="H024_PENDING",
    )
    fake = FakeMT5(orders=[order])

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert record["observed"]["h024_order_count"] == 1
    assert any(
        violation["code"] == "H024_ORDERS_PRESENT"
        for violation in record["violations"]
    )


def test_usdjpy_h024_order_fails_closed() -> None:
    order = SimpleNamespace(
        ticket=777,
        symbol=USDJPY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume_current=0.01,
        type=0,
        comment="H024_USDJPY_PENDING",
    )
    fake = FakeMT5(orders=[order])

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        violation["code"] == "ORDER_NOT_USDJPY_H024"
        for violation in record["violations"]
    )


def test_positions_get_missing_fails_closed() -> None:
    fake = FakeMT5(positions=None)

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "positions_get_available" and not check["passed"] for check in record["checks"])


def test_orders_get_missing_fails_closed() -> None:
    fake = FakeMT5(orders=None)

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "orders_get_available" and not check["passed"] for check in record["checks"])


def test_heartbeat_failure_fails_closed_before_inventory_can_pass() -> None:
    fake = FakeMT5(account_info=SimpleNamespace(server="Wrong-Server", currency=EXPECTED_ACCOUNT_CURRENCY))

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "runtime_safety_heartbeat_passed" and not check["passed"] for check in record["checks"])


def test_tick_spread_failure_fails_closed() -> None:
    fake = FakeMT5(
        tick_by_symbol={
            "XAUUSDm": SimpleNamespace(bid=4728.300, ask=4728.100, time_msc=NOW * 1000, time=NOW),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=NOW * 1000, time=NOW),
        }
    )

    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "runtime_tick_spread_supervisor_passed" and not check["passed"] for check in record["checks"])


def test_verifier_requires_all_authorizations_false() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)
    record["authorizations"]["order_send_authorized"] = True

    verification = verify_h024_runtime_exposure_inventory_safety_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNSAFE_AUTHORIZATION_TRUE"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_fail_closed_record_under_require_pass() -> None:
    wrong = canary_position()
    wrong.volume = 0.02
    fake = FakeMT5(positions=[wrong])
    record = collect_h024_runtime_exposure_inventory_safety_supervisor(mt5_client=fake)

    verification = verify_h024_runtime_exposure_inventory_safety_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RECORD_VERDICT_NOT_PASS"
        for violation in verification["verification_violations"]
    )