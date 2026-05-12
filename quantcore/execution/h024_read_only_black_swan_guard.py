from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


SCHEMA_VERSION = "1.0"
STRATEGY = "H024"
PACKET_TYPE = "h024_read_only_black_swan_guard"

PASS_OPERATOR_STATE = "BLACK_SWAN_GUARD_CLEAR_BUT_TRADING_NOT_AUTHORIZED"
PASS_OPERATOR_NEXT_ACTION = "CONTINUE_READ_ONLY_SUPERVISION_NO_TRADING_AUTHORIZED"
FAIL_OPERATOR_STATE = "FAIL_CLOSED_BLACK_SWAN_GUARD_ACTIVE_OR_UNVERIFIED_NO_TRADING_AUTHORIZED"
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_RUNTIME_SYMBOL = "XAUUSDm"
EXPECTED_MODEL_SYMBOL = "XAUUSD"
EXPECTED_MAGIC = 240024
EXPECTED_VOLUME = 0.01
EXPECTED_POSITION_TYPE = 1

DEFAULT_MAX_UPSTREAM_AGE_SECONDS = 3600
DEFAULT_EXTREME_SPREAD_LIMIT = 1000.0
DEFAULT_MIN_MARGIN_LEVEL = 100.0
DEFAULT_MIN_EQUITY_TO_BALANCE_RATIO = 0.20

AUTHORIZATION_KEYS = (
    "broker_mutation_authorized",
    "order_check_authorized",
    "order_send_authorized",
    "entry_authorized",
    "close_modify_authorized",
    "xauusd_order_authorized",
    "usdjpy_order_authorized",
    "trading_loop_authorized",
    "automatic_execution_authorized",
    "operator_decision_v2_preview_authorizes_action",
    "manual_approval_gate_preview_authorizes_action",
    "execution_readiness_dry_run_schema_preview_authorizes_execution",
    "dry_run_request_shape_preview_authorizes_execution",
    "black_swan_guard_authorizes_trading",
    "black_swan_guard_authorizes_broker_mutation",
    "black_swan_guard_authorizes_close_modify",
    "live_broker_request_constructed",
    "executable_trade_request_constructed",
    "mt5_request_dictionary_constructed",
    "order_check_planned",
    "order_send_planned",
    "symbol_select_planned",
)

EXPECTED_FALSE_TOP_LEVEL_FIELDS = (
    "broker_mutation_authorized",
    "order_check_authorized",
    "order_send_authorized",
    "entry_authorized",
    "close_modify_authorized",
    "xauusd_order_authorized",
    "usdjpy_order_authorized",
    "trading_loop_authorized",
    "automatic_execution_authorized",
    "black_swan_guard_authorizes_trading",
    "black_swan_guard_authorizes_broker_mutation",
    "black_swan_guard_authorizes_close_modify",
    "live_broker_request_constructed",
    "executable_trade_request_constructed",
    "mt5_request_dictionary_constructed",
    "order_check_planned",
    "order_send_planned",
    "symbol_select_planned",
)

FORBIDDEN_EXECUTABLE_OBJECT_KEYS = {
    "live_broker_request",
    "broker_request",
    "trade_request",
    "executable_trade_request",
    "mt5_request",
    "mt5_request_dictionary",
    "order_check_request",
    "order_send_request",
}

LOCKOUT_ACTIVE_KEYS = {
    "global_no_new_entry_lockout_active",
    "global_no_new_entry_active",
    "manual_override_lockout_active",
    "manual_lockout_active",
    "xauusd_no_new_entry_lockout_active",
    "xauusd_no_new_entry_active",
    "usdjpy_no_new_entry_lockout_active",
    "usdjpy_no_new_entry_active",
    "lockout_active",
}

UPSTREAM_SPECS: Mapping[str, tuple[str, ...]] = {
    "runtime_heartbeat": (
        "h024_runtime_safety_heartbeat.jsonl",
        "*runtime*heartbeat*.jsonl",
        "*heartbeat*.jsonl",
    ),
    "runtime_lockout_reader": (
        "h024_runtime_safety_lockout.jsonl",
        "*runtime*safety*lockout*.jsonl",
        "*lockout*.jsonl",
    ),
    "runtime_tick_spread": (
        "h024_runtime_tick_spread_safety_supervisor.jsonl",
        "h024_runtime_tick_and_spread_safety_supervisor.jsonl",
        "*tick*spread*.jsonl",
    ),
    "runtime_exposure_inventory": (
        "h024_runtime_exposure_inventory_safety_supervisor.jsonl",
        "*exposure*inventory*.jsonl",
    ),
    "runtime_account_risk_margin": (
        "h024_runtime_account_risk_margin_safety_supervisor.jsonl",
        "*account*risk*margin*.jsonl",
    ),
    "runtime_safety_aggregate": (
        "h024_runtime_safety_aggregate_supervisor.jsonl",
        "*runtime*safety*aggregate*.jsonl",
    ),
    "unified_read_only_runtime_supervision": (
        "h024_unified_read_only_runtime_supervision.jsonl",
        "*unified*runtime*supervision*.jsonl",
    ),
    "runtime_no_mutation_safety_gate": (
        "h024_runtime_no_mutation_safety_gate.jsonl",
        "*no_mutation*safety_gate*.jsonl",
    ),
    "exact_ticket_close_modify_governance": (
        "h024_exact_ticket_canary_close_modify_governance.jsonl",
        "*exact_ticket*close*modify*governance*.jsonl",
        "*exact_ticket*governance*.jsonl",
    ),
    "exact_ticket_decision_artifact_validator": (
        "h024_exact_ticket_canary_close_modify_decision_artifact.jsonl",
        "*close*modify*decision_artifact*.jsonl",
    ),
    "pre_action_evidence_aggregate": (
        "h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl",
        "*pre_action_evidence_aggregate*.jsonl",
    ),
    "bar_age_exit_condition_evidence": (
        "h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl",
        "*bar_age_exit_condition_evidence*.jsonl",
    ),
    "manual_approval_gate_preview": (
        "h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl",
        "*manual_approval_gate_preview*.jsonl",
    ),
    "operator_decision_v2_preview": (
        "h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl",
        "*operator_decision_v2_preview*.jsonl",
    ),
    "execution_readiness_dry_run_schema_preview": (
        "h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl",
        "*execution_readiness_dry_run_schema_preview*.jsonl",
    ),
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iter_key_values(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield key, item
            yield from iter_key_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_key_values(item)


def first_key_value(value: Any, keys: Iterable[str]) -> Any:
    wanted = set(keys)
    for key, item in iter_key_values(value):
        if key in wanted:
            return item
    return None


def has_key_value(value: Any, keys: Iterable[str], expected: Any) -> bool:
    wanted = set(keys)
    for key, item in iter_key_values(value):
        if key not in wanted:
            continue
        if equivalent_value(item, expected):
            return True
    return False


def equivalent_value(observed: Any, expected: Any) -> bool:
    if observed == expected:
        return True
    if isinstance(expected, int):
        try:
            return int(observed) == expected
        except (TypeError, ValueError):
            return False
    if isinstance(expected, float):
        try:
            return abs(float(observed) - expected) <= 1e-9
        except (TypeError, ValueError):
            return False
    return str(observed) == str(expected)


def number_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def value_is_true(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str) and value.strip().lower() == "true":
        return True
    return False


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    violations: list[str] = []
    if not path.exists():
        return [], [f"missing upstream report: {path}"]

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            violations.append(f"{path}: line {line_number}: malformed JSONL: {exc}")
            continue
        if not isinstance(parsed, dict):
            violations.append(f"{path}: line {line_number}: record is not an object")
            continue
        records.append(parsed)

    if not records:
        violations.append(f"{path}: no JSONL records found")
    return records, violations


def write_jsonl(path: Path, record: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def select_latest_report(reports_dir: Path, patterns: Iterable[str]) -> Path | None:
    candidates: list[Path] = []
    for pattern in patterns:
        exact = reports_dir / pattern
        if exact.exists() and exact.is_file():
            candidates.append(exact)
        candidates.extend(path for path in reports_dir.glob(pattern) if path.is_file())
    unique = {path.resolve(): path for path in candidates}
    if not unique:
        return None
    return max(unique.values(), key=lambda path: path.stat().st_mtime)


def resolve_upstream_paths(reports_dir: Path) -> dict[str, Path | None]:
    return {
        name: select_latest_report(reports_dir, patterns)
        for name, patterns in UPSTREAM_SPECS.items()
    }


def summarize_identity(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "exact_ticket": first_key_value(record, ("exact_ticket", "ticket", "position_ticket")),
        "exact_identifier": first_key_value(record, ("exact_identifier", "identifier", "position_identifier")),
        "runtime_symbol": first_key_value(record, ("runtime_symbol", "symbol")),
        "model_symbol": first_key_value(record, ("model_symbol",)),
        "magic": first_key_value(record, ("magic", "position_magic")),
        "volume": first_key_value(record, ("volume", "position_volume")),
        "position_type": first_key_value(record, ("position_type", "type", "position_side_type")),
    }


def summarize_black_swan_inputs(name: str, record: Mapping[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "verdict": record.get("verdict"),
        "operator_state": record.get("operator_state"),
        "operator_next_action": record.get("operator_next_action"),
        "observed_at_utc": record.get("observed_at_utc"),
        "identity": summarize_identity(record),
    }

    if name == "runtime_heartbeat":
        summary["heartbeat_snapshot"] = {
            "server": first_key_value(record, ("server", "account_server", "expected_server")),
            "currency": first_key_value(record, ("currency", "account_currency", "expected_currency")),
            "terminal_connected": first_key_value(record, ("terminal_connected", "connected")),
            "account_available": first_key_value(record, ("account_available", "account_info_available")),
        }
    elif name == "runtime_lockout_reader":
        summary["lockout_snapshot"] = {
            key: first_key_value(record, (key,))
            for key in sorted(LOCKOUT_ACTIVE_KEYS)
            if first_key_value(record, (key,)) is not None
        }
    elif name == "runtime_tick_spread":
        summary["tick_spread_snapshot"] = {
            "bid": first_key_value(record, ("bid",)),
            "ask": first_key_value(record, ("ask",)),
            "spread": first_key_value(record, ("spread", "spread_points", "spread_raw")),
            "tick_time": first_key_value(record, ("tick_time", "time", "time_msc")),
        }
    elif name == "runtime_account_risk_margin":
        summary["account_risk_margin_snapshot"] = {
            "balance": first_key_value(record, ("balance", "account_balance")),
            "equity": first_key_value(record, ("equity", "account_equity")),
            "margin": first_key_value(record, ("margin", "account_margin")),
            "free_margin": first_key_value(record, ("free_margin", "margin_free", "freeMargin")),
            "margin_level": first_key_value(record, ("margin_level", "marginLevel")),
            "floating_pnl": first_key_value(record, ("floating_pnl", "unrealized_pnl", "profit")),
        }
    elif name == "runtime_exposure_inventory":
        summary["exposure_inventory_snapshot"] = {
            "canary_observed": first_key_value(record, ("canary_observed", "exact_canary_observed")),
            "h024_position_count": first_key_value(record, ("h024_position_count", "position_count")),
            "h024_order_count": first_key_value(record, ("h024_order_count", "order_count")),
            "usdjpy_exposure_detected": first_key_value(record, ("usdjpy_exposure_detected", "h024_usdjpy_exposure_detected")),
            "extra_h024_exposure_detected": first_key_value(record, ("extra_h024_exposure_detected",)),
        }
    return summary


def validate_common_upstream_record(
    name: str,
    path: Path | None,
    record: Mapping[str, Any] | None,
    now: datetime,
    max_age_seconds: int,
) -> list[str]:
    violations: list[str] = []

    if path is None:
        return [f"{name}: missing upstream report"]

    if record is None:
        return [f"{name}: missing upstream record"]

    if record.get("verdict") != "PASS":
        violations.append(f"{name}: upstream verdict is not PASS")

    embedded_violations = record.get("violations")
    if embedded_violations:
        violations.append(f"{name}: upstream record has embedded violations")

    observed_at_utc = record.get("observed_at_utc")
    observed_at = parse_utc_datetime(observed_at_utc)
    if observed_at is None:
        violations.append(f"{name}: missing or malformed observed_at_utc")
    else:
        age_seconds = abs((now - observed_at).total_seconds())
        if age_seconds > max_age_seconds:
            violations.append(
                f"{name}: upstream evidence stale: age_seconds={age_seconds:.3f} max={max_age_seconds}"
            )

    for key, value in iter_key_values(record):
        if key in AUTHORIZATION_KEYS and value_is_true(value):
            violations.append(f"{name}: unsafe authorization true: {key}")

    for key, value in iter_key_values(record):
        if key in FORBIDDEN_EXECUTABLE_OBJECT_KEYS and value not in (None, False, "", [], {}):
            violations.append(f"{name}: executable broker/trade request object present: {key}")

    return violations


def detect_black_swan_conditions(
    upstream_records: Mapping[str, Mapping[str, Any] | None],
    *,
    extreme_spread_limit: float,
    min_margin_level: float,
    min_equity_to_balance_ratio: float,
) -> list[str]:
    conditions: list[str] = []

    lockout = upstream_records.get("runtime_lockout_reader")
    if lockout is not None:
        for key, value in iter_key_values(lockout):
            if key in LOCKOUT_ACTIVE_KEYS and value_is_true(value):
                conditions.append(f"lockout active: {key}")

    heartbeat = upstream_records.get("runtime_heartbeat")
    if heartbeat is not None:
        connected = first_key_value(heartbeat, ("terminal_connected", "connected"))
        account_available = first_key_value(heartbeat, ("account_available", "account_info_available"))
        if connected is not None and value_is_true(connected) is False and str(connected).lower() in {"false", "0"}:
            conditions.append("heartbeat terminal disconnected")
        if account_available is not None and value_is_true(account_available) is False and str(account_available).lower() in {"false", "0"}:
            conditions.append("heartbeat account unavailable")

    tick_spread = upstream_records.get("runtime_tick_spread")
    if tick_spread is not None:
        bid = number_or_none(first_key_value(tick_spread, ("bid",)))
        ask = number_or_none(first_key_value(tick_spread, ("ask",)))
        spread = number_or_none(first_key_value(tick_spread, ("spread", "spread_points", "spread_raw")))

        if bid is not None and ask is not None and ask <= bid:
            conditions.append("bid/ask inversion or zero spread detected")
        if spread is not None and spread > extreme_spread_limit:
            conditions.append(f"extreme spread detected: spread={spread} limit={extreme_spread_limit}")

    account = upstream_records.get("runtime_account_risk_margin")
    if account is not None:
        balance = number_or_none(first_key_value(account, ("balance", "account_balance")))
        equity = number_or_none(first_key_value(account, ("equity", "account_equity")))
        free_margin = number_or_none(first_key_value(account, ("free_margin", "margin_free", "freeMargin")))
        margin_level = number_or_none(first_key_value(account, ("margin_level", "marginLevel")))

        if balance is not None and balance <= 0:
            conditions.append("non-positive account balance")
        if equity is not None and equity <= 0:
            conditions.append("non-positive account equity")
        if free_margin is not None and free_margin < 0:
            conditions.append("negative free margin")
        if margin_level is not None and margin_level < min_margin_level:
            conditions.append(f"margin level below black-swan floor: margin_level={margin_level} floor={min_margin_level}")
        if balance is not None and equity is not None and balance > 0:
            ratio = equity / balance
            if ratio < min_equity_to_balance_ratio:
                conditions.append(
                    f"extreme equity drawdown ratio: equity_to_balance={ratio:.6f} floor={min_equity_to_balance_ratio}"
                )

    exposure = upstream_records.get("runtime_exposure_inventory")
    if exposure is not None:
        canary_observed = first_key_value(exposure, ("canary_observed", "exact_canary_observed"))
        h024_order_count = number_or_none(first_key_value(exposure, ("h024_order_count", "order_count")))
        usdjpy_exposure_detected = first_key_value(exposure, ("usdjpy_exposure_detected", "h024_usdjpy_exposure_detected"))
        extra_h024_exposure_detected = first_key_value(exposure, ("extra_h024_exposure_detected",))

        if canary_observed is not None and value_is_true(canary_observed) is False and str(canary_observed).lower() in {"false", "0"}:
            conditions.append("known exact-ticket XAUUSDm canary not observed")
        if h024_order_count is not None and h024_order_count > 0:
            conditions.append(f"unexpected H024 pending/open orders detected: count={h024_order_count}")
        if value_is_true(usdjpy_exposure_detected):
            conditions.append("unexpected H024 USDJPY exposure detected")
        if value_is_true(extra_h024_exposure_detected):
            conditions.append("extra H024 exposure detected")

    return conditions


def identity_locks_present(records: Iterable[Mapping[str, Any]]) -> dict[str, bool]:
    record_list = list(records)
    return {
        "exact_ticket_locked": any(
            has_key_value(record, ("exact_ticket", "ticket", "position_ticket"), EXPECTED_TICKET)
            for record in record_list
        ),
        "exact_identifier_locked": any(
            has_key_value(record, ("exact_identifier", "identifier", "position_identifier"), EXPECTED_IDENTIFIER)
            for record in record_list
        ),
        "runtime_symbol_locked": any(
            has_key_value(record, ("runtime_symbol", "symbol"), EXPECTED_RUNTIME_SYMBOL)
            for record in record_list
        ),
        "model_symbol_locked": any(
            has_key_value(record, ("model_symbol",), EXPECTED_MODEL_SYMBOL)
            for record in record_list
        ),
        "magic_locked": any(
            has_key_value(record, ("magic", "position_magic"), EXPECTED_MAGIC)
            for record in record_list
        ),
        "volume_locked": any(
            has_key_value(record, ("volume", "position_volume"), EXPECTED_VOLUME)
            for record in record_list
        ),
        "position_type_locked": any(
            has_key_value(record, ("position_type", "type", "position_side_type"), EXPECTED_POSITION_TYPE)
            for record in record_list
        ),
    }


def build_read_only_black_swan_guard(
    *,
    reports_dir: Path = Path("reports"),
    max_upstream_age_seconds: int = DEFAULT_MAX_UPSTREAM_AGE_SECONDS,
    extreme_spread_limit: float = DEFAULT_EXTREME_SPREAD_LIMIT,
    min_margin_level: float = DEFAULT_MIN_MARGIN_LEVEL,
    min_equity_to_balance_ratio: float = DEFAULT_MIN_EQUITY_TO_BALANCE_RATIO,
    observed_at_utc: str | None = None,
    upstream_paths: Mapping[str, Path | None] | None = None,
) -> dict[str, Any]:
    observed_at_utc = observed_at_utc or utc_now_iso()
    now = parse_utc_datetime(observed_at_utc) or datetime.now(timezone.utc)
    upstream_paths = dict(upstream_paths or resolve_upstream_paths(reports_dir))

    violations: list[str] = []
    upstream_summaries: dict[str, Any] = {}
    upstream_records: dict[str, Mapping[str, Any] | None] = {}

    for name in UPSTREAM_SPECS:
        path = upstream_paths.get(name)
        if path is None:
            upstream_records[name] = None
            violations.append(f"{name}: missing upstream report")
            upstream_summaries[name] = {
                "path": None,
                "verdict": None,
                "operator_state": None,
                "observed_at_utc": None,
            }
            continue

        records, read_violations = read_jsonl(path)
        if read_violations:
            violations.extend(f"{name}: {violation}" for violation in read_violations)
            record = records[-1] if records else None
        else:
            record = records[-1]

        upstream_records[name] = record
        if record is not None:
            violations.extend(
                validate_common_upstream_record(
                    name,
                    path,
                    record,
                    now,
                    max_upstream_age_seconds,
                )
            )
            upstream_summaries[name] = {
                "path": str(path),
                **summarize_black_swan_inputs(name, record),
            }
        else:
            upstream_summaries[name] = {
                "path": str(path),
                "verdict": None,
                "operator_state": None,
                "observed_at_utc": None,
            }

    present_records = [record for record in upstream_records.values() if record is not None]
    locks = identity_locks_present(present_records)
    for key, locked in locks.items():
        if not locked:
            violations.append(f"{key} missing")

    black_swan_conditions = detect_black_swan_conditions(
        upstream_records,
        extreme_spread_limit=extreme_spread_limit,
        min_margin_level=min_margin_level,
        min_equity_to_balance_ratio=min_equity_to_balance_ratio,
    )
    violations.extend(f"black-swan condition active: {condition}" for condition in black_swan_conditions)

    verdict = "PASS" if not violations else "FAIL_CLOSED"
    black_swan_triggered = bool(black_swan_conditions or violations)

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
        "black_swan_guard_authorizes_trading": False,
        "black_swan_guard_authorizes_broker_mutation": False,
        "black_swan_guard_authorizes_close_modify": False,
        "live_broker_request_constructed": False,
        "executable_trade_request_constructed": False,
        "mt5_request_dictionary_constructed": False,
        "order_check_planned": False,
        "order_send_planned": False,
        "symbol_select_planned": False,
    }

    checks = {
        "all_required_upstream_reports_present": all(upstream_paths.get(name) is not None for name in UPSTREAM_SPECS),
        "all_upstream_records_pass": all(
            isinstance(record, Mapping) and record.get("verdict") == "PASS" and not record.get("violations")
            for record in upstream_records.values()
        ),
        "all_upstream_authorizations_blocked": True,
        "black_swan_conditions_absent": not black_swan_conditions,
        "heartbeat_not_extreme_unsafe": not any("heartbeat" in item for item in black_swan_conditions),
        "lockouts_clear": not any("lockout active" in item for item in black_swan_conditions),
        "spread_not_extreme": not any("spread" in item for item in black_swan_conditions),
        "account_risk_not_extreme": not any(
            marker in item
            for item in black_swan_conditions
            for marker in ("equity", "balance", "margin")
        ),
        "exposure_not_extreme_unsafe": not any(
            marker in item
            for item in black_swan_conditions
            for marker in ("exposure", "orders", "canary")
        ),
        **locks,
        "exact_canary_identity_locked": all(locks.values()),
        "live_broker_request_absent": True,
        "executable_trade_request_absent": True,
        "mt5_request_dictionary_absent": True,
        "order_check_absent": True,
        "order_send_absent": True,
        "symbol_select_absent": True,
        "all_action_authorizations_false": True,
    }

    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "exact_ticket": EXPECTED_TICKET,
            "exact_identifier": EXPECTED_IDENTIFIER,
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "magic": EXPECTED_MAGIC,
            "volume": EXPECTED_VOLUME,
            "position_type": EXPECTED_POSITION_TYPE,
            "max_upstream_age_seconds": max_upstream_age_seconds,
            "extreme_spread_limit": extreme_spread_limit,
            "min_margin_level": min_margin_level,
            "min_equity_to_balance_ratio": min_equity_to_balance_ratio,
            "hard_boundary": "READ_ONLY_BLACK_SWAN_GUARD_NO_BROKER_MUTATION_NO_EXECUTION_AUTHORIZED",
        },
        "upstream_summaries": upstream_summaries,
        "black_swan_guard": {
            "black_swan_guard_clear": verdict == "PASS",
            "black_swan_guard_triggered": black_swan_triggered,
            "conditions": black_swan_conditions,
            "mode": "READ_ONLY_FAIL_CLOSED_SUPERVISION_ONLY",
            "authorizes_trading": False,
            "authorizes_broker_mutation": False,
            "authorizes_close_modify": False,
            "constructs_live_broker_request": False,
            "constructs_executable_trade_request": False,
            "constructs_mt5_request_dictionary": False,
        },
        "current_read_only_evidence": {
            "heartbeat": upstream_summaries.get("runtime_heartbeat"),
            "lockout_reader": upstream_summaries.get("runtime_lockout_reader"),
            "tick_spread": upstream_summaries.get("runtime_tick_spread"),
            "exposure_inventory": upstream_summaries.get("runtime_exposure_inventory"),
            "account_risk_margin": upstream_summaries.get("runtime_account_risk_margin"),
            "runtime_safety_aggregate": upstream_summaries.get("runtime_safety_aggregate"),
            "no_mutation_gate": upstream_summaries.get("runtime_no_mutation_safety_gate"),
            "execution_readiness_dry_run_schema_preview": upstream_summaries.get(
                "execution_readiness_dry_run_schema_preview"
            ),
        },
        "checks": checks,
        "authorizations": authorizations,
        **authorizations,
        "black_swan_guard_clear": verdict == "PASS",
        "black_swan_guard_triggered": black_swan_triggered,
        "operator_state": PASS_OPERATOR_STATE if verdict == "PASS" else FAIL_OPERATOR_STATE,
        "operator_next_action": PASS_OPERATOR_NEXT_ACTION if verdict == "PASS" else FAIL_OPERATOR_NEXT_ACTION,
        "violations": violations,
        "verdict": verdict,
    }
    return record


def validate_output_record(record: Mapping[str, Any]) -> list[str]:
    violations: list[str] = []

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append("wrong schema_version")
    if record.get("strategy") != STRATEGY:
        violations.append("wrong strategy")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append("wrong packet_type")
    if not parse_utc_datetime(record.get("observed_at_utc")):
        violations.append("missing or malformed observed_at_utc")

    if record.get("effective_new_entries_blocked") is not True:
        violations.append("effective_new_entries_blocked must be true")

    for key in EXPECTED_FALSE_TOP_LEVEL_FIELDS:
        if record.get(key) is not False:
            violations.append(f"{key} must be false")

    expected = record.get("expected")
    if not isinstance(expected, Mapping):
        violations.append("missing expected object")
    else:
        expected_pairs = {
            "exact_ticket": EXPECTED_TICKET,
            "exact_identifier": EXPECTED_IDENTIFIER,
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "magic": EXPECTED_MAGIC,
            "volume": EXPECTED_VOLUME,
            "position_type": EXPECTED_POSITION_TYPE,
        }
        for key, value in expected_pairs.items():
            if not equivalent_value(expected.get(key), value):
                violations.append(f"expected.{key} mismatch")

    black_swan_guard = record.get("black_swan_guard")
    if not isinstance(black_swan_guard, Mapping):
        violations.append("missing black_swan_guard object")
    else:
        if black_swan_guard.get("authorizes_trading") is not False:
            violations.append("black_swan_guard.authorizes_trading must be false")
        if black_swan_guard.get("authorizes_broker_mutation") is not False:
            violations.append("black_swan_guard.authorizes_broker_mutation must be false")
        if black_swan_guard.get("authorizes_close_modify") is not False:
            violations.append("black_swan_guard.authorizes_close_modify must be false")
        if black_swan_guard.get("constructs_live_broker_request") is not False:
            violations.append("black_swan_guard constructs live broker request")
        if black_swan_guard.get("constructs_executable_trade_request") is not False:
            violations.append("black_swan_guard constructs executable trade request")
        if black_swan_guard.get("constructs_mt5_request_dictionary") is not False:
            violations.append("black_swan_guard constructs MT5 request dictionary")
        if record.get("verdict") == "PASS" and black_swan_guard.get("black_swan_guard_triggered") is not False:
            violations.append("PASS record cannot have black_swan_guard_triggered true")

    authorizations = record.get("authorizations")
    if not isinstance(authorizations, Mapping):
        violations.append("missing authorizations object")
    else:
        if authorizations.get("effective_new_entries_blocked") is not True:
            violations.append("authorizations.effective_new_entries_blocked must be true")
        for key in EXPECTED_FALSE_TOP_LEVEL_FIELDS:
            if authorizations.get(key) is not False:
                violations.append(f"authorizations.{key} must be false")

    for key, value in iter_key_values(record):
        if key in AUTHORIZATION_KEYS and value_is_true(value):
            violations.append(f"unsafe true action/execution field: {key}")
        if key in FORBIDDEN_EXECUTABLE_OBJECT_KEYS and value not in (None, False, "", [], {}):
            violations.append(f"executable broker/trade request object present: {key}")

    if record.get("verdict") == "PASS" and record.get("violations"):
        violations.append("PASS record contains embedded violations")

    if record.get("verdict") not in {"PASS", "FAIL_CLOSED"}:
        violations.append("verdict must be PASS or FAIL_CLOSED")

    return violations


def verify_jsonl_file(path: Path, *, require_pass: bool = False) -> tuple[str, list[str], list[dict[str, Any]]]:
    records, read_violations = read_jsonl(path)
    violations = list(read_violations)

    for index, record in enumerate(records, start=1):
        record_violations = validate_output_record(record)
        violations.extend(f"record {index}: {violation}" for violation in record_violations)

        if record.get("violations"):
            for embedded in record.get("violations", []):
                violations.append(f"record {index}: embedded violation: {embedded}")

        if require_pass and record.get("verdict") != "PASS":
            violations.append(f"record {index}: --require-pass rejects verdict {record.get('verdict')}")

    verifier_verdict = "PASS" if not violations else "FAIL"
    return verifier_verdict, violations, records


def print_record_summary(record: Mapping[str, Any], *, prefix: str = "") -> None:
    print(f"{prefix}Verdict: {record.get('verdict')}")
    print(f"{prefix}Violations: {len(record.get('violations') or [])}")
    print(f"{prefix}Operator state: {record.get('operator_state')}")
    print(f"{prefix}Operator next action: {record.get('operator_next_action')}")
    print(f"{prefix}Exact ticket: {record.get('expected', {}).get('exact_ticket')}")
    print(f"{prefix}Exact identifier: {record.get('expected', {}).get('exact_identifier')}")
    for key in (
        "black_swan_guard_clear",
        "black_swan_guard_triggered",
        "effective_new_entries_blocked",
        "broker_mutation_authorized",
        "order_check_authorized",
        "order_send_authorized",
        "entry_authorized",
        "close_modify_authorized",
        "xauusd_order_authorized",
        "usdjpy_order_authorized",
        "trading_loop_authorized",
        "automatic_execution_authorized",
        "black_swan_guard_authorizes_trading",
        "live_broker_request_constructed",
        "executable_trade_request_constructed",
        "mt5_request_dictionary_constructed",
    ):
        print(f"{prefix}{key}: {record.get(key)}")


def build_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build H024 read-only black-swan guard JSONL.")
    parser.add_argument("--reports-dir", default="reports", help="Directory containing upstream JSONL reports.")
    parser.add_argument(
        "--output",
        default="reports/h024_read_only_black_swan_guard.jsonl",
        help="Output JSONL path.",
    )
    parser.add_argument(
        "--max-upstream-age-seconds",
        type=int,
        default=DEFAULT_MAX_UPSTREAM_AGE_SECONDS,
        help="Maximum upstream packet age before fail-closed.",
    )
    parser.add_argument(
        "--extreme-spread-limit",
        type=float,
        default=DEFAULT_EXTREME_SPREAD_LIMIT,
        help="Extreme spread threshold used by the read-only guard.",
    )
    parser.add_argument(
        "--min-margin-level",
        type=float,
        default=DEFAULT_MIN_MARGIN_LEVEL,
        help="Minimum margin level floor used by the read-only guard.",
    )
    parser.add_argument(
        "--min-equity-to-balance-ratio",
        type=float,
        default=DEFAULT_MIN_EQUITY_TO_BALANCE_RATIO,
        help="Extreme equity drawdown ratio floor.",
    )
    args = parser.parse_args(argv)

    record = build_read_only_black_swan_guard(
        reports_dir=Path(args.reports_dir),
        max_upstream_age_seconds=args.max_upstream_age_seconds,
        extreme_spread_limit=args.extreme_spread_limit,
        min_margin_level=args.min_margin_level,
        min_equity_to_balance_ratio=args.min_equity_to_balance_ratio,
    )
    output = Path(args.output)
    write_jsonl(output, record)
    print(f"Wrote {output}")
    print_record_summary(record)
    return 0


def verify_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify H024 read-only black-swan guard JSONL.")
    parser.add_argument("path", help="JSONL path to verify.")
    parser.add_argument("--require-pass", action="store_true", help="Require all records to have verdict PASS.")
    args = parser.parse_args(argv)

    verdict, violations, records = verify_jsonl_file(Path(args.path), require_pass=args.require_pass)
    print(f"H024 read-only black-swan guard records: {len(records)}")
    print(f"Violations: {len(violations)}")
    print(f"Verifier verdict: {verdict}")

    if records:
        record = records[-1]
        print(f"Record verdict: {record.get('verdict')}")
        print(f"Operator state: {record.get('operator_state')}")
        print(f"Operator next action: {record.get('operator_next_action')}")
        print(f"Exact ticket: {record.get('expected', {}).get('exact_ticket')}")
        print(f"Exact identifier: {record.get('expected', {}).get('exact_identifier')}")
        for key in (
            "black_swan_guard_clear",
            "black_swan_guard_triggered",
            "effective_new_entries_blocked",
            "broker_mutation_authorized",
            "order_check_authorized",
            "order_send_authorized",
            "entry_authorized",
            "close_modify_authorized",
            "xauusd_order_authorized",
            "usdjpy_order_authorized",
            "trading_loop_authorized",
            "automatic_execution_authorized",
            "black_swan_guard_authorizes_trading",
            "live_broker_request_constructed",
            "executable_trade_request_constructed",
            "mt5_request_dictionary_constructed",
        ):
            print(f"{key}: {record.get(key)}")

    for violation in violations:
        print(f"VIOLATION: {violation}")

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(build_cli())
