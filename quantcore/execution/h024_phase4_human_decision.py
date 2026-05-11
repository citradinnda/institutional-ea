from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from quantcore.execution.h024_phase4_review_packet import verify_phase4_review_packet_jsonl

SCHEMA = "h024_phase4_human_decision_v1"
KIND = "PHASE4_HUMAN_DECISION_REVIEW_ONLY"

APPROVED_DECISION = "APPROVE_PHASE4_NO_EXECUTION"
REJECTED_DECISION = "REJECT_PHASE4_NO_EXECUTION"

APPROVED_STATUS = "PHASE4_APPROVED_NO_EXECUTION_AUTHORITY"
REJECTED_STATUS = "PHASE4_REJECTED_NO_EXECUTION_AUTHORITY"

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


class Phase4HumanDecisionError(ValueError):
    """Raised when the H024 Phase 4 human decision artifact is invalid."""


@dataclass(frozen=True)
class Phase4HumanDecisionInputs:
    review_packet_jsonl: Path

    @classmethod
    def standard_demo_reports(cls, reports_dir: str | Path = "reports") -> "Phase4HumanDecisionInputs":
        reports = Path(reports_dir)
        return cls(review_packet_jsonl=reports / "h024_standard_demo_phase4_review_packet.jsonl")


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
            raise Phase4HumanDecisionError(f"{source}:{line_no}: invalid JSONL: {exc}") from exc
        if not isinstance(payload, dict):
            raise Phase4HumanDecisionError(f"{source}:{line_no}: JSONL record must be an object")
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
    if normalized in {"approve", "approved", "approve_phase4", APPROVED_DECISION.lower()}:
        return APPROVED_DECISION
    if normalized in {"reject", "rejected", "reject_phase4", REJECTED_DECISION.lower()}:
        return REJECTED_DECISION
    raise Phase4HumanDecisionError(
        f"unsupported decision {decision!r}; expected approve or reject"
    )


def _load_verified_review_packet(
    review_packet_jsonl: str | Path,
    *,
    allowed_demo_server: str,
) -> dict[str, Any]:
    records, violations = verify_phase4_review_packet_jsonl(
        review_packet_jsonl,
        require_ready=True,
        allowed_demo_server=allowed_demo_server,
    )
    if violations:
        raise Phase4HumanDecisionError(
            "Phase 4 review packet verifier failed: " + "; ".join(violations)
        )
    if len(records) != 1:
        raise Phase4HumanDecisionError(
            f"expected exactly 1 Phase 4 review packet record, found {len(records)}"
        )
    return records[0]


def build_phase4_human_decision(
    inputs: Phase4HumanDecisionInputs,
    *,
    decision: str,
    operator_id: str,
    operator_statement: str,
    allowed_demo_server: str = "Exness-MT5Trial6",
    decided_utc: str | None = None,
) -> dict[str, Any]:
    clean_statement = operator_statement.strip()
    if not clean_statement:
        raise Phase4HumanDecisionError("operator_statement is required")

    clean_operator_id = operator_id.strip()
    if not clean_operator_id:
        raise Phase4HumanDecisionError("operator_id is required")

    normalized_decision = _normalize_decision(decision)
    review_packet = _load_verified_review_packet(
        inputs.review_packet_jsonl,
        allowed_demo_server=allowed_demo_server,
    )

    phase4_approved = normalized_decision == APPROVED_DECISION
    status = APPROVED_STATUS if phase4_approved else REJECTED_STATUS
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
        "source_review_packet_path": str(inputs.review_packet_jsonl),
        "source_review_packet_schema": review_packet.get("schema"),
        "source_review_packet_kind": review_packet.get("kind"),
        "source_review_packet_status": review_packet.get("status"),
        "stable_intent_id": review_packet.get("stable_intent_id"),
        "phase4_approved": phase4_approved,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_implementation_approved": False,
        "execution_adapter_approved": False,
        "execution_approved": False,
        "human_decision_required_for_execution": True,
        "execution_boundary": {
            "mt5_access_approved": False,
            "broker_request_construction_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_adapter_implementation_approved": False,
            "execution_adapter_approved": False,
            "order_send_approved": False,
            "order_check_approved": False,
            "execution_approved": False,
        },
        "next_required_gate": (
            "demo_only_execution_adapter_implementation_approval"
            if phase4_approved
            else "resolve_phase4_rejection_before_any_execution_work"
        ),
        "boundary_statement": (
            "This is a human Phase 4 decision artifact only. It does not approve MT5 access, "
            "broker request construction, demo order placement, live order placement, execution "
            "adapter implementation, OrderSend, OrderCheck, CTrade, or execution."
        ),
    }

    violations = validate_phase4_human_decision_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_approved=phase4_approved,
    )
    if violations:
        raise Phase4HumanDecisionError("built Phase 4 human decision record is invalid: " + "; ".join(violations))
    return record


def validate_phase4_human_decision_record(
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

    if require_approved and record.get("phase4_approved") is not True:
        violations.append("phase4_approved must be true when approval is required")
    if require_rejected and record.get("phase4_approved") is not False:
        violations.append("phase4_approved must be false when rejection is required")

    if record.get("demo_order_placement_approved") is not False:
        violations.append("demo_order_placement_approved must be false")
    if record.get("live_order_placement_approved") is not False:
        violations.append("live_order_placement_approved must be false")
    if record.get("execution_adapter_implementation_approved") is not False:
        violations.append("execution_adapter_implementation_approved must be false")
    if record.get("execution_adapter_approved") is not False:
        violations.append("execution_adapter_approved must be false")
    if record.get("execution_approved") is not False:
        violations.append("execution_approved must be false")

    if not str(record.get("operator_statement", "")).strip():
        violations.append("operator_statement is required")
    if not str(record.get("operator_id", "")).strip():
        violations.append("operator_id is required")

    boundary = record.get("execution_boundary")
    if not isinstance(boundary, dict):
        violations.append("execution_boundary must be an object")
    else:
        for key in (
            "mt5_access_approved",
            "broker_request_construction_approved",
            "demo_order_placement_approved",
            "live_order_placement_approved",
            "execution_adapter_implementation_approved",
            "execution_adapter_approved",
            "order_send_approved",
            "order_check_approved",
            "execution_approved",
        ):
            if boundary.get(key) is not False:
                violations.append(f"execution_boundary.{key} must be false")

    violations.extend(_forbidden_field_violations(record))
    return violations


def verify_phase4_human_decision_jsonl(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_approved: bool = False,
    require_rejected: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    records = read_jsonl_records(path)
    violations: list[str] = []
    if len(records) != 1:
        violations.append(f"expected exactly 1 Phase 4 human decision record, found {len(records)}")
    for index, record in enumerate(records, start=1):
        for violation in validate_phase4_human_decision_record(
            record,
            allowed_demo_server=allowed_demo_server,
            require_approved=require_approved,
            require_rejected=require_rejected,
        ):
            violations.append(f"record {index}: {violation}")
    return records, violations


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an H024 Phase 4 human decision JSONL artifact.")
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--review-packet", default=None)
    parser.add_argument("--output", default="reports/h024_standard_demo_phase4_human_decision.jsonl")
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    parser.add_argument("--decision", required=True, choices=["approve", "reject"])
    parser.add_argument("--operator-id", default="solo_retail_operator")
    parser.add_argument("--operator-statement", required=True)
    return parser


def main_build(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    inputs = Phase4HumanDecisionInputs.standard_demo_reports(args.reports_dir)
    if args.review_packet:
        inputs = Phase4HumanDecisionInputs(review_packet_jsonl=Path(args.review_packet))

    record = build_phase4_human_decision(
        inputs,
        decision=args.decision,
        operator_id=args.operator_id,
        operator_statement=args.operator_statement,
        allowed_demo_server=args.allowed_demo_server,
    )
    write_jsonl_record(args.output, record)

    print(f"Output: {args.output}")
    print("Human decision records: 1")
    print("Violations: 0")
    print(f"Decision: {record['decision']}")
    print(f"Status: {record['status']}")
    print(f"Phase 4 approved: {str(record['phase4_approved']).lower()}")
    print("Demo order placement approved: false")
    print("Live order placement approved: false")
    print("Execution adapter implementation approved: false")
    print("Execution approved: false")
    print("Verdict: PASS")
    return 0


def verify_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify an H024 Phase 4 human decision JSONL artifact.")
    parser.add_argument("jsonl_path")
    parser.add_argument("--allowed-demo-server", default=None)
    parser.add_argument("--require-approved", action="store_true")
    parser.add_argument("--require-rejected", action="store_true")
    return parser


def main_verify(argv: Sequence[str] | None = None) -> int:
    args = verify_arg_parser().parse_args(argv)
    records, violations = verify_phase4_human_decision_jsonl(
        args.jsonl_path,
        allowed_demo_server=args.allowed_demo_server,
        require_approved=args.require_approved,
        require_rejected=args.require_rejected,
    )
    print(f"Input: {args.jsonl_path}")
    print(f"Human decision records: {len(records)}")
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