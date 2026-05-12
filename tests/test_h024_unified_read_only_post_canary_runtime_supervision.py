from __future__ import annotations

import copy
import time
from types import SimpleNamespace

from quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor import (
    CANARY_POSITION_TYPE,
    CANARY_RUNTIME_SYMBOL,
    CANARY_TICKET_IDENTIFIER,
    CANARY_VOLUME,
    H024_MAGIC,
)
from quantcore.execution.h024_runtime_safety_aggregate_supervisor import (
    collect_h024_runtime_safety_aggregate_supervisor,
)
from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
)
from quantcore.execution.h024_unified_read_only_post_canary_runtime_supervision import (
    collect_h024_unified_read_only_post_canary_runtime_supervision,
    verify_h024_unified_read_only_post_canary_runtime_supervision_records,
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


def canary_supervision_record(*, verdict: str = "PASS") -> dict[str, object]:
    return {
        "schema_version": 1,
        "strategy": "H024",
        "packet_type": "H024_ONE_SHOT_DEMO_CANARY_READ_ONLY_SUPERVISION_RUN",
        "verdict": verdict,
        "violations": [] if verdict == "PASS" else [{"code": "SYNTHETIC_CANARY_FAILURE"}],
        "completed_stages": 8 if verdict == "PASS" else 7,
        "total_stages": 8,
        "first_failed_stage": None if verdict == "PASS" else "synthetic_failure",
        "operator_next_action": "read_supervisory_state_and_continue_observation",
        "broker_mutation_authorized": False,
        "trading_loop_authorized": False,
        "canary_identity": {
            "runtime_symbol": CANARY_RUNTIME_SYMBOL,
            "ticket": CANARY_TICKET_IDENTIFIER,
            "identifier": CANARY_TICKET_IDENTIFIER,
            "magic": H024_MAGIC,
            "volume": CANARY_VOLUME,
        },
    }


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
        raise AssertionError("symbol_select must never be called by unified supervision")

    def order_check(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_check must never be called by unified supervision")

    def order_send(self, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("order_send must never be called by unified supervision")


def test_unified_packet_passes_with_canary_supervision_and_runtime_aggregate() -> None:
    fake = FakeMT5()

    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )

    assert record["verdict"] == "PASS"
    assert record["operator_next_action"] == "READ_ONLY_CONTINUE_CANARY_AND_RUNTIME_SUPERVISION_NO_TRADING_AUTHORIZED"
    assert record["canary_read_only_supervision"]["summary"]["all_records_passed"] is True
    assert record["runtime_safety_aggregate"]["summary"]["verdict"] == "PASS"
    assert record["exact_known_canary"]["state"] == "OBSERVED_EXACT_KNOWN_CANARY"
    assert record["effective_new_entries_blocked"] is True
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        assert record["authorizations"][key] is False
        assert record[key] is False


def test_flat_runtime_inventory_can_pass_if_canary_supervision_passes() -> None:
    fake = FakeMT5(
        account_info=account(balance=10_000.0, equity=10_000.0, profit=0.0, margin=0.0, margin_free=10_000.0, margin_level=0.0),
        positions=[],
    )

    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )

    assert record["verdict"] == "PASS"
    assert record["exact_known_canary"]["state"] in {"OBSERVED_EXACT_KNOWN_CANARY", "NOT_OBSERVED", "NOT_OBSERVED_OR_NOT_EXTRACTED"}


def test_unified_packet_calls_no_mutation_or_execution_methods() -> None:
    fake = FakeMT5()

    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )

    assert record["verdict"] == "PASS"
    assert "symbol_select" not in fake.calls
    assert "order_check" not in fake.calls
    assert "order_send" not in fake.calls


def test_missing_canary_records_fail_closed() -> None:
    fake = FakeMT5()

    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[],
        invoke_canary_runner=False,
    )

    assert record["verdict"] == "FAIL"
    assert record["operator_next_action"] == "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    assert any(check["name"] == "canary_supervision_records_present" and not check["passed"] for check in record["checks"])


def test_failed_canary_supervision_fails_closed() -> None:
    fake = FakeMT5()

    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record(verdict="FAIL")],
        invoke_canary_runner=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "canary_supervision_verdict_pass" and not check["passed"] for check in record["checks"])


def test_failed_runtime_aggregate_fails_closed() -> None:
    fake = FakeMT5(account_info=account(margin_free=9_000.0))

    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "runtime_safety_aggregate_verdict_pass" and not check["passed"] for check in record["checks"])


def test_injected_failed_runtime_aggregate_fails_closed() -> None:
    fake = FakeMT5()
    aggregate = collect_h024_runtime_safety_aggregate_supervisor(mt5_client=fake)
    aggregate = copy.deepcopy(aggregate)
    aggregate["verdict"] = "FAIL"
    aggregate["violations"] = [{"code": "SYNTHETIC_AGGREGATE_FAILURE"}]

    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        canary_supervision_records=[canary_supervision_record()],
        runtime_safety_aggregate_record=aggregate,
        invoke_canary_runner=False,
    )

    assert record["verdict"] == "FAIL"
    assert any(check["name"] == "runtime_safety_aggregate_verdict_pass" and not check["passed"] for check in record["checks"])


def test_verifier_rejects_top_level_authorization_true() -> None:
    fake = FakeMT5()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )
    record["authorizations"]["order_send_authorized"] = True

    verification = verify_h024_unified_read_only_post_canary_runtime_supervision_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNSAFE_AUTHORIZATION_TRUE"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_missing_canary_section() -> None:
    fake = FakeMT5()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )
    del record["canary_read_only_supervision"]

    verification = verify_h024_unified_read_only_post_canary_runtime_supervision_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "CANARY_SUPERVISION_SECTION_MISSING"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_missing_runtime_aggregate_section() -> None:
    fake = FakeMT5()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )
    del record["runtime_safety_aggregate"]

    verification = verify_h024_unified_read_only_post_canary_runtime_supervision_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RUNTIME_AGGREGATE_SECTION_MISSING"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_aggregate_entries_unblocked() -> None:
    fake = FakeMT5()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )
    record["runtime_safety_aggregate"]["record"]["effective_new_entries_blocked"] = False

    verification = verify_h024_unified_read_only_post_canary_runtime_supervision_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RUNTIME_AGGREGATE_DOES_NOT_BLOCK_ENTRIES"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_fail_closed_record_under_require_pass() -> None:
    fake = FakeMT5()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[],
        invoke_canary_runner=False,
    )

    verification = verify_h024_unified_read_only_post_canary_runtime_supervision_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "RECORD_VERDICT_NOT_PASS"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_unexpected_operator_next_action_under_require_pass() -> None:
    fake = FakeMT5()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )
    record["operator_next_action"] = "UNSAFE_DO_SOMETHING_ELSE"

    verification = verify_h024_unified_read_only_post_canary_runtime_supervision_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "UNEXPECTED_OPERATOR_NEXT_ACTION"
        for violation in verification["verification_violations"]
    )


def test_verifier_rejects_pass_record_with_embedded_violation() -> None:
    fake = FakeMT5()
    record = collect_h024_unified_read_only_post_canary_runtime_supervision(
        mt5_client=fake,
        canary_supervision_records=[canary_supervision_record()],
        invoke_canary_runner=False,
    )
    record["violations"] = [{"code": "SHOULD_NOT_BE_IN_PASS_RECORD"}]

    verification = verify_h024_unified_read_only_post_canary_runtime_supervision_records([record], require_pass=True)

    assert verification["verifier_verdict"] == "FAIL"
    assert any(
        violation["code"] == "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS"
        for violation in verification["verification_violations"]
    )