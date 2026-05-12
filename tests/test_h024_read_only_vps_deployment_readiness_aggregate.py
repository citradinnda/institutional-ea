from __future__ import annotations

import json
import re
from datetime import timedelta
from pathlib import Path

import pytest

from quantcore.execution import h024_read_only_vps_deployment_readiness_aggregate as m


def _write_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")


def _base_upstream_record(now, **overrides):
    record = {
        "schema_version": "upstream.test.v1",
        "strategy": "H024",
        "packet_type": "upstream_test_packet",
        "observed_at_utc": m.isoformat_utc(now),
        "verdict": "PASS",
        "operator_state": "UPSTREAM_OK_BUT_TRADING_NOT_AUTHORIZED",
        "operator_next_action": "CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED",
        "violations": [],
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
        "live_broker_request_constructed": False,
        "executable_trade_request_constructed": False,
        "mt5_request_dictionary_constructed": False,
    }
    record.update(overrides)
    return record


def _write_all_upstreams(base_dir: Path, now, overrides_by_name: dict | None = None) -> None:
    overrides_by_name = overrides_by_name or {}
    for spec in m.UPSTREAM_SPECS:
        overrides = dict(overrides_by_name.get(spec.name, {}))
        if spec.name == "read_only_black_swan_guard":
            overrides.setdefault("exact_ticket", m.EXPECTED_EXACT_TICKET)
            overrides.setdefault("exact_identifier", m.EXPECTED_EXACT_IDENTIFIER)
            overrides.setdefault("black_swan_guard_clear", True)
            overrides.setdefault("black_swan_guard_triggered", False)
        path = base_dir / spec.path_candidates[0]
        _write_jsonl(path, _base_upstream_record(now, **overrides))


def _build(base_dir: Path, now):
    runner = base_dir / m.RUNNER_PATH
    runner.parent.mkdir(parents=True, exist_ok=True)
    runner.write_text("# read-only observer runner\n", encoding="utf-8")
    return m.build_readiness_aggregate(
        base_dir=base_dir,
        now_utc=now,
        require_venv=False,
        require_mt5_package=False,
    )


def test_happy_path_passes(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now)

    record = _build(tmp_path, now)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == m.PASS_OPERATOR_STATE
    assert record["read_only_observer_workflow_authorized_for_operator_review"] is True
    assert record["effective_new_entries_blocked"] is True
    for field in m.AUTHORIZATION_FIELDS:
        assert record[field] is False
    for field in m.CONSTRUCTION_FIELDS:
        assert record[field] is False
    assert record["symbol_select_authorized"] is False
    assert record["vps_deployment_readiness_authorizes_trading"] is False
    assert m.validate_records([record], require_pass=True) == []


def test_missing_upstream_report_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now)
    (tmp_path / m.UPSTREAM_SPECS[0].path_candidates[0]).unlink()

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("missing upstream report" in violation for violation in record["violations"])
    assert any("--require-pass rejects verdict" in v for v in m.validate_records([record], require_pass=True))


def test_malformed_upstream_report_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now)
    bad = tmp_path / m.UPSTREAM_SPECS[0].path_candidates[0]
    bad.write_text("{not json}\n", encoding="utf-8")

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("malformed upstream JSONL" in violation for violation in record["violations"])


def test_stale_upstream_report_fails_closed(tmp_path):
    now = m.utc_now()
    stale = now - timedelta(hours=3)
    _write_all_upstreams(tmp_path, now, {
        "runtime_heartbeat": {"observed_at_utc": m.isoformat_utc(stale)}
    })

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("stale" in violation for violation in record["violations"])


def test_upstream_fail_verdict_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now, {
        "runtime_safety_aggregate": {"verdict": "FAIL_CLOSED"}
    })

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("upstream verdict is not PASS" in violation for violation in record["violations"])


def test_upstream_embedded_violations_fail_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now, {
        "runtime_no_mutation_safety_gate": {"violations": ["unsafe"]}
    })

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("embedded violations" in violation for violation in record["violations"])


def test_unsafe_authorization_true_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now, {
        "execution_readiness_dry_run_schema_preview": {"order_send_authorized": True}
    })

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("order_send_authorized=True" in violation for violation in record["violations"])


def test_missing_authorization_field_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now)
    path = tmp_path / "reports/h024_runtime_safety_lockout.jsonl"
    upstream = json.loads(path.read_text(encoding="utf-8"))
    del upstream["close_modify_authorized"]
    _write_jsonl(path, upstream)

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("missing authorization field close_modify_authorized" in violation for violation in record["violations"])


def test_black_swan_triggered_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now, {
        "read_only_black_swan_guard": {
            "black_swan_guard_clear": False,
            "black_swan_guard_triggered": True,
        }
    })

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("black_swan_guard_clear is not true" in violation for violation in record["violations"])
    assert any("black_swan_guard_triggered is not false" in violation for violation in record["violations"])


def test_wrong_exact_canary_identity_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now, {
        "read_only_black_swan_guard": {"exact_ticket": 123}
    })

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("exact_ticket mismatch" in violation for violation in record["violations"])


def test_executable_request_object_fails_closed(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now, {
        "exact_ticket_operator_decision_v2_preview": {
            "live_broker_request": {"action": "not allowed"}
        }
    })

    record = _build(tmp_path, now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("request object present" in violation for violation in record["violations"])


def test_runbook_forbidden_command_fails_verifier(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now)
    record = _build(tmp_path, now)
    record["operator_runbook"]["commands"].append({
        "name": "bad",
        "operator_command": "python -c MetaTrader5.order_send({})",
    })

    violations = m.validate_records([record], require_pass=True)

    assert any("forbidden token" in violation for violation in violations)


def test_verifier_rejects_missing_own_authorization(tmp_path):
    now = m.utc_now()
    _write_all_upstreams(tmp_path, now)
    record = _build(tmp_path, now)
    del record["authorizations"]["order_check_authorized"]
    del record["order_check_authorized"]

    violations = m.validate_records([record], require_pass=True)

    assert any("missing authorization field order_check_authorized" in violation for violation in violations)


def test_verify_malformed_jsonl_returns_error(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text("{bad}\n", encoding="utf-8")

    with pytest.raises(ValueError):
        m.load_jsonl_records(path)


def test_static_sources_have_no_broker_mutation_call_sites():
    paths = [
        Path("quantcore/execution/h024_read_only_vps_deployment_readiness_aggregate.py"),
        Path("scripts/build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py"),
        Path("scripts/verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py"),
        Path("scripts/run_h024_read_only_vps_observer_once.ps1"),
    ]
    patterns = [
        r"\border_send\s*\(",
        r"\border_check\s*\(",
        r"\bsymbol_select\s*\(",
        r"\bTRADE_ACTION_",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            assert re.search(pattern, text) is None, f"{path} contains forbidden call pattern {pattern}"


def test_runner_does_not_invoke_legacy_canary_or_trading_loop():
    text = Path("scripts/run_h024_read_only_vps_observer_once.ps1").read_text(encoding="utf-8").lower()
    assert "run_h024_one_shot_demo_canary" not in text
    assert "h024_one_shot_demo_canary.py" not in text
    assert "trading_loop" not in text