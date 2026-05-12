import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from quantcore.execution import h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview as packet


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _base_upstream_record(name: str, **overrides):
    record = {
        "schema_version": "1.0",
        "strategy": "H024",
        "packet_type": name,
        "observed_at_utc": _iso_now(),
        "verdict": "PASS",
        "violations": [],
        "operator_state": f"{name.upper()}_OK_BUT_ACTION_NOT_AUTHORIZED",
        "operator_next_action": "KEEP_BLOCKED_NO_TRADING_AUTHORIZED",
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
    }
    record.update(overrides)
    return record


def _operator_decision_v2_record(**overrides):
    record = _base_upstream_record(
        "h024_exact_ticket_canary_close_modify_operator_decision_v2_preview",
        exact_ticket=4413054432,
        exact_identifier=4413054432,
        runtime_symbol="XAUUSDm",
        model_symbol="XAUUSD",
        magic=240024,
        volume=0.01,
        position_type=1,
        decision_preview_status="NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY",
        requested_action="NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY",
        operator_decision_v2_preview_authorizes_action=False,
        live_broker_request_constructed=False,
        dry_run_request_shape_preview_constructed=False,
    )
    record.update(overrides)
    return record


def _write_jsonl(path: Path, record: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def _write_all_upstream(tmp_path: Path, overrides_by_name=None):
    overrides_by_name = overrides_by_name or {}
    paths = {}

    for name in packet.UPSTREAM_SPECS:
        path = tmp_path / f"{name}.jsonl"
        if name == "operator_decision_v2_preview":
            record = _operator_decision_v2_record(**overrides_by_name.get(name, {}))
        elif name == "runtime_exposure_inventory":
            record = _base_upstream_record(
                name,
                exact_ticket=4413054432,
                exact_identifier=4413054432,
                runtime_symbol="XAUUSDm",
                model_symbol="XAUUSD",
                magic=240024,
                volume=0.01,
                position_type=1,
                canary_observed=True,
                h024_position_count=1,
                h024_order_count=0,
                **overrides_by_name.get(name, {}),
            )
        elif name == "runtime_account_risk_margin":
            record = _base_upstream_record(
                name,
                balance=10000.0,
                equity=9990.0,
                margin=50.0,
                margin_free=9940.0,
                margin_level=19980.0,
                floating_pnl=-10.0,
                **overrides_by_name.get(name, {}),
            )
        elif name == "runtime_tick_spread":
            record = _base_upstream_record(
                name,
                runtime_symbol="XAUUSDm",
                bid=4728.1,
                ask=4728.4,
                spread=0.3,
                tick_time=_iso_now(),
                **overrides_by_name.get(name, {}),
            )
        else:
            record = _base_upstream_record(name, **overrides_by_name.get(name, {}))

        _write_jsonl(path, record)
        paths[name] = path

    return paths


def test_builds_pass_with_all_required_upstream_packets(tmp_path):
    paths = _write_all_upstream(tmp_path)

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == packet.PASS_OPERATOR_STATE
    assert record["effective_new_entries_blocked"] is True
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["entry_authorized"] is False
    assert record["close_modify_authorized"] is False
    assert record["xauusd_order_authorized"] is False
    assert record["usdjpy_order_authorized"] is False
    assert record["trading_loop_authorized"] is False
    assert record["automatic_execution_authorized"] is False
    assert record["execution_readiness_dry_run_schema_preview_constructed"] is True
    assert record["execution_readiness_dry_run_schema_preview_authorizes_execution"] is False
    assert record["live_broker_request_constructed"] is False
    assert record["executable_trade_request_constructed"] is False
    assert record["mt5_request_dictionary_constructed"] is False
    assert record["execution_readiness_dry_run_schema_preview"]["contains_executable_trade_request"] is False


def test_missing_upstream_packet_fails_closed(tmp_path):
    paths = _write_all_upstream(tmp_path)
    paths["runtime_no_mutation_safety_gate"] = None

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert "runtime_no_mutation_safety_gate: missing upstream report" in record["violations"]


def test_stale_upstream_packet_fails_closed(tmp_path):
    stale = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    paths = _write_all_upstream(
        tmp_path,
        {"operator_decision_v2_preview": {"observed_at_utc": stale}},
    )

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
        max_upstream_age_seconds=60,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("operator_decision_v2_preview: upstream evidence stale" in item for item in record["violations"])


def test_upstream_fail_closed_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"manual_approval_gate_preview": {"verdict": "FAIL_CLOSED", "violations": ["blocked"]}},
    )

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("manual_approval_gate_preview: upstream verdict is not PASS" in item for item in record["violations"])
    assert any("manual_approval_gate_preview: upstream record has embedded violations" in item for item in record["violations"])


def test_upstream_unsafe_authorization_true_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_no_mutation_safety_gate": {"order_send_authorized": True}},
    )

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("unsafe authorization true: order_send_authorized" in item for item in record["violations"])


def test_operator_decision_ticket_mismatch_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"operator_decision_v2_preview": {"exact_ticket": 123}},
    )

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("exact ticket mismatch" in item for item in record["violations"])


def test_operator_decision_ambiguous_default_status_with_preview_action_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {
            "operator_decision_v2_preview": {
                "decision_preview_status": "NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY",
                "requested_action": "PREVIEW_CLOSE_ONLY",
            }
        },
    )

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("ambiguous default status" in item for item in record["violations"])


def test_operator_decision_intent_without_preview_action_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {
            "operator_decision_v2_preview": {
                "decision_preview_status": "OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY",
                "requested_action": "NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY",
            }
        },
    )

    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("ambiguous intent status" in item for item in record["violations"])


def test_verifier_accepts_valid_pass_record(tmp_path):
    paths = _write_all_upstream(tmp_path)
    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )
    output = tmp_path / "preview.jsonl"
    packet.write_jsonl(output, record)

    verdict, violations, records = packet.verify_jsonl_file(output, require_pass=True)

    assert verdict == "PASS"
    assert violations == []
    assert len(records) == 1


def test_verifier_rejects_true_authorization(tmp_path):
    paths = _write_all_upstream(tmp_path)
    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )
    record["order_check_authorized"] = True
    record["authorizations"]["order_check_authorized"] = True
    output = tmp_path / "preview.jsonl"
    packet.write_jsonl(output, record)

    verdict, violations, _ = packet.verify_jsonl_file(output, require_pass=True)

    assert verdict == "FAIL"
    assert any("order_check_authorized" in item for item in violations)


def test_verifier_rejects_fail_closed_when_require_pass(tmp_path):
    paths = _write_all_upstream(tmp_path)
    paths["operator_decision_v2_preview"] = None
    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )
    output = tmp_path / "preview.jsonl"
    packet.write_jsonl(output, record)

    verdict, violations, _ = packet.verify_jsonl_file(output, require_pass=True)

    assert verdict == "FAIL"
    assert any("--require-pass rejects verdict FAIL_CLOSED" in item for item in violations)


def test_verifier_rejects_executable_trade_request_object(tmp_path):
    paths = _write_all_upstream(tmp_path)
    record = packet.build_execution_readiness_dry_run_schema_preview(
        reports_dir=tmp_path,
        upstream_paths=paths,
    )
    record["trade_request"] = {"action": "DEAL", "symbol": "XAUUSDm"}
    output = tmp_path / "preview.jsonl"
    packet.write_jsonl(output, record)

    verdict, violations, _ = packet.verify_jsonl_file(output, require_pass=True)

    assert verdict == "FAIL"
    assert any("executable broker/trade request object present: trade_request" in item for item in violations)


def test_select_latest_report_uses_patterns(tmp_path):
    older = tmp_path / "old_no_mutation_safety_gate.jsonl"
    newer = tmp_path / "h024_runtime_no_mutation_safety_gate.jsonl"
    _write_jsonl(older, _base_upstream_record("old"))
    _write_jsonl(newer, _base_upstream_record("new"))

    selected = packet.select_latest_report(tmp_path, ("*no_mutation*safety_gate*.jsonl",))

    assert selected is not None
    assert selected.name.endswith("no_mutation_safety_gate.jsonl")


def test_static_source_has_no_broker_mutation_call_sites():
    source = Path(packet.__file__).read_text(encoding="utf-8")

    forbidden_call_patterns = (
        ".order_check(",
        "order_check(",
        ".order_send(",
        "order_send(",
        ".symbol_select(",
        "symbol_select(",
        "MetaTrader5",
        "mt5.",
    )

    for pattern in forbidden_call_patterns:
        assert pattern not in source
