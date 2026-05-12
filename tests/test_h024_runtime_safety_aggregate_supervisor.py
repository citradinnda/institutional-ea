from __future__ import annotations

import copy
import time
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor import (
    CANARY_POSITION_TYPE,
    CANARY_RUNTIME_SYMBOL,
    CANARY_TICKET_IDENTIFIER,
    CANARY_VOLUME,
    H024_MAGIC,
)
from quantcore.execution.h024_runtime_safety_aggregate_supervisor import (
    UPSTREAM_PACKET_TYPES,
    collect_h024_runtime_safety_aggregate_supervisor,
    verify_h024_runtime_safety_aggregate_supervisor_records,
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
        raise AssertionError("symbol_select must never be called by aggregate supervisor")

    def order_check(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_check must never be called by aggregate supervisor")

    def order_send(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_send must never be called by aggregate supervisor")


def test_healthy_aggregate_passes_but_authorizes_nothing() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == "RUNTIME_SAFETY_AGGREGATE_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert record["effective_new_entries_blocked"] is True
    assert set(record["upstream_records"]) == set(UPSTREAM_PACKET_TYPES)
    assert all(summary["verdict"] == "PASS" for summary in record["upstream_summaries"])
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        assert record["authorizations"][key] is False
        assert record[key] is False


def test_flat_inventory_aggregate_can_pass() -> None:
    fake = FakeMT5(
        account_info=account(balance=10_000.0, equity=10_000.0, profit=0.0, margin=0.0, margin_free=10_000.0, margin_level=0.0),
        positions=[],
    )

    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"


def test_aggregate_calls_no_mutation_or_execution_methods() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert "symbol_select" not in fake.calls
    assert "order_check" not in fake.calls
    assert "order_send" not in fake.calls


def test_heartbeat_failure_fails_closed() -> None:
    fake = FakeMT5(account_info=account(server="Wrong-Server"))

    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED_RUNTIME_SAFETY_AGGREGATE_BLOCKED"
    assert any(summary["source"] == "runtime_safety_heartbeat" and summary["verdict"] == "FAIL" for summary in record["upstream_summaries"])


def test_tick_spread_failure_fails_closed() -> None:
    fake = FakeMT5(
        tick_by_symbol={
            "XAUUSDm": SimpleNamespace(bid=4728.300, ask=4728.100, time_msc=NOW * 1000, time=NOW),
            "USDJPYm": SimpleNamespace(bid=155.100, ask=155.113, time_msc=NOW * 1000, time=NOW),
        }
    )

    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        summary["source"] == "runtime_tick_spread_safety_supervisor" and summary["verdict"] == "FAIL"
        for summary in record["upstream_summaries"]
    )


def test_exposure_inventory_failure_fails_closed() -> None:
    order = SimpleNamespace(
        ticket=555,
        symbol=CANARY_RUNTIME_SYMBOL,
        magic=H024_MAGIC,
        volume_current=0.01,
        type=1,
        comment="H024_PENDING",
    )
    fake = FakeMT5(orders=[order])

    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        summary["source"] == "runtime_exposure_inventory_safety_supervisor" and summary["verdict"] == "FAIL"
        for summary in record["upstream_summaries"]
    )


def test_account_risk_margin_failure_fails_closed() -> None:
    fake = FakeMT5(account_info=account(margin_free=9_000.0))

    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(
        summary["source"] == "runtime_account_risk_margin_safety_supervisor" and summary["verdict"] == "FAIL"
        for summary in record["upstream_summaries"]
    )


def test_verifier_rejects_top_level_authorization_true() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    record["authorizations"]["order_send_authorized"] = True

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNSAFE_AUTHORIZATION_TRUE"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_missing_upstream_packet() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    del record["upstream_records"]["runtime_safety_heartbeat"]

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UPSTREAM_PACKET_MISSING"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_stale_upstream_packet() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    stale = (datetime.now(UTC) - timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    record["upstream_records"]["runtime_safety_heartbeat"]["observed_at_utc"] = stale

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UPSTREAM_PACKET_FRESH"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_upstream_effective_entries_unblocked() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    record["upstream_records"]["runtime_safety_heartbeat"]["effective_new_entries_blocked"] = False

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UPSTREAM_EFFECTIVE_NEW_ENTRIES_BLOCKED"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_upstream_authorization_true() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    record["upstream_records"]["runtime_safety_heartbeat"]["order_send_authorized"] = True

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UPSTREAM_TOP_LEVEL_UNSAFE_AUTHORIZATION"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_fail_closed_record_under_require_pass() -> None:
    fake = FakeMT5(account_info=account(margin_free=9_000.0))
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RECORD_VERDICT_NOT_PASS"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_malformed_upstream_record() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    record["upstream_records"]["runtime_safety_heartbeat"] = "malformed"

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UPSTREAM_RECORD_OBJECT"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_pass_record_with_embedded_violation() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    record = copy.deepcopy(record)
    record["violations"] = [{"code": "SHOULD_NOT_BE_IN_PASS_RECORD"}]

    verification = verify_h024_runtime_safety_aggregate_supervisor_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS"
        for violation in verification["verification_violations"]
    )