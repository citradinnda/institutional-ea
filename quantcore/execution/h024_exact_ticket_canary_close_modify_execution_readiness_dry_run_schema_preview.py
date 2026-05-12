from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


SCHEMA_VERSION = "1.0"
STRATEGY = "H024"
PACKET_TYPE = "h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview"

PASS_OPERATOR_STATE = (
    "EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED"
)
PASS_OPERATOR_NEXT_ACTION = (
    "KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW"
)
FAIL_OPERATOR_STATE = (
    "FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_EXECUTION_READINESS_DRY_RUN_SCHEMA_PREVIEW_BLOCKED"
)
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_RUNTIME_SYMBOL = "XAUUSDm"
EXPECTED_MODEL_SYMBOL = "XAUUSD"
EXPECTED_MAGIC = 240024
EXPECTED_VOLUME = 0.01
EXPECTED_POSITION_TYPE = 1

DEFAULT_MAX_UPSTREAM_AGE_SECONDS = 3600

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
    "execution_readiness_dry_run_schema_preview_authorizes_execution",
    "dry_run_request_shape_preview_authorizes_execution",
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

UPSTREAM_SPECS: Mapping[str, tuple[str, ...]] = {
    "runtime_no_mutation_safety_gate": (
        "h024_runtime_no_mutation_safety_gate.jsonl",
        "*no_mutation*safety_gate*.jsonl",
    ),
    "unified_read_only_runtime_supervision": (
        "h024_unified_read_only_runtime_supervision.jsonl",
        "*unified*runtime*supervision*.jsonl",
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
    "runtime_exposure_inventory": (
        "h024_runtime_exposure_inventory_safety_supervisor.jsonl",
        "*exposure*inventory*.jsonl",
    ),
    "runtime_account_risk_margin": (
        "h024_runtime_account_risk_margin_safety_supervisor.jsonl",
        "*account*risk*margin*.jsonl",
    ),
    "runtime_tick_spread": (
        "h024_runtime_tick_spread_safety_supervisor.jsonl",
        "h024_runtime_tick_and_spread_safety_supervisor.jsonl",
        "*tick*spread*.jsonl",
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


def summarize_read_only_evidence(name: str, record: Mapping[str, Any]) -> dict[str, Any]:
    summary = {
        "verdict": record.get("verdict"),
        "operator_state": record.get("operator_state"),
        "operator_next_action": record.get("operator_next_action"),
        "observed_at_utc": record.get("observed_at_utc"),
        "identity": summarize_identity(record),
    }

    if name == "runtime_account_risk_margin":
        summary["account_risk_margin_snapshot"] = {
            "balance": first_key_value(record, ("balance", "account_balance")),
            "equity": first_key_value(record, ("equity", "account_equity")),
            "margin": first_key_value(record, ("margin", "account_margin")),
            "free_margin": first_key_value(record, ("free_margin", "margin_free", "freeMargin")),
            "margin_level": first_key_value(record, ("margin_level", "marginLevel")),
            "floating_pnl": first_key_value(record, ("floating_pnl", "unrealized_pnl", "profit")),
        }
    elif name == "runtime_tick_spread":
        summary["tick_spread_snapshot"] = {
            "bid": first_key_value(record, ("bid",)),
            "ask": first_key_value(record, ("ask",)),
            "spread": first_key_value(record, ("spread", "spread_points", "spread_raw")),
            "tick_time": first_key_value(record, ("tick_time", "time", "time_msc")),
        }
    elif name == "runtime_exposure_inventory":
        summary["exposure_inventory_snapshot"] = {
            "canary_observed": first_key_value(record, ("canary_observed", "exact_canary_observed")),
            "h024_position_count": first_key_value(record, ("h024_position_count", "position_count")),
            "h024_order_count": first_key_value(record, ("h024_order_count", "order_count")),
        }
    elif name == "operator_decision_v2_preview":
        summary["operator_decision_v2_preview"] = {
            "decision_preview_status": first_key_value(record, ("decision_preview_status",)),
            "requested_action": first_key_value(record, ("requested_action",)),
            "operator_id": first_key_value(record, ("operator_id",)),
            "operator_note": first_key_value(record, ("operator_note",)),
            "authorizes_action": first_key_value(
                record,
                ("operator_decision_v2_preview_authorizes_action",),
            ),
        }

    return summary


def validate_upstream_record(
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

    if name == "operator_decision_v2_preview":
        if not has_key_value(record, ("exact_ticket", "ticket", "position_ticket"), EXPECTED_TICKET):
            violations.append("operator_decision_v2_preview: exact ticket mismatch or missing")
        if not has_key_value(record, ("exact_identifier", "identifier", "position_identifier"), EXPECTED_IDENTIFIER):
            violations.append("operator_decision_v2_preview: exact identifier mismatch or missing")
        if not has_key_value(record, ("runtime_symbol", "symbol"), EXPECTED_RUNTIME_SYMBOL):
            violations.append("operator_decision_v2_preview: runtime symbol mismatch or missing")
        if not has_key_value(record, ("model_symbol",), EXPECTED_MODEL_SYMBOL):
            violations.append("operator_decision_v2_preview: model symbol mismatch or missing")
        if not has_key_value(record, ("magic", "position_magic"), EXPECTED_MAGIC):
            violations.append("operator_decision_v2_preview: magic mismatch or missing")
        if not has_key_value(record, ("volume", "position_volume"), EXPECTED_VOLUME):
            violations.append("operator_decision_v2_preview: volume mismatch or missing")
        if not has_key_value(record, ("position_type", "type", "position_side_type"), EXPECTED_POSITION_TYPE):
            violations.append("operator_decision_v2_preview: position type mismatch or missing")

        status = first_key_value(record, ("decision_preview_status",))
        requested_action = first_key_value(record, ("requested_action",))
        default_status = "NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY"
        default_action = "NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY"
        intent_status = "OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY"
        preview_actions = {
            "PREVIEW_CLOSE_ONLY",
            "PREVIEW_MODIFY_STOP_LOSS_ONLY",
            "PREVIEW_MODIFY_TAKE_PROFIT_ONLY",
            "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT",
        }

        if status == default_status and requested_action != default_action:
            violations.append("operator_decision_v2_preview: ambiguous default status with non-default action")
        elif status == intent_status and requested_action not in preview_actions:
            violations.append("operator_decision_v2_preview: ambiguous intent status without preview action")
        elif status not in {default_status, intent_status}:
            violations.append("operator_decision_v2_preview: unknown decision_preview_status")

    return violations


def build_execution_readiness_dry_run_schema_preview(
    *,
    reports_dir: Path = Path("reports"),
    max_upstream_age_seconds: int = DEFAULT_MAX_UPSTREAM_AGE_SECONDS,
    observed_at_utc: str | None = None,
    upstream_paths: Mapping[str, Path | None] | None = None,
) -> dict[str, Any]:
    observed_at_utc = observed_at_utc or utc_now_iso()
    now = parse_utc_datetime(observed_at_utc)
    if now is None:
        now = datetime.now(timezone.utc)

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
                validate_upstream_record(
                    name,
                    path,
                    record,
                    now,
                    max_upstream_age_seconds,
                )
            )
            upstream_summaries[name] = {
                "path": str(path),
                **summarize_read_only_evidence(name, record),
            }
        else:
            upstream_summaries[name] = {
                "path": str(path),
                "verdict": None,
                "operator_state": None,
                "observed_at_utc": None,
            }

    all_records = [record for record in upstream_records.values() if record is not None]

    exact_ticket_locked = any(
        has_key_value(record, ("exact_ticket", "ticket", "position_ticket"), EXPECTED_TICKET)
        for record in all_records
    )
    exact_identifier_locked = any(
        has_key_value(record, ("exact_identifier", "identifier", "position_identifier"), EXPECTED_IDENTIFIER)
        for record in all_records
    )
    runtime_symbol_locked = any(
        has_key_value(record, ("runtime_symbol", "symbol"), EXPECTED_RUNTIME_SYMBOL)
        for record in all_records
    )
    model_symbol_locked = any(
        has_key_value(record, ("model_symbol",), EXPECTED_MODEL_SYMBOL)
        for record in all_records
    )
    magic_locked = any(
        has_key_value(record, ("magic", "position_magic"), EXPECTED_MAGIC)
        for record in all_records
    )
    volume_locked = any(
        has_key_value(record, ("volume", "position_volume"), EXPECTED_VOLUME)
        for record in all_records
    )
    position_type_locked = any(
        has_key_value(record, ("position_type", "type", "position_side_type"), EXPECTED_POSITION_TYPE)
        for record in all_records
    )

    if not exact_ticket_locked:
        violations.append("exact ticket lock missing")
    if not exact_identifier_locked:
        violations.append("exact identifier lock missing")
    if not runtime_symbol_locked:
        violations.append("runtime symbol lock missing")
    if not model_symbol_locked:
        violations.append("model symbol lock missing")
    if not magic_locked:
        violations.append("magic lock missing")
    if not volume_locked:
        violations.append("volume lock missing")
    if not position_type_locked:
        violations.append("position type lock missing")

    exact_canary_identity_locked = all(
        (
            exact_ticket_locked,
            exact_identifier_locked,
            runtime_symbol_locked,
            model_symbol_locked,
            magic_locked,
            volume_locked,
            position_type_locked,
        )
    )

    verdict = "PASS" if not violations else "FAIL_CLOSED"

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
        "execution_readiness_dry_run_schema_preview_authorizes_execution": False,
        "dry_run_request_shape_preview_authorizes_execution": False,
        "live_broker_request_constructed": False,
        "executable_trade_request_constructed": False,
        "mt5_request_dictionary_constructed": False,
        "order_check_planned": False,
        "order_send_planned": False,
        "symbol_select_planned": False,
    }

    dry_run_schema_preview = {
        "schema_kind": "ABSTRACT_NON_EXECUTABLE_DRY_RUN_SCHEMA_PREVIEW_ONLY",
        "execution_readiness_dry_run_schema_preview_constructed": True,
        "contains_executable_trade_request": False,
        "contains_mt5_request_dictionary": False,
        "contains_live_broker_request": False,
        "authorizes_execution": False,
        "target_exact_ticket": EXPECTED_TICKET,
        "target_exact_identifier": EXPECTED_IDENTIFIER,
        "target_runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
        "target_model_symbol": EXPECTED_MODEL_SYMBOL,
        "target_magic": EXPECTED_MAGIC,
        "target_volume": EXPECTED_VOLUME,
        "target_position_type": EXPECTED_POSITION_TYPE,
        "non_executable_abstract_fields": [
            "target_exact_ticket",
            "target_exact_identifier",
            "target_runtime_symbol",
            "target_model_symbol",
            "target_magic",
            "target_volume",
            "target_position_type",
            "operator_decision_v2_preview_reference",
            "manual_approval_gate_preview_reference",
            "pre_action_evidence_aggregate_reference",
            "bar_age_exit_condition_evidence_reference",
            "account_risk_margin_snapshot_reference",
            "tick_spread_snapshot_reference",
            "exposure_inventory_snapshot_reference",
        ],
        "explicitly_absent_runtime_call_paths": {
            "live_broker_request": False,
            "executable_trade_request": False,
            "mt5_request_dictionary": False,
            "order_check": False,
            "order_send": False,
            "symbol_select": False,
            "close_modify": False,
            "new_entry": False,
            "trading_loop": False,
        },
    }

    checks = {
        "all_required_upstream_reports_present": all(upstream_paths.get(name) is not None for name in UPSTREAM_SPECS),
        "all_upstream_records_pass": all(
            isinstance(record, Mapping) and record.get("verdict") == "PASS" and not record.get("violations")
            for record in upstream_records.values()
        ),
        "exact_ticket_locked": exact_ticket_locked,
        "exact_identifier_locked": exact_identifier_locked,
        "runtime_symbol_locked": runtime_symbol_locked,
        "model_symbol_locked": model_symbol_locked,
        "magic_locked": magic_locked,
        "volume_locked": volume_locked,
        "position_type_locked": position_type_locked,
        "exact_canary_identity_locked": exact_canary_identity_locked,
        "dry_run_schema_preview_is_abstract_non_executable": True,
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
            "hard_boundary": "READ_ONLY_PREVIEW_ONLY_NO_BROKER_MUTATION_NO_EXECUTION_AUTHORIZED",
        },
        "upstream_summaries": upstream_summaries,
        "current_read_only_evidence": {
            "account_risk_margin": upstream_summaries.get("runtime_account_risk_margin"),
            "tick_spread": upstream_summaries.get("runtime_tick_spread"),
            "exposure_inventory": upstream_summaries.get("runtime_exposure_inventory"),
            "operator_decision_v2_preview": upstream_summaries.get("operator_decision_v2_preview"),
        },
        "execution_readiness_dry_run_schema_preview": dry_run_schema_preview,
        "checks": checks,
        "authorizations": authorizations,
        **authorizations,
        "execution_readiness_dry_run_schema_preview_constructed": True,
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

    if record.get("execution_readiness_dry_run_schema_preview_constructed") is not True:
        violations.append("execution_readiness_dry_run_schema_preview_constructed must be true")

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

    schema_preview = record.get("execution_readiness_dry_run_schema_preview")
    if not isinstance(schema_preview, Mapping):
        violations.append("missing execution_readiness_dry_run_schema_preview object")
    else:
        if schema_preview.get("schema_kind") != "ABSTRACT_NON_EXECUTABLE_DRY_RUN_SCHEMA_PREVIEW_ONLY":
            violations.append("dry-run schema preview is not abstract/non-executable")
        if schema_preview.get("contains_executable_trade_request") is not False:
            violations.append("dry-run schema preview contains executable trade request")
        if schema_preview.get("contains_mt5_request_dictionary") is not False:
            violations.append("dry-run schema preview contains MT5 request dictionary")
        if schema_preview.get("contains_live_broker_request") is not False:
            violations.append("dry-run schema preview contains live broker request")
        if schema_preview.get("authorizes_execution") is not False:
            violations.append("dry-run schema preview authorizes execution")

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
        "execution_readiness_dry_run_schema_preview_constructed",
        "execution_readiness_dry_run_schema_preview_authorizes_execution",
        "live_broker_request_constructed",
        "executable_trade_request_constructed",
        "mt5_request_dictionary_constructed",
    ):
        print(f"{prefix}{key}: {record.get(key)}")


def build_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build H024 exact-ticket close/modify execution-readiness dry-run schema preview JSONL."
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory containing upstream JSONL reports.",
    )
    parser.add_argument(
        "--output",
        default="reports/h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl",
        help="Output JSONL path.",
    )
    parser.add_argument(
        "--max-upstream-age-seconds",
        type=int,
        default=DEFAULT_MAX_UPSTREAM_AGE_SECONDS,
        help="Maximum upstream packet age before fail-closed.",
    )
    parser.add_argument(
        "--position-open-over-three-bars",
        action="store_true",
        help="Accepted for workflow compatibility; this packet only consumes upstream evidence.",
    )
    args = parser.parse_args(argv)

    record = build_execution_readiness_dry_run_schema_preview(
        reports_dir=Path(args.reports_dir),
        max_upstream_age_seconds=args.max_upstream_age_seconds,
    )
    output = Path(args.output)
    write_jsonl(output, record)
    print(f"Wrote {output}")
    print_record_summary(record)
    return 0


def verify_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify H024 exact-ticket close/modify execution-readiness dry-run schema preview JSONL."
    )
    parser.add_argument("path", help="JSONL path to verify.")
    parser.add_argument("--require-pass", action="store_true", help="Require all records to have verdict PASS.")
    args = parser.parse_args(argv)

    verdict, violations, records = verify_jsonl_file(Path(args.path), require_pass=args.require_pass)
    print(f"H024 exact-ticket canary close/modify execution readiness dry-run schema preview records: {len(records)}")
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
            "execution_readiness_dry_run_schema_preview_constructed",
            "execution_readiness_dry_run_schema_preview_authorizes_execution",
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
