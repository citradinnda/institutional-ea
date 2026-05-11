"""H024 Phase 4 demo adapter no-op transport contract.

This module defines a pure-Python, fail-closed no-op transport contract for
the H024 demo adapter readiness path. It deliberately does not construct any
broker request, MT5 request, order payload, or dispatch path.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "h024_demo_adapter_noop_transport_contract_v1"
KIND = "DEMO_ADAPTER_NOOP_TRANSPORT_CONTRACT"
STATUS = "NOOP_TRANSPORT_CONTRACT_READY_REFUSES_EXECUTION"
DECISION = "REFUSE_TRANSPORT_NO_ADAPTER_USE_AUTHORITY"

READINESS_HUMAN_DECISION_SCHEMA = "h024_phase4_demo_adapter_readiness_human_decision_v1"
READINESS_HUMAN_DECISION_KIND = "PHASE4_DEMO_ADAPTER_READINESS_HUMAN_DECISION"
READINESS_HUMAN_DECISION_DECISION = "APPROVE_ADAPTER_READINESS_REVIEW_NO_EXECUTION"

INTENT_REFUSAL_AUDIT_SCHEMA = "h024_demo_adapter_intent_refusal_audit_v1"
INTENT_REFUSAL_AUDIT_KIND = "DEMO_ADAPTER_INTENT_REFUSAL_AUDIT"
INTENT_REFUSAL_AUDIT_DECISION = "REFUSE_DISPATCH_NO_ORDER_AUTHORITY"

BOUNDARY_STATIC_VERIFIER_SCHEMA = "h024_demo_adapter_boundary_static_verifier_v1"
BOUNDARY_STATIC_VERIFIER_KIND = "DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER"

REQUIRED_REFUSAL_REASONS = (
    "execution_adapter_use_not_approved",
    "demo_order_placement_not_approved",
    "execution_not_approved",
)

REQUIRED_TRUE_FLAGS = (
    "phase4_approved",
    "demo_execution_adapter_implementation_approved",
    "execution_adapter_implementation_approved",
    "adapter_readiness_review_approved",
    "intent_context_available",
    "noop_transport_contract_defined",
)

REQUIRED_FALSE_FLAGS = (
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


def _walk_values(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_values(child)


def _recursive_contains_text(record: dict[str, Any], needle: str) -> bool:
    return any(isinstance(value, str) and needle in value for value in _walk_values(record))


def _recursive_find_key(record: dict[str, Any], key: str) -> Any:
    if key in record:
        return record[key]
    for value in record.values():
        if isinstance(value, dict):
            found = _recursive_find_key(value, key)
            if found is not None:
                return found
        elif isinstance(value, list):
            for child in value:
                if isinstance(child, dict):
                    found = _recursive_find_key(child, key)
                    if found is not None:
                        return found
    return None


def _bool_from_any(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "pass", "approved"}:
            return True
        if lowered in {"false", "no", "fail", "blocked", "pending"}:
            return False
    return None


def _recursive_bool(record: dict[str, Any], key: str) -> bool | None:
    return _bool_from_any(_recursive_find_key(record, key))


def _record_verdict_pass(record: dict[str, Any]) -> bool:
    verdict = _recursive_find_key(record, "verdict")
    if verdict is None:
        return True
    return str(verdict).upper() == "PASS"


def _zero_violations(record: dict[str, Any]) -> bool:
    violations = _recursive_find_key(record, "violations")
    if violations is None:
        return True
    if isinstance(violations, int):
        return violations == 0
    if isinstance(violations, list):
        return len(violations) == 0
    return False


def _required_upstream_ok(
    record: dict[str, Any],
    *,
    schema: str,
    kind: str,
    decision: str | None,
    label: str,
) -> list[str]:
    violations: list[str] = []
    if record.get("schema") != schema:
        violations.append(f"{label}: schema mismatch")
    if record.get("kind") != kind:
        violations.append(f"{label}: kind mismatch")
    if decision is not None and record.get("decision") != decision:
        violations.append(f"{label}: decision mismatch")
    if not _record_verdict_pass(record):
        violations.append(f"{label}: verdict is not PASS")
    if not _zero_violations(record):
        violations.append(f"{label}: violations are non-zero")
    return violations


def _summarize_upstream(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": record.get("schema"),
        "kind": record.get("kind"),
        "status": record.get("status"),
        "decision": record.get("decision"),
        "verdict": record.get("verdict", "PASS"),
        "violations": record.get("violations", 0),
    }


def build_noop_transport_contract_record(
    *,
    readiness_human_decision: dict[str, Any],
    intent_refusal_audit: dict[str, Any],
    boundary_static_verifier: dict[str, Any] | None = None,
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    violations: list[str] = []

    violations.extend(
        _required_upstream_ok(
            readiness_human_decision,
            schema=READINESS_HUMAN_DECISION_SCHEMA,
            kind=READINESS_HUMAN_DECISION_KIND,
            decision=READINESS_HUMAN_DECISION_DECISION,
            label="readiness_human_decision",
        )
    )
    violations.extend(
        _required_upstream_ok(
            intent_refusal_audit,
            schema=INTENT_REFUSAL_AUDIT_SCHEMA,
            kind=INTENT_REFUSAL_AUDIT_KIND,
            decision=INTENT_REFUSAL_AUDIT_DECISION,
            label="intent_refusal_audit",
        )
    )

    if boundary_static_verifier is not None:
        violations.extend(
            _required_upstream_ok(
                boundary_static_verifier,
                schema=BOUNDARY_STATIC_VERIFIER_SCHEMA,
                kind=BOUNDARY_STATIC_VERIFIER_KIND,
                decision=None,
                label="boundary_static_verifier",
            )
        )

    if allowed_demo_server and not (
        _recursive_contains_text(readiness_human_decision, allowed_demo_server)
        or _recursive_contains_text(intent_refusal_audit, allowed_demo_server)
    ):
        violations.append(f"allowed demo server not observed: {allowed_demo_server}")

    record: dict[str, Any] = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "allowed_demo_server": allowed_demo_server,
        "authority": {
            "phase4_approved": True,
            "demo_execution_adapter_implementation_approved": True,
            "execution_adapter_implementation_approved": True,
            "adapter_readiness_review_approved": True,
            "execution_adapter_use_approved": False,
            "execution_adapter_approved": False,
            "broker_request_approved": False,
            "mt5_execution_approved": False,
            "terminal_mutation_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_approved": False,
        },
        "contract": {
            "intent_context_available": True,
            "noop_transport_contract_defined": True,
            "refusal_reasons": list(REQUIRED_REFUSAL_REASONS),
            "transport_decision": "REFUSE",
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
            "readiness_human_decision": _summarize_upstream(readiness_human_decision),
            "intent_refusal_audit": _summarize_upstream(intent_refusal_audit),
            "boundary_static_verifier": (
                _summarize_upstream(boundary_static_verifier)
                if boundary_static_verifier is not None
                else None
            ),
        },
        "non_authorizations_preserved": [
            "execution_adapter_use",
            "broker_request_construction",
            "mt5_execution",
            "terminal_mutation",
            "demo_order_placement",
            "live_order_placement",
            "execution",
        ],
    }

    verification = verify_noop_transport_contract_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_pass=False,
    )
    if verification.violations:
        record["verdict"] = "FAIL"
        record["violations"] = list(dict.fromkeys([*violations, *verification.violations]))

    return record


def build_noop_transport_contract_from_files(
    *,
    readiness_human_decision_jsonl: str | Path,
    intent_refusal_audit_jsonl: str | Path,
    output_jsonl: str | Path,
    boundary_static_verifier_jsonl: str | Path | None = None,
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    readiness = read_single_jsonl_record(readiness_human_decision_jsonl)
    intent = read_single_jsonl_record(intent_refusal_audit_jsonl)
    boundary = (
        read_single_jsonl_record(boundary_static_verifier_jsonl)
        if boundary_static_verifier_jsonl is not None
        else None
    )

    record = build_noop_transport_contract_record(
        readiness_human_decision=readiness,
        intent_refusal_audit=intent,
        boundary_static_verifier=boundary,
        allowed_demo_server=allowed_demo_server,
    )
    write_single_jsonl_record(output_jsonl, record)
    return record


def verify_noop_transport_contract_record(
    record: dict[str, Any],
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    violations: list[str] = []

    expected_scalars = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
    }
    for key, expected in expected_scalars.items():
        if record.get(key) != expected:
            violations.append(f"{key} mismatch: expected {expected!r}, got {record.get(key)!r}")

    if require_pass and record.get("verdict") != "PASS":
        violations.append("verdict is not PASS")

    raw_violations = record.get("violations")
    if raw_violations not in (0, [], None):
        violations.append("record violations are non-zero")

    if allowed_demo_server and not _recursive_contains_text(record, allowed_demo_server):
        violations.append(f"allowed demo server not observed: {allowed_demo_server}")

    for key in REQUIRED_TRUE_FLAGS:
        if _recursive_bool(record, key) is not True:
            violations.append(f"{key} must be true")

    for key in REQUIRED_FALSE_FLAGS:
        if _recursive_bool(record, key) is not False:
            violations.append(f"{key} must be false")

    refusal_reasons = _recursive_find_key(record, "refusal_reasons")
    if not isinstance(refusal_reasons, list):
        violations.append("refusal_reasons must be a list")
    else:
        missing = sorted(set(REQUIRED_REFUSAL_REASONS) - set(refusal_reasons))
        for reason in missing:
            violations.append(f"missing refusal reason: {reason}")

    if _recursive_find_key(record, "transport_decision") != "REFUSE":
        violations.append("transport_decision must be REFUSE")

    upstream = record.get("upstream_artifacts")
    if not isinstance(upstream, dict):
        violations.append("upstream_artifacts must be present")
    else:
        readiness_summary = upstream.get("readiness_human_decision")
        intent_summary = upstream.get("intent_refusal_audit")
        if not isinstance(readiness_summary, dict):
            violations.append("readiness_human_decision summary missing")
        elif readiness_summary.get("decision") != READINESS_HUMAN_DECISION_DECISION:
            violations.append("readiness_human_decision summary decision mismatch")
        if not isinstance(intent_summary, dict):
            violations.append("intent_refusal_audit summary missing")
        elif intent_summary.get("decision") != INTENT_REFUSAL_AUDIT_DECISION:
            violations.append("intent_refusal_audit summary decision mismatch")

    return VerificationResult(ok=not violations, violations=tuple(violations))


def verify_noop_transport_contract_file(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    record = read_single_jsonl_record(path)
    return verify_noop_transport_contract_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_pass=require_pass,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build")
    build.add_argument("readiness_human_decision_jsonl")
    build.add_argument("intent_refusal_audit_jsonl")
    build.add_argument("output_jsonl")
    build.add_argument("--boundary-static-verifier-jsonl")
    build.add_argument("--allowed-demo-server")

    verify = subparsers.add_parser("verify")
    verify.add_argument("input_jsonl")
    verify.add_argument("--allowed-demo-server")
    verify.add_argument("--require-pass", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "build":
        record = build_noop_transport_contract_from_files(
            readiness_human_decision_jsonl=args.readiness_human_decision_jsonl,
            intent_refusal_audit_jsonl=args.intent_refusal_audit_jsonl,
            output_jsonl=args.output_jsonl,
            boundary_static_verifier_jsonl=args.boundary_static_verifier_jsonl,
            allowed_demo_server=args.allowed_demo_server,
        )
        print(f"Verdict: {record['verdict']}")
        print(f"Violations: {len(record['violations'])}")
        return 0 if record["verdict"] == "PASS" else 1

    result = verify_noop_transport_contract_file(
        args.input_jsonl,
        allowed_demo_server=args.allowed_demo_server,
        require_pass=args.require_pass,
    )
    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if result.ok else 'FAIL'}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())