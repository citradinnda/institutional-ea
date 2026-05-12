from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_LEDGER_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_ledger.jsonl")
DEFAULT_POST_ORDER_AUDIT_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_post_order_audit.jsonl")
DEFAULT_MONITOR_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl")
DEFAULT_LIFECYCLE_DECISION_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_lifecycle_decision.jsonl")
DEFAULT_OUTPUT_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_observation_analysis.jsonl")

EXPECTED_CANARY: dict[str, Any] = {
    "strategy": "H024",
    "allowed_demo_server": "Exness-MT5Trial6",
    "account_currency": "USD",
    "runtime_symbol": "XAUUSDm",
    "model_symbol": "XAUUSD",
    "side": "sell",
    "type": 1,
    "volume": 0.01,
    "magic": 240024,
    "order": 4413054432,
    "ticket": 4413054432,
    "identifier": 4413054432,
    "deal": 3788869526,
    "request_id": 3072064830,
    "request_comment": "H024_ONE_SHOT_DEMO_CANARY",
    "stored_comment": "H024_ONE_SHOT_DE",
    "requested_price": 4728.367,
    "fill_price": 4728.4490000000005,
    "stop_loss": 4817.394,
    "order_check_retcode": 0,
    "order_send_retcode": 10009,
    "order_check_margin": 2.36,
}

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


def _dig(record: dict[str, Any] | None, path: tuple[str, ...]) -> Any:
    current: Any = record
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


def _find_successful_canary_record(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    for record in reversed(records):
        attempt_stage = record.get("attempt_stage")
        retcode = _as_int(_dig(record, ("order_send_result", "retcode")))
        order = _as_int(_dig(record, ("order_send_result", "order")))
        deal = _as_int(_dig(record, ("order_send_result", "deal")))
        if attempt_stage == "send_succeeded" and retcode == EXPECTED_CANARY["order_send_retcode"]:
            return record
        if retcode == EXPECTED_CANARY["order_send_retcode"] and order == EXPECTED_CANARY["order"] and deal == EXPECTED_CANARY["deal"]:
            return record
    return None


def _append_equal_violation(violations: list[str], name: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        violations.append(f"{name} mismatch: expected {expected!r}, observed {actual!r}")


def _append_float_violation(
    violations: list[str],
    name: str,
    actual: Any,
    expected: float,
    tolerance: float = 1e-9,
) -> None:
    actual_float = _as_float(actual)
    if actual_float is None or abs(actual_float - expected) > tolerance:
        violations.append(f"{name} mismatch: expected {expected!r}, observed {actual!r}")


def _latest_record(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    return records[-1] if records else None


def build_observation_analysis(
    *,
    ledger_path: str | Path = DEFAULT_LEDGER_PATH,
    post_order_audit_path: str | Path = DEFAULT_POST_ORDER_AUDIT_PATH,
    monitor_path: str | Path = DEFAULT_MONITOR_PATH,
    lifecycle_decision_path: str | Path = DEFAULT_LIFECYCLE_DECISION_PATH,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    ledger_path = Path(ledger_path)
    post_order_audit_path = Path(post_order_audit_path)
    monitor_path = Path(monitor_path)
    lifecycle_decision_path = Path(lifecycle_decision_path)

    ledger_records = read_jsonl(ledger_path)
    post_order_audit_records = read_jsonl(post_order_audit_path)
    monitor_records = read_jsonl(monitor_path)
    lifecycle_decision_records = read_jsonl(lifecycle_decision_path)

    successful_canary = _find_successful_canary_record(ledger_records)
    post_order_audit = _latest_record(post_order_audit_records)
    monitor = _latest_record(monitor_records)
    lifecycle_decision = _latest_record(lifecycle_decision_records)

    violations: list[str] = []

    if not ledger_records:
        violations.append(f"missing ledger records at {ledger_path}")
    if not post_order_audit_records:
        violations.append(f"missing post-order audit records at {post_order_audit_path}")
    if not monitor_records:
        violations.append(f"missing monitor records at {monitor_path}")
    if not lifecycle_decision_records:
        violations.append(f"missing lifecycle decision records at {lifecycle_decision_path}")

    if successful_canary is None:
        violations.append("no successful H024 canary ledger record found")
    else:
        request = successful_canary.get("request", {})
        order_check_result = successful_canary.get("order_check_result", {})
        order_send_result = successful_canary.get("order_send_result", {})

        _append_equal_violation(violations, "strategy", successful_canary.get("strategy"), EXPECTED_CANARY["strategy"])
        _append_equal_violation(violations, "allowed_demo_server", successful_canary.get("allowed_demo_server"), EXPECTED_CANARY["allowed_demo_server"])
        _append_equal_violation(violations, "symbol", successful_canary.get("symbol"), EXPECTED_CANARY["runtime_symbol"])
        _append_equal_violation(violations, "request.symbol", request.get("symbol"), EXPECTED_CANARY["runtime_symbol"])
        _append_equal_violation(violations, "request.magic", _as_int(request.get("magic")), EXPECTED_CANARY["magic"])
        _append_equal_violation(violations, "request.type", _as_int(request.get("type")), EXPECTED_CANARY["type"])
        _append_float_violation(violations, "request.volume", request.get("volume"), EXPECTED_CANARY["volume"])
        _append_float_violation(violations, "request.price", request.get("price"), EXPECTED_CANARY["requested_price"])
        _append_float_violation(violations, "request.sl", request.get("sl"), EXPECTED_CANARY["stop_loss"])
        _append_equal_violation(violations, "request.comment", request.get("comment"), EXPECTED_CANARY["request_comment"])
        _append_equal_violation(violations, "order_check_result.retcode", _as_int(order_check_result.get("retcode")), EXPECTED_CANARY["order_check_retcode"])
        _append_float_violation(violations, "order_check_result.margin", order_check_result.get("margin"), EXPECTED_CANARY["order_check_margin"])
        _append_equal_violation(violations, "order_send_result.retcode", _as_int(order_send_result.get("retcode")), EXPECTED_CANARY["order_send_retcode"])
        _append_equal_violation(violations, "order_send_result.order", _as_int(order_send_result.get("order")), EXPECTED_CANARY["order"])
        _append_equal_violation(violations, "order_send_result.deal", _as_int(order_send_result.get("deal")), EXPECTED_CANARY["deal"])
        _append_equal_violation(violations, "order_send_result.request_id", _as_int(order_send_result.get("request_id")), EXPECTED_CANARY["request_id"])
        _append_float_violation(violations, "order_send_result.price", order_send_result.get("price"), EXPECTED_CANARY["fill_price"])
        _append_float_violation(violations, "order_send_result.volume", order_send_result.get("volume"), EXPECTED_CANARY["volume"])
        _append_equal_violation(violations, "order_send_result.comment", order_send_result.get("comment"), EXPECTED_CANARY["stored_comment"])

    post_order_verdict = _first(post_order_audit, [("verdict",), ("summary", "verdict")])
    post_order_violations = _violation_count(post_order_audit)
    post_order_open_count = _first(
        post_order_audit,
        [
            ("open_canary_positions_found",),
            ("open_positions_found",),
            ("exact_open_canary_positions_found",),
            ("summary", "open_canary_positions_found"),
        ],
    )

    if post_order_audit is not None:
        if post_order_verdict != "PASS":
            violations.append(f"post-order audit verdict must be PASS, observed {post_order_verdict!r}")
        if post_order_violations not in {0, None}:
            violations.append(f"post-order audit violation count must be 0, observed {post_order_violations!r}")
        if _as_int(post_order_open_count) not in {1, None}:
            violations.append(f"post-order audit open canary count must be 1, observed {post_order_open_count!r}")

    monitor_verdict = _first(monitor, [("verdict",), ("summary", "verdict")])
    monitor_violations = _violation_count(monitor)
    monitor_state = _first(monitor, [("lifecycle_state",), ("state",), ("summary", "lifecycle_state")])
    monitor_exact_open_count = _first(
        monitor,
        [
            ("exact_open_canary_positions_found",),
            ("exact_open_positions_found",),
            ("summary", "exact_open_canary_positions_found"),
        ],
    )
    monitor_pending_count = _first(
        monitor,
        [
            ("unexpected_h024_pending_orders_found",),
            ("unexpected_pending_orders_found",),
            ("summary", "unexpected_h024_pending_orders_found"),
        ],
    )
    monitor_ledger_success_count = _first(
        monitor,
        [
            ("ledger_successful_canary_records_found",),
            ("successful_canary_ledger_records_found",),
            ("summary", "ledger_successful_canary_records_found"),
        ],
    )
    monitor_current_price = _first_with_recursive_fallback(
        monitor,
        [("current_price",), ("position", "price_current"), ("summary", "current_price")],
        {"current_price", "price_current"},
    )
    if monitor_current_price is None:
        monitor_current_price = _first_with_recursive_fallback(
            lifecycle_decision,
            [("current_price",), ("position", "price_current"), ("summary", "current_price")],
            {"current_price", "price_current"},
        )

    monitor_floating_pl = _first_with_recursive_fallback(
        monitor,
        [("floating_pl",), ("floating_p_l",), ("floating_pnl",), ("floating_profit",), ("profit",), ("position", "profit"), ("summary", "floating_pl")],
        {"floating_pl", "floating_p_l", "floating_pnl", "floating_profit", "profit"},
    )
    if monitor_floating_pl is None:
        monitor_floating_pl = _first_with_recursive_fallback(
            lifecycle_decision,
            [("floating_pl",), ("floating_p_l",), ("floating_pnl",), ("floating_profit",), ("profit",), ("position", "profit"), ("summary", "floating_pl")],
            {"floating_pl", "floating_p_l", "floating_pnl", "floating_profit", "profit"},
        )

    monitor_swap = _first_with_recursive_fallback(
        monitor,
        [("swap",), ("position", "swap"), ("summary", "swap")],
        {"swap"},
    )
    if monitor_swap is None:
        monitor_swap = _first_with_recursive_fallback(
            lifecycle_decision,
            [("swap",), ("position", "swap"), ("summary", "swap")],
            {"swap"},
        )

    if monitor is not None:
        if monitor_verdict != "PASS":
            violations.append(f"monitor verdict must be PASS, observed {monitor_verdict!r}")
        if monitor_violations not in {0, None}:
            violations.append(f"monitor violation count must be 0, observed {monitor_violations!r}")
        if monitor_state not in ACCEPTED_MONITOR_STATES:
            violations.append(f"monitor lifecycle state must be one of {sorted(ACCEPTED_MONITOR_STATES)!r}, observed {monitor_state!r}")
        if _as_int(monitor_pending_count) not in {0, None}:
            violations.append(f"unexpected H024 pending order count must be 0, observed {monitor_pending_count!r}")
        if _as_int(monitor_ledger_success_count) not in {1, None}:
            violations.append(f"successful canary ledger count must be 1, observed {monitor_ledger_success_count!r}")
        if monitor_state == "open":
            if _as_float(monitor_current_price) is None:
                violations.append("open monitor state must expose a current price")
            if _as_float(monitor_floating_pl) is None:
                violations.append("open monitor state must expose floating P/L")
            if _as_float(monitor_swap) is None:
                violations.append("open monitor state must expose swap")

    lifecycle_verdict = _first(lifecycle_decision, [("verdict",), ("summary", "verdict")])
    lifecycle_violations = _violation_count(lifecycle_decision)
    lifecycle_decision_value = _first(lifecycle_decision, [("decision",), ("summary", "decision")])
    broker_mutation_authorized = _first(lifecycle_decision, [("broker_mutation_authorized",), ("summary", "broker_mutation_authorized")])
    call_authorized = _first(lifecycle_decision, [("mt5_call_authorized",), ("call_authorized",), ("summary", "mt5_call_authorized")])
    close_authorized = _first(lifecycle_decision, [("close_authorized",), ("summary", "close_authorized")])
    modify_authorized = _first(lifecycle_decision, [("modify_authorized",), ("summary", "modify_authorized")])
    entry_authorized = _first(lifecycle_decision, [("entry_authorized",), ("summary", "entry_authorized")])
    live_deployment_authorized = _first(lifecycle_decision, [("live_deployment_authorized",), ("summary", "live_deployment_authorized")])

    if lifecycle_decision is not None:
        if lifecycle_verdict != "PASS":
            violations.append(f"lifecycle decision verdict must be PASS, observed {lifecycle_verdict!r}")
        if lifecycle_violations not in {0, None}:
            violations.append(f"lifecycle decision violation count must be 0, observed {lifecycle_violations!r}")
        if lifecycle_decision_value != "continue_hold":
            violations.append(f"lifecycle decision must be continue_hold, observed {lifecycle_decision_value!r}")
        for field_name, raw_value in {
            "broker_mutation_authorized": broker_mutation_authorized,
            "mt5_call_authorized": call_authorized,
            "close_authorized": close_authorized,
            "modify_authorized": modify_authorized,
            "entry_authorized": entry_authorized,
            "live_deployment_authorized": live_deployment_authorized,
        }.items():
            parsed = _as_bool(raw_value)
            if parsed is True:
                violations.append(f"lifecycle {field_name} must remain False, observed {raw_value!r}")

    requested_price = _as_float(_dig(successful_canary, ("request", "price")) if successful_canary else None)
    fill_price = _as_float(_dig(successful_canary, ("order_send_result", "price")) if successful_canary else None)
    stop_loss = _as_float(_dig(successful_canary, ("request", "sl")) if successful_canary else None)

    slippage_absolute = None
    slippage_adverse_to_sell = None
    if requested_price is not None and fill_price is not None:
        slippage_absolute = round(fill_price - requested_price, 6)
        slippage_adverse_to_sell = slippage_absolute > 0

    stop_distance_from_request = None
    stop_distance_from_fill = None
    if requested_price is not None and stop_loss is not None:
        stop_distance_from_request = round(stop_loss - requested_price, 6)
    if fill_price is not None and stop_loss is not None:
        stop_distance_from_fill = round(stop_loss - fill_price, 6)

    request_comment = _dig(successful_canary, ("request", "comment")) if successful_canary else None
    stored_comment = _dig(successful_canary, ("order_send_result", "comment")) if successful_canary else None
    comment_truncated = bool(
        isinstance(request_comment, str)
        and isinstance(stored_comment, str)
        and request_comment != stored_comment
        and request_comment.startswith(stored_comment)
    )

    record: dict[str, Any] = {
        "schema_version": 1,
        "record_type": "h024_one_shot_demo_canary_observation_analysis",
        "generated_at_utc": generated_at_utc or utc_now_iso(),
        "strategy": "H024",
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
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
            "ledger": {"path": str(ledger_path), "records": len(ledger_records), "exists": ledger_path.exists()},
            "post_order_audit": {"path": str(post_order_audit_path), "records": len(post_order_audit_records), "exists": post_order_audit_path.exists()},
            "monitor": {"path": str(monitor_path), "records": len(monitor_records), "exists": monitor_path.exists()},
            "lifecycle_decision": {"path": str(lifecycle_decision_path), "records": len(lifecycle_decision_records), "exists": lifecycle_decision_path.exists()},
        },
        "execution_observations": {
            "requested_price": requested_price,
            "fill_price": fill_price,
            "slippage_absolute": slippage_absolute,
            "slippage_unit": "price",
            "slippage_interpretation": "positive means fill above requested price; adverse for this sell canary",
            "slippage_adverse_to_sell": slippage_adverse_to_sell,
            "stop_loss": stop_loss,
            "stop_distance_from_request": stop_distance_from_request,
            "stop_distance_from_fill": stop_distance_from_fill,
            "order_check_retcode": _as_int(_dig(successful_canary, ("order_check_result", "retcode")) if successful_canary else None),
            "order_send_retcode": _as_int(_dig(successful_canary, ("order_send_result", "retcode")) if successful_canary else None),
            "order_check_margin": _as_float(_dig(successful_canary, ("order_check_result", "margin")) if successful_canary else None),
            "request_id": _as_int(_dig(successful_canary, ("order_send_result", "request_id")) if successful_canary else None),
            "request_comment": request_comment,
            "stored_comment": stored_comment,
            "comment_truncated": comment_truncated,
        },
        "lifecycle_observations": {
            "post_order_audit_verdict": post_order_verdict,
            "post_order_audit_violations": post_order_violations,
            "post_order_audit_open_canary_positions_found": _as_int(post_order_open_count),
            "monitor_verdict": monitor_verdict,
            "monitor_violations": monitor_violations,
            "monitor_lifecycle_state": monitor_state,
            "monitor_exact_open_canary_positions_found": _as_int(monitor_exact_open_count),
            "monitor_unexpected_h024_pending_orders_found": _as_int(monitor_pending_count),
            "monitor_ledger_successful_canary_records_found": _as_int(monitor_ledger_success_count),
            "lifecycle_decision_verdict": lifecycle_verdict,
            "lifecycle_decision_violations": lifecycle_violations,
            "lifecycle_decision": lifecycle_decision_value,
            "lifecycle_broker_mutation_authorized": _as_bool(broker_mutation_authorized),
            "lifecycle_mt5_call_authorized": _as_bool(call_authorized),
            "lifecycle_close_authorized": _as_bool(close_authorized),
            "lifecycle_modify_authorized": _as_bool(modify_authorized),
            "lifecycle_entry_authorized": _as_bool(entry_authorized),
            "lifecycle_live_deployment_authorized": _as_bool(live_deployment_authorized),
        },
        "latest_mark_to_market": {
            "current_price": _as_float(monitor_current_price),
            "floating_pl": _as_float(monitor_floating_pl),
            "swap": _as_float(monitor_swap),
            "note": "Mark-to-market values are observational and change with broker price.",
        },
        "engineering_interpretation": {
            "plumbing_validated": True,
            "strategy_edge_validated": False,
            "single_canary_is_edge_evidence": False,
            "safe_next_mode": "read_only_observation_or_separately_governed_close_only",
            "summary": "The one-shot standard-demo canary validates request construction, terminal connectivity, broker acceptance, ledgering, read-only monitoring, and lifecycle refusal to mutate. It does not validate H024 strategy edge or live readiness.",
        },
    }

    return record


def verify_observation_analysis_record(record: dict[str, Any], *, require_pass: bool = False) -> list[str]:
    violations: list[str] = []

    if record.get("record_type") != "h024_one_shot_demo_canary_observation_analysis":
        violations.append(f"unexpected record_type: {record.get('record_type')!r}")

    for field_name in [
        "broker_mutation_authorized",
        "mt5_call_authorized",
        "entry_authorized",
        "close_authorized",
        "modify_authorized",
        "live_deployment_authorized",
        "trading_loop_authorized",
        "edge_inference_authorized",
    ]:
        if record.get(field_name) is not False:
            violations.append(f"{field_name} must be False")

    embedded_violations = record.get("violations")
    if not isinstance(embedded_violations, list):
        violations.append("record violations field must be a list")
    elif embedded_violations:
        violations.extend(f"embedded violation: {item}" for item in embedded_violations)

    if require_pass and record.get("verdict") != "PASS":
        violations.append(f"verdict must be PASS, observed {record.get('verdict')!r}")

    interpretation = record.get("engineering_interpretation", {})
    if not isinstance(interpretation, dict):
        violations.append("engineering_interpretation must be an object")
    else:
        if interpretation.get("plumbing_validated") is not True:
            violations.append("plumbing_validated must be True")
        if interpretation.get("strategy_edge_validated") is not False:
            violations.append("strategy_edge_validated must be False")
        if interpretation.get("single_canary_is_edge_evidence") is not False:
            violations.append("single_canary_is_edge_evidence must be False")

    return violations