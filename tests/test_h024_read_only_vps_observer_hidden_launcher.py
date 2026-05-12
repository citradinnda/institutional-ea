from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "scripts" / "run_h024_read_only_vps_observer_scheduled_hidden.vbs"
RUNBOOK = ROOT / "docs" / "operations" / "H024_READ_ONLY_VPS_OBSERVER_NO_CONSOLE_LAUNCHER_RUNBOOK.md"

FORBIDDEN = (
    "order_check",
    "order_send",
    "symbol_select",
    "TRADE_ACTION_DEAL",
    "TRADE_ACTION_SLTP",
    "PositionClose",
    "OrderSend",
    "mt5.order",
)


def test_hidden_launcher_exists_and_delegates_to_scheduled_wrapper() -> None:
    text = LAUNCHER.read_text(encoding="ascii")

    assert "run_h024_read_only_vps_observer_scheduled.ps1" in text
    assert "shell.Run(command, 0, True)" in text
    assert "WScript.Quit exitCode" in text
    assert "run_h024_read_only_vps_observer_once.ps1" not in text


def test_hidden_launcher_contains_no_trading_or_broker_mutation_terms() -> None:
    text = LAUNCHER.read_text(encoding="ascii")
    lowered = text.lower()

    for forbidden in FORBIDDEN:
        assert forbidden.lower() not in lowered


def test_hidden_launcher_runbook_documents_non_authorizing_boundary() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")

    assert "no `order_check`" in text
    assert "no `order_send`" in text
    assert "no `symbol_select`" in text
    assert "no broker mutation" in text
    assert "does not change broker safety" in text
    assert "black_swan:UPSTREAM_NOT_PASS" in text
