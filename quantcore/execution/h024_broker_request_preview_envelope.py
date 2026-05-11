"""H024 broker-request preview envelope.

This module adds two tightly scoped artifacts:

1. A preview-only broker-request construction approval.
2. An inert broker-request preview envelope built from verified H024 intent context.

The preview envelope is not an MT5 request, not a broker request, and not an
order payload. It is a review-only JSON envelope. It does not import MT5,
dispatch transport, mutate terminal state, mutate broker state, place demo/live
orders, or approve execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


APPROVAL_SCHEMA = "h024_broker_request_preview_construction_approval_v1"
APPROVAL_KIND = "BROKER_REQUEST_PREVIEW_CONSTRUCTION_APPROVAL"
APPROVAL_STATUS = "BROKER_REQUEST_PREVIEW_CONSTRUCTION_APPROVED_NO_DISPATCH_AUTHORITY"
APPROVAL_DECISION = "APPROVE_PREVIEW_ENVELOPE_CONSTRUCTION_ONLY_NO_MT5_NO_DISPATCH"

READINESS_SCHEMA = "h024_broker_request_construction_readiness_packet_v1"
READINESS_KIND = "BROKER_REQUEST_CONSTRUCTION_READINESS_PACKET_REVIEW_ONLY"
READINESS_DECISION = "REQUEST_HUMAN_BROKER_REQUEST_CONSTRUCTION_REVIEW_NO_EXECUTION_AUTHORITY"

PREVIEW_SCHEMA = "h024_broker_request_preview_envelope_v1"
PREVIEW_KIND = "BROKER_REQUEST_PREVIEW_ENVELOPE"
PREVIEW_STATUS = "PREVIEW_ENVELOPE_CONSTRUCTED_NO_BROKER_REQUEST_NO_DISPATCH"
PREVIEW_DECISION = "CONSTRUCT_PREVIEW_ENVELOPE_ONLY_REFUSE_DISPATCH"

REQUIRED_TRUE_APPROVAL_FLAGS = (
    "phase4_approved",
    "demo_execution_adapter_implementation_approved",
    "execution_adapter_implementation_approved",
    "adapter_readiness_review_approved",
    "adapter_use_readiness_review_approved",
    "noop_adapter_use_approved",
    "broker_request_construction_readiness_reviewed",
    "broker_request_preview_construction_approved",
    "preview_envelope_only",
)

REQUIRED_TRUE_PREVIEW_FLAGS = (
    "broker_request_preview_construction_approved",
    "preview_envelope_only",
    "preview_envelope_constructed",
    "verified_intent_consumed",
    "h020_sizing_consumed_not_reinterpreted",
    "idempotency_key_attached",
    "kill_switch_allow_state_required",
    "request_construction_refused_beyond_preview",
)

REQUIRED_FALSE_FLAGS = (
    "broker_request_construction_approved",
    "execution_adapter_use_approved",
    "execution_adapter_approved",
    "broker_request_approved",
    "mt5_execution_approved",
    "terminal_mutation_approved",
    "demo_order_placement_approved",
    "live_order_placement_approved",
    "execution_approved",
    "broker_request_constructed",
    "mt5_request_constructed",
    "order_payload_constructed",
    "transport_dispatch_attempted",
    "dispatch_attempted",
    "terminal_mutated",
    "broker_state_mutated",
)


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    violations: tuple[str, ...]


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            records.append(value)
    return records


def read_single_jsonl_record(path: str | Path) -> dict[str, Any]:
    records = _read_jsonl(Path(path))
    if len(records) != 1:
        raise ValueError(f"{path}: expected exactly one JSONL record, found {len(records)}")
    return records[0]


def write_single_jsonl_record(path: str | Path, record: dict[str, Any]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
        handle.write("\n")


def read_json_or_jsonl(path: str | Path) -> dict[str, Any]:
    input_path = Path(path)
    text = input_path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError(f"{path}: empty file")
    if text.startswith("{"):
        value = json.loads(text)
        if not isinstance(value, dict):
            raise ValueError(f"{path}: expected JSON object")
        return value
    return read_single_jsonl_record(input_path)


def _stable_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _json_contains_text(record: dict[str, Any], needle: str) -> bool:
    return needle in json.dumps(record, sort_keys=True, default=str)


def _violations_zero(value: Any) -> bool:
    return value in (0, [], None)


def _verdict_pass(record: dict[str, Any]) -> bool:
    return str(record.get("verdict", "PASS")).upper() == "PASS"


def _walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _find_first_key(record: dict[str, Any], *keys: str) -> Any:
    lowered = {key.lower() for key in keys}
    for value in _walk(record):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in lowered:
                    return child
    return None


def _nested_bool(record: dict[str, Any], key: str) -> bool | None:
    for value in _walk(record):
        if isinstance(value, dict) and key in value and isinstance(value[key], bool):
            return value[key]
    return None


def _upstream_summary(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": record.get("schema"),
        "kind": record.get("kind"),
        "status": record.get("status"),
        "decision": record.get("decision"),
        "verdict": record.get("verdict", "PASS"),
        "violations": record.get("violations", 0),
        "digest": _stable_digest(record),
    }


def _require_upstream(
    record: dict[str, Any],
    *,
    schema: str | None,
    kind: str | None,
    decision: str | None,
    label: str,
) -> list[str]:
    violations: list[str] = []
    if schema is not None and record.get("schema") != schema:
        violations.append(f"{label}: schema mismatch")
    if kind is not None and record.get("kind") != kind:
        violations.append(f"{label}: kind mismatch")
    if decision is not None and record.get("decision") != decision:
        violations.append(f"{label}: decision mismatch")
    if not _verdict_pass(record):
        violations.append(f"{label}: verdict is not PASS")
    if not _violations_zero(record.get("violations")):
        violations.append(f"{label}: violations are non-zero")
    return violations


def build_preview_construction_approval_record(
    *,
    readiness_packet: dict[str, Any],
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    violations = _require_upstream(
        readiness_packet,
        schema=READINESS_SCHEMA,
        kind=READINESS_KIND,
        decision=READINESS_DECISION,
        label="broker_request_construction_readiness_packet",
    )

    if allowed_demo_server and not _json_contains_text(readiness_packet, allowed_demo_server):
        violations.append(f"allowed demo server not observed: {allowed_demo_server}")

    record: dict[str, Any] = {
        "schema": APPROVAL_SCHEMA,
        "kind": APPROVAL_KIND,
        "status": APPROVAL_STATUS,
        "decision": APPROVAL_DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": allowed_demo_server,
        "authority": {
            "phase4_approved": True,
            "demo_execution_adapter_implementation_approved": True,
            "execution_adapter_implementation_approved": True,
            "adapter_readiness_review_approved": True,
            "adapter_use_readiness_review_approved": True,
            "noop_adapter_use_approved": True,
            "broker_request_construction_readiness_reviewed": True,
            "broker_request_preview_construction_approved": True,
            "preview_envelope_only": True,
            "broker_request_construction_approved": False,
            "execution_adapter_use_approved": False,
            "execution_adapter_approved": False,
            "broker_request_approved": False,
            "mt5_execution_approved": False,
            "terminal_mutation_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_approved": False,
        },
        "approved_scope": {
            "scope": "preview_envelope_construction_only",
            "may_build_preview_envelope": True,
            "may_construct_broker_request": False,
            "may_construct_mt5_request": False,
            "may_construct_order_payload": False,
            "may_dispatch_transport": False,
            "may_mutate_terminal": False,
            "may_mutate_broker_state": False,
            "may_place_demo_order": False,
            "may_place_live_order": False,
        },
        "mutation_safety": {
            "broker_request_constructed": False,
            "mt5_request_constructed": False,
            "order_payload_constructed": False,
            "transport_dispatch_attempted": False,
            "dispatch_attempted": False,
            "terminal_mutated": False,
            "broker_state_mutated": False,
        },
        "upstream_artifacts": {
            "broker_request_construction_readiness_packet": _upstream_summary(readiness_packet),
        },
    }

    result = verify_preview_construction_approval_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_pass=False,
    )
    if result.violations:
        record["verdict"] = "FAIL"
        record["violations"] = list(dict.fromkeys([*violations, *result.violations]))

    return record


def build_preview_construction_approval_from_files(
    *,
    readiness_packet_jsonl: str | Path,
    output_jsonl: str | Path,
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    readiness_packet = read_single_jsonl_record(readiness_packet_jsonl)
    record = build_preview_construction_approval_record(
        readiness_packet=readiness_packet,
        allowed_demo_server=allowed_demo_server,
    )
    write_single_jsonl_record(output_jsonl, record)
    return record


def verify_preview_construction_approval_record(
    record: dict[str, Any],
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    violations: list[str] = []

    expected_scalars = {
        "schema": APPROVAL_SCHEMA,
        "kind": APPROVAL_KIND,
        "status": APPROVAL_STATUS,
        "decision": APPROVAL_DECISION,
    }
    for key, expected in expected_scalars.items():
        if record.get(key) != expected:
            violations.append(f"{key} mismatch: expected {expected!r}, got {record.get(key)!r}")

    if require_pass and record.get("verdict") != "PASS":
        violations.append("verdict is not PASS")
    if not _violations_zero(record.get("violations")):
        violations.append("record violations are non-zero")
    if allowed_demo_server and not _json_contains_text(record, allowed_demo_server):
        violations.append(f"allowed demo server not observed: {allowed_demo_server}")

    for key in REQUIRED_TRUE_APPROVAL_FLAGS:
        if _nested_bool(record, key) is not True:
            violations.append(f"{key} must be true")
    for key in REQUIRED_FALSE_FLAGS:
        if _nested_bool(record, key) is not False:
            violations.append(f"{key} must be false")

    approved_scope = record.get("approved_scope")
    if not isinstance(approved_scope, dict):
        violations.append("approved_scope block missing")
    else:
        if approved_scope.get("scope") != "preview_envelope_construction_only":
            violations.append("scope must be preview_envelope_construction_only")
        if approved_scope.get("may_build_preview_envelope") is not True:
            violations.append("may_build_preview_envelope must be true")
        for key, value in approved_scope.items():
            if key.startswith("may_") and key != "may_build_preview_envelope" and value is not False:
                violations.append(f"{key} must be false")

    return VerificationResult(ok=not violations, violations=tuple(violations))


def verify_preview_construction_approval_file(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    return verify_preview_construction_approval_record(
        read_single_jsonl_record(path),
        allowed_demo_server=allowed_demo_server,
        require_pass=require_pass,
    )


def _intent_summary(order_intent_simulation: dict[str, Any]) -> dict[str, Any]:
    digest = _stable_digest(order_intent_simulation)
    return {
        "intent_digest": digest,
        "intent_id": _find_first_key(order_intent_simulation, "intent_id", "stable_intent_id")
        or digest[:24],
        "symbol": _find_first_key(order_intent_simulation, "symbol"),
        "normalized_symbol": _find_first_key(order_intent_simulation, "normalized_symbol"),
        "side": _find_first_key(order_intent_simulation, "side"),
        "timeframe": _find_first_key(order_intent_simulation, "timeframe"),
        "entry": _find_first_key(order_intent_simulation, "entry", "entry_price"),
        "stop": _find_first_key(order_intent_simulation, "stop", "stop_price"),
        "final_lots": _find_first_key(order_intent_simulation, "final_lots", "lots", "volume"),
        "risk_fraction": _find_first_key(order_intent_simulation, "risk_fraction"),
    }


def build_preview_envelope_record(
    *,
    preview_construction_approval: dict[str, Any],
    order_intent_simulation: dict[str, Any],
    allow_state_preflight: dict[str, Any],
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    violations: list[str] = []
    violations.extend(
        _require_upstream(
            preview_construction_approval,
            schema=APPROVAL_SCHEMA,
            kind=APPROVAL_KIND,
            decision=APPROVAL_DECISION,
            label="preview_construction_approval",
        )
    )
    violations.extend(
        _require_upstream(
            order_intent_simulation,
            schema=None,
            kind=None,
            decision=None,
            label="order_intent_simulation",
        )
    )
    violations.extend(
        _require_upstream(
            allow_state_preflight,
            schema=None,
            kind=None,
            decision=None,
            label="allow_state_preflight",
        )
    )

    if allowed_demo_server and not (
        _json_contains_text(preview_construction_approval, allowed_demo_server)
        or _json_contains_text(order_intent_simulation, allowed_demo_server)
        or _json_contains_text(allow_state_preflight, allowed_demo_server)
    ):
        violations.append(f"allowed demo server not observed: {allowed_demo_server}")

    intent_summary = _intent_summary(order_intent_simulation)
    idempotency_material = {
        "intent_summary": intent_summary,
        "approval_digest": _stable_digest(preview_construction_approval),
        "allow_state_digest": _stable_digest(allow_state_preflight),
    }
    idempotency_key = "h024-preview-" + _stable_digest(idempotency_material)[:32]

    record: dict[str, Any] = {
        "schema": PREVIEW_SCHEMA,
        "kind": PREVIEW_KIND,
        "status": PREVIEW_STATUS,
        "decision": PREVIEW_DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": allowed_demo_server,
        "authority": {
            "broker_request_preview_construction_approved": True,
            "preview_envelope_only": True,
            "broker_request_construction_approved": False,
            "execution_adapter_use_approved": False,
            "execution_adapter_approved": False,
            "broker_request_approved": False,
            "mt5_execution_approved": False,
            "terminal_mutation_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_approved": False,
        },
        "preview_envelope": {
            "preview_envelope_constructed": True,
            "verified_intent_consumed": True,
            "h020_sizing_consumed_not_reinterpreted": True,
            "idempotency_key_attached": True,
            "idempotency_key": idempotency_key,
            "kill_switch_allow_state_required": True,
            "request_construction_refused_beyond_preview": True,
            "intent_summary": intent_summary,
            "not_mt5_request": True,
            "not_broker_request": True,
            "not_order_payload": True,
        },
        "mutation_safety": {
            "broker_request_constructed": False,
            "mt5_request_constructed": False,
            "order_payload_constructed": False,
            "transport_dispatch_attempted": False,
            "dispatch_attempted": False,
            "terminal_mutated": False,
            "broker_state_mutated": False,
        },
        "upstream_artifacts": {
            "preview_construction_approval": _upstream_summary(preview_construction_approval),
            "order_intent_simulation": _upstream_summary(order_intent_simulation),
            "allow_state_preflight": _upstream_summary(allow_state_preflight),
        },
    }

    result = verify_preview_envelope_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_pass=False,
    )
    if result.violations:
        record["verdict"] = "FAIL"
        record["violations"] = list(dict.fromkeys([*violations, *result.violations]))

    return record


def build_preview_envelope_from_files(
    *,
    preview_construction_approval_jsonl: str | Path,
    order_intent_simulation_jsonl: str | Path,
    allow_state_preflight_jsonl: str | Path,
    output_jsonl: str | Path,
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    approval = read_single_jsonl_record(preview_construction_approval_jsonl)
    order_intent = read_single_jsonl_record(order_intent_simulation_jsonl)
    allow_state = read_single_jsonl_record(allow_state_preflight_jsonl)
    record = build_preview_envelope_record(
        preview_construction_approval=approval,
        order_intent_simulation=order_intent,
        allow_state_preflight=allow_state,
        allowed_demo_server=allowed_demo_server,
    )
    write_single_jsonl_record(output_jsonl, record)
    return record


def verify_preview_envelope_record(
    record: dict[str, Any],
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    violations: list[str] = []

    expected_scalars = {
        "schema": PREVIEW_SCHEMA,
        "kind": PREVIEW_KIND,
        "status": PREVIEW_STATUS,
        "decision": PREVIEW_DECISION,
    }
    for key, expected in expected_scalars.items():
        if record.get(key) != expected:
            violations.append(f"{key} mismatch: expected {expected!r}, got {record.get(key)!r}")

    if require_pass and record.get("verdict") != "PASS":
        violations.append("verdict is not PASS")
    if not _violations_zero(record.get("violations")):
        violations.append("record violations are non-zero")
    if allowed_demo_server and not _json_contains_text(record, allowed_demo_server):
        violations.append(f"allowed demo server not observed: {allowed_demo_server}")

    for key in REQUIRED_TRUE_PREVIEW_FLAGS:
        if _nested_bool(record, key) is not True:
            violations.append(f"{key} must be true")
    for key in REQUIRED_FALSE_FLAGS:
        if _nested_bool(record, key) is not False:
            violations.append(f"{key} must be false")

    preview = record.get("preview_envelope")
    if not isinstance(preview, dict):
        violations.append("preview_envelope block missing")
    else:
        idempotency_key = preview.get("idempotency_key")
        if not isinstance(idempotency_key, str) or not idempotency_key.startswith("h024-preview-"):
            violations.append("idempotency_key must be a stable h024-preview key")
        for key in ("not_mt5_request", "not_broker_request", "not_order_payload"):
            if preview.get(key) is not True:
                violations.append(f"{key} must be true")

    return VerificationResult(ok=not violations, violations=tuple(violations))


def verify_preview_envelope_file(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    return verify_preview_envelope_record(
        read_single_jsonl_record(path),
        allowed_demo_server=allowed_demo_server,
        require_pass=require_pass,
    )


def main_approval(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("readiness_packet_jsonl")
    parser.add_argument("output_jsonl")
    parser.add_argument("--allowed-demo-server")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args(argv)

    if args.verify:
        result = verify_preview_construction_approval_file(
            args.readiness_packet_jsonl,
            allowed_demo_server=args.allowed_demo_server,
            require_pass=args.require_pass,
        )
        print(f"Violations: {len(result.violations)}")
        for violation in result.violations:
            print(f"- {violation}")
        print(f"Verdict: {'PASS' if result.ok else 'FAIL'}")
        return 0 if result.ok else 1

    record = build_preview_construction_approval_from_files(
        readiness_packet_jsonl=args.readiness_packet_jsonl,
        output_jsonl=args.output_jsonl,
        allowed_demo_server=args.allowed_demo_server,
    )
    print(f"Output: {args.output_jsonl}")
    print(f"Status: {record['status']}")
    print(f"Decision: {record['decision']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1


def main_preview(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("preview_construction_approval_jsonl")
    parser.add_argument("order_intent_simulation_jsonl")
    parser.add_argument("allow_state_preflight_jsonl")
    parser.add_argument("output_jsonl")
    parser.add_argument("--allowed-demo-server")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args(argv)

    if args.verify:
        result = verify_preview_envelope_file(
            args.preview_construction_approval_jsonl,
            allowed_demo_server=args.allowed_demo_server,
            require_pass=args.require_pass,
        )
        print(f"Violations: {len(result.violations)}")
        for violation in result.violations:
            print(f"- {violation}")
        print(f"Verdict: {'PASS' if result.ok else 'FAIL'}")
        return 0 if result.ok else 1

    record = build_preview_envelope_from_files(
        preview_construction_approval_jsonl=args.preview_construction_approval_jsonl,
        order_intent_simulation_jsonl=args.order_intent_simulation_jsonl,
        allow_state_preflight_jsonl=args.allow_state_preflight_jsonl,
        output_jsonl=args.output_jsonl,
        allowed_demo_server=args.allowed_demo_server,
    )
    print(f"Output: {args.output_jsonl}")
    print(f"Status: {record['status']}")
    print(f"Decision: {record['decision']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Verdict: {record['verdict']}")
    return 0 if record["verdict"] == "PASS" else 1