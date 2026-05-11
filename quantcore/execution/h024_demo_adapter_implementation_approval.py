from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from quantcore.execution.h024_phase4_human_decision import verify_phase4_human_decision_jsonl

SCHEMA = "h024_demo_adapter_implementation_approval_v1"
KIND = "DEMO_ADAPTER_IMPLEMENTATION_APPROVAL_REVIEW_ONLY"

APPROVED_DECISION = "APPROVE_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT"
REJECTED_DECISION = "REJECT_DEMO_ADAPTER_IMPLEMENTATION_NO_ORDER_PLACEMENT"

APPROVED_STATUS = "DEMO_ADAPTER_IMPLEMENTATION_APPROVED_NO_ORDER_AUTHORITY"
REJECTED_STATUS = "DEMO_ADAPTER_IMPLEMENTATION_REJECTED_NO_ORDER_AUTHORITY"

FORBIDDEN_EXECUTION_FIELD_NAMES = {
    "ordersend",
    "order_send",
    "ordersendasync",
    "order_send_async",
    "ordercheck",
    "order_check",
    "ctrade",
    "c_trade",
    "mqltraderequest",
    "mql_trade_request",
    "mqltraderesult",
    "mql_trade_result",
    "mt5_request",
    "broker_request",
    "trade_request",
    "order_request",
    "position_open",
    "position_close",
    "position_modify",
    "pending_order_request",
}


class DemoAdapterImplementationApprovalError(ValueError):
    """Raised when the H024 demo adapter implementation approval artifact is invalid."""


@dataclass(frozen=True)
class DemoAdapterImplementationApprovalInputs:
    phase4_human_decision_jsonl: Path

    @classmethod
    def standard_demo_reports(cls, reports_dir: str | Path = "reports") -> "DemoAdapterImplementationApprovalInputs":
        reports = Path(reports_dir)
        return cls(phase4_human_decision_jsonl=reports / "h024_standard_demo_phase4_human_decision.jsonl")


def read_jsonl_records(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    records: list[dict[str, Any]] = []
    for line_no, raw_line in enumerate(source.read_text(encoding="utf-8-sig").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DemoAdapterImplementationApprovalError(f"{source}:{line_no}: invalid JSONL: {exc}") from exc
        if not isinstance(payload, dict):
            raise DemoAdapterImplementationApprovalError(f"{source}:{line_no}: JSONL record must be an object")
        records.append(payload)
    return records


def write_jsonl_record(path: str | Path, record: dict[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def _walk(payload: Any, prefix: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_path = (*prefix, str(key))
            yield key_path, value
            yield from _walk(value, key_path)
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            yield from _walk(value, (*prefix, str(index)))


def _forbidden_field_violations(payload: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for key_path, _value in _walk(payload):
        if key_path and key_path[-1].lower() in FORBIDDEN_EXECUTION_FIELD_NAMES:
            violations.append(f"forbidden execution-like field {'.'.join(key_path)} is present")
    return violations


def _normalize_decision(decision: str) -> str:
    normalized = decision.strip().lower()
    if normalized in {"approve", "approved", "approve_demo_adapter", APPROVED_DECISION.lower()}:
        return APPROVED_DECISION
    if normalized in {"reject", "rejected", "reject_demo_adapter", REJECTED_DECISION.lower()}:
        return REJECTED_DECISION
    raise DemoAdapterImplementationApprovalError(
        f"unsupported decision {decision!r}; expected approve or reject"
    )


def _load_verified_phase4_decision(
    phase4_human_decision_jsonl: str | Path,
    *,
    allowed_demo_server: str,
) -> dict[str, Any]:
    records, violations = verify_phase4_human_decision_jsonl(
        phase4_human_decision_jsonl,
        allowed_demo_server=allowed_demo_server,
        require_approved=True,
    )
    if violations:
        raise DemoAdapterImplementationApprovalError(
            "Phase 4 human decision verifier failed: " + "; ".join(violations)
        )
    if len(records) != 1:
        raise DemoAdapterImplementationApprovalError(
            f"expected exactly 1 Phase 4 human decision record, found {len(records)}"
        )
    return records[0]


def build_demo_adapter_implementation_approval(
    inputs: DemoAdapterImplementationApprovalInputs,
    *,
    decision: str,
    operator_id: str,
    operator_statement: str,
    allowed_demo_server: str = "Exness-MT5Trial6",
    decided_utc: str | None = None,
) -> dict[str, Any]:
    clean_operator_id = operator_id.strip()
    if not clean_operator_id:
        raise DemoAdapterImplementationApprovalError("operator_id is required")

    clean_statement = operator_statement.strip()
    if not clean_statement:
        raise DemoAdapterImplementationApprovalError("operator_statement is required")

    normalized_decision = _normalize_decision(decision)
    phase4_decision = _load_verified_phase4_decision(
        inputs.phase4_human_decision_jsonl,
        allowed_demo_server=allowed_demo_server,
    )

    implementation_approved = normalized_decision == APPROVED_DECISION
    status = APPROVED_STATUS if implementation_approved else REJECTED_STATUS
    decided = decided_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    record = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": status,
        "decision": normalized_decision,
        "decided_utc": decided,
        "operator_id": clean_operator_id,
        "operator_statement": clean_statement,
        "strategy_id": "H024",
        "environment": "standard_demo_review_only",
        "allowed_demo_server": allowed_demo_server,
        "source_phase4_human_decision_path": str(inputs.phase4_human_decision_jsonl),
        "source_phase4_human_decision_schema": phase4_decision.get("schema"),
        "source_phase4_human_decision_kind": phase4_decision.get("kind"),
        "source_phase4_human_decision_status": phase4_decision.get("status"),
        "phase4_approved": True,
        "demo_execution_adapter_implementation_approved": implementation_approved,
        "execution_adapter_implementation_approved": implementation_approved,
        "execution_adapter_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "implementation_scope": {
            "demo_only": True,
            "pure_python_contracts_allowed": True,
            "fail_closed_adapter_skeleton_allowed": implementation_approved,
            "mt5_import_allowed": False,
            "terminal_mutation_allowed": False,
            "broker_request_construction_allowed": False,
            "order_placement_allowed": False,
            "live_trading_allowed": False,
            "execution_allowed": False,
        },
        "execution_boundary": {
            "mt5_access_approved": False,
            "terminal_mutation_approved": False,
            "broker_request_construction_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_adapter_approved": False,
            "order_send_approved": False,
            "order_check_approved": False,
            "execution_approved": False,
        },
        "next_required_gate": (
            "demo_only_execution_adapter_skeleton_contract"
            if implementation_approved
            else "resolve_demo_adapter_implementation_rejection"
        ),
        "boundary_statement": (
            "This artifact approves implementation work for a demo-only, fail-closed H024 execution adapter "
            "skeleton/contract only. It does not approve MT5 imports, terminal mutation, broker request "
            "construction, demo order placement, live order placement, OrderSend, OrderCheck, CTrade, or execution."
        ),
    }

    violations = validate_demo_adapter_implementation_approval_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_approved=implementation_approved,
    )
    if violations:
        raise DemoAdapterImplementationApprovalError(
            "built demo adapter implementation approval record is invalid: " + "; ".join(violations)
        )
    return record


def validate_demo_adapter_implementation_approval_record(
    record: dict[str, Any],
    *,
    allowed_demo_server: str | None = None,
    require_approved: bool = False,
    require_rejected: bool = False,
) -> list[str]:
    violations: list[str] = []

    if record.get("schema") != SCHEMA:
        violations.append(f"expected schema {SCHEMA!r}, found {record.get('schema')!r}")
    if record.get("kind") != KIND:
        violations.append(f"expected kind {KIND!r}, found {record.get('kind')!r}")

    decision = record.get("decision")
    status = record.get("status")

    if decision not in {APPROVED_DECISION, REJECTED_DECISION}:
        violations.append(f"unexpected decision {decision!r}")
    if decision == APPROVED_DECISION and status != APPROVED_STATUS:
        violations.append(f"approved decision must use status {APPROVED_STATUS!r}")
    if decision == REJECTED_DECISION and status != REJECTED_STATUS:
        violations.append(f"rejected decision must use status {REJECTED_STATUS!r}")

    if allowed_demo_server and record.get("allowed_demo_server") != allowed_demo_server:
        violations.append(
            f"expected allowed_demo_server {allowed_demo_server!r}, found {record.get('allowed_demo_server')!r}"
        )

    if record.get("phase4_approved") is not True:
        violations.append("phase4_approved must be true")

    if require_approved:
        if record.get("demo_execution_adapter_implementation_approved") is not True:
            violations.append("demo_execution_adapter_implementation_approved must be true")
        if record.get("execution_adapter_implementation_approved") is not True:
            violations.append("execution_adapter_implementation_approved must be true")

    if require_rejected:
        if record.get("demo_execution_adapter_implementation_approved") is not False:
            violations.append("demo_execution_adapter_implementation_approved must be false when rejected")
        if record.get("execution_adapter_implementation_approved") is not False:
            violations.append("execution_adapter_implementation_approved must be false when rejected")

    if record.get("execution_adapter_approved") is not False:
        violations.append("execution_adapter_approved must be false")
    if record.get("demo_order_placement_approved") is not False:
        violations.append("demo_order_placement_approved must be false")
    if record.get("live_order_placement_approved") is not False:
        violations.append("live_order_placement_approved must be false")
    if record.get("execution_approved") is not False:
        violations.append("execution_approved must be false")

    if not str(record.get("operator_statement", "")).strip():
        violations.append("operator_statement is required")
    if not str(record.get("operator_id", "")).strip():
        violations.append("operator_id is required")

    scope = record.get("implementation_scope")
    if not isinstance(scope, dict):
        violations.append("implementation_scope must be an object")
    else:
        if scope.get("demo_only") is not True:
            violations.append("implementation_scope.demo_only must be true")
        for key in (
            "mt5_import_allowed",
            "terminal_mutation_allowed",
            "broker_request_construction_allowed",
            "order_placement_allowed",
            "live_trading_allowed",
            "execution_allowed",
        ):
            if scope.get(key) is not False:
                violations.append(f"implementation_scope.{key} must be false")

    boundary = record.get("execution_boundary")
    if not isinstance(boundary, dict):
        violations.append("execution_boundary must be an object")
    else:
        for key in (
            "mt5_access_approved",
            "terminal_mutation_approved",
            "broker_request_construction_approved",
            "demo_order_placement_approved",
            "live_order_placement_approved",
            "execution_adapter_approved",
            "order_send_approved",
            "order_check_approved",
            "execution_approved",
        ):
            if boundary.get(key) is not False:
                violations.append(f"execution_boundary.{key} must be false")

    violations.extend(_forbidden_field_violations(record))
    return violations


def verify_demo_adapter_implementation_approval_jsonl(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_approved: bool = False,
    require_rejected: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    records = read_jsonl_records(path)
    violations: list[str] = []

    if len(records) != 1:
        violations.append(f"expected exactly 1 demo adapter implementation approval record, found {len(records)}")

    for index, record in enumerate(records, start=1):
        for violation in validate_demo_adapter_implementation_approval_record(
            record,
            allowed_demo_server=allowed_demo_server,
            require_approved=require_approved,
            require_rejected=require_rejected,
        ):
            violations.append(f"record {index}: {violation}")

    return records, violations


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an H024 demo adapter implementation approval JSONL artifact.")
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--phase4-human-decision", default=None)
    parser.add_argument("--output", default="reports/h024_standard_demo_demo_adapter_implementation_approval.jsonl")
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    parser.add_argument("--decision", required=True, choices=["approve", "reject"])
    parser.add_argument("--operator-id", default="solo_retail_operator")
    parser.add_argument("--operator-statement", required=True)
    return parser


def main_build(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    inputs = DemoAdapterImplementationApprovalInputs.standard_demo_reports(args.reports_dir)
    if args.phase4_human_decision:
        inputs = DemoAdapterImplementationApprovalInputs(phase4_human_decision_jsonl=Path(args.phase4_human_decision))

    record = build_demo_adapter_implementation_approval(
        inputs,
        decision=args.decision,
        operator_id=args.operator_id,
        operator_statement=args.operator_statement,
        allowed_demo_server=args.allowed_demo_server,
    )
    write_jsonl_record(args.output, record)

    print(f"Output: {args.output}")
    print("Demo adapter implementation approval records: 1")
    print("Violations: 0")
    print(f"Decision: {record['decision']}")
    print(f"Status: {record['status']}")
    print(f"Phase 4 approved: {str(record['phase4_approved']).lower()}")
    print(f"Demo execution adapter implementation approved: {str(record['demo_execution_adapter_implementation_approved']).lower()}")
    print(f"Execution adapter implementation approved: {str(record['execution_adapter_implementation_approved']).lower()}")
    print("Execution adapter approved: false")
    print("Demo order placement approved: false")
    print("Live order placement approved: false")
    print("Execution approved: false")
    print("Verdict: PASS")
    return 0


def verify_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify an H024 demo adapter implementation approval JSONL artifact.")
    parser.add_argument("jsonl_path")
    parser.add_argument("--allowed-demo-server", default=None)
    parser.add_argument("--require-approved", action="store_true")
    parser.add_argument("--require-rejected", action="store_true")
    return parser


def main_verify(argv: Sequence[str] | None = None) -> int:
    args = verify_arg_parser().parse_args(argv)
    records, violations = verify_demo_adapter_implementation_approval_jsonl(
        args.jsonl_path,
        allowed_demo_server=args.allowed_demo_server,
        require_approved=args.require_approved,
        require_rejected=args.require_rejected,
    )
    print(f"Input: {args.jsonl_path}")
    print(f"Demo adapter implementation approval records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    if violations:
        print("Verdict: FAIL")
        return 1
    print("Verdict: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_build())