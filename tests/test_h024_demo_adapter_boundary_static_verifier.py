from __future__ import annotations

import copy

from quantcore.execution.h024_demo_adapter_boundary_static_verifier import (
    DECISION,
    KIND,
    SCHEMA,
    STATUS,
    build_static_verifier_record,
    build_static_verifier_records,
    read_jsonl,
    scan_adapter_boundary_targets,
    verify_static_verifier_records,
    write_jsonl,
)


def test_clean_pure_python_adapter_surface_passes(tmp_path) -> None:
    target = tmp_path / "adapter.py"
    target.write_text(
        "from __future__ import annotations\n"
        "DISPATCH_ATTEMPTED = False\n"
        "BROKER_STATE_MUTATED = False\n",
        encoding="utf-8",
    )

    record = build_static_verifier_record([target], root=tmp_path)

    assert record["schema"] == SCHEMA
    assert record["kind"] == KIND
    assert record["status"] == STATUS
    assert record["decision"] == DECISION
    assert record["verdict"] == "PASS"
    assert record["adapter_boundary_static_verified"] is True
    assert record["prohibited_finding_count"] == 0
    assert verify_static_verifier_records([record], require_pass=True) == []


def test_python_strings_and_comments_do_not_fail_static_boundary(tmp_path) -> None:
    target = tmp_path / "adapter.py"
    target.write_text(
        '"""Refuse OrderSend, OrderCheck, MqlTradeRequest, and MetaTrader5 execution."""\n'
        "# Never call mt5.order_send from this adapter.\n"
        'REFUSAL_REASON = "no broker_request or mt5_request may be constructed"\n'
        "dispatch_attempted = False\n",
        encoding="utf-8",
    )

    record = build_static_verifier_record([target], root=tmp_path)

    assert record["verdict"] == "PASS"
    assert record["prohibited_finding_count"] == 0


def test_detects_metatrader5_import(tmp_path) -> None:
    target = tmp_path / "bad_adapter.py"
    target.write_text("import MetaTrader5 as mt5\n", encoding="utf-8")

    record = build_static_verifier_record([target], root=tmp_path)

    assert record["verdict"] == "FAIL"
    assert record["prohibited_finding_count"] == 1
    assert "metatrader5_import" in record["violations"][0]


def test_detects_metatrader5_from_import(tmp_path) -> None:
    target = tmp_path / "bad_adapter.py"
    target.write_text("from MetaTrader5 import order_send\n", encoding="utf-8")

    record = build_static_verifier_record([target], root=tmp_path)

    assert record["verdict"] == "FAIL"
    assert any("metatrader5_import" in violation for violation in record["violations"])


def test_detects_python_mt5_order_send_call(tmp_path) -> None:
    target = tmp_path / "bad_adapter.py"
    target.write_text("result = mt5.order_send(payload)\n", encoding="utf-8")

    record = build_static_verifier_record([target], root=tmp_path)

    assert record["verdict"] == "FAIL"
    assert any("python_execution_attr_call" in violation for violation in record["violations"])


def test_detects_python_direct_order_send_call(tmp_path) -> None:
    target = tmp_path / "bad_adapter.py"
    target.write_text("result = order_send(payload)\n", encoding="utf-8")

    record = build_static_verifier_record([target], root=tmp_path)

    assert record["verdict"] == "FAIL"
    assert any("python_execution_direct_call" in violation for violation in record["violations"])


def test_detects_python_mt5_session_call(tmp_path) -> None:
    target = tmp_path / "bad_adapter.py"
    target.write_text("ok = mt5.initialize()\n", encoding="utf-8")

    record = build_static_verifier_record([target], root=tmp_path)

    assert record["verdict"] == "FAIL"
    assert any("python_mt5_session_call" in violation for violation in record["violations"])


def test_detects_mql_order_send_symbol(tmp_path) -> None:
    target = tmp_path / "bad_adapter.mq5"
    target.write_text("bool ok = OrderSend(request, result);\n", encoding="utf-8")

    results = scan_adapter_boundary_targets([target], root=tmp_path)

    assert results[0]["findings"]
    assert results[0]["findings"][0]["pattern_id"] == "mql_execution_symbol"


def test_missing_target_fails_closed(tmp_path) -> None:
    record = build_static_verifier_record([tmp_path / "missing.py"], root=tmp_path)

    assert record["verdict"] == "FAIL"
    assert record["prohibited_finding_count"] == 1
    assert "target_missing" in record["violations"][0]


def test_verifier_rejects_any_execution_authority_true(tmp_path) -> None:
    target = tmp_path / "adapter.py"
    target.write_text("SAFE = True\n", encoding="utf-8")
    record = build_static_verifier_record([target], root=tmp_path)
    mutated = copy.deepcopy(record)
    mutated["execution_approved"] = True

    violations = verify_static_verifier_records([mutated], require_pass=True)

    assert "record_0_execution_approved_not_false" in violations


def test_verifier_rejects_constructed_broker_request_flag(tmp_path) -> None:
    target = tmp_path / "adapter.py"
    target.write_text("SAFE = True\n", encoding="utf-8")
    record = build_static_verifier_record([target], root=tmp_path)
    mutated = copy.deepcopy(record)
    mutated["broker_request_constructed"] = True

    violations = verify_static_verifier_records([mutated], require_pass=True)

    assert "record_0_broker_request_constructed_not_false" in violations


def test_file_round_trip(tmp_path) -> None:
    target = tmp_path / "adapter.py"
    output = tmp_path / "static_verifier.jsonl"
    target.write_text("SAFE = True\n", encoding="utf-8")

    records = build_static_verifier_records([target], root=tmp_path)
    write_jsonl(output, records)
    loaded = read_jsonl(output)

    assert loaded == records
    assert verify_static_verifier_records(loaded, require_pass=True) == []


def test_default_targets_include_current_adapter_surface() -> None:
    record = build_static_verifier_record()

    target_paths = {target["path"] for target in record["target_files"]}

    assert "quantcore/execution/h024_demo_execution_adapter_skeleton.py" in target_paths
    assert "quantcore/execution/h024_demo_adapter_intent_refusal_audit.py" in target_paths