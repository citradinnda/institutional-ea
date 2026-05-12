"""Read-only H024 exact-ticket canary close/modify pre-action evidence aggregate."""

from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = "1.0"
STRATEGY = "H024"
PACKET_TYPE = "H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE"
PASS_VERDICT = "PASS"
FAIL_VERDICT = "FAIL_CLOSED"
OK_OPERATOR_STATE = "EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_OK_BUT_ACTION_NOT_AUTHORIZED"
OK_OPERATOR_NEXT_ACTION = "KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_PRE_ACTION_EVIDENCE_REVIEW"
FAIL_OPERATOR_STATE = "FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_PRE_ACTION_EVIDENCE_AGGREGATE_BLOCKED"
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_RUNTIME_SYMBOL = "XAUUSDm"
EXPECTED_MODEL_SYMBOL = "XAUUSD"
EXPECTED_SIDE = "sell"
EXPECTED_MT5_POSITION_TYPE = 1
EXPECTED_VOLUME = 0.01
EXPECTED_MAGIC = 240024
EXPECTED_CANARY_STATE = "OBSERVED_EXACT_KNOWN_CANARY"
EXPECTED_DECISION_STATUS = "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY"
EXPECTED_REQUESTED_ACTION = "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY"
DEFAULT_MAX_UPSTREAM_AGE_SECONDS = 300.0
DEFAULT_FUTURE_TOLERANCE_SECONDS = 60.0

UPSTREAM_PACKET_TYPES: Mapping[str, str] = {
    "no_mutation_gate": "H024_RUNTIME_NO_MUTATION_SAFETY_GATE",
    "unified_runtime_supervision": "H024_UNIFIED_READ_ONLY_POST_CANARY_RUNTIME_SUPERVISION",
    "exact_ticket_governance": "H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE",
    "decision_artifact": "H024_EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT",
}
AUTHORIZATION_KEYS: tuple[str, ...] = (
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
BLOCKED_KEYS: tuple[str, ...] = tuple(k.replace("authorized", "blocked") for k in AUTHORIZATION_KEYS)
IDENTITY_ALIASES: Mapping[str, tuple[str, ...]] = {
    "ticket": ("exact_ticket", "ticket", "position_ticket", "canary_ticket"),
    "identifier": ("exact_identifier", "identifier", "position_identifier", "canary_identifier"),
    "runtime_symbol": ("runtime_symbol", "symbol", "position_symbol"),
    "model_symbol": ("model_symbol",),
    "side": ("side", "position_side"),
    "mt5_position_type": ("mt5_position_type", "position_type", "type"),
    "volume": ("volume", "position_volume"),
    "magic": ("magic", "position_magic"),
    "exact_canary_state": ("exact_canary_state", "canary_state"),
    "exact_canary_observed": ("exact_canary_observed", "canary_observed"),
}
EXPECTED_IDENTITY: Mapping[str, Any] = {
    "ticket": EXPECTED_TICKET,
    "identifier": EXPECTED_IDENTIFIER,
    "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
    "model_symbol": EXPECTED_MODEL_SYMBOL,
    "side": EXPECTED_SIDE,
    "mt5_position_type": EXPECTED_MT5_POSITION_TYPE,
    "volume": EXPECTED_VOLUME,
    "magic": EXPECTED_MAGIC,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00") if value.strip().endswith("Z") else value.strip()
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _norm(key: str) -> str:
    return "".join(ch.lower() for ch in str(key) if ch.isalnum())


def _walk(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = (*path, str(key))
            yield child_path, child
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, (*path, str(index)))


def _values(record: Mapping[str, Any], aliases: Sequence[str]) -> list[Any]:
    wanted = {_norm(alias) for alias in aliases}
    return [value for path, value in _walk(record) if path and _norm(path[-1]) in wanted]


def _first(record: Mapping[str, Any], aliases: Sequence[str]) -> Any:
    values = _values(record, aliases)
    return values[0] if values else None


def _immediate_values(record: Mapping[str, Any], aliases: Sequence[str]) -> list[Any]:
    wanted = {_norm(alias) for alias in aliases}
    values: list[Any] = []
    for key, value in record.items():
        if _norm(key) in wanted:
            values.append(value)
    return values




def _coerce_observed_value(value: Any) -> Any:
    if isinstance(value, Mapping) and "observed" in value:
        return value.get("observed")
    return value


def _unwrapped_values(record: Mapping[str, Any], aliases: Sequence[str]) -> list[Any]:
    return [_coerce_observed_value(value) for value in _values(record, aliases)]

def _walk_mappings(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Mapping[str, Any]]]:
    if isinstance(value, Mapping):
        yield path, value
        for key, child in value.items():
            yield from _walk_mappings(child, (*path, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_mappings(child, (*path, str(index)))



def _identity_candidate_from_mapping(record: Mapping[str, Any]) -> dict[str, list[Any]]:
    candidate: dict[str, list[Any]] = {}
    for field, aliases in IDENTITY_ALIASES.items():
        values = [_coerce_observed_value(value) for value in _immediate_values(record, aliases)]
        values = [value for value in values if value is not None]
        if values:
            candidate[field] = values
    return candidate

def _candidate_has_expected_canary_anchor(candidate: Mapping[str, Sequence[Any]]) -> bool:
    for field, expected in EXPECTED_IDENTITY.items():
        values = candidate.get(field, ())
        for actual in values:
            if field in {"ticket", "identifier", "mt5_position_type", "magic"} and _as_int(actual) == int(expected):
                return True
            if field == "volume":
                as_float = _as_float(actual)
                if as_float is not None and abs(as_float - float(expected)) <= 1e-9:
                    return True
            if field not in {"ticket", "identifier", "mt5_position_type", "magic", "volume"} and str(actual) == str(expected):
                return True
    return False



def _identity_candidate_is_relevant(path: tuple[str, ...], candidate: Mapping[str, Sequence[Any]]) -> bool:
    if not candidate:
        return False

    lowered = tuple(str(part).lower() for part in path)
    path_text = ".".join(lowered)

    # Tick/spread expected symbol maps legitimately contain both XAUUSD and USDJPY.
    # They are market-data coverage evidence, not canary identity evidence.
    if "symbols" in lowered and (
        "tick_spread" in path_text
        or "tick_spread_record" in path_text
        or "market_data" in path_text
        or "runtime_tick_spread_safety_supervisor" in path_text
    ):
        return False

    # Any explicit exact-canary or H024 position context is identity evidence.
    if any(
        token in path_text
        for token in (
            "exact_canary",
            "known_canary",
            "canary_identity",
            "exact_ticket",
            "h024_position",
            "position",
            "decision_artifact",
            "governance",
        )
    ):
        return True

    # Ticket, identifier, and magic are sufficiently specific anchors for the exact canary.
    if any(field in candidate for field in ("ticket", "identifier", "magic")):
        return True

    return False

def _identity_candidates(record: Mapping[str, Any]) -> Iterable[tuple[tuple[str, ...], dict[str, list[Any]]]]:
    for path, mapping in _walk_mappings(record):
        candidate = _identity_candidate_from_mapping(mapping)
        if _identity_candidate_is_relevant(path, candidate):
            yield path, candidate


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().lower() in {"true", "false", "1", "0", "yes", "no"}:
        return value.strip().lower() in {"true", "1", "yes"}
    return None


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def _as_float(value: Any) -> float | None:
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


def extract_identity(record: Mapping[str, Any]) -> dict[str, Any]:
    extracted: dict[str, Any] = {}
    for _path, candidate in _identity_candidates(record):
        for field, values in candidate.items():
            if field not in extracted and values:
                extracted[field] = values[0]
    return extracted


def _timestamp(record: Mapping[str, Any]) -> Any:
    return _first(record, ("observed_at_utc", "generated_at_utc", "recorded_at_utc", "decision_timestamp_utc", "timestamp_utc"))


def _auth_value(record: Mapping[str, Any], key: str) -> Any:
    wanted = _norm(key)
    for top_key, value in record.items():
        if _norm(top_key) == wanted:
            return value
    for container_key in ("authorizations", "authorization", "execution_authorizations"):
        container = record.get(container_key)
        if isinstance(container, Mapping):
            for child_key, value in container.items():
                if _norm(child_key) == wanted:
                    return value
    return None


def _validate_auth_false(record: Mapping[str, Any], context: str) -> list[str]:
    violations: list[str] = []
    if _as_bool(_auth_value(record, "effective_new_entries_blocked")) is not True:
        violations.append(f"{context}: effective_new_entries_blocked is not true")
    for key in AUTHORIZATION_KEYS:
        value = _as_bool(_auth_value(record, key))
        if value is None:
            violations.append(f"{context}: missing authorization field {key}")
        elif value is not False:
            violations.append(f"{context}: unsafe authorization true for {key}")
    return violations


def _validate_identity(record: Mapping[str, Any], context: str, *, require_all: bool = False) -> list[str]:
    violations: list[str] = []
    present: dict[str, bool] = {field: False for field in EXPECTED_IDENTITY}
    relevant_candidate_seen = False

    for path, candidate in _identity_candidates(record):
        relevant_candidate_seen = True
        path_label = ".".join(path) or "<top-level>"
        for field, expected in EXPECTED_IDENTITY.items():
            vals = candidate.get(field, ())
            if vals:
                present[field] = True
            for actual in vals:
                if field in {"ticket", "identifier", "mt5_position_type", "magic"}:
                    if _as_int(actual) != int(expected):
                        violations.append(
                            f"{context}: {field} mismatch at {path_label}: expected {expected}, got {actual!r}"
                        )
                elif field == "volume":
                    as_float = _as_float(actual)
                    if as_float is None or abs(as_float - float(expected)) > 1e-9:
                        violations.append(
                            f"{context}: {field} mismatch at {path_label}: expected {expected}, got {actual!r}"
                        )
                elif str(actual) != str(expected):
                    violations.append(
                        f"{context}: {field} mismatch at {path_label}: expected {expected}, got {actual!r}"
                    )

    if require_all:
        if not relevant_candidate_seen:
            violations.append(f"{context}: missing required exact canary identity evidence")
        for field, was_present in present.items():
            if not was_present:
                violations.append(f"{context}: missing required exact canary identity field {field}")
    return violations




def _record_has_exact_canary_observed_true(record: Mapping[str, Any]) -> bool:
    explicit_values: list[Any] = []
    state_values: list[Any] = []

    for _path, mapping in _walk_mappings(record):
        for key, value in mapping.items():
            normalized = _norm(key)
            observed = _coerce_observed_value(value)
            if normalized in {"exactcanaryobserved", "canaryobserved"}:
                explicit_values.append(observed)
            elif normalized in {"exactcanarystate", "canarystate"}:
                state_values.append(observed)

    for value in explicit_values:
        as_bool = _as_bool(value)
        if as_bool is False:
            return False
    for value in explicit_values:
        as_bool = _as_bool(value)
        if as_bool is True:
            return True

    return EXPECTED_CANARY_STATE in state_values

def _packet_type_matches(actual: Any, expected: str) -> bool:
    return actual == expected or (isinstance(actual, str) and expected.lower() in actual.lower())




def _decision_values(record: Mapping[str, Any], key: str) -> list[Any]:
    aliases = (key, key.replace("_", " "), key.replace("_", "-"))
    wanted = {_norm(alias) for alias in aliases}
    values: list[Any] = []

    for _path, mapping in _walk_mappings(record):
        for child_key, child_value in mapping.items():
            if _norm(child_key) in wanted:
                coerced = _coerce_observed_value(child_value)
                if coerced is not None:
                    values.append(coerced)

    return values

def _validate_decision_values(record: Mapping[str, Any], context: str) -> list[str]:
    violations: list[str] = []
    for key in ("requested_action", "human_decision", "decision_status"):
        for value in _decision_values(record, key):
            if value not in {EXPECTED_DECISION_STATUS, EXPECTED_REQUESTED_ACTION}:
                violations.append(f"{context}: {key} is not non-authorizing: {value!r}")
    return violations



def _validate_upstream(
    key: str,
    record: Any,
    observed_at: datetime,
    max_age_seconds: float,
    future_tolerance_seconds: float,
) -> tuple[dict[str, Any], list[str]]:
    summary: dict[str, Any] = {"upstream_key": key}
    if not isinstance(record, Mapping):
        return summary, [f"{key}: missing or non-object upstream record"]

    summary.update(
        packet_type=record.get("packet_type"),
        verdict=record.get("verdict"),
        operator_state=record.get("operator_state"),
        operator_next_action=record.get("operator_next_action"),
        identity=extract_identity(record),
    )
    violations: list[str] = []

    if record.get("strategy") not in (STRATEGY, None):
        violations.append(f"{key}: wrong strategy {record.get('strategy')!r}")

    if not _packet_type_matches(record.get("packet_type"), UPSTREAM_PACKET_TYPES[key]):
        violations.append(f"{key}: wrong packet_type {record.get('packet_type')!r}; expected {UPSTREAM_PACKET_TYPES[key]}")

    if record.get("verdict") != PASS_VERDICT:
        violations.append(f"{key}: upstream verdict is not PASS")

    embedded = record.get("violations")
    summary["embedded_violation_count"] = len(embedded or []) if isinstance(embedded, list) else 0
    if embedded not in (None, []):
        violations.append(f"{key}: upstream contains embedded violations")

    upstream_ts = parse_utc_timestamp(_timestamp(record))
    if upstream_ts is None:
        violations.append(f"{key}: missing or malformed freshness timestamp")
        summary["age_seconds"] = None
    else:
        age_seconds = (observed_at - upstream_ts).total_seconds()
        summary["observed_at_utc"] = upstream_ts.isoformat().replace("+00:00", "Z")
        summary["age_seconds"] = age_seconds
        if age_seconds > max_age_seconds:
            violations.append(f"{key}: upstream packet stale: age_seconds={age_seconds:.3f}")
        if age_seconds < -future_tolerance_seconds:
            violations.append(f"{key}: upstream packet timestamp is too far in the future: age_seconds={age_seconds:.3f}")

    violations.extend(_validate_auth_false(record, key))
    violations.extend(_validate_identity(record, key, require_all=(key == "decision_artifact")))
    violations.extend(_validate_decision_values(record, key))

    if key in {"unified_runtime_supervision", "exact_ticket_governance"}:
        canary_states = _unwrapped_values(record, ("exact_canary_state", "canary_state"))
        canary_state = canary_states[0] if canary_states else None
        canary_observed = _record_has_exact_canary_observed_true(record)
        summary["exact_canary_state"] = canary_state
        summary["exact_canary_observed"] = canary_observed
        if EXPECTED_CANARY_STATE not in canary_states:
            violations.append(f"{key}: exact canary state is not {EXPECTED_CANARY_STATE}")
        if canary_observed is not True:
            violations.append(f"{key}: exact canary observed is not true")

    if key == "decision_artifact":
        decision_status_values = _decision_values(record, "decision_status")
        requested_action_values = _decision_values(record, "requested_action")
        if EXPECTED_DECISION_STATUS not in decision_status_values:
            violations.append(f"{key}: missing required decision_status {EXPECTED_DECISION_STATUS}")
        if EXPECTED_REQUESTED_ACTION not in requested_action_values:
            violations.append(f"{key}: missing required requested_action {EXPECTED_REQUESTED_ACTION}")

    return summary, violations

def build_pre_action_evidence_aggregate_record(
    upstream_records: Mapping[str, Mapping[str, Any] | None],
    *,
    observed_at_utc: str | None = None,
    max_upstream_age_seconds: float = DEFAULT_MAX_UPSTREAM_AGE_SECONDS,
    future_tolerance_seconds: float = DEFAULT_FUTURE_TOLERANCE_SECONDS,
    user_reported_position_open_over_three_bars: bool = False,
) -> dict[str, Any]:
    observed_at_utc = observed_at_utc or utc_now_iso()
    observed_at = parse_utc_timestamp(observed_at_utc) or datetime.now(timezone.utc)
    violations: list[str] = []
    summaries: dict[str, dict[str, Any]] = {}
    copied: dict[str, Any] = {}

    for key in UPSTREAM_PACKET_TYPES:
        copied[key] = copy.deepcopy(upstream_records.get(key)) if key in upstream_records else None
        summary, upstream_violations = _validate_upstream(
            key, copied[key], observed_at, max_upstream_age_seconds, future_tolerance_seconds
        )
        summaries[key] = summary
        violations.extend(upstream_violations)

    verdict = PASS_VERDICT if not violations else FAIL_VERDICT
    authorizations = {key: False for key in AUTHORIZATION_KEYS}
    blocked = {key: True for key in BLOCKED_KEYS}
    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "exact_ticket": EXPECTED_TICKET,
            "exact_identifier": EXPECTED_IDENTIFIER,
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "side": EXPECTED_SIDE,
            "mt5_position_type": EXPECTED_MT5_POSITION_TYPE,
            "volume": EXPECTED_VOLUME,
            "magic": EXPECTED_MAGIC,
            "exact_canary_state": EXPECTED_CANARY_STATE,
            "decision_status": EXPECTED_DECISION_STATUS,
            "requested_action": EXPECTED_REQUESTED_ACTION,
            "max_upstream_age_seconds": max_upstream_age_seconds,
            "future_tolerance_seconds": future_tolerance_seconds,
        },
        "operator_context": {
            "user_reported_position_open_over_three_bars": bool(user_reported_position_open_over_three_bars),
            "bar_age_is_action_authorization": False,
            "bar_age_is_broker_request_authorization": False,
        },
        "upstream_summaries": summaries,
        "upstream_records": copied,
        "checks": {
            "all_upstream_packets_present": all(isinstance(copied[key], Mapping) for key in UPSTREAM_PACKET_TYPES),
            "all_upstream_packets_pass": all(isinstance(copied[key], Mapping) and copied[key].get("verdict") == PASS_VERDICT for key in UPSTREAM_PACKET_TYPES),
            "no_broker_request_constructed": True,
            "read_only_only": True,
        },
        "effective_new_entries_blocked": True,
        **authorizations,
        **blocked,
        "authorizations": authorizations,
        "operator_state": OK_OPERATOR_STATE if verdict == PASS_VERDICT else FAIL_OPERATOR_STATE,
        "operator_next_action": OK_OPERATOR_NEXT_ACTION if verdict == PASS_VERDICT else FAIL_OPERATOR_NEXT_ACTION,
        "violations": violations,
        "verdict": verdict,
    }


def validate_aggregate_record(record: Mapping[str, Any]) -> list[str]:
    if not isinstance(record, Mapping):
        return ["aggregate record is not an object"]
    violations: list[str] = []
    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append(f"wrong schema_version {record.get('schema_version')!r}")
    if record.get("strategy") != STRATEGY:
        violations.append(f"wrong strategy {record.get('strategy')!r}")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append(f"wrong packet_type {record.get('packet_type')!r}")
    violations.extend(_validate_auth_false(record, "aggregate"))
    if record.get("violations") not in (None, []):
        violations.append("aggregate contains embedded violations")
    upstream_records = record.get("upstream_records")
    if not isinstance(upstream_records, Mapping):
        violations.append("missing upstream_records object")
    else:
        observed_at = parse_utc_timestamp(record.get("observed_at_utc")) or datetime.now(timezone.utc)
        expected = record.get("expected") if isinstance(record.get("expected"), Mapping) else {}
        max_age = _as_float(expected.get("max_upstream_age_seconds")) or DEFAULT_MAX_UPSTREAM_AGE_SECONDS
        future_tolerance = _as_float(expected.get("future_tolerance_seconds")) or DEFAULT_FUTURE_TOLERANCE_SECONDS
        for key in UPSTREAM_PACKET_TYPES:
            _summary, upstream_violations = _validate_upstream(key, upstream_records.get(key), observed_at, max_age, future_tolerance)
            violations.extend(upstream_violations)
    if record.get("verdict") == PASS_VERDICT and violations:
        violations.append("aggregate verdict is PASS despite verifier violations")
    if record.get("verdict") not in {PASS_VERDICT, FAIL_VERDICT}:
        violations.append(f"unexpected aggregate verdict {record.get('verdict')!r}")
    return violations


def read_jsonl(path: str | Path) -> tuple[list[dict[str, Any]], list[str]]:
    path = Path(path)
    if not path.exists():
        return [], [f"missing JSONL path: {path}"]
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"malformed JSONL at {path}:{line_number}: {exc}")
            continue
        if not isinstance(parsed, dict):
            errors.append(f"non-object JSONL record at {path}:{line_number}")
            continue
        records.append(parsed)
    if not records and not errors:
        errors.append(f"no JSONL records found at {path}")
    return records, errors


def load_latest_jsonl_record(path: str | Path) -> dict[str, Any]:
    records, errors = read_jsonl(path)
    if errors:
        raise ValueError("; ".join(errors))
    return records[-1]


def write_jsonl_record(path: str | Path, record: Mapping[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def verify_jsonl_records(records: Sequence[Mapping[str, Any]], *, require_pass: bool = False) -> tuple[bool, list[str]]:
    violations: list[str] = []
    if not records:
        violations.append("no aggregate records found")
    for index, record in enumerate(records):
        violations.extend(f"record {index}: {item}" for item in validate_aggregate_record(record))
        if require_pass and record.get("verdict") != PASS_VERDICT:
            violations.append(f"record {index}: --require-pass used but verdict is {record.get('verdict')!r}")
    return not violations, violations


def verify_jsonl_path(path: str | Path, *, require_pass: bool = False) -> tuple[bool, list[str], list[dict[str, Any]]]:
    records, errors = read_jsonl(path)
    if errors:
        return False, errors, records
    ok, violations = verify_jsonl_records(records, require_pass=require_pass)
    return ok, violations, records
