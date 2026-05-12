import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

from quantcore.execution import h024_read_only_black_swan_guard as guard


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
        "operator_state": f"{name.upper()}_OK_BUT_TRADING_NOT_AUTHORIZED",
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


def _identity_record(name: str, **overrides):
    record = _base_upstream_record(
        name,
        exact_ticket=4413054432,
        exact_identifier=4413054432,
        runtime_symbol="XAUUSDm",
        model_symbol="XAUUSD",
        magic=240024,
        volume=0.01,
        position_type=1,
    )
    record.update(overrides)
    return record


def _write_jsonl(path: Path, record: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def _merge_defaults(defaults: dict, overrides: dict) -> dict:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _write_all_upstream(tmp_path: Path, overrides_by_name=None):
    overrides_by_name = overrides_by_name or {}
    paths = {}

    for name in guard.UPSTREAM_SPECS:
        path = tmp_path / f"{name}.jsonl"
        overrides = overrides_by_name.get(name, {})
        if name == "runtime_heartbeat":
            record = _base_upstream_record(
                name,
                **_merge_defaults(
                    {
                        "server": "Exness-MT5Trial6",
                        "currency": "USD",
                        "terminal_connected": True,
                        "account_available": True,
                    },
                    overrides,
                ),
            )
        elif name == "runtime_lockout_reader":
            record = _base_upstream_record(
                name,
                **_merge_defaults(
                    {
                        "global_no_new_entry_lockout_active": False,
                        "manual_override_lockout_active": False,
                        "xauusd_no_new_entry_lockout_active": False,
                        "usdjpy_no_new_entry_lockout_active": False,
                    },
                    overrides,
                ),
            )
        elif name == "runtime_tick_spread":
            record = _base_upstream_record(
                name,
                **_merge_defaults(
                    {
                        "runtime_symbol": "XAUUSDm",
                        "bid": 4728.1,
                        "ask": 4728.4,
                        "spread": 0.3,
                        "tick_time": _iso_now(),
                    },
                    overrides,
                ),
            )
        elif name == "runtime_account_risk_margin":
            record = _base_upstream_record(
                name,
                **_merge_defaults(
                    {
                        "balance": 10000.0,
                        "equity": 9990.0,
                        "margin": 50.0,
                        "margin_free": 9940.0,
                        "margin_level": 19980.0,
                        "floating_pnl": -10.0,
                    },
                    overrides,
                ),
            )
        elif name == "runtime_exposure_inventory":
            record = _identity_record(
                name,
                **_merge_defaults(
                    {
                        "canary_observed": True,
                        "h024_position_count": 1,
                        "h024_order_count": 0,
                        "usdjpy_exposure_detected": False,
                        "extra_h024_exposure_detected": False,
                    },
                    overrides,
                ),
            )
        elif name in {
            "operator_decision_v2_preview",
            "execution_readiness_dry_run_schema_preview",
            "manual_approval_gate_preview",
            "pre_action_evidence_aggregate",
            "bar_age_exit_condition_evidence",
            "exact_ticket_close_modify_governance",
            "exact_ticket_decision_artifact_validator",
        }:
            record = _identity_record(
                name,
                **_merge_defaults(
                    {
                        "operator_decision_v2_preview_authorizes_action": False,
                        "manual_approval_gate_preview_authorizes_action": False,
                        "execution_readiness_dry_run_schema_preview_authorizes_execution": False,
                        "live_broker_request_constructed": False,
                        "executable_trade_request_constructed": False,
                        "mt5_request_dictionary_constructed": False,
                    },
                    overrides,
                ),
            )
        else:
            record = _base_upstream_record(name, **overrides)

        _write_jsonl(path, record)
        paths[name] = path

    return paths

def test_builds_pass_when_all_upstream_clear(tmp_path):
    paths = _write_all_upstream(tmp_path)

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "PASS"
    assert record["operator_state"] == guard.PASS_OPERATOR_STATE
    assert record["black_swan_guard_clear"] is True
    assert record["black_swan_guard_triggered"] is False
    assert record["effective_new_entries_blocked"] is True
    assert record["broker_mutation_authorized"] is False
    assert record["order_check_authorized"] is False
    assert record["order_send_authorized"] is False
    assert record["entry_authorized"] is False
    assert record["close_modify_authorized"] is False
    assert record["black_swan_guard_authorizes_trading"] is False
    assert record["live_broker_request_constructed"] is False
    assert record["executable_trade_request_constructed"] is False
    assert record["mt5_request_dictionary_constructed"] is False


def test_missing_upstream_packet_fails_closed(tmp_path):
    paths = _write_all_upstream(tmp_path)
    paths["runtime_heartbeat"] = None

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("runtime_heartbeat: missing upstream report" in item for item in record["violations"])


def test_stale_upstream_packet_fails_closed(tmp_path):
    stale = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    paths = _write_all_upstream(tmp_path, {"runtime_tick_spread": {"observed_at_utc": stale}})

    record = guard.build_read_only_black_swan_guard(
        reports_dir=tmp_path,
        upstream_paths=paths,
        max_upstream_age_seconds=60,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("runtime_tick_spread: upstream evidence stale" in item for item in record["violations"])


def test_upstream_fail_closed_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_safety_aggregate": {"verdict": "FAIL_CLOSED", "violations": ["blocked"]}},
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("runtime_safety_aggregate: upstream verdict is not PASS" in item for item in record["violations"])
    assert any("runtime_safety_aggregate: upstream record has embedded violations" in item for item in record["violations"])


def test_unsafe_upstream_authorization_true_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_no_mutation_safety_gate": {"order_send_authorized": True}},
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("unsafe authorization true: order_send_authorized" in item for item in record["violations"])


def test_lockout_active_triggers_black_swan_fail_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_lockout_reader": {"manual_override_lockout_active": True}},
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert record["black_swan_guard_triggered"] is True
    assert any("lockout active: manual_override_lockout_active" in item for item in record["violations"])


def test_bid_ask_inversion_triggers_black_swan_fail_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_tick_spread": {"bid": 100.0, "ask": 99.0}},
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("bid/ask inversion" in item for item in record["violations"])


def test_extreme_spread_triggers_black_swan_fail_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_tick_spread": {"spread": 5000.0}},
    )

    record = guard.build_read_only_black_swan_guard(
        reports_dir=tmp_path,
        upstream_paths=paths,
        extreme_spread_limit=1000.0,
    )

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("extreme spread detected" in item for item in record["violations"])


def test_negative_free_margin_triggers_black_swan_fail_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_account_risk_margin": {"margin_free": -1.0}},
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("negative free margin" in item for item in record["violations"])


def test_low_margin_level_triggers_black_swan_fail_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_account_risk_margin": {"margin_level": 50.0}},
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("margin level below black-swan floor" in item for item in record["violations"])


def test_unexpected_h024_order_triggers_black_swan_fail_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {"runtime_exposure_inventory": {"h024_order_count": 1}},
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("unexpected H024 pending/open orders detected" in item for item in record["violations"])


def test_missing_exact_ticket_identity_fails_closed(tmp_path):
    paths = _write_all_upstream(
        tmp_path,
        {
            "runtime_exposure_inventory": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
            "operator_decision_v2_preview": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
            "execution_readiness_dry_run_schema_preview": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
            "manual_approval_gate_preview": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
            "pre_action_evidence_aggregate": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
            "bar_age_exit_condition_evidence": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
            "exact_ticket_close_modify_governance": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
            "exact_ticket_decision_artifact_validator": {
                "exact_ticket": None,
                "exact_identifier": None,
                "runtime_symbol": None,
                "model_symbol": None,
                "magic": None,
                "volume": None,
                "position_type": None,
            },
        },
    )

    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)

    assert record["verdict"] == "FAIL_CLOSED"
    assert any("exact_ticket_locked missing" in item for item in record["violations"])


def test_verifier_accepts_valid_pass_record(tmp_path):
    paths = _write_all_upstream(tmp_path)
    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)
    output = tmp_path / "black_swan.jsonl"
    guard.write_jsonl(output, record)

    verdict, violations, records = guard.verify_jsonl_file(output, require_pass=True)

    assert verdict == "PASS"
    assert violations == []
    assert len(records) == 1


def test_verifier_rejects_true_authorization(tmp_path):
    paths = _write_all_upstream(tmp_path)
    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)
    record["broker_mutation_authorized"] = True
    record["authorizations"]["broker_mutation_authorized"] = True
    output = tmp_path / "black_swan.jsonl"
    guard.write_jsonl(output, record)

    verdict, violations, _ = guard.verify_jsonl_file(output, require_pass=True)

    assert verdict == "FAIL"
    assert any("broker_mutation_authorized" in item for item in violations)


def test_verifier_rejects_fail_closed_when_require_pass(tmp_path):
    paths = _write_all_upstream(tmp_path)
    paths["runtime_heartbeat"] = None
    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)
    output = tmp_path / "black_swan.jsonl"
    guard.write_jsonl(output, record)

    verdict, violations, _ = guard.verify_jsonl_file(output, require_pass=True)

    assert verdict == "FAIL"
    assert any("--require-pass rejects verdict FAIL_CLOSED" in item for item in violations)


def test_verifier_rejects_executable_trade_request_object(tmp_path):
    paths = _write_all_upstream(tmp_path)
    record = guard.build_read_only_black_swan_guard(reports_dir=tmp_path, upstream_paths=paths)
    record["trade_request"] = {"symbol": "XAUUSDm"}
    output = tmp_path / "black_swan.jsonl"
    guard.write_jsonl(output, record)

    verdict, violations, _ = guard.verify_jsonl_file(output, require_pass=True)

    assert verdict == "FAIL"
    assert any("executable broker/trade request object present: trade_request" in item for item in violations)


def test_static_source_has_no_broker_mutation_call_sites():
    source = Path(guard.__file__).read_text(encoding="utf-8")

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
