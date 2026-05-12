from __future__ import annotations

import time
from types import SimpleNamespace

from quantcore.execution.h024_runtime_account_risk_margin_safety_supervisor import (
    collect_h024_runtime_account_risk_margin_safety_supervisor,
    verify_h024_runtime_account_risk_margin_safety_supervisor_records,
)
from quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor import (
    CANARY_POSITION_TYPE,
    CANARY_RUNTIME_SYMBOL,
    CANARY_TICKET_IDENTIFIER,
    CANARY_VOLUME,
    H024_MAGIC,
    USDJPY_RUNTIME_SYMBOL,
)
from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
)

NOW = int(time.time())
_MISSING = object()


def account(
    *,
    server: str = EXPECTED_SERVER,
    currency: str = EXPECTED_ACCOUNT_CURRENCY,
    balance: float = 10_000.0,
    equity: float = 9_995.0,
    profit: float = -5.0,
    margin: float = 2.50,
    margin_free: float = 9_992.50,
    margin_level: float = 399_800.0,
    credit: float = 0.0,
) -> SimpleNamespace:
    return SimpleNamespace(
        server=server,
        currency=currency,
        balance=balance,
        equity=equity,
        profit=profit,
        margin=margin,
        margin_free=margin_free,
        margin_level=margin_level,
        credit=credit,
        login=123456,
    )


def canary_position(*, profit: float = -5.0, volume: float = CANARY_VOLUME) -> SimpleNamespace:
    return SimpleNamespace(
        ticket=CANARY_TICKET_IDENTIFIER,
        identifier=CANARY_TICKET_IDENTIFIER,
        symbol=CANARY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume=volume,
        type=CANARY_POSITION_TYPE,
        profit=profit,
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
        self._account_info = account() if account_info is _MISSING else account_info
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
        raise AssertionError("symbol_select must never be called by account risk/margin supervisor")

    def order_check(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_check must never be called by account risk/margin supervisor")

    def order_send(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_send must never be called by account risk/margin supervisor")


def test_healthy_account_with_exact_canary_passes_but_authorizes_nothing() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == "ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert record["observed"]["currency"] == EXPECTED_ACCOUNT_CURRENCY
    assert record["observed"]["canary_state"] == "OBSERVED_EXACT_KNOWN_CANARY"
    assert record["effective_new_entries_blocked"] is True
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        assert record["authorizations"][key] is False
        assert record[key] is False


def test_flat_h024_inventory_with_zero_margin_can_pass() -> None:
    fake = FakeMT5(
        account_info=account(balance=10_000.0, equity=10_000.0, profit=0.0, margin=0.0, margin_free=10_000.0, margin_level=0.0),
        positions=[],
    )

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert record["observed"]["canary_state"] == "NOT_OBSERVED"
    assert record["observed"]["margin_used_fraction"] == 0.0


def test_supervisor_calls_no_mutation_or_execution_methods() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert "symbol_select" not in fake.calls
    assert "order_check" not in fake.calls
    assert "order_send" not in fake.calls


def test_missing_account_info_fails_closed() -> None:
    fake = FakeMT5(account_info=None)

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "account_info_available" and not check["passed"] for check in record["checks"])


def test_wrong_currency_fails_closed() -> None:
    fake = FakeMT5(account_info=account(currency="IDR"))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "account_currency_expected" and not check["passed"] for check in record["checks"])


def test_negative_balance_fails_closed() -> None:
    fake = FakeMT5(account_info=account(balance=-1.0, equity=-6.0, profit=-5.0, margin_free=-8.5))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "balance_finite_and_non_negative" and not check["passed"] for check in record["checks"])


def test_negative_equity_fails_closed() -> None:
    fake = FakeMT5(account_info=account(balance=10.0, equity=-5.0, profit=-15.0, margin=2.5, margin_free=-7.5))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "equity_finite_and_non_negative" and not check["passed"] for check in record["checks"])


def test_negative_margin_fails_closed() -> None:
    fake = FakeMT5(account_info=account(margin=-1.0, margin_free=9_996.0))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "margin_finite_and_non_negative" and not check["passed"] for check in record["checks"])


def test_negative_free_margin_fails_closed() -> None:
    fake = FakeMT5(account_info=account(balance=10_000.0, equity=5.0, profit=-9_995.0, margin=10.0, margin_free=-5.0, margin_level=50.0))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "free_margin_finite_and_non_negative" and not check["passed"] for check in record["checks"])


def test_free_margin_identity_mismatch_fails_closed() -> None:
    fake = FakeMT5(account_info=account(margin_free=9_000.0))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "free_margin_identity_consistent" and not check["passed"] for check in record["checks"])


def test_equity_balance_profit_identity_mismatch_fails_closed() -> None:
    fake = FakeMT5(account_info=account(equity=9_500.0, profit=-5.0, margin_free=9_497.5, margin_level=380_000.0))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        check["name"] == "equity_balance_profit_identity_consistent_where_available" and not check["passed"]
        for check in record["checks"]
    )


def test_position_profit_sum_mismatch_fails_closed() -> None:
    fake = FakeMT5(positions=[canary_position(profit=-25.0)])

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        check["name"] == "floating_pnl_consistent_with_positions_where_available" and not check["passed"]
        for check in record["checks"]
    )


def test_margin_level_compression_fails_closed() -> None:
    fake = FakeMT5(account_info=account(balance=10_000.0, equity=9_995.0, profit=-5.0, margin=5_000.0, margin_free=4_995.0, margin_level=199.9))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "margin_level_sane_where_available" and not check["passed"] for check in record["checks"])


def test_margin_used_fraction_compression_fails_closed() -> None:
    fake = FakeMT5(account_info=account(balance=10_000.0, equity=9_995.0, profit=-5.0, margin=6_000.0, margin_free=3_995.0, margin_level=166.58333333333334))

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "total_margin_used_fraction_bounded" and not check["passed"] for check in record["checks"])


def test_canary_volume_above_bound_fails_closed() -> None:
    fake = FakeMT5(positions=[canary_position(volume=0.02)])

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "runtime_exposure_inventory_supervisor_passed" and not check["passed"] for check in record["checks"])


def test_h024_order_fails_closed_via_exposure_inventory() -> None:
    order = SimpleNamespace(
        ticket=555,
        symbol=CANARY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume_current=0.01,
        type=1,
        comment="H024_PENDING",
    )
    fake = FakeMT5(orders=[order])

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "runtime_exposure_inventory_supervisor_passed" and not check["passed"] for check in record["checks"])


def test_usdjpy_h024_position_fails_closed_via_exposure_inventory() -> None:
    usd = SimpleNamespace(
        ticket=123,
        identifier=123,
        symbol=USDJPY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume=0.01,
        type=0,
        profit=0.0,
        comment="H024_USDJPY",
    )
    fake = FakeMT5(
        account_info=account(balance=10_000.0, equity=10_000.0, profit=0.0, margin=0.0, margin_free=10_000.0, margin_level=0.0),
        positions=[usd],
    )

    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "runtime_exposure_inventory_supervisor_passed" and not check["passed"] for check in record["checks"])


def test_verifier_requires_all_authorizations_false() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)
    record["authorizations"]["order_send_authorized"] = True

    verification = verify_h024_runtime_account_risk_margin_safety_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNSAFE_AUTHORIZATION_TRUE"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_fail_closed_record_under_require_pass() -> None:
    fake = FakeMT5(account_info=account(margin_free=9_000.0))
    record = collect_h024_runtime_account_risk_margin_safety_supervisor(mt5_client=fake)

    verification = verify_h024_runtime_account_risk_margin_safety_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RECORD_VERDICT_NOT_PASS"
        for violation in verification["verification_violations"]
    )