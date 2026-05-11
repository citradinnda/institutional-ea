from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from quantcore.execution.h024_demo_adapter_implementation_approval import (
    verify_demo_adapter_implementation_approval_jsonl,
)

SCHEMA = "h024_demo_execution_adapter_skeleton_v1"
KIND = "DEMO_EXECUTION_ADAPTER_SKELETON_FAIL_CLOSED"

STATUS = "DEMO_EXECUTION_ADAPTER_SKELETON_IMPLEMENTED_FAIL_CLOSED"
DECISION = "REFUSE_DISPATCH_NO_ORDER_AUTHORITY"

FORBIDDEN_FIELD_NAMES = {
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


class DemoExecutionAdapterSkeletonError(ValueError):
    """Raised when the H024 demo adapter skeleton artifact is invalid."""


@dataclass(frozen=True)
class DemoExecutionAdapterSkeletonInputs:
    implementation_approval_jsonl: Path

    @classmethod
    def standard_demo_reports(cls, reports_dir: str | Path = "reports") -> "DemoExecutionAdapterSkeletonInputs":
        reports = Path(reports_dir)
        return cls(
            implementation_approval_jsonl=reports / "h024_standard_demo_demo_adapter_implementation_approval.jsonl"
        )


@dataclass(frozen=True)
class DemoExecutionAdapterAuthority:
    phase4_approved: bool
    demo_execution_adapter_implementation_approved: bool
    execution_adapter_implementation_approved: bool
    execution_adapter_approved: bool
    demo_order_placement_approved: bool
    live_order_placement_approved: bool
    execution_approved: bool

    @classmethod
    def from_implementation_approval(cls, payload: dict[str, Any]) -> "DemoExecutionAdapterAuthority":
        return cls(
            phase4_approved=payload.get("phase4_approved") is True,
            demo_execution_adapter_implementation_approved=payload.get(
                "demo_execution_adapter_implementation_approved"
            )
            is True,
            execution_adapter_implementation_approved=payload.get("execution_adapter_implementation_approved")
            is True,
            execution_adapter_approved=payload.get("execution_adapter_approved") is True,
            demo_order_placement_approved=payload.get("demo_order_placement_approved") is True,
            live_order_placement_approved=payload.get("live_order_placement_approved") is True,
            execution_approved=payload.get("execution_approved") is True,
        )


@dataclass(frozen=True)
class DemoExecutionIntentEnvelope:
    strategy_id: str
    adapter_mode: str
    source_authority_path: str
    stable_intent_id: str | None
    normalized_symbol: str | None
    side: str | None
    final_lots: str | None
    intent_source: str


@dataclass(frozen=True)
class FailClosedTransportResult:
    transport_name: str
    dispatch_attempted: bool
    terminal_mutated: bool
    broker_state_mutated: bool
    reason: str


class FailClosedDemoTransport:
    """A no-op transport proving the adapter skeleton refuses to mutate terminal or broker state."""

    name = "fail_closed_noop_demo_transport"

    def dispatch(self, _intent: DemoExecutionIntentEnvelope, refusal_reasons: Sequence[str]) -> FailClosedTransportResult:
        reason = "; ".join(refusal_reasons) if refusal_reasons else "dispatch_disabled_by_design"
        return FailClosedTransportResult(
            transport_name=self.name,
            dispatch_attempted=False,
            terminal_mutated=False,
            broker_state_mutated=False,
            reason=reason,
        )


class FailClosedDemoExecutionAdapter:
    """Pure-Python adapter skeleton. It never imports MT5 and never dispatches."""

    def __init__(self, transport: FailClosedDemoTransport | None = None) -> None:
        self.transport = transport or FailClosedDemoTransport()

    def evaluate(
        self,
        *,
        intent: DemoExecutionIntentEnvelope,
        authority: DemoExecutionAdapterAuthority,
    ) -> dict[str, Any]:
        refusal_reasons = evaluate_refusal_reasons(authority)
        transport_result = self.transport.dispatch(intent, refusal_reasons)

        return {
            "schema": SCHEMA,
            "kind": KIND,
            "status": STATUS,
            "decision": DECISION,
            "created_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "strategy_id": intent.strategy_id,
            "adapter_mode": intent.adapter_mode,
            "source_authority_path": intent.source_authority_path,
            "stable_intent_id": intent.stable_intent_id,
            "intent_summary": asdict(intent),
            "authority": asdict(authority),
            "refusal_reasons": refusal_reasons,
            "transport_result": asdict(transport_result),
            "phase4_approved": authority.phase4_approved,
            "demo_execution_adapter_implementation_approved": authority.demo_execution_adapter_implementation_approved,
            "execution_adapter_implementation_approved": authority.execution_adapter_implementation_approved,
            "execution_adapter_approved": authority.execution_adapter_approved,
            "demo_order_placement_approved": authority.demo_order_placement_approved,
            "live_order_placement_approved": authority.live_order_placement_approved,
            "execution_approved": authority.execution_approved,
            "adapter_boundary": {
                "pure_python_only": True,
                "mt5_imported": False,
                "terminal_mutation_attempted": False,
                "broker_state_mutation_attempted": False,
                "dispatch_attempted": False,
                "demo_order_placement_attempted": False,
                "live_order_placement_attempted": False,
                "execution_attempted": False,
            },
            "boundary_statement": (
                "The demo adapter skeleton is implemented and fail-closed. It refuses dispatch because "
                "execution adapter use, demo order placement, live order placement, and execution remain unapproved."
            ),
        }


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
            raise DemoExecutionAdapterSkeletonError(f"{source}:{line_no}: invalid JSONL: {exc}") from exc
        if not isinstance(payload, dict):
            raise DemoExecutionAdapterSkeletonError(f"{source}:{line_no}: JSONL record must be an object")
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
        if key_path and key_path[-1].lower() in FORBIDDEN_FIELD_NAMES:
            violations.append(f"forbidden execution-like field {'.'.join(key_path)} is present")
    return violations


def _load_verified_implementation_approval(
    implementation_approval_jsonl: str | Path,
    *,
    allowed_demo_server: str,
) -> dict[str, Any]:
    records, violations = verify_demo_adapter_implementation_approval_jsonl(
        implementation_approval_jsonl,
        allowed_demo_server=allowed_demo_server,
        require_approved=True,
    )
    if violations:
        raise DemoExecutionAdapterSkeletonError(
            "demo adapter implementation approval verifier failed: " + "; ".join(violations)
        )
    if len(records) != 1:
        raise DemoExecutionAdapterSkeletonError(
            f"expected exactly 1 implementation approval record, found {len(records)}"
        )
    return records[0]


def evaluate_refusal_reasons(authority: DemoExecutionAdapterAuthority) -> list[str]:
    reasons: list[str] = []

    if not authority.phase4_approved:
        reasons.append("phase4_not_approved")
    if not authority.demo_execution_adapter_implementation_approved:
        reasons.append("demo_adapter_implementation_not_approved")
    if not authority.execution_adapter_implementation_approved:
        reasons.append("execution_adapter_implementation_not_approved")
    if not authority.execution_adapter_approved:
        reasons.append("execution_adapter_use_not_approved")
    if not authority.demo_order_placement_approved:
        reasons.append("demo_order_placement_not_approved")
    if authority.live_order_placement_approved:
        reasons.append("live_order_placement_must_remain_false_for_demo_skeleton")
    if not authority.execution_approved:
        reasons.append("execution_not_approved")

    if not reasons:
        reasons.append("dispatch_disabled_by_fail_closed_skeleton")

    return reasons


def build_demo_execution_adapter_skeleton(
    inputs: DemoExecutionAdapterSkeletonInputs,
    *,
    allowed_demo_server: str = "Exness-MT5Trial6",
    created_utc: str | None = None,
) -> dict[str, Any]:
    approval = _load_verified_implementation_approval(
        inputs.implementation_approval_jsonl,
        allowed_demo_server=allowed_demo_server,
    )
    authority = DemoExecutionAdapterAuthority.from_implementation_approval(approval)
    intent = DemoExecutionIntentEnvelope(
        strategy_id="H024",
        adapter_mode="standard_demo_fail_closed_skeleton",
        source_authority_path=str(inputs.implementation_approval_jsonl),
        stable_intent_id=approval.get("stable_intent_id"),
        normalized_symbol=None,
        side=None,
        final_lots=None,
        intent_source="authority_only_no_order_payload",
    )

    record = FailClosedDemoExecutionAdapter().evaluate(intent=intent, authority=authority)
    if created_utc is not None:
        record["created_utc"] = created_utc

    violations = validate_demo_execution_adapter_skeleton_record(
        record,
        allowed_demo_server=allowed_demo_server,
        require_refusal=True,
    )
    if violations:
        raise DemoExecutionAdapterSkeletonError(
            "built demo execution adapter skeleton record is invalid: " + "; ".join(violations)
        )
    return record


def validate_demo_execution_adapter_skeleton_record(
    record: dict[str, Any],
    *,
    allowed_demo_server: str | None = None,
    require_refusal: bool = False,
) -> list[str]:
    violations: list[str] = []

    if record.get("schema") != SCHEMA:
        violations.append(f"expected schema {SCHEMA!r}, found {record.get('schema')!r}")
    if record.get("kind") != KIND:
        violations.append(f"expected kind {KIND!r}, found {record.get('kind')!r}")
    if record.get("status") != STATUS:
        violations.append(f"expected status {STATUS!r}, found {record.get('status')!r}")
    if require_refusal and record.get("decision") != DECISION:
        violations.append(f"expected decision {DECISION!r}, found {record.get('decision')!r}")

    if record.get("phase4_approved") is not True:
        violations.append("phase4_approved must be true")
    if record.get("demo_execution_adapter_implementation_approved") is not True:
        violations.append("demo_execution_adapter_implementation_approved must be true")
    if record.get("execution_adapter_implementation_approved") is not True:
        violations.append("execution_adapter_implementation_approved must be true")
    if record.get("execution_adapter_approved") is not False:
        violations.append("execution_adapter_approved must be false")
    if record.get("demo_order_placement_approved") is not False:
        violations.append("demo_order_placement_approved must be false")
    if record.get("live_order_placement_approved") is not False:
        violations.append("live_order_placement_approved must be false")
    if record.get("execution_approved") is not False:
        violations.append("execution_approved must be false")

    reasons = record.get("refusal_reasons")
    if not isinstance(reasons, list) or not reasons:
        violations.append("refusal_reasons must be a non-empty list")
    else:
        for required_reason in (
            "execution_adapter_use_not_approved",
            "demo_order_placement_not_approved",
            "execution_not_approved",
        ):
            if required_reason not in reasons:
                violations.append(f"refusal_reasons must include {required_reason!r}")

    transport_result = record.get("transport_result")
    if not isinstance(transport_result, dict):
        violations.append("transport_result must be an object")
    else:
        for key in ("dispatch_attempted", "terminal_mutated", "broker_state_mutated"):
            if transport_result.get(key) is not False:
                violations.append(f"transport_result.{key} must be false")

    boundary = record.get("adapter_boundary")
    if not isinstance(boundary, dict):
        violations.append("adapter_boundary must be an object")
    else:
        if boundary.get("pure_python_only") is not True:
            violations.append("adapter_boundary.pure_python_only must be true")
        for key in (
            "mt5_imported",
            "terminal_mutation_attempted",
            "broker_state_mutation_attempted",
            "dispatch_attempted",
            "demo_order_placement_attempted",
            "live_order_placement_attempted",
            "execution_attempted",
        ):
            if boundary.get(key) is not False:
                violations.append(f"adapter_boundary.{key} must be false")

    if allowed_demo_server is not None:
        source_path = str(record.get("source_authority_path", ""))
        if not source_path:
            violations.append("source_authority_path is required")

    violations.extend(_forbidden_field_violations(record))
    return violations


def verify_demo_execution_adapter_skeleton_jsonl(
    path: str | Path,
    *,
    allowed_demo_server: str | None = None,
    require_refusal: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    records = read_jsonl_records(path)
    violations: list[str] = []

    if len(records) != 1:
        violations.append(f"expected exactly 1 demo execution adapter skeleton record, found {len(records)}")

    for index, record in enumerate(records, start=1):
        for violation in validate_demo_execution_adapter_skeleton_record(
            record,
            allowed_demo_server=allowed_demo_server,
            require_refusal=require_refusal,
        ):
            violations.append(f"record {index}: {violation}")

    return records, violations


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an H024 fail-closed demo execution adapter skeleton JSONL artifact.")
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--implementation-approval", default=None)
    parser.add_argument("--output", default="reports/h024_standard_demo_demo_execution_adapter_skeleton.jsonl")
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    return parser


def main_build(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    inputs = DemoExecutionAdapterSkeletonInputs.standard_demo_reports(args.reports_dir)
    if args.implementation_approval:
        inputs = DemoExecutionAdapterSkeletonInputs(implementation_approval_jsonl=Path(args.implementation_approval))

    record = build_demo_execution_adapter_skeleton(inputs, allowed_demo_server=args.allowed_demo_server)
    write_jsonl_record(args.output, record)

    print(f"Output: {args.output}")
    print("Demo execution adapter skeleton records: 1")
    print("Violations: 0")
    print(f"Status: {record['status']}")
    print(f"Decision: {record['decision']}")
    print(f"Refusal reasons: {len(record['refusal_reasons'])}")
    print("Phase 4 approved: true")
    print("Demo execution adapter implementation approved: true")
    print("Execution adapter approved: false")
    print("Demo order placement approved: false")
    print("Live order placement approved: false")
    print("Execution approved: false")
    print("Dispatch attempted: false")
    print("Terminal mutated: false")
    print("Broker state mutated: false")
    print("Verdict: PASS")
    return 0


def verify_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify an H024 fail-closed demo execution adapter skeleton JSONL artifact.")
    parser.add_argument("jsonl_path")
    parser.add_argument("--allowed-demo-server", default=None)
    parser.add_argument("--require-refusal", action="store_true")
    return parser


def main_verify(argv: Sequence[str] | None = None) -> int:
    args = verify_arg_parser().parse_args(argv)
    records, violations = verify_demo_execution_adapter_skeleton_jsonl(
        args.jsonl_path,
        allowed_demo_server=args.allowed_demo_server,
        require_refusal=args.require_refusal,
    )

    print(f"Input: {args.jsonl_path}")
    print(f"Demo execution adapter skeleton records: {len(records)}")
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