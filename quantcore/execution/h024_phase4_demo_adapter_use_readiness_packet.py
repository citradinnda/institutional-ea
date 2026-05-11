"""H024 Phase 4 demo adapter-use readiness packet.

This is a review-only governance packet. It aggregates the pure-Python no-op
transport contract and adapter boundary proof, then requests human review for
adapter-use readiness while preserving all no-execution boundaries.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA = "h024_phase4_demo_adapter_use_readiness_packet_v1"
KIND = "PHASE4_DEMO_ADAPTER_USE_READINESS_PACKET_REVIEW_ONLY"
STATUS = "READY_FOR_HUMAN_ADAPTER_USE_REVIEW_NO_EXECUTION"
DECISION = "REQUEST_HUMAN_ADAPTER_USE_REVIEW_NO_EXECUTION_AUTHORITY"

NOOP_TRANSPORT_SCHEMA = "h024_demo_adapter_noop_transport_contract_v1"
NOOP_TRANSPORT_KIND = "DEMO_ADAPTER_NOOP_TRANSPORT_CONTRACT"
NOOP_TRANSPORT_DECISION = "REFUSE_TRANSPORT_NO_ADAPTER_USE_AUTHORITY"

BOUNDARY_SCHEMA = "h024_demo_adapter_boundary_static_verifier_v1"
BOUNDARY_KIND = "DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER"

REQUIRED_TRUE_FLAGS = (
    "phase4_approved",
    "demo_execution_adapter_implementation_approved",
    "execution_adapter_implementation_approved",
    "adapter_readiness_review_approved",
    "noop_transport_contract_passed",
    "adapter_boundary_static_verifier_passed",
    "adapter_use_readiness_packet_defined",
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


def _json_contains_text(record: dict[str, Any], needle: str) -> bool:
    return needle in json.dumps(record, sort_keys=True)


def _violations_zero(value: Any) -> bool:
    return value in (0, [], None)


def _verdict_pass(record: dict[str, Any]) -> bool:
    return str(record.get("verdict", "PASS")).upper() == "PASS"


def _upstream_summary(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": record.get("schema"),
        "kind": record.get("kind"),
        "status": record.get("status"),
        "decision": record.get("decision"),
        "verdict": record.get("verdict", "PASS"),
        "violations": record.get("violations", 0),
    }


def _require_upstream(
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
    if not _verdict_pass(record):
        violations.append(f"{label}: verdict is not PASS")
    if not _violations_zero(record.get("violations")):
        violations.append(f"{label}: violations are non-zero")
    return violations


def build_adapter_use_readiness_packet_record(
    *,
    noop_transport_contract: dict[str, Any],
    boundary_static_verifier: dict[str, Any],
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    violations: list[str] = []

    violations.extend(
        _require_upstream(
            noop_transport_contract,
            schema=NOOP_TRANSPORT_SCHEMA,
            kind=NOOP_TRANSPORT_KIND,
            decision=NOOP_TRANSPORT_DECISION,
            label="noop_transport_contract",
        )
    )
    violations.extend(
        _require_upstream(
            boundary_static_verifier,
            schema=BOUNDARY_SCHEMA,
            kind=BOUNDARY_KIND,
            decision=None,
            label="boundary_static_verifier",
        )
    )

    if allowed_demo_server and not _json_contains_text(noop_transport_contract, allowed_demo_server):
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
        "readiness": {
            "noop_transport_contract_passed": True,
            "adapter_boundary_static_verifier_passed": True,
            "adapter_use_readiness_packet_defined": True,
            "requested_human_review": "adapter_use_readiness_only",
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
            "noop_transport_contract": _upstream_summary(noop_transport_contract),
            "boundary_static_verifier": _upstream_summary(boundary_static_verifier),
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

    verification = verify_adapter_use_readiness_packet_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_pass=False,
    )
    if verification.violations:
        record["verdict"] = "FAIL"
        record["violations"] = list(dict.fromkeys([*violations, *verification.violations]))

    return record


def build_adapter_use_readiness_packet_from_files(
    *,
    noop_transport_contract_jsonl: str | Path,
    boundary_static_verifier_jsonl: str | Path,
    output_jsonl: str | Path,
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    noop_transport_contract = read_single_jsonl_record(noop_transport_contract_jsonl)
    boundary_static_verifier = read_single_jsonl_record(boundary_static_verifier_jsonl)

    record = build_adapter_use_readiness_packet_record(
        noop_transport_contract=noop_transport_contract,
        boundary_static_verifier=boundary_static_verifier,
        allowed_demo_server=allowed_demo_server,
    )
    write_single_jsonl_record(output_jsonl, record)
    return record


def _nested_bool(record: dict[str, Any], key: str) -> bool | None:
    for value in record.values():
        if isinstance(value, dict):
            if key in value and isinstance(value[key], bool):
                return value[key]
            found = _nested_bool(value, key)
            if found is not None:
                return found
    return None


def verify_adapter_use_readiness_packet_record(
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

    if not _violations_zero(record.get("violations")):
        violations.append("record violations are non-zero")

    if allowed_demo_server and not _json_contains_text(record, allowed_demo_server):
        violations.append(f"allowed demo server not observed: {allowed_demo_server}")

    for key in REQUIRED_TRUE_FLAGS:
        if _nested_bool(record, key) is not True:
            violations.append(f"{key} must be true")

    for key in REQUIRED_FALSE_FLAGS:
        if _nested_bool(record, key) is not False:
            violations.append(f"{key} must be false")

    readiness = record.get("readiness")
    if not isinstance(readiness, dict):
        violations.append("readiness block missing")
    elif readiness.get("requested_human_review") != "adapter_use_readiness_only":
        violations.append("requested_human_review must be adapter_use_readiness_only")

    upstream = record.get("upstream_artifacts")
    if not isinstance(upstream, dict):
        violations.append("upstream_artifacts block missing")
    else:
        noop = upstream.get("noop_transport_contract")
        boundary = upstream.get("boundary_static_verifier")
        if not isinstance(noop, dict) or noop.get("decision") != NOOP_TRANSPORT_DECISION:
            violations.append("noop transport upstream summary mismatch")
        if not isinstance(boundary, dict) or boundary.get("kind") != BOUNDARY_KIND:
            violations.append("boundary upstream summary mismatch")

    return VerificationResult(ok=not violations, violations=tuple(violations))


def verify_adapter_use_readiness_packet_file(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    return verify_adapter_use_readiness_packet_record(
        read_single_jsonl_record(path),
        allowed_demo_server=allowed_demo_server,
        require_pass=require_pass,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build")
    build.add_argument("noop_transport_contract_jsonl")
    build.add_argument("boundary_static_verifier_jsonl")
    build.add_argument("output_jsonl")
    build.add_argument("--allowed-demo-server")

    verify = subparsers.add_parser("verify")
    verify.add_argument("input_jsonl")
    verify.add_argument("--allowed-demo-server")
    verify.add_argument("--require-pass", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "build":
        record = build_adapter_use_readiness_packet_from_files(
            noop_transport_contract_jsonl=args.noop_transport_contract_jsonl,
            boundary_static_verifier_jsonl=args.boundary_static_verifier_jsonl,
            output_jsonl=args.output_jsonl,
            allowed_demo_server=args.allowed_demo_server,
        )
        print(f"Output: {args.output_jsonl}")
        print(f"Status: {record['status']}")
        print(f"Decision: {record['decision']}")
        print(f"Violations: {len(record['violations'])}")
        print(f"Verdict: {record['verdict']}")
        return 0 if record["verdict"] == "PASS" else 1

    result = verify_adapter_use_readiness_packet_file(
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