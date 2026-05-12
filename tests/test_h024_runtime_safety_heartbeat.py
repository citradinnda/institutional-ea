from __future__ import annotations

from types import SimpleNamespace

from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
    collect_h024_runtime_safety_heartbeat,
    verify_h024_runtime_safety_heartbeat_records,
)


_MISSING = object()


class FakeMT5:
    def __init__(
        self,
        *,
        initialize_result: bool = True,
        account_info: object = _MISSING,
        terminal_info: object = _MISSING,
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

    def order_check(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_check must never be called by heartbeat")

    def order_send(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_send must never be called by heartbeat")


def test_successful_heartbeat_passes_but_authorizes_nothing() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == "RUNTIME_HEARTBEAT_OK_BUT_TRADING_NOT_AUTHORIZED"
    assert record["effective_new_entries_blocked"] is True
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        assert record["authorizations"][key] is False
        assert record[key] is False


def test_heartbeat_calls_no_order_check_or_order_send() -> None:
    fake = FakeMT5()

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "PASS"
    assert "order_check" not in fake.calls
    assert "order_send" not in fake.calls


def test_failed_initialize_fails_closed() -> None:
    fake = FakeMT5(initialize_result=False)

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert record["operator_state"] == "FAIL_CLOSED_RUNTIME_HEARTBEAT_BLOCKED"
    assert record["effective_new_entries_blocked"] is True
    assert any(check["name"] == "mt5_initialize_succeeded" and not check["passed"] for check in record["checks"])


def test_missing_account_info_fails_closed() -> None:
    fake = FakeMT5(account_info=None)

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "account_info_available" and not check["passed"] for check in record["checks"])


def test_wrong_server_fails_closed() -> None:
    fake = FakeMT5(account_info=SimpleNamespace(server="Wrong-Server", currency=EXPECTED_ACCOUNT_CURRENCY))

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "account_server_expected" and not check["passed"] for check in record["checks"])


def test_wrong_currency_fails_closed() -> None:
    fake = FakeMT5(account_info=SimpleNamespace(server=EXPECTED_SERVER, currency="IDR"))

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "account_currency_expected" and not check["passed"] for check in record["checks"])


def test_missing_terminal_info_fails_closed() -> None:
    fake = FakeMT5(terminal_info=None)

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "terminal_info_available" and not check["passed"] for check in record["checks"])


def test_disconnected_terminal_fails_closed() -> None:
    fake = FakeMT5(terminal_info=SimpleNamespace(connected=False, trade_allowed=True))

    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "terminal_connected" and not check["passed"] for check in record["checks"])


def test_verifier_requires_all_authorizations_false() -> None:
    fake = FakeMT5()
    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)
    record["authorizations"]["order_send_authorized"] = True

    verification = verify_h024_runtime_safety_heartbeat_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNSAFE_AUTHORIZATION_TRUE"
        for violation in verification["verification_violations"]
    )


def test_verifier_require_pass_rejects_fail_closed_record() -> None:
    fake = FakeMT5(initialize_result=False)
    record = collect_h024_runtime_safety_heartbeat(mt5_client=fake)

    verification = verify_h024_runtime_safety_heartbeat_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RECORD_VERDICT_NOT_PASS"
        for violation in verification["verification_violations"]
    )