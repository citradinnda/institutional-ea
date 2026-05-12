"""H024 exact-ticket canary close/modify governance specification.

This module is intentionally read-only. It defines and validates the
governance prerequisites that must exist before any future close/modify could
even be considered for the exact known H024 XAUUSDm canary. A PASS from this
packet never authorizes broker mutation, order_check, order_send, entry,
close/modify, XAUUSD order, USDJPY order, a trading loop, or automatic
execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

SCHEMA_VERSION = "1.0"
STRATEGY = "H024"
PACKET_TYPE = "h024_exact_ticket_canary_close_modify_governance"
DECISION_ARTIFACT_TYPE = (
    "h024_exact_ticket_canary_close_modify_governance_human_decision"
)
NO_MUTATION_GATE_PACKET_TYPE = "h024_runtime_no_mutation_safety_gate"
UNIFIED_PACKET_TYPE = "h024_unified_read_only_post_canary_runtime_supervision"

PASS_OPERATOR_STATE = (
    "EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_SPEC_OK_BUT_ACTION_NOT_AUTHORIZED"
)
FAIL_OPERATOR_STATE = "FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_GOVERNANCE_BLOCKED"
PASS_OPERATOR_NEXT_ACTION = (
    "KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_GOVERNANCE_REVIEW"
)
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_RUNTIME_SYMBOL = "XAUUSDm"
EXPECTED_MODEL_SYMBOL = "XAUUSD"
EXPECTED_SIDE = "sell"
EXPECTED_POSITION_TYPE = 1
EXPECTED_VOLUME = 0.01
EXPECTED_MAGIC = 240024
EXPECTED_CANARY_STATE = "OBSERVED_EXACT_KNOWN_CANARY"

ALLOWED_SPEC_ONLY_DECISIONS = {
    "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY",
    "READ_ONLY_GOVERNANCE_SPECIFICATION_ONLY_NO_ACTION_AUTHORIZED",
}

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
)

BLOCKED_KEYS = (
    "automatic_execution_blocked",
    "broker_mutation_blocked",
    "close_modify_blocked",
    "entry_blocked",
    "order_check_blocked",
    "order_send_blocked",
    "trading_loop_blocked",
    "usdjpy_order_blocked",
    "xauusd_order_blocked",
)


@dataclass(frozen=True)
class VerificationResult:
    """Result returned by governance packet verification."""

    verifier_verdict: str
    record_count: int
    violations: tuple[str, ...]
    embedded_violations: int
    record_verdict: str | None
    operator_state: str | None
    operator_next_action: str | None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _format_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _parse_utc(value: Any) -> datetime | None:
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


def _json_safe(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _iter_dicts(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_dicts(child)


def _recursive_values_for_key(value: Any, key: str) -> list[Any]:
    found: list[Any] = []
    for item in _iter_dicts(value):
        if key in item:
            found.append(item[key])
    return found


def _first_value_for_key(value: Any, key: str, default: Any = None) -> Any:
    values = _recursive_values_for_key(value, key)
    return values[0] if values else default


def _find_packet(value: Any, packet_type: str) -> Mapping[str, Any] | None:
    for item in _iter_dicts(value):
        if item.get("packet_type") == packet_type:
            return item
    return None


def _bool_is_false(value: Any) -> bool:
    return value is False


def _bool_is_true(value: Any) -> bool:
    return value is True


def _number_equal(left: Any, right: float, *, tolerance: float = 1e-9) -> bool:
    try:
        return abs(float(left) - float(right)) <= tolerance
    except (TypeError, ValueError):
        return False


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _nested_authorization(value: Mapping[str, Any], key: str) -> Any:
    if key in value:
        return value[key]
    nested = value.get("authorizations")
    if isinstance(nested, Mapping) and key in nested:
        return nested[key]
    return None


def _all_authorizations_false(value: Mapping[str, Any]) -> bool:
    return all(_bool_is_false(_nested_authorization(value, key)) for key in AUTHORIZATION_KEYS)


def _authorizations() -> dict[str, bool]:
    return {key: False for key in AUTHORIZATION_KEYS}


def _blocked_flags() -> dict[str, bool]:
    return {key: True for key in BLOCKED_KEYS}


def _has_positive_usdjpy_exposure_or_order(value: Any) -> bool:
    for item in _iter_dicts(value):
        for key, raw in item.items():
            lower = str(key).lower()
            if "usdjpy" not in lower:
                continue
            if not any(
                token in lower
                for token in ("position", "positions", "exposure", "order", "orders", "count")
            ):
                continue
            if isinstance(raw, bool):
                if raw:
                    return True
                continue
            parsed = _int_or_none(raw)
            if parsed is not None and parsed > 0:
                return True
    return False


def _contains_any_key_fragment(value: Any, fragments: tuple[str, ...]) -> bool:
    fragments_lower = tuple(fragment.lower() for fragment in fragments)
    for item in _iter_dicts(value):
        for key in item.keys():
            lower = str(key).lower()
            if any(fragment in lower for fragment in fragments_lower):
                return True
    return False


def _has_snapshot_bundle(value: Any) -> tuple[bool, bool, bool]:
    account = _find_packet(value, "h024_runtime_account_risk_margin_safety_supervisor")
    exposure = _find_packet(value, "h024_runtime_exposure_inventory_safety_supervisor")
    tick = _find_packet(value, "h024_runtime_tick_spread_safety_supervisor")

    has_account = account is not None or _contains_any_key_fragment(
        value, ("account_risk_margin", "margin_level", "margin_used_fraction", "free_margin")
    )
    has_exposure = exposure is not None or _contains_any_key_fragment(
        value, ("exposure_inventory", "h024_position_count", "exact_canary_state")
    )
    has_tick = tick is not None or _contains_any_key_fragment(
        value, ("tick_spread", "spread_points", "tick_age_seconds", "bid", "ask")
    )
    return has_account, has_exposure, has_tick


def _fresh_observed_at(
    value: Mapping[str, Any] | None,
    *,
    now: datetime,
    max_age_seconds: int,
) -> bool:
    if value is None:
        return False
    observed_at = _parse_utc(value.get("observed_at_utc"))
    if observed_at is None:
        return False
    age = (now - observed_at).total_seconds()
    return age >= -5 and age <= max_age_seconds


def _decision_not_expired(decision: Mapping[str, Any], *, now: datetime) -> bool:
    valid_until = _parse_utc(decision.get("valid_until_utc"))
    if valid_until is None:
        return False
    return valid_until >= now


def _check(
    checks: list[dict[str, Any]],
    name: str,
    passed: bool,
    *,
    fail_reason: str,
    detail: Mapping[str, Any] | None = None,
) -> None:
    record: dict[str, Any] = {"name": name, "status": "PASS" if passed else "FAIL"}
    if detail:
        record["detail"] = dict(detail)
    if not passed:
        record["fail_reason"] = fail_reason
    checks.append(record)


def _violations_from_checks(checks: Iterable[Mapping[str, Any]]) -> list[str]:
    violations: list[str] = []
    for item in checks:
        if item.get("status") != "PASS":
            name = item.get("name", "unknown_check")
            reason = item.get("fail_reason", "check failed")
            violations.append(f"{name}: {reason}")
    return violations


def _embedded_violations(value: Any) -> list[Any]:
    violations: list[Any] = []
    for item in _iter_dicts(value):
        raw = item.get("violations")
        if isinstance(raw, list) and raw:
            violations.extend(raw)
    return violations


def _canonical_expected() -> dict[str, Any]:
    return {
        "exact_ticket_lock": {
            "ticket": EXPECTED_TICKET,
            "identifier": EXPECTED_IDENTIFIER,
        },
        "exact_canary_identity": {
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "side": EXPECTED_SIDE,
            "position_type": EXPECTED_POSITION_TYPE,
            "volume": EXPECTED_VOLUME,
            "magic": EXPECTED_MAGIC,
        },
        "required_upstream": {
            "runtime_no_mutation_safety_gate": "PASS_AND_MUTATION_PATH_CLOSED",
            "unified_post_canary_runtime_supervision": "PASS",
            "runtime_tick_spread_safety_supervisor": "PRESENT_AND_FRESH",
            "runtime_exposure_inventory_safety_supervisor": "PRESENT_AND_FRESH",
            "runtime_account_risk_margin_safety_supervisor": "PRESENT_AND_FRESH",
        },
        "required_governance_artifacts": {
            "explicit_human_decision_artifact": (
                "SPECIFICATION_ONLY_NO_CLOSE_MODIFY_AUTHORIZED"
            ),
            "pre_close_risk_snapshot_bundle": (
                "ACCOUNT_RISK_MARGIN_EXPOSURE_INVENTORY_TICK_SPREAD"
            ),
        },
        "no_current_authorization": {
            **_authorizations(),
            "effective_new_entries_blocked": True,
        },
    }


def load_latest_jsonl_record(path: str | Path) -> Mapping[str, Any] | None:
    """Return the last non-empty JSONL record from *path*, or None."""

    candidate = Path(path)
    if not candidate.exists():
        return None
    latest: Mapping[str, Any] | None = None
    with candidate.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            loaded = json.loads(line)
            if not isinstance(loaded, Mapping):
                raise ValueError(f"JSONL record in {candidate} is not an object")
            latest = loaded
    return latest


def load_json_object(path: str | Path) -> Mapping[str, Any] | None:
    """Return a JSON object from *path*, or None when the path is absent."""

    candidate = Path(path)
    if not candidate.exists():
        return None
    loaded = json.loads(candidate.read_text(encoding="utf-8"))
    if not isinstance(loaded, Mapping):
        raise ValueError(f"JSON document in {candidate} is not an object")
    return loaded


def build_governance_packet(
    *,
    no_mutation_gate_record: Mapping[str, Any] | None,
    human_decision_record: Mapping[str, Any] | None,
    observed_at_utc: str | None = None,
    max_gate_age_seconds: int = 3600,
    max_snapshot_age_seconds: int = 3600,
) -> dict[str, Any]:
    """Build a read-only exact-ticket close/modify governance packet.

    The resulting packet is a specification/governance artifact only. It never
    opens a broker mutation path.
    """

    now = _parse_utc(observed_at_utc) if observed_at_utc else _utc_now()
    if now is None:
        now = _utc_now()
    observed_at = _format_utc(now)

    checks: list[dict[str, Any]] = []
    gate = no_mutation_gate_record if isinstance(no_mutation_gate_record, Mapping) else None
    decision = human_decision_record if isinstance(human_decision_record, Mapping) else None

    _check(
        checks,
        "runtime_no_mutation_gate_record_present",
        gate is not None,
        fail_reason="runtime no-mutation safety gate is missing or malformed",
    )
    if gate is not None:
        _check(
            checks,
            "runtime_no_mutation_gate_identity",
            gate.get("strategy") == STRATEGY
            and gate.get("packet_type") == NO_MUTATION_GATE_PACKET_TYPE,
            fail_reason="runtime no-mutation safety gate has wrong strategy or packet type",
            detail={
                "strategy": gate.get("strategy"),
                "packet_type": gate.get("packet_type"),
            },
        )
        _check(
            checks,
            "runtime_no_mutation_gate_pass",
            gate.get("verdict") == "PASS",
            fail_reason="runtime no-mutation safety gate is not PASS",
            detail={"verdict": gate.get("verdict")},
        )
        _check(
            checks,
            "runtime_no_mutation_gate_trusted",
            gate.get("trusted", True) is not False,
            fail_reason="runtime no-mutation safety gate is explicitly untrusted",
            detail={"trusted": gate.get("trusted", True)},
        )
        _check(
            checks,
            "runtime_no_mutation_gate_fresh",
            _fresh_observed_at(gate, now=now, max_age_seconds=max_gate_age_seconds),
            fail_reason="runtime no-mutation safety gate is missing observed_at_utc or stale",
            detail={
                "observed_at_utc": gate.get("observed_at_utc"),
                "max_gate_age_seconds": max_gate_age_seconds,
            },
        )
        _check(
            checks,
            "runtime_no_mutation_gate_keeps_mutation_path_closed",
            gate.get("gate_opens_mutation_path") is False,
            fail_reason="runtime no-mutation safety gate opens a mutation path",
            detail={"gate_opens_mutation_path": gate.get("gate_opens_mutation_path")},
        )
        _check(
            checks,
            "runtime_no_mutation_gate_requires_future_checks",
            gate.get("future_broker_facing_code_must_check_gate") is True,
            fail_reason="future broker-facing code is not required to check the gate",
            detail={
                "future_broker_facing_code_must_check_gate": gate.get(
                    "future_broker_facing_code_must_check_gate"
                )
            },
        )
        _check(
            checks,
            "runtime_no_mutation_gate_authorizations_false",
            _all_authorizations_false(gate)
            and gate.get("effective_new_entries_blocked") is True,
            fail_reason="runtime no-mutation safety gate has unsafe authorization flags",
        )

        unified = _find_packet(gate, UNIFIED_PACKET_TYPE)
        unified_verdict = (
            unified.get("verdict") if unified is not None else gate.get("unified_supervision_verdict")
        )
        _check(
            checks,
            "unified_post_canary_runtime_supervision_present",
            unified is not None or gate.get("unified_supervision_verdict") is not None,
            fail_reason="unified post-canary runtime supervision is missing",
        )
        _check(
            checks,
            "unified_post_canary_runtime_supervision_pass",
            unified_verdict == "PASS",
            fail_reason="unified post-canary runtime supervision is not PASS",
            detail={"unified_supervision_verdict": unified_verdict},
        )

        exact_state = _first_value_for_key(gate, "exact_canary_state", gate.get("exact_canary_state"))
        exact_observed = _first_value_for_key(
            gate, "exact_canary_observed", gate.get("exact_canary_observed")
        )
        h024_position_count = _first_value_for_key(
            gate, "h024_position_count", gate.get("h024_position_count")
        )
        h024_order_count = _first_value_for_key(gate, "h024_order_count", gate.get("h024_order_count"))

        exact_known_canary = exact_state == EXPECTED_CANARY_STATE and exact_observed is True
        ticket_values = set(_recursive_values_for_key(gate, "ticket")) | set(
            _recursive_values_for_key(gate, "identifier")
        )
        ticket_lock_ok = EXPECTED_TICKET in ticket_values or exact_known_canary

        _check(
            checks,
            "exact_ticket_or_identifier_lock",
            ticket_lock_ok,
            fail_reason="exact canary ticket/identifier lock is not observed",
            detail={
                "expected_ticket": EXPECTED_TICKET,
                "expected_identifier": EXPECTED_IDENTIFIER,
                "observed_ticket_or_identifier_values": sorted(
                    str(value) for value in ticket_values
                )[:10],
            },
        )
        _check(
            checks,
            "exact_known_canary_identity_match",
            exact_known_canary,
            fail_reason="exact known XAUUSDm canary identity is not observed",
            detail={
                "exact_canary_state": exact_state,
                "exact_canary_observed": exact_observed,
            },
        )
        _check(
            checks,
            "no_usdjpy_h024_exposure_or_order",
            not _has_positive_usdjpy_exposure_or_order(gate),
            fail_reason="USDJPY H024 exposure/order is present",
        )
        _check(
            checks,
            "no_additional_h024_exposure_or_order",
            _int_or_none(h024_position_count) == 1 and _int_or_none(h024_order_count) == 0,
            fail_reason="additional H024 exposure/order is present or inventory count is ambiguous",
            detail={
                "h024_position_count": h024_position_count,
                "h024_order_count": h024_order_count,
            },
        )

        has_account_snapshot, has_exposure_snapshot, has_tick_snapshot = _has_snapshot_bundle(gate)
        _check(
            checks,
            "pre_close_account_risk_margin_snapshot_present",
            has_account_snapshot,
            fail_reason="account risk/margin snapshot is missing",
        )
        _check(
            checks,
            "pre_close_exposure_inventory_snapshot_present",
            has_exposure_snapshot,
            fail_reason="exposure/inventory snapshot is missing",
        )
        _check(
            checks,
            "pre_close_tick_spread_snapshot_present",
            has_tick_snapshot,
            fail_reason="tick/spread snapshot is missing",
        )
        snapshot_packets = [
            _find_packet(gate, "h024_runtime_account_risk_margin_safety_supervisor"),
            _find_packet(gate, "h024_runtime_exposure_inventory_safety_supervisor"),
            _find_packet(gate, "h024_runtime_tick_spread_safety_supervisor"),
        ]
        available_snapshot_packets = [packet for packet in snapshot_packets if packet is not None]
        if available_snapshot_packets:
            snapshots_fresh = all(
                _fresh_observed_at(
                    packet, now=now, max_age_seconds=max_snapshot_age_seconds
                )
                for packet in available_snapshot_packets
            )
        else:
            snapshots_fresh = _fresh_observed_at(
                gate, now=now, max_age_seconds=max_snapshot_age_seconds
            )
        _check(
            checks,
            "pre_close_risk_snapshot_fresh",
            snapshots_fresh,
            fail_reason="pre-close risk snapshot bundle is missing observed_at_utc or stale",
            detail={"max_snapshot_age_seconds": max_snapshot_age_seconds},
        )

        embedded_violations = _embedded_violations(gate)
        _check(
            checks,
            "upstream_embedded_violations_absent",
            len(embedded_violations) == 0,
            fail_reason="upstream packet contains embedded violations",
            detail={"embedded_violation_count": len(embedded_violations)},
        )

    _check(
        checks,
        "explicit_human_decision_artifact_present",
        decision is not None,
        fail_reason="explicit human decision artifact is missing or malformed",
    )
    if decision is not None:
        _check(
            checks,
            "explicit_human_decision_artifact_identity",
            decision.get("schema_version") == SCHEMA_VERSION
            and decision.get("strategy") == STRATEGY
            and decision.get("artifact_type") == DECISION_ARTIFACT_TYPE,
            fail_reason="explicit human decision artifact has wrong schema, strategy, or type",
            detail={
                "schema_version": decision.get("schema_version"),
                "strategy": decision.get("strategy"),
                "artifact_type": decision.get("artifact_type"),
            },
        )
        _check(
            checks,
            "explicit_human_decision_is_spec_only_and_unambiguous",
            decision.get("decision_is_explicit") is True
            and decision.get("decision") in ALLOWED_SPEC_ONLY_DECISIONS
            and decision.get("close_modify_requested") is False,
            fail_reason="human decision artifact is stale, ambiguous, or requests action",
            detail={
                "decision": decision.get("decision"),
                "decision_is_explicit": decision.get("decision_is_explicit"),
                "close_modify_requested": decision.get("close_modify_requested"),
            },
        )
        target = decision.get("target")
        target = target if isinstance(target, Mapping) else {}
        _check(
            checks,
            "explicit_human_decision_targets_exact_ticket",
            target.get("ticket") == EXPECTED_TICKET
            and target.get("identifier") == EXPECTED_IDENTIFIER
            and target.get("runtime_symbol") == EXPECTED_RUNTIME_SYMBOL
            and target.get("model_symbol") == EXPECTED_MODEL_SYMBOL
            and target.get("magic") == EXPECTED_MAGIC
            and _number_equal(target.get("volume"), EXPECTED_VOLUME)
            and target.get("position_type") == EXPECTED_POSITION_TYPE
            and target.get("side") == EXPECTED_SIDE,
            fail_reason="human decision artifact does not target the exact known canary identity",
            detail={"target": dict(target)},
        )
        _check(
            checks,
            "explicit_human_decision_not_stale",
            _decision_not_expired(decision, now=now),
            fail_reason="human decision artifact is missing valid_until_utc or is stale",
            detail={"valid_until_utc": decision.get("valid_until_utc")},
        )
        _check(
            checks,
            "explicit_human_decision_authorizations_false",
            _all_authorizations_false(decision)
            and decision.get("effective_new_entries_blocked") is True,
            fail_reason="human decision artifact has unsafe authorization flags",
        )

    record_authorizations = _authorizations()
    record_blocked_flags = _blocked_flags()

    _check(
        checks,
        "governance_packet_authorizations_false",
        all(value is False for value in record_authorizations.values()),
        fail_reason="governance packet authorization flags are unsafe",
    )

    violations = _violations_from_checks(checks)
    verdict = "PASS" if not violations else "FAIL"

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at,
        "expected": _canonical_expected(),
        "governance_scope": {
            "scope": "READ_ONLY_EXACT_TICKET_CLOSE_MODIFY_GOVERNANCE_SPECIFICATION",
            "pass_semantics": "COHERENT_GOVERNANCE_SPEC_ONLY_NO_ACTION_AUTHORIZED",
            "close_modify_consideration_only_for_ticket": EXPECTED_TICKET,
            "broker_request_built": False,
            "mt5_state_mutated": False,
            "trading_loop_started": False,
        },
        "required_artifacts": {
            "runtime_no_mutation_gate_packet": NO_MUTATION_GATE_PACKET_TYPE,
            "explicit_human_decision_artifact": DECISION_ARTIFACT_TYPE,
            "pre_close_risk_snapshot_bundle": [
                "h024_runtime_account_risk_margin_safety_supervisor",
                "h024_runtime_exposure_inventory_safety_supervisor",
                "h024_runtime_tick_spread_safety_supervisor",
            ],
        },
        "observed": {
            "runtime_no_mutation_gate_present": gate is not None,
            "human_decision_artifact_present": decision is not None,
            "gate_observed_at_utc": gate.get("observed_at_utc") if gate else None,
            "gate_verdict": gate.get("verdict") if gate else None,
            "gate_opens_mutation_path": gate.get("gate_opens_mutation_path") if gate else None,
            "unified_supervision_verdict": (
                gate.get("unified_supervision_verdict") if gate else None
            ),
            "exact_canary_state": _first_value_for_key(gate, "exact_canary_state")
            if gate
            else None,
            "exact_canary_observed": _first_value_for_key(gate, "exact_canary_observed")
            if gate
            else None,
            "h024_position_count": _first_value_for_key(gate, "h024_position_count")
            if gate
            else None,
            "h024_order_count": _first_value_for_key(gate, "h024_order_count")
            if gate
            else None,
            "human_decision": decision.get("decision") if decision else None,
            "human_decision_valid_until_utc": decision.get("valid_until_utc")
            if decision
            else None,
        },
        "checks": checks,
        "authorizations": record_authorizations,
        "effective_new_entries_blocked": True,
        **record_authorizations,
        **record_blocked_flags,
        "operator_state": PASS_OPERATOR_STATE if verdict == "PASS" else FAIL_OPERATOR_STATE,
        "operator_next_action": (
            PASS_OPERATOR_NEXT_ACTION if verdict == "PASS" else FAIL_OPERATOR_NEXT_ACTION
        ),
        "violations": violations,
        "verdict": verdict,
    }


def validate_governance_record(record: Mapping[str, Any], *, require_pass: bool = False) -> list[str]:
    """Return verifier violations for one governance packet record."""

    violations: list[str] = []
    if not isinstance(record, Mapping):
        return ["record is not a JSON object"]

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append("wrong schema_version")
    if record.get("strategy") != STRATEGY:
        violations.append("wrong strategy")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append("wrong packet_type")
    if _parse_utc(record.get("observed_at_utc")) is None:
        violations.append("missing or malformed observed_at_utc")
    if "expected" not in record or not isinstance(record.get("expected"), Mapping):
        violations.append("missing expected block")
    if "checks" not in record or not isinstance(record.get("checks"), list):
        violations.append("missing checks block")

    for key in AUTHORIZATION_KEYS:
        if key not in record:
            violations.append(f"missing top-level authorization flag {key}")
        elif record.get(key) is not False:
            violations.append(f"unsafe top-level authorization flag {key}")
    nested_auth = record.get("authorizations")
    if not isinstance(nested_auth, Mapping):
        violations.append("missing nested authorizations block")
    else:
        for key in AUTHORIZATION_KEYS:
            if key not in nested_auth:
                violations.append(f"missing nested authorization flag {key}")
            elif nested_auth.get(key) is not False:
                violations.append(f"unsafe nested authorization flag {key}")

    if record.get("effective_new_entries_blocked") is not True:
        violations.append("effective_new_entries_blocked is not true")

    for key in BLOCKED_KEYS:
        if record.get(key) is not True:
            violations.append(f"{key} is not true")

    embedded_violations = record.get("violations")
    if not isinstance(embedded_violations, list):
        violations.append("violations is not a list")
    elif embedded_violations:
        violations.append("record contains violations")

    checks = record.get("checks")
    if isinstance(checks, list):
        failing_checks = [
            check.get("name", "unknown_check")
            for check in checks
            if not isinstance(check, Mapping) or check.get("status") != "PASS"
        ]
        if failing_checks:
            violations.append("one or more checks failed: " + ", ".join(failing_checks))

    if record.get("verdict") == "PASS" and violations:
        violations.append("record verdict PASS is inconsistent with verifier violations")
    if require_pass and record.get("verdict") != "PASS":
        violations.append("require-pass set but record verdict is not PASS")
    if record.get("verdict") not in {"PASS", "FAIL"}:
        violations.append("record verdict must be PASS or FAIL")

    return violations


def verify_jsonl_file(path: str | Path, *, require_pass: bool = False) -> VerificationResult:
    """Verify a governance JSONL file."""

    candidate = Path(path)
    if not candidate.exists():
        return VerificationResult(
            verifier_verdict="FAIL",
            record_count=0,
            violations=(f"missing JSONL file: {candidate}",),
            embedded_violations=0,
            record_verdict=None,
            operator_state=None,
            operator_next_action=None,
        )

    records: list[Mapping[str, Any]] = []
    malformed: list[str] = []
    with candidate.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                loaded = json.loads(line)
            except json.JSONDecodeError as exc:
                malformed.append(f"line {line_number}: malformed JSON: {exc}")
                continue
            if not isinstance(loaded, Mapping):
                malformed.append(f"line {line_number}: record is not a JSON object")
                continue
            records.append(loaded)

    if malformed:
        return VerificationResult(
            verifier_verdict="FAIL",
            record_count=len(records),
            violations=tuple(malformed),
            embedded_violations=0,
            record_verdict=records[-1].get("verdict") if records else None,
            operator_state=records[-1].get("operator_state") if records else None,
            operator_next_action=records[-1].get("operator_next_action") if records else None,
        )

    if not records:
        return VerificationResult(
            verifier_verdict="FAIL",
            record_count=0,
            violations=("no JSONL records found",),
            embedded_violations=0,
            record_verdict=None,
            operator_state=None,
            operator_next_action=None,
        )

    latest = records[-1]
    violations = validate_governance_record(latest, require_pass=require_pass)
    embedded = latest.get("violations")
    embedded_count = len(embedded) if isinstance(embedded, list) else 0
    return VerificationResult(
        verifier_verdict="PASS" if not violations else "FAIL",
        record_count=len(records),
        violations=tuple(violations),
        embedded_violations=embedded_count,
        record_verdict=latest.get("verdict"),
        operator_state=latest.get("operator_state"),
        operator_next_action=latest.get("operator_next_action"),
    )


def write_jsonl_record(path: str | Path, record: Mapping[str, Any]) -> None:
    """Write a single JSONL record to *path*."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")
