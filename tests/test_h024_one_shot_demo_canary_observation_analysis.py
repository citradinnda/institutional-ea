from __future__ import annotations

import json
from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_observation_analysis import (
    build_observation_analysis,
    verify_observation_analysis_record,
)


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def _sample_ledger_record() -> dict:
    return {
        "allowed_demo_server": "Exness-MT5Trial6",
        "attempt_stage": "send_succeeded",
        "canary_comment": "H024_ONE_SHOT_DEMO_CANARY",
        "generated_at_utc": "2026-05-11T15:51:39Z",
        "order_check_result": {
            "balance": 10000.0,
            "comment": "Done",
            "equity": 10000.0,
            "margin": 2.36,
            "margin_free": 9997.64,
            "margin_level": 423728.81355932204,
            "profit": 0.0,
            "retcode": 0,
        },
        "order_send_result": {
            "ask": 4728.7570000000005,
            "bid": 4728.4490000000005,
            "comment": "H024_ONE_SHOT_DE",
            "deal": 3788869526,
            "order": 4413054432,
            "price": 4728.4490000000005,
            "request_id": 3072064830,
            "retcode": 10009,
            "retcode_external": 0,
            "volume": 0.01,
        },
        "request": {
            "action": 1,
            "comment": "H024_ONE_SHOT_DEMO_CANARY",
            "deviation": 50,
            "magic": 240024,
            "price": 4728.367,
            "sl": 4817.394,
            "symbol": "XAUUSDm",
            "type": 1,
            "type_filling": 1,
            "type_time": 0,
            "volume": 0.01,
        },
        "strategy": "H024",
        "symbol": "XAUUSDm",
    }


def _sample_audit_record() -> dict:
    return {
        "verdict": "PASS",
        "violations": [],
        "open_canary_positions_found": 1,
        "open_canary_positions": [
            {
                "ticket": 4413054432,
                "identifier": 4413054432,
                "symbol": "XAUUSDm",
                "magic": 240024,
                "type": 1,
                "volume": 0.01,
                "price_open": 4728.4490000000005,
                "sl": 4817.394,
                "comment": "H024_ONE_SHOT_DE",
            }
        ],
    }


def _sample_monitor_record() -> dict:
    return {
        "verdict": "PASS",
        "violations": [],
        "lifecycle_state": "open",
        "exact_open_canary_positions_found": 1,
        "unexpected_h024_pending_orders_found": 0,
        "ledger_successful_canary_records_found": 1,
        "current_price": 4747.721,
        "floating_pl": -19.27,
        "swap": 0.0,
    }


def _sample_lifecycle_record() -> dict:
    return {
        "verdict": "PASS",
        "decision": "continue_hold",
        "violations": [],
        "broker_mutation_authorized": False,
        "mt5_call_authorized": False,
        "close_authorized": False,
        "modify_authorized": False,
        "entry_authorized": False,
        "live_deployment_authorized": False,
        "current_price": 4747.721,
        "floating_pl": -19.27,
        "swap": 0.0,
    }


def _write_sample_inputs(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "ledger_path": tmp_path / "reports" / "ledger.jsonl",
        "post_order_audit_path": tmp_path / "reports" / "post_order_audit.jsonl",
        "monitor_path": tmp_path / "reports" / "monitor.jsonl",
        "lifecycle_decision_path": tmp_path / "reports" / "lifecycle.jsonl",
    }
    _write_jsonl(paths["ledger_path"], [_sample_ledger_record()])
    _write_jsonl(paths["post_order_audit_path"], [_sample_audit_record()])
    _write_jsonl(paths["monitor_path"], [_sample_monitor_record()])
    _write_jsonl(paths["lifecycle_decision_path"], [_sample_lifecycle_record()])
    return paths


def test_observation_analysis_passes_and_computes_execution_facts(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)

    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["broker_mutation_authorized"] is False
    assert record["edge_inference_authorized"] is False
    assert record["execution_observations"]["slippage_absolute"] == 0.082
    assert record["execution_observations"]["slippage_adverse_to_sell"] is True
    assert record["execution_observations"]["order_check_margin"] == 2.36
    assert record["execution_observations"]["comment_truncated"] is True
    assert record["lifecycle_observations"]["monitor_lifecycle_state"] == "open"
    assert record["lifecycle_observations"]["lifecycle_decision"] == "continue_hold"
    assert record["latest_mark_to_market"]["floating_pl"] == -19.27


def test_observation_analysis_rejects_missing_successful_canary(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)
    failed = _sample_ledger_record()
    failed["attempt_stage"] = "order_send_failed"
    failed["order_send_result"]["retcode"] = 10027
    _write_jsonl(paths["ledger_path"], [failed])

    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "FAIL"
    assert any("no successful H024 canary ledger record found" in violation for violation in record["violations"])


def test_observation_analysis_rejects_monitor_failure(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)
    monitor = _sample_monitor_record()
    monitor["verdict"] = "FAIL"
    monitor["violations"] = ["unexpected order"]
    _write_jsonl(paths["monitor_path"], [monitor])

    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "FAIL"
    assert any("monitor verdict must be PASS" in violation for violation in record["violations"])


def test_observation_analysis_rejects_lifecycle_mutation_authorization(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)
    lifecycle = _sample_lifecycle_record()
    lifecycle["broker_mutation_authorized"] = True
    _write_jsonl(paths["lifecycle_decision_path"], [lifecycle])

    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "FAIL"
    assert any("broker_mutation_authorized must remain False" in violation for violation in record["violations"])


def test_observation_analysis_rejects_edge_inference_if_record_is_tampered(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)
    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")
    record["edge_inference_authorized"] = True

    violations = verify_observation_analysis_record(record, require_pass=True)

    assert "edge_inference_authorized must be False" in violations


def test_observation_analysis_verifier_requires_plumbing_not_edge(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)
    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    violations = verify_observation_analysis_record(record, require_pass=True)

    assert violations == []
    assert record["engineering_interpretation"]["plumbing_validated"] is True
    assert record["engineering_interpretation"]["strategy_edge_validated"] is False
    assert record["engineering_interpretation"]["single_canary_is_edge_evidence"] is False


def test_observation_analysis_module_is_local_file_analysis_only() -> None:
    source = Path("quantcore/execution/h024_one_shot_demo_canary_observation_analysis.py").read_text(encoding="utf-8")

    assert "import MetaTrader5" not in source
    assert "MetaTrader5 as" not in source
    assert "mt5." not in source
    assert ".order_check(" not in source
    assert ".order_send(" not in source

def test_observation_analysis_finds_nested_mark_to_market_fields(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)
    monitor = _sample_monitor_record()
    monitor.pop("current_price")
    monitor.pop("floating_pl")
    monitor.pop("swap")
    monitor["position_snapshot"] = {
        "position": {
            "price_current": 4747.721,
            "profit": -19.27,
            "swap": 0.0,
        }
    }
    _write_jsonl(paths["monitor_path"], [monitor])

    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "PASS"
    assert record["latest_mark_to_market"]["current_price"] == 4747.721
    assert record["latest_mark_to_market"]["floating_pl"] == -19.27
    assert record["latest_mark_to_market"]["swap"] == 0.0


def test_observation_analysis_requires_mark_to_market_for_open_state(tmp_path: Path) -> None:
    paths = _write_sample_inputs(tmp_path)
    monitor = _sample_monitor_record()
    monitor.pop("current_price")
    monitor.pop("floating_pl")
    monitor.pop("swap")
    _write_jsonl(paths["monitor_path"], [monitor])

    lifecycle = _sample_lifecycle_record()
    lifecycle.pop("current_price")
    lifecycle.pop("floating_pl")
    lifecycle.pop("swap")
    _write_jsonl(paths["lifecycle_decision_path"], [lifecycle])

    record = build_observation_analysis(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "FAIL"
    assert any("open monitor state must expose a current price" in violation for violation in record["violations"])
    assert any("open monitor state must expose floating P/L" in violation for violation in record["violations"])
    assert any("open monitor state must expose swap" in violation for violation in record["violations"])

