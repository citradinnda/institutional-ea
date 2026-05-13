from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_h024_standard_demo_order_check_gate_design_jsonl.py"
PATH_MAP_BUILDER = ROOT / "scripts" / "build_h024_standard_demo_existing_path_map_jsonl.py"
REPLAY_BUILDER = ROOT / "scripts" / "build_h024_standard_demo_existing_path_replay_jsonl.py"
REPLAY_REPORT = ROOT / "reports" / "h024_standard_demo_existing_path_replay.jsonl"
DESIGN_JSONL = ROOT / "reports" / "h024_standard_demo_order_check_gate_design.jsonl"
DESIGN_TXT = ROOT / "reports" / "h024_standard_demo_order_check_gate_design.txt"


def _load_module():
    spec = importlib.util.spec_from_file_location("h024_order_check_gate_design", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _ensure_replay_report() -> None:
    assert PATH_MAP_BUILDER.exists(), "path-map builder must exist"
    assert REPLAY_BUILDER.exists(), "replay builder must exist"

    subprocess.run(
        [sys.executable, str(PATH_MAP_BUILDER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    subprocess.run(
        [sys.executable, str(REPLAY_BUILDER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert REPLAY_REPORT.exists()


def _latest_jsonl(path: Path) -> dict:
    latest = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = json.loads(line)
    assert latest is not None
    return latest


def test_order_check_gate_design_passes_after_existing_path_replay() -> None:
    _ensure_replay_report()
    module = _load_module()

    packet = module.build_order_check_gate_design_packet()

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == "H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_ACCEPTED"
    assert packet["order_check_gate_design_state"] == "READ_ONLY_GATE_CONTRACT_DEFINED"
    assert packet["existing_path_replay_verdict"] == "PASS"
    assert packet["ready_for_order_check_gate_design"] is True
    assert packet["ready_for_order_check_gate_operator_authorization_packet_design"] is True
    assert packet["next_target"] == "H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN"
    assert packet["violation_count"] == 0


def test_order_check_gate_design_does_not_authorize_broker_mutation_or_invocation() -> None:
    _ensure_replay_report()
    module = _load_module()

    packet = module.build_order_check_gate_design_packet()

    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["order_check_authorized"] is False
    assert packet["order_send_authorized"] is False
    assert packet["symbol_select_authorized"] is False
    assert packet["executable_trade_request_constructed"] is False
    assert packet["new_entry_authorized"] is False
    assert packet["close_modify_authorized"] is False
    assert packet["live_money_supported"] is False
    assert packet["read_only_design_only"] is True
    assert packet["ready_for_demo_order_check_gate"] is False
    assert packet["ready_for_demo_order_check_gate_implementation"] is False
    assert packet["ready_for_demo_order_check_invocation"] is False


def test_future_gate_schema_requires_exact_operator_authorization_scope() -> None:
    _ensure_replay_report()
    module = _load_module()

    packet = module.build_order_check_gate_design_packet()
    schema = packet["future_gate_schema"]

    assert schema["required_operator_authorization_scope"] == "H024_STANDARD_DEMO_ORDER_CHECK_GATE_ONLY"
    assert "operator_authorization_packet" in schema["required_inputs"]
    assert "operator_authorization_id" in schema["required_inputs"]
    assert "authorization_scope" in schema["required_inputs"]
    assert "expired_operator_authorization" in schema["fail_closed_conditions"]
    assert "authorization_scope_not_exactly_h024_standard_demo_order_check_gate_only" in schema["fail_closed_conditions"]


def test_future_gate_schema_preserves_symbol_and_risk_constraints() -> None:
    _ensure_replay_report()
    module = _load_module()

    packet = module.build_order_check_gate_design_packet()
    schema = packet["future_gate_schema"]

    assert schema["allowed_symbols"] == ["USDJPYm", "XAUUSDm"]
    assert schema["banned_symbols"] == ["EURUSDm", "GBPUSDm", "US500m"]
    assert schema["max_risk_per_trade_pct"] == 0.5
    assert schema["max_portfolio_heat_pct"] == 1.0
    assert "symbol_not_in_allowed_demo_symbols" in schema["fail_closed_conditions"]
    assert "symbol_in_banned_symbols" in schema["fail_closed_conditions"]
    assert "risk_or_heat_limit_exceeded" in schema["fail_closed_conditions"]


def test_order_check_gate_design_fails_closed_when_replay_report_missing(tmp_path: Path) -> None:
    module = _load_module()

    packet = module.build_order_check_gate_design_packet(
        replay_report=tmp_path / "missing_replay.jsonl",
    )

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["operator_state"] == "FAIL_CLOSED_H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_UNVERIFIED"
    assert packet["ready_for_order_check_gate_design"] is False
    assert packet["ready_for_demo_order_check_gate"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == "existing_path_replay_report_missing" for v in packet["violations"])


def test_order_check_gate_design_fails_closed_when_replay_report_is_not_pass(tmp_path: Path) -> None:
    module = _load_module()

    bad_replay = tmp_path / "bad_replay.jsonl"
    bad_replay.write_text(
        json.dumps(
            {
                "verdict": "FAIL_CLOSED",
                "stage": "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY",
                "operator_state": "FAIL_CLOSED_TEST",
                "existing_path_replay_state": "BLOCKED",
                "ready_for_existing_path_replay": False,
                "ready_for_demo_order_check_gate": False,
                "ready_for_demo_order_check_gate_design": False,
                "trading_authorized": False,
                "broker_mutation_authorized": False,
                "order_check_authorized": False,
                "order_send_authorized": False,
                "symbol_select_authorized": False,
                "executable_trade_request_constructed": False,
                "new_entry_authorized": False,
                "close_modify_authorized": False,
                "read_only_replay_only": True,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    packet = module.build_order_check_gate_design_packet(replay_report=bad_replay)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["existing_path_replay_verdict"] == "FAIL_CLOSED"
    assert any(v["code"] == "existing_path_replay_verdict_unexpected" for v in packet["violations"])


def test_order_check_gate_design_report_files_are_written() -> None:
    _ensure_replay_report()

    completed = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert DESIGN_JSONL.exists()
    assert DESIGN_TXT.exists()

    latest = _latest_jsonl(DESIGN_JSONL)
    assert latest["verdict"] == "PASS"
    assert latest["stage"] == "H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN"
    assert latest["order_check_authorized"] is False
    assert latest["broker_mutation_authorized"] is False
    assert "H024 standard-demo order-check gate design summary" in DESIGN_TXT.read_text(encoding="utf-8")


def test_order_check_gate_design_source_contains_no_broker_mutation_invocation() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")

    forbidden_tokens = [
        "mt5." + "order_check",
        "mt5." + "order_send",
        "mt5." + "symbol_select",
        "order_" + "check(",
        "order_" + "send(",
        "symbol_" + "select(",
        "Meta" + "Trader5",
    ]

    for token in forbidden_tokens:
        assert token not in source
