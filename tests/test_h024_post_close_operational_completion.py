from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.build_h024_post_close_operational_completion_jsonl import (
    EXPECTED_STATE,
    build_packet,
)


SCRIPT_PATH = Path("scripts/build_h024_post_close_operational_completion_jsonl.py")


def write_jsonl(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def state_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "verdict": "PASS",
        "canary_absence_classification": "INTENTIONALLY_CLOSED_BY_H025",
        "dashboard_wording": EXPECTED_STATE,
        "readiness_wording": EXPECTED_STATE,
        "exact_ticket_open": False,
        "h024_position_count": 0,
        "h024_order_count": 0,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
    }
    payload.update(overrides)
    return payload


def adapter_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "verdict": "PASS",
        "dashboard_state": EXPECTED_STATE,
        "readiness_state": EXPECTED_STATE,
        "h024_dashboard_compatible": True,
        "h024_readiness_compatible": True,
        "legacy_open_canary_required": False,
        "post_close_no_open_canary_accepted": True,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
    }
    payload.update(overrides)
    return payload


def write_inputs(tmp_path: Path, state: dict[str, object], adapter: dict[str, object]) -> tuple[Path, Path]:
    state_path = tmp_path / "state.jsonl"
    adapter_path = tmp_path / "adapter.jsonl"
    write_jsonl(state_path, state)
    write_jsonl(adapter_path, adapter)
    return state_path, adapter_path


def test_passes_when_state_and_adapter_confirm_h024_post_close_completion(tmp_path: Path) -> None:
    paths = write_inputs(tmp_path, state_payload(), adapter_payload())

    packet = build_packet(*paths)

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == "H024_POST_CLOSE_OPERATIONAL_COMPLETION_ACCEPTED"
    assert packet["post_close_operational_state"] == EXPECTED_STATE
    assert packet["dashboard_state"] == EXPECTED_STATE
    assert packet["readiness_state"] == EXPECTED_STATE
    assert packet["legacy_open_canary_required"] is False
    assert packet["post_close_no_open_canary_accepted"] is True
    assert packet["demo_automation_readiness_transition_allowed"] is True
    assert packet["demo_automation_next_target"] == "DEMO_AUTOMATION_READINESS_BRIDGE"
    assert packet["exact_ticket_open"] is False
    assert packet["h024_position_count"] == 0
    assert packet["h024_order_count"] == 0
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["violations"] == []
    assert "define one-shot demo entry authorization scope" in packet["demo_automation_blockers_remaining"]


@pytest.mark.parametrize(
    ("source", "key", "value", "expected_code"),
    [
        ("state", "verdict", "FAIL_CLOSED", "state_verdict_not_pass"),
        ("state", "canary_absence_classification", "UNEXPECTED", "state_absence_not_intentionally_closed"),
        ("state", "dashboard_wording", "OLD", "state_dashboard_wording_unexpected"),
        ("state", "readiness_wording", "OLD", "state_readiness_wording_unexpected"),
        ("state", "exact_ticket_open", True, "state_exact_ticket_open_not_false"),
        ("state", "h024_position_count", 1, "state_h024_position_count_not_zero"),
        ("state", "h024_order_count", 1, "state_h024_order_count_not_zero"),
        ("adapter", "verdict", "FAIL_CLOSED", "adapter_verdict_not_pass"),
        ("adapter", "dashboard_state", "OLD", "adapter_dashboard_state_unexpected"),
        ("adapter", "readiness_state", "OLD", "adapter_readiness_state_unexpected"),
        ("adapter", "h024_dashboard_compatible", False, "adapter_dashboard_not_compatible"),
        ("adapter", "h024_readiness_compatible", False, "adapter_readiness_not_compatible"),
        ("adapter", "legacy_open_canary_required", True, "adapter_legacy_open_canary_required_not_false"),
        ("adapter", "post_close_no_open_canary_accepted", False, "adapter_post_close_not_accepted"),
    ],
)
def test_fails_closed_when_required_completion_evidence_is_not_safe(
    tmp_path: Path,
    source: str,
    key: str,
    value: object,
    expected_code: str,
) -> None:
    state = state_payload()
    adapter = adapter_payload()

    if source == "state":
        state[key] = value
    elif source == "adapter":
        adapter[key] = value
    else:
        raise AssertionError(source)

    paths = write_inputs(tmp_path, state, adapter)

    packet = build_packet(*paths)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["post_close_operational_state"] == "UNVERIFIED"
    assert packet["demo_automation_readiness_transition_allowed"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == expected_code for v in packet["violations"])


@pytest.mark.parametrize("label", ["state", "adapter"])
def test_fails_closed_when_required_input_is_missing(tmp_path: Path, label: str) -> None:
    state_path, adapter_path = write_inputs(tmp_path, state_payload(), adapter_payload())

    if label == "state":
        state_path.unlink()
    elif label == "adapter":
        adapter_path.unlink()

    packet = build_packet(state_path, adapter_path)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["demo_automation_readiness_transition_allowed"] is False
    assert any(v["code"] == f"{label}_report_unreadable" for v in packet["violations"])


@pytest.mark.parametrize("label", ["state", "adapter"])
def test_fails_closed_when_any_input_authorizes_trading_or_broker_mutation(tmp_path: Path, label: str) -> None:
    state = state_payload()
    adapter = adapter_payload()

    target = {"state": state, "adapter": adapter}[label]
    target["trading_authorized"] = True
    target["broker_mutation_authorized"] = True

    paths = write_inputs(tmp_path, state, adapter)

    packet = build_packet(*paths)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any(v["code"] == f"{label}_trading_authorized_not_false" for v in packet["violations"])
    assert any(v["code"] == f"{label}_broker_mutation_authorized_not_false" for v in packet["violations"])


def test_cli_writes_jsonl_and_text_outputs(tmp_path: Path) -> None:
    paths = write_inputs(tmp_path, state_payload(), adapter_payload())
    output_jsonl = tmp_path / "completion.jsonl"
    output_text = tmp_path / "completion.txt"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--state-report",
            str(paths[0]),
            "--adapter-report",
            str(paths[1]),
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
    assert packet["post_close_operational_state"] == EXPECTED_STATE
    assert packet["demo_automation_readiness_transition_allowed"] is True
    assert EXPECTED_STATE in text
    assert "Demo automation readiness transition allowed: True" in text
    assert "Broker mutation authorized: False" in text


def test_script_is_read_only_and_contains_no_broker_execution_api() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")

    forbidden_snippets = [
        "import MetaTrader5",
        "from MetaTrader5",
        "mt5.",
        "order_send(",
        "order_check(",
        "symbol_select(",
        "TRADE_ACTION",
        "ORDER_TYPE_BUY",
        "ORDER_TYPE_SELL",
    ]

    for snippet in forbidden_snippets:
        assert snippet not in source
