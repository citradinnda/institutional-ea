from __future__ import annotations

import ast
from pathlib import Path

from quantcore.execution.h024_safety_supervisor_spec import (
    MODEL_SYMBOLS,
    REQUIRED_GLOBAL_GUARDS,
    REQUIRED_SYMBOL_CIRCUIT_BREAKERS,
    RUNTIME_SYMBOLS,
    build_h024_safety_supervisor_spec_record,
    verify_h024_safety_supervisor_spec_records,
)


def test_safety_supervisor_spec_passes_as_read_only_spec():
    record = build_h024_safety_supervisor_spec_record(generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["read_only"] is True
    assert record["specification_only"] is True
    assert record["implementation_status"] == "specified_not_runtime_enforced"
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["entry_authorized"] is False
    assert record["close_modify_authorized"] is False
    assert record["xauusd_order_authorized"] is False
    assert record["usdjpy_order_authorized"] is False
    assert record["trading_loop_authorized"] is False
    assert record["automatic_execution_authorized"] is False


def test_all_required_global_guards_are_defined():
    record = build_h024_safety_supervisor_spec_record()
    guards = record["global_guards"]

    assert set(REQUIRED_GLOBAL_GUARDS).issubset(guards)

    for name in REQUIRED_GLOBAL_GUARDS:
        guard = guards[name]
        assert guard["required_before_trading_loop"] is True
        assert guard["fail_closed_default"] is True
        assert guard["status"] == "specified_not_runtime_enforced"
        assert guard["required_runtime_inputs"]
        assert guard["fail_closed_condition"]
        assert guard["blocks"]
        assert guard["broker_mutation_authorized"] is False
        assert guard["order_check_authorized"] is False
        assert guard["order_send_authorized"] is False
        assert guard["entry_authorized"] is False
        assert guard["close_modify_authorized"] is False
        assert guard["trading_loop_authorized"] is False


def test_symbol_circuit_breakers_exist_for_xauusd_and_usdjpy():
    record = build_h024_safety_supervisor_spec_record()
    circuit_breakers = record["symbol_circuit_breakers"]

    assert tuple(record["model_symbols"]) == MODEL_SYMBOLS
    assert record["runtime_symbols"] == RUNTIME_SYMBOLS
    assert set(circuit_breakers) == {"XAUUSD", "USDJPY"}

    for model_symbol in MODEL_SYMBOLS:
        symbol_block = circuit_breakers[model_symbol]
        assert symbol_block["runtime_symbol"] == RUNTIME_SYMBOLS[model_symbol]
        assert symbol_block["required_before_trading_loop"] is True
        assert symbol_block["broker_mutation_authorized"] is False
        assert symbol_block["order_check_authorized"] is False
        assert symbol_block["order_send_authorized"] is False
        assert symbol_block["entry_authorized"] is False
        assert symbol_block["close_modify_authorized"] is False
        assert symbol_block["trading_loop_authorized"] is False
        assert set(REQUIRED_SYMBOL_CIRCUIT_BREAKERS).issubset(symbol_block["breakers"])

        for breaker_name in REQUIRED_SYMBOL_CIRCUIT_BREAKERS:
            breaker = symbol_block["breakers"][breaker_name]
            assert breaker["model_symbol"] == model_symbol
            assert breaker["runtime_symbol"] == RUNTIME_SYMBOLS[model_symbol]
            assert breaker["required_before_trading_loop"] is True
            assert breaker["fail_closed_default"] is True
            assert breaker["required_runtime_inputs"]
            assert breaker["fail_closed_condition"]
            assert breaker["blocks"]
            assert breaker["broker_mutation_authorized"] is False
            assert breaker["order_check_authorized"] is False
            assert breaker["order_send_authorized"] is False
            assert breaker["entry_authorized"] is False
            assert breaker["close_modify_authorized"] is False
            assert breaker["trading_loop_authorized"] is False


def test_verifier_accepts_clean_spec_when_require_pass():
    record = build_h024_safety_supervisor_spec_record()

    summary = verify_h024_safety_supervisor_spec_records([record], require_pass=True)

    assert summary["verdict"] == "PASS"
    assert summary["violations"] == []
    assert summary["record_count"] == 1
    assert summary["global_guard_count"] == len(REQUIRED_GLOBAL_GUARDS)
    assert summary["symbol_count"] == 2


def test_verifier_rejects_broker_mutation_authorization():
    record = build_h024_safety_supervisor_spec_record()
    record["broker_mutation_authorized"] = True

    summary = verify_h024_safety_supervisor_spec_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "h024_safety_supervisor_spec.broker_mutation_authorized_must_be_false" in summary["violations"]


def test_verifier_rejects_nested_order_send_authorization():
    record = build_h024_safety_supervisor_spec_record()
    record["global_guards"]["global_no_new_entry_switch"]["order_send_authorized"] = True

    summary = verify_h024_safety_supervisor_spec_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "global_no_new_entry_switch.order_send_authorized_must_be_false" in summary["violations"]


def test_verifier_rejects_nested_symbol_entry_authorization():
    record = build_h024_safety_supervisor_spec_record()
    breaker = record["symbol_circuit_breakers"]["USDJPY"]["breakers"]["symbol_no_new_entry_breaker"]
    breaker["entry_authorized"] = True

    summary = verify_h024_safety_supervisor_spec_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "symbol_no_new_entry_breaker.entry_authorized_must_be_false" in summary["violations"]


def test_verifier_rejects_missing_global_guard():
    record = build_h024_safety_supervisor_spec_record()
    del record["global_guards"]["daily_loss_lockout"]

    summary = verify_h024_safety_supervisor_spec_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "missing_global_guard_daily_loss_lockout" in summary["violations"]


def test_verifier_rejects_missing_symbol_breaker():
    record = build_h024_safety_supervisor_spec_record()
    del record["symbol_circuit_breakers"]["XAUUSD"]["breakers"]["symbol_spread_shock_breaker"]

    summary = verify_h024_safety_supervisor_spec_records([record], require_pass=True)

    assert summary["verdict"] == "FAIL"
    assert "missing_XAUUSD_symbol_spread_shock_breaker" in summary["violations"]


def test_module_has_no_metatrader5_or_broker_mutation_calls():
    source_path = Path("quantcore/execution/h024_safety_supervisor_spec.py")
    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    imported_names = set()
    called_attributes = set()
    called_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_names.add(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                called_attributes.add(node.func.attr)
            elif isinstance(node.func, ast.Name):
                called_names.add(node.func.id)

    assert "MetaTrader5" not in imported_names
    assert "mt5" not in imported_names
    assert "order_check" not in called_attributes
    assert "order_send" not in called_attributes
    assert "positions_get" not in called_attributes
    assert "orders_get" not in called_attributes
    assert "initialize" not in called_attributes
    assert "shutdown" not in called_attributes
    assert "copy_rates_from_pos" not in called_attributes
    assert "symbol_info_tick" not in called_attributes
    assert "account_info" not in called_attributes
    assert "subprocess" not in imported_names
    assert "system" not in called_names