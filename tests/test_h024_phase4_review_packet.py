from __future__ import annotations

import json
from pathlib import Path

import pytest

from quantcore.execution.h024_phase4_review_packet import (
    Phase4ReviewPacketError,
    Phase4ReviewPacketPaths,
    build_phase4_review_packet,
    verify_phase4_review_packet_jsonl,
    write_jsonl_record,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def _paths(tmp_path: Path) -> Phase4ReviewPacketPaths:
    return Phase4ReviewPacketPaths.standard_demo_reports(tmp_path / "reports")


def _seed_valid_artifacts(paths: Phase4ReviewPacketPaths) -> None:
    common_false = {
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "execution_approved": False,
        "server": "Exness-MT5Trial6",
    }
    _write_json(
        paths.phase4_readiness_review_jsonl,
        {
            "schema": "h024_phase4_readiness_review_v1",
            "kind": "PHASE4_READINESS_REVIEW_REQUEST_REVIEW_ONLY",
            "review_request_status": "READY_FOR_PHASE4_REVIEW_REQUEST",
            **common_false,
        },
    )
    _write_json(
        paths.execution_safety_controls_design_jsonl,
        {
            "schema": "h024_execution_safety_controls_design_v1",
            "kind": "EXECUTION_SAFETY_CONTROLS_DESIGN_REVIEW_ONLY",
            "design_status": "SAFETY_CONTROLS_DESIGN_SPEC_ONLY_NOT_IMPLEMENTED",
            **common_false,
        },
    )
    _write_json(
        paths.default_blocked_safety_preflight_jsonl,
        {
            "schema": "h024_execution_safety_controls_preflight_v1",
            "kind": "EXECUTION_SAFETY_CONTROLS_PREFLIGHT_REVIEW_ONLY",
            "control_status": "SAFETY_CONTROLS_BLOCKED_REVIEW_ONLY",
            "control_decision": "BLOCK",
            "blocked_reasons": ["missing_kill_switch_state"],
            **common_false,
        },
    )
    _write_json(
        paths.operator_control_state_snapshot_json,
        {
            "schema": "h024_operator_control_state_snapshot_v1",
            "kind": "OPERATOR_CONTROL_STATE_SNAPSHOT_REVIEW_ONLY",
            "snapshot_status": "ALLOW_STATE_REVIEW_ONLY_NOT_EXECUTION_APPROVAL",
            "stable_intent_id": "af20bcb4a54f6b51aafadeb15a65320bf9c448dbae20cf33066da3cd5adb4363",
            **common_false,
        },
    )
    _write_json(
        paths.allow_state_safety_preflight_jsonl,
        {
            "schema": "h024_execution_safety_controls_preflight_v1",
            "kind": "EXECUTION_SAFETY_CONTROLS_PREFLIGHT_REVIEW_ONLY",
            "control_status": "SAFETY_CONTROLS_PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL",
            "control_decision": "PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL",
            "blocked_reasons": [],
            **common_false,
        },
    )


def test_build_phase4_review_packet_from_verified_artifacts(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _seed_valid_artifacts(paths)

    packet = build_phase4_review_packet(
        paths,
        created_utc="2026-05-11T00:00:00Z",
        upstream_verifier_results=[{"command": ["python", "verifier.py"], "returncode": 0, "passed": True}],
    )

    assert packet["schema"] == "h024_phase4_review_packet_v1"
    assert packet["kind"] == "PHASE4_REVIEW_PACKET_REVIEW_ONLY"
    assert packet["status"] == "READY_FOR_HUMAN_PHASE4_REVIEW"
    assert packet["human_review_required"] is True
    assert packet["phase4_approved"] is False
    assert packet["demo_order_placement_approved"] is False
    assert packet["live_order_placement_approved"] is False
    assert packet["execution_adapter_approved"] is False
    assert packet["execution_approved"] is False
    assert packet["gate_checks"]["default_missing_kill_switch_blocks"] is True
    assert packet["gate_checks"]["explicit_allow_state_preflight_passes_review_only"] is True
    assert packet["stable_intent_id"].startswith("af20bcb4")
    assert len(packet["required_artifacts"]) == 5


def test_build_rejects_default_preflight_that_does_not_block(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _seed_valid_artifacts(paths)
    _write_json(
        paths.default_blocked_safety_preflight_jsonl,
        {
            "control_decision": "PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL",
            "blocked_reasons": [],
            "execution_approved": False,
            "phase4_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "server": "Exness-MT5Trial6",
        },
    )

    with pytest.raises(Phase4ReviewPacketError, match="default_blocked_safety_preflight"):
        build_phase4_review_packet(paths)


def test_build_rejects_allow_state_preflight_with_blocked_reason(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _seed_valid_artifacts(paths)
    _write_json(
        paths.allow_state_safety_preflight_jsonl,
        {
            "control_decision": "PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL",
            "blocked_reasons": ["duplicate_intent_id"],
            "execution_approved": False,
            "phase4_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "server": "Exness-MT5Trial6",
        },
    )

    with pytest.raises(Phase4ReviewPacketError, match="expected no blocked reasons"):
        build_phase4_review_packet(paths)


def test_build_rejects_true_approval_flag_anywhere(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _seed_valid_artifacts(paths)
    _write_json(
        paths.phase4_readiness_review_jsonl,
        {
            "review_request_status": "READY_FOR_PHASE4_REVIEW_REQUEST",
            "phase4_approved": True,
            "execution_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "server": "Exness-MT5Trial6",
        },
    )

    with pytest.raises(Phase4ReviewPacketError, match="approval flag"):
        build_phase4_review_packet(paths)


def test_build_rejects_forbidden_execution_like_field(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _seed_valid_artifacts(paths)
    _write_json(
        paths.execution_safety_controls_design_jsonl,
        {
            "design_status": "SAFETY_CONTROLS_DESIGN_SPEC_ONLY_NOT_IMPLEMENTED",
            "mql_trade_request": {},
            "execution_approved": False,
            "phase4_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "server": "Exness-MT5Trial6",
        },
    )

    with pytest.raises(Phase4ReviewPacketError, match="forbidden execution-like field"):
        build_phase4_review_packet(paths)


def test_verify_packet_jsonl_accepts_single_ready_packet(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _seed_valid_artifacts(paths)
    packet = build_phase4_review_packet(paths, created_utc="2026-05-11T00:00:00Z")
    packet_path = tmp_path / "packet.jsonl"
    write_jsonl_record(packet_path, packet)

    records, violations = verify_phase4_review_packet_jsonl(
        packet_path,
        require_ready=True,
        allowed_demo_server="Exness-MT5Trial6",
    )

    assert len(records) == 1
    assert violations == []


def test_verify_packet_jsonl_rejects_execution_approval(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    _seed_valid_artifacts(paths)
    packet = build_phase4_review_packet(paths, created_utc="2026-05-11T00:00:00Z")
    packet["execution_approved"] = True
    packet_path = tmp_path / "packet.jsonl"
    write_jsonl_record(packet_path, packet)

    _, violations = verify_phase4_review_packet_jsonl(packet_path, require_ready=True)

    assert any("execution_approved" in violation for violation in violations)