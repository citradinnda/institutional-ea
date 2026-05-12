from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MONITOR_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl")
DEFAULT_LIFECYCLE_DECISION_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_lifecycle_decision.jsonl")
DEFAULT_OBSERVATION_ANALYSIS_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_observation_analysis.jsonl")
DEFAULT_OUTPUT_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_supervisory_state.jsonl")

EXPECTED_CANARY = {
    "strategy": "H024",
    "server": "Exness-MT5Trial6",
    "runtime_symbol": "XAUUSDm",
    "model_symbol": "XAUUSD",
    "side": "sell",
    "volume": 0.01,
    "magic": 240024,
    "ticket": 4413054432,
    "identifier": 4413054432,
    "entry_deal": 3788869526,
    "fill_price": 4728.4490000000005,
    "stop_loss": 4817.394,
}

DEFAULT_MANUAL_REVIEW_LOSS_USD = 40.0
DEFAULT_MANUAL_REVIEW_ADVERSE_PRICE_MOVE = 45.0
ACCEPTED_MONITOR_STATES = {"open", "closed_explained"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    candidate = Path(path)
    if not candidate.exists():
        return []

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(candidate.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        loaded = json.loads(stripped)
        if not isinstance(loaded, dict):
            raise ValueError(f"{candidate}:{line_number} is not a JSON object")
        records.append(loaded)
    return records


def write_jsonl(path: str | Path, records: list[dict[str, Any]]) -> None:
    candidate = Path(path)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in records)
    candidate.write_text(payload, encoding="utf-8")


def _latest(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    return records[-1] if records else None


def _dig(record: Any, path: tuple[str, ...]) -> Any:
    current = record
    for key in path:
        if not isinstance(current, dict):
            return None
        if key not in current:
            return None
        current = current[key]
    return current


def _first(record: dict[str, Any] | None, paths: list[tuple[str, ...]]) -> Any:
    for path in paths:
        value = _dig(record, path)
        if value is not None:
            return value
    return None


def _find_key_recursive(value: Any, keys: set[str]) -> Any:
    if isinstance(value, dict):
        for key in keys:
            if key in value and value[key] is not None:
                return value[key]
        for child in value.values():
            found = _find_key_recursive(child, keys)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find_key_recursive(child, keys)
            if found is not None:
                return found
    return None


def _first_with_recursive_fallback(
    record: dict[str, Any] | None,
    paths: list[tuple[str, ...]],
    recursive_keys: set[str],
) -> Any:
    value = _first(record, paths)
    if value is not None:
        return value
    return _find_key_recursive(record, recursive_keys)


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"false", "0", "no", "n"}:
            return False
        if normalized in {"true", "1", "yes", "y"}:
            return True
    return None


def _violation_count(record: dict[str, Any] | None) -> int | None:
    raw = _first(record, [("violation_count",), ("violations_count",), ("violations",), ("summary", "violations")])
    if isinstance(raw, list):
        return len(raw)
    return _as_int(raw)


def _verdict(record: dict[str, Any] | None) -> Any:
    return _first(record, [("verdict",), ("summary", "verdict")])


def _monitor_state(monitor: dict[str, Any] | None, observation: dict[str, Any] | None) -> Any:
    return _first(
        monitor,
        [("lifecycle_state",), ("state",), ("summary", "lifecycle_state")],
    ) or _first(
        observation,
        [("lifecycle_observations", "monitor_lifecycle_state")],
    )


def _lifecycle_decision(lifecycle: dict[str, Any] | None, observation: dict[str, Any] | None) -> Any:
    return _first(
        lifecycle,
        [("decision",), ("summary", "decision")],
    ) or _first(
        observation,
        [("lifecycle_observations", "lifecycle_decision")],
    )


def _latest_mark_to_market(
    monitor: dict[str, Any] | None,
    lifecycle: dict[str, Any] | None,
    observation: dict[str, Any] | None,
) -> dict[str, float | None]:
    current_price = _first(
        observation,
        [("latest_mark_to_market", "current_price")],
    )
    if current_price is None:
        current_price = _first_with_recursive_fallback(
            monitor,
            [("current_price",), ("position", "price_current"), ("summary", "current_price")],
            {"current_price", "price_current"},
        )
    if current_price is None:
        current_price = _first_with_recursive_fallback(
            lifecycle,
            [("current_price",), ("position", "price_current"), ("summary", "current_price")],
            {"current_price", "price_current"},
        )

    floating_pl = _first(
        observation,
        [("latest_mark_to_market", "floating_pl")],
    )
    if floating_pl is None:
        floating_pl = _first_with_recursive_fallback(
            monitor,
            [("floating_pl",), ("floating_p_l",), ("floating_pnl",), ("floating_profit",), ("profit",), ("position", "profit")],
            {"floating_pl", "floating_p_l", "floating_pnl", "floating_profit", "profit"},
        )
    if floating_pl is None:
        floating_pl = _first_with_recursive_fallback(
            lifecycle,
            [("floating_pl",), ("floating_p_l",), ("floating_pnl",), ("floating_profit",), ("profit",), ("position", "profit")],
            {"floating_pl", "floating_p_l", "floating_pnl", "floating_profit", "profit"},
        )

    swap = _first(observation, [("latest_mark_to_market", "swap")])
    if swap is None:
        swap = _first_with_recursive_fallback(monitor, [("swap",), ("position", "swap")], {"swap"})
    if swap is None:
        swap = _first_with_recursive_fallback(lifecycle, [("swap",), ("position", "swap")], {"swap"})

    return {
        "current_price": _as_float(current_price),
        "floating_pl": _as_float(floating_pl),
        "swap": _as_float(swap),
    }


def _authorization_snapshot(
    lifecycle: dict[str, Any] | None,
    observation: dict[str, Any] | None,
) -> dict[str, bool | None]:
    fields = [
        "broker_mutation_authorized",
        "mt5_call_authorized",
        "entry_authorized",
        "close_authorized",
        "modify_authorized",
        "live_deployment_authorized",
        "trading_loop_authorized",
        "edge_inference_authorized",
    ]
    snapshot: dict[str, bool | None] = {}
    for field in fields:
        parsed_values = [
            _as_bool(_first(observation, [(field,)])),
            _as_bool(_first(observation, [("automation_boundary", field)])),
            _as_bool(_first(lifecycle, [(field,)])),
            _as_bool(_first(lifecycle, [("summary", field)])),
        ]
        present_values = [value for value in parsed_values if value is not None]

        if any(value is True for value in present_values):
            snapshot[field] = True
        elif any(value is False for value in present_values):
            snapshot[field] = False
        else:
            snapshot[field] = None

    return snapshot


def _observation_execution(observation: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "slippage_absolute": _as_float(_first(observation, [("execution_observations", "slippage_absolute")])),
        "slippage_adverse_to_sell": _as_bool(_first(observation, [("execution_observations", "slippage_adverse_to_sell")])),
        "order_check_margin": _as_float(_first(observation, [("execution_observations", "order_check_margin")])),
        "comment_truncated": _as_bool(_first(observation, [("execution_observations", "comment_truncated")])),
        "fill_price": _as_float(_first(observation, [("execution_observations", "fill_price"), ("canonical_canary", "fill_price")])),
        "stop_loss": _as_float(_first(observation, [("execution_observations", "stop_loss"), ("canonical_canary", "stop_loss")])),
    }


def build_supervisory_state(
    *,
    monitor_path: str | Path = DEFAULT_MONITOR_PATH,
    lifecycle_decision_path: str | Path = DEFAULT_LIFECYCLE_DECISION_PATH,
    observation_analysis_path: str | Path = DEFAULT_OBSERVATION_ANALYSIS_PATH,
    manual_review_loss_usd: float = DEFAULT_MANUAL_REVIEW_LOSS_USD,
    manual_review_adverse_price_move: float = DEFAULT_MANUAL_REVIEW_ADVERSE_PRICE_MOVE,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    monitor_path = Path(monitor_path)
    lifecycle_decision_path = Path(lifecycle_decision_path)
    observation_analysis_path = Path(observation_analysis_path)

    monitor_records = read_jsonl(monitor_path)
    lifecycle_records = read_jsonl(lifecycle_decision_path)
    observation_records = read_jsonl(observation_analysis_path)

    monitor = _latest(monitor_records)
    lifecycle = _latest(lifecycle_records)
    observation = _latest(observation_records)

    monitor_verdict = _verdict(monitor)
    lifecycle_verdict = _verdict(lifecycle)
    observation_verdict = _verdict(observation)

    monitor_violations = _violation_count(monitor)
    lifecycle_violations = _violation_count(lifecycle)
    observation_violations = _violation_count(observation)

    monitor_state = _monitor_state(monitor, observation)
    decision = _lifecycle_decision(lifecycle, observation)
    mark_to_market = _latest_mark_to_market(monitor, lifecycle, observation)
    authorization = _authorization_snapshot(lifecycle, observation)
    execution = _observation_execution(observation)

    violations: list[str] = []

    if not monitor_records:
        violations.append(f"missing monitor records at {monitor_path}")
    if not lifecycle_records:
        violations.append(f"missing lifecycle decision records at {lifecycle_decision_path}")
    if not observation_records:
        violations.append(f"missing observation analysis records at {observation_analysis_path}")

    if monitor_verdict != "PASS":
        violations.append(f"monitor verdict must be PASS, observed {monitor_verdict!r}")
    if lifecycle_verdict != "PASS":
        violations.append(f"lifecycle decision verdict must be PASS, observed {lifecycle_verdict!r}")
    if observation_verdict != "PASS":
        violations.append(f"observation analysis verdict must be PASS, observed {observation_verdict!r}")

    if monitor_violations not in {0, None}:
        violations.append(f"monitor violation count must be 0, observed {monitor_violations!r}")
    if lifecycle_violations not in {0, None}:
        violations.append(f"lifecycle violation count must be 0, observed {lifecycle_violations!r}")
    if observation_violations not in {0, None}:
        violations.append(f"observation analysis violation count must be 0, observed {observation_violations!r}")

    if monitor_state not in ACCEPTED_MONITOR_STATES:
        violations.append(f"monitor lifecycle state must be one of {sorted(ACCEPTED_MONITOR_STATES)!r}, observed {monitor_state!r}")
    if decision != "continue_hold":
        violations.append(f"lifecycle decision must be continue_hold, observed {decision!r}")

    for field, value in authorization.items():
        if value is True:
            violations.append(f"{field} must remain False, observed True")

    if monitor_state == "open":
        for field in ["current_price", "floating_pl", "swap"]:
            if mark_to_market[field] is None:
                violations.append(f"open monitor state must expose {field}")

    fill_price = execution["fill_price"] if execution["fill_price"] is not None else EXPECTED_CANARY["fill_price"]
    stop_loss = execution["stop_loss"] if execution["stop_loss"] is not None else EXPECTED_CANARY["stop_loss"]
    current_price = mark_to_market["current_price"]

    adverse_price_move_from_fill = None
    stop_distance_from_fill = None
    adverse_move_fraction_of_stop = None
    if current_price is not None and fill_price is not None:
        adverse_price_move_from_fill = round(current_price - fill_price, 6)
    if stop_loss is not None and fill_price is not None:
        stop_distance_from_fill = round(stop_loss - fill_price, 6)
    if adverse_price_move_from_fill is not None and stop_distance_from_fill not in {None, 0.0}:
        adverse_move_fraction_of_stop = round(adverse_price_move_from_fill / stop_distance_from_fill, 6)

    review_triggers: list[str] = []
    floating_pl = mark_to_market["floating_pl"]
    if monitor_state == "open" and floating_pl is not None and floating_pl <= -abs(manual_review_loss_usd):
        review_triggers.append(
            f"floating P/L {floating_pl} crossed manual review loss threshold {-abs(manual_review_loss_usd)}"
        )
    if (
        monitor_state == "open"
        and adverse_price_move_from_fill is not None
        and adverse_price_move_from_fill >= manual_review_adverse_price_move
    ):
        review_triggers.append(
            f"adverse price move from fill {adverse_price_move_from_fill} crossed manual review threshold {manual_review_adverse_price_move}"
        )

    human_review_recommended = bool(review_triggers)

    if violations:
        supervisory_state = "invalid_stop_and_investigate"
        operator_next_action = "stop_and_investigate_local_artifacts_no_broker_mutation"
        supervisory_verdict = "FAIL"
    elif human_review_recommended:
        supervisory_state = "human_review_recommended_no_code_mutation"
        operator_next_action = "human_review_risk_state_manual_mt5_management_allowed_no_code_close"
        supervisory_verdict = "REVIEW"
    elif monitor_state == "open":
        supervisory_state = "continue_observe_open"
        operator_next_action = "refresh_read_only_monitor_lifecycle_observation_supervisor"
        supervisory_verdict = "PASS"
    elif monitor_state == "closed_explained":
        supervisory_state = "closed_explained_archive_no_reentry"
        operator_next_action = "archive_post_canary_evidence_no_reentry"
        supervisory_verdict = "PASS"
    else:
        supervisory_state = "invalid_stop_and_investigate"
        operator_next_action = "stop_and_investigate_local_artifacts_no_broker_mutation"
        supervisory_verdict = "FAIL"

    return {
        "schema_version": 1,
        "record_type": "h024_one_shot_demo_canary_supervisory_state",
        "generated_at_utc": generated_at_utc or utc_now_iso(),
        "strategy": "H024",
        "supervisory_verdict": supervisory_verdict,
        "supervisory_state": supervisory_state,
        "operator_next_action": operator_next_action,
        "violations": violations,
        "review_triggers": review_triggers,
        "human_review_recommended": human_review_recommended,
        "manual_review_thresholds": {
            "floating_loss_usd": abs(manual_review_loss_usd),
            "adverse_price_move_from_fill": manual_review_adverse_price_move,
        },
        "broker_mutation_authorized": False,
        "mt5_call_authorized": False,
        "entry_authorized": False,
        "close_authorized": False,
        "modify_authorized": False,
        "live_deployment_authorized": False,
        "trading_loop_authorized": False,
        "edge_inference_authorized": False,
        "canonical_canary": EXPECTED_CANARY,
        "source_files": {
            "monitor": {"path": str(monitor_path), "exists": monitor_path.exists(), "records": len(monitor_records), "verdict": monitor_verdict},
            "lifecycle_decision": {"path": str(lifecycle_decision_path), "exists": lifecycle_decision_path.exists(), "records": len(lifecycle_records), "verdict": lifecycle_verdict},
            "observation_analysis": {"path": str(observation_analysis_path), "exists": observation_analysis_path.exists(), "records": len(observation_records), "verdict": observation_verdict},
        },
        "state_inputs": {
            "monitor_lifecycle_state": monitor_state,
            "lifecycle_decision": decision,
            "monitor_violations": monitor_violations,
            "lifecycle_violations": lifecycle_violations,
            "observation_violations": observation_violations,
        },
        "latest_mark_to_market": {
            "current_price": mark_to_market["current_price"],
            "floating_pl": mark_to_market["floating_pl"],
            "swap": mark_to_market["swap"],
            "adverse_price_move_from_fill": adverse_price_move_from_fill,
            "stop_distance_from_fill": stop_distance_from_fill,
            "adverse_move_fraction_of_stop": adverse_move_fraction_of_stop,
            "note": "For this sell canary, positive adverse_price_move_from_fill means price is above fill.",
        },
        "execution_observations": execution,
        "automation_boundary": {
            "observation_automation_now_safe": True,
            "broker_mutation_automation_now_safe": False,
            "usd_jpy_requires_separate_broker_readiness": True,
            "summary": "Automate read-only supervision before any mutation automation. USDJPY belongs in H024, but must pass its own broker-symbol readiness and canary governance rather than piggybacking on the XAUUSDm canary.",
        },
    }


def verify_supervisory_state_record(record: dict[str, Any], *, require_pass: bool = False) -> list[str]:
    violations: list[str] = []

    if record.get("record_type") != "h024_one_shot_demo_canary_supervisory_state":
        violations.append(f"unexpected record_type: {record.get('record_type')!r}")

    for field in [
        "broker_mutation_authorized",
        "mt5_call_authorized",
        "entry_authorized",
        "close_authorized",
        "modify_authorized",
        "live_deployment_authorized",
        "trading_loop_authorized",
        "edge_inference_authorized",
    ]:
        if record.get(field) is not False:
            violations.append(f"{field} must be False")

    embedded_violations = record.get("violations")
    if not isinstance(embedded_violations, list):
        violations.append("violations field must be a list")
    elif embedded_violations:
        violations.extend(f"embedded violation: {violation}" for violation in embedded_violations)

    state = record.get("supervisory_state")
    if state not in {
        "continue_observe_open",
        "human_review_recommended_no_code_mutation",
        "closed_explained_archive_no_reentry",
        "invalid_stop_and_investigate",
    }:
        violations.append(f"unexpected supervisory_state: {state!r}")

    if require_pass and record.get("supervisory_verdict") != "PASS":
        violations.append(f"supervisory_verdict must be PASS, observed {record.get('supervisory_verdict')!r}")

    boundary = record.get("automation_boundary", {})
    if not isinstance(boundary, dict):
        violations.append("automation_boundary must be an object")
    else:
        if boundary.get("observation_automation_now_safe") is not True:
            violations.append("observation_automation_now_safe must be True")
        if boundary.get("broker_mutation_automation_now_safe") is not False:
            violations.append("broker_mutation_automation_now_safe must be False")
        if boundary.get("usd_jpy_requires_separate_broker_readiness") is not True:
            violations.append("usd_jpy_requires_separate_broker_readiness must be True")

    if record.get("supervisory_state") == "continue_observe_open":
        mtm = record.get("latest_mark_to_market", {})
        if not isinstance(mtm, dict):
            violations.append("latest_mark_to_market must be an object")
        else:
            for field in ["current_price", "floating_pl", "swap"]:
                if _as_float(mtm.get(field)) is None:
                    violations.append(f"continue_observe_open requires latest_mark_to_market.{field}")

    return violations
