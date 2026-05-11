"""H024 demo adapter no-op use approval.

This artifact approves only the pure-Python no-op adapter-use path. It does not
approve an execution-capable adapter, broker request construction, MT5 execution,
terminal mutation, demo order placement, live order placement, or execution.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA = "h024_demo_adapter_noop_use_approval_v1"
KIND = "DEMO_ADAPTER_NOOP_USE_APPROVAL"
STATUS = "NOOP_ADAPTER_USE_APPROVED_NO_EXECUTION_AUTHORITY"
DECISION = "APPROVE_NOOP_ADAPTER_USE_ONLY_NO_BROKER_REQUEST_AUTHORITY"

UPSTREAM_SCHEMA = "h024_phase4_demo_adapter_use_readiness_human_decision_v1"
UPSTREAM_KIND = "PHASE4_DEMO_ADAPTER_USE_READINESS_HUMAN_DECISION"
UPSTREAM_DECISION = "APPROVE_ADAPTER_USE_READINESS_REVIEW_NO_EXECUTION"

REQUIRED_TRUE_FLAGS = (
    "phase4_approved",
    "demo_execution_adapter_implementation_approved",
    "execution_adapter_implementation_approved",
    "adapter_readiness_review_approved",
    "adapter_use_readiness_review_approved",
    "noop_adapter_use_approved",
    "noop_adapter_use_only",
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


def _require_upstream(record: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    if record.get("schema") != UPSTREAM_SCHEMA:
        violations.append("adapter_use_readiness_human_decision: schema mismatch")
    if record.get("kind") != UPSTREAM_KIND:
        violations.append("adapter_use_readiness_human_decision: kind mismatch")
    if record.get("decision") != UPSTREAM_DECISION:
        violations.append("adapter_use_readiness_human_decision: decision mismatch")
    if not _verdict_pass(record):
        violations.append("adapter_use_readiness_human_decision: verdict is not PASS")
    if not _violations_zero(record.get("violations")):
        violations.append("adapter_use_readiness_human_decision: violations are non-zero")
    return violations


def build_noop_use_approval_record(
    *,
    adapter_use_readiness_human_decision: dict[str, Any],
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    violations = _require_upstream(adapter_use_readiness_human_decision)

    if allowed_demo_server and not _json_contains_text(
        adapter_use_readiness_human_decision,
        allowed_demo_server,
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
            "adapter_use_readiness_review_approved": True,
            "noop_adapter_use_approved": True,
            "noop_adapter_use_only": True,
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
            "scope": "pure_python_noop_adapter_use_only",
            "may_invoke_noop_transport_contract": True,
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
            "adapter_use_readiness_human_decision": _upstream_summary(
                adapter_use_readiness_human_decision
            ),
        },
    }

    verification = verify_noop_use_approval_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_pass=False,
    )
    if verification.violations:
        record["verdict"] = "FAIL"
        record["violations"] = list(dict.fromkeys([*violations, *verification.violations]))

    return record


def build_noop_use_approval_from_files(
    *,
    adapter_use_readiness_human_decision_jsonl: str | Path,
    output_jsonl: str | Path,
    allowed_demo_server: str | None = None,
) -> dict[str, Any]:
    upstream = read_single_jsonl_record(adapter_use_readiness_human_decision_jsonl)
    record = build_noop_use_approval_record(
        adapter_use_readiness_human_decision=upstream,
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


def verify_noop_use_approval_record(
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

    approved_scope = record.get("approved_scope")
    if not isinstance(approved_scope, dict):
        violations.append("approved_scope block missing")
    elif approved_scope.get("scope") != "pure_python_noop_adapter_use_only":
        violations.append("scope must be pure_python_noop_adapter_use_only")

    upstream = record.get("upstream_artifacts")
    if not isinstance(upstream, dict):
        violations.append("upstream_artifacts block missing")
    else:
        decision = upstream.get("adapter_use_readiness_human_decision")
        if not isinstance(decision, dict) or decision.get("decision") != UPSTREAM_DECISION:
            violations.append("adapter_use_readiness_human_decision upstream summary mismatch")

    return VerificationResult(ok=not violations, violations=tuple(violations))


def verify_noop_use_approval_file(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_pass: bool = False,
) -> VerificationResult:
    return verify_noop_use_approval_record(
        read_single_jsonl_record(path),
        allowed_demo_server=allowed_demo_server,
        require_pass=require_pass,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build")
    build.add_argument("adapter_use_readiness_human_decision_jsonl")
    build.add_argument("output_jsonl")
    build.add_argument("--allowed-demo-server")

    verify = subparsers.add_parser("verify")
    verify.add_argument("input_jsonl")
    verify.add_argument("--allowed-demo-server")
    verify.add_argument("--require-approved", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "build":
        record = build_noop_use_approval_from_files(
            adapter_use_readiness_human_decision_jsonl=(
                args.adapter_use_readiness_human_decision_jsonl
            ),
            output_jsonl=args.output_jsonl,
            allowed_demo_server=args.allowed_demo_server,
        )
        print(f"Output: {args.output_jsonl}")
        print(f"Status: {record['status']}")
        print(f"Decision: {record['decision']}")
        print(f"Violations: {len(record['violations'])}")
        print(f"Verdict: {record['verdict']}")
        return 0 if record["verdict"] == "PASS" else 1

    result = verify_noop_use_approval_file(
        args.input_jsonl,
        allowed_demo_server=args.allowed_demo_server,
        require_pass=args.require_approved,
    )
    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"- {violation}")
    print(f"Verdict: {'PASS' if result.ok else 'FAIL'}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())