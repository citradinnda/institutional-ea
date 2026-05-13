from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.build_h024_standard_demo_existing_path_map_jsonl import (
    CORE_SOURCE_COMPONENTS,
    DEFAULT_OUTPUT_JSONL,
    DEFAULT_OUTPUT_TEXT,
    EXPECTED_ALLOWED_MODEL_SYMBOLS,
    EXPECTED_ALLOWED_RUNTIME_SYMBOLS,
    FORBIDDEN_SELF_SNIPPETS,
    SAFETY_SOURCE_COMPONENTS,
    STANDARD_DEMO_DOC_COMPONENTS,
    TEST_COMPONENTS,
    build_packet,
)


SCRIPT_PATH = Path("scripts/build_h024_standard_demo_existing_path_map_jsonl.py")


def test_existing_path_map_identifies_real_h024_standard_demo_chain() -> None:
    packet = build_packet(Path("."))

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == "H024_STANDARD_DEMO_EXISTING_PATH_MAP_ACCEPTED"
    assert packet["existing_path_map_state"] == "REAL_H024_STANDARD_DEMO_PATH_IDENTIFIED"
    assert packet["ready_for_existing_path_replay"] is True
    assert packet["ready_for_demo_order_check_gate"] is False
    assert packet["next_target"] == "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY"
    assert packet["standalone_scaffold_rejected"] is True
    assert packet["strategy_hypothesis_id_allocated"] is False
    assert packet["allowed_model_symbols"] == ["USDJPY", "XAUUSD"]
    assert packet["allowed_runtime_symbols"] == ["USDJPYm", "XAUUSDm"]


def test_path_map_preserves_no_broker_mutation_authorization() -> None:
    packet = build_packet(Path("."))

    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["entry_authorized"] is False
    assert packet["close_all_authorized"] is False
    assert packet["live_money_authorized"] is False
    assert packet["order_check_authorized"] is False
    assert packet["order_send_authorized"] is False
    assert packet["symbol_select_authorized"] is False
    assert packet["executable_trade_request_authorized"] is False
    assert packet["executable_trade_request_constructed"] is False
    assert packet["demo_order_check_gate_requires_new_explicit_operator_approval"] is True
    assert packet["demo_order_send_gate_requires_separate_future_operator_approval"] is True


def test_all_declared_core_safety_docs_and_tests_exist() -> None:
    for group in [
        CORE_SOURCE_COMPONENTS,
        SAFETY_SOURCE_COMPONENTS,
        STANDARD_DEMO_DOC_COMPONENTS,
        TEST_COMPONENTS,
    ]:
        for spec in group:
            path = Path(spec["path"])
            assert path.exists(), f"Expected existing H024 path component missing: {path}"


def test_core_component_static_markers_exist() -> None:
    packet = build_packet(Path("."))

    for group_name in ["core_components", "safety_components"]:
        for component in packet[group_name]:
            assert component["exists"] is True
            assert component["missing_keywords"] == [], component


def test_shortest_route_uses_existing_h024_modules_before_future_order_capable_gates() -> None:
    packet = build_packet(Path("."))
    route = packet["shortest_existing_route_to_controlled_demo_order_check_order_send"]

    names = [step["name"] for step in route]

    assert names[:7] == [
        "order_intent_simulation",
        "dry_run",
        "dry_run_log_and_verifier",
        "runtime_safety_supervisors",
        "manual_approval_checkpoint",
        "broker_request_draft_envelope",
        "mt5_request_shape_preview",
    ]
    assert names[7:] == [
        "future_demo_order_check_gate",
        "future_one_shot_demo_order_send_gate",
    ]

    for step in route[:7]:
        assert step["mutation"] is False

    for step in route[7:]:
        assert step["mutation"] == "future_only_requires_new_explicit_operator_authorization"


def test_path_map_script_is_read_only_and_contains_no_broker_execution_api() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")

    for snippet in FORBIDDEN_SELF_SNIPPETS:
        assert snippet not in source


def test_cli_writes_jsonl_and_text_outputs(tmp_path: Path) -> None:
    output_jsonl = tmp_path / "path_map.jsonl"
    output_text = tmp_path / "path_map.txt"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--output-jsonl",
            str(output_jsonl),
            "--output-text",
            str(output_text),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    packet = json.loads(output_jsonl.read_text(encoding="utf-8"))
    text = output_text.read_text(encoding="utf-8")

    assert packet["verdict"] == "PASS"
    assert packet["ready_for_existing_path_replay"] is True
    assert packet["ready_for_demo_order_check_gate"] is False
    assert "order_intent_simulation" in text
    assert "broker_request_draft_envelope" in text
    assert "future_demo_order_check_gate" in text


def test_fail_closed_when_repo_root_has_missing_required_components(tmp_path: Path) -> None:
    packet = build_packet(tmp_path)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["existing_path_map_state"] == "INCOMPLETE"
    assert packet["ready_for_existing_path_replay"] is False
    assert packet["ready_for_demo_order_check_gate"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["violations"]


def test_expected_symbols_match_research_carry_forward() -> None:
    assert EXPECTED_ALLOWED_MODEL_SYMBOLS == ["USDJPY", "XAUUSD"]
    assert EXPECTED_ALLOWED_RUNTIME_SYMBOLS == ["USDJPYm", "XAUUSDm"]
