from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_h024_standard_demo_existing_path_replay_jsonl.py"
PATH_MAP_BUILDER = ROOT / "scripts" / "build_h024_standard_demo_existing_path_map_jsonl.py"
PATH_MAP_REPORT = ROOT / "reports" / "h024_standard_demo_existing_path_map.jsonl"
REPLAY_JSONL = ROOT / "reports" / "h024_standard_demo_existing_path_replay.jsonl"
REPLAY_TXT = ROOT / "reports" / "h024_standard_demo_existing_path_replay.txt"


def _load_module():
    spec = importlib.util.spec_from_file_location("h024_existing_path_replay", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _ensure_path_map_report() -> None:
    if PATH_MAP_REPORT.exists():
        return
    assert PATH_MAP_BUILDER.exists(), "path-map builder script must exist before replay"
    subprocess.run(
        [sys.executable, str(PATH_MAP_BUILDER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def _latest_jsonl(path: Path) -> dict:
    latest = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = json.loads(line)
    assert latest is not None
    return latest


def test_replay_packet_passes_against_existing_path_map() -> None:
    _ensure_path_map_report()
    module = _load_module()

    packet = module.build_replay_packet(run_existing_tests=False)

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_ACCEPTED"
    assert packet["existing_path_replay_state"] == "REAL_H024_STANDARD_DEMO_PATH_REPLAYED_READ_ONLY"
    assert packet["path_map_verdict"] == "PASS"
    assert packet["next_target"] == "H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN"
    assert packet["ready_for_existing_path_replay"] is True
    assert packet["ready_for_demo_order_check_gate"] is False
    assert packet["ready_for_demo_order_check_gate_design"] is True
    assert packet["violation_count"] == 0


def test_replay_preserves_all_hard_authorization_boundaries_false() -> None:
    _ensure_path_map_report()
    module = _load_module()

    packet = module.build_replay_packet(run_existing_tests=False)

    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert packet["order_check_authorized"] is False
    assert packet["order_send_authorized"] is False
    assert packet["symbol_select_authorized"] is False
    assert packet["executable_trade_request_constructed"] is False
    assert packet["new_entry_authorized"] is False
    assert packet["close_modify_authorized"] is False
    assert packet["live_money_supported"] is False
    assert packet["read_only_replay_only"] is True


def test_replay_identifies_latest_existing_artifact_before_broker_mutation() -> None:
    _ensure_path_map_report()
    module = _load_module()

    packet = module.build_replay_packet(run_existing_tests=False)

    assert (
        packet["latest_existing_artifact_before_broker_mutation"]
        == "docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md"
    )
    assert packet["latest_existing_artifact_before_broker_mutation_exists"] is True


def test_replay_uses_real_h024_path_not_standalone_inert_scaffold() -> None:
    _ensure_path_map_report()
    module = _load_module()

    packet = module.build_replay_packet(run_existing_tests=False)
    joined_path = "\n".join(packet["existing_path_sequence"])

    assert "h024_order_intent_simulation.py" in joined_path
    assert "h024_dry_run.py" in joined_path
    assert "h024_dry_run_log.py" in joined_path
    assert "h024_manual_approval_checkpoint.py" in joined_path
    assert "h024_broker_request_draft_envelope.py" in joined_path
    assert "INERT_DEMO_ENTRY_REQUEST_PREVIEW" not in joined_path
    assert "build_inert_demo_entry_request_preview_jsonl.py" not in joined_path


def test_replay_fails_closed_when_path_map_report_is_missing(tmp_path: Path) -> None:
    module = _load_module()

    packet = module.build_replay_packet(
        path_map_report=tmp_path / "missing_path_map.jsonl",
        run_existing_tests=False,
    )

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["ready_for_existing_path_replay"] is False
    assert packet["ready_for_demo_order_check_gate"] is False
    assert packet["trading_authorized"] is False
    assert packet["broker_mutation_authorized"] is False
    assert any(v["code"] == "path_map_report_missing" for v in packet["violations"])


def test_replay_fails_closed_when_path_map_verdict_is_not_pass(tmp_path: Path) -> None:
    module = _load_module()

    bad_path_map = tmp_path / "bad_path_map.jsonl"
    bad_path_map.write_text(
        json.dumps(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_TEST",
                "existing_path_map_state": "BLOCKED",
                "ready_for_existing_path_replay": False,
                "ready_for_demo_order_check_gate": False,
                "trading_authorized": False,
                "broker_mutation_authorized": False,
                "order_check_authorized": False,
                "order_send_authorized": False,
                "symbol_select_authorized": False,
                "executable_trade_request_constructed": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    packet = module.build_replay_packet(
        path_map_report=bad_path_map,
        run_existing_tests=False,
    )

    assert packet["verdict"] == "FAIL_CLOSED"
    assert packet["path_map_verdict"] == "FAIL_CLOSED"
    assert any(v["code"] == "path_map_verdict_unexpected" for v in packet["violations"])


def test_replay_report_files_are_written() -> None:
    _ensure_path_map_report()

    completed = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert REPLAY_JSONL.exists()
    assert REPLAY_TXT.exists()

    latest = _latest_jsonl(REPLAY_JSONL)
    assert latest["verdict"] == "PASS"
    assert latest["stage"] == "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY"
    assert latest["trading_authorized"] is False
    assert "H024 standard-demo existing path replay summary" in REPLAY_TXT.read_text(encoding="utf-8")


def test_replay_source_contains_no_direct_mt5_broker_mutation_calls() -> None:
    source = SCRIPT_PATH.read_text(encoding="utf-8")

    forbidden_tokens = [
        "mt5.order_check",
        "mt5.order_send",
        "mt5.symbol_select",
        "order_send(",
        "order_check(",
        "symbol_select(",
    ]

    for token in forbidden_tokens:
        assert token not in source
