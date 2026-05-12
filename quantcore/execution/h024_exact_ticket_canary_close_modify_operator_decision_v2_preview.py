from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
STRATEGY = "H024"
PACKET_TYPE = "h024_exact_ticket_canary_close_modify_operator_decision_v2_preview"

PASS_VERDICT = "PASS"
FAIL_VERDICT = "FAIL_CLOSED"

PASS_OPERATOR_STATE = "EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED"
PASS_OPERATOR_NEXT_ACTION = "KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_OPERATOR_DECISION_V2_PREVIEW"
FAIL_OPERATOR_STATE = "FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_OPERATOR_DECISION_V2_PREVIEW_BLOCKED"
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

EXPECTED_IDENTITY = {
    "exact_ticket": 4413054432,
    "exact_identifier": 4413054432,
    "runtime_symbol": "XAUUSDm",
    "model_symbol": "XAUUSD",
    "magic": 240024,
    "volume": 0.01,
    "position_type": 1,
}

AUTHORIZATION_FIELDS = (
    "broker_mutation_authorized",
    "order_check_authorized",
    "order_send_authorized",
    "entry_authorized",
    "close_modify_authorized",
    "xauusd_order_authorized",
    "usdjpy_order_authorized",
    "trading_loop_authorized",
    "automatic_execution_authorized",
)

BLOCKING_FIELDS = AUTHORIZATION_FIELDS + (
    "manual_approval_gate_preview_authorizes_action",
    "operator_decision_v2_preview_authorizes_action",
    "live_broker_request_constructed",
    "dry_run_request_shape_preview_constructed",
    "dry_run_request_shape_preview_authorizes_execution",
)

ALLOWED_DECISION_PREVIEW_STATUSES = (
    "NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY",
    "OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY",
)

ALLOWED_REQUESTED_ACTIONS = (
    "NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY",
    "PREVIEW_CLOSE_ONLY",
    "PREVIEW_MODIFY_STOP_LOSS_ONLY",
    "PREVIEW_MODIFY_TAKE_PROFIT_ONLY",
    "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT",
)

UPSTREAM_REPORTS = {
    "no_mutation_gate": "h024_runtime_no_mutation_safety_gate.jsonl",
    "unified_runtime_supervision": "h024_unified_read_only_post_canary_runtime_supervision.jsonl",
    "exact_ticket_governance": "h024_exact_ticket_canary_close_modify_governance.jsonl",
    "decision_artifact": "h024_exact_ticket_canary_close_modify_decision_artifact.jsonl",
    "pre_action_evidence_aggregate": "h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl",
    "bar_age_exit_condition_evidence": "h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl",
    "manual_approval_gate_preview": "h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl",
    "runtime_exposure_inventory": "h024_runtime_exposure_inventory_safety_supervisor.jsonl",
    "runtime_account_risk_margin": "h024_runtime_account_risk_margin_safety_supervisor.jsonl",
    "runtime_tick_spread": "h024_runtime_tick_spread_safety_supervisor.jsonl",
}

UPSTREAM_BUILDERS = (
    ("scripts/build_h024_runtime_no_mutation_safety_gate_jsonl.py", ()),
    ("scripts/build_h024_exact_ticket_canary_close_modify_governance_jsonl.py", ()),
    ("scripts/build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py", ()),
    ("scripts/build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py", ("--position-open-over-three-bars",)),
    ("scripts/build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py", ("--position-open-over-three-bars",)),
    ("scripts/build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py", ("--position-open-over-three-bars",)),
)

DEFAULT_REPORT_PATH = Path("reports") / f"{PACKET_TYPE}.jsonl"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_utc(dt: datetime | None = None) -> str:
    dt = dt or utc_now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def find_key_values(obj: Any, key: str) -> list[Any]:
    values: list[Any] = []
    if isinstance(obj, dict):
        for current_key, value in obj.items():
            if current_key == key:
                values.append(value)
            values.extend(find_key_values(value, key))
    elif isinstance(obj, list):
        for value in obj:
            values.extend(find_key_values(value, key))
    return values


def first_key_value(obj: Any, keys: Iterable[str]) -> Any:
    for key in keys:
        values = find_key_values(obj, key)
        for value in values:
            if value is not None:
                return value
    return None


def coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            parsed = float(value.strip())
        except ValueError:
            return None
        if parsed.is_integer():
            return int(parsed)
    return None


def coerce_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def read_jsonl_records(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], [f"missing JSONL report: {path}"]
    violations: list[str] = []
    records: list[dict[str, Any]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            violations.append(f"malformed JSONL at {path}:{index}: {exc}")
            continue
        if not isinstance(parsed, dict):
            violations.append(f"JSONL record at {path}:{index} is not an object")
            continue
        records.append(parsed)
    if not records and not violations:
        violations.append(f"JSONL report has no records: {path}")
    return records, violations


def latest_jsonl_record(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    records, violations = read_jsonl_records(path)
    if violations:
        return None, violations
    return records[-1], []


def embedded_violations(record: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for value in find_key_values(record, "violations"):
        if isinstance(value, list):
            found.extend(str(item) for item in value if item)
        elif value:
            found.append(str(value))
    return found


def check_authorization_blocked(record: dict[str, Any], context: str) -> list[str]:
    violations: list[str] = []

    effective_values = find_key_values(record, "effective_new_entries_blocked")
    if True not in effective_values:
        violations.append(f"{context} effective_new_entries_blocked missing or not true")
    if False in effective_values:
        violations.append(f"{context} effective_new_entries_blocked contains false")

    for field in AUTHORIZATION_FIELDS:
        values = find_key_values(record, field)
        if not values:
            violations.append(f"{context} missing authorization field {field}")
            continue
        if any(value is True for value in values):
            violations.append(f"{context} unsafe authorization true: {field}")
        if not any(value is False for value in values):
            violations.append(f"{context} authorization field {field} has no explicit false value")

    return violations


def report_age_seconds(record: dict[str, Any], now: datetime) -> float | None:
    observed_at = first_key_value(record, ("observed_at_utc", "generated_at_utc", "created_at_utc"))
    parsed = parse_utc_timestamp(observed_at)
    if parsed is None:
        return None
    return (now - parsed).total_seconds()


def validate_upstream_record(name: str, record: dict[str, Any] | None, *, now: datetime, max_age_seconds: float) -> list[str]:
    if not isinstance(record, dict):
        return [f"upstream {name} missing or malformed"]

    violations: list[str] = []
    if record.get("verdict") != PASS_VERDICT:
        violations.append(f"upstream {name} verdict is not PASS: {record.get('verdict')!r}")

    strategy = record.get("strategy")
    if strategy not in (None, STRATEGY):
        violations.append(f"upstream {name} strategy mismatch: {strategy!r}")

    upstream_violations = embedded_violations(record)
    if upstream_violations:
        violations.append(f"upstream {name} contains embedded violations: {upstream_violations[:5]}")

    violations.extend(check_authorization_blocked(record, f"upstream {name}"))

    age = report_age_seconds(record, now)
    if age is None:
        violations.append(f"upstream {name} missing parseable observed timestamp")
    elif age > max_age_seconds:
        violations.append(f"upstream {name} stale: age_seconds={age:.3f} max={max_age_seconds}")
    elif age < -300:
        violations.append(f"upstream {name} timestamp too far in the future: age_seconds={age:.3f}")

    return violations


def load_upstream_reports(reports_dir: Path, *, now: datetime, max_age_seconds: float) -> tuple[dict[str, dict[str, Any] | None], list[str]]:
    upstream: dict[str, dict[str, Any] | None] = {}
    violations: list[str] = []
    for name, filename in UPSTREAM_REPORTS.items():
        record, read_violations = latest_jsonl_record(reports_dir / filename)
        upstream[name] = record
        violations.extend(f"upstream {name}: {item}" for item in read_violations)
        violations.extend(validate_upstream_record(name, record, now=now, max_age_seconds=max_age_seconds))
    return upstream, violations


def candidate_dicts(obj: Any) -> Iterable[dict[str, Any]]:
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from candidate_dicts(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from candidate_dicts(value)


def extract_tick_spread_snapshot(record: dict[str, Any] | None, symbol: str = "XAUUSDm") -> tuple[dict[str, Any], list[str]]:
    snapshot: dict[str, Any] = {"runtime_symbol": symbol}
    violations: list[str] = []

    if isinstance(record, dict):
        for candidate in candidate_dicts(record):
            if symbol in candidate and isinstance(candidate[symbol], dict):
                candidate = candidate[symbol]
            if candidate.get("symbol") == symbol or candidate.get("runtime_symbol") == symbol or {"bid", "ask", "spread_points"} <= set(candidate):
                for key in ("bid", "ask", "spread_points", "tick_age_seconds", "verdict"):
                    if key in candidate and key not in snapshot:
                        snapshot[key] = candidate[key]

    for key in ("bid", "ask", "spread_points"):
        if key not in snapshot:
            violations.append(f"{symbol} tick/spread snapshot missing {key}")

    bid = coerce_float(snapshot.get("bid"))
    ask = coerce_float(snapshot.get("ask"))
    spread = coerce_float(snapshot.get("spread_points"))
    if bid is not None:
        snapshot["bid"] = bid
    if ask is not None:
        snapshot["ask"] = ask
    if spread is not None:
        snapshot["spread_points"] = spread
    if bid is not None and ask is not None and ask <= bid:
        violations.append(f"{symbol} tick/spread snapshot ask must be greater than bid")
    if spread is not None and spread <= 0:
        violations.append(f"{symbol} tick/spread snapshot spread_points must be positive")

    return snapshot, violations


def extract_account_snapshot(record: dict[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    aliases = {
        "account_server": ("account_server", "server"),
        "account_currency": ("account_currency", "currency"),
        "balance": ("balance",),
        "equity": ("equity",),
        "profit": ("profit", "floating_profit", "floating_pnl"),
        "margin": ("margin", "margin_used"),
        "free_margin": ("free_margin", "margin_free", "freeMargin", "free margin"),
        "margin_level": ("margin_level", "margin_level_percent"),
        "margin_used_fraction": ("margin_used_fraction",),
        "canary_state": ("canary_state", "exact_canary_state"),
    }
    snapshot: dict[str, Any] = {}
    violations: list[str] = []

    if isinstance(record, dict):
        for canonical_key, key_aliases in aliases.items():
            value = first_key_value(record, key_aliases)
            if value is not None:
                snapshot[canonical_key] = value

    for numeric_key in ("balance", "equity", "profit", "margin", "free_margin"):
        if numeric_key in snapshot:
            converted = coerce_float(snapshot[numeric_key])
            if converted is None:
                violations.append(f"account snapshot {numeric_key} is not numeric")
            else:
                snapshot[numeric_key] = converted

    for required_key in ("equity", "profit", "margin", "free_margin"):
        if required_key not in snapshot:
            violations.append(f"account snapshot missing {required_key}")

    return snapshot, violations

def extract_exposure_snapshot(record: dict[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    snapshot: dict[str, Any] = {
        "expected_identity": dict(EXPECTED_IDENTITY),
        "exact_canary_state": first_key_value(record, ("exact_canary_state", "canary_state")) if isinstance(record, dict) else None,
        "h024_position_count": first_key_value(record, ("h024_position_count",)) if isinstance(record, dict) else None,
        "h024_order_count": first_key_value(record, ("h024_order_count",)) if isinstance(record, dict) else None,
    }
    violations: list[str] = []

    if not isinstance(record, dict):
        return snapshot, ["exposure snapshot source missing"]

    best: dict[str, Any] | None = None
    for candidate in candidate_dicts(record):
        if candidate.get("symbol") == "XAUUSDm" or candidate.get("runtime_symbol") == "XAUUSDm":
            best = candidate
            break
        if candidate.get("ticket") == 4413054432 or candidate.get("identifier") == 4413054432:
            best = candidate
            break

    source = best or record
    observed = {
        "exact_ticket": coerce_int(first_key_value(source, ("exact_ticket", "ticket"))),
        "exact_identifier": coerce_int(first_key_value(source, ("exact_identifier", "identifier"))),
        "runtime_symbol": first_key_value(source, ("runtime_symbol", "symbol")),
        "magic": coerce_int(first_key_value(source, ("magic",))),
        "volume": coerce_float(first_key_value(source, ("volume",))),
        "position_type": coerce_int(first_key_value(source, ("position_type", "type"))),
    }
    if observed["exact_identifier"] is None:
        observed["exact_identifier"] = observed["exact_ticket"]

    snapshot["observed_identity"] = observed

    for key, expected in EXPECTED_IDENTITY.items():
        if key == "model_symbol":
            continue
        actual = observed.get(key)
        if key == "volume":
            if actual is None or abs(float(actual) - float(expected)) > 1e-9:
                violations.append(f"exact canary {key} mismatch: {actual!r} != {expected!r}")
        elif actual != expected:
            violations.append(f"exact canary {key} mismatch: {actual!r} != {expected!r}")

    return snapshot, violations


def build_default_operator_decision(
    *,
    now: datetime,
    decision_preview_status: str = "NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY",
    requested_action: str = "NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY",
    operator_id: str = "NO_OPERATOR_DECISION_REQUESTED",
    operator_note: str = "",
    preview_stop_loss: float | None = None,
    preview_take_profit: float | None = None,
    operator_attests_exact_ticket_identity: bool = False,
) -> dict[str, Any]:
    return {
        "decision_preview_status": decision_preview_status,
        "requested_action": requested_action,
        "decision_created_at_utc": isoformat_utc(now),
        "operator_id": operator_id,
        "operator_note": operator_note,
        **EXPECTED_IDENTITY,
        "operator_attests_exact_ticket_identity": operator_attests_exact_ticket_identity,
        "operator_attests_preview_only": True,
        "operator_attests_no_broker_mutation_authorized": True,
        "operator_attests_no_order_check_authorized": True,
        "operator_attests_no_order_send_authorized": True,
        "operator_attests_no_close_modify_authorized": True,
        "close_preview_requested": requested_action == "PREVIEW_CLOSE_ONLY",
        "modify_stop_loss_preview_requested": requested_action in ("PREVIEW_MODIFY_STOP_LOSS_ONLY", "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT"),
        "modify_take_profit_preview_requested": requested_action in ("PREVIEW_MODIFY_TAKE_PROFIT_ONLY", "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT"),
        "preview_stop_loss": preview_stop_loss,
        "preview_take_profit": preview_take_profit,
        "operator_decision_v2_preview_authorizes_action": False,
        "live_broker_request_constructed": False,
        "dry_run_request_shape_preview_constructed": False,
        "dry_run_request_shape_preview_authorizes_execution": False,
    }


def validate_operator_decision_preview(decision: dict[str, Any], *, now: datetime, max_decision_age_seconds: float) -> list[str]:
    violations: list[str] = []
    status = decision.get("decision_preview_status")
    action = decision.get("requested_action")

    if status not in ALLOWED_DECISION_PREVIEW_STATUSES:
        violations.append(f"invalid decision_preview_status: {status!r}")
    if action not in ALLOWED_REQUESTED_ACTIONS:
        violations.append(f"invalid requested_action: {action!r}")

    if status == "NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY":
        if action != "NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY":
            violations.append("no-decision status must use no-close-modify requested action")
        if decision.get("operator_id") not in (None, "", "NO_OPERATOR_DECISION_REQUESTED"):
            violations.append("no-decision status must not carry a real operator_id")
        if decision.get("preview_stop_loss") is not None or decision.get("preview_take_profit") is not None:
            violations.append("no-decision status must not carry stop-loss/take-profit preview values")

    if status == "OPERATOR_INTENT_RECORDED_V2_PREVIEW_ONLY":
        if action == "NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY":
            violations.append("recorded operator intent must request a preview action")
        if not decision.get("operator_id") or decision.get("operator_id") == "NO_OPERATOR_DECISION_REQUESTED":
            violations.append("recorded operator intent requires non-empty operator_id")
        if decision.get("operator_attests_exact_ticket_identity") is not True:
            violations.append("recorded operator intent requires exact-ticket identity attestation")
        if decision.get("operator_attests_preview_only") is not True:
            violations.append("recorded operator intent requires preview-only attestation")

    for field, label in (
        ("operator_attests_no_broker_mutation_authorized", "no-broker-mutation"),
        ("operator_attests_no_order_check_authorized", "no-order-check"),
        ("operator_attests_no_order_send_authorized", "no-order-send"),
        ("operator_attests_no_close_modify_authorized", "no-close-modify"),
    ):
        if decision.get(field) is not True:
            violations.append(f"missing {label} authorization attestation")

    expected_flags = {
        "NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY": set(),
        "PREVIEW_CLOSE_ONLY": {"close_preview_requested"},
        "PREVIEW_MODIFY_STOP_LOSS_ONLY": {"modify_stop_loss_preview_requested"},
        "PREVIEW_MODIFY_TAKE_PROFIT_ONLY": {"modify_take_profit_preview_requested"},
        "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT": {"modify_stop_loss_preview_requested", "modify_take_profit_preview_requested"},
    }
    active_flags = {field for field in ("close_preview_requested", "modify_stop_loss_preview_requested", "modify_take_profit_preview_requested") if decision.get(field) is True}
    if action in expected_flags and active_flags != expected_flags[action]:
        violations.append(f"preview action flags do not match requested_action: {action}")

    if action in ("PREVIEW_MODIFY_STOP_LOSS_ONLY", "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT") and coerce_float(decision.get("preview_stop_loss")) is None:
        violations.append("stop-loss modify preview requires numeric preview_stop_loss")
    if action in ("PREVIEW_MODIFY_TAKE_PROFIT_ONLY", "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT") and coerce_float(decision.get("preview_take_profit")) is None:
        violations.append("take-profit modify preview requires numeric preview_take_profit")
    if action == "PREVIEW_CLOSE_ONLY" and (decision.get("preview_stop_loss") is not None or decision.get("preview_take_profit") is not None):
        violations.append("close-only preview must not include stop-loss/take-profit preview values")

    created = parse_utc_timestamp(decision.get("decision_created_at_utc"))
    if created is None:
        violations.append("decision_created_at_utc missing or malformed")
    else:
        age = (now - created).total_seconds()
        if age > max_decision_age_seconds:
            violations.append(f"operator decision stale: age_seconds={age:.3f} max={max_decision_age_seconds}")
        if age < -300:
            violations.append(f"operator decision timestamp too far in the future: age_seconds={age:.3f}")

    for key, expected in EXPECTED_IDENTITY.items():
        actual = decision.get(key)
        if key == "volume":
            if coerce_float(actual) != expected:
                violations.append(f"decision identity {key} mismatch: {actual!r} != {expected!r}")
        elif actual != expected:
            violations.append(f"decision identity {key} mismatch: {actual!r} != {expected!r}")

    return violations


def build_packet(
    *,
    reports_dir: Path = Path("reports"),
    now: datetime | None = None,
    max_upstream_age_seconds: float = 900.0,
    max_decision_age_seconds: float = 900.0,
    operator_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = now or utc_now()
    upstream, violations = load_upstream_reports(Path(reports_dir), now=now, max_age_seconds=max_upstream_age_seconds)
    operator_decision = operator_decision or build_default_operator_decision(now=now)

    violations.extend(validate_operator_decision_preview(operator_decision, now=now, max_decision_age_seconds=max_decision_age_seconds))

    exposure_snapshot, exposure_violations = extract_exposure_snapshot(upstream.get("runtime_exposure_inventory"))
    account_snapshot, account_violations = extract_account_snapshot(upstream.get("runtime_account_risk_margin"))
    tick_snapshot, tick_violations = extract_tick_spread_snapshot(upstream.get("runtime_tick_spread"))
    violations.extend(exposure_violations)
    violations.extend(account_violations)
    violations.extend(tick_violations)

    manual_preview = upstream.get("manual_approval_gate_preview") or {}
    manual_values = find_key_values(manual_preview, "manual_approval_gate_preview_authorizes_action")
    if not manual_values:
        violations.append("manual approval gate preview authorization field missing")
    elif any(value is True for value in manual_values):
        violations.append("manual approval gate preview authorizes action")

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
        "operator_decision_v2_preview_authorizes_action": False,
        "manual_approval_gate_preview_authorizes_action": False,
        "live_broker_request_constructed": False,
        "dry_run_request_shape_preview_constructed": False,
        "dry_run_request_shape_preview_authorizes_execution": False,
    }

    packet = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": isoformat_utc(now),
        "expected": {
            "identity": dict(EXPECTED_IDENTITY),
            "allowed_decision_preview_statuses": list(ALLOWED_DECISION_PREVIEW_STATUSES),
            "allowed_requested_actions": list(ALLOWED_REQUESTED_ACTIONS),
            "max_upstream_age_seconds": max_upstream_age_seconds,
            "max_decision_age_seconds": max_decision_age_seconds,
        },
        "operator_decision_v2_preview_schema": operator_decision,
        "read_only_evidence": {
            "upstream_report_names": dict(UPSTREAM_REPORTS),
            "exposure_inventory_snapshot": exposure_snapshot,
            "account_risk_margin_snapshot": account_snapshot,
            "xauusdm_tick_spread_snapshot": tick_snapshot,
        },
        "upstream": {
            name: {
                "verdict": record.get("verdict") if isinstance(record, dict) else None,
                "operator_state": record.get("operator_state") if isinstance(record, dict) else None,
                "observed_at_utc": first_key_value(record, ("observed_at_utc", "generated_at_utc", "created_at_utc")) if isinstance(record, dict) else None,
                "age_seconds": report_age_seconds(record, now) if isinstance(record, dict) else None,
                "embedded_violations": embedded_violations(record) if isinstance(record, dict) else ["missing upstream record"],
            }
            for name, record in upstream.items()
        },
        "checks": {
            "all_upstreams_present_pass_fresh_and_non_authorizing": not any(item.startswith("upstream ") for item in violations),
            "exact_ticket_identity_locked": not any("exact canary" in item or "decision identity" in item for item in violations),
            "operator_decision_non_ambiguous": not any(
                fragment in item
                for item in violations
                for fragment in ("invalid ", "must ", "requires ", "stale", "flags do not match")
            ),
            "manual_approval_gate_preview_non_authorizing": not any("manual approval gate preview authorizes action" in item for item in violations),
            "no_live_or_dry_run_broker_request_constructed": True,
        },
        "authorizations": authorizations,
        **authorizations,
        "operator_state": PASS_OPERATOR_STATE if not violations else FAIL_OPERATOR_STATE,
        "operator_next_action": PASS_OPERATOR_NEXT_ACTION if not violations else FAIL_OPERATOR_NEXT_ACTION,
        "violations": violations,
        "verdict": PASS_VERDICT if not violations else FAIL_VERDICT,
    }
    return packet


def verify_record(record: dict[str, Any], *, require_pass: bool = False) -> list[str]:
    violations: list[str] = []
    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append(f"schema_version mismatch: {record.get('schema_version')!r}")
    if record.get("strategy") != STRATEGY:
        violations.append(f"strategy mismatch: {record.get('strategy')!r}")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append(f"packet_type mismatch: {record.get('packet_type')!r}")
    if record.get("verdict") not in (PASS_VERDICT, FAIL_VERDICT):
        violations.append(f"invalid verdict: {record.get('verdict')!r}")
    if require_pass and record.get("verdict") != PASS_VERDICT:
        violations.append(f"--require-pass set but record verdict is {record.get('verdict')!r}")
    if record.get("operator_state") not in (PASS_OPERATOR_STATE, FAIL_OPERATOR_STATE):
        violations.append(f"unexpected operator_state: {record.get('operator_state')!r}")
    if record.get("operator_next_action") not in (PASS_OPERATOR_NEXT_ACTION, FAIL_OPERATOR_NEXT_ACTION):
        violations.append(f"unexpected operator_next_action: {record.get('operator_next_action')!r}")

    top_violations = record.get("violations")
    if not isinstance(top_violations, list):
        violations.append("record violations field missing or not a list")
    elif record.get("verdict") == PASS_VERDICT and top_violations:
        violations.append("PASS record contains violations")

    violations.extend(check_authorization_blocked(record, "record"))

    for field in BLOCKING_FIELDS:
        values = find_key_values(record, field)
        if any(value is True for value in values):
            violations.append(f"unsafe true blocking/action field: {field}")

    decision = record.get("operator_decision_v2_preview_schema")
    if not isinstance(decision, dict):
        violations.append("operator_decision_v2_preview_schema missing or malformed")
    else:
        now = parse_utc_timestamp(record.get("observed_at_utc")) or utc_now()
        violations.extend(validate_operator_decision_preview(decision, now=now, max_decision_age_seconds=10**12))

    evidence = record.get("read_only_evidence")
    if not isinstance(evidence, dict):
        violations.append("read_only_evidence missing or malformed")
    else:
        tick = evidence.get("xauusdm_tick_spread_snapshot")
        account = evidence.get("account_risk_margin_snapshot")
        if not isinstance(tick, dict):
            violations.append("xauusdm_tick_spread_snapshot missing or malformed")
        else:
            for key in ("bid", "ask", "spread_points"):
                if key not in tick:
                    violations.append(f"xauusdm_tick_spread_snapshot missing {key}")
        if not isinstance(account, dict):
            violations.append("account_risk_margin_snapshot missing or malformed")
        else:
            for key in ("equity", "profit", "margin", "free_margin"):
                if key not in account:
                    violations.append(f"account_risk_margin_snapshot missing {key}")

    upstream = record.get("upstream")
    if not isinstance(upstream, dict):
        violations.append("upstream summary missing or malformed")
    else:
        for name in UPSTREAM_REPORTS:
            summary = upstream.get(name)
            if not isinstance(summary, dict):
                violations.append(f"upstream summary missing {name}")
                continue
            if record.get("verdict") == PASS_VERDICT and summary.get("verdict") != PASS_VERDICT:
                violations.append(f"PASS record has non-PASS upstream {name}: {summary.get('verdict')!r}")
            if summary.get("embedded_violations"):
                violations.append(f"upstream summary {name} contains embedded violations")

    return violations


def verify_jsonl_file(path: Path, *, require_pass: bool = False) -> dict[str, Any]:
    records, read_violations = read_jsonl_records(path)
    violations = list(read_violations)
    for index, record in enumerate(records, start=1):
        violations.extend(f"record {index}: {item}" for item in verify_record(record, require_pass=require_pass))
    return {
        "path": str(path),
        "record_count": len(records),
        "violations": violations,
        "verdict": PASS_VERDICT if not violations else FAIL_VERDICT,
        "last_record": records[-1] if records else None,
    }


def write_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def run_upstream_builders() -> list[str]:
    violations: list[str] = []
    for script, extra_args in UPSTREAM_BUILDERS:
        if not Path(script).exists():
            violations.append(f"missing upstream builder script: {script}")
            continue
        completed = subprocess.run([sys.executable, script, *extra_args], text=True, capture_output=True)
        if completed.returncode != 0:
            violations.append(
                f"upstream builder failed: {script} rc={completed.returncode} "
                f"stdout={completed.stdout[-1000:]} stderr={completed.stderr[-1000:]}"
            )
    return violations


def build_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build H024 exact-ticket operator decision v2 preview JSONL.")
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--output", default=str(DEFAULT_REPORT_PATH))
    parser.add_argument("--skip-upstream-build", action="store_true")
    parser.add_argument("--max-upstream-age-seconds", type=float, default=900.0)
    parser.add_argument("--max-decision-age-seconds", type=float, default=900.0)
    parser.add_argument("--decision-preview-status", default="NO_OPERATOR_DECISION_REQUESTED_V2_PREVIEW_ONLY")
    parser.add_argument("--requested-action", default="NO_CLOSE_MODIFY_REQUESTED_V2_PREVIEW_ONLY")
    parser.add_argument("--operator-id", default="NO_OPERATOR_DECISION_REQUESTED")
    parser.add_argument("--operator-note", default="")
    parser.add_argument("--preview-stop-loss", type=float, default=None)
    parser.add_argument("--preview-take-profit", type=float, default=None)
    parser.add_argument("--operator-attests-exact-ticket-identity", action="store_true")
    parser.add_argument("--position-open-over-three-bars", action="store_true")
    args = parser.parse_args(argv)

    builder_violations: list[str] = []
    if not args.skip_upstream_build:
        builder_violations.extend(run_upstream_builders())

    now = utc_now()
    decision = build_default_operator_decision(
        now=now,
        decision_preview_status=args.decision_preview_status,
        requested_action=args.requested_action,
        operator_id=args.operator_id,
        operator_note=args.operator_note,
        preview_stop_loss=args.preview_stop_loss,
        preview_take_profit=args.preview_take_profit,
        operator_attests_exact_ticket_identity=args.operator_attests_exact_ticket_identity,
    )
    packet = build_packet(
        reports_dir=Path(args.reports_dir),
        now=now,
        max_upstream_age_seconds=args.max_upstream_age_seconds,
        max_decision_age_seconds=args.max_decision_age_seconds,
        operator_decision=decision,
    )
    if builder_violations:
        packet["violations"].extend(builder_violations)
        packet["verdict"] = FAIL_VERDICT
        packet["operator_state"] = FAIL_OPERATOR_STATE
        packet["operator_next_action"] = FAIL_OPERATOR_NEXT_ACTION

    output = Path(args.output)
    write_jsonl(output, packet)

    print(f"Wrote {output}")
    print(f"Verdict: {packet['verdict']}")
    print(f"Violations: {len(packet['violations'])}")
    print(f"Operator state: {packet['operator_state']}")
    print(f"Operator next action: {packet['operator_next_action']}")
    print(f"Exact ticket: {EXPECTED_IDENTITY['exact_ticket']}")
    print(f"Exact identifier: {EXPECTED_IDENTITY['exact_identifier']}")
    for field in ("effective_new_entries_blocked",) + AUTHORIZATION_FIELDS:
        print(f"{field}: {packet[field]}")
    print(f"operator_decision_v2_preview_authorizes_action: {packet['operator_decision_v2_preview_authorizes_action']}")
    print(f"live_broker_request_constructed: {packet['live_broker_request_constructed']}")
    print(f"dry_run_request_shape_preview_constructed: {packet['dry_run_request_shape_preview_constructed']}")
    return 0 if packet["verdict"] == PASS_VERDICT else 1


def verify_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify H024 exact-ticket operator decision v2 preview JSONL.")
    parser.add_argument("path")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args(argv)

    result = verify_jsonl_file(Path(args.path), require_pass=args.require_pass)
    last = result["last_record"] or {}

    print("H024 exact-ticket canary close/modify operator decision v2 preview records:", result["record_count"])
    print("Violations:", len(result["violations"]))
    for violation in result["violations"]:
        print("VIOLATION:", violation)
    print("Verifier verdict:", result["verdict"])
    if last:
        print("Record verdict:", last.get("verdict"))
        print("Operator state:", last.get("operator_state"))
        print("Operator next action:", last.get("operator_next_action"))
        print("Exact ticket:", EXPECTED_IDENTITY["exact_ticket"])
        print("Exact identifier:", EXPECTED_IDENTITY["exact_identifier"])
        for field in ("effective_new_entries_blocked",) + AUTHORIZATION_FIELDS:
            print(f"{field}: {last.get(field)}")
        print("operator_decision_v2_preview_authorizes_action:", last.get("operator_decision_v2_preview_authorizes_action"))
        print("live_broker_request_constructed:", last.get("live_broker_request_constructed"))
        print("dry_run_request_shape_preview_constructed:", last.get("dry_run_request_shape_preview_constructed"))

    return 0 if result["verdict"] == PASS_VERDICT else 1
