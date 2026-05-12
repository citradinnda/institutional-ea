from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from quantcore.execution import h024_exact_ticket_canary_close_modify_operator_decision_v2_preview as mod

NOW = datetime(2026, 5, 12, 1, 0, 0, tzinfo=timezone.utc)


def _write_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")


def _base_record(packet_type: str, *, observed_at: datetime = NOW, extra: dict | None = None) -> dict:
    record = {
        "schema_version": "1.0",
        "strategy": "H024",
        "packet_type": packet_type,
        "observed_at_utc": mod.isoformat_utc(observed_at),
        "verdict": "PASS",
        "operator_state": "UPSTREAM_OK_BUT_ACTION_NOT_AUTHORIZED",
        "operator_next_action": "KEEP_BLOCKED",
        "effective_new_entries_blocked": True,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "xauusd_order_authorized": False,
        "usdjpy_order_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
        "violations": [],
    }
    if extra:
        record.update(extra)
    return record


def _populate_reports(tmp_path: Path, *, observed_at: datetime = NOW, overrides: dict[str, dict] | None = None) -> None:
    overrides = overrides or {}
    for name, filename in mod.UPSTREAM_REPORTS.items():
        extra = {}
        if name == "runtime_exposure_inventory":
            extra = {
                "canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
                "h024_position_count": 1,
                "h024_order_count": 0,
                "position": {
                    "symbol": "XAUUSDm",
                    "ticket": 4413054432,
                    "identifier": 4413054432,
                    "magic": 240024,
                    "volume": 0.01,
                    "type": 1,
                },
            }
        elif name == "runtime_account_risk_margin":
            extra = {
                "account_server": "Exness-MT5Trial6",
                "account_currency": "USD",
                "balance": 10000.0,
                "equity": 10025.0,
                "profit": 25.0,
                "margin": 2.36,
                "free_margin": 10022.64,
                "margin_level": 424000.0,
                "margin_used_fraction": 0.000236,
                "canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
            }
        elif name == "runtime_tick_spread":
            extra = {
                "observed": {
                    "symbols": {
                        "XAUUSDm": {
                            "verdict": "PASS",
                            "bid": 4702.0,
                            "ask": 4702.3,
                            "spread_points": 300.0,
                            "tick_age_seconds": 1.0,
                        }
                    }
                }
            }
        elif name == "manual_approval_gate_preview":
            extra = {
                "manual_approval_gate_preview_authorizes_action": False,
                "live_broker_request_constructed": False,
                "dry_run_request_shape_preview_constructed": False,
            }
        elif name in ("unified_runtime_supervision", "exact_ticket_governance", "decision_artifact", "pre_action_evidence_aggregate", "bar_age_exit_condition_evidence"):
            extra = {
                "exact_ticket": 4413054432,
                "exact_identifier": 4413054432,
                "exact_canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
            }
        elif name == "no_mutation_gate":
            extra = {
                "gate_opens_mutation_path": False,
                "automatic_execution_blocked": True,
                "broker_mutation_blocked": True,
                "close_modify_blocked": True,
                "entry_blocked": True,
                "order_check_blocked": True,
                "order_send_blocked": True,
                "trading_loop_blocked": True,
                "usdjpy_order_blocked": True,
                "xauusd_order_blocked": True,
            }

        record = _base_record(name, observed_at=observed_at, extra=extra)
        record.update(overrides.get(name, {}))
        _write_jsonl(tmp_path / filename, record)


def test_build_default_preview_passes_with_fresh_non_authorizing_upstreams(tmp_path: Path) -> None:
    _populate_reports(tmp_path)
    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)

    assert packet["verdict"] == "PASS"
    assert packet["operator_state"] == mod.PASS_OPERATOR_STATE
    assert packet["effective_new_entries_blocked"] is True
    assert packet["broker_mutation_authorized"] is False
    assert packet["order_check_authorized"] is False
    assert packet["order_send_authorized"] is False
    assert packet["entry_authorized"] is False
    assert packet["close_modify_authorized"] is False
    assert packet["xauusd_order_authorized"] is False
    assert packet["usdjpy_order_authorized"] is False
    assert packet["trading_loop_authorized"] is False
    assert packet["automatic_execution_authorized"] is False
    assert packet["operator_decision_v2_preview_authorizes_action"] is False
    assert packet["live_broker_request_constructed"] is False
    assert packet["dry_run_request_shape_preview_constructed"] is False
    assert packet["read_only_evidence"]["xauusdm_tick_spread_snapshot"]["bid"] == 4702.0


def test_missing_upstream_fails_closed(tmp_path: Path) -> None:
    _populate_reports(tmp_path)
    (tmp_path / mod.UPSTREAM_REPORTS["runtime_tick_spread"]).unlink()

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("runtime_tick_spread" in item for item in packet["violations"])


def test_stale_upstream_fails_closed(tmp_path: Path) -> None:
    _populate_reports(tmp_path, observed_at=NOW - timedelta(hours=2))

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW, max_upstream_age_seconds=60)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("stale" in item for item in packet["violations"])


def test_upstream_embedded_violation_fails_closed(tmp_path: Path) -> None:
    _populate_reports(tmp_path, overrides={"decision_artifact": {"violations": ["bad decision"]}})

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("embedded violations" in item for item in packet["violations"])


def test_unsafe_authorization_true_fails_closed(tmp_path: Path) -> None:
    _populate_reports(tmp_path, overrides={"no_mutation_gate": {"order_send_authorized": True}})

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("order_send_authorized" in item for item in packet["violations"])


def test_exact_ticket_mismatch_fails_closed(tmp_path: Path) -> None:
    _populate_reports(
        tmp_path,
        overrides={
            "runtime_exposure_inventory": {
                "position": {
                    "symbol": "XAUUSDm",
                    "ticket": 123,
                    "identifier": 123,
                    "magic": 240024,
                    "volume": 0.01,
                    "type": 1,
                }
            }
        },
    )

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("exact canary exact_ticket mismatch" in item for item in packet["violations"])


def test_recorded_close_preview_requires_operator_identity_attestation(tmp_path: Path) -> None:
    _populate_reports(tmp_path)
    decision = mod.build_default_operator_decision(
        now=NOW,
        decision_preview_status="OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY",
        requested_action="PREVIEW_CLOSE_ONLY",
        operator_id="NO_OPERATOR_DECISION_REQUESTED",
        operator_attests_exact_ticket_identity=False,
    )

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW, operator_decision=decision)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("operator_id" in item for item in packet["violations"])
    assert any("identity attestation" in item for item in packet["violations"])


def test_modify_stop_loss_preview_requires_numeric_preview_stop_loss(tmp_path: Path) -> None:
    _populate_reports(tmp_path)
    decision = mod.build_default_operator_decision(
        now=NOW,
        decision_preview_status="OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY",
        requested_action="PREVIEW_MODIFY_STOP_LOSS_ONLY",
        operator_id="operator-1",
        operator_attests_exact_ticket_identity=True,
    )

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW, operator_decision=decision)

    assert packet["verdict"] == "FAIL_CLOSED"
    assert any("preview_stop_loss" in item for item in packet["violations"])


def test_recorded_modify_stop_loss_preview_can_be_coherent_but_non_authorizing(tmp_path: Path) -> None:
    _populate_reports(tmp_path)
    decision = mod.build_default_operator_decision(
        now=NOW,
        decision_preview_status="OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY",
        requested_action="PREVIEW_MODIFY_STOP_LOSS_ONLY",
        operator_id="operator-1",
        preview_stop_loss=4817.394,
        operator_attests_exact_ticket_identity=True,
    )

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW, operator_decision=decision)

    assert packet["verdict"] == "PASS"
    assert packet["close_modify_authorized"] is False
    assert packet["operator_decision_v2_preview_authorizes_action"] is False
    assert packet["live_broker_request_constructed"] is False
    assert packet["dry_run_request_shape_preview_constructed"] is False


def test_verifier_rejects_require_pass_fail_closed_record(tmp_path: Path) -> None:
    _populate_reports(tmp_path)
    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)
    packet["verdict"] = "FAIL_CLOSED"
    packet["violations"] = ["forced failure"]
    path = tmp_path / "operator_decision_v2_preview.jsonl"
    _write_jsonl(path, packet)

    result = mod.verify_jsonl_file(path, require_pass=True)

    assert result["verdict"] == "FAIL_CLOSED"
    assert any("--require-pass" in item for item in result["violations"])


def test_verifier_rejects_true_blocking_field(tmp_path: Path) -> None:
    _populate_reports(tmp_path)
    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)
    packet["live_broker_request_constructed"] = True
    path = tmp_path / "operator_decision_v2_preview.jsonl"
    _write_jsonl(path, packet)

    result = mod.verify_jsonl_file(path, require_pass=True)

    assert result["verdict"] == "FAIL_CLOSED"
    assert any("live_broker_request_constructed" in item for item in result["violations"])



def test_account_snapshot_accepts_mt5_margin_free_alias(tmp_path: Path) -> None:
    _populate_reports(
        tmp_path,
        overrides={
            "runtime_account_risk_margin": {
                "free_margin": None,
                "margin_free": 10022.64,
            }
        },
    )

    packet = mod.build_packet(reports_dir=tmp_path, now=NOW)

    assert packet["verdict"] == "PASS"
    assert packet["read_only_evidence"]["account_risk_margin_snapshot"]["free_margin"] == 10022.64

def test_static_new_module_has_no_broker_mutation_call_sites() -> None:
    source = Path(mod.__file__).read_text(encoding="utf-8")
    forbidden_call_patterns = (
        ".order_send(",
        " order_send(",
        ".order_check(",
        " order_check(",
        ".symbol_select(",
        " symbol_select(",
        "positions_get(",
        "orders_get(",
    )
    for pattern in forbidden_call_patterns:
        assert pattern not in source
