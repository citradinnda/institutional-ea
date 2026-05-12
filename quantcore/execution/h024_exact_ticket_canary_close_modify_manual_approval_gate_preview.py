from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = "1.0"
STRATEGY = "H024"
PACKET_TYPE = "h024_exact_ticket_canary_close_modify_manual_approval_gate_preview"

PASS_VERDICT = "PASS"
FAIL_VERDICT = "FAIL_CLOSED"

PASS_OPERATOR_STATE = (
    "EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_OK_BUT_ACTION_NOT_AUTHORIZED"
)
PASS_OPERATOR_NEXT_ACTION = (
    "KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_MANUAL_APPROVAL_GATE_PREVIEW"
)
FAIL_OPERATOR_STATE = (
    "FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_MANUAL_APPROVAL_GATE_PREVIEW_BLOCKED"
)
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

EXPECTED_SERVER = "Exness-MT5Trial6"
EXPECTED_ACCOUNT_CURRENCY = "USD"
EXPECTED_RUNTIME_SYMBOL = "XAUUSDm"
EXPECTED_MODEL_SYMBOL = "XAUUSD"
EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_MAGIC = 240024
EXPECTED_VOLUME = 0.01
EXPECTED_POSITION_TYPE = 1

DEFAULT_MAX_UPSTREAM_AGE_SECONDS = 300.0
DEFAULT_MAX_FUTURE_SKEW_SECONDS = 60.0

REPORT_PATHS = {
    "no_mutation_gate": Path("reports/h024_runtime_no_mutation_safety_gate.jsonl"),
    "unified_runtime_supervision": Path(
        "reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl"
    ),
    "exact_ticket_governance": Path(
        "reports/h024_exact_ticket_canary_close_modify_governance.jsonl"
    ),
    "decision_artifact": Path(
        "reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl"
    ),
    "pre_action_evidence_aggregate": Path(
        "reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl"
    ),
    "bar_age_exit_condition_evidence": Path(
        "reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl"
    ),
    "runtime_exposure_inventory": Path(
        "reports/h024_runtime_exposure_inventory_safety_supervisor.jsonl"
    ),
    "runtime_account_risk_margin": Path(
        "reports/h024_runtime_account_risk_margin_safety_supervisor.jsonl"
    ),
    "runtime_tick_spread": Path(
        "reports/h024_runtime_tick_spread_safety_supervisor.jsonl"
    ),
}

AUTHORIZATION_FALSE_FIELDS = (
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

EXACT_IDENTITY_UPSTREAMS = (
    "exact_ticket_governance",
    "decision_artifact",
    "pre_action_evidence_aggregate",
    "bar_age_exit_condition_evidence",
    "runtime_exposure_inventory",
)

ACTION_PREVIEW_SCHEMA = {
    "schema_name": "h024_exact_ticket_manual_close_modify_approval_preview",
    "schema_version": SCHEMA_VERSION,
    "preview_only": True,
    "approval_preview_status": "NO_MANUAL_APPROVAL_REQUESTED_PREVIEW_ONLY",
    "requested_action": "NO_CLOSE_MODIFY_REQUESTED_PREVIEW_ONLY",
    "allowed_requested_action_values": [
        "NO_CLOSE_MODIFY_REQUESTED_PREVIEW_ONLY",
        "PREVIEW_CLOSE_ONLY",
        "PREVIEW_MODIFY_STOP_LOSS_ONLY",
        "PREVIEW_MODIFY_TAKE_PROFIT_ONLY",
        "PREVIEW_MODIFY_STOP_LOSS_AND_TAKE_PROFIT",
    ],
    "required_non_ambiguous_operator_fields": [
        "approval_preview_status",
        "requested_action",
        "exact_ticket",
        "exact_identifier",
        "runtime_symbol",
        "model_symbol",
        "magic",
        "position_type",
        "volume",
        "operator_attests_exact_ticket_identity",
        "operator_attests_preview_only",
        "operator_attests_no_broker_mutation_authorized",
        "operator_attests_no_order_check_authorized",
        "operator_attests_no_order_send_authorized",
        "operator_attests_no_close_modify_authorized",
    ],
    "operator_attestation_fields": {
        "operator_attests_exact_ticket_identity": False,
        "operator_attests_preview_only": True,
        "operator_attests_no_broker_mutation_authorized": True,
        "operator_attests_no_order_check_authorized": True,
        "operator_attests_no_order_send_authorized": True,
        "operator_attests_no_close_modify_authorized": True,
    },
    "approval_preview_authorizes_action": False,
    "live_broker_request_constructed": False,
    "dry_run_request_shape_preview_constructed": False,
    "dry_run_request_shape_preview_authorizes_execution": False,
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc_datetime(raw: Any) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    text = raw.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def read_jsonl_record(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    violations: list[str] = []
    if not path.exists():
        return None, [f"{path}: missing upstream report"]
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return None, [f"{path}: unreadable upstream report: {exc}"]

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError as exc:
            violations.append(f"{path}: malformed JSONL line {line_number}: {exc}")
            continue
        if not isinstance(parsed, dict):
            violations.append(f"{path}: line {line_number} is not a JSON object")
            continue
        records.append(parsed)

    if not records:
        violations.append(f"{path}: no JSON object records found")
        return None, violations

    if len(records) != 1:
        violations.append(f"{path}: expected exactly 1 JSONL record, got {len(records)}")

    return records[-1], violations


def walk_values(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, Mapping):
        for child in value.values():
            yield from walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_values(child)


def walk_key_values(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield str(key), child
            yield from walk_key_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_key_values(child)


def get_first_by_keys(value: Mapping[str, Any], keys: Sequence[str]) -> Any:
    wanted = {key.lower() for key in keys}
    for key, child in walk_key_values(value):
        if key.lower() in wanted:
            return child
    return None


def get_all_by_keys(value: Mapping[str, Any], keys: Sequence[str]) -> list[Any]:
    wanted = {key.lower() for key in keys}
    return [child for key, child in walk_key_values(value) if key.lower() in wanted]


def coerce_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    return None


def coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def coerce_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return float(value)
    if isinstance(value, str):
        try:
            parsed = float(value.strip())
        except ValueError:
            return None
        if math.isfinite(parsed):
            return parsed
    return None


def authorization_value(record: Mapping[str, Any], field: str) -> Any:
    if field in record:
        return record[field]
    authorizations = record.get("authorizations")
    if isinstance(authorizations, Mapping) and field in authorizations:
        return authorizations[field]
    return None


def validate_effective_blocks(record: Mapping[str, Any], prefix: str) -> list[str]:
    violations: list[str] = []

    blocked = authorization_value(record, "effective_new_entries_blocked")
    if coerce_bool(blocked) is not True:
        violations.append(f"{prefix}: effective_new_entries_blocked must be true")

    for field in AUTHORIZATION_FALSE_FIELDS:
        raw = authorization_value(record, field)
        if coerce_bool(raw) is not False:
            violations.append(f"{prefix}: {field} must be false")

    gate_opens = get_first_by_keys(record, ("gate_opens_mutation_path",))
    if gate_opens is not None and coerce_bool(gate_opens) is not False:
        violations.append(f"{prefix}: gate_opens_mutation_path must be false when present")

    symbol_select = authorization_value(record, "symbol_select_authorized")
    if symbol_select is not None and coerce_bool(symbol_select) is not False:
        violations.append(f"{prefix}: symbol_select_authorized must be false when present")

    return violations


def values_contain_int(record: Mapping[str, Any], keys: Sequence[str], expected: int) -> bool:
    for raw in get_all_by_keys(record, keys):
        if coerce_int(raw) == expected:
            return True
    return False


def values_contain_string(record: Mapping[str, Any], keys: Sequence[str], expected: str) -> bool:
    for raw in get_all_by_keys(record, keys):
        if isinstance(raw, str) and raw == expected:
            return True
    return False


def values_contain_float(record: Mapping[str, Any], keys: Sequence[str], expected: float) -> bool:
    for raw in get_all_by_keys(record, keys):
        parsed = coerce_float(raw)
        if parsed is not None and abs(parsed - expected) < 1e-9:
            return True
    return False


def summarize_upstream(
    *,
    name: str,
    path: Path,
    record: Mapping[str, Any] | None,
    now: datetime,
    max_age_seconds: float,
    max_future_skew_seconds: float,
) -> tuple[dict[str, Any], list[str]]:
    if record is None:
        return {
            "name": name,
            "path": str(path),
            "loaded": False,
            "verdict": None,
            "age_seconds": None,
            "embedded_violations": None,
        }, [f"{name}: upstream record not loaded"]

    violations: list[str] = []
    verdict = record.get("verdict")
    embedded_violations = record.get("violations")
    if verdict != PASS_VERDICT:
        violations.append(f"{name}: upstream verdict must be PASS, got {verdict!r}")
    if embedded_violations not in ([], None):
        violations.append(f"{name}: upstream embedded violations must be empty")

    observed_at = (
        record.get("observed_at_utc")
        or record.get("generated_at_utc")
        or record.get("created_at_utc")
        or record.get("timestamp_utc")
    )
    parsed_observed_at = parse_utc_datetime(observed_at)
    age_seconds: float | None = None
    if parsed_observed_at is None:
        violations.append(f"{name}: missing or malformed observed_at_utc")
    else:
        age_seconds = (now - parsed_observed_at).total_seconds()
        if age_seconds > max_age_seconds:
            violations.append(
                f"{name}: upstream evidence is stale: age_seconds={age_seconds:.3f} "
                f"max={max_age_seconds:.3f}"
            )
        if age_seconds < -max_future_skew_seconds:
            violations.append(
                f"{name}: upstream evidence is future-skewed: age_seconds={age_seconds:.3f} "
                f"max_future_skew={max_future_skew_seconds:.3f}"
            )

    violations.extend(validate_effective_blocks(record, name))

    summary = {
        "name": name,
        "path": str(path),
        "loaded": True,
        "packet_type": record.get("packet_type"),
        "schema_version": record.get("schema_version"),
        "strategy": record.get("strategy"),
        "verdict": verdict,
        "operator_state": record.get("operator_state"),
        "operator_next_action": record.get("operator_next_action"),
        "observed_at_utc": observed_at,
        "age_seconds": age_seconds,
        "embedded_violations": len(embedded_violations)
        if isinstance(embedded_violations, list)
        else embedded_violations,
    }
    return summary, violations


def validate_exact_identity(upstreams: Mapping[str, Mapping[str, Any]]) -> list[str]:
    violations: list[str] = []
    ticket_keys = (
        "ticket",
        "position_ticket",
        "canary_ticket",
        "exact_ticket",
        "expected_ticket",
    )
    identifier_keys = (
        "identifier",
        "position_identifier",
        "canary_identifier",
        "exact_identifier",
        "expected_identifier",
    )
    symbol_keys = (
        "symbol",
        "runtime_symbol",
        "position_symbol",
        "canary_symbol",
        "exact_symbol",
        "expected_runtime_symbol",
    )
    magic_keys = ("magic", "position_magic", "expected_magic")
    volume_keys = ("volume", "position_volume", "expected_volume")
    type_keys = ("type", "position_type", "mt5_position_type", "expected_position_type")

    for name in EXACT_IDENTITY_UPSTREAMS:
        record = upstreams.get(name)
        if record is None:
            violations.append(f"{name}: missing exact-identity upstream")
            continue

        if not values_contain_int(record, ticket_keys, EXPECTED_TICKET):
            violations.append(f"{name}: missing exact ticket {EXPECTED_TICKET}")
        if not values_contain_int(record, identifier_keys, EXPECTED_IDENTIFIER):
            violations.append(f"{name}: missing exact identifier {EXPECTED_IDENTIFIER}")
        if not values_contain_string(record, symbol_keys, EXPECTED_RUNTIME_SYMBOL):
            violations.append(f"{name}: missing runtime symbol {EXPECTED_RUNTIME_SYMBOL}")

    exposure = upstreams.get("runtime_exposure_inventory")
    if exposure is not None:
        if not values_contain_int(exposure, magic_keys, EXPECTED_MAGIC):
            violations.append("runtime_exposure_inventory: missing expected magic 240024")
        if not values_contain_float(exposure, volume_keys, EXPECTED_VOLUME):
            violations.append("runtime_exposure_inventory: missing expected volume 0.01")
        if not values_contain_int(exposure, type_keys, EXPECTED_POSITION_TYPE):
            violations.append("runtime_exposure_inventory: missing expected MT5 position type 1")

        h024_position_count = get_first_by_keys(exposure, ("h024_position_count", "position_count"))
        if h024_position_count is not None and coerce_int(h024_position_count) != 1:
            violations.append("runtime_exposure_inventory: H024 position count must be exactly 1")

        h024_order_count = get_first_by_keys(exposure, ("h024_order_count", "order_count"))
        if h024_order_count is not None and coerce_int(h024_order_count) != 0:
            violations.append("runtime_exposure_inventory: H024 order count must be exactly 0")

        canary_observed = get_first_by_keys(exposure, ("exact_canary_observed",))
        if canary_observed is not None and coerce_bool(canary_observed) is not True:
            violations.append("runtime_exposure_inventory: exact_canary_observed must be true")

        canary_state = get_first_by_keys(exposure, ("canary_state", "exact_canary_state"))
        if canary_state is not None and canary_state != "OBSERVED_EXACT_KNOWN_CANARY":
            violations.append("runtime_exposure_inventory: canary state must be OBSERVED_EXACT_KNOWN_CANARY")

    return violations


def extract_account_snapshot(record: Mapping[str, Any] | None) -> dict[str, Any]:
    if record is None:
        return {}
    fields = {
        "server": ("server", "account_server"),
        "currency": ("currency", "account_currency"),
        "balance": ("balance",),
        "equity": ("equity",),
        "profit": ("profit", "floating_profit", "pnl", "floating_pnl"),
        "margin": ("margin",),
        "free_margin": ("free_margin", "margin_free"),
        "margin_level": ("margin_level",),
        "margin_used_fraction": ("margin_used_fraction",),
    }
    snapshot: dict[str, Any] = {}
    for output_key, source_keys in fields.items():
        value = get_first_by_keys(record, source_keys)
        if value is not None:
            snapshot[output_key] = value
    return snapshot


def extract_tick_spread_snapshot(record: Mapping[str, Any] | None) -> dict[str, Any]:
    if record is None:
        return {}

    symbols: dict[str, dict[str, Any]] = {}

    def consume_symbol_mapping(symbol: str, mapping: Mapping[str, Any]) -> None:
        snapshot: dict[str, Any] = {"symbol": symbol}

        for field in ("bid", "ask", "spread", "spread_points", "tick_age_seconds", "verdict"):
            if field in mapping:
                snapshot[field] = mapping.get(field)
            else:
                nested_value = get_first_by_keys(mapping, (field,))
                if nested_value is not None:
                    snapshot[field] = nested_value

        runtime_symbol = mapping.get("runtime_symbol")
        if isinstance(runtime_symbol, str):
            snapshot["runtime_symbol"] = runtime_symbol
        else:
            snapshot["runtime_symbol"] = symbol

        if any(key in snapshot for key in ("bid", "ask", "spread", "spread_points", "tick_age_seconds")):
            symbols[symbol] = snapshot

    def visit(value: Any) -> None:
        if isinstance(value, Mapping):
            for target_symbol in ("XAUUSDm", "USDJPYm"):
                direct_child = value.get(target_symbol)
                if isinstance(direct_child, Mapping):
                    consume_symbol_mapping(target_symbol, direct_child)

            symbol_value = (
                value.get("symbol")
                or value.get("runtime_symbol")
                or value.get("position_symbol")
            )
            if symbol_value in ("XAUUSDm", "USDJPYm"):
                consume_symbol_mapping(str(symbol_value), value)

            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(record)

    return symbols


def extract_exposure_snapshot(record: Mapping[str, Any] | None) -> dict[str, Any]:
    if record is None:
        return {}
    snapshot: dict[str, Any] = {
        "canary_state": get_first_by_keys(record, ("canary_state", "exact_canary_state")),
        "exact_canary_observed": get_first_by_keys(record, ("exact_canary_observed",)),
        "h024_position_count": get_first_by_keys(record, ("h024_position_count", "position_count")),
        "h024_order_count": get_first_by_keys(record, ("h024_order_count", "order_count")),
        "ticket": EXPECTED_TICKET,
        "identifier": EXPECTED_IDENTIFIER,
        "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
        "model_symbol": EXPECTED_MODEL_SYMBOL,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "position_type": EXPECTED_POSITION_TYPE,
    }
    return {key: value for key, value in snapshot.items() if value is not None}


def validate_evidence_snapshots(
    *,
    account_snapshot: Mapping[str, Any],
    tick_spread_snapshot: Mapping[str, Any],
    exposure_snapshot: Mapping[str, Any],
) -> list[str]:
    violations: list[str] = []

    if account_snapshot.get("server") not in (EXPECTED_SERVER, None):
        violations.append("account risk snapshot server mismatch")
    if account_snapshot.get("currency") not in (EXPECTED_ACCOUNT_CURRENCY, None):
        violations.append("account risk snapshot currency mismatch")

    for field in ("balance", "equity", "profit", "margin", "free_margin"):
        if field not in account_snapshot:
            violations.append(f"account risk snapshot missing {field}")

    if EXPECTED_RUNTIME_SYMBOL not in tick_spread_snapshot:
        violations.append("tick/spread snapshot missing XAUUSDm")
    else:
        xauusd = tick_spread_snapshot[EXPECTED_RUNTIME_SYMBOL]
        if isinstance(xauusd, Mapping):
            for field in ("bid", "ask", "spread_points"):
                if xauusd.get(field) is None:
                    violations.append(f"XAUUSDm tick/spread snapshot missing {field}")

    if exposure_snapshot.get("ticket") != EXPECTED_TICKET:
        violations.append("exposure snapshot exact ticket mismatch")
    if exposure_snapshot.get("identifier") != EXPECTED_IDENTIFIER:
        violations.append("exposure snapshot exact identifier mismatch")
    if exposure_snapshot.get("runtime_symbol") != EXPECTED_RUNTIME_SYMBOL:
        violations.append("exposure snapshot exact runtime symbol mismatch")

    return violations


def build_manual_approval_gate_preview_record(
    *,
    report_paths: Mapping[str, Path] | None = None,
    max_upstream_age_seconds: float = DEFAULT_MAX_UPSTREAM_AGE_SECONDS,
    max_future_skew_seconds: float = DEFAULT_MAX_FUTURE_SKEW_SECONDS,
    observed_at: datetime | None = None,
) -> dict[str, Any]:
    now = observed_at or utc_now()
    paths = dict(REPORT_PATHS)
    if report_paths is not None:
        paths.update(report_paths)

    violations: list[str] = []
    upstream_records: dict[str, dict[str, Any]] = {}
    upstream_summaries: dict[str, dict[str, Any]] = {}

    for name, path in paths.items():
        record, read_violations = read_jsonl_record(path)
        violations.extend([f"{name}: {item}" for item in read_violations])
        if record is not None:
            upstream_records[name] = record
        summary, upstream_violations = summarize_upstream(
            name=name,
            path=path,
            record=record,
            now=now,
            max_age_seconds=max_upstream_age_seconds,
            max_future_skew_seconds=max_future_skew_seconds,
        )
        upstream_summaries[name] = summary
        violations.extend(upstream_violations)

    violations.extend(validate_exact_identity(upstream_records))

    account_snapshot = extract_account_snapshot(upstream_records.get("runtime_account_risk_margin"))
    tick_spread_snapshot = extract_tick_spread_snapshot(upstream_records.get("runtime_tick_spread"))
    exposure_snapshot = extract_exposure_snapshot(upstream_records.get("runtime_exposure_inventory"))

    violations.extend(
        validate_evidence_snapshots(
            account_snapshot=account_snapshot,
            tick_spread_snapshot=tick_spread_snapshot,
            exposure_snapshot=exposure_snapshot,
        )
    )

    approval_preview = {
        **ACTION_PREVIEW_SCHEMA,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
        "model_symbol": EXPECTED_MODEL_SYMBOL,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "position_type": EXPECTED_POSITION_TYPE,
    }

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
        "symbol_select_authorized": False,
        "manual_approval_gate_preview_authorizes_action": False,
        "live_broker_request_constructed": False,
        "dry_run_request_shape_preview_constructed": False,
    }

    checks = {
        "upstream_packets_required": {
            "passed": set(upstream_summaries) == set(REPORT_PATHS),
            "detail": "all required upstream packet paths are configured",
        },
        "all_upstream_packets_pass": {
            "passed": all(summary.get("verdict") == PASS_VERDICT for summary in upstream_summaries.values()),
            "detail": "every consumed upstream packet must have verdict PASS",
        },
        "all_authorizations_remain_blocked": {
            "passed": not validate_effective_blocks({**authorizations}, "manual_approval_gate_preview"),
            "detail": "all direct action authorization fields remain non-authorizing",
        },
        "exact_ticket_identity_locked": {
            "passed": EXPECTED_TICKET == EXPECTED_IDENTIFIER == 4413054432,
            "detail": "exact ticket/identifier 4413054432 is hard-locked for preview",
        },
        "preview_only_no_live_request": {
            "passed": (
                approval_preview["preview_only"] is True
                and approval_preview["approval_preview_authorizes_action"] is False
                and approval_preview["live_broker_request_constructed"] is False
            ),
            "detail": "manual approval gate preview is review-only and constructs no live request",
        },
        "runtime_risk_evidence_present": {
            "passed": bool(account_snapshot),
            "detail": "account risk/margin snapshot was extracted from runtime account evidence",
        },
        "runtime_tick_spread_evidence_present": {
            "passed": EXPECTED_RUNTIME_SYMBOL in tick_spread_snapshot,
            "detail": "XAUUSDm tick/spread snapshot was extracted from runtime tick/spread evidence",
        },
    }

    verdict = PASS_VERDICT if not violations else FAIL_VERDICT

    record = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": isoformat_z(now),
        "expected": {
            "server": EXPECTED_SERVER,
            "account_currency": EXPECTED_ACCOUNT_CURRENCY,
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "ticket": EXPECTED_TICKET,
            "identifier": EXPECTED_IDENTIFIER,
            "magic": EXPECTED_MAGIC,
            "volume": EXPECTED_VOLUME,
            "position_type": EXPECTED_POSITION_TYPE,
            "max_upstream_age_seconds": max_upstream_age_seconds,
            "max_future_skew_seconds": max_future_skew_seconds,
        },
        "approval_preview_schema": approval_preview,
        "read_only_evidence": {
            "exposure": exposure_snapshot,
            "account_risk_margin": account_snapshot,
            "tick_spread": tick_spread_snapshot,
        },
        "upstreams": upstream_summaries,
        "checks": checks,
        "authorizations": authorizations,
        **authorizations,
        "operator_state": PASS_OPERATOR_STATE if verdict == PASS_VERDICT else FAIL_OPERATOR_STATE,
        "operator_next_action": PASS_OPERATOR_NEXT_ACTION if verdict == PASS_VERDICT else FAIL_OPERATOR_NEXT_ACTION,
        "violations": violations,
        "verdict": verdict,
    }

    return record


def write_jsonl(record: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def load_records(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    violations: list[str] = []
    if not path.exists():
        return [], [f"{path}: missing report"]
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return [], [f"{path}: unreadable report: {exc}"]

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError as exc:
            violations.append(f"{path}: malformed JSONL line {line_number}: {exc}")
            continue
        if not isinstance(parsed, dict):
            violations.append(f"{path}: line {line_number} is not a JSON object")
            continue
        records.append(parsed)

    if not records:
        violations.append(f"{path}: no records found")
    return records, violations


def verify_record(record: Mapping[str, Any]) -> list[str]:
    violations: list[str] = []

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append("schema_version mismatch")
    if record.get("strategy") != STRATEGY:
        violations.append("strategy mismatch")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append("packet_type mismatch")

    observed_at = parse_utc_datetime(record.get("observed_at_utc"))
    if observed_at is None:
        violations.append("observed_at_utc missing or malformed")

    embedded_violations = record.get("violations")
    if embedded_violations not in ([], None):
        violations.append("record contains embedded violations")

    violations.extend(validate_effective_blocks(record, "manual_approval_gate_preview"))

    approval_preview = record.get("approval_preview_schema")
    if not isinstance(approval_preview, Mapping):
        violations.append("approval_preview_schema missing or malformed")
    else:
        if approval_preview.get("exact_ticket") != EXPECTED_TICKET:
            violations.append("approval_preview_schema exact_ticket mismatch")
        if approval_preview.get("exact_identifier") != EXPECTED_IDENTIFIER:
            violations.append("approval_preview_schema exact_identifier mismatch")
        if approval_preview.get("runtime_symbol") != EXPECTED_RUNTIME_SYMBOL:
            violations.append("approval_preview_schema runtime_symbol mismatch")
        if approval_preview.get("preview_only") is not True:
            violations.append("approval_preview_schema preview_only must be true")
        for field in (
            "approval_preview_authorizes_action",
            "live_broker_request_constructed",
            "dry_run_request_shape_preview_constructed",
            "dry_run_request_shape_preview_authorizes_execution",
        ):
            if approval_preview.get(field) is not False:
                violations.append(f"approval_preview_schema {field} must be false")
        attestation = approval_preview.get("operator_attestation_fields")
        if not isinstance(attestation, Mapping):
            violations.append("operator_attestation_fields missing or malformed")
        else:
            if attestation.get("operator_attests_preview_only") is not True:
                violations.append("operator_attests_preview_only must be true")
            for field in (
                "operator_attests_no_broker_mutation_authorized",
                "operator_attests_no_order_check_authorized",
                "operator_attests_no_order_send_authorized",
                "operator_attests_no_close_modify_authorized",
            ):
                if attestation.get(field) is not True:
                    violations.append(f"{field} must be true")

    read_only_evidence = record.get("read_only_evidence")
    if not isinstance(read_only_evidence, Mapping):
        violations.append("read_only_evidence missing or malformed")
    else:
        account_snapshot = read_only_evidence.get("account_risk_margin")
        tick_spread_snapshot = read_only_evidence.get("tick_spread")
        exposure_snapshot = read_only_evidence.get("exposure")
        if not isinstance(account_snapshot, Mapping):
            violations.append("read_only_evidence.account_risk_margin missing or malformed")
            account_snapshot = {}
        if not isinstance(tick_spread_snapshot, Mapping):
            violations.append("read_only_evidence.tick_spread missing or malformed")
            tick_spread_snapshot = {}
        if not isinstance(exposure_snapshot, Mapping):
            violations.append("read_only_evidence.exposure missing or malformed")
            exposure_snapshot = {}
        violations.extend(
            validate_evidence_snapshots(
                account_snapshot=account_snapshot,
                tick_spread_snapshot=tick_spread_snapshot,
                exposure_snapshot=exposure_snapshot,
            )
        )

    upstreams = record.get("upstreams")
    if not isinstance(upstreams, Mapping):
        violations.append("upstreams missing or malformed")
    else:
        missing = set(REPORT_PATHS) - set(upstreams)
        extra = set(upstreams) - set(REPORT_PATHS)
        if missing:
            violations.append(f"missing upstream summaries: {sorted(missing)}")
        if extra:
            violations.append(f"unexpected upstream summaries: {sorted(extra)}")
        for name, summary in upstreams.items():
            if not isinstance(summary, Mapping):
                violations.append(f"upstream summary {name} malformed")
                continue
            if summary.get("verdict") != PASS_VERDICT:
                violations.append(f"upstream summary {name} verdict must be PASS")
            embedded = summary.get("embedded_violations")
            if embedded not in (0, [], None):
                violations.append(f"upstream summary {name} embedded violations must be 0")

    if record.get("verdict") == PASS_VERDICT and violations:
        violations.append("record verdict PASS is inconsistent with verifier violations")

    return violations


def verify_report(path: Path, *, require_pass: bool = False) -> tuple[list[dict[str, Any]], list[str]]:
    records, violations = load_records(path)
    if len(records) != 1:
        violations.append(f"expected exactly 1 record, got {len(records)}")

    for record in records:
        violations.extend(verify_record(record))
        if require_pass and record.get("verdict") != PASS_VERDICT:
            violations.append(f"--require-pass set but record verdict is {record.get('verdict')!r}")

    return records, violations


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build or verify the H024 exact-ticket manual approval gate preview packet."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument(
        "--output",
        default="reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl",
    )
    build_parser.add_argument("--max-upstream-age-seconds", type=float, default=DEFAULT_MAX_UPSTREAM_AGE_SECONDS)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("path")
    verify_parser.add_argument("--require-pass", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "build":
        record = build_manual_approval_gate_preview_record(
            max_upstream_age_seconds=args.max_upstream_age_seconds
        )
        output = Path(args.output)
        write_jsonl(record, output)
        print(f"Wrote {output}")
        print(f"Verdict: {record['verdict']}")
        print(f"Violations: {len(record['violations'])}")
        print(f"Operator state: {record['operator_state']}")
        print(f"Operator next action: {record['operator_next_action']}")
        print(f"Exact ticket: {EXPECTED_TICKET}")
        print(f"Exact identifier: {EXPECTED_IDENTIFIER}")
        print(f"Effective new entries blocked: {record['effective_new_entries_blocked']}")
        for field in AUTHORIZATION_FALSE_FIELDS:
            print(f"{field}: {record[field]}")
        return 0 if record["verdict"] == PASS_VERDICT else 1

    records, violations = verify_report(Path(args.path), require_pass=args.require_pass)
    print(f"H024 exact-ticket canary close/modify manual approval gate preview records: {len(records)}")
    print(f"Violations: {len(violations)}")
    if records:
        record = records[-1]
        print(f"Record verdict: {record.get('verdict')}")
        print(f"Verifier verdict: {'PASS' if not violations else 'FAIL_CLOSED'}")
        print(f"Operator state: {record.get('operator_state')}")
        print(f"Operator next action: {record.get('operator_next_action')}")
        print(f"Exact ticket: {EXPECTED_TICKET}")
        print(f"Exact identifier: {EXPECTED_IDENTIFIER}")
        print(f"Effective new entries blocked: {record.get('effective_new_entries_blocked')}")
        for field in AUTHORIZATION_FALSE_FIELDS:
            print(f"{field}: {record.get(field)}")
    for violation in violations:
        print(f"VIOLATION: {violation}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
