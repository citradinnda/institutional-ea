from pathlib import Path
from types import SimpleNamespace

import pytest

from quantcore.execution.h024_one_shot_demo_canary import (
    ACKNOWLEDGEMENT_TEXT,
    CANARY_COMMENT,
    CanaryExecutionRefusal,
    OneShotDemoCanaryConfig,
    execute_one_shot_demo_canary,
    validate_config,
    validate_final_audit_packet,
)


class FakeTerminal:
    TRADE_ACTION_DEAL = 1
    ORDER_TYPE_BUY = 2
    ORDER_TYPE_SELL = 3
    ORDER_TIME_GTC = 4
    ORDER_FILLING_IOC = 5
    TRADE_RETCODE_DONE = 10009
    ACCOUNT_TRADE_MODE_DEMO = 0

    def __init__(self):
        self.sent_requests = []
        self.checked_requests = []
        self.server = "Exness-MT5Trial6"
        self.currency = "USD"
        self.trade_mode = self.ACCOUNT_TRADE_MODE_DEMO
        self.positions = []
        self.orders = []
        self.visible = True
        self.check_retcode = self.TRADE_RETCODE_DONE
        self.send_retcode = self.TRADE_RETCODE_DONE

    def account_info(self):
        return SimpleNamespace(server=self.server, currency=self.currency, trade_mode=self.trade_mode)

    def symbol_info(self, symbol):
        return SimpleNamespace(visible=self.visible, volume_min=0.01, volume_max=200.0, volume_step=0.01)

    def symbol_info_tick(self, symbol):
        return SimpleNamespace(bid=3000.0, ask=3000.5)

    def positions_get(self, symbol=None):
        return self.positions

    def orders_get(self, symbol=None):
        return self.orders

    def order_check(self, request):
        self.checked_requests.append(request)
        return SimpleNamespace(retcode=self.check_retcode, comment="checked")

    def order_send(self, request):
        self.sent_requests.append(request)
        return SimpleNamespace(retcode=self.send_retcode, order=123456, comment="sent")


def final_audit_packet():
    return {
        "schema_version": "h024_final_pre_dispatch_audit_packet_v1",
        "kind": "h024_final_pre_dispatch_audit_packet",
        "decision": "COMPLETE_FINAL_INERT_PRE_DISPATCH_AUDIT_FOR_ONE_DEMO_CANARY_NO_DISPATCH",
        "verdict": "PASS",
        "pre_dispatch_audit_passed": True,
        "allowed_demo_server": "Exness-MT5Trial6",
        "expected_runtime_symbol": "XAUUSDm",
        "max_lot_cap": 0.01,
        "authority": {
            "one_shot_execution_capable_demo_path_implementation_allowed": True,
            "max_approved_canary_orders": 1,
            "live_order_placement_approved": False,
        },
        "verified_controls": {
            "allowed_demo_server_lock": "Exness-MT5Trial6",
            "account_currency_lock": "USD",
            "account_context_lock": "standard_demo_only",
            "runtime_symbol_lock": "XAUUSDm",
            "kill_switch_allow_state_required": True,
            "idempotency_ledger_required": True,
            "single_canary_order_limit": 1,
            "max_lot_cap": 0.01,
            "pre_dispatch_final_audit_required": True,
            "post_order_audit_required_if_later_approved": True,
            "live_order_forbidden": True,
        },
    }


def test_config_blocks_send_without_exact_acknowledgement():
    config = OneShotDemoCanaryConfig(send=True, acknowledgement="wrong")
    assert "exact_acknowledgement_required_for_send" in validate_config(config)


def test_final_audit_packet_accepts_verified_controls():
    config = OneShotDemoCanaryConfig()
    assert validate_final_audit_packet(final_audit_packet(), config) == []


def test_dry_run_builds_request_without_order_check_or_send(tmp_path: Path):
    terminal = FakeTerminal()
    config = OneShotDemoCanaryConfig(send=False)
    result = execute_one_shot_demo_canary(
        terminal=terminal,
        final_audit_packet=final_audit_packet(),
        ledger_path=tmp_path / "ledger.jsonl",
        config=config,
    )

    assert result["attempt_stage"] == "request_built_dry_run_no_send"
    assert result["request"]["symbol"] == "XAUUSDm"
    assert result["request"]["volume"] == 0.01
    assert result["request"]["comment"] == CANARY_COMMENT
    assert result["request"]["type"] == terminal.ORDER_TYPE_SELL
    assert result["request"]["price"] == 3000.0
    assert result["request"]["sl"] == pytest.approx(3089.027)
    assert terminal.checked_requests == []
    assert terminal.sent_requests == []


def test_send_requires_demo_server_and_blocks_wrong_server(tmp_path: Path):
    terminal = FakeTerminal()
    terminal.server = "Some-Live-Server"
    config = OneShotDemoCanaryConfig(send=True, acknowledgement=ACKNOWLEDGEMENT_TEXT)

    with pytest.raises(CanaryExecutionRefusal, match="terminal_server_mismatch"):
        execute_one_shot_demo_canary(
            terminal=terminal,
            final_audit_packet=final_audit_packet(),
            ledger_path=tmp_path / "ledger.jsonl",
            config=config,
        )


def test_send_writes_ledger_and_blocks_second_attempt(tmp_path: Path):
    terminal = FakeTerminal()
    ledger = tmp_path / "ledger.jsonl"
    config = OneShotDemoCanaryConfig(send=True, acknowledgement=ACKNOWLEDGEMENT_TEXT)

    result = execute_one_shot_demo_canary(
        terminal=terminal,
        final_audit_packet=final_audit_packet(),
        ledger_path=ledger,
        config=config,
    )

    assert result["attempt_stage"] == "send_succeeded"
    assert len(terminal.checked_requests) == 1
    assert len(terminal.sent_requests) == 1
    assert ledger.exists()

    with pytest.raises(CanaryExecutionRefusal, match="idempotency_ledger_already_contains_prior_canary_attempt"):
        execute_one_shot_demo_canary(
            terminal=terminal,
            final_audit_packet=final_audit_packet(),
            ledger_path=ledger,
            config=config,
        )


def test_existing_symbol_position_blocks_canary(tmp_path: Path):
    terminal = FakeTerminal()
    terminal.positions = [SimpleNamespace(ticket=1)]
    config = OneShotDemoCanaryConfig(send=True, acknowledgement=ACKNOWLEDGEMENT_TEXT)

    with pytest.raises(CanaryExecutionRefusal, match="existing_symbol_position_blocks_one_shot_canary"):
        execute_one_shot_demo_canary(
            terminal=terminal,
            final_audit_packet=final_audit_packet(),
            ledger_path=tmp_path / "ledger.jsonl",
            config=config,
        )


def test_order_check_failure_records_attempt_and_refuses_send(tmp_path: Path):
    terminal = FakeTerminal()
    terminal.check_retcode = 999
    ledger = tmp_path / "ledger.jsonl"
    config = OneShotDemoCanaryConfig(send=True, acknowledgement=ACKNOWLEDGEMENT_TEXT)

    with pytest.raises(CanaryExecutionRefusal, match="order_check_failed_retcode_999"):
        execute_one_shot_demo_canary(
            terminal=terminal,
            final_audit_packet=final_audit_packet(),
            ledger_path=ledger,
            config=config,
        )

    assert ledger.exists()
    text = ledger.read_text(encoding="utf-8")
    assert "order_check_failed" in text
    assert terminal.sent_requests == []