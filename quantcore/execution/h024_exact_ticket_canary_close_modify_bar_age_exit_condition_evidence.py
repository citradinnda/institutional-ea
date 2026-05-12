"""H024 exact-ticket canary close/modify bar-age and exit-condition evidence.

This module is intentionally read-only. It consumes already-generated JSONL
supervision/governance/decision/evidence packets and emits a fail-closed
operator evidence packet. A PASS means evidence coherence only; it never
authorizes broker mutation, order checks, order sends, entries, close/modify,
XAUUSD orders, USDJPY orders, trading loops, or automatic execution.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, MutableMapping, Sequence


SCHEMA_VERSION = "1.0.0"
STRATEGY = "H024"
PACKET_TYPE = "h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence"

EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_RUNTIME_SYMBOL = "XAUUSDm"
EXPECTED_MODEL_SYMBOL = "XAUUSD"
EXPECTED_SIDE = "sell"
EXPECTED_MT5_POSITION_TYPE = 1
EXPECTED_VOLUME = 0.01
EXPECTED_MAGIC = 240024
EXPECTED_CANARY_STATE = "OBSERVED_EXACT_KNOWN_CANARY"

NO_CLOSE_MODIFY_DECISION = "NO_CLOSE_MODIFY_REQUESTED_SPECIFICATION_ONLY"

PASS_OPERATOR_STATE = (
    "EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_EVIDENCE_OK_"
    "BUT_ACTION_NOT_AUTHORIZED"
)
PASS_OPERATOR_NEXT_ACTION = (
    "KEEP_EXACT_TICKET_CLOSE_MODIFY_BLOCKED_CONTINUE_READ_ONLY_BAR_AGE_"
    "EXIT_CONDITION_EVIDENCE_REVIEW"
)
FAIL_OPERATOR_STATE = (
    "FAIL_CLOSED_EXACT_TICKET_CANARY_CLOSE_MODIFY_BAR_AGE_EXIT_CONDITION_"
    "EVIDENCE_BLOCKED"
)
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

DEFAULT_MAX_UPSTREAM_AGE_SECONDS = 300.0
DEFAULT_MAX_FUTURE_SKEW_SECONDS = 60.0

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

REQUIRED_UPSTREAM_REPORTS = {
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


@dataclass(frozen=True)
class LoadedJsonl:
    path: Path
    records: tuple[dict[str, Any], ...]


class PacketError(ValueError):
    """Raised for malformed packet inputs."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc(value: Any) -> datetime | None:
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


def normalized_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def iter_paths(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, Mapping):
        for key, item in value.items():
            yield from iter_paths(item, path + (str(key),))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_paths(item, path + (str(index),))


def values_for_keys(value: Any, candidate_keys: Iterable[str]) -> list[tuple[tuple[str, ...], Any]]:
    wanted = {normalized_key(key) for key in candidate_keys}
    found: list[tuple[tuple[str, ...], Any]] = []
    for path, item in iter_paths(value):
        if not path:
            continue
        if normalized_key(path[-1]) in wanted:
            found.append((path, item))
    return found


def unwrap_observed_value(value: Any) -> Any:
    """Return observed/actual scalar values from nested H024 check-wrapper shapes."""

    current = value
    for _ in range(12):
        if not isinstance(current, Mapping):
            return current

        by_normalized_key = {normalized_key(str(key)): item for key, item in current.items()}
        advanced = False
        for candidate in (
            "observed",
            "observed_value",
            "actual",
            "actual_value",
            "value",
            "observedValue",
            "actualValue",
        ):
            normalized = normalized_key(candidate)
            if normalized in by_normalized_key and by_normalized_key[normalized] is not None:
                next_value = by_normalized_key[normalized]
                if next_value is current:
                    return current
                current = next_value
                advanced = True
                break

        if not advanced:
            return current

    return current


def bool_check_value(value: Any) -> bool | None:
    """Coerce direct bools or H024 check-wrapper bools.

    Authorization fields in older packets may appear as either direct booleans
    or check wrappers. This function evaluates the observed value first. If a
    wrapper has no scalar observed value but explicitly passed against a boolean
    expected value, it falls back to that expected value for compatibility with
    already-validated upstream PASS packets.
    """

    observed_value = unwrap_observed_value(value)
    parsed = bool_value(observed_value)
    if parsed is not None:
        return parsed

    if isinstance(value, Mapping):
        by_normalized_key = {normalized_key(str(key)): item for key, item in value.items()}
        passed = bool_value(by_normalized_key.get("passed"))
        expected = bool_value(unwrap_observed_value(by_normalized_key.get("expected")))
        if passed is True and expected is not None:
            return expected

    return None


def first_value(value: Any, candidate_keys: Iterable[str]) -> Any:
    for _path, item in values_for_keys(value, candidate_keys):
        unwrapped = unwrap_observed_value(item)
        if unwrapped is not None:
            return unwrapped
    return None

def bool_value(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "yes", "1"}:
            return True
        if text in {"false", "no", "0"}:
            return False
    return None


def int_value(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
        if parsed.is_integer():
            return int(parsed)
    return None


def float_value(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return float(value)
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
        if math.isfinite(parsed):
            return parsed
    return None


def load_jsonl(path: Path) -> LoadedJsonl:
    if not path.exists():
        raise PacketError(f"missing upstream JSONL: {path}")
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_no, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                record = json.loads(text)
            except json.JSONDecodeError as exc:
                raise PacketError(f"malformed JSONL at {path}:{line_no}: {exc}") from exc
            if not isinstance(record, dict):
                raise PacketError(f"non-object JSONL record at {path}:{line_no}")
            records.append(record)
    if len(records) != 1:
        raise PacketError(f"expected exactly one JSONL record in {path}, found {len(records)}")
    return LoadedJsonl(path=path, records=tuple(records))


def dumped_json_line(record: Mapping[str, Any]) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"


def write_jsonl(path: Path, record: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumped_json_line(record), encoding="utf-8")


def authorization_map() -> dict[str, bool]:
    return {key: False for key in AUTHORIZATION_FALSE_FIELDS}


def count_embedded_violations(record: Mapping[str, Any]) -> int:
    count = 0
    for path, value in iter_paths(record):
        if path and normalized_key(path[-1]) == "violations" and isinstance(value, list):
            count += len(value)
    return count


def unsafe_authorization_paths(record: Mapping[str, Any]) -> list[str]:
    """Find unsafe effective authorization fields.

    Audit/check metadata under keys named "checks" is not an effective
    authorization field. However, an explicit failed check for a blocked
    authorization invariant still fails closed.
    """

    unsafe: list[str] = []
    wanted = {normalized_key(key) for key in AUTHORIZATION_FALSE_FIELDS}
    wanted.add("effectivenewentriesblocked")

    for path, value in iter_paths(record):
        if not path:
            continue

        normalized_path = [normalized_key(part) for part in path]
        key = normalized_key(path[-1])

        if key not in wanted:
            continue

        joined = ".".join(path)

        if "checks" in normalized_path:
            if isinstance(value, Mapping):
                by_normalized_key = {normalized_key(str(k)): v for k, v in value.items()}
                passed = bool_value(by_normalized_key.get("passed"))
                if passed is False:
                    unsafe.append(f"{joined} check explicitly failed")
            continue

        parsed = bool_check_value(value)
        observed_value = unwrap_observed_value(value)

        if key == "effectivenewentriesblocked":
            if parsed is not True:
                unsafe.append(f"{joined} expected true got {observed_value!r}")
        elif parsed is not False:
            unsafe.append(f"{joined} expected false got {observed_value!r}")

    return unsafe

def summarize_upstream(
    name: str,
    loaded: LoadedJsonl | None,
    observed_at: datetime,
    max_age_seconds: float,
    max_future_skew_seconds: float,
) -> dict[str, Any]:
    if loaded is None:
        return {
            "path": str(REQUIRED_UPSTREAM_REPORTS.get(name, "")),
            "loaded": False,
            "verdict": None,
            "observed_at_utc": None,
            "age_seconds": None,
            "embedded_violations": None,
        }

    record = loaded.records[0]
    upstream_observed_at_text = first_value(record, ("observed_at_utc", "observed_at"))
    upstream_observed_at = parse_utc(upstream_observed_at_text)
    age_seconds: float | None = None
    if upstream_observed_at is not None:
        age_seconds = (observed_at - upstream_observed_at).total_seconds()

    return {
        "path": str(loaded.path),
        "loaded": True,
        "schema_version": record.get("schema_version"),
        "strategy": record.get("strategy"),
        "packet_type": record.get("packet_type"),
        "verdict": record.get("verdict"),
        "observed_at_utc": upstream_observed_at_text,
        "age_seconds": age_seconds,
        "max_allowed_age_seconds": max_age_seconds,
        "max_allowed_future_skew_seconds": max_future_skew_seconds,
        "embedded_violations": count_embedded_violations(record),
    }


def add_check(
    checks: list[dict[str, Any]],
    violations: list[str],
    name: str,
    passed: bool,
    expected: Any = None,
    observed: Any = None,
    violation: str | None = None,
) -> None:
    check = {"name": name, "passed": bool(passed)}
    if expected is not None:
        check["expected"] = expected
    if observed is not None:
        check["observed"] = observed
    checks.append(check)
    if not passed:
        violations.append(violation or name)


def first_across(
    loaded_records: Mapping[str, Mapping[str, Any]],
    upstream_names: Sequence[str],
    candidate_keys: Iterable[str],
) -> Any:
    for name in upstream_names:
        record = loaded_records.get(name)
        if record is None:
            continue
        value = first_value(record, candidate_keys)
        if value is not None:
            return value
    return None


def extract_symbol_snapshots(record: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    snapshots: dict[str, dict[str, Any]] = {}

    def record_symbol(symbol: str, payload: Mapping[str, Any]) -> None:
        snapshots.setdefault(symbol, {})
        target = snapshots[symbol]
        for source_key, output_key in (
            ("verdict", "verdict"),
            ("bid", "bid"),
            ("ask", "ask"),
            ("spread_points", "spread_points"),
            ("spread", "spread"),
            ("tick_age_seconds", "tick_age_seconds"),
            ("time", "time"),
            ("time_msc", "time_msc"),
        ):
            value = first_value(payload, (source_key,))
            if value is not None and output_key not in target:
                target[output_key] = value

    for _path, value in iter_paths(record):
        if isinstance(value, Mapping):
            symbol = first_value(value, ("symbol", "runtime_symbol"))
            if symbol in {EXPECTED_RUNTIME_SYMBOL, "USDJPYm"}:
                record_symbol(str(symbol), value)
            for symbol_key in (EXPECTED_RUNTIME_SYMBOL, "USDJPYm"):
                nested = value.get(symbol_key)
                if isinstance(nested, Mapping):
                    record_symbol(symbol_key, nested)

    return snapshots


def build_record(
    report_paths: Mapping[str, Path] | None = None,
    *,
    observed_at: datetime | None = None,
    max_upstream_age_seconds: float = DEFAULT_MAX_UPSTREAM_AGE_SECONDS,
    max_future_skew_seconds: float = DEFAULT_MAX_FUTURE_SKEW_SECONDS,
    position_open_over_three_bars: bool = False,
    machine_validated_over_three_bars: bool = False,
    machine_bar_count: int | None = None,
    bar_timeframe: str | None = None,
    position_open_time_utc: str | None = None,
) -> dict[str, Any]:
    observed_at = observed_at or utc_now()
    paths = dict(REQUIRED_UPSTREAM_REPORTS)
    if report_paths is not None:
        paths.update({key: Path(value) for key, value in report_paths.items()})

    violations: list[str] = []
    checks: list[dict[str, Any]] = []
    loaded: dict[str, LoadedJsonl | None] = {}

    for name, path in paths.items():
        try:
            loaded[name] = load_jsonl(path)
        except PacketError as exc:
            loaded[name] = None
            violations.append(str(exc))
            checks.append(
                {
                    "name": f"upstream_{name}_loaded",
                    "passed": False,
                    "expected": "one valid JSON object record",
                    "observed": str(exc),
                }
            )

    upstreams = {
        name: summarize_upstream(
            name,
            item,
            observed_at,
            max_upstream_age_seconds,
            max_future_skew_seconds,
        )
        for name, item in loaded.items()
    }
    loaded_records = {
        name: item.records[0]
        for name, item in loaded.items()
        if item is not None and item.records
    }

    for name, summary in upstreams.items():
        add_check(
            checks,
            violations,
            f"upstream_{name}_verdict_pass",
            summary.get("verdict") == "PASS",
            expected="PASS",
            observed=summary.get("verdict"),
            violation=f"{name}: upstream verdict is not PASS",
        )
        add_check(
            checks,
            violations,
            f"upstream_{name}_has_no_embedded_violations",
            summary.get("embedded_violations") == 0,
            expected=0,
            observed=summary.get("embedded_violations"),
            violation=f"{name}: upstream embedded violations present",
        )
        age_seconds = summary.get("age_seconds")
        add_check(
            checks,
            violations,
            f"upstream_{name}_fresh",
            isinstance(age_seconds, (int, float))
            and age_seconds <= max_upstream_age_seconds
            and age_seconds >= -max_future_skew_seconds,
            expected={
                "max_age_seconds": max_upstream_age_seconds,
                "max_future_skew_seconds": max_future_skew_seconds,
            },
            observed=age_seconds,
            violation=f"{name}: upstream evidence is missing, stale, or future-skewed",
        )

        record = loaded_records.get(name)
        if record is not None:
            unsafe = unsafe_authorization_paths(record)
            add_check(
                checks,
                violations,
                f"upstream_{name}_authorizations_remain_blocked",
                not unsafe,
                expected="all authorizations false and effective_new_entries_blocked true",
                observed=unsafe,
                violation=f"{name}: unsafe upstream authorization state",
            )

    ticket = first_across(
        loaded_records,
        ("pre_action_evidence_aggregate", "decision_artifact", "exact_ticket_governance"),
        ("exact_ticket",),
    )
    identifier = first_across(
        loaded_records,
        ("pre_action_evidence_aggregate", "decision_artifact", "exact_ticket_governance"),
        ("exact_identifier",),
    )
    canary_state = first_across(
        loaded_records,
        (
            "runtime_exposure_inventory",
            "unified_runtime_supervision",
            "pre_action_evidence_aggregate",
            "exact_ticket_governance",
        ),
        ("exact_canary_state", "canary_state"),
    )
    canary_observed = first_across(
        loaded_records,
        (
            "runtime_exposure_inventory",
            "unified_runtime_supervision",
            "pre_action_evidence_aggregate",
            "exact_ticket_governance",
        ),
        ("exact_canary_observed", "canary_observed"),
    )
    h024_position_count = first_across(
        loaded_records,
        ("runtime_exposure_inventory", "pre_action_evidence_aggregate", "exact_ticket_governance"),
        ("h024_position_count",),
    )
    h024_order_count = first_across(
        loaded_records,
        ("runtime_exposure_inventory", "pre_action_evidence_aggregate", "exact_ticket_governance"),
        ("h024_order_count",),
    )
    decision_status = first_across(
        loaded_records,
        ("decision_artifact", "exact_ticket_governance", "pre_action_evidence_aggregate"),
        ("decision_status",),
    )
    requested_action = first_across(
        loaded_records,
        ("decision_artifact", "pre_action_evidence_aggregate", "exact_ticket_governance"),
        ("requested_action",),
    )

    ticket_int = int_value(ticket)
    identifier_int = int_value(identifier)
    position_count_int = int_value(h024_position_count)
    order_count_int = int_value(h024_order_count)
    canary_observed_bool = bool_value(canary_observed)

    add_check(
        checks,
        violations,
        "exact_ticket_preserved",
        ticket_int == EXPECTED_TICKET,
        expected=EXPECTED_TICKET,
        observed=ticket,
        violation="exact ticket mismatch or missing",
    )
    add_check(
        checks,
        violations,
        "exact_identifier_preserved",
        identifier_int == EXPECTED_IDENTIFIER,
        expected=EXPECTED_IDENTIFIER,
        observed=identifier,
        violation="exact identifier mismatch or missing",
    )
    add_check(
        checks,
        violations,
        "exact_canary_state_observed",
        canary_state == EXPECTED_CANARY_STATE and canary_observed_bool is True,
        expected={"state": EXPECTED_CANARY_STATE, "observed": True},
        observed={"state": canary_state, "observed": canary_observed},
        violation="exact XAUUSDm canary is not observed",
    )
    add_check(
        checks,
        violations,
        "no_extra_h024_exposure",
        position_count_int == 1 and order_count_int == 0,
        expected={"h024_position_count": 1, "h024_order_count": 0},
        observed={"h024_position_count": h024_position_count, "h024_order_count": h024_order_count},
        violation="unexpected H024 exposure/order state",
    )
    add_check(
        checks,
        violations,
        "decision_artifact_non_authorizing",
        decision_status == NO_CLOSE_MODIFY_DECISION and requested_action == NO_CLOSE_MODIFY_DECISION,
        expected={
            "decision_status": NO_CLOSE_MODIFY_DECISION,
            "requested_action": NO_CLOSE_MODIFY_DECISION,
        },
        observed={"decision_status": decision_status, "requested_action": requested_action},
        violation="decision artifact is missing, ambiguous, or action-implying",
    )

    if machine_validated_over_three_bars:
        classification = "MACHINE_VALIDATED"
        sufficient_machine_evidence = (
            isinstance(machine_bar_count, int)
            and machine_bar_count > 3
            and isinstance(bar_timeframe, str)
            and bool(bar_timeframe.strip())
        )
    elif position_open_over_three_bars:
        classification = "OPERATOR_REPORTED_ONLY"
        sufficient_machine_evidence = False
    else:
        classification = "INSUFFICIENT_BAR_AGE_EVIDENCE"
        sufficient_machine_evidence = False

    add_check(
        checks,
        violations,
        "bar_age_evidence_classified",
        classification in {"MACHINE_VALIDATED", "OPERATOR_REPORTED_ONLY"},
        expected="machine-validated or explicitly operator-reported over-three-bars evidence",
        observed=classification,
        violation="missing over-three-bars evidence",
    )
    add_check(
        checks,
        violations,
        "machine_validation_has_sufficient_evidence_when_claimed",
        (not machine_validated_over_three_bars) or sufficient_machine_evidence,
        expected="machine validation requires bar_timeframe and machine_bar_count > 3",
        observed={"bar_timeframe": bar_timeframe, "machine_bar_count": machine_bar_count},
        violation="machine-validated bar age claimed without sufficient read-only evidence",
    )

    risk_record = loaded_records.get("runtime_account_risk_margin", {})
    exposure_record = loaded_records.get("runtime_exposure_inventory", {})
    tick_record = loaded_records.get("runtime_tick_spread", {})

    risk_snapshot = {
        "account_server": first_value(risk_record, ("account_server", "server")),
        "account_currency": first_value(risk_record, ("account_currency", "currency")),
        "balance": first_value(risk_record, ("balance",)),
        "equity": first_value(risk_record, ("equity",)),
        "profit": first_value(risk_record, ("profit",)),
        "margin": first_value(risk_record, ("margin",)),
        "free_margin": first_value(risk_record, ("free_margin", "margin_free")),
        "margin_level": first_value(risk_record, ("margin_level",)),
        "margin_used_fraction": first_value(risk_record, ("margin_used_fraction",)),
    }
    exposure_snapshot = {
        "canary_state": canary_state,
        "exact_canary_observed": canary_observed_bool,
        "h024_position_count": h024_position_count,
        "h024_order_count": h024_order_count,
        "position_profit": first_value(exposure_record, ("profit", "position_profit")),
        "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
        "model_symbol": EXPECTED_MODEL_SYMBOL,
        "side": EXPECTED_SIDE,
        "mt5_position_type": EXPECTED_MT5_POSITION_TYPE,
        "volume": EXPECTED_VOLUME,
        "magic": EXPECTED_MAGIC,
    }
    spread_snapshot = {
        "symbols": extract_symbol_snapshots(tick_record),
    }

    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": format_utc(observed_at),
        "expected": {
            "exact_ticket": EXPECTED_TICKET,
            "exact_identifier": EXPECTED_IDENTIFIER,
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "side": EXPECTED_SIDE,
            "mt5_position_type": EXPECTED_MT5_POSITION_TYPE,
            "volume": EXPECTED_VOLUME,
            "magic": EXPECTED_MAGIC,
            "canary_state": EXPECTED_CANARY_STATE,
            "decision_status": NO_CLOSE_MODIFY_DECISION,
            "requested_action": NO_CLOSE_MODIFY_DECISION,
            "required_upstreams": sorted(REQUIRED_UPSTREAM_REPORTS),
        },
        "upstreams": upstreams,
        "canary_identity": {
            "exact_ticket": ticket,
            "exact_identifier": identifier,
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "side": EXPECTED_SIDE,
            "mt5_position_type": EXPECTED_MT5_POSITION_TYPE,
            "volume": EXPECTED_VOLUME,
            "magic": EXPECTED_MAGIC,
            "canary_state": canary_state,
            "exact_canary_observed": canary_observed_bool,
        },
        "bar_age_evidence": {
            "classification": classification,
            "operator_reported_position_open_over_three_bars": bool(position_open_over_three_bars),
            "machine_validated_over_three_bars": bool(machine_validated_over_three_bars),
            "sufficient_machine_evidence": sufficient_machine_evidence,
            "machine_bar_count": machine_bar_count,
            "bar_timeframe": bar_timeframe,
            "position_open_time_utc": position_open_time_utc,
            "operator_reported_only_caveat": classification == "OPERATOR_REPORTED_ONLY",
        },
        "exit_condition_evidence": {
            "decision_status": decision_status,
            "requested_action": requested_action,
            "close_modify_authorized": False,
            "exit_condition_authorizes_action": False,
            "interpretation": (
                "bar-age and exit-condition evidence is for read-only operator review only"
            ),
        },
        "risk_snapshot": risk_snapshot,
        "exposure_snapshot": exposure_snapshot,
        "spread_snapshot": spread_snapshot,
        "checks": checks,
        "effective_new_entries_blocked": True,
        **authorization_map(),
        "violations": violations,
    }

    if violations:
        record["operator_state"] = FAIL_OPERATOR_STATE
        record["operator_next_action"] = FAIL_OPERATOR_NEXT_ACTION
        record["verdict"] = "FAIL_CLOSED"
    else:
        record["operator_state"] = PASS_OPERATOR_STATE
        record["operator_next_action"] = PASS_OPERATOR_NEXT_ACTION
        record["verdict"] = "PASS"

    return record


def validate_record(record: Mapping[str, Any]) -> list[str]:
    violations: list[str] = []

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append("wrong or missing schema_version")
    if record.get("strategy") != STRATEGY:
        violations.append("wrong or missing strategy")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append("wrong or missing packet_type")

    if record.get("effective_new_entries_blocked") is not True:
        violations.append("effective_new_entries_blocked is not true")
    for field in AUTHORIZATION_FALSE_FIELDS:
        if record.get(field) is not False:
            violations.append(f"{field} is not false")

    expected = record.get("expected")
    if not isinstance(expected, Mapping):
        violations.append("expected block missing or malformed")
    else:
        if int_value(expected.get("exact_ticket")) != EXPECTED_TICKET:
            violations.append("expected exact ticket mismatch")
        if int_value(expected.get("exact_identifier")) != EXPECTED_IDENTIFIER:
            violations.append("expected exact identifier mismatch")

    canary_identity = record.get("canary_identity")
    if not isinstance(canary_identity, Mapping):
        violations.append("canary_identity block missing or malformed")
    else:
        if int_value(canary_identity.get("exact_ticket")) != EXPECTED_TICKET:
            violations.append("canary_identity exact ticket mismatch")
        if int_value(canary_identity.get("exact_identifier")) != EXPECTED_IDENTIFIER:
            violations.append("canary_identity exact identifier mismatch")
        if canary_identity.get("runtime_symbol") != EXPECTED_RUNTIME_SYMBOL:
            violations.append("canary_identity runtime symbol mismatch")
        if canary_identity.get("model_symbol") != EXPECTED_MODEL_SYMBOL:
            violations.append("canary_identity model symbol mismatch")
        if canary_identity.get("side") != EXPECTED_SIDE:
            violations.append("canary_identity side mismatch")
        if int_value(canary_identity.get("mt5_position_type")) != EXPECTED_MT5_POSITION_TYPE:
            violations.append("canary_identity MT5 position type mismatch")
        if float_value(canary_identity.get("volume")) != EXPECTED_VOLUME:
            violations.append("canary_identity volume mismatch")
        if int_value(canary_identity.get("magic")) != EXPECTED_MAGIC:
            violations.append("canary_identity magic mismatch")
        if canary_identity.get("canary_state") != EXPECTED_CANARY_STATE:
            violations.append("canary_identity canary state mismatch")
        if canary_identity.get("exact_canary_observed") is not True:
            violations.append("canary_identity exact canary not observed")

    upstreams = record.get("upstreams")
    if not isinstance(upstreams, Mapping):
        violations.append("upstreams block missing or malformed")
    else:
        for name in REQUIRED_UPSTREAM_REPORTS:
            summary = upstreams.get(name)
            if not isinstance(summary, Mapping):
                violations.append(f"missing upstream summary {name}")
                continue
            if summary.get("verdict") != "PASS":
                violations.append(f"upstream {name} verdict is not PASS")
            if summary.get("embedded_violations") != 0:
                violations.append(f"upstream {name} has embedded violations")

    bar_age = record.get("bar_age_evidence")
    if not isinstance(bar_age, Mapping):
        violations.append("bar_age_evidence block missing or malformed")
    else:
        classification = bar_age.get("classification")
        if classification not in {"MACHINE_VALIDATED", "OPERATOR_REPORTED_ONLY"}:
            violations.append("bar age evidence classification is not passable")
        if classification == "MACHINE_VALIDATED":
            if bar_age.get("machine_validated_over_three_bars") is not True:
                violations.append("machine classification without machine flag")
            if bar_age.get("sufficient_machine_evidence") is not True:
                violations.append("machine classification without sufficient evidence")
            if int_value(bar_age.get("machine_bar_count")) is None or int_value(bar_age.get("machine_bar_count")) <= 3:
                violations.append("machine classification without machine_bar_count > 3")
            if not isinstance(bar_age.get("bar_timeframe"), str) or not bar_age.get("bar_timeframe").strip():
                violations.append("machine classification without bar_timeframe")
        if classification == "OPERATOR_REPORTED_ONLY":
            if bar_age.get("operator_reported_position_open_over_three_bars") is not True:
                violations.append("operator-reported classification without operator report")
            if bar_age.get("machine_validated_over_three_bars") is True:
                violations.append("operator-reported classification conflicts with machine flag")

    exit_evidence = record.get("exit_condition_evidence")
    if not isinstance(exit_evidence, Mapping):
        violations.append("exit_condition_evidence block missing or malformed")
    else:
        if exit_evidence.get("decision_status") != NO_CLOSE_MODIFY_DECISION:
            violations.append("exit decision_status is not non-authorizing")
        if exit_evidence.get("requested_action") != NO_CLOSE_MODIFY_DECISION:
            violations.append("exit requested_action is not non-authorizing")
        if exit_evidence.get("exit_condition_authorizes_action") is not False:
            violations.append("exit condition authorizes action")

    embedded_violations = record.get("violations")
    if record.get("verdict") == "PASS" and embedded_violations:
        violations.append("PASS record contains violations")
    if record.get("verdict") == "PASS" and record.get("operator_state") != PASS_OPERATOR_STATE:
        violations.append("PASS record has wrong operator_state")
    if record.get("verdict") == "FAIL_CLOSED" and record.get("operator_state") != FAIL_OPERATOR_STATE:
        violations.append("FAIL_CLOSED record has wrong operator_state")
    if record.get("verdict") not in {"PASS", "FAIL_CLOSED"}:
        violations.append("verdict is not PASS or FAIL_CLOSED")

    return violations


def verify_jsonl(path: Path, *, require_pass: bool = False) -> dict[str, Any]:
    try:
        loaded = load_jsonl(path)
    except PacketError as exc:
        return {
            "record_count": 0,
            "violations": [str(exc)],
            "record_verdict": None,
            "verifier_verdict": "FAIL",
        }

    record = loaded.records[0]
    violations = validate_record(record)
    if require_pass and record.get("verdict") != "PASS":
        violations.append("--require-pass used but record verdict is not PASS")

    return {
        "record_count": len(loaded.records),
        "violations": violations,
        "record_verdict": record.get("verdict"),
        "verifier_verdict": "PASS" if not violations else "FAIL",
        "operator_state": record.get("operator_state"),
        "operator_next_action": record.get("operator_next_action"),
        "exact_ticket": first_value(record, ("exact_ticket",)),
        "exact_identifier": first_value(record, ("exact_identifier",)),
        "effective_new_entries_blocked": record.get("effective_new_entries_blocked"),
        **{field: record.get(field) for field in AUTHORIZATION_FALSE_FIELDS},
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl",
        help="Output JSONL path.",
    )
    parser.add_argument(
        "--position-open-over-three-bars",
        action="store_true",
        help="Record operator-reported evidence that the exact canary has been open over three bars.",
    )
    parser.add_argument(
        "--machine-validated-over-three-bars",
        action="store_true",
        help="Claim machine-validated over-three-bars evidence. Requires --bar-timeframe and --machine-bar-count > 3.",
    )
    parser.add_argument("--machine-bar-count", type=int, default=None)
    parser.add_argument("--bar-timeframe", default=None)
    parser.add_argument("--position-open-time-utc", default=None)
    parser.add_argument("--max-upstream-age-seconds", type=float, default=DEFAULT_MAX_UPSTREAM_AGE_SECONDS)
    return parser


def build_main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    record = build_record(
        position_open_over_three_bars=args.position_open_over_three_bars,
        machine_validated_over_three_bars=args.machine_validated_over_three_bars,
        machine_bar_count=args.machine_bar_count,
        bar_timeframe=args.bar_timeframe,
        position_open_time_utc=args.position_open_time_utc,
        max_upstream_age_seconds=args.max_upstream_age_seconds,
    )
    output = Path(args.output)
    write_jsonl(output, record)

    print(f"Wrote {output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Operator state: {record['operator_state']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Exact ticket: {record['canary_identity']['exact_ticket']}")
    print(f"Exact identifier: {record['canary_identity']['exact_identifier']}")
    print(f"Bar-age classification: {record['bar_age_evidence']['classification']}")
    print(
        "Operator reported position open over three bars: "
        f"{record['bar_age_evidence']['operator_reported_position_open_over_three_bars']}"
    )
    print(
        "Machine validated over three bars: "
        f"{record['bar_age_evidence']['machine_validated_over_three_bars']}"
    )
    print(f"Effective new entries blocked: {record['effective_new_entries_blocked']}")
    for field in AUTHORIZATION_FALSE_FIELDS:
        print(f"{field}: {record[field]}")
    for name, summary in record["upstreams"].items():
        print(
            f"Upstream {name}: verdict={summary.get('verdict')} "
            f"age_seconds={summary.get('age_seconds')} "
            f"embedded_violations={summary.get('embedded_violations')}"
        )

    return 0 if record["verdict"] == "PASS" else 1


def verify_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify H024 bar-age exit-condition evidence JSONL.")
    parser.add_argument("path")
    parser.add_argument("--require-pass", action="store_true")
    return parser


def verify_main(argv: Sequence[str] | None = None) -> int:
    parser = verify_arg_parser()
    args = parser.parse_args(argv)
    result = verify_jsonl(Path(args.path), require_pass=args.require_pass)

    print("H024 exact-ticket canary close/modify bar-age exit-condition evidence records: "
          f"{result['record_count']}")
    print(f"Violations: {len(result['violations'])}")
    for violation in result["violations"]:
        print(f"- {violation}")
    print(f"Record verdict: {result['record_verdict']}")
    print(f"Verifier verdict: {result['verifier_verdict']}")
    print(f"Operator state: {result.get('operator_state')}")
    print(f"Operator next action: {result.get('operator_next_action')}")
    print(f"Exact ticket: {result.get('exact_ticket')}")
    print(f"Exact identifier: {result.get('exact_identifier')}")
    print(f"Effective new entries blocked: {result.get('effective_new_entries_blocked')}")
    for field in AUTHORIZATION_FALSE_FIELDS:
        print(f"{field}: {result.get(field)}")

    return 0 if result["verifier_verdict"] == "PASS" else 1


__all__ = [
    "AUTHORIZATION_FALSE_FIELDS",
    "DEFAULT_MAX_UPSTREAM_AGE_SECONDS",
    "EXPECTED_IDENTIFIER",
    "EXPECTED_TICKET",
    "PACKET_TYPE",
    "PASS_OPERATOR_NEXT_ACTION",
    "PASS_OPERATOR_STATE",
    "REQUIRED_UPSTREAM_REPORTS",
    "SCHEMA_VERSION",
    "STRATEGY",
    "build_record",
    "validate_record",
    "verify_jsonl",
    "bool_check_value",
    "unwrap_observed_value",
    "write_jsonl",
]
