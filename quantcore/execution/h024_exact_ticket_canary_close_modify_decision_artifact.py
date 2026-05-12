"""H024 exact-ticket canary close/modify decision artifact validator.

This module is deliberately read-only. It validates the human/operator decision
artifact schema referenced by the exact-ticket governance packet while keeping
all broker mutation and trading paths blocked.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

SCHEMA_VERSION = 1
STRATEGY = "H024"
PACKET_TYPE = "h024_exact_ticket_canary_close_modify_decision_artifact"
ARTIFACT_TYPE = PACKET_TYPE
DEFAULT_MAX_AGE_SECONDS = 300
DEFAULT_FUTURE_SKEW_SECONDS = 30
PASS_OPERATOR_STATE = (
    "EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_OK_BUT_ACTION_NOT_AUTHORIZED"
)
FAIL_OPERATOR_STATE = "FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_DECISION_ARTIFACT_BLOCKED"
PASS_OPERATOR_NEXT_ACTION = (
    "KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_DECISION_ARTIFACT_REVIEW"
)
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

EXPECTED_CANARY: dict[str, Any] = {
    "server": "Exness-MT5Trial6",
    "account_currency": "USD",
    "runtime_symbol": "XAUUSDm",
    "model_symbol": "XAUUSD",
    "side": "sell",
    "mt5_position_type": 1,
    "volume": 0.01,
    "magic": 240024,
    "ticket": 4413054432,
    "identifier": 4413054432,
    "entry_deal": 3788869526,
}

AUTHORIZATION_FIELDS: tuple[str, ...] = (
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

REQUIRED_ATTESTATION_TRUE_FIELDS: tuple[str, ...] = (
    "attests_exact_ticket_identity_reviewed",
    "attests_read_only_review_only",
    "attests_no_broker_mutation_authorized",
    "attests_no_order_check_authorized",
    "attests_no_order_send_authorized",
    "attests_no_entry_authorized",
    "attests_no_close_modify_authorized",
    "attests_no_xauusd_order_authorized",
    "attests_no_usdjpy_order_authorized",
    "attests_no_trading_loop_authorized",
    "attests_no_automatic_execution_authorized",
)

ALLOWED_REQUESTED_ACTIONS: tuple[str, ...] = (
    "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
    "REQUEST_EXACT_TICKET_CLOSE_REVIEW_ONLY",
    "REQUEST_EXACT_TICKET_MODIFY_REVIEW_ONLY",
    "REQUEST_EXACT_TICKET_CLOSE_MODIFY_REVIEW_ONLY",
)

FORBIDDEN_ARTIFACT_KEYS: tuple[str, ...] = (
    "broker_request",
    "mt5_request",
    "order_request",
    "trade_request",
    "execution_request",
    "close_request",
    "modify_request",
    "sl_tp_request",
    "request_payload",
    "dispatch_payload",
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_utc(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc(value: Any, field_name: str, violations: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        violations.append(f"{field_name} missing or not a non-empty UTC timestamp string")
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        violations.append(f"{field_name} is not ISO-8601 parseable")
        return None
    if parsed.tzinfo is None:
        violations.append(f"{field_name} is timezone-naive")
        return None
    return parsed.astimezone(timezone.utc)


def default_authorizations() -> dict[str, bool]:
    return {field: False for field in AUTHORIZATION_FIELDS}


def _walk_mapping_keys(value: Any, path: str = "$.") -> Iterable[tuple[str, str]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}{key_text}"
            yield key_text, child_path
            yield from _walk_mapping_keys(child, f"{child_path}.")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_mapping_keys(child, f"{path}[{index}].")


def _replace_template_timestamps(value: Any, observed_at_utc: str, expires_at_utc: str) -> Any:
    if isinstance(value, str):
        return value.replace("__OBSERVED_AT_UTC__", observed_at_utc).replace(
            "__EXPIRES_AT_UTC__", expires_at_utc
        )
    if isinstance(value, list):
        return [_replace_template_timestamps(item, observed_at_utc, expires_at_utc) for item in value]
    if isinstance(value, dict):
        return {
            key: _replace_template_timestamps(child, observed_at_utc, expires_at_utc)
            for key, child in value.items()
        }
    return value


def load_decision_artifact_template(path: Path | str) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("decision artifact template must be a JSON object")
    return data


def materialize_decision_artifact_template(
    template: Mapping[str, Any],
    *,
    now: datetime | None = None,
    max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
) -> dict[str, Any]:
    observed = now or utc_now()
    if observed.tzinfo is None:
        observed = observed.replace(tzinfo=timezone.utc)
    observed = observed.astimezone(timezone.utc)
    expires = observed + timedelta(seconds=max_age_seconds)
    return _replace_template_timestamps(deepcopy(dict(template)), format_utc(observed), format_utc(expires))


def build_default_decision_artifact(*, now: datetime | None = None) -> dict[str, Any]:
    observed = now or utc_now()
    artifact = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "artifact_type": ARTIFACT_TYPE,
        "decision_id": "DEFAULT-NON-AUTHORIZING-EXACT-TICKET-CLOSE-MODIFY-DECISION-ARTIFACT",
        "decision_timestamp_utc": format_utc(observed),
        "expires_at_utc": format_utc(observed + timedelta(seconds=DEFAULT_MAX_AGE_SECONDS)),
        "decision_status": "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
        "exact_canary": deepcopy(EXPECTED_CANARY),
        "operator_intent": {
            "requested_action": "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
            "intent_scope": "READ_ONLY_GOVERNANCE_REVIEW_ONLY",
            "intent_is_explicit": True,
            "intent_is_ambiguous": False,
            "immediate_action_requested": False,
            "reason": "Default non-authorizing artifact for schema validation only.",
        },
        "operator_attestation": {
            "operator_id": "DEFAULT_NON_AUTHORIZING_ARTIFACT",
            "attested_at_utc": format_utc(observed),
            "attests_exact_ticket_identity_reviewed": True,
            "attests_read_only_review_only": True,
            "attests_no_broker_mutation_authorized": True,
            "attests_no_order_check_authorized": True,
            "attests_no_order_send_authorized": True,
            "attests_no_entry_authorized": True,
            "attests_no_close_modify_authorized": True,
            "attests_no_xauusd_order_authorized": True,
            "attests_no_usdjpy_order_authorized": True,
            "attests_no_trading_loop_authorized": True,
            "attests_no_automatic_execution_authorized": True,
            "attestation_text": (
                "This artifact is for read-only decision-schema validation only and "
                "authorizes no broker mutation."
            ),
        },
        "effective_new_entries_blocked": True,
        "authorizations": default_authorizations(),
    }
    return artifact


def validate_decision_artifact(
    artifact: Any,
    *,
    now: datetime | None = None,
    max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
    future_skew_seconds: int = DEFAULT_FUTURE_SKEW_SECONDS,
) -> dict[str, Any]:
    observed_at = now or utc_now()
    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(tzinfo=timezone.utc)
    observed_at = observed_at.astimezone(timezone.utc)
    violations: list[str] = []
    checks: dict[str, dict[str, Any]] = {}

    def add_check(name: str, passed: bool, detail: str) -> None:
        checks[name] = {"passed": bool(passed), "detail": detail}
        if not passed:
            violations.append(detail)

    if not isinstance(artifact, Mapping):
        artifact = {}
        add_check("artifact_is_object", False, "decision artifact missing or not a JSON object")
    else:
        add_check("artifact_is_object", True, "decision artifact is a JSON object")

    for key, path in _walk_mapping_keys(artifact):
        if key in FORBIDDEN_ARTIFACT_KEYS:
            add_check(
                f"forbidden_key_absent:{path}",
                False,
                f"forbidden broker/execution request key present at {path}",
            )

    add_check("schema_version", artifact.get("schema_version") == SCHEMA_VERSION, "wrong schema_version")
    add_check("strategy", artifact.get("strategy") == STRATEGY, "wrong strategy")
    add_check("artifact_type", artifact.get("artifact_type") == ARTIFACT_TYPE, "wrong artifact_type")

    decision_id = artifact.get("decision_id")
    add_check(
        "decision_id",
        isinstance(decision_id, str) and bool(decision_id.strip()),
        "decision_id missing or empty",
    )

    timestamp_violations: list[str] = []
    decision_timestamp = parse_utc(
        artifact.get("decision_timestamp_utc"), "decision_timestamp_utc", timestamp_violations
    )
    expires_at = parse_utc(artifact.get("expires_at_utc"), "expires_at_utc", timestamp_violations)
    attested_at = parse_utc(
        artifact.get("operator_attestation", {}).get("attested_at_utc")
        if isinstance(artifact.get("operator_attestation"), Mapping)
        else None,
        "operator_attestation.attested_at_utc",
        timestamp_violations,
    )
    for item in timestamp_violations:
        violations.append(item)
    checks["timestamps_parse"] = {"passed": not timestamp_violations, "detail": "timestamps parse as UTC"}

    freshness_passed = decision_timestamp is not None
    freshness_detail = "decision timestamp is fresh"
    age_seconds: float | None = None
    if decision_timestamp is not None:
        age_seconds = (observed_at - decision_timestamp).total_seconds()
        if age_seconds < -future_skew_seconds:
            freshness_passed = False
            freshness_detail = "decision timestamp is too far in the future"
        elif age_seconds > max_age_seconds:
            freshness_passed = False
            freshness_detail = "decision artifact is stale"
    add_check("decision_freshness", freshness_passed, freshness_detail)

    expiry_passed = expires_at is not None and expires_at >= observed_at
    add_check("decision_not_expired", expiry_passed, "decision artifact is expired or missing expiry")

    attestation_fresh = attested_at is not None
    if attested_at is not None:
        attestation_age = abs((observed_at - attested_at).total_seconds())
        attestation_fresh = attestation_age <= max_age_seconds + future_skew_seconds
    add_check("attestation_freshness", attestation_fresh, "operator attestation timestamp is stale or invalid")

    exact_canary = artifact.get("exact_canary")
    canary_passed = isinstance(exact_canary, Mapping)
    canary_details: dict[str, Any] = {}
    if not canary_passed:
        add_check("exact_canary_object", False, "exact_canary missing or not a JSON object")
        exact_canary = {}
    else:
        add_check("exact_canary_object", True, "exact_canary is a JSON object")
        for field, expected in EXPECTED_CANARY.items():
            observed = exact_canary.get(field)
            if isinstance(expected, float):
                field_passed = isinstance(observed, (int, float)) and abs(float(observed) - expected) <= 1e-12
            else:
                field_passed = observed == expected
            canary_details[field] = {"expected": expected, "observed": observed, "passed": field_passed}
            if not field_passed:
                violations.append(f"exact canary {field} mismatch")
    checks["exact_canary_identity"] = {
        "passed": bool(canary_passed and all(item["passed"] for item in canary_details.values())),
        "detail": "exact ticket/identifier and XAUUSDm canary identity match required values",
        "fields": canary_details,
    }

    operator_intent = artifact.get("operator_intent")
    if not isinstance(operator_intent, Mapping):
        add_check("operator_intent_object", False, "operator_intent missing or not a JSON object")
        operator_intent = {}
    else:
        add_check("operator_intent_object", True, "operator_intent is a JSON object")

    requested_action = operator_intent.get("requested_action")
    add_check(
        "operator_intent_requested_action",
        requested_action in ALLOWED_REQUESTED_ACTIONS,
        "operator intent requested_action missing, unsupported, or ambiguous",
    )
    add_check(
        "operator_intent_scope",
        operator_intent.get("intent_scope") == "READ_ONLY_GOVERNANCE_REVIEW_ONLY",
        "operator intent scope must be read-only governance review only",
    )
    add_check(
        "operator_intent_explicit",
        operator_intent.get("intent_is_explicit") is True,
        "operator intent must be explicitly marked true",
    )
    add_check(
        "operator_intent_not_ambiguous",
        operator_intent.get("intent_is_ambiguous") is False,
        "operator intent is ambiguous",
    )
    add_check(
        "operator_intent_no_immediate_action",
        operator_intent.get("immediate_action_requested") is False,
        "operator intent implies immediate close/modify action",
    )

    operator_attestation = artifact.get("operator_attestation")
    if not isinstance(operator_attestation, Mapping):
        add_check(
            "operator_attestation_object", False, "operator_attestation missing or not a JSON object"
        )
        operator_attestation = {}
    else:
        add_check("operator_attestation_object", True, "operator_attestation is a JSON object")
    for field in REQUIRED_ATTESTATION_TRUE_FIELDS:
        add_check(
            f"operator_attestation_{field}",
            operator_attestation.get(field) is True,
            f"operator attestation {field} missing or not true",
        )

    authorizations = artifact.get("authorizations")
    if not isinstance(authorizations, Mapping):
        add_check("authorizations_object", False, "authorizations missing or not a JSON object")
        authorizations = {}
    else:
        add_check("authorizations_object", True, "authorizations is a JSON object")
    for field in AUTHORIZATION_FIELDS:
        add_check(
            f"authorization_{field}_false",
            authorizations.get(field) is False,
            f"unsafe or missing authorization field: {field}",
        )
    add_check(
        "effective_new_entries_blocked",
        artifact.get("effective_new_entries_blocked") is True,
        "effective_new_entries_blocked must be true",
    )

    verdict = "PASS" if not violations else "FAIL_CLOSED"
    operator_state = PASS_OPERATOR_STATE if verdict == "PASS" else FAIL_OPERATOR_STATE
    operator_next_action = PASS_OPERATOR_NEXT_ACTION if verdict == "PASS" else FAIL_OPERATOR_NEXT_ACTION

    record = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": format_utc(observed_at),
        "expected": {
            "exact_canary": deepcopy(EXPECTED_CANARY),
            "max_age_seconds": max_age_seconds,
            "future_skew_seconds": future_skew_seconds,
            "allowed_requested_actions": list(ALLOWED_REQUESTED_ACTIONS),
        },
        "observed": {
            "decision_id": artifact.get("decision_id"),
            "decision_status": artifact.get("decision_status"),
            "requested_action": requested_action if isinstance(operator_intent, Mapping) else None,
            "intent_scope": operator_intent.get("intent_scope") if isinstance(operator_intent, Mapping) else None,
            "decision_timestamp_utc": artifact.get("decision_timestamp_utc"),
            "expires_at_utc": artifact.get("expires_at_utc"),
            "age_seconds": age_seconds,
            "exact_canary": deepcopy(dict(exact_canary)) if isinstance(exact_canary, Mapping) else None,
        },
        "checks": checks,
        "effective_new_entries_blocked": True,
        "authorizations": default_authorizations(),
        "operator_state": operator_state,
        "operator_next_action": operator_next_action,
        "violations": violations,
        "verdict": verdict,
    }
    return record


def write_jsonl_record(record: Mapping[str, Any], path: Path | str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")


def read_jsonl_records(path: Path | str) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    violations: list[str] = []
    input_path = Path(path)
    if not input_path.exists():
        return [], [f"JSONL file does not exist: {input_path}"]
    with input_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError as exc:
                violations.append(f"line {line_number} is malformed JSON: {exc}")
                continue
            if not isinstance(parsed, dict):
                violations.append(f"line {line_number} is not a JSON object")
                continue
            records.append(parsed)
    if not records and not violations:
        violations.append("JSONL file has no records")
    return records, violations


def verify_record(record: Mapping[str, Any], *, require_pass: bool = False) -> list[str]:
    violations: list[str] = []
    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append("record schema_version mismatch")
    if record.get("strategy") != STRATEGY:
        violations.append("record strategy mismatch")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append("record packet_type mismatch")
    embedded_violations = record.get("violations")
    if not isinstance(embedded_violations, list):
        violations.append("record violations field missing or malformed")
        embedded_violations = []
    verdict = record.get("verdict")
    if verdict not in {"PASS", "FAIL_CLOSED"}:
        violations.append("record verdict must be PASS or FAIL_CLOSED")
    if verdict == "PASS" and embedded_violations:
        violations.append("PASS record contains embedded violations")
    if require_pass and verdict != "PASS":
        violations.append("--require-pass specified but record verdict is not PASS")
    if record.get("effective_new_entries_blocked") is not True:
        violations.append("effective_new_entries_blocked must be true")
    authorizations = record.get("authorizations")
    if not isinstance(authorizations, Mapping):
        violations.append("authorizations field missing or malformed")
        authorizations = {}
    for field in AUTHORIZATION_FIELDS:
        if authorizations.get(field) is not False:
            violations.append(f"unsafe or missing authorization field: {field}")
    if verdict == "PASS":
        if record.get("operator_state") != PASS_OPERATOR_STATE:
            violations.append("PASS record has unexpected operator_state")
        if record.get("operator_next_action") != PASS_OPERATOR_NEXT_ACTION:
            violations.append("PASS record has unexpected operator_next_action")
    return violations


def verify_jsonl(path: Path | str, *, require_pass: bool = False) -> dict[str, Any]:
    records, violations = read_jsonl_records(path)
    record_violations: list[str] = []
    embedded_count = 0
    for index, record in enumerate(records, start=1):
        embedded = record.get("violations")
        if isinstance(embedded, list):
            embedded_count += len(embedded)
        for violation in verify_record(record, require_pass=require_pass):
            record_violations.append(f"record {index}: {violation}")
    all_violations = violations + record_violations
    return {
        "record_count": len(records),
        "violations": all_violations,
        "embedded_violations": embedded_count,
        "verifier_verdict": "PASS" if not all_violations else "FAIL",
        "records": records,
    }
