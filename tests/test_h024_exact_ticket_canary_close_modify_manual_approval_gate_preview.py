from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from quantcore.execution import h024_exact_ticket_canary_close_modify_manual_approval_gate_preview as manual_preview


def _write_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")


def _base_upstream(
    now: datetime,
    *,
    ticket: int = manual_preview.EXPECTED_TICKET,
    verdict: str = "PASS",
    violations=None,
    auth_overrides=None,
) -> dict:
    if violations is None:
        violations = []
    authorizations = {
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
    if auth_overrides:
        authorizations.update(auth_overrides)
    record = {
        "schema_version": "1.0",
        "strategy": "H024",
        "packet_type": "synthetic_upstream",
        "observed_at_utc": manual_preview.isoformat_z(now),
        "verdict": verdict,
        "violations": violations,
        "operator_state": "SYNTHETIC_OK_BUT_TRADING_NOT_AUTHORIZED",
        "operator_next_action": "KEEP_BLOCKED",
        "ticket": ticket,
        "identifier": manual_preview.EXPECTED_IDENTIFIER,
        "runtime_symbol": manual_preview.EXPECTED_RUNTIME_SYMBOL,
        "model_symbol": manual_preview.EXPECTED_MODEL_SYMBOL,
        "magic": manual_preview.EXPECTED_MAGIC,
        "volume": manual_preview.EXPECTED_VOLUME,
        "position_type": manual_preview.EXPECTED_POSITION_TYPE,
        "canary_state": "OBSERVED_EXACT_KNOWN_CANARY",
        "exact_canary_observed": True,
        "h024_position_count": 1,
        "h024_order_count": 0,
        "balance": 10000.0,
        "equity": 10025.0,
        "profit": 25.0,
        "margin": 2.36,
        "free_margin": 10022.64,
        "margin_level": 424000.0,
        "symbols": [
            {
                "symbol": "XAUUSDm",
                "bid": 4700.0,
                "ask": 4700.3,
                "spread_points": 300.0,
                "tick_age_seconds": 0.2,
                "verdict": "PASS",
            },
            {
                "symbol": "USDJPYm",
                "bid": 157.4,
                "ask": 157.41,
                "spread_points": 10.0,
                "tick_age_seconds": 0.2,
                "verdict": "PASS",
            },
        ],
    }
    record.update(authorizations)
    record["authorizations"] = dict(authorizations)
    return record


def _write_all_upstreams(tmp_path: Path, now: datetime, **kwargs) -> dict[str, Path]:
    paths = {name: tmp_path / path.name for name, path in manual_preview.REPORT_PATHS.items()}
    for name, path in paths.items():
        _write_jsonl(path, _base_upstream(now, **kwargs.get(name, {})))
    return paths


def test_build_preview_passes_with_fresh_safe_upstreams(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(tmp_path, now)

    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["approval_preview_schema"]["preview_only"] is True
    assert record["approval_preview_schema"]["live_broker_request_constructed"] is False
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["close_modify_authorized"] is False
    assert record["manual_approval_gate_preview_authorizes_action"] is False


def test_missing_upstream_fails_closed(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(tmp_path, now)
    paths["no_mutation_gate"].unlink()

    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("missing upstream report" in item for item in record["violations"])


def test_stale_upstream_fails_closed(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 10, tzinfo=timezone.utc)
    stale = now - timedelta(seconds=301)
    paths = _write_all_upstreams(tmp_path, stale)

    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("stale" in item for item in record["violations"])


def test_future_skewed_upstream_fails_closed(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    future = now + timedelta(seconds=61)
    paths = _write_all_upstreams(tmp_path, future)

    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("future-skewed" in item for item in record["violations"])


def test_unsafe_upstream_authorization_fails_closed(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(
        tmp_path,
        now,
        no_mutation_gate={"auth_overrides": {"order_send_authorized": True}},
    )

    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("order_send_authorized must be false" in item for item in record["violations"])


def test_wrong_exact_ticket_fails_closed(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(
        tmp_path,
        now,
        bar_age_exit_condition_evidence={"ticket": 123},
    )

    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("missing exact ticket" in item for item in record["violations"])


def test_verifier_rejects_action_authorization(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(tmp_path, now)
    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)
    record["broker_mutation_authorized"] = True
    report = tmp_path / "preview.jsonl"
    manual_preview.write_jsonl(record, report)

    _, violations = manual_preview.verify_report(report, require_pass=True)

    assert any("broker_mutation_authorized must be false" in item for item in violations)


def test_require_pass_rejects_fail_closed_record(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(tmp_path, now)
    paths["decision_artifact"].unlink()
    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)
    report = tmp_path / "preview.jsonl"
    manual_preview.write_jsonl(record, report)

    _, violations = manual_preview.verify_report(report, require_pass=True)

    assert any("--require-pass set" in item for item in violations)


def test_verifier_rejects_live_request_preview_flags(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(tmp_path, now)
    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)
    record["approval_preview_schema"]["live_broker_request_constructed"] = True
    report = tmp_path / "preview.jsonl"
    manual_preview.write_jsonl(record, report)

    _, violations = manual_preview.verify_report(report, require_pass=True)

    assert any("live_broker_request_constructed must be false" in item for item in violations)


def test_static_no_broker_mutation_call_sites() -> None:
    source = Path(
        "quantcore/execution/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.py"
    ).read_text(encoding="utf-8")
    forbidden_call_fragments = [
        "order_send(",
        "order_check(",
        "symbol_select(",
        ".order_send",
        ".order_check",
        ".symbol_select",
        "TRADE_ACTION_DEAL",
        "TRADE_ACTION_SLTP",
    ]
    for fragment in forbidden_call_fragments:
        assert fragment not in source
    assert "MetaTrader5" not in source

def test_build_preview_accepts_keyed_tick_spread_symbol_map(tmp_path: Path) -> None:
    now = datetime(2026, 5, 12, 0, 0, tzinfo=timezone.utc)
    paths = _write_all_upstreams(tmp_path, now)

    tick_record = _base_upstream(now)
    tick_record.pop("symbols", None)
    tick_record["observed"] = {
        "symbols": {
            "XAUUSDm": {
                "bid": 4701.0,
                "ask": 4701.308,
                "spread_points": 308.0,
                "tick_age_seconds": 0.3,
                "verdict": "PASS",
            },
            "USDJPYm": {
                "bid": 157.4,
                "ask": 157.41,
                "spread_points": 10.0,
                "tick_age_seconds": 0.4,
                "verdict": "PASS",
            },
        }
    }
    _write_jsonl(paths["runtime_tick_spread"], tick_record)

    record = manual_preview.build_manual_approval_gate_preview_record(report_paths=paths, observed_at=now)

    assert record["verdict"] == "PASS"
    xauusd = record["read_only_evidence"]["tick_spread"]["XAUUSDm"]
    assert xauusd["bid"] == 4701.0
    assert xauusd["ask"] == 4701.308
    assert xauusd["spread_points"] == 308.0

