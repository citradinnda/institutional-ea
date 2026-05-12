from __future__ import annotations

import json
from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_supervisory_state import (
    build_supervisory_state,
    verify_supervisory_state_record,
)


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def _monitor_record() -> dict:
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


def _lifecycle_record() -> dict:
    return {
        "verdict": "PASS",
        "violations": [],
        "decision": "continue_hold",
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


def _observation_record() -> dict:
    return {
        "verdict": "PASS",
        "violations": [],
        "broker_mutation_authorized": False,
        "mt5_call_authorized": False,
        "entry_authorized": False,
        "close_authorized": False,
        "modify_authorized": False,
        "live_deployment_authorized": False,
        "trading_loop_authorized": False,
        "edge_inference_authorized": False,
        "canonical_canary": {
            "fill_price": 4728.4490000000005,
            "stop_loss": 4817.394,
        },
        "execution_observations": {
            "slippage_absolute": 0.082,
            "slippage_adverse_to_sell": True,
            "order_check_margin": 2.36,
            "comment_truncated": True,
            "fill_price": 4728.4490000000005,
            "stop_loss": 4817.394,
        },
        "lifecycle_observations": {
            "monitor_lifecycle_state": "open",
            "lifecycle_decision": "continue_hold",
        },
        "latest_mark_to_market": {
            "current_price": 4747.721,
            "floating_pl": -19.27,
            "swap": 0.0,
        },
    }


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "monitor_path": tmp_path / "reports" / "monitor.jsonl",
        "lifecycle_decision_path": tmp_path / "reports" / "lifecycle.jsonl",
        "observation_analysis_path": tmp_path / "reports" / "observation.jsonl",
    }
    _write_jsonl(paths["monitor_path"], [_monitor_record()])
    _write_jsonl(paths["lifecycle_decision_path"], [_lifecycle_record()])
    _write_jsonl(paths["observation_analysis_path"], [_observation_record()])
    return paths


def test_supervisory_state_continues_observing_open_canary(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)

    record = build_supervisory_state(**paths, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["supervisory_verdict"] == "PASS"
    assert record["supervisory_state"] == "continue_observe_open"
    assert record["operator_next_action"] == "refresh_read_only_monitor_lifecycle_observation_supervisor"
    assert record["violations"] == []
    assert record["human_review_recommended"] is False
    assert record["latest_mark_to_market"]["current_price"] == 4747.721
    assert record["latest_mark_to_market"]["floating_pl"] == -19.27
    assert record["latest_mark_to_market"]["adverse_price_move_from_fill"] == 19.272
    assert record["broker_mutation_authorized"] is False
    assert record["trading_loop_authorized"] is False
    assert record["automation_boundary"]["observation_automation_now_safe"] is True
    assert record["automation_boundary"]["broker_mutation_automation_now_safe"] is False
    assert record["automation_boundary"]["usd_jpy_requires_separate_broker_readiness"] is True


def test_supervisory_state_recommends_human_review_without_authorizing_close(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    observation = _observation_record()
    observation["latest_mark_to_market"]["current_price"] = 4775.0
    observation["latest_mark_to_market"]["floating_pl"] = -46.55
    _write_jsonl(paths["observation_analysis_path"], [observation])

    record = build_supervisory_state(**paths, manual_review_loss_usd=40.0, manual_review_adverse_price_move=45.0)

    assert record["supervisory_verdict"] == "REVIEW"
    assert record["supervisory_state"] == "human_review_recommended_no_code_mutation"
    assert record["human_review_recommended"] is True
    assert record["close_authorized"] is False
    assert record["broker_mutation_authorized"] is False
    assert len(record["review_triggers"]) >= 1


def test_supervisory_state_fails_on_lifecycle_mutation_authorization(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    lifecycle = _lifecycle_record()
    lifecycle["broker_mutation_authorized"] = True
    _write_jsonl(paths["lifecycle_decision_path"], [lifecycle])

    record = build_supervisory_state(**paths)

    assert record["supervisory_verdict"] == "FAIL"
    assert record["supervisory_state"] == "invalid_stop_and_investigate"
    assert any("broker_mutation_authorized must remain False" in violation for violation in record["violations"])


def test_supervisory_state_fails_on_observation_failure(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    observation = _observation_record()
    observation["verdict"] = "FAIL"
    observation["violations"] = ["missing current price"]
    _write_jsonl(paths["observation_analysis_path"], [observation])

    record = build_supervisory_state(**paths)

    assert record["supervisory_verdict"] == "FAIL"
    assert any("observation analysis verdict must be PASS" in violation for violation in record["violations"])


def test_supervisory_state_accepts_closed_explained_without_reentry(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    monitor = _monitor_record()
    monitor["lifecycle_state"] = "closed_explained"
    monitor["exact_open_canary_positions_found"] = 0
    _write_jsonl(paths["monitor_path"], [monitor])

    observation = _observation_record()
    observation["lifecycle_observations"]["monitor_lifecycle_state"] = "closed_explained"
    _write_jsonl(paths["observation_analysis_path"], [observation])

    record = build_supervisory_state(**paths)

    assert record["supervisory_verdict"] == "PASS"
    assert record["supervisory_state"] == "closed_explained_archive_no_reentry"
    assert record["entry_authorized"] is False


def test_supervisory_verifier_rejects_tampered_trading_loop_authorization(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    record = build_supervisory_state(**paths)
    record["trading_loop_authorized"] = True

    violations = verify_supervisory_state_record(record, require_pass=True)

    assert "trading_loop_authorized must be False" in violations


def test_supervisory_verifier_requires_automation_boundary(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    record = build_supervisory_state(**paths)
    record["automation_boundary"]["broker_mutation_automation_now_safe"] = True

    violations = verify_supervisory_state_record(record, require_pass=True)

    assert "broker_mutation_automation_now_safe must be False" in violations


def test_supervisory_module_is_local_file_analysis_only() -> None:
    source = Path("quantcore/execution/h024_one_shot_demo_canary_supervisory_state.py").read_text(encoding="utf-8")

    assert "import MetaTrader5" not in source
    assert "MetaTrader5 as" not in source
    assert "mt5." not in source
    assert ".order_check(" not in source
    assert ".order_send(" not in source

def test_supervisory_state_fails_on_observation_mutation_authorization(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    observation = _observation_record()
    observation["close_authorized"] = True
    _write_jsonl(paths["observation_analysis_path"], [observation])

    record = build_supervisory_state(**paths)

    assert record["supervisory_verdict"] == "FAIL"
    assert record["supervisory_state"] == "invalid_stop_and_investigate"
    assert any("close_authorized must remain False" in violation for violation in record["violations"])
